# Application Architecture Specification
## 015 - Queries

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial das Queries do OrganizeG3.

As Queries representam operações exclusivamente de leitura.

Elas nunca alteram o estado do sistema.

As Queries fazem parte do lado de leitura da arquitetura CQRS.

---

# O que é uma Query?

Uma Query representa uma solicitação de consulta.

Ela descreve quais informações o usuário deseja obter.

Exemplos

```text
Buscar Cliente

Listar Produtos

Consultar Estoque

Pesquisar Pedidos

Dashboard Financeiro

Extrato Bancário

Agenda de Produção
```

---

# Responsabilidades

Uma Query deverá apenas:

- transportar parâmetros de pesquisa;
- transportar filtros;
- transportar paginação;
- transportar ordenação.

Nunca deverá:

- alterar dados;
- executar regras de domínio;
- publicar eventos;
- executar Commands.

---

# Arquitetura

```text
Presentation

↓

Query

↓

Validator

↓

Query Handler

↓

Read Model

↓

DTO

↓

Presentation
```

---

# CQRS

Queries pertencem ao lado de leitura.

Commands pertencem ao lado de escrita.

```text
Write

↓

Commands

↓

Repositories

↓

Domain
```

```text
Read

↓

Queries

↓

Read Database

↓

DTOs
```

---

# Estrutura

Toda Query deverá possuir:

```text
QueryId

TenantId

UserId

CorrelationId

OccurredAt

Payload
```

---

# QueryId

Cada Query possuirá um identificador.

Padrão

```text
UUID v4
```

---

# TenantId

Toda Query deverá informar:

```text
TenantId
```

Nenhuma consulta poderá acessar outro Tenant.

---

# UserId

Responsável por:

- auditoria;
- permissões;
- personalização;
- segurança.

---

# CorrelationId

Toda Query deverá possuir:

```text
CorrelationId
```

Permitindo rastrear toda a operação.

---

# Payload

O Payload poderá conter:

```text
Filtros

Ordenação

Paginação

Pesquisa

Datas

Status

Identificadores
```

---

# Tipos de Query

## Consulta por ID

Exemplo

```text
GetCustomerByIdQuery

GetProductByIdQuery

GetInvoiceByIdQuery
```

---

## Pesquisa

Exemplo

```text
SearchCustomersQuery

SearchProductsQuery

SearchDocumentsQuery
```

---

## Listagem

Exemplo

```text
ListProductsQuery

ListWarehousesQuery

ListEmployeesQuery
```

---

## Dashboard

Exemplo

```text
FinancialDashboardQuery

SalesDashboardQuery

ProductionDashboardQuery
```

---

## Relatórios

Exemplo

```text
InventoryReportQuery

CashFlowReportQuery

ProductionReportQuery
```

---

# Imutabilidade

Toda Query deverá ser imutável.

Após criada, não poderá sofrer alterações.

---

# Paginação

Toda consulta grande deverá suportar paginação.

Campos

```text
Page

PageSize

Offset

Limit
```

---

# Ordenação

Toda Query poderá definir:

```text
SortBy

Direction

Multiple Sorts
```

---

# Filtros

Filtros deverão ser explícitos.

Exemplo

```text
Status

Período

Categoria

Cliente

Projeto

Fornecedor
```

Nunca utilizar filtros genéricos.

---

# Pesquisa

Queries poderão utilizar:

```text
Texto

Código

Documento

Email

Telefone

SKU

Código de Barras
```

---

# Read Models

As Queries utilizarão Read Models.

Nunca Aggregates.

Objetivo

```text
Maior desempenho

Menor acoplamento

Consultas específicas
```

---

# DTOs

Toda Query retornará DTOs.

Nunca retornar:

```text
Entities

Aggregates

Repositories

SQLAlchemy Models
```

---

# Performance

Queries poderão utilizar:

```text
Views

Materialized Views

Cache

Índices

Read Database
```

Sem impactar o domínio.

---

# Cache

Consultas poderão utilizar cache.

Exemplos

```text
Dashboard

Relatórios

Listagens

Catálogos
```

Nunca cachear dados críticos sem invalidação.

---

# Segurança

Toda Query deverá validar:

```text
Tenant

Permissões

Usuário

Feature Flags
```

Antes da execução.

---

# Auditoria

Registrar:

```text
QueryId

CorrelationId

TenantId

UserId

ExecutionTime

Quantidade de Registros
```

---

# Validação

Toda Query poderá possuir Validator.

Responsável por:

```text
Filtros obrigatórios

Datas válidas

Paginação

Ordenação

Tipos
```

Nunca validar regras de domínio.

---

# Assincronismo

Algumas Queries poderão ser executadas em background.

Exemplos

```text
Grandes relatórios

Exportações

Business Intelligence

Analytics
```

---

# Convenções

Nome

```text
Verbo + Objeto + Query
```

Exemplos

```text
GetCustomerByIdQuery

SearchProductsQuery

ListProjectsQuery

GenerateCashFlowReportQuery
```

---

# Exemplos

## CRM

```text
GetCustomerByIdQuery

SearchCustomersQuery

ListCustomersQuery

CustomerHistoryQuery
```

---

## Comercial

```text
QuotationDetailsQuery

SalesOrderDetailsQuery

SalesDashboardQuery
```

---

## Compras

```text
PurchaseOrderQuery

SupplierBalanceQuery
```

---

## Estoque

```text
InventoryBalanceQuery

InventoryMovementQuery

WarehouseOccupancyQuery
```

---

## Produção

```text
ProductionQueueQuery

ProductionTimelineQuery

CapacityAnalysisQuery
```

---

## Financeiro

```text
CashFlowQuery

ReceivablesQuery

PayablesQuery

BankStatementQuery
```

---

## Fiscal

```text
FiscalDocumentQuery

TaxSummaryQuery
```

---

## Projetos

```text
ProjectStatusQuery

TaskBoardQuery
```

---

## Workflow

```text
WorkflowBoardQuery

WorkflowHistoryQuery
```

---

## IA

```text
PromptHistoryQuery

ConversationQuery

AgentUsageQuery
```

---

# Anti-Patterns

Nunca fazer:

```text
Alterar banco

Executar Commands

Salvar dados

Atualizar Aggregates

Executar Commit
```

Queries são exclusivamente leitura.

---

# Checklist

Antes de criar uma Query verificar:

- altera dados?
- executa regras?
- retorna DTO?
- suporta Tenant?
- possui CorrelationId?
- possui paginação?
- possui filtros claros?
- possui testes?

Se qualquer resposta estiver incorreta, revisar a modelagem.

---

# Regras Gerais

Toda Query deverá:

- ser imutável;
- representar uma consulta;
- retornar DTOs;
- nunca alterar dados;
- nunca utilizar Aggregates;
- utilizar Read Models;
- possuir validação;
- possuir testes.

---

# Fluxo Completo

```text
Request

↓

Query

↓

Validator

↓

Query Handler

↓

Read Model

↓

DTO

↓

Response
```

---

# Próximo Documento

```text
016-query-handlers.md
```