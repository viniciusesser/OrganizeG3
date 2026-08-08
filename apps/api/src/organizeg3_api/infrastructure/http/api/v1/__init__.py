"""Version 1 API router."""

from fastapi import APIRouter

from organizeg3_api.infrastructure.http.api.v1 import (
    auth,
    customers,
)

router = APIRouter()

router.include_router(
    auth.router
)

router.include_router(
    customers.router
)

__all__ = [
    "router",
]
