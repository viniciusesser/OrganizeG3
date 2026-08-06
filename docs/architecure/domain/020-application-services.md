# Application Architecture Specification
## 020 - Application Services

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos Application Services do OrganizeG3.

Application Services são responsáveis por coordenar Casos de Uso complexos que envolvem múltiplos Commands, múltiplos Aggregates ou integração entre diversos módulos.

Eles pertencem exclusivamente à camada Application.

Nunca representam regras de negócio.

---

# O que é um Application Service?

Um Application Service coordena processos de alto nível.

Ele funciona como um orquestrador.

Exemplo

```text
Fechamento Financeiro

↓

Recebimentos

↓

Pagamentos

↓

Conciliação

↓

Relatórios

↓

Eventos
```

Toda essa coordenação pertence ao Application Service.

---

# Responsabilidades

Um Application Service poderá:

- coordenar múltiplos Handlers;
- executar Workflows;
- iniciar Unit Of Work;
- utilizar vários Repositories;
- coordenar integrações;
- controlar transações;
- iniciar processos assíncronos.

Nunca deverá:

- executar regras de domínio;
- executar SQL;
- alterar Entities diretamente;
- substituir Aggregates.

---

# Quando utilizar

Utilizar Application Service quando:

- existir um processo longo;
- envolver vários Aggregates;
- envolver diversos módulos;
- envolver múltiplos Commands;
- envolver integrações.

---

# Quando NÃO utilizar

Não utilizar Application Service para:

```text
CRUD simples

Regras de domínio

Validações

Persistência

Queries simples
```

Nestes casos utilizar:

```text
Command Handler

↓

Aggregate

↓

Repository
```

---

# Arquitetura

```text
Presentation

↓

Application Service

↓

Commands

↓

Handlers

↓

Domain

↓

Infrastructure
```

---

# Fluxo

```text
Request

↓

Application Service

↓

Command Handler

↓

Unit Of Work

↓

Repositories

↓

Commit

↓

Domain Events
```

---

# Exemplos

## Fechamento Financeiro

```text
Validar Caixa

↓

Recebimentos

↓

Pagamentos

↓

Conciliação

↓

Encerramento

↓

Relatório
```

---

## Importação de Produtos

```text
Arquivo

↓

Parser

↓

Validação

↓

CreateProductCommand

↓

Commit

↓

Resumo
```

---

## Backup Completo

```text
Verificar Licença

↓

Preparar Banco

↓

Gerar Backup

↓

Compactar

↓

Enviar Storage

↓

Registrar Auditoria
```

---

## Sincronização Offline

```text
Receber Alterações

↓

Resolver Conflitos

↓

Executar Commands

↓

Commit

↓

Atualizar Snapshot
```

---

## Assistente de IA

```text
Receber Pergunta

↓

Buscar Contexto

↓

Executar RAG

↓

Selecionar Modelo

↓

Executar IA

↓

Registrar Histórico

↓

Retornar Resposta
```

---

# Dependências Permitidas

Um Application Service poderá depender de:

```text
Command Handlers

Repositories

Unit Of Work

Application Services

Domain Services

Policies

Cache

Storage

Queues

Event Bus
```

Nunca diretamente de:

```text
Presentation

UI

Views

Widgets

SQLAlchemy ORM Models
```

---

# Comunicação

Um Application Service poderá executar:

```text
Command

↓

Handler

↓

Command

↓

Handler

↓

Command

↓

Handler
```

Sempre mantendo cada Caso de Uso isolado.

---

# Integrações

Toda integração deverá ser iniciada pelo Application Service.

Exemplos

```text
Supabase

Email

WhatsApp

OCR

OpenAI

Storage

Banco

Webhook
```

Sempre utilizando Interfaces.

---

# Transações

Quando houver persistência:

```text
Application Service

↓

Unit Of Work

↓

Commit
```

Nunca executar commits em diversos pontos do fluxo.

---

# Processos Assíncronos

Poderão iniciar:

```text
Workers

Jobs

Filas

Background Tasks

Eventos
```

Exemplos

```text
Backup

OCR

Importações

Exportações

IA

Sincronização
```

---

# Orquestração

Application Services nunca deverão executar regras.

Eles apenas coordenam.

Exemplo

Errado

```text
Application Service calcula impostos.
```

Correto

```text
Application Service

↓

TaxCalculationService

↓

Aggregate
```

---

# Tratamento de Erros

Responsável por coordenar:

```text
Rollback

Retry

Compensações

Logs

Auditoria
```

Sem ocultar exceções inesperadas.

---

# Auditoria

Registrar:

```text
ExecutionId

CorrelationId

TenantId

UserId

ExecutionTime

Result

Modules

Commands

Events
```

---

# Performance

Application Services poderão utilizar:

```text
Parallelismo

Background Jobs

Cache

Streaming

Batch Processing
```

Sempre preservando consistência.

---

# Organização

Estrutura

```text
application/

    services/

        financial/

        production/

        synchronization/

        ai/

        importation/

        exportation/

        backup/

        reporting/
```

---

# Exemplos previstos

## Financeiro

```text
FinancialClosingService

CashFlowGenerationService

BankReconciliationService
```

---

## Produção

```text
ProductionPlanningService

MRPGenerationService

CapacityPlanningService
```

---

## Estoque

```text
InventorySynchronizationService

InventoryImportService
```

---

## CRM

```text
CustomerImportService

CustomerMergeService
```

---

## Documentos

```text
DocumentImportService

OCRProcessingService

DocumentIndexingService
```

---

## IA

```text
ConversationService

PromptExecutionService

AgentExecutionService

EmbeddingGenerationService
```

---

## Backup

```text
BackupService

RestoreService
```

---

## Sincronização

```text
SynchronizationService

ConflictResolutionService

SnapshotGenerationService
```

---

# Testabilidade

Todo Application Service deverá possuir testes.

Casos mínimos

```text
Execução completa

Falha intermediária

Rollback

Retry

Integrações simuladas

Eventos

Background Jobs
```

---

# Anti-Patterns

Nunca fazer

```text
Executar SQL

Criar UI

Executar regras do domínio

Modificar Entities diretamente

Executar Queries diretamente no banco

Misturar lógica técnica e lógica de negócio
```

---

# Checklist

Antes de criar um Application Service verificar:

- coordena mais de um Caso de Uso?
- envolve vários módulos?
- não contém regras de domínio?
- utiliza Dependency Injection?
- utiliza Unit Of Work quando necessário?
- utiliza Interfaces?
- possui testes?

---

# Regras Gerais

Todo Application Service deverá:

- coordenar processos;
- nunca conter regras de domínio;
- ser pequeno e coeso;
- utilizar Dependency Injection;
- utilizar Interfaces;
- permitir testes independentes;
- ser desacoplado da infraestrutura.

---

# Fluxo Completo

```text
Presentation

↓

Application Service

↓

Command Handler

↓

Aggregate

↓

Repository

↓

Unit Of Work

↓

Commit

↓

Outbox

↓

Workers

↓

Integrações

↓

Response
```

---

# Encerramento da Application Layer

Com este documento conclui-se a especificação da camada **Application**.

Os documentos produzidos até aqui definem toda a arquitetura da camada de aplicação do OrganizeG3:

```text
011 - Unit Of Work

012 - Application Layer

013 - Commands

014 - Command Handlers

015 - Queries

016 - Query Handlers

017 - DTOs

018 - Validators

019 - Mappers

020 - Application Services
```

---

# Próximo Documento

```text
021-infrastructure-overview.md
```