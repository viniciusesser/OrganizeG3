"""Tests for customer tenant and identity constraints."""

from io import StringIO
from pathlib import Path
import re

from alembic.config import Config
from alembic.migration import (
    MigrationContext,
)
from alembic.operations import Operations
from alembic.script import ScriptDirectory
import pytest

pytestmark = pytest.mark.migration

_PROJECT_ROOT = (
    Path(__file__).resolve().parents[4]
)
_REVISION_ID = "a81c5e7d2f34"


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
    """Render one revision using PostgreSQL offline mode."""

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
    """Collapse SQL whitespace for stable assertions."""

    return re.sub(
        r"\s+",
        " ",
        sql,
    ).strip()


def test_constraint_revision_has_expected_parent() -> None:
    revision = alembic_script().get_revision(
        _REVISION_ID
    )

    assert revision is not None
    assert (
        revision.down_revision
        == "7d4f2a9c6b81"
    )


def test_upgrade_adds_tenant_guarantees() -> None:
    sql = normalize_sql(
        render_revision_sql(
            upgrade=True
        )
    )

    assert (
        "ALTER TABLE clientes "
        "ALTER COLUMN tenant_id SET NOT NULL"
        in sql
    )

    assert (
        "fk_clientes_tenant_id_tenants"
        in sql
    )

    assert "REFERENCES tenants" in sql

    assert (
        "ck_clientes_tenant_id_not_nil"
        in sql
    )

    assert (
        "00000000-0000-0000-0000-000000000000"
        in sql
    )


def test_upgrade_adds_normalized_unique_indexes() -> None:
    sql = normalize_sql(
        render_revision_sql(
            upgrade=True
        )
    )

    assert (
        "uq_clientes_tenant_document_normalized"
        in sql
    )

    assert (
        "uq_clientes_tenant_email_normalized"
        in sql
    )

    assert "CREATE UNIQUE INDEX" in sql
    assert "BTRIM(cpf_cnpj)" in sql
    assert "LOWER" in sql
    assert "BTRIM(email)" in sql


def test_downgrade_removes_constraints_and_indexes() -> None:
    sql = normalize_sql(
        render_revision_sql(
            upgrade=False
        )
    )

    assert (
        "DROP INDEX IF EXISTS "
        "uq_clientes_tenant_document_normalized"
        in sql
    )

    assert (
        "DROP INDEX IF EXISTS "
        "uq_clientes_tenant_email_normalized"
        in sql
    )

    assert (
        "fk_clientes_tenant_id_tenants"
        in sql
    )

    assert (
        "ck_clientes_tenant_id_not_nil"
        in sql
    )

    assert (
        "ALTER TABLE clientes "
        "ALTER COLUMN tenant_id DROP NOT NULL"
        in sql
    )
