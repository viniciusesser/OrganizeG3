"""SQLAlchemy repository for tenant suppliers."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.supplier.entity import (
    Supplier,
)
from organizeg3_api.domain.supplier.repository import (
    SupplierRepository,
)
from organizeg3_api.domain.supplier.value_objects import (
    SupplierDocument,
)
from organizeg3_api.infrastructure.persistence.models.supplier import (
    SupplierModel,
)


class SQLAlchemySupplierRepository(
    SupplierRepository
):
    """Persist supplier data using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        supplier_id: uuid.UUID,
    ) -> Supplier | None:
        """Return one supplier belonging to a tenant."""

        statement = (
            select(
                SupplierModel
            )
            .where(
                SupplierModel.id
                == supplier_id,
                SupplierModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def get_by_document_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
    ) -> Supplier | None:
        """Return one supplier by CPF or CNPJ."""

        normalized_document = SupplierDocument(
            document_number
        ).value

        statement = (
            select(
                SupplierModel
            )
            .where(
                SupplierModel.tenant_id
                == tenant_id,
                SupplierModel.document_number
                == normalized_document,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def add(
        self,
        supplier: Supplier,
    ) -> Supplier:
        """Persist a new supplier."""

        model = SupplierModel(
            id=supplier.id,
            tenant_id=supplier.tenant_id,
            code=supplier.code,
            name=supplier.name,
            trade_name=supplier.trade_name,
            legal_name=supplier.legal_name,
            document_number=(
                supplier.document_number
            ),
            state_registration=(
                supplier.state_registration
            ),
            email=supplier.email,
            invoice_email=supplier.invoice_email,
            phone=supplier.phone,
            secondary_phone=(
                supplier.secondary_phone
            ),
            website=supplier.website,
            contact_name=supplier.contact_name,
            postal_code=supplier.postal_code,
            street=supplier.street,
            number=supplier.number,
            district=supplier.district,
            city=supplier.city,
            state=supplier.state,
            is_active=supplier.is_active,
            created_at=supplier.created_at,
            updated_at=supplier.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()

        return self._to_domain(
            model
        )

    @staticmethod
    def _to_domain(
        model: SupplierModel,
    ) -> Supplier:
        """Convert persistence model to domain entity."""

        return Supplier(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            code=model.code,
            name=model.name,
            trade_name=model.trade_name,
            legal_name=model.legal_name,
            document_number=model.document_number,
            state_registration=(
                model.state_registration
            ),
            email=model.email,
            invoice_email=model.invoice_email,
            phone=model.phone,
            secondary_phone=model.secondary_phone,
            website=model.website,
            contact_name=model.contact_name,
            postal_code=model.postal_code,
            street=model.street,
            number=model.number,
            district=model.district,
            city=model.city,
            state=model.state,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
