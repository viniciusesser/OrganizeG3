"""Create-customer use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.customer.duplication_policy import (
    CustomerDuplicationPolicy,
)
from organizeg3_api.application.customer.schemas import (
    CustomerCreate,
)
from organizeg3_api.core.exceptions import (
    ValidationError,
)
from organizeg3_api.domain.customer.entity import (
    Customer,
)
from organizeg3_api.domain.customer.repository import (
    ICustomerRepository,
)
from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
)


class CreateCustomerUseCase:
    """Create and persist a customer for the tenant."""

    def __init__(
        self,
        repository: ICustomerRepository,
    ) -> None:
        self._repository = repository
        self._duplication_policy = (
            CustomerDuplicationPolicy(repository)
        )

    def execute(
        self,
        tenant_id: uuid.UUID,
        payload: CustomerCreate,
    ) -> Customer:
        """Execute creation using the tenant context."""

        unique_code = (
            f"CUST-{uuid.uuid4().hex[:8].upper()}"
        )

        try:
            customer = Customer(
                tenant_id=tenant_id,
                code=unique_code,
                name=payload.name,
                customer_type=payload.customer_type,
                document_number=(
                    payload.document_number
                ),
                email=payload.email,
                phone=payload.phone,
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        self._duplication_policy.ensure_available(
            tenant_id,
            document_number=(
                customer.document_number
                if isinstance(
                    customer.document_number,
                    DocumentNumber,
                )
                else None
            ),
            email=(
                customer.email
                if isinstance(
                    customer.email,
                    EmailAddress,
                )
                else None
            ),
        )

        return self._repository.save(customer)
