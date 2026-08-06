# Domain Model Specification
## 001 - Domain Overview

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura do Domínio do OrganizeG3.

Ele representa a principal referência para todo o desenvolvimento do sistema.

Todo código implementado deverá obedecer às definições contidas nesta documentação.

Caso exista divergência entre o código e este documento, este documento possui prioridade.

---

# O que é o Domínio?

O Domínio representa as regras de negócio da aplicação.

Ele descreve como a empresa funciona.

O Domínio não conhece:

- Banco de Dados
- SQLAlchemy
- PostgreSQL
- SQLite
- FastAPI
- PySide6
- Qt
- Supabase
- Redis
- APIs externas
- Interface gráfica

O Domínio conhece apenas regras de negócio.

---

# Objetivos

O Domínio deve ser:

- puro;
- independente;
- testável;
- desacoplado;
- determinístico;
- reutilizável.

Nenhuma tecnologia poderá influenciar o domínio.

---

# Arquitetura

O OrganizeG3 utilizará Domain Driven Design.

A estrutura será:

```text
Application

↓

Domain

↓

Infrastructure
```

O fluxo sempre será:

```text
UI

↓

Application

↓

Domain

↓

Infrastructure
```

Nunca:

```text
UI

↓

Banco de Dados
```

---

# Camadas

## Domain

Responsável por:

- regras;
- entidades;
- agregados;
- serviços;
- políticas;
- eventos.

Não conhece infraestrutura.

---

## Application

Responsável por:

- Commands;
- Queries;
- Handlers;
- DTOs;
- Casos de Uso.

Conhece o domínio.

Não conhece SQL.

---

## Infrastructure

Responsável por:

- Banco;
- API;
- Email;
- Storage;
- Cache;
- Filas;
- Integrações.

Conhece o domínio.

Nunca contém regras de negócio.

---

## Presentation

Responsável por:

Desktop

Web

Mobile

API

CLI

Não possui regra de negócio.

---

# Bounded Contexts

O OrganizeG3 será dividido em Contextos.

Cada contexto representa um domínio independente.

Os contextos iniciais serão:

```text
Identity

Organization

CRM

Sales

Purchasing

Inventory

Manufacturing

Production

Projects

Financial

Fiscal

Quality

Maintenance

Documents

Workflow

Automation

AI

Synchronization

Configuration

Notifications

Audit

Reporting
```

Cada contexto possui:

- linguagem própria;
- regras próprias;
- eventos próprios;
- agregados próprios.

---

# Comunicação

Os contextos nunca acessam diretamente os dados uns dos outros.

Toda comunicação ocorrerá através de:

```text
Commands

Events

Queries
```

---

# Aggregate

Um Aggregate representa um conjunto consistente de regras.

Todo Aggregate possui:

- Root;
- Entities;
- Value Objects;
- Events;
- Policies.

Somente o Aggregate Root poderá ser acessado externamente.

---

# Entity

Uma Entity possui identidade.

Exemplos:

```text
Customer

SalesOrder

Invoice

ProductionOrder

PurchaseOrder

Product

Employee
```

---

# Value Object

Um Value Object não possui identidade.

Exemplos:

```text
Money

Address

Email

Phone

Percentage

CPF

CNPJ

Dimensions

Color

Coordinates
```

---

# Domain Events

Sempre que algo importante acontecer, um Domain Event será publicado.

Exemplos:

```text
CustomerCreated

SalesOrderApproved

InvoiceAuthorized

PaymentReceived

MaterialConsumed

ProductionFinished
```

Eventos representam fatos.

Nunca comandos.

---

# Domain Services

Quando uma regra não pertence a uma única entidade, ela deverá ser implementada como Domain Service.

Exemplos:

```text
PriceCalculator

TaxCalculator

ProductionScheduler

StockReservation

CommissionCalculator
```

---

# Specifications

Regras reutilizáveis deverão utilizar Specifications.

Exemplos:

```text
CustomerCanBuySpecification

MaterialAvailableSpecification

CreditLimitSpecification

InvoiceCanBeCancelledSpecification
```

---

# Policies

Policies representam regras corporativas.

Exemplos:

```text
DiscountPolicy

PaymentPolicy

InventoryPolicy

ApprovalPolicy

ProductionPolicy
```

---

# Factories

Objetos complexos deverão ser criados através de Factories.

Nunca utilizar construtores gigantes.

Exemplos:

```text
SalesOrderFactory

ProductionOrderFactory

InvoiceFactory
```

---

# Regras Gerais

Todo Aggregate deverá:

- proteger seus invariantes;
- publicar eventos;
- impedir estados inválidos;
- ser independente da infraestrutura;
- possuir testes unitários.

---

# Próximo Documento

```text
002-aggregate-design.md
```