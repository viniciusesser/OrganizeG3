"""SQLAlchemy ORM mapping for the legacy ``clientes`` table."""

from __future__ import annotations

from datetime import UTC, datetime
import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.infrastructure.database.base import (
    Base,
    CodeMixin,
    OptimisticLockMixin,
    SoftDeleteMixin,
)


class CustomerModel(
    Base,
    CodeMixin,
    OptimisticLockMixin,
    SoftDeleteMixin,
):
    """ORM mapping preserving legacy Portuguese column names."""

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "tenants.id",
            name="fk_clientes_tenant_id_tenants",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        "nome",
        String(255),
        nullable=False,
        index=True,
    )

    customer_type: Mapped[str] = mapped_column(
        "tipo_pessoa",
        String(20),
        nullable=False,
        default="INDIVIDUAL",
    )

    document_number: Mapped[str | None] = mapped_column(
        "cpf_cnpj",
        String(30),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        "email",
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        "telefone",
        String(50),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        "ativo",
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        "data_cadastro",
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
