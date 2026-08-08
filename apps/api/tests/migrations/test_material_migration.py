"""Tests for the brand and material foundation migration."""

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

MATERIAL_REVISION = "ab28ad8ed9ed"
PREVIOUS_REVISION = "86408a055683"


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


def material_revision() -> object:
    """Return the brand/material migration revision."""

    return alembic_script().get_revision(
        MATERIAL_REVISION
    )


def render_upgrade_sql() -> str:
    """Render PostgreSQL upgrade SQL."""

    revision = material_revision()
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
    """Render PostgreSQL downgrade SQL."""

    revision = material_revision()
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
    revision = material_revision()

    assert (
        revision.down_revision
        == PREVIOUS_REVISION
    )


def test_upgrade_creates_brands_table() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE TABLE brands"
        in generated_sql
    )


def test_upgrade_creates_materials_table() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE TABLE materials"
        in generated_sql
    )


def test_upgrade_contains_legacy_bridges() -> None:
    generated_sql = render_upgrade_sql()

    assert "legacy_brand_id" in generated_sql
    assert "legacy_material_id" in generated_sql

    assert (
        "uq_brands_tenant_legacy_brand_id"
        in generated_sql
    )

    assert (
        "uq_materials_tenant_legacy_material_id"
        in generated_sql
    )


def test_upgrade_contains_composite_brand_scope_fk() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "fk_materials_brand_tenant"
        in generated_sql
    )

    assert (
        "uq_brands_id_tenant"
        in generated_sql
    )


def test_upgrade_creates_expected_indexes() -> None:
    generated_sql = render_upgrade_sql()

    expected_indexes = [
        "ix_brands_tenant_active",
        "ix_brands_tenant_id",
        "ix_materials_tenant_active",
        "ix_materials_tenant_brand",
        "ix_materials_tenant_category",
        "ix_materials_tenant_id",
        "ix_materials_tenant_name",
    ]

    for index_name in expected_indexes:
        assert index_name in generated_sql


def test_upgrade_contains_legacy_preconditions() -> None:
    generated_sql = render_upgrade_sql()

    expected_checks = [
        "legacy_tenant_count",
        "invalid_brand_id_count",
        "blank_brand_name_count",
        "duplicate_brand_name_count",
        "invalid_material_id_count",
        "blank_material_name_count",
        "blank_material_category_count",
        "blank_material_unit_count",
        "oversized_material_count",
        "orphan_brand_reference_count",
    ]

    for check_name in expected_checks:
        assert check_name in generated_sql


def test_upgrade_backfills_brands() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "INSERT INTO brands"
        in generated_sql
    )

    assert (
        "FROM marcas"
        in generated_sql
    )

    assert "'MARCA-'" in generated_sql


def test_upgrade_backfills_materials() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "INSERT INTO materials"
        in generated_sql
    )

    assert (
        "FROM materiais"
        in generated_sql
    )

    assert "'MAT-'" in generated_sql


def test_upgrade_resolves_legacy_brand_reference() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "LEFT JOIN brands"
        in generated_sql
    )

    assert (
        "modern_brand.legacy_brand_id"
        in generated_sql
    )


def test_upgrade_normalizes_material_unit() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "upper("
        in generated_sql.lower()
    )

    assert (
        "legacy_material.unidade"
        in generated_sql
    )


def test_upgrade_does_not_move_inventory_or_cost_data() -> None:
    generated_sql = render_upgrade_sql()

    forbidden_fields = [
        "estoque_atual",
        "estoque_minimo",
        "preco_custo",
    ]

    for field_name in forbidden_fields:
        assert field_name not in generated_sql


def test_upgrade_preserves_price_and_stock_tables() -> None:
    generated_sql = render_upgrade_sql()

    forbidden_operations = [
        "DROP TABLE precos_materiais",
        "DROP TABLE historico_precos",
        "DROP TABLE movimentos_estoque",
        "DROP TABLE materiais",
        "DROP TABLE marcas",
    ]

    for operation in forbidden_operations:
        assert operation not in generated_sql


def test_downgrade_drops_modern_catalog_tables() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE materials"
        in generated_sql
    )

    assert (
        "DROP TABLE brands"
        in generated_sql
    )


def test_downgrade_preserves_legacy_catalog() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP TABLE materiais"
        not in generated_sql
    )

    assert (
        "DROP TABLE marcas"
        not in generated_sql
    )
