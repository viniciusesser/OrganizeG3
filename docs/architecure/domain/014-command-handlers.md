# Application Architecture Specification
## 014 - Command Handlers

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos Command Handlers do OrganizeG3.

Os Command Handlers representam a implementação dos Casos de Uso da aplicação.

Cada Handler é responsável por receber um Command, coordenar o domínio e persistir as alterações.

Nenhum Handler deverá conter regras de negócio.

---

# O que é um Command Handler?

Um Command Handler é responsável por executar exatamente um Command.

Exemplo

```text
CreateCustomerCommand

↓

CreateCustomerHandler
```

Existe uma relação de 1 para 1.

---

# Responsabilidades

Um Command Handler deverá:

- receber o Command;
- iniciar o Unit Of Work;
- consultar Repositories;
- utilizar Factories;
- executar o Aggregate;
- persistir alterações;
- executar Commit;
- retornar o resultado.

Nunca deverá:

- executar SQL;
- validar regras de domínio;
- calcular impostos;
- aplicar descontos;
- manipular interface.

---

# Fluxo

```text
Presentation

↓

Command

↓

Validator

↓

Command Handler

↓

Repositories

↓

Factories

↓

Aggregate

↓

Unit Of Work

↓

Commit

↓

Domain Events

↓

Response
```

---

# Estrutura

Todo Handler deverá possuir:

```text
Command

↓

Dependencies

↓

Execute()

↓

Result
```

---

# Dependências Permitidas

Um Handler poderá depender de:

```text
Repositories

Unit Of Work

Factories

Domain Services

Policies

Application Services

Clock

Id Generator
```

Nunca diretamente de:

```text
SQLAlchemy

SQLite

HTTP

Filesystem

Redis

FastAPI

PySide6
```

---

# Responsabilidade Única

Cada Handler deverá executar apenas um Caso de Uso.

Exemplo

```text
ApproveSalesOrderHandler
```

Nunca deverá:

```text
Criar Pedido

↓

Emitir Nota

↓

Enviar Email

↓

Gerar Produção
```

No mesmo Handler.

As demais ações ocorrerão através de Domain Events.

---

# Nomeclatura

Sempre utilizar:

```text
<Command>Handler
```

Exemplos

```text
CreateCustomerHandler

UpdateCustomerHandler

ApproveSalesOrderHandler

IssueInvoiceHandler

ReceivePaymentHandler
```

---

# Passos de Execução

Todo Handler deverá seguir a sequência:

```text
1. Validar Command

↓

2. Abrir Unit Of Work

↓

3. Buscar Aggregates

↓

4. Executar regra do Domínio

↓

5. Persistir alterações

↓

6. Commit

↓

7. Retornar resultado
```

---

# Exemplo

Fluxo

```text
ApproveSalesOrderCommand

↓

Buscar Pedido

↓

SalesOrder.Approve()

↓

Repository.Update()

↓

Commit()

↓

SalesOrderApproved
```

---

# Repositories

O Handler nunca deverá executar SQL.

Sempre utilizar:

```text
CustomerRepository

SalesOrderRepository

ProductRepository

InvoiceRepository
```

---

# Factories

Quando necessário:

```text
Command

↓

Factory

↓

Aggregate
```

Nunca construir objetos complexos diretamente no Handler.

---

# Domain Services

Quando uma regra envolver múltiplos Aggregates:

```text
Handler

↓

Domain Service

↓

Aggregate
```

---

# Unit Of Work

Todo Handler deverá utilizar exatamente um Unit Of Work.

Nunca:

```text
Commit()

↓

Commit()

↓

Commit()
```

No mesmo Caso de Uso.

---

# Eventos

Os Handlers nunca publicarão Domain Events manualmente.

Fluxo correto

```text
Aggregate

↓

Domain Events

↓

Commit

↓

Outbox

↓

Message Bus
```

---

# Resultado

Todo Handler deverá retornar um objeto de resultado.

Exemplo

```text
Success

AggregateId

Messages

Warnings
```

Nunca retornar:

```text
Entity

SQL

Response HTTP
```

---

# Exceções

O Handler poderá tratar:

```text
ValidationException

BusinessException

NotFoundException

ConcurrencyException

PermissionException
```

Nunca mascarar erros inesperados.

---

# Segurança

Antes da execução deverão ser verificadas:

```text
Tenant

Usuário

Permissões

Feature Flags

Licença
```

---

# Auditoria

Registrar:

```text
CommandId

CorrelationId

UserId

TenantId

ExecutionTime

Result
```

---

# Assincronismo

Handlers assíncronos poderão executar:

```text
OCR

IA

Backup

Importação

Exportação

Sincronização
```

Sempre utilizando filas.

---

# Performance

Handlers deverão ser curtos.

Idealmente

```text
50 a 150 linhas
```

Caso ultrapasse isso, extrair responsabilidades.

---

# Anti-Patterns

Nunca fazer

```text
SQL direto

Regras de domínio

Ifs gigantes

Switch enormes

Múltiplos casos de uso

Dependência da UI

Commit manual em vários pontos
```

---

# Organização

Estrutura

```text
commands/

    create_customer/

        command.py

        handler.py

        validator.py

        result.py

    create_sales_order/

        command.py

        handler.py

        validator.py

        result.py
```

Cada Caso de Uso possui sua própria pasta.

---

# Testabilidade

Todo Handler deverá possuir testes de:

- execução válida;
- validação;
- Aggregate inexistente;
- permissão negada;
- erro de concorrência;
- rollback;
- commit.

---

# Checklist

Antes de implementar verificar:

- executa apenas um Caso de Uso?
- utiliza Unit Of Work?
- utiliza Repository?
- não possui regra de negócio?
- não executa SQL?
- publica eventos apenas via Aggregate?
- possui testes?

---

# Regras Gerais

Todo Command Handler deverá:

- possuir responsabilidade única;
- ser pequeno;
- utilizar Dependency Injection;
- utilizar Unit Of Work;
- utilizar Repositories;
- nunca conhecer infraestrutura;
- nunca executar regras de domínio;
- nunca acessar banco diretamente.

---

# Fluxo Completo

```text
Request

↓

Command

↓

Validator

↓

Handler

↓

Repositories

↓

Aggregate

↓

Commit

↓

Outbox

↓

Response
```

---

# Próximo Documento

```text
015-queries.md
```