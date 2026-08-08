"""Tests for the industrial machine catalog migration."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
import pytest

pytestmark = pytest.mark.migration

PROJECT_ROOT = Path(
    __file__
).resolve().parents[4]

MACHINE_REVISION = "63f6df64a945"
PREVIOUS_REVISION = "242d7df3df33"


def alembic_script() -> ScriptDirectory:
    """Return the project Alembic script directory."""

    configuration = Config(
        PROJECT_ROOT / "alembic.ini"
    )

    configuration.set_main_option(
        "script_location",
        str(
            PROJECT_ROOT
            / "database"
            / "migrations"
        ),
    )

    return ScriptDirectory.from_config(
        configuration
    )


def machine_revision() -> object:
    """Return the machine migration revision."""

    return alembic_script().get_revision(
        MACHINE_REVISION
    )


def render_upgrade_sql() -> str:
    """Render PostgreSQL machine upgrade SQL."""

    revision = machine_revision()
    output = StringIO()

    context = MigrationContext.configure(
        dialect_name="postgresql",
        opts={
            "as_sql": True,
            "output_buffer": output,
        },
    )

    with Operations.context(
        context
    ):
        revision.module.upgrade()

    return output.getvalue()


def render_downgrade_sql() -> str:
    """Render PostgreSQL machine downgrade SQL."""

    revision = machine_revision()
    output = StringIO()

    context = MigrationContext.configure(
        dialect_name="postgresql",
        opts={
            "as_sql": True,
            "output_buffer": output,
        },
    )

    with Operations.context(
        context
    ):
        revision.module.downgrade()

    return output.getvalue()


def test_revision_has_expected_parent() -> None:
    revision = machine_revision()

    assert (
        revision.down_revision
        == PREVIOUS_REVISION
    )


def test_upgrade_creates_machines_table() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE TABLE machines"
        in generated_sql
    )


def test_upgrade_contains_expected_columns() -> None:
    generated_sql = render_upgrade_sql()

    expected_columns = [
        "branch_id",
        "code",
        "name",
        "machine_type",
        "manufacturer",
        "model",
        "serial_number",
        "status",
        "is_active",
        "id",
        "tenant_id",
        "created_at",
        "updated_at",
    ]

    for column_name in expected_columns:
        assert column_name in generated_sql


def test_upgrade_contains_expected_constraints() -> None:
    generated_sql = render_upgrade_sql()

    expected_constraints = [
        "ck_machines_code_not_blank",
        "ck_machines_name_not_blank",
        "ck_machines_machine_type_not_blank",
        "ck_machines_status_valid",
        "fk_machines_branch_tenant",
        "fk_machines_tenant_id_tenants",
        "uq_machines_tenant_code",
    ]

    for constraint_name in expected_constraints:
        assert constraint_name in generated_sql


def test_upgrade_contains_branch_tenant_scope() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "fk_machines_branch_tenant"
        in generated_sql
    )

    assert "branch_id" in generated_sql
    assert "tenant_id" in generated_sql

    assert "branches" in generated_sql


def test_upgrade_restricts_machine_status() -> None:
    generated_sql = render_upgrade_sql()

    expected_statuses = [
        "'AVAILABLE'",
        "'IN_USE'",
        "'MAINTENANCE'",
        "'OUT_OF_SERVICE'",
    ]

    for status in expected_statuses:
        assert status in generated_sql


def test_upgrade_creates_expected_indexes() -> None:
    generated_sql = render_upgrade_sql()

    expected_indexes = [
        "ix_machines_tenant_active",
        "ix_machines_tenant_branch",
        "ix_machines_tenant_id",
        "ix_machines_tenant_name",
        "ix_machines_tenant_status",
        "ix_machines_tenant_type",
    ]

    for index_name in expected_indexes:
        assert index_name in generated_sql


def test_upgrade_is_greenfield() -> None:
    generated_sql = render_upgrade_sql()

    forbidden_fragments = [
        "legacy_machine_id",
        "INSERT INTO machines",
        "ALTER TABLE maquininhas",
        "FROM maquininhas",
    ]

    for fragment in forbidden_fragments:
        assert fragment not in generated_sql


def test_downgrade_drops_machines() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE machines"
        in generated_sql
    )


def test_downgrade_preserves_financial_card_machine_table() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "maquininhas"
        not in generated_sql
    )
