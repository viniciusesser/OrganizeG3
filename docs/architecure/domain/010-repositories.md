# Domain Model Specification
## 010 - Repositories

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos Repositories do OrganizeG3.

Repositories são responsáveis por abstrair completamente a persistência dos Aggregates.

O Domínio nunca conhecerá:

- SQLAlchemy
- PostgreSQL
- SQLite
- Supabase
- Redis
- MongoDB
- API
- Arquivos

O Domínio conhecerá apenas Interfaces de Repository.

---

# O que é um Repository?

Um Repository representa uma coleção de Aggregates.

Sua responsabilidade é fornecer acesso aos objetos do domínio.

Ele funciona como uma coleção em memória, independentemente da tecnologia utilizada.

---

# Objetivos

Os Repositories existem para:

- isolar infraestrutura;
- simplificar a Application Layer;
- encapsular persistência;
- facilitar testes;
- permitir troca de banco de dados.

---

# Responsabilidades

Um Repository poderá:

- carregar Aggregates;
- salvar Aggregates;
- remover Aggregates;
- consultar Aggregates;
- verificar existência.

Nunca deverá:

- executar regra de negócio;
- validar domínio;
- calcular impostos;
- aplicar descontos;
- publicar eventos.

---

# Repository Interface

Cada Aggregate Root deverá possuir exatamente um Repository.

Exemplos

```text
CustomerRepository

SupplierRepository

ProductRepository

SalesOrderRepository

PurchaseOrderRepository

ProductionOrderRepository

InvoiceRepository

ProjectRepository

WorkflowRepository
```

Nunca criar Repository para Entities internas.

---

# Aggregate Root

Somente Aggregate Roots poderão possuir Repository.

Correto

```text
SalesOrderRepository
```

Errado

```text
SalesOrderItemRepository
```

SalesOrderItem pertence ao Aggregate.

---

# Operações Básicas

Todo Repository deverá fornecer:

```text
Add()

Update()

Delete()

GetById()

Exists()

NextIdentity()
```

Quando aplicável

```text
Find()

Search()

Count()
```

---

# GetById

Retorna exatamente um Aggregate.

Entrada

```text
AggregateId
```

Saída

```text
Aggregate
```

Caso não exista

```text
None

ou

AggregateNotFoundException
```

---

# Exists

Responsável por verificar existência.

Entrada

```text
AggregateId
```

Saída

```text
Boolean
```

---

# Add

Adiciona um novo Aggregate.

Nunca deverá validar regras de domínio.

O Aggregate já deverá estar consistente.

---

# Update

Persiste alterações.

Nunca modifica regras.

Apenas persiste.

---

# Delete

Quando aplicável.

Preferencialmente utilizar:

```text
Soft Delete
```

---

# Search

Consultas complexas pertencem ao lado de leitura (CQRS).

Repository deverá fornecer apenas consultas necessárias ao domínio.

Exemplo

```text
FindByEmail()

FindByDocument()

FindByCode()
```

Evitar

```text
FindEverything()
```

---

# CQRS

Write Model

↓

Repositories

Read Model

↓

Queries

↓

Read Database

Repositories pertencem ao lado de escrita.

---

# Persistência

A implementação poderá utilizar

```text
SQLAlchemy

PostgreSQL

SQLite

Supabase

Future Database
```

Sem alterar o domínio.

---

# Unit of Work

Repositories deverão trabalhar em conjunto com Unit Of Work.

Fluxo

```text
Application

↓

Repository

↓

Unit Of Work

↓

Commit
```

Nunca executar commit internamente.

---

# Interfaces

As interfaces pertencem ao Domain.

As implementações pertencem à Infrastructure.

Exemplo

```text
Domain

↓

ICustomerRepository
```

Infrastructure

↓

```text
SqlAlchemyCustomerRepository
```

---

# Métodos Permitidos

Exemplo

```text
GetById()

FindByEmail()

FindByDocument()

FindBySku()

Exists()

Add()

Update()

Delete()
```

---

# Métodos Proibidos

```text
ExecuteSQL()

RunQuery()

OpenConnection()

Commit()

Rollback()

Close()

ExecuteProcedure()
```

Esses pertencem à infraestrutura.

---

# Consultas

Repositories deverão retornar:

```text
Aggregates

Entities internas

Value Objects

Collections
```

Nunca retornar

```text
DTO

JSON

DataFrame

Response HTTP
```

---

# Paginação

Paginação pertence às Queries.

Não ao domínio.

---

# Ordenação

Ordenações complexas pertencem às Queries.

Não aos Repositories.

---

# Cache

Repositories não conhecerão cache.

Caso exista cache:

Infrastructure.

---

# Transações

Repositories nunca iniciarão transações.

A responsabilidade pertence ao Unit Of Work.

---

# Assincronismo

A interface não deverá depender de tecnologia.

A implementação poderá ser:

```text
Sync

Async
```

Sem alterar o domínio.

---

# Testabilidade

Repositories poderão ser substituídos por:

```text
Fake Repository

Memory Repository

Mock Repository
```

Facilitando testes.

---

# Repositories previstos

## Identity

```text
TenantRepository

BranchRepository

UserRepository

RoleRepository

PermissionRepository
```

---

## CRM

```text
CustomerRepository

LeadRepository

OpportunityRepository
```

---

## Comercial

```text
QuotationRepository

SalesOrderRepository

SalesContractRepository
```

---

## Compras

```text
SupplierRepository

PurchaseOrderRepository

PurchaseReceiptRepository
```

---

## Estoque

```text
ProductRepository

InventoryRepository

WarehouseRepository

LotRepository
```

---

## Produção

```text
ProductionOrderRepository

BillOfMaterialsRepository

ProductionRouteRepository
```

---

## Financeiro

```text
ReceivableRepository

PayableRepository

FinancialAccountRepository
```

---

## Fiscal

```text
FiscalDocumentRepository

TaxAssessmentRepository
```

---

## Projetos

```text
ProjectRepository

TaskRepository
```

---

## Workflow

```text
WorkflowRepository

WorkflowBoardRepository
```

---

## Documentos

```text
DocumentRepository
```

---

## IA

```text
PromptRepository

AgentRepository
```

---

## Sincronização

```text
SyncDeviceRepository

SnapshotRepository
```

---

# Convenções

Nome

```text
<Aggregate>Repository
```

Implementação

```text
SqlAlchemyCustomerRepository

SqlAlchemySalesOrderRepository

SqlAlchemyInvoiceRepository
```

Interfaces

```text
ICustomerRepository

ISalesOrderRepository

IInvoiceRepository
```

---

# Checklist

Antes de criar um Repository verificar:

- pertence a um Aggregate Root?
- não contém regra de negócio?
- não realiza commit?
- não conhece SQL diretamente?
- retorna Aggregates?
- pode ser implementado em memória?
- pode ser testado facilmente?

---

# Regras Gerais

Todo Repository deverá:

- representar uma coleção de Aggregates;
- abstrair completamente a persistência;
- não conter regras de negócio;
- trabalhar junto ao Unit Of Work;
- ser facilmente substituível;
- possuir interface no Domínio;
- possuir implementação na Infrastructure.

---

# Fluxo Arquitetural

```text
Presentation

↓

Application

↓

Command Handler

↓

Repository Interface

↓

Unit Of Work

↓

Infrastructure Repository

↓

Database
```

---

# Próximo Documento

```text
011-unit-of-work.md
```