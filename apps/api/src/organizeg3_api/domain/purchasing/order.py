"""Purchase order domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.purchasing.value_objects import (
    PurchaseOrderStatus,
    normalize_money,
    normalize_optional_text,
    normalize_purchase_code,
    normalize_quantity,
)


@dataclass(slots=True)
class PurchaseOrder:
    """Represent a tenant-scoped purchase order."""

    tenant_id: uuid.UUID
    supplier_id: uuid.UUID
    code: str
    status: PurchaseOrderStatus

    branch_id: uuid.UUID | None = None
    issued_at: datetime | None = None
    expected_at: datetime | None = None
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

        self.code = normalize_purchase_code(
            self.code
        )

        self.notes = normalize_optional_text(
            self.notes
        )

        if not isinstance(
            self.status,
            PurchaseOrderStatus,
        ):
            raise TypeError(
                "O status deve ser PurchaseOrderStatus."
            )

        self._validate_dates()

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        supplier_id: uuid.UUID,
        code: str,
        branch_id: uuid.UUID | None = None,
        expected_at: datetime | None = None,
        notes: str | None = None,
    ) -> PurchaseOrder:
        """Create a draft purchase order."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            supplier_id=supplier_id,
            branch_id=branch_id,
            code=code,
            status=PurchaseOrderStatus.DRAFT,
            issued_at=None,
            expected_at=expected_at,
            notes=notes,
            created_at=now,
            updated_at=now,
        )

    def issue(
        self,
        *,
        issued_at: datetime | None = None,
    ) -> None:
        """Issue the purchase order to the supplier."""

        if self.status is not PurchaseOrderStatus.DRAFT:
            raise ValueError(
                "Somente uma ordem em rascunho pode ser emitida."
            )

        effective_issued_at = (
            issued_at
            or datetime.now(UTC)
        )

        if (
            self.expected_at is not None
            and self.expected_at < effective_issued_at
        ):
            raise ValueError(
                "A previsão de entrega não pode "
                "anteceder a emissão."
            )

        self.issued_at = effective_issued_at
        self.status = PurchaseOrderStatus.ISSUED
        self._touch()

    def mark_partially_received(self) -> None:
        """Mark the order as partially received."""

        if self.status not in {
            PurchaseOrderStatus.ISSUED,
            PurchaseOrderStatus.PARTIALLY_RECEIVED,
        }:
            raise ValueError(
                "A ordem não pode ser marcada "
                "como parcialmente recebida."
            )

        self.status = (
            PurchaseOrderStatus.PARTIALLY_RECEIVED
        )
        self._touch()

    def mark_received(self) -> None:
        """Mark the order as fully received."""

        if self.status not in {
            PurchaseOrderStatus.ISSUED,
            PurchaseOrderStatus.PARTIALLY_RECEIVED,
        }:
            raise ValueError(
                "A ordem não pode ser marcada como recebida."
            )

        self.status = PurchaseOrderStatus.RECEIVED
        self._touch()

    def close(self) -> None:
        """Close an order without further receipts."""

        if self.status not in {
            PurchaseOrderStatus.ISSUED,
            PurchaseOrderStatus.PARTIALLY_RECEIVED,
        }:
            raise ValueError(
                "A ordem não pode ser encerrada."
            )

        self.status = PurchaseOrderStatus.CLOSED
        self._touch()

    def cancel(self) -> None:
        """Cancel an unreceived purchase order."""

        if self.status not in {
            PurchaseOrderStatus.DRAFT,
            PurchaseOrderStatus.ISSUED,
        }:
            raise ValueError(
                "A ordem não pode ser cancelada "
                "no status atual."
            )

        self.status = PurchaseOrderStatus.CANCELLED
        self._touch()

    def assign_branch(
        self,
        branch_id: uuid.UUID,
    ) -> None:
        """Assign a branch to the order."""

        if self.status is not PurchaseOrderStatus.DRAFT:
            raise ValueError(
                "A filial somente pode ser alterada "
                "enquanto a ordem estiver em rascunho."
            )

        self._validate_uuid(
            branch_id,
            "filial",
        )

        self.branch_id = branch_id
        self._touch()

    def remove_branch(self) -> None:
        """Remove branch assignment."""

        if self.status is not PurchaseOrderStatus.DRAFT:
            raise ValueError(
                "A filial somente pode ser alterada "
                "enquanto a ordem estiver em rascunho."
            )

        self.branch_id = None
        self._touch()

    def _validate_dates(self) -> None:
        if (
            self.issued_at is not None
            and self.expected_at is not None
            and self.expected_at < self.issued_at
        ):
            raise ValueError(
                "A previsão de entrega não pode "
                "anteceder a emissão."
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
class PurchaseOrderItem:
    """Represent one material requested on a purchase order."""

    tenant_id: uuid.UUID
    purchase_order_id: uuid.UUID
    sequence: int
    material_id: uuid.UUID
    quantity: Decimal
    unit_price: Decimal
    received_quantity: Decimal

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
            self.purchase_order_id,
            "ordem de compra",
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

        if self.sequence <= 0:
            raise ValueError(
                "A sequência deve ser maior que zero."
            )

        self.quantity = normalize_quantity(
            self.quantity
        )

        self.unit_price = normalize_money(
            self.unit_price
        )

        self.received_quantity = normalize_quantity(
            self.received_quantity,
            allow_zero=True,
        )

        if self.received_quantity > self.quantity:
            raise ValueError(
                "A quantidade recebida não pode exceder "
                "a quantidade pedida."
            )

        self.notes = normalize_optional_text(
            self.notes
        )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        purchase_order_id: uuid.UUID,
        sequence: int,
        material_id: uuid.UUID,
        quantity: Decimal | int | str,
        unit_price: Decimal | int | str,
        notes: str | None = None,
    ) -> PurchaseOrderItem:
        """Create a purchase order item."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            purchase_order_id=purchase_order_id,
            sequence=sequence,
            material_id=material_id,
            quantity=normalize_quantity(
                quantity
            ),
            unit_price=normalize_money(
                unit_price
            ),
            received_quantity=Decimal("0"),
            notes=notes,
            created_at=now,
            updated_at=now,
        )

    @property
    def remaining_quantity(self) -> Decimal:
        """Return quantity still expected."""

        return (
            self.quantity
            - self.received_quantity
        )

    @property
    def total_amount(self) -> Decimal:
        """Return ordered line amount."""

        return (
            self.quantity
            * self.unit_price
        )

    def register_receipt(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Register received quantity for this item."""

        normalized = normalize_quantity(
            quantity
        )

        if normalized > self.remaining_quantity:
            raise ValueError(
                "O recebimento excede o saldo "
                "pendente do item."
            )

        self.received_quantity += normalized
        self._touch()

    def change_quantity(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Change ordered quantity without invalidating receipts."""

        normalized = normalize_quantity(
            quantity
        )

        if normalized < self.received_quantity:
            raise ValueError(
                "A quantidade pedida não pode ficar "
                "abaixo da quantidade já recebida."
            )

        self.quantity = normalized
        self._touch()

    def change_unit_price(
        self,
        unit_price: Decimal | int | str,
    ) -> None:
        """Change item unit price."""

        self.unit_price = normalize_money(
            unit_price
        )
        self._touch()

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
