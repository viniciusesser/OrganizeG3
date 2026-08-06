# Domain Model Specification
## 006 - Domain Services

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para implementação de Domain Services no OrganizeG3.

Os Domain Services representam regras de negócio que não pertencem naturalmente a uma Entity, Aggregate ou Value Object.

Todo Domain Service deverá seguir exatamente estas definições.

---

# O que é um Domain Service?

Um Domain Service representa um comportamento do domínio.

Ele executa regras que envolvem múltiplos objetos de negócio.

Exemplo

```text
Pedido

↓

Cliente

↓

Tabela de Preços

↓

Campanha

↓

Política Comercial

↓

Preço Final
```

Essa lógica pertence a um Domain Service.

---

# Quando utilizar

Utilizar Domain Service quando:

- envolver mais de um Aggregate;
- envolver várias Entities;
- envolver diversos Value Objects;
- a regra não possuir um dono claro;
- representar um processo de negócio.

---

# Quando NÃO utilizar

Não utilizar Domain Service para:

```text
CRUD

Persistência

SQL

HTTP

API

Email

Cache

Logs

Arquivos

Integrações
```

Essas responsabilidades pertencem à Infrastructure.

---

# Responsabilidades

Um Domain Service deverá:

- executar regras de negócio;
- coordenar Aggregates;
- utilizar Specifications;
- consultar Policies;
- produzir resultados previsíveis.

Nunca deverá alterar diretamente a infraestrutura.

---

# Dependências

Um Domain Service poderá depender apenas de:

```text
Aggregates

Entities

Value Objects

Policies

Specifications

Outros Domain Services
```

Nunca depender de:

```text
FastAPI

SQLAlchemy

Redis

Filesystem

HTTP

Supabase

Qt

PySide

Logger
```

---

# Exemplo

## PriceCalculator

Responsável por calcular:

```text
Preço Base

↓

Desconto

↓

Tabela Comercial

↓

Promoção

↓

Impostos

↓

Preço Final
```

---

## TaxCalculator

Responsável por:

```text
ICMS

IPI

PIS

COFINS

ISS

Retenções
```

---

## CommissionCalculator

Responsável por:

```text
Vendedor

Supervisor

Gerente

Campanhas

Bonificações
```

---

## InventoryReservationService

Responsável por:

```text
Reservar estoque

Liberar estoque

Validar disponibilidade

Priorizar reservas
```

---

## ProductionPlanningService

Responsável por:

```text
Planejamento

Sequenciamento

Capacidade

Recursos

Materiais
```

---

# Stateless

Todo Domain Service deverá ser Stateless.

Nunca armazenar:

```text
Estado

Sessão

Cache

Variáveis globais
```

Cada execução deverá ser independente.

---

# Retorno

Um Domain Service deverá retornar:

```text
Value Objects

Entities

Resultados

Decisões
```

Nunca retornar:

```text
Response HTTP

JSON bruto

SQL

Objetos da infraestrutura
```

---

# Regras

Um Domain Service nunca deverá:

- persistir dados;
- abrir conexões;
- enviar emails;
- executar SQL;
- chamar APIs externas;
- acessar arquivos.

Essas responsabilidades pertencem à camada Infrastructure.

---

# Composição

Um Domain Service poderá utilizar:

```text
Policies

Specifications

Value Objects

Factories
```

Para compor sua lógica.

---

# Domain Services previstos

## Comercial

```text
PriceCalculator

DiscountCalculator

CommercialPolicyService

QuotationGenerator

CommissionCalculator
```

---

## Financeiro

```text
InterestCalculator

FineCalculator

CashFlowCalculator

PaymentAllocationService

BankReconciliationService
```

---

## Fiscal

```text
TaxCalculator

FiscalRuleService

NFeValidationService

CFOPResolver

TributaryClassifier
```

---

## Produção

```text
ProductionPlanningService

CapacityPlanner

OperationSequencer

ProductionCostCalculator

ResourceAllocationService
```

---

## Estoque

```text
InventoryReservationService

StockAvailabilityService

InventoryValuationService

LotSelectionService
```

---

## Compras

```text
SupplierSelectionService

PurchaseSuggestionService

LeadTimeCalculator

PurchaseApprovalService
```

---

## CRM

```text
LeadScoringService

CustomerClassificationService

CustomerCreditAnalyzer
```

---

## Projetos

```text
ProjectSchedulingService

CriticalPathCalculator

ResourcePlanner
```

---

## Workflow

```text
WorkflowExecutionService

WorkflowValidationService

WorkflowRoutingService
```

---

## Documentos

```text
DocumentClassificationService

DocumentVersionService

DocumentValidationService
```

---

## Qualidade

```text
InspectionEvaluationService

NonConformityService

QualityScoreCalculator
```

---

# Exemplo de Fluxo

```text
Sales Order

↓

PriceCalculator

↓

DiscountCalculator

↓

TaxCalculator

↓

SalesOrderTotal
```

Cada serviço possui responsabilidade única.

---

# Comunicação

Domain Services poderão publicar Domain Events através do Aggregate Root.

Nunca publicar diretamente no Event Bus.

Fluxo correto

```text
Domain Service

↓

Aggregate

↓

Domain Event

↓

Application

↓

Infrastructure
```

---

# Testabilidade

Todo Domain Service deverá possuir testes unitários.

Os testes nunca dependerão de:

```text
Banco

API

Fila

Cache

Filesystem
```

---

# Performance

Domain Services deverão ser determinísticos.

Uma mesma entrada deverá produzir exatamente a mesma saída.

Sempre que possível.

---

# Convenções

Nomenclatura

```text
<Domínio><Ação>Service
```

Exemplos

```text
PriceCalculatorService

ProductionPlanningService

InventoryReservationService

PaymentAllocationService

TaxCalculationService
```

---

# Checklist

Antes de criar um Domain Service verificar:

- a regra pertence realmente ao domínio?
- envolve mais de um Aggregate?
- não pertence a uma Entity?
- não pertence ao Aggregate Root?
- não depende da infraestrutura?
- é reutilizável?
- possui testes?

Se alguma resposta for "não", revisar a modelagem.

---

# Regras Gerais

Todo Domain Service deverá:

- possuir responsabilidade única;
- ser Stateless;
- ser determinístico;
- não conhecer infraestrutura;
- utilizar linguagem de negócio;
- ser altamente reutilizável;
- possuir testes independentes.

---

# Próximo Documento

```text
007-specifications.md
```