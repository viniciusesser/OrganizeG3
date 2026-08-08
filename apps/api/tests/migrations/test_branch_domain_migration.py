"""Tests for the branch domain expansion migration."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
import pytest

pytestmark = pytest.mark.migration

PROJECT_ROOT = Path(__file__).resolve().parents[4]

BRANCH_DOMAIN_REVISION = "792dc8f069c5"
PREVIOUS_REVISION = "e47492c9a55a"


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


def branch_revision() -> object:
    """Return the branch domain migration revision."""

    return alembic_script().get_revision(
        BRANCH_DOMAIN_REVISION
    )


def render_upgrade_sql() -> str:
    """Render branch upgrade SQL for PostgreSQL."""

    revision = branch_revision()
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
    """Render branch downgrade SQL for PostgreSQL."""

    revision = branch_revision()
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
    revision = branch_revision()

    assert (
        revision.down_revision
        == PREVIOUS_REVISION
    )


def test_upgrade_adds_branch_business_columns() -> None:
    generated_sql = render_upgrade_sql()

    expected_columns = [
        "state_registration",
        "email",
        "phone",
        "website",
        "street",
        "number",
        "district",
        "city",
        "state",
        "postal_code",
    ]

    for column_name in expected_columns:
        assert (
            f"ALTER TABLE branches "
            f"ADD COLUMN {column_name}"
            in generated_sql
        )


def test_upgrade_does_not_modify_document_number() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "ALTER COLUMN document_number"
        not in generated_sql
    )


def test_upgrade_creates_partial_headquarters_index() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE UNIQUE INDEX "
        "uq_branches_tenant_headquarters"
        in generated_sql
    )

    assert (
        "WHERE is_headquarters = true"
        in generated_sql
    )


def test_headquarters_index_is_tenant_scoped() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "uq_branches_tenant_headquarters "
        "ON branches (tenant_id)"
        in generated_sql
    )


def test_downgrade_removes_headquarters_index() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP INDEX "
        "uq_branches_tenant_headquarters"
        in generated_sql
    )


def test_downgrade_removes_added_columns() -> None:
    generated_sql = render_downgrade_sql()

    expected_columns = [
        "postal_code",
        "state",
        "city",
        "district",
        "number",
        "street",
        "website",
        "phone",
        "email",
        "state_registration",
    ]

    for column_name in expected_columns:
        assert (
            f"ALTER TABLE branches "
            f"DROP COLUMN {column_name}"
            in generated_sql
        )
