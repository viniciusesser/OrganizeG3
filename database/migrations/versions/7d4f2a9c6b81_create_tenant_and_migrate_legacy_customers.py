"""Create root tenant and migrate legacy customers.

Revision ID: 7d4f2a9c6b81
Revises: 0439fdabfa05
Create Date: 2026-08-05
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "7d4f2a9c6b81"
down_revision: str | None = "0439fdabfa05"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ROOT_TENANT_ID = (
    "b25e0e50-b18d-5c5e-900a-f0ca7f01028f"
)
_NULL_TENANT_ID = (
    "00000000-0000-0000-0000-000000000000"
)

_BACKUP_TABLE = (
    "migration_7d4f2a9c6b81_customer_backup"
)

_BACKUP_CUSTOMERS_SQL = """
INSERT INTO migration_7d4f2a9c6b81_customer_backup (
    customer_id,
    tenant_id_before,
    customer_type_before,
    document_number_before,
    phone_before,
    code_before,
    row_version_before,
    updated_at_before,
    backed_up_at
)
SELECT
    id,
    tenant_id,
    tipo_pessoa,
    cpf_cnpj,
    telefone,
    code,
    row_version,
    updated_at,
    CURRENT_TIMESTAMP
FROM clientes
WHERE
    tenant_id IS NULL
    OR CAST(tenant_id AS VARCHAR)
        = '00000000-0000-0000-0000-000000000000'
"""

_INSERT_ROOT_TENANT_SQL = """
INSERT INTO tenants (
    id,
    legacy_config_id,
    name,
    legal_name,
    document_number,
    email,
    phone,
    status,
    is_active,
    created_at,
    updated_at
)
SELECT
    'b25e0e50-b18d-5c5e-900a-f0ca7f01028f',
    id,
    COALESCE(
        NULLIF(TRIM(empresa_nome), ''),
        'MARCENARIA GALDINO'
    ),
    NULLIF(
        TRIM(empresa_razao_social),
        ''
    ),
    NULLIF(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        TRIM(empresa_cnpj),
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
    ),
    NULLIF(
        LOWER(TRIM(empresa_email)),
        ''
    ),
    NULLIF(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            TRIM(empresa_telefone),
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
    ),
    CASE
        WHEN UPPER(
            COALESCE(
                TRIM(status_licenca),
                'ATIVO'
            )
        ) = 'ATIVO'
        THEN 'ACTIVE'
        ELSE 'INACTIVE'
    END,
    CASE
        WHEN UPPER(
            COALESCE(
                TRIM(status_licenca),
                'ATIVO'
            )
        ) = 'ATIVO'
        THEN TRUE
        ELSE FALSE
    END,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM configuracoes
WHERE id = 1
"""

_UPDATE_CUSTOMERS_POSTGRESQL_SQL = """
UPDATE clientes
SET
    tenant_id =
        'b25e0e50-b18d-5c5e-900a-f0ca7f01028f',
    tipo_pessoa = CASE
        WHEN UPPER(
            TRIM(
                COALESCE(
                    tipo_pessoa,
                    ''
                )
            )
        ) IN (
            'PF',
            'PESSOA FISICA',
            'PESSOA FÍSICA'
        )
        THEN 'INDIVIDUAL'

        WHEN UPPER(
            TRIM(
                COALESCE(
                    tipo_pessoa,
                    ''
                )
            )
        ) IN (
            'PJ',
            'PESSOA JURIDICA',
            'PESSOA JURÍDICA'
        )
        THEN 'CORPORATE'

        ELSE tipo_pessoa
    END,
    cpf_cnpj = CASE
        WHEN
            id = 3
            AND TRIM(
                COALESCE(
                    cpf_cnpj,
                    ''
                )
            ) = '111.222.333-44'
        THEN NULL
        ELSE cpf_cnpj
    END,
    telefone = CASE
        WHEN
            id = 3
            AND TRIM(
                COALESCE(
                    telefone,
                    ''
                )
            ) = '(11) 98765-4322'
        THEN '11987654322'
        ELSE telefone
    END,
    code = CASE
        WHEN
            code IS NULL
            OR TRIM(code) = ''
            OR UPPER(TRIM(code)) = 'LEGADO'
        THEN
            'LEGADO-'
            || LPAD(
                CAST(id AS VARCHAR),
                6,
                '0'
            )
        ELSE code
    END,
    row_version = COALESCE(
        row_version,
        1
    ) + 1,
    updated_at = CURRENT_TIMESTAMP
WHERE
    (
        tenant_id IS NULL
        OR CAST(tenant_id AS VARCHAR)
            = '00000000-0000-0000-0000-000000000000'
    )
    AND EXISTS (
        SELECT 1
        FROM tenants
        WHERE id =
            'b25e0e50-b18d-5c5e-900a-f0ca7f01028f'
    )
"""

_UPDATE_CUSTOMERS_SQLITE_SQL = """
UPDATE clientes
SET
    tenant_id =
        'b25e0e50-b18d-5c5e-900a-f0ca7f01028f',
    tipo_pessoa = CASE
        WHEN UPPER(
            TRIM(
                COALESCE(
                    tipo_pessoa,
                    ''
                )
            )
        ) IN (
            'PF',
            'PESSOA FISICA',
            'PESSOA FÍSICA'
        )
        THEN 'INDIVIDUAL'

        WHEN UPPER(
            TRIM(
                COALESCE(
                    tipo_pessoa,
                    ''
                )
            )
        ) IN (
            'PJ',
            'PESSOA JURIDICA',
            'PESSOA JURÍDICA'
        )
        THEN 'CORPORATE'

        ELSE tipo_pessoa
    END,
    cpf_cnpj = CASE
        WHEN
            id = 3
            AND TRIM(
                COALESCE(
                    cpf_cnpj,
                    ''
                )
            ) = '111.222.333-44'
        THEN NULL
        ELSE cpf_cnpj
    END,
    telefone = CASE
        WHEN
            id = 3
            AND TRIM(
                COALESCE(
                    telefone,
                    ''
                )
            ) = '(11) 98765-4322'
        THEN '11987654322'
        ELSE telefone
    END,
    code = CASE
        WHEN
            code IS NULL
            OR TRIM(code) = ''
            OR UPPER(TRIM(code)) = 'LEGADO'
        THEN
            'LEGADO-'
            || PRINTF(
                '%06d',
                id
            )
        ELSE code
    END,
    row_version = COALESCE(
        row_version,
        1
    ) + 1,
    updated_at = CURRENT_TIMESTAMP
WHERE
    (
        tenant_id IS NULL
        OR CAST(tenant_id AS VARCHAR)
            = '00000000-0000-0000-0000-000000000000'
    )
    AND EXISTS (
        SELECT 1
        FROM tenants
        WHERE id =
            'b25e0e50-b18d-5c5e-900a-f0ca7f01028f'
    )
"""

_RESTORE_CUSTOMERS_SQL = """
UPDATE clientes
SET
    tenant_id = (
        SELECT tenant_id_before
        FROM migration_7d4f2a9c6b81_customer_backup
        WHERE customer_id = clientes.id
    ),
    tipo_pessoa = (
        SELECT customer_type_before
        FROM migration_7d4f2a9c6b81_customer_backup
        WHERE customer_id = clientes.id
    ),
    cpf_cnpj = (
        SELECT document_number_before
        FROM migration_7d4f2a9c6b81_customer_backup
        WHERE customer_id = clientes.id
    ),
    telefone = (
        SELECT phone_before
        FROM migration_7d4f2a9c6b81_customer_backup
        WHERE customer_id = clientes.id
    ),
    code = (
        SELECT code_before
        FROM migration_7d4f2a9c6b81_customer_backup
        WHERE customer_id = clientes.id
    ),
    row_version = (
        SELECT row_version_before
        FROM migration_7d4f2a9c6b81_customer_backup
        WHERE customer_id = clientes.id
    ),
    updated_at = (
        SELECT updated_at_before
        FROM migration_7d4f2a9c6b81_customer_backup
        WHERE customer_id = clientes.id
    )
WHERE EXISTS (
    SELECT 1
    FROM migration_7d4f2a9c6b81_customer_backup
    WHERE customer_id = clientes.id
)
"""

_DELETE_ROOT_TENANT_SQL = """
DELETE FROM tenants
WHERE id =
    'b25e0e50-b18d-5c5e-900a-f0ca7f01028f'
"""


def upgrade() -> None:
    """Create root tenant and migrate legacy customers."""

    op.create_table(
        "tenants",
        sa.Column(
            "id",
            sa.Uuid(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "legacy_config_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "name",
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
            "status",
            sa.String(length=30),
            nullable=False,
            server_default=sa.text(
                "'ACTIVE'"
            ),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text(
                "CURRENT_TIMESTAMP"
            ),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text(
                "CURRENT_TIMESTAMP"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_tenants",
        ),
        sa.UniqueConstraint(
            "legacy_config_id",
            name="uq_tenants_legacy_config_id",
        ),
        sa.UniqueConstraint(
            "document_number",
            name="uq_tenants_document_number",
        ),
    )

    op.create_index(
        "ix_tenants_is_active",
        "tenants",
        ["is_active"],
        unique=False,
    )

    op.create_table(
        _BACKUP_TABLE,
        sa.Column(
            "customer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id_before",
            sa.Uuid(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "customer_type_before",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "document_number_before",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "phone_before",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "code_before",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "row_version_before",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "updated_at_before",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "backed_up_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text(
                "CURRENT_TIMESTAMP"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "customer_id",
            name=(
                "pk_migration_7d4f2a9c6b81_"
                "customer_backup"
            ),
        ),
    )

    op.execute(
        sa.text(_BACKUP_CUSTOMERS_SQL)
    )

    op.execute(
        sa.text(_INSERT_ROOT_TENANT_SQL)
    )

    bind = op.get_bind()

    if bind.dialect.name == "sqlite":
        update_statement = (
            _UPDATE_CUSTOMERS_SQLITE_SQL
        )
    else:
        update_statement = (
            _UPDATE_CUSTOMERS_POSTGRESQL_SQL
        )

    op.execute(
        sa.text(update_statement)
    )


def downgrade() -> None:
    """Restore legacy customers and remove tenant structures."""

    op.execute(
        sa.text(_RESTORE_CUSTOMERS_SQL)
    )

    op.execute(
        sa.text(_DELETE_ROOT_TENANT_SQL)
    )

    op.drop_table(
        _BACKUP_TABLE
    )

    op.drop_index(
        "ix_tenants_is_active",
        table_name="tenants",
    )

    op.drop_table(
        "tenants"
    )
