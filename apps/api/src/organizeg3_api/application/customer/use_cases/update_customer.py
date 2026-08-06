"""Update-customer use case."""

from __future__ import annotations

from dataclasses import replace
import uuid

from organizeg3_api.application.customer.concurrency import (
    ensure_customer_version,
)
from organizeg3_api.application.customer.duplication_policy import (
    CustomerDuplicationPolicy,
)
from organizeg3_api.application.customer.schemas import (
    CustomerUpdate,
)
from organizeg3_api.core.exceptions import (
    NotFoundError,
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


class UpdateCustomerUseCase:
    """Update customer data within the tenant."""

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
        customer_id: int,
        payload: CustomerUpdate,
    ) -> Customer:
        """Apply a partial update with version validation."""

        customer = self._repository.get_by_id(
            tenant_id,
            customer_id,
        )

        if customer is None:
            raise NotFoundError(
                "Cliente não encontrado."
            )

        ensure_customer_version(
            customer,
            payload.row_version,
        )

        changed_fields = (
            payload.model_fields_set
            - {"row_version"}
        )

        if not changed_fields:
            raise ValidationError(
                "Informe ao menos um campo para atualizar."
            )

        updated_name = customer.name

        if "name" in changed_fields:
            if payload.name is None:
                raise ValidationError(
                    "O nome do cliente não pode ser nulo."
                )

            updated_name = payload.name

        updated_customer_type = (
            customer.customer_type
        )

        if "customer_type" in changed_fields:
            if payload.customer_type is None:
                raise ValidationError(
                    "O tipo de cliente não pode ser nulo."
                )

            updated_customer_type = (
                payload.customer_type
            )

        candidate = replace(customer)

        try:
            candidate.update_profile(
                name=updated_name,
                customer_type=updated_customer_type,
                document_number=(
                    payload.document_number
                    if "document_number"
                    in changed_fields
                    else customer.document_number
                ),
                email=(
                    payload.email
                    if "email" in changed_fields
                    else customer.email
                ),
                phone=(
                    payload.phone
                    if "phone" in changed_fields
                    else customer.phone
                ),
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
                candidate.document_number
                if isinstance(
                    candidate.document_number,
                    DocumentNumber,
                )
                else None
            ),
            email=(
                candidate.email
                if isinstance(
                    candidate.email,
                    EmailAddress,
                )
                else None
            ),
            exclude_customer_id=customer_id,
        )

        return self._repository.save(
            candidate
        )
