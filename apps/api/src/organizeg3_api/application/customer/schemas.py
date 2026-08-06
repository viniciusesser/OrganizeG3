"""Customer DTOs used by the application and HTTP layers."""

from __future__ import annotations

from typing import Self
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from organizeg3_api.domain.customer.entity import (
    CustomerType,
)
from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
    PhoneNumber,
    optional_document,
)


class CustomerContactFields(BaseModel):
    """Shared normalized identity and contact fields."""

    document_number: str | None = Field(
        default=None,
        max_length=30,
    )
    email: str | None = Field(
        default=None,
        max_length=255,
    )
    phone: str | None = Field(
        default=None,
        max_length=50,
    )

    @field_validator(
        "document_number",
        mode="before",
    )
    @classmethod
    def validate_document_number(
        cls,
        value: object,
    ) -> str | None:
        if (
            value is None
            or not str(value).strip()
        ):
            return None

        return str(
            DocumentNumber(str(value))
        )

    @field_validator(
        "email",
        mode="before",
    )
    @classmethod
    def validate_email(
        cls,
        value: object,
    ) -> str | None:
        if (
            value is None
            or not str(value).strip()
        ):
            return None

        return str(
            EmailAddress(str(value))
        )

    @field_validator(
        "phone",
        mode="before",
    )
    @classmethod
    def validate_phone(
        cls,
        value: object,
    ) -> str | None:
        if (
            value is None
            or not str(value).strip()
        ):
            return None

        return str(
            PhoneNumber(str(value))
        )


class CustomerCreate(CustomerContactFields):
    """Payload accepted when creating a customer."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: str = Field(
        min_length=1,
        max_length=255,
    )
    customer_type: CustomerType = (
        CustomerType.INDIVIDUAL
    )

    @model_validator(mode="after")
    def validate_document_type(
        self,
    ) -> Self:
        document = optional_document(
            self.document_number
        )

        if document is None:
            return self

        if (
            self.customer_type
            is CustomerType.INDIVIDUAL
            and not document.is_cpf
        ):
            raise ValueError(
                "Cliente pessoa física deve utilizar CPF."
            )

        if (
            self.customer_type
            is CustomerType.CORPORATE
            and not document.is_cnpj
        ):
            raise ValueError(
                "Cliente pessoa jurídica deve utilizar CNPJ."
            )

        return self


class CustomerUpdate(CustomerContactFields):
    """Partial update protected by optimistic concurrency."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    row_version: int = Field(ge=1)
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    customer_type: CustomerType | None = None

    @model_validator(mode="after")
    def validate_submitted_document_type(
        self,
    ) -> Self:
        submitted_fields = (
            self.model_fields_set
        )

        if (
            "document_number"
            not in submitted_fields
            or "customer_type"
            not in submitted_fields
        ):
            return self

        if (
            self.document_number is None
            or self.customer_type is None
        ):
            return self

        document = DocumentNumber(
            self.document_number
        )

        if (
            self.customer_type
            is CustomerType.INDIVIDUAL
            and not document.is_cpf
        ):
            raise ValueError(
                "Cliente pessoa física deve utilizar CPF."
            )

        if (
            self.customer_type
            is CustomerType.CORPORATE
            and not document.is_cnpj
        ):
            raise ValueError(
                "Cliente pessoa jurídica deve utilizar CNPJ."
            )

        return self


class CustomerVersionCommand(BaseModel):
    """Command containing the expected optimistic version."""

    model_config = ConfigDict(
        extra="forbid"
    )

    row_version: int = Field(ge=1)


class CustomerResponse(BaseModel):
    """Response payload for a customer."""

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    tenant_id: uuid.UUID
    code: str
    name: str
    customer_type: CustomerType
    document_number: str | None
    email: str | None
    phone: str | None
    is_active: bool
    row_version: int
