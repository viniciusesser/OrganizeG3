"""Customer duplicate-prevention policy."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    DuplicateCustomerError,
)
from organizeg3_api.domain.customer.repository import (
    ICustomerRepository,
)
from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
)


class CustomerDuplicationPolicy:
    """Ensure normalized identity data is unique per tenant."""

    def __init__(
        self,
        repository: ICustomerRepository,
    ) -> None:
        self._repository = repository

    def ensure_available(
        self,
        tenant_id: uuid.UUID,
        *,
        document_number: DocumentNumber | None,
        email: EmailAddress | None,
        exclude_customer_id: int | None = None,
    ) -> None:
        """Reject duplicate document or email."""

        if (
            document_number is not None
            and self._repository.exists_by_document(
                tenant_id,
                document_number,
                exclude_customer_id=exclude_customer_id,
            )
        ):
            raise DuplicateCustomerError(
                "Já existe um cliente com este CPF/CNPJ.",
                details={
                    "field": "document_number",
                },
            )

        if (
            email is not None
            and self._repository.exists_by_email(
                tenant_id,
                email,
                exclude_customer_id=exclude_customer_id,
            )
        ):
            raise DuplicateCustomerError(
                "Já existe um cliente com este e-mail.",
                details={
                    "field": "email",
                },
            )
