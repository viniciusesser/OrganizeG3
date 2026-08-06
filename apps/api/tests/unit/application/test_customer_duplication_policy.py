"""Unit tests for the customer duplication policy."""

from collections.abc import Sequence
import uuid

import pytest

from organizeg3_api.application.customer.duplication_policy import (
    CustomerDuplicationPolicy,
)
from organizeg3_api.core.exceptions import (
    DuplicateCustomerError,
)
from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)
from organizeg3_api.domain.customer.repository import (
    ICustomerRepository,
)
from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
)

pytestmark = pytest.mark.unit


class DuplicateCheckingRepository(
    ICustomerRepository
):
    def __init__(self) -> None:
        self.duplicate_document = False
        self.duplicate_email = False
        self.document_exclusion: int | None = None
        self.email_exclusion: int | None = None

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        del tenant_id
        del customer_id
        del include_archived

        return None

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
        del include_archived

        return customer

    def exists_by_document(
        self,
        tenant_id: uuid.UUID,
        document_number: DocumentNumber,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        del tenant_id
        del document_number

        self.document_exclusion = (
            exclude_customer_id
        )

        return self.duplicate_document

    def exists_by_email(
        self,
        tenant_id: uuid.UUID,
        email: EmailAddress,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        del tenant_id
        del email

        self.email_exclusion = (
            exclude_customer_id
        )

        return self.duplicate_email


def test_accepts_available_identity_data() -> None:
    repository = DuplicateCheckingRepository()

    CustomerDuplicationPolicy(
        repository
    ).ensure_available(
        uuid.uuid4(),
        document_number=DocumentNumber(
            "52998224725"
        ),
        email=EmailAddress(
            "cliente@example.com"
        ),
    )


def test_rejects_duplicate_document() -> None:
    repository = DuplicateCheckingRepository()
    repository.duplicate_document = True

    with pytest.raises(
        DuplicateCustomerError
    ) as error:
        CustomerDuplicationPolicy(
            repository
        ).ensure_available(
            uuid.uuid4(),
            document_number=DocumentNumber(
                "52998224725"
            ),
            email=None,
        )

    assert error.value.details == {
        "field": "document_number"
    }


def test_rejects_duplicate_email() -> None:
    repository = DuplicateCheckingRepository()
    repository.duplicate_email = True

    with pytest.raises(
        DuplicateCustomerError
    ) as error:
        CustomerDuplicationPolicy(
            repository
        ).ensure_available(
            uuid.uuid4(),
            document_number=None,
            email=EmailAddress(
                "cliente@example.com"
            ),
        )

    assert error.value.details == {
        "field": "email"
    }


def test_forwards_customer_exclusion_on_update() -> None:
    repository = DuplicateCheckingRepository()

    CustomerDuplicationPolicy(
        repository
    ).ensure_available(
        uuid.uuid4(),
        document_number=DocumentNumber(
            "52998224725"
        ),
        email=EmailAddress(
            "cliente@example.com"
        ),
        exclude_customer_id=42,
    )

    assert repository.document_exclusion == 42
    assert repository.email_exclusion == 42
