"""Update-branch use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.branch.schemas import (
    BranchUpdate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.domain.branch.repository import (
    BranchRepository,
)


class UpdateBranchUseCase:
    """Partially update one tenant-owned branch."""

    def __init__(
        self,
        repository: BranchRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
        payload: BranchUpdate,
    ) -> Branch:
        """Apply a partial update to one branch."""

        branch = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                branch_id=branch_id,
            )
        )

        if branch is None:
            raise NotFoundError(
                "Filial não encontrada."
            )

        changed_fields = payload.model_fields_set

        if not changed_fields:
            raise ValidationError(
                "Informe ao menos um campo para atualizar."
            )

        if (
            "code" in changed_fields
            and payload.code is None
        ):
            raise ValidationError(
                "O código da filial não pode ser nulo."
            )

        if (
            "name" in changed_fields
            and payload.name is None
        ):
            raise ValidationError(
                "O nome da filial não pode ser nulo."
            )

        if (
            "is_headquarters" in changed_fields
            and payload.is_headquarters is None
        ):
            raise ValidationError(
                "A indicação de matriz não pode ser nula."
            )

        code = (
            payload.code
            if "code" in changed_fields
            else branch.code
        )

        name = (
            payload.name
            if "name" in changed_fields
            else branch.name
        )

        is_headquarters = (
            payload.is_headquarters
            if "is_headquarters" in changed_fields
            else branch.is_headquarters
        )

        if code is None:
            raise ValidationError(
                "O código da filial é obrigatório."
            )

        if name is None:
            raise ValidationError(
                "O nome da filial é obrigatório."
            )

        if is_headquarters is None:
            raise ValidationError(
                "A indicação de matriz é obrigatória."
            )

        if (
            code != branch.code
            and self._repository.exists_by_code(
                tenant_id=tenant_id,
                code=code,
                exclude_branch_id=branch_id,
            )
        ):
            raise ConflictError(
                "Já existe uma filial com este código."
            )

        if (
            is_headquarters
            and not branch.is_headquarters
            and self._repository.exists_headquarters_for_tenant(
                tenant_id=tenant_id,
                exclude_branch_id=branch_id,
            )
        ):
            raise ConflictError(
                "O tenant já possui uma filial matriz."
            )

        def text_value_for(
            field_name: str,
            current_value: str | None,
        ) -> str | None:
            """Resolve one optional textual field from a partial update."""

            if field_name not in changed_fields:
                return current_value

            value = getattr(
                payload,
                field_name,
            )

            if value is None:
                return None

            if not isinstance(
                value,
                str,
            ):
                raise ValidationError(
                    f"O campo {field_name} deve ser textual."
                )

            return value

        try:
            branch.update_details(
                code=code,
                name=name,
                legal_name=text_value_for(
                    "legal_name",
                    branch.legal_name,
                ),
                document_number=text_value_for(
                    "document_number",
                    branch.document_number,
                ),
                state_registration=text_value_for(
                    "state_registration",
                    branch.state_registration,
                ),
                email=text_value_for(
                    "email",
                    branch.email,
                ),
                phone=text_value_for(
                    "phone",
                    branch.phone,
                ),
                website=text_value_for(
                    "website",
                    branch.website,
                ),
                street=text_value_for(
                    "street",
                    branch.street,
                ),
                number=text_value_for(
                    "number",
                    branch.number,
                ),
                district=text_value_for(
                    "district",
                    branch.district,
                ),
                city=text_value_for(
                    "city",
                    branch.city,
                ),
                state=text_value_for(
                    "state",
                    branch.state,
                ),
                postal_code=text_value_for(
                    "postal_code",
                    branch.postal_code,
                ),
                is_headquarters=is_headquarters,
            )
        except (TypeError, ValueError) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        return self._repository.save(
            branch
        )
