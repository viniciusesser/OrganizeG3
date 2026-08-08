"""Create brands and materials and migrate safe legacy catalog data.

Revision ID: ab28ad8ed9ed
Revises: 86408a055683
Create Date: 2026-08-07 14:21:50.067110
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "ab28ad8ed9ed"
down_revision: str | None = "86408a055683"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create modern brands/materials and migrate safe legacy catalog data."""

    _create_brands_table()
    _create_materials_table()

    _validate_legacy_catalog_preconditions()

    _backfill_legacy_brands()
    _backfill_legacy_materials()


def downgrade() -> None:
    """Remove modern catalog tables while preserving all legacy data."""

    op.drop_index(
        "ix_materials_tenant_name",
        table_name="materials",
    )

    op.drop_index(
        op.f(
            "ix_materials_tenant_id"
        ),
        table_name="materials",
    )

    op.drop_index(
        "ix_materials_tenant_category",
        table_name="materials",
    )

    op.drop_index(
        "ix_materials_tenant_brand",
        table_name="materials",
    )

    op.drop_index(
        "ix_materials_tenant_active",
        table_name="materials",
    )

    op.drop_table(
        "materials"
    )

    op.drop_index(
        op.f(
            "ix_brands_tenant_id"
        ),
        table_name="brands",
    )

    op.drop_index(
        "ix_brands_tenant_active",
        table_name="brands",
    )

    op.drop_table(
        "brands"
    )


def _create_brands_table() -> None:
    """Create the modern tenant-scoped brands table."""

    op.create_table(
        "brands",
        sa.Column(
            "legacy_brand_id",
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
            "is_active",
            sa.Boolean(),
            server_default=sa.text(
                "true"
            ),
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
            sa.DateTime(
                timezone=True
            ),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(
                timezone=True
            ),
            nullable=False,
        ),
        sa.CheckConstraint(
            "TRIM(code) <> ''",
            name=op.f(
                "ck_brands_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(name) <> ''",
            name=op.f(
                "ck_brands_name_not_blank"
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
                "fk_brands_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_brands"
            ),
        ),
        sa.UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_brands_id_tenant",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_brands_tenant_code",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "legacy_brand_id",
            name=(
                "uq_brands_tenant_"
                "legacy_brand_id"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "name",
            name="uq_brands_tenant_name",
        ),
    )

    op.create_index(
        "ix_brands_tenant_active",
        "brands",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_brands_tenant_id"
        ),
        "brands",
        [
            "tenant_id",
        ],
        unique=False,
    )


def _create_materials_table() -> None:
    """Create the modern tenant-scoped materials table."""

    op.create_table(
        "materials",
        sa.Column(
            "legacy_material_id",
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
            "category",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "unit",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "brand_id",
            sa.Uuid(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text(
                "true"
            ),
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
            sa.DateTime(
                timezone=True
            ),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(
                timezone=True
            ),
            nullable=False,
        ),
        sa.CheckConstraint(
            "TRIM(category) <> ''",
            name=op.f(
                "ck_materials_category_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(code) <> ''",
            name=op.f(
                "ck_materials_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(name) <> ''",
            name=op.f(
                "ck_materials_name_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(unit) <> ''",
            name=op.f(
                "ck_materials_unit_not_blank"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "brand_id",
                "tenant_id",
            ],
            [
                "brands.id",
                "brands.tenant_id",
            ],
            name="fk_materials_brand_tenant",
        ),
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_materials_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_materials"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_materials_tenant_code",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "legacy_material_id",
            name=(
                "uq_materials_tenant_"
                "legacy_material_id"
            ),
        ),
    )

    op.create_index(
        "ix_materials_tenant_active",
        "materials",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        "ix_materials_tenant_brand",
        "materials",
        [
            "tenant_id",
            "brand_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_materials_tenant_category",
        "materials",
        [
            "tenant_id",
            "category",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_materials_tenant_id"
        ),
        "materials",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_materials_tenant_name",
        "materials",
        [
            "tenant_id",
            "name",
        ],
        unique=False,
    )


def _validate_legacy_catalog_preconditions() -> None:
    """Reject ambiguous or unsafe legacy catalog data."""

    op.execute(
        sa.text(
            """
            DO $$
            DECLARE
                legacy_brand_count BIGINT;
                legacy_material_count BIGINT;
                legacy_tenant_count BIGINT;

                invalid_brand_id_count BIGINT;
                blank_brand_name_count BIGINT;
                oversized_brand_name_count BIGINT;
                duplicate_brand_name_count BIGINT;

                invalid_material_id_count BIGINT;
                blank_material_name_count BIGINT;
                blank_material_category_count BIGINT;
                blank_material_unit_count BIGINT;
                oversized_material_count BIGINT;
                orphan_brand_reference_count BIGINT;
            BEGIN
                SELECT COUNT(*)
                INTO legacy_brand_count
                FROM marcas;

                SELECT COUNT(*)
                INTO legacy_material_count
                FROM materiais;

                IF
                    legacy_brand_count = 0
                    AND legacy_material_count = 0
                THEN
                    RETURN;
                END IF;

                SELECT COUNT(*)
                INTO legacy_tenant_count
                FROM tenants
                WHERE legacy_config_id IS NOT NULL;

                IF legacy_tenant_count <> 1 THEN
                    RAISE EXCEPTION
                        'Catalog migration requires exactly '
                        'one tenant linked to legacy '
                        'configuration; found %.',
                        legacy_tenant_count;
                END IF;

                SELECT COUNT(*)
                INTO invalid_brand_id_count
                FROM marcas
                WHERE id <= 0;

                IF invalid_brand_id_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % brands '
                        'with non-positive legacy IDs.',
                        invalid_brand_id_count;
                END IF;

                SELECT COUNT(*)
                INTO blank_brand_name_count
                FROM marcas
                WHERE
                    nome IS NULL
                    OR btrim(nome) = '';

                IF blank_brand_name_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % brands '
                        'without a valid name.',
                        blank_brand_name_count;
                END IF;

                SELECT COUNT(*)
                INTO oversized_brand_name_count
                FROM marcas
                WHERE
                    length(
                        btrim(nome)
                    ) > 255;

                IF oversized_brand_name_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % brands '
                        'with names exceeding 255 '
                        'characters.',
                        oversized_brand_name_count;
                END IF;

                SELECT COUNT(*)
                INTO duplicate_brand_name_count
                FROM (
                    SELECT
                        lower(
                            btrim(nome)
                        )
                    FROM marcas
                    WHERE
                        nome IS NOT NULL
                        AND btrim(nome) <> ''
                    GROUP BY
                        lower(
                            btrim(nome)
                        )
                    HAVING COUNT(*) > 1
                ) AS duplicates;

                IF duplicate_brand_name_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % groups '
                        'of duplicate normalized brand '
                        'names.',
                        duplicate_brand_name_count;
                END IF;

                SELECT COUNT(*)
                INTO invalid_material_id_count
                FROM materiais
                WHERE id <= 0;

                IF invalid_material_id_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % materials '
                        'with non-positive legacy IDs.',
                        invalid_material_id_count;
                END IF;

                SELECT COUNT(*)
                INTO blank_material_name_count
                FROM materiais
                WHERE
                    nome IS NULL
                    OR btrim(nome) = '';

                IF blank_material_name_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % materials '
                        'without a valid name.',
                        blank_material_name_count;
                END IF;

                SELECT COUNT(*)
                INTO blank_material_category_count
                FROM materiais
                WHERE
                    categoria IS NULL
                    OR btrim(categoria) = '';

                IF blank_material_category_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % materials '
                        'without a valid category.',
                        blank_material_category_count;
                END IF;

                SELECT COUNT(*)
                INTO blank_material_unit_count
                FROM materiais
                WHERE
                    unidade IS NULL
                    OR btrim(unidade) = '';

                IF blank_material_unit_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % materials '
                        'without a valid unit.',
                        blank_material_unit_count;
                END IF;

                SELECT COUNT(*)
                INTO oversized_material_count
                FROM materiais
                WHERE
                    length(
                        btrim(nome)
                    ) > 255
                    OR length(
                        btrim(categoria)
                    ) > 100
                    OR length(
                        btrim(unidade)
                    ) > 30;

                IF oversized_material_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % materials '
                        'with values exceeding modern '
                        'field limits.',
                        oversized_material_count;
                END IF;

                SELECT COUNT(*)
                INTO orphan_brand_reference_count
                FROM materiais AS material
                LEFT JOIN marcas AS brand
                    ON brand.id = material.marca_id
                WHERE
                    material.marca_id IS NOT NULL
                    AND brand.id IS NULL;

                IF orphan_brand_reference_count > 0 THEN
                    RAISE EXCEPTION
                        'Catalog migration found % materials '
                        'referencing missing legacy brands.',
                        orphan_brand_reference_count;
                END IF;
            END;
            $$;
            """
        )
    )


def _backfill_legacy_brands() -> None:
    """Migrate legacy brands into the tenant-scoped brand catalog."""

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
            prepared AS (
                SELECT
                    legacy_brand.id AS legacy_brand_id,
                    btrim(
                        legacy_brand.nome
                    ) AS brand_name,
                    legacy_tenant.id AS tenant_id,
                    md5(
                        'organizeg3:brand:'
                        || legacy_tenant.id::TEXT
                        || ':'
                        || legacy_brand.id::TEXT
                    ) AS brand_hash
                FROM marcas AS legacy_brand
                CROSS JOIN legacy_tenant
            )
            INSERT INTO brands (
                id,
                tenant_id,
                legacy_brand_id,
                code,
                name,
                is_active,
                created_at,
                updated_at
            )
            SELECT
                (
                    substring(
                        brand_hash,
                        1,
                        8
                    )
                    || '-'
                    || substring(
                        brand_hash,
                        9,
                        4
                    )
                    || '-'
                    || substring(
                        brand_hash,
                        13,
                        4
                    )
                    || '-'
                    || substring(
                        brand_hash,
                        17,
                        4
                    )
                    || '-'
                    || substring(
                        brand_hash,
                        21,
                        12
                    )
                )::UUID,
                tenant_id,
                legacy_brand_id,
                'MARCA-'
                    || CASE
                        WHEN length(
                            legacy_brand_id::TEXT
                        ) < 6
                        THEN lpad(
                            legacy_brand_id::TEXT,
                            6,
                            '0'
                        )
                        ELSE legacy_brand_id::TEXT
                    END,
                brand_name,
                TRUE,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            FROM prepared
            WHERE NOT EXISTS (
                SELECT 1
                FROM brands AS existing
                WHERE
                    existing.tenant_id
                        = prepared.tenant_id
                    AND existing.legacy_brand_id
                        = prepared.legacy_brand_id
            );
            """
        )
    )


def _backfill_legacy_materials() -> None:
    """Migrate catalog-only legacy material data."""

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
            prepared AS (
                SELECT
                    legacy_material.id
                        AS legacy_material_id,
                    btrim(
                        legacy_material.nome
                    ) AS material_name,
                    btrim(
                        legacy_material.categoria
                    ) AS material_category,
                    upper(
                        btrim(
                            legacy_material.unidade
                        )
                    ) AS material_unit,
                    legacy_material.marca_id
                        AS legacy_brand_id,
                    COALESCE(
                        legacy_material.ativo,
                        TRUE
                    ) AS material_is_active,
                    legacy_tenant.id
                        AS tenant_id,
                    md5(
                        'organizeg3:material:'
                        || legacy_tenant.id::TEXT
                        || ':'
                        || legacy_material.id::TEXT
                    ) AS material_hash
                FROM materiais AS legacy_material
                CROSS JOIN legacy_tenant
            )
            INSERT INTO materials (
                id,
                tenant_id,
                legacy_material_id,
                code,
                name,
                category,
                unit,
                brand_id,
                is_active,
                created_at,
                updated_at
            )
            SELECT
                (
                    substring(
                        prepared.material_hash,
                        1,
                        8
                    )
                    || '-'
                    || substring(
                        prepared.material_hash,
                        9,
                        4
                    )
                    || '-'
                    || substring(
                        prepared.material_hash,
                        13,
                        4
                    )
                    || '-'
                    || substring(
                        prepared.material_hash,
                        17,
                        4
                    )
                    || '-'
                    || substring(
                        prepared.material_hash,
                        21,
                        12
                    )
                )::UUID,
                prepared.tenant_id,
                prepared.legacy_material_id,
                'MAT-'
                    || CASE
                        WHEN length(
                            prepared.legacy_material_id::TEXT
                        ) < 6
                        THEN lpad(
                            prepared.legacy_material_id::TEXT,
                            6,
                            '0'
                        )
                        ELSE
                            prepared.legacy_material_id::TEXT
                    END,
                prepared.material_name,
                prepared.material_category,
                prepared.material_unit,
                modern_brand.id,
                prepared.material_is_active,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            FROM prepared
            LEFT JOIN brands AS modern_brand
                ON
                    modern_brand.tenant_id
                        = prepared.tenant_id
                    AND modern_brand.legacy_brand_id
                        = prepared.legacy_brand_id
            WHERE NOT EXISTS (
                SELECT 1
                FROM materials AS existing
                WHERE
                    existing.tenant_id
                        = prepared.tenant_id
                    AND existing.legacy_material_id
                        = prepared.legacy_material_id
            );
            """
        )
    )
