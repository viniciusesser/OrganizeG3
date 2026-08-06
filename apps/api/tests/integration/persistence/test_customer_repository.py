"""Integration tests for SQLAlchemy customer persistence."""

from datetime import UTC, datetime
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.core.exceptions import (
    ConcurrencyError,
    NotFoundError,
)
from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def make_customer(
    tenant_id: uuid.UUID,
    **changes: object,
) -> Customer:
    values: dict[str, object] = {
        "tenant_id": tenant_id,
        "code": (
            f"CUST-{uuid.uuid4().hex[:8].upper()}"
        ),
        "name": "Cliente Teste",
        "customer_type": (
            CustomerType.INDIVIDUAL
        ),
    }

    values.update(changes)

    return Customer(
        **values
    )  # type: ignore[arg-type]


def test_creates_and_recovers_customer(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    saved = repository.save(
        make_customer(
            tenant_id,
            email="cliente@example.com",
        )
    )

    recovered = repository.get_by_id(
        tenant_id,
        saved.id or 0,
    )

    assert saved.id is not None
    assert recovered is not None
    assert recovered.id == saved.id
    assert recovered.tenant_id == tenant_id
    assert (
        recovered.email
        == "cliente@example.com"
    )


def test_does_not_recover_customer_from_other_tenant(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    saved = repository.save(
        make_customer(tenant_id)
    )

    assert (
        repository.get_by_id(
            other_tenant_id,
            saved.id or 0,
        )
        is None
    )


def test_lists_only_current_tenant(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            name="Cliente A",
        )
    )

    repository.save(
        make_customer(
            other_tenant_id,
            name="Cliente B",
        )
    )

    result = repository.list_all(
        tenant_id
    )

    assert [
        customer.name
        for customer in result
    ] == ["Cliente A"]


def test_excludes_inactive_by_default_and_can_include_them(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            name="Ativo",
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            name="Inativo",
            is_active=False,
        )
    )

    active_only = repository.list_all(
        tenant_id
    )

    all_customers = repository.list_all(
        tenant_id,
        include_inactive=True,
    )

    assert [
        customer.name
        for customer in active_only
    ] == ["Ativo"]

    assert [
        customer.name
        for customer in all_customers
    ] == [
        "Ativo",
        "Inativo",
    ]


def test_excludes_soft_deleted_customer(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    session.add(
        CustomerModel(
            tenant_id=tenant_id,
            code="CUST-DELETED",
            name="Excluído",
            customer_type="INDIVIDUAL",
            is_active=False,
            deleted_at=datetime.now(UTC),
        )
    )

    session.flush()

    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    assert (
        repository.list_all(
            tenant_id,
            include_inactive=True,
        )
        == []
    )


def test_rejects_cross_tenant_update(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    saved = repository.save(
        make_customer(tenant_id)
    )

    forged = make_customer(
        other_tenant_id,
        id=saved.id,
        code=saved.code,
        row_version=saved.row_version,
    )

    with pytest.raises(
        NotFoundError
    ):
        repository.save(forged)


def test_increments_optimistic_version_on_update(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    saved = repository.save(
        make_customer(tenant_id)
    )

    saved.name = "Cliente Atualizado"

    updated = repository.save(saved)

    assert (
        updated.name
        == "Cliente Atualizado"
    )
    assert updated.row_version == 2


def test_rejects_stale_optimistic_version(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    saved = repository.save(
        make_customer(tenant_id)
    )

    stale_version = saved.row_version

    saved.name = "Primeira alteração"

    repository.save(saved)

    stale = make_customer(
        tenant_id,
        id=saved.id,
        code=saved.code,
        name="Alteração antiga",
        row_version=stale_version,
    )

    with pytest.raises(
        ConcurrencyError
    ):
        repository.save(stale)


def test_searches_by_name_code_document_email_and_phone(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            code="CLI-METAL",
            name="Metalúrgica Horizonte",
            document_number=(
                "11222333000181"
            ),
            email=(
                "vendas@horizonte.test"
            ),
            phone="18999990000",
            customer_type=(
                CustomerType.CORPORATE
            ),
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            name="Cliente Residencial",
        )
    )

    assert [
        item.name
        for item in repository.list_all(
            tenant_id,
            search="metal",
        )
    ] == [
        "Metalúrgica Horizonte"
    ]

    assert [
        item.name
        for item in repository.list_all(
            tenant_id,
            search="11222333",
        )
    ] == [
        "Metalúrgica Horizonte"
    ]

    assert [
        item.name
        for item in repository.list_all(
            tenant_id,
            search="horizonte.test",
        )
    ] == [
        "Metalúrgica Horizonte"
    ]

    assert [
        item.name
        for item in repository.list_all(
            tenant_id,
            search="99999",
        )
    ] == [
        "Metalúrgica Horizonte"
    ]


def test_filters_customer_type_and_applies_pagination(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = (
        SQLAlchemyCustomerRepository(
            session
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            name="Empresa A",
            customer_type=(
                CustomerType.CORPORATE
            ),
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            name="Empresa B",
            customer_type=(
                CustomerType.CORPORATE
            ),
        )
    )

    repository.save(
        make_customer(
            tenant_id,
            name="Pessoa C",
        )
    )

    result = repository.list_all(
        tenant_id,
        customer_type=(
            CustomerType.CORPORATE
        ),
        limit=1,
        offset=1,
    )

    assert [
        customer.name
        for customer in result
    ] == ["Empresa B"]
