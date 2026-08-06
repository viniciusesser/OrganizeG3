# Application Architecture Specification
## 012 - Application Layer

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial da camada Application do OrganizeG3.

A Application Layer é responsável por orquestrar os Casos de Uso (Use Cases) da plataforma.

Ela conecta:

- Presentation
- Domain
- Infrastructure

Sem possuir regras de negócio.

---

# Responsabilidade

A Application Layer deverá:

- executar Casos de Uso;
- receber Commands;
- executar Queries;
- iniciar Unit Of Work;
- utilizar Repositories;
- chamar Domain Services;
- retornar DTOs;
- publicar eventos da aplicação.

Nunca deverá conter regras de negócio.

---

# Arquitetura

```text
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

A Application conhece:

- Domain
- Contracts

Nunca conhece:

- SQLAlchemy
- PostgreSQL
- SQLite
- Qt
- FastAPI Internals
- Redis
- HTTP

---

# Estrutura

A camada Application será composta por:

```text
Commands

Queries

Handlers

DTOs

Validators

Mappers

Application Services

Pipelines

Behaviors

Interfaces
```

---

# Casos de Uso

Cada operação do sistema será representada por um Caso de Uso.

Exemplos

```text
Cadastrar Cliente

Cadastrar Produto

Criar Pedido

Aprovar Pedido

Cancelar Pedido

Emitir Nota Fiscal

Criar Ordem de Produção

Receber Pagamento

Registrar Compra

Cadastrar Funcionário
```

Cada Caso de Uso será independente.

---

# Fluxo

```text
Request

↓

Validation

↓

Command

↓

Handler

↓

Unit Of Work

↓

Repositories

↓

Domain

↓

Commit

↓

Response
```

---

# Command Side

Operações que alteram dados.

Exemplos

```text
CreateCustomerCommand

UpdateCustomerCommand

DeleteCustomerCommand

ApproveSalesOrderCommand

CancelInvoiceCommand
```

Sempre passam pelo domínio.

---

# Query Side

Operações somente leitura.

Exemplos

```text
GetCustomerByIdQuery

SearchCustomersQuery

ListProductsQuery

DashboardQuery

InventoryBalanceQuery
```

Queries nunca alteram estado.

---

# Command Handler

Cada Command possuirá exatamente um Handler.

Exemplo

```text
CreateCustomerCommand

↓

CreateCustomerHandler
```

Nunca:

```text
Dois Handlers

ou

Nenhum Handler
```

---

# Query Handler

Cada Query possuirá exatamente um Handler.

Exemplo

```text
SearchProductsQuery

↓

SearchProductsHandler
```

---

# DTOs

Toda comunicação com a Presentation utilizará DTOs.

Nunca retornar Entities.

Exemplo

```text
CustomerDto

ProductDto

SalesOrderDto

InvoiceDto
```

---

# Validators

Todo Command deverá possuir validação.

Responsabilidades

```text
Obrigatórios

Tipos

Tamanho

Formato

Regras simples
```

Regras de domínio permanecem no Domain.

---

# Mappers

Responsáveis por transformar:

```text
DTO

↓

Domain

↓

DTO
```

Nunca executar regras de negócio.

---

# Application Services

Application Services coordenam Casos de Uso maiores.

Exemplo

```text
CloseMonthService

GenerateMRPService

ImportProductsService

SyncOfflineDataService
```

Nunca conter regras de domínio.

---

# Pipelines

A execução poderá utilizar comportamentos transversais.

Exemplos

```text
Validation

Authorization

Logging

Auditing

Performance

Transactions

Caching

Metrics
```

Fluxo

```text
Pipeline

↓

Handler

↓

Pipeline
```

---

# Behaviors

Behaviors poderão executar:

```text
Logging

Retry

Performance

Metrics

CorrelationId

Authorization

Validation
```

Sem alterar o domínio.

---

# Dependências

A Application poderá depender de:

```text
Domain

Contracts

Shared
```

Nunca depender diretamente de:

```text
SQLAlchemy

SQLite

PostgreSQL

Redis

Qt

PySide

Filesystem
```

---

# Comunicação

A comunicação com o domínio ocorrerá através de:

```text
Repositories

Factories

Domain Services

Policies

Specifications
```

Nunca através de SQL.

---

# Comunicação com Infrastructure

Sempre por interfaces.

Exemplo

```text
IDocumentStorage

IEmailSender

IEventBus

ICache

IFileStorage
```

A implementação pertence à Infrastructure.

---

# Tratamento de Erros

A Application deverá tratar:

```text
ValidationException

BusinessException

ConcurrencyException

PermissionException

NotFoundException
```

Nunca expor exceções internas para a UI.

---

# Segurança

Toda operação deverá validar:

```text
Tenant

Permissões

Usuário

Filial

Feature Flags
```

Antes da execução.

---

# Auditoria

Cada Caso de Uso deverá registrar:

```text
UserId

TenantId

CorrelationId

ExecutionTime

Success

Failure
```

---

# Assincronismo

Alguns Casos de Uso poderão ser assíncronos.

Exemplos

```text
Enviar Emails

OCR

IA

Backup

Integrações

Sincronização
```

Sempre utilizando filas.

---

# Testabilidade

Toda classe da Application deverá possuir testes.

Os testes nunca dependerão de:

```text
Banco

API

Filesystem

Redis

Email
```

Utilizar Fakes e Mocks.

---

# Convenções

Cada Caso de Uso deverá possuir:

```text
Command

Handler

Validator

DTO

Tests
```

Quando aplicável

```text
Mapper

Application Service
```

---

# Estrutura de Pastas

```text
application/

    commands/

    command_handlers/

    queries/

    query_handlers/

    validators/

    dtos/

    mappers/

    services/

    pipelines/

    behaviors/
```

---

# Regras Gerais

A Application Layer deverá:

- ser fina;
- orquestrar o domínio;
- nunca conter regras de negócio;
- utilizar Dependency Injection;
- ser totalmente testável;
- utilizar Unit Of Work;
- utilizar Repositories;
- utilizar DTOs;
- utilizar Validators.

---

# Fluxo Completo

```text
Presentation

↓

Application

↓

Domain

↓

Infrastructure

↓

Database
```

Cada camada possui responsabilidades claramente definidas.

---

# Próximo Documento

```text
013-commands.md
```