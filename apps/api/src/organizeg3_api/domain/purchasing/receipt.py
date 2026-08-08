"""Purchase receipt domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.purchasing.value_objects import (
    PurchaseReceiptStatus,
    normalize_optional_text,
    normalize_quantity,
)


@dataclass(slots=True)
class PurchaseReceipt:
    """Represent a physical supplier delivery document."""

    tenant_id: uuid.UUID
    purchase_order_id: uuid.UUID
    supplier_id: uuid.UUID
    received_at: datetime
    status: PurchaseReceiptStatus

    branch_id: uuid.UUID | None = None
    supplier_document_number: str | None = None
    notes: str | None = None
    posted_at: datetime | None = None
    cancelled_at: datetime | None = None

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )
        self._validate_uuid(
            self.purchase_order_id,
            "ordem de compra",
        )
        self._validate_uuid(
            self.supplier_id,
            "fornecedor",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.branch_id is not None:
            self._validate_uuid(
                self.branch_id,
                "filial",
            )

        if not isinstance(
            self.status,
            PurchaseReceiptStatus,
        ):
            raise TypeError(
                "O status deve ser PurchaseReceiptStatus."
            )

        self.supplier_document_number = (
            normalize_optional_text(
                self.supplier_document_number
            )
        )

        self.notes = normalize_optional_text(
            self.notes
        )

        self._validate_status_dates()

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        purchase_order_id: uuid.UUID,
        supplier_id: uuid.UUID,
        received_at: datetime | None = None,
        branch_id: uuid.UUID | None = None,
        supplier_document_number: str | None = None,
        notes: str | None = None,
    ) -> PurchaseReceipt:
        """Create a draft purchase receipt."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            purchase_order_id=purchase_order_id,
            supplier_id=supplier_id,
            branch_id=branch_id,
            received_at=received_at or now,
            status=PurchaseReceiptStatus.DRAFT,
            supplier_document_number=(
                supplier_document_number
            ),
            notes=notes,
            posted_at=None,
            cancelled_at=None,
            created_at=now,
            updated_at=now,
        )

    def post(
        self,
        *,
        posted_at: datetime | None = None,
    ) -> None:
        """Post the receipt for inventory integration."""

        if self.status is not PurchaseReceiptStatus.DRAFT:
            raise ValueError(
                "Somente um recebimento em rascunho "
                "pode ser confirmado."
            )

        effective_posted_at = (
            posted_at
            or datetime.now(UTC)
        )

        if effective_posted_at < self.received_at:
            raise ValueError(
                "A confirmação não pode anteceder "
                "o recebimento físico."
            )

        self.status = PurchaseReceiptStatus.POSTED
        self.posted_at = effective_posted_at
        self.cancelled_at = None
        self._touch()

    def cancel(
        self,
        *,
        cancelled_at: datetime | None = None,
    ) -> None:
        """Cancel an unposted receipt."""

        if self.status is not PurchaseReceiptStatus.DRAFT:
            raise ValueError(
                "Somente um recebimento em rascunho "
                "pode ser cancelado."
            )

        effective_cancelled_at = (
            cancelled_at
            or datetime.now(UTC)
        )

        if effective_cancelled_at < self.received_at:
            raise ValueError(
                "O cancelamento não pode anteceder "
                "o recebimento físico."
            )

        self.status = PurchaseReceiptStatus.CANCELLED
        self.cancelled_at = effective_cancelled_at
        self.posted_at = None
        self._touch()

    def _validate_status_dates(self) -> None:
        if (
            self.status is PurchaseReceiptStatus.DRAFT
            and (
                self.posted_at is not None
                or self.cancelled_at is not None
            )
        ):
            raise ValueError(
                "Recebimento em rascunho não pode possuir "
                "data de confirmação ou cancelamento."
            )

        if self.status is PurchaseReceiptStatus.POSTED:
            if self.posted_at is None:
                raise ValueError(
                    "Recebimento confirmado exige "
                    "data de confirmação."
                )

            if self.cancelled_at is not None:
                raise ValueError(
                    "Recebimento confirmado não pode possuir "
                    "data de cancelamento."
                )

        if self.status is PurchaseReceiptStatus.CANCELLED:
            if self.cancelled_at is None:
                raise ValueError(
                    "Recebimento cancelado exige "
                    "data de cancelamento."
                )

            if self.posted_at is not None:
                raise ValueError(
                    "Recebimento cancelado não pode possuir "
                    "data de confirmação."
                )

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)


@dataclass(slots=True)
class PurchaseReceiptItem:
    """Represent one material quantity physically received."""

    tenant_id: uuid.UUID
    purchase_receipt_id: uuid.UUID
    purchase_order_id: uuid.UUID
    purchase_order_item_id: uuid.UUID
    material_id: uuid.UUID
    quantity: Decimal

    notes: str | None = None

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )
        self._validate_uuid(
            self.purchase_receipt_id,
            "recebimento",
        )
        self._validate_uuid(
            self.purchase_order_id,
            "ordem de compra",
        )
        self._validate_uuid(
            self.purchase_order_item_id,
            "item da ordem",
        )
        self._validate_uuid(
            self.material_id,
            "material",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        self.quantity = normalize_quantity(
            self.quantity
        )

        self.notes = normalize_optional_text(
            self.notes
        )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        purchase_receipt_id: uuid.UUID,
        purchase_order_id: uuid.UUID,
        purchase_order_item_id: uuid.UUID,
        material_id: uuid.UUID,
        quantity: Decimal | int | str,
        notes: str | None = None,
    ) -> PurchaseReceiptItem:
        """Create one purchase receipt item."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            purchase_receipt_id=purchase_receipt_id,
            purchase_order_id=purchase_order_id,
            purchase_order_item_id=purchase_order_item_id,
            material_id=material_id,
            quantity=normalize_quantity(
                quantity
            ),
            notes=notes,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )
