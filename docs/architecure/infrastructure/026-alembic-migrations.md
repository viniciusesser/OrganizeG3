# Infrastructure Architecture Specification
## 026 - Alembic Migrations

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para gerenciamento de migrações do banco de dados do OrganizeG3.

Toda alteração estrutural do banco deverá ocorrer exclusivamente através do Alembic.

Nunca serão realizadas alterações manuais diretamente no banco de produção.

---

# Objetivos

O sistema de migrações deverá garantir:

- evolução segura do banco;
- rastreabilidade;
- rollback;
- compatibilidade entre versões;
- automação de deploy;
- sincronização entre ambientes.

---

# Tecnologias

Migrações

```text
Alembic
```

ORM

```text
SQLAlchemy 2.x
```

Banco

```text
SQLite

PostgreSQL
```

---

# Arquitetura

```text
SQLAlchemy Models

↓

Alembic Revision

↓

Migration Script

↓

Database
```

---

# Estrutura

```text
database/

    migrations/

        env.py

        script.py.mako

        versions/

            20260804_001_initial.py

            20260808_002_customers.py

            20260811_003_products.py
```

---

# Versionamento

Cada Migration deverá possuir:

```text
Revision ID

↓

Down Revision

↓

Data

↓

Descrição
```

Exemplo

```text
20260811_003_products
```

---

# Convenção de Nome

Sempre utilizar

```text
YYYYMMDD_NNN_descricao
```

Exemplos

```text
20260804_001_initial

20260810_002_customers

20260811_003_products

20260812_004_sales_orders
```

---

# Fluxo

```text
Alterar Model

↓

Gerar Migration

↓

Revisar

↓

Testar

↓

Commit

↓

Deploy
```

---

# Geração

Sempre utilizar

```bash
alembic revision --autogenerate -m "customers"
```

Após gerar:

Revisar manualmente.

Nunca confiar totalmente no autogenerate.

---

# Revisão Obrigatória

Toda Migration deverá ser revisada verificando:

- nomes;
- índices;
- constraints;
- tipos;
- defaults;
- nullable;
- foreign keys.

---

# Upgrade

Toda Migration deverá implementar

```python
upgrade()
```

Responsável por:

- criar tabelas;
- alterar colunas;
- criar índices;
- criar constraints.

---

# Downgrade

Toda Migration deverá implementar

```python
downgrade()
```

Permitindo reversão completa.

Nunca deixar downgrade vazio.

---

# Ordem

As Migrations deverão ser lineares.

Fluxo

```text
001

↓

002

↓

003

↓

004
```

Evitar branches paralelos.

---

# Dados

Migrações estruturais não deverão inserir dados de negócio.

Permitido apenas:

```text
Configurações iniciais

Permissões padrão

Feature Flags

Dados técnicos
```

---

# Seed

Dados iniciais deverão utilizar:

```text
Seed Scripts
```

Nunca Migrations.

---

# Alteração de Colunas

Fluxo recomendado

```text
Adicionar coluna

↓

Popular dados

↓

Validar

↓

Remover coluna antiga
```

Evitar alterações destrutivas.

---

# Exclusão

Nunca remover colunas imediatamente.

Fluxo

```text
Descontinuar

↓

Migrar dados

↓

Nova versão

↓

Remover
```

---

# Renomeação

Evitar renomear diretamente.

Preferir

```text
Criar

↓

Copiar

↓

Atualizar

↓

Excluir
```

---

# Índices

Sempre criar índices através de Migration.

Nunca manualmente.

---

# Constraints

Toda Constraint deverá possuir nome.

Exemplo

```text
pk_customers

fk_sales_orders_customer_id_customers

uq_users_email

ck_products_price
```

---

# Multi-Tenant

Toda tabela criada deverá possuir:

```text
tenant_id
```

Quando aplicável.

Os índices compostos deverão considerar Tenant.

---

# Auditoria

Toda tabela criada deverá possuir:

```text
created_at

updated_at

version
```

Quando aplicável

```text
deleted_at

is_deleted
```

---

# SQLite

As Migrations deverão permanecer compatíveis com SQLite.

Evitar recursos exclusivos do PostgreSQL quando houver alternativa.

---

# PostgreSQL

Recursos específicos poderão ser utilizados quando encapsulados.

Exemplos

```text
JSONB

GIN Index

Generated Columns

Extensions
```

Sempre mantendo compatibilidade arquitetural.

---

# Rollback

Toda Migration deverá suportar rollback.

Fluxo

```text
Upgrade

↓

Teste

↓

Downgrade

↓

Teste
```

---

# Integridade

Após cada Migration validar:

```text
Constraints

Foreign Keys

Índices

Tipos

Dados
```

---

# Performance

Após grandes alterações verificar:

```text
Plano de Execução

Índices

Tempo

Locks
```

---

# Backup

Antes de executar Migrations em produção:

```text
Backup

↓

Migration

↓

Validação

↓

Liberação
```

---

# Ambientes

Fluxo

```text
Development

↓

Homologação

↓

Produção
```

Nunca aplicar Migration diretamente em produção sem validação.

---

# CI/CD

O Pipeline deverá executar:

```text
Migration

↓

Testes

↓

Rollback Test

↓

Deploy
```

---

# Testabilidade

Toda Migration deverá possuir:

```text
Upgrade Test

Downgrade Test

SQLite Test

PostgreSQL Test

Performance Test
```

---

# Organização

Estrutura

```text
database/

    migrations/

        versions/

        seeds/

        fixtures/
```

---

# Anti-Patterns

Nunca fazer

```text
Editar Migration antiga

Excluir Migration publicada

Alterar banco manualmente

Executar SQL em produção fora do Alembic

Ignorar Downgrade
```

---

# Checklist

Antes de publicar uma Migration verificar:

- possui upgrade?
- possui downgrade?
- foi revisada?
- foi testada?
- possui nomes padronizados?
- possui índices?
- possui constraints?
- funciona em SQLite?
- funciona em PostgreSQL?

---

# Regras Gerais

Toda Migration deverá:

- ser determinística;
- ser reversível;
- ser auditável;
- possuir revisão manual;
- possuir testes;
- ser compatível com os bancos suportados.

---

# Fluxo Completo

```text
Model

↓

Alembic Revision

↓

Migration

↓

Review

↓

Testes

↓

Deploy

↓

Banco Atualizado
```

---

# Próximo Documento

```text
027-outbox-pattern.md
```