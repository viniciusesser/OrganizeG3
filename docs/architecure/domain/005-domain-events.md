# Domain Model Specification
## 005 - Domain Events

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial de Domain Events do OrganizeG3.

Todo evento publicado pelo sistema deverá seguir estas definições.

Os Domain Events representam fatos ocorridos dentro do domínio.

Eles são a base da arquitetura Event-Driven utilizada pelo OrganizeG3.

---

# O que é um Domain Event?

Um Domain Event representa algo que já aconteceu.

Ele descreve um fato consumado.

Exemplos

```text
Cliente criado

Pedido aprovado

Produção iniciada

Pagamento recebido

Nota fiscal autorizada
```

Eventos representam fatos.

Nunca intenções.

---

# Commands x Events

Command

```text
ApproveSalesOrder
```

Significa

```text
Aprovar pedido.
```

Ainda pode falhar.

---

Domain Event

```text
SalesOrderApproved
```

Significa

```text
O pedido foi aprovado.
```

Já aconteceu.

Nunca falha.

---

# Características

Todo Domain Event deverá ser:

```text
Imutável

Auditável

Versionado

Serializável

Rastreável
```

---

# Estrutura

Todo evento deverá possuir

```text
EventId

AggregateId

AggregateType

TenantId

OccurredAt

Version

CorrelationId

UserId

Payload
```

---

# EventId

Todo evento possuirá

```text
UUID v4
```

Nunca reutilizado.

---

# AggregateId

Indica qual Aggregate gerou o evento.

Exemplo

```text
SalesOrderId
```

---

# AggregateType

Exemplos

```text
Customer

SalesOrder

Invoice

ProductionOrder

PurchaseOrder
```

---

# Version

Cada evento possuirá sua própria versão.

Exemplo

```text
1

2

3
```

Permitindo evolução futura.

---

# CorrelationId

Todos os eventos derivados da mesma operação compartilharão o mesmo CorrelationId.

Exemplo

```text
Create Sales Order

↓

SalesOrderCreated

↓

StockReserved

↓

ProductionCreated

↓

NotificationSent
```

Todos com o mesmo CorrelationId.

---

# Payload

O Payload deverá conter apenas informações necessárias.

Exemplo

```json
{
    "sales_order_id": "...",
    "customer_id": "...",
    "status": "APPROVED"
}
```

Nunca incluir objetos completos.

Sempre utilizar referências.

---

# Imutabilidade

Eventos nunca poderão ser alterados.

Caso seja necessário corrigir alguma informação:

Publicar um novo evento.

Nunca editar o anterior.

---

# Publicação

Eventos deverão ser publicados somente pelo Aggregate Root.

Fluxo

```text
Entity

↓

Aggregate Root

↓

Domain Event

↓

Application

↓

Event Bus
```

---

# Consumo

Eventos poderão ser consumidos por:

```text
Application Layer

Automation

Notifications

Synchronization

Audit

Reporting

AI

Outros Contextos
```

Nunca diretamente pela UI.

---

# Ordem

Eventos deverão respeitar a ordem de publicação do Aggregate.

Exemplo

```text
Created

↓

Approved

↓

Executed

↓

Finished
```

Nunca

```text
Finished

↓

Created
```

---

# Persistência

Todos os Domain Events deverão ser armazenados.

Objetivos

```text
Auditoria

Replay

Sincronização

Integrações

Histórico
```

---

# Replay

O sistema deverá permitir reproduzir eventos.

Exemplo

```text
CustomerCreated

↓

CustomerUpdated

↓

CustomerArchived
```

Permite reconstruir o histórico.

---

# Versionamento

Quando o Payload mudar:

Incrementar

```text
Version
```

Nunca quebrar compatibilidade sem migração.

---

# Eventos do Sistema

Exemplos

```text
CustomerCreated

CustomerUpdated

CustomerArchived

SupplierCreated

ProductCreated

ProductUpdated

SalesOrderCreated

SalesOrderApproved

SalesOrderCancelled

PurchaseOrderCreated

PurchaseOrderApproved

ProductionStarted

ProductionFinished

InventoryReserved

InventoryReleased

InvoiceIssued

InvoiceAuthorized

InvoiceCancelled

PaymentReceived

PaymentSent

ProjectCreated

TaskCompleted

DocumentUploaded

WorkflowStarted

WorkflowFinished

AutomationExecuted

BackupCreated

SynchronizationCompleted
```

---

# Eventos Técnicos

Separados dos Domain Events.

Exemplos

```text
DatabaseConnected

ApiStarted

WorkerRunning

CacheInvalidated

EmailDelivered

WebhookExecuted
```

Esses eventos pertencem à infraestrutura.

Nunca ao domínio.

---

# Naming Convention

Sempre utilizar:

```text
Substantivo + Verbo no passado
```

Correto

```text
CustomerCreated

PaymentReceived

InvoiceAuthorized

StockReserved
```

Errado

```text
CreateCustomer

DoPayment

Invoice

Stock
```

---

# Eventos Compostos

Um único Command poderá gerar vários eventos.

Exemplo

```text
Approve Sales Order

↓

SalesOrderApproved

↓

InventoryReserved

↓

ProductionRequested

↓

CustomerNotified
```

---

# Eventos Cruzados

Bounded Contexts nunca executarão lógica diretamente.

Sempre responderão através de eventos.

Exemplo

```text
Sales

↓

SalesOrderApproved

↓

Inventory

↓

ReserveInventoryCommand

↓

InventoryReserved

↓

Production

↓

CreateProductionOrderCommand
```

---

# Integrações

Eventos poderão ser publicados para

```text
Kafka

RabbitMQ

Redis Streams

Azure Service Bus

Amazon SQS

Webhooks
```

A implementação ficará na Infrastructure.

---

# Auditoria

Todo evento deverá registrar

```text
User

Device

Tenant

Timestamp

CorrelationId

Aggregate

Version

Payload
```

---

# Segurança

Nunca incluir no Payload

```text
Senha

JWT

Refresh Token

Private Key

Secrets

Hash Interno
```

---

# Event Store

Todos os eventos poderão ser armazenados em um Event Store.

Estrutura

```text
EventId

AggregateId

AggregateType

Version

OccurredAt

Payload

Metadata
```

---

# Metadata

Todo evento poderá conter

```text
Application

Device

Platform

OS

IP

UserAgent

Locale
```

---

# Checklist

Todo Domain Event deverá

- representar um fato;
- ser imutável;
- possuir EventId;
- possuir AggregateId;
- possuir CorrelationId;
- possuir Version;
- ser serializável;
- ser auditável;
- possuir Payload mínimo.

---

# Convenções

Nunca utilizar eventos para executar regras de negócio.

As regras pertencem ao Aggregate.

Os eventos apenas comunicam que algo ocorreu.

---

# Próximo Documento

```text
006-domain-services.md
```