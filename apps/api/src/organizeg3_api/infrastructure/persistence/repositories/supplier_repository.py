"""SQLAlchemy repository for tenant suppliers."""

from __future__ import annotations

import re
from typing import cast
import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from organizeg3_api.domain.supplier.entity import Supplier
from organizeg3_api.domain.supplier.repository import SupplierRepository
from organizeg3_api.domain.supplier.value_objects import (
    SupplierCode,
    SupplierDocument,
)
from organizeg3_api.infrastructure.persistence.models.supplier import (
    SupplierModel,
)

_NON_DIGIT_PATTERN = re.compile(r"\D+")


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
            select(SupplierModel)
            .where(
                SupplierModel.id == supplier_id,
                SupplierModel.tenant_id == tenant_id,
            )
            .limit(1)
        )

        model = self._session.scalar(
            statement
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
            select(SupplierModel)
            .where(
                SupplierModel.tenant_id == tenant_id,
                SupplierModel.document_number
                == normalized_document,
            )
            .limit(1)
        )

        model = self._session.scalar(
            statement
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Supplier]:
        """List suppliers within one tenant."""

        statement = select(
            SupplierModel
        ).where(
            SupplierModel.tenant_id
            == tenant_id
        )

        if not include_inactive:
            statement = statement.where(
                SupplierModel.is_active.is_(
                    True
                )
            )

        search_value = (
            search.strip()
            if search is not None
            else ""
        )

        if search_value:
            pattern = f"%{search_value}%"

            conditions: list[
                ColumnElement[bool]
            ] = [
                SupplierModel.code.ilike(
                    pattern
                ),
                SupplierModel.name.ilike(
                    pattern
                ),
                SupplierModel.trade_name.ilike(
                    pattern
                ),
                SupplierModel.legal_name.ilike(
                    pattern
                ),
                SupplierModel.email.ilike(
                    pattern
                ),
                SupplierModel.invoice_email.ilike(
                    pattern
                ),
                SupplierModel.contact_name.ilike(
                    pattern
                ),
            ]

            document_digits = (
                _NON_DIGIT_PATTERN.sub(
                    "",
                    search_value,
                )
            )

            if document_digits:
                conditions.append(
                    SupplierModel.document_number.contains(
                        document_digits
                    )
                )

            statement = statement.where(
                or_(
                    *conditions
                )
            )

        statement = (
            statement
            .order_by(
                SupplierModel.name,
                SupplierModel.code,
                SupplierModel.id,
            )
            .limit(limit)
            .offset(offset)
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(
                model
            )
            for model in models
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_supplier_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a supplier code already exists."""

        normalized_code = SupplierCode(
            code
        ).value

        statement = select(
            SupplierModel.id
        ).where(
            SupplierModel.tenant_id
            == tenant_id,
            SupplierModel.code
            == normalized_code,
        )

        if exclude_supplier_id is not None:
            statement = statement.where(
                SupplierModel.id
                != exclude_supplier_id
            )

        statement = statement.limit(1)

        return (
            self._session.scalar(
                statement
            )
            is not None
        )

    def exists_by_document(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
        exclude_supplier_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a supplier document already exists."""

        normalized_document = SupplierDocument(
            document_number
        ).value

        statement = select(
            SupplierModel.id
        ).where(
            SupplierModel.tenant_id
            == tenant_id,
            SupplierModel.document_number
            == normalized_document,
        )

        if exclude_supplier_id is not None:
            statement = statement.where(
                SupplierModel.id
                != exclude_supplier_id
            )

        statement = statement.limit(1)

        return (
            self._session.scalar(
                statement
            )
            is not None
        )

    def add(
        self,
        supplier: Supplier,
    ) -> Supplier:
        """Persist a new supplier."""

        if supplier.id is None:
            raise ValueError(
                "Supplier id is required before persistence."
            )

        if supplier.created_at is None:
            raise ValueError(
                "Supplier created_at is required before persistence."
            )

        if supplier.updated_at is None:
            raise ValueError(
                "Supplier updated_at is required before persistence."
            )

        model = SupplierModel(
            id=supplier.id,
            tenant_id=supplier.tenant_id,
            code=supplier.code,
            name=supplier.name,
            trade_name=supplier.trade_name,
            legal_name=supplier.legal_name,
            document_number=supplier.document_number,
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

    def save(
        self,
        supplier: Supplier,
    ) -> Supplier:
        """Persist changes to an existing supplier."""

        if supplier.id is None:
            raise ValueError(
                "Supplier id is required before persistence."
            )

        if supplier.updated_at is None:
            raise ValueError(
                "Supplier updated_at is required before persistence."
            )

        statement = (
            select(SupplierModel)
            .where(
                SupplierModel.id == supplier.id,
                SupplierModel.tenant_id
                == supplier.tenant_id,
            )
            .limit(1)
        )

        model = self._session.scalar(
            statement
        )

        if model is None:
            raise ValueError(
                "Supplier does not exist for persistence."
            )

        model.code = supplier.code
        model.name = supplier.name
        model.trade_name = supplier.trade_name
        model.legal_name = supplier.legal_name
        model.document_number = (
            supplier.document_number
        )
        model.state_registration = (
            supplier.state_registration
        )
        model.email = supplier.email
        model.invoice_email = supplier.invoice_email
        model.phone = supplier.phone
        model.secondary_phone = (
            supplier.secondary_phone
        )
        model.website = supplier.website
        model.contact_name = supplier.contact_name
        model.postal_code = supplier.postal_code
        model.street = supplier.street
        model.number = supplier.number
        model.district = supplier.district
        model.city = supplier.city
        model.state = supplier.state
        model.is_active = supplier.is_active
        model.updated_at = supplier.updated_at

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
