"""Version 1 API router."""

from fastapi import APIRouter

from organizeg3_api.infrastructure.http.api.v1 import (
    auth,
    branches,
    company,
    customers,
    employees,
    materials,
    services,
    suppliers,
)

router = APIRouter()

router.include_router(
    auth.router
)

router.include_router(
    company.router
)

router.include_router(
    branches.router
)

router.include_router(
    customers.router
)

router.include_router(
    employees.router
)

router.include_router(
    suppliers.router
)

router.include_router(
    materials.router
)

router.include_router(
    services.router
)


__all__ = [
    "router",
]
