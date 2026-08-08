"""Sales quote domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.sales.value_objects import (
    SalesQuoteStatus,
    normalize_money,
    normalize_optional_text,
    normalize_quantity,
    normalize_required_text,
    normalize_sales_code,
)


@dataclass(slots=True)
class SalesQuote:
    """Represent a commercial proposal before a sale is confirmed."""

    tenant_id: uuid.UUID
    customer_id: int
    code: str
    status: SalesQuoteStatus
    project_name: str
    proposed_amount: Decimal

    branch_id: uuid.UUID | None = None
    salesperson_employee_id: uuid.UUID | None = None

    description: str | None = None
    issued_at: datetime | None = None
    valid_until: date | None = None
    expected_delivery_at: date | None = None
    payment_terms: str | None = None
    notes: str | None = None

    material_cost: Decimal = Decimal("0")
    labor_cost: Decimal = Decimal("0")
    transport_cost: Decimal = Decimal("0")
    other_cost: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")

    approved_amount: Decimal | None = None
    approved_at: datetime | None = None
    rejected_at: datetime | None = None
    cancelled_at: datetime | None = None
    expired_at: datetime | None = None

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )

        self._validate_customer_id(
            self.customer_id
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

        if self.salesperson_employee_id is not None:
            self._validate_uuid(
                self.salesperson_employee_id,
                "vendedor",
            )

        if not isinstance(
            self.status,
            SalesQuoteStatus,
        ):
            raise TypeError(
                "O status deve ser SalesQuoteStatus."
            )

        self.code = normalize_sales_code(
            self.code
        )

        self.project_name = normalize_required_text(
            self.project_name,
            field_name="O nome do projeto",
        )

        self.description = normalize_optional_text(
            self.description
        )

        self.payment_terms = normalize_optional_text(
            self.payment_terms
        )

        self.notes = normalize_optional_text(
            self.notes
        )

        self.proposed_amount = normalize_money(
            self.proposed_amount,
            field_name="O valor proposto",
        )

        self.material_cost = normalize_money(
            self.material_cost,
            field_name="O custo de materiais",
        )

        self.labor_cost = normalize_money(
            self.labor_cost,
            field_name="O custo de mão de obra",
        )

        self.transport_cost = normalize_money(
            self.transport_cost,
            field_name="O custo de transporte",
        )

        self.other_cost = normalize_money(
            self.other_cost,
            field_name="Os outros custos",
        )

        self.tax_amount = normalize_money(
            self.tax_amount,
            field_name="O valor de impostos",
        )

        self.discount_amount = normalize_money(
            self.discount_amount,
            field_name="O desconto",
        )

        if self.approved_amount is not None:
            self.approved_amount = normalize_money(
                self.approved_amount,
                field_name="O valor aprovado",
                allow_zero=False,
            )

        self._validate_dates()
        self._validate_status()

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        customer_id: int,
        code: str,
        project_name: str,
        proposed_amount: Decimal | int | str = Decimal("0"),
        branch_id: uuid.UUID | None = None,
        salesperson_employee_id: uuid.UUID | None = None,
        description: str | None = None,
        valid_until: date | None = None,
        expected_delivery_at: date | None = None,
        payment_terms: str | None = None,
        notes: str | None = None,
        material_cost: Decimal | int | str = Decimal("0"),
        labor_cost: Decimal | int | str = Decimal("0"),
        transport_cost: Decimal | int | str = Decimal("0"),
        other_cost: Decimal | int | str = Decimal("0"),
        tax_amount: Decimal | int | str = Decimal("0"),
        discount_amount: Decimal | int | str = Decimal("0"),
    ) -> SalesQuote:
        """Create a new draft commercial quote."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            customer_id=customer_id,
            branch_id=branch_id,
            salesperson_employee_id=(
                salesperson_employee_id
            ),
            code=code,
            status=SalesQuoteStatus.DRAFT,
            project_name=project_name,
            description=description,
            issued_at=None,
            valid_until=valid_until,
            expected_delivery_at=(
                expected_delivery_at
            ),
            payment_terms=payment_terms,
            notes=notes,
            material_cost=normalize_money(
                material_cost,
                field_name="O custo de materiais",
            ),
            labor_cost=normalize_money(
                labor_cost,
                field_name="O custo de mão de obra",
            ),
            transport_cost=normalize_money(
                transport_cost,
                field_name="O custo de transporte",
            ),
            other_cost=normalize_money(
                other_cost,
                field_name="Os outros custos",
            ),
            tax_amount=normalize_money(
                tax_amount,
                field_name="O valor de impostos",
            ),
            discount_amount=normalize_money(
                discount_amount,
                field_name="O desconto",
            ),
            proposed_amount=normalize_money(
                proposed_amount,
                field_name="O valor proposto",
            ),
            approved_amount=None,
            approved_at=None,
            rejected_at=None,
            cancelled_at=None,
            expired_at=None,
            created_at=now,
            updated_at=now,
        )

    @property
    def total_cost(self) -> Decimal:
        """Return estimated total internal cost."""

        return (
            self.material_cost
            + self.labor_cost
            + self.transport_cost
            + self.other_cost
            + self.tax_amount
        )

    @property
    def estimated_profit(self) -> Decimal:
        """Return estimated profit for the proposal."""

        return (
            self.proposed_amount
            - self.total_cost
        )

    def issue(
        self,
        *,
        issued_at: datetime | None = None,
    ) -> None:
        """Send the quote to the customer."""

        if self.status is not SalesQuoteStatus.DRAFT:
            raise ValueError(
                "Somente orçamento em rascunho "
                "pode ser enviado."
            )

        if self.proposed_amount <= 0:
            raise ValueError(
                "O orçamento deve possuir valor proposto "
                "maior que zero antes do envio."
            )

        effective_issued_at = (
            issued_at
            or datetime.now(UTC)
        )

        self.status = SalesQuoteStatus.SENT
        self.issued_at = effective_issued_at

        self._validate_dates()
        self._touch()

    def start_negotiation(self) -> None:
        """Move a sent quote into negotiation."""

        if self.status not in {
            SalesQuoteStatus.SENT,
            SalesQuoteStatus.NEGOTIATION,
        }:
            raise ValueError(
                "Somente orçamento enviado pode entrar "
                "em negociação."
            )

        self.status = SalesQuoteStatus.NEGOTIATION
        self._touch()

    def approve(
        self,
        *,
        approved_amount: Decimal | int | str,
        approved_at: datetime | None = None,
    ) -> None:
        """Approve the quote and freeze its accepted amount."""

        if self.status not in {
            SalesQuoteStatus.SENT,
            SalesQuoteStatus.NEGOTIATION,
        }:
            raise ValueError(
                "Somente orçamento enviado ou em negociação "
                "pode ser aprovado."
            )

        normalized_amount = normalize_money(
            approved_amount,
            field_name="O valor aprovado",
            allow_zero=False,
        )

        effective_approved_at = (
            approved_at
            or datetime.now(UTC)
        )

        if (
            self.issued_at is not None
            and effective_approved_at < self.issued_at
        ):
            raise ValueError(
                "A aprovação não pode anteceder "
                "o envio do orçamento."
            )

        self.status = SalesQuoteStatus.APPROVED
        self.approved_amount = normalized_amount
        self.approved_at = effective_approved_at

        self.rejected_at = None
        self.cancelled_at = None
        self.expired_at = None

        self._touch()

    def reject(
        self,
        *,
        rejected_at: datetime | None = None,
    ) -> None:
        """Record explicit customer rejection."""

        if self.status not in {
            SalesQuoteStatus.SENT,
            SalesQuoteStatus.NEGOTIATION,
        }:
            raise ValueError(
                "Somente orçamento enviado ou em negociação "
                "pode ser rejeitado."
            )

        effective_rejected_at = (
            rejected_at
            or datetime.now(UTC)
        )

        self._validate_terminal_date(
            effective_rejected_at,
            "A rejeição",
        )

        self.status = SalesQuoteStatus.REJECTED
        self.rejected_at = effective_rejected_at
        self._touch()

    def cancel(
        self,
        *,
        cancelled_at: datetime | None = None,
    ) -> None:
        """Cancel a quote that has not been approved."""

        if self.status in {
            SalesQuoteStatus.APPROVED,
            SalesQuoteStatus.REJECTED,
            SalesQuoteStatus.CANCELLED,
            SalesQuoteStatus.EXPIRED,
        }:
            raise ValueError(
                "O orçamento não pode ser cancelado "
                "no status atual."
            )

        effective_cancelled_at = (
            cancelled_at
            or datetime.now(UTC)
        )

        self._validate_terminal_date(
            effective_cancelled_at,
            "O cancelamento",
        )

        self.status = SalesQuoteStatus.CANCELLED
        self.cancelled_at = effective_cancelled_at
        self._touch()

    def expire(
        self,
        *,
        expired_at: datetime | None = None,
    ) -> None:
        """Expire an unanswered quote."""

        if self.status not in {
            SalesQuoteStatus.SENT,
            SalesQuoteStatus.NEGOTIATION,
        }:
            raise ValueError(
                "Somente orçamento enviado ou em negociação "
                "pode expirar."
            )

        effective_expired_at = (
            expired_at
            or datetime.now(UTC)
        )

        self._validate_terminal_date(
            effective_expired_at,
            "A expiração",
        )

        if (
            self.valid_until is not None
            and effective_expired_at.date()
            <= self.valid_until
        ):
            raise ValueError(
                "O orçamento ainda está dentro "
                "do prazo de validade."
            )

        self.status = SalesQuoteStatus.EXPIRED
        self.expired_at = effective_expired_at
        self._touch()

    def change_proposed_amount(
        self,
        value: Decimal | int | str,
    ) -> None:
        """Change proposed amount while quote remains editable."""

        self._require_editable()

        self.proposed_amount = normalize_money(
            value,
            field_name="O valor proposto",
        )

        self._touch()

    def _require_editable(self) -> None:
        if self.status not in {
            SalesQuoteStatus.DRAFT,
            SalesQuoteStatus.SENT,
            SalesQuoteStatus.NEGOTIATION,
        }:
            raise ValueError(
                "O orçamento não pode mais ser alterado."
            )

    def _validate_dates(self) -> None:
        if (
            self.issued_at is not None
            and self.valid_until is not None
            and self.valid_until < self.issued_at.date()
        ):
            raise ValueError(
                "A validade não pode anteceder "
                "o envio do orçamento."
            )

    def _validate_status(self) -> None:
        terminal_dates = (
            self.approved_at,
            self.rejected_at,
            self.cancelled_at,
            self.expired_at,
        )

        if self.status is SalesQuoteStatus.APPROVED:
            if self.approved_amount is None:
                raise ValueError(
                    "Orçamento aprovado exige "
                    "valor aprovado."
                )

            if self.approved_at is None:
                raise ValueError(
                    "Orçamento aprovado exige "
                    "data de aprovação."
                )

        if (
            self.status is SalesQuoteStatus.REJECTED
            and self.rejected_at is None
        ):
                raise ValueError(
                    "Orçamento rejeitado exige "
                    "data de rejeição."
                )

        if (
            self.status is SalesQuoteStatus.CANCELLED
            and self.cancelled_at is None
        ):
                raise ValueError(
                    "Orçamento cancelado exige "
                    "data de cancelamento."
                )

        if (
            self.status is SalesQuoteStatus.EXPIRED
            and self.expired_at is None
        ):
                raise ValueError(
                    "Orçamento expirado exige "
                    "data de expiração."
                )

        non_null_terminal_dates = sum(
            value is not None
            for value in terminal_dates
        )

        if non_null_terminal_dates > 1:
            raise ValueError(
                "O orçamento não pode possuir "
                "múltiplos encerramentos."
            )

    def _validate_terminal_date(
        self,
        value: datetime,
        field_name: str,
    ) -> None:
        if (
            self.issued_at is not None
            and value < self.issued_at
        ):
            raise ValueError(
                f"{field_name} não pode anteceder "
                "o envio do orçamento."
            )

    @staticmethod
    def _validate_customer_id(
        value: object,
    ) -> None:
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
        ):
            raise TypeError(
                "O cliente deve possuir identificador inteiro."
            )

        if value <= 0:
            raise ValueError(
                "O identificador do cliente "
                "deve ser maior que zero."
            )

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(value, uuid.UUID):
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
class SalesQuoteItem:
    """Represent one commercial quote line snapshot."""

    tenant_id: uuid.UUID
    sales_quote_id: uuid.UUID
    sequence: int
    description_snapshot: str
    quantity: Decimal
    unit_price: Decimal
    discount_amount: Decimal

    material_id: uuid.UUID | None = None
    service_id: uuid.UUID | None = None

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )
        self._validate_uuid(
            self.sales_quote_id,
            "orçamento",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.material_id is not None:
            self._validate_uuid(
                self.material_id,
                "material",
            )

        if self.service_id is not None:
            self._validate_uuid(
                self.service_id,
                "serviço",
            )

        if (
            self.material_id is not None
            and self.service_id is not None
        ):
            raise ValueError(
                "Um item comercial não pode referenciar "
                "material e serviço simultaneamente."
            )

        if (
            not isinstance(self.sequence, int)
            or isinstance(self.sequence, bool)
        ):
            raise TypeError(
                "A sequência do item deve ser inteira."
            )

        if self.sequence <= 0:
            raise ValueError(
                "A sequência do item deve ser maior que zero."
            )

        self.description_snapshot = normalize_required_text(
            self.description_snapshot,
            field_name="A descrição do item",
        )

        self.quantity = normalize_quantity(
            self.quantity
        )

        self.unit_price = normalize_money(
            self.unit_price,
            field_name="O valor unitário",
        )

        self.discount_amount = normalize_money(
            self.discount_amount,
            field_name="O desconto do item",
        )

        if self.discount_amount > self.gross_amount:
            raise ValueError(
                "O desconto do item não pode ser maior "
                "que o valor bruto."
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        sales_quote_id: uuid.UUID,
        sequence: int,
        description_snapshot: str,
        quantity: Decimal | int | str,
        unit_price: Decimal | int | str,
        discount_amount: Decimal | int | str = Decimal("0"),
        material_id: uuid.UUID | None = None,
        service_id: uuid.UUID | None = None,
    ) -> SalesQuoteItem:
        """Create one quote item snapshot."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            sales_quote_id=sales_quote_id,
            sequence=sequence,
            description_snapshot=description_snapshot,
            quantity=normalize_quantity(
                quantity
            ),
            unit_price=normalize_money(
                unit_price,
                field_name="O valor unitário",
            ),
            discount_amount=normalize_money(
                discount_amount,
                field_name="O desconto do item",
            ),
            material_id=material_id,
            service_id=service_id,
            created_at=now,
            updated_at=now,
        )

    @property
    def gross_amount(self) -> Decimal:
        """Return quantity multiplied by unit price."""

        return (
            self.quantity
            * self.unit_price
        )

    @property
    def total_amount(self) -> Decimal:
        """Return final line amount after discount."""

        return (
            self.gross_amount
            - self.discount_amount
        )

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(value, uuid.UUID):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )
