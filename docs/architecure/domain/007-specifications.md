# Domain Model Specification
## 007 - Specifications

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial das Specifications do OrganizeG3.

Specifications representam regras de negócio reutilizáveis que respondem apenas uma pergunta:

```text
Esta condição é verdadeira?
```

Sempre retornam:

```text
True

ou

False
```

Nunca executam ações.

Nunca alteram estado.

---

# O que é uma Specification?

Uma Specification encapsula uma regra de negócio.

Ela representa uma condição reutilizável.

Exemplos

```text
Cliente pode comprar?

Produto está ativo?

Pedido pode ser aprovado?

Estoque suficiente?

Fornecedor homologado?
```

---

# Responsabilidade

Uma Specification deve apenas:

- validar regras;
- responder verdadeiro ou falso;
- ser reutilizável;
- ser independente da infraestrutura.

Nunca deverá:

- salvar dados;
- alterar entidades;
- enviar eventos;
- executar comandos.

---

# Estrutura

Uma Specification possui:

```text
Nome

↓

Critério

↓

Resultado Booleano
```

---

# Interface

Toda Specification deverá implementar:

```text
IsSatisfiedBy()
```

Exemplo

```text
CustomerCanBuySpecification

↓

IsSatisfiedBy(Customer)
```

Retorno

```text
True
```

ou

```text
False
```

---

# Composição

Specifications poderão ser combinadas.

Operadores

```text
AND

OR

NOT

XOR
```

---

## Exemplo

```text
CustomerIsActive

AND

CustomerHasCredit

AND

CustomerHasNoRestrictions
```

↓

```text
CustomerCanBuySpecification
```

---

# Reutilização

Uma mesma Specification poderá ser utilizada por:

```text
Sales

CRM

Financial

Automation

AI
```

Sem qualquer alteração.

---

# Quando utilizar

Utilizar Specifications quando:

- regras forem reutilizadas;
- regras forem complexas;
- regras precisarem ser compostas;
- regras forem independentes da entidade.

---

# Quando NÃO utilizar

Não utilizar para:

```text
Persistência

SQL

CRUD

HTTP

API

Infraestrutura

UI
```

---

# Specifications do CRM

Exemplos

```text
CustomerIsActiveSpecification

CustomerHasCreditSpecification

CustomerCanBuySpecification

CustomerHasValidEmailSpecification

CustomerHasValidDocumentSpecification

LeadCanBeConvertedSpecification

OpportunityCanBeWonSpecification
```

---

# Specifications do Comercial

```text
QuotationCanBeApprovedSpecification

DiscountAllowedSpecification

PriceTableValidSpecification

SalesOrderCanBeApprovedSpecification

SalesOrderCanBeCancelledSpecification
```

---

# Specifications do Financeiro

```text
PaymentCanBeReceivedSpecification

InvoiceCanBeIssuedSpecification

ReceivableOverdueSpecification

BankAccountActiveSpecification

CreditLimitAvailableSpecification
```

---

# Specifications do Estoque

```text
StockAvailableSpecification

LotAvailableSpecification

WarehouseActiveSpecification

MaterialCanBeReservedSpecification

InventoryMovementAllowedSpecification
```

---

# Specifications da Produção

```text
ProductionCanStartSpecification

MachineAvailableSpecification

MaterialAvailableSpecification

OperationCompletedSpecification

CapacityAvailableSpecification
```

---

# Specifications Fiscal

```text
InvoiceCanBeAuthorizedSpecification

TaxRuleValidSpecification

CFOPAllowedSpecification

NCMValidSpecification
```

---

# Specifications de Projetos

```text
TaskCanStartSpecification

TaskCanFinishSpecification

ProjectCanCloseSpecification

MilestoneReachedSpecification
```

---

# Specifications de Workflow

```text
WorkflowCanAdvanceSpecification

StageCompletedSpecification

CardCanMoveSpecification
```

---

# Specifications de Documentos

```text
DocumentCanBeArchivedSpecification

DocumentCanBeDeletedSpecification

DocumentVersionValidSpecification
```

---

# Specifications de Segurança

```text
PasswordStrongSpecification

UserCanLoginSpecification

PermissionGrantedSpecification

DeviceAuthorizedSpecification
```

---

# Composição Avançada

Exemplo

```text
SalesOrderCanBeApprovedSpecification

=

CustomerIsActive

AND

CustomerHasCredit

AND

HasItems

AND

TotalGreaterThanZero

AND

StatusIsDraft
```

Cada regra permanece independente.

---

# Dependências

Uma Specification poderá utilizar:

```text
Entities

Value Objects

Policies

Outras Specifications
```

Nunca depender de:

```text
Banco

HTTP

Redis

Logger

Filesystem

API

SQLAlchemy
```

---

# Stateless

Toda Specification deverá ser Stateless.

Nunca armazenar estado interno.

---

# Determinismo

A mesma entrada deverá produzir exatamente a mesma saída.

Sempre.

---

# Nomeclatura

Padrão

```text
<Objeto><Condição>Specification
```

Exemplos

```text
CustomerCanBuySpecification

InvoiceCanBeCancelledSpecification

MaterialAvailableSpecification

ProjectCanCloseSpecification
```

---

# Testabilidade

Toda Specification deverá possuir testes unitários.

Casos mínimos

```text
Caso verdadeiro

Caso falso

Casos extremos

Valores inválidos
```

---

# Performance

Specifications deverão ser leves.

Nunca executar:

- consultas SQL;
- chamadas HTTP;
- leitura de arquivos.

Caso dependam de dados externos, estes deverão ser fornecidos pelo Application Layer.

---

# Regras Gerais

Uma Specification nunca deverá:

- alterar estado;
- publicar eventos;
- executar comandos;
- salvar entidades.

Ela apenas responde:

```text
A regra é satisfeita?
```

---

# Checklist

Antes de criar uma Specification verificar:

- representa uma regra de negócio?
- retorna apenas verdadeiro ou falso?
- é reutilizável?
- é Stateless?
- não depende da infraestrutura?
- pode ser combinada com outras Specifications?
- possui testes?

Se qualquer resposta for "não", revisar a modelagem.

---

# Convenções

Toda Specification deverá:

- possuir responsabilidade única;
- ser altamente reutilizável;
- ser determinística;
- ser independente da infraestrutura;
- utilizar linguagem do domínio;
- permitir composição.

---

# Próximo Documento

```text
008-policies.md
```