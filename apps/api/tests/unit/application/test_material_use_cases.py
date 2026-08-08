"""Unit tests for material application use cases."""

from __future__ import annotations

from datetime import UTC, datetime
import uuid

import pytest

from organizeg3_api.application.material.schemas import (
    MaterialCreate,
    MaterialUpdate,
)
from organizeg3_api.application.material.use_cases import (
    CreateMaterialUseCase,
    DeactivateMaterialUseCase,
    GetMaterialUseCase,
    ListMaterialsUseCase,
    ReactivateMaterialUseCase,
    UpdateMaterialUseCase,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.material.entity import (
    Material,
)


class FakeMaterialRepository:
    """In-memory material repository used by application tests."""

    def __init__(self) -> None:
        self.materials: dict[
            tuple[uuid.UUID, uuid.UUID],
            Material,
        ] = {}

        self.last_list_arguments: dict[
            str,
            object,
        ] | None = None

        self.raise_on_add: Exception | None = None
        self.raise_on_save: Exception | None = None

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> Material | None:
        return self.materials.get(
            (
                tenant_id,
                material_id,
            )
        )

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Material | None:
        normalized = code.strip().upper()

        for (
            stored_tenant_id,
            _,
        ), material in self.materials.items():
            if (
                stored_tenant_id == tenant_id
                and material.code == normalized
            ):
                return material

        return None

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        category: str | None = None,
        brand_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Material]:
        self.last_list_arguments = {
            "tenant_id": tenant_id,
            "include_inactive": include_inactive,
            "search": search,
            "category": category,
            "brand_id": brand_id,
            "limit": limit,
            "offset": offset,
        }

        result = [
            material
            for (
                stored_tenant_id,
                _,
            ), material in self.materials.items()
            if stored_tenant_id == tenant_id
        ]

        if not include_inactive:
            result = [
                material
                for material in result
                if material.is_active
            ]

        if search is not None:
            normalized_search = search.lower()

            result = [
                material
                for material in result
                if (
                    normalized_search
                    in material.code.lower()
                    or normalized_search
                    in material.name.lower()
                    or normalized_search
                    in material.category.lower()
                    or normalized_search
                    in material.unit.lower()
                )
            ]

        if category is not None:
            result = [
                material
                for material in result
                if material.category == category
            ]

        if brand_id is not None:
            result = [
                material
                for material in result
                if material.brand_id == brand_id
            ]

        result.sort(
            key=lambda material: (
                material.name,
                material.code,
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
        exclude_material_id: uuid.UUID | None = None,
    ) -> bool:
        normalized = code.strip().upper()

        for (
            stored_tenant_id,
            stored_material_id,
        ), material in self.materials.items():
            if stored_tenant_id != tenant_id:
                continue

            if (
                exclude_material_id is not None
                and stored_material_id
                == exclude_material_id
            ):
                continue

            if material.code == normalized:
                return True

        return False

    def add(
        self,
        material: Material,
    ) -> Material:
        if self.raise_on_add is not None:
            raise self.raise_on_add

        assert material.id is not None

        self.materials[
            (
                material.tenant_id,
                material.id,
            )
        ] = material

        return material

    def save(
        self,
        material: Material,
    ) -> Material:
        if self.raise_on_save is not None:
            raise self.raise_on_save

        assert material.id is not None

        self.materials[
            (
                material.tenant_id,
                material.id,
            )
        ] = material

        return material


def make_material(
    *,
    tenant_id: uuid.UUID | None = None,
    material_id: uuid.UUID | None = None,
    code: str = "MAT-001",
    name: str = "MDF Branco TX 15mm",
    category: str = "Chapas",
    unit: str = "UN",
    brand_id: uuid.UUID | None = None,
    is_active: bool = True,
) -> Material:
    """Create a material fixture."""

    now = datetime.now(UTC)

    return Material(
        id=material_id or uuid.uuid4(),
        tenant_id=tenant_id or uuid.uuid4(),
        code=code,
        name=name,
        category=category,
        unit=unit,
        brand_id=brand_id,
        is_active=is_active,
        created_at=now,
        updated_at=now,
    )


def test_create_material() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    result = CreateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        MaterialCreate(
            code=" mat-001 ",
            name="MDF Branco",
            category="Chapas",
            unit="un",
        ),
    )

    assert result.tenant_id == tenant_id
    assert result.code == "MAT-001"
    assert result.unit == "UN"
    assert result.is_active is True


def test_create_material_with_brand() -> None:
    tenant_id = uuid.uuid4()
    brand_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    result = CreateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        MaterialCreate(
            code="MAT-001",
            name="MDF",
            category="Chapas",
            unit="UN",
            brand_id=brand_id,
        ),
    )

    assert result.brand_id == brand_id


def test_create_rejects_duplicate_code() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    existing = make_material(
        tenant_id=tenant_id,
    )
    repository.add(existing)

    use_case = CreateMaterialUseCase(
        repository
    )

    with pytest.raises(
        ConflictError,
    ):
        use_case.execute(
            tenant_id,
            MaterialCreate(
                code=" mat-001 ",
                name="Outro",
                category="Chapas",
                unit="UN",
            ),
        )


def test_create_allows_same_code_other_tenant() -> None:
    repository = FakeMaterialRepository()

    repository.add(
        make_material(
            tenant_id=uuid.uuid4(),
            code="MAT-001",
        )
    )

    tenant_id = uuid.uuid4()

    result = CreateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        MaterialCreate(
            code="MAT-001",
            name="Material",
            category="Categoria",
            unit="UN",
        ),
    )

    assert result.tenant_id == tenant_id


def test_create_converts_repository_validation_error() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    repository.raise_on_add = ValueError(
        "A marca do material não pertence ao tenant informado."
    )

    with pytest.raises(
        ValidationError,
        match="marca",
    ):
        CreateMaterialUseCase(
            repository
        ).execute(
            tenant_id,
            MaterialCreate(
                code="MAT-001",
                name="Material",
                category="Categoria",
                unit="UN",
                brand_id=uuid.uuid4(),
            ),
        )


def test_get_material() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    assert material.id is not None

    result = GetMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
    )

    assert result is material


def test_get_unknown_material() -> None:
    with pytest.raises(
        NotFoundError,
    ):
        GetMaterialUseCase(
            FakeMaterialRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )


def test_get_enforces_tenant_scope() -> None:
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=uuid.uuid4(),
    )
    repository.add(material)

    assert material.id is not None

    with pytest.raises(
        NotFoundError,
    ):
        GetMaterialUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            material.id,
        )


def test_list_materials() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    repository.add(
        make_material(
            tenant_id=tenant_id,
            code="MAT-001",
            name="Material A",
        )
    )
    repository.add(
        make_material(
            tenant_id=tenant_id,
            code="MAT-002",
            name="Material B",
        )
    )
    repository.add(
        make_material(
            tenant_id=uuid.uuid4(),
            code="MAT-003",
        )
    )

    result = ListMaterialsUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert len(result) == 2


def test_list_normalizes_search_and_category() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    ListMaterialsUseCase(
        repository
    ).execute(
        tenant_id,
        search=" MDF ",
        category=" Chapas ",
    )

    assert repository.last_list_arguments is not None

    assert (
        repository.last_list_arguments["search"]
        == "MDF"
    )
    assert (
        repository.last_list_arguments["category"]
        == "Chapas"
    )


def test_list_passes_brand_filter() -> None:
    tenant_id = uuid.uuid4()
    brand_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    ListMaterialsUseCase(
        repository
    ).execute(
        tenant_id,
        brand_id=brand_id,
    )

    assert repository.last_list_arguments is not None
    assert (
        repository.last_list_arguments["brand_id"]
        == brand_id
    )


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (0, 0),
        (-1, 0),
        (201, 0),
        (100, -1),
    ],
)
def test_list_rejects_invalid_pagination(
    limit: int,
    offset: int,
) -> None:
    with pytest.raises(
        ValidationError,
    ):
        ListMaterialsUseCase(
            FakeMaterialRepository()
        ).execute(
            uuid.uuid4(),
            limit=limit,
            offset=offset,
        )


def test_update_material() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    assert material.id is not None

    result = UpdateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
        MaterialUpdate(
            name="MDF Cristallo 15mm",
            category="MDF",
            unit="chapa",
        ),
    )

    assert result.name == "MDF Cristallo 15mm"
    assert result.category == "MDF"
    assert result.unit == "CHAPA"
    assert result.code == "MAT-001"


def test_update_changes_code() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    assert material.id is not None

    result = UpdateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
        MaterialUpdate(
            code=" mat-999 ",
        ),
    )

    assert result.code == "MAT-999"


def test_update_assigns_brand() -> None:
    tenant_id = uuid.uuid4()
    brand_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    assert material.id is not None

    result = UpdateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
        MaterialUpdate(
            brand_id=brand_id,
        ),
    )

    assert result.brand_id == brand_id


def test_update_explicit_null_removes_brand() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
        brand_id=uuid.uuid4(),
    )
    repository.add(material)

    assert material.id is not None

    result = UpdateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
        MaterialUpdate(
            brand_id=None,
        ),
    )

    assert result.brand_id is None


def test_update_omitted_brand_is_preserved() -> None:
    tenant_id = uuid.uuid4()
    brand_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
        brand_id=brand_id,
    )
    repository.add(material)

    assert material.id is not None

    result = UpdateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
        MaterialUpdate(
            name="Novo nome",
        ),
    )

    assert result.brand_id == brand_id


def test_update_rejects_empty_payload() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    assert material.id is not None

    with pytest.raises(
        ValidationError,
    ):
        UpdateMaterialUseCase(
            repository
        ).execute(
            tenant_id,
            material.id,
            MaterialUpdate(),
        )


def test_update_unknown_material() -> None:
    with pytest.raises(
        NotFoundError,
    ):
        UpdateMaterialUseCase(
            FakeMaterialRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
            MaterialUpdate(
                name="Novo nome",
            ),
        )


def test_update_rejects_duplicate_code() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    first = make_material(
        tenant_id=tenant_id,
        code="MAT-001",
    )
    second = make_material(
        tenant_id=tenant_id,
        code="MAT-002",
    )

    repository.add(first)
    repository.add(second)

    assert second.id is not None

    with pytest.raises(
        ConflictError,
    ):
        UpdateMaterialUseCase(
            repository
        ).execute(
            tenant_id,
            second.id,
            MaterialUpdate(
                code="MAT-001",
            ),
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "name",
        "category",
        "unit",
    ],
)
def test_update_rejects_null_required_fields(
    field_name: str,
) -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    assert material.id is not None

    payload = MaterialUpdate.model_validate(
        {
            field_name: None,
        }
    )

    with pytest.raises(
        ValidationError,
    ):
        UpdateMaterialUseCase(
            repository
        ).execute(
            tenant_id,
            material.id,
            payload,
        )


def test_update_converts_repository_validation_error() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    repository.raise_on_save = ValueError(
        "A marca do material não pertence ao tenant informado."
    )

    assert material.id is not None

    with pytest.raises(
        ValidationError,
        match="marca",
    ):
        UpdateMaterialUseCase(
            repository
        ).execute(
            tenant_id,
            material.id,
            MaterialUpdate(
                brand_id=uuid.uuid4(),
            ),
        )


def test_deactivate_material() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
    )
    repository.add(material)

    assert material.id is not None

    result = DeactivateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
    )

    assert result.is_active is False


def test_deactivate_is_idempotent() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
        is_active=False,
    )
    repository.add(material)

    assert material.id is not None
    previous_updated_at = material.updated_at

    result = DeactivateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
    )

    assert result.is_active is False
    assert result.updated_at == previous_updated_at


def test_deactivate_unknown_material() -> None:
    with pytest.raises(
        NotFoundError,
    ):
        DeactivateMaterialUseCase(
            FakeMaterialRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )


def test_reactivate_material() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
        is_active=False,
    )
    repository.add(material)

    assert material.id is not None

    result = ReactivateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
    )

    assert result.is_active is True


def test_reactivate_is_idempotent() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMaterialRepository()

    material = make_material(
        tenant_id=tenant_id,
        is_active=True,
    )
    repository.add(material)

    assert material.id is not None
    previous_updated_at = material.updated_at

    result = ReactivateMaterialUseCase(
        repository
    ).execute(
        tenant_id,
        material.id,
    )

    assert result.is_active is True
    assert result.updated_at == previous_updated_at


def test_reactivate_unknown_material() -> None:
    with pytest.raises(
        NotFoundError,
    ):
        ReactivateMaterialUseCase(
            FakeMaterialRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )
