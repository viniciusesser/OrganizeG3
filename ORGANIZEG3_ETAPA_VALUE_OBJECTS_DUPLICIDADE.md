# OrganizeG3 — Value Objects e política de duplicidade de Clientes

Esta etapa adiciona:

- CPF e CNPJ com validação de dígitos verificadores;
- e-mail normalizado e validado;
- telefone brasileiro normalizado e validado;
- compatibilidade entre CPF/CNPJ e tipo de cliente;
- prevenção de CPF/CNPJ e e-mail duplicados por tenant;
- reserva de identidade também para clientes arquivados;
- compatibilidade de leitura com dados legados inválidos;
- tratamento JSON seguro para erros de validação do Pydantic;
- testes unitários, de integração e API.

> Não há migration nesta etapa. A unicidade no banco será adicionada somente depois de uma auditoria dos dados legados existentes.

## 1. Criar os arquivos novos

Execute na raiz do projeto:

```powershell
$arquivos = @(
    "apps/api/src/organizeg3_api/domain/customer/value_objects.py",
    "apps/api/src/organizeg3_api/application/customer/duplication_policy.py",
    "apps/api/tests/unit/domain/test_customer_value_objects.py",
    "apps/api/tests/unit/domain/test_customer_document_compatibility.py",
    "apps/api/tests/unit/application/test_customer_duplication_policy.py",
    "apps/api/tests/integration/persistence/test_customer_uniqueness_repository.py",
    "apps/api/tests/api/test_customer_identity_routes.py",
)

foreach ($arquivo in $arquivos) {
    $pasta = Split-Path $arquivo -Parent
    New-Item -ItemType Directory -Path $pasta -Force | Out-Null

    if (-not (Test-Path $arquivo)) {
        New-Item -ItemType File -Path $arquivo | Out-Null
    }
}

Write-Host "Arquivos criados com sucesso." -ForegroundColor Green
```

## 2. Arquivos novos

### `apps/api/src/organizeg3_api/domain/customer/value_objects.py`

```python
"""Value objects for customer identity and contact data."""

from __future__ import annotations

import re
from typing import Final

_NON_DIGITS: Final = re.compile(r"\D+")
_DOMAIN_LABEL: Final = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_CPF_LENGTH: Final = 11
_CNPJ_LENGTH: Final = 14
_MAX_EMAIL_LENGTH: Final = 255
_MAX_LOCAL_PART_LENGTH: Final = 64
_BRAZIL_COUNTRY_CODE: Final = "55"


class DocumentNumber(str):
    """Validated and normalized Brazilian CPF or CNPJ."""

    def __new__(cls, value: str) -> DocumentNumber:
        if not isinstance(value, str):
            raise TypeError("CPF/CNPJ deve ser informado como texto.")

        digits = _NON_DIGITS.sub("", value)
        if len(digits) == _CPF_LENGTH:
            if not cls._is_valid_cpf(digits):
                raise ValueError("CPF inválido.")
        elif len(digits) == _CNPJ_LENGTH:
            if not cls._is_valid_cnpj(digits):
                raise ValueError("CNPJ inválido.")
        else:
            raise ValueError("CPF/CNPJ deve possuir 11 ou 14 dígitos.")

        return str.__new__(cls, digits)

    @property
    def is_cpf(self) -> bool:
        """Return whether this document is a CPF."""

        return len(self) == _CPF_LENGTH

    @property
    def is_cnpj(self) -> bool:
        """Return whether this document is a CNPJ."""

        return len(self) == _CNPJ_LENGTH

    @staticmethod
    def _is_valid_cpf(digits: str) -> bool:
        if digits == digits[0] * len(digits):
            return False

        first_total = sum(
            int(digit) * weight
            for digit, weight in zip(
                digits[:9],
                range(10, 1, -1),
                strict=True,
            )
        )
        first_remainder = first_total % 11
        first_digit = 0 if first_remainder < 2 else 11 - first_remainder
        if first_digit != int(digits[9]):
            return False

        second_total = sum(
            int(digit) * weight
            for digit, weight in zip(
                digits[:10],
                range(11, 1, -1),
                strict=True,
            )
        )
        second_remainder = second_total % 11
        second_digit = 0 if second_remainder < 2 else 11 - second_remainder
        return second_digit == int(digits[10])

    @staticmethod
    def _is_valid_cnpj(digits: str) -> bool:
        if digits == digits[0] * len(digits):
            return False

        first_weights = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        first_total = sum(
            int(digit) * weight
            for digit, weight in zip(
                digits[:12],
                first_weights,
                strict=True,
            )
        )
        first_remainder = first_total % 11
        first_digit = 0 if first_remainder < 2 else 11 - first_remainder
        if first_digit != int(digits[12]):
            return False

        second_weights = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        second_total = sum(
            int(digit) * weight
            for digit, weight in zip(
                digits[:13],
                second_weights,
                strict=True,
            )
        )
        second_remainder = second_total % 11
        second_digit = 0 if second_remainder < 2 else 11 - second_remainder
        return second_digit == int(digits[13])


class EmailAddress(str):
    """Normalized email address with conservative syntax validation."""

    def __new__(cls, value: str) -> EmailAddress:
        if not isinstance(value, str):
            raise TypeError("E-mail deve ser informado como texto.")

        normalized = value.strip().lower()
        if len(normalized) > _MAX_EMAIL_LENGTH or normalized.count("@") != 1:
            raise ValueError("E-mail inválido.")

        local_part, domain = normalized.rsplit("@", 1)
        if not local_part or len(local_part) > _MAX_LOCAL_PART_LENGTH:
            raise ValueError("E-mail inválido.")
        if local_part.startswith(".") or local_part.endswith(".") or ".." in local_part:
            raise ValueError("E-mail inválido.")
        if any(character.isspace() for character in local_part):
            raise ValueError("E-mail inválido.")

        labels = domain.split(".")
        if len(labels) < 2 or any(not _DOMAIN_LABEL.fullmatch(label) for label in labels):
            raise ValueError("E-mail inválido.")

        return str.__new__(cls, normalized)


class PhoneNumber(str):
    """Normalized Brazilian landline or mobile phone number."""

    def __new__(cls, value: str) -> PhoneNumber:
        if not isinstance(value, str):
            raise TypeError("Telefone deve ser informado como texto.")

        digits = _NON_DIGITS.sub("", value)
        if len(digits) in {12, 13} and digits.startswith(_BRAZIL_COUNTRY_CODE):
            digits = digits[len(_BRAZIL_COUNTRY_CODE) :]

        if len(digits) not in {10, _CPF_LENGTH}:
            raise ValueError("Telefone deve possuir DDD e 10 ou 11 dígitos.")
        if digits[0] == "0" or digits[1] == "0":
            raise ValueError("DDD do telefone é inválido.")
        if len(digits) == _CPF_LENGTH and digits[2] != "9":
            raise ValueError("Celular deve iniciar com 9 após o DDD.")
        if len(digits) == 10 and digits[2] not in "2345":
            raise ValueError("Telefone fixo possui prefixo inválido.")

        return str.__new__(cls, digits)


def optional_document(value: str | DocumentNumber | None) -> DocumentNumber | None:
    """Build an optional document value object."""

    if value is None or not str(value).strip():
        return None
    if isinstance(value, DocumentNumber):
        return value
    return DocumentNumber(value)


def optional_email(value: str | EmailAddress | None) -> EmailAddress | None:
    """Build an optional email value object."""

    if value is None or not str(value).strip():
        return None
    if isinstance(value, EmailAddress):
        return value
    return EmailAddress(value)


def optional_phone(value: str | PhoneNumber | None) -> PhoneNumber | None:
    """Build an optional phone value object."""

    if value is None or not str(value).strip():
        return None
    if isinstance(value, PhoneNumber):
        return value
    return PhoneNumber(value)
```

### `apps/api/src/organizeg3_api/application/customer/duplication_policy.py`

```python
"""Customer duplicate-prevention policy."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import DuplicateCustomerError
from organizeg3_api.domain.customer.repository import ICustomerRepository
from organizeg3_api.domain.customer.value_objects import DocumentNumber, EmailAddress


class CustomerDuplicationPolicy:
    """Ensure normalized customer identity data is unique per tenant."""

    def __init__(self, repository: ICustomerRepository) -> None:
        self._repository = repository

    def ensure_available(
        self,
        tenant_id: uuid.UUID,
        *,
        document_number: DocumentNumber | None,
        email: EmailAddress | None,
        exclude_customer_id: int | None = None,
    ) -> None:
        """Reject duplicate document or email, including archived records."""

        if document_number is not None and self._repository.exists_by_document(
            tenant_id,
            document_number,
            exclude_customer_id=exclude_customer_id,
        ):
            raise DuplicateCustomerError(
                "Já existe um cliente com este CPF/CNPJ.",
                details={"field": "document_number"},
            )

        if email is not None and self._repository.exists_by_email(
            tenant_id,
            email,
            exclude_customer_id=exclude_customer_id,
        ):
            raise DuplicateCustomerError(
                "Já existe um cliente com este e-mail.",
                details={"field": "email"},
            )
```

### `apps/api/tests/unit/domain/test_customer_value_objects.py`

```python
"""Unit tests for customer value objects."""

import pytest

from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
    PhoneNumber,
)

pytestmark = pytest.mark.unit


def test_normalizes_valid_cpf() -> None:
    document = DocumentNumber("529.982.247-25")

    assert document == "52998224725"
    assert document.is_cpf is True
    assert document.is_cnpj is False


def test_rejects_invalid_cpf() -> None:
    with pytest.raises(ValueError, match="CPF inválido"):
        DocumentNumber("529.982.247-24")


def test_normalizes_valid_cnpj() -> None:
    document = DocumentNumber("11.222.333/0001-81")

    assert document == "11222333000181"
    assert document.is_cnpj is True
    assert document.is_cpf is False


def test_rejects_invalid_cnpj() -> None:
    with pytest.raises(ValueError, match="CNPJ inválido"):
        DocumentNumber("11.222.333/0001-82")


def test_rejects_repeated_document_digits() -> None:
    with pytest.raises(ValueError):
        DocumentNumber("111.111.111-11")


def test_normalizes_email() -> None:
    email = EmailAddress("  CONTATO@EXAMPLE.COM  ")

    assert email == "contato@example.com"


@pytest.mark.parametrize(
    "value",
    [
        "sem-arroba.example.com",
        "duplo@@example.com",
        ".inicio@example.com",
        "fim.@example.com",
        "nome@example",
        "nome@-example.com",
    ],
)
def test_rejects_invalid_email(value: str) -> None:
    with pytest.raises(ValueError, match="E-mail inválido"):
        EmailAddress(value)


def test_normalizes_mobile_phone_with_country_code() -> None:
    phone = PhoneNumber("+55 (18) 99999-0000")

    assert phone == "18999990000"


def test_normalizes_landline_phone() -> None:
    phone = PhoneNumber("(18) 3222-4455")

    assert phone == "1832224455"


@pytest.mark.parametrize(
    "value",
    [
        "9999-0000",
        "(00) 99999-0000",
        "(18) 89999-0000",
        "(18) 9999-0000",
    ],
)
def test_rejects_invalid_phone(value: str) -> None:
    with pytest.raises(ValueError):
        PhoneNumber(value)
```

### `apps/api/tests/unit/domain/test_customer_document_compatibility.py`

```python
"""Unit tests for customer type and document compatibility."""

import uuid

import pytest

from organizeg3_api.domain.customer.entity import Customer, CustomerType

pytestmark = pytest.mark.unit


def test_individual_customer_accepts_cpf() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-0001",
        name="Pessoa Física",
        customer_type=CustomerType.INDIVIDUAL,
        document_number="529.982.247-25",
    )

    assert customer.document_number == "52998224725"


def test_corporate_customer_accepts_cnpj() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-0002",
        name="Pessoa Jurídica",
        customer_type=CustomerType.CORPORATE,
        document_number="11.222.333/0001-81",
    )

    assert customer.document_number == "11222333000181"


def test_individual_customer_rejects_cnpj() -> None:
    with pytest.raises(ValueError, match="pessoa física"):
        Customer(
            tenant_id=uuid.uuid4(),
            code="CUST-0003",
            name="Pessoa Física",
            customer_type=CustomerType.INDIVIDUAL,
            document_number="11.222.333/0001-81",
        )


def test_corporate_customer_rejects_cpf() -> None:
    with pytest.raises(ValueError, match="pessoa jurídica"):
        Customer(
            tenant_id=uuid.uuid4(),
            code="CUST-0004",
            name="Pessoa Jurídica",
            customer_type=CustomerType.CORPORATE,
            document_number="529.982.247-25",
        )


def test_legacy_invalid_contact_data_can_be_loaded() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-LEGACY",
        name="Cliente Legado",
        customer_type=CustomerType.INDIVIDUAL,
        document_number="123",
        email="EMAIL LEGADO",
        phone="SEM TELEFONE",
        _allow_legacy_contacts=True,
    )

    assert customer.document_number == "123"
    assert customer.email == "email legado"
    assert customer.phone == "SEM TELEFONE"


def test_unrelated_update_preserves_legacy_contact_data() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-LEGACY",
        name="Cliente Legado",
        customer_type=CustomerType.INDIVIDUAL,
        document_number="123",
        email="EMAIL LEGADO",
        phone="SEM TELEFONE",
        _allow_legacy_contacts=True,
    )

    customer.update_profile(
        name="Cliente Legado Atualizado",
        customer_type=CustomerType.INDIVIDUAL,
        document_number=customer.document_number,
        email=customer.email,
        phone=customer.phone,
    )

    assert customer.name == "Cliente Legado Atualizado"
    assert customer.document_number == "123"
```

### `apps/api/tests/unit/application/test_customer_duplication_policy.py`

```python
"""Unit tests for the customer duplication policy."""

from collections.abc import Sequence
import uuid

import pytest

from organizeg3_api.application.customer.duplication_policy import (
    CustomerDuplicationPolicy,
)
from organizeg3_api.core.exceptions import DuplicateCustomerError
from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.domain.customer.repository import ICustomerRepository
from organizeg3_api.domain.customer.value_objects import DocumentNumber, EmailAddress

pytestmark = pytest.mark.unit


class DuplicateCheckingRepository(ICustomerRepository):
    def __init__(self) -> None:
        self.duplicate_document = False
        self.duplicate_email = False
        self.document_exclusion: int | None = None
        self.email_exclusion: int | None = None

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        del tenant_id, customer_id, include_archived
        return None

    def list_all(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        customer_type: CustomerType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Customer]:
        del tenant_id, include_inactive, search, customer_type, limit, offset
        return []

    def save(
        self,
        customer: Customer,
        *,
        include_archived: bool = False,
    ) -> Customer:
        del include_archived
        return customer

    def exists_by_document(
        self,
        tenant_id: uuid.UUID,
        document_number: DocumentNumber,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        del tenant_id, document_number
        self.document_exclusion = exclude_customer_id
        return self.duplicate_document

    def exists_by_email(
        self,
        tenant_id: uuid.UUID,
        email: EmailAddress,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        del tenant_id, email
        self.email_exclusion = exclude_customer_id
        return self.duplicate_email


def test_accepts_available_identity_data() -> None:
    repository = DuplicateCheckingRepository()

    CustomerDuplicationPolicy(repository).ensure_available(
        uuid.uuid4(),
        document_number=DocumentNumber("52998224725"),
        email=EmailAddress("cliente@example.com"),
    )


def test_rejects_duplicate_document() -> None:
    repository = DuplicateCheckingRepository()
    repository.duplicate_document = True

    with pytest.raises(DuplicateCustomerError) as error:
        CustomerDuplicationPolicy(repository).ensure_available(
            uuid.uuid4(),
            document_number=DocumentNumber("52998224725"),
            email=None,
        )

    assert error.value.details == {"field": "document_number"}


def test_rejects_duplicate_email() -> None:
    repository = DuplicateCheckingRepository()
    repository.duplicate_email = True

    with pytest.raises(DuplicateCustomerError) as error:
        CustomerDuplicationPolicy(repository).ensure_available(
            uuid.uuid4(),
            document_number=None,
            email=EmailAddress("cliente@example.com"),
        )

    assert error.value.details == {"field": "email"}


def test_forwards_customer_exclusion_on_update() -> None:
    repository = DuplicateCheckingRepository()

    CustomerDuplicationPolicy(repository).ensure_available(
        uuid.uuid4(),
        document_number=DocumentNumber("52998224725"),
        email=EmailAddress("cliente@example.com"),
        exclude_customer_id=42,
    )

    assert repository.document_exclusion == 42
    assert repository.email_exclusion == 42
```

### `apps/api/tests/integration/persistence/test_customer_uniqueness_repository.py`

```python
"""Integration tests for customer duplicate lookup operations."""

from datetime import UTC, datetime
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.customer.value_objects import DocumentNumber, EmailAddress
from organizeg3_api.infrastructure.persistence.models.customer import CustomerModel
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)

pytestmark = [pytest.mark.integration, pytest.mark.database]


def add_customer_model(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    document_number: str | None,
    email: str | None,
    deleted_at: datetime | None = None,
) -> CustomerModel:
    model = CustomerModel(
        tenant_id=tenant_id,
        code=f"CUST-{uuid.uuid4().hex[:8].upper()}",
        name="Cliente Existente",
        customer_type="INDIVIDUAL",
        document_number=document_number,
        email=email,
        is_active=deleted_at is None,
        deleted_at=deleted_at,
    )
    session.add(model)
    session.flush()
    return model


def test_detects_formatted_document_and_case_insensitive_email(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="529.982.247-25",
        email="  CLIENTE@EXAMPLE.COM  ",
    )
    repository = SQLAlchemyCustomerRepository(session)

    assert repository.exists_by_document(
        tenant_id,
        DocumentNumber("52998224725"),
    )
    assert repository.exists_by_email(
        tenant_id,
        EmailAddress("cliente@example.com"),
    )


def test_duplicate_checks_are_tenant_scoped(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="52998224725",
        email="cliente@example.com",
    )
    repository = SQLAlchemyCustomerRepository(session)

    assert not repository.exists_by_document(
        other_tenant_id,
        DocumentNumber("52998224725"),
    )
    assert not repository.exists_by_email(
        other_tenant_id,
        EmailAddress("cliente@example.com"),
    )


def test_archived_customer_reserves_document_and_email(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="52998224725",
        email="cliente@example.com",
        deleted_at=datetime.now(UTC),
    )
    repository = SQLAlchemyCustomerRepository(session)

    assert repository.exists_by_document(
        tenant_id,
        DocumentNumber("52998224725"),
    )
    assert repository.exists_by_email(
        tenant_id,
        EmailAddress("cliente@example.com"),
    )


def test_duplicate_checks_can_exclude_current_customer(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    model = add_customer_model(
        session,
        tenant_id=tenant_id,
        document_number="52998224725",
        email="cliente@example.com",
    )
    repository = SQLAlchemyCustomerRepository(session)

    assert not repository.exists_by_document(
        tenant_id,
        DocumentNumber("52998224725"),
        exclude_customer_id=model.id,
    )
    assert not repository.exists_by_email(
        tenant_id,
        EmailAddress("cliente@example.com"),
        exclude_customer_id=model.id,
    )
```

### `apps/api/tests/api/test_customer_identity_routes.py`

```python
"""HTTP tests for customer identity validation and duplicate prevention."""

import uuid

from fastapi.testclient import TestClient
import pytest

pytestmark = pytest.mark.api


def tenant_headers(tenant_id: uuid.UUID) -> dict[str, str]:
    return {"X-Tenant-ID": str(tenant_id)}


def test_create_normalizes_identity_and_contact_data(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={
            "name": "Cliente Normalizado",
            "customer_type": "INDIVIDUAL",
            "document_number": "529.982.247-25",
            "email": "  CLIENTE@EXAMPLE.COM  ",
            "phone": "+55 (18) 99999-0000",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["document_number"] == "52998224725"
    assert body["email"] == "cliente@example.com"
    assert body["phone"] == "18999990000"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("document_number", "529.982.247-24"),
        ("email", "email-invalido"),
        ("phone", "9999-0000"),
    ],
)
def test_create_rejects_invalid_identity_data(
    client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
    value: str,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={"name": "Cliente Inválido", field: value},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "request.validation_error"


def test_create_rejects_document_incompatible_with_customer_type(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={
            "name": "Empresa Inválida",
            "customer_type": "CORPORATE",
            "document_number": "529.982.247-25",
        },
    )

    assert response.status_code == 422


def test_rejects_duplicate_document_in_same_tenant(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    payload = {
        "name": "Primeiro Cliente",
        "document_number": "529.982.247-25",
    }
    assert client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json=payload,
    ).status_code == 201

    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={
            "name": "Segundo Cliente",
            "document_number": "52998224725",
        },
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "customer.duplicate"
    assert response.json()["error"]["details"] == {"field": "document_number"}


def test_rejects_duplicate_email_case_insensitively(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    assert client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={"name": "Primeiro Cliente", "email": "cliente@example.com"},
    ).status_code == 201

    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={"name": "Segundo Cliente", "email": "CLIENTE@EXAMPLE.COM"},
    )

    assert response.status_code == 409
    assert response.json()["error"]["details"] == {"field": "email"}


def test_allows_same_identity_data_in_other_tenant(
    client: TestClient,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    payload = {
        "name": "Cliente",
        "document_number": "52998224725",
        "email": "cliente@example.com",
    }
    assert client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json=payload,
    ).status_code == 201

    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(other_tenant_id),
        json=payload,
    )

    assert response.status_code == 201


def test_update_rejects_identity_used_by_another_customer(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    first = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={
            "name": "Primeiro",
            "email": "primeiro@example.com",
        },
    ).json()
    second = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={
            "name": "Segundo",
            "email": "segundo@example.com",
        },
    ).json()

    response = client.patch(
        f"/api/v1/customers/{second['id']}",
        headers=tenant_headers(tenant_id),
        json={
            "row_version": second["row_version"],
            "email": first["email"],
        },
    )

    assert response.status_code == 409
    assert response.json()["error"]["details"] == {"field": "email"}


def test_update_keeps_own_identity_data(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = client.post(
        "/api/v1/customers",
        headers=tenant_headers(tenant_id),
        json={
            "name": "Cliente",
            "document_number": "52998224725",
            "email": "cliente@example.com",
        },
    ).json()

    response = client.patch(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(tenant_id),
        json={
            "row_version": created["row_version"],
            "name": "Cliente Atualizado",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Cliente Atualizado"
```

## 3. Arquivos existentes que devem ser substituídos integralmente

### `apps/api/src/organizeg3_api/domain/customer/entity.py`

```python
"""Customer domain entity and customer classification."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
import uuid

from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
    PhoneNumber,
    optional_document,
    optional_email,
    optional_phone,
)


class CustomerType(StrEnum):
    """Customer classification type."""

    INDIVIDUAL = "INDIVIDUAL"
    CORPORATE = "CORPORATE"


@dataclass
class Customer:
    """Pure domain entity representing a customer."""

    tenant_id: uuid.UUID
    code: str
    name: str
    customer_type: CustomerType
    id: int | None = None
    document_number: DocumentNumber | str | None = None
    email: EmailAddress | str | None = None
    phone: PhoneNumber | str | None = None
    is_active: bool = True
    row_version: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = None
    _allow_legacy_contacts: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        """Normalize primitive values and enforce current domain invariants."""

        raw_tenant_id: object = self.tenant_id
        if not isinstance(raw_tenant_id, uuid.UUID):
            raise TypeError("tenant_id deve ser um UUID válido.")
        if raw_tenant_id.int == 0:
            raise ValueError("tenant_id não pode ser o UUID nulo.")

        self.code = self.code.strip()
        self.name = self.name.strip()
        self.customer_type = self._coerce_customer_type(self.customer_type)
        if self._allow_legacy_contacts:
            self.document_number = self._normalize_legacy_document(self.document_number)
            self.email = self._normalize_legacy_email(self.email)
            self.phone = self._normalize_legacy_phone(self.phone)
        else:
            self.document_number = optional_document(self.document_number)
            self.email = optional_email(self.email)
            self.phone = optional_phone(self.phone)

        if not self.code:
            raise ValueError("O código do cliente é obrigatório.")
        if not self.name:
            raise ValueError("O nome do cliente é obrigatório.")
        if self.row_version < 1:
            raise ValueError("row_version deve ser maior ou igual a 1.")

        self._validate_document_compatibility()

    def update_profile(
        self,
        *,
        name: str,
        customer_type: CustomerType,
        document_number: DocumentNumber | str | None,
        email: EmailAddress | str | None,
        phone: PhoneNumber | str | None,
    ) -> None:
        """Update editable customer data while preserving domain invariants."""

        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("O nome do cliente é obrigatório.")

        previous_customer_type = self.customer_type
        self.name = normalized_name
        self.customer_type = self._coerce_customer_type(customer_type)

        document_changed = document_number != self.document_number
        email_changed = email != self.email
        phone_changed = phone != self.phone
        type_changed = self.customer_type is not previous_customer_type

        if document_changed or type_changed or not self._allow_legacy_contacts:
            self.document_number = optional_document(document_number)
        if email_changed or not self._allow_legacy_contacts:
            self.email = optional_email(email)
        if phone_changed or not self._allow_legacy_contacts:
            self.phone = optional_phone(phone)

        self._validate_document_compatibility()
        self._touch()

    def activate(self) -> None:
        """Activate the customer without changing archival state."""

        self.is_active = True
        self._touch()

    def deactivate(self) -> None:
        """Deactivate the customer without archiving it."""

        self.is_active = False
        self._touch()

    def archive(self) -> None:
        """Archive the customer using logical deletion."""

        if self.deleted_at is not None:
            raise ValueError("O cliente já está arquivado.")

        now = datetime.now(UTC)
        self.deleted_at = now
        self.updated_at = now
        self.is_active = False

    def reactivate(self) -> None:
        """Restore an archived customer and make it active again."""

        if self.deleted_at is None:
            raise ValueError("O cliente não está arquivado.")

        self.deleted_at = None
        self.is_active = True
        self._touch()

    def mark_as_deleted(self) -> None:
        """Compatibility alias for the archival operation."""

        self.archive()

    def _validate_document_compatibility(self) -> None:
        if self.document_number is None or not isinstance(self.document_number, DocumentNumber):
            return
        if self.customer_type is CustomerType.INDIVIDUAL and not self.document_number.is_cpf:
            raise ValueError("Cliente pessoa física deve utilizar CPF.")
        if self.customer_type is CustomerType.CORPORATE and not self.document_number.is_cnpj:
            raise ValueError("Cliente pessoa jurídica deve utilizar CNPJ.")

    @staticmethod
    def _normalize_legacy_document(
        value: DocumentNumber | str | None,
    ) -> DocumentNumber | str | None:
        if value is None or not str(value).strip():
            return None
        try:
            return optional_document(value)
        except (TypeError, ValueError):
            return str(value).strip()

    @staticmethod
    def _normalize_legacy_email(
        value: EmailAddress | str | None,
    ) -> EmailAddress | str | None:
        if value is None or not str(value).strip():
            return None
        try:
            return optional_email(value)
        except (TypeError, ValueError):
            return str(value).strip().lower()

    @staticmethod
    def _normalize_legacy_phone(
        value: PhoneNumber | str | None,
    ) -> PhoneNumber | str | None:
        if value is None or not str(value).strip():
            return None
        try:
            return optional_phone(value)
        except (TypeError, ValueError):
            return str(value).strip()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)

    @staticmethod
    def _coerce_customer_type(value: object) -> CustomerType:
        if isinstance(value, CustomerType):
            return value
        if not isinstance(value, str):
            raise TypeError("O tipo de cliente deve ser informado como texto.")

        try:
            return CustomerType(value)
        except ValueError as exception:
            raise ValueError("O tipo de cliente é inválido.") from exception
```

### `apps/api/src/organizeg3_api/domain/customer/repository.py`

```python
"""Repository contract for customer persistence operations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
import uuid

from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.domain.customer.value_objects import DocumentNumber, EmailAddress


class ICustomerRepository(ABC):
    """Port interface for customer persistence operations."""

    @abstractmethod
    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        """Fetch one customer within a tenant scope."""

    @abstractmethod
    def list_all(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        customer_type: CustomerType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Customer]:
        """List and search non-archived customers within a tenant scope."""

    @abstractmethod
    def save(
        self,
        customer: Customer,
        *,
        include_archived: bool = False,
    ) -> Customer:
        """Persist or update a customer domain entity."""

    def exists_by_document(
        self,
        tenant_id: uuid.UUID,
        document_number: DocumentNumber,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        """Return whether a document is already reserved in the tenant."""

        del tenant_id, document_number, exclude_customer_id
        return False

    def exists_by_email(
        self,
        tenant_id: uuid.UUID,
        email: EmailAddress,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        """Return whether an email is already reserved in the tenant."""

        del tenant_id, email, exclude_customer_id
        return False
```

### `apps/api/src/organizeg3_api/application/customer/schemas.py`

```python
"""Customer DTOs used by the application and HTTP layers."""

from __future__ import annotations

from typing import Self
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from organizeg3_api.domain.customer.entity import CustomerType
from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
    PhoneNumber,
    optional_document,
    optional_email,
    optional_phone,
)


class CustomerContactFields(BaseModel):
    """Shared normalized identity and contact fields."""

    document_number: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)

    @field_validator("document_number", mode="before")
    @classmethod
    def validate_document_number(cls, value: object) -> str | None:
        if value is None or not str(value).strip():
            return None
        return str(DocumentNumber(str(value)))

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value: object) -> str | None:
        if value is None or not str(value).strip():
            return None
        return str(EmailAddress(str(value)))

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone(cls, value: object) -> str | None:
        if value is None or not str(value).strip():
            return None
        return str(PhoneNumber(str(value)))


class CustomerCreate(CustomerContactFields):
    """Payload accepted when creating a customer."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=255)
    customer_type: CustomerType = CustomerType.INDIVIDUAL

    @model_validator(mode="after")
    def validate_document_type(self) -> Self:
        document = optional_document(self.document_number)
        if document is None:
            return self
        if self.customer_type is CustomerType.INDIVIDUAL and not document.is_cpf:
            raise ValueError("Cliente pessoa física deve utilizar CPF.")
        if self.customer_type is CustomerType.CORPORATE and not document.is_cnpj:
            raise ValueError("Cliente pessoa jurídica deve utilizar CNPJ.")
        return self


class CustomerUpdate(CustomerContactFields):
    """Partial update payload protected by optimistic concurrency."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    row_version: int = Field(ge=1)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    customer_type: CustomerType | None = None

    @model_validator(mode="after")
    def validate_submitted_document_type(self) -> Self:
        submitted_fields = self.model_fields_set
        if (
            "document_number" not in submitted_fields
            or "customer_type" not in submitted_fields
        ):
            return self
        if self.document_number is None or self.customer_type is None:
            return self

        document = DocumentNumber(self.document_number)
        if self.customer_type is CustomerType.INDIVIDUAL and not document.is_cpf:
            raise ValueError("Cliente pessoa física deve utilizar CPF.")
        if self.customer_type is CustomerType.CORPORATE and not document.is_cnpj:
            raise ValueError("Cliente pessoa jurídica deve utilizar CNPJ.")
        return self


class CustomerVersionCommand(BaseModel):
    """Command payload containing the expected optimistic version."""

    model_config = ConfigDict(extra="forbid")

    row_version: int = Field(ge=1)


class CustomerResponse(BaseModel):
    """Response payload for a customer."""

    model_config = ConfigDict(from_attributes=True)

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
```

### `apps/api/src/organizeg3_api/application/customer/use_cases/create_customer.py`

```python
"""Create-customer use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.customer.duplication_policy import CustomerDuplicationPolicy
from organizeg3_api.application.customer.schemas import CustomerCreate
from organizeg3_api.core.exceptions import ValidationError
from organizeg3_api.domain.customer.entity import Customer
from organizeg3_api.domain.customer.repository import ICustomerRepository
from organizeg3_api.domain.customer.value_objects import DocumentNumber, EmailAddress


class CreateCustomerUseCase:
    """Create and persist a customer for the authenticated tenant."""

    def __init__(self, repository: ICustomerRepository) -> None:
        self._repository = repository
        self._duplication_policy = CustomerDuplicationPolicy(repository)

    def execute(self, tenant_id: uuid.UUID, payload: CustomerCreate) -> Customer:
        """Execute customer creation using the tenant context, never the payload."""

        unique_code = f"CUST-{uuid.uuid4().hex[:8].upper()}"
        try:
            customer = Customer(
                tenant_id=tenant_id,
                code=unique_code,
                name=payload.name,
                customer_type=payload.customer_type,
                document_number=payload.document_number,
                email=payload.email,
                phone=payload.phone,
            )
        except (TypeError, ValueError) as exception:
            raise ValidationError(str(exception)) from exception

        self._duplication_policy.ensure_available(
            tenant_id,
            document_number=(
                customer.document_number
                if isinstance(customer.document_number, DocumentNumber)
                else None
            ),
            email=customer.email if isinstance(customer.email, EmailAddress) else None,
        )
        return self._repository.save(customer)
```

### `apps/api/src/organizeg3_api/application/customer/use_cases/update_customer.py`

```python
"""Update-customer use case."""

from __future__ import annotations

from dataclasses import replace
import uuid

from organizeg3_api.application.customer.concurrency import ensure_customer_version
from organizeg3_api.application.customer.duplication_policy import CustomerDuplicationPolicy
from organizeg3_api.application.customer.schemas import CustomerUpdate
from organizeg3_api.core.exceptions import NotFoundError, ValidationError
from organizeg3_api.domain.customer.entity import Customer
from organizeg3_api.domain.customer.repository import ICustomerRepository
from organizeg3_api.domain.customer.value_objects import DocumentNumber, EmailAddress


class UpdateCustomerUseCase:
    """Update editable customer data within the authenticated tenant."""

    def __init__(self, repository: ICustomerRepository) -> None:
        self._repository = repository
        self._duplication_policy = CustomerDuplicationPolicy(repository)

    def execute(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        payload: CustomerUpdate,
    ) -> Customer:
        """Apply a tenant-scoped partial update with version validation."""

        customer = self._repository.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise NotFoundError("Cliente não encontrado.")

        ensure_customer_version(customer, payload.row_version)
        changed_fields = payload.model_fields_set - {"row_version"}
        if not changed_fields:
            raise ValidationError("Informe ao menos um campo para atualizar.")

        updated_name = customer.name
        if "name" in changed_fields:
            if payload.name is None:
                raise ValidationError("O nome do cliente não pode ser nulo.")
            updated_name = payload.name

        updated_customer_type = customer.customer_type
        if "customer_type" in changed_fields:
            if payload.customer_type is None:
                raise ValidationError("O tipo de cliente não pode ser nulo.")
            updated_customer_type = payload.customer_type

        candidate = replace(customer)
        try:
            candidate.update_profile(
                name=updated_name,
                customer_type=updated_customer_type,
                document_number=(
                    payload.document_number
                    if "document_number" in changed_fields
                    else customer.document_number
                ),
                email=payload.email if "email" in changed_fields else customer.email,
                phone=payload.phone if "phone" in changed_fields else customer.phone,
            )
        except (TypeError, ValueError) as exception:
            raise ValidationError(str(exception)) from exception

        self._duplication_policy.ensure_available(
            tenant_id,
            document_number=(
                candidate.document_number
                if isinstance(candidate.document_number, DocumentNumber)
                else None
            ),
            email=candidate.email if isinstance(candidate.email, EmailAddress) else None,
            exclude_customer_id=customer_id,
        )
        return self._repository.save(candidate)
```

### `apps/api/src/organizeg3_api/core/exceptions.py`

```python
"""Application exceptions exposed through the Platform API."""

from __future__ import annotations

from typing import Any


class OrganizeG3Error(Exception):
    """Base exception for controlled OrganizeG3 errors."""

    error_code = "organizeg3.error"
    status_code = 500

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.details = details or {}


class ValidationError(OrganizeG3Error):
    """Raised when submitted data violates an application rule."""

    error_code = "validation.error"
    status_code = 422


class NotFoundError(OrganizeG3Error):
    """Raised when an authorized resource cannot be found."""

    error_code = "resource.not_found"
    status_code = 404


class ConflictError(OrganizeG3Error):
    """Raised when an operation conflicts with current state."""

    error_code = "resource.conflict"
    status_code = 409


class DuplicateCustomerError(ConflictError):
    """Raised when customer identity data is already used in a tenant."""

    error_code = "customer.duplicate"


class PermissionDeniedError(OrganizeG3Error):
    """Raised when the authenticated actor lacks permission."""

    error_code = "authorization.permission_denied"
    status_code = 403


class AuthenticationError(OrganizeG3Error):
    """Raised when authentication is missing or invalid."""

    error_code = "authentication.invalid"
    status_code = 401


class InvalidTransitionError(ConflictError):
    """Raised when a workflow transition is not allowed."""

    error_code = "workflow.invalid_transition"


class ConcurrencyError(ConflictError):
    """Raised when optimistic concurrency validation fails."""

    error_code = "concurrency.conflict"


class IdempotencyConflictError(ConflictError):
    """Raised when an idempotency key is reused incompatibly."""

    error_code = "idempotency.conflict"


class ConfigurationError(OrganizeG3Error):
    """Raised when the application configuration is invalid."""

    error_code = "configuration.error"
    status_code = 500
```

### `apps/api/src/organizeg3_api/infrastructure/persistence/repositories/customer_repository.py`

```python
"""Synchronous SQLAlchemy implementation of the customer repository."""

from __future__ import annotations

from collections.abc import Sequence
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from organizeg3_api.core.exceptions import ConcurrencyError, NotFoundError
from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.domain.customer.repository import ICustomerRepository
from organizeg3_api.domain.customer.value_objects import DocumentNumber, EmailAddress
from organizeg3_api.infrastructure.persistence.models.customer import CustomerModel


class SQLAlchemyCustomerRepository(ICustomerRepository):
    """SQLAlchemy adapter enforcing tenant isolation on every operation."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        statement = select(CustomerModel).where(
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.id == customer_id,
        )

        if not include_archived:
            statement = statement.where(CustomerModel.deleted_at.is_(None))

        model = self._session.execute(statement).scalar_one_or_none()
        return self._to_domain(model) if model is not None else None

    def list_all(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        customer_type: CustomerType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Customer]:
        statement = select(CustomerModel).where(
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.deleted_at.is_(None),
        )

        if not include_inactive:
            statement = statement.where(CustomerModel.is_active.is_(True))

        if customer_type is not None:
            statement = statement.where(CustomerModel.customer_type == customer_type.value)

        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    CustomerModel.code.ilike(pattern),
                    CustomerModel.name.ilike(pattern),
                    CustomerModel.document_number.ilike(pattern),
                    CustomerModel.email.ilike(pattern),
                    CustomerModel.phone.ilike(pattern),
                )
            )

        statement = (
            statement.order_by(CustomerModel.name, CustomerModel.id)
            .offset(offset)
            .limit(limit)
        )
        models = self._session.execute(statement).scalars().all()
        return [self._to_domain(model) for model in models]

    def exists_by_document(
        self,
        tenant_id: uuid.UUID,
        document_number: DocumentNumber,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        normalized_column = func.replace(
            func.replace(
                func.replace(CustomerModel.document_number, ".", ""),
                "-",
                "",
            ),
            "/",
            "",
        )
        statement = select(CustomerModel.id).where(
            CustomerModel.tenant_id == tenant_id,
            normalized_column == str(document_number),
        )
        if exclude_customer_id is not None:
            statement = statement.where(CustomerModel.id != exclude_customer_id)
        return self._session.execute(statement.limit(1)).scalar_one_or_none() is not None

    def exists_by_email(
        self,
        tenant_id: uuid.UUID,
        email: EmailAddress,
        *,
        exclude_customer_id: int | None = None,
    ) -> bool:
        statement = select(CustomerModel.id).where(
            CustomerModel.tenant_id == tenant_id,
            func.lower(func.trim(CustomerModel.email)) == str(email),
        )
        if exclude_customer_id is not None:
            statement = statement.where(CustomerModel.id != exclude_customer_id)
        return self._session.execute(statement.limit(1)).scalar_one_or_none() is not None

    def save(
        self,
        customer: Customer,
        *,
        include_archived: bool = False,
    ) -> Customer:
        if customer.id is None:
            model = CustomerModel(
                tenant_id=customer.tenant_id,
                code=customer.code,
                name=customer.name,
                customer_type=customer.customer_type.value,
                document_number=customer.document_number,
                email=customer.email,
                phone=customer.phone,
                is_active=customer.is_active,
                row_version=customer.row_version,
                deleted_at=customer.deleted_at,
            )
            self._session.add(model)
        else:
            statement = select(CustomerModel).where(
                CustomerModel.id == customer.id,
                CustomerModel.tenant_id == customer.tenant_id,
            )

            if not include_archived:
                statement = statement.where(CustomerModel.deleted_at.is_(None))

            existing_model = self._session.execute(statement).scalar_one_or_none()
            if existing_model is None:
                raise NotFoundError("Cliente não encontrado para a empresa informada.")

            model = existing_model
            if model.row_version != customer.row_version:
                raise ConcurrencyError(
                    "O cliente foi alterado por outro processo.",
                    details={
                        "expected_version": customer.row_version,
                        "current_version": model.row_version,
                    },
                )

            model.name = customer.name
            model.code = customer.code
            model.customer_type = customer.customer_type.value
            model.document_number = customer.document_number
            model.email = customer.email
            model.phone = customer.phone
            model.is_active = customer.is_active
            model.deleted_at = customer.deleted_at

        try:
            self._session.flush()
        except StaleDataError as exception:
            raise ConcurrencyError(
                "O cliente foi alterado por outro processo durante a gravação."
            ) from exception

        self._session.refresh(model)
        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: CustomerModel) -> Customer:
        return Customer(
            id=model.id,
            tenant_id=model.tenant_id,
            code=model.code,
            name=model.name,
            customer_type=CustomerType(model.customer_type),
            document_number=model.document_number,
            email=model.email,
            phone=model.phone,
            is_active=model.is_active,
            row_version=model.row_version,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
            _allow_legacy_contacts=True,
        )
```

### `apps/api/src/organizeg3_api/middleware/error_handler.py`

```python
"""Global exception handlers for the OrganizeG3 Platform API."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from organizeg3_api.core.exceptions import OrganizeG3Error
from organizeg3_api.core.logging import get_logger

logger = get_logger(__name__)


def get_correlation_id(request: Request) -> str | None:
    """Return the current request correlation identifier."""

    return getattr(request.state, "correlation_id", None)


def build_error_response(
    *,
    request: Request,
    status_code: int,
    error_code: str,
    message: str,
    details: Any = None,  # noqa: ANN401
) -> JSONResponse:
    """Build the standard API error response."""

    correlation_id = get_correlation_id(request)

    content: dict[str, Any] = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "details": details,
        },
        "meta": {
            "correlation_id": correlation_id,
        },
    }

    return JSONResponse(
        status_code=status_code,
        content=content,
    )


def sanitize_validation_errors(
    errors: list[dict[str, Any]] | tuple[dict[str, Any], ...],
) -> list[dict[str, Any]]:
    """Convert non-JSON validation context values into safe strings."""

    sanitized: list[dict[str, Any]] = []
    for error in errors:
        item = dict(error)
        context = item.get("ctx")
        if isinstance(context, dict):
            item["ctx"] = {
                key: str(value) if isinstance(value, BaseException) else value
                for key, value in context.items()
            }
        sanitized.append(item)
    return sanitized


def register_exception_handlers(application: FastAPI) -> None:
    """Register the global exception handlers."""

    @application.exception_handler(OrganizeG3Error)
    async def handle_organizeg3_error(
        request: Request,
        exception: OrganizeG3Error,
    ) -> JSONResponse:
        logger.warning(
            "controlled_application_error",
            error_code=exception.error_code,
            error_message=exception.message,
            path=request.url.path,
            method=request.method,
        )

        return build_error_response(
            request=request,
            status_code=exception.status_code,
            error_code=exception.error_code,
            message=exception.message,
            details=exception.details or None,
        )

    @application.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        validation_errors = sanitize_validation_errors(list(exception.errors()))

        logger.warning(
            "request_validation_failed",
            path=request.url.path,
            method=request.method,
            validation_errors=validation_errors,
        )

        return build_error_response(
            request=request,
            status_code=422,
            error_code="request.validation_error",
            message="Os dados enviados são inválidos.",
            details=validation_errors,
        )

    @application.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        request: Request,
        exception: StarletteHTTPException,
    ) -> JSONResponse:
        message = (
            exception.detail
            if isinstance(exception.detail, str)
            else "A requisição não pôde ser processada."
        )

        return build_error_response(
            request=request,
            status_code=exception.status_code,
            error_code=f"http.{exception.status_code}",
            message=message,
        )

    @application.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request,
        exception: Exception,
    ) -> JSONResponse:
        logger.error(
            "unexpected_application_error",
            path=request.url.path,
            method=request.method,
            exception_type=type(exception).__name__,
            exc_info=exception,
        )

        return build_error_response(
            request=request,
            status_code=500,
            error_code="internal_server_error",
            message="Ocorreu um erro interno inesperado.",
        )
```

### `apps/api/tests/unit/domain/test_customer_mutations.py`

```python
"""Unit tests for customer profile changes and lifecycle transitions."""

import uuid

import pytest

from organizeg3_api.domain.customer.entity import Customer, CustomerType

pytestmark = pytest.mark.unit


def make_customer(**changes: object) -> Customer:
    values: dict[str, object] = {
        "tenant_id": uuid.uuid4(),
        "code": "CUST-0001",
        "name": "Cliente Teste",
        "customer_type": CustomerType.INDIVIDUAL,
    }
    values.update(changes)
    return Customer(**values)  # type: ignore[arg-type]


def test_update_profile_normalizes_and_clears_optional_values() -> None:
    customer = make_customer(
        document_number="529.982.247-25",
        email="old@example.com",
        phone="18999990000",
    )
    previous_timestamp = customer.updated_at

    customer.update_profile(
        name="  Empresa Atualizada  ",
        customer_type=CustomerType.CORPORATE,
        document_number="11.222.333/0001-81",
        email="   ",
        phone=None,
    )

    assert customer.name == "Empresa Atualizada"
    assert customer.customer_type is CustomerType.CORPORATE
    assert customer.document_number == "11222333000181"
    assert customer.email is None
    assert customer.phone is None
    assert customer.updated_at >= previous_timestamp


def test_archive_rejects_second_archival() -> None:
    customer = make_customer()
    customer.archive()

    with pytest.raises(ValueError, match="já está arquivado"):
        customer.archive()


def test_reactivate_restores_archived_customer() -> None:
    customer = make_customer()
    customer.archive()
    archived_at = customer.deleted_at

    customer.reactivate()

    assert archived_at is not None
    assert customer.deleted_at is None
    assert customer.is_active is True
    assert customer.updated_at >= archived_at


def test_reactivate_rejects_customer_that_is_not_archived() -> None:
    customer = make_customer()

    with pytest.raises(ValueError, match="não está arquivado"):
        customer.reactivate()
```

### `apps/api/tests/integration/persistence/test_customer_repository.py`

```python
"""Integration tests for SQLAlchemy customer persistence."""

from datetime import UTC, datetime
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.core.exceptions import ConcurrencyError, NotFoundError
from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.infrastructure.persistence.models.customer import CustomerModel
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)

pytestmark = [pytest.mark.integration, pytest.mark.database]


def make_customer(tenant_id: uuid.UUID, **changes: object) -> Customer:
    values: dict[str, object] = {
        "tenant_id": tenant_id,
        "code": f"CUST-{uuid.uuid4().hex[:8].upper()}",
        "name": "Cliente Teste",
        "customer_type": CustomerType.INDIVIDUAL,
    }
    values.update(changes)
    return Customer(**values)  # type: ignore[arg-type]


def test_creates_and_recovers_customer(session: Session, tenant_id: uuid.UUID) -> None:
    repository = SQLAlchemyCustomerRepository(session)

    saved = repository.save(make_customer(tenant_id, email="cliente@example.com"))
    recovered = repository.get_by_id(tenant_id, saved.id or 0)

    assert saved.id is not None
    assert recovered is not None
    assert recovered.id == saved.id
    assert recovered.tenant_id == tenant_id
    assert recovered.email == "cliente@example.com"


def test_does_not_recover_customer_from_other_tenant(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    saved = repository.save(make_customer(tenant_id))

    assert repository.get_by_id(other_tenant_id, saved.id or 0) is None


def test_lists_only_current_tenant(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    repository.save(make_customer(tenant_id, name="Cliente A"))
    repository.save(make_customer(other_tenant_id, name="Cliente B"))

    result = repository.list_all(tenant_id)

    assert [customer.name for customer in result] == ["Cliente A"]


def test_excludes_inactive_by_default_and_can_include_them(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    repository.save(make_customer(tenant_id, name="Ativo"))
    repository.save(make_customer(tenant_id, name="Inativo", is_active=False))

    active_only = repository.list_all(tenant_id)
    all_customers = repository.list_all(tenant_id, include_inactive=True)

    assert [customer.name for customer in active_only] == ["Ativo"]
    assert [customer.name for customer in all_customers] == ["Ativo", "Inativo"]


def test_excludes_soft_deleted_customer(session: Session, tenant_id: uuid.UUID) -> None:
    session.add(
        CustomerModel(
            tenant_id=tenant_id,
            code="CUST-DELETED",
            name="Excluído",
            customer_type="INDIVIDUAL",
            is_active=False,
            deleted_at=datetime.now(UTC),
        )
    )
    session.flush()
    repository = SQLAlchemyCustomerRepository(session)

    assert repository.list_all(tenant_id, include_inactive=True) == []


def test_rejects_cross_tenant_update(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    saved = repository.save(make_customer(tenant_id))
    forged = make_customer(
        other_tenant_id,
        id=saved.id,
        code=saved.code,
        row_version=saved.row_version,
    )

    with pytest.raises(NotFoundError):
        repository.save(forged)


def test_increments_optimistic_version_on_update(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    saved = repository.save(make_customer(tenant_id))
    saved.name = "Cliente Atualizado"

    updated = repository.save(saved)

    assert updated.name == "Cliente Atualizado"
    assert updated.row_version == 2


def test_rejects_stale_optimistic_version(session: Session, tenant_id: uuid.UUID) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    saved = repository.save(make_customer(tenant_id))
    stale_version = saved.row_version
    saved.name = "Primeira alteração"
    repository.save(saved)

    stale = make_customer(
        tenant_id,
        id=saved.id,
        code=saved.code,
        name="Alteração antiga",
        row_version=stale_version,
    )
    with pytest.raises(ConcurrencyError):
        repository.save(stale)


def test_searches_by_name_code_document_email_and_phone(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    repository.save(
        make_customer(
            tenant_id,
            code="CLI-METAL",
            name="Metalúrgica Horizonte",
            document_number="11222333000181",
            email="vendas@horizonte.test",
            phone="18999990000",
            customer_type=CustomerType.CORPORATE,
        )
    )
    repository.save(make_customer(tenant_id, name="Cliente Residencial"))

    assert [item.name for item in repository.list_all(tenant_id, search="metal")] == [
        "Metalúrgica Horizonte"
    ]
    assert [item.name for item in repository.list_all(tenant_id, search="11222333")] == [
        "Metalúrgica Horizonte"
    ]
    assert [item.name for item in repository.list_all(tenant_id, search="horizonte.test")] == [
        "Metalúrgica Horizonte"
    ]
    assert [item.name for item in repository.list_all(tenant_id, search="99999")] == [
        "Metalúrgica Horizonte"
    ]


def test_filters_customer_type_and_applies_pagination(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCustomerRepository(session)
    repository.save(
        make_customer(
            tenant_id,
            name="Empresa A",
            customer_type=CustomerType.CORPORATE,
        )
    )
    repository.save(
        make_customer(
            tenant_id,
            name="Empresa B",
            customer_type=CustomerType.CORPORATE,
        )
    )
    repository.save(make_customer(tenant_id, name="Pessoa C"))

    result = repository.list_all(
        tenant_id,
        customer_type=CustomerType.CORPORATE,
        limit=1,
        offset=1,
    )

    assert [customer.name for customer in result] == ["Empresa B"]
```

## 4. Formatar e validar

Execute:

```powershell
$env:TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

python -m ruff check . --fix
python -m ruff check .
python -m mypy apps/api/src
python -m pytest -v
python -m pytest --cov=apps/api/src --cov-report=term-missing
python -m alembic current
python -m alembic heads
```

Resultado esperado:

```text
All checks passed!
Success: no issues found
113 passed
0439fdabfa05 (head)
```

## 5. Regras implementadas

- CPF é permitido somente para `INDIVIDUAL`.
- CNPJ é permitido somente para `CORPORATE`.
- E-mail é salvo em letras minúsculas.
- Telefone é salvo somente com DDD e dígitos nacionais.
- Prefixo internacional `+55` é aceito e removido na normalização.
- CPF/CNPJ e e-mail são exclusivos por tenant.
- O mesmo CPF/CNPJ ou e-mail pode existir em tenants diferentes.
- Clientes arquivados continuam reservando CPF/CNPJ e e-mail.
- O próprio cliente é excluído da verificação durante edição.
- Telefone não é único porque pode ser compartilhado.

## 6. Limite deliberado desta etapa

A verificação de duplicidade está na camada de aplicação e no repositório. Ainda não existe índice único no PostgreSQL, porque a criação segura desse índice exige primeiro uma auditoria para identificar duplicidades e formatos antigos na tabela legada `clientes`.
