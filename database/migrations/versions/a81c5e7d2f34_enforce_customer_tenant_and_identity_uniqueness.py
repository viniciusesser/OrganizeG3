"""Enforce customer tenant and identity uniqueness.

Revision ID: a81c5e7d2f34
Revises: 7d4f2a9c6b81
Create Date: 2026-08-05
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "a81c5e7d2f34"
down_revision: str | None = "7d4f2a9c6b81"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CUSTOMER_TENANT_FOREIGN_KEY = (
    "fk_clientes_tenant_id_tenants"
)
_CUSTOMER_TENANT_NOT_NIL_CHECK = (
    "ck_clientes_tenant_id_not_nil"
)
_CUSTOMER_DOCUMENT_UNIQUE_INDEX = (
    "uq_clientes_tenant_document_normalized"
)
_CUSTOMER_EMAIL_UNIQUE_INDEX = (
    "uq_clientes_tenant_email_normalized"
)

_NULL_TENANT_ID = (
    "00000000-0000-0000-0000-000000000000"
)

_INVALID_TENANT_COUNT_SQL = """
SELECT COUNT(*)
FROM clientes
WHERE
    tenant_id IS NULL
    OR tenant_id =
        '00000000-0000-0000-0000-000000000000'::uuid
"""

_ORPHAN_TENANT_COUNT_SQL = """
SELECT COUNT(*)
FROM clientes AS customer
LEFT JOIN tenants AS tenant
    ON tenant.id = customer.tenant_id
WHERE tenant.id IS NULL
"""

_DUPLICATE_DOCUMENT_GROUP_COUNT_SQL = """
SELECT COUNT(*)
FROM (
    SELECT
        tenant_id,
        REPLACE(
            REPLACE(
                REPLACE(
                    BTRIM(cpf_cnpj),
                    '.',
                    ''
                ),
                '-',
                ''
            ),
            '/',
            ''
        ) AS normalized_document
    FROM clientes
    WHERE
        cpf_cnpj IS NOT NULL
        AND BTRIM(cpf_cnpj) <> ''
    GROUP BY
        tenant_id,
        REPLACE(
            REPLACE(
                REPLACE(
                    BTRIM(cpf_cnpj),
                    '.',
                    ''
                ),
                '-',
                ''
            ),
            '/',
            ''
        )
    HAVING COUNT(*) > 1
) AS duplicate_documents
"""

_DUPLICATE_EMAIL_GROUP_COUNT_SQL = """
SELECT COUNT(*)
FROM (
    SELECT
        tenant_id,
        LOWER(
            BTRIM(email)
        ) AS normalized_email
    FROM clientes
    WHERE
        email IS NOT NULL
        AND BTRIM(email) <> ''
    GROUP BY
        tenant_id,
        LOWER(
            BTRIM(email)
        )
    HAVING COUNT(*) > 1
) AS duplicate_emails
"""

_INVALID_CUSTOMER_TYPE_COUNT_SQL = """
SELECT COUNT(*)
FROM clientes
WHERE
    tipo_pessoa IS NULL
    OR BTRIM(tipo_pessoa) NOT IN (
        'INDIVIDUAL',
        'CORPORATE'
    )
"""

_CREATE_DOCUMENT_INDEX_SQL = """
CREATE UNIQUE INDEX
    uq_clientes_tenant_document_normalized
ON clientes (
    tenant_id,
    (
        REPLACE(
            REPLACE(
                REPLACE(
                    BTRIM(cpf_cnpj),
                    '.',
                    ''
                ),
                '-',
                ''
            ),
            '/',
            ''
        )
    )
)
WHERE
    cpf_cnpj IS NOT NULL
    AND BTRIM(cpf_cnpj) <> ''
"""

_CREATE_EMAIL_INDEX_SQL = """
CREATE UNIQUE INDEX
    uq_clientes_tenant_email_normalized
ON clientes (
    tenant_id,
    (
        LOWER(
            BTRIM(email)
        )
    )
)
WHERE
    email IS NOT NULL
    AND BTRIM(email) <> ''
"""

_DROP_DOCUMENT_INDEX_SQL = f"""
DROP INDEX IF EXISTS
    {_CUSTOMER_DOCUMENT_UNIQUE_INDEX}
"""

_DROP_EMAIL_INDEX_SQL = f"""
DROP INDEX IF EXISTS
    {_CUSTOMER_EMAIL_UNIQUE_INDEX}
"""


def _scalar_count(
    statement: str,
) -> int:
    """Execute one defensive count query."""

    result = op.get_bind().execute(
        sa.text(statement)
    ).scalar_one()

    return int(result)


def _validate_existing_data() -> None:
    """Abort before DDL when existing rows violate constraints."""

    validations = (
        (
            _INVALID_TENANT_COUNT_SQL,
            (
                "Existem clientes sem tenant válido. "
                "Execute a auditoria e o backfill antes "
                "desta migration."
            ),
        ),
        (
            _ORPHAN_TENANT_COUNT_SQL,
            (
                "Existem clientes associados a tenants "
                "inexistentes."
            ),
        ),
        (
            _DUPLICATE_DOCUMENT_GROUP_COUNT_SQL,
            (
                "Existem CPF/CNPJ duplicados dentro do "
                "mesmo tenant."
            ),
        ),
        (
            _DUPLICATE_EMAIL_GROUP_COUNT_SQL,
            (
                "Existem e-mails duplicados dentro do "
                "mesmo tenant."
            ),
        ),
        (
            _INVALID_CUSTOMER_TYPE_COUNT_SQL,
            (
                "Existem clientes com tipo de pessoa "
                "incompatível com a regra atual."
            ),
        ),
    )

    for statement, message in validations:
        if _scalar_count(statement) > 0:
            raise RuntimeError(message)


def upgrade() -> None:
    """Apply tenant and identity constraints to customers."""

    migration_context = op.get_context()

    if not migration_context.as_sql:
        _validate_existing_data()

    op.alter_column(
        "clientes",
        "tenant_id",
        existing_type=sa.Uuid(
            as_uuid=True
        ),
        nullable=False,
    )

    op.create_foreign_key(
        _CUSTOMER_TENANT_FOREIGN_KEY,
        "clientes",
        "tenants",
        ["tenant_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.create_check_constraint(
        _CUSTOMER_TENANT_NOT_NIL_CHECK,
        "clientes",
        (
            "tenant_id <> "
            f"'{_NULL_TENANT_ID}'::uuid"
        ),
    )

    op.execute(
        sa.text(
            _CREATE_DOCUMENT_INDEX_SQL
        )
    )

    op.execute(
        sa.text(
            _CREATE_EMAIL_INDEX_SQL
        )
    )


def downgrade() -> None:
    """Remove customer tenant and identity constraints."""

    op.execute(
        sa.text(
            _DROP_EMAIL_INDEX_SQL
        )
    )

    op.execute(
        sa.text(
            _DROP_DOCUMENT_INDEX_SQL
        )
    )

    op.drop_constraint(
        _CUSTOMER_TENANT_NOT_NIL_CHECK,
        "clientes",
        type_="check",
    )

    op.drop_constraint(
        _CUSTOMER_TENANT_FOREIGN_KEY,
        "clientes",
        type_="foreignkey",
    )

    op.alter_column(
        "clientes",
        "tenant_id",
        existing_type=sa.Uuid(
            as_uuid=True
        ),
        nullable=True,
    )
