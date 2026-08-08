"""Create companies and migrate existing business data.

Revision ID: e47492c9a55a
Revises: 9fb2267cbba8
Create Date: 2026-08-07 11:55:01.271818
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "e47492c9a55a"
down_revision: str | None = "9fb2267cbba8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_BACKFILL_COMPANIES_SQL = """
WITH legacy_company_data AS (
    SELECT
        tenant.id AS tenant_id,

        COALESCE(
            NULLIF(TRIM(tenant.name), ''),
            NULLIF(TRIM(config.empresa_nome), ''),
            'Empresa'
        ) AS trade_name,

        COALESCE(
            NULLIF(TRIM(tenant.legal_name), ''),
            NULLIF(TRIM(config.empresa_razao_social), '')
        ) AS legal_name,

        COALESCE(
            NULLIF(TRIM(tenant.document_number), ''),
            NULLIF(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                TRIM(config.empresa_cnpj),
                                '.',
                                ''
                            ),
                            '/',
                            ''
                        ),
                        '-',
                        ''
                    ),
                    ' ',
                    ''
                ),
                ''
            )
        ) AS raw_document_number,

        NULLIF(
            TRIM(config.empresa_inscricao_estadual),
            ''
        ) AS state_registration,

        COALESCE(
            NULLIF(
                LOWER(TRIM(tenant.email)),
                ''
            ),
            NULLIF(
                LOWER(TRIM(config.empresa_email)),
                ''
            )
        ) AS email,

        COALESCE(
            NULLIF(
                TRIM(tenant.phone),
                ''
            ),
            NULLIF(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    TRIM(config.empresa_telefone),
                                    '(',
                                    ''
                                ),
                                ')',
                                ''
                            ),
                            '-',
                            ''
                        ),
                        ' ',
                        ''
                    ),
                    '+',
                    ''
                ),
                ''
            )
        ) AS phone,

        NULLIF(
            TRIM(config.empresa_site),
            ''
        ) AS website,

        NULLIF(
            TRIM(config.empresa_logo_path),
            ''
        ) AS logo_path,

        NULLIF(
            TRIM(config.empresa_logradouro),
            ''
        ) AS street,

        NULLIF(
            TRIM(config.empresa_numero),
            ''
        ) AS number,

        NULLIF(
            TRIM(config.empresa_bairro),
            ''
        ) AS district,

        NULLIF(
            TRIM(config.empresa_cidade),
            ''
        ) AS city,

        NULLIF(
            UPPER(
                TRIM(config.empresa_estado)
            ),
            ''
        ) AS raw_state,

        NULLIF(
            REPLACE(
                REPLACE(
                    TRIM(config.empresa_cep),
                    '-',
                    ''
                ),
                ' ',
                ''
            ),
            ''
        ) AS raw_postal_code,

        tenant.is_active AS is_active,

        COALESCE(
            tenant.created_at,
            CURRENT_TIMESTAMP
        ) AS created_at,

        COALESCE(
            tenant.updated_at,
            CURRENT_TIMESTAMP
        ) AS updated_at

    FROM tenants AS tenant

    LEFT JOIN configuracoes AS config
        ON config.id = tenant.legacy_config_id
)

INSERT INTO companies (
    id,
    tenant_id,
    trade_name,
    legal_name,
    document_number,
    state_registration,
    email,
    phone,
    website,
    logo_path,
    street,
    number,
    district,
    city,
    state,
    postal_code,
    is_active,
    created_at,
    updated_at
)

SELECT
    data.tenant_id,
    data.tenant_id,
    data.trade_name,
    data.legal_name,

    CASE
        WHEN LENGTH(
            data.raw_document_number
        ) IN (11, 14)
        THEN data.raw_document_number
        ELSE NULL
    END,

    data.state_registration,
    data.email,
    data.phone,
    data.website,
    data.logo_path,
    data.street,
    data.number,
    data.district,
    data.city,

    CASE
        WHEN LENGTH(
            data.raw_state
        ) = 2
        THEN data.raw_state
        ELSE NULL
    END,

    CASE
        WHEN LENGTH(
            data.raw_postal_code
        ) = 8
        THEN data.raw_postal_code
        ELSE NULL
    END,

    data.is_active,
    data.created_at,
    data.updated_at

FROM legacy_company_data AS data

WHERE NOT EXISTS (
    SELECT 1
    FROM companies AS company
    WHERE company.tenant_id = data.tenant_id
)
"""


def upgrade() -> None:
    """Create company structures and migrate existing business data."""

    op.create_table(
        "companies",
        sa.Column(
            "trade_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "legal_name",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "document_number",
            sa.String(length=14),
            nullable=True,
        ),
        sa.Column(
            "state_registration",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "website",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "logo_path",
            sa.String(length=1024),
            nullable=True,
        ),
        sa.Column(
            "street",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "number",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "district",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "city",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "state",
            sa.String(length=2),
            nullable=True,
        ),
        sa.Column(
            "postal_code",
            sa.String(length=8),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
            "TRIM(trade_name) <> ''",
            name=op.f(
                "ck_companies_trade_name_not_blank"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name=op.f(
                "fk_companies_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_companies"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            name="uq_companies_tenant_id",
        ),
    )

    op.create_index(
        "ix_companies_tenant_active",
        "companies",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_companies_tenant_id"
        ),
        "companies",
        ["tenant_id"],
        unique=False,
    )

    op.create_index(
        "uq_companies_document_number_normalized",
        "companies",
        [
            sa.literal_column(
                "NULLIF("
                "TRIM(BOTH FROM document_number), "
                "''"
                ")"
            )
        ],
        unique=True,
    )

    op.execute(
        sa.text(
            _BACKFILL_COMPANIES_SQL
        )
    )


def downgrade() -> None:
    """Remove company structures."""

    op.drop_index(
        "uq_companies_document_number_normalized",
        table_name="companies",
    )

    op.drop_index(
        op.f(
            "ix_companies_tenant_id"
        ),
        table_name="companies",
    )

    op.drop_index(
        "ix_companies_tenant_active",
        table_name="companies",
    )

    op.drop_table(
        "companies"
    )
