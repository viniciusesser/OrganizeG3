"""Tests for archival and reactivation use cases."""

from collections.abc import Sequence
from datetime import UTC, datetime
import uuid

import pytest

from organizeg3_api.application.customer.use_cases.archive_customer import (
    ArchiveCustomerUseCase,
)
from organizeg3_api.application.customer.use_cases.reactivate_customer import (
    ReactivateCustomerUseCase,
)
from organizeg3_api.core.exceptions import (
    ConcurrencyError,
    InvalidTransitionError,
    NotFoundError,
)
from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)
from organizeg3_api.domain.customer.repository import (
    ICustomerRepository,
)

pytestmark = pytest.mark.unit


class LifecycleCustomerRepository(
    ICustomerRepository
):
    def __init__(
        self,
        customer: Customer | None,
    ) -> None:
        self.customer = customer
        self.get_included_archived = False
        self.save_included_archived = False

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        del tenant_id
        del customer_id

        self.get_included_archived = (
            include_archived
        )

        return self.customer

    def list_all(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        customer_type: CustomerType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Customer]:
        del tenant_id
        del include_inactive
        del search
        del customer_type
        del limit
        del offset

        return []

    def save(
        self,
        customer: Customer,
        *,
        include_archived: bool = False,
    ) -> Customer:
        self.save_included_archived = (
            include_archived
        )

        customer.row_version += 1
        self.customer = customer

        return customer


def make_customer(
    *,
    archived: bool = False,
    version: int = 1,
) -> Customer:
    return Customer(
        id=10,
        tenant_id=uuid.uuid4(),
        code="CUST-0001",
        name="Cliente",
        customer_type=CustomerType.INDIVIDUAL,
        row_version=version,
        is_active=not archived,
        deleted_at=(
            datetime.now(UTC)
            if archived
            else None
        ),
    )


def test_archives_customer() -> None:
    customer = make_customer(version=2)
    repository = LifecycleCustomerRepository(
        customer
    )

    result = ArchiveCustomerUseCase(
        repository
    ).execute(
        customer.tenant_id,
        customer.id or 0,
        2,
    )

    assert result.deleted_at is not None
    assert result.is_active is False
    assert result.row_version == 3
    assert repository.get_included_archived is True
    assert repository.save_included_archived is True


def test_reactivates_archived_customer() -> None:
    customer = make_customer(
        archived=True,
        version=4,
    )
    repository = LifecycleCustomerRepository(
        customer
    )

    result = ReactivateCustomerUseCase(
        repository
    ).execute(
        customer.tenant_id,
        customer.id or 0,
        4,
    )

    assert result.deleted_at is None
    assert result.is_active is True
    assert result.row_version == 5
    assert repository.get_included_archived is True
    assert repository.save_included_archived is True


def test_rejects_archiving_twice() -> None:
    customer = make_customer(archived=True)
    repository = LifecycleCustomerRepository(
        customer
    )

    with pytest.raises(
        InvalidTransitionError,
        match="já está arquivado",
    ):
        ArchiveCustomerUseCase(
            repository
        ).execute(
            customer.tenant_id,
            customer.id or 0,
            customer.row_version,
        )


def test_rejects_invalid_reactivation() -> None:
    customer = make_customer()
    repository = LifecycleCustomerRepository(
        customer
    )

    with pytest.raises(
        InvalidTransitionError,
        match="não está arquivado",
    ):
        ReactivateCustomerUseCase(
            repository
        ).execute(
            customer.tenant_id,
            customer.id or 0,
            customer.row_version,
        )


def test_lifecycle_validates_version() -> None:
    customer = make_customer(version=3)
    repository = LifecycleCustomerRepository(
        customer
    )

    with pytest.raises(ConcurrencyError):
        ArchiveCustomerUseCase(
            repository
        ).execute(
            customer.tenant_id,
            customer.id or 0,
            2,
        )


def test_lifecycle_raises_not_found() -> None:
    repository = LifecycleCustomerRepository(
        None
    )

    with pytest.raises(NotFoundError):
        ArchiveCustomerUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            99,
            1,
        )

    with pytest.raises(NotFoundError):
        ReactivateCustomerUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            99,
            1,
        )
