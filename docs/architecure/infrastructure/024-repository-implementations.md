# Infrastructure Architecture Specification
## 024 - Repository Implementations

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para implementação dos Repositories da camada Infrastructure do OrganizeG3.

Os Repositories concretos são responsáveis por implementar as interfaces definidas no Domínio utilizando SQLAlchemy.

Eles representam a única camada autorizada a conhecer:

- SQLAlchemy
- Sessões
- Models ORM
- Banco de Dados

O restante do sistema permanece desacoplado da persistência.

---

# Arquitetura

```text
Application

↓

Repository Interface

↓

SQLAlchemy Repository

↓

SQLAlchemy Session

↓

Database
```

---

# Objetivos

Os Repositories deverão:

- implementar interfaces do domínio;
- mapear Aggregates;
- persistir Models;
- executar consultas técnicas;
- respeitar o Unit Of Work;
- nunca conter regras de negócio.

---

# Responsabilidades

Um Repository concreto poderá:

- consultar banco;
- persistir Models;
- converter Models em Aggregates;
- converter Aggregates em Models;
- executar consultas técnicas;
- aplicar filtros técnicos.

Nunca deverá:

- executar regras de domínio;
- validar Commands;
- iniciar transações;
- executar Commit;
- publicar eventos.

---

# Implementações

Cada Interface possuirá exatamente uma implementação padrão.

Exemplo

```text
ICustomerRepository

↓

SqlAlchemyCustomerRepository
```

---

```text
ISalesOrderRepository

↓

SqlAlchemySalesOrderRepository
```

---

# Estrutura

```text
repositories/

    customer_repository.py

    supplier_repository.py

    product_repository.py

    inventory_repository.py

    sales_order_repository.py

    invoice_repository.py

    production_repository.py
```

---

# Dependências

Os Repositories poderão depender de:

```text
AsyncSession

SQLAlchemy Models

Mapper

Database Session

Infrastructure Helpers
```

Nunca depender de:

```text
Presentation

FastAPI

Qt

Widgets

Commands

Queries
```

---

# Sessão

Toda operação utilizará:

```python
AsyncSession
```

Recebida por Dependency Injection.

Nunca criar sessões internamente.

Errado

```python
session = AsyncSession(...)
```

Correto

```python
Repository(session)
```

---

# Unit Of Work

O Repository nunca executará:

```python
commit()

rollback()

close()
```

Toda transação pertence ao Unit Of Work.

---

# Conversão

Fluxo

```text
Aggregate

↓

Mapper

↓

SQLAlchemy Model

↓

Persistência
```

Retorno

```text
SQLAlchemy Model

↓

Mapper

↓

Aggregate
```

---

# Consultas

Os Repositories poderão executar:

```text
SELECT

INSERT

UPDATE

DELETE (Soft Delete)

EXISTS

COUNT
```

Nunca SQL manual quando o ORM oferecer solução equivalente.

---

# Soft Delete

Remoções deverão utilizar:

```text
is_deleted = true

deleted_at

deleted_by_user_id
```

Nunca excluir registros de negócio.

---

# Métodos Obrigatórios

Todo Repository deverá implementar:

```text
add()

update()

delete()

exists()

get_by_id()

next_identity()
```

Quando necessário

```text
find_by_code()

find_by_email()

find_by_document()

find_by_name()
```

---

# Métodos Proibidos

Nunca implementar:

```text
commit()

rollback()

open()

close()

execute_sql()

truncate()

vacuum()
```

---

# Consultas por Tenant

Toda consulta obrigatoriamente deverá possuir:

```text
tenant_id
```

Exemplo

```python
WHERE tenant_id = :tenant_id
```

Nenhum Repository poderá acessar dados de outro Tenant.

---

# Concorrência

Atualizações deverão utilizar:

```text
version
```

Caso a versão não corresponda:

```text
ConcurrencyException
```

---

# Lazy Loading

Preferir:

```text
selectinload()
```

Quando necessário.

Evitar consultas N+1.

---

# Eager Loading

Utilizar apenas quando:

- realmente necessário;
- reduzir consultas;
- houver ganho comprovado.

---

# Paginação

Paginação pertence às Queries.

Não aos Repositories do domínio.

---

# Cache

Repositories não conhecerão cache.

Caso exista cache:

```text
Application

↓

Read Model

↓

Cache
```

---

# Logging

Toda operação poderá registrar:

```text
Repository

Método

Duration

Rows

CorrelationId

TenantId
```

Sem registrar dados sensíveis.

---

# Performance

Prioridades

```text
Índices

Selectin

Batch

Bulk Operations

Projection
```

Evitar

```text
SELECT *

JOINs desnecessários

N+1

Loops com consultas
```

---

# Tratamento de Erros

Traduzir exceções técnicas para exceções da aplicação.

Exemplo

```text
IntegrityError

↓

DuplicateEntityException
```

---

```text
NoResultFound

↓

EntityNotFoundException
```

Nunca expor exceções do SQLAlchemy para o domínio.

---

# Organização por Contexto

```text
repositories/

    identity/

    crm/

    commercial/

    purchasing/

    inventory/

    production/

    financial/

    fiscal/

    workflow/

    ai/
```

---

# Repositories previstos

## Identity

```text
SqlAlchemyTenantRepository

SqlAlchemyUserRepository

SqlAlchemyRoleRepository
```

---

## CRM

```text
SqlAlchemyCustomerRepository

SqlAlchemyLeadRepository

SqlAlchemyOpportunityRepository
```

---

## Comercial

```text
SqlAlchemyQuotationRepository

SqlAlchemySalesOrderRepository
```

---

## Compras

```text
SqlAlchemyPurchaseOrderRepository

SqlAlchemySupplierRepository
```

---

## Estoque

```text
SqlAlchemyProductRepository

SqlAlchemyInventoryRepository

SqlAlchemyWarehouseRepository
```

---

## Produção

```text
SqlAlchemyProductionOrderRepository

SqlAlchemyBillOfMaterialsRepository
```

---

## Financeiro

```text
SqlAlchemyReceivableRepository

SqlAlchemyPayableRepository
```

---

## Fiscal

```text
SqlAlchemyInvoiceRepository
```

---

## Projetos

```text
SqlAlchemyProjectRepository

SqlAlchemyTaskRepository
```

---

# Dependency Injection

Todos os Repositories deverão ser registrados no Container.

Fluxo

```text
Interface

↓

Implementação

↓

Dependency Injection

↓

Application
```

---

# Testabilidade

Todo Repository deverá possuir:

```text
Unit Tests

Integration Tests

SQLite Tests

PostgreSQL Tests

Performance Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Business Rules

Commands

Queries

Commit

Rollback

UI

HTTP

Eventos de Domínio
```

Dentro dos Repositories.

---

# Checklist

Antes de implementar verificar:

- implementa Interface?
- utiliza AsyncSession?
- utiliza Mapper?
- respeita Tenant?
- respeita Version?
- não executa Commit?
- não possui regra de negócio?
- possui testes?

---

# Regras Gerais

Todo Repository deverá:

- implementar Interface do Domínio;
- utilizar SQLAlchemy;
- utilizar AsyncSession;
- respeitar Unit Of Work;
- respeitar Multi-Tenant;
- respeitar Soft Delete;
- respeitar Versionamento;
- nunca conter regras de negócio.

---

# Fluxo Completo

```text
Command Handler

↓

Repository Interface

↓

SqlAlchemy Repository

↓

Mapper

↓

SQLAlchemy Model

↓

Database
```

---

# Próximo Documento

```text
025-database-session.md
```