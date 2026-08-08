"""Tests for the identity and authorization migration."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
import re

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
import pytest

pytestmark = pytest.mark.migration

_PROJECT_ROOT = (
    Path(__file__).resolve().parents[4]
)

_REVISION_ID = "d3f6a1c8e902"


def alembic_script() -> ScriptDirectory:
    """Build the project Alembic script directory."""

    configuration = Config(
        str(
            _PROJECT_ROOT
            / "alembic.ini"
        )
    )

    configuration.set_main_option(
        "script_location",
        str(
            _PROJECT_ROOT
            / "database"
            / "migrations"
        ),
    )

    return ScriptDirectory.from_config(
        configuration
    )


def render_revision_sql(
    *,
    upgrade: bool,
) -> str:
    """Render the revision using PostgreSQL offline mode."""

    revision = alembic_script().get_revision(
        _REVISION_ID
    )

    assert revision is not None

    output = StringIO()

    context = MigrationContext.configure(
        dialect_name="postgresql",
        opts={
            "as_sql": True,
            "output_buffer": output,
        },
    )

    with Operations.context(context):
        if upgrade:
            revision.module.upgrade()
        else:
            revision.module.downgrade()

    return output.getvalue()


def normalize_sql(
    sql: str,
) -> str:
    """Collapse whitespace for stable assertions."""

    return re.sub(
        r"\s+",
        " ",
        sql,
    ).strip()


def test_revision_has_expected_parent() -> None:
    revision = alembic_script().get_revision(
        _REVISION_ID
    )

    assert revision is not None
    assert (
        revision.down_revision
        == "a81c5e7d2f34"
    )


def test_upgrade_creates_identity_tables() -> None:
    sql = normalize_sql(
        render_revision_sql(
            upgrade=True
        )
    )

    expected_tables = (
        "users",
        "tenant_memberships",
        "access_profiles",
        "permissions",
        "access_profile_permissions",
        "tenant_membership_profiles",
        (
            "tenant_membership_"
            "permission_overrides"
        ),
    )

    for table_name in expected_tables:
        assert (
            f"CREATE TABLE {table_name}"
            in sql
        )


def test_upgrade_creates_identity_constraints() -> None:
    sql = normalize_sql(
        render_revision_sql(
            upgrade=True
        )
    )

    assert (
        "uq_users_auth_user_id"
        in sql
    )

    assert (
        "uq_tenant_memberships_tenant_user"
        in sql
    )

    assert (
        "fk_tenant_memberships_tenant_id_tenants"
        in sql
    )

    assert (
        "fk_tenant_memberships_user_id_users"
        in sql
    )

    assert (
        "effect IN ('ALLOW', 'DENY')"
        in sql
    )


def test_upgrade_creates_normalized_unique_indexes() -> None:
    sql = normalize_sql(
        render_revision_sql(
            upgrade=True
        )
    )

    assert (
        "uq_users_email_normalized"
        in sql
    )

    assert (
        "uq_access_profiles_tenant_code_normalized"
        in sql
    )

    assert (
        "uq_permissions_code_normalized"
        in sql
    )

    assert "LOWER(TRIM(email))" in sql
    assert "LOWER(TRIM(code))" in sql


def test_downgrade_removes_identity_tables() -> None:
    sql = normalize_sql(
        render_revision_sql(
            upgrade=False
        )
    )

    assert (
        "DROP TABLE users"
        in sql
    )

    assert (
        "DROP TABLE tenant_memberships"
        in sql
    )

    assert (
        "DROP TABLE access_profiles"
        in sql
    )

    assert (
        "DROP TABLE permissions"
        in sql
    )
