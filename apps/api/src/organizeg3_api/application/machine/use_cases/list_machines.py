"""List-machines application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    ValidationError,
)
from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.repository import (
    MachineRepository,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
    MachineType,
)

MAX_LIST_LIMIT = 200


class ListMachinesUseCase:
    """List tenant machines with filtering and pagination."""

    def __init__(
        self,
        repository: MachineRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        machine_type: str | None = None,
        status: MachineStatus | None = None,
        branch_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Machine]:
        """Return tenant machines matching the supplied filters."""

        try:
            self._validate_pagination(
                limit=limit,
                offset=offset,
            )

            normalized_search = self._normalize_optional_filter(
                search,
                field_name="busca",
            )

            normalized_machine_type = (
                self._normalize_machine_type(
                    machine_type
                )
            )

            normalized_status = (
                self._normalize_status(
                    status
                )
            )

            self._validate_optional_uuid(
                branch_id,
                field_name="filial",
            )

            return self._repository.list_all(
                tenant_id=tenant_id,
                include_inactive=include_inactive,
                search=normalized_search,
                machine_type=normalized_machine_type,
                status=normalized_status,
                branch_id=branch_id,
                limit=limit,
                offset=offset,
            )

        except ValidationError:
            raise
        except (TypeError, ValueError) as exc:
            raise ValidationError(
                str(exc)
            ) from exc

    @staticmethod
    def _validate_pagination(
        *,
        limit: int,
        offset: int,
    ) -> None:
        if isinstance(
            limit,
            bool,
        ) or not isinstance(
            limit,
            int,
        ):
            raise ValidationError(
                "O limite deve ser um número inteiro."
            )

        if limit < 1 or limit > MAX_LIST_LIMIT:
            raise ValidationError(
                "O limite deve estar entre 1 e 200."
            )

        if isinstance(
            offset,
            bool,
        ) or not isinstance(
            offset,
            int,
        ):
            raise ValidationError(
                "O offset deve ser um número inteiro."
            )

        if offset < 0:
            raise ValidationError(
                "O offset não pode ser negativo."
            )

    @staticmethod
    def _normalize_optional_filter(
        value: str | None,
        *,
        field_name: str,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(
            value,
            str,
        ):
            raise ValidationError(
                f"O filtro de {field_name} deve ser texto."
            )

        normalized = value.strip()

        if not normalized:
            raise ValidationError(
                f"O filtro de {field_name} não pode ser vazio."
            )

        return normalized

    @staticmethod
    def _normalize_machine_type(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return MachineType(
            value
        ).value

    @staticmethod
    def _normalize_status(
        value: MachineStatus | None,
    ) -> MachineStatus | None:
        if value is None:
            return None

        if not isinstance(
            value,
            MachineStatus,
        ):
            raise ValidationError(
                "O filtro de status deve ser um MachineStatus."
            )

        return value

    @staticmethod
    def _validate_optional_uuid(
        value: uuid.UUID | None,
        *,
        field_name: str,
    ) -> None:
        if value is None:
            return

        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise ValidationError(
                f"O filtro de {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValidationError(
                f"O filtro de {field_name} não pode "
                "possuir UUID nulo."
            )
