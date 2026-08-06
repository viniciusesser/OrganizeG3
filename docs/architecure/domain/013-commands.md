# Application Architecture Specification
## 013 - Commands

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos Commands do OrganizeG3.

Commands representam uma intenção explícita de alterar o estado do sistema.

Todo Command deverá seguir exatamente estas definições.

---

# O que é um Command?

Um Command representa uma solicitação de alteração no domínio.

Ele descreve algo que o usuário deseja fazer.

Exemplos

```text
Criar Cliente

Atualizar Produto

Cancelar Pedido

Aprovar Compra

Emitir Nota Fiscal
```

Um Command representa uma intenção.

Ele ainda não significa que a operação será executada.

---

# Características

Todo Command deverá ser:

```text
Imutável

Serializável

Auditável

Versionável

Validável
```

---

# Responsabilidades

Um Command deverá apenas:

- transportar dados;
- representar uma intenção;
- identificar quem solicitou a operação;
- permitir validação.

Nunca deverá:

- executar regras;
- acessar banco;
- acessar API;
- executar SQL;
- publicar eventos.

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

Domain

↓

Repository

↓

Unit Of Work
```

---

# Estrutura

Todo Command deverá possuir:

```text
CommandId

CorrelationId

TenantId

UserId

OccurredAt

Payload
```

---

# CommandId

Cada Command possuirá um identificador único.

Padrão

```text
UUID v4
```

---

# CorrelationId

Todos os Commands originados da mesma operação compartilharão o mesmo CorrelationId.

Exemplo

```text
Criar Pedido

↓

Criar Produção

↓

Reservar Estoque

↓

Enviar Notificação
```

Todos pertencem ao mesmo fluxo.

---

# TenantId

Todo Command deverá informar o Tenant responsável.

Nenhuma operação poderá ocorrer sem Tenant.

---

# UserId

Identifica quem iniciou a operação.

Será utilizado para:

- auditoria;
- permissões;
- histórico;
- rastreabilidade.

---

# Payload

O Payload deverá conter apenas os dados necessários.

Nunca transportar:

- objetos completos;
- entidades persistidas;
- conexões;
- serviços.

---

# Imutabilidade

Após criado, um Command nunca poderá ser alterado.

Caso seja necessário modificar informações:

Criar um novo Command.

---

# Nomeclatura

Sempre utilizar:

```text
Verbo + Objeto + Command
```

Correto

```text
CreateCustomerCommand

ApproveSalesOrderCommand

CancelInvoiceCommand

RegisterPaymentCommand
```

Errado

```text
CustomerCommand

InvoiceAction

DoPayment
```

---

# Commands do CRM

```text
CreateCustomerCommand

UpdateCustomerCommand

ArchiveCustomerCommand

ConvertLeadCommand

CreateOpportunityCommand
```

---

# Commands Comerciais

```text
CreateQuotationCommand

ApproveQuotationCommand

CreateSalesOrderCommand

ApproveSalesOrderCommand

CancelSalesOrderCommand

CloseSalesOrderCommand
```

---

# Commands Compras

```text
CreatePurchaseRequestCommand

ApprovePurchaseRequestCommand

CreatePurchaseOrderCommand

ApprovePurchaseOrderCommand

ReceivePurchaseCommand
```

---

# Commands Estoque

```text
RegisterInventoryMovementCommand

ReserveInventoryCommand

ReleaseInventoryCommand

TransferInventoryCommand

AdjustInventoryCommand
```

---

# Commands Produção

```text
CreateProductionOrderCommand

StartProductionCommand

PauseProductionCommand

FinishProductionCommand

ConsumeMaterialCommand
```

---

# Commands Financeiros

```text
CreateReceivableCommand

ReceivePaymentCommand

CreatePayableCommand

PayInvoiceCommand

CloseCashRegisterCommand
```

---

# Commands Fiscais

```text
IssueInvoiceCommand

AuthorizeInvoiceCommand

CancelInvoiceCommand

InvalidateInvoiceNumberCommand
```

---

# Commands Projetos

```text
CreateProjectCommand

CreateTaskCommand

FinishTaskCommand

CloseProjectCommand
```

---

# Commands Workflow

```text
CreateWorkflowCommand

MoveWorkflowCardCommand

ApproveWorkflowStageCommand

CompleteWorkflowCommand
```

---

# Commands Documentos

```text
UploadDocumentCommand

ArchiveDocumentCommand

CreateDocumentVersionCommand
```

---

# Commands IA

```text
CreatePromptCommand

PublishPromptCommand

CreateAgentCommand

StartConversationCommand
```

---

# Commands Sincronização

```text
RegisterDeviceCommand

CreateSnapshotCommand

SynchronizeDeviceCommand
```

---

# Validação

Todo Command deverá possuir um Validator.

Exemplo

```text
CreateCustomerCommand

↓

CreateCustomerValidator
```

O Validator verifica:

- obrigatoriedade;
- formato;
- tamanho;
- tipos;
- consistência básica.

Nunca regras de negócio.

---

# Regras de Negócio

As regras pertencem ao Domain.

Nunca ao Command.

Exemplo

Errado

```text
Command verifica limite de crédito.
```

Correto

```text
Aggregate verifica limite de crédito.
```

---

# Segurança

Todo Command deverá validar:

```text
Tenant

Usuário

Permissões

Feature Flags
```

Antes de chegar ao domínio.

---

# Auditoria

Todo Command deverá registrar:

```text
CommandId

UserId

TenantId

CorrelationId

OccurredAt

ExecutionTime

Resultado
```

---

# Idempotência

Commands críticos deverão suportar:

```text
Idempotency Key
```

Exemplos

```text
Receber Pagamento

Emitir Nota

Criar Pedido

Registrar Produção
```

Evita duplicidade em caso de reenvio.

---

# Retry

Caso ocorra falha de infraestrutura:

O mesmo Command poderá ser reenviado.

Como é imutável, produzirá exatamente o mesmo comportamento esperado.

---

# Assincronismo

Alguns Commands poderão ser executados em background.

Exemplos

```text
OCR

IA

Backup

Sincronização

Importação

Exportação
```

---

# Testabilidade

Todo Command deverá possuir testes de:

- serialização;
- validação;
- compatibilidade;
- versionamento.

---

# Convenções

Todo Command deverá:

- ser imutável;
- representar uma intenção;
- possuir CommandId;
- possuir CorrelationId;
- possuir TenantId;
- possuir UserId;
- possuir Validator;
- possuir testes.

---

# Fluxo Completo

```text
UI

↓

Command

↓

Validator

↓

Command Handler

↓

Domain

↓

Repository

↓

Unit Of Work

↓

Commit

↓

Domain Event
```

---

# Próximo Documento

```text
014-command-handlers.md
```