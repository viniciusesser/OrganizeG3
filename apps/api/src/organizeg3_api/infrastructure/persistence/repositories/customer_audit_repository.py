"""Read-only repository for customer data auditing."""

from __future__ import annotations

from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.application.customer.data_audit import (
    CustomerAuditRecord,
)
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)


class SQLAlchemyCustomerAuditRepository:
    """Read raw customer columns without domain coercion."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def fetch_all(
        self,
    ) -> list[CustomerAuditRecord]:
        """Return every customer, including archived records."""

        statement = (
            select(
                CustomerModel.id.label(
                    "customer_id"
                ),
                CustomerModel.tenant_id.label(
                    "tenant_id"
                ),
                CustomerModel.code.label(
                    "code"
                ),
                CustomerModel.name.label(
                    "name"
                ),
                CustomerModel.customer_type.label(
                    "customer_type"
                ),
                CustomerModel.document_number.label(
                    "document_number"
                ),
                CustomerModel.email.label(
                    "email"
                ),
                CustomerModel.phone.label(
                    "phone"
                ),
                CustomerModel.deleted_at.label(
                    "deleted_at"
                ),
            )
            .order_by(CustomerModel.id)
        )

        rows = self._session.execute(
            statement
        ).mappings().all()

        return [
            CustomerAuditRecord(
                customer_id=cast(
                    int,
                    row["customer_id"],
                ),
                tenant_id=self._optional_text(
                    row["tenant_id"]
                ),
                code=self._optional_text(
                    row["code"]
                ),
                name=self._optional_text(
                    row["name"]
                ),
                customer_type=self._optional_text(
                    row["customer_type"]
                ),
                document_number=(
                    self._optional_text(
                        row["document_number"]
                    )
                ),
                email=self._optional_text(
                    row["email"]
                ),
                phone=self._optional_text(
                    row["phone"]
                ),
                is_archived=(
                    row["deleted_at"]
                    is not None
                ),
            )
            for row in rows
        ]

    @staticmethod
    def _optional_text(
        value: object,
    ) -> str | None:
        if value is None:
            return None

        return str(value)
