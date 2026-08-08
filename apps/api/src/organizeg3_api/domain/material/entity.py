"""Material domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.material.value_objects import (
    MaterialCategory,
    MaterialCode,
    MaterialName,
    MaterialUnit,
)


@dataclass(slots=True)
class Material:
    """Represent a material catalog item belonging to one tenant."""

    tenant_id: uuid.UUID
    code: str
    name: str
    category: str
    unit: str

    id: uuid.UUID | None = None

    brand_id: uuid.UUID | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize material state."""

        self._validate_uuid(
            self.tenant_id,
            field_name="tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                field_name="identificador",
            )

        if self.brand_id is not None:
            self._validate_uuid(
                self.brand_id,
                field_name="marca",
            )

        self.code = MaterialCode(
            self.code
        ).value

        self.name = MaterialName(
            self.name
        ).value

        self.category = MaterialCategory(
            self.category
        ).value

        self.unit = MaterialUnit(
            self.unit
        ).value

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        name: str,
        category: str,
        unit: str,
        brand_id: uuid.UUID | None = None,
    ) -> Material:
        """Create a new active material."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            code=code,
            name=name,
            category=category,
            unit=unit,
            brand_id=brand_id,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def assign_brand(
        self,
        brand_id: uuid.UUID,
    ) -> None:
        """Assign a brand to the material."""

        self._validate_uuid(
            brand_id,
            field_name="marca",
        )

        if self.brand_id == brand_id:
            return

        self.brand_id = brand_id
        self._touch()

    def remove_brand(self) -> None:
        """Remove the current brand assignment."""

        if self.brand_id is None:
            return

        self.brand_id = None
        self._touch()

    def deactivate(self) -> None:
        """Deactivate the material."""

        if not self.is_active:
            return

        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Reactivate the material."""

        if self.is_active:
            return

        self.is_active = True
        self._touch()

    @staticmethod
    def _validate_uuid(
        value: object,
        *,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} do material "
                "deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} do material "
                "não pode possuir UUID nulo."
            )

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
