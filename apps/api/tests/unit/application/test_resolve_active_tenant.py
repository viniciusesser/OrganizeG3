"""Unit tests for active tenant resolution."""

import uuid

import pytest

from organizeg3_api.application.tenant.resolve_active_tenant import (
    ResolveActiveTenant,
)
from organizeg3_api.core.exceptions import (
    PermissionDeniedError,
)
from organizeg3_api.domain.tenant.repository import (
    ITenantRepository,
)

pytestmark = pytest.mark.unit


class TenantRepositoryStub(
    ITenantRepository
):
    """Configurable repository stub."""

    def __init__(
        self,
        *,
        active: bool,
    ) -> None:
        self._active = active
        self.received_tenant_id: uuid.UUID | None = None

    def exists_active(
        self,
        tenant_id: uuid.UUID,
    ) -> bool:
        self.received_tenant_id = tenant_id
        return self._active


def test_returns_active_tenant() -> None:
    tenant_id = uuid.uuid4()

    repository = TenantRepositoryStub(
        active=True
    )

    service = ResolveActiveTenant(
        repository
    )

    result = service.execute(
        tenant_id
    )

    assert result == tenant_id
    assert (
        repository.received_tenant_id
        == tenant_id
    )


def test_rejects_unavailable_tenant() -> None:
    repository = TenantRepositoryStub(
        active=False
    )

    service = ResolveActiveTenant(
        repository
    )

    with pytest.raises(
        PermissionDeniedError
    ) as captured:
        service.execute(
            uuid.uuid4()
        )

    assert (
        captured.value.details["reason"]
        == "tenant_unavailable"
    )


def test_rejects_null_uuid() -> None:
    repository = TenantRepositoryStub(
        active=True
    )

    service = ResolveActiveTenant(
        repository
    )

    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        service.execute(
            uuid.UUID(int=0)
        )
