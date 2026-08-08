"""Create employees and migrate legacy employee identity data.

Revision ID: 5bb11e5247c3
Revises: 792dc8f069c5
Create Date: 2026-08-07 13:36:51.886134
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "5bb11e5247c3"
down_revision: str | None = "792dc8f069c5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create employees and backfill safe legacy employee data."""

    op.create_table(
        "employees",
        sa.Column(
            "legacy_employee_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "branch_id",
            sa.Uuid(),
            nullable=True,
        ),
        sa.Column(
            "code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "full_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "document_number",
            sa.String(length=11),
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
            "job_title",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "contract_type",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default=sa.text("'ACTIVE'"),
            nullable=False,
        ),
        sa.Column(
            "birth_date",
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            "admission_date",
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            "termination_date",
            sa.Date(),
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
                "ck_employees_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(full_name) <> ''",
            name=op.f(
                "ck_employees_full_name_not_blank"
            ),
        ),
        sa.CheckConstraint(
            (
                "status IN ("
                "'ACTIVE', "
                "'ON_LEAVE', "
                "'INACTIVE', "
                "'TERMINATED'"
                ")"
            ),
            name=op.f(
                "ck_employees_status_valid"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name="fk_employees_branch_tenant",
        ),
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_employees_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_employees"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_employees_tenant_code",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "document_number",
            name=(
                "uq_employees_tenant_"
                "document_number"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "legacy_employee_id",
            name=(
                "uq_employees_tenant_"
                "legacy_employee_id"
            ),
        ),
    )

    op.create_index(
        "ix_employees_tenant_active",
        "employees",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        "ix_employees_tenant_branch",
        "employees",
        [
            "tenant_id",
            "branch_id",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_employees_tenant_id"
        ),
        "employees",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_employees_tenant_status",
        "employees",
        [
            "tenant_id",
            "status",
        ],
        unique=False,
    )

    _create_legacy_cpf_validator()
    _validate_legacy_employee_preconditions()
    _backfill_legacy_employees()
    _drop_legacy_cpf_validator()


def downgrade() -> None:
    """Remove employees while preserving all legacy employee data."""

    op.drop_index(
        "ix_employees_tenant_status",
        table_name="employees",
    )

    op.drop_index(
        op.f(
            "ix_employees_tenant_id"
        ),
        table_name="employees",
    )

    op.drop_index(
        "ix_employees_tenant_branch",
        table_name="employees",
    )

    op.drop_index(
        "ix_employees_tenant_active",
        table_name="employees",
    )

    op.drop_table(
        "employees"
    )


def _create_legacy_cpf_validator() -> None:
    """Create a temporary migration helper for CPF validation."""

    op.execute(
        sa.text(
            """
            CREATE OR REPLACE FUNCTION
                migration_5bb11e5247c3_is_valid_cpf(
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

                IF length(normalized) <> 11 THEN
                    RETURN FALSE;
                END IF;

                IF normalized ~ '^([0-9])\\1{10}$' THEN
                    RETURN FALSE;
                END IF;

                FOR position_index IN 1..9 LOOP
                    first_total := first_total
                        + substring(
                            normalized,
                            position_index,
                            1
                        )::INTEGER
                        * (11 - position_index);
                END LOOP;

                first_digit := 11 - (
                    first_total % 11
                );

                IF first_digit >= 10 THEN
                    first_digit := 0;
                END IF;

                FOR position_index IN 1..10 LOOP
                    second_total := second_total
                        + substring(
                            normalized,
                            position_index,
                            1
                        )::INTEGER
                        * (12 - position_index);
                END LOOP;

                second_digit := 11 - (
                    second_total % 11
                );

                IF second_digit >= 10 THEN
                    second_digit := 0;
                END IF;

                RETURN substring(
                    normalized,
                    10,
                    1
                )::INTEGER = first_digit
                AND substring(
                    normalized,
                    11,
                    1
                )::INTEGER = second_digit;
            END;
            $$;
            """
        )
    )


def _validate_legacy_employee_preconditions() -> None:
    """Fail safely when legacy data cannot be migrated unambiguously."""

    op.execute(
        sa.text(
            """
            DO $$
            DECLARE
                legacy_count BIGINT;
                legacy_tenant_count BIGINT;
                blank_name_count BIGINT;
                invalid_date_count BIGINT;
                duplicate_cpf_count BIGINT;
            BEGIN
                SELECT COUNT(*)
                INTO legacy_count
                FROM funcionarios;

                IF legacy_count = 0 THEN
                    RETURN;
                END IF;

                SELECT COUNT(*)
                INTO legacy_tenant_count
                FROM tenants
                WHERE
                    legacy_config_id IS NOT NULL
                    AND is_active = TRUE;

                IF legacy_tenant_count <> 1 THEN
                    RAISE EXCEPTION
                        'Employee migration requires exactly '
                        'one active tenant linked to legacy '
                        'configuration; found %.',
                        legacy_tenant_count;
                END IF;

                SELECT COUNT(*)
                INTO blank_name_count
                FROM funcionarios
                WHERE
                    nome_completo IS NULL
                    OR btrim(nome_completo) = '';

                IF blank_name_count > 0 THEN
                    RAISE EXCEPTION
                        'Employee migration found % legacy '
                        'employees with blank names.',
                        blank_name_count;
                END IF;

                SELECT COUNT(*)
                INTO invalid_date_count
                FROM funcionarios
                WHERE
                    data_nascimento IS NOT NULL
                    AND data_admissao IS NOT NULL
                    AND data_nascimento
                        >= data_admissao;

                IF invalid_date_count > 0 THEN
                    RAISE EXCEPTION
                        'Employee migration found % legacy '
                        'employees with invalid birth and '
                        'admission dates.',
                        invalid_date_count;
                END IF;

                SELECT COUNT(*)
                INTO duplicate_cpf_count
                FROM (
                    SELECT
                        regexp_replace(
                            cpf,
                            '[^0-9]',
                            '',
                            'g'
                        ) AS normalized_cpf
                    FROM funcionarios
                    WHERE
                        NULLIF(
                            btrim(cpf),
                            ''
                        ) IS NOT NULL
                        AND
                        migration_5bb11e5247c3_is_valid_cpf(
                            cpf
                        )
                    GROUP BY
                        regexp_replace(
                            cpf,
                            '[^0-9]',
                            '',
                            'g'
                        )
                    HAVING COUNT(*) > 1
                ) AS duplicates;

                IF duplicate_cpf_count > 0 THEN
                    RAISE EXCEPTION
                        'Employee migration found % duplicate '
                        'valid normalized CPF values.',
                        duplicate_cpf_count;
                END IF;
            END;
            $$;
            """
        )
    )


def _backfill_legacy_employees() -> None:
    """Backfill safe employee identity data from funcionarios."""

    op.execute(
        sa.text(
            """
            WITH legacy_tenant AS (
                SELECT id
                FROM tenants
                WHERE
                    legacy_config_id IS NOT NULL
                    AND is_active = TRUE
                ORDER BY id
                LIMIT 1
            ),
            normalized AS (
                SELECT
                    f.*,
                    regexp_replace(
                        COALESCE(
                            f.cpf,
                            ''
                        ),
                        '[^0-9]',
                        '',
                        'g'
                    ) AS normalized_cpf,
                    lower(
                        btrim(
                            COALESCE(
                                f.email,
                                ''
                            )
                        )
                    ) AS normalized_email,
                    regexp_replace(
                        COALESCE(
                            f.telefone,
                            ''
                        ),
                        '[^0-9]',
                        '',
                        'g'
                    ) AS phone_digits
                FROM funcionarios AS f
            ),
            prepared AS (
                SELECT
                    n.*,
                    CASE
                        WHEN
                            length(n.phone_digits) > 11
                            AND left(
                                n.phone_digits,
                                2
                            ) = '55'
                        THEN substring(
                            n.phone_digits
                            FROM 3
                        )
                        ELSE n.phone_digits
                    END AS normalized_phone
                FROM normalized AS n
            )
            INSERT INTO employees (
                id,
                tenant_id,
                legacy_employee_id,
                branch_id,
                code,
                full_name,
                document_number,
                email,
                phone,
                job_title,
                contract_type,
                status,
                birth_date,
                admission_date,
                termination_date,
                is_active,
                created_at,
                updated_at
            )
            SELECT
                (
                    substring(
                        employee_hash,
                        1,
                        8
                    )
                    || '-'
                    || substring(
                        employee_hash,
                        9,
                        4
                    )
                    || '-'
                    || substring(
                        employee_hash,
                        13,
                        4
                    )
                    || '-'
                    || substring(
                        employee_hash,
                        17,
                        4
                    )
                    || '-'
                    || substring(
                        employee_hash,
                        21,
                        12
                    )
                )::UUID,
                legacy_tenant.id,
                prepared.id,
                NULL,
                'EMP-'
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
                btrim(
                    prepared.nome_completo
                ),
                CASE
                    WHEN
                        NULLIF(
                            btrim(
                                prepared.cpf
                            ),
                            ''
                        ) IS NOT NULL
                        AND
                        migration_5bb11e5247c3_is_valid_cpf(
                            prepared.cpf
                        )
                    THEN prepared.normalized_cpf
                    ELSE NULL
                END,
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
                    THEN prepared.normalized_email
                    ELSE NULL
                END,
                CASE
                    WHEN length(
                        prepared.normalized_phone
                    ) IN (
                        10,
                        11
                    )
                    THEN prepared.normalized_phone
                    ELSE NULL
                END,
                NULLIF(
                    btrim(
                        prepared.funcao
                    ),
                    ''
                ),
                NULLIF(
                    btrim(
                        prepared.tipo_contrato
                    ),
                    ''
                ),
                CASE upper(
                    btrim(
                        COALESCE(
                            prepared.status,
                            ''
                        )
                    )
                )
                    WHEN 'ATIVO'
                        THEN 'ACTIVE'
                    WHEN 'ACTIVE'
                        THEN 'ACTIVE'
                    WHEN 'AFASTADO'
                        THEN 'ON_LEAVE'
                    WHEN 'ON_LEAVE'
                        THEN 'ON_LEAVE'
                    ELSE 'INACTIVE'
                END,
                prepared.data_nascimento,
                prepared.data_admissao,
                NULL,
                CASE upper(
                    btrim(
                        COALESCE(
                            prepared.status,
                            ''
                        )
                    )
                )
                    WHEN 'ATIVO'
                        THEN TRUE
                    WHEN 'ACTIVE'
                        THEN TRUE
                    WHEN 'AFASTADO'
                        THEN TRUE
                    WHEN 'ON_LEAVE'
                        THEN TRUE
                    ELSE FALSE
                END,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            FROM prepared
            CROSS JOIN legacy_tenant
            CROSS JOIN LATERAL (
                SELECT md5(
                    'organizeg3:employee:'
                    || legacy_tenant.id::TEXT
                    || ':'
                    || prepared.id::TEXT
                ) AS employee_hash
            ) AS generated
            WHERE NOT EXISTS (
                SELECT 1
                FROM employees AS existing
                WHERE
                    existing.tenant_id
                        = legacy_tenant.id
                    AND existing.legacy_employee_id
                        = prepared.id
            );
            """
        )
    )


def _drop_legacy_cpf_validator() -> None:
    """Remove the migration-only CPF helper."""

    op.execute(
        sa.text(
            """
            DROP FUNCTION IF EXISTS
                migration_5bb11e5247c3_is_valid_cpf(
                    TEXT
                );
            """
        )
    )
