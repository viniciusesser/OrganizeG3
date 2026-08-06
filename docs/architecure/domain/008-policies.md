# Domain Model Specification
## 008 - Policies

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial das Policies do OrganizeG3.

Policies representam políticas corporativas que orientam decisões do domínio.

Enquanto uma Specification responde se algo é verdadeiro ou falso, uma Policy define **como uma decisão deve ser tomada**.

---

# O que é uma Policy?

Uma Policy representa uma política da empresa.

Ela centraliza regras que podem variar conforme:

- empresa;
- filial;
- legislação;
- contrato;
- configuração;
- estratégia comercial.

As Policies tornam o domínio flexível sem alterar o código das Entities.

---

# Responsabilidades

Uma Policy deverá:

- representar regras corporativas;
- definir critérios de decisão;
- ser reutilizável;
- ser independente da infraestrutura;
- utilizar linguagem de negócio.

Nunca deverá:

- executar SQL;
- acessar APIs;
- alterar banco de dados;
- enviar eventos;
- modificar Aggregates diretamente.

---

# Quando utilizar

Utilizar Policies quando:

- uma regra depende da empresa;
- uma regra pode mudar ao longo do tempo;
- uma decisão envolve diversos fatores;
- uma regra pode ser configurável.

---

# Quando NÃO utilizar

Não utilizar Policies para:

```text
CRUD

Persistência

Autenticação

Interface

Infraestrutura

Cache

HTTP
```

---

# Diferença entre Specification e Policy

## Specification

Responde apenas:

```text
Sim

Não
```

Exemplo

```text
Cliente pode comprar?
```

---

## Policy

Define:

```text
Como decidir.
```

Exemplo

```text
Qual desconto aplicar?
```

---

# Exemplo

Uma empresa pode definir:

```text
Até 5%

↓

Vendedor
```

```text
Até 10%

↓

Supervisor
```

```text
Acima de 10%

↓

Diretoria
```

Essa lógica pertence a uma Policy.

---

# Estrutura

Uma Policy poderá utilizar:

```text
Entities

Value Objects

Specifications

Configuration

Outras Policies
```

Nunca utilizar infraestrutura.

---

# Policies Comerciais

Exemplos

```text
DiscountPolicy

CommercialPolicy

SalesApprovalPolicy

CommissionPolicy

PricePolicy

PromotionPolicy

ContractPolicy
```

---

## DiscountPolicy

Responsável por decidir:

```text
Quem pode conceder desconto

Valor máximo

Percentual permitido

Exceções

Motivos obrigatórios
```

---

## PricePolicy

Responsável por definir:

```text
Tabela utilizada

Preço mínimo

Preço máximo

Preço promocional

Preço por cliente
```

---

## CommissionPolicy

Define:

```text
Percentual

Campanhas

Metas

Bonificações

Comissões especiais
```

---

# Policies Financeiras

```text
CreditPolicy

PaymentPolicy

ReceivablePolicy

PayablePolicy

CashFlowPolicy

BankPolicy
```

---

## CreditPolicy

Responsável por:

```text
Limite

Bloqueios

Análise

Risco

Garantias
```

---

## PaymentPolicy

Define:

```text
Parcelamento

Juros

Multa

Desconto

Carência
```

---

# Policies de Estoque

```text
InventoryPolicy

ReservationPolicy

ReorderPolicy

TransferPolicy
```

---

## ReservationPolicy

Define:

```text
Prioridade

Validade

Liberação

Expiração

Regras de consumo
```

---

# Policies da Produção

```text
ProductionPolicy

CapacityPolicy

SchedulingPolicy

RoutingPolicy

MaterialConsumptionPolicy
```

---

## ProductionPolicy

Responsável por definir:

```text
Ordem de execução

Prioridades

Capacidade

Recursos

Reprocessamentos
```

---

# Policies Fiscais

```text
TaxPolicy

InvoicePolicy

FiscalApprovalPolicy
```

---

## TaxPolicy

Responsável por decidir:

```text
Tributação

Alíquotas

Exceções

Retenções

Substituição Tributária
```

---

# Policies de Qualidade

```text
InspectionPolicy

ApprovalPolicy

NonConformityPolicy
```

---

# Policies de Workflow

```text
WorkflowPolicy

ApprovalWorkflowPolicy

EscalationPolicy
```

---

# Policies de Segurança

```text
PasswordPolicy

SessionPolicy

AuthenticationPolicy

AuthorizationPolicy
```

---

## PasswordPolicy

Define:

```text
Comprimento mínimo

Caracteres especiais

Expiração

Histórico

Tentativas
```

---

# Policies de IA

```text
PromptPolicy

AgentPolicy

SafetyPolicy

CostPolicy
```

---

## CostPolicy

Responsável por decidir:

```text
Modelo permitido

Limite diário

Limite mensal

Modelo premium

Modelo econômico
```

---

# Configuração

Policies poderão utilizar parâmetros vindos do módulo Configuration.

Exemplo

```text
Desconto máximo

↓

Configuration

↓

DiscountPolicy
```

Assim nenhuma regra ficará hardcoded.

---

# Composição

Policies poderão utilizar Specifications.

Exemplo

```text
DiscountPolicy

↓

CustomerHasCreditSpecification

↓

CustomerIsActiveSpecification
```

---

# Determinismo

Uma Policy deverá produzir sempre o mesmo resultado para a mesma entrada e mesma configuração.

---

# Stateless

Policies nunca armazenam estado.

Cada execução deverá ser independente.

---

# Testabilidade

Toda Policy deverá possuir testes unitários.

Casos mínimos

- cenário padrão;
- exceções;
- limites;
- configurações diferentes.

---

# Convenções

Nome

```text
<Assunto>Policy
```

Exemplos

```text
DiscountPolicy

TaxPolicy

PaymentPolicy

InventoryPolicy

ProductionPolicy

ApprovalPolicy
```

---

# Checklist

Antes de criar uma Policy verificar:

- representa uma política corporativa?
- depende de configuração?
- poderá mudar no futuro?
- não pertence a uma Entity?
- não pertence a uma Specification?
- não depende da infraestrutura?
- possui testes?

Se alguma resposta for "não", revisar a modelagem.

---

# Regras Gerais

Toda Policy deverá:

- possuir responsabilidade única;
- ser reutilizável;
- utilizar linguagem do domínio;
- ser independente da infraestrutura;
- ser configurável;
- nunca conter código específico da interface.

---

# Relação com outros componentes

```text
Aggregate

↓

Policy

↓

Specification

↓

Value Objects

↓

Resultado
```

A Policy representa a decisão.

A Specification valida condições.

O Aggregate aplica a regra.

---

# Próximo Documento

```text
009-factories.md
```