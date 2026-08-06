"""Version 1 API router aggregation."""

from fastapi import APIRouter

from organizeg3_api.infrastructure.http.api.v1.customers import router as customers_router

router = APIRouter()
router.include_router(customers_router)

__all__ = ["router"]
