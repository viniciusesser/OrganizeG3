"""Update-service use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.service.schemas import (
    ServiceUpdate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.repository import (
    ServiceRepository,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceCode,
    ServiceExecutionMode,
)


class UpdateServiceUseCase:
    """Partially update one tenant-scoped service."""

    def __init__(
        self,
        repository: ServiceRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        service_id: uuid.UUID,
        data: ServiceUpdate,
    ) -> Service:
        """Validate and persist a service partial update."""

        service = self._get_service(
            tenant_id=tenant_id,
            service_id=service_id,
        )

        submitted_fields = data.model_fields_set

        if not submitted_fields:
            raise ValidationError(
                "Informe ao menos um campo para atualização."
            )

        code = self._resolve_required_string(
            field_name="code",
            submitted_fields=submitted_fields,
            submitted_value=data.code,
            current_value=service.code,
            null_message=(
                "O código do serviço não pode ser nulo."
            ),
        )

        name = self._resolve_required_string(
            field_name="name",
            submitted_fields=submitted_fields,
            submitted_value=data.name,
            current_value=service.name,
            null_message=(
                "O nome do serviço não pode ser nulo."
            ),
        )

        category = self._resolve_required_string(
            field_name="category",
            submitted_fields=submitted_fields,
            submitted_value=data.category,
            current_value=service.category,
            null_message=(
                "A categoria do serviço não pode ser nula."
            ),
        )

        unit = self._resolve_required_string(
            field_name="unit",
            submitted_fields=submitted_fields,
            submitted_value=data.unit,
            current_value=service.unit,
            null_message=(
                "A unidade do serviço não pode ser nula."
            ),
        )

        execution_mode = self._resolve_execution_mode(
            submitted_fields=submitted_fields,
            submitted_value=data.execution_mode,
            current_value=service.execution_mode,
        )

        estimated_duration_minutes = (
            data.estimated_duration_minutes
            if (
                "estimated_duration_minutes"
                in submitted_fields
            )
            else service.estimated_duration_minutes
        )

        normalized_code = self._normalize_code(
            code
        )

        self._ensure_code_available(
            tenant_id=tenant_id,
            service=service,
            normalized_code=normalized_code,
        )

        try:
            service.update_details(
                code=code,
                name=name,
                category=category,
                unit=unit,
                execution_mode=execution_mode,
                estimated_duration_minutes=(
                    estimated_duration_minutes
                ),
            )

            return self._repository.save(
                service
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValidationError(
                str(exc)
            ) from exc

    def _get_service(
        self,
        *,
        tenant_id: uuid.UUID,
        service_id: uuid.UUID,
    ) -> Service:
        service = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                service_id=service_id,
            )
        )

        if service is None:
            raise NotFoundError(
                "Serviço não encontrado."
            )

        return service

    @staticmethod
    def _resolve_required_string(
        *,
        field_name: str,
        submitted_fields: set[str],
        submitted_value: str | None,
        current_value: str,
        null_message: str,
    ) -> str:
        if field_name not in submitted_fields:
            return current_value

        if submitted_value is None:
            raise ValidationError(
                null_message
            )

        return submitted_value

    @staticmethod
    def _resolve_execution_mode(
        *,
        submitted_fields: set[str],
        submitted_value: ServiceExecutionMode | None,
        current_value: ServiceExecutionMode,
    ) -> ServiceExecutionMode:
        if "execution_mode" not in submitted_fields:
            return current_value

        if submitted_value is None:
            raise ValidationError(
                "O modo de execução do serviço "
                "não pode ser nulo."
            )

        if not isinstance(
            submitted_value,
            ServiceExecutionMode,
        ):
            raise ValidationError(
                "O modo de execução informado é inválido."
            )

        return submitted_value

    @staticmethod
    def _normalize_code(
        code: str,
    ) -> str:
        try:
            return ServiceCode(
                code
            ).value
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValidationError(
                str(exc)
            ) from exc

    def _ensure_code_available(
        self,
        *,
        tenant_id: uuid.UUID,
        service: Service,
        normalized_code: str,
    ) -> None:
        if normalized_code == service.code:
            return

        if not self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=normalized_code,
            exclude_service_id=service.id,
        ):
            return

        raise ConflictError(
            "Já existe um serviço com este código.",
            details={
                "field": "code",
                "value": normalized_code,
            },
        )


__all__ = [
    "UpdateServiceUseCase",
]
