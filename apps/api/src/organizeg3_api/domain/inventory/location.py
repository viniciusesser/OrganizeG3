"""Inventory location domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.inventory.value_objects import (
    InventoryLocationType,
    normalize_inventory_code,
    normalize_optional_text,
    normalize_required_text,
)


@dataclass(slots=True)
class InventoryLocation:
    """Represent a physical inventory location."""

    tenant_id: uuid.UUID
    code: str
    name: str
    location_type: InventoryLocationType

    branch_id: uuid.UUID | None = None
    description: str | None = None
    is_active: bool = True

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.branch_id is not None:
            self._validate_uuid(
                self.branch_id,
                "filial",
            )

        self.code = normalize_inventory_code(
            self.code
        )

        self.name = normalize_required_text(
            self.name,
            field_name="nome",
        )

        self.description = normalize_optional_text(
            self.description
        )

        if not isinstance(
            self.location_type,
            InventoryLocationType,
        ):
            raise TypeError(
                "O tipo do local deve ser InventoryLocationType."
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        name: str,
        location_type: InventoryLocationType,
        branch_id: uuid.UUID | None = None,
        description: str | None = None,
    ) -> InventoryLocation:
        """Create an inventory location."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            branch_id=branch_id,
            code=code,
            name=name,
            location_type=location_type,
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def rename(
        self,
        name: str,
    ) -> None:
        """Rename the location."""

        self.name = normalize_required_text(
            name,
            field_name="nome",
        )
        self._touch()

    def activate(self) -> None:
        """Activate the location."""

        self.is_active = True
        self._touch()

    def deactivate(self) -> None:
        """Deactivate the location."""

        self.is_active = False
        self._touch()

    def assign_branch(
        self,
        branch_id: uuid.UUID,
    ) -> None:
        """Assign a branch."""

        self._validate_uuid(
            branch_id,
            "filial",
        )

        self.branch_id = branch_id
        self._touch()

    def remove_branch(self) -> None:
        """Remove branch association."""

        self.branch_id = None
        self._touch()

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
