"""Tests for the service catalog migration."""

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

SERVICE_REVISION = "242d7df3df33"
PREVIOUS_REVISION = "ab28ad8ed9ed"


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


def service_revision() -> object:
    """Return the service migration revision."""

    return alembic_script().get_revision(
        SERVICE_REVISION
    )


def render_upgrade_sql() -> str:
    """Render PostgreSQL service upgrade SQL."""

    revision = service_revision()
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
    """Render PostgreSQL service downgrade SQL."""

    revision = service_revision()
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
    revision = service_revision()

    assert (
        revision.down_revision
        == PREVIOUS_REVISION
    )


def test_upgrade_creates_services_table() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE TABLE services"
        in generated_sql
    )


def test_upgrade_contains_expected_columns() -> None:
    generated_sql = render_upgrade_sql()

    expected_columns = [
        "code",
        "name",
        "category",
        "unit",
        "execution_mode",
        "estimated_duration_minutes",
        "is_active",
        "tenant_id",
        "created_at",
        "updated_at",
    ]

    for column_name in expected_columns:
        assert column_name in generated_sql


def test_upgrade_contains_expected_constraints() -> None:
    generated_sql = render_upgrade_sql()

    expected_constraints = [
        "ck_services_category_not_blank",
        "ck_services_code_not_blank",
        "ck_services_name_not_blank",
        "ck_services_unit_not_blank",
        "ck_services_execution_mode_valid",
        "ck_services_estimated_duration_positive",
        "fk_services_tenant_id_tenants",
        "uq_services_tenant_code",
    ]

    for constraint_name in expected_constraints:
        assert constraint_name in generated_sql


def test_upgrade_restricts_execution_mode() -> None:
    generated_sql = render_upgrade_sql()

    assert "'INTERNAL'" in generated_sql
    assert "'EXTERNAL'" in generated_sql
    assert "'BOTH'" in generated_sql


def test_upgrade_requires_positive_duration_when_present() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "estimated_duration_minutes IS NULL "
        "OR estimated_duration_minutes > 0"
        in generated_sql
    )


def test_upgrade_creates_expected_indexes() -> None:
    generated_sql = render_upgrade_sql()

    expected_indexes = [
        "ix_services_tenant_active",
        "ix_services_tenant_category",
        "ix_services_tenant_execution_mode",
        "ix_services_tenant_id",
        "ix_services_tenant_name",
    ]

    for index_name in expected_indexes:
        assert index_name in generated_sql


def test_upgrade_is_greenfield() -> None:
    generated_sql = render_upgrade_sql()

    forbidden_fragments = [
        "legacy_service_id",
        "INSERT INTO services",
        "ALTER TABLE orcamentos",
        "descricao_servico",
        "imposto_servico",
    ]

    for fragment in forbidden_fragments:
        assert fragment not in generated_sql


def test_downgrade_drops_services() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE services"
        in generated_sql
    )


def test_downgrade_does_not_modify_budgets() -> None:
    generated_sql = render_downgrade_sql()

    assert "orcamentos" not in generated_sql
