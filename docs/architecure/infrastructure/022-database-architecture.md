# Infrastructure Architecture Specification
## 022 - Database Architecture

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do banco de dados do OrganizeG3.

Toda persistência do sistema deverá seguir exatamente estas definições.

Nenhuma tabela poderá ser criada fora deste padrão.

---

# Objetivos

A arquitetura do banco deverá garantir:

- escalabilidade;
- performance;
- consistência;
- auditoria;
- sincronização;
- isolamento entre empresas;
- evolução sem quebra de compatibilidade.

---

# Tecnologias

O OrganizeG3 utilizará oficialmente:

Desenvolvimento Desktop

```text
SQLite
```

Servidor

```text
PostgreSQL
```

Sincronização

```text
Supabase PostgreSQL
```

ORM

```text
SQLAlchemy 2.x
```

Migrações

```text
Alembic
```

---

# Filosofia

O banco de dados deverá ser:

```text
Normalizado

Auditável

Versionado

Multi-Tenant

Escalável

Determinístico
```

---

# Arquitetura

```text
Application

↓

Repositories

↓

SQLAlchemy

↓

Database Session

↓

SQLite / PostgreSQL
```

O domínio nunca acessa tabelas diretamente.

---

# Convenções de Nome

## Tabelas

Sempre utilizar:

```text
snake_case
```

Exemplos

```text
customers

sales_orders

sales_order_items

production_orders

inventory_movements

financial_transactions
```

Nunca utilizar:

```text
Customers

tb_customer

tblCustomer
```

---

# Colunas

Sempre utilizar:

```text
snake_case
```

Exemplos

```text
customer_id

created_at

updated_at

tenant_id

is_deleted
```

---

# Primary Keys

Todas as tabelas utilizarão:

```text
UUID v4
```

Tipo

```text
UUID
```

Nunca utilizar:

```text
INTEGER AUTOINCREMENT
```

Como chave pública.

---

# Foreign Keys

Toda Foreign Key deverá utilizar UUID.

Exemplo

```text
customer_id

↓

customers.id
```

---

# Naming Convention

Constraints

```text
pk_<table>

fk_<table>_<column>_<target>

ix_<table>_<column>

uq_<table>_<column>

ck_<table>_<rule>
```

Exemplo

```text
pk_customers

fk_sales_orders_customer_id_customers

ix_products_sku

uq_users_email
```

---

# Auditoria

Toda tabela deverá possuir:

```text
created_at

created_by_user_id

updated_at

updated_by_user_id

version
```

Quando aplicável

```text
deleted_at

deleted_by_user_id

is_deleted
```

---

# Multi-Tenant

Toda tabela de negócio deverá possuir:

```text
tenant_id
```

Quando necessário

```text
branch_id

department_id
```

Nunca permitir registros sem Tenant.

---

# Versionamento

Toda tabela deverá possuir:

```text
version
```

Objetivos

```text
Concorrência otimista

Sincronização

Auditoria
```

---

# Soft Delete

Nunca excluir registros importantes.

Utilizar:

```text
is_deleted

deleted_at

deleted_by_user_id
```

---

# Datas

Todas as datas deverão utilizar:

```text
TIMESTAMP WITH TIME ZONE
```

Sempre em:

```text
UTC
```

Nunca persistir horário local.

---

# Valores Monetários

Nunca utilizar:

```text
FLOAT
```

Sempre utilizar:

```text
NUMERIC
```

Precisão

```text
18,4
```

---

# Quantidades

Utilizar:

```text
NUMERIC

INTEGER
```

Dependendo da necessidade.

Nunca utilizar float.

---

# Booleanos

Utilizar

```text
BOOLEAN
```

Nunca

```text
CHAR

INTEGER

VARCHAR
```

Para representar verdadeiro ou falso.

---

# Texto

Tipos

```text
VARCHAR

TEXT
```

Critérios

```text
VARCHAR

↓

Campos limitados

TEXT

↓

Conteúdo livre
```

---

# Enumerações

Preferencialmente utilizar:

```text
VARCHAR
```

Com validação pelo domínio.

Evitar ENUM nativo do banco para facilitar evolução.

---

# Índices

Toda tabela deverá possuir índices para:

```text
tenant_id

created_at

updated_at

is_deleted
```

Quando aplicável

```text
status

code

sku

document

email
```

---

# Índices Compostos

Exemplos

```text
tenant_id + status

tenant_id + created_at

tenant_id + customer_id

tenant_id + code
```

---

# Unique Constraints

Exemplos

```text
email

sku

cpf

cnpj

internal_code
```

Sempre considerando Tenant quando necessário.

---

# Check Constraints

Exemplos

```text
quantity >= 0

price >= 0

discount >= 0

discount <= 100
```

---

# Relacionamentos

Tipos

```text
One-To-One

One-To-Many

Many-To-One
```

Evitar Many-To-Many direto.

Preferir tabela intermediária.

---

# Cascatas

Nunca utilizar:

```text
Cascade Delete
```

Para entidades de negócio.

Preferir:

```text
Restrict

Soft Delete
```

---

# Sessões

Toda sessão será gerenciada pelo:

```text
Unit Of Work
```

Nunca abrir sessões diretamente na Application.

---

# Migrações

Toda alteração estrutural deverá ocorrer através do Alembic.

Nunca alterar o banco manualmente.

Fluxo

```text
Model

↓

Migration

↓

Review

↓

Deploy
```

---

# Performance

Prioridades

```text
Índices

Paginação

Batch

Projection

Read Models
```

Evitar

```text
SELECT *

JOIN excessivo

Subqueries profundas
```

---

# Particionamento

Preparado para futuro suporte.

Possíveis critérios

```text
Tenant

Ano

Empresa

Centro de Custo
```

---

# Arquivamento

Registros antigos poderão ser arquivados.

Sem perda da rastreabilidade.

---

# Integridade

Toda integridade deverá existir em três níveis:

```text
Domínio

↓

Application

↓

Banco
```

Nunca confiar apenas no banco.

---

# Eventos

Persistência de eventos utilizará:

```text
event_store

outbox_events
```

Separadas das tabelas de negócio.

---

# Logs Técnicos

Nunca armazenar logs de aplicação no banco principal.

Utilizar estrutura dedicada.

---

# Backup

Estratégia

```text
Backup completo

↓

Incremental

↓

Snapshot
```

Compatível com restauração por Tenant.

---

# Segurança

Nunca armazenar

```text
Senha

JWT

Secrets

Private Keys
```

Sem criptografia.

---

# Criptografia

Campos sensíveis poderão utilizar:

```text
AES

Hash

Tokenização
```

Dependendo do tipo de dado.

---

# Health Check

Verificações

```text
Conectividade

Latência

Versão

Migrações

Pool

Integridade
```

---

# Banco Local

SQLite será utilizado apenas para:

```text
Cache

Offline

Sincronização

Desktop
```

Nunca como banco definitivo da empresa.

---

# Banco Servidor

PostgreSQL será considerado:

```text
Fonte Oficial dos Dados
```

---

# Estrutura Física

```text
database/

    migrations/

    seed/

    session/

    models/

    repositories/

    scripts/

    fixtures/

    health/

    backup/
```

---

# Testes

Toda alteração deverá possuir:

```text
Migration Test

Rollback Test

Performance Test

Integrity Test

Concurrency Test
```

---

# Checklist

Antes de criar uma tabela verificar:

- possui UUID?
- possui tenant_id?
- possui auditoria?
- possui version?
- possui índices?
- possui soft delete?
- possui constraints?
- possui migration?

---

# Regras Gerais

Toda tabela deverá:

- possuir UUID;
- possuir auditoria;
- possuir versionamento;
- possuir isolamento por Tenant;
- possuir índices adequados;
- suportar sincronização;
- ser compatível com SQLite e PostgreSQL;
- permitir evolução por migrações.

---

# Fluxo Completo

```text
Aggregate

↓

Repository

↓

SQLAlchemy Model

↓

Session

↓

SQLite / PostgreSQL

↓

Alembic
```

---

# Próximo Documento

```text
023-sqlalchemy-models.md
```