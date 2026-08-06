# Infrastructure Architecture Specification
## 025 - Database Session

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do gerenciamento de sessões de banco de dados do OrganizeG3.

Toda conexão com SQLite, PostgreSQL e Supabase deverá seguir exatamente este padrão.

Nenhuma classe da aplicação poderá criar conexões diretamente.

---

# Responsabilidade

O módulo Database Session será responsável por:

- criar Engines;
- criar Session Factory;
- gerenciar Connection Pool;
- controlar transações;
- executar Health Checks;
- fornecer Sessions para o Unit Of Work;
- encerrar conexões corretamente.

---

# Arquitetura

```text
Application

↓

Unit Of Work

↓

Database Session

↓

Async Engine

↓

Connection Pool

↓

Database
```

---

# Tecnologias

ORM

```text
SQLAlchemy 2.x
```

Sessões

```text
AsyncSession
```

Engine

```text
AsyncEngine
```

Drivers

SQLite

```text
aiosqlite
```

PostgreSQL

```text
asyncpg
```

---

# Componentes

O módulo será composto por:

```text
Engine Factory

Session Factory

Database Manager

Health Check

Retry Policy

Configuration

Lifecycle
```

---

# Database Manager

Responsável por:

- criar Engine;
- criar Session Factory;
- fornecer Sessions;
- executar Health Checks;
- encerrar recursos.

Será Singleton por processo.

---

# Engine

Existirá apenas um Engine por banco.

Exemplo

```text
Application

↓

DatabaseManager

↓

AsyncEngine
```

Nunca criar Engines por requisição.

---

# Session Factory

Será criada apenas uma vez.

Tipo

```python
async_sessionmaker
```

Toda Session será criada através dela.

---

# Session

Cada Unit Of Work utilizará uma Session exclusiva.

Fluxo

```text
Request

↓

Unit Of Work

↓

AsyncSession

↓

Dispose
```

Nunca compartilhar Sessions entre Threads.

---

# Dependency Injection

A Session será fornecida por DI.

Fluxo

```text
DatabaseManager

↓

Session Factory

↓

AsyncSession

↓

Repository
```

---

# Ciclo de Vida

```text
Criar Session

↓

Executar Operações

↓

Commit

↓

Rollback (se necessário)

↓

Close
```

Sempre liberar recursos.

---

# Connection Pool

PostgreSQL utilizará Pool.

Configurações padrão

```text
Pool Size

10
```

```text
Max Overflow

20
```

```text
Pool Timeout

30 segundos
```

```text
Pool Recycle

1800 segundos
```

Os valores poderão ser configuráveis.

---

# SQLite

SQLite não utilizará Pool tradicional.

Será utilizada configuração específica para acesso local.

Objetivos

```text
Baixa Latência

Compatibilidade

Offline
```

---

# Retry

Falhas transitórias poderão utilizar Retry.

Exemplos

```text
Timeout

Perda temporária

Conexão interrompida
```

Nunca repetir:

```text
Constraint Errors

Validation Errors

Integrity Errors
```

---

# Health Check

O módulo deverá disponibilizar:

```text
IsHealthy()

Ping()

Latency()

Database Version()

Pool Status()
```

---

# Health Query

Consulta padrão

```sql
SELECT 1
```

Executada utilizando a Session.

---

# Timeout

Toda operação deverá possuir timeout.

Exemplo

```text
30 segundos
```

Configurável.

---

# Logging

Toda abertura de Session poderá registrar:

```text
CorrelationId

TenantId

Database

Duration

Pool Usage
```

Nunca registrar credenciais.

---

# Configuração

A configuração será obtida através de:

```text
Settings

↓

DatabaseManager
```

Nunca utilizar valores hardcoded.

---

# Ambientes

Development

```text
SQLite

ou

PostgreSQL Local
```

Production

```text
PostgreSQL
```

Offline

```text
SQLite
```

---

# Multi-Tenant

Toda Session deverá respeitar:

```text
Tenant Context
```

Os filtros serão aplicados pelos Repositories.

Nunca pela Session.

---

# Transações

A Session nunca decidirá quando executar Commit.

Essa responsabilidade pertence ao:

```text
Unit Of Work
```

---

# Rollback

Sempre executar Rollback em caso de:

```text
Exception

Timeout

Concurrency Error

Database Error
```

---

# Fechamento

Toda Session deverá ser encerrada.

Fluxo

```text
Close()

↓

Dispose()

↓

Liberar Conexão
```

Nunca deixar conexões abertas.

---

# Shutdown

Durante o encerramento da aplicação:

```text
Dispose Engine

↓

Encerrar Pool

↓

Liberar Recursos
```

---

# Startup

Durante inicialização:

```text
Carregar Configuração

↓

Criar Engine

↓

Criar Session Factory

↓

Executar Health Check
```

---

# Dependency Graph

```text
Settings

↓

DatabaseManager

↓

AsyncEngine

↓

Session Factory

↓

Repositories

↓

Unit Of Work
```

---

# Concorrência

Cada Request possuirá:

```text
Uma Session
```

Nunca compartilhar Session entre:

```text
Threads

Workers

Tasks Independentes
```

---

# Context Manager

Sempre utilizar:

```python
async with
```

Exemplo

```python
async with session.begin():
    ...
```

Evitar gerenciamento manual quando possível.

---

# Segurança

Nunca registrar:

```text
Connection String

Senha

Token

Secrets
```

Nos logs.

---

# Organização

Estrutura

```text
database/

    session.py

    manager.py

    engine.py

    configuration.py

    health.py

    retry.py
```

---

# Testabilidade

O módulo deverá possuir:

```text
SQLite Tests

PostgreSQL Tests

Pool Tests

Retry Tests

Shutdown Tests

Health Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Criar Engine por Request

Criar Session Global

Executar Commit automático

Executar Rollback manual fora do Unit Of Work

Compartilhar Sessions
```

---

# Checklist

Antes de implementar verificar:

- existe apenas um Engine?
- existe apenas uma Session Factory?
- cada Request cria uma Session?
- o Unit Of Work controla Commit?
- há Health Check?
- há Shutdown correto?
- há testes?

---

# Regras Gerais

O módulo Database Session deverá:

- criar apenas um Engine;
- criar apenas uma Session Factory;
- fornecer AsyncSession;
- suportar SQLite e PostgreSQL;
- respeitar Dependency Injection;
- ser altamente testável;
- liberar corretamente todos os recursos.

---

# Fluxo Completo

```text
Startup

↓

Settings

↓

DatabaseManager

↓

AsyncEngine

↓

Session Factory

↓

Unit Of Work

↓

Repository

↓

Database

↓

Shutdown
```

---

# Próximo Documento

```text
026-alembic-migrations.md
```