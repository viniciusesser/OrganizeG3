"""Unit tests for active tenant resolution."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.application.tenant.resolve_active_tenant import (
    ResolveActiveTenant,
)
from organizeg3_api.core.exceptions import TenantUnavailableError


class FakeTenantRepository:
    """In-memory tenant availability repository."""

    def __init__(
        self,
        active_tenant_ids: set[uuid.UUID],
    ) -> None:
        self._active_tenant_ids = active_tenant_ids

    def is_active(
        self,
        tenant_id: uuid.UUID,
    ) -> bool:
        return tenant_id in self._active_tenant_ids


def test_returns_active_tenant_id() -> None:
    tenant_id = uuid.uuid4()

    resolver = ResolveActiveTenant(
        FakeTenantRepository(
            {
                tenant_id,
            }
        )
    )

    assert resolver.execute(
        tenant_id
    ) == tenant_id


def test_rejects_unavailable_tenant() -> None:
    tenant_id = uuid.uuid4()

    resolver = ResolveActiveTenant(
        FakeTenantRepository(set())
    )

    with pytest.raises(
        TenantUnavailableError
    ) as captured:
        resolver.execute(
            tenant_id
        )

    assert (
        captured.value.error_code
        == "tenant.unavailable"
    )
