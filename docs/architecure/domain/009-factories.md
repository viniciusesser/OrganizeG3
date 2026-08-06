# Domain Model Specification
## 009 - Factories

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para implementação das Factories do OrganizeG3.

Factories são responsáveis por construir Aggregates, Entities e Value Objects complexos, garantindo que todos sejam criados em um estado válido.

Nenhuma regra de criação complexa deverá ficar em construtores.

---

# O que é uma Factory?

Uma Factory encapsula o processo de criação de objetos de domínio.

Ela garante que todas as regras obrigatórias sejam aplicadas antes que o objeto exista.

Exemplo

```text
Novo Pedido

↓

Validar Cliente

↓

Validar Empresa

↓

Gerar Número

↓

Criar Pedido

↓

Publicar Evento
```

---

# Objetivos

Factories existem para:

- reduzir construtores complexos;
- centralizar regras de criação;
- evitar objetos inválidos;
- facilitar testes;
- melhorar legibilidade;
- desacoplar o processo de construção.

---

# Quando utilizar

Utilizar Factory quando:

- o objeto possui muitos parâmetros;
- existem diversas validações obrigatórias;
- existe geração automática de dados;
- há composição de várias Entities;
- há criação de Value Objects complexos.

---

# Quando NÃO utilizar

Não utilizar Factories para:

```text
Persistência

Atualização

Consulta

Remoção

Infraestrutura

HTTP

SQL

API
```

---

# Responsabilidades

Uma Factory poderá:

- criar Aggregates;
- criar Entities;
- criar Value Objects;
- montar estruturas complexas;
- aplicar regras iniciais;
- inicializar coleções;
- configurar estados iniciais.

Nunca deverá:

- salvar dados;
- executar SQL;
- chamar APIs;
- enviar emails;
- publicar eventos diretamente.

---

# Aggregate Factory

Cada Aggregate complexo poderá possuir sua própria Factory.

Exemplo

```text
SalesOrderFactory

CustomerFactory

InvoiceFactory

ProductionOrderFactory

ProjectFactory
```

---

# Exemplo

Fluxo

```text
Create Sales Order

↓

SalesOrderFactory

↓

Customer Validation

↓

Price Policy

↓

Sales Order

↓

SalesOrderCreated
```

---

# Estados Iniciais

Toda Factory deverá criar objetos em estado consistente.

Exemplo

```text
SalesOrder

↓

Status

Draft
```

Nunca

```text
Status

Approved
```

Na criação.

---

# Inicialização

Toda coleção deverá nascer inicializada.

Correto

```text
Items = []
```

Nunca

```text
Items = null
```

---

# Geração de Identificadores

A Factory poderá gerar:

```text
UUID

Número temporário

Código interno

Sequência provisória
```

Numerações oficiais dependerão das Policies apropriadas.

---

# Value Objects

A Factory deverá criar Value Objects sempre que necessário.

Exemplo

```text
CustomerFactory

↓

Email

↓

Phone

↓

Address

↓

Customer
```

Nunca deixar essa responsabilidade para a interface.

---

# Factories previstas

## Comercial

```text
CustomerFactory

LeadFactory

OpportunityFactory

QuotationFactory

SalesOrderFactory

SalesContractFactory
```

---

## Compras

```text
SupplierFactory

PurchaseRequestFactory

PurchaseOrderFactory

PurchaseReceiptFactory
```

---

## Produção

```text
ProductionOrderFactory

BillOfMaterialsFactory

ProductionRouteFactory

OperationFactory
```

---

## Estoque

```text
InventoryItemFactory

WarehouseFactory

InventoryLotFactory
```

---

## Financeiro

```text
ReceivableFactory

PayableFactory

FinancialAccountFactory

BankTransactionFactory
```

---

## Fiscal

```text
FiscalDocumentFactory

TaxAssessmentFactory
```

---

## Projetos

```text
ProjectFactory

TaskFactory

MilestoneFactory
```

---

## Workflow

```text
WorkflowFactory

WorkflowCardFactory

WorkflowStageFactory
```

---

## Documentos

```text
DocumentFactory

DocumentVersionFactory
```

---

## IA

```text
PromptFactory

AgentFactory

ConversationFactory
```

---

## Sincronização

```text
SyncDeviceFactory

SnapshotFactory
```

---

# Dependências

Factories poderão utilizar:

```text
Value Objects

Policies

Specifications

Domain Services
```

Nunca depender de:

```text
Banco

Redis

FastAPI

HTTP

Filesystem

Logger

Supabase
```

---

# Composição

Factories poderão utilizar outras Factories.

Exemplo

```text
SalesOrderFactory

↓

CustomerFactory

↓

AddressFactory

↓

PhoneFactory
```

---

# Imutabilidade

Factories não armazenam estado.

Cada execução é independente.

---

# Testabilidade

Toda Factory deverá possuir testes.

Casos mínimos

```text
Criação válida

Dados inválidos

Valores obrigatórios

Valores opcionais

Estados iniciais
```

---

# Convenções

Nome

```text
<Entity>Factory
```

Exemplos

```text
CustomerFactory

SalesOrderFactory

InvoiceFactory

ProductionOrderFactory
```

---

# Checklist

Antes de criar uma Factory verificar:

- existe lógica de criação complexa?
- há muitas validações?
- o construtor ficou grande?
- existem vários Value Objects?
- existem estados iniciais?
- a Factory não depende da infraestrutura?
- possui testes?

---

# Regras Gerais

Toda Factory deverá:

- criar objetos válidos;
- aplicar regras iniciais;
- utilizar linguagem de domínio;
- não conhecer infraestrutura;
- não persistir dados;
- não executar integrações.

---

# Fluxo Arquitetural

```text
Application

↓

Command Handler

↓

Factory

↓

Aggregate

↓

Domain Event

↓

Repository

↓

Infrastructure
```

---

# Próximo Documento

```text
010-repositories.md
```