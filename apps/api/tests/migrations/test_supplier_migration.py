"""Tests for the supplier foundation migration."""

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

SUPPLIER_REVISION = "86408a055683"
PREVIOUS_REVISION = "5bb11e5247c3"


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


def supplier_revision() -> object:
    """Return the supplier migration revision."""

    return alembic_script().get_revision(
        SUPPLIER_REVISION
    )


def render_upgrade_sql() -> str:
    """Render supplier upgrade SQL for PostgreSQL."""

    revision = supplier_revision()
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
    """Render supplier downgrade SQL for PostgreSQL."""

    revision = supplier_revision()
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
    revision = supplier_revision()

    assert (
        revision.down_revision
        == PREVIOUS_REVISION
    )


def test_upgrade_creates_suppliers_table() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE TABLE suppliers"
        in generated_sql
    )


def test_upgrade_contains_legacy_supplier_bridge() -> None:
    generated_sql = render_upgrade_sql()

    assert "legacy_supplier_id" in generated_sql

    assert (
        "uq_suppliers_tenant_legacy_supplier_id"
        in generated_sql
    )


def test_upgrade_creates_expected_indexes() -> None:
    generated_sql = render_upgrade_sql()

    expected_indexes = [
        "ix_suppliers_tenant_active",
        "ix_suppliers_tenant_id",
        "ix_suppliers_tenant_name",
    ]

    for index_name in expected_indexes:
        assert index_name in generated_sql


def test_upgrade_contains_cnpj_validation() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "migration_86408a055683_is_valid_cnpj"
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


def test_upgrade_contains_legacy_preconditions() -> None:
    generated_sql = render_upgrade_sql()

    assert "legacy_tenant_count" in generated_sql
    assert "blank_name_count" in generated_sql

    assert (
        "duplicate_document_count"
        in generated_sql
    )

    assert (
        "oversized_value_count"
        in generated_sql
    )


def test_upgrade_backfills_legacy_suppliers() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "INSERT INTO suppliers"
        in generated_sql
    )

    assert (
        "FROM fornecedores"
        in generated_sql
    )

    assert "'FORN-'" in generated_sql


def test_upgrade_uses_safe_name_fallback() -> None:
    generated_sql = render_upgrade_sql()

    assert "nome_fantasia" in generated_sql
    assert "razao_social" in generated_sql
    assert "COALESCE" in generated_sql


def test_upgrade_does_not_migrate_banking_data() -> None:
    generated_sql = render_upgrade_sql()

    forbidden_fields = [
        "banco_nome",
        "banco_agencia",
        "banco_conta",
        "chave_pix",
        "obs_bancarias",
        "saldo_inicial",
    ]

    for field_name in forbidden_fields:
        assert field_name not in generated_sql


def test_downgrade_drops_suppliers() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE suppliers"
        in generated_sql
    )


def test_downgrade_preserves_legacy_fornecedores() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE fornecedores"
        not in generated_sql
    )
