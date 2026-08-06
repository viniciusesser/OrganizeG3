# Application Architecture Specification
## 017 - DTOs (Data Transfer Objects)

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos DTOs (Data Transfer Objects) do OrganizeG3.

DTOs são objetos destinados exclusivamente à transferência de dados entre camadas da aplicação.

Eles não representam regras de negócio.

Não representam entidades.

Não representam tabelas do banco.

Representam apenas contratos de comunicação.

---

# O que é um DTO?

Um DTO é um objeto simples utilizado para transportar dados.

Fluxo

```text
Presentation

↓

DTO

↓

Application

↓

DTO

↓

Presentation
```

O domínio nunca deverá expor Entities diretamente.

---

# Objetivos

Os DTOs existem para:

- desacoplar o domínio;
- proteger Entities;
- reduzir dependências;
- facilitar serialização;
- padronizar respostas;
- controlar versionamento da API.

---

# Responsabilidades

Um DTO poderá:

- transportar dados;
- validar tipos básicos;
- serializar informações;
- desserializar informações.

Nunca deverá:

- executar regras de negócio;
- acessar banco;
- executar SQL;
- publicar eventos;
- modificar Aggregates.

---

# Estrutura

Todo DTO deverá conter apenas:

```text
Campos

Tipos

Documentação

Metadados
```

Nunca métodos de negócio.

---

# Tipos de DTO

O OrganizeG3 utilizará cinco categorias principais.

```text
Request DTO

Response DTO

Summary DTO

Detail DTO

Event DTO
```

---

# Request DTO

Representa dados enviados para execução de um Caso de Uso.

Exemplo

```text
CreateCustomerRequest

UpdateProductRequest

ApproveSalesOrderRequest
```

Nunca conter:

```text
Campos calculados

Regras

Estado interno
```

---

# Response DTO

Representa dados retornados para a interface.

Exemplo

```text
CustomerResponse

ProductResponse

SalesOrderResponse
```

---

# Summary DTO

Utilizado em listagens.

Exemplo

```text
CustomerSummary

ProductSummary

SupplierSummary
```

Possui apenas campos necessários para exibição.

---

# Detail DTO

Representa uma visualização completa.

Exemplo

```text
CustomerDetails

SalesOrderDetails

ProductionOrderDetails
```

Pode conter coleções.

---

# Event DTO

Utilizado para integração.

Exemplo

```text
CustomerCreatedEventDto

InvoiceAuthorizedEventDto

PaymentReceivedEventDto
```

---

# Convenções

Nome

```text
<Entity><Tipo>
```

Exemplos

```text
CustomerResponse

CustomerSummary

CustomerDetails

CustomerRequest
```

---

# Imutabilidade

Sempre que possível DTOs deverão ser imutáveis.

Após criados:

```text
↓

Somente leitura
```

---

# Serialização

Todo DTO deverá suportar:

```text
JSON

MessagePack

XML

CSV

Excel

Parquet

Future Formats
```

Quando aplicável.

---

# Validação

DTOs poderão validar apenas:

```text
Tipos

Obrigatoriedade

Tamanho

Formato

Valores padrão
```

Nunca:

```text
Regras de domínio
```

---

# Versionamento

DTOs poderão possuir versões.

Exemplo

```text
CustomerResponseV1

CustomerResponseV2
```

Permitindo evolução da API.

---

# Relacionamentos

DTOs poderão conter outros DTOs.

Exemplo

```text
SalesOrderDetails

↓

CustomerSummary

↓

Items

↓

Totals
```

Nunca Entities.

---

# Mapeamento

A transformação entre Domain e DTO será responsabilidade dos Mappers.

Nunca do próprio DTO.

Fluxo

```text
Aggregate

↓

Mapper

↓

DTO
```

---

# DTOs por Contexto

## Identity

```text
TenantResponse

BranchResponse

UserResponse

RoleResponse
```

---

## CRM

```text
CustomerSummary

CustomerDetails

LeadSummary

OpportunityDetails
```

---

## Comercial

```text
QuotationResponse

SalesOrderResponse

SalesOrderSummary

SalesOrderDetails
```

---

## Compras

```text
PurchaseOrderResponse

PurchaseReceiptResponse
```

---

## Estoque

```text
ProductResponse

InventoryBalanceResponse

WarehouseResponse
```

---

## Produção

```text
ProductionOrderResponse

OperationResponse

MaterialConsumptionResponse
```

---

## Financeiro

```text
ReceivableResponse

PayableResponse

BankTransactionResponse

CashFlowResponse
```

---

## Fiscal

```text
InvoiceResponse

TaxSummaryResponse
```

---

## Projetos

```text
ProjectResponse

TaskResponse

MilestoneResponse
```

---

## Workflow

```text
WorkflowResponse

WorkflowCardResponse
```

---

## IA

```text
ConversationResponse

PromptResponse

AgentResponse
```

---

## Sincronização

```text
DeviceResponse

SnapshotResponse

SynchronizationResponse
```

---

# Campos Calculados

DTOs poderão conter informações calculadas.

Exemplo

```text
Total Items

Total Value

Remaining Balance

Completion Percentage

Current Status Description
```

Esses dados não pertencem ao domínio.

São preparados pelo Query Handler.

---

# Paginação

Listagens utilizarão:

```text
Items

Page

PageSize

TotalItems

TotalPages

HasNext

HasPrevious
```

---

# Ordenação

DTOs poderão informar:

```text
SortField

Direction
```

Para auxiliar a interface.

---

# Localização

Datas e valores poderão ser formatados na Presentation.

DTOs preferencialmente transportarão:

```text
UTC

Decimal

ISO-8601

Currency Code
```

---

# Segurança

DTOs nunca deverão conter:

```text
Password

PasswordHash

Refresh Token

Private Keys

Secrets

Internal IDs

Connection Strings
```

---

# Performance

DTOs deverão conter apenas os dados necessários.

Evitar:

```text
Campos desnecessários

Objetos enormes

Coleções completas
```

Utilizar DTOs específicos para cada tela.

---

# Testabilidade

Todo DTO deverá possuir testes de:

```text
Serialização

Desserialização

Versionamento

Compatibilidade

Campos obrigatórios
```

---

# Organização

Estrutura sugerida

```text
dtos/

    requests/

    responses/

    summaries/

    details/

    events/

    shared/
```

---

# Checklist

Antes de criar um DTO verificar:

- representa apenas transporte de dados?
- não contém regras?
- não depende do domínio?
- pode ser serializado?
- possui nome adequado?
- contém apenas campos necessários?

---

# Regras Gerais

Todo DTO deverá:

- ser simples;
- ser pequeno;
- ser serializável;
- ser independente do domínio;
- nunca conter regras de negócio;
- nunca conhecer infraestrutura;
- ser facilmente versionável.

---

# Fluxo Completo

```text
Presentation

↓

Request DTO

↓

Command

↓

Domain

↓

Mapper

↓

Response DTO

↓

Presentation
```

---

# Próximo Documento

```text
018-validators.md
```