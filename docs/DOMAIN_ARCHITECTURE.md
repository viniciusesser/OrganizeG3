# ORGANIZEG3 PLATFORM
# Arquitetura de Domínio

> Versão: 1.0
>
> Este documento define a arquitetura oficial de domínio do OrganizeG3.
>
> Nenhuma entidade, tabela, API ou tela deverá ser implementada antes que esteja prevista neste documento.
>
> Toda alteração estrutural deverá começar por este arquivo.

---

# Objetivos

O OrganizeG3 é uma plataforma ERP industrial construída para empresas que:

- compram materiais;
- produzem sob encomenda;
- produzem em série;
- prestam serviços;
- vendem produtos;
- possuem múltiplas unidades;
- trabalham com estoque;
- possuem processos internos.

A arquitetura foi desenvolvida utilizando conceitos de:

- Domain Driven Design (DDD)
- Clean Architecture
- SOLID
- Event Driven Architecture
- CQRS (quando necessário)
- Repository Pattern
- Unit Of Work
- Specification Pattern

---

# Estrutura Geral

```
Platform

├── Identity
├── Organization
├── CRM
├── Commercial
├── Workflow
├── Production
├── Engineering
├── Inventory
├── Purchasing
├── Financial
├── Fiscal
├── Manufacturing
├── Quality
├── Maintenance
├── Documents
├── Notifications
├── Audit
├── Analytics
├── AI
├── Configuration
└── Integrations
```

Cada módulo representa um Bounded Context.

Os módulos não devem acessar diretamente o banco de outro módulo.

Toda comunicação deverá ocorrer através de:

- Domain Events
- Application Services
- Interfaces

---

# Camadas

Cada módulo seguirá exatamente esta estrutura.

```
Module

Entities

Value Objects

Aggregates

Factories

Specifications

Repositories

Services

Policies

Events

Commands

Queries

DTOs

Validators
```

Nenhuma regra de negócio deverá existir dentro da infraestrutura.

---

# Camadas Técnicas

```
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

Dependências sempre apontam para dentro.

Infrastructure nunca poderá ser utilizada diretamente pelo Domain.

---

# Bounded Contexts

## Identity

Responsável por autenticação.

Entidades

- User
- Role
- Permission
- Session
- RefreshToken
- LoginHistory

Responsabilidades

- Login
- Logout
- JWT
- MFA
- Permissões
- Auditoria de acesso

---

## Organization

Responsável pela empresa.

Entidades

- Company
- Branch
- Department
- CostCenter
- Employee

Responsabilidades

- Multiempresa
- Filiais
- Departamentos
- Estrutura organizacional

---

## CRM

Responsável pelos relacionamentos.

Entidades

- Customer

- Supplier

- Lead

- Contact

- Address

- Opportunity

Responsabilidades

- Cadastro

- Histórico

- Atendimento

- Comercial

---

## Commercial

Responsável pelas vendas.

Entidades

- Proposal

- Quotation

- SalesOrder

- Contract

- InvoiceRequest

Responsabilidades

- Orçamentos

- Propostas

- Contratos

- Pedidos

---

## Workflow

Responsável pelo Kanban.

Entidades

- Board

- Stage

- Card

- Checklist

- ChecklistItem

Responsabilidades

- Fluxos

- Etapas

- Aprovações

---

## Production

Responsável pela produção.

Entidades

- ProductionOrder

- ProductionItem

- Operation

- WorkCenter

- Machine

- Operator

Responsabilidades

- Ordens

- Produção

- Capacidade

- Apontamentos

---

## Engineering

Responsável pela engenharia.

Entidades

- Product

- ProductStructure

- BOM

- TechnicalDrawing

- Revision

Responsabilidades

- Estrutura

- Projetos

- Revisões

---

## Inventory

Responsável pelo estoque.

Entidades

- Item

- Warehouse

- Stock

- Batch

- Movement

- Reservation

Responsabilidades

- Estoque

- Localização

- Movimentações

---

## Purchasing

Responsável pelas compras.

Entidades

- PurchaseRequest

- PurchaseOrder

- SupplierQuotation

Responsabilidades

- Solicitações

- Compras

- Aprovação

---

## Financial

Responsável pelo financeiro.

Entidades

- AccountReceivable

- AccountPayable

- BankAccount

- CashFlow

- FinancialTransaction

Responsabilidades

- Recebimentos

- Pagamentos

- Fluxo de Caixa

---

## Fiscal

Responsável pela tributação.

Entidades

- TaxRule

- FiscalDocument

- CFOP

- NCM

Responsabilidades

- Impostos

- Documentos fiscais

---

## Manufacturing

Responsável pelo processo fabril.

Entidades

- Routing

- OperationSequence

- Resource

- ProductionCalendar

Responsabilidades

- Sequenciamento

- Roteiros

---

## Quality

Responsável pela qualidade.

Entidades

- Inspection

- NonConformity

- CorrectiveAction

Responsabilidades

- Controle de qualidade

- Auditorias

---

## Maintenance

Responsável pelos ativos.

Entidades

- Equipment

- MaintenanceOrder

- PreventivePlan

Responsabilidades

- Manutenção

- Equipamentos

---

## Documents

Responsável pelos arquivos.

Entidades

- Document

- Folder

- Version

- Attachment

Responsabilidades

- Versionamento

- Storage

- Upload

---

## Notifications

Responsável pelas mensagens.

Entidades

- Notification

- NotificationTemplate

- NotificationQueue

Responsabilidades

- Email

- WhatsApp

- Push

---

## Audit

Responsável pelos eventos.

Entidades

- AuditLog

- DomainEvent

- SystemEvent

Responsabilidades

- Auditoria

- Histórico

- Rastreabilidade

---

## Analytics

Responsável pelos indicadores.

Entidades

- Dashboard

- KPI

- Report

Responsabilidades

- Indicadores

- BI

- Métricas

---

## AI

Responsável pela Inteligência Artificial.

Responsabilidades

- Assistente

- Automações

- Sugestões

- Previsões

- Classificações

- Geração de documentos

---

## Configuration

Responsável pelas parametrizações.

Entidades

- Parameter

- Sequence

- Numbering

- Theme

- FeatureFlag

Responsabilidades

- Configurações

- Numerações

- Temas

---

## Integrations

Responsável pelas integrações externas.

Integrações previstas

- Supabase

- WhatsApp

- Email

- Google

- Microsoft

- APIs de transporte

- APIs bancárias

- APIs fiscais

---

# Comunicação

Os módulos nunca conversam diretamente.

Sempre:

```
Domain Event

↓

Application Service

↓

Repository

↓

Infrastructure
```

---

# Banco de Dados

Cada agregado possuirá suas próprias tabelas.

Nenhuma tabela poderá conter responsabilidade pertencente a outro agregado.

---

# Regras Gerais

Toda entidade deverá possuir:

- UUID

- Tenant

- Auditoria

- Versionamento

- Soft Delete

- Controle de concorrência

- Datas UTC

---

# Objetivo Final

O OrganizeG3 deverá ser capaz de atender pequenas, médias e grandes empresas industriais, mantendo isolamento entre módulos, alta escalabilidade e facilidade de manutenção.