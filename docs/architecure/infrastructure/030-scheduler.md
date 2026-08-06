# Infrastructure Architecture Specification
## 030 - Scheduler

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do Scheduler do OrganizeG3.

O Scheduler é responsável por executar tarefas recorrentes, programadas ou condicionais da plataforma.

Ele coordena a criação de Jobs para os Background Workers.

Nunca executa processamento pesado diretamente.

Sua responsabilidade é apenas decidir:

- quando;
- o quê;
- com qual prioridade;
- em qual Worker.

---

# Objetivos

O Scheduler deverá garantir:

- automação;
- previsibilidade;
- escalabilidade;
- observabilidade;
- confiabilidade;
- rastreabilidade.

---

# Arquitetura

```text
Scheduler

↓

Schedule

↓

Job

↓

Queue

↓

Worker

↓

Resultado
```

---

# Responsabilidades

O Scheduler deverá:

- verificar agendas;
- criar Jobs;
- controlar recorrência;
- evitar duplicidade;
- respeitar prioridades;
- registrar auditoria.

Nunca deverá:

- executar regras de negócio;
- executar processamento pesado;
- acessar interface.

---

# Tipos de Agendamento

O OrganizeG3 suportará:

```text
Único

Recorrente

Intervalo

Cron

Evento

Condicional
```

---

# Agendamento Único

Executado apenas uma vez.

Exemplo

```text
Backup amanhã às 02:00
```

---

# Agendamento Recorrente

Executado periodicamente.

Exemplo

```text
Todo dia

↓

02:00
```

---

# Intervalo

Executado após determinado período.

Exemplo

```text
A cada

5 minutos

30 minutos

2 horas
```

---

# Cron

Expressões completas.

Exemplo

```text
0 2 * * *
```

---

# Evento

Disparado por condição.

Exemplo

```text
Nova sincronização

↓

Criar Snapshot
```

---

# Condicional

Executado quando determinada condição for satisfeita.

Exemplo

```text
Espaço livre < 10%

↓

Executar limpeza
```

---

# Componentes

O Scheduler será composto por:

```text
Scheduler Engine

Task Registry

Trigger

Cron Parser

Job Factory

Queue Dispatcher

Monitoring
```

---

# Scheduler Engine

Responsável por:

```text
Carregar tarefas

↓

Avaliar horários

↓

Criar Jobs
```

---

# Task Registry

Responsável por registrar todas as tarefas agendadas.

Cada tarefa possuirá:

```text
Nome

Descrição

Categoria

Trigger

Worker

Prioridade

Timeout
```

---

# Trigger

Tipos

```text
Cron

Intervalo

Evento

Manual

Condição
```

---

# Job Factory

Responsável por transformar:

```text
Schedule

↓

Job
```

---

# Queue Dispatcher

Responsável por:

```text
Enviar Job

↓

Fila Correta
```

---

# Categorias

## Sistema

```text
Backup

Health Check

Snapshots

Cleanup

Logs

Métricas
```

---

## Banco

```text
Vacuum SQLite

Analyze PostgreSQL

Reindex

Verificação de Integridade
```

---

## Sincronização

```text
Upload

Download

Merge

Snapshot

Conferência
```

---

## IA

```text
Embeddings

OCR

Resumo

Indexação

Vetorização
```

---

## Comunicação

```text
Email

WhatsApp

Push

SMS
```

---

## Licenciamento

```text
Atualizar Licenças

Verificar Assinaturas

Renovar Tokens
```

---

## Financeiro

```text
Fechamento Diário

Conciliação

Atualização Cambial
```

---

## Produção

```text
MRP

Planejamento

Atualizar Filas
```

---

# Estrutura de uma Tarefa

Toda tarefa possuirá:

```text
TaskId

TaskName

Schedule

Trigger

Enabled

Priority

Worker

Timeout

Retry

Tenant Scope
```

---

# Prioridades

Categorias

```text
Critical

High

Normal

Low

Idle
```

---

# Timeout

Toda tarefa possuirá timeout.

Exemplo

```text
5 minutos

30 minutos

2 horas
```

Configurável.

---

# Retry

Toda tarefa poderá utilizar:

```text
Retry

↓

Exponential Backoff

↓

Dead Letter
```

---

# Concorrência

Nunca permitir:

```text
Mesmo Backup

↓

Executando duas vezes
```

Utilizar Locks.

---

# Locks

Tipos

```text
Database Lock

Distributed Lock

Mutex
```

---

# Auditoria

Registrar:

```text
TaskId

ExecutionId

StartedAt

FinishedAt

Duration

Worker

Status

Retries
```

---

# Logging

Campos mínimos

```text
Task

Worker

Duration

Memory

CPU

Result
```

---

# Monitoramento

Métricas

```text
Execuções

Falhas

Tempo Médio

Timeouts

Retries

Fila
```

---

# Health Check

O Scheduler deverá informar:

```text
Última Execução

Próxima Execução

Tarefas Ativas

Falhas

Estado
```

---

# Cancelamento

Toda tarefa deverá suportar cancelamento.

Fluxo

```text
Cancel

↓

Worker

↓

Graceful Stop
```

---

# Configuração

As tarefas poderão ser:

```text
Globais

Por Tenant

Por Empresa

Por Filial
```

---

# Multi-Tenant

Cada Tenant poderá possuir:

```text
Horários

Backup

Sincronização

Configurações

Políticas
```

Independentes.

---

# Escalabilidade

O Scheduler deverá suportar:

```text
Milhares de tarefas

Centenas de Workers

Múltiplas Filas
```

---

# Organização

```text
scheduler/

    engine.py

    registry.py

    dispatcher.py

    cron.py

    triggers.py

    jobs.py

    metrics.py

    locks.py
```

---

# Testabilidade

Todo Scheduler deverá possuir:

```text
Cron Tests

Retry Tests

Timeout Tests

Lock Tests

Performance Tests

Concurrency Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Executar processamento pesado

Executar SQL diretamente

Executar regras de domínio

Executar UI

Criar Threads manualmente
```

---

# Checklist

Antes de implementar verificar:

- tarefa é recorrente?
- Worker correto?
- suporta Retry?
- suporta Timeout?
- suporta Lock?
- suporta Cancelamento?
- possui Logs?
- possui Métricas?

---

# Regras Gerais

Todo Scheduler deverá:

- apenas agendar;
- nunca executar processamento pesado;
- utilizar Workers;
- ser escalável;
- ser observável;
- ser altamente configurável.

---

# Fluxo Completo

```text
Scheduler

↓

Trigger

↓

Job

↓

Queue

↓

Worker

↓

Resultado

↓

Logs

↓

Métricas
```

---

# Próximo Documento

```text
031-storage-architecture.md
```