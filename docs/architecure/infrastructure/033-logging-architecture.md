# Infrastructure Architecture Specification
## 033 - Logging Architecture

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial de Logging do OrganizeG3.

Todo log produzido pela plataforma deverá seguir exatamente esta especificação.

O objetivo é garantir rastreabilidade completa de qualquer operação executada no sistema.

---

# Objetivos

O sistema de Logging deverá garantir:

- rastreabilidade;
- observabilidade;
- auditoria técnica;
- diagnóstico rápido;
- suporte à produção;
- integração com ferramentas externas.

---

# Arquitetura

```text
Application

↓

Logger Interface

↓

Logging Provider

↓

Console

Arquivo

OpenTelemetry

ELK

Loki
```

---

# Filosofia

Logs deverão responder rapidamente:

```text
Quem?

Quando?

Onde?

O quê?

Quanto tempo?

Resultado?

Erro?
```

---

# Responsabilidades

O sistema de Logging deverá:

- registrar eventos técnicos;
- registrar exceções;
- registrar performance;
- registrar integrações;
- registrar infraestrutura.

Nunca substituir Auditoria.

Nunca substituir Domain Events.

---

# Tecnologias

Implementação inicial

```text
structlog
```

Backend

```text
Python Logging
```

Formato

```text
JSON
```

---

# Estrutura

Todo log deverá possuir:

```text
Timestamp

Level

Message

CorrelationId

TenantId

UserId

Application

Module

Class

Method

Duration

Environment
```

---

# CorrelationId

Todo log deverá possuir:

```text
CorrelationId
```

Permitindo rastrear toda uma operação.

Exemplo

```text
HTTP Request

↓

Command

↓

Repository

↓

SQL

↓

Outbox

↓

Worker
```

Mesmo CorrelationId.

---

# CausationId

Quando houver eventos encadeados:

```text
CorrelationId

↓

CausationId
```

Permitindo rastrear toda a cadeia.

---

# Tenant

Sempre registrar

```text
TenantId
```

Quando aplicável.

---

# User

Sempre registrar

```text
UserId
```

Quando disponível.

Nunca registrar:

```text
Senha

JWT

Refresh Token
```

---

# Níveis

Utilizar apenas:

```text
TRACE

DEBUG

INFO

WARNING

ERROR

CRITICAL
```

---

# TRACE

Utilizado para:

```text
Fluxo detalhado

Diagnóstico profundo
```

Desabilitado em produção.

---

# DEBUG

Utilizado para:

```text
Desenvolvimento

Testes

Diagnóstico
```

---

# INFO

Utilizado para:

```text
Inicialização

Login

Logout

Backup

Importação

Exportação

Eventos importantes
```

---

# WARNING

Utilizado para:

```text
Timeout

Retry

Cache Miss

Configuração

Uso elevado
```

---

# ERROR

Utilizado para:

```text
Exceções

Falhas

Integrações

Banco

Workers
```

---

# CRITICAL

Utilizado apenas para:

```text
Falha geral

Banco indisponível

Corrupção

Perda de dados

Inicialização impossível
```

---

# Campos Obrigatórios

Todo log deverá possuir:

```text
timestamp

level

message

correlation_id

application

environment
```

---

# Campos Opcionais

```text
tenant_id

user_id

branch_id

request_id

duration

memory

cpu

host

worker

job_id
```

---

# Logs HTTP

Registrar:

```text
Método

URL

Status

Tempo

IP

User-Agent

CorrelationId
```

Nunca registrar corpo contendo dados sensíveis.

---

# Logs Database

Registrar

```text
Repository

Query Time

Rows

Retries

Timeout

Database
```

Nunca registrar SQL com dados confidenciais.

---

# Logs Workers

Registrar

```text
Worker

JobId

Queue

Duration

Retries

Result
```

---

# Logs Cache

Registrar

```text
Operation

Key

Provider

Hit

Miss

Duration
```

---

# Logs Storage

Registrar

```text
Upload

Download

Delete

Provider

FileId

Size
```

---

# Logs IA

Registrar

```text
Provider

Model

Prompt Tokens

Completion Tokens

Latency

Cost (quando disponível)
```

Nunca registrar prompts confidenciais sem autorização.

---

# Logs Segurança

Registrar

```text
Login

Logout

Falha Login

Permissão Negada

Token Expirado

Tentativas Suspeitas
```

---

# Exceções

Toda exceção deverá registrar:

```text
Tipo

Mensagem

Stack Trace

CorrelationId

Contexto
```

---

# Stack Trace

Registrar apenas em:

```text
ERROR

CRITICAL
```

---

# Performance

Registrar operações acima do limite.

Exemplo

```text
HTTP > 2 segundos

↓

WARNING
```

```text
SQL > 500 ms

↓

WARNING
```

---

# Rotação

Arquivos deverão possuir:

```text
Rotação diária

↓

Compressão

↓

Retenção
```

Padrão

```text
30 dias
```

Configurável.

---

# Estrutura Física

```text
logs/

    api/

    desktop/

    workers/

    scheduler/

    synchronization/

    audit/

    archive/
```

---

# Observabilidade

Integração prevista

```text
OpenTelemetry

Grafana

Prometheus

Loki

ELK

Jaeger
```

---

# Métricas

Registrar

```text
Logs/minuto

Errors

Warnings

Exceptions

Latency

Throughput
```

---

# Segurança

Nunca registrar:

```text
Senha

JWT

Refresh Token

Connection String

API Keys

Private Keys

Dados Bancários

Cartões
```

---

# Multi-Tenant

Todo log deverá respeitar:

```text
TenantId
```

Permitindo filtros por empresa.

---

# Organização

```text
logging/

    configuration.py

    formatter.py

    context.py

    middleware.py

    filters.py

    handlers.py

    metrics.py
```

---

# Testabilidade

O sistema deverá possuir testes para:

```text
Contexto

CorrelationId

Formatação

JSON

Performance

Rotação

Filtros
```

---

# Anti-Patterns

Nunca fazer

```text
print()

Logs sem contexto

Logs duplicados

Logs sensíveis

Stack Trace em INFO

Silenciar exceções
```

---

# Checklist

Antes de registrar um log verificar:

- possui CorrelationId?
- possui nível correto?
- contém informação sensível?
- possui contexto suficiente?
- será útil em produção?

---

# Regras Gerais

Todo log deverá:

- ser estruturado;
- utilizar JSON;
- possuir CorrelationId;
- possuir contexto;
- nunca conter dados sensíveis;
- permitir rastreabilidade completa.

---

# Fluxo Completo

```text
Request

↓

Middleware

↓

Contexto

↓

Logger

↓

Provider

↓

Arquivo / Console / Observabilidade
```

---

# Próximo Documento

```text
034-configuration-architecture.md
```