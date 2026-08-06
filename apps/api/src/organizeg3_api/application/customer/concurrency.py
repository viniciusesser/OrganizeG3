"""Optimistic-concurrency helpers for customer services."""

from organizeg3_api.core.exceptions import ConcurrencyError
from organizeg3_api.domain.customer.entity import Customer


def ensure_customer_version(
    customer: Customer,
    expected_version: int,
) -> None:
    """Reject commands based on an outdated customer."""

    if customer.row_version != expected_version:
        raise ConcurrencyError(
            "O cliente foi alterado por outro processo.",
            details={
                "expected_version": expected_version,
                "current_version": customer.row_version,
            },
        )
