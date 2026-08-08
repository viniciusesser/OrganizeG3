"""Unit tests for brand application use cases."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.application.brand.schemas import (
    BrandCreate,
    BrandUpdate,
)
from organizeg3_api.application.brand.use_cases import (
    CreateBrand,
    DeactivateBrand,
    GetBrand,
    ListBrands,
    ReactivateBrand,
    UpdateBrand,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.brand.entity import (
    Brand,
)


class FakeBrandRepository:
    """In-memory brand repository for application tests."""

    def __init__(self) -> None:
        self.brands: dict[
            uuid.UUID,
            Brand,
        ] = {}

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        brand_id: uuid.UUID,
    ) -> Brand | None:
        brand = self.brands.get(
            brand_id
        )

        if (
            brand is None
            or brand.tenant_id != tenant_id
        ):
            return None

        return brand

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Brand | None:
        normalized = code.strip().upper()

        for brand in self.brands.values():
            if (
                brand.tenant_id == tenant_id
                and brand.code == normalized
            ):
                return brand

        return None

    def get_by_name_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        name: str,
    ) -> Brand | None:
        normalized = name.strip()

        for brand in self.brands.values():
            if (
                brand.tenant_id == tenant_id
                and brand.name == normalized
            ):
                return brand

        return None

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Brand]:
        result = [
            brand
            for brand in self.brands.values()
            if brand.tenant_id == tenant_id
            and (
                include_inactive
                or brand.is_active
            )
        ]

        if search is not None:
            normalized_search = (
                search.strip().lower()
            )

            result = [
                brand
                for brand in result
                if (
                    normalized_search
                    in brand.code.lower()
                    or normalized_search
                    in brand.name.lower()
                )
            ]

        result.sort(
            key=lambda brand: (
                brand.name,
                str(
                    brand.id
                ),
            )
        )

        return result[
            offset : offset + limit
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_brand_id: uuid.UUID | None = None,
    ) -> bool:
        normalized = code.strip().upper()

        return any(
            brand.tenant_id == tenant_id
            and brand.code == normalized
            and brand.id != exclude_brand_id
            for brand in self.brands.values()
        )

    def exists_by_name(
        self,
        *,
        tenant_id: uuid.UUID,
        name: str,
        exclude_brand_id: uuid.UUID | None = None,
    ) -> bool:
        normalized = name.strip()

        return any(
            brand.tenant_id == tenant_id
            and brand.name == normalized
            and brand.id != exclude_brand_id
            for brand in self.brands.values()
        )

    def add(
        self,
        brand: Brand,
    ) -> Brand:
        brand_id = require_brand_id(
            brand
        )

        self.brands[
            brand_id
        ] = brand

        return brand

    def save(
        self,
        brand: Brand,
    ) -> Brand:
        brand_id = require_brand_id(
            brand
        )

        existing = self.brands.get(
            brand_id
        )

        if (
            existing is None
            or existing.tenant_id
            != brand.tenant_id
        ):
            raise ValueError(
                "Marca não encontrada."
            )

        self.brands[
            brand_id
        ] = brand

        return brand


def require_brand_id(
    brand: Brand,
) -> uuid.UUID:
    """Return the identifier of a persisted test brand."""

    if brand.id is None:
        raise RuntimeError(
            "A marca de teste deveria possuir identificador."
        )

    return brand.id


def add_brand(
    repository: FakeBrandRepository,
    *,
    tenant_id: uuid.UUID,
    code: str = "MARCA-001",
    name: str = "Duratex",
) -> Brand:
    """Create and persist one test brand."""

    brand = Brand.create(
        tenant_id=tenant_id,
        code=code,
        name=name,
    )

    repository.add(
        brand
    )

    return brand


def test_create_brand() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    response = CreateBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        data=BrandCreate(
            code=" marca-001 ",
            name=" Duratex ",
        ),
    )

    assert response.tenant_id == tenant_id
    assert response.code == "MARCA-001"
    assert response.name == "Duratex"
    assert response.is_active is True


def test_create_rejects_duplicate_code() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_id,
    )

    with pytest.raises(
        ConflictError
    ) as exc_info:
        CreateBrand(
            repository
        ).execute(
            tenant_id=tenant_id,
            data=BrandCreate(
                code="marca-001",
                name="Arauco",
            ),
        )

    assert (
        exc_info.value.details["field"]
        == "code"
    )


def test_create_rejects_duplicate_name() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_id,
    )

    with pytest.raises(
        ConflictError
    ) as exc_info:
        CreateBrand(
            repository
        ).execute(
            tenant_id=tenant_id,
            data=BrandCreate(
                code="MARCA-002",
                name="Duratex",
            ),
        )

    assert (
        exc_info.value.details["field"]
        == "name"
    )


def test_same_brand_data_is_allowed_in_different_tenants() -> None:
    repository = FakeBrandRepository()

    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_a,
    )

    response = CreateBrand(
        repository
    ).execute(
        tenant_id=tenant_b,
        data=BrandCreate(
            code="MARCA-001",
            name="Duratex",
        ),
    )

    assert response.tenant_id == tenant_b


def test_get_brand() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    response = GetBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
    )

    assert response.code == "MARCA-001"


def test_get_unknown_brand_raises_not_found() -> None:
    repository = FakeBrandRepository()

    with pytest.raises(
        NotFoundError
    ):
        GetBrand(
            repository
        ).execute(
            tenant_id=uuid.uuid4(),
            brand_id=uuid.uuid4(),
        )


def test_get_brand_is_tenant_scoped() -> None:
    repository = FakeBrandRepository()

    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_a,
    )

    with pytest.raises(
        NotFoundError
    ):
        GetBrand(
            repository
        ).execute(
            tenant_id=tenant_b,
            brand_id=require_brand_id(
                brand
            ),
        )


def test_list_brands() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    response = ListBrands(
        repository
    ).execute(
        tenant_id=tenant_id
    )

    assert [
        item.name
        for item in response
    ] == [
        "Arauco",
        "Duratex",
    ]


def test_list_is_tenant_scoped() -> None:
    repository = FakeBrandRepository()

    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_a,
        name="Arauco",
    )

    add_brand(
        repository,
        tenant_id=tenant_b,
        name="Duratex",
    )

    response = ListBrands(
        repository
    ).execute(
        tenant_id=tenant_a
    )

    assert len(
        response
    ) == 1
    assert response[0].name == "Arauco"


def test_list_searches_code_and_name() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    by_code = ListBrands(
        repository
    ).execute(
        tenant_id=tenant_id,
        search="marca-001",
    )

    by_name = ListBrands(
        repository
    ).execute(
        tenant_id=tenant_id,
        search="duratex",
    )

    assert len(
        by_code
    ) == 1
    assert by_code[0].code == "MARCA-001"

    assert len(
        by_name
    ) == 1
    assert by_name[0].name == "Duratex"


def test_list_rejects_blank_search() -> None:
    repository = FakeBrandRepository()

    with pytest.raises(
        ValidationError
    ):
        ListBrands(
            repository
        ).execute(
            tenant_id=uuid.uuid4(),
            search="   ",
        )


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (
            0,
            0,
        ),
        (
            201,
            0,
        ),
        (
            100,
            -1,
        ),
    ],
)
def test_list_rejects_invalid_pagination(
    limit: int,
    offset: int,
) -> None:
    repository = FakeBrandRepository()

    with pytest.raises(
        ValidationError
    ):
        ListBrands(
            repository
        ).execute(
            tenant_id=uuid.uuid4(),
            limit=limit,
            offset=offset,
        )


def test_list_paginates() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-003",
        name="Guararapes",
    )

    response = ListBrands(
        repository
    ).execute(
        tenant_id=tenant_id,
        limit=1,
        offset=1,
    )

    assert len(
        response
    ) == 1
    assert response[0].name == "Duratex"


def test_list_excludes_inactive_by_default() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    active = add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    inactive = add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    inactive.deactivate()

    response = ListBrands(
        repository
    ).execute(
        tenant_id=tenant_id
    )

    ids = {
        item.id
        for item in response
    }

    assert require_brand_id(
        active
    ) in ids

    assert require_brand_id(
        inactive
    ) not in ids


def test_list_can_include_inactive() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    inactive = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    inactive.deactivate()

    response = ListBrands(
        repository
    ).execute(
        tenant_id=tenant_id,
        include_inactive=True,
    )

    assert len(
        response
    ) == 1
    assert response[0].is_active is False


def test_update_brand() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    response = UpdateBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
        data=BrandUpdate(
            code=" marca-002 ",
            name=" Arauco ",
        ),
    )

    assert response.code == "MARCA-002"
    assert response.name == "Arauco"


def test_update_preserves_unspecified_fields() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    response = UpdateBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
        data=BrandUpdate(
            name="Arauco"
        ),
    )

    assert response.code == "MARCA-001"
    assert response.name == "Arauco"


def test_update_rejects_empty_payload() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    with pytest.raises(
        ValidationError
    ):
        UpdateBrand(
            repository
        ).execute(
            tenant_id=tenant_id,
            brand_id=require_brand_id(
                brand
            ),
            data=BrandUpdate(),
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "name",
    ],
)
def test_update_rejects_null_required_fields(
    field_name: str,
) -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    payload = BrandUpdate.model_validate(
        {
            field_name: None,
        }
    )

    with pytest.raises(
        ValidationError
    ) as exc_info:
        UpdateBrand(
            repository
        ).execute(
            tenant_id=tenant_id,
            brand_id=require_brand_id(
                brand
            ),
            data=payload,
        )

    assert (
        exc_info.value.details["field"]
        == field_name
    )


def test_update_rejects_duplicate_code() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    first = add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    second = add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    assert first.id is not None

    with pytest.raises(
        ConflictError
    ) as exc_info:
        UpdateBrand(
            repository
        ).execute(
            tenant_id=tenant_id,
            brand_id=require_brand_id(
                second
            ),
            data=BrandUpdate(
                code="marca-001"
            ),
        )

    assert (
        exc_info.value.details["field"]
        == "code"
    )


def test_update_rejects_duplicate_name() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    second = add_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    with pytest.raises(
        ConflictError
    ) as exc_info:
        UpdateBrand(
            repository
        ).execute(
            tenant_id=tenant_id,
            brand_id=require_brand_id(
                second
            ),
            data=BrandUpdate(
                name="Duratex"
            ),
        )

    assert (
        exc_info.value.details["field"]
        == "name"
    )


def test_update_allows_unchanged_code_and_name() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    response = UpdateBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
        data=BrandUpdate(
            code="MARCA-001",
            name="Duratex",
        ),
    )

    assert response.code == "MARCA-001"
    assert response.name == "Duratex"


def test_update_is_tenant_scoped() -> None:
    repository = FakeBrandRepository()

    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_a,
    )

    with pytest.raises(
        NotFoundError
    ):
        UpdateBrand(
            repository
        ).execute(
            tenant_id=tenant_b,
            brand_id=require_brand_id(
                brand
            ),
            data=BrandUpdate(
                name="Arauco"
            ),
        )


def test_deactivate_brand() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    response = DeactivateBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
    )

    assert response.is_active is False


def test_deactivate_is_idempotent() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    use_case = DeactivateBrand(
        repository
    )

    first = use_case.execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
    )

    second = use_case.execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
    )

    assert first.is_active is False
    assert second.is_active is False
    assert (
        second.updated_at
        == first.updated_at
    )


def test_deactivate_unknown_brand_raises_not_found() -> None:
    repository = FakeBrandRepository()

    with pytest.raises(
        NotFoundError
    ):
        DeactivateBrand(
            repository
        ).execute(
            tenant_id=uuid.uuid4(),
            brand_id=uuid.uuid4(),
        )


def test_reactivate_brand() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    brand.deactivate()

    response = ReactivateBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
    )

    assert response.is_active is True


def test_reactivate_is_idempotent() -> None:
    repository = FakeBrandRepository()
    tenant_id = uuid.uuid4()

    brand = add_brand(
        repository,
        tenant_id=tenant_id,
    )

    original_updated_at = brand.updated_at

    response = ReactivateBrand(
        repository
    ).execute(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            brand
        ),
    )

    assert response.is_active is True
    assert (
        response.updated_at
        == original_updated_at
    )


def test_reactivate_unknown_brand_raises_not_found() -> None:
    repository = FakeBrandRepository()

    with pytest.raises(
        NotFoundError
    ):
        ReactivateBrand(
            repository
        ).execute(
            tenant_id=uuid.uuid4(),
            brand_id=uuid.uuid4(),
        )
