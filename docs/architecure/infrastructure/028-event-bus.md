# Infrastructure Architecture Specification
## 028 - Event Bus

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do Event Bus do OrganizeG3.

O Event Bus é responsável por transportar eventos entre os módulos da aplicação e entre sistemas externos.

Ele representa o mecanismo oficial de comunicação assíncrona da plataforma.

Nenhum módulo deverá depender diretamente de outro módulo.

Toda comunicação assíncrona ocorrerá através do Event Bus.

---

# Objetivos

O Event Bus deverá garantir:

- desacoplamento;
- escalabilidade;
- extensibilidade;
- confiabilidade;
- observabilidade;
- rastreabilidade.

---

# Arquitetura

```text
Aggregate

↓

Domain Event

↓

Outbox

↓

Dispatcher

↓

Event Bus

↓

Subscribers

↓

Application
```

---

# Responsabilidades

O Event Bus deverá:

- publicar eventos;
- localizar Subscribers;
- distribuir mensagens;
- controlar falhas;
- registrar métricas;
- permitir evolução dos contratos.

Nunca executar regras de negócio.

---

# Componentes

O Event Bus será composto por:

```text
Publisher

Subscriber

Event Registry

Message Serializer

Message Envelope

Retry Policy

Metrics

Tracing
```

---

# Publisher

Responsável por:

```text
Receber Evento

↓

Serializar

↓

Enviar ao Broker
```

Nunca conhecer Consumers.

---

# Subscriber

Responsável por:

```text
Receber Evento

↓

Desserializar

↓

Executar Handler
```

Cada Subscriber deverá possuir responsabilidade única.

---

# Event Registry

Responsável por registrar:

```text
Nome

Versão

Tipo

Payload

Subscribers
```

Permitindo descoberta automática.

---

# Message Envelope

Todo evento será transportado em um Envelope.

Campos mínimos

```text
MessageId

EventName

Version

CorrelationId

CausationId

TenantId

OccurredAt

Payload

Metadata
```

---

# MessageId

Cada mensagem possuirá um UUID.

Nunca reutilizar identificadores.

---

# Event Name

Formato

```text
<Context>.<Aggregate>.<Action>
```

Exemplos

```text
CRM.Customer.Created

Sales.Order.Approved

Inventory.Stock.Reserved

Financial.Payment.Received

Production.Order.Started
```

---

# Version

Todo evento deverá possuir:

```text
Version
```

Exemplo

```text
1

2

3
```

Permitindo compatibilidade futura.

---

# Payload

O Payload conterá apenas dados necessários.

Nunca incluir:

```text
Repositories

Entities

Services

Connections
```

---

# Metadata

Campos

```text
Application

Environment

Hostname

UserId

TenantId

CorrelationId

CausationId

Timestamp
```

---

# Fluxo

```text
Aggregate

↓

Domain Event

↓

Outbox

↓

Dispatcher

↓

Event Bus

↓

Subscriber

↓

Application Service
```

---

# Event Handlers

Cada evento poderá possuir:

```text
0

1

N
```

Subscribers.

Exemplo

```text
CustomerCreated

↓

CRM

↓

Marketing

↓

Analytics

↓

Auditoria
```

---

# Garantia de Entrega

Objetivo

```text
At-Least-Once Delivery
```

A aplicação deverá ser idempotente.

---

# Ordem

Eventos do mesmo Aggregate deverão manter ordem.

Exemplo

```text
OrderCreated

↓

OrderApproved

↓

InvoiceIssued
```

---

# Retry

Em caso de falha:

```text
Retry

↓

Backoff

↓

Dead Letter
```

---

# Dead Letter Queue

Após exceder retries:

```text
Dead Letter Queue
```

Permite análise manual.

---

# Timeout

Todo Subscriber deverá possuir timeout configurável.

Exemplo

```text
30 segundos
```

---

# Paralelismo

Eventos independentes poderão ser processados em paralelo.

Eventos do mesmo Aggregate deverão respeitar a ordem.

---

# Idempotência

Todo Subscriber deverá suportar:

```text
Reprocessamento
```

Sem produzir efeitos duplicados.

---

# Brokers Suportados

Arquitetura compatível com:

```text
RabbitMQ

Kafka

Redis Streams

Azure Service Bus

Amazon SQS

Google Pub/Sub
```

A escolha do Broker não altera a Application.

---

# Interfaces

A Application conhecerá apenas:

```text
IEventBus

IEventPublisher

IEventSubscriber
```

A implementação pertence à Infrastructure.

---

# Monitoramento

Métricas

```text
Published

Processed

Retries

Failures

Dead Letters

Latency
```

---

# Logging

Toda publicação deverá registrar:

```text
MessageId

EventName

Duration

Retries

Subscriber

CorrelationId

TenantId
```

---

# Observabilidade

Integração prevista com:

```text
OpenTelemetry

Prometheus

Grafana

Jaeger
```

---

# Segurança

Todo evento deverá validar:

```text
Tenant

Schema

Version

Integrity
```

Nunca transportar:

```text
Senha

Secrets

JWT

Private Keys
```

---

# Evolução

Eventos nunca deverão ser alterados de forma incompatível.

Sempre criar nova versão quando necessário.

---

# Organização

```text
messaging/

    event_bus/

        publisher.py

        subscriber.py

        registry.py

        serializer.py

        envelope.py

        dispatcher.py
```

---

# Testabilidade

Todo Event Bus deverá possuir testes para:

```text
Publicação

Serialização

Desserialização

Retry

Dead Letter

Subscribers

Performance
```

---

# Anti-Patterns

Nunca fazer

```text
Subscriber chamar outro Subscriber

Executar SQL diretamente

Executar Commit

Executar regra de domínio

Acoplar módulos
```

---

# Checklist

Antes de implementar verificar:

- existe Publisher?
- existe Subscriber?
- existe Envelope?
- existe Retry?
- existe Dead Letter?
- existe Versionamento?
- existe Idempotência?
- existe Observabilidade?

---

# Regras Gerais

Todo Event Bus deverá:

- ser desacoplado;
- ser idempotente;
- suportar múltiplos Brokers;
- ser altamente observável;
- ser altamente escalável;
- ser independente da tecnologia utilizada.

---

# Fluxo Completo

```text
Domain Event

↓

Outbox

↓

Dispatcher

↓

Event Bus

↓

Subscribers

↓

Application Services

↓

Integrações
```

---

# Próximo Documento

```text
029-background-workers.md
```