"""Tests for the company foundation migration."""

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

COMPANY_REVISION = "e47492c9a55a"
PREVIOUS_REVISION = "9fb2267cbba8"


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


def company_revision() -> object:
    """Return the company migration revision."""

    return alembic_script().get_revision(
        COMPANY_REVISION
    )


def render_upgrade_sql() -> str:
    """Render company upgrade SQL for PostgreSQL."""

    revision = company_revision()

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
    """Render company downgrade SQL for PostgreSQL."""

    revision = company_revision()

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
    revision = company_revision()

    assert revision.down_revision == PREVIOUS_REVISION


def test_upgrade_creates_companies_table() -> None:
    generated_sql = render_upgrade_sql()

    assert "CREATE TABLE companies" in generated_sql

    assert (
        "CONSTRAINT pk_companies PRIMARY KEY (id)"
        in generated_sql
    )

    assert (
        "FOREIGN KEY(tenant_id) "
        "REFERENCES tenants (id) "
        "ON DELETE CASCADE"
        in generated_sql
    )

    assert (
        "CONSTRAINT uq_companies_tenant_id "
        "UNIQUE (tenant_id)"
        in generated_sql
    )


def test_upgrade_creates_company_indexes() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "CREATE INDEX ix_companies_tenant_active"
        in generated_sql
    )

    assert (
        "CREATE INDEX ix_companies_tenant_id"
        in generated_sql
    )

    assert (
        "CREATE UNIQUE INDEX "
        "uq_companies_document_number_normalized"
        in generated_sql
    )


def test_upgrade_contains_legacy_company_backfill() -> None:
    generated_sql = render_upgrade_sql()

    assert "INSERT INTO companies" in generated_sql
    assert "FROM tenants AS tenant" in generated_sql

    assert (
        "LEFT JOIN configuracoes AS config"
        in generated_sql
    )

    assert (
        "config.empresa_inscricao_estadual"
        in generated_sql
    )

    assert (
        "config.empresa_site"
        in generated_sql
    )

    assert (
        "config.empresa_logo_path"
        in generated_sql
    )

    assert (
        "config.empresa_logradouro"
        in generated_sql
    )

    assert (
        "config.empresa_cep"
        in generated_sql
    )


def test_backfill_validates_bounded_legacy_fields() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "IN (11, 14)"
        in generated_sql
    )

    assert (
        "data.raw_state"
        in generated_sql
    )

    assert (
        "data.raw_postal_code"
        in generated_sql
    )

    assert (
        "THEN data.raw_postal_code"
        in generated_sql
    )

    assert (
        "ELSE NULL"
        in generated_sql
    )


def test_backfill_uses_tenant_as_company_identity() -> None:
    generated_sql = render_upgrade_sql()

    assert (
        "data.tenant_id,\n"
        "    data.tenant_id,"
        in generated_sql
    )


def test_downgrade_removes_company_structure() -> None:
    generated_sql = render_downgrade_sql()

    assert (
        "DROP INDEX "
        "uq_companies_document_number_normalized"
        in generated_sql
    )

    assert (
        "DROP INDEX ix_companies_tenant_id"
        in generated_sql
    )

    assert (
        "DROP INDEX ix_companies_tenant_active"
        in generated_sql
    )

    assert "DROP TABLE companies" in generated_sql
