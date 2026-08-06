# Infrastructure Architecture Specification
## 038 - Sync Queue

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial da Sync Queue do OrganizeG3.

A Sync Queue é responsável por registrar todas as alterações realizadas localmente antes que sejam sincronizadas com o servidor.

Ela representa o mecanismo central da estratégia **Offline First**.

Nenhuma alteração realizada no banco local poderá ser enviada diretamente para a API.

Toda alteração deverá passar obrigatoriamente pela Sync Queue.

---

# Objetivos

A Sync Queue deverá garantir:

- persistência das alterações;
- processamento ordenado;
- recuperação após falhas;
- sincronização incremental;
- auditoria;
- idempotência.

---

# Arquitetura

```text
Command

↓

SQLite

↓

Commit

↓

Sync Queue

↓

Synchronization Engine

↓

API

↓

PostgreSQL
```

---

# Responsabilidades

A Sync Queue deverá:

- registrar operações;
- armazenar payloads;
- controlar status;
- controlar retries;
- controlar prioridade;
- fornecer lote para sincronização.

Nunca executar sincronização diretamente.

---

# Estrutura Física

Tabela

```text
sync_queue
```

---

# Estrutura

Campos obrigatórios

```text
id

tenant_id

device_id

table_name

record_id

operation

payload

version

status

priority

retry_count

created_at

updated_at

processed_at

correlation_id

causation_id

synchronization_id
```

---

# Id

Tipo

```text
UUID v4
```

Identificador único da operação.

---

# Tenant

Toda operação deverá possuir:

```text
tenant_id
```

Nunca misturar registros de empresas diferentes.

---

# Device

Cada alteração será vinculada ao:

```text
device_id
```

Permitindo rastrear a origem.

---

# Table Name

Nome da tabela alterada.

Exemplo

```text
customers

products

sales_orders

inventory_movements
```

---

# Record Id

Identificador do registro alterado.

Tipo

```text
UUID
```

---

# Operation

Operações suportadas

```text
INSERT

UPDATE

DELETE

RESTORE
```

---

# Payload

Formato

```text
JSON
```

O Payload deverá conter apenas os campos alterados.

Exemplo

```json
{
  "name": "Cliente A",
  "email": "cliente@email.com"
}
```

---

# Version

Cada operação possuirá:

```text
version
```

Utilizada para:

```text
Concorrência

Sincronização

Resolução de Conflitos
```

---

# Status

Valores possíveis

```text
Pending

Processing

Completed

Failed

Cancelled

DeadLetter
```

---

# Pending

Operação aguardando sincronização.

---

# Processing

Operação atualmente sendo enviada.

---

# Completed

Operação sincronizada com sucesso.

---

# Failed

Falha temporária.

Entrará na política de Retry.

---

# Cancelled

Operação cancelada pelo sistema.

---

# DeadLetter

Falha permanente.

Necessita intervenção.

---

# Prioridade

Valores

```text
Critical

High

Normal

Low
```

---

# Retry Count

Campo

```text
retry_count
```

Incrementado automaticamente.

---

# Retry Policy

Utilizar:

```text
Exponential Backoff
```

Sequência

```text
5 s

10 s

20 s

40 s

80 s
```

---

# Lote

O Synchronization Engine deverá consumir operações em lote.

Exemplo

```text
100 registros
```

Configurável.

---

# Ordenação

A fila deverá respeitar:

```text
CreatedAt

↓

Priority

↓

Dependencies
```

---

# Dependências

Nunca sincronizar:

```text
Pedido

↓

Antes do Cliente
```

A ordem deverá respeitar dependências entre entidades.

---

# Idempotência

Uma operação nunca poderá ser aplicada duas vezes.

Cada operação será identificada por:

```text
SynchronizationId

+

RecordId

+

Version
```

---

# Compressão

Lotes grandes poderão ser comprimidos.

Formatos

```text
GZIP

Zstandard
```

---

# Criptografia

Toda comunicação utilizará:

```text
TLS
```

Quando necessário:

```text
AES-256
```

---

# Limpeza

Após sincronização:

```text
Completed

↓

Retenção

↓

Remoção
```

Período padrão

```text
30 dias
```

Configurável.

---

# Recuperação

Após desligamento inesperado:

```text
Sync Queue

↓

Recuperação

↓

Retomar processamento
```

Sem perda de dados.

---

# Auditoria

Registrar

```text
SynchronizationId

DeviceId

Operation

Status

Retries

Duration

CorrelationId
```

---

# Logging

Campos

```text
Queue Size

Operation

Table

Status

Duration

Retries
```

---

# Métricas

Registrar

```text
Pending

Completed

Failed

Retries

DeadLetter

Average Queue Time
```

---

# Health Check

Informar

```text
Queue Size

Oldest Record

Retries

Dead Letters

Worker Status
```

---

# Organização

```text
synchronization/

    queue/

        model.py

        repository.py

        dispatcher.py

        cleanup.py

        retry.py

        metrics.py
```

---

# Testabilidade

A Sync Queue deverá possuir:

```text
Insert Tests

Retry Tests

Recovery Tests

Ordering Tests

Concurrency Tests

Performance Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Enviar alterações diretamente

Ignorar Retry

Ignorar Dependências

Excluir registros imediatamente

Compartilhar fila entre Tenants
```

---

# Checklist

Antes de implementar verificar:

- utiliza UUID?
- possui Status?
- possui Retry?
- respeita Ordenação?
- respeita Dependências?
- suporta Recuperação?
- possui Auditoria?
- possui Testes?

---

# Regras Gerais

Toda Sync Queue deverá:

- ser persistente;
- ser idempotente;
- suportar Retry;
- respeitar ordenação;
- respeitar Multi-Tenant;
- permitir recuperação;
- ser altamente observável.

---

# Fluxo Completo

```text
Command

↓

SQLite

↓

Commit

↓

Sync Queue

↓

Synchronization Engine

↓

API

↓

PostgreSQL

↓

Completed
```

---

# Próximo Documento

```text
039-delta-synchronization.md
```