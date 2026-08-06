# Application Architecture Specification
## 011 - Unit Of Work

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do Unit Of Work do OrganizeG3.

O Unit Of Work é responsável por controlar todas as alterações realizadas durante um Caso de Uso (Use Case), garantindo consistência, atomicidade e integridade das transações.

Nenhum Command Handler deverá executar commits diretamente.

Toda persistência deverá ocorrer através do Unit Of Work.

---

# O que é Unit Of Work?

O Unit Of Work representa uma transação da aplicação.

Durante sua execução ele:

- controla os Repositories utilizados;
- controla a transação;
- registra alterações;
- publica Domain Events;
- executa Commit;
- executa Rollback quando necessário.

---

# Objetivos

O Unit Of Work existe para:

- garantir consistência;
- centralizar transações;
- evitar commits parciais;
- publicar eventos somente após persistência;
- facilitar testes.

---

# Fluxo

```text
Command

↓

Command Handler

↓

Repositories

↓

Unit Of Work

↓

Commit

↓

Domain Events

↓

Outbox

↓

Message Bus
```

---

# Responsabilidades

O Unit Of Work deverá:

- abrir transação;
- controlar Repositories;
- persistir alterações;
- confirmar transação;
- cancelar transação;
- despachar eventos;
- registrar auditoria.

Nunca deverá conter regras de negócio.

---

# Escopo

Cada execução de um Command deverá possuir exatamente um Unit Of Work.

Exemplo

```text
Create Sales Order

↓

1 Unit Of Work
```

Outro exemplo

```text
Approve Invoice

↓

1 Unit Of Work
```

Nunca compartilhar Unit Of Work entre requisições.

---

# Ciclo de Vida

```text
Open

↓

Repositories

↓

Changes

↓

Commit

↓

Publish Events

↓

Dispose
```

Caso ocorra erro

```text
Open

↓

Repositories

↓

Exception

↓

Rollback

↓

Dispose
```

---

# Commit

O Commit deverá ocorrer apenas uma vez.

Após:

- todas as validações;
- todas as alterações;
- todas as verificações de domínio.

Nunca executar múltiplos commits em um mesmo Caso de Uso.

---

# Rollback

Sempre que ocorrer:

```text
Exception

Validation Error

Concurrency Error

Infrastructure Failure
```

O Unit Of Work deverá executar Rollback.

Nenhuma alteração parcial poderá permanecer persistida.

---

# Repositories

Todos os Repositories utilizados durante um Caso de Uso deverão compartilhar o mesmo Unit Of Work.

Exemplo

```text
CustomerRepository

SalesOrderRepository

InventoryRepository

↓

Mesmo Unit Of Work
```

---

# Domain Events

Durante a execução:

Os Aggregates armazenam Domain Events internamente.

Após o Commit:

```text
Commit

↓

Coletar Events

↓

Outbox

↓

Event Bus
```

Nunca publicar eventos antes da persistência.

---

# Outbox Pattern

Após o Commit:

Todos os Domain Events deverão ser gravados na Outbox.

Fluxo

```text
Aggregate

↓

Domain Event

↓

Outbox

↓

Worker

↓

Message Bus
```

Garantindo consistência entre banco e mensageria.

---

# Auditoria

Durante o Commit registrar:

```text
TenantId

UserId

CorrelationId

Repositories

Aggregates

Duration

Timestamp
```

---

# Concorrência

O Unit Of Work deverá validar:

```text
Version
```

Caso a versão tenha sido alterada:

```text
ConcurrencyException
```

Executar Rollback.

---

# Isolation

O Unit Of Work deverá respeitar o isolamento por Tenant.

Nunca permitir alterações entre empresas diferentes.

---

# Repositories Disponíveis

O Unit Of Work disponibilizará acesso aos Repositories.

Exemplo

```text
Customers

Products

SalesOrders

PurchaseOrders

ProductionOrders

Inventory

Financial

Projects

Documents
```

Todos compartilhando a mesma transação.

---

# Transações Distribuídas

Evitar.

Sempre que possível utilizar:

```text
Eventual Consistency

Domain Events

Outbox Pattern
```

Nunca Two Phase Commit entre módulos.

---

# Integrações

Integrações externas nunca deverão ocorrer dentro da transação.

Exemplo incorreto

```text
Commit

↓

Enviar Email

↓

Salvar Pedido
```

Correto

```text
Salvar Pedido

↓

Commit

↓

Publicar Evento

↓

Worker

↓

Enviar Email
```

---

# Testabilidade

O Unit Of Work deverá permitir:

```text
Fake Unit Of Work

Memory Unit Of Work

Transactional Tests
```

Sem depender do banco real.

---

# Interface

A camada Domain conhecerá apenas a interface.

Exemplo

```text
IUnitOfWork
```

Implementações

```text
SqlAlchemyUnitOfWork

MemoryUnitOfWork
```

---

# Responsabilidades da Infrastructure

A Infrastructure será responsável por:

- abrir conexão;
- iniciar transação;
- executar commit;
- executar rollback;
- fechar conexão.

---

# Responsabilidades da Application

A Application será responsável por:

- iniciar o Unit Of Work;
- utilizar os Repositories;
- executar o Caso de Uso;
- solicitar Commit.

---

# Convenções

Nunca chamar:

```text
Repository.Commit()

Repository.Rollback()

Database.Commit()
```

Sempre utilizar

```text
UnitOfWork.Commit()
```

---

# Checklist

Antes de implementar verificar:

- existe apenas um Unit Of Work?
- todos os Repositories compartilham a mesma transação?
- Domain Events são publicados após Commit?
- existe Rollback?
- existe controle de concorrência?
- existe auditoria?
- existe isolamento por Tenant?

---

# Regras Gerais

Todo Unit Of Work deverá:

- controlar uma única transação;
- publicar eventos somente após Commit;
- impedir commits parciais;
- executar Rollback automaticamente;
- ser descartado ao final do Caso de Uso;
- ser independente da interface.

---

# Fluxo Completo

```text
Request

↓

Middleware

↓

Command

↓

Command Handler

↓

Unit Of Work

↓

Repositories

↓

Aggregates

↓

Commit

↓

Outbox

↓

Message Bus

↓

Response
```

---

# Próximo Documento

```text
012-application-layer.md
```