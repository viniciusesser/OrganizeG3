"""Brand domain entity."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
import uuid

from organizeg3_api.domain.brand.value_objects import (
    BrandCode,
    BrandName,
)


def _next_timestamp(
    previous: datetime | None,
) -> datetime:
    """Return a UTC timestamp strictly newer than the previous value."""

    now = datetime.now(UTC)

    if previous is None:
        return now

    comparable_previous = previous

    if comparable_previous.tzinfo is None:
        comparable_previous = comparable_previous.replace(
            tzinfo=UTC
        )

    if now <= comparable_previous:
        return comparable_previous + timedelta(
            microseconds=1
        )

    return now


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

    def update_details(
        self,
        *,
        code: str,
        name: str,
    ) -> None:
        """Update editable brand details atomically."""

        candidate = replace(
            self,
            code=code,
            name=name,
            updated_at=_next_timestamp(
                self.updated_at
            ),
        )

        self.code = candidate.code
        self.name = candidate.name
        self.updated_at = candidate.updated_at

    def deactivate(self) -> None:
        """Deactivate the brand."""

        if not self.is_active:
            return

        self.is_active = False
        self.updated_at = _next_timestamp(
            self.updated_at
        )

    def activate(self) -> None:
        """Reactivate the brand."""

        if self.is_active:
            return

        self.is_active = True
        self.updated_at = _next_timestamp(
            self.updated_at
        )

    @staticmethod
    def _validate_uuid(
        value: object,
        *,
        field_name: str,
    ) -> None:
        """Validate one required non-null UUID."""

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
