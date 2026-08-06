# Domain Model Specification
## 002 - Aggregate Design

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para construção de Aggregates dentro do OrganizeG3.

Todo Aggregate implementado no sistema deverá seguir exatamente estas diretrizes.

Nenhum Aggregate poderá violar as regras aqui estabelecidas.

---

# O que é um Aggregate?

Um Aggregate representa um conjunto de objetos de domínio que devem permanecer consistentes entre si.

O Aggregate é a menor unidade de consistência transacional do sistema.

Exemplo:

```text
Sales Order

┌──────────────────────────────┐
│ SalesOrder (Root)            │
├──────────────────────────────┤
│ SalesOrderItem               │
│ SalesOrderPayment            │
│ SalesOrderDiscount           │
│ SalesOrderAttachment         │
└──────────────────────────────┘
```

Toda alteração deve ocorrer através do Aggregate Root.

---

# Aggregate Root

Todo Aggregate possui exatamente um Aggregate Root.

Exemplos:

```text
Customer

Supplier

Product

SalesOrder

PurchaseOrder

ProductionOrder

Invoice

Project

Workflow

Document
```

Somente o Root poderá ser acessado por outros Contextos.

Nunca acessar Entities internas diretamente.

---

# Responsabilidades

O Aggregate Root é responsável por:

- proteger invariantes;
- validar regras;
- controlar alterações;
- publicar eventos;
- manter consistência;
- impedir estados inválidos.

Nunca delegar essas responsabilidades para a infraestrutura.

---

# Estrutura

Todo Aggregate deverá possuir:

```text
Aggregate Root

↓

Entities

↓

Value Objects

↓

Domain Events

↓

Policies

↓

Specifications
```

---

# Exemplo

```text
SalesOrder

├── Items

├── Discounts

├── Delivery

├── Payments

├── Attachments

├── Events

└── Policies
```

---

# Invariantes

Todo Aggregate deverá proteger seus invariantes.

Exemplos:

## Sales Order

```text
Não pode possuir itens negativos.

Não pode ser aprovada sem cliente.

Não pode ser faturada sem aprovação.

Não pode ser cancelada após faturamento.
```

---

## Product

```text
SKU único.

Nome obrigatório.

Unidade obrigatória.

Categoria obrigatória.
```

---

## Customer

```text
Documento único.

Nome obrigatório.

Status válido.

Tenant obrigatório.
```

---

# Consistência

O Aggregate deverá garantir consistência interna.

Nunca depender de outro Aggregate para permanecer consistente.

Exemplo

```text
SalesOrder

↓

Consistente
```

Mesmo que:

```text
Inventory

↓

Offline
```

---

# Limites

Um Aggregate deve ser pequeno.

Sinais de Aggregate grande:

- centenas de Entities;
- milhares de linhas;
- muitas responsabilidades;
- muitas regras independentes.

Nestes casos deverá ser dividido.

---

# Referências

Aggregates nunca armazenam outros Aggregates completos.

Sempre utilizar referências.

Correto

```text
CustomerId

ProductId

SupplierId
```

Errado

```text
Customer

Product

Supplier
```

---

# Comunicação

Um Aggregate nunca modifica outro Aggregate.

Sempre utilizar:

```text
Commands

Events
```

Exemplo

```text
SalesOrderApproved

↓

Inventory

↓

ReserveStockCommand
```

---

# Persistência

O Aggregate desconhece completamente:

```text
SQLAlchemy

SQLite

PostgreSQL

Redis

Supabase

MongoDB
```

Persistência pertence à Infrastructure.

---

# Ciclo de Vida

Todo Aggregate deverá possuir um ciclo de vida claramente definido.

Exemplo

```text
Draft

↓

Pending

↓

Approved

↓

Executing

↓

Completed

↓

Archived
```

As transições deverão ser controladas pelo próprio Aggregate.

---

# Estados Inválidos

O Aggregate nunca permitirá estados inválidos.

Exemplo

```text
Invoice

Status = Authorized

Sem Número Fiscal
```

Nunca permitido.

Outro exemplo

```text
SalesOrder

Approved

Sem Itens
```

Nunca permitido.

---

# Eventos

Sempre que ocorrer uma alteração importante:

```text
↓

Publicar Domain Event
```

Exemplo

```text
CustomerCreated

CustomerUpdated

CustomerArchived
```

Os eventos pertencem ao Aggregate.

---

# Versionamento

Todo Aggregate deverá possuir:

```text
Version
```

Incrementado automaticamente.

Objetivos

- concorrência otimista;
- sincronização;
- auditoria;
- replay de eventos.

---

# Auditoria

Todo Aggregate deverá registrar:

```text
CreatedAt

CreatedBy

UpdatedAt

UpdatedBy

CorrelationId
```

Quando aplicável:

```text
DeletedAt

DeletedBy

ArchivedAt

ArchivedBy
```

---

# Multi-Tenant

Todo Aggregate deverá possuir:

```text
TenantId
```

Quando necessário:

```text
BranchId

DepartmentId
```

Nunca permitir acesso cruzado entre Tenants.

---

# Soft Delete

Todo Aggregate deverá suportar:

```text
IsDeleted

DeletedAt

DeletedBy
```

Nunca excluir fisicamente registros de negócio.

---

# Concorrência

Toda atualização deverá validar:

```text
Version
```

Em caso de conflito:

```text
ConcurrencyException
```

---

# Métodos

O Aggregate deverá expor apenas comportamentos.

Correto

```text
Approve()

Cancel()

Archive()

AddItem()

RemoveItem()

ChangePrice()
```

Errado

```text
SetStatus()

SetValue()

SetField()

UpdateEverything()
```

O comportamento deve refletir linguagem de negócio.

---

# Construtores

Construtores deverão ser mínimos.

Objetos complexos deverão utilizar:

```text
Factories
```

---

# Dependências

O Aggregate não poderá depender de:

```text
Database

API

HTTP

Email

Storage

Filesystem

Redis

Queue

Logger
```

---

# Testabilidade

Todo Aggregate deverá possuir testes unitários independentes.

Sem banco.

Sem API.

Sem infraestrutura.

---

# Convenções

Todo Aggregate deverá:

- possuir um único Root;
- proteger invariantes;
- publicar eventos;
- utilizar Value Objects sempre que possível;
- impedir alteração direta do estado interno;
- expor apenas comportamentos de negócio;
- ser independente da infraestrutura;
- ser completamente determinístico.

---

# Lista inicial de Aggregates do OrganizeG3

```text
Tenant

Branch

User

Role

Permission

Customer

Supplier

Lead

Opportunity

Quotation

SalesOrder

SalesContract

PurchaseRequest

PurchaseOrder

PurchaseReceipt

Product

Material

InventoryItem

Warehouse

ProductionOrder

ProductionRoute

BillOfMaterials

QualityInspection

MaintenanceOrder

Project

Task

Document

Workflow

WorkflowCard

Notification

FinancialAccount

Receivable

Payable

BankTransaction

FiscalDocument

TaxAssessment

AutomationWorkflow

AIAgent

SyncDevice

AuditLog
```

---

# Próximo Documento

```text
003-entity-design.md
```