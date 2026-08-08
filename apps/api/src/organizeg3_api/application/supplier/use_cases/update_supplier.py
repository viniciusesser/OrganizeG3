"""Update supplier application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.supplier.schemas import (
    SupplierUpdate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.supplier import (
    Supplier,
    SupplierRepository,
)


class UpdateSupplierUseCase:
    """Update supplier details inside one tenant."""

    def __init__(
        self,
        repository: SupplierRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        supplier_id: uuid.UUID,
        payload: SupplierUpdate,
    ) -> Supplier:
        """Validate and persist a partial supplier update."""

        if not payload.model_fields_set:
            raise ValidationError(
                "Nenhum campo foi informado para atualização."
            )

        supplier = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                supplier_id=supplier_id,
            )
        )

        if supplier is None:
            raise NotFoundError(
                "Fornecedor não encontrado."
            )

        code = (
            payload.code
            if "code" in payload.model_fields_set
            else supplier.code
        )

        name = (
            payload.name
            if "name" in payload.model_fields_set
            else supplier.name
        )

        if code is None:
            raise ValidationError(
                "O código do fornecedor é obrigatório."
            )

        if name is None:
            raise ValidationError(
                "O nome do fornecedor é obrigatório."
            )

        try:
            supplier.update_details(
                code=code,
                name=name,
                trade_name=self._value(
                    payload,
                    supplier,
                    "trade_name",
                ),
                legal_name=self._value(
                    payload,
                    supplier,
                    "legal_name",
                ),
                document_number=self._value(
                    payload,
                    supplier,
                    "document_number",
                ),
                state_registration=self._value(
                    payload,
                    supplier,
                    "state_registration",
                ),
                email=self._value(
                    payload,
                    supplier,
                    "email",
                ),
                invoice_email=self._value(
                    payload,
                    supplier,
                    "invoice_email",
                ),
                phone=self._value(
                    payload,
                    supplier,
                    "phone",
                ),
                secondary_phone=self._value(
                    payload,
                    supplier,
                    "secondary_phone",
                ),
                website=self._value(
                    payload,
                    supplier,
                    "website",
                ),
                contact_name=self._value(
                    payload,
                    supplier,
                    "contact_name",
                ),
                postal_code=self._value(
                    payload,
                    supplier,
                    "postal_code",
                ),
                street=self._value(
                    payload,
                    supplier,
                    "street",
                ),
                number=self._value(
                    payload,
                    supplier,
                    "number",
                ),
                district=self._value(
                    payload,
                    supplier,
                    "district",
                ),
                city=self._value(
                    payload,
                    supplier,
                    "city",
                ),
                state=self._value(
                    payload,
                    supplier,
                    "state",
                ),
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
            exclude_supplier_id=supplier_id,
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
                exclude_supplier_id=supplier_id,
            )
        ):
            raise ConflictError(
                "Já existe um fornecedor com este documento.",
                details={
                    "field": "document_number",
                    "value": supplier.document_number,
                },
            )

        return self._repository.save(
            supplier
        )

    @staticmethod
    def _value(
        payload: SupplierUpdate,
        supplier: Supplier,
        field_name: str,
    ) -> str | None:
        if field_name in payload.model_fields_set:
            value = getattr(
                payload,
                field_name,
            )

            if value is None:
                return None

            return str(
                value
            )

        current_value = getattr(
            supplier,
            field_name,
        )

        if current_value is None:
            return None

        return str(
            current_value
        )
