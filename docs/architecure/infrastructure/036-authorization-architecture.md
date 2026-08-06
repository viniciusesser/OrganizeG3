# Infrastructure Architecture Specification
## 036 - Authorization Architecture

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do sistema de Autorização do OrganizeG3.

Após a autenticação identificar o usuário, a autorização será responsável por responder:

```text
O usuário pode executar esta ação?
```

O sistema deverá suportar controle fino de permissões em todos os módulos da plataforma.

---

# Objetivos

A autorização deverá garantir:

- segurança;
- flexibilidade;
- escalabilidade;
- multi-tenant;
- auditoria;
- baixo acoplamento.

---

# Arquitetura

```text
Request

↓

Authentication

↓

Authorization

↓

Policy Engine

↓

Application

↓

Response
```

---

# Responsabilidades

A autorização deverá:

- validar permissões;
- validar políticas;
- validar Feature Flags;
- validar licenciamento;
- validar escopo;
- registrar auditoria.

Nunca executar regras de negócio.

---

# Modelo

O OrganizeG3 utilizará:

```text
RBAC

+

Claims

+

Policies

+

Feature Flags
```

---

# RBAC

Controle baseado em papéis.

Fluxo

```text
Usuário

↓

Cargo

↓

Permissões
```

---

# Claims

Cada usuário possuirá Claims.

Exemplos

```text
TenantId

BranchId

DepartmentId

RoleId

Permissions

License

Features
```

---

# Policies

Policies representam regras técnicas.

Exemplo

```text
Pode emitir NF?

↓

Policy

↓

Sim / Não
```

---

# Feature Flags

Toda funcionalidade poderá ser habilitada ou desabilitada.

Exemplos

```text
IA

OCR

Marketplace

Offline

Financeiro

BI
```

---

# Hierarquia

O sistema seguirá a hierarquia:

```text
Tenant

↓

Empresa

↓

Filial

↓

Departamento

↓

Cargo

↓

Usuário
```

---

# Permissões

Cada permissão possuirá:

```text
PermissionId

Code

Description

Module

Action
```

---

# Estrutura

Formato

```text
<Modulo>.<Recurso>.<Ação>
```

---

# Exemplos

CRM

```text
crm.customer.read

crm.customer.create

crm.customer.update

crm.customer.delete
```

---

Comercial

```text
sales.order.read

sales.order.create

sales.order.approve
```

---

Compras

```text
purchase.order.read

purchase.order.receive
```

---

Estoque

```text
inventory.product.read

inventory.stock.adjust
```

---

Produção

```text
production.order.start

production.order.finish
```

---

Financeiro

```text
financial.payment.create

financial.cash.close

financial.bank.reconcile
```

---

Fiscal

```text
fiscal.invoice.issue

fiscal.invoice.cancel
```

---

Projetos

```text
project.task.update

project.timeline.read
```

---

Workflow

```text
workflow.board.move

workflow.card.create
```

---

IA

```text
ai.chat.use

ai.embedding.generate

ai.ocr.execute
```

---

Marketplace

```text
marketplace.install

marketplace.publish

marketplace.update
```

---

# Ações

Ações padrão

```text
create

read

update

delete

approve

cancel

execute

manage

export

import
```

---

# Escopo

Uma permissão poderá possuir escopo.

Tipos

```text
Global

Tenant

Branch

Department

Own Records
```

---

# Exemplos

```text
Visualizar apenas clientes da filial.
```

---

```text
Editar apenas projetos próprios.
```

---

```text
Aprovar pedidos da empresa inteira.
```

---

# Herança

Permissões poderão ser herdadas.

Exemplo

```text
Administrador

↓

Gerente

↓

Operador
```

O nível superior poderá herdar permissões inferiores.

---

# Exceções

Permissões individuais poderão sobrescrever o cargo.

Fluxo

```text
Cargo

↓

Permissão

↓

Exceção do Usuário
```

---

# Policies

Policies poderão validar:

```text
Horário

Licença

Plano

Status

Tenant

Departamento

Filial
```

---

# Licenciamento

Toda autorização verificará:

```text
Plano

↓

Feature Flag

↓

Permissão
```

Exemplo

Plano Básico

↓

Sem IA

↓

Permissão negada.

---

# Offline

Durante operação Offline:

Permissões armazenadas localmente.

Sincronização posterior.

---

# API

Toda rota protegida deverá declarar:

```text
Permission

↓

Policy

↓

Authentication
```

---

# Desktop

Toda tela deverá declarar:

```text
Required Permission
```

Antes de abrir.

---

# PWA

Menus deverão ser montados conforme permissões.

Itens proibidos não deverão aparecer.

---

# Auditoria

Registrar

```text
Permission

Policy

Result

Tenant

User

CorrelationId

Timestamp
```

---

# Logging

Campos

```text
Permission

Module

Action

Granted

Denied

Duration
```

---

# Cache

Permissões poderão utilizar cache.

TTL configurável.

Invalidação após alteração.

---

# Multi-Tenant

Nunca permitir:

```text
Usuário

↓

Acessar outro Tenant
```

Mesmo sendo Administrador.

---

# Organização

```text
authorization/

    policies/

    permissions/

    roles/

    claims/

    feature_flags/

    evaluators/

    cache/
```

---

# Interfaces

O sistema deverá possuir:

```text
IAuthorizationService

IPermissionProvider

IPolicyEvaluator

IFeatureFlagProvider
```

---

# Testabilidade

Todo módulo deverá possuir:

```text
Permission Tests

Policy Tests

Role Tests

Claims Tests

Feature Flag Tests

Performance Tests
```

---

# Anti-Patterns

Nunca fazer

```text
if user.is_admin

Permissões hardcoded

Permissões na UI

Ignorar Tenant

Misturar autenticação e autorização
```

---

# Checklist

Antes de adicionar uma permissão verificar:

- pertence a um módulo?
- possui ação?
- possui escopo?
- suporta Tenant?
- possui testes?
- possui documentação?

---

# Regras Gerais

Todo sistema de autorização deverá:

- utilizar RBAC;
- suportar Claims;
- utilizar Policies;
- suportar Feature Flags;
- respeitar Multi-Tenant;
- registrar Auditoria;
- ser totalmente desacoplado da Application.

---

# Fluxo Completo

```text
Request

↓

Authentication

↓

Claims

↓

Roles

↓

Policies

↓

Feature Flags

↓

Authorization

↓

Application

↓

Response
```

---

# Próximo Documento

```text
037-synchronization-architecture.md
```