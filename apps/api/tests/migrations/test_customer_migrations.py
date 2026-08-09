"""Tests for the complete Alembic revision chain."""

from __future__ import annotations

from io import StringIO
from itertools import pairwise
from pathlib import Path

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import Script, ScriptDirectory
import pytest

pytestmark = pytest.mark.migration


PROJECT_ROOT = Path(__file__).resolve().parents[4]

EXPECTED_REVISIONS = [
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
    "b7c2a91d4e6f",
]

EXPECTED_HEAD = "b7c2a91d4e6f"

NO_OP_REVISIONS = {
    "acc9bffaedbc",
    "62bc842a4881",
}


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


def ordered_revisions() -> list[Script]:
    """Return revisions ordered from oldest to newest."""

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


def render_upgrade_sql(
    revision: Script,
) -> str:
    """Render PostgreSQL upgrade SQL for one revision."""

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


def test_has_one_head_and_expected_head() -> None:
    """Ensure the migration graph has exactly one known head."""

    script = alembic_script()

    assert script.get_heads() == [
        EXPECTED_HEAD
    ]


def test_revision_chain_is_continuous() -> None:
    """Ensure the complete migration chain remains linear."""

    revisions = ordered_revisions()

    assert [
        revision.revision
        for revision in revisions
    ] == EXPECTED_REVISIONS

    assert revisions[0].down_revision is None

    for previous, current in pairwise(
        revisions
    ):
        assert (
            current.down_revision
            == previous.revision
        )


def test_non_no_op_revisions_render_upgrade_sql() -> None:
    """Ensure every non-no-op revision renders PostgreSQL upgrade SQL."""

    for revision in ordered_revisions():
        sql = render_upgrade_sql(
            revision
        )

        if revision.revision in NO_OP_REVISIONS:
            assert sql == ""
            continue

        assert sql


def test_no_op_revision_allowlist_is_exact() -> None:
    """Ensure only the known intentional revisions remain SQL no-ops."""

    actual_no_op_revisions = {
        revision.revision
        for revision in ordered_revisions()
        if not render_upgrade_sql(
            revision
        )
    }

    assert actual_no_op_revisions == NO_OP_REVISIONS


def test_head_revision_is_audit_event_migration() -> None:
    """Ensure the audit-event migration remains the current head."""

    script = alembic_script()

    revision = script.get_revision(
        EXPECTED_HEAD
    )

    assert revision is not None

    assert (
        revision.down_revision
        == "6f217e7442e3"
    )
