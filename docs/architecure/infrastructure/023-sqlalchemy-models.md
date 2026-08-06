# Infrastructure Architecture Specification
## 023 - SQLAlchemy Models

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para implementação dos modelos SQLAlchemy do OrganizeG3.

Todos os Models da aplicação deverão seguir exatamente esta especificação.

Nenhum Model poderá ser criado fora deste padrão.

---

# Objetivos

Os Models deverão:

- representar tabelas do banco;
- ser compatíveis com SQLite e PostgreSQL;
- suportar sincronização;
- suportar auditoria;
- suportar versionamento;
- suportar multi-tenant;
- permanecer desacoplados do Domínio.

---

# Arquitetura

```text
Aggregate

↓

Repository

↓

SQLAlchemy Model

↓

Database
```

O Aggregate nunca conhecerá o Model.

O Model nunca conterá regra de negócio.

---

# Classe Base

Todos os Models deverão herdar de:

```text
BaseModel
```

Nunca diretamente de:

```python
DeclarativeBase
```

---

# Estrutura Base

Todo Model deverá possuir:

```text
UUIDMixin

TenantMixin

AuditMixin

VersionMixin

SoftDeleteMixin
```

Quando aplicável.

---

# UUIDMixin

Responsável por:

```text
id
```

Tipo

```text
UUID
```

Exemplo

```python
id: Mapped[UUID]
```

---

# TenantMixin

Responsável por:

```text
tenant_id
```

Quando necessário

```text
branch_id
```

---

# AuditMixin

Campos

```text
created_at

created_by_user_id

updated_at

updated_by_user_id
```

Sempre em UTC.

---

# VersionMixin

Campo

```text
version
```

Responsável por:

```text
Optimistic Lock

Sincronização

Auditoria
```

---

# SoftDeleteMixin

Campos

```text
is_deleted

deleted_at

deleted_by_user_id
```

---

# Nome das Classes

Sempre utilizar:

```text
PascalCase
```

Exemplos

```text
CustomerModel

SalesOrderModel

InvoiceModel

WarehouseModel
```

---

# Nome das Tabelas

Sempre utilizar:

```text
snake_case
```

Plural.

Exemplos

```text
customers

sales_orders

inventory_movements

production_orders
```

---

# Colunas

Sempre utilizar:

```text
snake_case
```

Nunca abreviações.

Correto

```text
customer_name

created_at

updated_at
```

Errado

```text
custName

dtCad

upd
```

---

# Tipos

UUID

↓

```text
UUID
```

Texto

↓

```text
String

Text
```

Datas

↓

```text
DateTime(timezone=True)
```

Valores

↓

```text
Numeric(18,4)
```

Booleanos

↓

```text
Boolean
```

---

# Relacionamentos

Utilizar:

```text
relationship()
```

Sempre explicitando:

```text
back_populates

lazy

cascade
```

---

# Lazy Loading

Padrão

```text
selectin
```

Evitar

```text
joined
```

Quando gerar grandes JOINs.

---

# Cascatas

Permitido

```text
save-update

merge
```

Evitar

```text
delete-orphan

all
```

Para entidades críticas.

---

# Foreign Keys

Sempre nomeadas.

Exemplo

```text
customer_id

↓

customers.id
```

---

# Constraints

Utilizar:

```text
Primary Key

Foreign Key

Unique

Check

Index
```

Nunca depender apenas da aplicação.

---

# Índices

Sempre criar índices para:

```text
tenant_id

created_at

updated_at

status
```

Quando aplicável.

---

# Campos Obrigatórios

Sempre utilizar:

```python
nullable=False
```

Quando o domínio exigir obrigatoriedade.

---

# Valores Padrão

Utilizar:

```python
default=
```

Ou

```python
server_default=
```

Conforme necessidade.

Nunca utilizar valores mágicos.

---

# Enumerações

Preferir:

```text
String
```

Validada pelo domínio.

Evitar ENUM do banco.

---

# JSON

Campos JSON poderão utilizar:

```text
JSON

JSONB
```

Quando realmente necessário.

Nunca substituir modelagem relacional.

---

# Herança

Evitar herança entre Models.

Preferir:

```text
Mixins
```

---

# Métodos

Models poderão possuir apenas:

```text
Representação

Conversões técnicas

Helpers internos
```

Nunca:

```text
Regra de negócio
```

---

# Eventos ORM

Permitido utilizar:

```text
before_insert

before_update

after_update
```

Apenas para infraestrutura.

Nunca executar lógica de domínio.

---

# Sessão

Models nunca abrirão sessões.

Nunca executar:

```python
session.commit()
```

Dentro do Model.

---

# Conversão

Conversão entre:

```text
Model

↓

Aggregate
```

Será responsabilidade dos Repositories.

---

# Segurança

Nunca armazenar:

```text
Senha em texto

JWT

Secrets

API Keys
```

Sem criptografia.

---

# Organização

Estrutura

```text
models/

    identity/

    crm/

    commercial/

    purchasing/

    inventory/

    production/

    financial/

    fiscal/

    projects/

    workflow/

    ai/

    synchronization/
```

---

# Convenções

Nome

```text
<Entity>Model
```

Exemplos

```text
CustomerModel

ProductModel

InvoiceModel

ProductionOrderModel
```

---

# Testabilidade

Todo Model deverá possuir testes para:

```text
Constraints

Relacionamentos

Defaults

Índices

Versionamento

Soft Delete

Auditoria
```

---

# Anti-Patterns

Nunca fazer

```text
Business Rules

Repository

SQL Manual

HTTP

API

Email

Logs

Eventos de Domínio
```

Dentro dos Models.

---

# Checklist

Antes de criar um Model verificar:

- herda BaseModel?
- possui UUID?
- possui auditoria?
- possui tenant?
- possui version?
- possui soft delete?
- possui índices?
- possui constraints?
- não possui regra de negócio?

---

# Regras Gerais

Todo SQLAlchemy Model deverá:

- representar apenas persistência;
- ser altamente consistente;
- ser compatível com SQLite e PostgreSQL;
- utilizar Mixins;
- não conter regras de domínio;
- ser facilmente testável;
- possuir tipagem completa.

---

# Fluxo Completo

```text
Aggregate

↓

Repository

↓

Mapper

↓

SQLAlchemy Model

↓

Session

↓

Database
```

---

# Próximo Documento

```text
024-repository-implementations.md
```