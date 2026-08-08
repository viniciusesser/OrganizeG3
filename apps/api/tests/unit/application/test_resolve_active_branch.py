"""Unit tests for active branch resolution."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.application.branch.exceptions import (
    BranchUnavailableError,
    InvalidBranchIdentifierError,
)
from organizeg3_api.application.branch.resolve_active_branch import (
    ResolveActiveBranch,
)


class StubBranchRepository:
    """Configurable branch repository for unit tests."""

    def __init__(
        self,
        *,
        available: bool,
    ) -> None:
        self.available = available

    def exists_active_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> bool:
        del tenant_id, branch_id

        return self.available


def test_returns_none_when_branch_is_not_selected() -> None:
    repository = StubBranchRepository(
        available=False
    )

    service = ResolveActiveBranch(
        repository
    )

    assert (
        service.execute(
            tenant_id=uuid.uuid4(),
            branch_id=None,
        )
        is None
    )


def test_returns_available_branch() -> None:
    branch_id = uuid.uuid4()

    repository = StubBranchRepository(
        available=True
    )

    service = ResolveActiveBranch(
        repository
    )

    assert (
        service.execute(
            tenant_id=uuid.uuid4(),
            branch_id=branch_id,
        )
        == branch_id
    )


def test_rejects_unavailable_branch() -> None:
    repository = StubBranchRepository(
        available=False
    )

    service = ResolveActiveBranch(
        repository
    )

    with pytest.raises(
        BranchUnavailableError
    ):
        service.execute(
            tenant_id=uuid.uuid4(),
            branch_id=uuid.uuid4(),
        )


def test_rejects_null_branch_uuid() -> None:
    repository = StubBranchRepository(
        available=True
    )

    service = ResolveActiveBranch(
        repository
    )

    with pytest.raises(
        InvalidBranchIdentifierError
    ):
        service.execute(
            tenant_id=uuid.uuid4(),
            branch_id=uuid.UUID(int=0),
        )
