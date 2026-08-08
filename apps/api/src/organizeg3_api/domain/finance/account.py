"""Financial account domain entity."""

from __future__ import annotations

from dataclasses import dataclass
import uuid

from organizeg3_api.domain.finance.value_objects import (
    FinancialAccountType,
    normalize_code,
    normalize_currency,
    normalize_required_text,
)


@dataclass(
    slots=True,
)
class FinancialAccount:
    """Account where real money is held or cleared."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    code: str
    name: str
    account_type: FinancialAccountType
    branch_id: uuid.UUID | None = None
    currency: str = "BRL"
    is_active: bool = True

    def __post_init__(
        self,
    ) -> None:
        """Validate and normalize account data."""

        self.code = normalize_code(
            self.code
        )

        self.name = normalize_required_text(
            self.name,
            field_name="Account name",
            max_length=255,
        )

        self.currency = normalize_currency(
            self.currency
        )

    def deactivate(
        self,
    ) -> None:
        """Prevent future use without deleting history."""

        self.is_active = False

    def activate(
        self,
    ) -> None:
        """Reactivate the account."""

        self.is_active = True
