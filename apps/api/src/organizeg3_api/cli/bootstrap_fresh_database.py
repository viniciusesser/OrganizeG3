"""Initialize a fresh OrganizeG3 database and create its first administrator.

Place this file at:
apps/api/src/organizeg3_api/cli/bootstrap_fresh_database.py

Run it from the repository root after configuring DATABASE_URL in .env:

    python -m organizeg3_api.cli.bootstrap_fresh_database \
        --auth-user-id <SUPABASE_AUTH_USER_UUID> \
        --email <EMAIL> \
        --display-name <NAME> \
        --tenant-name <TENANT>

The command is intentionally conservative. It initializes only an empty public
schema, or reuses a schema that already contains every current ORM table and is
stamped at the current Alembic head. A partial or differently versioned schema
is rejected without modification.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import sys
import uuid

from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import func, inspect, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from organizeg3_api.config import get_settings
from organizeg3_api.domain.identity.enums import MembershipStatus
from organizeg3_api.infrastructure.database.base import Base, utc_now
from organizeg3_api.infrastructure.database.session import (
    dispose_database_manager,
    get_database_manager,
)
from organizeg3_api.infrastructure.persistence import models as persistence_models
from organizeg3_api.infrastructure.persistence.authorization import (
    sync_permission_catalog,
)
from organizeg3_api.infrastructure.persistence.models import (
    AccessProfileModel,
    AccessProfilePermissionModel,
    PermissionModel,
    TenantMembershipModel,
    TenantMembershipProfileModel,
    TenantRecordModel,
    UserModel,
)

del persistence_models

ADMIN_PROFILE_CODE = "ADMIN"
ADMIN_PROFILE_NAME = "Administrador"
ADMIN_PROFILE_DESCRIPTION = "Acesso administrativo completo ao tenant."
ALEMBIC_VERSION_TABLE = "alembic_version"


def _write_stdout(message: str) -> None:
    """Write one informational line to the command standard output."""

    sys.stdout.write(f"{message}\n")


def _write_stderr(message: str) -> None:
    """Write one error line to the command standard error."""

    sys.stderr.write(f"{message}\n")


class BootstrapError(RuntimeError):
    """Raised when safely initializing the database is not possible."""


@dataclass(frozen=True, slots=True)
class BootstrapArguments:
    """Validated input for the first administrator bootstrap."""

    auth_user_id: uuid.UUID
    email: str
    display_name: str
    tenant_name: str


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    """Summary of the records ensured by the bootstrap."""

    tenant_id: uuid.UUID
    user_id: uuid.UUID
    membership_id: uuid.UUID
    profile_id: uuid.UUID
    permission_count: int
    schema_created: bool
    alembic_revision: str


def _project_root() -> Path:
    """Return the repository root from this module's expected location."""

    root = Path(__file__).resolve().parents[5]
    alembic_ini = root / "alembic.ini"

    if not alembic_ini.is_file():
        raise BootstrapError(
            "alembic.ini não foi encontrado. Coloque este arquivo no caminho "
            "apps/api/src/organizeg3_api/cli/bootstrap_fresh_database.py."
        )

    return root


def _alembic_configuration(project_root: Path) -> Config:
    configuration = Config(str(project_root / "alembic.ini"))
    configuration.set_main_option(
        "script_location",
        str(project_root / "database" / "migrations"),
    )
    return configuration


def _current_revision(engine: Engine) -> str | None:
    with engine.connect() as connection:
        return MigrationContext.configure(connection).get_current_revision()


def _head_revision(configuration: Config) -> str:
    heads = ScriptDirectory.from_config(configuration).get_heads()

    if len(heads) != 1:
        raise BootstrapError(
            "A árvore de migrations deve possuir exatamente um head antes do "
            "bootstrap."
        )

    return heads[0]


def _initialize_schema(
    engine: Engine,
    configuration: Config,
) -> tuple[bool, str]:
    """Create the current mapped schema only when public is safely empty."""

    inspector = inspect(engine)
    public_tables = set(inspector.get_table_names(schema="public"))
    managed_tables = set(Base.metadata.tables)
    current_revision = _current_revision(engine)
    head_revision = _head_revision(configuration)

    present_managed = public_tables & managed_tables
    unexpected_tables = public_tables - managed_tables - {ALEMBIC_VERSION_TABLE}

    if current_revision is not None:
        if current_revision != head_revision:
            raise BootstrapError(
                "O banco já possui uma revisão Alembic diferente do head atual. "
                "Execute o fluxo normal de migrations em vez deste bootstrap."
            )

        missing_tables = managed_tables - public_tables
        if missing_tables:
            missing = ", ".join(sorted(missing_tables))
            raise BootstrapError(
                "O banco está marcado no head, mas faltam tabelas mapeadas: "
                f"{missing}. Nenhuma alteração foi realizada."
            )

        return False, head_revision

    if unexpected_tables:
        unexpected = ", ".join(sorted(unexpected_tables))
        raise BootstrapError(
            "O schema public contém tabelas não reconhecidas: "
            f"{unexpected}. Nenhuma alteração foi realizada."
        )

    if present_managed:
        present = ", ".join(sorted(present_managed))
        raise BootstrapError(
            "Foi encontrado um schema parcial sem controle Alembic. Tabelas "
            f"presentes: {present}. Nenhuma alteração foi realizada."
        )

    Base.metadata.create_all(bind=engine, checkfirst=True)

    try:
        command.stamp(configuration, head_revision)
    except Exception:
        Base.metadata.drop_all(bind=engine, checkfirst=True)
        raise

    return True, head_revision


def _stable_uuid(namespace: uuid.UUID, value: str) -> uuid.UUID:
    return uuid.uuid5(namespace, value.strip().casefold())


def _ensure_tenant(
    session: Session,
    tenant_name: str,
) -> TenantRecordModel:
    tenant_id = _stable_uuid(
        uuid.NAMESPACE_URL,
        f"organizeg3:tenant:{tenant_name}",
    )
    tenant = session.get(TenantRecordModel, tenant_id)

    if tenant is None:
        tenant = TenantRecordModel(
            id=tenant_id,
            name=tenant_name,
            status="ACTIVE",
            is_active=True,
        )
        session.add(tenant)
        session.flush()
        return tenant

    tenant.name = tenant_name
    tenant.status = "ACTIVE"
    tenant.is_active = True
    return tenant


def _ensure_user(
    session: Session,
    arguments: BootstrapArguments,
) -> UserModel:
    user_by_auth_id = session.scalar(
        select(UserModel).where(
            UserModel.auth_user_id == arguments.auth_user_id,
        )
    )
    user_by_email = session.scalar(
        select(UserModel).where(
            func.lower(func.trim(UserModel.email)) == arguments.email,
        )
    )

    if (
        user_by_auth_id is not None
        and user_by_email is not None
        and user_by_auth_id.id != user_by_email.id
    ):
        raise BootstrapError(
            "O UUID do Supabase Auth e o e-mail já pertencem a usuários locais "
            "diferentes. Nenhuma alteração foi confirmada."
        )

    user = user_by_auth_id or user_by_email

    if user is None:
        user = UserModel(
            id=_stable_uuid(
                uuid.NAMESPACE_URL,
                f"organizeg3:user:{arguments.auth_user_id}",
            ),
            auth_user_id=arguments.auth_user_id,
            email=arguments.email,
            display_name=arguments.display_name,
            is_active=True,
        )
        session.add(user)
        session.flush()
        return user

    if user.auth_user_id != arguments.auth_user_id:
        raise BootstrapError(
            "O e-mail informado já está associado a outro UUID do Supabase Auth."
        )

    user.email = arguments.email
    user.display_name = arguments.display_name
    user.is_active = True
    user.deleted_at = None
    return user


def _ensure_membership(
    session: Session,
    tenant: TenantRecordModel,
    user: UserModel,
) -> TenantMembershipModel:
    membership = session.scalar(
        select(TenantMembershipModel).where(
            TenantMembershipModel.tenant_id == tenant.id,
            TenantMembershipModel.user_id == user.id,
        )
    )

    if membership is None:
        membership = TenantMembershipModel(
            id=_stable_uuid(
                tenant.id,
                f"membership:{user.id}",
            ),
            tenant_id=tenant.id,
            user_id=user.id,
            status=MembershipStatus.ACTIVE.value,
            joined_at=utc_now(),
        )
        session.add(membership)
        session.flush()
        return membership

    membership.status = MembershipStatus.ACTIVE.value
    membership.joined_at = membership.joined_at or utc_now()
    membership.suspended_at = None
    membership.revoked_at = None
    return membership


def _ensure_admin_profile(
    session: Session,
    tenant: TenantRecordModel,
) -> AccessProfileModel:
    profile = session.scalar(
        select(AccessProfileModel).where(
            AccessProfileModel.tenant_id == tenant.id,
            func.lower(func.trim(AccessProfileModel.code))
            == ADMIN_PROFILE_CODE.casefold(),
        )
    )

    if profile is None:
        profile = AccessProfileModel(
            id=_stable_uuid(tenant.id, f"profile:{ADMIN_PROFILE_CODE}"),
            tenant_id=tenant.id,
            code=ADMIN_PROFILE_CODE,
            name=ADMIN_PROFILE_NAME,
            description=ADMIN_PROFILE_DESCRIPTION,
            is_system=True,
            is_active=True,
        )
        session.add(profile)
        session.flush()
        return profile

    profile.name = ADMIN_PROFILE_NAME
    profile.description = ADMIN_PROFILE_DESCRIPTION
    profile.is_system = True
    profile.is_active = True
    profile.deleted_at = None
    return profile


def _grant_all_permissions(
    session: Session,
    profile: AccessProfileModel,
) -> int:
    permissions = tuple(
        session.scalars(
            select(PermissionModel)
            .where(PermissionModel.is_active.is_(True))
            .order_by(PermissionModel.code.asc())
        ).all()
    )
    existing_permission_ids = set(
        session.scalars(
            select(AccessProfilePermissionModel.permission_id).where(
                AccessProfilePermissionModel.access_profile_id == profile.id,
            )
        ).all()
    )

    for permission in permissions:
        if permission.id in existing_permission_ids:
            continue

        session.add(
            AccessProfilePermissionModel(
                access_profile_id=profile.id,
                permission_id=permission.id,
            )
        )

    return len(permissions)


def _assign_profile(
    session: Session,
    tenant: TenantRecordModel,
    membership: TenantMembershipModel,
    profile: AccessProfileModel,
) -> None:
    assignment = session.get(
        TenantMembershipProfileModel,
        {
            "tenant_id": tenant.id,
            "membership_id": membership.id,
            "access_profile_id": profile.id,
        },
    )

    if assignment is None:
        session.add(
            TenantMembershipProfileModel(
                tenant_id=tenant.id,
                membership_id=membership.id,
                access_profile_id=profile.id,
            )
        )


def bootstrap(
    arguments: BootstrapArguments,
) -> BootstrapResult:
    """Initialize schema and ensure the complete first-admin relationship."""

    project_root = _project_root()
    configuration = _alembic_configuration(project_root)
    manager = get_database_manager(get_settings())
    schema_created, revision = _initialize_schema(
        manager.engine,
        configuration,
    )

    with manager.session() as session:
        sync_permission_catalog(session)
        tenant = _ensure_tenant(session, arguments.tenant_name)
        user = _ensure_user(session, arguments)
        membership = _ensure_membership(session, tenant, user)
        profile = _ensure_admin_profile(session, tenant)
        permission_count = _grant_all_permissions(session, profile)
        _assign_profile(session, tenant, membership, profile)
        session.flush()

        return BootstrapResult(
            tenant_id=tenant.id,
            user_id=user.id,
            membership_id=membership.id,
            profile_id=profile.id,
            permission_count=permission_count,
            schema_created=schema_created,
            alembic_revision=revision,
        )


def _non_blank(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise argparse.ArgumentTypeError(f"{field_name} não pode ficar vazio.")
    return normalized


def _email(value: str) -> str:
    normalized = _non_blank(value, "email").casefold()
    if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
        raise argparse.ArgumentTypeError("Informe um e-mail válido.")
    return normalized


def _uuid(value: str) -> uuid.UUID:
    try:
        parsed = uuid.UUID(value.strip())
    except ValueError as exception:
        raise argparse.ArgumentTypeError(
            "Informe o UUID exibido em Authentication > Users no Supabase."
        ) from exception
    if parsed.int == 0:
        raise argparse.ArgumentTypeError("O UUID não pode ser nulo.")
    return parsed


def _parse_arguments(argv: Sequence[str] | None = None) -> BootstrapArguments:
    parser = argparse.ArgumentParser(
        description=(
            "Inicializa um banco OrganizeG3 vazio e cria o primeiro administrador."
        )
    )
    parser.add_argument("--auth-user-id", required=True, type=_uuid)
    parser.add_argument("--email", required=True, type=_email)
    parser.add_argument(
        "--display-name",
        required=True,
        type=lambda value: _non_blank(value, "display-name"),
    )
    parser.add_argument(
        "--tenant-name",
        required=True,
        type=lambda value: _non_blank(value, "tenant-name"),
    )
    namespace = parser.parse_args(argv)
    return BootstrapArguments(
        auth_user_id=namespace.auth_user_id,
        email=namespace.email,
        display_name=namespace.display_name,
        tenant_name=namespace.tenant_name,
    )


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parse_arguments(argv)

    try:
        result = bootstrap(arguments)
    # The CLI boundary converts every operational failure into a stable exit code.
    except Exception as exception:  # noqa: BLE001
        _write_stderr(f"ERRO: {exception}")
        return 1
    finally:
        dispose_database_manager()

    _write_stdout("Bootstrap concluído com sucesso.")
    _write_stdout(
        "Schema criado: "
        f"{'sim' if result.schema_created else 'não, já existia'}"
    )
    _write_stdout(f"Revisão Alembic: {result.alembic_revision}")
    _write_stdout(f"Tenant ID: {result.tenant_id}")
    _write_stdout(f"User ID: {result.user_id}")
    _write_stdout(f"Membership ID: {result.membership_id}")
    _write_stdout(f"Profile ID: {result.profile_id}")
    _write_stdout(f"Permissões concedidas: {result.permission_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
