"""SQLAlchemy persistence models."""

from organizeg3_api.infrastructure.persistence.models.customer import CustomerModel
from organizeg3_api.infrastructure.persistence.models.tenant import TenantModel

__all__ = [
    "CustomerModel",
    "TenantModel",
]
