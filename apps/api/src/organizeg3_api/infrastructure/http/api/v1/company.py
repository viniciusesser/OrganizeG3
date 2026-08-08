"""FastAPI endpoints for the authenticated tenant company."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    CompanyPermissions,
)
from organizeg3_api.infrastructure.http.audit_context import (
    get_audit_context,
)
from organizeg3_api.infrastructure.http.authentication import (
    require_permission,
)
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
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


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create the tenant company",
)
def create_company(
    payload: CompanyCreate,
    context: CreateCompanyContext,
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

    return CompanyResponse.model_validate(
        company
    )


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
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CompanyResponse:
    """Partially update the authenticated tenant company."""

    repository = SQLAlchemyCompanyRepository(
        session
    )

    company = UpdateCompanyUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    return CompanyResponse.model_validate(
        company
    )
