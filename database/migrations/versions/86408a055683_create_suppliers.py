"""Create suppliers and migrate safe legacy supplier data.

Revision ID: 86408a055683
Revises: 5bb11e5247c3
Create Date: 2026-08-07 14:00:03.169007
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "86408a055683"
down_revision: str | None = "5bb11e5247c3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create suppliers and migrate safe legacy supplier identity data."""

    op.create_table(
        "suppliers",
        sa.Column(
            "legacy_supplier_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "trade_name",
            sa.String(length=255),
            nullable=True,
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
            "invoice_email",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "secondary_phone",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "website",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "contact_name",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "postal_code",
            sa.String(length=8),
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
            "TRIM(code) <> ''",
            name=op.f(
                "ck_suppliers_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(name) <> ''",
            name=op.f(
                "ck_suppliers_name_not_blank"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_suppliers_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_suppliers"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_suppliers_tenant_code",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "document_number",
            name=(
                "uq_suppliers_tenant_"
                "document_number"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "legacy_supplier_id",
            name=(
                "uq_suppliers_tenant_"
                "legacy_supplier_id"
            ),
        ),
    )

    op.create_index(
        "ix_suppliers_tenant_active",
        "suppliers",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_suppliers_tenant_id"
        ),
        "suppliers",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_suppliers_tenant_name",
        "suppliers",
        [
            "tenant_id",
            "name",
        ],
        unique=False,
    )

    _create_legacy_cnpj_validator()
    _validate_legacy_supplier_preconditions()
    _backfill_legacy_suppliers()
    _drop_legacy_cnpj_validator()


def downgrade() -> None:
    """Remove suppliers while preserving the legacy supplier table."""

    op.drop_index(
        "ix_suppliers_tenant_name",
        table_name="suppliers",
    )

    op.drop_index(
        op.f(
            "ix_suppliers_tenant_id"
        ),
        table_name="suppliers",
    )

    op.drop_index(
        "ix_suppliers_tenant_active",
        table_name="suppliers",
    )

    op.drop_table(
        "suppliers"
    )


def _create_legacy_cnpj_validator() -> None:
    """Create a migration-only CNPJ validation helper."""

    op.execute(
        sa.text(
            """
            CREATE OR REPLACE FUNCTION
                migration_86408a055683_is_valid_cnpj(
                    raw_value TEXT
                )
            RETURNS BOOLEAN
            LANGUAGE plpgsql
            IMMUTABLE
            AS $$
            DECLARE
                normalized TEXT;
                first_total INTEGER := 0;
                second_total INTEGER := 0;
                first_digit INTEGER;
                second_digit INTEGER;
                position_index INTEGER;
                first_weights INTEGER[] :=
                    ARRAY[
                        5, 4, 3, 2, 9, 8,
                        7, 6, 5, 4, 3, 2
                    ];
                second_weights INTEGER[] :=
                    ARRAY[
                        6, 5, 4, 3, 2, 9, 8,
                        7, 6, 5, 4, 3, 2
                    ];
            BEGIN
                IF raw_value IS NULL THEN
                    RETURN FALSE;
                END IF;

                normalized := regexp_replace(
                    raw_value,
                    '[^0-9]',
                    '',
                    'g'
                );

                IF length(normalized) <> 14 THEN
                    RETURN FALSE;
                END IF;

                IF normalized = repeat(
                    substring(
                        normalized,
                        1,
                        1
                    ),
                    14
                ) THEN
                    RETURN FALSE;
                END IF;

                FOR position_index IN 1..12 LOOP
                    first_total := first_total
                        + substring(
                            normalized,
                            position_index,
                            1
                        )::INTEGER
                        * first_weights[
                            position_index
                        ];
                END LOOP;

                first_digit := 11 - (
                    first_total % 11
                );

                IF first_digit >= 10 THEN
                    first_digit := 0;
                END IF;

                FOR position_index IN 1..13 LOOP
                    second_total := second_total
                        + substring(
                            normalized,
                            position_index,
                            1
                        )::INTEGER
                        * second_weights[
                            position_index
                        ];
                END LOOP;

                second_digit := 11 - (
                    second_total % 11
                );

                IF second_digit >= 10 THEN
                    second_digit := 0;
                END IF;

                RETURN substring(
                    normalized,
                    13,
                    1
                )::INTEGER = first_digit
                AND substring(
                    normalized,
                    14,
                    1
                )::INTEGER = second_digit;
            END;
            $$;
            """
        )
    )


def _validate_legacy_supplier_preconditions() -> None:
    """Reject ambiguous or structurally unsafe legacy supplier data."""

    op.execute(
        sa.text(
            """
            DO $$
            DECLARE
                legacy_count BIGINT;
                legacy_tenant_count BIGINT;
                blank_name_count BIGINT;
                duplicate_document_count BIGINT;
                oversized_value_count BIGINT;
            BEGIN
                SELECT COUNT(*)
                INTO legacy_count
                FROM fornecedores;

                IF legacy_count = 0 THEN
                    RETURN;
                END IF;

                SELECT COUNT(*)
                INTO legacy_tenant_count
                FROM tenants
                WHERE legacy_config_id IS NOT NULL;

                IF legacy_tenant_count <> 1 THEN
                    RAISE EXCEPTION
                        'Supplier migration requires exactly '
                        'one tenant linked to legacy '
                        'configuration; found %.',
                        legacy_tenant_count;
                END IF;

                SELECT COUNT(*)
                INTO blank_name_count
                FROM fornecedores
                WHERE
                    NULLIF(
                        btrim(nome_fantasia),
                        ''
                    ) IS NULL
                    AND NULLIF(
                        btrim(razao_social),
                        ''
                    ) IS NULL;

                IF blank_name_count > 0 THEN
                    RAISE EXCEPTION
                        'Supplier migration found % legacy '
                        'suppliers without trade name or '
                        'legal name.',
                        blank_name_count;
                END IF;

                SELECT COUNT(*)
                INTO duplicate_document_count
                FROM (
                    SELECT
                        regexp_replace(
                            cnpj,
                            '[^0-9]',
                            '',
                            'g'
                        )
                    FROM fornecedores
                    WHERE
                        NULLIF(
                            btrim(cnpj),
                            ''
                        ) IS NOT NULL
                        AND
                        migration_86408a055683_is_valid_cnpj(
                            cnpj
                        )
                    GROUP BY
                        regexp_replace(
                            cnpj,
                            '[^0-9]',
                            '',
                            'g'
                        )
                    HAVING COUNT(*) > 1
                ) AS duplicates;

                IF duplicate_document_count > 0 THEN
                    RAISE EXCEPTION
                        'Supplier migration found % duplicate '
                        'valid normalized CNPJ values.',
                        duplicate_document_count;
                END IF;

                SELECT COUNT(*)
                INTO oversized_value_count
                FROM fornecedores
                WHERE
                    length(
                        COALESCE(
                            NULLIF(
                                btrim(nome_fantasia),
                                ''
                            ),
                            NULLIF(
                                btrim(razao_social),
                                ''
                            )
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(nome_fantasia),
                            ''
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(razao_social),
                            ''
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(inscricao_estadual),
                            ''
                        )
                    ) > 50
                    OR length(
                        NULLIF(
                            btrim(email),
                            ''
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(email_nfe),
                            ''
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(site),
                            ''
                        )
                    ) > 500
                    OR length(
                        NULLIF(
                            btrim(contato_nome),
                            ''
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(endereco),
                            ''
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(numero),
                            ''
                        )
                    ) > 50
                    OR length(
                        NULLIF(
                            btrim(bairro),
                            ''
                        )
                    ) > 255
                    OR length(
                        NULLIF(
                            btrim(cidade),
                            ''
                        )
                    ) > 255;

                IF oversized_value_count > 0 THEN
                    RAISE EXCEPTION
                        'Supplier migration found % legacy '
                        'suppliers with values exceeding '
                        'the new supplier field limits.',
                        oversized_value_count;
                END IF;
            END;
            $$;
            """
        )
    )


def _backfill_legacy_suppliers() -> None:
    """Backfill safe supplier identity data from fornecedores."""

    op.execute(
        sa.text(
            """
            WITH legacy_tenant AS (
                SELECT id
                FROM tenants
                WHERE legacy_config_id IS NOT NULL
                ORDER BY id
                LIMIT 1
            ),
            normalized AS (
                SELECT
                    f.*,
                    regexp_replace(
                        COALESCE(
                            f.cnpj,
                            ''
                        ),
                        '[^0-9]',
                        '',
                        'g'
                    ) AS normalized_document,
                    lower(
                        btrim(
                            COALESCE(
                                f.email,
                                ''
                            )
                        )
                    ) AS normalized_email,
                    lower(
                        btrim(
                            COALESCE(
                                f.email_nfe,
                                ''
                            )
                        )
                    ) AS normalized_invoice_email,
                    regexp_replace(
                        COALESCE(
                            f.telefone,
                            ''
                        ),
                        '[^0-9]',
                        '',
                        'g'
                    ) AS phone_digits,
                    regexp_replace(
                        COALESCE(
                            f.telefone_secundario,
                            ''
                        ),
                        '[^0-9]',
                        '',
                        'g'
                    ) AS secondary_phone_digits,
                    regexp_replace(
                        COALESCE(
                            f.cep,
                            ''
                        ),
                        '[^0-9]',
                        '',
                        'g'
                    ) AS postal_code_digits
                FROM fornecedores AS f
            ),
            prepared AS (
                SELECT
                    normalized.*,
                    CASE
                        WHEN
                            length(
                                normalized.phone_digits
                            ) > 11
                            AND left(
                                normalized.phone_digits,
                                2
                            ) = '55'
                        THEN substring(
                            normalized.phone_digits
                            FROM 3
                        )
                        ELSE normalized.phone_digits
                    END AS normalized_phone,
                    CASE
                        WHEN
                            length(
                                normalized.secondary_phone_digits
                            ) > 11
                            AND left(
                                normalized.secondary_phone_digits,
                                2
                            ) = '55'
                        THEN substring(
                            normalized.secondary_phone_digits
                            FROM 3
                        )
                        ELSE
                            normalized.secondary_phone_digits
                    END AS normalized_secondary_phone
                FROM normalized
            )
            INSERT INTO suppliers (
                id,
                tenant_id,
                legacy_supplier_id,
                code,
                name,
                trade_name,
                legal_name,
                document_number,
                state_registration,
                email,
                invoice_email,
                phone,
                secondary_phone,
                website,
                contact_name,
                postal_code,
                street,
                number,
                district,
                city,
                state,
                is_active,
                created_at,
                updated_at
            )
            SELECT
                (
                    substring(
                        generated.supplier_hash,
                        1,
                        8
                    )
                    || '-'
                    || substring(
                        generated.supplier_hash,
                        9,
                        4
                    )
                    || '-'
                    || substring(
                        generated.supplier_hash,
                        13,
                        4
                    )
                    || '-'
                    || substring(
                        generated.supplier_hash,
                        17,
                        4
                    )
                    || '-'
                    || substring(
                        generated.supplier_hash,
                        21,
                        12
                    )
                )::UUID,
                legacy_tenant.id,
                prepared.id,
                'FORN-'
                    || CASE
                        WHEN length(
                            prepared.id::TEXT
                        ) < 6
                        THEN lpad(
                            prepared.id::TEXT,
                            6,
                            '0'
                        )
                        ELSE prepared.id::TEXT
                    END,
                COALESCE(
                    NULLIF(
                        btrim(
                            prepared.nome_fantasia
                        ),
                        ''
                    ),
                    NULLIF(
                        btrim(
                            prepared.razao_social
                        ),
                        ''
                    )
                ),
                NULLIF(
                    btrim(
                        prepared.nome_fantasia
                    ),
                    ''
                ),
                NULLIF(
                    btrim(
                        prepared.razao_social
                    ),
                    ''
                ),
                CASE
                    WHEN
                        NULLIF(
                            btrim(
                                prepared.cnpj
                            ),
                            ''
                        ) IS NOT NULL
                        AND
                        migration_86408a055683_is_valid_cnpj(
                            prepared.cnpj
                        )
                    THEN prepared.normalized_document
                    ELSE NULL
                END,
                NULLIF(
                    btrim(
                        prepared.inscricao_estadual
                    ),
                    ''
                ),
                CASE
                    WHEN
                        prepared.normalized_email <> ''
                        AND (
                            length(
                                prepared.normalized_email
                            )
                            - length(
                                replace(
                                    prepared.normalized_email,
                                    '@',
                                    ''
                                )
                            )
                        ) = 1
                        AND split_part(
                            prepared.normalized_email,
                            '@',
                            1
                        ) <> ''
                        AND split_part(
                            prepared.normalized_email,
                            '@',
                            2
                        ) <> ''
                        AND position(
                            '.'
                            IN split_part(
                                prepared.normalized_email,
                                '@',
                                2
                            )
                        ) > 0
                        AND left(
                            split_part(
                                prepared.normalized_email,
                                '@',
                                1
                            ),
                            1
                        ) <> '.'
                        AND right(
                            split_part(
                                prepared.normalized_email,
                                '@',
                                1
                            ),
                            1
                        ) <> '.'
                        AND left(
                            split_part(
                                prepared.normalized_email,
                                '@',
                                2
                            ),
                            1
                        ) <> '-'
                        AND right(
                            split_part(
                                prepared.normalized_email,
                                '@',
                                2
                            ),
                            1
                        ) <> '-'
                    THEN prepared.normalized_email
                    ELSE NULL
                END,
                CASE
                    WHEN
                        prepared.normalized_invoice_email <> ''
                        AND (
                            length(
                                prepared.normalized_invoice_email
                            )
                            - length(
                                replace(
                                    prepared.normalized_invoice_email,
                                    '@',
                                    ''
                                )
                            )
                        ) = 1
                        AND split_part(
                            prepared.normalized_invoice_email,
                            '@',
                            1
                        ) <> ''
                        AND split_part(
                            prepared.normalized_invoice_email,
                            '@',
                            2
                        ) <> ''
                        AND position(
                            '.'
                            IN split_part(
                                prepared.normalized_invoice_email,
                                '@',
                                2
                            )
                        ) > 0
                        AND left(
                            split_part(
                                prepared.normalized_invoice_email,
                                '@',
                                1
                            ),
                            1
                        ) <> '.'
                        AND right(
                            split_part(
                                prepared.normalized_invoice_email,
                                '@',
                                1
                            ),
                            1
                        ) <> '.'
                        AND left(
                            split_part(
                                prepared.normalized_invoice_email,
                                '@',
                                2
                            ),
                            1
                        ) <> '-'
                        AND right(
                            split_part(
                                prepared.normalized_invoice_email,
                                '@',
                                2
                            ),
                            1
                        ) <> '-'
                    THEN prepared.normalized_invoice_email
                    ELSE NULL
                END,
                CASE
                    WHEN
                        length(
                            prepared.normalized_phone
                        ) IN (
                            10,
                            11
                        )
                        AND left(
                            prepared.normalized_phone,
                            2
                        ) <> '00'
                    THEN prepared.normalized_phone
                    ELSE NULL
                END,
                CASE
                    WHEN
                        length(
                            prepared.normalized_secondary_phone
                        ) IN (
                            10,
                            11
                        )
                        AND left(
                            prepared.normalized_secondary_phone,
                            2
                        ) <> '00'
                    THEN
                        prepared.normalized_secondary_phone
                    ELSE NULL
                END,
                NULLIF(
                    btrim(
                        prepared.site
                    ),
                    ''
                ),
                NULLIF(
                    btrim(
                        prepared.contato_nome
                    ),
                    ''
                ),
                CASE
                    WHEN length(
                        prepared.postal_code_digits
                    ) = 8
                    THEN prepared.postal_code_digits
                    ELSE NULL
                END,
                NULLIF(
                    btrim(
                        prepared.endereco
                    ),
                    ''
                ),
                NULLIF(
                    btrim(
                        prepared.numero
                    ),
                    ''
                ),
                NULLIF(
                    btrim(
                        prepared.bairro
                    ),
                    ''
                ),
                NULLIF(
                    btrim(
                        prepared.cidade
                    ),
                    ''
                ),
                CASE
                    WHEN
                        btrim(
                            COALESCE(
                                prepared.estado,
                                ''
                            )
                        ) ~ '^[A-Za-z]{2}$'
                    THEN upper(
                        btrim(
                            prepared.estado
                        )
                    )
                    ELSE NULL
                END,
                COALESCE(
                    prepared.ativo,
                    TRUE
                ),
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            FROM prepared
            CROSS JOIN legacy_tenant
            CROSS JOIN LATERAL (
                SELECT md5(
                    'organizeg3:supplier:'
                    || legacy_tenant.id::TEXT
                    || ':'
                    || prepared.id::TEXT
                ) AS supplier_hash
            ) AS generated
            WHERE NOT EXISTS (
                SELECT 1
                FROM suppliers AS existing
                WHERE
                    existing.tenant_id
                        = legacy_tenant.id
                    AND existing.legacy_supplier_id
                        = prepared.id
            );
            """
        )
    )


def _drop_legacy_cnpj_validator() -> None:
    """Remove the migration-only CNPJ helper."""

    op.execute(
        sa.text(
            """
            DROP FUNCTION IF EXISTS
                migration_86408a055683_is_valid_cnpj(
                    TEXT
                );
            """
        )
    )
