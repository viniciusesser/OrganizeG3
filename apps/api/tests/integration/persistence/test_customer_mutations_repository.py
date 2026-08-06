"""Integration tests for archived customer persistence."""

import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def make_customer(
    tenant_id: uuid.UUID,
) -> Customer:
    return Customer(
        tenant_id=tenant_id,
        code=(
            f"CUST-{uuid.uuid4().hex[:8].upper()}"
        ),
        name="Cliente Teste",
        customer_type=CustomerType.INDIVIDUAL,
    )


def test_archived_customer_requires_explicit_lookup(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(
        session
    )

    saved = repository.save(
        make_customer(tenant_id)
    )

    saved.archive()

    archived = repository.save(
        saved,
        include_archived=True,
    )

    assert (
        repository.get_by_id(
            tenant_id,
            archived.id or 0,
        )
        is None
    )

    recovered = repository.get_by_id(
        tenant_id,
        archived.id or 0,
        include_archived=True,
    )

    assert recovered is not None
    assert recovered.deleted_at is not None
    assert recovered.is_active is False


def test_reactivates_archived_customer(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(
        session
    )

    saved = repository.save(
        make_customer(tenant_id)
    )

    saved.archive()

    archived = repository.save(
        saved,
        include_archived=True,
    )

    archived.reactivate()

    restored = repository.save(
        archived,
        include_archived=True,
    )

    assert restored.deleted_at is None
    assert restored.is_active is True
    assert restored.row_version == 3

    assert (
        repository.get_by_id(
            tenant_id,
            restored.id or 0,
        )
        is not None
    )


def test_archived_update_requires_permission(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(
        session
    )

    saved = repository.save(
        make_customer(tenant_id)
    )

    saved.archive()

    archived = repository.save(
        saved,
        include_archived=True,
    )

    archived.name = "Tentativa indevida"

    with pytest.raises(NotFoundError):
        repository.save(archived)
