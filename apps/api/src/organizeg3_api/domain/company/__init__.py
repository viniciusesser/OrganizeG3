"""Company domain definitions."""

from organizeg3_api.domain.company.entity import (
    Company,
)
from organizeg3_api.domain.company.repository import (
    ICompanyRepository,
)
from organizeg3_api.domain.company.value_objects import (
    CompanyDocument,
    CompanyEmail,
    CompanyPhone,
    PostalCode,
)

__all__ = [
    "Company",
    "CompanyDocument",
    "CompanyEmail",
    "CompanyPhone",
    "ICompanyRepository",
    "PostalCode",
]
