"""Integration tests for supplier persistence."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.supplier.entity import (
    Supplier,
)
from organizeg3_api.infrastructure.persistence.models import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemySupplierRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def create_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    name: str,
) -> TenantRecordModel:
    """Create one active tenant."""

    tenant = TenantRecordModel(
        id=tenant_id,
        name=name,
        status="ACTIVE",
        is_active=True,
    )

    session.add(
        tenant
    )
    session.flush()

    return tenant


def test_adds_and_recovers_complete_supplier(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Supplier",
    )

    supplier = Supplier.create(
        tenant_id=tenant_id,
        code="FORN-001",
        name="Fornecedor Teste",
        trade_name="Loja Teste",
        legal_name="Fornecedor Teste Ltda",
        document_number="04.252.011/0001-10",
        state_registration="123456",
        email="comercial@example.com",
        invoice_email="nfe@example.com",
        phone="(18) 99999-1234",
        secondary_phone="(18) 3222-1234",
        website="https://example.com",
        contact_name="Contato",
        postal_code="19200-000",
        street="Rua Teste",
        number="100",
        district="Centro",
        city="Rosana",
        state="SP",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    saved = repository.add(
        supplier
    )

    assert saved.id is not None

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        supplier_id=saved.id,
    )

    assert recovered is not None

    assert recovered.id == supplier.id
    assert recovered.tenant_id == tenant_id
    assert recovered.code == "FORN-001"
    assert recovered.name == "Fornecedor Teste"
    assert recovered.trade_name == "Loja Teste"

    assert (
        recovered.legal_name
        == "Fornecedor Teste Ltda"
    )

    assert (
        recovered.document_number
        == "04252011000110"
    )

    assert (
        recovered.state_registration
        == "123456"
    )

    assert (
        recovered.email
        == "comercial@example.com"
    )

    assert (
        recovered.invoice_email
        == "nfe@example.com"
    )

    assert recovered.phone == "18999991234"
    assert recovered.secondary_phone == "1832221234"
    assert recovered.website == "https://example.com"
    assert recovered.contact_name == "Contato"
    assert recovered.postal_code == "19200000"
    assert recovered.street == "Rua Teste"
    assert recovered.number == "100"
    assert recovered.district == "Centro"
    assert recovered.city == "Rosana"
    assert recovered.state == "SP"
    assert recovered.is_active is True


def test_supplier_lookup_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    saved = repository.add(
        Supplier.create(
            tenant_id=tenant_a_id,
            code="FORN-A",
            name="Fornecedor A",
        )
    )

    assert saved.id is not None

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b_id,
        supplier_id=saved.id,
    )

    assert result is None


def test_finds_supplier_by_normalized_document(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_id,
            code="FORN-001",
            name="Fornecedor",
            document_number="04.252.011/0001-10",
        )
    )

    recovered = (
        repository.get_by_document_for_tenant(
            tenant_id=tenant_id,
            document_number="04.252.011/0001-10",
        )
    )

    assert recovered is not None

    assert (
        recovered.document_number
        == "04252011000110"
    )


def test_document_lookup_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_a_id,
            code="FORN-A",
            name="Fornecedor A",
            document_number="04.252.011/0001-10",
        )
    )

    result = (
        repository.get_by_document_for_tenant(
            tenant_id=tenant_b_id,
            document_number="04.252.011/0001-10",
        )
    )

    assert result is None


def test_allows_same_code_in_different_tenants(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_a_id,
            code="FORN-001",
            name="Fornecedor A",
        )
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_b_id,
            code="FORN-001",
            name="Fornecedor B",
        )
    )


def test_rejects_duplicate_code_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_id,
            code="FORN-001",
            name="Fornecedor A",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Supplier.create(
                tenant_id=tenant_id,
                code="forn-001",
                name="Fornecedor B",
            )
        )


def test_rejects_duplicate_document_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_id,
            code="FORN-001",
            name="Fornecedor A",
            document_number="04.252.011/0001-10",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Supplier.create(
                tenant_id=tenant_id,
                code="FORN-002",
                name="Fornecedor B",
                document_number="04252011000110",
            )
        )


def test_allows_same_document_in_different_tenants(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_a_id,
            code="FORN-A",
            name="Fornecedor A",
            document_number="04.252.011/0001-10",
        )
    )

    repository.add(
        Supplier.create(
            tenant_id=tenant_b_id,
            code="FORN-B",
            name="Fornecedor B",
            document_number="04.252.011/0001-10",
        )
    )


def test_persists_supplier_without_document(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemySupplierRepository(
        session
    )

    first = repository.add(
        Supplier.create(
            tenant_id=tenant_id,
            code="FORN-001",
            name="Fornecedor A",
        )
    )

    second = repository.add(
        Supplier.create(
            tenant_id=tenant_id,
            code="FORN-002",
            name="Fornecedor B",
        )
    )

    assert first.document_number is None
    assert second.document_number is None
