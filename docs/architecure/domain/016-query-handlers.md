# Application Architecture Specification
## 016 - Query Handlers

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos Query Handlers do OrganizeG3.

Os Query Handlers representam a implementação dos Casos de Uso de leitura.

Seu objetivo é executar consultas de forma eficiente, segura e desacoplada do Domínio.

Os Query Handlers pertencem exclusivamente ao lado de leitura (Read Side) da arquitetura CQRS.

---

# O que é um Query Handler?

Um Query Handler é responsável por executar exatamente uma Query.

Exemplo

```text
SearchCustomersQuery

↓

SearchCustomersQueryHandler
```

Existe uma relação de:

```text
1 Query

↓

1 Handler
```

---

# Responsabilidades

Um Query Handler deverá:

- receber uma Query;
- validar permissões;
- consultar Read Models;
- aplicar filtros;
- aplicar paginação;
- aplicar ordenação;
- montar DTOs;
- retornar resultados.

Nunca deverá:

- alterar dados;
- executar Commands;
- publicar eventos;
- executar regras de domínio;
- iniciar transações.

---

# Fluxo

```text
Presentation

↓

Query

↓

Validator

↓

Query Handler

↓

Read Database

↓

DTO

↓

Presentation
```

---

# Dependências Permitidas

Um Query Handler poderá depender de:

```text
Read Repository

Read Database

Read Models

Cache

DTO Mapper

Localization

Feature Flags
```

Nunca depender diretamente de:

```text
Aggregates

Factories

Repositories de Escrita

Unit Of Work

SQLAlchemy Models do Domínio

Command Handlers
```

---

# Read Model

Toda leitura deverá utilizar Read Models.

Nunca consultar diretamente Aggregates.

Exemplo

```text
Sales Dashboard

↓

SalesDashboardReadModel

↓

DTO
```

---

# DTO Mapping

O Handler será responsável por transformar:

```text
Read Model

↓

DTO
```

Nunca retornar:

```text
Entity

Aggregate

ORM Model
```

---

# Estrutura

Todo Query Handler deverá possuir:

```text
Query

↓

Validate()

↓

Read()

↓

Map()

↓

Return()
```

---

# Paginação

Sempre que necessário utilizar:

```text
Page

PageSize

TotalRecords

TotalPages
```

Nunca retornar milhares de registros sem paginação.

---

# Ordenação

Toda ordenação deverá ser explícita.

Exemplo

```text
Nome ASC

↓

Data DESC

↓

Código ASC
```

Nunca depender da ordem natural do banco.

---

# Filtros

Filtros deverão ser opcionais e independentes.

Exemplo

```text
Cliente

Status

Categoria

Período

Vendedor

Projeto

Filial
```

---

# Pesquisa

Suportar pesquisa por:

```text
Código

Nome

Documento

Telefone

Email

Descrição

SKU
```

Sempre respeitando Tenant.

---

# Segurança

Antes de executar qualquer consulta verificar:

```text
Tenant

Usuário

Permissões

Feature Flags
```

Nenhuma Query poderá acessar dados de outro Tenant.

---

# Cache

Consultas poderão utilizar cache quando apropriado.

Exemplos

```text
Dashboard

Catálogo

Tabela de Preços

Relatórios

Configurações
```

Nunca cachear:

```text
Permissões

Saldo Financeiro

Sessão

Autenticação
```

Sem política clara de invalidação.

---

# Performance

Prioridades

```text
Índices

Read Models

Views

Materialized Views

Projection Tables

Cache
```

Evitar

```text
N+1

JOINs desnecessários

SELECT *

Consultas sem índice
```

---

# Consultas Complexas

Relatórios grandes deverão utilizar:

```text
Projection Tables

Views

Materialized Views

Analytics Database
```

Nunca carregar Aggregates completos.

---

# Exportações

Exportações poderão retornar:

```text
CSV

Excel

PDF

JSON

XML
```

Sempre utilizando Read Models.

---

# Auditoria

Registrar:

```text
QueryId

CorrelationId

TenantId

UserId

ExecutionTime

ReturnedRows

CacheHit

Timestamp
```

---

# Erros

O Query Handler poderá lançar:

```text
ValidationException

PermissionException

QueryException

NotFoundException
```

Nunca lançar exceções de infraestrutura diretamente para a Presentation.

---

# Assincronismo

Consultas demoradas poderão ser executadas em background.

Exemplos

```text
Business Intelligence

Relatórios

Exportações

Dashboards Analíticos
```

---

# Organização

Estrutura sugerida

```text
queries/

    search_customers/

        query.py

        handler.py

        validator.py

        dto.py

    sales_dashboard/

        query.py

        handler.py

        dto.py
```

Cada Query possui sua própria pasta.

---

# Testabilidade

Todo Query Handler deverá possuir testes.

Casos mínimos

```text
Consulta válida

Sem resultados

Permissão negada

Paginação

Ordenação

Filtros

Cache

Performance
```

---

# Convenções

Nome

```text
<Query>Handler
```

Exemplos

```text
SearchCustomersQueryHandler

InventoryBalanceQueryHandler

SalesDashboardQueryHandler

ProjectStatusQueryHandler
```

---

# Anti-Patterns

Nunca fazer

```text
Executar Commands

Alterar banco

Executar Commit

Modificar Aggregates

Publicar Domain Events

Utilizar Unit Of Work
```

Query Handler pertence exclusivamente ao lado de leitura.

---

# Checklist

Antes de implementar verificar:

- executa apenas leitura?
- retorna DTO?
- utiliza Read Model?
- suporta Tenant?
- suporta paginação?
- suporta ordenação?
- suporta filtros?
- possui testes?

---

# Regras Gerais

Todo Query Handler deverá:

- executar apenas leitura;
- nunca modificar estado;
- utilizar Read Models;
- retornar DTOs;
- ser pequeno;
- ser altamente performático;
- respeitar isolamento por Tenant;
- possuir testes automatizados.

---

# Fluxo Completo

```text
Request

↓

Query

↓

Validator

↓

Query Handler

↓

Read Model

↓

DTO

↓

Response
```

---

# Próximo Documento

```text
017-dtos.md
```