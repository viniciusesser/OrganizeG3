# Infrastructure Architecture Specification
## 048 - Audit Architecture

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do sistema de Auditoria do OrganizeG3.

A Auditoria é responsável por registrar permanentemente todas as operações relevantes realizadas na plataforma, permitindo rastreabilidade completa, conformidade legal, investigação de incidentes e reconstrução histórica dos eventos.

Diferentemente do Logging, a Auditoria representa o histórico oficial das ações executadas pelos usuários e pelo sistema.

---

# Objetivos

O sistema de Auditoria deverá garantir:

- rastreabilidade completa;
- integridade histórica;
- não repúdio;
- conformidade;
- investigação de incidentes;
- reconstrução de operações.

---

# Diferença entre Auditoria e Logging

Logging responde:

```text
O que aconteceu tecnicamente?
```

Auditoria responde:

```text
Quem fez?

↓

Quando fez?

↓

O que alterou?

↓

Qual era o valor anterior?

↓

Qual passou a ser o novo valor?
```

---

# Arquitetura

```text
Application

↓

Audit Service

↓

Audit Repository

↓

Audit Database

↓

Consulta

↓

Relatórios
```

---

# Responsabilidades

O sistema de Auditoria deverá:

- registrar ações;
- registrar alterações;
- registrar usuário;
- registrar contexto;
- registrar origem;
- preservar histórico.

Nunca executar regras de negócio.

---

# Eventos Auditáveis

O OrganizeG3 deverá auditar:

```text
Login

Logout

CRUD

Aprovações

Cancelamentos

Sincronizações

Backup

Importação

Exportação

Permissões

Licenciamento

Configurações

Integrações
```

---

# Eventos Não Auditáveis

Não registrar:

```text
Cache

Health Check

Telemetry

Métricas

Heartbeat

Operações temporárias
```

---

# Estrutura

Tabela

```text
audit_logs
```

Campos obrigatórios

```text
id

tenant_id

user_id

device_id

session_id

entity_name

entity_id

operation

old_values

new_values

timestamp

correlation_id

trace_id

ip_address

user_agent

application

environment
```

---

# Operações

Valores

```text
CREATE

READ

UPDATE

DELETE

RESTORE

LOGIN

LOGOUT

APPROVE

CANCEL

IMPORT

EXPORT
```

---

# Entity Name

Exemplos

```text
Customer

SalesOrder

Invoice

Product

User

Role
```

---

# Entity Id

Identificador único do registro auditado.

Tipo

```text
UUID
```

---

# Valores Anteriores

Campo

```text
old_values
```

Formato

```text
JSON
```

---

# Novos Valores

Campo

```text
new_values
```

Formato

```text
JSON
```

---

# Alterações

Sempre registrar apenas os campos alterados.

Exemplo

Antes

```json
{
  "email": "cliente@empresa.com"
}
```

Depois

```json
{
  "email": "novo@empresa.com"
}
```

---

# Usuário

Registrar

```text
UserId

Nome

Cargo
```

Nunca registrar senha.

---

# Dispositivo

Registrar

```text
DeviceId

Hostname

Sistema Operacional

Versão
```

---

# Sessão

Registrar

```text
SessionId
```

Permitindo reconstrução da atividade do usuário.

---

# Origem

Registrar

```text
Desktop

API

Worker

Scheduler

Integração

Marketplace
```

---

# Contexto

Todo registro deverá possuir:

```text
TenantId

CorrelationId

TraceId

Environment

ApplicationVersion
```

---

# Integridade

Cada registro poderá possuir:

```text
SHA-256
```

Permitindo validação futura.

---

# Imutabilidade

Registros de Auditoria nunca poderão ser alterados.

Somente:

```text
Inserção

↓

Consulta
```

Nunca:

```text
UPDATE

DELETE
```

---

# Retenção

Política padrão

```text
10 anos
```

Configurável conforme legislação.

---

# Consulta

Filtros previstos

```text
Usuário

Tenant

Data

Módulo

Entidade

Operação

Dispositivo

CorrelationId
```

---

# Exportação

Permitir exportação em:

```text
PDF

CSV

Excel

JSON
```

---

# Pesquisa

Suportar pesquisa por:

```text
EntityId

TraceId

CorrelationId

UserId
```

---

# Multi-Tenant

Toda Auditoria deverá ser isolada por:

```text
TenantId
```

Nunca permitir acesso cruzado.

---

# Segurança

Registros de Auditoria deverão possuir:

```text
Somente Leitura
```

Apenas administradores autorizados poderão consultá-los.

---

# LGPD

Quando aplicável:

```text
Anonimização

Mas

↓

Sem perder rastreabilidade.
```

---

# Backup

Registros de Auditoria deverão participar das rotinas de backup.

Nunca poderão ser ignorados.

---

# Logging

Toda gravação de Auditoria poderá registrar:

```text
AuditId

Duration

Entity

Operation
```

---

# Métricas

Registrar

```text
Audits por minuto

Operações

Alterações

Consultas

Exportações
```

---

# Organização

```text
audit/

    models.py

    repository.py

    service.py

    exporter.py

    filters.py

    validators.py

    retention.py
```

---

# Integração

A Auditoria poderá ser alimentada por:

```text
Application Services

Repositories

Synchronization

Authentication

Authorization

Workers
```

Nunca diretamente pela UI.

---

# Testabilidade

O sistema deverá possuir:

```text
Create Tests

Update Tests

Delete Tests

Integrity Tests

Retention Tests

Performance Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Permitir UPDATE

Permitir DELETE

Registrar Senhas

Misturar Logs Técnicos

Ignorar CorrelationId

Ignorar Tenant
```

---

# Checklist

Antes de adicionar Auditoria verificar:

- registra usuário?
- registra Tenant?
- registra valores antigos?
- registra novos valores?
- é imutável?
- possui testes?

---

# Regras Gerais

Todo registro de Auditoria deverá:

- ser imutável;
- possuir contexto completo;
- registrar alterações;
- respeitar Multi-Tenant;
- integrar-se ao Tracing;
- permitir reconstrução histórica.

---

# Fluxo Completo

```text
Usuário

↓

Application

↓

Audit Service

↓

Audit Repository

↓

Audit Database

↓

Consulta

↓

Relatórios

↓

Compliance
```

---

# Próximo Documento

```text
049-backup-architecture.md
```