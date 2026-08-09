"""FastAPI endpoints for the authenticated tenant company."""

from __future__ import annotations

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from organizeg3_api.application.audit import (
    RecordAuditEvent,
)
from organizeg3_api.application.company.schemas import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)
from organizeg3_api.application.company.use_cases import (
    CreateCompanyUseCase,
    GetCompanyUseCase,
    UpdateCompanyUseCase,
)
from organizeg3_api.domain.audit import (
    AuditAction,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    CompanyPermissions,
)
from organizeg3_api.infrastructure.http.audit_context import (
    AuditRequestContext,
    get_audit_context,
)
from organizeg3_api.infrastructure.http.authentication import (
    require_permission,
)
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.company_repository import (
    SQLAlchemyCompanyRepository,
)

router = APIRouter(
    prefix="/company",
    tags=["Company"],
    dependencies=[
        Depends(get_audit_context),
    ],
)


ReadCompanyContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CompanyPermissions.READ
        )
    ),
]

CreateCompanyContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CompanyPermissions.CREATE
        )
    ),
]

UpdateCompanyContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CompanyPermissions.UPDATE
        )
    ),
]


def _company_snapshot(
    company: CompanyResponse,
) -> dict[str, object]:
    """Build the complete public auditable company state."""

    return {
        "id": company.id,
        "tenant_id": company.tenant_id,
        "trade_name": company.trade_name,
        "legal_name": company.legal_name,
        "document_number": company.document_number,
        "state_registration": company.state_registration,
        "email": company.email,
        "phone": company.phone,
        "website": company.website,
        "logo_path": company.logo_path,
        "street": company.street,
        "number": company.number,
        "district": company.district,
        "city": company.city,
        "state": company.state,
        "postal_code": company.postal_code,
        "is_active": company.is_active,
    }


def _load_company_snapshot(
    *,
    repository: SQLAlchemyCompanyRepository,
    tenant_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load the tenant company before a mutation."""

    company = repository.get_by_tenant(
        tenant_id
    )

    if company is None:
        return None

    response = CompanyResponse.model_validate(
        company
    )

    return _company_snapshot(
        response
    )


def _record_company_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    company: CompanyResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one company audit event in the current transaction."""

    after = _company_snapshot(
        company
    )

    if (
        before is not None
        and before == after
    ):
        return

    RecordAuditEvent(
        SQLAlchemyAuditEventRepository(
            session
        )
    ).execute(
        context=audit_context,
        action=action,
        resource="companies",
        resource_id=company.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create the tenant company",
)
def create_company(
    payload: CompanyCreate,
    context: CreateCompanyContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CompanyResponse:
    """Create the company owned by the authenticated tenant."""

    repository = SQLAlchemyCompanyRepository(
        session
    )

    company = CreateCompanyUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    response = CompanyResponse.model_validate(
        company
    )

    _record_company_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        company=response,
    )

    return response


@router.get(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the tenant company",
)
def get_company(
    context: ReadCompanyContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CompanyResponse:
    """Return the company owned by the authenticated tenant."""

    repository = SQLAlchemyCompanyRepository(
        session
    )

    company = GetCompanyUseCase(
        repository
    ).execute(
        context.tenant_id
    )

    return CompanyResponse.model_validate(
        company
    )


@router.patch(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Update the tenant company",
)
def update_company(
    payload: CompanyUpdate,
    context: UpdateCompanyContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CompanyResponse:
    """Partially update the authenticated tenant company."""

    repository = SQLAlchemyCompanyRepository(
        session
    )

    before = _load_company_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
    )

    company = UpdateCompanyUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    response = CompanyResponse.model_validate(
        company
    )

    _record_company_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        company=response,
        before=before,
    )

    return response
