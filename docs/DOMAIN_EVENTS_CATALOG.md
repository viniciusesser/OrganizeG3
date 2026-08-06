# OrganizeG3 — Domain Events Catalog

> Catálogo oficial de eventos de domínio e integração da plataforma OrganizeG3.

---

| Propriedade            | Valor                                           |
| ---------------------- | ----------------------------------------------- |
| Documento              | DOMAIN_EVENTS_CATALOG.md                        |
| Versão                 | 1.0.0                                           |
| Status                 | Baseline arquitetural                           |
| Abrangência            | Toda a plataforma                               |
| Depende de             | DOMAIN_ARCHITECTURE.md, DOMAIN_RELATIONSHIPS.md |
| Idioma da documentação | Português                                       |
| Idioma dos eventos     | Inglês                                          |
| Convenção              | `context.entity.action`                         |

---

# 1. Objetivo

Este documento define o catálogo oficial de eventos do OrganizeG3.

Ele estabelece:

* convenções de nomenclatura;
* estrutura obrigatória dos eventos;
* responsabilidades de publicação;
* regras de imutabilidade;
* versionamento;
* classificação;
* eventos produzidos por cada contexto;
* consumidores previstos;
* dados mínimos de cada evento;
* regras de segurança;
* critérios para criação de novos eventos.

Todo evento publicado pela plataforma deverá estar previsto neste catálogo ou ser incluído nele antes da implementação.

---

# 2. Definição

Um evento representa um fato relevante que já aconteceu no domínio.

Exemplos:

```text
production.execution_started
workflow.stage_changed
commercial.quotation_approved
inventory.stock_reserved
document.version_uploaded
```

Um evento não é uma solicitação.

Correto:

```text
production.execution_started
```

Incorreto:

```text
production.start_execution
```

O primeiro representa um fato concluído.

O segundo representa uma intenção e deveria ser tratado como comando.

---

# 3. Eventos, comandos e auditoria

## 3.1 Comando

Comando expressa intenção.

Exemplo:

```text
StartExecutionCommand
```

Pode ser rejeitado.

## 3.2 Evento

Evento registra o resultado confirmado.

Exemplo:

```text
production.execution_started
```

Já aconteceu e não pode ser rejeitado retroativamente.

## 3.3 Auditoria

Auditoria registra quem executou uma ação, em qual contexto e quais dados foram alterados.

Exemplo:

```text
action = production.execution.start
entity_type = OperationExecution
entity_id = ...
```

Eventos e auditorias poderão compartilhar:

* `correlation_id`;
* `causation_id`;
* usuário;
* funcionário;
* dispositivo;
* origem.

Porém deverão permanecer em estruturas distintas.

---

# 4. Convenção de nomes

Todos os eventos utilizarão:

```text
context.entity.action
```

Exemplos:

```text
identity.user_created
organization.employee_transferred
commercial.quotation_approved
workflow.instance_completed
production.execution_paused
inventory.stock_adjusted
```

## 4.1 Contexto

Primeiro segmento.

Exemplos:

```text
identity
organization
crm
commercial
workflow
production
inventory
purchasing
quality
maintenance
documents
forms
notifications
financial
fiscal
configuration
analytics
ai
```

## 4.2 Entidade ou conceito

Segundo segmento.

Exemplos:

```text
user
employee
quotation
instance
execution
stock
document
submission
```

## 4.3 Ação no passado

Terceiro segmento.

Exemplos:

```text
created
updated
approved
started
paused
finished
cancelled
archived
uploaded
resolved
```

## 4.4 Regras de nomenclatura

Os nomes deverão:

* usar letras minúsculas;
* utilizar `_` em termos compostos;
* evitar abreviações;
* representar fatos concluídos;
* permanecer estáveis;
* ser semanticamente específicos;
* evitar nomes genéricos.

Evitar:

```text
record.updated
entity.changed
system.event
data.saved
item.processed
```

Preferir:

```text
commercial.quotation_version_created
production.execution_finished
inventory.stock_reservation_failed
```

---

# 5. Estrutura obrigatória

Todo evento deverá possuir o envelope mínimo:

```json
{
  "event_id": "uuid",
  "tenant_id": "uuid",
  "aggregate_type": "OperationExecution",
  "aggregate_id": "uuid",
  "aggregate_sequence": 4,
  "event_type": "production.execution_started",
  "schema_version": 1,
  "actor": {
    "user_id": "uuid",
    "employee_id": "uuid"
  },
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "source": "pwa",
  "occurred_at": "2026-08-04T18:00:00Z",
  "recorded_at": "2026-08-04T18:00:01Z",
  "payload": {},
  "metadata": {}
}
```

---

# 6. Campos do envelope

## `event_id`

Identificador único do evento.

Deve ser UUID.

Nunca reutilizar.

## `tenant_id`

Empresa proprietária do evento.

Obrigatório para eventos empresariais.

Eventos de plataforma poderão utilizar contexto específico e controlado.

## `aggregate_type`

Nome do agregado que gerou o evento.

Exemplos:

```text
Quotation
WorkflowInstance
OperationExecution
StockReservation
Document
```

## `aggregate_id`

Identificador do agregado.

## `aggregate_sequence`

Número sequencial do evento dentro do agregado.

Permite:

* ordenação;
* controle de concorrência;
* detecção de lacunas;
* reconstrução futura;
* rastreabilidade.

## `event_type`

Nome oficial do evento.

## `schema_version`

Versão do contrato do evento.

Começa em:

```text
1
```

Mudanças incompatíveis exigem nova versão.

## `actor`

Identifica o responsável pela ação.

Pode conter:

```json
{
  "user_id": "uuid",
  "employee_id": "uuid",
  "actor_type": "USER"
}
```

Possíveis tipos:

```text
USER
SYSTEM
AUTOMATION
AI
INTEGRATION
MIGRATION
```

## `correlation_id`

Agrupa ações relacionadas ao mesmo fluxo.

Exemplo:

```text
aprovação de orçamento
    ↓
criação de pedido
    ↓
criação de produção
    ↓
criação de workflow
```

Todos podem compartilhar o mesmo `correlation_id`.

## `causation_id`

Identifica o evento ou comando que causou o atual.

## `source`

Origem da ação.

Valores iniciais:

```text
desktop
pwa
api
automation
ai
integration
migration
system
```

## `occurred_at`

Momento em que o fato aconteceu.

Sempre em UTC.

## `recorded_at`

Momento em que o evento foi persistido.

## `payload`

Dados específicos do evento.

## `metadata`

Dados técnicos adicionais.

Exemplos:

```json
{
  "device_id": "uuid",
  "ip_address": "127.0.0.1",
  "application_version": "0.1.0",
  "offline_command_id": "uuid"
}
```

---

# 7. Classificação dos eventos

## 7.1 Domain Event

Representa fato interno de um agregado.

Exemplo:

```text
production.execution_started
```

## 7.2 Integration Event

Contrato público enviado para outros contextos.

Pode derivar de um Domain Event.

Exemplo:

```text
commercial.quotation_approved
```

consumido por:

* Production;
* Workflow;
* Notifications;
* Analytics.

## 7.3 System Event

Representa fatos técnicos.

Exemplos:

```text
system.application_started
system.database_connection_failed
system.background_job_failed
```

Não substitui logging.

## 7.4 Timeline Event

Evento classificado para apresentação ao usuário.

Nem todo evento técnico aparece na Timeline.

## 7.5 Analytics Event

Evento autorizado para alimentar indicadores.

## 7.6 Notification Event

Evento configurado para gerar notificação.

---

# 8. Persistência

Eventos deverão ser persistidos em tabela append-only.

Estrutura conceitual:

```text
domain_events
```

Regras:

* não atualizar;
* não excluir;
* não sobrescrever payload;
* não alterar timestamps;
* não reutilizar `event_id`;
* proteger por permissões no banco;
* registrar versão do schema.

Correções deverão gerar novos eventos.

---

# 9. Transactional Outbox

Eventos destinados a outros consumidores deverão utilizar Outbox.

Fluxo:

```text
Comando executado
    ↓
Agregado alterado
    ↓
Evento criado
    ↓
Evento e Outbox persistidos na mesma transação
    ↓
Transação confirmada
    ↓
Worker publica mensagem
    ↓
Consumidores processam
```

Nunca publicar uma mensagem externa antes da confirmação da transação.

---

# 10. Idempotência

Consumidores devem armazenar controle de processamento.

Estruturas recomendadas:

```text
inbox_messages
processed_events
event_consumer_checkpoints
```

O mesmo evento não poderá gerar efeitos duplicados.

A idempotência deverá considerar:

```text
consumer_name + event_id
```

---

# 11. Ordenação

A ordem global de eventos não é garantida.

A ordem por agregado deverá utilizar:

```text
aggregate_id
aggregate_sequence
```

Consumidores que dependem de sequência deverão validar lacunas.

---

# 12. Evolução dos contratos

## 12.1 Mudança compatível

Pode manter a mesma versão:

* adicionar campo opcional;
* adicionar metadado opcional;
* ampliar enum preservando consumidores;
* corrigir descrição sem mudar comportamento.

## 12.2 Mudança incompatível

Exige nova versão:

* remover campo;
* renomear campo;
* mudar tipo;
* alterar semântica;
* tornar campo opcional obrigatório;
* mudar estrutura do payload.

## 12.3 Regra

Eventos antigos permanecem válidos.

Consumidores devem declarar versões suportadas.

---

# 13. Dados sensíveis

Eventos não deverão conter desnecessariamente:

* senhas;
* tokens;
* segredos;
* documentos pessoais completos;
* dados bancários completos;
* arquivos;
* conteúdo sensível integral;
* credenciais externas.

Quando necessário, utilizar:

* identificadores;
* mascaramento;
* referências;
* hashes;
* campos classificados.

---

# 14. Identity Events

## `identity.user_created`

Publicado quando uma identidade de usuário é criada.

Payload mínimo:

```json
{
  "user_id": "uuid",
  "email": "usuario@empresa.com",
  "full_name": "Nome do usuário",
  "is_platform_admin": false
}
```

Consumidores:

* Organization;
* Notifications;
* Audit;
* Analytics.

---

## `identity.user_authenticated`

Publicado após autenticação bem-sucedida.

Payload:

```json
{
  "user_id": "uuid",
  "session_id": "uuid",
  "device_id": "uuid",
  "authentication_method": "PASSWORD"
}
```

Não incluir token.

Consumidores:

* Audit;
* Security Analytics.

---

## `identity.authentication_failed`

Publicado após tentativa de autenticação rejeitada.

Payload:

```json
{
  "email_hash": "hash",
  "reason_code": "INVALID_CREDENTIALS",
  "device_id": "uuid"
}
```

Consumidores:

* Security;
* Audit;
* Notifications, quando configurado.

---

## `identity.session_revoked`

Payload:

```json
{
  "user_id": "uuid",
  "session_id": "uuid",
  "reason_code": "USER_LOGOUT"
}
```

---

## `identity.device_registered`

Payload:

```json
{
  "user_id": "uuid",
  "device_id": "uuid",
  "platform": "PWA",
  "trusted": false
}
```

---

## `identity.password_changed`

Payload:

```json
{
  "user_id": "uuid",
  "all_other_sessions_revoked": true
}
```

---

## `identity.user_blocked`

Payload:

```json
{
  "user_id": "uuid",
  "reason": "Acesso suspenso pelo administrador"
}
```

---

# 15. Organization Events

## `organization.tenant_created`

Payload:

```json
{
  "tenant_id": "uuid",
  "legal_name": "Empresa",
  "trade_name": "Nome fantasia",
  "timezone": "America/Sao_Paulo",
  "locale": "pt-BR"
}
```

Consumidores:

* Configuration;
* Authorization;
* Notifications;
* Analytics.

---

## `organization.tenant_suspended`

Payload:

```json
{
  "tenant_id": "uuid",
  "reason_code": "LICENSE_EXPIRED",
  "effective_at": "datetime"
}
```

Consumidores:

* Identity;
* Authorization;
* Notifications.

---

## `organization.branch_created`

Payload:

```json
{
  "branch_id": "uuid",
  "code": "MATRIZ",
  "name": "Matriz",
  "is_headquarters": true
}
```

---

## `organization.branch_archived`

Payload:

```json
{
  "branch_id": "uuid",
  "reason": "Unidade encerrada"
}
```

---

## `organization.sector_created`

Payload:

```json
{
  "sector_id": "uuid",
  "branch_id": "uuid",
  "parent_sector_id": null,
  "code": "CORTE",
  "name": "Corte"
}
```

---

## `organization.employee_created`

Payload:

```json
{
  "employee_id": "uuid",
  "user_id": "uuid",
  "full_name": "Funcionário",
  "branch_id": "uuid",
  "sector_id": "uuid"
}
```

---

## `organization.employee_assigned`

Payload:

```json
{
  "employee_id": "uuid",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "job_title": "Marceneiro"
}
```

---

## `organization.employee_transferred`

Payload:

```json
{
  "employee_id": "uuid",
  "previous_branch_id": "uuid",
  "previous_sector_id": "uuid",
  "new_branch_id": "uuid",
  "new_sector_id": "uuid",
  "effective_at": "datetime"
}
```

---

## `organization.employee_terminated`

Payload:

```json
{
  "employee_id": "uuid",
  "terminated_on": "date",
  "membership_disabled": true
}
```

Consumidores:

* Identity;
* Authorization;
* Production;
* Scheduling.

---

## `organization.membership_created`

Payload:

```json
{
  "membership_id": "uuid",
  "user_id": "uuid",
  "employee_id": "uuid",
  "status": "ACTIVE"
}
```

---

## `organization.membership_disabled`

Payload:

```json
{
  "membership_id": "uuid",
  "user_id": "uuid",
  "reason": "Funcionário desligado"
}
```

---

# 16. Authorization Events

## `authorization.role_created`

Payload:

```json
{
  "role_id": "uuid",
  "code": "PRODUCTION_OPERATOR",
  "name": "Operador de produção"
}
```

---

## `authorization.permission_granted`

Payload:

```json
{
  "role_id": "uuid",
  "permission_code": "production.execution.start",
  "scope": {
    "assigned_only": true
  }
}
```

---

## `authorization.permission_revoked`

Payload:

```json
{
  "role_id": "uuid",
  "permission_code": "production.execution.start"
}
```

---

## `authorization.role_assigned`

Payload:

```json
{
  "membership_id": "uuid",
  "role_id": "uuid"
}
```

---

## `authorization.role_removed`

Payload:

```json
{
  "membership_id": "uuid",
  "role_id": "uuid"
}
```

---

# 17. CRM Events

## `crm.lead_created`

Payload:

```json
{
  "lead_id": "uuid",
  "name": "Cliente potencial",
  "source": "WHATSAPP",
  "assigned_user_id": "uuid"
}
```

---

## `crm.lead_qualified`

Payload:

```json
{
  "lead_id": "uuid",
  "qualification": "QUALIFIED",
  "notes": "Solicitou orçamento de cozinha"
}
```

---

## `crm.lead_converted`

Payload:

```json
{
  "lead_id": "uuid",
  "customer_id": "uuid"
}
```

Consumidores:

* Commercial;
* Workflow;
* Analytics.

---

## `crm.customer_created`

Payload:

```json
{
  "customer_id": "uuid",
  "name": "Cliente",
  "person_type": "INDIVIDUAL",
  "tax_id_masked": "***"
}
```

---

## `crm.customer_updated`

Payload:

```json
{
  "customer_id": "uuid",
  "changed_fields": [
    "contact_data"
  ]
}
```

---

## `crm.opportunity_created`

Payload:

```json
{
  "opportunity_id": "uuid",
  "customer_id": "uuid",
  "title": "Cozinha planejada",
  "estimated_value": "25000.00"
}
```

---

## `crm.opportunity_won`

Payload:

```json
{
  "opportunity_id": "uuid",
  "quotation_id": "uuid"
}
```

---

## `crm.opportunity_lost`

Payload:

```json
{
  "opportunity_id": "uuid",
  "loss_reason_code": "PRICE"
}
```

---

# 18. Commercial Events

## `commercial.quotation_created`

Payload:

```json
{
  "quotation_id": "uuid",
  "customer_id": "uuid",
  "code": "ORC-000001",
  "initial_version_number": 1
}
```

---

## `commercial.quotation_version_created`

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "version_number": 2,
  "change_reason": "Alteração solicitada pelo cliente",
  "total_amount": "27000.00"
}
```

---

## `commercial.quotation_sent`

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "sent_at": "datetime",
  "delivery_channel": "WHATSAPP"
}
```

---

## `commercial.quotation_approved`

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "customer_id": "uuid",
  "total_amount": "27000.00",
  "approved_at": "datetime",
  "approval_method": "SIGNED_CONTRACT"
}
```

Consumidores:

* CRM;
* Production;
* Workflow;
* Financial;
* Notifications;
* Analytics.

---

## `commercial.quotation_rejected`

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "reason_code": "CUSTOMER_DECLINED"
}
```

---

## `commercial.quotation_archived`

Payload:

```json
{
  "quotation_id": "uuid",
  "reason": "Substituído por novo orçamento"
}
```

---

## `commercial.contract_created`

Payload:

```json
{
  "contract_id": "uuid",
  "quotation_id": "uuid",
  "customer_id": "uuid",
  "version_number": 1
}
```

---

## `commercial.contract_signed`

Payload:

```json
{
  "contract_id": "uuid",
  "customer_id": "uuid",
  "signed_at": "datetime",
  "signature_method": "DIGITAL"
}
```

---

## `commercial.sales_order_created`

Payload:

```json
{
  "sales_order_id": "uuid",
  "quotation_id": "uuid",
  "contract_id": "uuid",
  "customer_id": "uuid"
}
```

Consumidores:

* Production;
* Financial;
* Fiscal;
* Analytics.

---

# 19. Workflow Events

## `workflow.definition_created`

Payload:

```json
{
  "workflow_definition_id": "uuid",
  "code": "PRODUCTION_DEFAULT",
  "name": "Produção padrão",
  "kind": "PRODUCTION"
}
```

---

## `workflow.version_created`

Payload:

```json
{
  "workflow_definition_id": "uuid",
  "workflow_version_id": "uuid",
  "version_number": 2
}
```

---

## `workflow.version_published`

Payload:

```json
{
  "workflow_definition_id": "uuid",
  "workflow_version_id": "uuid",
  "version_number": 2,
  "published_at": "datetime"
}
```

---

## `workflow.instance_created`

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "workflow_definition_id": "uuid",
  "workflow_version_id": "uuid",
  "initial_stage_id": "uuid",
  "reference_type": "PRODUCTION_ORDER",
  "reference_id": "uuid"
}
```

---

## `workflow.stage_changed`

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "from_stage_id": "uuid",
  "to_stage_id": "uuid",
  "transition_id": "uuid",
  "justification": null,
  "is_return": false,
  "is_skip": false
}
```

Consumidores:

* Production;
* Notifications;
* Timeline;
* Analytics;
* Automation.

---

## `workflow.stage_skipped`

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "skipped_stage_id": "uuid",
  "target_stage_id": "uuid",
  "justification": "Etapa não se aplica"
}
```

---

## `workflow.instance_returned`

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "from_stage_id": "uuid",
  "to_stage_id": "uuid",
  "reason": "Peça faltante"
}
```

---

## `workflow.instance_paused`

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "reason_code": "MATERIAL_UNAVAILABLE"
}
```

---

## `workflow.instance_resumed`

Payload:

```json
{
  "workflow_instance_id": "uuid"
}
```

---

## `workflow.instance_completed`

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "completed_at": "datetime",
  "terminal_stage_id": "uuid"
}
```

---

## `workflow.instance_cancelled`

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "reason_code": "CUSTOMER_CANCELLED"
}
```

---

# 20. Production Events

## `production.order_created`

Payload:

```json
{
  "production_order_id": "uuid",
  "sales_order_id": "uuid",
  "quotation_id": "uuid",
  "customer_id": "uuid",
  "workflow_instance_id": "uuid"
}
```

---

## `production.operation_created`

Payload:

```json
{
  "operation_instance_id": "uuid",
  "production_order_id": "uuid",
  "stage_definition_id": "uuid",
  "operation_definition_id": "uuid",
  "name": "Corte da estrutura"
}
```

---

## `production.operation_assigned`

Payload:

```json
{
  "operation_instance_id": "uuid",
  "employee_ids": [
    "uuid",
    "uuid"
  ],
  "assigned_at": "datetime"
}
```

---

## `production.operation_unassigned`

Payload:

```json
{
  "operation_instance_id": "uuid",
  "employee_id": "uuid",
  "reason": "Reorganização da equipe"
}
```

---

## `production.execution_created`

Payload:

```json
{
  "execution_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_number": 1
}
```

---

## `production.execution_started`

Payload:

```json
{
  "execution_id": "uuid",
  "operation_instance_id": "uuid",
  "employee_ids": [
    "uuid"
  ],
  "machine_ids": [],
  "started_at": "datetime",
  "device_id": "uuid"
}
```

Consumidores:

* Timeline;
* Analytics;
* Scheduling;
* Notifications.

---

## `production.execution_participant_joined`

Payload:

```json
{
  "execution_id": "uuid",
  "employee_id": "uuid",
  "joined_at": "datetime",
  "role_in_execution": "HELPER"
}
```

---

## `production.execution_participant_left`

Payload:

```json
{
  "execution_id": "uuid",
  "employee_id": "uuid",
  "left_at": "datetime"
}
```

---

## `production.execution_paused`

Payload:

```json
{
  "execution_id": "uuid",
  "pause_id": "uuid",
  "category": "MATERIAL",
  "reason_code": "MISSING_PART",
  "reason_text": "Falta fundo de MDF",
  "started_at": "datetime"
}
```

Consumidores:

* Notifications;
* Timeline;
* Analytics;
* Inventory, quando relacionado a material.

---

## `production.execution_resumed`

Payload:

```json
{
  "execution_id": "uuid",
  "pause_id": "uuid",
  "resumed_at": "datetime",
  "paused_seconds": 1800
}
```

---

## `production.execution_finished`

Payload:

```json
{
  "execution_id": "uuid",
  "operation_instance_id": "uuid",
  "finished_at": "datetime",
  "worked_seconds": 7200,
  "paused_seconds": 1800,
  "result": "COMPLETED"
}
```

Consumidores:

* Workflow;
* Quality;
* Timeline;
* Analytics;
* Automation.

---

## `production.operation_completed`

Payload:

```json
{
  "operation_instance_id": "uuid",
  "production_order_id": "uuid",
  "completed_at": "datetime",
  "execution_count": 2
}
```

---

## `production.operation_skipped`

Payload:

```json
{
  "operation_instance_id": "uuid",
  "reason": "Operação não se aplica a este serviço"
}
```

---

## `production.rework_requested`

Payload:

```json
{
  "original_operation_instance_id": "uuid",
  "rework_operation_instance_id": "uuid",
  "reason_code": "MANUFACTURING_ERROR",
  "responsible_employee_id": "uuid",
  "requested_at": "datetime"
}
```

Consumidores:

* Quality;
* Analytics;
* Notifications.

---

## `production.material_requested`

Payload:

```json
{
  "material_request_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "requested_by_employee_id": "uuid",
  "items": [
    {
      "material_id": "uuid",
      "quantity": "2.0000",
      "unit": "UN"
    }
  ]
}
```

Consumidores:

* Inventory;
* Purchasing;
* Notifications;
* Timeline.

---

## `production.machine_incident_reported`

Payload:

```json
{
  "execution_id": "uuid",
  "machine_id": "uuid",
  "incident_id": "uuid",
  "description": "Serra parou durante o corte"
}
```

---

## `production.order_completed`

Payload:

```json
{
  "production_order_id": "uuid",
  "workflow_instance_id": "uuid",
  "completed_at": "datetime",
  "total_worked_seconds": 54000,
  "total_paused_seconds": 7200
}
```

---

## `production.order_cancelled`

Payload:

```json
{
  "production_order_id": "uuid",
  "reason_code": "CUSTOMER_CANCELLED"
}
```

Consumidores:

* Inventory;
* Scheduling;
* Financial;
* Analytics.

---

# 21. Forms Events

## `forms.definition_created`

Payload:

```json
{
  "form_definition_id": "uuid",
  "code": "CUTTING_CHECKLIST",
  "name": "Checklist de corte",
  "is_checklist": true
}
```

---

## `forms.version_published`

Payload:

```json
{
  "form_definition_id": "uuid",
  "form_version_id": "uuid",
  "version_number": 2
}
```

---

## `forms.binding_created`

Payload:

```json
{
  "form_definition_id": "uuid",
  "binding_type": "OPERATION",
  "operation_definition_id": "uuid",
  "is_required": true
}
```

---

## `forms.submission_started`

Payload:

```json
{
  "form_submission_id": "uuid",
  "form_version_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_id": "uuid"
}
```

---

## `forms.submission_completed`

Payload:

```json
{
  "form_submission_id": "uuid",
  "form_version_id": "uuid",
  "submitted_by_employee_id": "uuid",
  "submitted_at": "datetime"
}
```

---

## `forms.submission_reopened`

Payload:

```json
{
  "form_submission_id": "uuid",
  "reason": "Correção autorizada pelo administrador"
}
```

---

## `forms.validation_failed`

Payload:

```json
{
  "form_submission_id": "uuid",
  "field_codes": [
    "piece_quantity"
  ],
  "validation_codes": [
    "REQUIRED"
  ]
}
```

---

# 22. Documents Events

## `documents.document_created`

Payload:

```json
{
  "document_id": "uuid",
  "title": "Plano de corte",
  "document_type": "CUTTING_PLAN",
  "status": "ACTIVE"
}
```

---

## `documents.version_uploaded`

Payload:

```json
{
  "document_id": "uuid",
  "document_version_id": "uuid",
  "storage_object_id": "uuid",
  "version_number": 2,
  "original_filename": "plano_corte_v2.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 500000
}
```

Consumidores:

* Timeline;
* Search;
* Notifications;
* AI indexing.

---

## `documents.version_marked_current`

Payload:

```json
{
  "document_id": "uuid",
  "document_version_id": "uuid",
  "previous_current_version_id": "uuid"
}
```

---

## `documents.document_marked_obsolete`

Payload:

```json
{
  "document_id": "uuid",
  "reason": "Substituído por revisão posterior"
}
```

---

## `documents.document_archived`

Payload:

```json
{
  "document_id": "uuid",
  "reason": "Projeto concluído"
}
```

---

## `documents.link_created`

Payload:

```json
{
  "document_id": "uuid",
  "entity_type": "PRODUCTION_ORDER",
  "entity_id": "uuid",
  "relationship_type": "TECHNICAL_REFERENCE"
}
```

---

## `documents.permission_changed`

Payload:

```json
{
  "document_id": "uuid",
  "visibility_policy": {
    "roles": [
      "PRODUCTION_OPERATOR"
    ]
  }
}
```

---

# 23. Inventory Events

## `inventory.material_created`

Payload:

```json
{
  "material_id": "uuid",
  "code": "MDF-BRANCO-15",
  "name": "MDF Branco TX 15 mm",
  "unit": "CHAPA"
}
```

---

## `inventory.stock_received`

Payload:

```json
{
  "stock_movement_id": "uuid",
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "quantity": "10.0000",
  "source_type": "PURCHASE_ORDER",
  "source_id": "uuid"
}
```

---

## `inventory.stock_reserved`

Payload:

```json
{
  "reservation_id": "uuid",
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "production_order_id": "uuid",
  "quantity": "2.0000"
}
```

---

## `inventory.stock_reservation_failed`

Payload:

```json
{
  "material_request_id": "uuid",
  "material_id": "uuid",
  "requested_quantity": "2.0000",
  "available_quantity": "0.5000",
  "shortage_quantity": "1.5000"
}
```

Consumidores:

* Purchasing;
* Production;
* Notifications.

---

## `inventory.stock_released`

Payload:

```json
{
  "reservation_id": "uuid",
  "quantity": "2.0000",
  "reason_code": "PRODUCTION_ORDER_CANCELLED"
}
```

---

## `inventory.material_consumed`

Payload:

```json
{
  "stock_movement_id": "uuid",
  "material_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "quantity": "2.0000"
}
```

---

## `inventory.stock_adjusted`

Payload:

```json
{
  "stock_movement_id": "uuid",
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "previous_quantity": "10.0000",
  "new_quantity": "9.5000",
  "reason": "Inventário físico"
}
```

---

## `inventory.reorder_point_reached`

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "available_quantity": "1.0000",
  "reorder_point": "3.0000"
}
```

---

# 24. Purchasing Events

## `purchasing.request_created`

Payload:

```json
{
  "purchase_request_id": "uuid",
  "origin_type": "MATERIAL_SHORTAGE",
  "origin_id": "uuid",
  "items": [
    {
      "material_id": "uuid",
      "quantity": "2.0000"
    }
  ]
}
```

---

## `purchasing.request_approved`

Payload:

```json
{
  "purchase_request_id": "uuid",
  "approved_by_user_id": "uuid",
  "approved_at": "datetime"
}
```

---

## `purchasing.supplier_quotation_received`

Payload:

```json
{
  "supplier_quotation_id": "uuid",
  "purchase_request_id": "uuid",
  "supplier_id": "uuid",
  "total_amount": "1500.00"
}
```

---

## `purchasing.purchase_order_created`

Payload:

```json
{
  "purchase_order_id": "uuid",
  "purchase_request_id": "uuid",
  "supplier_id": "uuid",
  "total_amount": "1500.00"
}
```

---

## `purchasing.purchase_order_approved`

Payload:

```json
{
  "purchase_order_id": "uuid",
  "approved_by_user_id": "uuid"
}
```

---

## `purchasing.material_received`

Payload:

```json
{
  "purchase_order_id": "uuid",
  "receipt_id": "uuid",
  "stock_location_id": "uuid",
  "items": [
    {
      "material_id": "uuid",
      "received_quantity": "2.0000"
    }
  ]
}
```

Consumidores:

* Inventory;
* Financial;
* Quality;
* Production.

---

## `purchasing.purchase_cancelled`

Payload:

```json
{
  "purchase_order_id": "uuid",
  "reason": "Fornecedor não atenderá"
}
```

---

# 25. Quality Events

## `quality.inspection_requested`

Payload:

```json
{
  "inspection_id": "uuid",
  "inspection_type": "OPERATION_OUTPUT",
  "operation_execution_id": "uuid"
}
```

---

## `quality.inspection_completed`

Payload:

```json
{
  "inspection_id": "uuid",
  "result": "APPROVED",
  "completed_at": "datetime"
}
```

---

## `quality.nonconformity_created`

Payload:

```json
{
  "nonconformity_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "severity": "HIGH",
  "description": "Peça cortada fora da medida"
}
```

---

## `quality.rework_required`

Payload:

```json
{
  "nonconformity_id": "uuid",
  "original_operation_instance_id": "uuid",
  "reason_code": "DIMENSION_ERROR"
}
```

Consumidores:

* Production;
* Scheduling;
* Analytics;
* Notifications.

---

## `quality.material_rejected`

Payload:

```json
{
  "inspection_id": "uuid",
  "material_id": "uuid",
  "receipt_id": "uuid",
  "rejected_quantity": "1.0000",
  "reason": "Material danificado"
}
```

---

## `quality.corrective_action_completed`

Payload:

```json
{
  "corrective_action_id": "uuid",
  "nonconformity_id": "uuid",
  "completed_at": "datetime"
}
```

---

# 26. Maintenance Events

## `maintenance.machine_unavailable`

Payload:

```json
{
  "machine_id": "uuid",
  "equipment_id": "uuid",
  "reason_code": "BREAKDOWN",
  "unavailable_since": "datetime"
}
```

Consumidores:

* Production;
* Scheduling;
* Notifications;
* Analytics.

---

## `maintenance.order_created`

Payload:

```json
{
  "maintenance_order_id": "uuid",
  "equipment_id": "uuid",
  "maintenance_type": "CORRECTIVE",
  "priority": "HIGH"
}
```

---

## `maintenance.execution_started`

Payload:

```json
{
  "maintenance_order_id": "uuid",
  "execution_id": "uuid",
  "started_at": "datetime"
}
```

---

## `maintenance.execution_finished`

Payload:

```json
{
  "maintenance_order_id": "uuid",
  "execution_id": "uuid",
  "finished_at": "datetime",
  "resolution": "Troca de componente"
}
```

---

## `maintenance.machine_released`

Payload:

```json
{
  "machine_id": "uuid",
  "released_at": "datetime"
}
```

---

## `maintenance.preventive_due`

Payload:

```json
{
  "equipment_id": "uuid",
  "preventive_plan_id": "uuid",
  "due_at": "datetime"
}
```

---

# 27. Scheduling Events

## `scheduling.item_created`

Payload:

```json
{
  "schedule_item_id": "uuid",
  "schedule_type": "OPERATION",
  "operation_instance_id": "uuid",
  "start_at": "datetime",
  "end_at": "datetime"
}
```

---

## `scheduling.resource_assigned`

Payload:

```json
{
  "schedule_item_id": "uuid",
  "resource_type": "EMPLOYEE",
  "resource_id": "uuid",
  "allocation_percentage": 100
}
```

---

## `scheduling.conflict_detected`

Payload:

```json
{
  "schedule_item_id": "uuid",
  "resource_type": "MACHINE",
  "resource_id": "uuid",
  "conflicting_schedule_item_ids": [
    "uuid"
  ]
}
```

---

## `scheduling.item_rescheduled`

Payload:

```json
{
  "schedule_item_id": "uuid",
  "previous_start_at": "datetime",
  "previous_end_at": "datetime",
  "new_start_at": "datetime",
  "new_end_at": "datetime"
}
```

---

## `scheduling.item_cancelled`

Payload:

```json
{
  "schedule_item_id": "uuid",
  "reason_code": "PRODUCTION_ORDER_CANCELLED"
}
```

---

# 28. Incident Events

## `incident.created`

Payload:

```json
{
  "incident_id": "uuid",
  "incident_type": "MATERIAL_SHORTAGE",
  "severity": "HIGH",
  "workflow_instance_id": "uuid",
  "operation_instance_id": "uuid",
  "reported_by_employee_id": "uuid",
  "description": "Falta material para continuar"
}
```

---

## `incident.assigned`

Payload:

```json
{
  "incident_id": "uuid",
  "assigned_sector_id": "uuid",
  "assigned_user_id": "uuid"
}
```

---

## `incident.acknowledged`

Payload:

```json
{
  "incident_id": "uuid",
  "acknowledged_by_user_id": "uuid",
  "acknowledged_at": "datetime"
}
```

---

## `incident.responded`

Payload:

```json
{
  "incident_id": "uuid",
  "response": "Material será entregue amanhã",
  "responded_by_user_id": "uuid"
}
```

---

## `incident.resolved`

Payload:

```json
{
  "incident_id": "uuid",
  "resolution": "Material entregue ao setor",
  "resolved_at": "datetime"
}
```

---

## `incident.escalated`

Payload:

```json
{
  "incident_id": "uuid",
  "previous_severity": "NORMAL",
  "new_severity": "CRITICAL",
  "reason": "Produção bloqueada"
}
```

---

# 29. Notification Events

## `notifications.notification_created`

Payload:

```json
{
  "notification_id": "uuid",
  "notification_type": "MATERIAL_SHORTAGE",
  "recipient_type": "SECTOR",
  "recipient_id": "uuid",
  "channels": [
    "PUSH",
    "DESKTOP"
  ]
}
```

---

## `notifications.notification_sent`

Payload:

```json
{
  "notification_id": "uuid",
  "channel": "PUSH",
  "sent_at": "datetime"
}
```

---

## `notifications.notification_delivered`

Payload:

```json
{
  "notification_id": "uuid",
  "channel": "PUSH",
  "delivered_at": "datetime"
}
```

---

## `notifications.notification_failed`

Payload:

```json
{
  "notification_id": "uuid",
  "channel": "PUSH",
  "error_code": "INVALID_DEVICE_TOKEN"
}
```

---

## `notifications.notification_read`

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "read_at": "datetime"
}
```

---

# 30. Financial Events

## `financial.receivable_created`

Payload:

```json
{
  "receivable_id": "uuid",
  "customer_id": "uuid",
  "contract_id": "uuid",
  "amount": "13500.00",
  "due_date": "date"
}
```

---

## `financial.receivable_paid`

Payload:

```json
{
  "receivable_id": "uuid",
  "payment_id": "uuid",
  "paid_amount": "13500.00",
  "paid_at": "datetime"
}
```

---

## `financial.receivable_overdue`

Payload:

```json
{
  "receivable_id": "uuid",
  "customer_id": "uuid",
  "due_date": "date",
  "outstanding_amount": "13500.00"
}
```

---

## `financial.payable_created`

Payload:

```json
{
  "payable_id": "uuid",
  "purchase_order_id": "uuid",
  "supplier_id": "uuid",
  "amount": "1500.00",
  "due_date": "date"
}
```

---

## `financial.payable_paid`

Payload:

```json
{
  "payable_id": "uuid",
  "payment_id": "uuid",
  "paid_amount": "1500.00",
  "paid_at": "datetime"
}
```

---

## `financial.cash_transaction_created`

Payload:

```json
{
  "financial_transaction_id": "uuid",
  "transaction_type": "OUTFLOW",
  "amount": "1500.00",
  "cost_center_id": "uuid"
}
```

---

# 31. Fiscal Events

## `fiscal.document_created`

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "document_type": "INVOICE",
  "reference_type": "SALES_ORDER",
  "reference_id": "uuid"
}
```

---

## `fiscal.document_authorized`

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "authorization_key": "masked",
  "authorized_at": "datetime"
}
```

---

## `fiscal.document_rejected`

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "rejection_code": "VALIDATION_ERROR",
  "message": "Documento rejeitado"
}
```

---

## `fiscal.document_cancelled`

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "cancelled_at": "datetime",
  "reason": "Operação cancelada"
}
```

---

# 32. Configuration Events

## `configuration.definition_created`

Payload:

```json
{
  "configuration_definition_id": "uuid",
  "key": "production.allow_parallel_execution",
  "value_type": "BOOLEAN",
  "default_value": true
}
```

---

## `configuration.value_changed`

Payload:

```json
{
  "configuration_definition_id": "uuid",
  "scope_type": "TENANT",
  "scope_id": "uuid",
  "previous_value": true,
  "new_value": false
}
```

---

## `configuration.feature_pack_enabled`

Payload:

```json
{
  "feature_pack_id": "uuid",
  "tenant_id": "uuid",
  "capability_codes": [
    "production_execution",
    "documents"
  ]
}
```

---

## `configuration.feature_pack_disabled`

Payload:

```json
{
  "feature_pack_id": "uuid",
  "tenant_id": "uuid",
  "reason": "Plano encerrado"
}
```

---

## `configuration.capability_enabled`

Payload:

```json
{
  "tenant_capability_id": "uuid",
  "capability_code": "inventory",
  "configuration": {}
}
```

---

## `configuration.capability_disabled`

Payload:

```json
{
  "tenant_capability_id": "uuid",
  "capability_code": "inventory"
}
```

---

# 33. Automation Events

## `automation.rule_created`

Payload:

```json
{
  "automation_rule_id": "uuid",
  "code": "NOTIFY_MATERIAL_SHORTAGE",
  "trigger_event_type": "inventory.stock_reservation_failed"
}
```

---

## `automation.execution_started`

Payload:

```json
{
  "automation_execution_id": "uuid",
  "automation_rule_id": "uuid",
  "source_event_id": "uuid"
}
```

---

## `automation.execution_completed`

Payload:

```json
{
  "automation_execution_id": "uuid",
  "automation_rule_id": "uuid",
  "actions_executed": 2
}
```

---

## `automation.execution_failed`

Payload:

```json
{
  "automation_execution_id": "uuid",
  "automation_rule_id": "uuid",
  "error_code": "ACTION_FAILED"
}
```

---

# 34. AI Events

## `ai.conversation_created`

Payload:

```json
{
  "conversation_id": "uuid",
  "user_id": "uuid",
  "assistant_profile": "PRODUCTION_ASSISTANT",
  "context_entity_type": "PRODUCTION_ORDER",
  "context_entity_id": "uuid"
}
```

---

## `ai.response_generated`

Payload:

```json
{
  "conversation_id": "uuid",
  "message_id": "uuid",
  "assistant_profile": "PRODUCTION_ASSISTANT",
  "citation_count": 3
}
```

Não incluir o conteúdo integral quando contiver dados sensíveis.

---

## `ai.command_proposed`

Payload:

```json
{
  "conversation_id": "uuid",
  "proposed_command_type": "PauseExecutionCommand",
  "target_entity_id": "uuid",
  "requires_confirmation": true
}
```

---

## `ai.command_confirmed`

Payload:

```json
{
  "conversation_id": "uuid",
  "proposed_command_id": "uuid",
  "confirmed_by_user_id": "uuid"
}
```

---

## `ai.command_rejected`

Payload:

```json
{
  "conversation_id": "uuid",
  "proposed_command_id": "uuid",
  "rejected_by_user_id": "uuid"
}
```

---

## `ai.tool_execution_failed`

Payload:

```json
{
  "conversation_id": "uuid",
  "tool_name": "production.get_order",
  "error_code": "PERMISSION_DENIED"
}
```

---

# 35. Analytics Events

Analytics utiliza principalmente eventos dos outros contextos.

Eventos próprios:

## `analytics.projection_updated`

Payload:

```json
{
  "projection_name": "production_operation_metrics",
  "source_event_id": "uuid",
  "updated_at": "datetime"
}
```

---

## `analytics.projection_rebuilt`

Payload:

```json
{
  "projection_name": "production_operation_metrics",
  "period_start": "datetime",
  "period_end": "datetime",
  "record_count": 1000
}
```

---

## `analytics.kpi_threshold_reached`

Payload:

```json
{
  "kpi_code": "REWORK_RATE",
  "current_value": "12.5",
  "threshold_value": "10.0",
  "comparison": "GREATER_THAN"
}
```

---

# 36. Search Events

## `search.document_indexed`

Payload:

```json
{
  "document_id": "uuid",
  "document_version_id": "uuid",
  "index_version": 1
}
```

---

## `search.entity_indexed`

Payload:

```json
{
  "entity_type": "CUSTOMER",
  "entity_id": "uuid",
  "index_version": 1
}
```

---

## `search.indexing_failed`

Payload:

```json
{
  "entity_type": "DOCUMENT",
  "entity_id": "uuid",
  "error_code": "CONTENT_EXTRACTION_FAILED"
}
```

---

# 37. Synchronization Events

## `sync.command_received`

Payload:

```json
{
  "command_id": "uuid",
  "idempotency_key": "string",
  "device_id": "uuid",
  "command_type": "StartExecutionCommand"
}
```

---

## `sync.command_processed`

Payload:

```json
{
  "command_id": "uuid",
  "idempotency_key": "string",
  "result": "SUCCESS"
}
```

---

## `sync.command_rejected`

Payload:

```json
{
  "command_id": "uuid",
  "idempotency_key": "string",
  "error_code": "CONCURRENCY_CONFLICT"
}
```

---

## `sync.conflict_detected`

Payload:

```json
{
  "command_id": "uuid",
  "entity_type": "OPERATION_EXECUTION",
  "entity_id": "uuid",
  "client_version": 2,
  "server_version": 3
}
```

---

## `sync.device_synchronized`

Payload:

```json
{
  "device_id": "uuid",
  "user_id": "uuid",
  "synchronized_at": "datetime",
  "processed_command_count": 15
}
```

---

# 38. System Events

## `system.application_started`

Payload:

```json
{
  "service": "organizeg3-api",
  "version": "0.1.0",
  "environment": "production"
}
```

## `system.application_stopped`

Payload:

```json
{
  "service": "organizeg3-api",
  "reason": "GRACEFUL_SHUTDOWN"
}
```

## `system.database_connection_failed`

Payload:

```json
{
  "service": "organizeg3-api",
  "database_role": "OPERATIONAL",
  "error_code": "CONNECTION_TIMEOUT"
}
```

## `system.background_job_failed`

Payload:

```json
{
  "job_name": "outbox_publisher",
  "execution_id": "uuid",
  "error_code": "PUBLISH_FAILED"
}
```

Eventos técnicos críticos poderão gerar alertas, mas não deverão carregar stack traces no payload.

---

# 39. Eventos exibidos na Timeline

Eventos candidatos à Timeline:

* `commercial.quotation_created`;
* `commercial.quotation_sent`;
* `commercial.quotation_approved`;
* `workflow.stage_changed`;
* `workflow.instance_completed`;
* `production.operation_assigned`;
* `production.execution_started`;
* `production.execution_paused`;
* `production.execution_resumed`;
* `production.execution_finished`;
* `production.rework_requested`;
* `production.material_requested`;
* `forms.submission_completed`;
* `documents.version_uploaded`;
* `incident.created`;
* `incident.responded`;
* `incident.resolved`;
* `quality.nonconformity_created`;
* `quality.rework_required`;
* `inventory.stock_reservation_failed`;
* `purchasing.material_received`;
* `maintenance.machine_unavailable`;
* `maintenance.machine_released`.

A Timeline poderá transformar o evento em uma mensagem amigável.

Exemplo:

Evento:

```text
production.execution_paused
```

Timeline:

```text
João pausou a operação “Corte da estrutura” por falta de material.
```

---

# 40. Eventos que podem gerar notificações

Eventos inicialmente notificáveis:

```text
commercial.quotation_approved
workflow.stage_changed
production.operation_assigned
production.execution_paused
production.material_requested
production.rework_requested
inventory.stock_reservation_failed
purchasing.material_received
quality.nonconformity_created
quality.rework_required
maintenance.machine_unavailable
maintenance.machine_released
incident.created
incident.escalated
financial.receivable_overdue
```

A geração de notificação será configurável.

---

# 41. Eventos destinados ao Analytics

Eventos operacionais relevantes deverão alimentar projeções.

Prioridade inicial:

```text
commercial.quotation_created
commercial.quotation_approved
workflow.stage_changed
production.execution_started
production.execution_paused
production.execution_resumed
production.execution_finished
production.rework_requested
inventory.material_consumed
inventory.stock_adjusted
purchasing.material_received
quality.nonconformity_created
maintenance.machine_unavailable
financial.receivable_paid
financial.payable_paid
```

---

# 42. Eventos críticos

São considerados críticos:

* autenticação suspeita;
* alteração de permissões;
* aprovação de orçamento;
* assinatura de contrato;
* início e conclusão de produção;
* movimentação de estoque;
* retrabalho;
* não conformidade;
* pagamentos;
* documentos fiscais;
* alteração de configurações críticas;
* ação executada por IA;
* falha de integração;
* conflito de sincronização.

Eventos críticos devem possuir:

* persistência confirmada;
* auditoria;
* `correlation_id`;
* ator;
* origem;
* versionamento;
* proteção contra exclusão.

---

# 43. Eventos e automações

Uma regra de automação poderá declarar:

```json
{
  "trigger_event_type": "inventory.stock_reservation_failed",
  "conditions": {
    "shortage_quantity": {
      "greater_than": 0
    }
  },
  "actions": [
    {
      "type": "CREATE_PURCHASE_REQUEST"
    },
    {
      "type": "SEND_NOTIFICATION"
    }
  ]
}
```

Automações não alteram diretamente o banco.

Elas executam comandos oficiais.

---

# 44. Eventos e IA

A IA poderá:

* consultar eventos autorizados;
* resumir Timeline;
* explicar atrasos;
* identificar padrões;
* sugerir ações;
* preparar comandos.

A IA não poderá:

* modificar eventos;
* esconder eventos;
* publicar eventos falsos;
* criar fatos sem executar comando oficial;
* acessar eventos sem permissão.

---

# 45. Eventos offline

Comandos realizados offline deverão preservar:

```text
command_id
idempotency_key
device_id
client_occurred_at
client_sequence
contract_version
```

Quando processados, os eventos utilizarão:

* `occurred_at`: horário validado do fato;
* `recorded_at`: horário do servidor;
* metadado de origem offline.

Exemplo:

```json
{
  "metadata": {
    "offline": true,
    "offline_command_id": "uuid",
    "client_occurred_at": "datetime",
    "device_id": "uuid"
  }
}
```

---

# 46. Erros de processamento

Falhas de consumidor deverão registrar:

```text
consumer_name
event_id
attempt
error_code
error_message_safe
next_retry_at
dead_lettered_at
```

Após o limite de tentativas, o evento poderá ser encaminhado para Dead Letter Queue.

O evento original não é alterado.

---

# 47. Retenção

Eventos operacionais deverão ser preservados enquanto houver obrigação legal, contratual ou valor histórico.

A política de retenção poderá variar por categoria, mas deverá considerar:

* LGPD;
* documentos fiscais;
* auditoria;
* contratos;
* movimentações financeiras;
* histórico de produção;
* garantia;
* rastreabilidade.

Excluir informações pessoais de eventos exige processo específico de anonimização, não alteração arbitrária.

---

# 48. Checklist para criação de novo evento

Antes de adicionar um evento, responder:

1. O fato realmente aconteceu?
2. O evento é relevante para o domínio?
3. Qual agregado publica?
4. Qual contexto é proprietário?
5. Quem consumirá?
6. O evento precisa ser público entre contextos?
7. Qual é o payload mínimo?
8. Há dados sensíveis?
9. Deve aparecer na Timeline?
10. Deve gerar notificação?
11. Deve alimentar Analytics?
12. Deve disparar automação?
13. Precisa funcionar offline?
14. Qual será o `schema_version`?
15. O evento é idempotente para consumidores?
16. Existe outro evento com a mesma semântica?
17. O nome está no passado?
18. A auditoria correspondente foi considerada?

---

# 49. Critérios de conformidade

Um evento estará em conformidade quando:

* possuir nome oficial;
* representar fato concluído;
* utilizar envelope padrão;
* possuir Tenant;
* possuir agregado;
* possuir sequência;
* possuir versão;
* possuir ator quando aplicável;
* possuir `correlation_id`;
* possuir payload mínimo;
* não conter segredos;
* ser append-only;
* ser publicado após a transação;
* usar Outbox quando houver consumidores externos;
* possuir consumidores idempotentes;
* estar documentado neste catálogo;
* possuir testes de contrato.

---

# 50. Conclusão

Os eventos são a memória operacional do OrganizeG3.

Eles permitem:

* rastreabilidade;
* Timeline;
* automações;
* notificações;
* sincronização;
* integrações;
* Analytics;
* Inteligência Artificial;
* explicação de decisões;
* reconstrução de contexto.

Um evento deve ser tratado como contrato duradouro da plataforma.

Sua criação exige clareza semântica, versionamento, segurança e responsabilidade definida.
