"""Integration tests for customer duplicate lookup operations."""

from datetime import UTC, datetime
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
)
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def add_customer_model(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    document_number: str | None,
    email: str | None,
    deleted_at: datetime | None = None,
) -> CustomerModel:
    model = CustomerModel(
        tenant_id=tenant_id,
        code=(
            f"CUST-{uuid.uuid4().hex[:8].upper()}"
        ),
        name="Cliente Existente",
        customer_type="INDIVIDUAL",
        document_number=document_number,
        email=email,
        is_active=deleted_at is None,
        deleted_at=deleted_at,
    )

    session.add(model)
    session.flush()

    return model


def test_detects_formatted_document_and_case_insensitive_email(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="529.982.247-25",
        email="  CLIENTE@EXAMPLE.COM  ",
    )

    repository = SQLAlchemyCustomerRepository(
        session
    )

    assert repository.exists_by_document(
        tenant_id,
        DocumentNumber(
            "52998224725"
        ),
    )

    assert repository.exists_by_email(
        tenant_id,
        EmailAddress(
            "cliente@example.com"
        ),
    )


def test_duplicate_checks_are_tenant_scoped(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="52998224725",
        email="cliente@example.com",
    )

    repository = SQLAlchemyCustomerRepository(
        session
    )

    assert not repository.exists_by_document(
        other_tenant_id,
        DocumentNumber(
            "52998224725"
        ),
    )

    assert not repository.exists_by_email(
        other_tenant_id,
        EmailAddress(
            "cliente@example.com"
        ),
    )


def test_archived_customer_reserves_document_and_email(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="52998224725",
        email="cliente@example.com",
        deleted_at=datetime.now(UTC),
    )

    repository = SQLAlchemyCustomerRepository(
        session
    )

    assert repository.exists_by_document(
        tenant_id,
        DocumentNumber(
            "52998224725"
        ),
    )

    assert repository.exists_by_email(
        tenant_id,
        EmailAddress(
            "cliente@example.com"
        ),
    )


def test_duplicate_checks_can_exclude_current_customer(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    model = add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="52998224725",
        email="cliente@example.com",
    )

    repository = SQLAlchemyCustomerRepository(
        session
    )

    assert not repository.exists_by_document(
        tenant_id,
        DocumentNumber(
            "52998224725"
        ),
        exclude_customer_id=model.id,
    )

    assert not repository.exists_by_email(
        tenant_id,
        EmailAddress(
            "cliente@example.com"
        ),
        exclude_customer_id=model.id,
    )
