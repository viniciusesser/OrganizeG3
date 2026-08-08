"""Application schemas for brand operations."""

from __future__ import annotations

from datetime import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from organizeg3_api.domain.brand.entity import (
    Brand,
)
from organizeg3_api.domain.brand.value_objects import (
    BrandCode,
    BrandName,
)


class BrandCreate(BaseModel):
    """Payload used to create a brand."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    code: str = Field(
        min_length=1,
        max_length=100,
    )

    name: str = Field(
        min_length=1,
        max_length=255,
    )

    @field_validator(
        "code",
    )
    @classmethod
    def normalize_code(
        cls,
        value: str,
    ) -> str:
        """Normalize the brand code."""

        return BrandCode(
            value
        ).value

    @field_validator(
        "name",
    )
    @classmethod
    def normalize_name(
        cls,
        value: str,
    ) -> str:
        """Normalize the brand name."""

        return BrandName(
            value
        ).value


class BrandUpdate(BaseModel):
    """Payload used for partial brand updates."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    code: str | None = Field(
        default=None,
        max_length=100,
    )

    name: str | None = Field(
        default=None,
        max_length=255,
    )

    @field_validator(
        "code",
    )
    @classmethod
    def normalize_code(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional brand code."""

        if value is None:
            return None

        return BrandCode(
            value
        ).value

    @field_validator(
        "name",
    )
    @classmethod
    def normalize_name(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional brand name."""

        if value is None:
            return None

        return BrandName(
            value
        ).value


class BrandResponse(BaseModel):
    """Public application representation of a brand."""

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    tenant_id: uuid.UUID

    code: str
    name: str

    is_active: bool

    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def from_entity(
        cls,
        brand: Brand,
    ) -> BrandResponse:
        """Build a response from one persisted brand."""

        if brand.id is None:
            raise ValueError(
                "A marca deve possuir identificador "
                "para ser apresentada."
            )

        return cls(
            id=brand.id,
            tenant_id=brand.tenant_id,
            code=brand.code,
            name=brand.name,
            is_active=brand.is_active,
            created_at=brand.created_at,
            updated_at=brand.updated_at,
        )
