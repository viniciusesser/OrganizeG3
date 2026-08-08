"""Repository contracts for company persistence."""

from __future__ import annotations

from abc import ABC, abstractmethod
import uuid

from organizeg3_api.domain.company.entity import (
    Company,
)


class ICompanyRepository(ABC):
    """Expose company operations required by the domain layer."""

    @abstractmethod
    def get_by_tenant(
        self,
        tenant_id: uuid.UUID,
    ) -> Company | None:
        """Return the company owned by one tenant."""

    @abstractmethod
    def add(
        self,
        company: Company,
    ) -> Company:
        """Persist a new company."""
