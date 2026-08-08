"""List-services use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    ValidationError,
)
from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.repository import (
    ServiceRepository,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceCategory,
    ServiceExecutionMode,
)

MAX_LIST_LIMIT = 200


class ListServicesUseCase:
    """List services belonging to one tenant."""

    def __init__(
        self,
        repository: ServiceRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        category: str | None = None,
        execution_mode: ServiceExecutionMode | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Service]:
        """Return a filtered and paginated service list."""

        if limit < 1:
            raise ValidationError(
                "O limite deve ser maior que zero."
            )

        if limit > MAX_LIST_LIMIT:
            raise ValidationError(
                f"O limite máximo é {MAX_LIST_LIMIT}."
            )

        if offset < 0:
            raise ValidationError(
                "O deslocamento não pode ser negativo."
            )

        normalized_search: str | None = None

        if search is not None:
            normalized_search = search.strip()

            if not normalized_search:
                raise ValidationError(
                    "A busca não pode ser vazia."
                )

        normalized_category: str | None = None

        if category is not None:
            try:
                normalized_category = (
                    ServiceCategory(
                        category
                    ).value
                )
            except (
                TypeError,
                ValueError,
            ) as exc:
                raise ValidationError(
                    str(exc)
                ) from exc

        if (
            execution_mode is not None
            and not isinstance(
                execution_mode,
                ServiceExecutionMode,
            )
        ):
            raise ValidationError(
                "O modo de execução informado é inválido."
            )

        return self._repository.list_all(
            tenant_id=tenant_id,
            include_inactive=include_inactive,
            search=normalized_search,
            category=normalized_category,
            execution_mode=execution_mode,
            limit=limit,
            offset=offset,
        )


__all__ = [
    "MAX_LIST_LIMIT",
    "ListServicesUseCase",
]
