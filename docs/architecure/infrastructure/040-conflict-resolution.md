# Infrastructure Architecture Specification
## 040 - Conflict Resolution

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial de Resolução de Conflitos do OrganizeG3.

O Conflict Resolution é responsável por detectar, classificar e resolver alterações concorrentes realizadas em diferentes dispositivos ou clientes.

Seu objetivo é garantir que a sincronização mantenha a consistência dos dados sem perda de informações.

---

# Objetivos

O sistema de resolução de conflitos deverá garantir:

- consistência;
- previsibilidade;
- auditabilidade;
- rastreabilidade;
- recuperação;
- intervenção manual quando necessária.

---

# Definição

Existe um conflito quando:

```text
Dois ou mais dispositivos

↓

Alteram

↓

O mesmo registro

↓

Antes da sincronização
```

---

# Arquitetura

```text
Desktop A

↓

SQLite

↓

Sync Queue

↓

API

↑

↓

Sync Queue

↓

SQLite

↓

Desktop B
```

---

# Responsabilidades

O Conflict Resolver deverá:

- detectar conflitos;
- classificar conflitos;
- aplicar estratégia adequada;
- registrar auditoria;
- preservar integridade.

Nunca executar regras de negócio.

---

# Tipos de Conflito

O OrganizeG3 suportará:

```text
Update vs Update

Delete vs Update

Delete vs Delete

Restore vs Delete

Insert Duplicado

Version Conflict
```

---

# Update vs Update

Exemplo

```text
Desktop A

↓

Cliente altera telefone

↓

Desktop B

↓

Cliente altera email

↓

Conflito
```

---

# Delete vs Update

Exemplo

```text
Desktop A

↓

Exclui Cliente

↓

Desktop B

↓

Edita Cliente
```

---

# Delete vs Delete

Exemplo

```text
Desktop A

↓

Excluir

↓

Desktop B

↓

Excluir
```

Não há perda de consistência.

---

# Restore vs Delete

Exemplo

```text
Desktop A

↓

Restaurar

↓

Desktop B

↓

Excluir
```

Necessita resolução.

---

# Insert Duplicado

Exemplo

```text
Mesmo Código

↓

Mesmo Documento

↓

Mesmo Tenant
```

Necessita validação.

---

# Version Conflict

O conflito será detectado quando:

```text
Version Local

≠

Version Servidor
```

---

# Estratégias

O OrganizeG3 suportará:

```text
Server Wins

Client Wins

Merge

Manual

Custom Policy
```

---

# Server Wins

Fluxo

```text
Servidor

↓

Sobrescreve Cliente
```

Utilizado para dados críticos.

---

# Client Wins

Fluxo

```text
Cliente

↓

Sobrescreve Servidor
```

Utilizado apenas quando explicitamente permitido.

---

# Merge

Campos independentes poderão ser unidos.

Exemplo

```text
Telefone

+

Email

↓

Registro Final
```

---

# Manual

Quando não existir resolução automática.

Fluxo

```text
Conflito

↓

Fila

↓

Usuário

↓

Escolha
```

---

# Policy

Cada Aggregate poderá definir sua política.

Exemplo

```text
Customer

↓

Merge
```

```text
Invoice

↓

Server Wins
```

```text
Financial Transaction

↓

Manual
```

---

# Versionamento

Todo registro utilizará:

```text
version
```

Comparação

```text
Version Local

↓

Version Remota

↓

Resolver
```

---

# Snapshot

Quando necessário:

```text
Snapshot

↓

Reconstrução

↓

Nova Sincronização
```

---

# Registro de Conflitos

Tabela

```text
sync_conflicts
```

Campos

```text
id

tenant_id

device_id

table_name

record_id

local_version

remote_version

local_payload

remote_payload

strategy

status

created_at

resolved_at

resolved_by
```

---

# Status

Valores

```text
Pending

Resolved

Ignored

Cancelled
```

---

# Payload

Armazenar:

```text
Versão Local

Versão Servidor

Diferenças
```

---

# Diferenças

O sistema deverá identificar:

```text
Campos alterados

Campos removidos

Campos adicionados
```

---

# Interface

No Desktop poderá existir tela de resolução.

Exemplo

```text
Valor Local

↓

Valor Servidor

↓

Escolha

↓

Aplicar
```

---

# Automação

Sempre que possível utilizar resolução automática.

A intervenção manual deverá ser exceção.

---

# Idempotência

Resolver o mesmo conflito duas vezes nunca deverá gerar inconsistência.

---

# Auditoria

Registrar

```text
ConflictId

Strategy

User

Device

Duration

CorrelationId

Timestamp
```

---

# Logging

Campos

```text
Conflict

Aggregate

Strategy

Duration

Result
```

---

# Métricas

Registrar

```text
Conflicts

Automatic Resolution

Manual Resolution

Average Time

Merge Success
```

---

# Health Check

Informar

```text
Pending Conflicts

Resolved Today

Average Resolution Time
```

---

# Segurança

Toda resolução deverá respeitar:

```text
Tenant

Permissões

Versionamento
```

---

# Organização

```text
synchronization/

    conflict/

        resolver.py

        detector.py

        strategies.py

        merge.py

        repository.py

        metrics.py
```

---

# Estratégias Padrão

## Cadastros

```text
Merge
```

---

## Financeiro

```text
Manual
```

---

## Fiscal

```text
Server Wins
```

---

## Estoque

```text
Version + Manual
```

---

## Produção

```text
Merge
```

---

## Workflow

```text
Merge
```

---

# Testabilidade

O Conflict Resolver deverá possuir:

```text
Update Tests

Delete Tests

Merge Tests

Manual Tests

Retry Tests

Performance Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Ignorar Version

Sobrescrever silenciosamente

Descartar alterações

Misturar Tenants

Resolver sem Auditoria
```

---

# Checklist

Antes de implementar verificar:

- detecta conflito?
- identifica estratégia?
- registra auditoria?
- suporta Merge?
- suporta resolução manual?
- possui testes?

---

# Regras Gerais

Todo Conflict Resolver deverá:

- utilizar Versionamento;
- preservar consistência;
- registrar auditoria;
- suportar múltiplas estratégias;
- respeitar Multi-Tenant;
- ser determinístico.

---

# Fluxo Completo

```text
Sync

↓

Comparar Version

↓

Existe conflito?

↓

Não

↓

Aplicar

↓

Fim

Sim

↓

Resolver

↓

Aplicar Estratégia

↓

Registrar Auditoria

↓

Sincronização Continua
```

---

# Próximo Documento

```text
041-snapshot-architecture.md
```