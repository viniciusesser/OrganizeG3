"""Authenticated identity HTTP endpoints."""

from __future__ import annotations

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.infrastructure.http.authentication import (
    get_authenticated_context,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class CurrentIdentityResponse(BaseModel):
    """Current authenticated user and tenant context."""

    model_config = ConfigDict(
        extra="forbid",
    )

    tenant_id: uuid.UUID
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID
    email: str
    display_name: str
    permissions: list[str]


@router.get(
    "/me",
    response_model=CurrentIdentityResponse,
    summary="Consultar o contexto autenticado",
)
def get_current_identity(
    context: Annotated[
        AuthenticatedContext,
        Depends(
            get_authenticated_context
        ),
    ],
) -> CurrentIdentityResponse:
    """Return authenticated user, tenant and permissions."""

    return CurrentIdentityResponse(
        tenant_id=context.tenant_id,
        user_id=context.user_id,
        membership_id=context.membership_id,
        auth_user_id=context.auth_user_id,
        email=context.email,
        display_name=context.display_name,
        permissions=sorted(
            context.permission_codes
        ),
    )
