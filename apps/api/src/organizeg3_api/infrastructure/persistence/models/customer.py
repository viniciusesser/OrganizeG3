"""SQLAlchemy ORM mapping for the legacy ``clientes`` table."""

from __future__ import annotations

from datetime import UTC, datetime
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
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

    __table_args__ = (
        CheckConstraint(
            (
                "tenant_id <> "
                "'00000000-0000-0000-0000-000000000000'"
            ),
            name="ck_clientes_tenant_id_not_nil",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_clientes_id_tenant",
        ),
        Index(
            "uq_clientes_tenant_email_normalized",
            "tenant_id",
            text("lower(btrim(email))"),
            unique=True,
            postgresql_where=text(
                "email IS NOT NULL "
                "AND btrim(email) <> ''"
            ),
        ).ddl_if(
            dialect="postgresql"
        ),
        Index(
            "uq_clientes_tenant_document_normalized",
            "tenant_id",
            text(
                "replace("
                "replace("
                "replace("
                "btrim(cpf_cnpj), "
                "'.', ''"
                "), "
                "'-', ''"
                "), "
                "'/', ''"
                ")"
            ),
            unique=True,
            postgresql_where=text(
                "cpf_cnpj IS NOT NULL "
                "AND btrim(cpf_cnpj) <> ''"
            ),
        ).ddl_if(
            dialect="postgresql"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "tenants.id",
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

    state_registration: Mapped[
        str | None
    ] = mapped_column(
        "rg_ie",
        String(50),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        "telefone",
        String(50),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        "email",
        String(255),
        nullable=True,
    )

    postal_code: Mapped[str | None] = mapped_column(
        "cep",
        String(20),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        "endereco",
        String(255),
        nullable=True,
    )

    address_number: Mapped[
        str | None
    ] = mapped_column(
        "numero",
        String(50),
        nullable=True,
    )

    address_complement: Mapped[
        str | None
    ] = mapped_column(
        "complemento",
        String(255),
        nullable=True,
    )

    district: Mapped[str | None] = mapped_column(
        "bairro",
        String(255),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        "cidade",
        String(255),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        "estado",
        String(10),
        nullable=True,
    )

    nationality: Mapped[str | None] = mapped_column(
        "nacionalidade",
        String(100),
        nullable=True,
    )

    marital_status: Mapped[
        str | None
    ] = mapped_column(
        "estado_civil",
        String(100),
        nullable=True,
    )

    profession: Mapped[str | None] = mapped_column(
        "profissao",
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        "data_cadastro",
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    is_active: Mapped[bool] = mapped_column(
        "ativo",
        Boolean,
        nullable=False,
        default=True,
    )

    notes: Mapped[str | None] = mapped_column(
        "observacoes",
        Text,
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
