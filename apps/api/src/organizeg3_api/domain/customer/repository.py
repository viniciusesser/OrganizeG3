"""Repository contract for customer persistence operations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
import uuid

from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)
from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
)


class ICustomerRepository(ABC):
    """Port interface for customer persistence operations."""

    @abstractmethod
    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        """Fetch one customer within a tenant scope."""

    @abstractmethod
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
        """List and search non-archived customers."""

    @abstractmethod
    def save(
        self,
        customer: Customer,
        *,
        include_archived: bool = False,
    ) -> Customer:
        """Persist or update a customer domain entity."""

    def exists_by_document(
        self,
        tenant_id: uuid.UUID,
        document_number: DocumentNumber,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        """Return whether a document is reserved in the tenant."""

        del tenant_id
        del document_number
        del exclude_customer_id

        return False

    def exists_by_email(
        self,
        tenant_id: uuid.UUID,
        email: EmailAddress,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        """Return whether an email is reserved in the tenant."""

        del tenant_id
        del email
        del exclude_customer_id

        return False
