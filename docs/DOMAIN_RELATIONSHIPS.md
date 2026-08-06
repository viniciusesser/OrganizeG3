# OrganizeG3 — Domain Relationships

> Especificação oficial de relacionamentos entre os contextos de domínio do OrganizeG3.

---

| Propriedade            | Valor                   |
| ---------------------- | ----------------------- |
| Documento              | DOMAIN_RELATIONSHIPS.md |
| Versão                 | 1.0.0                   |
| Status                 | Baseline arquitetural   |
| Abrangência            | Toda a plataforma       |
| Depende de             | DOMAIN_ARCHITECTURE.md  |
| Idioma da documentação | Português               |
| Idioma do código       | Inglês                  |

---

# 1. Objetivo

Este documento define:

* os limites dos contextos de domínio;
* os agregados principais;
* as relações entre agregados;
* os identificadores compartilhados;
* as cardinalidades conceituais;
* os eventos de integração;
* as dependências permitidas;
* as dependências proibidas;
* os responsáveis por cada informação;
* os fluxos entre os módulos da plataforma.

Seu objetivo é impedir que o OrganizeG3 evolua como um conjunto de tabelas e telas acopladas.

Toda nova entidade, caso de uso, evento, API ou integração deverá respeitar os limites definidos neste documento.

---

# 2. Princípios de relacionamento

## 2.1 Cada informação possui um proprietário

Uma informação deverá possuir apenas um contexto responsável por sua criação, validação e alteração.

Exemplos:

* usuário pertence ao contexto Identity;
* funcionário pertence ao contexto Organization;
* cliente pertence ao contexto CRM;
* orçamento pertence ao contexto Commercial;
* definição de workflow pertence ao contexto Workflow;
* execução produtiva pertence ao contexto Production;
* saldo de estoque pertence ao contexto Inventory;
* documento pertence ao contexto Documents.

Outros contextos poderão referenciar essas informações por identificador, mas não deverão assumir sua propriedade.

---

## 2.2 Referências entre contextos utilizam identificadores

Agregados de contextos diferentes devem ser relacionados principalmente por identificadores.

Exemplo:

```text
ProductionOrder
    customer_id
    quotation_id
    workflow_instance_id
```

O agregado `ProductionOrder` não deve incorporar internamente toda a estrutura de `Customer`, `Quotation` ou `WorkflowInstance`.

---

## 2.3 Relacionamento não significa dependência de implementação

Um contexto pode utilizar informações de outro contexto sem importar suas implementações internas.

A comunicação poderá ocorrer por:

* portas da Application Layer;
* queries autorizadas;
* contratos públicos;
* eventos de integração;
* projeções de leitura;
* APIs internas.

---

## 2.4 Eventos representam fatos, não ordens

Um evento informa algo que já aconteceu.

Exemplo:

```text
quotation.approved
```

Ele não significa:

```text
create.production.order
```

A reação ao evento pertence ao consumidor.

---

## 2.5 Comandos possuem um único responsável

Um comando deverá ser executado pelo contexto proprietário da ação.

Exemplos:

```text
ApproveQuotationCommand
StartExecutionCommand
ReserveMaterialCommand
UploadDocumentVersionCommand
```

Um contexto não deverá alterar diretamente os agregados pertencentes a outro.

---

## 2.6 Transações não devem atravessar contextos arbitrariamente

Uma transação deve permanecer, preferencialmente, dentro de um único agregado.

Quando um fluxo envolver múltiplos contextos:

1. o contexto inicial confirma sua transação;
2. publica um evento através do Outbox;
3. os demais contextos processam o evento;
4. falhas são tratadas de maneira explícita;
5. operações devem ser idempotentes.

---

# 3. Mapa geral de contextos

```text
                              Identity
                                  │
                                  │ autentica
                                  ▼
                            Organization
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
               CRM           Configuration     Notifications
                │                 │                 ▲
                ▼                 ▼                 │
            Commercial ───────► Workflow ──────────┤
                │                 │                 │
                │                 ▼                 │
                └────────────► Production ──────────┤
                                  │                 │
                       ┌──────────┼──────────┐      │
                       ▼          ▼          ▼      │
                  Engineering  Inventory  Quality   │
                       │          │          │      │
                       │          ▼          │      │
                       └─────► Purchasing ◄──┘      │
                                  │                 │
                                  ▼                 │
                              Financial ────────────┘
                                  │
                                  ▼
                                Fiscal

Todos os contextos:
    ├── publicam eventos;
    ├── geram auditoria;
    ├── podem vincular documentos;
    ├── podem alimentar Analytics;
    └── podem ser consultados pela AI Layer com autorização.
```

---

# 4. Contexto Identity

## 4.1 Responsabilidade

Identity é responsável por:

* autenticação;
* credenciais;
* sessões;
* tokens;
* dispositivos autenticados;
* histórico de acesso;
* identidade global do usuário.

## 4.2 Agregado principal

```text
User
    ├── UserSession
    ├── AuthenticationIdentity
    ├── TrustedDevice
    └── LoginHistory
```

## 4.3 Relações externas

```text
User 1 ─── N TenantMembership
User 0..1 ─── 1 Employee por Tenant
User N ─── N Role por Membership
```

Identity não é responsável pelo cargo, setor ou vínculo trabalhista da pessoa.

Essas informações pertencem a Organization.

## 4.4 Eventos publicados

```text
identity.user_created
identity.user_authenticated
identity.authentication_failed
identity.session_revoked
identity.device_registered
identity.password_changed
identity.user_blocked
```

## 4.5 Eventos consumidos

```text
organization.membership_disabled
organization.employee_terminated
tenant.suspended
```

## 4.6 Dependências permitidas

Identity poderá consultar:

* status do Tenant;
* status do Membership;
* políticas de autenticação;
* permissões efetivas.

## 4.7 Dependências proibidas

Identity não deverá:

* alterar funcionário;
* alterar filial;
* definir cargo;
* criar orçamento;
* movimentar workflow;
* acessar dados produtivos.

---

# 5. Contexto Organization

## 5.1 Responsabilidade

Organization representa a estrutura da empresa.

## 5.2 Agregados principais

```text
Tenant
    ├── Branch
    ├── Sector
    ├── CostCenter
    └── OrganizationPolicy
```

```text
Employee
    ├── EmployeeAssignment
    ├── EmployeeSkill
    ├── EmployeeAvailability
    └── EmployeeStatusHistory
```

```text
TenantMembership
    ├── MembershipRole
    └── MembershipScope
```

## 5.3 Relações internas

```text
Tenant 1 ─── N Branch
Branch 1 ─── N Sector
Sector 0..1 ─── N ChildSector
Tenant 1 ─── N Employee
Employee 0..1 ─── 1 User
Employee N ─── 1 Branch
Employee N ─── 0..1 Sector
```

Filiais e setores são opcionais.

Uma empresa poderá operar:

* sem filiais;
* sem estoque por setor;
* com apenas uma unidade;
* com múltiplas unidades;
* com setores hierárquicos.

## 5.4 Relações externas

Organization fornece referências para:

* Production;
* Inventory;
* Purchasing;
* Financial;
* Workflow;
* Notifications;
* Scheduling;
* Audit.

## 5.5 Eventos publicados

```text
organization.tenant_created
organization.branch_created
organization.sector_created
organization.employee_created
organization.employee_assigned
organization.employee_transferred
organization.employee_terminated
organization.membership_created
organization.membership_disabled
```

## 5.6 Dependências proibidas

Organization não deverá:

* armazenar credenciais;
* calcular saldo de estoque;
* controlar execução de operação;
* aprovar orçamento;
* emitir documento fiscal.

---

# 6. Contexto Authorization

Embora relacionado a Identity e Organization, a autorização é uma capacidade transversal.

## 6.1 Agregados principais

```text
Role
    └── RolePermission
```

```text
Permission
```

```text
Membership
    └── AssignedRole
```

## 6.2 Relações

```text
Tenant 1 ─── N Role
Role N ─── N Permission
Membership N ─── N Role
Permission N ─── 1 Capability
```

## 6.3 Escopos

Permissões poderão ser restringidas por:

* Tenant;
* Branch;
* Sector;
* entidade atribuída;
* operação própria;
* equipe;
* papel administrativo.

Exemplo:

```text
production.execution.start
scope:
    assigned_only = true
```

## 6.4 Regra fundamental

A interface nunca será a barreira de segurança.

Toda ação deverá ser validada na Application Layer e reforçada no banco por RLS quando aplicável.

---

# 7. Contexto CRM

## 7.1 Responsabilidade

CRM representa relacionamentos comerciais.

## 7.2 Agregados principais

```text
Customer
    ├── CustomerContact
    ├── CustomerAddress
    ├── CustomerNote
    └── CustomerRelationshipHistory
```

```text
Lead
    ├── LeadContact
    ├── LeadInteraction
    └── LeadQualification
```

```text
Opportunity
```

```text
SupplierProfile
```

O cadastro operacional de fornecedor poderá ser compartilhado com Purchasing através de contrato público, mas sua gestão comercial permanece no contexto responsável.

## 7.3 Relações

```text
Lead 0..1 ─── 1 Customer após conversão
Customer 1 ─── N Opportunity
Customer 1 ─── N Quotation
Customer 1 ─── N Contract
Customer 1 ─── N WorkflowInstance
```

## 7.4 Eventos publicados

```text
crm.lead_created
crm.lead_qualified
crm.lead_converted
crm.customer_created
crm.customer_updated
crm.opportunity_created
crm.opportunity_won
crm.opportunity_lost
```

## 7.5 Eventos consumidos

```text
commercial.quotation_sent
commercial.quotation_approved
commercial.contract_signed
financial.receivable_overdue
production.order_completed
```

## 7.6 Dependências proibidas

CRM não deverá:

* calcular orçamento;
* movimentar produção;
* reservar estoque;
* criar lançamentos financeiros diretamente.

---

# 8. Contexto Commercial

## 8.1 Responsabilidade

Commercial controla propostas, orçamentos, contratos e pedidos comerciais.

## 8.2 Agregados principais

```text
Quotation
    ├── QuotationVersion
    ├── QuotationItem
    ├── QuotationCondition
    ├── QuotationAdjustment
    └── QuotationApproval
```

```text
Contract
    ├── ContractVersion
    ├── ContractClause
    └── ContractSignature
```

```text
SalesOrder
    └── SalesOrderItem
```

## 8.3 Versionamento obrigatório

Um orçamento aprovado não poderá ser alterado silenciosamente.

Estrutura:

```text
Quotation
    current_version_number
    status

QuotationVersion
    version_number
    snapshot
    created_at
    created_by
    change_reason
```

## 8.4 Relações

```text
Customer 1 ─── N Quotation
Quotation 1 ─── N QuotationVersion
Quotation 0..1 ─── 1 Contract
Quotation 0..1 ─── 1 SalesOrder
SalesOrder 0..1 ─── 1 ProductionOrder
Quotation 0..1 ─── N Document
```

## 8.5 Eventos publicados

```text
commercial.quotation_created
commercial.quotation_version_created
commercial.quotation_sent
commercial.quotation_approved
commercial.quotation_rejected
commercial.quotation_archived
commercial.contract_created
commercial.contract_signed
commercial.sales_order_created
```

## 8.6 Eventos consumidos

```text
crm.customer_created
document.version_uploaded
financial.payment_confirmed
```

## 8.7 Integração com Workflow

O funil comercial utiliza `WorkflowInstance`.

A saída configurada do Workflow comercial poderá iniciar:

* ProductionOrder;
* novo Workflow produtivo;
* Contract;
* SalesOrder;
* solicitação administrativa.

A reação deverá ser configurável.

---

# 9. Contexto Workflow

## 9.1 Responsabilidade

Workflow representa processos configuráveis.

Kanban é apenas uma forma de visualização.

## 9.2 Agregados principais

```text
WorkflowDefinition
    ├── WorkflowVersion
    │   ├── StageDefinition
    │   ├── TransitionDefinition
    │   └── OperationDefinition
    └── CurrentPublishedVersion
```

```text
WorkflowInstance
    ├── CurrentStage
    ├── StageHistory
    ├── WorkflowAssignment
    └── DynamicData
```

## 9.3 Relações

```text
Tenant 1 ─── N WorkflowDefinition
WorkflowDefinition 1 ─── N WorkflowVersion
WorkflowVersion 1 ─── N StageDefinition
WorkflowVersion 1 ─── N TransitionDefinition
WorkflowDefinition 1 ─── N WorkflowInstance
WorkflowInstance N ─── 1 PublishedWorkflowVersion
WorkflowInstance N ─── 1 CurrentStage
```

## 9.4 Tipos de workflow

```text
SALES
PRODUCTION
PURCHASE
INVENTORY
FINANCIAL
QUALITY
MAINTENANCE
SUPPORT
CUSTOM
```

## 9.5 Regras

Uma versão publicada é imutável.

Alterações geram nova versão.

Instâncias existentes continuam vinculadas à versão que as originou, salvo processo explícito de migração.

## 9.6 Eventos publicados

```text
workflow.definition_created
workflow.version_published
workflow.instance_created
workflow.stage_changed
workflow.instance_paused
workflow.instance_completed
workflow.instance_cancelled
workflow.stage_skipped
workflow.instance_returned
```

## 9.7 Relações externas

`WorkflowInstance` poderá referenciar:

* Customer;
* Quotation;
* Contract;
* ProductionOrder;
* PurchaseRequest;
* MaintenanceOrder;
* QualityInspection;
* entidade customizada.

Essas relações deverão utilizar referências explícitas e autorizadas.

## 9.8 Dependências proibidas

Workflow não deverá:

* executar diretamente tarefas produtivas;
* controlar saldo de estoque;
* armazenar documentos físicos;
* calcular valores financeiros;
* assumir regras específicas de marcenaria.

---

# 10. Contexto Production

## 10.1 Responsabilidade

Production controla o trabalho executado.

## 10.2 Agregados principais

```text
ProductionOrder
    ├── ProductionOrderItem
    ├── ProductionRequirement
    └── ProductionStatusHistory
```

```text
OperationInstance
    ├── OperationAssignment
    ├── OperationExecution
    │   ├── ExecutionParticipant
    │   ├── ExecutionPause
    │   └── ExecutionMachine
    ├── OperationChecklist
    └── ReworkReference
```

## 10.3 Relações

```text
ProductionOrder 1 ─── N OperationInstance
OperationInstance 1 ─── N OperationExecution
OperationExecution 1 ─── N ExecutionParticipant
OperationExecution 1 ─── N ExecutionPause
OperationExecution N ─── N Machine
OperationInstance 0..1 ─── N ReworkOperation
```

## 10.4 Relação com Workflow

```text
ProductionOrder 1 ─── 1 WorkflowInstance
```

A instância do Workflow indica o estado geral do processo.

As operações representam o trabalho real.

Uma etapa poderá possuir várias operações.

Uma operação poderá ser executada várias vezes.

## 10.5 Trabalho parcial

Uma operação poderá:

* iniciar;
* pausar;
* retomar;
* finalizar parcialmente;
* gerar nova execução;
* ter mais de um funcionário;
* utilizar máquina;
* ser repetida;
* gerar retrabalho;
* ser ignorada com justificativa.

Exemplo:

```text
Corte da estrutura
    ↓
Montagem da estrutura
    ↓
Corte dos fundos
    ↓
Montagem dos fundos
    ↓
Corte do tamponamento
    ↓
Montagem do tamponamento
```

O Workflow geral poderá permanecer na mesma etapa enquanto várias operações ocorrem.

## 10.6 Tempo

O sistema deverá registrar separadamente:

* tempo trabalhado;
* tempo pausado;
* motivo da pausa;
* participante;
* máquina;
* horário de entrada;
* horário de saída;
* interrupções;
* ajuda em outra operação.

## 10.7 Eventos publicados

```text
production.order_created
production.operation_created
production.operation_assigned
production.execution_started
production.execution_paused
production.execution_resumed
production.execution_finished
production.operation_skipped
production.rework_requested
production.order_completed
```

## 10.8 Eventos consumidos

```text
commercial.quotation_approved
workflow.stage_changed
inventory.material_reserved
inventory.material_unavailable
quality.nonconformity_created
maintenance.machine_unavailable
```

---

# 11. Contexto Engineering

## 11.1 Responsabilidade

Engineering representa especificações técnicas de produtos, projetos e estruturas.

## 11.2 Agregados principais

```text
ProductDefinition
    ├── ProductRevision
    ├── BillOfMaterials
    ├── RoutingReference
    └── TechnicalSpecification
```

```text
ProjectDefinition
    ├── ProjectRevision
    ├── ProjectComponent
    └── TechnicalRequirement
```

## 11.3 Relações

```text
ProductDefinition 1 ─── N ProductRevision
ProductRevision 1 ─── N BOMItem
ProductRevision 0..1 ─── N Document
ProductionOrder N ─── 1 ProductRevision ou ProjectRevision
```

## 11.4 Regras

Uma ordem produtiva deve manter referência à revisão utilizada.

Uma revisão posterior não deve modificar automaticamente ordens existentes.

## 11.5 Arquivos pesados

Arquivos como:

* SKP;
* DWG;
* RVT;
* CNC;
* arquivos nativos de máquinas;

não serão armazenados no Storage padrão, salvo configuração futura específica.

O sistema poderá armazenar:

* PDF;
* imagens;
* planos de corte exportados;
* documentação técnica;
* planilhas permitidas.

---

# 12. Contexto Inventory

## 12.1 Responsabilidade

Inventory controla disponibilidade e movimentação de materiais.

## 12.2 Agregados principais

```text
Material
    ├── MaterialSpecification
    └── MaterialUnit
```

```text
StockLocation
```

```text
StockBalance
```

```text
StockMovement
```

```text
StockReservation
```

## 12.3 Relações

```text
Tenant 1 ─── N StockLocation
Branch 0..1 ─── N StockLocation
Sector 0..1 ─── N StockLocation
StockLocation N ─── N Material por StockBalance
ProductionOrder 1 ─── N StockReservation
StockMovement N ─── 1 Material
```

## 12.4 Configurabilidade

A empresa poderá utilizar:

* estoque único;
* estoque por filial;
* estoque por setor;
* estoque por almoxarifado;
* localização interna;
* nenhuma separação física.

A existência de filiais ou estoques separados não será obrigatória.

## 12.5 Eventos publicados

```text
inventory.material_created
inventory.stock_received
inventory.stock_reserved
inventory.reservation_failed
inventory.stock_released
inventory.material_consumed
inventory.stock_adjusted
inventory.reorder_point_reached
```

## 12.6 Eventos consumidos

```text
production.material_requested
production.order_cancelled
purchasing.material_received
quality.material_rejected
```

---

# 13. Contexto Purchasing

## 13.1 Responsabilidade

Purchasing controla solicitações e aquisições.

## 13.2 Agregados principais

```text
PurchaseRequest
    └── PurchaseRequestItem
```

```text
SupplierQuotation
    └── SupplierQuotationItem
```

```text
PurchaseOrder
    ├── PurchaseOrderItem
    └── PurchaseApproval
```

## 13.3 Fluxo de falta de material

```text
Funcionário registra falta
    ↓
Production publica material.requested
    ↓
Inventory recebe solicitação
    ↓
Inventory verifica disponibilidade
    ↓
Se disponível:
    reserva material
    responde produção
    ↓
Se indisponível:
    cria necessidade de compra
    ↓
Purchasing processa solicitação
    ↓
Administrador acompanha todo o fluxo
```

## 13.4 Relações

```text
PurchaseRequest 1 ─── N PurchaseRequestItem
PurchaseRequest 0..1 ─── N SupplierQuotation
SupplierQuotation 0..1 ─── 1 PurchaseOrder
PurchaseOrder N ─── 1 Supplier
PurchaseOrderItem N ─── 1 Material
```

## 13.5 Eventos publicados

```text
purchasing.request_created
purchasing.request_approved
purchasing.supplier_quotation_received
purchasing.purchase_order_created
purchasing.purchase_order_approved
purchasing.material_received
purchasing.purchase_cancelled
```

## 13.6 Eventos consumidos

```text
inventory.reservation_failed
inventory.reorder_point_reached
production.material_requested
quality.material_rejected
```

---

# 14. Contexto Quality

## 14.1 Responsabilidade

Quality controla inspeções, não conformidades e ações corretivas.

## 14.2 Agregados principais

```text
QualityInspection
    ├── InspectionItem
    ├── InspectionResult
    └── InspectionEvidence
```

```text
NonConformity
    ├── NonConformityCause
    ├── CorrectiveAction
    └── PreventiveAction
```

## 14.3 Relações

```text
OperationExecution 0..1 ─── N QualityInspection
ProductionOrder 0..1 ─── N NonConformity
MaterialReceipt 0..1 ─── N QualityInspection
NonConformity 0..1 ─── N ReworkOperation
```

## 14.4 Eventos publicados

```text
quality.inspection_requested
quality.inspection_completed
quality.nonconformity_created
quality.rework_required
quality.material_rejected
quality.corrective_action_completed
```

## 14.5 Eventos consumidos

```text
production.execution_finished
purchasing.material_received
maintenance.machine_repaired
```

---

# 15. Contexto Maintenance

## 15.1 Responsabilidade

Maintenance controla máquinas, equipamentos e manutenção.

## 15.2 Agregados principais

```text
Equipment
    ├── MaintenancePlan
    ├── MaintenanceHistory
    └── EquipmentStatus
```

```text
MaintenanceOrder
    ├── MaintenanceTask
    ├── MaintenanceExecution
    └── MaintenanceMaterial
```

## 15.3 Relações

```text
Machine 1 ─── 1 Equipment
Equipment 1 ─── N MaintenanceOrder
MaintenanceOrder 0..1 ─── 1 WorkflowInstance
ExecutionMachine N ─── 1 Machine
```

## 15.4 Eventos publicados

```text
maintenance.machine_unavailable
maintenance.order_created
maintenance.execution_started
maintenance.execution_finished
maintenance.machine_released
maintenance.preventive_due
```

## 15.5 Eventos consumidos

```text
production.machine_incident_reported
scheduling.machine_assigned
quality.machine_related_nonconformity
```

---

# 16. Contexto Scheduling

## 16.1 Responsabilidade

Scheduling trata tempo como recurso operacional.

## 16.2 Agregados principais

```text
ScheduleItem
    ├── ScheduleResource
    ├── ScheduleConstraint
    └── ScheduleStatus
```

```text
AvailabilityCalendar
```

## 16.3 Recursos planejáveis

* funcionários;
* equipes;
* máquinas;
* setores;
* filiais;
* veículos;
* operações;
* entregas;
* manutenções.

## 16.4 Relações

```text
ScheduleItem N ─── N Employee
ScheduleItem N ─── N Machine
ScheduleItem 0..1 ─── 1 OperationInstance
ScheduleItem 0..1 ─── 1 WorkflowInstance
```

## 16.5 Eventos publicados

```text
scheduling.item_created
scheduling.resource_assigned
scheduling.conflict_detected
scheduling.item_rescheduled
scheduling.item_cancelled
```

---

# 17. Contexto Documents

## 17.1 Responsabilidade

Documents controla documentos, arquivos, versões e vínculos.

## 17.2 Agregados principais

```text
Document
    ├── DocumentVersion
    │   └── StorageObject
    ├── DocumentPermission
    └── DocumentStatusHistory
```

## 17.3 Relações genéricas

Um documento poderá ser relacionado a qualquer entidade autorizada através de:

```text
DocumentLink
    document_id
    entity_type
    entity_id
    relationship_type
```

Exemplos:

```text
Document ─── WorkflowInstance
Document ─── ProductionOrder
Document ─── OperationInstance
Document ─── Customer
Document ─── Quotation
Document ─── Incident
Document ─── QualityInspection
```

## 17.4 Regras

* versões antigas não serão apagadas;
* uma versão poderá ser marcada como atual;
* arquivos antigos poderão ser marcados como obsoletos;
* a visibilidade deverá respeitar permissões;
* o Storage não será acessado diretamente pela interface;
* uploads deverão ser validados por tipo e tamanho.

## 17.5 Eventos publicados

```text
document.created
document.version_uploaded
document.marked_obsolete
document.archived
document.link_created
document.permission_changed
```

---

# 18. Contexto Forms

## 18.1 Responsabilidade

Forms define formulários e checklists configuráveis.

## 18.2 Agregados principais

```text
FormDefinition
    └── FormVersion
        ├── FieldDefinition
        ├── ValidationRule
        └── VisibilityRule
```

```text
FormSubmission
    ├── SubmissionResponse
    └── SubmissionAttachment
```

## 18.3 Relações

```text
FormDefinition 1 ─── N FormVersion
FormVersion 1 ─── N FormSubmission
FormDefinition N ─── N StageDefinition
FormDefinition N ─── N OperationDefinition
FormSubmission 0..1 ─── 1 WorkflowInstance
FormSubmission 0..1 ─── 1 OperationInstance
FormSubmission 0..1 ─── 1 OperationExecution
```

## 18.4 Checklists

Checklist é uma especialização de formulário.

Um checklist poderá ser:

* obrigatório;
* opcional;
* repetível;
* individual;
* coletivo;
* vinculado a uma etapa;
* vinculado a uma operação;
* vinculado a uma execução;
* condicionado por regra.

## 18.5 Eventos publicados

```text
forms.definition_created
forms.version_published
forms.submission_started
forms.submission_completed
forms.submission_reopened
forms.validation_failed
```

---

# 19. Contexto Incidents

Ocorrências podem ser tratadas como capacidade transversal ou subcontexto de Production.

## 19.1 Agregado principal

```text
Incident
    ├── IncidentResponse
    ├── IncidentAssignment
    ├── IncidentEvidence
    └── IncidentResolution
```

## 19.2 Relações

```text
Incident 0..1 ─── 1 WorkflowInstance
Incident 0..1 ─── 1 OperationInstance
Incident 0..1 ─── 1 OperationExecution
Incident 0..1 ─── 1 Machine
Incident 0..1 ─── 1 Material
Incident N ─── 1 ReportingEmployee
```

## 19.3 Exemplos

* falta de material;
* peça danificada;
* máquina parada;
* erro de projeto;
* erro de fabricação;
* necessidade de retrabalho;
* problema de qualidade;
* impedimento externo.

## 19.4 Eventos publicados

```text
incident.created
incident.assigned
incident.acknowledged
incident.responded
incident.resolved
incident.escalated
```

---

# 20. Contexto Notifications

## 20.1 Responsabilidade

Notifications entrega informações aos usuários.

## 20.2 Agregados principais

```text
Notification
    ├── NotificationRecipient
    ├── NotificationChannel
    └── DeliveryAttempt
```

```text
NotificationTemplate
```

## 20.3 Canais

* push;
* desktop;
* e-mail;
* WhatsApp;
* notificação interna.

## 20.4 Relações

Uma notificação poderá ter como destinatário:

* User;
* Role;
* Sector;
* Branch;
* equipe;
* responsável por entidade.

## 20.5 Eventos consumidos

Exemplos:

```text
incident.created
production.material_requested
inventory.reservation_failed
workflow.stage_changed
quality.nonconformity_created
maintenance.machine_unavailable
commercial.quotation_approved
```

## 20.6 Eventos publicados

```text
notification.created
notification.sent
notification.delivered
notification.failed
notification.read
```

---

# 21. Contexto Financial

## 21.1 Responsabilidade

Financial controla obrigações e recebimentos.

## 21.2 Agregados principais

```text
AccountReceivable
    ├── ReceivableInstallment
    └── ReceiptAllocation
```

```text
AccountPayable
    ├── PayableInstallment
    └── PaymentAllocation
```

```text
FinancialTransaction
```

```text
BankAccount
```

## 21.3 Relações

```text
Contract 0..1 ─── N AccountReceivable
SalesOrder 0..1 ─── N AccountReceivable
PurchaseOrder 0..1 ─── N AccountPayable
Customer 1 ─── N AccountReceivable
Supplier 1 ─── N AccountPayable
```

## 21.4 Eventos publicados

```text
financial.receivable_created
financial.receivable_paid
financial.receivable_overdue
financial.payable_created
financial.payable_paid
financial.cash_transaction_created
```

## 21.5 Dependências proibidas

Financial não deverá alterar:

* orçamento;
* contrato;
* pedido de compra;
* cliente;
* fornecedor.

Ele reage a fatos e mantém seus próprios registros.

---

# 22. Contexto Fiscal

## 22.1 Responsabilidade

Fiscal controla regras e documentos tributários.

## 22.2 Agregados principais

```text
FiscalDocument
    ├── FiscalDocumentItem
    ├── TaxCalculation
    └── FiscalAuthorization
```

```text
TaxRule
```

## 22.3 Relações

```text
SalesOrder 0..1 ─── N FiscalDocument
PurchaseOrder 0..1 ─── N IncomingFiscalDocument
Customer N ─── 1 FiscalProfile
Material N ─── 1 FiscalClassification
```

O módulo fiscal deverá ser tratado como capacidade específica e poderá permanecer desativado para empresas que não necessitem dele.

---

# 23. Contexto Configuration

## 23.1 Responsabilidade

Configuration centraliza comportamentos configuráveis.

## 23.2 Agregados principais

```text
ConfigurationDefinition
```

```text
ConfigurationValue
```

```text
FeaturePack
    └── Capability
```

```text
SequenceDefinition
```

## 23.3 Escopos

Configurações poderão ser aplicadas por:

1. plataforma;
2. Tenant;
3. Branch;
4. Sector;
5. Role;
6. User.

A configuração mais específica prevalecerá quando permitido.

## 23.4 Relações

```text
FeaturePack N ─── N Capability
Tenant N ─── N EnabledCapability
ConfigurationDefinition 1 ─── N ConfigurationValue
```

## 23.5 Regra

Configuração não deve substituir regras críticas do domínio.

Ela define comportamentos permitidos, não viola invariantes.

---

# 24. Contexto Capabilities

## 24.1 Responsabilidade

Capabilities representa recursos disponíveis na plataforma.

## 24.2 Exemplos

```text
workflow
production_execution
documents
forms
inventory
purchasing
financial
quality
maintenance
analytics
ai_assistant
push_notifications
```

## 24.3 Relações

```text
Capability N ─── N FeaturePack
Capability 1 ─── N Permission
Tenant N ─── N Capability
Plugin 1 ─── N Capability
```

## 24.4 Regra

O Core conhece capacidades.

Plugins, pacotes e integrações são meios de fornecer capacidades.

---

# 25. Contexto Audit

## 25.1 Responsabilidade

Audit registra rastreabilidade administrativa.

## 25.2 Agregado principal

```text
AuditLog
```

## 25.3 Informações obrigatórias

* Tenant;
* usuário;
* funcionário;
* ação;
* entidade;
* identificador;
* estado anterior;
* estado posterior;
* justificativa;
* origem;
* IP;
* dispositivo;
* correlation_id;
* data e hora.

## 25.4 Relação com eventos

```text
DomainEvent
    representa fato operacional

AuditLog
    representa ação administrativa ou técnica
```

Os dois poderão compartilhar `correlation_id`, mas não deverão utilizar a mesma tabela.

---

# 26. Contexto Events

## 26.1 Agregado principal

```text
DomainEvent
```

## 26.2 Campos mínimos

```text
event_id
tenant_id
aggregate_type
aggregate_id
aggregate_sequence
event_type
schema_version
actor_user_id
actor_employee_id
correlation_id
causation_id
source
payload
metadata
occurred_at
recorded_at
```

## 26.3 Relações

```text
Aggregate 1 ─── N DomainEvent
DomainEvent 1 ─── 0..1 OutboxMessage
DomainEvent 1 ─── N EventConsumerCheckpoint
```

## 26.4 Regra de imutabilidade

Eventos não poderão ser atualizados ou excluídos pela aplicação.

Correções deverão ocorrer através de novos eventos.

---

# 27. Timeline

Timeline é uma projeção de leitura, não a origem da verdade.

## 27.1 Estrutura

```text
TimelineEntry
    entity_type
    entity_id
    entry_type
    title
    body
    actor
    source_event_id
    occurred_at
    data
```

## 27.2 Fontes

A Timeline poderá ser alimentada por:

* eventos;
* comentários;
* documentos;
* mudanças de etapa;
* execuções;
* pausas;
* ocorrências;
* checklists;
* ações administrativas permitidas.

## 27.3 Relações

```text
Entity 1 ─── N TimelineEntry
DomainEvent 0..1 ─── N TimelineEntry
```

---

# 28. Contexto Analytics

## 28.1 Responsabilidade

Analytics constrói indicadores e projeções.

## 28.2 Fontes

Analytics consome:

* eventos;
* execuções;
* movimentações;
* resultados financeiros;
* mudanças de workflow;
* checklists;
* ocorrências;
* qualidade;
* manutenção.

## 28.3 Regra

Analytics não deverá ser fonte primária de dados operacionais.

Dashboards e relatórios utilizam projeções próprias.

## 28.4 Exemplos

* tempo médio por operação;
* tempo parado por motivo;
* produtividade por equipe;
* retrabalho;
* atraso;
* lead time;
* consumo de material;
* utilização de máquina;
* conversão comercial;
* rentabilidade;
* desempenho por filial.

---

# 29. Contexto AI

## 29.1 Responsabilidade

AI utiliza informações autorizadas para auxiliar usuários.

## 29.2 Relações

A IA poderá consultar:

* Search;
* Timeline;
* Documents;
* Analytics;
* Workflow;
* Production;
* CRM;
* Commercial;
* Inventory;
* Financial;
* outros contextos permitidos.

## 29.3 Limites

A IA não deverá:

* acessar banco diretamente;
* ignorar permissões;
* alterar agregados diretamente;
* executar comandos sem autorização;
* inventar dados;
* ocultar a origem de informações críticas.

## 29.4 Ações

A IA poderá:

1. preparar um comando;
2. explicar o impacto;
3. solicitar confirmação;
4. enviar à Application Layer;
5. registrar auditoria;
6. apresentar o resultado.

## 29.5 Perfis de assistente

```text
CommercialAssistant
ProductionAssistant
PCPAssistant
InventoryAssistant
PurchasingAssistant
FinancialAssistant
HRDesignedAssistant
ManagementAssistant
```

Todos utilizarão o mesmo AI Engine e políticas de autorização.

---

# 30. Matriz de propriedade dos dados

| Informação       | Contexto proprietário            | Contextos consumidores               |
| ---------------- | -------------------------------- | ------------------------------------ |
| Credencial       | Identity                         | API, Desktop, PWA                    |
| Usuário          | Identity                         | Organization, Audit, Notifications   |
| Funcionário      | Organization                     | Production, Scheduling, Audit        |
| Filial           | Organization                     | Inventory, Production, Financial     |
| Setor            | Organization                     | Production, Inventory, Notifications |
| Cliente          | CRM                              | Commercial, Financial, Production    |
| Orçamento        | Commercial                       | CRM, Production, Financial           |
| Workflow         | Workflow                         | Commercial, Production, Purchasing   |
| Operação         | Production                       | Scheduling, Quality, Analytics       |
| Execução         | Production                       | Analytics, Audit, Timeline           |
| Máquina          | Maintenance/Production Resources | Production, Scheduling               |
| Material         | Inventory                        | Engineering, Purchasing, Production  |
| Saldo de estoque | Inventory                        | Production, Purchasing               |
| Pedido de compra | Purchasing                       | Inventory, Financial                 |
| Documento        | Documents                        | Todos, mediante autorização          |
| Checklist        | Forms                            | Workflow, Production, Quality        |
| Notificação      | Notifications                    | Interfaces                           |
| Evento           | Events                           | Timeline, Analytics, Automation      |
| Auditoria        | Audit                            | Administração                        |
| Configuração     | Configuration                    | Todos os contextos autorizados       |
| Capacidade       | Capabilities                     | Authorization, UI, Plugins           |
| Indicador        | Analytics                        | Dashboard, AI, Reports               |

---

# 31. Matriz de dependências permitidas

| Contexto      | Pode depender de                          |
| ------------- | ----------------------------------------- |
| Identity      | contratos mínimos de Tenant e Membership  |
| Organization  | Identity por identificador                |
| CRM           | Organization, Documents                   |
| Commercial    | CRM, Workflow, Documents, Configuration   |
| Workflow      | Organization, Forms, Configuration        |
| Production    | Workflow, Organization, Forms, Scheduling |
| Engineering   | Documents, Inventory por referência       |
| Inventory     | Organization, Material definitions        |
| Purchasing    | Inventory, CRM/Supplier, Organization     |
| Quality       | Production, Inventory, Forms, Documents   |
| Maintenance   | Organization, Scheduling, Inventory       |
| Scheduling    | Organization, Production, Maintenance     |
| Financial     | Commercial, Purchasing, Organization      |
| Fiscal        | Commercial, Purchasing, Financial         |
| Documents     | Identity, Authorization, Storage          |
| Notifications | Identity, Organization, Events            |
| Analytics     | eventos e projeções públicas              |
| AI            | Application Layer e Search autorizados    |
| Audit         | contexto autenticado e ações da aplicação |

---

# 32. Dependências proibidas

São proibidos:

* Domain importar Infrastructure;
* PWA acessar banco diretamente;
* Desktop acessar banco diretamente;
* IA alterar tabela diretamente;
* Workflow alterar estoque;
* Production alterar orçamento;
* Inventory alterar pedido de compra;
* Financial alterar contrato;
* Documents decidir regra de negócio;
* Analytics alterar operação;
* Notification alterar entidade de origem;
* um contexto utilizar modelos ORM internos de outro contexto;
* uma tela implementar regra exclusiva;
* um módulo depender de cor, fonte ou estilo hardcoded.

---

# 33. Consistência transacional

## 33.1 Consistência forte

Aplicar dentro do mesmo agregado.

Exemplo:

```text
StartExecution
    altera OperationExecution
    cria participante
    gera evento
    grava Outbox
```

Tudo na mesma transação.

## 33.2 Consistência eventual

Aplicar entre contextos.

Exemplo:

```text
Commercial aprova orçamento
    ↓
publica quotation.approved
    ↓
Production cria ordem
    ↓
Workflow cria instância
    ↓
Notifications avisa responsáveis
```

Cada contexto confirma sua própria transação.

## 33.3 Compensação

Quando necessário, utilizar ações compensatórias explícitas.

Exemplo:

```text
ProductionOrderCreated
    ↓
ReservationFailed
    ↓
ProductionOrderBlocked
```

Não realizar rollback distribuído entre contextos.

---

# 34. Idempotência

Consumidores de eventos e comandos deverão ser idempotentes.

Estruturas recomendadas:

```text
ProcessedCommand
EventConsumerCheckpoint
OutboxMessage
InboxMessage
```

Uma mensagem repetida não poderá produzir efeitos duplicados.

---

# 35. Identificadores e integridade

## 35.1 Identificadores

Todos os agregados utilizarão UUID.

## 35.2 Tenant

Toda entidade empresarial deverá possuir `tenant_id`.

## 35.3 Integridade entre contextos

Chaves estrangeiras poderão ser utilizadas quando:

* os contextos estiverem no mesmo banco;
* não criarem acoplamento de ciclo de vida;
* preservarem isolamento por Tenant;
* não permitirem alterações externas indevidas.

Em integrações futuras ou bancos separados, essas relações poderão ser mantidas apenas por identificador.

---

# 36. Exclusão e arquivamento

## 36.1 Exclusão física

Deverá ser evitada em informações de negócio.

## 36.2 Arquivamento

Utilizar para:

* clientes inativos;
* documentos antigos;
* workflows substituídos;
* orçamentos encerrados;
* funcionários desligados;
* configurações antigas.

## 36.3 Imutabilidade

Não deverão ser removidos:

* eventos;
* auditorias;
* versões publicadas;
* movimentações de estoque;
* execuções concluídas;
* documentos financeiros;
* documentos fiscais.

---

# 37. Eventos principais de integração

## Comercial para produção

```text
commercial.quotation_approved
commercial.sales_order_created
```

## Produção para estoque

```text
production.material_requested
production.material_consumed
production.order_cancelled
```

## Estoque para compras

```text
inventory.reservation_failed
inventory.reorder_point_reached
```

## Compras para estoque

```text
purchasing.material_received
purchasing.purchase_cancelled
```

## Produção para qualidade

```text
production.execution_finished
production.rework_requested
```

## Qualidade para produção

```text
quality.rework_required
quality.inspection_approved
```

## Máquina para produção

```text
maintenance.machine_unavailable
maintenance.machine_released
```

## Todos para Notifications

Eventos configurados como notificáveis.

## Todos para Analytics

Eventos operacionais relevantes.

## Todos para Timeline

Eventos classificados como apresentáveis ao usuário.

---

# 38. Fluxo principal: orçamento até produção

```text
Lead criado
    ↓
Lead convertido em Customer
    ↓
Quotation criada
    ↓
QuotationVersion criada
    ↓
Quotation enviada
    ↓
Quotation aprovada
    ↓
Contract criado ou SalesOrder criado
    ↓
WorkflowInstance comercial concluída
    ↓
ProductionOrder criada
    ↓
WorkflowInstance produtiva criada
    ↓
OperationInstances geradas
    ↓
Funcionários atribuídos
    ↓
Execuções registradas
    ↓
Checklists preenchidos
    ↓
Documentos consultados
    ↓
Ocorrências tratadas
    ↓
Produção concluída
    ↓
Entrega
    ↓
Financeiro e documentação final
```

---

# 39. Fluxo principal: execução móvel

```text
Usuário autentica
    ↓
Identity valida sessão
    ↓
Authorization calcula permissões
    ↓
PWA consulta operações atribuídas
    ↓
Funcionário inicia execução
    ↓
Application Layer valida:
    - Tenant;
    - atribuição;
    - etapa;
    - operação;
    - permissões;
    - concorrência;
    - idempotência
    ↓
Production inicia execução
    ↓
Evento execution.started
    ↓
Timeline atualizada
    ↓
Analytics recebe evento
    ↓
Administrador visualiza em tempo real
```

---

# 40. Fluxo principal: pausa e ajuda em outra tarefa

```text
Funcionário pausa execução A
    ↓
Informa motivo:
    HELPING_OTHER_TASK
    ↓
ExecutionPause criada
    ↓
Funcionário entra como participante da execução B
    ↓
Tempo da execução B começa a ser registrado para ele
    ↓
Funcionário sai da execução B
    ↓
Retoma execução A
```

O sistema deverá preservar todos os intervalos de tempo.

---

# 41. Fluxo principal: falta de material

```text
Funcionário registra ocorrência
    ↓
Incident criado
    ↓
MaterialRequest criada
    ↓
Inventory é notificado
    ↓
Inventory responde:
    - disponível;
    - parcialmente disponível;
    - indisponível;
    - substituição sugerida
    ↓
Se indisponível:
    PurchaseRequest criada
    ↓
Purchasing responde previsão
    ↓
Production recebe atualização
    ↓
Administrador acompanha toda a Timeline
```

---

# 42. Fluxo principal: retrabalho

```text
Erro identificado
    ↓
NonConformity ou Incident criado
    ↓
Rework solicitado
    ↓
Nova OperationInstance criada
    ↓
Referência à operação original preservada
    ↓
Funcionário atribuído
    ↓
Nova execução registrada
    ↓
Tempo e custo separados
    ↓
Analytics contabiliza retrabalho
```

A operação original não deverá ser apagada ou sobrescrita.

---

# 43. Fluxo principal: documentos

```text
Usuário envia arquivo permitido
    ↓
StorageObject criado
    ↓
Document criado ou localizado
    ↓
DocumentVersion criada
    ↓
DocumentLink vincula ao contexto
    ↓
Evento document.version_uploaded
    ↓
Timeline recebe entrada
    ↓
Usuários autorizados visualizam
```

Versões anteriores permanecem disponíveis.

---

# 44. Critérios para novos relacionamentos

Antes de criar um novo relacionamento, responder:

1. Qual contexto é proprietário da informação?
2. O relacionamento precisa ser síncrono?
3. Um identificador é suficiente?
4. É necessário um evento?
5. O consumidor precisa de projeção local?
6. A relação respeita o Tenant?
7. Existe risco de ciclo entre contextos?
8. O relacionamento exige versão?
9. O histórico precisa ser preservado?
10. A IA poderá consultar essa relação?
11. Quais permissões se aplicam?
12. O fluxo precisa funcionar offline?

---

# 45. Critérios de conformidade

Uma implementação estará em conformidade quando:

* respeitar os limites dos contextos;
* possuir proprietário claro para cada dado;
* não compartilhar modelos ORM entre contextos;
* utilizar comandos explícitos;
* publicar eventos após a transação;
* utilizar Outbox para integração;
* preservar idempotência;
* respeitar isolamento por Tenant;
* separar eventos de auditoria;
* preservar versionamento;
* utilizar identificadores entre agregados;
* evitar transações distribuídas;
* não implementar regras em telas;
* não inserir estilos gráficos hardcoded.

---

# 46. Conclusão

Os relacionamentos de domínio do OrganizeG3 devem preservar independência, rastreabilidade e evolução segura.

A plataforma não será construída como um conjunto de módulos isolados ou tabelas interligadas indiscriminadamente.

Ela será composta por contextos responsáveis, agregados com limites claros, comandos explícitos, eventos imutáveis e integrações controladas.

Todo relacionamento deverá existir por uma razão de negócio clara e possuir um responsável definido.
