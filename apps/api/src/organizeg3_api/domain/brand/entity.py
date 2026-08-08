"""Brand domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.brand.value_objects import (
    BrandCode,
    BrandName,
)


@dataclass(slots=True)
class Brand:
    """Represent a material brand belonging to one tenant."""

    tenant_id: uuid.UUID
    code: str
    name: str

    id: uuid.UUID | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize brand state."""

        self._validate_uuid(
            self.tenant_id,
            field_name="tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                field_name="identificador",
            )

        self.code = BrandCode(
            self.code
        ).value

        self.name = BrandName(
            self.name
        ).value

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        name: str,
    ) -> Brand:
        """Create a new active brand."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            code=code,
            name=name,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def deactivate(self) -> None:
        """Deactivate the brand."""

        if not self.is_active:
            return

        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Reactivate the brand."""

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
                f"O {field_name} da marca "
                "deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} da marca "
                "não pode possuir UUID nulo."
            )

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
