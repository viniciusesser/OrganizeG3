"""Integration tests for customer audit persistence."""

from datetime import UTC, datetime
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_audit_repository import (
    SQLAlchemyCustomerAuditRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def test_fetches_raw_active_and_archived_customer_data(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    now = datetime.now(UTC)

    active_model = CustomerModel(
        tenant_id=tenant_id,
        code="CUST-ACTIVE",
        name="Cliente Ativo",
        customer_type="INDIVIDUAL",
        document_number="529.982.247-25",
        email="CLIENTE@EXAMPLE.COM",
        phone="(18) 99999-0000",
        is_active=True,
        row_version=1,
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )

    archived_model = CustomerModel(
        tenant_id=tenant_id,
        code="CUST-ARCHIVED",
        name="Cliente Arquivado",
        customer_type="CORPORATE",
        document_number="123",
        email="EMAIL LEGADO",
        phone="SEM TELEFONE",
        is_active=False,
        row_version=1,
        created_at=now,
        updated_at=now,
        deleted_at=now,
    )

    session.add_all(
        [
            active_model,
            archived_model,
        ]
    )
    session.flush()

    records = (
        SQLAlchemyCustomerAuditRepository(
            session
        ).fetch_all()
    )

    assert len(records) == 2

    records_by_code = {
        record.code: record
        for record in records
    }

    active = records_by_code["CUST-ACTIVE"]
    archived = records_by_code[
        "CUST-ARCHIVED"
    ]

    assert (
        active.document_number
        == "529.982.247-25"
    )
    assert (
        active.email
        == "CLIENTE@EXAMPLE.COM"
    )
    assert active.phone == "(18) 99999-0000"
    assert active.customer_type == "INDIVIDUAL"
    assert active.is_archived is False

    assert archived.document_number == "123"
    assert archived.email == "EMAIL LEGADO"
    assert archived.phone == "SEM TELEFONE"
    assert archived.customer_type == "CORPORATE"
    assert archived.is_archived is True
