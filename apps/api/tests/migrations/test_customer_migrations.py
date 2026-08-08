"""Tests for the Alembic revision chain and customer migration SQL."""

from io import StringIO
from itertools import pairwise
from pathlib import Path

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
import pytest

from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)

pytestmark = pytest.mark.migration

PROJECT_ROOT = Path(
    __file__
).resolve().parents[4]


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


def ordered_revisions() -> list[object]:
    """Return all migrations ordered from base to head."""

    script = alembic_script()

    return list(
        reversed(
            list(
                script.walk_revisions(
                    base="base",
                    head="heads",
                )
            )
        )
    )


def test_has_one_head_and_expected_head() -> None:
    script = alembic_script()

    assert script.get_heads() == [
        "6f217e7442e3"
    ]


def test_revision_chain_is_continuous() -> None:
    revisions = ordered_revisions()

    assert [
        revision.revision
        for revision in revisions
    ] == [
        "acc9bffaedbc",
        "62bc842a4881",
        "0439fdabfa05",
        "7d4f2a9c6b81",
        "a81c5e7d2f34",
        "d3f6a1c8e902",
        "9fb2267cbba8",
        "e47492c9a55a",
        "792dc8f069c5",
        "5bb11e5247c3",
        "86408a055683",
        "ab28ad8ed9ed",
        "242d7df3df33",
        "63f6df64a945",
        "49b92745c01a",
        "7b2db4ad5a69",
        "51b4d66e1411",
        "9189ddfdd4b1",
        "69e086a75bdb",
        "6f217e7442e3",
    ]

    assert revisions[0].down_revision is None

    for previous, current in pairwise(
        revisions
    ):
        assert (
            current.down_revision
            == previous.revision
        )


def test_legacy_baseline_is_non_destructive() -> None:
    baseline = alembic_script().get_revision(
        "acc9bffaedbc"
    )

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
        baseline.module.upgrade()
        baseline.module.downgrade()

    assert output.getvalue() == ""


def test_baseline_to_head_generates_postgresql_upgrade_sql() -> None:
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
        for revision in ordered_revisions():
            revision.module.upgrade()

    generated_sql = output.getvalue()

    expected_fragments = [
        "ALTER TABLE clientes ADD COLUMN tenant_id UUID",
        "CREATE INDEX ix_clientes_tenant_id",
        "ALTER TABLE clientes ALTER COLUMN nome SET NOT NULL",
        "CREATE TABLE companies",
        "INSERT INTO companies",
        "ALTER TABLE branches ADD COLUMN state_registration",
        "CREATE UNIQUE INDEX uq_branches_tenant_headquarters",
        "WHERE is_headquarters = true",
        "CREATE TABLE employees",
        "INSERT INTO employees",
        "FROM funcionarios",
        "CREATE TABLE suppliers",
        "INSERT INTO suppliers",
        "FROM fornecedores",
        "CREATE TABLE brands",
        "INSERT INTO brands",
        "FROM marcas",
        "CREATE TABLE materials",
        "INSERT INTO materials",
        "FROM materiais",
        "CREATE TABLE services",
        "CREATE TABLE machines",
    ]

    for fragment in expected_fragments:
        assert fragment in generated_sql


def test_customer_downgrade_and_upgrade_generate_inverse_sql() -> None:
    customer_revision = (
        alembic_script().get_revision(
            "0439fdabfa05"
        )
    )

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
        customer_revision.module.downgrade()
        customer_revision.module.upgrade()

    generated_sql = output.getvalue()

    assert (
        "ALTER TABLE clientes "
        "DROP COLUMN tenant_id"
        in generated_sql
    )

    assert (
        "ALTER TABLE clientes "
        "ADD COLUMN tenant_id UUID"
        in generated_sql
    )


def test_customer_model_contains_migrated_and_legacy_columns() -> None:
    columns = set(
        CustomerModel.__table__.columns.keys()
    )

    assert {
        "id",
        "tenant_id",
        "code",
        "nome",
        "tipo_pessoa",
        "cpf_cnpj",
        "email",
        "telefone",
        "ativo",
        "data_cadastro",
        "updated_at",
        "row_version",
        "deleted_at",
    }.issubset(
        columns
    )
