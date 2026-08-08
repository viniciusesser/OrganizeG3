"""Update-machine application use case."""

from __future__ import annotations

from typing import TypeVar, cast
import uuid

from organizeg3_api.application.machine.schemas import (
    MachineUpdate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.repository import (
    MachineRepository,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineCode,
)

T = TypeVar("T")


class UpdateMachineUseCase:
    """Update tenant machine registration data."""

    _REQUIRED_FIELDS = frozenset(
        {
            "code",
            "name",
            "machine_type",
        }
    )

    def __init__(
        self,
        repository: MachineRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
        data: MachineUpdate,
    ) -> Machine:
        """Update one tenant-scoped machine."""

        machine = self._get_machine(
            tenant_id=tenant_id,
            machine_id=machine_id,
        )

        supplied_fields = data.model_fields_set

        if not supplied_fields:
            raise ValidationError(
                "Informe ao menos um campo para atualização."
            )

        self._reject_null_required_fields(
            data
        )

        code = self._resolve(
            data=data,
            field_name="code",
            current=machine.code,
        )

        name = self._resolve(
            data=data,
            field_name="name",
            current=machine.name,
        )

        machine_type = self._resolve(
            data=data,
            field_name="machine_type",
            current=machine.machine_type,
        )

        branch_id = self._resolve(
            data=data,
            field_name="branch_id",
            current=machine.branch_id,
        )

        manufacturer = self._resolve(
            data=data,
            field_name="manufacturer",
            current=machine.manufacturer,
        )

        model = self._resolve(
            data=data,
            field_name="model",
            current=machine.model,
        )

        serial_number = self._resolve(
            data=data,
            field_name="serial_number",
            current=machine.serial_number,
        )

        try:
            normalized_code = MachineCode(
                code
            ).value

            self._ensure_code_available(
                tenant_id=tenant_id,
                machine_id=machine_id,
                code=normalized_code,
            )

            machine.update_details(
                code=normalized_code,
                name=name,
                machine_type=machine_type,
                branch_id=branch_id,
                manufacturer=manufacturer,
                model=model,
                serial_number=serial_number,
            )

            return self._repository.save(
                machine
            )

        except ConflictError:
            raise
        except (TypeError, ValueError) as exc:
            raise ValidationError(
                str(exc)
            ) from exc

    def _get_machine(
        self,
        *,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
    ) -> Machine:
        machine = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                machine_id=machine_id,
            )
        )

        if machine is None:
            raise NotFoundError(
                "Máquina não encontrada."
            )

        return machine

    def _reject_null_required_fields(
        self,
        data: MachineUpdate,
    ) -> None:
        for field_name in (
            data.model_fields_set
            & self._REQUIRED_FIELDS
        ):
            if getattr(
                data,
                field_name,
            ) is None:
                raise ValidationError(
                    f"O campo {field_name} "
                    "não pode ser nulo."
                )

    @staticmethod
    def _resolve(
        *,
        data: MachineUpdate,
        field_name: str,
        current: T,
    ) -> T:
        if field_name not in data.model_fields_set:
            return current

        return cast(
            T,
            getattr(
                data,
                field_name,
            ),
        )

    def _ensure_code_available(
        self,
        *,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
        code: str,
    ) -> None:
        if not self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=code,
            exclude_machine_id=machine_id,
        ):
            return

        raise ConflictError(
            "Já existe uma máquina com este código.",
            details={
                "field": "code",
                "value": code,
            },
        )
