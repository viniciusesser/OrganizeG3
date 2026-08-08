"""Unit tests for branch HTTP dependencies."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.application.branch.exceptions import (
    BranchRequiredError,
)
from organizeg3_api.core.exceptions import ValidationError
from organizeg3_api.domain.branch.context import (
    BranchContext,
)
from organizeg3_api.infrastructure.http.branch_context import (
    require_branch,
)
from organizeg3_api.infrastructure.http.dependencies import (
    parse_branch_header,
)


def test_missing_branch_header_returns_none() -> None:
    assert parse_branch_header(None) is None


def test_blank_branch_header_returns_none() -> None:
    assert parse_branch_header("   ") is None


def test_parses_valid_branch_uuid() -> None:
    branch_id = uuid.uuid4()

    assert (
        parse_branch_header(
            str(branch_id)
        )
        == branch_id
    )


def test_rejects_invalid_branch_uuid() -> None:
    with pytest.raises(
        ValidationError
    ):
        parse_branch_header(
            "invalid"
        )


def test_rejects_null_branch_uuid() -> None:
    with pytest.raises(
        ValidationError
    ):
        parse_branch_header(
            str(
                uuid.UUID(int=0)
            )
        )


def test_require_branch_returns_selected_branch() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    context = BranchContext(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert require_branch(
        context
    ) == branch_id


def test_require_branch_rejects_missing_branch() -> None:
    context = BranchContext(
        tenant_id=uuid.uuid4(),
        branch_id=None,
    )

    with pytest.raises(
        BranchRequiredError
    ):
        require_branch(
            context
        )
