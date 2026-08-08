"""Unit tests for supplier application use cases."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.application.supplier.schemas import (
    SupplierCreate,
    SupplierUpdate,
)
from organizeg3_api.application.supplier.use_cases import (
    CreateSupplierUseCase,
    DeactivateSupplierUseCase,
    GetSupplierUseCase,
    ListSuppliersUseCase,
    ReactivateSupplierUseCase,
    UpdateSupplierUseCase,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.supplier import Supplier


class FakeSupplierRepository:
    """In-memory supplier repository used by application tests."""

    def __init__(self) -> None:
        self.suppliers: dict[uuid.UUID, Supplier] = {}

        self.last_list_tenant_id: uuid.UUID | None = None
        self.last_include_inactive = False
        self.last_search: str | None = None
        self.last_limit = 0
        self.last_offset = 0

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        supplier_id: uuid.UUID,
    ) -> Supplier | None:
        supplier = self.suppliers.get(
            supplier_id
        )

        if supplier is None:
            return None

        if supplier.tenant_id != tenant_id:
            return None

        return supplier

    def get_by_document_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
    ) -> Supplier | None:
        normalized_document = "".join(
            character
            for character in document_number
            if character.isdigit()
        )

        for supplier in self.suppliers.values():
            if supplier.tenant_id != tenant_id:
                continue

            if (
                supplier.document_number
                == normalized_document
            ):
                return supplier

        return None

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Supplier]:
        self.last_list_tenant_id = tenant_id
        self.last_include_inactive = (
            include_inactive
        )
        self.last_search = search
        self.last_limit = limit
        self.last_offset = offset

        suppliers = [
            supplier
            for supplier in self.suppliers.values()
            if supplier.tenant_id == tenant_id
        ]

        if not include_inactive:
            suppliers = [
                supplier
                for supplier in suppliers
                if supplier.is_active
            ]

        if search is not None:
            normalized_search = (
                search.strip().lower()
            )

            if normalized_search:
                suppliers = [
                    supplier
                    for supplier in suppliers
                    if self._matches_search(
                        supplier,
                        normalized_search,
                    )
                ]

        suppliers.sort(
            key=lambda supplier: (
                supplier.name,
                supplier.code,
            )
        )

        return suppliers[
            offset : offset + limit
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_supplier_id: uuid.UUID | None = None,
    ) -> bool:
        normalized_code = code.strip().upper()

        return any(
            supplier.tenant_id == tenant_id
            and supplier.code == normalized_code
            and supplier.id
            != exclude_supplier_id
            for supplier in self.suppliers.values()
        )

    def exists_by_document(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
        exclude_supplier_id: uuid.UUID | None = None,
    ) -> bool:
        normalized_document = "".join(
            character
            for character in document_number
            if character.isdigit()
        )

        return any(
            supplier.tenant_id == tenant_id
            and supplier.document_number
            == normalized_document
            and supplier.id
            != exclude_supplier_id
            for supplier in self.suppliers.values()
        )

    def add(
        self,
        supplier: Supplier,
    ) -> Supplier:
        assert supplier.id is not None

        self.suppliers[
            supplier.id
        ] = supplier

        return supplier

    def save(
        self,
        supplier: Supplier,
    ) -> Supplier:
        assert supplier.id is not None

        self.suppliers[
            supplier.id
        ] = supplier

        return supplier

    @staticmethod
    def _matches_search(
        supplier: Supplier,
        search: str,
    ) -> bool:
        values = [
            supplier.code,
            supplier.name,
            supplier.trade_name,
            supplier.legal_name,
            supplier.document_number,
            supplier.email,
            supplier.invoice_email,
            supplier.contact_name,
        ]

        return any(
            search in value.lower()
            for value in values
            if value is not None
        )


def create_supplier(
    repository: FakeSupplierRepository,
    *,
    tenant_id: uuid.UUID | None = None,
    code: str = "FORN-001",
    name: str = "Fornecedor Teste",
    document_number: str | None = None,
    email: str | None = None,
) -> Supplier:
    """Create and persist one supplier for tests."""

    supplier = Supplier.create(
        tenant_id=(
            tenant_id
            if tenant_id is not None
            else uuid.uuid4()
        ),
        code=code,
        name=name,
        document_number=document_number,
        email=email,
    )

    repository.add(
        supplier
    )

    return supplier


def test_create_supplier_normalizes_and_persists() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    use_case = CreateSupplierUseCase(
        repository
    )

    result = use_case.execute(
        tenant_id,
        SupplierCreate(
            code=" forn-001 ",
            name=" Fornecedor Teste ",
            document_number="04.252.011/0001-10",
            email=" COMERCIAL@EXAMPLE.COM ",
            phone="(18) 99999-1234",
            postal_code="19200-000",
            state="sp",
        ),
    )

    assert result.id is not None
    assert result.tenant_id == tenant_id
    assert result.code == "FORN-001"
    assert result.name == "Fornecedor Teste"

    assert (
        result.document_number
        == "04252011000110"
    )

    assert (
        result.email
        == "comercial@example.com"
    )

    assert result.phone == "18999991234"
    assert result.postal_code == "19200000"
    assert result.state == "SP"

    assert result.id in repository.suppliers


def test_create_supplier_rejects_duplicate_code() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-001",
    )

    use_case = CreateSupplierUseCase(
        repository
    )

    with pytest.raises(
        ConflictError
    ) as captured:
        use_case.execute(
            tenant_id,
            SupplierCreate(
                code="forn-001",
                name="Outro Fornecedor",
            ),
        )

    assert captured.value.details == {
        "field": "code",
        "value": "FORN-001",
    }


def test_create_supplier_rejects_duplicate_document() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-001",
        document_number="04.252.011/0001-10",
    )

    use_case = CreateSupplierUseCase(
        repository
    )

    with pytest.raises(
        ConflictError
    ) as captured:
        use_case.execute(
            tenant_id,
            SupplierCreate(
                code="FORN-002",
                name="Outro Fornecedor",
                document_number="04252011000110",
            ),
        )

    assert captured.value.details == {
        "field": "document_number",
        "value": "04252011000110",
    }


def test_create_supplier_allows_same_identity_in_other_tenant() -> None:
    repository = FakeSupplierRepository()

    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_supplier(
        repository,
        tenant_id=tenant_a_id,
        code="FORN-001",
        document_number="04.252.011/0001-10",
    )

    result = CreateSupplierUseCase(
        repository
    ).execute(
        tenant_b_id,
        SupplierCreate(
            code="FORN-001",
            name="Fornecedor B",
            document_number="04.252.011/0001-10",
        ),
    )

    assert result.tenant_id == tenant_b_id


def test_create_supplier_converts_domain_error_to_validation_error() -> None:
    repository = FakeSupplierRepository()

    use_case = CreateSupplierUseCase(
        repository
    )

    with pytest.raises(
        ValidationError
    ):
        use_case.execute(
            uuid.uuid4(),
            SupplierCreate(
                code="FORN-001",
                name="Fornecedor",
                email="email-invalido",
            ),
        )


def test_get_supplier_returns_tenant_supplier() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
    )

    assert supplier.id is not None

    result = GetSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
    )

    assert result is supplier


def test_get_supplier_rejects_unknown_supplier() -> None:
    repository = FakeSupplierRepository()

    with pytest.raises(
        NotFoundError
    ):
        GetSupplierUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )


def test_get_supplier_preserves_tenant_isolation() -> None:
    repository = FakeSupplierRepository()

    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_a_id,
    )

    assert supplier.id is not None

    with pytest.raises(
        NotFoundError
    ):
        GetSupplierUseCase(
            repository
        ).execute(
            tenant_b_id,
            supplier.id,
        )


def test_list_suppliers_uses_default_filters() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    create_supplier(
        repository,
        tenant_id=tenant_id,
    )

    result = ListSuppliersUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert len(result) == 1
    assert repository.last_list_tenant_id == tenant_id
    assert repository.last_include_inactive is False
    assert repository.last_search is None
    assert repository.last_limit == 100
    assert repository.last_offset == 0


def test_list_suppliers_passes_filters_and_pagination() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-001",
        name="Alfa",
    )

    create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-002",
        name="Beta",
    )

    result = ListSuppliersUseCase(
        repository
    ).execute(
        tenant_id,
        include_inactive=True,
        search="beta",
        limit=20,
        offset=0,
    )

    assert len(result) == 1
    assert result[0].name == "Beta"

    assert repository.last_include_inactive is True
    assert repository.last_search == "beta"
    assert repository.last_limit == 20
    assert repository.last_offset == 0


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (0, 0),
        (201, 0),
        (100, -1),
    ],
)
def test_list_suppliers_rejects_invalid_pagination(
    limit: int,
    offset: int,
) -> None:
    repository = FakeSupplierRepository()

    with pytest.raises(
        ValidationError
    ):
        ListSuppliersUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            limit=limit,
            offset=offset,
        )


def test_update_supplier_updates_and_normalizes_fields() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-001",
        name="Fornecedor Antigo",
    )

    assert supplier.id is not None

    previous_updated_at = (
        supplier.updated_at
    )

    result = UpdateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
        SupplierUpdate(
            code=" forn-002 ",
            name=" Fornecedor Novo ",
            document_number="04.252.011/0001-10",
            email=" NOVO@EXAMPLE.COM ",
            phone="(18) 99999-1234",
            postal_code="19200-000",
            state="sp",
        ),
    )

    assert result.code == "FORN-002"
    assert result.name == "Fornecedor Novo"

    assert (
        result.document_number
        == "04252011000110"
    )

    assert result.email == "novo@example.com"
    assert result.phone == "18999991234"
    assert result.postal_code == "19200000"
    assert result.state == "SP"

    assert result.updated_at is not None
    assert previous_updated_at is not None

    assert (
        result.updated_at
        > previous_updated_at
    )


def test_update_supplier_preserves_unspecified_fields() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = Supplier.create(
        tenant_id=tenant_id,
        code="FORN-001",
        name="Fornecedor",
        email="original@example.com",
        phone="18999991234",
        city="Rosana",
    )

    repository.add(
        supplier
    )

    assert supplier.id is not None

    result = UpdateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
        SupplierUpdate(
            name="Fornecedor Atualizado"
        ),
    )

    assert result.name == "Fornecedor Atualizado"

    assert (
        result.email
        == "original@example.com"
    )

    assert result.phone == "18999991234"
    assert result.city == "Rosana"


def test_update_supplier_can_clear_optional_fields() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = Supplier.create(
        tenant_id=tenant_id,
        code="FORN-001",
        name="Fornecedor",
        email="original@example.com",
        phone="18999991234",
        city="Rosana",
    )

    repository.add(
        supplier
    )

    assert supplier.id is not None

    result = UpdateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
        SupplierUpdate(
            email=None,
            phone=None,
            city=None,
        ),
    )

    assert result.email is None
    assert result.phone is None
    assert result.city is None


def test_update_supplier_rejects_empty_payload() -> None:
    repository = FakeSupplierRepository()

    with pytest.raises(
        ValidationError
    ):
        UpdateSupplierUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
            SupplierUpdate(),
        )


def test_update_supplier_rejects_unknown_supplier() -> None:
    repository = FakeSupplierRepository()

    with pytest.raises(
        NotFoundError
    ):
        UpdateSupplierUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
            SupplierUpdate(
                name="Fornecedor"
            ),
        )


def test_update_supplier_preserves_tenant_isolation() -> None:
    repository = FakeSupplierRepository()

    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_a_id,
    )

    assert supplier.id is not None

    with pytest.raises(
        NotFoundError
    ):
        UpdateSupplierUseCase(
            repository
        ).execute(
            tenant_b_id,
            supplier.id,
            SupplierUpdate(
                name="Alteração Indevida"
            ),
        )


def test_update_supplier_rejects_duplicate_code() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-001",
        name="Fornecedor A",
    )

    supplier_b = create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-002",
        name="Fornecedor B",
    )

    assert supplier_b.id is not None

    with pytest.raises(
        ConflictError
    ) as captured:
        UpdateSupplierUseCase(
            repository
        ).execute(
            tenant_id,
            supplier_b.id,
            SupplierUpdate(
                code="FORN-001"
            ),
        )

    assert captured.value.details == {
        "field": "code",
        "value": "FORN-001",
    }


def test_update_supplier_rejects_duplicate_document() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-001",
        name="Fornecedor A",
        document_number="04.252.011/0001-10",
    )

    supplier_b = create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-002",
        name="Fornecedor B",
    )

    assert supplier_b.id is not None

    with pytest.raises(
        ConflictError
    ) as captured:
        UpdateSupplierUseCase(
            repository
        ).execute(
            tenant_id,
            supplier_b.id,
            SupplierUpdate(
                document_number=(
                    "04.252.011/0001-10"
                )
            ),
        )

    assert captured.value.details == {
        "field": "document_number",
        "value": "04252011000110",
    }


def test_update_supplier_allows_own_code_and_document() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
        code="FORN-001",
        document_number="04.252.011/0001-10",
    )

    assert supplier.id is not None

    result = UpdateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
        SupplierUpdate(
            code="FORN-001",
            document_number="04.252.011/0001-10",
        ),
    )

    assert result.code == "FORN-001"

    assert (
        result.document_number
        == "04252011000110"
    )


def test_update_supplier_validation_is_atomic() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
        email="original@example.com",
    )

    assert supplier.id is not None

    original_name = supplier.name
    original_email = supplier.email
    original_updated_at = supplier.updated_at

    with pytest.raises(
        ValidationError
    ):
        UpdateSupplierUseCase(
            repository
        ).execute(
            tenant_id,
            supplier.id,
            SupplierUpdate(
                name="Nome Alterado",
                email="email-invalido",
            ),
        )

    assert supplier.name == original_name
    assert supplier.email == original_email

    assert (
        supplier.updated_at
        == original_updated_at
    )


def test_deactivate_supplier() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
    )

    assert supplier.id is not None

    previous_updated_at = (
        supplier.updated_at
    )

    result = DeactivateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
    )

    assert result.is_active is False
    assert result.updated_at is not None
    assert previous_updated_at is not None

    assert (
        result.updated_at
        > previous_updated_at
    )


def test_deactivate_supplier_is_idempotent() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
    )

    assert supplier.id is not None

    supplier.deactivate()

    previous_updated_at = (
        supplier.updated_at
    )

    result = DeactivateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
    )

    assert result.is_active is False

    assert (
        result.updated_at
        == previous_updated_at
    )


def test_deactivate_unknown_supplier() -> None:
    repository = FakeSupplierRepository()

    with pytest.raises(
        NotFoundError
    ):
        DeactivateSupplierUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )


def test_reactivate_supplier() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
    )

    supplier.deactivate()

    assert supplier.id is not None

    previous_updated_at = (
        supplier.updated_at
    )

    result = ReactivateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
    )

    assert result.is_active is True
    assert result.updated_at is not None
    assert previous_updated_at is not None

    assert (
        result.updated_at
        > previous_updated_at
    )


def test_reactivate_supplier_is_idempotent() -> None:
    repository = FakeSupplierRepository()
    tenant_id = uuid.uuid4()

    supplier = create_supplier(
        repository,
        tenant_id=tenant_id,
    )

    assert supplier.id is not None

    previous_updated_at = (
        supplier.updated_at
    )

    result = ReactivateSupplierUseCase(
        repository
    ).execute(
        tenant_id,
        supplier.id,
    )

    assert result.is_active is True

    assert (
        result.updated_at
        == previous_updated_at
    )


def test_reactivate_unknown_supplier() -> None:
    repository = FakeSupplierRepository()

    with pytest.raises(
        NotFoundError
    ):
        ReactivateSupplierUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )
