"""Tests for the employee foundation migration."""

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

EMPLOYEE_REVISION = "5bb11e5247c3"
PREVIOUS_REVISION = "792dc8f069c5"


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


def employee_revision() -> object:
    """Return the employee migration revision."""

    return alembic_script().get_revision(
        EMPLOYEE_REVISION
    )


def render_upgrade_sql() -> str:
    """Render employee upgrade SQL for PostgreSQL."""

    revision = employee_revision()
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
    """Render employee downgrade SQL for PostgreSQL."""

    revision = employee_revision()
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
    revision = employee_revision()

    assert (
        revision.down_revision
        == PREVIOUS_REVISION
    )


def test_upgrade_creates_employees_table() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE TABLE employees"
        in generated_sql
    )


def test_upgrade_contains_legacy_bridge() -> None:
    generated_sql = render_upgrade_sql()

    assert "legacy_employee_id" in generated_sql

    assert (
        "uq_employees_tenant_legacy_employee_id"
        in generated_sql
    )


def test_upgrade_contains_branch_tenant_foreign_key() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "fk_employees_branch_tenant"
        in generated_sql
    )

    assert (
        "FOREIGN KEY(branch_id, tenant_id)"
        in generated_sql
    )


def test_upgrade_creates_expected_indexes() -> None:
    generated_sql = render_upgrade_sql()

    expected_indexes = [
        "ix_employees_tenant_active",
        "ix_employees_tenant_branch",
        "ix_employees_tenant_id",
        "ix_employees_tenant_status",
    ]

    for index_name in expected_indexes:
        assert index_name in generated_sql


def test_upgrade_contains_legacy_preconditions() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "legacy_tenant_count"
        in generated_sql
    )

    assert (
        "blank_name_count"
        in generated_sql
    )

    assert (
        "invalid_date_count"
        in generated_sql
    )

    assert (
        "duplicate_cpf_count"
        in generated_sql
    )


def test_upgrade_contains_cpf_validation_helper() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "migration_5bb11e5247c3_is_valid_cpf"
        in generated_sql
    )

    assert (
        "CREATE OR REPLACE FUNCTION"
        in generated_sql
    )

    assert (
        "DROP FUNCTION IF EXISTS"
        in generated_sql
    )


def test_upgrade_backfills_legacy_employees() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "INSERT INTO employees"
        in generated_sql
    )

    assert (
        "FROM funcionarios"
        in generated_sql
    )

    assert (
        "'EMP-'"
        in generated_sql
    )

    assert (
        "legacy_employee_id"
        in generated_sql
    )


def test_upgrade_does_not_assign_legacy_branch() -> None:
    generated_sql = render_upgrade_sql()

    assert "branch_id" in generated_sql

    assert (
        "prepared.id,\n                NULL,"
        in generated_sql
    )


def test_downgrade_drops_employees() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE employees"
        in generated_sql
    )


def test_downgrade_does_not_drop_legacy_funcionarios() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE funcionarios"
        not in generated_sql
    )
