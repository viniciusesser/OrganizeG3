# Infrastructure Architecture Specification
## 027 - Outbox Pattern

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a implementação oficial do Outbox Pattern do OrganizeG3.

O Outbox Pattern garante consistência entre o banco de dados e os eventos publicados pelo sistema.

Nenhum evento deverá ser enviado diretamente para filas, brokers ou integrações externas durante uma transação.

Todos os eventos deverão passar obrigatoriamente pela Outbox.

---

# Problema

Considere o fluxo:

```text
Criar Pedido

↓

Salvar Banco

↓

Enviar Evento
```

Caso ocorra uma falha após salvar o banco e antes do envio do evento:

```text
Pedido salvo

↓

Evento perdido
```

O sistema ficará inconsistente.

---

# Solução

Utilizar Outbox Pattern.

Fluxo

```text
Aggregate

↓

Domain Event

↓

Commit

↓

Outbox Table

↓

Worker

↓

Message Bus

↓

Consumers
```

---

# Objetivos

O Outbox deverá garantir:

- consistência;
- confiabilidade;
- reprocessamento;
- auditoria;
- idempotência;
- desacoplamento.

---

# Arquitetura

```text
Aggregate

↓

Domain Event

↓

Repository

↓

Unit Of Work

↓

Commit

↓

Outbox

↓

Dispatcher

↓

Broker

↓

Consumers
```

---

# Responsabilidades

O Outbox será responsável por:

- armazenar eventos;
- controlar publicação;
- controlar retries;
- registrar falhas;
- garantir entrega.

Nunca executar regras de domínio.

---

# Fluxo Completo

```text
Command

↓

Handler

↓

Aggregate

↓

Domain Event

↓

Commit

↓

Outbox Table

↓

Worker

↓

Publish

↓

Success

↓

Processed
```

---

# Estrutura da Tabela

Tabela

```text
outbox_events
```

Campos mínimos

```text
id

tenant_id

aggregate_type

aggregate_id

event_name

payload

occurred_at

created_at

processed_at

retry_count

status

correlation_id

causation_id

version
```

---

# Status

Valores possíveis

```text
Pending

Processing

Published

Failed

DeadLetter
```

---

# Pending

Evento recém gravado.

Ainda não processado.

---

# Processing

Evento sendo publicado.

Utilizado para evitar concorrência.

---

# Published

Evento entregue com sucesso.

Não deverá ser reenviado.

---

# Failed

Publicação falhou.

Entrará na política de Retry.

---

# DeadLetter

Após exceder o número máximo de tentativas.

Será enviado para análise.

---

# Payload

O Payload deverá conter:

```text
Nome do Evento

Versão

Dados

Metadata
```

Formato

```text
JSON
```

---

# Metadata

Campos

```text
CorrelationId

CausationId

TenantId

UserId

OccurredAt

Application

Version
```

---

# Dispatcher

Responsável por:

```text
Buscar Pending

↓

Marcar Processing

↓

Publicar

↓

Atualizar Status
```

---

# Worker

O Dispatcher será executado por Workers.

Nunca pela requisição HTTP.

---

# Frequência

Configuração padrão

```text
1 segundo
```

Configurável.

---

# Retry

Eventos com falha poderão ser reenviados.

Exemplo

```text
Tentativa 1

↓

Falha

↓

Tentativa 2

↓

Falha

↓

Tentativa 3

↓

Publicado
```

---

# Retry Policy

Utilizar

```text
Exponential Backoff
```

Exemplo

```text
5 s

10 s

20 s

40 s

80 s
```

---

# Retry Count

Campo

```text
retry_count
```

Incrementado automaticamente.

---

# Limite

Após:

```text
10 tentativas
```

Evento deverá ir para:

```text
Dead Letter
```

Configurável.

---

# Idempotência

O Dispatcher deverá garantir:

```text
Mesmo evento

↓

Nunca publicado duas vezes
```

---

# Ordenação

Eventos do mesmo Aggregate deverão respeitar a ordem de criação.

```text
OrderCreated

↓

OrderApproved

↓

InvoiceIssued
```

Nunca inverter a sequência.

---

# Concorrência

Workers diferentes poderão publicar eventos distintos.

Nunca o mesmo evento simultaneamente.

---

# Locks

Utilizar:

```text
Optimistic Lock

ou

Database Lock
```

Para evitar dupla publicação.

---

# Auditoria

Registrar:

```text
Dispatcher

Worker

Duration

Retries

PublishedAt

Exception
```

---

# Segurança

Payload nunca deverá conter:

```text
Senha

Token

Secrets

Connection String
```

---

# Versionamento

Todo evento deverá possuir:

```text
Version
```

Permitindo evolução do contrato.

---

# Limpeza

Eventos publicados poderão ser:

```text
Arquivados

↓

Removidos
```

Após política de retenção.

Exemplo

```text
180 dias
```

---

# Monitoramento

Métricas

```text
Pending

Published

Failed

DeadLetter

Retries

Latency
```

---

# Alertas

Gerar alerta quando:

```text
Fila crescendo

Dead Letter

Retry elevado

Dispatcher parado
```

---

# Integrações

Após publicação:

```text
RabbitMQ

Kafka

Redis Streams

Azure Service Bus

Amazon SQS

Webhooks
```

Todos através de Interfaces.

---

# Organização

Estrutura

```text
messaging/

    outbox/

        dispatcher.py

        worker.py

        repository.py

        model.py

        retry.py

        metrics.py
```

---

# Testabilidade

Todo Outbox deverá possuir testes para:

```text
Persistência

Retry

Dead Letter

Ordenação

Idempotência

Concorrência

Performance
```

---

# Anti-Patterns

Nunca fazer

```text
Enviar evento antes do Commit

Publicar diretamente do Aggregate

Executar publicação na Request

Ignorar Retry

Ignorar Dead Letter
```

---

# Checklist

Antes de implementar verificar:

- evento é gravado antes da publicação?
- existe Dispatcher?
- existe Retry?
- existe Dead Letter?
- existe Idempotência?
- existe Auditoria?
- existe Monitoramento?

---

# Regras Gerais

Toda implementação do Outbox deverá:

- garantir consistência;
- suportar Retry;
- suportar Dead Letter;
- ser idempotente;
- ser auditável;
- ser monitorável;
- ser independente do Broker.

---

# Fluxo Completo

```text
Aggregate

↓

Domain Event

↓

Unit Of Work

↓

Commit

↓

Outbox Table

↓

Dispatcher

↓

Message Broker

↓

Consumers

↓

Integrações
```

---

# Próximo Documento

```text
028-event-bus.md
```