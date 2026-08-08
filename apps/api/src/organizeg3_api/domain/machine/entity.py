"""Machine domain entity."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
import uuid

from organizeg3_api.domain.machine.value_objects import (
    MachineCode,
    MachineName,
    MachineStatus,
    MachineType,
    OptionalMachineText,
)


@dataclass(slots=True)
class Machine:
    """Represent a tenant-scoped industrial machine."""

    tenant_id: uuid.UUID
    code: str
    name: str
    machine_type: str

    status: MachineStatus = MachineStatus.AVAILABLE

    branch_id: uuid.UUID | None = None
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None

    id: uuid.UUID | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize machine state."""

        self._validate_uuid(
            self.tenant_id,
            field_name="tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                field_name="identificador",
            )

        if self.branch_id is not None:
            self._validate_uuid(
                self.branch_id,
                field_name="filial",
            )

        self.code = MachineCode(
            self.code
        ).value

        self.name = MachineName(
            self.name
        ).value

        self.machine_type = MachineType(
            self.machine_type
        ).value

        self.manufacturer = OptionalMachineText(
            self.manufacturer
        ).value

        self.model = OptionalMachineText(
            self.model
        ).value

        self.serial_number = OptionalMachineText(
            self.serial_number
        ).value

        self.status = self._normalize_status(
            self.status
        )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        name: str,
        machine_type: str,
        branch_id: uuid.UUID | None = None,
        manufacturer: str | None = None,
        model: str | None = None,
        serial_number: str | None = None,
    ) -> Machine:
        """Create a new available machine."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            branch_id=branch_id,
            code=code,
            name=name,
            machine_type=machine_type,
            manufacturer=manufacturer,
            model=model,
            serial_number=serial_number,
            status=MachineStatus.AVAILABLE,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def update_details(
        self,
        *,
        code: str,
        name: str,
        machine_type: str,
        branch_id: uuid.UUID | None,
        manufacturer: str | None,
        model: str | None,
        serial_number: str | None,
    ) -> None:
        """Atomically update editable machine details."""

        candidate = replace(
            self,
            code=code,
            name=name,
            machine_type=machine_type,
            branch_id=branch_id,
            manufacturer=manufacturer,
            model=model,
            serial_number=serial_number,
        )

        changed = (
            self.code != candidate.code
            or self.name != candidate.name
            or self.machine_type != candidate.machine_type
            or self.branch_id != candidate.branch_id
            or self.manufacturer != candidate.manufacturer
            or self.model != candidate.model
            or self.serial_number != candidate.serial_number
        )

        if not changed:
            return

        self.code = candidate.code
        self.name = candidate.name
        self.machine_type = candidate.machine_type
        self.branch_id = candidate.branch_id
        self.manufacturer = candidate.manufacturer
        self.model = candidate.model
        self.serial_number = candidate.serial_number

        self._touch()

    def assign_branch(
        self,
        branch_id: uuid.UUID,
    ) -> None:
        """Assign the machine to a branch."""

        self._validate_uuid(
            branch_id,
            field_name="filial",
        )

        if self.branch_id == branch_id:
            return

        self.branch_id = branch_id
        self._touch()

    def remove_branch(self) -> None:
        """Remove the machine branch assignment."""

        if self.branch_id is None:
            return

        self.branch_id = None
        self._touch()

    def mark_available(self) -> None:
        """Mark the machine as available."""

        self._change_status(
            MachineStatus.AVAILABLE
        )

    def mark_in_use(self) -> None:
        """Mark the machine as currently in use."""

        self._change_status(
            MachineStatus.IN_USE
        )

    def send_to_maintenance(self) -> None:
        """Mark the machine as under maintenance."""

        self._change_status(
            MachineStatus.MAINTENANCE
        )

    def mark_out_of_service(self) -> None:
        """Mark the machine as unavailable for operation."""

        self._change_status(
            MachineStatus.OUT_OF_SERVICE
        )

    def deactivate(self) -> None:
        """Deactivate the machine."""

        if not self.is_active:
            return

        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Reactivate the machine."""

        if self.is_active:
            return

        self.is_active = True
        self._touch()

    def _change_status(
        self,
        status: MachineStatus,
    ) -> None:
        normalized = self._normalize_status(
            status
        )

        if self.status == normalized:
            return

        self.status = normalized
        self._touch()

    @staticmethod
    def _normalize_status(
        value: MachineStatus,
    ) -> MachineStatus:
        if not isinstance(
            value,
            MachineStatus,
        ):
            raise TypeError(
                "O status da máquina deve ser "
                "um MachineStatus."
            )

        return value

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
                f"O {field_name} da máquina "
                "deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} da máquina "
                "não pode possuir UUID nulo."
            )

    @staticmethod
    def _next_timestamp(
        previous: datetime | None,
    ) -> datetime:
        """Return a UTC timestamp strictly newer than the previous one."""

        now = datetime.now(UTC)

        if previous is None:
            return now

        if previous.tzinfo is None:
            normalized_previous = previous.replace(
                tzinfo=UTC
            )
        else:
            normalized_previous = previous.astimezone(
                UTC
            )

        if now > normalized_previous:
            return now

        return (
            normalized_previous
            + timedelta(
                microseconds=1
            )
        )

    def _touch(self) -> None:
        self.updated_at = self._next_timestamp(
            self.updated_at
        )
