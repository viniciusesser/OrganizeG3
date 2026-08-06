"""Synchronous SQLAlchemy customer repository."""

from __future__ import annotations

from collections.abc import Sequence
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from organizeg3_api.core.exceptions import (
    ConcurrencyError,
    NotFoundError,
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
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)


class SQLAlchemyCustomerRepository(
    ICustomerRepository
):
    """SQLAlchemy adapter enforcing tenant isolation."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        statement = select(
            CustomerModel
        ).where(
            CustomerModel.tenant_id
            == tenant_id,
            CustomerModel.id
            == customer_id,
        )

        if not include_archived:
            statement = statement.where(
                CustomerModel.deleted_at.is_(
                    None
                )
            )

        model = self._session.execute(
            statement
        ).scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

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
        statement = select(
            CustomerModel
        ).where(
            CustomerModel.tenant_id
            == tenant_id,
            CustomerModel.deleted_at.is_(
                None
            ),
        )

        if not include_inactive:
            statement = statement.where(
                CustomerModel.is_active.is_(
                    True
                )
            )

        if customer_type is not None:
            statement = statement.where(
                CustomerModel.customer_type
                == customer_type.value
            )

        if search:
            pattern = (
                f"%{search.strip()}%"
            )

            statement = statement.where(
                or_(
                    CustomerModel.code.ilike(
                        pattern
                    ),
                    CustomerModel.name.ilike(
                        pattern
                    ),
                    CustomerModel.document_number.ilike(
                        pattern
                    ),
                    CustomerModel.email.ilike(
                        pattern
                    ),
                    CustomerModel.phone.ilike(
                        pattern
                    ),
                )
            )

        statement = (
            statement.order_by(
                CustomerModel.name,
                CustomerModel.id,
            )
            .offset(offset)
            .limit(limit)
        )

        models = self._session.execute(
            statement
        ).scalars().all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def exists_by_document(
        self,
        tenant_id: uuid.UUID,
        document_number: DocumentNumber,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        """Check normalized CPF/CNPJ across legacy formats."""

        normalized_column = func.replace(
            func.replace(
                func.replace(
                    CustomerModel.document_number,
                    ".",
                    "",
                ),
                "-",
                "",
            ),
            "/",
            "",
        )

        statement = select(
            CustomerModel.id
        ).where(
            CustomerModel.tenant_id
            == tenant_id,
            normalized_column
            == str(document_number),
        )

        if exclude_customer_id is not None:
            statement = statement.where(
                CustomerModel.id
                != exclude_customer_id
            )

        result = self._session.execute(
            statement.limit(1)
        ).scalar_one_or_none()

        return result is not None

    def exists_by_email(
        self,
        tenant_id: uuid.UUID,
        email: EmailAddress,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        """Check normalized case-insensitive email."""

        statement = select(
            CustomerModel.id
        ).where(
            CustomerModel.tenant_id
            == tenant_id,
            func.lower(
                func.trim(
                    CustomerModel.email
                )
            )
            == str(email),
        )

        if exclude_customer_id is not None:
            statement = statement.where(
                CustomerModel.id
                != exclude_customer_id
            )

        result = self._session.execute(
            statement.limit(1)
        ).scalar_one_or_none()

        return result is not None

    def save(
        self,
        customer: Customer,
        *,
        include_archived: bool = False,
    ) -> Customer:
        if customer.id is None:
            model = CustomerModel(
                tenant_id=customer.tenant_id,
                code=customer.code,
                name=customer.name,
                customer_type=(
                    customer.customer_type.value
                ),
                document_number=(
                    customer.document_number
                ),
                email=customer.email,
                phone=customer.phone,
                is_active=customer.is_active,
                row_version=customer.row_version,
                deleted_at=customer.deleted_at,
            )

            self._session.add(model)

        else:
            statement = select(
                CustomerModel
            ).where(
                CustomerModel.id
                == customer.id,
                CustomerModel.tenant_id
                == customer.tenant_id,
            )

            if not include_archived:
                statement = statement.where(
                    CustomerModel.deleted_at.is_(
                        None
                    )
                )

            existing_model = (
                self._session.execute(
                    statement
                ).scalar_one_or_none()
            )

            if existing_model is None:
                raise NotFoundError(
                    "Cliente não encontrado para a empresa informada."
                )

            model = existing_model

            if (
                model.row_version
                != customer.row_version
            ):
                raise ConcurrencyError(
                    "O cliente foi alterado por outro processo.",
                    details={
                        "expected_version": (
                            customer.row_version
                        ),
                        "current_version": (
                            model.row_version
                        ),
                    },
                )

            model.name = customer.name
            model.code = customer.code
            model.customer_type = (
                customer.customer_type.value
            )
            model.document_number = (
                customer.document_number
            )
            model.email = customer.email
            model.phone = customer.phone
            model.is_active = (
                customer.is_active
            )
            model.deleted_at = (
                customer.deleted_at
            )

        try:
            self._session.flush()
        except StaleDataError as exception:
            raise ConcurrencyError(
                "O cliente foi alterado por outro processo durante a gravação."
            ) from exception

        self._session.refresh(model)

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: CustomerModel,
    ) -> Customer:
        return Customer(
            id=model.id,
            tenant_id=model.tenant_id,
            code=model.code,
            name=model.name,
            customer_type=CustomerType(
                model.customer_type
            ),
            document_number=(
                model.document_number
            ),
            email=model.email,
            phone=model.phone,
            is_active=model.is_active,
            row_version=model.row_version,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
            _allow_legacy_contacts=True,
        )
