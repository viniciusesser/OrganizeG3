# Domain Model Specification
## 003 - Entity Design

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para implementação de Entities no OrganizeG3.

Toda Entity do sistema deverá seguir exatamente estas regras.

Caso exista divergência entre o código e esta documentação, este documento prevalece.

---

# O que é uma Entity?

Uma Entity representa um objeto do domínio que possui identidade própria.

Mesmo que seus atributos mudem ao longo do tempo, sua identidade permanece.

Exemplos

```text
Cliente

Fornecedor

Pedido

Produto

Projeto

Documento

Funcionário
```

---

# Características

Toda Entity possui:

- identidade;
- ciclo de vida;
- comportamento;
- regras de negócio;
- estado mutável.

---

# Identidade

Toda Entity deverá possuir um identificador único.

Padrão

```text
UUID v4
```

Exemplo

```text
CustomerId

ProductId

SalesOrderId

InvoiceId

ProductionOrderId
```

A identidade nunca muda.

---

# Entity x Value Object

Entity

```text
Possui identidade.

Pode mudar.

É rastreável.
```

Value Object

```text
Não possui identidade.

É imutável.

É comparado pelo valor.
```

---

# Responsabilidades

Uma Entity deverá ser responsável por:

- proteger seu estado;
- validar alterações;
- executar regras de negócio locais;
- impedir estados inválidos.

Nunca deverá conhecer:

- banco de dados;
- API;
- SQL;
- infraestrutura;
- interface gráfica.

---

# Comportamentos

Uma Entity deve expor comportamentos.

Correto

```text
Activate()

Deactivate()

Approve()

Cancel()

Archive()

Rename()

Move()

Assign()
```

Evitar

```text
SetStatus()

SetName()

SetValue()

Update()
```

Os métodos devem refletir linguagem de negócio.

---

# Estado

O estado interno deverá ser protegido.

Nunca expor coleções mutáveis diretamente.

Correto

```text
ReadOnlyCollection
```

Errado

```text
List pública
```

---

# Construtores

Construtores devem ser mínimos.

Quando a criação exigir muitas regras utilizar:

```text
Factory
```

---

# Ciclo de Vida

Toda Entity deverá possuir um ciclo de vida definido.

Exemplo

```text
Created

↓

Active

↓

Inactive

↓

Archived
```

Nem toda Entity utilizará todos os estados.

---

# Integridade

Uma Entity nunca poderá assumir um estado inválido.

Exemplo

```text
Produto

Preço negativo
```

Nunca permitido.

Outro exemplo

```text
Cliente

Email inválido
```

Nunca permitido.

---

# Atualizações

Toda alteração deverá ocorrer através de métodos específicos.

Exemplo

Correto

```text
ChangeEmail()

ChangePhone()

ChangeAddress()

ChangeCreditLimit()
```

Errado

```text
Update()
```

---

# Igualdade

Entities são comparadas pela identidade.

Exemplo

```text
Customer

Id = 10
```

Mesmo alterando:

```text
Nome

Telefone

Email
```

Continua sendo o mesmo Customer.

---

# Auditoria

Toda Entity deverá armazenar quando aplicável

```text
CreatedAt

CreatedBy

UpdatedAt

UpdatedBy

Version
```

---

# Multi-Tenant

Toda Entity pertencente ao domínio empresarial deverá possuir

```text
TenantId
```

Quando necessário

```text
BranchId

DepartmentId
```

---

# Exclusão

Entities de negócio utilizarão Soft Delete.

Campos

```text
IsDeleted

DeletedAt

DeletedBy
```

Nunca excluir registros importantes fisicamente.

---

# Versionamento

Toda Entity deverá possuir

```text
Version
```

Incrementado automaticamente a cada alteração.

Objetivos

- concorrência otimista;
- sincronização;
- auditoria.

---

# Navegação

Uma Entity poderá navegar apenas para objetos pertencentes ao mesmo Aggregate.

Nunca navegar diretamente para outro Aggregate.

Correto

```text
SalesOrder

↓

SalesOrderItem
```

Errado

```text
SalesOrder

↓

Customer
```

Utilizar apenas

```text
CustomerId
```

---

# Eventos

Sempre que ocorrer uma alteração relevante:

```text
↓

Aggregate publica Domain Event
```

A Entity nunca publica eventos diretamente.

Sempre comunica ao Aggregate Root.

---

# Dependências

Entities nunca dependerão de

```text
SQLAlchemy

FastAPI

Redis

SQLite

PostgreSQL

HTTP

Filesystem

Logger

Email

Storage
```

---

# Persistência

A Entity desconhece completamente como será persistida.

Ela poderá existir:

- em memória;
- em SQLite;
- PostgreSQL;
- Event Store;
- outro banco.

Sem qualquer alteração na regra de negócio.

---

# Imutabilidade Parcial

Alguns atributos poderão ser imutáveis.

Exemplo

```text
Id

CreatedAt

CreatedBy

TenantId
```

Nunca alterados após criação.

---

# Encapsulamento

Nunca permitir

```python
customer.name = "Novo Nome"
```

Sempre utilizar

```python
customer.rename(...)
```

---

# Coleções

Coleções internas deverão ser protegidas.

Adicionar

```text
AddItem()
```

Remover

```text
RemoveItem()
```

Nunca permitir

```text
Items.Clear()

Items.Add()

Items.Remove()
```

Externamente.

---

# Validação

Toda validação pertencente à Entity deverá ocorrer nela própria.

Exemplo

```text
Email

Telefone

CPF

CNPJ

Nome
```

Validações complexas poderão utilizar Specifications.

---

# Tamanho

Uma Entity deve possuir responsabilidade única.

Sinais de Entity excessivamente grande

- centenas de métodos;
- dezenas de responsabilidades;
- múltiplos domínios.

Nestes casos deverá ser dividida.

---

# Herança

Evitar herança profunda.

Preferir

```text
Composição

Interfaces

Value Objects
```

---

# Exemplos de Entities do OrganizeG3

```text
Customer

Supplier

Lead

Opportunity

Quotation

SalesOrderItem

PurchaseOrderItem

Material

Product

InventoryLot

WarehouseLocation

ProductionOperation

ProductionResource

InspectionItem

MaintenanceTask

ProjectTask

DocumentVersion

NotificationRecipient

ReceivableInstallment

PayableInstallment

FiscalDocumentItem

WorkflowStage

WorkflowCard

AutomationStep

PromptVersion

SyncDevice

AuditEntry
```

---

# Checklist de uma Entity

Antes de implementar verificar:

- possui identidade?
- pertence a um Aggregate?
- protege seu estado?
- expõe comportamentos?
- impede estados inválidos?
- não depende da infraestrutura?
- possui testes?
- possui Version?
- possui TenantId quando necessário?
- utiliza Value Objects sempre que possível?

Se qualquer resposta for "não", revisar a modelagem.

---

# Próximo Documento

```text
004-value-objects.md
```