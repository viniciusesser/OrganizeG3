"""Create supplier application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.supplier.schemas import (
    SupplierCreate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    ValidationError,
)
from organizeg3_api.domain.supplier import (
    Supplier,
    SupplierRepository,
)


class CreateSupplierUseCase:
    """Create one supplier inside a tenant."""

    def __init__(
        self,
        repository: SupplierRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        payload: SupplierCreate,
    ) -> Supplier:
        """Create and persist a supplier."""

        try:
            supplier = Supplier.create(
                tenant_id=tenant_id,
                code=payload.code,
                name=payload.name,
                trade_name=payload.trade_name,
                legal_name=payload.legal_name,
                document_number=payload.document_number,
                state_registration=payload.state_registration,
                email=payload.email,
                invoice_email=payload.invoice_email,
                phone=payload.phone,
                secondary_phone=payload.secondary_phone,
                website=payload.website,
                contact_name=payload.contact_name,
                postal_code=payload.postal_code,
                street=payload.street,
                number=payload.number,
                district=payload.district,
                city=payload.city,
                state=payload.state,
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        if self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=supplier.code,
        ):
            raise ConflictError(
                "Já existe um fornecedor com este código.",
                details={
                    "field": "code",
                    "value": supplier.code,
                },
            )

        if (
            supplier.document_number is not None
            and self._repository.exists_by_document(
                tenant_id=tenant_id,
                document_number=supplier.document_number,
            )
        ):
            raise ConflictError(
                "Já existe um fornecedor com este documento.",
                details={
                    "field": "document_number",
                    "value": supplier.document_number,
                },
            )

        return self._repository.add(
            supplier
        )
