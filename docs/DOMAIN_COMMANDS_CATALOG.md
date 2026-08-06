# OrganizeG3 — Domain Commands Catalog

> Catálogo oficial de comandos de domínio e aplicação da plataforma OrganizeG3.

---

| Propriedade            | Valor                                                                     |
| ---------------------- | ------------------------------------------------------------------------- |
| Documento              | DOMAIN_COMMANDS_CATALOG.md                                                |
| Versão                 | 1.0.0                                                                     |
| Status                 | Baseline arquitetural                                                     |
| Abrangência            | Toda a plataforma                                                         |
| Depende de             | DOMAIN_ARCHITECTURE.md, DOMAIN_RELATIONSHIPS.md, DOMAIN_EVENTS_CATALOG.md |
| Idioma da documentação | Português                                                                 |
| Idioma dos comandos    | Inglês                                                                    |
| Convenção              | `VerbEntityCommand`                                                       |

---

# 1. Objetivo

Este documento define os comandos oficiais do OrganizeG3.

Ele estabelece:

* convenções de nomenclatura;
* estrutura obrigatória dos comandos;
* responsabilidades de execução;
* regras de autorização;
* idempotência;
* concorrência;
* validação;
* transações;
* eventos resultantes;
* comandos permitidos por contexto;
* origem dos comandos;
* critérios para criação de novos comandos.

Todo comando executado pelo Desktop, PWA, API, automações, integrações ou Inteligência Artificial deverá estar previsto neste catálogo ou ser incluído nele antes da implementação.

---

# 2. Definição

Um comando representa uma intenção explícita de alterar o estado da plataforma.

Exemplos:

```text
CreateTenantCommand
InviteUserCommand
ApproveQuotationCommand
MoveWorkflowInstanceCommand
StartExecutionCommand
PauseExecutionCommand
ReserveMaterialCommand
UploadDocumentVersionCommand
```

Um comando pode:

* ser aceito;
* ser rejeitado;
* gerar nenhuma alteração;
* alterar um agregado;
* gerar eventos;
* iniciar processos em outros contextos através de eventos.

Um comando não representa um fato concluído.

Exemplo:

```text
StartExecutionCommand
```

expressa intenção.

O fato resultante será:

```text
production.execution_started
```

---

# 3. Comandos, eventos e queries

## 3.1 Command

Altera estado.

Exemplo:

```text
ApproveQuotationCommand
```

## 3.2 Event

Registra o fato confirmado.

Exemplo:

```text
commercial.quotation_approved
```

## 3.3 Query

Consulta dados sem alterar estado.

Exemplo:

```text
GetQuotationDetailsQuery
```

## 3.4 Regra fundamental

Uma Query não poderá alterar dados.

Um evento não poderá ser utilizado como comando.

Uma tela não poderá alterar diretamente entidades ou tabelas.

---

# 4. Convenção de nomes

Todos os comandos utilizarão:

```text
VerbEntityCommand
```

Exemplos:

```text
CreateEmployeeCommand
AssignRoleCommand
PublishWorkflowVersionCommand
StartExecutionCommand
RequestMaterialCommand
CompleteFormSubmissionCommand
ArchiveDocumentCommand
```

## 4.1 Verbo

O nome deverá começar por um verbo explícito.

Verbos recomendados:

```text
Create
Update
Archive
Restore
Activate
Deactivate
Assign
Unassign
Start
Pause
Resume
Finish
Cancel
Approve
Reject
Publish
Reopen
Move
Transfer
Request
Reserve
Release
Submit
Complete
Upload
Link
Unlink
Enable
Disable
Confirm
Resolve
Escalate
```

## 4.2 Entidade ou intenção

O restante do nome deverá indicar claramente o alvo.

Correto:

```text
PauseExecutionCommand
ApprovePurchaseOrderCommand
TransferEmployeeCommand
CreateQuotationVersionCommand
```

Evitar:

```text
UpdateDataCommand
SaveRecordCommand
ProcessItemCommand
ChangeStatusCommand
ExecuteActionCommand
```

## 4.3 Regra semântica

O comando deverá representar uma intenção de negócio, não uma operação genérica de banco.

Preferir:

```text
ApproveQuotationCommand
```

em vez de:

```text
UpdateQuotationStatusCommand
```

Preferir:

```text
ArchiveCustomerCommand
```

em vez de:

```text
SetCustomerActiveCommand
```

---

# 5. Envelope padrão

Todo comando deverá possuir um envelope mínimo.

```json
{
  "command_id": "uuid",
  "command_type": "StartExecutionCommand",
  "tenant_id": "uuid",
  "actor": {
    "user_id": "uuid",
    "employee_id": "uuid",
    "actor_type": "USER"
  },
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "idempotency_key": "string",
  "source": "pwa",
  "device_id": "uuid",
  "occurred_at": "2026-08-04T18:00:00Z",
  "contract_version": 1,
  "expected_entity_version": 3,
  "payload": {},
  "metadata": {}
}
```

---

# 6. Campos do envelope

## `command_id`

Identificador único da tentativa de comando.

Deve ser UUID.

Um mesmo comando reenviado deverá preservar o mesmo `command_id` quando for uma repetição técnica da mesma intenção.

---

## `command_type`

Nome oficial do comando.

Exemplo:

```text
StartExecutionCommand
```

---

## `tenant_id`

Empresa proprietária da operação.

O valor deverá ser derivado da sessão autenticada.

O cliente não poderá escolher livremente o Tenant.

---

## `actor`

Identifica quem está solicitando a ação.

Estrutura:

```json
{
  "user_id": "uuid",
  "employee_id": "uuid",
  "actor_type": "USER"
}
```

Tipos iniciais:

```text
USER
SYSTEM
AUTOMATION
AI
INTEGRATION
MIGRATION
```

---

## `correlation_id`

Agrupa todos os comandos e eventos pertencentes ao mesmo fluxo.

Exemplo:

```text
ApproveQuotationCommand
    ↓
commercial.quotation_approved
    ↓
CreateSalesOrderCommand
    ↓
commercial.sales_order_created
    ↓
CreateProductionOrderCommand
```

---

## `causation_id`

Identifica o comando ou evento que originou a ação atual.

---

## `idempotency_key`

Impede duplicação de efeitos.

Obrigatória em comandos:

* enviados pela PWA;
* executados offline;
* recebidos por integrações;
* relacionados a pagamentos;
* relacionados a estoque;
* relacionados a produção;
* relacionados a documentos;
* executados por automações;
* executados por IA.

---

## `source`

Origem do comando.

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

---

## `device_id`

Identifica o dispositivo de origem.

Obrigatório para comandos enviados pelo PWA ou Desktop quando houver sincronização.

---

## `occurred_at`

Momento em que o usuário executou a intenção.

Sempre em UTC.

Comandos offline poderão possuir horário do cliente, sujeito a validação.

---

## `contract_version`

Versão do contrato do comando.

Começa em:

```text
1
```

Mudanças incompatíveis exigem nova versão.

---

## `expected_entity_version`

Versão esperada do agregado.

Utilizada para concorrência otimista.

Exemplo:

```text
expected_entity_version = 3
```

Se o servidor possuir versão 4, o comando poderá ser rejeitado com:

```text
ConcurrencyError
```

---

## `payload`

Dados específicos do comando.

---

## `metadata`

Informações técnicas complementares.

Exemplo:

```json
{
  "application_version": "0.1.0",
  "offline": true,
  "client_sequence": 17
}
```

---

# 7. Ciclo de execução

Todo comando deverá seguir o fluxo:

```text
Receber comando
    ↓
Validar contrato
    ↓
Resolver Tenant
    ↓
Resolver ator
    ↓
Validar autenticação
    ↓
Validar permissão
    ↓
Validar idempotência
    ↓
Carregar agregado
    ↓
Validar versão
    ↓
Executar regra de domínio
    ↓
Persistir alterações
    ↓
Persistir eventos
    ↓
Persistir Outbox
    ↓
Persistir auditoria
    ↓
Confirmar transação
    ↓
Retornar resultado
```

---

# 8. Responsabilidades

## 8.1 Presentation Layer

Responsável por:

* receber entrada;
* validar formato básico;
* construir o comando;
* enviar para Application Layer;
* transformar o resultado em resposta.

Não executa regra de negócio.

---

## 8.2 Application Layer

Responsável por:

* autorização;
* idempotência;
* coordenação;
* carregamento de agregados;
* Unit of Work;
* publicação de eventos;
* auditoria;
* resultado do caso de uso.

---

## 8.3 Domain Layer

Responsável por:

* invariantes;
* decisões de negócio;
* transições;
* criação de eventos;
* validações de estado.

---

## 8.4 Infrastructure

Responsável por:

* persistência;
* banco;
* Outbox;
* mensageria;
* Storage;
* integrações externas.

---

# 9. Resultado padrão

Todo handler deverá retornar resultado explícito.

Exemplo conceitual:

```text
CommandResult
    success
    command_id
    entity_id
    entity_version
    events
    warnings
    metadata
```

Exemplo:

```json
{
  "success": true,
  "command_id": "uuid",
  "entity_id": "uuid",
  "entity_version": 4,
  "events": [
    "production.execution_started"
  ],
  "warnings": [],
  "metadata": {}
}
```

---

# 10. Erros padrão

Comandos poderão retornar erros controlados.

```text
ValidationError
NotFoundError
ConflictError
PermissionDeniedError
AuthenticationError
InvalidTransitionError
ConcurrencyError
IdempotencyConflictError
ConfigurationError
BusinessRuleError
ResourceUnavailableError
```

## 10.1 ValidationError

Dados inválidos.

## 10.2 NotFoundError

Entidade não localizada no Tenant autorizado.

## 10.3 ConflictError

Estado atual incompatível com a ação.

## 10.4 PermissionDeniedError

Ator sem permissão.

## 10.5 InvalidTransitionError

Transição de workflow não autorizada.

## 10.6 ConcurrencyError

Versão esperada diferente da versão persistida.

## 10.7 IdempotencyConflictError

A chave de idempotência já foi utilizada com payload diferente.

---

# 11. Idempotência

Todo comando crítico deverá possuir uma chave de idempotência.

Estrutura conceitual:

```text
ProcessedCommand
    tenant_id
    idempotency_key
    command_id
    command_type
    request_hash
    status
    result
    processed_at
```

## 11.1 Mesmo comando e mesmo payload

Retornar o resultado anterior.

## 11.2 Mesma chave e payload diferente

Rejeitar com:

```text
IdempotencyConflictError
```

## 11.3 Comando ainda em processamento

Retornar estado:

```text
PROCESSING
```

ou aguardar conforme política do caso de uso.

---

# 12. Concorrência otimista

Agregados mutáveis deverão possuir versão.

Exemplo:

```text
row_version = 5
```

Comando:

```text
expected_entity_version = 5
```

Após alteração:

```text
row_version = 6
```

Se a versão divergir, a alteração não será aplicada.

---

# 13. Transações

Um comando deverá alterar preferencialmente um único agregado principal.

A mesma transação poderá incluir:

* agregado;
* entidades internas;
* eventos;
* auditoria;
* Outbox;
* idempotência.

Não deverá incluir alterações arbitrárias em múltiplos contextos.

---

# 14. Autorização

Todo comando deverá declarar sua permissão.

Exemplo:

```text
StartExecutionCommand
permission = production.execution.start
```

Além da permissão, poderão ser validados escopos:

```text
assigned_only
same_branch
same_sector
own_records
team_records
administrator_only
```

---

# 15. Auditoria

Comandos críticos deverão gerar auditoria.

A auditoria deverá registrar:

* comando;
* ator;
* Tenant;
* entidade;
* estado anterior;
* estado posterior;
* justificativa;
* origem;
* dispositivo;
* correlation_id;
* resultado.

---

# 16. Comandos offline

Comandos enviados offline deverão possuir:

```text
command_id
idempotency_key
device_id
client_sequence
occurred_at
contract_version
expected_entity_version
```

O servidor deverá:

* ordenar por dispositivo quando necessário;
* validar duplicidade;
* detectar conflitos;
* rejeitar ações expiradas;
* preservar horário original;
* registrar horário de processamento.

---

# 17. Comandos executados pela IA

A IA não executará alterações diretamente.

Fluxo:

```text
IA interpreta solicitação
    ↓
IA prepara comando
    ↓
Application Layer valida
    ↓
Usuário confirma quando necessário
    ↓
Comando oficial é executado
    ↓
Auditoria registra ator AI e usuário confirmador
```

Comandos sensíveis sempre exigirão confirmação humana.

Exemplos:

* aprovar orçamento;
* cancelar ordem;
* alterar permissão;
* realizar pagamento;
* ajustar estoque;
* excluir ou arquivar documento;
* bloquear usuário;
* alterar configuração crítica.

---

# 18. Comandos executados por automações

Automações deverão utilizar os mesmos comandos da aplicação.

Exemplo:

```text
inventory.stock_reservation_failed
    ↓
Automation Rule
    ↓
CreatePurchaseRequestCommand
```

A automação não poderá alterar tabelas diretamente.

---

# 19. Comandos de Identity

## `CreateUserCommand`

Cria uma identidade de usuário.

Permissão:

```text
identity.user.create
```

Payload:

```json
{
  "email": "usuario@empresa.com",
  "full_name": "Nome do usuário",
  "auth_provider_id": "string",
  "is_platform_admin": false
}
```

Validações:

* e-mail válido;
* e-mail único;
* provedor válido;
* ator autorizado;
* plataforma admin somente por plataforma admin.

Evento resultante:

```text
identity.user_created
```

Erros possíveis:

```text
ValidationError
ConflictError
PermissionDeniedError
```

---

## `UpdateUserProfileCommand`

Atualiza informações básicas do usuário.

Permissão:

```text
identity.user.update
```

Payload:

```json
{
  "user_id": "uuid",
  "full_name": "Novo nome",
  "avatar_url": "url"
}
```

Regras:

* usuário pode editar seu próprio perfil;
* administrador pode editar usuários permitidos;
* alteração de e-mail deverá utilizar comando específico.

Evento resultante:

```text
identity.user_profile_updated
```

---

## `ChangeUserEmailCommand`

Altera o e-mail do usuário.

Permissão:

```text
identity.user.change_email
```

Payload:

```json
{
  "user_id": "uuid",
  "new_email": "novo@empresa.com",
  "confirmation_token": "string"
}
```

Validações:

* e-mail único;
* confirmação válida;
* reautenticação quando exigida.

Evento resultante:

```text
identity.user_email_changed
```

---

## `BlockUserCommand`

Bloqueia o acesso de um usuário.

Permissão:

```text
identity.user.block
```

Payload:

```json
{
  "user_id": "uuid",
  "reason": "Acesso suspenso"
}
```

Regras:

* não bloquear o último administrador da plataforma;
* revogar sessões ativas;
* registrar justificativa.

Eventos resultantes:

```text
identity.user_blocked
identity.session_revoked
```

---

## `UnblockUserCommand`

Restaura acesso de usuário bloqueado.

Permissão:

```text
identity.user.unblock
```

Payload:

```json
{
  "user_id": "uuid",
  "reason": "Acesso liberado"
}
```

Evento resultante:

```text
identity.user_unblocked
```

---

## `AuthenticateUserCommand`

Solicita autenticação.

Permissão:

```text
public
```

Payload:

```json
{
  "email": "usuario@empresa.com",
  "password": "secret",
  "device_id": "uuid",
  "device_name": "Celular"
}
```

Regras:

* senha não é persistida;
* validar Tenant e Membership após autenticação;
* limitar tentativas;
* registrar falhas;
* não revelar se o e-mail existe.

Eventos possíveis:

```text
identity.user_authenticated
identity.authentication_failed
identity.device_registered
```

---

## `RevokeSessionCommand`

Revoga uma sessão.

Permissão:

```text
identity.session.revoke
```

Payload:

```json
{
  "session_id": "uuid",
  "reason_code": "USER_LOGOUT"
}
```

Evento resultante:

```text
identity.session_revoked
```

---

## `RevokeAllUserSessionsCommand`

Revoga todas as sessões do usuário.

Permissão:

```text
identity.session.revoke_all
```

Payload:

```json
{
  "user_id": "uuid",
  "reason_code": "SECURITY_ACTION"
}
```

Eventos resultantes:

```text
identity.session_revoked
```

Um evento poderá ser gerado por sessão.

---

## `RegisterDeviceCommand`

Registra dispositivo utilizado pelo usuário.

Permissão:

```text
identity.device.register
```

Payload:

```json
{
  "device_key": "string",
  "platform": "PWA",
  "device_name": "Celular de João",
  "push_token": "string"
}
```

Evento resultante:

```text
identity.device_registered
```

---

## `TrustDeviceCommand`

Marca dispositivo como confiável.

Permissão:

```text
identity.device.trust
```

Payload:

```json
{
  "device_id": "uuid",
  "verification_code": "string"
}
```

Evento resultante:

```text
identity.device_trusted
```

---

## `UntrustDeviceCommand`

Remove a confiança de um dispositivo.

Permissão:

```text
identity.device.untrust
```

Payload:

```json
{
  "device_id": "uuid",
  "reason": "Dispositivo perdido"
}
```

Eventos resultantes:

```text
identity.device_untrusted
identity.session_revoked
```

---

## `ChangePasswordCommand`

Altera a senha do usuário.

Permissão:

```text
identity.password.change
```

Payload:

```json
{
  "current_password": "secret",
  "new_password": "secret",
  "revoke_other_sessions": true
}
```

Regras:

* validar senha atual;
* aplicar política de senha;
* nunca registrar senha em log ou evento.

Evento resultante:

```text
identity.password_changed
```

---

## `RequestPasswordResetCommand`

Solicita recuperação de senha.

Permissão:

```text
public
```

Payload:

```json
{
  "email": "usuario@empresa.com"
}
```

Regras:

* não revelar se a conta existe;
* limitar frequência;
* token com prazo.

Evento técnico possível:

```text
identity.password_reset_requested
```

---

## `ResetPasswordCommand`

Redefine senha por token.

Permissão:

```text
public
```

Payload:

```json
{
  "reset_token": "string",
  "new_password": "secret"
}
```

Eventos resultantes:

```text
identity.password_changed
identity.session_revoked
```

---

# 20. Comandos de Organization

## `CreateTenantCommand`

Cria uma nova empresa na plataforma.

Permissão:

```text
platform.tenant.create
```

Payload:

```json
{
  "legal_name": "Empresa Exemplo Ltda.",
  "trade_name": "Empresa Exemplo",
  "tax_id": "string",
  "slug": "empresa-exemplo",
  "timezone": "America/Sao_Paulo",
  "locale": "pt-BR"
}
```

Validações:

* slug único;
* documento fiscal válido quando informado;
* timezone válido;
* ator autorizado.

Evento resultante:

```text
organization.tenant_created
```

Reações esperadas:

* criar configurações padrão;
* habilitar capacidades do plano;
* criar role administrativa;
* criar workflow inicial opcional.

---

## `UpdateTenantCommand`

Atualiza dados cadastrais da empresa.

Permissão:

```text
organization.tenant.update
```

Payload:

```json
{
  "tenant_id": "uuid",
  "legal_name": "Novo nome",
  "trade_name": "Novo nome fantasia",
  "tax_id": "string",
  "timezone": "America/Sao_Paulo",
  "locale": "pt-BR"
}
```

Evento resultante:

```text
organization.tenant_updated
```

---

## `SuspendTenantCommand`

Suspende a empresa.

Permissão:

```text
platform.tenant.suspend
```

Payload:

```json
{
  "tenant_id": "uuid",
  "reason_code": "LICENSE_EXPIRED",
  "reason": "Licença expirada",
  "effective_at": "datetime"
}
```

Eventos resultantes:

```text
organization.tenant_suspended
```

Reações:

* bloquear novas sessões;
* limitar operações conforme política;
* notificar administradores.

---

## `ReactivateTenantCommand`

Reativa empresa suspensa.

Permissão:

```text
platform.tenant.reactivate
```

Payload:

```json
{
  "tenant_id": "uuid",
  "reason": "Licença renovada"
}
```

Evento resultante:

```text
organization.tenant_reactivated
```

---

## `CreateBranchCommand`

Cria uma filial ou unidade.

Permissão:

```text
organization.branch.create
```

Payload:

```json
{
  "code": "FILIAL-01",
  "name": "Filial Presidente Epitácio",
  "is_headquarters": false,
  "address": {}
}
```

Regras:

* código único por Tenant;
* empresa pode não possuir filiais;
* apenas uma matriz principal, salvo política específica.

Evento resultante:

```text
organization.branch_created
```

---

## `UpdateBranchCommand`

Atualiza uma filial.

Permissão:

```text
organization.branch.update
```

Payload:

```json
{
  "branch_id": "uuid",
  "name": "Novo nome",
  "address": {},
  "is_headquarters": false
}
```

Evento resultante:

```text
organization.branch_updated
```

---

## `ArchiveBranchCommand`

Arquiva uma filial.

Permissão:

```text
organization.branch.archive
```

Payload:

```json
{
  "branch_id": "uuid",
  "reason": "Unidade encerrada",
  "replacement_branch_id": "uuid"
}
```

Validações:

* não arquivar matriz sem substituição;
* verificar funcionários ativos;
* verificar estoque;
* verificar operações abertas;
* exigir plano de transferência quando necessário.

Evento resultante:

```text
organization.branch_archived
```

---

## `CreateSectorCommand`

Cria um setor.

Permissão:

```text
organization.sector.create
```

Payload:

```json
{
  "branch_id": "uuid",
  "parent_sector_id": null,
  "code": "CORTE",
  "name": "Corte"
}
```

Regras:

* filial opcional;
* setor pai opcional;
* código único no escopo configurado;
* impedir ciclo hierárquico.

Evento resultante:

```text
organization.sector_created
```

---

## `UpdateSectorCommand`

Atualiza um setor.

Permissão:

```text
organization.sector.update
```

Payload:

```json
{
  "sector_id": "uuid",
  "name": "Corte e usinagem",
  "parent_sector_id": "uuid"
}
```

Evento resultante:

```text
organization.sector_updated
```

---

## `ArchiveSectorCommand`

Arquiva um setor.

Permissão:

```text
organization.sector.archive
```

Payload:

```json
{
  "sector_id": "uuid",
  "reason": "Reorganização",
  "replacement_sector_id": "uuid"
}
```

Validações:

* verificar funcionários;
* verificar estoque;
* verificar operações;
* verificar notificações;
* verificar setores filhos.

Evento resultante:

```text
organization.sector_archived
```

---

## `CreateEmployeeCommand`

Cria um funcionário.

Permissão:

```text
organization.employee.create
```

Payload:

```json
{
  "user_id": "uuid",
  "registration_code": "FUNC-001",
  "full_name": "João da Silva",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "job_title": "Marceneiro",
  "hired_on": "date",
  "contact_data": {},
  "skills": {}
}
```

Regras:

* usuário é opcional;
* código único por Tenant;
* filial e setor opcionais;
* setor deve pertencer à filial quando ambos existirem.

Evento resultante:

```text
organization.employee_created
```

---

## `UpdateEmployeeCommand`

Atualiza dados do funcionário.

Permissão:

```text
organization.employee.update
```

Payload:

```json
{
  "employee_id": "uuid",
  "full_name": "Novo nome",
  "job_title": "Marceneiro líder",
  "contact_data": {},
  "skills": {}
}
```

Evento resultante:

```text
organization.employee_updated
```

---

## `AssignEmployeeCommand`

Atribui funcionário a filial, setor ou função operacional.

Permissão:

```text
organization.employee.assign
```

Payload:

```json
{
  "employee_id": "uuid",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "job_title": "Marceneiro"
}
```

Evento resultante:

```text
organization.employee_assigned
```

---

## `TransferEmployeeCommand`

Transfere funcionário.

Permissão:

```text
organization.employee.transfer
```

Payload:

```json
{
  "employee_id": "uuid",
  "new_branch_id": "uuid",
  "new_sector_id": "uuid",
  "new_job_title": "Líder de produção",
  "effective_at": "datetime",
  "reason": "Reorganização operacional"
}
```

Validações:

* destino válido;
* operações atuais avaliadas;
* agenda futura avaliada;
* permissões e escopos recalculados.

Evento resultante:

```text
organization.employee_transferred
```

---

## `TerminateEmployeeCommand`

Registra desligamento.

Permissão:

```text
organization.employee.terminate
```

Payload:

```json
{
  "employee_id": "uuid",
  "terminated_on": "date",
  "reason": "Desligamento",
  "disable_membership": true,
  "reassign_open_operations": true
}
```

Regras:

* encerrar atribuições futuras;
* verificar operações em andamento;
* desabilitar Membership quando solicitado;
* preservar histórico.

Eventos resultantes:

```text
organization.employee_terminated
organization.membership_disabled
```

---

## `CreateMembershipCommand`

Vincula usuário a um Tenant.

Permissão:

```text
organization.membership.create
```

Payload:

```json
{
  "user_id": "uuid",
  "employee_id": "uuid",
  "default_branch_id": "uuid",
  "default_sector_id": "uuid",
  "status": "ACTIVE"
}
```

Evento resultante:

```text
organization.membership_created
```

---

## `DisableMembershipCommand`

Desabilita o vínculo do usuário com a empresa.

Permissão:

```text
organization.membership.disable
```

Payload:

```json
{
  "membership_id": "uuid",
  "reason": "Funcionário desligado",
  "revoke_sessions": true
}
```

Eventos resultantes:

```text
organization.membership_disabled
identity.session_revoked
```

---

## `EnableMembershipCommand`

Reativa o vínculo.

Permissão:

```text
organization.membership.enable
```

Payload:

```json
{
  "membership_id": "uuid",
  "reason": "Retorno autorizado"
}
```

Evento resultante:

```text
organization.membership_enabled
```

---

## `UpdateMembershipPreferencesCommand`

Atualiza preferências específicas do usuário na empresa.

Permissão:

```text
organization.membership.preferences.update
```

Payload:

```json
{
  "membership_id": "uuid",
  "preferences": {
    "default_branch_id": "uuid",
    "default_sector_id": "uuid"
  }
}
```

Evento resultante:

```text
organization.membership_preferences_updated
```

---

# 21. Comandos de Authorization

## `CreateRoleCommand`

Cria um perfil de acesso.

Permissão:

```text
authorization.role.create
```

Payload:

```json
{
  "code": "PRODUCTION_OPERATOR",
  "name": "Operador de produção",
  "description": "Executa operações atribuídas"
}
```

Evento resultante:

```text
authorization.role_created
```

---

## `UpdateRoleCommand`

Atualiza o perfil.

Permissão:

```text
authorization.role.update
```

Payload:

```json
{
  "role_id": "uuid",
  "name": "Operador industrial",
  "description": "Descrição atualizada"
}
```

Evento resultante:

```text
authorization.role_updated
```

---

## `ArchiveRoleCommand`

Arquiva role que não será mais utilizada.

Permissão:

```text
authorization.role.archive
```

Payload:

```json
{
  "role_id": "uuid",
  "reason": "Perfil substituído",
  "replacement_role_id": "uuid"
}
```

Validações:

* roles de sistema poderão ter restrições;
* usuários vinculados devem ser avaliados;
* último administrador não pode perder acesso.

Evento resultante:

```text
authorization.role_archived
```

---

## `GrantPermissionToRoleCommand`

Concede permissão a uma role.

Permissão:

```text
authorization.permission.grant
```

Payload:

```json
{
  "role_id": "uuid",
  "permission_code": "production.execution.start",
  "effect": "ALLOW",
  "scope": {
    "assigned_only": true
  }
}
```

Evento resultante:

```text
authorization.permission_granted
```

---

## `RevokePermissionFromRoleCommand`

Remove permissão.

Permissão:

```text
authorization.permission.revoke
```

Payload:

```json
{
  "role_id": "uuid",
  "permission_code": "production.execution.start",
  "reason": "Perfil revisado"
}
```

Evento resultante:

```text
authorization.permission_revoked
```

---

## `AssignRoleCommand`

Atribui role a um Membership.

Permissão:

```text
authorization.role.assign
```

Payload:

```json
{
  "membership_id": "uuid",
  "role_id": "uuid"
}
```

Validações:

* role pertence ao Tenant;
* Membership ativo;
* não duplicar atribuição;
* não permitir escalada indevida.

Evento resultante:

```text
authorization.role_assigned
```

---

## `RemoveRoleCommand`

Remove role de um Membership.

Permissão:

```text
authorization.role.remove
```

Payload:

```json
{
  "membership_id": "uuid",
  "role_id": "uuid",
  "reason": "Alteração de função"
}
```

Validações:

* não remover último administrador;
* preservar acesso mínimo quando exigido.

Evento resultante:

```text
authorization.role_removed
```

---

## `CreatePermissionCommand`

Cria nova permissão da plataforma.

Permissão:

```text
platform.permission.create
```

Payload:

```json
{
  "code": "production.execution.start",
  "name": "Iniciar execução",
  "description": "Permite iniciar operação atribuída",
  "capability_code": "production_execution"
}
```

Evento resultante:

```text
authorization.permission_created
```

---

## `UpdatePermissionCommand`

Atualiza metadados da permissão.

Permissão:

```text
platform.permission.update
```

Payload:

```json
{
  "permission_id": "uuid",
  "name": "Iniciar execução produtiva",
  "description": "Descrição atualizada"
}
```

Evento resultante:

```text
authorization.permission_updated
```

O código da permissão não deverá ser alterado depois de utilizado.

---

## `RecalculateMembershipPermissionsCommand`

Reconstrói permissões efetivas do Membership.

Permissão:

```text
authorization.permissions.recalculate
```

Payload:

```json
{
  "membership_id": "uuid",
  "reason": "ROLE_CHANGED"
}
```

Evento resultante:

```text
authorization.permissions_recalculated
```

---

# 22. Comandos de CRM

## `CreateLeadCommand`

Cria um lead.

Permissão:

```text
crm.lead.create
```

Payload:

```json
{
  "name": "Cliente potencial",
  "source": "WHATSAPP",
  "assigned_user_id": "uuid",
  "contact_data": {},
  "notes": "Solicitou orçamento"
}
```

Evento resultante:

```text
crm.lead_created
```

---

## `UpdateLeadCommand`

Atualiza lead.

Permissão:

```text
crm.lead.update
```

Payload:

```json
{
  "lead_id": "uuid",
  "name": "Nome atualizado",
  "assigned_user_id": "uuid",
  "contact_data": {},
  "notes": "Novo contato"
}
```

Evento resultante:

```text
crm.lead_updated
```

---

## `QualifyLeadCommand`

Classifica o lead.

Permissão:

```text
crm.lead.qualify
```

Payload:

```json
{
  "lead_id": "uuid",
  "qualification": "QUALIFIED",
  "notes": "Projeto confirmado"
}
```

Evento resultante:

```text
crm.lead_qualified
```

---

## `ConvertLeadToCustomerCommand`

Converte lead em cliente.

Permissão:

```text
crm.lead.convert
```

Payload:

```json
{
  "lead_id": "uuid",
  "customer_data": {
    "name": "Cliente",
    "person_type": "INDIVIDUAL",
    "tax_id": "string",
    "contact_data": {},
    "address": {}
  }
}
```

Eventos resultantes:

```text
crm.customer_created
crm.lead_converted
```

---

## `ArchiveLeadCommand`

Arquiva lead.

Permissão:

```text
crm.lead.archive
```

Payload:

```json
{
  "lead_id": "uuid",
  "reason_code": "NO_INTEREST",
  "notes": "Cliente desistiu"
}
```

Evento resultante:

```text
crm.lead_archived
```

---

## `CreateCustomerCommand`

Cria cliente.

Permissão:

```text
crm.customer.create
```

Payload:

```json
{
  "code": "CLI-000001",
  "name": "Cliente",
  "person_type": "INDIVIDUAL",
  "tax_id": "string",
  "contact_data": {},
  "address": {}
}
```

Validações:

* documento fiscal quando exigido;
* duplicidade por documento;
* duplicidade aproximada poderá gerar alerta;
* código único.

Evento resultante:

```text
crm.customer_created
```

---

## `UpdateCustomerCommand`

Atualiza cliente.

Permissão:

```text
crm.customer.update
```

Payload:

```json
{
  "customer_id": "uuid",
  "name": "Nome atualizado",
  "tax_id": "string",
  "contact_data": {},
  "address": {}
}
```

Evento resultante:

```text
crm.customer_updated
```

---

## `ArchiveCustomerCommand`

Arquiva cliente.

Permissão:

```text
crm.customer.archive
```

Payload:

```json
{
  "customer_id": "uuid",
  "reason": "Cadastro duplicado",
  "replacement_customer_id": "uuid"
}
```

Validações:

* verificar contratos;
* verificar contas financeiras;
* verificar ordens abertas;
* não apagar histórico.

Evento resultante:

```text
crm.customer_archived
```

---

## `MergeCustomersCommand`

Consolida cadastros duplicados.

Permissão:

```text
crm.customer.merge
```

Payload:

```json
{
  "source_customer_id": "uuid",
  "target_customer_id": "uuid",
  "merge_strategy": {
    "contacts": "COMBINE",
    "addresses": "COMBINE",
    "tax_id": "TARGET"
  },
  "reason": "Cadastros duplicados"
}
```

Regras:

* operação irreversível sem processo administrativo;
* vínculos migram para o cliente de destino;
* origem é arquivada;
* auditoria completa obrigatória.

Evento resultante:

```text
crm.customers_merged
```

---

## `AddCustomerContactCommand`

Adiciona contato.

Permissão:

```text
crm.customer.contact.create
```

Payload:

```json
{
  "customer_id": "uuid",
  "contact_type": "PHONE",
  "value": "string",
  "label": "Principal",
  "is_primary": true
}
```

Evento resultante:

```text
crm.customer_contact_added
```

---

## `UpdateCustomerContactCommand`

Atualiza contato.

Permissão:

```text
crm.customer.contact.update
```

Payload:

```json
{
  "customer_id": "uuid",
  "contact_id": "uuid",
  "value": "string",
  "label": "Comercial",
  "is_primary": true
}
```

Evento resultante:

```text
crm.customer_contact_updated
```

---

## `RemoveCustomerContactCommand`

Remove contato ativo sem apagar histórico.

Permissão:

```text
crm.customer.contact.remove
```

Payload:

```json
{
  "customer_id": "uuid",
  "contact_id": "uuid",
  "reason": "Número desativado"
}
```

Evento resultante:

```text
crm.customer_contact_removed
```

---

## `AddCustomerAddressCommand`

Adiciona endereço.

Permissão:

```text
crm.customer.address.create
```

Payload:

```json
{
  "customer_id": "uuid",
  "address_type": "INSTALLATION",
  "address": {},
  "is_primary": false
}
```

Evento resultante:

```text
crm.customer_address_added
```

---

## `UpdateCustomerAddressCommand`

Atualiza endereço.

Permissão:

```text
crm.customer.address.update
```

Payload:

```json
{
  "customer_id": "uuid",
  "address_id": "uuid",
  "address": {},
  "is_primary": true
}
```

Evento resultante:

```text
crm.customer_address_updated
```

---

## `CreateOpportunityCommand`

Cria oportunidade comercial.

Permissão:

```text
crm.opportunity.create
```

Payload:

```json
{
  "customer_id": "uuid",
  "title": "Cozinha planejada",
  "description": "Projeto completo",
  "estimated_value": "25000.00",
  "assigned_user_id": "uuid",
  "expected_close_date": "date"
}
```

Evento resultante:

```text
crm.opportunity_created
```

---

## `UpdateOpportunityCommand`

Atualiza oportunidade.

Permissão:

```text
crm.opportunity.update
```

Payload:

```json
{
  "opportunity_id": "uuid",
  "title": "Projeto completo",
  "estimated_value": "27000.00",
  "assigned_user_id": "uuid",
  "expected_close_date": "date"
}
```

Evento resultante:

```text
crm.opportunity_updated
```

---

## `WinOpportunityCommand`

Marca oportunidade como ganha.

Permissão:

```text
crm.opportunity.win
```

Payload:

```json
{
  "opportunity_id": "uuid",
  "quotation_id": "uuid",
  "won_at": "datetime"
}
```

Evento resultante:

```text
crm.opportunity_won
```

---

## `LoseOpportunityCommand`

Marca oportunidade como perdida.

Permissão:

```text
crm.opportunity.lose
```

Payload:

```json
{
  "opportunity_id": "uuid",
  "loss_reason_code": "PRICE",
  "notes": "Cliente escolheu concorrente"
}
```

Evento resultante:

```text
crm.opportunity_lost
```

---

# 23. Continuação

A próxima parte continuará com:

```text
Commercial
Workflow
Production
Forms
Documents
Inventory
```

Fim da Parte 1.
# 24. Comandos de Commercial

## `CreateQuotationCommand`

Cria um novo orçamento comercial.

Permissão:

```text
commercial.quotation.create
```

Payload:

```json
{
  "customer_id": "uuid",
  "opportunity_id": "uuid",
  "code": "ORC-000001",
  "title": "Cozinha planejada",
  "description": "Projeto completo de cozinha",
  "currency": "BRL",
  "valid_until": "date",
  "payment_terms": {},
  "delivery_terms": {},
  "items": [
    {
      "item_type": "PRODUCT",
      "reference_id": "uuid",
      "description": "Cozinha planejada",
      "quantity": "1.0000",
      "unit": "UN",
      "unit_price": "25000.00",
      "discount_amount": "0.00"
    }
  ]
}
```

Validações:

* cliente ativo;
* código único por Tenant;
* itens válidos;
* quantidades positivas;
* valores não negativos;
* moeda suportada;
* prazo de validade válido;
* oportunidade pertencente ao mesmo cliente, quando informada.

Eventos resultantes:

```text
commercial.quotation_created
commercial.quotation_version_created
```

---

## `CreateQuotationVersionCommand`

Cria uma nova versão do orçamento.

Permissão:

```text
commercial.quotation.version.create
```

Payload:

```json
{
  "quotation_id": "uuid",
  "change_reason": "Alteração solicitada pelo cliente",
  "valid_until": "date",
  "payment_terms": {},
  "delivery_terms": {},
  "items": [
    {
      "item_type": "PRODUCT",
      "reference_id": "uuid",
      "description": "Cozinha revisada",
      "quantity": "1.0000",
      "unit": "UN",
      "unit_price": "27000.00",
      "discount_amount": "0.00"
    }
  ]
}
```

Regras:

* a versão anterior permanece imutável;
* não alterar orçamento cancelado ou arquivado;
* aprovação anterior poderá ser invalidada conforme política;
* nova versão recebe número sequencial;
* total deve ser recalculado pelo domínio.

Evento resultante:

```text
commercial.quotation_version_created
```

---

## `UpdateQuotationDraftCommand`

Atualiza a versão atual enquanto ainda estiver em rascunho.

Permissão:

```text
commercial.quotation.update
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "title": "Projeto revisado",
  "description": "Descrição atualizada",
  "valid_until": "date",
  "payment_terms": {},
  "delivery_terms": {},
  "items": []
}
```

Validações:

* somente versão em rascunho;
* versão deve ser a atual;
* concorrência otimista obrigatória;
* valores recalculados pelo domínio;
* não editar versão já enviada ou aprovada.

Evento resultante:

```text
commercial.quotation_draft_updated
```

---

## `AddQuotationItemCommand`

Adiciona item à versão atual do orçamento.

Permissão:

```text
commercial.quotation.item.create
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "item_type": "SERVICE",
  "reference_id": "uuid",
  "description": "Instalação",
  "quantity": "1.0000",
  "unit": "SV",
  "unit_price": "1500.00",
  "discount_amount": "0.00"
}
```

Evento resultante:

```text
commercial.quotation_item_added
```

---

## `UpdateQuotationItemCommand`

Atualiza item de uma versão em rascunho.

Permissão:

```text
commercial.quotation.item.update
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "quotation_item_id": "uuid",
  "description": "Instalação completa",
  "quantity": "1.0000",
  "unit": "SV",
  "unit_price": "1800.00",
  "discount_amount": "100.00"
}
```

Evento resultante:

```text
commercial.quotation_item_updated
```

---

## `RemoveQuotationItemCommand`

Remove item da versão em rascunho.

Permissão:

```text
commercial.quotation.item.remove
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "quotation_item_id": "uuid",
  "reason": "Item retirado pelo cliente"
}
```

Validações:

* não deixar orçamento inválido;
* preservar auditoria;
* somente versão em rascunho.

Evento resultante:

```text
commercial.quotation_item_removed
```

---

## `ApplyQuotationDiscountCommand`

Aplica desconto controlado.

Permissão:

```text
commercial.quotation.discount.apply
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "discount_type": "PERCENTAGE",
  "discount_value": "5.00",
  "reason": "Condição comercial negociada"
}
```

Validações:

* respeitar limite da permissão;
* desconto não pode tornar total negativo;
* descontos acima do limite exigem aprovação;
* registrar justificativa.

Eventos possíveis:

```text
commercial.quotation_discount_applied
commercial.quotation_discount_approval_requested
```

---

## `RemoveQuotationDiscountCommand`

Remove desconto aplicado.

Permissão:

```text
commercial.quotation.discount.remove
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "reason": "Condição comercial cancelada"
}
```

Evento resultante:

```text
commercial.quotation_discount_removed
```

---

## `SendQuotationCommand`

Registra o envio da versão atual ao cliente.

Permissão:

```text
commercial.quotation.send
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "delivery_channel": "WHATSAPP",
  "recipient": "masked",
  "document_id": "uuid",
  "sent_at": "datetime"
}
```

Validações:

* versão atual válida;
* documento gerado;
* cliente com contato compatível;
* orçamento não expirado;
* versão não cancelada.

Evento resultante:

```text
commercial.quotation_sent
```

---

## `ApproveQuotationCommand`

Aprova uma versão do orçamento.

Permissão:

```text
commercial.quotation.approve
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "approval_method": "SIGNED_CONTRACT",
  "approved_at": "datetime",
  "evidence_document_id": "uuid",
  "notes": "Aprovado pelo cliente"
}
```

Validações:

* versão atual;
* orçamento válido;
* cliente ativo;
* aprovação não duplicada;
* evidência exigida conforme configuração;
* condições de pagamento válidas;
* permissão do ator.

Eventos resultantes:

```text
commercial.quotation_approved
crm.opportunity_won
```

Reações esperadas:

* criar contrato ou pedido de venda;
* gerar conta a receber conforme configuração;
* iniciar produção;
* concluir workflow comercial;
* notificar responsáveis.

---

## `RejectQuotationCommand`

Registra rejeição do orçamento.

Permissão:

```text
commercial.quotation.reject
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "reason_code": "PRICE",
  "notes": "Cliente considerou o valor acima do esperado"
}
```

Evento resultante:

```text
commercial.quotation_rejected
```

---

## `CancelQuotationCommand`

Cancela orçamento ainda não convertido.

Permissão:

```text
commercial.quotation.cancel
```

Payload:

```json
{
  "quotation_id": "uuid",
  "reason_code": "CUSTOMER_CANCELLED",
  "reason": "Cliente cancelou o projeto"
}
```

Validações:

* verificar contrato;
* verificar pedido de venda;
* verificar produção;
* não cancelar silenciosamente processos derivados;
* acionar compensações quando necessário.

Evento resultante:

```text
commercial.quotation_cancelled
```

---

## `ArchiveQuotationCommand`

Arquiva orçamento encerrado.

Permissão:

```text
commercial.quotation.archive
```

Payload:

```json
{
  "quotation_id": "uuid",
  "reason": "Orçamento substituído"
}
```

Evento resultante:

```text
commercial.quotation_archived
```

---

## `ReopenQuotationCommand`

Reabre orçamento encerrado quando permitido.

Permissão:

```text
commercial.quotation.reopen
```

Payload:

```json
{
  "quotation_id": "uuid",
  "reason": "Cliente retomou a negociação"
}
```

Validações:

* não reabrir contrato ou pedido automaticamente;
* criar nova versão quando necessário;
* preservar aprovação anterior;
* verificar expiração.

Evento resultante:

```text
commercial.quotation_reopened
```

---

## `CreateContractCommand`

Cria contrato a partir de orçamento aprovado.

Permissão:

```text
commercial.contract.create
```

Payload:

```json
{
  "quotation_id": "uuid",
  "quotation_version_id": "uuid",
  "customer_id": "uuid",
  "code": "CTR-000001",
  "effective_date": "date",
  "expiration_date": "date",
  "payment_terms": {},
  "delivery_terms": {},
  "clauses": []
}
```

Validações:

* orçamento aprovado;
* versão correta;
* cliente correspondente;
* código único;
* datas coerentes;
* cláusulas obrigatórias presentes.

Evento resultante:

```text
commercial.contract_created
```

---

## `CreateContractVersionCommand`

Cria uma nova versão do contrato.

Permissão:

```text
commercial.contract.version.create
```

Payload:

```json
{
  "contract_id": "uuid",
  "change_reason": "Alteração de prazo",
  "effective_date": "date",
  "expiration_date": "date",
  "payment_terms": {},
  "delivery_terms": {},
  "clauses": []
}
```

Regras:

* versão anterior permanece imutável;
* contrato assinado exige aditivo ou política específica;
* alteração crítica pode invalidar assinaturas.

Evento resultante:

```text
commercial.contract_version_created
```

---

## `SignContractCommand`

Registra assinatura do contrato.

Permissão:

```text
commercial.contract.sign
```

Payload:

```json
{
  "contract_id": "uuid",
  "contract_version_id": "uuid",
  "signature_method": "DIGITAL",
  "signed_at": "datetime",
  "signature_document_id": "uuid",
  "signatories": [
    {
      "party_type": "CUSTOMER",
      "party_id": "uuid"
    }
  ]
}
```

Validações:

* versão atual;
* documento válido;
* signatários obrigatórios;
* assinatura não duplicada;
* contrato não cancelado.

Evento resultante:

```text
commercial.contract_signed
```

---

## `CancelContractCommand`

Cancela contrato conforme regras legais e operacionais.

Permissão:

```text
commercial.contract.cancel
```

Payload:

```json
{
  "contract_id": "uuid",
  "reason_code": "MUTUAL_AGREEMENT",
  "reason": "Cancelamento acordado",
  "effective_at": "datetime",
  "cancellation_document_id": "uuid"
}
```

Validações:

* impacto financeiro;
* impacto produtivo;
* impacto fiscal;
* documento comprobatório quando exigido;
* autorização especial.

Evento resultante:

```text
commercial.contract_cancelled
```

---

## `CreateSalesOrderCommand`

Cria pedido de venda.

Permissão:

```text
commercial.sales_order.create
```

Payload:

```json
{
  "quotation_id": "uuid",
  "contract_id": "uuid",
  "customer_id": "uuid",
  "code": "PED-000001",
  "order_date": "date",
  "expected_delivery_date": "date",
  "items": []
}
```

Validações:

* origem válida;
* cliente correspondente;
* código único;
* itens aprovados;
* datas coerentes;
* não duplicar pedido para mesma origem, salvo política explícita.

Evento resultante:

```text
commercial.sales_order_created
```

---

## `UpdateSalesOrderCommand`

Atualiza pedido antes de sua liberação.

Permissão:

```text
commercial.sales_order.update
```

Payload:

```json
{
  "sales_order_id": "uuid",
  "expected_delivery_date": "date",
  "delivery_address_id": "uuid",
  "notes": "Entrega agendada"
}
```

Validações:

* não alterar itens já liberados para produção sem revisão;
* concorrência obrigatória;
* preservar histórico.

Evento resultante:

```text
commercial.sales_order_updated
```

---

## `ReleaseSalesOrderCommand`

Libera pedido para processamento.

Permissão:

```text
commercial.sales_order.release
```

Payload:

```json
{
  "sales_order_id": "uuid",
  "released_at": "datetime"
}
```

Validações:

* pedido completo;
* contrato ou aprovação válida;
* condições financeiras satisfeitas conforme configuração;
* itens consistentes.

Evento resultante:

```text
commercial.sales_order_released
```

---

## `CancelSalesOrderCommand`

Cancela pedido de venda.

Permissão:

```text
commercial.sales_order.cancel
```

Payload:

```json
{
  "sales_order_id": "uuid",
  "reason_code": "CUSTOMER_CANCELLED",
  "reason": "Cliente solicitou cancelamento"
}
```

Validações:

* verificar produção;
* liberar reservas;
* avaliar contas financeiras;
* avaliar documentos fiscais;
* exigir autorização quando já liberado.

Evento resultante:

```text
commercial.sales_order_cancelled
```

---

# 25. Comandos de Workflow

## `CreateWorkflowDefinitionCommand`

Cria definição de workflow.

Permissão:

```text
workflow.definition.create
```

Payload:

```json
{
  "code": "PRODUCTION_DEFAULT",
  "name": "Produção padrão",
  "kind": "PRODUCTION",
  "description": "Fluxo produtivo principal"
}
```

Validações:

* código único por Tenant;
* tipo suportado;
* nome válido.

Evento resultante:

```text
workflow.definition_created
```

---

## `UpdateWorkflowDefinitionCommand`

Atualiza metadados da definição.

Permissão:

```text
workflow.definition.update
```

Payload:

```json
{
  "workflow_definition_id": "uuid",
  "name": "Produção padrão revisada",
  "description": "Descrição atualizada"
}
```

Não altera versões já publicadas.

Evento resultante:

```text
workflow.definition_updated
```

---

## `ArchiveWorkflowDefinitionCommand`

Arquiva definição.

Permissão:

```text
workflow.definition.archive
```

Payload:

```json
{
  "workflow_definition_id": "uuid",
  "reason": "Fluxo substituído",
  "replacement_workflow_definition_id": "uuid"
}
```

Validações:

* instâncias abertas;
* uso em configurações;
* workflow padrão;
* versão substituta quando exigida.

Evento resultante:

```text
workflow.definition_archived
```

---

## `CreateWorkflowVersionCommand`

Cria versão editável de um workflow.

Permissão:

```text
workflow.version.create
```

Payload:

```json
{
  "workflow_definition_id": "uuid",
  "based_on_version_id": "uuid",
  "change_reason": "Inclusão da etapa de limpeza"
}
```

Regras:

* número sequencial;
* cópia controlada da versão base;
* nova versão inicia em rascunho.

Evento resultante:

```text
workflow.version_created
```

---

## `AddWorkflowStageCommand`

Adiciona etapa à versão em rascunho.

Permissão:

```text
workflow.stage.create
```

Payload:

```json
{
  "workflow_version_id": "uuid",
  "code": "CUTTING",
  "name": "Corte",
  "order_index": 2,
  "is_initial": false,
  "is_terminal": false,
  "wip_limit": null,
  "configuration": {}
}
```

Validações:

* versão não publicada;
* código único na versão;
* ordem válida;
* etapa inicial única;
* etapa terminal coerente.

Evento resultante:

```text
workflow.stage_created
```

---

## `UpdateWorkflowStageCommand`

Atualiza etapa em versão não publicada.

Permissão:

```text
workflow.stage.update
```

Payload:

```json
{
  "workflow_version_id": "uuid",
  "stage_definition_id": "uuid",
  "name": "Corte e usinagem",
  "order_index": 2,
  "wip_limit": 10,
  "configuration": {}
}
```

Evento resultante:

```text
workflow.stage_updated
```

---

## `RemoveWorkflowStageCommand`

Remove etapa de versão em rascunho.

Permissão:

```text
workflow.stage.remove
```

Payload:

```json
{
  "workflow_version_id": "uuid",
  "stage_definition_id": "uuid",
  "reason": "Etapa consolidada com montagem"
}
```

Validações:

* versão não publicada;
* remover transições vinculadas explicitamente;
* preservar pelo menos etapa inicial e terminal;
* não deixar operações órfãs.

Evento resultante:

```text
workflow.stage_removed
```

---

## `ReorderWorkflowStagesCommand`

Reordena etapas.

Permissão:

```text
workflow.stage.reorder
```

Payload:

```json
{
  "workflow_version_id": "uuid",
  "stage_order": [
    {
      "stage_definition_id": "uuid",
      "order_index": 1
    }
  ]
}
```

Evento resultante:

```text
workflow.stages_reordered
```

---

## `CreateWorkflowTransitionCommand`

Cria transição entre etapas.

Permissão:

```text
workflow.transition.create
```

Payload:

```json
{
  "workflow_version_id": "uuid",
  "source_stage_id": "uuid",
  "target_stage_id": "uuid",
  "name": "Enviar para corte",
  "requires_justification": false,
  "conditions": {},
  "actions": []
}
```

Validações:

* etapas da mesma versão;
* impedir duplicidade;
* impedir transição inválida;
* ciclos somente quando autorizados;
* condições válidas.

Evento resultante:

```text
workflow.transition_created
```

---

## `UpdateWorkflowTransitionCommand`

Atualiza transição.

Permissão:

```text
workflow.transition.update
```

Payload:

```json
{
  "transition_definition_id": "uuid",
  "name": "Avançar para corte",
  "requires_justification": true,
  "conditions": {},
  "actions": []
}
```

Evento resultante:

```text
workflow.transition_updated
```

---

## `RemoveWorkflowTransitionCommand`

Remove transição.

Permissão:

```text
workflow.transition.remove
```

Payload:

```json
{
  "transition_definition_id": "uuid",
  "reason": "Transição não utilizada"
}
```

Evento resultante:

```text
workflow.transition_removed
```

---

## `AddOperationDefinitionCommand`

Adiciona definição de operação a uma etapa.

Permissão:

```text
workflow.operation_definition.create
```

Payload:

```json
{
  "stage_definition_id": "uuid",
  "code": "CUT_STRUCTURE",
  "name": "Corte da estrutura",
  "description": "Cortar peças estruturais",
  "order_index": 1,
  "is_required": true,
  "allow_multiple_executions": true,
  "allow_parallel_executions": false,
  "default_estimated_minutes": 120,
  "configuration": {}
}
```

Evento resultante:

```text
workflow.operation_definition_created
```

---

## `UpdateOperationDefinitionCommand`

Atualiza definição de operação.

Permissão:

```text
workflow.operation_definition.update
```

Payload:

```json
{
  "operation_definition_id": "uuid",
  "name": "Corte estrutural",
  "description": "Descrição revisada",
  "order_index": 1,
  "is_required": true,
  "default_estimated_minutes": 150,
  "configuration": {}
}
```

Evento resultante:

```text
workflow.operation_definition_updated
```

---

## `RemoveOperationDefinitionCommand`

Remove definição de operação de versão em rascunho.

Permissão:

```text
workflow.operation_definition.remove
```

Payload:

```json
{
  "operation_definition_id": "uuid",
  "reason": "Operação substituída"
}
```

Evento resultante:

```text
workflow.operation_definition_removed
```

---

## `PublishWorkflowVersionCommand`

Publica versão do workflow.

Permissão:

```text
workflow.version.publish
```

Payload:

```json
{
  "workflow_version_id": "uuid",
  "publication_notes": "Versão aprovada para uso"
}
```

Validações:

* uma etapa inicial;
* pelo menos uma etapa terminal;
* todas as etapas alcançáveis;
* transições coerentes;
* códigos únicos;
* operações válidas;
* formulários obrigatórios válidos;
* configuração sem referências quebradas.

Evento resultante:

```text
workflow.version_published
```

Após publicação, a versão é imutável.

---

## `DeprecateWorkflowVersionCommand`

Marca versão publicada como obsoleta para novas instâncias.

Permissão:

```text
workflow.version.deprecate
```

Payload:

```json
{
  "workflow_version_id": "uuid",
  "replacement_workflow_version_id": "uuid",
  "reason": "Nova versão publicada"
}
```

Evento resultante:

```text
workflow.version_deprecated
```

---

## `CreateWorkflowInstanceCommand`

Cria instância de workflow.

Permissão:

```text
workflow.instance.create
```

Payload:

```json
{
  "workflow_definition_id": "uuid",
  "workflow_version_id": "uuid",
  "code": "WF-000001",
  "title": "Produção Cliente X",
  "description": "Projeto de cozinha",
  "reference_type": "PRODUCTION_ORDER",
  "reference_id": "uuid",
  "customer_id": "uuid",
  "priority": "NORMAL",
  "due_at": "datetime",
  "dynamic_data": {}
}
```

Validações:

* versão publicada;
* referência autorizada;
* etapa inicial válida;
* código único;
* campos obrigatórios preenchidos.

Evento resultante:

```text
workflow.instance_created
```

---

## `MoveWorkflowInstanceCommand`

Move instância para outra etapa.

Permissão:

```text
workflow.instance.move
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "transition_definition_id": "uuid",
  "target_stage_id": "uuid",
  "justification": null,
  "dynamic_data": {}
}
```

Validações:

* instância ativa;
* transição válida;
* origem correspondente;
* condições satisfeitas;
* checklists obrigatórios concluídos;
* operações obrigatórias concluídas;
* WIP respeitado;
* permissão e escopo.

Evento resultante:

```text
workflow.stage_changed
```

---

## `ReturnWorkflowInstanceCommand`

Retorna instância a etapa anterior ou permitida.

Permissão:

```text
workflow.instance.return
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "target_stage_id": "uuid",
  "reason_code": "REWORK",
  "reason": "Necessário corrigir montagem"
}
```

Validações:

* retorno permitido;
* justificativa obrigatória;
* impacto em operações;
* possível criação de retrabalho.

Eventos possíveis:

```text
workflow.instance_returned
workflow.stage_changed
```

---

## `SkipWorkflowStageCommand`

Ignora etapa autorizada.

Permissão:

```text
workflow.stage.skip
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "skipped_stage_id": "uuid",
  "target_stage_id": "uuid",
  "justification": "Etapa não aplicável"
}
```

Validações:

* configuração permite;
* permissão especial;
* justificativa;
* operações obrigatórias avaliadas.

Eventos resultantes:

```text
workflow.stage_skipped
workflow.stage_changed
```

---

## `PauseWorkflowInstanceCommand`

Pausa workflow.

Permissão:

```text
workflow.instance.pause
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "reason_code": "MATERIAL_UNAVAILABLE",
  "reason": "Aguardando material"
}
```

Evento resultante:

```text
workflow.instance_paused
```

---

## `ResumeWorkflowInstanceCommand`

Retoma workflow pausado.

Permissão:

```text
workflow.instance.resume
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "reason": "Material disponível"
}
```

Evento resultante:

```text
workflow.instance_resumed
```

---

## `CompleteWorkflowInstanceCommand`

Conclui workflow.

Permissão:

```text
workflow.instance.complete
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "terminal_stage_id": "uuid",
  "completion_notes": "Processo concluído"
}
```

Validações:

* etapa terminal;
* operações obrigatórias concluídas;
* formulários obrigatórios concluídos;
* nenhuma pendência bloqueante;
* documentos obrigatórios presentes.

Evento resultante:

```text
workflow.instance_completed
```

---

## `CancelWorkflowInstanceCommand`

Cancela workflow.

Permissão:

```text
workflow.instance.cancel
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "reason_code": "SOURCE_CANCELLED",
  "reason": "Pedido de origem cancelado"
}
```

Validações:

* impacto em produção;
* operações em andamento;
* reservas;
* agenda;
* documentos;
* processos dependentes.

Evento resultante:

```text
workflow.instance_cancelled
```

---

## `AssignWorkflowInstanceCommand`

Atribui responsável.

Permissão:

```text
workflow.instance.assign
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "assignment_type": "USER",
  "assignee_id": "uuid",
  "role_in_workflow": "RESPONSIBLE"
}
```

Evento resultante:

```text
workflow.instance_assigned
```

---

## `UnassignWorkflowInstanceCommand`

Remove atribuição.

Permissão:

```text
workflow.instance.unassign
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "assignment_id": "uuid",
  "reason": "Responsável substituído"
}
```

Evento resultante:

```text
workflow.instance_unassigned
```

---

## `MigrateWorkflowInstanceVersionCommand`

Migra instância existente para nova versão.

Permissão:

```text
workflow.instance.migrate_version
```

Payload:

```json
{
  "workflow_instance_id": "uuid",
  "target_workflow_version_id": "uuid",
  "stage_mapping": {
    "old-stage-id": "new-stage-id"
  },
  "operation_mapping": {},
  "reason": "Adequação ao novo processo"
}
```

Regras:

* operação administrativa de alto risco;
* simulação obrigatória;
* mapeamento completo;
* auditoria detalhada;
* não perder histórico;
* não alterar eventos passados.

Evento resultante:

```text
workflow.instance_version_migrated
```

---

# 26. Comandos de Production

## `CreateProductionOrderCommand`

Cria ordem de produção.

Permissão:

```text
production.order.create
```

Payload:

```json
{
  "sales_order_id": "uuid",
  "quotation_id": "uuid",
  "customer_id": "uuid",
  "code": "OP-000001",
  "title": "Cozinha Cliente X",
  "priority": "NORMAL",
  "planned_start_at": "datetime",
  "due_at": "datetime",
  "workflow_definition_id": "uuid",
  "items": [
    {
      "reference_type": "PROJECT_REVISION",
      "reference_id": "uuid",
      "description": "Cozinha planejada",
      "quantity": "1.0000"
    }
  ]
}
```

Validações:

* origem válida;
* cliente correspondente;
* workflow publicado;
* revisão técnica válida quando exigida;
* código único;
* não duplicar por origem.

Eventos resultantes:

```text
production.order_created
workflow.instance_created
```

---

## `UpdateProductionOrderCommand`

Atualiza ordem antes ou durante execução conforme regras.

Permissão:

```text
production.order.update
```

Payload:

```json
{
  "production_order_id": "uuid",
  "title": "Cozinha revisada",
  "priority": "HIGH",
  "planned_start_at": "datetime",
  "due_at": "datetime",
  "notes": "Prioridade alterada"
}
```

Validações:

* campos alteráveis dependem do status;
* prazo pode exigir replanejamento;
* prioridade pode exigir autorização;
* concorrência otimista.

Evento resultante:

```text
production.order_updated
```

---

## `ReleaseProductionOrderCommand`

Libera ordem para execução.

Permissão:

```text
production.order.release
```

Payload:

```json
{
  "production_order_id": "uuid",
  "released_at": "datetime"
}
```

Validações:

* projeto aprovado;
* operações geradas;
* materiais avaliados;
* documentos obrigatórios;
* workflow válido;
* pedido comercial liberado.

Evento resultante:

```text
production.order_released
```

---

## `GenerateProductionOperationsCommand`

Gera operações a partir da versão do workflow.

Permissão:

```text
production.operation.generate
```

Payload:

```json
{
  "production_order_id": "uuid",
  "workflow_version_id": "uuid",
  "regenerate": false
}
```

Validações:

* não duplicar operações;
* preservar operações já executadas;
* regeneração exige autorização;
* usar definições da versão vinculada.

Eventos resultantes:

```text
production.operation_created
```

Um evento poderá ser gerado por operação.

---

## `CreateOperationCommand`

Cria operação adicional manual.

Permissão:

```text
production.operation.create
```

Payload:

```json
{
  "production_order_id": "uuid",
  "stage_definition_id": "uuid",
  "operation_definition_id": "uuid",
  "name": "Ajuste especial",
  "order_index": 5,
  "is_required": true,
  "estimated_minutes": 60,
  "reason": "Necessidade específica do projeto"
}
```

Evento resultante:

```text
production.operation_created
```

---

## `UpdateOperationCommand`

Atualiza operação não concluída.

Permissão:

```text
production.operation.update
```

Payload:

```json
{
  "operation_instance_id": "uuid",
  "name": "Ajuste final",
  "estimated_minutes": 90,
  "priority": "HIGH",
  "dynamic_data": {}
}
```

Validações:

* operação não concluída;
* não alterar definição histórica indevidamente;
* impacto em agenda e atribuições.

Evento resultante:

```text
production.operation_updated
```

---

## `AssignEmployeeToOperationCommand`

Atribui funcionário à operação.

Permissão:

```text
production.operation.assign
```

Payload:

```json
{
  "operation_instance_id": "uuid",
  "employee_id": "uuid",
  "role_in_operation": "PRIMARY",
  "assigned_at": "datetime"
}
```

Validações:

* funcionário ativo;
* Tenant correto;
* escopo válido;
* habilidade quando exigida;
* ausência de duplicidade;
* operação disponível.

Evento resultante:

```text
production.operation_assigned
```

---

## `AssignTeamToOperationCommand`

Atribui equipe.

Permissão:

```text
production.operation.assign_team
```

Payload:

```json
{
  "operation_instance_id": "uuid",
  "employee_ids": [
    "uuid",
    "uuid"
  ],
  "primary_employee_id": "uuid"
}
```

Evento resultante:

```text
production.operation_assigned
```

---

## `UnassignEmployeeFromOperationCommand`

Remove atribuição.

Permissão:

```text
production.operation.unassign
```

Payload:

```json
{
  "operation_instance_id": "uuid",
  "employee_id": "uuid",
  "reason": "Reorganização da equipe"
}
```

Validações:

* não remover participante de execução ativa sem procedimento;
* manter responsável quando obrigatório.

Evento resultante:

```text
production.operation_unassigned
```

---

## `MarkOperationReadyCommand`

Marca operação como pronta.

Permissão:

```text
production.operation.mark_ready
```

Payload:

```json
{
  "operation_instance_id": "uuid"
}
```

Validações:

* dependências concluídas;
* materiais disponíveis quando exigido;
* documentos disponíveis;
* etapa correta.

Evento resultante:

```text
production.operation_ready
```

---

## `CreateExecutionCommand`

Cria execução para operação.

Permissão:

```text
production.execution.create
```

Payload:

```json
{
  "operation_instance_id": "uuid",
  "participant_employee_ids": [
    "uuid"
  ],
  "machine_ids": [],
  "notes": null
}
```

Validações:

* operação permite nova execução;
* operação não cancelada;
* paralelismo permitido;
* participantes autorizados;
* máquinas disponíveis.

Evento resultante:

```text
production.execution_created
```

---

## `StartExecutionCommand`

Inicia execução.

Permissão:

```text
production.execution.start
```

Payload:

```json
{
  "execution_id": "uuid",
  "operation_instance_id": "uuid",
  "employee_id": "uuid",
  "machine_ids": [],
  "started_at": "datetime"
}
```

Validações:

* execução criada ou pausada conforme comando;
* funcionário atribuído ou autorizado;
* operação pronta;
* etapa correta;
* não existir execução incompatível;
* máquina disponível;
* checklists iniciais concluídos;
* idempotência obrigatória.

Evento resultante:

```text
production.execution_started
```

---

## `JoinExecutionCommand`

Adiciona participante à execução ativa.

Permissão:

```text
production.execution.join
```

Payload:

```json
{
  "execution_id": "uuid",
  "employee_id": "uuid",
  "role_in_execution": "HELPER",
  "joined_at": "datetime"
}
```

Validações:

* execução ativa;
* funcionário não participante;
* permissão;
* não estar em execução incompatível, salvo política.

Evento resultante:

```text
production.execution_participant_joined
```

---

## `LeaveExecutionCommand`

Remove participante de execução ativa.

Permissão:

```text
production.execution.leave
```

Payload:

```json
{
  "execution_id": "uuid",
  "employee_id": "uuid",
  "left_at": "datetime",
  "reason": "Retorno à operação original"
}
```

Validações:

* participante ativo;
* execução mantém responsável quando obrigatório.

Evento resultante:

```text
production.execution_participant_left
```

---

## `PauseExecutionCommand`

Pausa execução.

Permissão:

```text
production.execution.pause
```

Payload:

```json
{
  "execution_id": "uuid",
  "category": "MATERIAL",
  "reason_code": "MISSING_PART",
  "reason_text": "Falta peça de fundo",
  "started_at": "datetime"
}
```

Validações:

* execução ativa;
* não existir pausa aberta;
* motivo obrigatório;
* categorias configuradas;
* idempotência.

Evento resultante:

```text
production.execution_paused
```

---

## `ResumeExecutionCommand`

Retoma execução pausada.

Permissão:

```text
production.execution.resume
```

Payload:

```json
{
  "execution_id": "uuid",
  "pause_id": "uuid",
  "resumed_at": "datetime"
}
```

Validações:

* pausa aberta;
* motivo impeditivo resolvido quando exigido;
* participante autorizado.

Evento resultante:

```text
production.execution_resumed
```

---

## `FinishExecutionCommand`

Finaliza execução.

Permissão:

```text
production.execution.finish
```

Payload:

```json
{
  "execution_id": "uuid",
  "finished_at": "datetime",
  "result": "COMPLETED",
  "notes": "Operação concluída",
  "produced_quantity": "1.0000",
  "rejected_quantity": "0.0000"
}
```

Validações:

* execução ativa;
* nenhuma pausa aberta;
* checklists finais concluídos;
* quantidades válidas;
* resultado válido;
* participantes encerrados;
* máquina liberada;
* idempotência.

Eventos resultantes:

```text
production.execution_finished
production.operation_completed
```

O segundo ocorre quando a operação estiver integralmente concluída.

---

## `CancelExecutionCommand`

Cancela execução sem conclusão.

Permissão:

```text
production.execution.cancel
```

Payload:

```json
{
  "execution_id": "uuid",
  "reason_code": "CREATED_BY_MISTAKE",
  "reason": "Execução aberta incorretamente"
}
```

Validações:

* não ocultar tempo já registrado;
* autorização especial se houve trabalho;
* preservar histórico.

Evento resultante:

```text
production.execution_cancelled
```

---

## `SkipOperationCommand`

Ignora operação quando permitido.

Permissão:

```text
production.operation.skip
```

Payload:

```json
{
  "operation_instance_id": "uuid",
  "reason_code": "NOT_APPLICABLE",
  "reason": "Operação não se aplica ao serviço"
}
```

Validações:

* configuração permite;
* operação não iniciada;
* justificativa;
* permissão especial para operação obrigatória.

Evento resultante:

```text
production.operation_skipped
```

---

## `RequestReworkCommand`

Solicita retrabalho.

Permissão:

```text
production.rework.request
```

Payload:

```json
{
  "original_operation_instance_id": "uuid",
  "reason_code": "MANUFACTURING_ERROR",
  "reason": "Peça fora da medida",
  "responsible_employee_id": "uuid",
  "quality_nonconformity_id": "uuid",
  "estimated_minutes": 90
}
```

Validações:

* operação original existente;
* motivo válido;
* não alterar operação original;
* nova operação vinculada;
* responsabilidade opcional conforme política.

Eventos resultantes:

```text
production.rework_requested
production.operation_created
```

---

## `CompleteOperationCommand`

Conclui operação administrativamente.

Permissão:

```text
production.operation.complete
```

Payload:

```json
{
  "operation_instance_id": "uuid",
  "completion_reason": "Todas as execuções concluídas"
}
```

Validações:

* execuções concluídas;
* formulários obrigatórios;
* inspeções aprovadas quando exigidas;
* nenhuma pendência.

Evento resultante:

```text
production.operation_completed
```

---

## `RequestMaterialCommand`

Solicita material para produção.

Permissão:

```text
production.material.request
```

Payload:

```json
{
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "requested_by_employee_id": "uuid",
  "priority": "HIGH",
  "notes": "Material necessário para continuar",
  "items": [
    {
      "material_id": "uuid",
      "quantity": "2.0000",
      "unit": "UN"
    }
  ]
}
```

Validações:

* material válido;
* quantidade positiva;
* operação correspondente;
* evitar solicitação duplicada aberta;
* idempotência.

Evento resultante:

```text
production.material_requested
```

---

## `ReportMachineIncidentCommand`

Registra problema com máquina.

Permissão:

```text
production.machine_incident.report
```

Payload:

```json
{
  "execution_id": "uuid",
  "machine_id": "uuid",
  "description": "Máquina parou durante o corte",
  "severity": "HIGH",
  "reported_at": "datetime"
}
```

Eventos resultantes:

```text
production.machine_incident_reported
incident.created
maintenance.machine_unavailable
```

As reações podem ocorrer de forma assíncrona.

---

## `CompleteProductionOrderCommand`

Conclui ordem.

Permissão:

```text
production.order.complete
```

Payload:

```json
{
  "production_order_id": "uuid",
  "completed_at": "datetime",
  "completion_notes": "Produção finalizada"
}
```

Validações:

* operações obrigatórias concluídas;
* workflow em etapa terminal;
* checklists;
* qualidade;
* documentos;
* nenhuma ocorrência bloqueante;
* materiais regularizados.

Eventos resultantes:

```text
production.order_completed
workflow.instance_completed
```

---

## `CancelProductionOrderCommand`

Cancela ordem.

Permissão:

```text
production.order.cancel
```

Payload:

```json
{
  "production_order_id": "uuid",
  "reason_code": "CUSTOMER_CANCELLED",
  "reason": "Pedido cancelado"
}
```

Validações:

* execuções ativas;
* materiais consumidos;
* reservas;
* agenda;
* contratos;
* financeiro;
* autorização especial após início.

Eventos resultantes:

```text
production.order_cancelled
workflow.instance_cancelled
```

---

# 27. Comandos de Forms

## `CreateFormDefinitionCommand`

Cria formulário ou checklist.

Permissão:

```text
forms.definition.create
```

Payload:

```json
{
  "code": "CUTTING_CHECKLIST",
  "name": "Checklist de corte",
  "category": "PRODUCTION",
  "is_checklist": true,
  "description": "Validação da etapa de corte"
}
```

Evento resultante:

```text
forms.definition_created
```

---

## `CreateFormVersionCommand`

Cria versão editável.

Permissão:

```text
forms.version.create
```

Payload:

```json
{
  "form_definition_id": "uuid",
  "based_on_version_id": "uuid",
  "change_reason": "Inclusão do campo de quantidade"
}
```

Evento resultante:

```text
forms.version_created
```

---

## `UpdateFormVersionSchemaCommand`

Atualiza schema de versão em rascunho.

Permissão:

```text
forms.version.update_schema
```

Payload:

```json
{
  "form_version_id": "uuid",
  "schema": {},
  "ui_schema": {},
  "rules": []
}
```

Validações:

* versão não publicada;
* schema válido;
* códigos de campo únicos;
* regras sem referências quebradas;
* tipos suportados.

Evento resultante:

```text
forms.version_schema_updated
```

---

## `PublishFormVersionCommand`

Publica versão.

Permissão:

```text
forms.version.publish
```

Payload:

```json
{
  "form_version_id": "uuid",
  "publication_notes": "Versão aprovada"
}
```

Validações:

* schema válido;
* campos obrigatórios coerentes;
* regras válidas;
* versão torna-se imutável.

Evento resultante:

```text
forms.version_published
```

---

## `CreateFormBindingCommand`

Vincula formulário a processo.

Permissão:

```text
forms.binding.create
```

Payload:

```json
{
  "form_definition_id": "uuid",
  "binding_type": "OPERATION",
  "workflow_definition_id": "uuid",
  "stage_definition_id": "uuid",
  "operation_definition_id": "uuid",
  "is_required": true,
  "trigger": "BEFORE_FINISH"
}
```

Validações:

* alvos válidos;
* vínculo coerente;
* formulário publicado;
* evitar duplicidade.

Evento resultante:

```text
forms.binding_created
```

---

## `RemoveFormBindingCommand`

Remove vínculo para novas execuções.

Permissão:

```text
forms.binding.remove
```

Payload:

```json
{
  "form_binding_id": "uuid",
  "reason": "Checklist substituído"
}
```

Evento resultante:

```text
forms.binding_removed
```

---

## `StartFormSubmissionCommand`

Inicia preenchimento.

Permissão:

```text
forms.submission.start
```

Payload:

```json
{
  "form_definition_id": "uuid",
  "form_version_id": "uuid",
  "workflow_instance_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_id": "uuid",
  "submitted_by_employee_id": "uuid"
}
```

Validações:

* versão publicada;
* vínculo aplicável;
* usuário autorizado;
* submissão repetível ou única conforme configuração.

Evento resultante:

```text
forms.submission_started
```

---

## `SaveFormSubmissionDraftCommand`

Salva rascunho.

Permissão:

```text
forms.submission.save_draft
```

Payload:

```json
{
  "form_submission_id": "uuid",
  "response_data": {}
}
```

Validações:

* submissão em rascunho;
* campos conhecidos;
* concorrência;
* validações parciais quando configuradas.

Evento resultante:

```text
forms.submission_draft_saved
```

---

## `CompleteFormSubmissionCommand`

Conclui formulário.

Permissão:

```text
forms.submission.complete
```

Payload:

```json
{
  "form_submission_id": "uuid",
  "response_data": {},
  "submitted_at": "datetime"
}
```

Validações:

* campos obrigatórios;
* regras condicionais;
* anexos obrigatórios;
* assinatura quando exigida;
* versão correta;
* idempotência.

Evento resultante:

```text
forms.submission_completed
```

---

## `ApproveFormSubmissionCommand`

Aprova submissão.

Permissão:

```text
forms.submission.approve
```

Payload:

```json
{
  "form_submission_id": "uuid",
  "approval_notes": "Checklist aprovado"
}
```

Evento resultante:

```text
forms.submission_approved
```

---

## `RejectFormSubmissionCommand`

Rejeita submissão.

Permissão:

```text
forms.submission.reject
```

Payload:

```json
{
  "form_submission_id": "uuid",
  "reason_code": "INVALID_MEASUREMENT",
  "reason": "Medida informada inconsistente"
}
```

Evento resultante:

```text
forms.submission_rejected
```

---

## `ReopenFormSubmissionCommand`

Reabre submissão concluída.

Permissão:

```text
forms.submission.reopen
```

Payload:

```json
{
  "form_submission_id": "uuid",
  "reason": "Correção autorizada"
}
```

Validações:

* permissão especial;
* preservar versão anterior ou histórico de alterações;
* auditoria detalhada.

Evento resultante:

```text
forms.submission_reopened
```

---

# 28. Comandos de Documents

## `CreateDocumentCommand`

Cria registro lógico de documento.

Permissão:

```text
documents.document.create
```

Payload:

```json
{
  "code": "DOC-000001",
  "title": "Plano de corte",
  "document_type": "CUTTING_PLAN",
  "category": "PRODUCTION",
  "description": "Plano de corte do projeto",
  "visibility_policy": {}
}
```

Evento resultante:

```text
documents.document_created
```

---

## `UploadDocumentVersionCommand`

Envia nova versão.

Permissão:

```text
documents.version.upload
```

Payload:

```json
{
  "document_id": "uuid",
  "original_filename": "plano_corte_v2.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 500000,
  "content_hash": "sha256",
  "storage_upload_reference": "string",
  "change_summary": "Correção das medidas",
  "metadata": {}
}
```

Validações:

* extensão permitida;
* MIME compatível;
* tamanho permitido;
* hash;
* arquivo validado;
* documento ativo;
* idempotência;
* não aceitar caminho absoluto do cliente.

Evento resultante:

```text
documents.version_uploaded
```

---

## `MarkDocumentVersionCurrentCommand`

Define versão atual.

Permissão:

```text
documents.version.mark_current
```

Payload:

```json
{
  "document_id": "uuid",
  "document_version_id": "uuid"
}
```

Validações:

* versão pertence ao documento;
* versão ativa;
* preservar versão anterior.

Evento resultante:

```text
documents.version_marked_current
```

---

## `LinkDocumentCommand`

Vincula documento a entidade.

Permissão:

```text
documents.document.link
```

Payload:

```json
{
  "document_id": "uuid",
  "entity_type": "PRODUCTION_ORDER",
  "entity_id": "uuid",
  "relationship_type": "TECHNICAL_REFERENCE"
}
```

Validações:

* entidade autorizada;
* Tenant correspondente;
* relação não duplicada;
* permissão de leitura sobre ambos.

Evento resultante:

```text
documents.link_created
```

---

## `UnlinkDocumentCommand`

Remove vínculo.

Permissão:

```text
documents.document.unlink
```

Payload:

```json
{
  "document_link_id": "uuid",
  "reason": "Documento vinculado incorretamente"
}
```

Evento resultante:

```text
documents.link_removed
```

---

## `UpdateDocumentMetadataCommand`

Atualiza metadados.

Permissão:

```text
documents.document.update
```

Payload:

```json
{
  "document_id": "uuid",
  "title": "Plano de corte revisado",
  "category": "PRODUCTION",
  "description": "Descrição atualizada"
}
```

Evento resultante:

```text
documents.document_updated
```

---

## `ChangeDocumentVisibilityCommand`

Altera política de visibilidade.

Permissão:

```text
documents.permission.change
```

Payload:

```json
{
  "document_id": "uuid",
  "visibility_policy": {
    "roles": [
      "PRODUCTION_OPERATOR"
    ],
    "assigned_only": false
  },
  "reason": "Disponibilizar para produção"
}
```

Evento resultante:

```text
documents.permission_changed
```

---

## `MarkDocumentObsoleteCommand`

Marca documento como obsoleto.

Permissão:

```text
documents.document.mark_obsolete
```

Payload:

```json
{
  "document_id": "uuid",
  "reason": "Substituído por nova revisão",
  "replacement_document_id": "uuid"
}
```

Evento resultante:

```text
documents.document_marked_obsolete
```

---

## `ArchiveDocumentCommand`

Arquiva documento.

Permissão:

```text
documents.document.archive
```

Payload:

```json
{
  "document_id": "uuid",
  "reason": "Projeto encerrado"
}
```

Validações:

* documentos obrigatórios;
* obrigações legais;
* vínculos ativos;
* não excluir Storage automaticamente.

Evento resultante:

```text
documents.document_archived
```

---

## `RestoreDocumentCommand`

Restaura documento arquivado.

Permissão:

```text
documents.document.restore
```

Payload:

```json
{
  "document_id": "uuid",
  "reason": "Projeto reaberto"
}
```

Evento resultante:

```text
documents.document_restored
```

---

# 29. Comandos de Inventory

## `CreateMaterialCommand`

Cria material.

Permissão:

```text
inventory.material.create
```

Payload:

```json
{
  "code": "MDF-BRANCO-15",
  "name": "MDF Branco TX 15 mm",
  "unit": "CHAPA",
  "category": "MDF",
  "specifications": {
    "thickness_mm": 15,
    "finish": "TX"
  }
}
```

Validações:

* código único;
* unidade válida;
* especificações conforme categoria.

Evento resultante:

```text
inventory.material_created
```

---

## `UpdateMaterialCommand`

Atualiza material.

Permissão:

```text
inventory.material.update
```

Payload:

```json
{
  "material_id": "uuid",
  "name": "MDF Branco TX 15 mm",
  "category": "MDF",
  "specifications": {}
}
```

Validações:

* não alterar unidade com movimentações sem processo específico;
* preservar histórico.

Evento resultante:

```text
inventory.material_updated
```

---

## `ArchiveMaterialCommand`

Arquiva material.

Permissão:

```text
inventory.material.archive
```

Payload:

```json
{
  "material_id": "uuid",
  "reason": "Material descontinuado",
  "replacement_material_id": "uuid"
}
```

Validações:

* saldo;
* reservas;
* pedidos de compra;
* BOM;
* ordens abertas.

Evento resultante:

```text
inventory.material_archived
```

---

## `CreateStockLocationCommand`

Cria localização de estoque.

Permissão:

```text
inventory.stock_location.create
```

Payload:

```json
{
  "branch_id": "uuid",
  "sector_id": "uuid",
  "code": "ALMOX-01",
  "name": "Almoxarifado principal",
  "location_type": "WAREHOUSE"
}
```

Regras:

* filial e setor opcionais;
* código único no escopo;
* empresa pode possuir estoque único.

Evento resultante:

```text
inventory.stock_location_created
```

---

## `UpdateStockLocationCommand`

Atualiza localização.

Permissão:

```text
inventory.stock_location.update
```

Payload:

```json
{
  "stock_location_id": "uuid",
  "name": "Almoxarifado central",
  "branch_id": "uuid",
  "sector_id": "uuid"
}
```

Evento resultante:

```text
inventory.stock_location_updated
```

---

## `ArchiveStockLocationCommand`

Arquiva localização.

Permissão:

```text
inventory.stock_location.archive
```

Payload:

```json
{
  "stock_location_id": "uuid",
  "reason": "Local desativado",
  "transfer_destination_id": "uuid"
}
```

Validações:

* saldo zero ou transferência;
* reservas;
* movimentações pendentes.

Evento resultante:

```text
inventory.stock_location_archived
```

---

## `ReceiveStockCommand`

Registra entrada de estoque.

Permissão:

```text
inventory.stock.receive
```

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "quantity": "10.0000",
  "unit_cost": "150.0000",
  "source_type": "PURCHASE_ORDER",
  "source_id": "uuid",
  "received_at": "datetime",
  "batch_code": "LOTE-001"
}
```

Validações:

* quantidade positiva;
* material ativo;
* localização ativa;
* origem válida;
* idempotência;
* inspeção quando exigida.

Evento resultante:

```text
inventory.stock_received
```

---

## `ReserveStockCommand`

Reserva material.

Permissão:

```text
inventory.stock.reserve
```

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "quantity": "2.0000",
  "expires_at": "datetime"
}
```

Validações:

* disponibilidade;
* quantidade positiva;
* não duplicar reserva;
* origem autorizada;
* concorrência e bloqueio transacional.

Eventos possíveis:

```text
inventory.stock_reserved
inventory.stock_reservation_failed
```

---

## `ReleaseStockReservationCommand`

Libera reserva.

Permissão:

```text
inventory.stock.release
```

Payload:

```json
{
  "reservation_id": "uuid",
  "quantity": "2.0000",
  "reason_code": "PRODUCTION_ORDER_CANCELLED"
}
```

Validações:

* reserva ativa;
* quantidade não superior ao reservado.

Evento resultante:

```text
inventory.stock_released
```

---

## `ConsumeReservedStockCommand`

Consome material reservado.

Permissão:

```text
inventory.stock.consume
```

Payload:

```json
{
  "reservation_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "quantity": "2.0000",
  "consumed_at": "datetime"
}
```

Validações:

* reserva ativa;
* quantidade suficiente;
* operação correspondente;
* idempotência.

Evento resultante:

```text
inventory.material_consumed
```

---

## `ConsumeStockCommand`

Consome material sem reserva prévia quando permitido.

Permissão:

```text
inventory.stock.consume_unreserved
```

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "quantity": "1.0000",
  "reason": "Consumo emergencial"
}
```

Validações:

* política permite;
* saldo suficiente;
* permissão especial;
* justificativa.

Evento resultante:

```text
inventory.material_consumed
```

---

## `TransferStockCommand`

Transfere material entre locais.

Permissão:

```text
inventory.stock.transfer
```

Payload:

```json
{
  "material_id": "uuid",
  "source_stock_location_id": "uuid",
  "target_stock_location_id": "uuid",
  "quantity": "5.0000",
  "reason": "Abastecimento da produção"
}
```

Validações:

* locais diferentes;
* saldo disponível;
* Tenant igual;
* quantidade positiva;
* idempotência.

Evento resultante:

```text
inventory.stock_transferred
```

---

## `AdjustStockCommand`

Realiza ajuste administrativo.

Permissão:

```text
inventory.stock.adjust
```

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "new_quantity": "9.5000",
  "reason_code": "PHYSICAL_COUNT",
  "reason": "Inventário físico",
  "evidence_document_id": "uuid"
}
```

Validações:

* permissão especial;
* justificativa;
* evidência conforme política;
* não alterar movimentações antigas;
* criar movimento de diferença.

Evento resultante:

```text
inventory.stock_adjusted
```

---

## `SetReorderPointCommand`

Define ponto de reposição.

Permissão:

```text
inventory.reorder_point.set
```

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "reorder_point": "3.0000",
  "target_stock": "10.0000"
}
```

Evento resultante:

```text
inventory.reorder_point_changed
```

---

## `CreateStockCountCommand`

Inicia inventário físico.

Permissão:

```text
inventory.stock_count.create
```

Payload:

```json
{
  "stock_location_id": "uuid",
  "count_type": "FULL",
  "scheduled_at": "datetime",
  "material_ids": []
}
```

Evento resultante:

```text
inventory.stock_count_created
```

---

## `SubmitStockCountCommand`

Envia contagem física.

Permissão:

```text
inventory.stock_count.submit
```

Payload:

```json
{
  "stock_count_id": "uuid",
  "items": [
    {
      "material_id": "uuid",
      "counted_quantity": "9.5000"
    }
  ],
  "submitted_at": "datetime"
}
```

Evento resultante:

```text
inventory.stock_count_submitted
```

---

## `ApproveStockCountCommand`

Aprova inventário e gera ajustes.

Permissão:

```text
inventory.stock_count.approve
```

Payload:

```json
{
  "stock_count_id": "uuid",
  "approval_notes": "Contagem conferida"
}
```

Eventos resultantes:

```text
inventory.stock_count_approved
inventory.stock_adjusted
```

---

# 30. Continuação

A próxima parte continuará com:

```text
Purchasing
Quality
Maintenance
Scheduling
Incidents
Notifications
Financial
Fiscal
Configuration
Automation
AI
Synchronization
```

Fim da Parte 2.
# 31. Comandos de Purchasing

## `CreatePurchaseRequestCommand`

Cria uma solicitação de compra.

Permissão:

```text
purchasing.request.create
```

Payload:

```json
{
  "origin_type": "MATERIAL_SHORTAGE",
  "origin_id": "uuid",
  "requested_by_user_id": "uuid",
  "requested_by_employee_id": "uuid",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "priority": "HIGH",
  "required_by_date": "date",
  "justification": "Material necessário para continuidade da produção",
  "items": [
    {
      "material_id": "uuid",
      "description": "MDF Branco TX 15 mm",
      "requested_quantity": "2.0000",
      "unit": "CHAPA",
      "preferred_supplier_id": "uuid",
      "notes": null
    }
  ]
}
```

Validações:

* pelo menos um item;
* quantidades positivas;
* materiais ativos;
* unidade compatível;
* filial e setor pertencentes ao Tenant;
* origem válida quando informada;
* evitar solicitação duplicada para a mesma necessidade;
* data necessária coerente;
* idempotência obrigatória quando originada por evento ou sincronização offline.

Evento resultante:

```text
purchasing.request_created
```

Origens possíveis:

```text
MATERIAL_SHORTAGE
REORDER_POINT
PRODUCTION_REQUEST
MAINTENANCE_REQUEST
QUALITY_REPLACEMENT
MANUAL
```

---

## `UpdatePurchaseRequestCommand`

Atualiza uma solicitação de compra ainda editável.

Permissão:

```text
purchasing.request.update
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "priority": "NORMAL",
  "required_by_date": "date",
  "justification": "Prazo atualizado",
  "branch_id": "uuid",
  "sector_id": "uuid"
}
```

Validações:

* solicitação em rascunho ou pendente;
* não alterar solicitação já convertida integralmente em pedido;
* concorrência otimista;
* não remover rastreabilidade da origem;
* alterações após aprovação podem exigir nova aprovação.

Evento resultante:

```text
purchasing.request_updated
```

---

## `AddPurchaseRequestItemCommand`

Adiciona item a uma solicitação de compra.

Permissão:

```text
purchasing.request.item.create
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "material_id": "uuid",
  "description": "Fita de borda branca",
  "requested_quantity": "100.0000",
  "unit": "M",
  "preferred_supplier_id": "uuid",
  "notes": "Utilizar padrão compatível com o MDF"
}
```

Validações:

* solicitação editável;
* material ativo;
* quantidade positiva;
* unidade compatível;
* impedir duplicidade desnecessária do mesmo material;
* permitir consolidação quando configurada.

Evento resultante:

```text
purchasing.request_item_added
```

---

## `UpdatePurchaseRequestItemCommand`

Atualiza item da solicitação.

Permissão:

```text
purchasing.request.item.update
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "purchase_request_item_id": "uuid",
  "requested_quantity": "120.0000",
  "unit": "M",
  "preferred_supplier_id": "uuid",
  "notes": "Quantidade revisada após conferência"
}
```

Validações:

* item pertencente à solicitação;
* solicitação editável;
* quantidade positiva;
* não reduzir abaixo da quantidade já atendida;
* registrar alteração de quantidade.

Evento resultante:

```text
purchasing.request_item_updated
```

---

## `RemovePurchaseRequestItemCommand`

Remove item ainda não atendido.

Permissão:

```text
purchasing.request.item.remove
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "purchase_request_item_id": "uuid",
  "reason": "Material não será mais necessário"
}
```

Validações:

* item não convertido integralmente em compra;
* solicitação permanece válida;
* justificativa obrigatória;
* preservar histórico da remoção.

Evento resultante:

```text
purchasing.request_item_removed
```

---

## `SubmitPurchaseRequestCommand`

Envia a solicitação para aprovação.

Permissão:

```text
purchasing.request.submit
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "submitted_at": "datetime",
  "submission_notes": "Solicitação urgente para produção"
}
```

Validações:

* solicitação em rascunho;
* itens válidos;
* justificativa preenchida;
* centro de custo quando exigido;
* data necessária válida;
* fluxo de aprovação configurado.

Evento resultante:

```text
purchasing.request_submitted
```

---

## `ApprovePurchaseRequestCommand`

Aprova uma solicitação de compra.

Permissão:

```text
purchasing.request.approve
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Compra autorizada",
  "approved_item_ids": [
    "uuid"
  ]
}
```

Validações:

* solicitação submetida;
* ator dentro da alçada;
* limite financeiro respeitado;
* itens aprovados ainda pendentes;
* não permitir autoaprovação quando proibida;
* aprovação parcial permitida apenas quando configurada.

Evento resultante:

```text
purchasing.request_approved
```

Eventos adicionais possíveis:

```text
purchasing.request_partially_approved
purchasing.request_item_approved
```

---

## `RejectPurchaseRequestCommand`

Rejeita uma solicitação.

Permissão:

```text
purchasing.request.reject
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "reason_code": "BUDGET_UNAVAILABLE",
  "reason": "Compra não prevista no orçamento atual"
}
```

Validações:

* solicitação pendente de aprovação;
* justificativa obrigatória;
* preservar possibilidade de reabertura conforme política.

Evento resultante:

```text
purchasing.request_rejected
```

---

## `ReopenPurchaseRequestCommand`

Reabre uma solicitação rejeitada ou encerrada.

Permissão:

```text
purchasing.request.reopen
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "reason": "Orçamento liberado posteriormente"
}
```

Validações:

* status permite reabertura;
* nenhuma compra conflitante existente;
* itens e quantidades devem ser revalidados;
* nova aprovação poderá ser exigida.

Evento resultante:

```text
purchasing.request_reopened
```

---

## `CancelPurchaseRequestCommand`

Cancela uma solicitação de compra.

Permissão:

```text
purchasing.request.cancel
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "reason_code": "NEED_CANCELLED",
  "reason": "Produção não utilizará mais o material"
}
```

Validações:

* verificar cotações abertas;
* verificar pedidos de compra associados;
* não cancelar silenciosamente itens já comprados;
* emitir compensações quando necessário;
* liberar vínculos de planejamento sem apagar histórico.

Evento resultante:

```text
purchasing.request_cancelled
```

---

## `CreateSupplierQuotationCommand`

Registra uma cotação recebida de fornecedor.

Permissão:

```text
purchasing.supplier_quotation.create
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "supplier_id": "uuid",
  "quotation_number": "COT-4587",
  "quoted_at": "datetime",
  "valid_until": "date",
  "currency": "BRL",
  "freight_amount": "150.00",
  "discount_amount": "0.00",
  "payment_terms": {},
  "delivery_terms": {},
  "items": [
    {
      "purchase_request_item_id": "uuid",
      "material_id": "uuid",
      "quoted_quantity": "2.0000",
      "unit": "CHAPA",
      "unit_price": "450.00",
      "delivery_days": 5,
      "brand": "Fornecedor",
      "notes": null
    }
  ]
}
```

Validações:

* fornecedor ativo;
* solicitação válida;
* itens relacionados à necessidade;
* quantidades e valores válidos;
* moeda suportada;
* prazo de validade coerente;
* impedir duplicidade por fornecedor e número;
* total calculado pelo domínio.

Evento resultante:

```text
purchasing.supplier_quotation_received
```

---

## `UpdateSupplierQuotationCommand`

Atualiza cotação ainda não selecionada.

Permissão:

```text
purchasing.supplier_quotation.update
```

Payload:

```json
{
  "supplier_quotation_id": "uuid",
  "valid_until": "date",
  "freight_amount": "100.00",
  "discount_amount": "50.00",
  "payment_terms": {},
  "delivery_terms": {},
  "items": []
}
```

Validações:

* cotação editável;
* não alterar proposta já escolhida sem reavaliação;
* concorrência otimista;
* recalcular totais;
* registrar revisão.

Evento resultante:

```text
purchasing.supplier_quotation_updated
```

---

## `AttachSupplierQuotationDocumentCommand`

Vincula documento comprobatório à cotação.

Permissão:

```text
purchasing.supplier_quotation.document.attach
```

Payload:

```json
{
  "supplier_quotation_id": "uuid",
  "document_id": "uuid",
  "relationship_type": "SUPPLIER_QUOTATION_EVIDENCE"
}
```

Validações:

* documento acessível;
* cotação e documento pertencentes ao mesmo Tenant;
* vínculo não duplicado.

Evento resultante:

```text
purchasing.supplier_quotation_document_attached
```

---

## `CompareSupplierQuotationsCommand`

Gera uma comparação formal entre cotações.

Permissão:

```text
purchasing.supplier_quotation.compare
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "supplier_quotation_ids": [
    "uuid",
    "uuid",
    "uuid"
  ],
  "criteria": [
    "TOTAL_COST",
    "DELIVERY_TIME",
    "PAYMENT_TERMS",
    "SUPPLIER_SCORE"
  ],
  "weights": {
    "TOTAL_COST": 50,
    "DELIVERY_TIME": 25,
    "PAYMENT_TERMS": 15,
    "SUPPLIER_SCORE": 10
  }
}
```

Validações:

* cotações comparáveis;
* mesma solicitação ou itens compatíveis;
* pesos totalizam 100 quando utilizados;
* critérios válidos;
* comparação não aprova automaticamente a compra.

Evento resultante:

```text
purchasing.supplier_quotations_compared
```

A comparação poderá gerar uma projeção de leitura, sem alterar as cotações originais.

---

## `SelectSupplierQuotationCommand`

Seleciona uma cotação para compra.

Permissão:

```text
purchasing.supplier_quotation.select
```

Payload:

```json
{
  "supplier_quotation_id": "uuid",
  "purchase_request_id": "uuid",
  "selected_item_ids": [
    "uuid"
  ],
  "selection_reason": "Melhor custo total e prazo"
}
```

Validações:

* cotação válida e não expirada;
* fornecedor ativo;
* itens ainda pendentes;
* alçada de seleção;
* comparação obrigatória quando configurada;
* permitir seleção parcial por item;
* registrar justificativa quando não for a menor proposta.

Evento resultante:

```text
purchasing.supplier_quotation_selected
```

---

## `RejectSupplierQuotationCommand`

Marca cotação como não selecionada.

Permissão:

```text
purchasing.supplier_quotation.reject
```

Payload:

```json
{
  "supplier_quotation_id": "uuid",
  "reason_code": "DELIVERY_TIME",
  "reason": "Prazo incompatível com a produção"
}
```

Evento resultante:

```text
purchasing.supplier_quotation_rejected
```

---

## `CreatePurchaseOrderCommand`

Cria pedido de compra.

Permissão:

```text
purchasing.purchase_order.create
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "supplier_quotation_id": "uuid",
  "supplier_id": "uuid",
  "code": "PC-000001",
  "order_date": "date",
  "expected_delivery_date": "date",
  "branch_id": "uuid",
  "stock_location_id": "uuid",
  "cost_center_id": "uuid",
  "currency": "BRL",
  "payment_terms": {},
  "delivery_terms": {},
  "freight_amount": "100.00",
  "discount_amount": "50.00",
  "items": [
    {
      "purchase_request_item_id": "uuid",
      "supplier_quotation_item_id": "uuid",
      "material_id": "uuid",
      "ordered_quantity": "2.0000",
      "unit": "CHAPA",
      "unit_price": "450.00"
    }
  ]
}
```

Validações:

* fornecedor ativo;
* origem aprovada;
* itens ainda pendentes;
* quantidades positivas;
* valores válidos;
* local de entrega válido;
* código único;
* total calculado pelo domínio;
* evitar compra acima da necessidade sem autorização;
* idempotência obrigatória.

Evento resultante:

```text
purchasing.purchase_order_created
```

---

## `UpdatePurchaseOrderCommand`

Atualiza pedido ainda não aprovado ou enviado.

Permissão:

```text
purchasing.purchase_order.update
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "expected_delivery_date": "date",
  "stock_location_id": "uuid",
  "cost_center_id": "uuid",
  "payment_terms": {},
  "delivery_terms": {},
  "freight_amount": "120.00",
  "discount_amount": "50.00",
  "notes": "Entrega diretamente no almoxarifado"
}
```

Validações:

* pedido editável;
* não alterar fornecedor sem processo específico;
* não reduzir abaixo da quantidade recebida;
* alterações após aprovação exigem nova aprovação conforme política;
* concorrência otimista.

Evento resultante:

```text
purchasing.purchase_order_updated
```

---

## `AddPurchaseOrderItemCommand`

Adiciona item ao pedido.

Permissão:

```text
purchasing.purchase_order.item.create
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "purchase_request_item_id": "uuid",
  "material_id": "uuid",
  "ordered_quantity": "50.0000",
  "unit": "UN",
  "unit_price": "8.50",
  "notes": null
}
```

Validações:

* pedido editável;
* material ativo;
* quantidade e preço válidos;
* origem aprovada ou justificativa para item avulso;
* limite de compra respeitado.

Evento resultante:

```text
purchasing.purchase_order_item_added
```

---

## `UpdatePurchaseOrderItemCommand`

Atualiza item do pedido.

Permissão:

```text
purchasing.purchase_order.item.update
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "purchase_order_item_id": "uuid",
  "ordered_quantity": "60.0000",
  "unit_price": "8.20",
  "notes": "Preço renegociado"
}
```

Validações:

* pedido editável;
* quantidade não inferior ao recebido;
* valor válido;
* recalcular total;
* alterações significativas podem exigir nova aprovação.

Evento resultante:

```text
purchasing.purchase_order_item_updated
```

---

## `RemovePurchaseOrderItemCommand`

Remove item ainda não recebido.

Permissão:

```text
purchasing.purchase_order.item.remove
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "purchase_order_item_id": "uuid",
  "reason": "Item comprado em outro pedido"
}
```

Validações:

* nenhuma quantidade recebida;
* pedido permanece válido;
* preservar vínculo com solicitação;
* registrar justificativa.

Evento resultante:

```text
purchasing.purchase_order_item_removed
```

---

## `SubmitPurchaseOrderForApprovalCommand`

Envia o pedido para aprovação.

Permissão:

```text
purchasing.purchase_order.submit
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "submitted_at": "datetime",
  "notes": "Pedido conferido"
}
```

Validações:

* pedido completo;
* fornecedor e itens válidos;
* total calculado;
* centro de custo;
* condições de pagamento;
* alçada aplicável;
* documentos obrigatórios.

Evento resultante:

```text
purchasing.purchase_order_submitted
```

---

## `ApprovePurchaseOrderCommand`

Aprova pedido de compra.

Permissão:

```text
purchasing.purchase_order.approve
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Pedido autorizado"
}
```

Validações:

* pedido submetido;
* ator dentro da alçada;
* não permitir autoaprovação quando proibida;
* orçamento e centro de custo válidos;
* fornecedor não bloqueado;
* condições comerciais válidas.

Evento resultante:

```text
purchasing.purchase_order_approved
```

Reações esperadas:

* permitir envio ao fornecedor;
* gerar previsão financeira;
* atualizar planejamento de material;
* notificar solicitante.

---

## `RejectPurchaseOrderCommand`

Rejeita pedido de compra.

Permissão:

```text
purchasing.purchase_order.reject
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "reason_code": "VALUE_TOO_HIGH",
  "reason": "Necessário renegociar o valor"
}
```

Evento resultante:

```text
purchasing.purchase_order_rejected
```

---

## `SendPurchaseOrderCommand`

Registra envio do pedido ao fornecedor.

Permissão:

```text
purchasing.purchase_order.send
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "delivery_channel": "EMAIL",
  "recipient": "masked",
  "document_id": "uuid",
  "sent_at": "datetime"
}
```

Validações:

* pedido aprovado;
* documento oficial gerado;
* fornecedor com contato válido;
* pedido não cancelado.

Evento resultante:

```text
purchasing.purchase_order_sent
```

---

## `ConfirmPurchaseOrderCommand`

Registra confirmação do fornecedor.

Permissão:

```text
purchasing.purchase_order.confirm
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "supplier_confirmation_number": "CONF-7845",
  "confirmed_at": "datetime",
  "confirmed_delivery_date": "date",
  "notes": "Entrega confirmada"
}
```

Validações:

* pedido enviado;
* prazo coerente;
* confirmação não duplicada.

Evento resultante:

```text
purchasing.purchase_order_confirmed
```

---

## `ReschedulePurchaseOrderDeliveryCommand`

Altera previsão de entrega.

Permissão:

```text
purchasing.purchase_order.reschedule_delivery
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "previous_delivery_date": "date",
  "new_delivery_date": "date",
  "reason_code": "SUPPLIER_DELAY",
  "reason": "Fornecedor informou atraso"
}
```

Validações:

* pedido aberto;
* nova data válida;
* impacto em produção deve ser calculado;
* notificar contextos dependentes.

Evento resultante:

```text
purchasing.purchase_order_delivery_rescheduled
```

Consumidores:

* Production;
* Inventory;
* Scheduling;
* Notifications;
* Analytics.

---

## `ReceivePurchaseOrderCommand`

Registra recebimento total ou parcial.

Permissão:

```text
purchasing.purchase_order.receive
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "receipt_id": "uuid",
  "received_at": "datetime",
  "received_by_employee_id": "uuid",
  "stock_location_id": "uuid",
  "supplier_document_number": "NF-12345",
  "items": [
    {
      "purchase_order_item_id": "uuid",
      "material_id": "uuid",
      "received_quantity": "2.0000",
      "accepted_quantity": "2.0000",
      "rejected_quantity": "0.0000",
      "batch_code": "LOTE-001",
      "expiration_date": null,
      "notes": null
    }
  ]
}
```

Validações:

* pedido aprovado e aberto;
* itens pertencentes ao pedido;
* quantidades não excedem saldo pendente sem tolerância autorizada;
* local de estoque válido;
* recebimento parcial permitido;
* inspeção de qualidade quando exigida;
* idempotência obrigatória;
* documento do fornecedor conforme política.

Eventos resultantes:

```text
purchasing.material_received
inventory.stock_received
```

Eventos adicionais possíveis:

```text
quality.inspection_requested
purchasing.purchase_order_partially_received
purchasing.purchase_order_fully_received
```

---

## `CorrectPurchaseReceiptCommand`

Corrige recebimento registrado incorretamente.

Permissão:

```text
purchasing.receipt.correct
```

Payload:

```json
{
  "receipt_id": "uuid",
  "reason_code": "QUANTITY_ENTRY_ERROR",
  "reason": "Quantidade digitada incorretamente",
  "corrections": [
    {
      "receipt_item_id": "uuid",
      "corrected_received_quantity": "1.0000",
      "corrected_accepted_quantity": "1.0000",
      "corrected_rejected_quantity": "0.0000"
    }
  ]
}
```

Validações:

* permissão administrativa;
* não alterar registro original;
* gerar movimentos compensatórios;
* verificar estoque já consumido;
* auditoria detalhada;
* documentos fiscais relacionados.

Eventos resultantes:

```text
purchasing.receipt_corrected
inventory.stock_adjusted
```

---

## `RejectPurchaseReceiptItemCommand`

Rejeita material recebido.

Permissão:

```text
purchasing.receipt.item.reject
```

Payload:

```json
{
  "receipt_id": "uuid",
  "receipt_item_id": "uuid",
  "rejected_quantity": "1.0000",
  "reason_code": "DAMAGED",
  "reason": "Chapa danificada",
  "quality_inspection_id": "uuid",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* quantidade válida;
* item recebido;
* não rejeitar quantidade já consumida;
* evidência conforme política;
* manter material em localização de quarentena quando aplicável.

Eventos resultantes:

```text
quality.material_rejected
purchasing.receipt_item_rejected
```

---

## `RequestSupplierReplacementCommand`

Solicita substituição de material rejeitado.

Permissão:

```text
purchasing.supplier_replacement.request
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "receipt_item_id": "uuid",
  "supplier_id": "uuid",
  "quantity": "1.0000",
  "reason": "Material recebido com avaria",
  "required_by_date": "date"
}
```

Validações:

* item rejeitado;
* fornecedor correspondente;
* quantidade válida;
* não duplicar solicitação de substituição.

Evento resultante:

```text
purchasing.supplier_replacement_requested
```

---

## `ConfirmSupplierReplacementCommand`

Registra confirmação da reposição.

Permissão:

```text
purchasing.supplier_replacement.confirm
```

Payload:

```json
{
  "replacement_request_id": "uuid",
  "confirmed_quantity": "1.0000",
  "expected_delivery_date": "date",
  "supplier_confirmation_number": "REP-458"
}
```

Evento resultante:

```text
purchasing.supplier_replacement_confirmed
```

---

## `ReturnMaterialToSupplierCommand`

Registra devolução ao fornecedor.

Permissão:

```text
purchasing.material.return
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "receipt_item_id": "uuid",
  "supplier_id": "uuid",
  "returned_quantity": "1.0000",
  "returned_at": "datetime",
  "reason_code": "QUALITY_REJECTION",
  "reason": "Material fora da especificação",
  "fiscal_document_id": "uuid"
}
```

Validações:

* quantidade disponível para devolução;
* material segregado;
* fornecedor correto;
* documentação fiscal quando exigida;
* idempotência.

Eventos resultantes:

```text
purchasing.material_returned
inventory.stock_released
```

---

## `ClosePurchaseOrderCommand`

Encerra pedido atendido.

Permissão:

```text
purchasing.purchase_order.close
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "closed_at": "datetime",
  "closing_notes": "Pedido totalmente recebido e conferido"
}
```

Validações:

* itens atendidos ou cancelados;
* recebimentos concluídos;
* divergências resolvidas;
* qualidade concluída;
* financeiro criado ou reconciliado conforme configuração.

Evento resultante:

```text
purchasing.purchase_order_closed
```

---

## `ClosePurchaseOrderWithBalanceCommand`

Encerra pedido com saldo não recebido.

Permissão:

```text
purchasing.purchase_order.close_with_balance
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "reason_code": "SUPPLIER_UNABLE_TO_DELIVER",
  "reason": "Fornecedor não entregará o saldo restante",
  "create_new_purchase_request": true
}
```

Validações:

* saldo pendente;
* autorização especial;
* impacto em produção;
* nova solicitação quando necessário.

Eventos resultantes:

```text
purchasing.purchase_order_closed_with_balance
```

Evento opcional:

```text
purchasing.request_created
```

---

## `CancelPurchaseOrderCommand`

Cancela pedido de compra.

Permissão:

```text
purchasing.purchase_order.cancel
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "reason_code": "SUPPLIER_FAILURE",
  "reason": "Fornecedor não poderá atender",
  "cancelled_at": "datetime",
  "create_replacement_request": true
}
```

Validações:

* verificar recebimentos;
* impedir cancelamento integral após recebimento sem processo de devolução;
* avaliar financeiro;
* avaliar fiscal;
* avaliar materiais em trânsito;
* notificar produção;
* manter histórico.

Evento resultante:

```text
purchasing.purchase_cancelled
```

Eventos adicionais possíveis:

```text
purchasing.request_created
financial.payable_cancelled
```

---

## `CreateSupplierCommand`

Cria fornecedor operacional.

Permissão:

```text
purchasing.supplier.create
```

Payload:

```json
{
  "code": "FOR-000001",
  "legal_name": "Fornecedor Exemplo Ltda.",
  "trade_name": "Fornecedor Exemplo",
  "tax_id": "string",
  "contact_data": {},
  "address": {},
  "payment_terms": {},
  "categories": [
    "MDF",
    "HARDWARE"
  ]
}
```

Validações:

* código único;
* documento fiscal válido;
* duplicidade por documento;
* dados mínimos de contato;
* Tenant correto.

Evento resultante:

```text
purchasing.supplier_created
```

---

## `UpdateSupplierCommand`

Atualiza fornecedor.

Permissão:

```text
purchasing.supplier.update
```

Payload:

```json
{
  "supplier_id": "uuid",
  "legal_name": "Fornecedor Atualizado Ltda.",
  "trade_name": "Fornecedor Atualizado",
  "contact_data": {},
  "address": {},
  "payment_terms": {},
  "categories": []
}
```

Evento resultante:

```text
purchasing.supplier_updated
```

---

## `BlockSupplierCommand`

Bloqueia fornecedor para novas compras.

Permissão:

```text
purchasing.supplier.block
```

Payload:

```json
{
  "supplier_id": "uuid",
  "reason_code": "QUALITY_ISSUES",
  "reason": "Reincidência de materiais fora da especificação",
  "effective_at": "datetime"
}
```

Validações:

* justificar bloqueio;
* verificar pedidos abertos;
* definir se pedidos existentes permanecem válidos;
* notificar compradores.

Evento resultante:

```text
purchasing.supplier_blocked
```

---

## `UnblockSupplierCommand`

Desbloqueia fornecedor.

Permissão:

```text
purchasing.supplier.unblock
```

Payload:

```json
{
  "supplier_id": "uuid",
  "reason": "Fornecedor apresentou plano corretivo"
}
```

Evento resultante:

```text
purchasing.supplier_unblocked
```

---

## `ArchiveSupplierCommand`

Arquiva fornecedor sem apagar seu histórico.

Permissão:

```text
purchasing.supplier.archive
```

Payload:

```json
{
  "supplier_id": "uuid",
  "reason": "Fornecedor encerrou as atividades",
  "replacement_supplier_id": "uuid"
}
```

Validações:

* pedidos abertos;
* contas a pagar;
* documentos fiscais;
* cotações em andamento;
* histórico preservado.

Evento resultante:

```text
purchasing.supplier_archived
```

---

## `EvaluateSupplierCommand`

Registra avaliação de fornecedor.

Permissão:

```text
purchasing.supplier.evaluate
```

Payload:

```json
{
  "supplier_id": "uuid",
  "purchase_order_id": "uuid",
  "evaluation_period": "2026-08",
  "criteria": {
    "quality": 4,
    "delivery": 3,
    "price": 5,
    "service": 4
  },
  "notes": "Entrega com atraso de dois dias"
}
```

Validações:

* notas dentro da escala;
* pedido relacionado quando exigido;
* impedir avaliação duplicada do mesmo critério e período;
* cálculo da pontuação pelo domínio.

Evento resultante:

```text
purchasing.supplier_evaluated
```

---

## `ConsolidatePurchaseRequestsCommand`

Consolida solicitações compatíveis.

Permissão:

```text
purchasing.request.consolidate
```

Payload:

```json
{
  "purchase_request_ids": [
    "uuid",
    "uuid"
  ],
  "consolidation_strategy": "BY_MATERIAL",
  "target_branch_id": "uuid",
  "notes": "Consolidar compra de MDF"
}
```

Validações:

* solicitações aprovadas;
* itens compatíveis;
* mesma moeda e política de compra;
* filiais compatíveis ou transferência planejada;
* preservar vínculo de cada origem.

Evento resultante:

```text
purchasing.requests_consolidated
```

---

## `SplitPurchaseRequestCommand`

Divide uma solicitação em fluxos separados.

Permissão:

```text
purchasing.request.split
```

Payload:

```json
{
  "purchase_request_id": "uuid",
  "groups": [
    {
      "item_ids": [
        "uuid"
      ],
      "reason": "Fornecedor especializado"
    }
  ]
}
```

Validações:

* todos os itens mapeados;
* não duplicar quantidades;
* preservar origem;
* solicitações derivadas recebem novos identificadores.

Eventos resultantes:

```text
purchasing.request_split
purchasing.request_created
```

---

## `ChangePurchaseOrderSupplierCommand`

Substitui fornecedor antes do recebimento.

Permissão:

```text
purchasing.purchase_order.change_supplier
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "new_supplier_id": "uuid",
  "new_supplier_quotation_id": "uuid",
  "reason_code": "ORIGINAL_SUPPLIER_UNAVAILABLE",
  "reason": "Fornecedor original não poderá atender"
}
```

Validações:

* nenhum recebimento realizado;
* pedido não fiscalizado;
* nova cotação válida;
* reaprovação obrigatória;
* cancelar confirmação anterior;
* recalcular valores e prazos.

Eventos resultantes:

```text
purchasing.purchase_order_supplier_changed
purchasing.purchase_order_approval_revoked
```

---

## `RequestPurchaseOrderApprovalOverrideCommand`

Solicita aprovação excepcional.

Permissão:

```text
purchasing.purchase_order.approval_override.request
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "override_reason_code": "EMERGENCY_PURCHASE",
  "reason": "Produção parada por falta de material",
  "requested_approver_user_id": "uuid"
}
```

Validações:

* motivo excepcional permitido;
* aprovador com alçada;
* não executar aprovação automaticamente;
* auditoria reforçada.

Evento resultante:

```text
purchasing.purchase_order_approval_override_requested
```

---

## `ApprovePurchaseOrderOverrideCommand`

Aprova exceção de compra.

Permissão:

```text
purchasing.purchase_order.approval_override.approve
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "override_request_id": "uuid",
  "approval_notes": "Compra emergencial autorizada"
}
```

Validações:

* solicitação de exceção aberta;
* ator autorizado;
* não permitir autoaprovação;
* registrar todas as regras dispensadas.

Eventos resultantes:

```text
purchasing.purchase_order_override_approved
purchasing.purchase_order_approved
```

---

## `RejectPurchaseOrderOverrideCommand`

Rejeita exceção de compra.

Permissão:

```text
purchasing.purchase_order.approval_override.reject
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "override_request_id": "uuid",
  "reason": "Existe fornecedor alternativo aprovado"
}
```

Evento resultante:

```text
purchasing.purchase_order_override_rejected
```

---

# 32. Integrações de Purchasing

## Eventos consumidos

O contexto Purchasing deverá consumir, inicialmente:

```text
inventory.stock_reservation_failed
inventory.reorder_point_reached
production.material_requested
quality.material_rejected
maintenance.material_requested
```

## Reações previstas

### `inventory.stock_reservation_failed`

Poderá iniciar:

```text
CreatePurchaseRequestCommand
```

desde que:

* a automação esteja habilitada;
* não exista solicitação aberta equivalente;
* o material permita compra automática;
* a necessidade seja superior ao limite configurado.

### `inventory.reorder_point_reached`

Poderá gerar solicitação de reposição com base em:

* estoque atual;
* estoque alvo;
* consumo médio;
* pedidos já abertos;
* prazo médio do fornecedor.

### `production.material_requested`

Deverá consultar primeiro o Inventory.

Purchasing somente deverá assumir a necessidade quando o estoque confirmar indisponibilidade total ou parcial.

### `quality.material_rejected`

Poderá gerar:

* substituição pelo fornecedor;
* nova solicitação de compra;
* devolução;
* bloqueio ou reavaliação do fornecedor.

---

# 33. Regras de integridade de Purchasing

## 33.1 Solicitação não é pedido

`PurchaseRequest` representa necessidade.

`PurchaseOrder` representa compromisso de compra.

Uma solicitação poderá resultar em:

* nenhum pedido;
* um pedido;
* vários pedidos;
* compra parcial;
* consolidação com outras solicitações.

---

## 33.2 Cotação não altera estoque

Uma cotação de fornecedor não gera entrada, reserva ou previsão física por si mesma.

---

## 33.3 Recebimento não deve alterar registros antigos

Correções de recebimento devem gerar:

* registros compensatórios;
* novos movimentos;
* auditoria;
* eventos adicionais.

---

## 33.4 Compra parcial

Cada item deverá controlar:

```text
requested_quantity
approved_quantity
ordered_quantity
received_quantity
accepted_quantity
rejected_quantity
cancelled_quantity
outstanding_quantity
```

Esses valores não deverão ser derivados apenas de um status genérico.

---

## 33.5 Tolerância de recebimento

A empresa poderá configurar tolerância para:

* quantidade superior;
* quantidade inferior;
* diferença de preço;
* prazo;
* unidade alternativa.

Ultrapassar a tolerância deverá exigir autorização explícita.

---

## 33.6 Alçadas de aprovação

A aprovação poderá considerar:

* valor total;
* categoria de material;
* centro de custo;
* filial;
* urgência;
* fornecedor;
* compra emergencial;
* orçamento disponível.

---

## 33.7 Segregação de funções

Quando configurado, o mesmo usuário não poderá:

* solicitar;
* aprovar;
* comprar;
* receber;
* ajustar;
* pagar;

a mesma operação sem controles adicionais.

---

## 33.8 Fornecedor bloqueado

Fornecedor bloqueado não poderá receber novos pedidos, salvo:

* exceção autorizada;
* justificativa;
* aprovação especial;
* auditoria reforçada.

---

## 33.9 Documentos

Os seguintes documentos poderão ser exigidos:

* cotação do fornecedor;
* comparação de propostas;
* pedido oficial;
* comprovante de envio;
* confirmação;
* nota fiscal;
* comprovante de recebimento;
* evidência de avaria;
* documento de devolução.

---

## 33.10 Offline

Comandos de recebimento enviados offline deverão possuir:

```text
command_id
idempotency_key
device_id
client_sequence
occurred_at
purchase_order_id
receipt_id
expected_entity_version
```

O servidor deverá impedir recebimentos duplicados.

---

# 34. Eventos resultantes de Purchasing

Eventos principais:

```text
purchasing.request_created
purchasing.request_updated
purchasing.request_submitted
purchasing.request_approved
purchasing.request_rejected
purchasing.request_cancelled
purchasing.supplier_quotation_received
purchasing.supplier_quotation_selected
purchasing.purchase_order_created
purchasing.purchase_order_submitted
purchasing.purchase_order_approved
purchasing.purchase_order_rejected
purchasing.purchase_order_sent
purchasing.purchase_order_confirmed
purchasing.purchase_order_delivery_rescheduled
purchasing.material_received
purchasing.receipt_item_rejected
purchasing.material_returned
purchasing.purchase_order_closed
purchasing.purchase_cancelled
purchasing.supplier_created
purchasing.supplier_updated
purchasing.supplier_blocked
purchasing.supplier_evaluated
```

Consumidores principais:

* Inventory;
* Production;
* Financial;
* Fiscal;
* Quality;
* Notifications;
* Timeline;
* Analytics;
* Automation.

---

# 35. Continuação

A próxima subparte continuará com:

```text
Quality
```

Fim da Parte 3A.
# 36. Comandos de Quality

## `CreateQualityInspectionCommand`

Cria uma inspeção de qualidade.

Permissão:

```text
quality.inspection.create
```

Payload:

```json
{
  "inspection_type": "OPERATION_OUTPUT",
  "reference_type": "OPERATION_EXECUTION",
  "reference_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_id": "uuid",
  "material_id": null,
  "purchase_receipt_id": null,
  "inspection_plan_id": "uuid",
  "assigned_inspector_employee_id": "uuid",
  "priority": "NORMAL",
  "required_by_at": "datetime",
  "notes": "Conferir medidas e acabamento"
}
```

Tipos iniciais:

```text
INCOMING_MATERIAL
PROCESS
OPERATION_OUTPUT
FINAL_PRODUCT
DELIVERY
MAINTENANCE_RELEASE
CUSTOM
```

Validações:

* referência existente e pertencente ao Tenant;
* plano de inspeção publicado quando informado;
* inspetor ativo;
* tipo coerente com a origem;
* impedir duplicidade de inspeção obrigatória aberta;
* data de necessidade válida;
* permissão e escopo do ator.

Evento resultante:

```text
quality.inspection_requested
```

---

## `AssignQualityInspectorCommand`

Atribui responsável pela inspeção.

Permissão:

```text
quality.inspection.assign
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspector_employee_id": "uuid",
  "assigned_at": "datetime",
  "notes": null
}
```

Validações:

* inspeção aberta;
* funcionário ativo;
* habilidade ou perfil compatível quando exigido;
* mesmo Tenant;
* impedir duplicidade de atribuição ativa.

Evento resultante:

```text
quality.inspection_assigned
```

---

## `UnassignQualityInspectorCommand`

Remove a atribuição do inspetor.

Permissão:

```text
quality.inspection.unassign
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspector_employee_id": "uuid",
  "reason": "Reorganização da equipe"
}
```

Validações:

* inspeção não concluída;
* não remover durante execução ativa sem procedimento;
* manter responsável quando obrigatório.

Evento resultante:

```text
quality.inspection_unassigned
```

---

## `StartQualityInspectionCommand`

Inicia a execução de uma inspeção.

Permissão:

```text
quality.inspection.start
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspector_employee_id": "uuid",
  "started_at": "datetime",
  "device_id": "uuid"
}
```

Validações:

* inspeção pendente ou atribuída;
* inspetor autorizado;
* referência ainda válida;
* nenhuma execução incompatível;
* idempotência obrigatória em PWA;
* checklist inicial quando exigido.

Evento resultante:

```text
quality.inspection_started
```

---

## `RecordInspectionMeasurementCommand`

Registra uma medição da inspeção.

Permissão:

```text
quality.inspection.measurement.record
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspection_item_id": "uuid",
  "measurement_code": "WIDTH_MM",
  "measured_value": "598.50",
  "unit": "MM",
  "lower_tolerance": "597.00",
  "upper_tolerance": "599.00",
  "measured_at": "datetime",
  "instrument_id": "uuid",
  "notes": null
}
```

Validações:

* inspeção ativa;
* item pertencente ao plano;
* unidade compatível;
* instrumento válido quando exigido;
* valor numérico válido;
* tolerâncias provenientes do plano ou autorizadas;
* não sobrescrever medição anterior sem histórico.

Eventos possíveis:

```text
quality.inspection_measurement_recorded
quality.inspection_measurement_out_of_tolerance
```

---

## `RecordInspectionChecklistCommand`

Registra respostas de um checklist de inspeção.

Permissão:

```text
quality.inspection.checklist.record
```

Payload:

```json
{
  "inspection_id": "uuid",
  "form_submission_id": "uuid",
  "completed_at": "datetime"
}
```

Validações:

* formulário compatível;
* versão publicada;
* submissão concluída;
* vínculo com a inspeção;
* não utilizar formulário de outro Tenant.

Evento resultante:

```text
quality.inspection_checklist_recorded
```

---

## `AttachInspectionEvidenceCommand`

Vincula evidência à inspeção.

Permissão:

```text
quality.inspection.evidence.attach
```

Payload:

```json
{
  "inspection_id": "uuid",
  "document_id": "uuid",
  "evidence_type": "PHOTO",
  "description": "Foto da borda danificada"
}
```

Tipos iniciais:

```text
PHOTO
VIDEO_REFERENCE
REPORT
CERTIFICATE
MEASUREMENT_FILE
SUPPLIER_DOCUMENT
OTHER
```

Validações:

* documento acessível;
* mesmo Tenant;
* inspeção não arquivada;
* vínculo não duplicado;
* tipo permitido.

Evento resultante:

```text
quality.inspection_evidence_attached
```

---

## `RemoveInspectionEvidenceCommand`

Remove vínculo de evidência incorreta.

Permissão:

```text
quality.inspection.evidence.remove
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspection_evidence_id": "uuid",
  "reason": "Documento vinculado incorretamente"
}
```

Validações:

* não apagar o documento físico;
* preservar auditoria;
* evidência não obrigatória ou substituída;
* inspeção ainda alterável ou permissão administrativa.

Evento resultante:

```text
quality.inspection_evidence_removed
```

---

## `ApproveQualityInspectionCommand`

Conclui a inspeção com resultado aprovado.

Permissão:

```text
quality.inspection.approve
```

Payload:

```json
{
  "inspection_id": "uuid",
  "completed_at": "datetime",
  "result": "APPROVED",
  "approval_notes": "Peças dentro das tolerâncias",
  "approved_quantity": "10.0000",
  "rejected_quantity": "0.0000"
}
```

Validações:

* inspeção ativa;
* itens obrigatórios verificados;
* medições obrigatórias registradas;
* nenhuma medição bloqueante fora da tolerância;
* formulários obrigatórios concluídos;
* evidências obrigatórias anexadas;
* quantidades coerentes;
* inspetor autorizado;
* nenhuma não conformidade bloqueante aberta.

Evento resultante:

```text
quality.inspection_completed
```

Payload do evento deverá indicar:

```text
result = APPROVED
```

---

## `ConditionallyApproveInspectionCommand`

Aprova com ressalvas.

Permissão:

```text
quality.inspection.conditionally_approve
```

Payload:

```json
{
  "inspection_id": "uuid",
  "completed_at": "datetime",
  "conditions": [
    {
      "code": "MINOR_FINISH_ADJUSTMENT",
      "description": "Realizar pequeno ajuste antes da entrega"
    }
  ],
  "responsible_employee_id": "uuid",
  "due_at": "datetime",
  "approval_notes": "Liberado com correção obrigatória"
}
```

Validações:

* política permite aprovação condicional;
* desvio não classificado como crítico;
* condição possui responsável e prazo;
* não utilizar para ocultar não conformidade;
* aprovação por ator com alçada.

Eventos resultantes:

```text
quality.inspection_conditionally_approved
quality.corrective_action_created
```

---

## `RejectQualityInspectionCommand`

Conclui a inspeção com rejeição.

Permissão:

```text
quality.inspection.reject
```

Payload:

```json
{
  "inspection_id": "uuid",
  "completed_at": "datetime",
  "result": "REJECTED",
  "reason_code": "DIMENSION_OUT_OF_TOLERANCE",
  "reason": "Peça fora da medida especificada",
  "approved_quantity": "8.0000",
  "rejected_quantity": "2.0000",
  "create_nonconformity": true
}
```

Validações:

* inspeção ativa;
* motivo obrigatório;
* quantidades coerentes;
* evidência quando exigida;
* não conformidade obrigatória conforme severidade;
* bloquear liberação quando configurado.

Eventos resultantes:

```text
quality.inspection_completed
quality.nonconformity_created
```

Payload da inspeção deverá indicar:

```text
result = REJECTED
```

---

## `CancelQualityInspectionCommand`

Cancela uma inspeção criada indevidamente ou tornada desnecessária.

Permissão:

```text
quality.inspection.cancel
```

Payload:

```json
{
  "inspection_id": "uuid",
  "reason_code": "REFERENCE_CANCELLED",
  "reason": "Operação de origem foi cancelada"
}
```

Validações:

* inspeção não concluída;
* não ocultar medições já registradas;
* preservar histórico;
* não cancelar inspeção obrigatória sem substituição ou autorização.

Evento resultante:

```text
quality.inspection_cancelled
```

---

## `ReopenQualityInspectionCommand`

Reabre inspeção concluída.

Permissão:

```text
quality.inspection.reopen
```

Payload:

```json
{
  "inspection_id": "uuid",
  "reason_code": "NEW_EVIDENCE",
  "reason": "Foi identificada nova evidência após a conclusão"
}
```

Validações:

* permissão administrativa;
* preservar resultado anterior;
* criar nova revisão ou ciclo de inspeção;
* auditoria detalhada;
* impactos em produção e estoque avaliados.

Evento resultante:

```text
quality.inspection_reopened
```

---

# 37. Planos de inspeção

## `CreateInspectionPlanCommand`

Cria um plano de inspeção.

Permissão:

```text
quality.inspection_plan.create
```

Payload:

```json
{
  "code": "FINAL_FURNITURE_INSPECTION",
  "name": "Inspeção final do móvel",
  "category": "FINAL_PRODUCT",
  "description": "Verificações obrigatórias antes da entrega",
  "applicable_reference_types": [
    "PRODUCTION_ORDER"
  ]
}
```

Evento resultante:

```text
quality.inspection_plan_created
```

---

## `CreateInspectionPlanVersionCommand`

Cria uma versão editável do plano.

Permissão:

```text
quality.inspection_plan.version.create
```

Payload:

```json
{
  "inspection_plan_id": "uuid",
  "based_on_version_id": "uuid",
  "change_reason": "Inclusão de conferência de ferragens"
}
```

Evento resultante:

```text
quality.inspection_plan_version_created
```

---

## `AddInspectionPlanItemCommand`

Adiciona item ao plano.

Permissão:

```text
quality.inspection_plan.item.create
```

Payload:

```json
{
  "inspection_plan_version_id": "uuid",
  "code": "CHECK_DOOR_ALIGNMENT",
  "name": "Alinhamento das portas",
  "item_type": "BOOLEAN",
  "order_index": 1,
  "is_required": true,
  "acceptance_criteria": {
    "expected_value": true
  }
}
```

Tipos iniciais:

```text
BOOLEAN
NUMERIC
TEXT
SELECTION
PHOTO
DOCUMENT
SIGNATURE
MEASUREMENT
```

Validações:

* versão em rascunho;
* código único;
* critério compatível com o tipo;
* ordem válida;
* regra de obrigatoriedade coerente.

Evento resultante:

```text
quality.inspection_plan_item_added
```

---

## `UpdateInspectionPlanItemCommand`

Atualiza item do plano.

Permissão:

```text
quality.inspection_plan.item.update
```

Payload:

```json
{
  "inspection_plan_item_id": "uuid",
  "name": "Conferir alinhamento das portas",
  "order_index": 2,
  "is_required": true,
  "acceptance_criteria": {
    "expected_value": true
  }
}
```

Evento resultante:

```text
quality.inspection_plan_item_updated
```

---

## `RemoveInspectionPlanItemCommand`

Remove item de versão em rascunho.

Permissão:

```text
quality.inspection_plan.item.remove
```

Payload:

```json
{
  "inspection_plan_item_id": "uuid",
  "reason": "Verificação consolidada em outro item"
}
```

Validações:

* versão não publicada;
* plano permanece válido;
* referências condicionais atualizadas.

Evento resultante:

```text
quality.inspection_plan_item_removed
```

---

## `PublishInspectionPlanVersionCommand`

Publica a versão do plano.

Permissão:

```text
quality.inspection_plan.version.publish
```

Payload:

```json
{
  "inspection_plan_version_id": "uuid",
  "publication_notes": "Plano validado pela gestão"
}
```

Validações:

* pelo menos um item;
* códigos únicos;
* critérios válidos;
* regras sem referências quebradas;
* versão passa a ser imutável.

Evento resultante:

```text
quality.inspection_plan_version_published
```

---

## `DeprecateInspectionPlanVersionCommand`

Marca versão como obsoleta para novas inspeções.

Permissão:

```text
quality.inspection_plan.version.deprecate
```

Payload:

```json
{
  "inspection_plan_version_id": "uuid",
  "replacement_version_id": "uuid",
  "reason": "Nova versão publicada"
}
```

Evento resultante:

```text
quality.inspection_plan_version_deprecated
```

---

## `BindInspectionPlanCommand`

Vincula plano a uma origem.

Permissão:

```text
quality.inspection_plan.bind
```

Payload:

```json
{
  "inspection_plan_id": "uuid",
  "binding_type": "OPERATION_DEFINITION",
  "workflow_definition_id": "uuid",
  "stage_definition_id": "uuid",
  "operation_definition_id": "uuid",
  "material_category": null,
  "is_mandatory": true,
  "trigger": "AFTER_EXECUTION_FINISH"
}
```

Validações:

* plano publicado;
* alvo válido;
* vínculo não duplicado;
* trigger compatível;
* mesmo Tenant.

Evento resultante:

```text
quality.inspection_plan_bound
```

---

## `UnbindInspectionPlanCommand`

Remove o vínculo para novas operações.

Permissão:

```text
quality.inspection_plan.unbind
```

Payload:

```json
{
  "inspection_plan_binding_id": "uuid",
  "reason": "Plano substituído"
}
```

Evento resultante:

```text
quality.inspection_plan_unbound
```

---

# 38. Não conformidades

## `CreateNonConformityCommand`

Registra uma não conformidade.

Permissão:

```text
quality.nonconformity.create
```

Payload:

```json
{
  "source_type": "QUALITY_INSPECTION",
  "source_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_id": "uuid",
  "material_id": null,
  "supplier_id": null,
  "machine_id": null,
  "category": "DIMENSION",
  "severity": "HIGH",
  "title": "Peça fora da medida",
  "description": "Largura medida abaixo da tolerância",
  "detected_at": "datetime",
  "detected_by_employee_id": "uuid",
  "affected_quantity": "2.0000",
  "immediate_action": "Segregar peças"
}
```

Categorias iniciais:

```text
DIMENSION
MATERIAL
FINISH
ASSEMBLY
DESIGN
DOCUMENTATION
PROCESS
MACHINE
SUPPLIER
SAFETY
DELIVERY
OTHER
```

Severidades:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Validações:

* origem válida;
* descrição e categoria;
* severidade;
* quantidade afetada válida;
* referências pertencentes ao mesmo Tenant;
* evidência conforme política;
* impedir duplicidade evidente sem justificativa.

Evento resultante:

```text
quality.nonconformity_created
```

---

## `ClassifyNonConformityCommand`

Atualiza a classificação técnica.

Permissão:

```text
quality.nonconformity.classify
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "category": "MANUFACTURING_PROCESS",
  "severity": "HIGH",
  "probability": "MEDIUM",
  "impact": "HIGH",
  "classification_notes": "Erro recorrente na regulagem da máquina"
}
```

Validações:

* não conformidade aberta;
* valores de classificação válidos;
* mudança de severidade crítica exige notificação;
* preservar classificação anterior.

Evento resultante:

```text
quality.nonconformity_classified
```

---

## `AssignNonConformityCommand`

Atribui responsável pela análise e tratamento.

Permissão:

```text
quality.nonconformity.assign
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "assigned_user_id": "uuid",
  "assigned_employee_id": "uuid",
  "assigned_sector_id": "uuid",
  "due_at": "datetime"
}
```

Validações:

* não conformidade aberta;
* responsável ativo;
* prazo coerente;
* escopo adequado.

Evento resultante:

```text
quality.nonconformity_assigned
```

---

## `ContainNonConformityCommand`

Registra ação imediata de contenção.

Permissão:

```text
quality.nonconformity.contain
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "containment_action": "Segregar todas as peças do lote",
  "contained_quantity": "10.0000",
  "stock_location_id": "uuid",
  "performed_by_employee_id": "uuid",
  "performed_at": "datetime",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* quantidade válida;
* material ou produto identificável;
* local de quarentena quando aplicável;
* evidência conforme severidade;
* não reduzir rastreabilidade.

Eventos resultantes:

```text
quality.nonconformity_contained
inventory.stock_quarantined
```

O segundo evento será produzido pelo contexto Inventory após comando próprio.

---

## `RecordNonConformityCauseCommand`

Registra causa identificada.

Permissão:

```text
quality.nonconformity.cause.record
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "cause_type": "ROOT_CAUSE",
  "method": "FIVE_WHYS",
  "description": "Regulagem incorreta da serra após manutenção",
  "is_confirmed": true,
  "analysis_document_id": "uuid"
}
```

Tipos:

```text
IMMEDIATE_CAUSE
CONTRIBUTING_CAUSE
ROOT_CAUSE
```

Validações:

* não conformidade em análise;
* método válido;
* causa não vazia;
* confirmação técnica quando exigida.

Evento resultante:

```text
quality.nonconformity_cause_recorded
```

---

## `RequestReworkFromNonConformityCommand`

Solicita retrabalho a partir da não conformidade.

Permissão:

```text
quality.nonconformity.rework.request
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "original_operation_instance_id": "uuid",
  "affected_quantity": "2.0000",
  "reason": "Refazer peças fora da medida",
  "priority": "HIGH",
  "assigned_sector_id": "uuid",
  "estimated_minutes": 90
}
```

Validações:

* não conformidade aberta;
* origem produtiva válida;
* quantidade afetada;
* não duplicar retrabalho ativo;
* preservar operação original.

Eventos resultantes:

```text
quality.rework_required
production.rework_requested
```

O comando de criação efetiva do retrabalho deverá ser executado pelo contexto Production.

---

## `ApproveConcessionCommand`

Autoriza uso de item fora da especificação mediante concessão.

Permissão:

```text
quality.concession.approve
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "approved_quantity": "1.0000",
  "concession_reason": "Desvio sem impacto funcional ou visual",
  "approved_by_user_id": "uuid",
  "expires_at": null,
  "customer_approval_document_id": "uuid"
}
```

Validações:

* política permite concessão;
* severidade não crítica;
* impacto avaliado;
* alçada do aprovador;
* aprovação do cliente quando exigida;
* quantidade não superior à afetada.

Evento resultante:

```text
quality.concession_approved
```

---

## `RejectConcessionCommand`

Rejeita pedido de concessão.

Permissão:

```text
quality.concession.reject
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "reason": "Desvio pode comprometer a durabilidade"
}
```

Evento resultante:

```text
quality.concession_rejected
```

---

## `ScrapNonConformingItemCommand`

Classifica item como perda ou sucata.

Permissão:

```text
quality.nonconforming_item.scrap
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "material_id": "uuid",
  "production_order_id": "uuid",
  "quantity": "2.0000",
  "unit": "UN",
  "reason": "Peças sem possibilidade de reaproveitamento",
  "scrap_stock_location_id": "uuid"
}
```

Validações:

* quantidade válida;
* autorização conforme custo;
* material identificado;
* movimento de estoque obrigatório;
* custo de perda preservado.

Eventos resultantes:

```text
quality.nonconforming_item_scrapped
inventory.material_scrapped
```

O movimento físico será realizado pelo Inventory.

---

## `CloseNonConformityCommand`

Encerra uma não conformidade.

Permissão:

```text
quality.nonconformity.close
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "resolution_code": "REWORK_COMPLETED",
  "resolution_summary": "Peças refeitas e aprovadas",
  "closed_at": "datetime",
  "verification_inspection_id": "uuid"
}
```

Validações:

* contenção concluída;
* causa registrada quando exigida;
* ações corretivas obrigatórias concluídas;
* retrabalho ou descarte finalizado;
* inspeção de verificação aprovada;
* nenhuma pendência bloqueante.

Evento resultante:

```text
quality.nonconformity_closed
```

---

## `ReopenNonConformityCommand`

Reabre uma não conformidade encerrada.

Permissão:

```text
quality.nonconformity.reopen
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "reason": "Problema voltou a ocorrer após o encerramento"
}
```

Validações:

* permissão administrativa;
* preservar encerramento anterior;
* registrar reincidência;
* recalcular severidade quando necessário.

Evento resultante:

```text
quality.nonconformity_reopened
```

---

## `CancelNonConformityCommand`

Cancela registro criado indevidamente.

Permissão:

```text
quality.nonconformity.cancel
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "reason_code": "DUPLICATE_RECORD",
  "reason": "Registro duplicado",
  "replacement_nonconformity_id": "uuid"
}
```

Validações:

* não conformidade sem efeitos irreversíveis;
* indicar registro substituto quando duplicada;
* não apagar histórico;
* auditoria obrigatória.

Evento resultante:

```text
quality.nonconformity_cancelled
```

---

# 39. Ações corretivas e preventivas

## `CreateCorrectiveActionCommand`

Cria ação corretiva.

Permissão:

```text
quality.corrective_action.create
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "title": "Padronizar regulagem da serra",
  "description": "Criar checklist de regulagem antes do início do corte",
  "action_type": "CORRECTIVE",
  "responsible_user_id": "uuid",
  "responsible_employee_id": "uuid",
  "responsible_sector_id": "uuid",
  "due_at": "datetime",
  "verification_method": "PROCESS_AUDIT"
}
```

Evento resultante:

```text
quality.corrective_action_created
```

---

## `CreatePreventiveActionCommand`

Cria ação preventiva sem não conformidade obrigatória.

Permissão:

```text
quality.preventive_action.create
```

Payload:

```json
{
  "risk_reference_type": "PROCESS",
  "risk_reference_id": "uuid",
  "title": "Revisar plano de manutenção preventiva",
  "description": "Evitar perda de regulagem da máquina",
  "responsible_user_id": "uuid",
  "due_at": "datetime"
}
```

Evento resultante:

```text
quality.preventive_action_created
```

---

## `UpdateQualityActionCommand`

Atualiza ação aberta.

Permissão:

```text
quality.action.update
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "title": "Checklist de regulagem e liberação",
  "description": "Descrição revisada",
  "responsible_user_id": "uuid",
  "responsible_employee_id": "uuid",
  "due_at": "datetime",
  "priority": "HIGH"
}
```

Validações:

* ação não concluída;
* responsável ativo;
* prazo válido;
* concorrência otimista.

Evento resultante:

```text
quality.action_updated
```

---

## `StartQualityActionCommand`

Inicia ação corretiva ou preventiva.

Permissão:

```text
quality.action.start
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "started_at": "datetime"
}
```

Evento resultante:

```text
quality.action_started
```

---

## `CompleteQualityActionCommand`

Conclui ação.

Permissão:

```text
quality.action.complete
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "completed_at": "datetime",
  "completion_summary": "Checklist implantado e equipe treinada",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* ação iniciada;
* evidências quando exigidas;
* campos obrigatórios;
* não marcar como eficaz automaticamente.

Evento resultante:

```text
quality.corrective_action_completed
```

ou:

```text
quality.preventive_action_completed
```

---

## `VerifyQualityActionEffectivenessCommand`

Avalia a eficácia da ação.

Permissão:

```text
quality.action.verify_effectiveness
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "verification_result": "EFFECTIVE",
  "verified_at": "datetime",
  "verified_by_employee_id": "uuid",
  "verification_notes": "Não houve reincidência em 30 dias",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Resultados:

```text
EFFECTIVE
PARTIALLY_EFFECTIVE
INEFFECTIVE
INCONCLUSIVE
```

Validações:

* ação concluída;
* período mínimo quando configurado;
* verificador autorizado;
* evidência suficiente.

Eventos possíveis:

```text
quality.action_effectiveness_verified
quality.action_rework_required
```

---

## `CancelQualityActionCommand`

Cancela ação criada indevidamente ou substituída.

Permissão:

```text
quality.action.cancel
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "reason": "Ação consolidada em plano mais abrangente",
  "replacement_action_id": "uuid"
}
```

Evento resultante:

```text
quality.action_cancelled
```

---

# 40. Controle de materiais não conformes

## `QuarantineMaterialCommand`

Solicita segregação de material.

Permissão:

```text
quality.material.quarantine
```

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "quantity": "5.0000",
  "batch_code": "LOTE-001",
  "nonconformity_id": "uuid",
  "reason": "Aguardando análise de qualidade",
  "quarantine_location_id": "uuid"
}
```

Validações:

* saldo disponível;
* quantidade válida;
* localização de quarentena;
* não conformidade ativa;
* idempotência.

Eventos resultantes:

```text
quality.material_quarantine_requested
inventory.stock_quarantined
```

---

## `ReleaseQuarantinedMaterialCommand`

Libera material aprovado.

Permissão:

```text
quality.material.release
```

Payload:

```json
{
  "material_id": "uuid",
  "quarantine_record_id": "uuid",
  "quantity": "5.0000",
  "inspection_id": "uuid",
  "released_at": "datetime",
  "target_stock_location_id": "uuid"
}
```

Validações:

* inspeção aprovada;
* quantidade em quarentena;
* autorização do inspetor;
* destino válido.

Eventos resultantes:

```text
quality.material_released
inventory.quarantined_stock_released
```

---

## `RejectIncomingMaterialCommand`

Rejeita material recebido.

Permissão:

```text
quality.incoming_material.reject
```

Payload:

```json
{
  "inspection_id": "uuid",
  "purchase_order_id": "uuid",
  "receipt_id": "uuid",
  "receipt_item_id": "uuid",
  "material_id": "uuid",
  "rejected_quantity": "2.0000",
  "reason_code": "DAMAGED",
  "reason": "Chapas danificadas no transporte",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* inspeção de recebimento;
* quantidade válida;
* não consumir material rejeitado;
* evidência;
* fornecedor e lote identificados.

Eventos resultantes:

```text
quality.material_rejected
purchasing.receipt_item_rejected
```

---

## `AcceptIncomingMaterialWithDeviationCommand`

Aceita material com desvio autorizado.

Permissão:

```text
quality.incoming_material.accept_with_deviation
```

Payload:

```json
{
  "inspection_id": "uuid",
  "receipt_item_id": "uuid",
  "accepted_quantity": "2.0000",
  "deviation_description": "Variação de tonalidade sem impacto no projeto",
  "approved_by_user_id": "uuid",
  "supplier_credit_required": false
}
```

Validações:

* política permite;
* desvio não crítico;
* alçada;
* rastreabilidade do lote;
* concessão registrada.

Eventos resultantes:

```text
quality.incoming_material_accepted_with_deviation
quality.concession_approved
```

---

# 41. Auditorias de qualidade

## `CreateQualityAuditCommand`

Cria auditoria interna ou externa.

Permissão:

```text
quality.audit.create
```

Payload:

```json
{
  "audit_type": "INTERNAL_PROCESS",
  "code": "AUD-2026-001",
  "title": "Auditoria do processo de corte",
  "scope": "Setor de corte",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "planned_start_at": "datetime",
  "planned_end_at": "datetime",
  "lead_auditor_employee_id": "uuid",
  "audit_team_employee_ids": [
    "uuid"
  ],
  "criteria": [
    "PROCEDURE_COMPLIANCE",
    "RECORDS",
    "EQUIPMENT_CONDITION"
  ]
}
```

Evento resultante:

```text
quality.audit_created
```

---

## `StartQualityAuditCommand`

Inicia auditoria.

Permissão:

```text
quality.audit.start
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "started_at": "datetime"
}
```

Evento resultante:

```text
quality.audit_started
```

---

## `RecordQualityAuditFindingCommand`

Registra constatação.

Permissão:

```text
quality.audit.finding.record
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "finding_type": "NONCONFORMITY",
  "severity": "MEDIUM",
  "title": "Checklist não preenchido",
  "description": "Foram encontradas operações sem checklist final",
  "reference_type": "OPERATION",
  "reference_id": "uuid",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Tipos:

```text
CONFORMITY
OBSERVATION
OPPORTUNITY_FOR_IMPROVEMENT
NONCONFORMITY
CRITICAL_NONCONFORMITY
```

Eventos possíveis:

```text
quality.audit_finding_recorded
quality.nonconformity_created
```

---

## `CompleteQualityAuditCommand`

Conclui auditoria.

Permissão:

```text
quality.audit.complete
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "completed_at": "datetime",
  "summary": "Auditoria concluída com duas não conformidades",
  "overall_result": "PARTIALLY_COMPLIANT",
  "report_document_id": "uuid"
}
```

Validações:

* auditoria iniciada;
* achados classificados;
* relatório quando exigido;
* responsáveis definidos para pendências.

Evento resultante:

```text
quality.audit_completed
```

---

## `CancelQualityAuditCommand`

Cancela auditoria planejada.

Permissão:

```text
quality.audit.cancel
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "reason": "Unidade indisponível na data prevista"
}
```

Evento resultante:

```text
quality.audit_cancelled
```

---

# 42. Integrações de Quality

## Eventos consumidos

Quality deverá consumir inicialmente:

```text
production.execution_finished
production.rework_requested
purchasing.material_received
maintenance.machine_released
forms.submission_completed
incident.created
```

---

## Reação a `production.execution_finished`

Quando a operação exigir inspeção:

```text
CreateQualityInspectionCommand
```

A conclusão da operação poderá permanecer:

* pendente de qualidade;
* aprovada;
* rejeitada;
* aprovada condicionalmente.

---

## Reação a `purchasing.material_received`

Quando o material exigir inspeção de recebimento:

```text
CreateQualityInspectionCommand
```

O material deverá permanecer:

```text
PENDING_INSPECTION
```

ou em quarentena até o resultado.

---

## Reação a `maintenance.machine_released`

Poderá criar inspeção de liberação da máquina quando:

* manutenção afetar precisão;
* houver troca de componente crítico;
* calibração for necessária;
* a política de qualidade exigir.

---

## Reação a `incident.created`

Incidentes de qualidade poderão gerar:

```text
CreateNonConformityCommand
```

quando o tipo e a severidade justificarem.

---

# 43. Regras de integridade de Quality

## 43.1 Inspeção não é checklist

A inspeção representa a decisão de qualidade.

O checklist é um instrumento que pode apoiar a inspeção.

Uma inspeção poderá utilizar:

* formulário;
* medições;
* evidências;
* documentos;
* amostragem;
* parecer técnico.

---

## 43.2 Não conformidade não é retrabalho

A não conformidade registra o desvio.

O retrabalho é uma possível disposição do desvio.

Outras disposições:

```text
REWORK
REPAIR
SCRAP
RETURN_TO_SUPPLIER
USE_AS_IS
CONCESSION
RECLASSIFICATION
```

---

## 43.3 Resultado imutável

Uma inspeção concluída não deverá ter seu resultado sobrescrito.

Correções devem ocorrer por:

* reabertura;
* nova revisão;
* inspeção complementar;
* evento de correção;
* auditoria.

---

## 43.4 Amostragem

Planos de inspeção poderão definir:

* inspeção de 100%;
* amostragem fixa;
* amostragem por percentual;
* amostragem por lote;
* regra baseada no fornecedor;
* regra baseada em histórico;
* intensificação por reincidência.

---

## 43.5 Severidade

Severidade crítica poderá:

* bloquear produção;
* bloquear estoque;
* bloquear entrega;
* bloquear fornecedor;
* gerar notificação imediata;
* exigir aprovação executiva;
* abrir ação corretiva obrigatória.

---

## 43.6 Rastreabilidade

Todo resultado deverá permitir identificar:

* inspetor;
* data e hora;
* plano e versão;
* referência inspecionada;
* lote;
* material;
* ordem;
* operação;
* máquina;
* instrumento;
* medições;
* evidências;
* decisão;
* responsável pela aprovação.

---

## 43.7 Instrumentos de medição

Quando necessário, medições deverão registrar:

```text
instrument_id
calibration_status
calibration_due_at
measurement_unit
resolution
```

Instrumento vencido poderá invalidar ou bloquear a medição.

---

## 43.8 Ações corretivas

Uma ação concluída não é automaticamente eficaz.

A eficácia deve ser verificada posteriormente.

---

## 43.9 Responsabilidade

O registro de responsável por uma não conformidade não deve ser utilizado automaticamente como punição.

Deve representar responsabilidade pelo tratamento, salvo política explícita de apuração.

---

## 43.10 Offline

Inspeções offline deverão preservar:

```text
command_id
device_id
client_sequence
inspection_id
inspection_plan_version_id
occurred_at
expected_entity_version
measurement_records
evidence_references
```

O servidor deverá impedir duplicação e detectar alterações concorrentes.

---

# 44. Eventos resultantes de Quality

Eventos principais:

```text
quality.inspection_requested
quality.inspection_assigned
quality.inspection_started
quality.inspection_measurement_recorded
quality.inspection_measurement_out_of_tolerance
quality.inspection_completed
quality.inspection_conditionally_approved
quality.inspection_cancelled
quality.inspection_reopened
quality.nonconformity_created
quality.nonconformity_classified
quality.nonconformity_assigned
quality.nonconformity_contained
quality.nonconformity_cause_recorded
quality.rework_required
quality.concession_approved
quality.nonconforming_item_scrapped
quality.nonconformity_closed
quality.corrective_action_created
quality.corrective_action_completed
quality.action_effectiveness_verified
quality.material_quarantine_requested
quality.material_released
quality.material_rejected
quality.audit_created
quality.audit_finding_recorded
quality.audit_completed
```

Consumidores principais:

* Production;
* Inventory;
* Purchasing;
* Maintenance;
* Scheduling;
* Notifications;
* Timeline;
* Analytics;
* Automation;
* Documents.

---

# 45. Continuação

A próxima subparte continuará com:

```text
Maintenance
```

Fim da Parte 3B.
# 36. Comandos de Quality

## `CreateQualityInspectionCommand`

Cria uma inspeção de qualidade.

Permissão:

```text
quality.inspection.create
```

Payload:

```json
{
  "inspection_type": "OPERATION_OUTPUT",
  "reference_type": "OPERATION_EXECUTION",
  "reference_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_id": "uuid",
  "material_id": null,
  "purchase_receipt_id": null,
  "inspection_plan_id": "uuid",
  "assigned_inspector_employee_id": "uuid",
  "priority": "NORMAL",
  "required_by_at": "datetime",
  "notes": "Conferir medidas e acabamento"
}
```

Tipos iniciais:

```text
INCOMING_MATERIAL
PROCESS
OPERATION_OUTPUT
FINAL_PRODUCT
DELIVERY
MAINTENANCE_RELEASE
CUSTOM
```

Validações:

* referência existente e pertencente ao Tenant;
* plano de inspeção publicado quando informado;
* inspetor ativo;
* tipo coerente com a origem;
* impedir duplicidade de inspeção obrigatória aberta;
* data de necessidade válida;
* permissão e escopo do ator.

Evento resultante:

```text
quality.inspection_requested
```

---

## `AssignQualityInspectorCommand`

Atribui responsável pela inspeção.

Permissão:

```text
quality.inspection.assign
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspector_employee_id": "uuid",
  "assigned_at": "datetime",
  "notes": null
}
```

Validações:

* inspeção aberta;
* funcionário ativo;
* habilidade ou perfil compatível quando exigido;
* mesmo Tenant;
* impedir duplicidade de atribuição ativa.

Evento resultante:

```text
quality.inspection_assigned
```

---

## `UnassignQualityInspectorCommand`

Remove a atribuição do inspetor.

Permissão:

```text
quality.inspection.unassign
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspector_employee_id": "uuid",
  "reason": "Reorganização da equipe"
}
```

Validações:

* inspeção não concluída;
* não remover durante execução ativa sem procedimento;
* manter responsável quando obrigatório.

Evento resultante:

```text
quality.inspection_unassigned
```

---

## `StartQualityInspectionCommand`

Inicia a execução de uma inspeção.

Permissão:

```text
quality.inspection.start
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspector_employee_id": "uuid",
  "started_at": "datetime",
  "device_id": "uuid"
}
```

Validações:

* inspeção pendente ou atribuída;
* inspetor autorizado;
* referência ainda válida;
* nenhuma execução incompatível;
* idempotência obrigatória em PWA;
* checklist inicial quando exigido.

Evento resultante:

```text
quality.inspection_started
```

---

## `RecordInspectionMeasurementCommand`

Registra uma medição da inspeção.

Permissão:

```text
quality.inspection.measurement.record
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspection_item_id": "uuid",
  "measurement_code": "WIDTH_MM",
  "measured_value": "598.50",
  "unit": "MM",
  "lower_tolerance": "597.00",
  "upper_tolerance": "599.00",
  "measured_at": "datetime",
  "instrument_id": "uuid",
  "notes": null
}
```

Validações:

* inspeção ativa;
* item pertencente ao plano;
* unidade compatível;
* instrumento válido quando exigido;
* valor numérico válido;
* tolerâncias provenientes do plano ou autorizadas;
* não sobrescrever medição anterior sem histórico.

Eventos possíveis:

```text
quality.inspection_measurement_recorded
quality.inspection_measurement_out_of_tolerance
```

---

## `RecordInspectionChecklistCommand`

Registra respostas de um checklist de inspeção.

Permissão:

```text
quality.inspection.checklist.record
```

Payload:

```json
{
  "inspection_id": "uuid",
  "form_submission_id": "uuid",
  "completed_at": "datetime"
}
```

Validações:

* formulário compatível;
* versão publicada;
* submissão concluída;
* vínculo com a inspeção;
* não utilizar formulário de outro Tenant.

Evento resultante:

```text
quality.inspection_checklist_recorded
```

---

## `AttachInspectionEvidenceCommand`

Vincula evidência à inspeção.

Permissão:

```text
quality.inspection.evidence.attach
```

Payload:

```json
{
  "inspection_id": "uuid",
  "document_id": "uuid",
  "evidence_type": "PHOTO",
  "description": "Foto da borda danificada"
}
```

Tipos iniciais:

```text
PHOTO
VIDEO_REFERENCE
REPORT
CERTIFICATE
MEASUREMENT_FILE
SUPPLIER_DOCUMENT
OTHER
```

Validações:

* documento acessível;
* mesmo Tenant;
* inspeção não arquivada;
* vínculo não duplicado;
* tipo permitido.

Evento resultante:

```text
quality.inspection_evidence_attached
```

---

## `RemoveInspectionEvidenceCommand`

Remove vínculo de evidência incorreta.

Permissão:

```text
quality.inspection.evidence.remove
```

Payload:

```json
{
  "inspection_id": "uuid",
  "inspection_evidence_id": "uuid",
  "reason": "Documento vinculado incorretamente"
}
```

Validações:

* não apagar o documento físico;
* preservar auditoria;
* evidência não obrigatória ou substituída;
* inspeção ainda alterável ou permissão administrativa.

Evento resultante:

```text
quality.inspection_evidence_removed
```

---

## `ApproveQualityInspectionCommand`

Conclui a inspeção com resultado aprovado.

Permissão:

```text
quality.inspection.approve
```

Payload:

```json
{
  "inspection_id": "uuid",
  "completed_at": "datetime",
  "result": "APPROVED",
  "approval_notes": "Peças dentro das tolerâncias",
  "approved_quantity": "10.0000",
  "rejected_quantity": "0.0000"
}
```

Validações:

* inspeção ativa;
* itens obrigatórios verificados;
* medições obrigatórias registradas;
* nenhuma medição bloqueante fora da tolerância;
* formulários obrigatórios concluídos;
* evidências obrigatórias anexadas;
* quantidades coerentes;
* inspetor autorizado;
* nenhuma não conformidade bloqueante aberta.

Evento resultante:

```text
quality.inspection_completed
```

Payload do evento deverá indicar:

```text
result = APPROVED
```

---

## `ConditionallyApproveInspectionCommand`

Aprova com ressalvas.

Permissão:

```text
quality.inspection.conditionally_approve
```

Payload:

```json
{
  "inspection_id": "uuid",
  "completed_at": "datetime",
  "conditions": [
    {
      "code": "MINOR_FINISH_ADJUSTMENT",
      "description": "Realizar pequeno ajuste antes da entrega"
    }
  ],
  "responsible_employee_id": "uuid",
  "due_at": "datetime",
  "approval_notes": "Liberado com correção obrigatória"
}
```

Validações:

* política permite aprovação condicional;
* desvio não classificado como crítico;
* condição possui responsável e prazo;
* não utilizar para ocultar não conformidade;
* aprovação por ator com alçada.

Eventos resultantes:

```text
quality.inspection_conditionally_approved
quality.corrective_action_created
```

---

## `RejectQualityInspectionCommand`

Conclui a inspeção com rejeição.

Permissão:

```text
quality.inspection.reject
```

Payload:

```json
{
  "inspection_id": "uuid",
  "completed_at": "datetime",
  "result": "REJECTED",
  "reason_code": "DIMENSION_OUT_OF_TOLERANCE",
  "reason": "Peça fora da medida especificada",
  "approved_quantity": "8.0000",
  "rejected_quantity": "2.0000",
  "create_nonconformity": true
}
```

Validações:

* inspeção ativa;
* motivo obrigatório;
* quantidades coerentes;
* evidência quando exigida;
* não conformidade obrigatória conforme severidade;
* bloquear liberação quando configurado.

Eventos resultantes:

```text
quality.inspection_completed
quality.nonconformity_created
```

Payload da inspeção deverá indicar:

```text
result = REJECTED
```

---

## `CancelQualityInspectionCommand`

Cancela uma inspeção criada indevidamente ou tornada desnecessária.

Permissão:

```text
quality.inspection.cancel
```

Payload:

```json
{
  "inspection_id": "uuid",
  "reason_code": "REFERENCE_CANCELLED",
  "reason": "Operação de origem foi cancelada"
}
```

Validações:

* inspeção não concluída;
* não ocultar medições já registradas;
* preservar histórico;
* não cancelar inspeção obrigatória sem substituição ou autorização.

Evento resultante:

```text
quality.inspection_cancelled
```

---

## `ReopenQualityInspectionCommand`

Reabre inspeção concluída.

Permissão:

```text
quality.inspection.reopen
```

Payload:

```json
{
  "inspection_id": "uuid",
  "reason_code": "NEW_EVIDENCE",
  "reason": "Foi identificada nova evidência após a conclusão"
}
```

Validações:

* permissão administrativa;
* preservar resultado anterior;
* criar nova revisão ou ciclo de inspeção;
* auditoria detalhada;
* impactos em produção e estoque avaliados.

Evento resultante:

```text
quality.inspection_reopened
```

---

# 37. Planos de inspeção

## `CreateInspectionPlanCommand`

Cria um plano de inspeção.

Permissão:

```text
quality.inspection_plan.create
```

Payload:

```json
{
  "code": "FINAL_FURNITURE_INSPECTION",
  "name": "Inspeção final do móvel",
  "category": "FINAL_PRODUCT",
  "description": "Verificações obrigatórias antes da entrega",
  "applicable_reference_types": [
    "PRODUCTION_ORDER"
  ]
}
```

Evento resultante:

```text
quality.inspection_plan_created
```

---

## `CreateInspectionPlanVersionCommand`

Cria uma versão editável do plano.

Permissão:

```text
quality.inspection_plan.version.create
```

Payload:

```json
{
  "inspection_plan_id": "uuid",
  "based_on_version_id": "uuid",
  "change_reason": "Inclusão de conferência de ferragens"
}
```

Evento resultante:

```text
quality.inspection_plan_version_created
```

---

## `AddInspectionPlanItemCommand`

Adiciona item ao plano.

Permissão:

```text
quality.inspection_plan.item.create
```

Payload:

```json
{
  "inspection_plan_version_id": "uuid",
  "code": "CHECK_DOOR_ALIGNMENT",
  "name": "Alinhamento das portas",
  "item_type": "BOOLEAN",
  "order_index": 1,
  "is_required": true,
  "acceptance_criteria": {
    "expected_value": true
  }
}
```

Tipos iniciais:

```text
BOOLEAN
NUMERIC
TEXT
SELECTION
PHOTO
DOCUMENT
SIGNATURE
MEASUREMENT
```

Validações:

* versão em rascunho;
* código único;
* critério compatível com o tipo;
* ordem válida;
* regra de obrigatoriedade coerente.

Evento resultante:

```text
quality.inspection_plan_item_added
```

---

## `UpdateInspectionPlanItemCommand`

Atualiza item do plano.

Permissão:

```text
quality.inspection_plan.item.update
```

Payload:

```json
{
  "inspection_plan_item_id": "uuid",
  "name": "Conferir alinhamento das portas",
  "order_index": 2,
  "is_required": true,
  "acceptance_criteria": {
    "expected_value": true
  }
}
```

Evento resultante:

```text
quality.inspection_plan_item_updated
```

---

## `RemoveInspectionPlanItemCommand`

Remove item de versão em rascunho.

Permissão:

```text
quality.inspection_plan.item.remove
```

Payload:

```json
{
  "inspection_plan_item_id": "uuid",
  "reason": "Verificação consolidada em outro item"
}
```

Validações:

* versão não publicada;
* plano permanece válido;
* referências condicionais atualizadas.

Evento resultante:

```text
quality.inspection_plan_item_removed
```

---

## `PublishInspectionPlanVersionCommand`

Publica a versão do plano.

Permissão:

```text
quality.inspection_plan.version.publish
```

Payload:

```json
{
  "inspection_plan_version_id": "uuid",
  "publication_notes": "Plano validado pela gestão"
}
```

Validações:

* pelo menos um item;
* códigos únicos;
* critérios válidos;
* regras sem referências quebradas;
* versão passa a ser imutável.

Evento resultante:

```text
quality.inspection_plan_version_published
```

---

## `DeprecateInspectionPlanVersionCommand`

Marca versão como obsoleta para novas inspeções.

Permissão:

```text
quality.inspection_plan.version.deprecate
```

Payload:

```json
{
  "inspection_plan_version_id": "uuid",
  "replacement_version_id": "uuid",
  "reason": "Nova versão publicada"
}
```

Evento resultante:

```text
quality.inspection_plan_version_deprecated
```

---

## `BindInspectionPlanCommand`

Vincula plano a uma origem.

Permissão:

```text
quality.inspection_plan.bind
```

Payload:

```json
{
  "inspection_plan_id": "uuid",
  "binding_type": "OPERATION_DEFINITION",
  "workflow_definition_id": "uuid",
  "stage_definition_id": "uuid",
  "operation_definition_id": "uuid",
  "material_category": null,
  "is_mandatory": true,
  "trigger": "AFTER_EXECUTION_FINISH"
}
```

Validações:

* plano publicado;
* alvo válido;
* vínculo não duplicado;
* trigger compatível;
* mesmo Tenant.

Evento resultante:

```text
quality.inspection_plan_bound
```

---

## `UnbindInspectionPlanCommand`

Remove o vínculo para novas operações.

Permissão:

```text
quality.inspection_plan.unbind
```

Payload:

```json
{
  "inspection_plan_binding_id": "uuid",
  "reason": "Plano substituído"
}
```

Evento resultante:

```text
quality.inspection_plan_unbound
```

---

# 38. Não conformidades

## `CreateNonConformityCommand`

Registra uma não conformidade.

Permissão:

```text
quality.nonconformity.create
```

Payload:

```json
{
  "source_type": "QUALITY_INSPECTION",
  "source_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_id": "uuid",
  "material_id": null,
  "supplier_id": null,
  "machine_id": null,
  "category": "DIMENSION",
  "severity": "HIGH",
  "title": "Peça fora da medida",
  "description": "Largura medida abaixo da tolerância",
  "detected_at": "datetime",
  "detected_by_employee_id": "uuid",
  "affected_quantity": "2.0000",
  "immediate_action": "Segregar peças"
}
```

Categorias iniciais:

```text
DIMENSION
MATERIAL
FINISH
ASSEMBLY
DESIGN
DOCUMENTATION
PROCESS
MACHINE
SUPPLIER
SAFETY
DELIVERY
OTHER
```

Severidades:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Validações:

* origem válida;
* descrição e categoria;
* severidade;
* quantidade afetada válida;
* referências pertencentes ao mesmo Tenant;
* evidência conforme política;
* impedir duplicidade evidente sem justificativa.

Evento resultante:

```text
quality.nonconformity_created
```

---

## `ClassifyNonConformityCommand`

Atualiza a classificação técnica.

Permissão:

```text
quality.nonconformity.classify
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "category": "MANUFACTURING_PROCESS",
  "severity": "HIGH",
  "probability": "MEDIUM",
  "impact": "HIGH",
  "classification_notes": "Erro recorrente na regulagem da máquina"
}
```

Validações:

* não conformidade aberta;
* valores de classificação válidos;
* mudança de severidade crítica exige notificação;
* preservar classificação anterior.

Evento resultante:

```text
quality.nonconformity_classified
```

---

## `AssignNonConformityCommand`

Atribui responsável pela análise e tratamento.

Permissão:

```text
quality.nonconformity.assign
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "assigned_user_id": "uuid",
  "assigned_employee_id": "uuid",
  "assigned_sector_id": "uuid",
  "due_at": "datetime"
}
```

Validações:

* não conformidade aberta;
* responsável ativo;
* prazo coerente;
* escopo adequado.

Evento resultante:

```text
quality.nonconformity_assigned
```

---

## `ContainNonConformityCommand`

Registra ação imediata de contenção.

Permissão:

```text
quality.nonconformity.contain
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "containment_action": "Segregar todas as peças do lote",
  "contained_quantity": "10.0000",
  "stock_location_id": "uuid",
  "performed_by_employee_id": "uuid",
  "performed_at": "datetime",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* quantidade válida;
* material ou produto identificável;
* local de quarentena quando aplicável;
* evidência conforme severidade;
* não reduzir rastreabilidade.

Eventos resultantes:

```text
quality.nonconformity_contained
inventory.stock_quarantined
```

O segundo evento será produzido pelo contexto Inventory após comando próprio.

---

## `RecordNonConformityCauseCommand`

Registra causa identificada.

Permissão:

```text
quality.nonconformity.cause.record
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "cause_type": "ROOT_CAUSE",
  "method": "FIVE_WHYS",
  "description": "Regulagem incorreta da serra após manutenção",
  "is_confirmed": true,
  "analysis_document_id": "uuid"
}
```

Tipos:

```text
IMMEDIATE_CAUSE
CONTRIBUTING_CAUSE
ROOT_CAUSE
```

Validações:

* não conformidade em análise;
* método válido;
* causa não vazia;
* confirmação técnica quando exigida.

Evento resultante:

```text
quality.nonconformity_cause_recorded
```

---

## `RequestReworkFromNonConformityCommand`

Solicita retrabalho a partir da não conformidade.

Permissão:

```text
quality.nonconformity.rework.request
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "original_operation_instance_id": "uuid",
  "affected_quantity": "2.0000",
  "reason": "Refazer peças fora da medida",
  "priority": "HIGH",
  "assigned_sector_id": "uuid",
  "estimated_minutes": 90
}
```

Validações:

* não conformidade aberta;
* origem produtiva válida;
* quantidade afetada;
* não duplicar retrabalho ativo;
* preservar operação original.

Eventos resultantes:

```text
quality.rework_required
production.rework_requested
```

O comando de criação efetiva do retrabalho deverá ser executado pelo contexto Production.

---

## `ApproveConcessionCommand`

Autoriza uso de item fora da especificação mediante concessão.

Permissão:

```text
quality.concession.approve
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "approved_quantity": "1.0000",
  "concession_reason": "Desvio sem impacto funcional ou visual",
  "approved_by_user_id": "uuid",
  "expires_at": null,
  "customer_approval_document_id": "uuid"
}
```

Validações:

* política permite concessão;
* severidade não crítica;
* impacto avaliado;
* alçada do aprovador;
* aprovação do cliente quando exigida;
* quantidade não superior à afetada.

Evento resultante:

```text
quality.concession_approved
```

---

## `RejectConcessionCommand`

Rejeita pedido de concessão.

Permissão:

```text
quality.concession.reject
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "reason": "Desvio pode comprometer a durabilidade"
}
```

Evento resultante:

```text
quality.concession_rejected
```

---

## `ScrapNonConformingItemCommand`

Classifica item como perda ou sucata.

Permissão:

```text
quality.nonconforming_item.scrap
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "material_id": "uuid",
  "production_order_id": "uuid",
  "quantity": "2.0000",
  "unit": "UN",
  "reason": "Peças sem possibilidade de reaproveitamento",
  "scrap_stock_location_id": "uuid"
}
```

Validações:

* quantidade válida;
* autorização conforme custo;
* material identificado;
* movimento de estoque obrigatório;
* custo de perda preservado.

Eventos resultantes:

```text
quality.nonconforming_item_scrapped
inventory.material_scrapped
```

O movimento físico será realizado pelo Inventory.

---

## `CloseNonConformityCommand`

Encerra uma não conformidade.

Permissão:

```text
quality.nonconformity.close
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "resolution_code": "REWORK_COMPLETED",
  "resolution_summary": "Peças refeitas e aprovadas",
  "closed_at": "datetime",
  "verification_inspection_id": "uuid"
}
```

Validações:

* contenção concluída;
* causa registrada quando exigida;
* ações corretivas obrigatórias concluídas;
* retrabalho ou descarte finalizado;
* inspeção de verificação aprovada;
* nenhuma pendência bloqueante.

Evento resultante:

```text
quality.nonconformity_closed
```

---

## `ReopenNonConformityCommand`

Reabre uma não conformidade encerrada.

Permissão:

```text
quality.nonconformity.reopen
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "reason": "Problema voltou a ocorrer após o encerramento"
}
```

Validações:

* permissão administrativa;
* preservar encerramento anterior;
* registrar reincidência;
* recalcular severidade quando necessário.

Evento resultante:

```text
quality.nonconformity_reopened
```

---

## `CancelNonConformityCommand`

Cancela registro criado indevidamente.

Permissão:

```text
quality.nonconformity.cancel
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "reason_code": "DUPLICATE_RECORD",
  "reason": "Registro duplicado",
  "replacement_nonconformity_id": "uuid"
}
```

Validações:

* não conformidade sem efeitos irreversíveis;
* indicar registro substituto quando duplicada;
* não apagar histórico;
* auditoria obrigatória.

Evento resultante:

```text
quality.nonconformity_cancelled
```

---

# 39. Ações corretivas e preventivas

## `CreateCorrectiveActionCommand`

Cria ação corretiva.

Permissão:

```text
quality.corrective_action.create
```

Payload:

```json
{
  "nonconformity_id": "uuid",
  "title": "Padronizar regulagem da serra",
  "description": "Criar checklist de regulagem antes do início do corte",
  "action_type": "CORRECTIVE",
  "responsible_user_id": "uuid",
  "responsible_employee_id": "uuid",
  "responsible_sector_id": "uuid",
  "due_at": "datetime",
  "verification_method": "PROCESS_AUDIT"
}
```

Evento resultante:

```text
quality.corrective_action_created
```

---

## `CreatePreventiveActionCommand`

Cria ação preventiva sem não conformidade obrigatória.

Permissão:

```text
quality.preventive_action.create
```

Payload:

```json
{
  "risk_reference_type": "PROCESS",
  "risk_reference_id": "uuid",
  "title": "Revisar plano de manutenção preventiva",
  "description": "Evitar perda de regulagem da máquina",
  "responsible_user_id": "uuid",
  "due_at": "datetime"
}
```

Evento resultante:

```text
quality.preventive_action_created
```

---

## `UpdateQualityActionCommand`

Atualiza ação aberta.

Permissão:

```text
quality.action.update
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "title": "Checklist de regulagem e liberação",
  "description": "Descrição revisada",
  "responsible_user_id": "uuid",
  "responsible_employee_id": "uuid",
  "due_at": "datetime",
  "priority": "HIGH"
}
```

Validações:

* ação não concluída;
* responsável ativo;
* prazo válido;
* concorrência otimista.

Evento resultante:

```text
quality.action_updated
```

---

## `StartQualityActionCommand`

Inicia ação corretiva ou preventiva.

Permissão:

```text
quality.action.start
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "started_at": "datetime"
}
```

Evento resultante:

```text
quality.action_started
```

---

## `CompleteQualityActionCommand`

Conclui ação.

Permissão:

```text
quality.action.complete
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "completed_at": "datetime",
  "completion_summary": "Checklist implantado e equipe treinada",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* ação iniciada;
* evidências quando exigidas;
* campos obrigatórios;
* não marcar como eficaz automaticamente.

Evento resultante:

```text
quality.corrective_action_completed
```

ou:

```text
quality.preventive_action_completed
```

---

## `VerifyQualityActionEffectivenessCommand`

Avalia a eficácia da ação.

Permissão:

```text
quality.action.verify_effectiveness
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "verification_result": "EFFECTIVE",
  "verified_at": "datetime",
  "verified_by_employee_id": "uuid",
  "verification_notes": "Não houve reincidência em 30 dias",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Resultados:

```text
EFFECTIVE
PARTIALLY_EFFECTIVE
INEFFECTIVE
INCONCLUSIVE
```

Validações:

* ação concluída;
* período mínimo quando configurado;
* verificador autorizado;
* evidência suficiente.

Eventos possíveis:

```text
quality.action_effectiveness_verified
quality.action_rework_required
```

---

## `CancelQualityActionCommand`

Cancela ação criada indevidamente ou substituída.

Permissão:

```text
quality.action.cancel
```

Payload:

```json
{
  "quality_action_id": "uuid",
  "reason": "Ação consolidada em plano mais abrangente",
  "replacement_action_id": "uuid"
}
```

Evento resultante:

```text
quality.action_cancelled
```

---

# 40. Controle de materiais não conformes

## `QuarantineMaterialCommand`

Solicita segregação de material.

Permissão:

```text
quality.material.quarantine
```

Payload:

```json
{
  "material_id": "uuid",
  "stock_location_id": "uuid",
  "quantity": "5.0000",
  "batch_code": "LOTE-001",
  "nonconformity_id": "uuid",
  "reason": "Aguardando análise de qualidade",
  "quarantine_location_id": "uuid"
}
```

Validações:

* saldo disponível;
* quantidade válida;
* localização de quarentena;
* não conformidade ativa;
* idempotência.

Eventos resultantes:

```text
quality.material_quarantine_requested
inventory.stock_quarantined
```

---

## `ReleaseQuarantinedMaterialCommand`

Libera material aprovado.

Permissão:

```text
quality.material.release
```

Payload:

```json
{
  "material_id": "uuid",
  "quarantine_record_id": "uuid",
  "quantity": "5.0000",
  "inspection_id": "uuid",
  "released_at": "datetime",
  "target_stock_location_id": "uuid"
}
```

Validações:

* inspeção aprovada;
* quantidade em quarentena;
* autorização do inspetor;
* destino válido.

Eventos resultantes:

```text
quality.material_released
inventory.quarantined_stock_released
```

---

## `RejectIncomingMaterialCommand`

Rejeita material recebido.

Permissão:

```text
quality.incoming_material.reject
```

Payload:

```json
{
  "inspection_id": "uuid",
  "purchase_order_id": "uuid",
  "receipt_id": "uuid",
  "receipt_item_id": "uuid",
  "material_id": "uuid",
  "rejected_quantity": "2.0000",
  "reason_code": "DAMAGED",
  "reason": "Chapas danificadas no transporte",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* inspeção de recebimento;
* quantidade válida;
* não consumir material rejeitado;
* evidência;
* fornecedor e lote identificados.

Eventos resultantes:

```text
quality.material_rejected
purchasing.receipt_item_rejected
```

---

## `AcceptIncomingMaterialWithDeviationCommand`

Aceita material com desvio autorizado.

Permissão:

```text
quality.incoming_material.accept_with_deviation
```

Payload:

```json
{
  "inspection_id": "uuid",
  "receipt_item_id": "uuid",
  "accepted_quantity": "2.0000",
  "deviation_description": "Variação de tonalidade sem impacto no projeto",
  "approved_by_user_id": "uuid",
  "supplier_credit_required": false
}
```

Validações:

* política permite;
* desvio não crítico;
* alçada;
* rastreabilidade do lote;
* concessão registrada.

Eventos resultantes:

```text
quality.incoming_material_accepted_with_deviation
quality.concession_approved
```

---

# 41. Auditorias de qualidade

## `CreateQualityAuditCommand`

Cria auditoria interna ou externa.

Permissão:

```text
quality.audit.create
```

Payload:

```json
{
  "audit_type": "INTERNAL_PROCESS",
  "code": "AUD-2026-001",
  "title": "Auditoria do processo de corte",
  "scope": "Setor de corte",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "planned_start_at": "datetime",
  "planned_end_at": "datetime",
  "lead_auditor_employee_id": "uuid",
  "audit_team_employee_ids": [
    "uuid"
  ],
  "criteria": [
    "PROCEDURE_COMPLIANCE",
    "RECORDS",
    "EQUIPMENT_CONDITION"
  ]
}
```

Evento resultante:

```text
quality.audit_created
```

---

## `StartQualityAuditCommand`

Inicia auditoria.

Permissão:

```text
quality.audit.start
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "started_at": "datetime"
}
```

Evento resultante:

```text
quality.audit_started
```

---

## `RecordQualityAuditFindingCommand`

Registra constatação.

Permissão:

```text
quality.audit.finding.record
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "finding_type": "NONCONFORMITY",
  "severity": "MEDIUM",
  "title": "Checklist não preenchido",
  "description": "Foram encontradas operações sem checklist final",
  "reference_type": "OPERATION",
  "reference_id": "uuid",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Tipos:

```text
CONFORMITY
OBSERVATION
OPPORTUNITY_FOR_IMPROVEMENT
NONCONFORMITY
CRITICAL_NONCONFORMITY
```

Eventos possíveis:

```text
quality.audit_finding_recorded
quality.nonconformity_created
```

---

## `CompleteQualityAuditCommand`

Conclui auditoria.

Permissão:

```text
quality.audit.complete
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "completed_at": "datetime",
  "summary": "Auditoria concluída com duas não conformidades",
  "overall_result": "PARTIALLY_COMPLIANT",
  "report_document_id": "uuid"
}
```

Validações:

* auditoria iniciada;
* achados classificados;
* relatório quando exigido;
* responsáveis definidos para pendências.

Evento resultante:

```text
quality.audit_completed
```

---

## `CancelQualityAuditCommand`

Cancela auditoria planejada.

Permissão:

```text
quality.audit.cancel
```

Payload:

```json
{
  "quality_audit_id": "uuid",
  "reason": "Unidade indisponível na data prevista"
}
```

Evento resultante:

```text
quality.audit_cancelled
```

---

# 42. Integrações de Quality

## Eventos consumidos

Quality deverá consumir inicialmente:

```text
production.execution_finished
production.rework_requested
purchasing.material_received
maintenance.machine_released
forms.submission_completed
incident.created
```

---

## Reação a `production.execution_finished`

Quando a operação exigir inspeção:

```text
CreateQualityInspectionCommand
```

A conclusão da operação poderá permanecer:

* pendente de qualidade;
* aprovada;
* rejeitada;
* aprovada condicionalmente.

---

## Reação a `purchasing.material_received`

Quando o material exigir inspeção de recebimento:

```text
CreateQualityInspectionCommand
```

O material deverá permanecer:

```text
PENDING_INSPECTION
```

ou em quarentena até o resultado.

---

## Reação a `maintenance.machine_released`

Poderá criar inspeção de liberação da máquina quando:

* manutenção afetar precisão;
* houver troca de componente crítico;
* calibração for necessária;
* a política de qualidade exigir.

---

## Reação a `incident.created`

Incidentes de qualidade poderão gerar:

```text
CreateNonConformityCommand
```

quando o tipo e a severidade justificarem.

---

# 43. Regras de integridade de Quality

## 43.1 Inspeção não é checklist

A inspeção representa a decisão de qualidade.

O checklist é um instrumento que pode apoiar a inspeção.

Uma inspeção poderá utilizar:

* formulário;
* medições;
* evidências;
* documentos;
* amostragem;
* parecer técnico.

---

## 43.2 Não conformidade não é retrabalho

A não conformidade registra o desvio.

O retrabalho é uma possível disposição do desvio.

Outras disposições:

```text
REWORK
REPAIR
SCRAP
RETURN_TO_SUPPLIER
USE_AS_IS
CONCESSION
RECLASSIFICATION
```

---

## 43.3 Resultado imutável

Uma inspeção concluída não deverá ter seu resultado sobrescrito.

Correções devem ocorrer por:

* reabertura;
* nova revisão;
* inspeção complementar;
* evento de correção;
* auditoria.

---

## 43.4 Amostragem

Planos de inspeção poderão definir:

* inspeção de 100%;
* amostragem fixa;
* amostragem por percentual;
* amostragem por lote;
* regra baseada no fornecedor;
* regra baseada em histórico;
* intensificação por reincidência.

---

## 43.5 Severidade

Severidade crítica poderá:

* bloquear produção;
* bloquear estoque;
* bloquear entrega;
* bloquear fornecedor;
* gerar notificação imediata;
* exigir aprovação executiva;
* abrir ação corretiva obrigatória.

---

## 43.6 Rastreabilidade

Todo resultado deverá permitir identificar:

* inspetor;
* data e hora;
* plano e versão;
* referência inspecionada;
* lote;
* material;
* ordem;
* operação;
* máquina;
* instrumento;
* medições;
* evidências;
* decisão;
* responsável pela aprovação.

---

## 43.7 Instrumentos de medição

Quando necessário, medições deverão registrar:

```text
instrument_id
calibration_status
calibration_due_at
measurement_unit
resolution
```

Instrumento vencido poderá invalidar ou bloquear a medição.

---

## 43.8 Ações corretivas

Uma ação concluída não é automaticamente eficaz.

A eficácia deve ser verificada posteriormente.

---

## 43.9 Responsabilidade

O registro de responsável por uma não conformidade não deve ser utilizado automaticamente como punição.

Deve representar responsabilidade pelo tratamento, salvo política explícita de apuração.

---

## 43.10 Offline

Inspeções offline deverão preservar:

```text
command_id
device_id
client_sequence
inspection_id
inspection_plan_version_id
occurred_at
expected_entity_version
measurement_records
evidence_references
```

O servidor deverá impedir duplicação e detectar alterações concorrentes.

---

# 44. Eventos resultantes de Quality

Eventos principais:

```text
quality.inspection_requested
quality.inspection_assigned
quality.inspection_started
quality.inspection_measurement_recorded
quality.inspection_measurement_out_of_tolerance
quality.inspection_completed
quality.inspection_conditionally_approved
quality.inspection_cancelled
quality.inspection_reopened
quality.nonconformity_created
quality.nonconformity_classified
quality.nonconformity_assigned
quality.nonconformity_contained
quality.nonconformity_cause_recorded
quality.rework_required
quality.concession_approved
quality.nonconforming_item_scrapped
quality.nonconformity_closed
quality.corrective_action_created
quality.corrective_action_completed
quality.action_effectiveness_verified
quality.material_quarantine_requested
quality.material_released
quality.material_rejected
quality.audit_created
quality.audit_finding_recorded
quality.audit_completed
```

Consumidores principais:

* Production;
* Inventory;
* Purchasing;
* Maintenance;
* Scheduling;
* Notifications;
* Timeline;
* Analytics;
* Automation;
* Documents.

---

# 45. Continuação

A próxima subparte continuará com:

```text
Maintenance
```

Fim da Parte 3B.
# 55. Comandos de Scheduling

## `CreateScheduleItemCommand`

Cria um item de agenda operacional.

Permissão:

```text
scheduling.item.create
```

Payload:

```json
{
  "schedule_type": "OPERATION",
  "reference_type": "OPERATION_INSTANCE",
  "reference_id": "uuid",
  "title": "Corte da estrutura",
  "description": "Execução prevista para o setor de corte",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "work_center_id": "uuid",
  "planned_start_at": "datetime",
  "planned_end_at": "datetime",
  "priority": "NORMAL",
  "status": "PLANNED",
  "required_capacity": "1.0000",
  "capacity_unit": "RESOURCE",
  "configuration": {}
}
```

Tipos iniciais:

```text
OPERATION
PRODUCTION_ORDER
MAINTENANCE
INSPECTION
DELIVERY
PURCHASE_RECEIPT
MEETING
EMPLOYEE_BLOCK
MACHINE_BLOCK
CUSTOM
```

Validações:

* referência válida;
* início anterior ao término;
* filial, setor e centro de trabalho pertencentes ao Tenant;
* capacidade positiva;
* tipo compatível com a referência;
* impedir duplicidade quando a origem permitir apenas um agendamento ativo;
* verificar restrições obrigatórias;
* concorrência otimista;
* idempotência quando criado por automação ou evento.

Evento resultante:

```text
scheduling.item_created
```

---

## `UpdateScheduleItemCommand`

Atualiza dados de um item ainda não concluído.

Permissão:

```text
scheduling.item.update
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "title": "Corte estrutural",
  "description": "Descrição revisada",
  "priority": "HIGH",
  "branch_id": "uuid",
  "sector_id": "uuid",
  "work_center_id": "uuid",
  "required_capacity": "2.0000",
  "configuration": {}
}
```

Validações:

* item não concluído ou cancelado;
* referências estruturais válidas;
* alteração de capacidade reavalia conflitos;
* alteração de prioridade auditada;
* não modificar histórico de execução;
* concorrência otimista.

Evento resultante:

```text
scheduling.item_updated
```

---

## `ScheduleItemCommand`

Define ou confirma o período planejado.

Permissão:

```text
scheduling.item.schedule
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "planned_start_at": "datetime",
  "planned_end_at": "datetime",
  "scheduling_strategy": "MANUAL",
  "allow_soft_conflicts": false,
  "notes": "Planejamento confirmado"
}
```

Estratégias iniciais:

```text
MANUAL
EARLIEST_AVAILABLE
LATEST_POSSIBLE
FORWARD
BACKWARD
CAPACITY_BALANCED
PRIORITY_BASED
AUTOMATED
```

Validações:

* período válido;
* calendário operacional;
* disponibilidade de recursos obrigatórios;
* dependências anteriores;
* prazo da entidade de origem;
* restrições de capacidade;
* conflitos duros impedem o agendamento;
* conflitos flexíveis exigem autorização quando permitidos.

Eventos possíveis:

```text
scheduling.item_scheduled
scheduling.conflict_detected
```

---

## `RescheduleItemCommand`

Reagenda um item.

Permissão:

```text
scheduling.item.reschedule
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "new_start_at": "datetime",
  "new_end_at": "datetime",
  "reason_code": "MATERIAL_DELAY",
  "reason": "Material não chegará na data prevista",
  "propagate_to_dependencies": true
}
```

Motivos iniciais:

```text
MATERIAL_DELAY
MACHINE_UNAVAILABLE
EMPLOYEE_UNAVAILABLE
PRIORITY_CHANGE
CUSTOMER_REQUEST
PREVIOUS_TASK_DELAY
MAINTENANCE
QUALITY_HOLD
WEATHER
MANUAL_ADJUSTMENT
OTHER
```

Validações:

* item reagendável;
* novas datas válidas;
* dependências avaliadas;
* recursos revalidados;
* impacto no prazo calculado;
* propagação controlada;
* motivo obrigatório;
* não sobrescrever histórico anterior.

Evento resultante:

```text
scheduling.item_rescheduled
```

Eventos adicionais possíveis:

```text
scheduling.dependent_item_rescheduled
scheduling.due_date_risk_detected
```

---

## `CancelScheduleItemCommand`

Cancela o agendamento.

Permissão:

```text
scheduling.item.cancel
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "reason_code": "SOURCE_CANCELLED",
  "reason": "Ordem de origem cancelada",
  "release_resources": true
}
```

Validações:

* item não concluído;
* não apagar histórico;
* execução ativa deve ser tratada pelo contexto proprietário;
* liberar reservas de agenda;
* avaliar itens dependentes;
* notificar responsáveis quando necessário.

Evento resultante:

```text
scheduling.item_cancelled
```

---

## `CompleteScheduleItemCommand`

Marca o item como concluído do ponto de vista da agenda.

Permissão:

```text
scheduling.item.complete
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "completed_at": "datetime",
  "completion_reference_type": "OPERATION_EXECUTION",
  "completion_reference_id": "uuid",
  "notes": "Execução concluída"
}
```

Validações:

* item iniciado ou vinculado a fato concluído;
* referência de conclusão válida;
* não concluir antes da origem;
* preservar datas planejadas e reais.

Evento resultante:

```text
scheduling.item_completed
```

---

## `StartScheduleItemCommand`

Registra o início real do item.

Permissão:

```text
scheduling.item.start
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "started_at": "datetime",
  "source_reference_type": "OPERATION_EXECUTION",
  "source_reference_id": "uuid"
}
```

Validações:

* item planejado;
* horário coerente;
* recursos disponíveis;
* origem iniciada;
* impedir início duplicado.

Evento resultante:

```text
scheduling.item_started
```

---

## `PauseScheduleItemCommand`

Pausa o acompanhamento do item.

Permissão:

```text
scheduling.item.pause
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "paused_at": "datetime",
  "reason_code": "SOURCE_PAUSED",
  "reason": "Execução produtiva pausada"
}
```

Evento resultante:

```text
scheduling.item_paused
```

---

## `ResumeScheduleItemCommand`

Retoma item pausado.

Permissão:

```text
scheduling.item.resume
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "resumed_at": "datetime"
}
```

Evento resultante:

```text
scheduling.item_resumed
```

---

# 56. Recursos de agenda

## `AssignScheduleResourceCommand`

Atribui um recurso ao item.

Permissão:

```text
scheduling.resource.assign
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "resource_type": "EMPLOYEE",
  "resource_id": "uuid",
  "allocation_percentage": 100,
  "role_in_schedule": "PRIMARY",
  "assigned_at": "datetime"
}
```

Tipos de recurso:

```text
EMPLOYEE
TEAM
MACHINE
EQUIPMENT
WORK_CENTER
VEHICLE
ROOM
STOCK_LOCATION
SUPPLIER
CUSTOM
```

Validações:

* item ativo;
* recurso válido;
* percentual entre 1 e 100;
* recurso compatível;
* disponibilidade;
* capacidade;
* ausência de duplicidade;
* escopo e Tenant;
* habilidades ou qualificações quando exigidas.

Eventos possíveis:

```text
scheduling.resource_assigned
scheduling.conflict_detected
```

---

## `UnassignScheduleResourceCommand`

Remove recurso do item.

Permissão:

```text
scheduling.resource.unassign
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "schedule_resource_id": "uuid",
  "reason": "Funcionário substituído"
}
```

Validações:

* recurso vinculado;
* item não concluído;
* manter recursos mínimos obrigatórios;
* execução ativa avaliada;
* preservar histórico.

Evento resultante:

```text
scheduling.resource_unassigned
```

---

## `ReplaceScheduleResourceCommand`

Substitui recurso atribuído.

Permissão:

```text
scheduling.resource.replace
```

Payload:

```json
{
  "schedule_item_id": "uuid",
  "current_resource_id": "uuid",
  "new_resource_id": "uuid",
  "resource_type": "EMPLOYEE",
  "effective_at": "datetime",
  "reason": "Funcionário indisponível"
}
```

Validações:

* recurso atual vinculado;
* novo recurso disponível;
* compatibilidade;
* qualificações;
* período afetado;
* execução ativa tratada explicitamente.

Eventos resultantes:

```text
scheduling.resource_unassigned
scheduling.resource_assigned
scheduling.resource_replaced
```

---

## `ChangeResourceAllocationCommand`

Altera o percentual de alocação.

Permissão:

```text
scheduling.resource.allocation.change
```

Payload:

```json
{
  "schedule_resource_id": "uuid",
  "allocation_percentage": 50,
  "reason": "Recurso compartilhado com outra atividade"
}
```

Validações:

* percentual válido;
* capacidade suficiente;
* item permanece viável;
* conflitos recalculados.

Evento resultante:

```text
scheduling.resource_allocation_changed
```

---

## `ReserveScheduleResourceCommand`

Reserva recurso para um período.

Permissão:

```text
scheduling.resource.reserve
```

Payload:

```json
{
  "resource_type": "MACHINE",
  "resource_id": "uuid",
  "schedule_item_id": "uuid",
  "reserved_start_at": "datetime",
  "reserved_end_at": "datetime",
  "reservation_type": "EXCLUSIVE"
}
```

Tipos:

```text
EXCLUSIVE
SHARED
TENTATIVE
SOFT
```

Validações:

* período válido;
* recurso ativo;
* política de compartilhamento;
* conflitos;
* capacidade;
* idempotência.

Eventos possíveis:

```text
scheduling.resource_reserved
scheduling.resource_reservation_failed
```

---

## `ReleaseScheduleResourceCommand`

Libera reserva de recurso.

Permissão:

```text
scheduling.resource.release
```

Payload:

```json
{
  "schedule_resource_reservation_id": "uuid",
  "released_at": "datetime",
  "reason_code": "ITEM_CANCELLED"
}
```

Evento resultante:

```text
scheduling.resource_released
```

---

# 57. Calendários e disponibilidade

## `CreateAvailabilityCalendarCommand`

Cria calendário operacional.

Permissão:

```text
scheduling.calendar.create
```

Payload:

```json
{
  "code": "PRODUCTION_DEFAULT",
  "name": "Calendário padrão da produção",
  "timezone": "America/Sao_Paulo",
  "calendar_type": "WORKING",
  "scope_type": "TENANT",
  "scope_id": "uuid",
  "description": "Horário operacional padrão"
}
```

Tipos:

```text
WORKING
EMPLOYEE
TEAM
MACHINE
WORK_CENTER
BRANCH
SECTOR
DELIVERY
CUSTOM
```

Validações:

* código único;
* timezone válido;
* escopo válido;
* tipo coerente.

Evento resultante:

```text
scheduling.calendar_created
```

---

## `UpdateAvailabilityCalendarCommand`

Atualiza metadados do calendário.

Permissão:

```text
scheduling.calendar.update
```

Payload:

```json
{
  "availability_calendar_id": "uuid",
  "name": "Calendário industrial",
  "timezone": "America/Sao_Paulo",
  "description": "Descrição revisada"
}
```

Evento resultante:

```text
scheduling.calendar_updated
```

---

## `AddWorkingPeriodCommand`

Adiciona período recorrente de trabalho.

Permissão:

```text
scheduling.calendar.working_period.create
```

Payload:

```json
{
  "availability_calendar_id": "uuid",
  "day_of_week": "MONDAY",
  "start_time": "07:30:00",
  "end_time": "17:30:00",
  "break_periods": [
    {
      "start_time": "12:00:00",
      "end_time": "13:00:00"
    }
  ],
  "effective_from": "date",
  "effective_until": null
}
```

Validações:

* horário válido;
* intervalos sem sobreposição;
* início anterior ao fim;
* vigência coerente;
* impedir duplicidade incompatível.

Evento resultante:

```text
scheduling.calendar_working_period_added
```

---

## `UpdateWorkingPeriodCommand`

Atualiza período de trabalho.

Permissão:

```text
scheduling.calendar.working_period.update
```

Payload:

```json
{
  "working_period_id": "uuid",
  "start_time": "08:00:00",
  "end_time": "18:00:00",
  "break_periods": [],
  "effective_from": "date",
  "effective_until": null
}
```

Validações:

* período existente;
* agenda futura reavaliada;
* alterações não modificam histórico passado.

Evento resultante:

```text
scheduling.calendar_working_period_updated
```

---

## `RemoveWorkingPeriodCommand`

Remove período para datas futuras.

Permissão:

```text
scheduling.calendar.working_period.remove
```

Payload:

```json
{
  "working_period_id": "uuid",
  "effective_at": "date",
  "reason": "Alteração do turno"
}
```

Evento resultante:

```text
scheduling.calendar_working_period_removed
```

---

## `CreateCalendarExceptionCommand`

Cria exceção de disponibilidade.

Permissão:

```text
scheduling.calendar.exception.create
```

Payload:

```json
{
  "availability_calendar_id": "uuid",
  "exception_type": "UNAVAILABLE",
  "start_at": "datetime",
  "end_at": "datetime",
  "reason_code": "HOLIDAY",
  "reason": "Feriado municipal",
  "capacity_override": null
}
```

Tipos:

```text
AVAILABLE
UNAVAILABLE
REDUCED_CAPACITY
OVERTIME
MAINTENANCE_WINDOW
HOLIDAY
CUSTOM
```

Validações:

* intervalo válido;
* calendário correspondente;
* capacidade compatível;
* exceções sobrepostas tratadas;
* motivo obrigatório.

Evento resultante:

```text
scheduling.calendar_exception_created
```

---

## `UpdateCalendarExceptionCommand`

Atualiza exceção futura.

Permissão:

```text
scheduling.calendar.exception.update
```

Payload:

```json
{
  "calendar_exception_id": "uuid",
  "start_at": "datetime",
  "end_at": "datetime",
  "reason": "Data revisada",
  "capacity_override": "0.5000"
}
```

Evento resultante:

```text
scheduling.calendar_exception_updated
```

---

## `CancelCalendarExceptionCommand`

Cancela exceção.

Permissão:

```text
scheduling.calendar.exception.cancel
```

Payload:

```json
{
  "calendar_exception_id": "uuid",
  "reason": "Feriado cancelado"
}
```

Evento resultante:

```text
scheduling.calendar_exception_cancelled
```

---

## `BindCalendarToResourceCommand`

Vincula calendário a recurso.

Permissão:

```text
scheduling.calendar.bind
```

Payload:

```json
{
  "availability_calendar_id": "uuid",
  "resource_type": "MACHINE",
  "resource_id": "uuid",
  "priority": 10,
  "effective_from": "date"
}
```

Validações:

* calendário ativo;
* recurso válido;
* vínculo não duplicado;
* precedência coerente;
* mesmo Tenant.

Evento resultante:

```text
scheduling.calendar_bound
```

---

## `UnbindCalendarFromResourceCommand`

Remove vínculo.

Permissão:

```text
scheduling.calendar.unbind
```

Payload:

```json
{
  "calendar_binding_id": "uuid",
  "effective_at": "date",
  "reason": "Recurso seguirá outro calendário"
}
```

Evento resultante:

```text
scheduling.calendar_unbound
```

---

# 58. Turnos e capacidade

## `CreateShiftCommand`

Cria turno operacional.

Permissão:

```text
scheduling.shift.create
```

Payload:

```json
{
  "code": "SHIFT-DAY",
  "name": "Turno diurno",
  "start_time": "07:30:00",
  "end_time": "17:30:00",
  "crosses_midnight": false,
  "break_periods": [],
  "applicable_days": [
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY"
  ]
}
```

Evento resultante:

```text
scheduling.shift_created
```

---

## `UpdateShiftCommand`

Atualiza turno.

Permissão:

```text
scheduling.shift.update
```

Payload:

```json
{
  "shift_id": "uuid",
  "name": "Turno principal",
  "start_time": "08:00:00",
  "end_time": "18:00:00",
  "break_periods": []
}
```

Validações:

* turno ativo;
* horários válidos;
* agenda futura reavaliada;
* histórico preservado.

Evento resultante:

```text
scheduling.shift_updated
```

---

## `AssignEmployeeToShiftCommand`

Atribui funcionário a turno.

Permissão:

```text
scheduling.shift.employee.assign
```

Payload:

```json
{
  "shift_id": "uuid",
  "employee_id": "uuid",
  "effective_from": "date",
  "effective_until": null
}
```

Validações:

* funcionário ativo;
* turno válido;
* ausência de atribuições incompatíveis;
* vigência coerente.

Evento resultante:

```text
scheduling.employee_assigned_to_shift
```

---

## `RemoveEmployeeFromShiftCommand`

Remove atribuição de turno.

Permissão:

```text
scheduling.shift.employee.remove
```

Payload:

```json
{
  "shift_assignment_id": "uuid",
  "effective_at": "date",
  "reason": "Transferência de setor"
}
```

Evento resultante:

```text
scheduling.employee_removed_from_shift
```

---

## `SetResourceCapacityCommand`

Define capacidade nominal.

Permissão:

```text
scheduling.resource.capacity.set
```

Payload:

```json
{
  "resource_type": "WORK_CENTER",
  "resource_id": "uuid",
  "capacity_value": "4.0000",
  "capacity_unit": "SIMULTANEOUS_OPERATIONS",
  "effective_from": "date",
  "effective_until": null
}
```

Validações:

* capacidade positiva;
* unidade compatível;
* recurso válido;
* vigência coerente;
* histórico preservado.

Evento resultante:

```text
scheduling.resource_capacity_changed
```

---

## `OverrideResourceCapacityCommand`

Altera temporariamente a capacidade.

Permissão:

```text
scheduling.resource.capacity.override
```

Payload:

```json
{
  "resource_type": "WORK_CENTER",
  "resource_id": "uuid",
  "start_at": "datetime",
  "end_at": "datetime",
  "capacity_value": "2.0000",
  "reason_code": "EMPLOYEE_SHORTAGE",
  "reason": "Equipe reduzida"
}
```

Validações:

* período válido;
* capacidade não negativa;
* justificativa;
* conflitos futuros recalculados.

Evento resultante:

```text
scheduling.resource_capacity_overridden
```

---

# 59. Dependências e precedências

## `CreateScheduleDependencyCommand`

Cria dependência entre itens.

Permissão:

```text
scheduling.dependency.create
```

Payload:

```json
{
  "predecessor_schedule_item_id": "uuid",
  "successor_schedule_item_id": "uuid",
  "dependency_type": "FINISH_TO_START",
  "lag_minutes": 0,
  "is_mandatory": true
}
```

Tipos:

```text
FINISH_TO_START
START_TO_START
FINISH_TO_FINISH
START_TO_FINISH
```

Validações:

* itens distintos;
* mesmo Tenant;
* impedir ciclo;
* lag válido;
* dependência compatível com o fluxo.

Evento resultante:

```text
scheduling.dependency_created
```

---

## `UpdateScheduleDependencyCommand`

Atualiza dependência.

Permissão:

```text
scheduling.dependency.update
```

Payload:

```json
{
  "schedule_dependency_id": "uuid",
  "dependency_type": "FINISH_TO_START",
  "lag_minutes": 60,
  "is_mandatory": true
}
```

Validações:

* impedir ciclo;
* impacto no cronograma;
* itens não concluídos.

Evento resultante:

```text
scheduling.dependency_updated
```

---

## `RemoveScheduleDependencyCommand`

Remove dependência.

Permissão:

```text
scheduling.dependency.remove
```

Payload:

```json
{
  "schedule_dependency_id": "uuid",
  "reason": "Operações poderão ocorrer em paralelo"
}
```

Evento resultante:

```text
scheduling.dependency_removed
```

---

# 60. Conflitos de agenda

## `DetectScheduleConflictsCommand`

Solicita análise de conflitos.

Permissão:

```text
scheduling.conflict.detect
```

Payload:

```json
{
  "schedule_item_ids": [
    "uuid"
  ],
  "resource_ids": [],
  "period_start": "datetime",
  "period_end": "datetime",
  "include_soft_conflicts": true
}
```

Tipos de conflito:

```text
RESOURCE_OVERLAP
CAPACITY_EXCEEDED
UNAVAILABLE_PERIOD
DEPENDENCY_VIOLATION
QUALIFICATION_MISSING
MACHINE_BLOCKED
MAINTENANCE_CONFLICT
MATERIAL_UNAVAILABLE
LOCATION_CONFLICT
DUE_DATE_RISK
```

Evento resultante:

```text
scheduling.conflict_detected
```

A detecção poderá produzir projeção sem alterar itens.

---

## `AcknowledgeScheduleConflictCommand`

Registra ciência do conflito.

Permissão:

```text
scheduling.conflict.acknowledge
```

Payload:

```json
{
  "schedule_conflict_id": "uuid",
  "acknowledged_by_user_id": "uuid",
  "acknowledged_at": "datetime",
  "notes": "Conflito em avaliação"
}
```

Evento resultante:

```text
scheduling.conflict_acknowledged
```

---

## `ResolveScheduleConflictCommand`

Registra resolução.

Permissão:

```text
scheduling.conflict.resolve
```

Payload:

```json
{
  "schedule_conflict_id": "uuid",
  "resolution_code": "ITEM_RESCHEDULED",
  "resolution_reference_id": "uuid",
  "resolution_notes": "Operação reagendada",
  "resolved_at": "datetime"
}
```

Validações:

* conflito aberto;
* resolução verificável;
* itens envolvidos atualizados;
* não marcar resolvido sem correção quando conflito for bloqueante.

Evento resultante:

```text
scheduling.conflict_resolved
```

---

## `OverrideScheduleConflictCommand`

Autoriza conflito flexível.

Permissão:

```text
scheduling.conflict.override
```

Payload:

```json
{
  "schedule_conflict_id": "uuid",
  "reason_code": "MANAGED_RISK",
  "reason": "Recurso poderá atender parcialmente ambas as operações",
  "approved_by_user_id": "uuid",
  "expires_at": "datetime"
}
```

Validações:

* conflito classificável como flexível;
* alçada;
* prazo;
* justificativa;
* conflitos de segurança não podem ser ignorados;
* auditoria reforçada.

Evento resultante:

```text
scheduling.conflict_overridden
```

---

# 61. Planejamento automático

## `GenerateScheduleCommand`

Gera proposta de agenda.

Permissão:

```text
scheduling.plan.generate
```

Payload:

```json
{
  "reference_type": "PRODUCTION_ORDER",
  "reference_ids": [
    "uuid"
  ],
  "planning_horizon_start": "datetime",
  "planning_horizon_end": "datetime",
  "strategy": "CAPACITY_BALANCED",
  "constraints": {
    "respect_due_dates": true,
    "respect_material_availability": true,
    "respect_machine_availability": true,
    "respect_employee_skills": true
  },
  "simulation_only": true
}
```

Validações:

* horizonte válido;
* referências existentes;
* calendários;
* capacidades;
* dependências;
* dados suficientes;
* simulação não altera agenda oficial.

Eventos possíveis:

```text
scheduling.plan_generated
scheduling.plan_generation_failed
```

---

## `ApplyGeneratedScheduleCommand`

Aplica proposta gerada.

Permissão:

```text
scheduling.plan.apply
```

Payload:

```json
{
  "schedule_plan_id": "uuid",
  "selected_schedule_item_ids": [
    "uuid"
  ],
  "apply_mode": "REPLACE_PLANNED_ITEMS",
  "reason": "Plano aprovado pelo PCP"
}
```

Modos:

```text
CREATE_ONLY
REPLACE_PLANNED_ITEMS
MERGE
PARTIAL
```

Validações:

* plano ainda válido;
* dados-base não alterados de forma incompatível;
* conflitos reavaliados;
* itens em execução preservados;
* aprovação quando exigida;
* auditoria.

Eventos resultantes:

```text
scheduling.plan_applied
scheduling.item_scheduled
scheduling.item_rescheduled
```

---

## `CancelGeneratedScheduleCommand`

Descarta proposta.

Permissão:

```text
scheduling.plan.cancel
```

Payload:

```json
{
  "schedule_plan_id": "uuid",
  "reason": "Premissas alteradas"
}
```

Evento resultante:

```text
scheduling.plan_cancelled
```

---

# 62. Integrações de Scheduling

## Eventos consumidos

Scheduling deverá consumir inicialmente:

```text
production.order_created
production.operation_created
production.operation_assigned
production.execution_started
production.execution_paused
production.execution_resumed
production.execution_finished
production.order_cancelled
maintenance.machine_unavailable
maintenance.machine_released
maintenance.order_created
quality.rework_required
quality.nonconformity_created
inventory.stock_reservation_failed
purchasing.purchase_order_delivery_rescheduled
organization.employee_transferred
organization.employee_terminated
```

---

## Reação a `production.operation_created`

Poderá gerar:

```text
CreateScheduleItemCommand
```

quando a política de planejamento automático estiver habilitada.

---

## Reação a `production.execution_started`

Deverá atualizar o item correspondente por:

```text
StartScheduleItemCommand
```

sem transformar Scheduling em proprietário da execução.

---

## Reação a `maintenance.machine_unavailable`

Deverá:

* identificar itens futuros;
* registrar conflitos;
* propor reagendamento;
* bloquear novas reservas;
* notificar PCP.

---

## Reação a `quality.rework_required`

Poderá criar novo item de agenda para a operação de retrabalho.

---

## Reação a `organization.employee_terminated`

Deverá identificar:

* itens atribuídos;
* reservas futuras;
* conflitos de capacidade;
* necessidade de substituição.

---

# 63. Regras de integridade de Scheduling

## 63.1 Agenda não é execução

Scheduling representa intenção e alocação temporal.

Production e Maintenance representam a execução real.

A agenda não poderá declarar trabalho concluído sem referência ao contexto proprietário.

---

## 63.2 Planejado e realizado são distintos

Preservar:

```text
planned_start_at
planned_end_at
actual_start_at
actual_end_at
```

Reagendamentos não devem sobrescrever o histórico anterior.

---

## 63.3 Recursos opcionais

A empresa poderá planejar:

* sem máquinas;
* sem filiais;
* sem setores;
* somente por funcionário;
* somente por equipe;
* somente por etapa;
* por capacidade agregada.

O modelo não deverá exigir todos os recursos.

---

## 63.4 Conflitos duros e flexíveis

Conflitos duros:

* equipamento bloqueado;
* recurso inexistente;
* intervalo inválido;
* dependência obrigatória;
* regra de segurança;
* capacidade zero.

Conflitos flexíveis:

* sobrecarga permitida;
* atraso provável;
* recurso compartilhado;
* preferência de turno;
* prioridade concorrente.

---

## 63.5 Replanejamento

Reagendar um item poderá afetar:

* sucessores;
* entregas;
* máquinas;
* pessoas;
* inspeções;
* manutenção;
* materiais;
* prazo do cliente.

O impacto deverá ser apresentado antes da confirmação quando relevante.

---

## 63.6 Drag and drop

Interfaces não deverão depender de drag and drop para editar a agenda.

A alteração deverá ocorrer por comando explícito, inclusive quando a interface oferecer interação visual.

---

## 63.7 Itens simultâneos

Atividades simultâneas deverão ser representadas lado a lado nas interfaces, sem sobreposição visual que impeça leitura.

Essa regra pertence ao design da interface, não ao domínio.

---

## 63.8 Offline

Comandos offline deverão preservar:

```text
command_id
idempotency_key
device_id
schedule_item_id
occurred_at
expected_entity_version
```

Conflitos serão resolvidos no servidor.

---

# 64. Eventos resultantes de Scheduling

Eventos principais:

```text
scheduling.item_created
scheduling.item_updated
scheduling.item_scheduled
scheduling.item_rescheduled
scheduling.item_started
scheduling.item_paused
scheduling.item_resumed
scheduling.item_completed
scheduling.item_cancelled
scheduling.resource_assigned
scheduling.resource_unassigned
scheduling.resource_reserved
scheduling.resource_released
scheduling.calendar_created
scheduling.calendar_exception_created
scheduling.shift_created
scheduling.employee_assigned_to_shift
scheduling.resource_capacity_changed
scheduling.dependency_created
scheduling.conflict_detected
scheduling.conflict_resolved
scheduling.conflict_overridden
scheduling.plan_generated
scheduling.plan_applied
```

Consumidores principais:

* Production;
* Maintenance;
* Organization;
* Quality;
* Notifications;
* Timeline;
* Analytics;
* Automation.

---

# 65. Comandos de Incidents

## `CreateIncidentCommand`

Cria uma ocorrência operacional.

Permissão:

```text
incident.create
```

Payload:

```json
{
  "incident_type": "MATERIAL_SHORTAGE",
  "category": "PRODUCTION",
  "severity": "HIGH",
  "title": "Falta de material",
  "description": "Não há fundo de MDF disponível para continuar",
  "workflow_instance_id": "uuid",
  "production_order_id": "uuid",
  "operation_instance_id": "uuid",
  "execution_id": "uuid",
  "machine_id": null,
  "material_id": "uuid",
  "supplier_id": null,
  "branch_id": "uuid",
  "sector_id": "uuid",
  "reported_by_user_id": "uuid",
  "reported_by_employee_id": "uuid",
  "reported_at": "datetime",
  "requires_immediate_action": true,
  "metadata": {}
}
```

Tipos iniciais:

```text
MATERIAL_SHORTAGE
DAMAGED_PART
MACHINE_FAILURE
DESIGN_ERROR
MANUFACTURING_ERROR
QUALITY_ISSUE
SAFETY_RISK
DOCUMENT_MISSING
CUSTOMER_ISSUE
SUPPLIER_DELAY
DELIVERY_PROBLEM
SYSTEM_FAILURE
PROCESS_BLOCKAGE
OTHER
```

Validações:

* título e descrição;
* severidade válida;
* referências pertencentes ao mesmo Tenant;
* origem coerente;
* ator autorizado;
* impedir duplicidade evidente quando configurado;
* idempotência obrigatória em PWA;
* ocorrências críticas exigem notificação imediata.

Evento resultante:

```text
incident.created
```

---

## `UpdateIncidentCommand`

Atualiza dados classificatórios enquanto a ocorrência estiver aberta.

Permissão:

```text
incident.update
```

Payload:

```json
{
  "incident_id": "uuid",
  "title": "Falta de MDF Branco 6 mm",
  "description": "Descrição revisada",
  "category": "INVENTORY",
  "severity": "CRITICAL",
  "requires_immediate_action": true,
  "metadata": {}
}
```

Validações:

* ocorrência aberta;
* preservar descrição original;
* aumento ou redução de severidade auditado;
* referências estruturais não removidas indevidamente;
* concorrência otimista.

Evento resultante:

```text
incident.updated
```

---

## `ClassifyIncidentCommand`

Classifica tecnicamente a ocorrência.

Permissão:

```text
incident.classify
```

Payload:

```json
{
  "incident_id": "uuid",
  "incident_type": "MATERIAL_SHORTAGE",
  "category": "INVENTORY",
  "severity": "HIGH",
  "impact": "PRODUCTION_STOPPED",
  "urgency": "IMMEDIATE",
  "classification_notes": "Produção bloqueada"
}
```

Impactos iniciais:

```text
NO_IMMEDIATE_IMPACT
DELAY_RISK
PARTIAL_BLOCKAGE
PRODUCTION_STOPPED
QUALITY_RISK
SAFETY_RISK
FINANCIAL_IMPACT
CUSTOMER_IMPACT
LEGAL_OR_FISCAL_RISK
```

Evento resultante:

```text
incident.classified
```

---

## `AssignIncidentCommand`

Atribui a ocorrência.

Permissão:

```text
incident.assign
```

Payload:

```json
{
  "incident_id": "uuid",
  "assigned_user_id": "uuid",
  "assigned_employee_id": "uuid",
  "assigned_sector_id": "uuid",
  "assigned_role_code": "INVENTORY_MANAGER",
  "due_at": "datetime",
  "assignment_notes": "Verificar estoque e compra"
}
```

Validações:

* ocorrência aberta;
* responsável ativo;
* pelo menos um destinatário;
* prazo coerente;
* escopo compatível.

Evento resultante:

```text
incident.assigned
```

---

## `UnassignIncidentCommand`

Remove atribuição.

Permissão:

```text
incident.unassign
```

Payload:

```json
{
  "incident_id": "uuid",
  "incident_assignment_id": "uuid",
  "reason": "Responsável substituído"
}
```

Validações:

* ocorrência aberta;
* manter responsável quando obrigatório;
* justificativa.

Evento resultante:

```text
incident.unassigned
```

---

## `AcknowledgeIncidentCommand`

Registra ciência da ocorrência.

Permissão:

```text
incident.acknowledge
```

Payload:

```json
{
  "incident_id": "uuid",
  "acknowledged_by_user_id": "uuid",
  "acknowledged_by_employee_id": "uuid",
  "acknowledged_at": "datetime",
  "notes": "Estoque verificando disponibilidade"
}
```

Validações:

* ocorrência aberta;
* responsável ou ator autorizado;
* impedir confirmação duplicada do mesmo destinatário quando não necessária.

Evento resultante:

```text
incident.acknowledged
```

---

## `AddIncidentResponseCommand`

Adiciona resposta ou atualização.

Permissão:

```text
incident.response.create
```

Payload:

```json
{
  "incident_id": "uuid",
  "response_type": "STATUS_UPDATE",
  "message": "Material não disponível. Compra solicitada.",
  "responded_by_user_id": "uuid",
  "responded_by_employee_id": "uuid",
  "responded_at": "datetime",
  "visibility": "INTERNAL"
}
```

Tipos:

```text
STATUS_UPDATE
ACTION_TAKEN
REQUEST_FOR_INFORMATION
INFORMATION_PROVIDED
ESTIMATED_RESOLUTION
CUSTOMER_RESPONSE
SUPPLIER_RESPONSE
MANAGEMENT_DECISION
```

Visibilidades:

```text
INTERNAL
REPORTER_AND_ASSIGNEES
TENANT_AUTHORIZED
CUSTOMER_VISIBLE
SUPPLIER_VISIBLE
```

Validações:

* ocorrência existente;
* ator autorizado;
* mensagem não vazia;
* visibilidade permitida;
* dados sensíveis tratados.

Evento resultante:

```text
incident.responded
```

---

## `AttachIncidentEvidenceCommand`

Vincula evidência.

Permissão:

```text
incident.evidence.attach
```

Payload:

```json
{
  "incident_id": "uuid",
  "document_id": "uuid",
  "evidence_type": "PHOTO",
  "description": "Foto da peça danificada"
}
```

Validações:

* documento acessível;
* mesmo Tenant;
* vínculo não duplicado;
* tipo permitido.

Evento resultante:

```text
incident.evidence_attached
```

---

## `RemoveIncidentEvidenceCommand`

Remove vínculo incorreto.

Permissão:

```text
incident.evidence.remove
```

Payload:

```json
{
  "incident_id": "uuid",
  "incident_evidence_id": "uuid",
  "reason": "Documento vinculado incorretamente"
}
```

Validações:

* não apagar documento;
* preservar auditoria;
* evidência não obrigatória ou substituída.

Evento resultante:

```text
incident.evidence_removed
```

---

## `EscalateIncidentCommand`

Escala uma ocorrência.

Permissão:

```text
incident.escalate
```

Payload:

```json
{
  "incident_id": "uuid",
  "new_severity": "CRITICAL",
  "target_user_id": "uuid",
  "target_role_code": "PRODUCTION_MANAGER",
  "target_sector_id": "uuid",
  "reason_code": "SLA_BREACH",
  "reason": "Produção permanece bloqueada",
  "escalated_at": "datetime"
}
```

Validações:

* ocorrência aberta;
* nova severidade igual ou superior;
* alvo válido;
* motivo obrigatório;
* regras de escalonamento;
* evitar ciclos de escalonamento.

Evento resultante:

```text
incident.escalated
```

---

## `DeescalateIncidentCommand`

Reduz o nível de escalonamento.

Permissão:

```text
incident.deescalate
```

Payload:

```json
{
  "incident_id": "uuid",
  "new_severity": "MEDIUM",
  "reason": "Produção retomada parcialmente"
}
```

Validações:

* ocorrência aberta;
* justificativa;
* risco reavaliado;
* severidade crítica de segurança exige autorização especial.

Evento resultante:

```text
incident.deescalated
```

---

## `LinkIncidentCommand`

Vincula uma ocorrência a outra entidade.

Permissão:

```text
incident.link
```

Payload:

```json
{
  "incident_id": "uuid",
  "entity_type": "PURCHASE_REQUEST",
  "entity_id": "uuid",
  "relationship_type": "RESOLUTION_ACTION"
}
```

Validações:

* entidade válida;
* mesmo Tenant;
* relação não duplicada;
* ator possui acesso às duas entidades.

Evento resultante:

```text
incident.link_created
```

---

## `UnlinkIncidentCommand`

Remove vínculo.

Permissão:

```text
incident.unlink
```

Payload:

```json
{
  "incident_link_id": "uuid",
  "reason": "Vínculo criado incorretamente"
}
```

Evento resultante:

```text
incident.link_removed
```

---

## `MergeIncidentsCommand`

Consolida ocorrências duplicadas.

Permissão:

```text
incident.merge
```

Payload:

```json
{
  "source_incident_ids": [
    "uuid",
    "uuid"
  ],
  "target_incident_id": "uuid",
  "reason": "Ocorrências relativas ao mesmo problema"
}
```

Validações:

* mesmo Tenant;
* incidentes compatíveis;
* destino aberto;
* preservar respostas, evidências e vínculos;
* origens marcadas como consolidadas;
* operação auditada.

Eventos resultantes:

```text
incident.merged
incident.cancelled
```

---

## `SplitIncidentCommand`

Divide uma ocorrência com causas independentes.

Permissão:

```text
incident.split
```

Payload:

```json
{
  "incident_id": "uuid",
  "new_incidents": [
    {
      "incident_type": "MATERIAL_SHORTAGE",
      "title": "Falta de material",
      "description": "Descrição"
    },
    {
      "incident_type": "MACHINE_FAILURE",
      "title": "Falha de máquina",
      "description": "Descrição"
    }
  ],
  "reason": "Foram identificadas causas independentes"
}
```

Validações:

* ocorrência aberta;
* dados mínimos;
* vínculos distribuídos explicitamente;
* origem preservada;
* evitar duplicidade.

Eventos resultantes:

```text
incident.split
incident.created
```

---

## `ResolveIncidentCommand`

Resolve a ocorrência.

Permissão:

```text
incident.resolve
```

Payload:

```json
{
  "incident_id": "uuid",
  "resolution_code": "MATERIAL_PROVIDED",
  "resolution": "Material entregue ao setor",
  "resolved_by_user_id": "uuid",
  "resolved_by_employee_id": "uuid",
  "resolved_at": "datetime",
  "resolution_reference_type": "PURCHASE_RECEIPT",
  "resolution_reference_id": "uuid",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* ocorrência aberta;
* ação resolutiva concluída;
* pendências bloqueantes encerradas;
* referência válida quando exigida;
* evidência conforme severidade;
* responsável autorizado;
* não alterar entidade de origem diretamente.

Evento resultante:

```text
incident.resolved
```

---

## `CloseIncidentCommand`

Encerra a ocorrência após validação da resolução.

Permissão:

```text
incident.close
```

Payload:

```json
{
  "incident_id": "uuid",
  "closed_at": "datetime",
  "closure_notes": "Resolução confirmada pelo solicitante",
  "confirmed_by_user_id": "uuid"
}
```

Validações:

* ocorrência resolvida;
* confirmação quando exigida;
* nenhuma pendência;
* SLA calculado;
* avaliação de reincidência.

Evento resultante:

```text
incident.closed
```

---

## `ReopenIncidentCommand`

Reabre ocorrência.

Permissão:

```text
incident.reopen
```

Payload:

```json
{
  "incident_id": "uuid",
  "reason_code": "PROBLEM_RECURRED",
  "reason": "Problema voltou a ocorrer",
  "reopened_at": "datetime"
}
```

Validações:

* ocorrência resolvida ou fechada;
* preservar resolução anterior;
* registrar reincidência;
* severidade reavaliada.

Evento resultante:

```text
incident.reopened
```

---

## `CancelIncidentCommand`

Cancela ocorrência criada indevidamente.

Permissão:

```text
incident.cancel
```

Payload:

```json
{
  "incident_id": "uuid",
  "reason_code": "DUPLICATE",
  "reason": "Ocorrência duplicada",
  "replacement_incident_id": "uuid"
}
```

Validações:

* não ocultar efeitos relevantes;
* registro substituto quando duplicado;
* histórico preservado;
* permissão administrativa quando houver ações realizadas.

Evento resultante:

```text
incident.cancelled
```

---

# 66. Ações derivadas de Incidents

## `CreateIncidentActionCommand`

Cria uma ação para tratamento.

Permissão:

```text
incident.action.create
```

Payload:

```json
{
  "incident_id": "uuid",
  "action_type": "CHECK_INVENTORY",
  "title": "Verificar estoque",
  "description": "Conferir estoque físico e reservas",
  "assigned_user_id": "uuid",
  "assigned_employee_id": "uuid",
  "assigned_sector_id": "uuid",
  "due_at": "datetime",
  "priority": "HIGH"
}
```

Evento resultante:

```text
incident.action_created
```

---

## `StartIncidentActionCommand`

Inicia ação.

Permissão:

```text
incident.action.start
```

Payload:

```json
{
  "incident_action_id": "uuid",
  "started_at": "datetime"
}
```

Evento resultante:

```text
incident.action_started
```

---

## `CompleteIncidentActionCommand`

Conclui ação.

Permissão:

```text
incident.action.complete
```

Payload:

```json
{
  "incident_action_id": "uuid",
  "completed_at": "datetime",
  "completion_notes": "Estoque conferido",
  "result_data": {},
  "evidence_document_ids": []
}
```

Validações:

* ação aberta;
* responsável autorizado;
* resultado obrigatório conforme tipo;
* evidências quando exigidas.

Evento resultante:

```text
incident.action_completed
```

---

## `CancelIncidentActionCommand`

Cancela ação.

Permissão:

```text
incident.action.cancel
```

Payload:

```json
{
  "incident_action_id": "uuid",
  "reason": "Ação não será mais necessária"
}
```

Evento resultante:

```text
incident.action_cancelled
```

---

# 67. SLA e escalonamento

## `SetIncidentSlaCommand`

Define SLA aplicável.

Permissão:

```text
incident.sla.set
```

Payload:

```json
{
  "incident_id": "uuid",
  "acknowledgement_due_at": "datetime",
  "response_due_at": "datetime",
  "resolution_due_at": "datetime",
  "sla_policy_id": "uuid"
}
```

Validações:

* datas coerentes;
* política válida;
* ocorrência aberta;
* não reduzir prazos vencidos sem autorização.

Evento resultante:

```text
incident.sla_set
```

---

## `PauseIncidentSlaCommand`

Pausa contagem quando permitido.

Permissão:

```text
incident.sla.pause
```

Payload:

```json
{
  "incident_id": "uuid",
  "reason_code": "WAITING_EXTERNAL_PARTY",
  "reason": "Aguardando retorno do fornecedor",
  "paused_at": "datetime"
}
```

Validações:

* política permite;
* ocorrência aberta;
* nenhuma pausa de SLA ativa;
* justificativa.

Evento resultante:

```text
incident.sla_paused
```

---

## `ResumeIncidentSlaCommand`

Retoma SLA.

Permissão:

```text
incident.sla.resume
```

Payload:

```json
{
  "incident_id": "uuid",
  "sla_pause_id": "uuid",
  "resumed_at": "datetime",
  "reason": "Fornecedor respondeu"
}
```

Evento resultante:

```text
incident.sla_resumed
```

---

## `RegisterIncidentSlaBreachCommand`

Registra violação de SLA.

Permissão:

```text
incident.sla_breach.register
```

Payload:

```json
{
  "incident_id": "uuid",
  "breach_type": "RESOLUTION",
  "breached_at": "datetime",
  "automatic_escalation": true
}
```

Tipos:

```text
ACKNOWLEDGEMENT
RESPONSE
RESOLUTION
```

Eventos resultantes:

```text
incident.sla_breached
incident.escalated
```

---

# 68. Integrações de Incidents

## Eventos consumidos

Incidents poderá consumir:

```text
production.execution_paused
production.material_requested
production.machine_incident_reported
inventory.stock_reservation_failed
purchasing.purchase_order_delivery_rescheduled
quality.nonconformity_created
maintenance.machine_unavailable
scheduling.conflict_detected
system.background_job_failed
sync.conflict_detected
```

---

## Reação a `production.execution_paused`

Poderá criar ocorrência quando:

* motivo for bloqueante;
* duração exceder limite;
* categoria exigir ação externa;
* produção estiver parada.

---

## Reação a `inventory.stock_reservation_failed`

Poderá criar ou atualizar incidente de falta de material, evitando duplicidade por:

```text
production_order_id
operation_instance_id
material_id
open_status
```

---

## Reação a `maintenance.machine_unavailable`

Poderá criar incidente operacional quando houver impacto em produção.

---

## Reação a `scheduling.conflict_detected`

Somente conflitos críticos ou não resolvidos deverão virar ocorrência.

---

# 69. Regras de integridade de Incidents

## 69.1 Ocorrência não substitui o domínio de origem

Incidents coordena o tratamento.

Ele não deve:

* movimentar estoque;
* criar compra diretamente;
* reparar máquina;
* concluir produção;
* alterar qualidade;
* reagendar operação diretamente.

As ações devem utilizar comandos dos contextos proprietários.

---

## 69.2 Ocorrência e não conformidade

Uma ocorrência pode gerar uma não conformidade.

Nem toda ocorrência é uma não conformidade.

Exemplos de ocorrência sem não conformidade:

* atraso de fornecedor;
* ausência de funcionário;
* documento pendente;
* indisponibilidade externa.

---

## 69.3 Estado e resolução

Estados iniciais:

```text
OPEN
ACKNOWLEDGED
IN_ANALYSIS
ACTION_REQUIRED
WAITING
RESOLVED
CLOSED
CANCELLED
```

Resolver indica que a ação foi concluída.

Fechar indica que a resolução foi validada e o registro encerrado.

---

## 69.4 Severidade e prioridade

Severidade representa impacto.

Prioridade representa ordem de atendimento.

Uma ocorrência de alta severidade poderá ter prioridade ajustada conforme contexto, mas as duas informações não devem ser confundidas.

---

## 69.5 Histórico

Preservar:

* descrição original;
* classificações;
* atribuições;
* respostas;
* evidências;
* escalonamentos;
* ações;
* SLA;
* resolução;
* reaberturas.

---

## 69.6 Visibilidade

Ocorrências poderão conter dados restritos.

A visibilidade deverá considerar:

* Tenant;
* filial;
* setor;
* equipe;
* responsáveis;
* papéis;
* tipo de ocorrência;
* dados pessoais;
* segurança;
* cliente ou fornecedor.

---

## 69.7 Offline

Comandos offline deverão preservar:

```text
command_id
idempotency_key
device_id
incident_id
occurred_at
expected_entity_version
local_evidence_references
```

Uploads poderão ser sincronizados posteriormente sem perder o vínculo com o comando original.

---

# 70. Eventos resultantes de Incidents

Eventos principais:

```text
incident.created
incident.updated
incident.classified
incident.assigned
incident.unassigned
incident.acknowledged
incident.responded
incident.evidence_attached
incident.escalated
incident.deescalated
incident.link_created
incident.merged
incident.split
incident.resolved
incident.closed
incident.reopened
incident.cancelled
incident.action_created
incident.action_started
incident.action_completed
incident.sla_set
incident.sla_paused
incident.sla_resumed
incident.sla_breached
```

Consumidores principais:

* Production;
* Inventory;
* Purchasing;
* Quality;
* Maintenance;
* Scheduling;
* Notifications;
* Timeline;
* Analytics;
* Automation;
* AI.

---

# 71. Continuação

A próxima subparte continuará com:

```text
Notifications
Financial
```

Fim da Parte 3D.
# 72. Comandos de Notifications

## `CreateNotificationCommand`

Cria uma notificação interna.

Permissão:

```text
notifications.notification.create
```

Payload:

```json
{
  "notification_type": "MATERIAL_SHORTAGE",
  "title": "Material indisponível",
  "message": "O material MDF Branco TX 15 mm não está disponível.",
  "severity": "HIGH",
  "priority": "HIGH",
  "source_type": "INCIDENT",
  "source_id": "uuid",
  "reference_type": "PRODUCTION_ORDER",
  "reference_id": "uuid",
  "recipient_strategy": "EXPLICIT",
  "recipients": [
    {
      "recipient_type": "USER",
      "recipient_id": "uuid"
    }
  ],
  "channels": [
    "IN_APP"
  ],
  "action": {
    "action_type": "OPEN_ENTITY",
    "entity_type": "INCIDENT",
    "entity_id": "uuid"
  },
  "expires_at": null,
  "metadata": {}
}
```

Tipos iniciais:

```text
INFORMATION
ACTION_REQUIRED
APPROVAL_REQUIRED
ASSIGNMENT
REMINDER
WARNING
INCIDENT
MATERIAL_SHORTAGE
QUALITY_ALERT
MAINTENANCE_ALERT
FINANCIAL_ALERT
SECURITY_ALERT
SYSTEM_ALERT
CUSTOM
```

Severidades:

```text
INFO
LOW
NORMAL
HIGH
CRITICAL
```

Prioridades:

```text
LOW
NORMAL
HIGH
URGENT
```

Estratégias de destinatário:

```text
EXPLICIT
ROLE
SECTOR
BRANCH
ASSIGNED_USERS
ENTITY_RESPONSIBLES
MANAGERS
ADMINISTRATORS
EVENT_POLICY
CUSTOM
```

Validações:

* título e mensagem válidos;
* pelo menos um destinatário resolvível;
* canais habilitados;
* referência pertencente ao mesmo Tenant;
* origem válida;
* severidade e prioridade suportadas;
* não incluir informações sensíveis sem autorização;
* política de visibilidade aplicável;
* idempotência obrigatória quando criada por evento ou automação;
* impedir duplicidade dentro da janela configurada.

Evento resultante:

```text
notifications.notification_created
```

---

## `CreateNotificationFromEventCommand`

Cria notificação a partir de um evento oficial.

Permissão:

```text
notifications.notification.create_from_event
```

Payload:

```json
{
  "source_event_id": "uuid",
  "notification_policy_id": "uuid",
  "template_id": "uuid",
  "template_version_id": "uuid",
  "recipient_context": {
    "branch_id": "uuid",
    "sector_id": "uuid",
    "assigned_user_ids": [
      "uuid"
    ]
  },
  "variables": {
    "material_name": "MDF Branco TX 15 mm",
    "production_order_code": "OP-000001"
  }
}
```

Validações:

* evento existente;
* evento pertencente ao Tenant;
* política ativa;
* template publicado;
* versão compatível;
* variáveis obrigatórias disponíveis;
* destinatários autorizados;
* evento ainda não processado pela mesma política;
* idempotência por `source_event_id + notification_policy_id`.

Eventos possíveis:

```text
notifications.notification_created
notifications.notification_suppressed
```

---

## `CreateBulkNotificationCommand`

Cria notificações para múltiplos destinatários.

Permissão:

```text
notifications.notification.bulk_create
```

Payload:

```json
{
  "notification_type": "SYSTEM_ALERT",
  "title": "Atualização programada",
  "message": "O sistema ficará indisponível para manutenção.",
  "severity": "INFO",
  "priority": "NORMAL",
  "recipient_strategy": "ROLE",
  "recipient_filters": {
    "role_codes": [
      "ADMIN"
    ],
    "branch_ids": [],
    "sector_ids": []
  },
  "channels": [
    "IN_APP",
    "EMAIL"
  ],
  "scheduled_at": "datetime",
  "expires_at": "datetime",
  "metadata": {}
}
```

Validações:

* ator autorizado para comunicação em massa;
* filtros válidos;
* destinatários limitados ao Tenant;
* canais permitidos;
* conteúdo não sensível;
* volume dentro dos limites;
* agendamento válido;
* respeitar preferências quando a comunicação não for obrigatória;
* idempotência.

Evento resultante:

```text
notifications.bulk_notification_created
```

---

## `UpdateNotificationCommand`

Atualiza uma notificação ainda não enviada.

Permissão:

```text
notifications.notification.update
```

Payload:

```json
{
  "notification_id": "uuid",
  "title": "Título revisado",
  "message": "Mensagem revisada",
  "priority": "HIGH",
  "expires_at": "datetime",
  "action": {}
}
```

Validações:

* notificação em rascunho ou agendada;
* nenhuma entrega iniciada;
* alteração autorizada;
* conteúdo e ação válidos;
* concorrência otimista.

Evento resultante:

```text
notifications.notification_updated
```

---

## `CancelNotificationCommand`

Cancela uma notificação ainda não entregue.

Permissão:

```text
notifications.notification.cancel
```

Payload:

```json
{
  "notification_id": "uuid",
  "reason_code": "CREATED_BY_MISTAKE",
  "reason": "Notificação criada com informações incorretas"
}
```

Validações:

* notificação cancelável;
* entregas já concluídas não são apagadas;
* tentativas pendentes são interrompidas;
* histórico preservado;
* justificativa obrigatória.

Evento resultante:

```text
notifications.notification_cancelled
```

---

## `ArchiveNotificationCommand`

Arquiva uma notificação interna.

Permissão:

```text
notifications.notification.archive
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "archived_at": "datetime"
}
```

Validações:

* usuário é destinatário ou administrador autorizado;
* arquivamento não remove histórico de entrega;
* não alterar o estado para outros destinatários.

Evento resultante:

```text
notifications.notification_archived
```

---

## `RestoreNotificationCommand`

Restaura uma notificação arquivada.

Permissão:

```text
notifications.notification.restore
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "restored_at": "datetime"
}
```

Evento resultante:

```text
notifications.notification_restored
```

---

# 73. Destinatários

## `AddNotificationRecipientCommand`

Adiciona destinatário antes do envio.

Permissão:

```text
notifications.recipient.add
```

Payload:

```json
{
  "notification_id": "uuid",
  "recipient_type": "USER",
  "recipient_id": "uuid",
  "channels": [
    "IN_APP",
    "PUSH"
  ]
}
```

Tipos:

```text
USER
MEMBERSHIP
EMPLOYEE
ROLE
SECTOR
BRANCH
TEAM
EXTERNAL_CONTACT
CUSTOM
```

Validações:

* notificação ainda não finalizada;
* destinatário válido;
* mesmo Tenant;
* canais compatíveis;
* impedir duplicidade;
* autorização de visibilidade.

Evento resultante:

```text
notifications.recipient_added
```

---

## `RemoveNotificationRecipientCommand`

Remove destinatário antes do envio.

Permissão:

```text
notifications.recipient.remove
```

Payload:

```json
{
  "notification_id": "uuid",
  "notification_recipient_id": "uuid",
  "reason": "Destinatário incluído incorretamente"
}
```

Validações:

* entrega ainda não iniciada para o destinatário;
* preservar histórico;
* notificação continua com destinatários válidos.

Evento resultante:

```text
notifications.recipient_removed
```

---

## `ResolveNotificationRecipientsCommand`

Resolve destinatários dinâmicos.

Permissão:

```text
notifications.recipient.resolve
```

Payload:

```json
{
  "notification_id": "uuid",
  "recipient_strategy": "ENTITY_RESPONSIBLES",
  "context": {
    "entity_type": "PRODUCTION_ORDER",
    "entity_id": "uuid"
  }
}
```

Validações:

* estratégia válida;
* entidade acessível;
* escopo de Tenant;
* usuários ativos;
* Membership ativo;
* respeitar permissões;
* impedir destinatários duplicados.

Evento resultante:

```text
notifications.recipients_resolved
```

---

## `ReplaceNotificationRecipientCommand`

Substitui destinatário ainda não notificado.

Permissão:

```text
notifications.recipient.replace
```

Payload:

```json
{
  "notification_recipient_id": "uuid",
  "new_recipient_type": "USER",
  "new_recipient_id": "uuid",
  "reason": "Responsável alterado"
}
```

Validações:

* destinatário original ainda não entregue;
* novo destinatário válido;
* mesmo Tenant;
* histórico da substituição preservado.

Evento resultante:

```text
notifications.recipient_replaced
```

---

# 74. Entrega de notificações

## `QueueNotificationDeliveryCommand`

Enfileira a entrega.

Permissão:

```text
notifications.delivery.queue
```

Payload:

```json
{
  "notification_id": "uuid",
  "recipient_id": "uuid",
  "channel": "PUSH",
  "scheduled_at": "datetime",
  "delivery_policy": {
    "max_attempts": 5,
    "retry_strategy": "EXPONENTIAL"
  }
}
```

Canais:

```text
IN_APP
PUSH
DESKTOP
EMAIL
WHATSAPP
SMS
WEBHOOK
CUSTOM
```

Validações:

* notificação ativa;
* destinatário válido;
* canal habilitado;
* endereço ou token disponível;
* preferências avaliadas;
* comunicação obrigatória pode ignorar opt-out apenas quando permitido;
* não duplicar entrega;
* idempotência obrigatória.

Evento resultante:

```text
notifications.delivery_queued
```

---

## `SendNotificationCommand`

Executa tentativa de envio.

Permissão:

```text
notifications.delivery.send
```

Payload:

```json
{
  "delivery_id": "uuid",
  "attempt_number": 1,
  "provider": "PUSH_PROVIDER",
  "sent_at": "datetime"
}
```

Validações:

* entrega enfileirada;
* tentativa dentro do limite;
* provedor disponível;
* credencial válida;
* destinatário ainda elegível;
* notificação não cancelada;
* mensagem renderizada;
* idempotência por `delivery_id + attempt_number`.

Eventos possíveis:

```text
notifications.notification_sent
notifications.notification_failed
```

---

## `ConfirmNotificationDeliveryCommand`

Registra confirmação de entrega pelo provedor.

Permissão:

```text
notifications.delivery.confirm
```

Payload:

```json
{
  "delivery_id": "uuid",
  "provider_message_id": "string",
  "delivered_at": "datetime",
  "provider_status": "DELIVERED",
  "metadata": {}
}
```

Validações:

* entrega existente;
* confirmação compatível;
* impedir duplicidade;
* assinatura do provedor validada quando aplicável.

Evento resultante:

```text
notifications.notification_delivered
```

---

## `RegisterNotificationFailureCommand`

Registra falha de entrega.

Permissão:

```text
notifications.delivery.failure.register
```

Payload:

```json
{
  "delivery_id": "uuid",
  "attempt_number": 2,
  "error_code": "INVALID_DEVICE_TOKEN",
  "error_message_safe": "Token de dispositivo inválido",
  "failed_at": "datetime",
  "retryable": false,
  "provider_response_code": "string"
}
```

Validações:

* entrega existente;
* tentativa válida;
* mensagem segura sem segredos;
* classificar falha como transitória ou definitiva;
* não armazenar resposta sensível integral.

Eventos possíveis:

```text
notifications.notification_failed
notifications.delivery_retry_scheduled
notifications.delivery_dead_lettered
```

---

## `RetryNotificationDeliveryCommand`

Agenda nova tentativa.

Permissão:

```text
notifications.delivery.retry
```

Payload:

```json
{
  "delivery_id": "uuid",
  "next_attempt_at": "datetime",
  "reason_code": "TRANSIENT_PROVIDER_FAILURE"
}
```

Validações:

* falha recuperável;
* limite de tentativas;
* próxima data conforme política;
* notificação ainda válida;
* destinatário ainda ativo.

Evento resultante:

```text
notifications.delivery_retry_scheduled
```

---

## `CancelNotificationDeliveryCommand`

Cancela uma entrega pendente.

Permissão:

```text
notifications.delivery.cancel
```

Payload:

```json
{
  "delivery_id": "uuid",
  "reason_code": "NOTIFICATION_CANCELLED",
  "reason": "A notificação de origem foi cancelada"
}
```

Validações:

* entrega ainda não concluída;
* preservar tentativas anteriores;
* não revogar mensagem já entregue.

Evento resultante:

```text
notifications.delivery_cancelled
```

---

## `MoveNotificationDeliveryToDeadLetterCommand`

Move entrega definitivamente falha para tratamento manual.

Permissão:

```text
notifications.delivery.dead_letter
```

Payload:

```json
{
  "delivery_id": "uuid",
  "reason_code": "MAX_ATTEMPTS_EXCEEDED",
  "dead_lettered_at": "datetime",
  "notes": "Falha após cinco tentativas"
}
```

Evento resultante:

```text
notifications.delivery_dead_lettered
```

---

## `RequeueDeadLetterDeliveryCommand`

Reprocessa uma entrega após correção.

Permissão:

```text
notifications.delivery.dead_letter.requeue
```

Payload:

```json
{
  "delivery_id": "uuid",
  "reason": "Token do dispositivo atualizado",
  "scheduled_at": "datetime"
}
```

Validações:

* entrega em Dead Letter;
* causa corrigida;
* destinatário válido;
* autorização administrativa;
* nova tentativa explicitamente registrada.

Evento resultante:

```text
notifications.delivery_requeued
```

---

# 75. Interação do usuário

## `MarkNotificationReadCommand`

Marca notificação como lida para um destinatário.

Permissão:

```text
notifications.notification.read
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "read_at": "datetime",
  "device_id": "uuid"
}
```

Validações:

* usuário destinatário;
* leitura não altera outros destinatários;
* idempotência;
* notificação existente.

Evento resultante:

```text
notifications.notification_read
```

---

## `MarkNotificationUnreadCommand`

Marca como não lida.

Permissão:

```text
notifications.notification.mark_unread
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "marked_unread_at": "datetime"
}
```

Evento resultante:

```text
notifications.notification_marked_unread
```

---

## `MarkAllNotificationsReadCommand`

Marca todas as notificações elegíveis como lidas.

Permissão:

```text
notifications.notification.read_all
```

Payload:

```json
{
  "user_id": "uuid",
  "up_to_at": "datetime",
  "filters": {
    "notification_types": [],
    "severity": []
  }
}
```

Validações:

* somente notificações do usuário;
* escopo do Tenant atual;
* filtros válidos;
* processamento em lote idempotente.

Evento resultante:

```text
notifications.notifications_marked_read
```

---

## `AcknowledgeNotificationCommand`

Registra ciência explícita.

Permissão:

```text
notifications.notification.acknowledge
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "acknowledged_at": "datetime",
  "notes": "Ocorrência recebida e em análise"
}
```

Validações:

* notificação exige confirmação;
* usuário destinatário;
* ainda não confirmada;
* prazo de confirmação quando aplicável.

Evento resultante:

```text
notifications.notification_acknowledged
```

---

## `DismissNotificationCommand`

Dispensa notificação não obrigatória.

Permissão:

```text
notifications.notification.dismiss
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "dismissed_at": "datetime",
  "reason_code": "NOT_RELEVANT"
}
```

Validações:

* notificação dispensável;
* notificações críticas poderão exigir confirmação;
* estado individual por destinatário.

Evento resultante:

```text
notifications.notification_dismissed
```

---

## `SnoozeNotificationCommand`

Adia a reapresentação.

Permissão:

```text
notifications.notification.snooze
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "snoozed_until": "datetime",
  "reason": "Relembrar após o almoço"
}
```

Validações:

* notificação permite adiamento;
* data futura;
* limite máximo conforme política;
* notificações críticas podem não permitir;
* usuário destinatário.

Evento resultante:

```text
notifications.notification_snoozed
```

---

## `UnsnoozeNotificationCommand`

Remove o adiamento.

Permissão:

```text
notifications.notification.unsnooze
```

Payload:

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "unsnoozed_at": "datetime"
}
```

Evento resultante:

```text
notifications.notification_unsnoozed
```

---

## `ExecuteNotificationActionCommand`

Executa a ação associada à notificação.

Permissão:

```text
notifications.notification.action.execute
```

Payload:

```json
{
  "notification_id": "uuid",
  "notification_action_id": "uuid",
  "user_id": "uuid",
  "action_payload": {}
}
```

Validações:

* usuário destinatário;
* ação ainda válida;
* permissão real do contexto de destino;
* notificação não substitui autorização;
* ação executada através do comando oficial do contexto proprietário;
* idempotência.

Eventos possíveis:

```text
notifications.notification_action_executed
notifications.notification_action_failed
```

---

# 76. Templates de notificação

## `CreateNotificationTemplateCommand`

Cria um template.

Permissão:

```text
notifications.template.create
```

Payload:

```json
{
  "code": "MATERIAL_SHORTAGE_ALERT",
  "name": "Alerta de falta de material",
  "description": "Notifica responsáveis quando um material não está disponível",
  "notification_type": "MATERIAL_SHORTAGE",
  "supported_channels": [
    "IN_APP",
    "PUSH",
    "EMAIL"
  ],
  "required_variables": [
    "material_name",
    "production_order_code",
    "requested_quantity"
  ],
  "default_severity": "HIGH",
  "default_priority": "HIGH"
}
```

Validações:

* código único por Tenant;
* tipo válido;
* canais suportados;
* variáveis únicas;
* nomes de variáveis válidos;
* template sem conteúdo executável inseguro.

Evento resultante:

```text
notifications.template_created
```

---

## `UpdateNotificationTemplateCommand`

Atualiza os metadados do template.

Permissão:

```text
notifications.template.update
```

Payload:

```json
{
  "notification_template_id": "uuid",
  "name": "Alerta de indisponibilidade de material",
  "description": "Descrição revisada",
  "supported_channels": [
    "IN_APP",
    "PUSH",
    "EMAIL"
  ],
  "default_severity": "HIGH",
  "default_priority": "URGENT"
}
```

Validações:

* template ativo;
* não alterar versões publicadas;
* canais válidos;
* concorrência otimista.

Evento resultante:

```text
notifications.template_updated
```

---

## `CreateNotificationTemplateVersionCommand`

Cria uma versão editável.

Permissão:

```text
notifications.template.version.create
```

Payload:

```json
{
  "notification_template_id": "uuid",
  "based_on_version_id": "uuid",
  "change_reason": "Melhoria da mensagem enviada por e-mail"
}
```

Evento resultante:

```text
notifications.template_version_created
```

---

## `UpdateNotificationTemplateContentCommand`

Atualiza o conteúdo de uma versão em rascunho.

Permissão:

```text
notifications.template.version.update_content
```

Payload:

```json
{
  "notification_template_version_id": "uuid",
  "channel_contents": {
    "IN_APP": {
      "title": "Material indisponível",
      "body": "O material {{ material_name }} não está disponível para a ordem {{ production_order_code }}."
    },
    "PUSH": {
      "title": "Falta de material",
      "body": "{{ material_name }} indisponível."
    },
    "EMAIL": {
      "subject": "Falta de material na produção",
      "body_html": "<p>O material {{ material_name }} está indisponível.</p>",
      "body_text": "O material {{ material_name }} está indisponível."
    }
  },
  "action_definition": {
    "action_type": "OPEN_ENTITY",
    "entity_type": "INCIDENT"
  }
}
```

Validações:

* versão em rascunho;
* canais pertencentes ao template;
* variáveis declaradas;
* sintaxe válida;
* HTML sanitizado;
* links autorizados;
* conteúdo mínimo;
* evitar dados sensíveis;
* não permitir scripts.

Evento resultante:

```text
notifications.template_version_content_updated
```

---

## `PreviewNotificationTemplateCommand`

Gera visualização do template sem enviar.

Permissão:

```text
notifications.template.preview
```

Payload:

```json
{
  "notification_template_version_id": "uuid",
  "channel": "EMAIL",
  "variables": {
    "material_name": "MDF Branco TX 15 mm",
    "production_order_code": "OP-000001",
    "requested_quantity": "2 chapas"
  }
}
```

Validações:

* template válido;
* variáveis completas;
* renderização segura;
* não enviar mensagem;
* dados de exemplo identificados como preview.

Evento técnico opcional:

```text
notifications.template_preview_generated
```

---

## `PublishNotificationTemplateVersionCommand`

Publica uma versão.

Permissão:

```text
notifications.template.version.publish
```

Payload:

```json
{
  "notification_template_version_id": "uuid",
  "publication_notes": "Template aprovado"
}
```

Validações:

* conteúdo para todos os canais obrigatórios;
* variáveis válidas;
* renderização testada;
* HTML sanitizado;
* nenhuma referência quebrada;
* versão torna-se imutável.

Evento resultante:

```text
notifications.template_version_published
```

---

## `DeprecateNotificationTemplateVersionCommand`

Marca versão como obsoleta.

Permissão:

```text
notifications.template.version.deprecate
```

Payload:

```json
{
  "notification_template_version_id": "uuid",
  "replacement_version_id": "uuid",
  "reason": "Nova versão publicada"
}
```

Evento resultante:

```text
notifications.template_version_deprecated
```

---

## `ArchiveNotificationTemplateCommand`

Arquiva template.

Permissão:

```text
notifications.template.archive
```

Payload:

```json
{
  "notification_template_id": "uuid",
  "reason": "Template substituído",
  "replacement_template_id": "uuid"
}
```

Validações:

* políticas ativas;
* agendamentos;
* automações;
* template substituto quando necessário;
* histórico preservado.

Evento resultante:

```text
notifications.template_archived
```

---

## `RestoreNotificationTemplateCommand`

Restaura template arquivado.

Permissão:

```text
notifications.template.restore
```

Payload:

```json
{
  "notification_template_id": "uuid",
  "reason": "Template voltará a ser utilizado"
}
```

Evento resultante:

```text
notifications.template_restored
```

---

# 77. Políticas de notificação

## `CreateNotificationPolicyCommand`

Cria uma política que transforma eventos em notificações.

Permissão:

```text
notifications.policy.create
```

Payload:

```json
{
  "code": "NOTIFY_MATERIAL_SHORTAGE",
  "name": "Notificar falta de material",
  "description": "Notifica estoque e produção quando uma reserva falha",
  "trigger_event_type": "inventory.stock_reservation_failed",
  "trigger_event_schema_versions": [
    1
  ],
  "template_id": "uuid",
  "recipient_strategy": "SECTOR",
  "recipient_configuration": {
    "sector_codes": [
      "INVENTORY",
      "PRODUCTION"
    ]
  },
  "channel_strategy": {
    "channels": [
      "IN_APP",
      "PUSH"
    ]
  },
  "conditions": {},
  "deduplication_window_seconds": 900,
  "priority": "HIGH",
  "is_mandatory": true
}
```

Validações:

* código único;
* evento registrado no catálogo;
* versões suportadas;
* template publicado;
* estratégia de destinatário válida;
* canais habilitados;
* condições válidas;
* janela de deduplicação não negativa;
* política não cria ciclo de eventos.

Evento resultante:

```text
notifications.policy_created
```

---

## `UpdateNotificationPolicyCommand`

Atualiza política inativa ou editável.

Permissão:

```text
notifications.policy.update
```

Payload:

```json
{
  "notification_policy_id": "uuid",
  "name": "Notificar indisponibilidade de material",
  "template_id": "uuid",
  "recipient_strategy": "ENTITY_RESPONSIBLES",
  "recipient_configuration": {},
  "channel_strategy": {
    "channels": [
      "IN_APP",
      "PUSH",
      "EMAIL"
    ]
  },
  "conditions": {},
  "deduplication_window_seconds": 1800,
  "priority": "URGENT",
  "is_mandatory": true
}
```

Validações:

* política não arquivada;
* alterações em política ativa podem exigir nova versão;
* template válido;
* canais e destinatários;
* condições seguras;
* concorrência otimista.

Evento resultante:

```text
notifications.policy_updated
```

---

## `ActivateNotificationPolicyCommand`

Ativa política.

Permissão:

```text
notifications.policy.activate
```

Payload:

```json
{
  "notification_policy_id": "uuid",
  "effective_at": "datetime"
}
```

Validações:

* template publicado;
* evento válido;
* destinatários resolvíveis;
* canais configurados;
* provedor disponível quando obrigatório;
* política sem erros de validação.

Evento resultante:

```text
notifications.policy_activated
```

---

## `PauseNotificationPolicyCommand`

Pausa geração automática.

Permissão:

```text
notifications.policy.pause
```

Payload:

```json
{
  "notification_policy_id": "uuid",
  "reason": "Política em revisão",
  "paused_at": "datetime"
}
```

Evento resultante:

```text
notifications.policy_paused
```

---

## `ResumeNotificationPolicyCommand`

Retoma política.

Permissão:

```text
notifications.policy.resume
```

Payload:

```json
{
  "notification_policy_id": "uuid",
  "resumed_at": "datetime",
  "reason": "Revisão concluída"
}
```

Evento resultante:

```text
notifications.policy_resumed
```

---

## `ArchiveNotificationPolicyCommand`

Arquiva política.

Permissão:

```text
notifications.policy.archive
```

Payload:

```json
{
  "notification_policy_id": "uuid",
  "reason": "Política substituída",
  "replacement_policy_id": "uuid"
}
```

Evento resultante:

```text
notifications.policy_archived
```

---

## `TestNotificationPolicyCommand`

Executa simulação sem entrega real.

Permissão:

```text
notifications.policy.test
```

Payload:

```json
{
  "notification_policy_id": "uuid",
  "sample_event": {
    "event_type": "inventory.stock_reservation_failed",
    "schema_version": 1,
    "payload": {}
  },
  "resolve_recipients": true,
  "render_templates": true
}
```

Validações:

* política válida;
* evento de teste identificado;
* nenhum envio real;
* nenhum efeito em destinatários;
* conteúdo e resolução retornados como preview.

Evento técnico opcional:

```text
notifications.policy_tested
```

---

# 78. Preferências de notificação

## `CreateNotificationPreferenceCommand`

Cria preferência individual.

Permissão:

```text
notifications.preference.create
```

Payload:

```json
{
  "user_id": "uuid",
  "notification_type": "MATERIAL_SHORTAGE",
  "channel": "PUSH",
  "enabled": true,
  "minimum_severity": "HIGH",
  "quiet_hours": {
    "enabled": true,
    "start_time": "22:00:00",
    "end_time": "07:00:00",
    "timezone": "America/Sao_Paulo"
  }
}
```

Validações:

* usuário correspondente ou administrador autorizado;
* tipo e canal válidos;
* timezone válido;
* horários coerentes;
* preferências não podem desabilitar comunicações obrigatórias proibidas por política.

Evento resultante:

```text
notifications.preference_created
```

---

## `UpdateNotificationPreferenceCommand`

Atualiza preferência.

Permissão:

```text
notifications.preference.update
```

Payload:

```json
{
  "notification_preference_id": "uuid",
  "enabled": false,
  "minimum_severity": "CRITICAL",
  "quiet_hours": {
    "enabled": true,
    "start_time": "21:00:00",
    "end_time": "08:00:00",
    "timezone": "America/Sao_Paulo"
  }
}
```

Evento resultante:

```text
notifications.preference_updated
```

---

## `ResetNotificationPreferencesCommand`

Restaura preferências padrão.

Permissão:

```text
notifications.preference.reset
```

Payload:

```json
{
  "user_id": "uuid",
  "scope": "CURRENT_TENANT"
}
```

Escopos:

```text
CURRENT_TENANT
ALL_TENANTS
CHANNEL
NOTIFICATION_TYPE
```

Validações:

* escopo autorizado;
* não remover políticas obrigatórias;
* redefinir valores conforme padrão vigente.

Evento resultante:

```text
notifications.preferences_reset
```

---

## `SetNotificationQuietHoursCommand`

Define horário silencioso.

Permissão:

```text
notifications.preference.quiet_hours.set
```

Payload:

```json
{
  "user_id": "uuid",
  "start_time": "22:00:00",
  "end_time": "07:00:00",
  "timezone": "America/Sao_Paulo",
  "allowed_severities": [
    "CRITICAL"
  ]
}
```

Validações:

* timezone válido;
* intervalo válido;
* comunicações críticas não bloqueadas indevidamente;
* preferência individual.

Evento resultante:

```text
notifications.quiet_hours_changed
```

---

## `DisableNotificationQuietHoursCommand`

Desativa horário silencioso.

Permissão:

```text
notifications.preference.quiet_hours.disable
```

Payload:

```json
{
  "user_id": "uuid"
}
```

Evento resultante:

```text
notifications.quiet_hours_disabled
```

---

## `SetNotificationDigestPreferenceCommand`

Configura resumo periódico.

Permissão:

```text
notifications.preference.digest.set
```

Payload:

```json
{
  "user_id": "uuid",
  "digest_type": "DAILY",
  "delivery_time": "08:00:00",
  "timezone": "America/Sao_Paulo",
  "channels": [
    "EMAIL",
    "IN_APP"
  ],
  "notification_types": [
    "INFORMATION",
    "REMINDER"
  ],
  "exclude_severities": [
    "CRITICAL"
  ]
}
```

Tipos:

```text
HOURLY
DAILY
WEEKLY
CUSTOM
```

Validações:

* frequência suportada;
* horário e timezone;
* canais habilitados;
* notificações urgentes não aguardam digest;
* preferências aplicáveis ao Tenant.

Evento resultante:

```text
notifications.digest_preference_changed
```

---

# 79. Dispositivos e endpoints

## `RegisterNotificationEndpointCommand`

Registra endpoint de entrega.

Permissão:

```text
notifications.endpoint.register
```

Payload:

```json
{
  "user_id": "uuid",
  "device_id": "uuid",
  "channel": "PUSH",
  "provider": "WEB_PUSH",
  "endpoint_reference": "encrypted-or-token-reference",
  "application": "PWA",
  "application_version": "0.1.0",
  "platform": "WINDOWS",
  "locale": "pt-BR",
  "timezone": "America/Sao_Paulo"
}
```

Validações:

* usuário autenticado;
* dispositivo correspondente;
* endpoint válido;
* segredo não armazenado em log;
* evitar duplicidade;
* criptografia ou referência segura;
* consentimento quando necessário.

Evento resultante:

```text
notifications.endpoint_registered
```

---

## `UpdateNotificationEndpointCommand`

Atualiza endpoint.

Permissão:

```text
notifications.endpoint.update
```

Payload:

```json
{
  "notification_endpoint_id": "uuid",
  "endpoint_reference": "updated-reference",
  "application_version": "0.2.0",
  "locale": "pt-BR",
  "timezone": "America/Sao_Paulo"
}
```

Evento resultante:

```text
notifications.endpoint_updated
```

---

## `DisableNotificationEndpointCommand`

Desativa endpoint inválido ou revogado.

Permissão:

```text
notifications.endpoint.disable
```

Payload:

```json
{
  "notification_endpoint_id": "uuid",
  "reason_code": "INVALID_TOKEN",
  "reason": "Provedor informou token inválido"
}
```

Evento resultante:

```text
notifications.endpoint_disabled
```

---

## `RemoveNotificationEndpointCommand`

Remove endpoint do usuário.

Permissão:

```text
notifications.endpoint.remove
```

Payload:

```json
{
  "notification_endpoint_id": "uuid",
  "reason": "Dispositivo removido pelo usuário"
}
```

Validações:

* usuário proprietário ou administrador autorizado;
* preservar histórico de entregas;
* não apagar tentativas anteriores.

Evento resultante:

```text
notifications.endpoint_removed
```

---

## `VerifyNotificationEndpointCommand`

Verifica funcionamento do endpoint.

Permissão:

```text
notifications.endpoint.verify
```

Payload:

```json
{
  "notification_endpoint_id": "uuid",
  "verification_code": "string"
}
```

Validações:

* endpoint ativo;
* código válido e não expirado;
* tentativa limitada;
* não registrar código em logs.

Evento resultante:

```text
notifications.endpoint_verified
```

---

# 80. Agendamento de notificações

## `ScheduleNotificationCommand`

Agenda uma notificação futura.

Permissão:

```text
notifications.notification.schedule
```

Payload:

```json
{
  "notification_id": "uuid",
  "scheduled_at": "datetime",
  "timezone": "America/Sao_Paulo",
  "respect_quiet_hours": true
}
```

Validações:

* notificação em rascunho;
* data futura;
* timezone válido;
* conteúdo e destinatários completos;
* expiração posterior ao envio;
* idempotência.

Evento resultante:

```text
notifications.notification_scheduled
```

---

## `RescheduleNotificationCommand`

Reagenda a notificação.

Permissão:

```text
notifications.notification.reschedule
```

Payload:

```json
{
  "notification_id": "uuid",
  "new_scheduled_at": "datetime",
  "reason": "Horário ajustado"
}
```

Validações:

* entrega não iniciada;
* nova data válida;
* histórico preservado.

Evento resultante:

```text
notifications.notification_rescheduled
```

---

## `SendScheduledNotificationNowCommand`

Antecipa o envio.

Permissão:

```text
notifications.notification.send_now
```

Payload:

```json
{
  "notification_id": "uuid",
  "reason": "Informação tornou-se urgente"
}
```

Validações:

* notificação agendada;
* ator autorizado;
* canais disponíveis;
* horário silencioso e prioridade reavaliados.

Evento resultante:

```text
notifications.notification_released_for_delivery
```

---

## `CancelScheduledNotificationCommand`

Cancela agendamento.

Permissão:

```text
notifications.notification.schedule.cancel
```

Payload:

```json
{
  "notification_id": "uuid",
  "reason": "Comunicação não será mais necessária"
}
```

Evento resultante:

```text
notifications.notification_schedule_cancelled
```

---

# 81. Resumos de notificação

## `GenerateNotificationDigestCommand`

Gera resumo de notificações.

Permissão:

```text
notifications.digest.generate
```

Payload:

```json
{
  "user_id": "uuid",
  "period_start": "datetime",
  "period_end": "datetime",
  "digest_type": "DAILY",
  "channels": [
    "EMAIL",
    "IN_APP"
  ]
}
```

Validações:

* período válido;
* preferências do usuário;
* notificações elegíveis;
* excluir notificações já resumidas quando necessário;
* respeitar Tenant;
* não omitir alertas críticos;
* idempotência por usuário, período e tipo.

Eventos possíveis:

```text
notifications.digest_generated
notifications.digest_skipped
```

---

## `SendNotificationDigestCommand`

Envia resumo gerado.

Permissão:

```text
notifications.digest.send
```

Payload:

```json
{
  "notification_digest_id": "uuid",
  "channel": "EMAIL",
  "scheduled_at": "datetime"
}
```

Validações:

* resumo válido;
* destinatário ativo;
* canal habilitado;
* período ainda aplicável;
* evitar envio duplicado.

Eventos possíveis:

```text
notifications.digest_sent
notifications.digest_failed
```

---

## `RegenerateNotificationDigestCommand`

Regera resumo antes do envio.

Permissão:

```text
notifications.digest.regenerate
```

Payload:

```json
{
  "notification_digest_id": "uuid",
  "reason": "Novas notificações foram incluídas"
}
```

Validações:

* resumo ainda não entregue;
* conteúdo anterior preservado em histórico;
* período original mantido.

Evento resultante:

```text
notifications.digest_regenerated
```

---

# 82. Comunicação externa

## `SendEmailNotificationCommand`

Envia comunicação por e-mail.

Permissão:

```text
notifications.email.send
```

Payload:

```json
{
  "notification_id": "uuid",
  "recipient_contact_id": "uuid",
  "recipient_email": "masked-or-resolved-server-side",
  "template_version_id": "uuid",
  "variables": {},
  "attachments": [
    {
      "document_id": "uuid",
      "document_version_id": "uuid"
    }
  ]
}
```

Validações:

* e-mail resolvido no servidor;
* destinatário autorizado;
* template publicado;
* anexos acessíveis;
* tamanho total permitido;
* dados pessoais protegidos;
* domínio e provedor autorizados;
* idempotência.

Eventos possíveis:

```text
notifications.notification_sent
notifications.notification_failed
```

---

## `SendWhatsAppNotificationCommand`

Envia comunicação por WhatsApp.

Permissão:

```text
notifications.whatsapp.send
```

Payload:

```json
{
  "notification_id": "uuid",
  "recipient_contact_id": "uuid",
  "approved_template_reference": "string",
  "variables": {},
  "media_document_id": "uuid"
}
```

Validações:

* integração habilitada;
* contato com consentimento quando necessário;
* template externo aprovado;
* janela de comunicação respeitada;
* número resolvido no servidor;
* mídia permitida;
* idempotência.

Eventos possíveis:

```text
notifications.notification_sent
notifications.notification_failed
```

---

## `SendSmsNotificationCommand`

Envia SMS quando habilitado.

Permissão:

```text
notifications.sms.send
```

Payload:

```json
{
  "notification_id": "uuid",
  "recipient_contact_id": "uuid",
  "message": "Mensagem curta",
  "provider": "SMS_PROVIDER"
}
```

Validações:

* canal habilitado;
* número válido;
* tamanho suportado;
* consentimento;
* conteúdo sem dados sensíveis desnecessários;
* custo autorizado;
* idempotência.

Eventos possíveis:

```text
notifications.notification_sent
notifications.notification_failed
```

---

## `SendWebhookNotificationCommand`

Entrega evento autorizado a webhook externo.

Permissão:

```text
notifications.webhook.send
```

Payload:

```json
{
  "notification_id": "uuid",
  "webhook_subscription_id": "uuid",
  "payload_reference": "uuid",
  "signature_version": 1
}
```

Validações:

* inscrição ativa;
* evento permitido;
* payload sanitizado;
* assinatura;
* segredo armazenado com segurança;
* proteção contra SSRF;
* retry e idempotência.

Eventos possíveis:

```text
notifications.notification_sent
notifications.notification_failed
```

---

# 83. Supressão e deduplicação

## `SuppressNotificationCommand`

Suprime uma notificação segundo política.

Permissão:

```text
notifications.notification.suppress
```

Payload:

```json
{
  "notification_id": "uuid",
  "reason_code": "DUPLICATE_WITHIN_WINDOW",
  "reason": "Notificação equivalente já enviada",
  "matching_notification_id": "uuid"
}
```

Motivos:

```text
DUPLICATE_WITHIN_WINDOW
RECIPIENT_DISABLED
QUIET_HOURS
POLICY_CONDITION_NOT_MET
SOURCE_EVENT_OBSOLETE
RATE_LIMIT
INVALID_RECIPIENT
NO_ELIGIBLE_CHANNEL
MANUAL_SUPPRESSION
```

Validações:

* regra aplicável;
* notificações obrigatórias não suprimidas indevidamente;
* histórico e motivo preservados;
* notificação equivalente identificada quando duplicada.

Evento resultante:

```text
notifications.notification_suppressed
```

---

## `ReleaseSuppressedNotificationCommand`

Libera notificação suprimida.

Permissão:

```text
notifications.notification.suppression.release
```

Payload:

```json
{
  "notification_id": "uuid",
  "reason": "Alerta tornou-se crítico",
  "released_at": "datetime"
}
```

Validações:

* notificação suprimida;
* ainda válida;
* destinatários e canais reavaliados;
* autorização.

Evento resultante:

```text
notifications.notification_released
```

---

## `MergeNotificationsCommand`

Agrupa notificações equivalentes.

Permissão:

```text
notifications.notification.merge
```

Payload:

```json
{
  "source_notification_ids": [
    "uuid",
    "uuid"
  ],
  "target_notification_id": "uuid",
  "merge_strategy": "INCREMENT_COUNTER",
  "reason": "Alertas repetidos do mesmo material"
}
```

Estratégias:

```text
INCREMENT_COUNTER
COMBINE_REFERENCES
COMBINE_MESSAGES
REPLACE_WITH_LATEST
CUSTOM
```

Validações:

* mesmo Tenant;
* notificações compatíveis;
* visibilidade equivalente;
* estado de entrega avaliado;
* não apagar histórico.

Evento resultante:

```text
notifications.notifications_merged
```

---

# 84. Integrações de Notifications

## Eventos consumidos

Notifications deverá consumir, inicialmente:

```text
identity.authentication_failed
identity.user_blocked
organization.employee_terminated
organization.membership_disabled
commercial.quotation_approved
commercial.contract_signed
workflow.stage_changed
workflow.instance_completed
production.operation_assigned
production.execution_paused
production.material_requested
production.rework_requested
inventory.stock_reservation_failed
inventory.reorder_point_reached
purchasing.purchase_order_delivery_rescheduled
purchasing.material_received
quality.nonconformity_created
quality.rework_required
maintenance.machine_unavailable
maintenance.machine_released
maintenance.preventive_due
scheduling.conflict_detected
incident.created
incident.escalated
incident.sla_breached
financial.receivable_overdue
system.background_job_failed
sync.conflict_detected
```

---

## Reação a eventos

A reação deverá seguir:

```text
Evento recebido
    ↓
Validar contrato e versão
    ↓
Localizar políticas ativas
    ↓
Avaliar condições
    ↓
Resolver destinatários
    ↓
Avaliar preferências
    ↓
Deduplicar
    ↓
Renderizar template
    ↓
Criar Notification
    ↓
Criar entregas
    ↓
Enfileirar canais
```

---

## Reação a `production.operation_assigned`

Poderá notificar:

* funcionário atribuído;
* líder do setor;
* equipe;
* administrador, quando configurado.

---

## Reação a `production.execution_paused`

Somente deverá notificar automaticamente quando:

* motivo exigir ação externa;
* duração exceder limite;
* severidade for alta;
* produção estiver bloqueada;
* política estiver ativa.

---

## Reação a `incident.escalated`

Deverá ignorar horário silencioso quando a severidade for crítica e a política classificar a comunicação como obrigatória.

---

## Reação a `financial.receivable_overdue`

Poderá notificar:

* financeiro;
* responsável comercial;
* administrador;
* cliente, apenas por política específica e canal autorizado.

---

# 85. Regras de integridade de Notifications

## 85.1 Notification não é Domain Event

O evento registra um fato.

A notificação comunica esse fato a alguém.

Um evento poderá gerar:

* nenhuma notificação;
* uma notificação;
* várias notificações;
* resumo posterior;
* comunicação por diferentes canais.

---

## 85.2 Entrega individual

Cada destinatário e canal deverão possuir estado próprio.

Exemplo:

```text
Notification
    Recipient A
        IN_APP = DELIVERED
        PUSH = FAILED
    Recipient B
        EMAIL = DELIVERED
```

Um status único na notificação não é suficiente.

---

## 85.3 Preferências

Preferências pessoais podem controlar comunicações opcionais.

Não poderão impedir indevidamente:

* alertas de segurança;
* avisos legais;
* comunicações administrativas obrigatórias;
* eventos críticos;
* mensagens transacionais indispensáveis.

---

## 85.4 Conteúdo sensível

Notificações em canais externos devem evitar:

* dados bancários completos;
* documentos pessoais;
* informações médicas;
* senhas;
* tokens;
* segredos;
* conteúdo operacional sigiloso integral.

Preferir mensagem resumida e link autenticado.

---

## 85.5 Links e ações

Links não deverão conter credenciais ou dados sensíveis.

A ação deve abrir uma rota autenticada e validar novamente:

* Tenant;
* Membership;
* permissão;
* escopo;
* entidade;
* estado atual.

---

## 85.6 Provedores externos

O contexto deve abstrair provedores.

O domínio conhece o canal.

A infraestrutura conhece o fornecedor tecnológico.

Exemplo:

```text
Channel = EMAIL
Provider = SMTP, SES ou outro adaptador
```

---

## 85.7 Falhas

Falhas de entrega não devem alterar o fato de origem.

Exemplo:

```text
production.material_requested
```

continua válido mesmo que o Push falhe.

---

## 85.8 Idempotência

A chave recomendada para notificações derivadas de eventos:

```text
tenant_id
source_event_id
notification_policy_id
recipient_id
channel
```

---

## 85.9 Rate limiting

Aplicar limites por:

* Tenant;
* usuário;
* canal;
* política;
* provedor;
* período;
* tipo de mensagem.

Alertas críticos deverão possuir política específica.

---

## 85.10 Auditoria

Auditar:

* criação manual;
* comunicação em massa;
* alteração de template;
* alteração de política;
* envio externo;
* cancelamento;
* supressão manual;
* reprocessamento;
* comunicação executada por IA.

---

## 85.11 Retenção

Preservar pelo período necessário:

* conteúdo enviado;
* template e versão;
* destinatário;
* canal;
* tentativa;
* status;
* provedor;
* confirmação;
* falha;
* interação;
* origem;
* correlation_id.

Dados pessoais deverão seguir políticas de retenção e anonimização.

---

## 85.12 Offline

A leitura e interação poderão ser registradas offline.

Comandos deverão possuir:

```text
command_id
idempotency_key
device_id
notification_id
user_id
occurred_at
expected_entity_version
```

O envio externo não será executado diretamente pelo cliente offline.

---

# 86. Eventos resultantes de Notifications

Eventos principais:

```text
notifications.notification_created
notifications.notification_updated
notifications.notification_scheduled
notifications.notification_rescheduled
notifications.notification_cancelled
notifications.notification_archived
notifications.notification_restored
notifications.recipient_added
notifications.recipient_removed
notifications.recipients_resolved
notifications.delivery_queued
notifications.notification_sent
notifications.notification_delivered
notifications.notification_failed
notifications.delivery_retry_scheduled
notifications.delivery_dead_lettered
notifications.delivery_requeued
notifications.notification_read
notifications.notification_marked_unread
notifications.notification_acknowledged
notifications.notification_dismissed
notifications.notification_snoozed
notifications.notification_action_executed
notifications.template_created
notifications.template_version_created
notifications.template_version_published
notifications.template_archived
notifications.policy_created
notifications.policy_activated
notifications.policy_paused
notifications.policy_archived
notifications.preference_created
notifications.preference_updated
notifications.quiet_hours_changed
notifications.endpoint_registered
notifications.endpoint_disabled
notifications.digest_generated
notifications.digest_sent
notifications.notification_suppressed
notifications.notification_released
notifications.notifications_merged
```

Consumidores principais:

* Audit;
* Timeline;
* Analytics;
* Security;
* Administration;
* AI;
* Automation.

---

# 87. Continuação

A próxima subparte continuará com:

```text
Financial
```

Fim da Parte 3E-A.
# 88. Comandos de Financial

## `CreateBankAccountCommand`

Cria uma conta bancária, carteira ou caixa financeiro.

Permissão:

```text
financial.bank_account.create
```

Payload:

```json
{
  "code": "BANK-001",
  "name": "Conta corrente principal",
  "account_type": "CHECKING",
  "bank_code": "001",
  "branch_number": "1234",
  "account_number_masked": "*****-1",
  "pix_key_reference": null,
  "currency": "BRL",
  "branch_id": "uuid",
  "cost_center_id": null,
  "opening_balance": "0.00",
  "opening_balance_date": "date",
  "allows_overdraft": false,
  "overdraft_limit": "0.00",
  "integration_provider_id": null,
  "configuration": {}
}
```

Tipos iniciais:

```text
CHECKING
SAVINGS
CASH
DIGITAL_WALLET
PAYMENT_ACCOUNT
INVESTMENT
CREDIT_CARD_CLEARING
INTERNAL_CLEARING
OTHER
```

Validações:

* código único por Tenant;
* nome válido;
* moeda suportada;
* filial pertencente ao Tenant quando informada;
* saldo inicial acompanhado de data;
* limite não negativo;
* conta bancária não deve armazenar credenciais de acesso;
* dados bancários sensíveis devem ser mascarados ou referenciados;
* integração deve utilizar segredo armazenado na infraestrutura.

Evento resultante:

```text
financial.bank_account_created
```

---

## `UpdateBankAccountCommand`

Atualiza os dados operacionais da conta.

Permissão:

```text
financial.bank_account.update
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "name": "Conta corrente operacional",
  "branch_id": "uuid",
  "cost_center_id": "uuid",
  "allows_overdraft": true,
  "overdraft_limit": "10000.00",
  "configuration": {}
}
```

Validações:

* conta ativa;
* moeda não pode ser alterada após movimentações sem processo específico;
* informações bancárias sensíveis não devem ser substituídas sem autorização;
* concorrência otimista;
* alterações de limite devem ser auditadas.

Evento resultante:

```text
financial.bank_account_updated
```

---

## `DeactivateBankAccountCommand`

Desativa a conta para novas movimentações.

Permissão:

```text
financial.bank_account.deactivate
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "reason": "Conta encerrada pela instituição",
  "effective_at": "datetime",
  "replacement_bank_account_id": "uuid"
}
```

Validações:

* não existir conciliação pendente incompatível;
* saldo deve ser tratado;
* lançamentos futuros devem ser remanejados;
* integrações devem ser desativadas;
* histórico preservado;
* conta substituta quando necessária.

Evento resultante:

```text
financial.bank_account_deactivated
```

---

## `ReactivateBankAccountCommand`

Reativa uma conta desativada.

Permissão:

```text
financial.bank_account.reactivate
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "reason": "Conta reaberta",
  "effective_at": "datetime"
}
```

Validações:

* conta não arquivada definitivamente;
* dados bancários válidos;
* integração revalidada;
* usuário autorizado.

Evento resultante:

```text
financial.bank_account_reactivated
```

---

## `ArchiveBankAccountCommand`

Arquiva uma conta sem apagar seu histórico.

Permissão:

```text
financial.bank_account.archive
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "reason": "Conta encerrada e sem movimentações pendentes"
}
```

Validações:

* conta desativada;
* saldo tratado;
* nenhuma conciliação aberta;
* nenhum pagamento ou recebimento futuro vinculado;
* histórico mantido.

Evento resultante:

```text
financial.bank_account_archived
```

---

# 89. Contas a receber

## `CreateReceivableCommand`

Cria uma conta a receber.

Permissão:

```text
financial.receivable.create
```

Payload:

```json
{
  "customer_id": "uuid",
  "contract_id": "uuid",
  "sales_order_id": "uuid",
  "quotation_id": "uuid",
  "code": "REC-000001",
  "description": "Entrada do projeto de cozinha",
  "document_number": "CTR-000001",
  "issue_date": "date",
  "competence_date": "date",
  "currency": "BRL",
  "total_amount": "13500.00",
  "payment_method": "PIX",
  "bank_account_id": "uuid",
  "cost_center_id": "uuid",
  "category_id": "uuid",
  "installments": [
    {
      "installment_number": 1,
      "due_date": "date",
      "amount": "13500.00"
    }
  ],
  "notes": null
}
```

Validações:

* cliente ativo;
* valor positivo;
* soma das parcelas igual ao total;
* datas válidas;
* moeda suportada;
* origem pertencente ao mesmo cliente;
* conta bancária ativa;
* centro de custo e categoria válidos;
* código único;
* impedir duplicidade por origem e parcela;
* idempotência quando criada por evento comercial.

Evento resultante:

```text
financial.receivable_created
```

---

## `CreateReceivableFromContractCommand`

Cria contas a receber a partir do contrato.

Permissão:

```text
financial.receivable.create_from_contract
```

Payload:

```json
{
  "contract_id": "uuid",
  "contract_version_id": "uuid",
  "customer_id": "uuid",
  "payment_schedule": [
    {
      "installment_number": 1,
      "percentage": "50.00",
      "due_rule": "ON_CONTRACT_SIGNATURE"
    },
    {
      "installment_number": 2,
      "percentage": "50.00",
      "due_rule": "ON_DELIVERY"
    }
  ],
  "bank_account_id": "uuid",
  "cost_center_id": "uuid",
  "category_id": "uuid"
}
```

Validações:

* contrato assinado ou elegível;
* versão vigente;
* condições financeiras válidas;
* percentuais totalizam 100;
* não duplicar contas já criadas;
* regras de vencimento suportadas;
* idempotência por contrato e versão.

Eventos resultantes:

```text
financial.receivable_created
financial.receivable_schedule_created
```

---

## `UpdateReceivableCommand`

Atualiza uma conta ainda editável.

Permissão:

```text
financial.receivable.update
```

Payload:

```json
{
  "receivable_id": "uuid",
  "description": "Entrada do contrato",
  "competence_date": "date",
  "bank_account_id": "uuid",
  "cost_center_id": "uuid",
  "category_id": "uuid",
  "notes": "Descrição revisada"
}
```

Validações:

* conta não liquidada ou cancelada;
* não alterar valor pago;
* alterações estruturais podem exigir comando específico;
* conta bancária e classificação válidas;
* concorrência otimista.

Evento resultante:

```text
financial.receivable_updated
```

---

## `AddReceivableInstallmentCommand`

Adiciona parcela a uma conta a receber.

Permissão:

```text
financial.receivable.installment.create
```

Payload:

```json
{
  "receivable_id": "uuid",
  "installment_number": 3,
  "due_date": "date",
  "amount": "5000.00",
  "payment_method": "BANK_TRANSFER"
}
```

Validações:

* conta editável;
* número da parcela único;
* valor positivo;
* data válida;
* total da conta recalculado ou diferença autorizada;
* não adicionar parcela após liquidação total.

Evento resultante:

```text
financial.receivable_installment_added
```

---

## `UpdateReceivableInstallmentCommand`

Atualiza parcela ainda não paga.

Permissão:

```text
financial.receivable.installment.update
```

Payload:

```json
{
  "receivable_installment_id": "uuid",
  "due_date": "date",
  "amount": "5200.00",
  "payment_method": "PIX",
  "notes": "Parcela renegociada"
}
```

Validações:

* parcela aberta;
* valor não inferior ao já recebido;
* data válida;
* alterações após emissão de cobrança devem gerar nova cobrança;
* concorrência otimista.

Evento resultante:

```text
financial.receivable_installment_updated
```

---

## `RemoveReceivableInstallmentCommand`

Remove parcela ainda sem recebimento.

Permissão:

```text
financial.receivable.installment.remove
```

Payload:

```json
{
  "receivable_installment_id": "uuid",
  "reason": "Parcela consolidada em outra"
}
```

Validações:

* nenhum recebimento alocado;
* conta não liquidada;
* total permanece válido;
* justificativa;
* preservar histórico.

Evento resultante:

```text
financial.receivable_installment_removed
```

---

## `RescheduleReceivableInstallmentCommand`

Altera o vencimento de uma parcela.

Permissão:

```text
financial.receivable.installment.reschedule
```

Payload:

```json
{
  "receivable_installment_id": "uuid",
  "new_due_date": "date",
  "reason_code": "CUSTOMER_NEGOTIATION",
  "reason": "Novo vencimento acordado com o cliente",
  "agreement_document_id": "uuid"
}
```

Validações:

* parcela aberta;
* nova data válida;
* política de renegociação;
* juros e multas avaliados;
* documento comprobatório quando exigido;
* histórico do vencimento anterior preservado.

Evento resultante:

```text
financial.receivable_installment_rescheduled
```

---

## `ApplyReceivableDiscountCommand`

Aplica desconto a uma conta ou parcela.

Permissão:

```text
financial.receivable.discount.apply
```

Payload:

```json
{
  "receivable_id": "uuid",
  "receivable_installment_id": "uuid",
  "discount_type": "FIXED_AMOUNT",
  "discount_value": "500.00",
  "reason_code": "COMMERCIAL_AGREEMENT",
  "reason": "Desconto autorizado",
  "effective_until": "date"
}
```

Validações:

* saldo aberto;
* desconto não superior ao saldo;
* alçada do ator;
* motivo;
* prazo de validade quando temporário;
* impactos tributários;
* não alterar valor original sem preservar o ajuste.

Evento resultante:

```text
financial.receivable_discount_applied
```

---

## `RemoveReceivableDiscountCommand`

Remove desconto ainda não utilizado.

Permissão:

```text
financial.receivable.discount.remove
```

Payload:

```json
{
  "receivable_adjustment_id": "uuid",
  "reason": "Condição de desconto expirada"
}
```

Validações:

* desconto ativo;
* não utilizado em recebimento;
* justificativa;
* recalcular saldo.

Evento resultante:

```text
financial.receivable_discount_removed
```

---

## `ApplyReceivableInterestCommand`

Aplica juros.

Permissão:

```text
financial.receivable.interest.apply
```

Payload:

```json
{
  "receivable_installment_id": "uuid",
  "calculation_type": "DAILY_PERCENTAGE",
  "rate": "0.033",
  "calculation_start_date": "date",
  "calculation_end_date": "date",
  "calculated_amount": "50.00",
  "reason": "Atraso no pagamento"
}
```

Validações:

* parcela vencida ou regra contratual;
* taxa dentro da política;
* período válido;
* cálculo reproduzível;
* não duplicar juros do mesmo período;
* conformidade legal.

Evento resultante:

```text
financial.receivable_interest_applied
```

---

## `ApplyReceivablePenaltyCommand`

Aplica multa.

Permissão:

```text
financial.receivable.penalty.apply
```

Payload:

```json
{
  "receivable_installment_id": "uuid",
  "penalty_type": "PERCENTAGE",
  "penalty_value": "2.00",
  "calculated_amount": "270.00",
  "reason": "Multa contratual por atraso"
}
```

Validações:

* previsão contratual;
* percentual legalmente permitido;
* multa ainda não aplicada;
* cálculo auditável.

Evento resultante:

```text
financial.receivable_penalty_applied
```

---

## `RegisterReceivablePaymentCommand`

Registra um recebimento.

Permissão:

```text
financial.receivable.payment.register
```

Payload:

```json
{
  "receivable_id": "uuid",
  "receivable_installment_id": "uuid",
  "payment_id": "uuid",
  "bank_account_id": "uuid",
  "paid_at": "datetime",
  "amount": "13500.00",
  "interest_amount": "0.00",
  "penalty_amount": "0.00",
  "discount_amount": "0.00",
  "fee_amount": "0.00",
  "payment_method": "PIX",
  "transaction_reference": "masked-reference",
  "document_id": "uuid",
  "notes": null
}
```

Validações:

* conta e parcela abertas;
* valor positivo;
* conta bancária ativa;
* moeda compatível;
* valor não superior ao saldo sem política de crédito;
* referência externa não duplicada;
* alocação correta;
* idempotência obrigatória;
* comprovante quando exigido;
* data coerente.

Eventos possíveis:

```text
financial.receivable_paid
financial.receivable_partially_paid
financial.financial_transaction_created
```

---

## `AllocateReceivablePaymentCommand`

Aloca um pagamento a uma ou mais parcelas.

Permissão:

```text
financial.receivable.payment.allocate
```

Payload:

```json
{
  "payment_id": "uuid",
  "allocations": [
    {
      "receivable_installment_id": "uuid",
      "principal_amount": "10000.00",
      "interest_amount": "100.00",
      "penalty_amount": "50.00",
      "discount_amount": "0.00"
    }
  ],
  "unallocated_amount_strategy": "KEEP_AS_CUSTOMER_CREDIT"
}
```

Estratégias:

```text
KEEP_AS_CUSTOMER_CREDIT
REFUND
ALLOCATE_TO_NEXT_INSTALLMENT
REJECT
MANUAL
```

Validações:

* pagamento existente;
* soma das alocações não superior ao pagamento;
* parcelas do mesmo cliente ou política permitida;
* valores não negativos;
* não duplicar alocação;
* saldo e crédito recalculados.

Evento resultante:

```text
financial.receivable_payment_allocated
```

---

## `ReverseReceivablePaymentCommand`

Estorna um recebimento.

Permissão:

```text
financial.receivable.payment.reverse
```

Payload:

```json
{
  "payment_id": "uuid",
  "reason_code": "BANK_REVERSAL",
  "reason": "Pagamento estornado pelo banco",
  "reversed_at": "datetime",
  "reversal_document_id": "uuid"
}
```

Validações:

* pagamento registrado;
* não estornado anteriormente;
* período contábil aberto ou autorização especial;
* lançamento compensatório;
* conciliação avaliada;
* evidência;
* não excluir transação original.

Eventos resultantes:

```text
financial.receivable_payment_reversed
financial.financial_transaction_reversed
```

---

## `WriteOffReceivableCommand`

Realiza baixa sem recebimento financeiro.

Permissão:

```text
financial.receivable.write_off
```

Payload:

```json
{
  "receivable_id": "uuid",
  "receivable_installment_id": "uuid",
  "write_off_reason_code": "UNCOLLECTIBLE",
  "reason": "Crédito considerado irrecuperável",
  "write_off_amount": "1000.00",
  "written_off_at": "datetime",
  "approval_document_id": "uuid"
}
```

Validações:

* saldo aberto;
* alçada;
* motivo permitido;
* valor não superior ao saldo;
* impacto contábil e fiscal;
* documentação;
* lançamento de perda;
* histórico preservado.

Eventos resultantes:

```text
financial.receivable_written_off
financial.financial_transaction_created
```

---

## `CancelReceivableCommand`

Cancela uma conta a receber.

Permissão:

```text
financial.receivable.cancel
```

Payload:

```json
{
  "receivable_id": "uuid",
  "reason_code": "SOURCE_CANCELLED",
  "reason": "Contrato cancelado",
  "cancelled_at": "datetime"
}
```

Validações:

* pagamentos existentes;
* créditos;
* documento fiscal;
* origem;
* não cancelar saldo já pago sem estorno;
* gerar compensações;
* permissão especial quando necessário.

Evento resultante:

```text
financial.receivable_cancelled
```

---

## `ReopenReceivableCommand`

Reabre conta cancelada ou encerrada.

Permissão:

```text
financial.receivable.reopen
```

Payload:

```json
{
  "receivable_id": "uuid",
  "reason": "Contrato reativado",
  "reopened_at": "datetime"
}
```

Validações:

* conta elegível;
* origem válida;
* período financeiro;
* cobranças reavaliadas;
* preservar estado anterior.

Evento resultante:

```text
financial.receivable_reopened
```

---

## `MarkReceivableOverdueCommand`

Marca parcela como vencida.

Permissão:

```text
financial.receivable.mark_overdue
```

Payload:

```json
{
  "receivable_installment_id": "uuid",
  "evaluated_at": "datetime",
  "outstanding_amount": "13500.00"
}
```

Validações:

* data atual posterior ao vencimento;
* saldo aberto;
* não marcar parcelas canceladas;
* processamento idempotente.

Evento resultante:

```text
financial.receivable_overdue
```

---

## `MarkReceivableDisputedCommand`

Registra contestação do cliente.

Permissão:

```text
financial.receivable.dispute.open
```

Payload:

```json
{
  "receivable_installment_id": "uuid",
  "customer_id": "uuid",
  "reason_code": "AMOUNT_DISPUTE",
  "reason": "Cliente contesta o valor cobrado",
  "opened_at": "datetime",
  "evidence_document_ids": [
    "uuid"
  ]
}
```

Validações:

* parcela aberta;
* cliente correspondente;
* motivo;
* suspender cobrança automática conforme política;
* preservar valores originais.

Evento resultante:

```text
financial.receivable_dispute_opened
```

---

## `ResolveReceivableDisputeCommand`

Resolve contestação.

Permissão:

```text
financial.receivable.dispute.resolve
```

Payload:

```json
{
  "receivable_dispute_id": "uuid",
  "resolution_code": "AMOUNT_ADJUSTED",
  "resolution": "Valor corrigido conforme contrato",
  "resolved_at": "datetime",
  "adjustment_amount": "500.00",
  "document_id": "uuid"
}
```

Validações:

* contestação aberta;
* resolução autorizada;
* ajuste dentro da alçada;
* documento;
* cobrança e saldo recalculados.

Eventos resultantes:

```text
financial.receivable_dispute_resolved
financial.receivable_discount_applied
```

quando houver ajuste.

---

# 90. Contas a pagar

## `CreatePayableCommand`

Cria uma conta a pagar.

Permissão:

```text
financial.payable.create
```

Payload:

```json
{
  "supplier_id": "uuid",
  "purchase_order_id": "uuid",
  "purchase_receipt_id": "uuid",
  "maintenance_order_id": "uuid",
  "code": "PAY-000001",
  "description": "Compra de MDF",
  "document_number": "NF-12345",
  "issue_date": "date",
  "competence_date": "date",
  "currency": "BRL",
  "total_amount": "1500.00",
  "payment_method": "BANK_TRANSFER",
  "bank_account_id": "uuid",
  "cost_center_id": "uuid",
  "category_id": "uuid",
  "installments": [
    {
      "installment_number": 1,
      "due_date": "date",
      "amount": "1500.00"
    }
  ],
  "notes": null
}
```

Validações:

* fornecedor ativo;
* origem válida;
* valor positivo;
* soma das parcelas igual ao total;
* conta bancária e classificações válidas;
* código único;
* impedir duplicidade por fornecedor, documento e origem;
* idempotência quando criada por evento de compra;
* retenções avaliadas quando aplicáveis.

Evento resultante:

```text
financial.payable_created
```

---

## `CreatePayableFromPurchaseOrderCommand`

Cria conta a pagar a partir de um pedido ou recebimento.

Permissão:

```text
financial.payable.create_from_purchase_order
```

Payload:

```json
{
  "purchase_order_id": "uuid",
  "purchase_receipt_id": "uuid",
  "supplier_id": "uuid",
  "supplier_document_number": "NF-12345",
  "payment_terms": {},
  "bank_account_id": "uuid",
  "cost_center_id": "uuid",
  "category_id": "uuid",
  "recognition_strategy": "ON_RECEIPT"
}
```

Estratégias:

```text
ON_ORDER_APPROVAL
ON_SUPPLIER_CONFIRMATION
ON_RECEIPT
ON_FISCAL_DOCUMENT
MANUAL
```

Validações:

* pedido aprovado;
* recebimento quando exigido;
* fornecedor correspondente;
* valores reconciliados;
* não duplicar obrigação;
* documento fiscal quando exigido;
* idempotência.

Evento resultante:

```text
financial.payable_created
```

---

## `UpdatePayableCommand`

Atualiza conta ainda editável.

Permissão:

```text
financial.payable.update
```

Payload:

```json
{
  "payable_id": "uuid",
  "description": "Compra de materiais",
  "competence_date": "date",
  "bank_account_id": "uuid",
  "cost_center_id": "uuid",
  "category_id": "uuid",
  "notes": "Descrição revisada"
}
```

Validações:

* conta aberta;
* não alterar valor já pago;
* origem e fornecedor preservados;
* classificações válidas;
* concorrência otimista.

Evento resultante:

```text
financial.payable_updated
```

---

## `AddPayableInstallmentCommand`

Adiciona parcela.

Permissão:

```text
financial.payable.installment.create
```

Payload:

```json
{
  "payable_id": "uuid",
  "installment_number": 2,
  "due_date": "date",
  "amount": "750.00",
  "payment_method": "BANK_TRANSFER"
}
```

Validações:

* conta editável;
* número único;
* valor positivo;
* total coerente;
* nenhuma liquidação integral.

Evento resultante:

```text
financial.payable_installment_added
```

---

## `UpdatePayableInstallmentCommand`

Atualiza parcela aberta.

Permissão:

```text
financial.payable.installment.update
```

Payload:

```json
{
  "payable_installment_id": "uuid",
  "due_date": "date",
  "amount": "800.00",
  "payment_method": "PIX",
  "notes": "Vencimento alterado pelo fornecedor"
}
```

Validações:

* parcela aberta;
* valor não inferior ao pago;
* datas válidas;
* documento do fornecedor quando necessário;
* concorrência otimista.

Evento resultante:

```text
financial.payable_installment_updated
```

---

## `RemovePayableInstallmentCommand`

Remove parcela não paga.

Permissão:

```text
financial.payable.installment.remove
```

Payload:

```json
{
  "payable_installment_id": "uuid",
  "reason": "Parcela consolidada"
}
```

Validações:

* nenhuma alocação de pagamento;
* conta permanece válida;
* justificativa;
* histórico.

Evento resultante:

```text
financial.payable_installment_removed
```

---

## `ReschedulePayableInstallmentCommand`

Altera vencimento.

Permissão:

```text
financial.payable.installment.reschedule
```

Payload:

```json
{
  "payable_installment_id": "uuid",
  "new_due_date": "date",
  "reason_code": "SUPPLIER_NEGOTIATION",
  "reason": "Prazo renegociado",
  "agreement_document_id": "uuid"
}
```

Validações:

* parcela aberta;
* nova data válida;
* fornecedor correspondente;
* fluxo de caixa atualizado;
* histórico preservado.

Evento resultante:

```text
financial.payable_installment_rescheduled
```

---

## `ApprovePayableCommand`

Aprova uma conta para pagamento.

Permissão:

```text
financial.payable.approve
```

Payload:

```json
{
  "payable_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Documento e recebimento conferidos"
}
```

Validações:

* conta pendente de aprovação;
* origem e documento conferidos;
* fornecedor ativo;
* valor reconciliado;
* alçada;
* segregação de funções;
* não permitir autoaprovação quando proibida.

Evento resultante:

```text
financial.payable_approved
```

---

## `RejectPayableCommand`

Rejeita conta para correção.

Permissão:

```text
financial.payable.reject
```

Payload:

```json
{
  "payable_id": "uuid",
  "reason_code": "DOCUMENT_MISMATCH",
  "reason": "Valor do documento diverge do pedido"
}
```

Evento resultante:

```text
financial.payable_rejected
```

---

## `SchedulePayablePaymentCommand`

Agenda um pagamento.

Permissão:

```text
financial.payable.payment.schedule
```

Payload:

```json
{
  "payable_id": "uuid",
  "payable_installment_id": "uuid",
  "bank_account_id": "uuid",
  "scheduled_payment_date": "date",
  "scheduled_amount": "1500.00",
  "payment_method": "BANK_TRANSFER",
  "beneficiary_reference": "uuid",
  "notes": null
}
```

Validações:

* conta aprovada;
* parcela aberta;
* valor válido;
* conta bancária ativa;
* saldo ou limite avaliado;
* beneficiário validado;
* data válida;
* impedir agendamento duplicado;
* idempotência.

Evento resultante:

```text
financial.payable_payment_scheduled
```

---

## `ApproveScheduledPaymentCommand`

Aprova o pagamento agendado.

Permissão:

```text
financial.payable.payment.approve
```

Payload:

```json
{
  "scheduled_payment_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Pagamento autorizado"
}
```

Validações:

* agendamento pendente;
* alçada;
* segregação de funções;
* dados bancários do beneficiário;
* saldo projetado;
* não permitir aprovação após alteração sem revalidação.

Evento resultante:

```text
financial.payable_payment_approved
```

---

## `ExecutePayablePaymentCommand`

Registra ou solicita a execução do pagamento.

Permissão:

```text
financial.payable.payment.execute
```

Payload:

```json
{
  "scheduled_payment_id": "uuid",
  "payment_id": "uuid",
  "bank_account_id": "uuid",
  "executed_at": "datetime",
  "amount": "1500.00",
  "payment_method": "BANK_TRANSFER",
  "provider_transaction_reference": "masked-reference",
  "document_id": "uuid"
}
```

Validações:

* pagamento aprovado;
* parcela aberta;
* valor e conta correspondentes;
* integração autorizada quando automática;
* idempotência obrigatória;
* não registrar segredo;
* saldo e limite;
* confirmação bancária conforme política.

Eventos possíveis:

```text
financial.payable_paid
financial.payable_payment_processing
financial.financial_transaction_created
```

---

## `ConfirmPayablePaymentCommand`

Confirma pagamento processado pelo banco.

Permissão:

```text
financial.payable.payment.confirm
```

Payload:

```json
{
  "payment_id": "uuid",
  "provider_transaction_reference": "masked-reference",
  "confirmed_at": "datetime",
  "confirmed_amount": "1500.00",
  "bank_statement_entry_id": "uuid"
}
```

Validações:

* pagamento em processamento;
* confirmação autêntica;
* valor compatível;
* impedir confirmação duplicada;
* conciliação vinculável.

Evento resultante:

```text
financial.payable_paid
```

---

## `RegisterPayablePaymentFailureCommand`

Registra falha.

Permissão:

```text
financial.payable.payment.failure.register
```

Payload:

```json
{
  "payment_id": "uuid",
  "error_code": "INSUFFICIENT_FUNDS",
  "error_message_safe": "Saldo insuficiente",
  "failed_at": "datetime",
  "retryable": true
}
```

Validações:

* pagamento em processamento;
* erro seguro;
* não armazenar resposta bancária sensível;
* conta permanece aberta;
* política de nova tentativa.

Eventos possíveis:

```text
financial.payable_payment_failed
financial.payable_payment_retry_required
```

---

## `RetryPayablePaymentCommand`

Reagenda pagamento falho.

Permissão:

```text
financial.payable.payment.retry
```

Payload:

```json
{
  "payment_id": "uuid",
  "new_scheduled_date": "date",
  "bank_account_id": "uuid",
  "reason": "Saldo regularizado"
}
```

Validações:

* falha recuperável;
* parcela aberta;
* dados revalidados;
* nova aprovação quando exigida.

Evento resultante:

```text
financial.payable_payment_rescheduled
```

---

## `ReversePayablePaymentCommand`

Estorna pagamento.

Permissão:

```text
financial.payable.payment.reverse
```

Payload:

```json
{
  "payment_id": "uuid",
  "reason_code": "BANK_REVERSAL",
  "reason": "Pagamento devolvido pelo banco",
  "reversed_at": "datetime",
  "document_id": "uuid"
}
```

Validações:

* pagamento confirmado;
* não estornado;
* período permitido;
* lançamento compensatório;
* conciliação;
* documento;
* não excluir registro original.

Eventos resultantes:

```text
financial.payable_payment_reversed
financial.financial_transaction_reversed
```

---

## `ApplyPayableDiscountCommand`

Registra desconto obtido.

Permissão:

```text
financial.payable.discount.apply
```

Payload:

```json
{
  "payable_installment_id": "uuid",
  "discount_amount": "100.00",
  "reason": "Desconto por pagamento antecipado",
  "effective_until": "date"
}
```

Validações:

* saldo aberto;
* desconto não superior ao saldo;
* condição comprovada;
* valor final não negativo.

Evento resultante:

```text
financial.payable_discount_applied
```

---

## `ApplyPayableInterestCommand`

Registra juros ou encargos.

Permissão:

```text
financial.payable.interest.apply
```

Payload:

```json
{
  "payable_installment_id": "uuid",
  "interest_amount": "50.00",
  "penalty_amount": "20.00",
  "reason": "Pagamento após o vencimento",
  "supplier_document_id": "uuid"
}
```

Validações:

* saldo aberto;
* valores não negativos;
* documento ou regra contratual;
* não duplicar encargo;
* alçada quando necessário.

Evento resultante:

```text
financial.payable_charges_applied
```

---

## `CancelPayableCommand`

Cancela obrigação.

Permissão:

```text
financial.payable.cancel
```

Payload:

```json
{
  "payable_id": "uuid",
  "reason_code": "PURCHASE_CANCELLED",
  "reason": "Pedido de compra cancelado",
  "cancelled_at": "datetime"
}
```

Validações:

* pagamentos existentes;
* pedido ou documento fiscal;
* não cancelar valor pago sem estorno;
* créditos com fornecedor;
* compensações;
* autorização.

Evento resultante:

```text
financial.payable_cancelled
```

---

## `ReopenPayableCommand`

Reabre obrigação.

Permissão:

```text
financial.payable.reopen
```

Payload:

```json
{
  "payable_id": "uuid",
  "reason": "Pedido reativado",
  "reopened_at": "datetime"
}
```

Validações:

* conta elegível;
* origem válida;
* período financeiro;
* pagamento e conciliação reavaliados.

Evento resultante:

```text
financial.payable_reopened
```

---

## `MarkPayableOverdueCommand`

Marca parcela vencida.

Permissão:

```text
financial.payable.mark_overdue
```

Payload:

```json
{
  "payable_installment_id": "uuid",
  "evaluated_at": "datetime",
  "outstanding_amount": "1500.00"
}
```

Validações:

* vencimento ultrapassado;
* saldo aberto;
* não duplicar processamento.

Evento resultante:

```text
financial.payable_overdue
```

---

# 91. Transações financeiras

## `CreateFinancialTransactionCommand`

Cria uma transação financeira manual.

Permissão:

```text
financial.transaction.create
```

Payload:

```json
{
  "transaction_type": "OUTFLOW",
  "bank_account_id": "uuid",
  "transaction_date": "date",
  "competence_date": "date",
  "amount": "500.00",
  "currency": "BRL",
  "description": "Despesa operacional",
  "category_id": "uuid",
  "cost_center_id": "uuid",
  "counterparty_type": "SUPPLIER",
  "counterparty_id": "uuid",
  "source_type": "MANUAL",
  "source_id": null,
  "document_id": "uuid",
  "notes": null
}
```

Tipos:

```text
INFLOW
OUTFLOW
TRANSFER_IN
TRANSFER_OUT
ADJUSTMENT
REVERSAL
FEE
INTEREST
INVESTMENT
WITHDRAWAL
DEPOSIT
```

Validações:

* valor positivo;
* conta ativa;
* moeda compatível;
* categoria e centro válidos;
* data válida;
* contraparte quando exigida;
* documento conforme política;
* idempotência;
* transação não substitui conta a pagar ou receber quando estas forem obrigatórias.

Evento resultante:

```text
financial.financial_transaction_created
```

---

## `UpdateFinancialTransactionCommand`

Atualiza transação ainda não conciliada.

Permissão:

```text
financial.transaction.update
```

Payload:

```json
{
  "financial_transaction_id": "uuid",
  "description": "Despesa operacional revisada",
  "category_id": "uuid",
  "cost_center_id": "uuid",
  "competence_date": "date",
  "document_id": "uuid",
  "notes": "Classificação atualizada"
}
```

Validações:

* transação não conciliada;
* não alterar valor ou conta sem comando específico;
* classificações válidas;
* concorrência otimista;
* histórico de alterações.

Evento resultante:

```text
financial.financial_transaction_updated
```

---

## `ReclassifyFinancialTransactionCommand`

Reclassifica categoria ou centro de custo.

Permissão:

```text
financial.transaction.reclassify
```

Payload:

```json
{
  "financial_transaction_id": "uuid",
  "new_category_id": "uuid",
  "new_cost_center_id": "uuid",
  "reason": "Classificação inicial incorreta"
}
```

Validações:

* transação existente;
* período aberto ou autorização;
* classificação válida;
* justificativa;
* histórico preservado.

Evento resultante:

```text
financial.financial_transaction_reclassified
```

---

## `ReverseFinancialTransactionCommand`

Estorna uma transação.

Permissão:

```text
financial.transaction.reverse
```

Payload:

```json
{
  "financial_transaction_id": "uuid",
  "reason_code": "ENTRY_ERROR",
  "reason": "Lançamento duplicado",
  "reversed_at": "datetime",
  "document_id": "uuid"
}
```

Validações:

* transação não estornada;
* não excluir original;
* conciliação avaliada;
* período financeiro;
* lançamento compensatório;
* autorização.

Eventos resultantes:

```text
financial.financial_transaction_reversed
financial.financial_transaction_created
```

---

## `TransferBetweenBankAccountsCommand`

Transfere valores entre contas.

Permissão:

```text
financial.bank_account.transfer
```

Payload:

```json
{
  "source_bank_account_id": "uuid",
  "target_bank_account_id": "uuid",
  "amount": "5000.00",
  "currency": "BRL",
  "transfer_date": "date",
  "description": "Transferência para conta operacional",
  "fee_amount": "5.00",
  "document_id": "uuid"
}
```

Validações:

* contas distintas;
* contas ativas;
* moeda compatível ou conversão explícita;
* saldo e limite;
* valor positivo;
* idempotência;
* gerar dois lados vinculados;
* taxa em transação separada quando aplicável.

Eventos resultantes:

```text
financial.bank_transfer_created
financial.financial_transaction_created
```

---

## `ConfirmBankTransferCommand`

Confirma transferência processada.

Permissão:

```text
financial.bank_account.transfer.confirm
```

Payload:

```json
{
  "bank_transfer_id": "uuid",
  "confirmed_at": "datetime",
  "provider_reference": "masked-reference",
  "source_statement_entry_id": "uuid",
  "target_statement_entry_id": "uuid"
}
```

Validações:

* transferência pendente;
* confirmação autêntica;
* valores compatíveis;
* não duplicar;
* duas pontas reconciliáveis.

Evento resultante:

```text
financial.bank_transfer_confirmed
```

---

## `CancelBankTransferCommand`

Cancela transferência ainda não executada.

Permissão:

```text
financial.bank_account.transfer.cancel
```

Payload:

```json
{
  "bank_transfer_id": "uuid",
  "reason": "Transferência não será mais necessária"
}
```

Validações:

* transferência pendente;
* nenhuma confirmação bancária;
* preservar histórico.

Evento resultante:

```text
financial.bank_transfer_cancelled
```

---

## `RegisterBankFeeCommand`

Registra tarifa bancária.

Permissão:

```text
financial.bank_fee.register
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "statement_entry_id": "uuid",
  "fee_type": "ACCOUNT_MAINTENANCE",
  "amount": "35.00",
  "transaction_date": "date",
  "description": "Tarifa mensal"
}
```

Validações:

* conta ativa;
* valor positivo;
* não duplicar tarifa;
* classificação contábil;
* idempotência quando importada.

Evento resultante:

```text
financial.bank_fee_registered
```

---

## `RegisterFinancialAdjustmentCommand`

Registra ajuste financeiro controlado.

Permissão:

```text
financial.adjustment.register
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "adjustment_type": "BALANCE_CORRECTION",
  "amount": "-10.00",
  "transaction_date": "date",
  "reason_code": "RECONCILIATION_DIFFERENCE",
  "reason": "Diferença identificada na conciliação",
  "document_id": "uuid"
}
```

Validações:

* valor diferente de zero;
* autorização especial;
* motivo e evidência;
* período aberto;
* não alterar saldo diretamente;
* gerar transação de ajuste.

Evento resultante:

```text
financial.adjustment_registered
```

---

# 92. Categorias e centros de custo financeiros

## `CreateFinancialCategoryCommand`

Cria categoria financeira.

Permissão:

```text
financial.category.create
```

Payload:

```json
{
  "code": "MATERIAL_PURCHASE",
  "name": "Compra de materiais",
  "category_type": "EXPENSE",
  "parent_category_id": "uuid",
  "is_leaf": true,
  "default_cost_center_id": "uuid",
  "configuration": {}
}
```

Tipos:

```text
REVENUE
EXPENSE
TRANSFER
ASSET
LIABILITY
EQUITY
ADJUSTMENT
```

Validações:

* código único;
* categoria pai válida;
* impedir ciclo;
* tipo compatível com o pai;
* centro padrão válido.

Evento resultante:

```text
financial.category_created
```

---

## `UpdateFinancialCategoryCommand`

Atualiza categoria.

Permissão:

```text
financial.category.update
```

Payload:

```json
{
  "financial_category_id": "uuid",
  "name": "Materiais produtivos",
  "parent_category_id": "uuid",
  "default_cost_center_id": "uuid",
  "configuration": {}
}
```

Validações:

* categoria ativa;
* impedir ciclo;
* não alterar tipo estrutural com lançamentos sem migração;
* concorrência otimista.

Evento resultante:

```text
financial.category_updated
```

---

## `ArchiveFinancialCategoryCommand`

Arquiva categoria.

Permissão:

```text
financial.category.archive
```

Payload:

```json
{
  "financial_category_id": "uuid",
  "reason": "Categoria substituída",
  "replacement_category_id": "uuid"
}
```

Validações:

* lançamentos futuros;
* categoria substituta;
* filhos;
* histórico preservado.

Evento resultante:

```text
financial.category_archived
```

---

## `CreateFinancialCostCenterCommand`

Cria centro de custo financeiro quando não for reutilizado diretamente de Organization.

Permissão:

```text
financial.cost_center.create
```

Payload:

```json
{
  "code": "PRODUCTION",
  "name": "Produção",
  "organization_cost_center_id": "uuid",
  "parent_cost_center_id": null,
  "branch_id": "uuid",
  "configuration": {}
}
```

Validações:

* código único;
* vínculo organizacional válido;
* impedir ciclo;
* filial compatível.

Evento resultante:

```text
financial.cost_center_created
```

---

## `UpdateFinancialCostCenterCommand`

Atualiza centro de custo.

Permissão:

```text
financial.cost_center.update
```

Payload:

```json
{
  "financial_cost_center_id": "uuid",
  "name": "Produção industrial",
  "parent_cost_center_id": "uuid",
  "branch_id": "uuid"
}
```

Evento resultante:

```text
financial.cost_center_updated
```

---

## `ArchiveFinancialCostCenterCommand`

Arquiva centro de custo.

Permissão:

```text
financial.cost_center.archive
```

Payload:

```json
{
  "financial_cost_center_id": "uuid",
  "reason": "Setor reorganizado",
  "replacement_cost_center_id": "uuid"
}
```

Validações:

* lançamentos futuros;
* orçamentos;
* centro substituto;
* histórico.

Evento resultante:

```text
financial.cost_center_archived
```

---

# 93. Rateio financeiro

## `CreateFinancialAllocationRuleCommand`

Cria regra de rateio.

Permissão:

```text
financial.allocation_rule.create
```

Payload:

```json
{
  "code": "ADMINISTRATIVE_EXPENSE_SPLIT",
  "name": "Rateio de despesas administrativas",
  "allocation_basis": "FIXED_PERCENTAGE",
  "lines": [
    {
      "cost_center_id": "uuid",
      "percentage": "60.00"
    },
    {
      "cost_center_id": "uuid",
      "percentage": "40.00"
    }
  ],
  "effective_from": "date",
  "effective_until": null
}
```

Bases:

```text
FIXED_PERCENTAGE
REVENUE
HEADCOUNT
AREA
PRODUCTION_HOURS
MACHINE_HOURS
DIRECT_COST
CUSTOM
```

Validações:

* código único;
* linhas válidas;
* percentuais totalizam 100 quando fixos;
* centros ativos;
* vigência coerente.

Evento resultante:

```text
financial.allocation_rule_created
```

---

## `UpdateFinancialAllocationRuleCommand`

Atualiza regra futura.

Permissão:

```text
financial.allocation_rule.update
```

Payload:

```json
{
  "financial_allocation_rule_id": "uuid",
  "name": "Rateio administrativo revisado",
  "lines": [],
  "effective_from": "date",
  "effective_until": null
}
```

Validações:

* regra ativa;
* não alterar rateios já processados;
* vigência e total;
* concorrência otimista.

Evento resultante:

```text
financial.allocation_rule_updated
```

---

## `ApplyFinancialAllocationCommand`

Aplica rateio a uma transação.

Permissão:

```text
financial.allocation.apply
```

Payload:

```json
{
  "financial_transaction_id": "uuid",
  "financial_allocation_rule_id": "uuid",
  "allocation_date": "date",
  "lines": [
    {
      "cost_center_id": "uuid",
      "amount": "600.00"
    },
    {
      "cost_center_id": "uuid",
      "amount": "400.00"
    }
  ]
}
```

Validações:

* transação elegível;
* soma igual ao valor rateável;
* centros ativos;
* não duplicar rateio;
* regra vigente;
* valores reproduzíveis.

Evento resultante:

```text
financial.transaction_allocated
```

---

## `ReverseFinancialAllocationCommand`

Estorna rateio.

Permissão:

```text
financial.allocation.reverse
```

Payload:

```json
{
  "financial_allocation_id": "uuid",
  "reason": "Regra de rateio incorreta"
}
```

Validações:

* rateio existente;
* período aberto;
* não excluir original;
* nova classificação será realizada separadamente.

Evento resultante:

```text
financial.transaction_allocation_reversed
```

---

# 94. Fluxo de caixa

## `CreateCashFlowForecastCommand`

Cria uma projeção de fluxo de caixa.

Permissão:

```text
financial.cash_flow_forecast.create
```

Payload:

```json
{
  "code": "CASHFLOW-2026-08",
  "name": "Fluxo de caixa de agosto",
  "period_start": "date",
  "period_end": "date",
  "currency": "BRL",
  "bank_account_ids": [
    "uuid"
  ],
  "include_receivables": true,
  "include_payables": true,
  "include_planned_transactions": true,
  "scenario": "BASE"
}
```

Cenários:

```text
BASE
OPTIMISTIC
PESSIMISTIC
CUSTOM
```

Validações:

* período válido;
* contas ativas;
* moeda;
* código único;
* dados-base disponíveis.

Evento resultante:

```text
financial.cash_flow_forecast_created
```

---

## `RecalculateCashFlowForecastCommand`

Recalcula uma projeção.

Permissão:

```text
financial.cash_flow_forecast.recalculate
```

Payload:

```json
{
  "cash_flow_forecast_id": "uuid",
  "as_of_at": "datetime",
  "include_new_transactions": true,
  "reason": "Novos pagamentos e recebimentos registrados"
}
```

Validações:

* projeção ativa;
* dados disponíveis;
* versão anterior preservada;
* cálculo reproduzível.

Evento resultante:

```text
financial.cash_flow_forecast_recalculated
```

---

## `CreateCashFlowScenarioCommand`

Cria cenário alternativo.

Permissão:

```text
financial.cash_flow_scenario.create
```

Payload:

```json
{
  "cash_flow_forecast_id": "uuid",
  "scenario_name": "Queda de receitas",
  "scenario_type": "CUSTOM",
  "assumptions": {
    "receivable_delay_days": 15,
    "revenue_reduction_percentage": "20.00",
    "expense_increase_percentage": "5.00"
  }
}
```

Validações:

* projeção existente;
* premissas válidas;
* não alterar cenário-base;
* identificação explícita de simulação.

Evento resultante:

```text
financial.cash_flow_scenario_created
```

---

## `ArchiveCashFlowForecastCommand`

Arquiva projeção.

Permissão:

```text
financial.cash_flow_forecast.archive
```

Payload:

```json
{
  "cash_flow_forecast_id": "uuid",
  "reason": "Período encerrado"
}
```

Evento resultante:

```text
financial.cash_flow_forecast_archived
```

---

# 95. Orçamento financeiro

## `CreateFinancialBudgetCommand`

Cria orçamento financeiro.

Permissão:

```text
financial.budget.create
```

Payload:

```json
{
  "code": "BUDGET-2027",
  "name": "Orçamento anual 2027",
  "period_start": "date",
  "period_end": "date",
  "currency": "BRL",
  "budget_type": "ANNUAL",
  "version_number": 1,
  "lines": [
    {
      "category_id": "uuid",
      "cost_center_id": "uuid",
      "period": "2027-01",
      "budgeted_amount": "10000.00"
    }
  ]
}
```

Tipos:

```text
MONTHLY
QUARTERLY
ANNUAL
PROJECT
DEPARTMENT
CUSTOM
```

Validações:

* código único;
* período válido;
* linhas e classificações;
* valores não negativos;
* moeda;
* versão;
* evitar sobreposição incompatível.

Evento resultante:

```text
financial.budget_created
```

---

## `CreateFinancialBudgetVersionCommand`

Cria nova versão.

Permissão:

```text
financial.budget.version.create
```

Payload:

```json
{
  "financial_budget_id": "uuid",
  "based_on_version_id": "uuid",
  "change_reason": "Revisão após definição de metas"
}
```

Evento resultante:

```text
financial.budget_version_created
```

---

## `UpdateFinancialBudgetLinesCommand`

Atualiza linhas em rascunho.

Permissão:

```text
financial.budget.lines.update
```

Payload:

```json
{
  "financial_budget_version_id": "uuid",
  "lines": [
    {
      "category_id": "uuid",
      "cost_center_id": "uuid",
      "period": "2027-01",
      "budgeted_amount": "12000.00",
      "notes": "Ajuste previsto"
    }
  ]
}
```

Validações:

* versão em rascunho;
* período dentro do orçamento;
* classificações válidas;
* valores;
* linhas únicas por dimensão.

Evento resultante:

```text
financial.budget_lines_updated
```

---

## `SubmitFinancialBudgetCommand`

Envia orçamento para aprovação.

Permissão:

```text
financial.budget.submit
```

Payload:

```json
{
  "financial_budget_version_id": "uuid",
  "submitted_at": "datetime",
  "notes": "Orçamento consolidado"
}
```

Validações:

* versão completa;
* linhas válidas;
* totais;
* fluxo de aprovação;
* nenhuma inconsistência bloqueante.

Evento resultante:

```text
financial.budget_submitted
```

---

## `ApproveFinancialBudgetCommand`

Aprova orçamento.

Permissão:

```text
financial.budget.approve
```

Payload:

```json
{
  "financial_budget_version_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Orçamento aprovado pela diretoria"
}
```

Validações:

* submetido;
* alçada;
* segregação;
* período;
* versão atual;
* torna-se referência oficial.

Evento resultante:

```text
financial.budget_approved
```

---

## `RejectFinancialBudgetCommand`

Rejeita orçamento.

Permissão:

```text
financial.budget.reject
```

Payload:

```json
{
  "financial_budget_version_id": "uuid",
  "reason": "Despesas administrativas acima da meta"
}
```

Evento resultante:

```text
financial.budget_rejected
```

---

## `CloseFinancialBudgetCommand`

Encerra orçamento de período concluído.

Permissão:

```text
financial.budget.close
```

Payload:

```json
{
  "financial_budget_id": "uuid",
  "closed_at": "datetime",
  "closing_notes": "Exercício encerrado"
}
```

Validações:

* período concluído;
* nenhuma revisão aberta;
* valores realizados consolidados;
* histórico preservado.

Evento resultante:

```text
financial.budget_closed
```

---

# 96. Continuação

A próxima subparte continuará com:

```text
Financial:
- Conciliação bancária
- Cobrança
- Adiantamentos
- Reembolsos
- Fechamento financeiro
- Integrações e regras finais
```

Fim da Parte 3E-B.
97. Comandos de Financial — Conciliação Bancária
CreateBankReconciliationCommand

Cria uma nova conciliação bancária.

Permissão:

financial.bank_reconciliation.create

Payload:

{
  "bank_account_id": "uuid",
  "statement_period_start": "date",
  "statement_period_end": "date",
  "opening_balance": "10000.00",
  "closing_balance": "15482.35",
  "statement_reference": "Extrato Agosto/2026",
  "import_source": "OFX"
}

Validações:

conta bancária ativa;
período não sobreposto a conciliações fechadas;
saldo inicial compatível;
período cronologicamente válido;
não existir conciliação aberta para o mesmo intervalo;
moeda compatível com a conta.

Evento resultante:

financial.bank_reconciliation_created
ImportBankStatementCommand

Importa extrato bancário.

Permissão:

financial.bank_statement.import

Payload:

{
  "bank_reconciliation_id": "uuid",
  "provider": "OFX",
  "document_id": "uuid",
  "imported_at": "datetime"
}

Validações:

formato suportado;
arquivo íntegro;
conta bancária correspondente;
impedir importação duplicada;
preservar arquivo original para auditoria.

Eventos resultantes:

financial.bank_statement_imported
financial.bank_statement_entries_created
MatchBankStatementEntryCommand

Realiza a conciliação de um lançamento do extrato.

Permissão:

financial.bank_reconciliation.match

Payload:

{
  "statement_entry_id": "uuid",
  "financial_transaction_id": "uuid",
  "matching_method": "AUTOMATIC",
  "confidence_score": "0.98"
}

Métodos:

AUTOMATIC
MANUAL
RULE
AI

Validações:

lançamento ainda não conciliado;
transação financeira existente;
valores compatíveis;
moeda compatível;
impedir dupla conciliação;
registrar método utilizado.

Evento resultante:

financial.bank_statement_entry_matched
UnmatchBankStatementEntryCommand

Remove uma conciliação realizada.

Permissão:

financial.bank_reconciliation.unmatch

Payload:

{
  "statement_entry_id": "uuid",
  "reason": "Conciliação incorreta"
}

Validações:

lançamento conciliado;
conciliação ainda aberta;
justificativa obrigatória;
preservar histórico da conciliação anterior.

Evento resultante:

financial.bank_statement_entry_unmatched
CreateBankReconciliationAdjustmentCommand

Cria um ajuste identificado durante a conciliação.

Permissão:

financial.bank_reconciliation.adjustment.create

Payload:

{
  "bank_reconciliation_id": "uuid",
  "adjustment_type": "MISSING_TRANSACTION",
  "amount": "-120.50",
  "reason": "Tarifa não registrada",
  "document_id": "uuid"
}

Tipos iniciais:

MISSING_TRANSACTION
BANK_FEE
INTEREST
REVERSAL
ROUNDING
OTHER

Validações:

valor diferente de zero;
justificativa obrigatória;
documento quando exigido;
período financeiro aberto;
autorização conforme política financeira.

Evento resultante:

financial.bank_reconciliation_adjustment_created

98. Comandos de Financial — Cobranças
CreateAccountsReceivableCommand

Cria um título a receber.

Permissão:

financial.accounts_receivable.create

Payload:

{
  "customer_id": "uuid",
  "origin_type": "SALES_ORDER",
  "origin_id": "uuid",
  "document_number": "REC-000001",
  "issue_date": "date",
  "due_date": "date",
  "amount": "2500.00",
  "currency": "BRL",
  "description": "Parcela 1/3"
}

Validações:

cliente ativo;
valor maior que zero;
vencimento válido;
documento único por Tenant;
origem válida quando informada;
moeda suportada.

Evento resultante:

financial.accounts_receivable_created
UpdateAccountsReceivableCommand

Atualiza título ainda não liquidado.

Permissão:

financial.accounts_receivable.update

Payload:

{
  "accounts_receivable_id": "uuid",
  "due_date": "date",
  "description": "Primeira parcela",
  "notes": "Negociação realizada"
}

Validações:

título aberto;
concorrência otimista;
alterações permitidas pela política financeira.

Evento resultante:

financial.accounts_receivable_updated
CancelAccountsReceivableCommand

Cancela um título a receber.

Permissão:

financial.accounts_receivable.cancel

Payload:

{
  "accounts_receivable_id": "uuid",
  "reason_code": "CUSTOMER_CANCELLATION",
  "reason": "Pedido cancelado"
}

Validações:

título não liquidado;
não possuir cobrança ativa;
autorização conforme política.

Evento resultante:

financial.accounts_receivable_cancelled
GeneratePixChargeCommand

Gera cobrança PIX.

Permissão:

financial.pix.generate

Payload:

{
  "accounts_receivable_id": "uuid",
  "expiration_at": "datetime",
  "allow_after_due_date": false
}

Validações:

título ativo;
valor válido;
integração bancária disponível;
não existir PIX ativo quando não permitido.

Evento resultante:

financial.pix_charge_generated
GenerateBankSlipCommand

Gera boleto bancário.

Permissão:

financial.bank_slip.generate

Payload:

{
  "accounts_receivable_id": "uuid",
  "bank_account_id": "uuid",
  "instruction_set": {},
  "interest_configuration": {},
  "fine_configuration": {}
}

Validações:

conta habilitada;
carteira configurada;
convênio ativo;
vencimento válido;
integração disponível.

Evento resultante:

financial.bank_slip_generated
GeneratePaymentLinkCommand

Gera link de pagamento.

Permissão:

financial.payment_link.generate

Payload:

{
  "accounts_receivable_id": "uuid",
  "provider": "MERCADO_PAGO",
  "accepted_methods": [
    "PIX",
    "CREDIT_CARD"
  ],
  "expiration_at": "datetime"
}

Validações:

provedor configurado;
integração ativa;
título aberto;
valor válido.

Evento resultante:

financial.payment_link_generated
RegisterIncomingPaymentCommand

Registra recebimento financeiro.

Permissão:

financial.payment.register

Payload:

{
  "accounts_receivable_id": "uuid",
  "payment_method": "PIX",
  "received_amount": "2500.00",
  "received_at": "datetime",
  "bank_account_id": "uuid",
  "external_reference": "string"
}

Validações:

título aberto;
valor recebido positivo;
conta válida;
impedir duplicidade;
permitir recebimento parcial conforme configuração.

Evento resultante:

financial.payment_received
ReverseIncomingPaymentCommand

Estorna um recebimento.

Permissão:

financial.payment.reverse

Payload:

{
  "payment_id": "uuid",
  "reason": "Pagamento registrado incorretamente"
}

Validações:

pagamento existente;
período financeiro aberto;
autorização especial quando necessário;
preservar trilha de auditoria.

Evento resultante:

financial.payment_reversed
WriteOffAccountsReceivableCommand

Realiza baixa por perda.

Permissão:

financial.accounts_receivable.write_off

Payload:

{
  "accounts_receivable_id": "uuid",
  "reason_code": "UNCOLLECTIBLE",
  "reason": "Crédito considerado irrecuperável"
}

Validações:

título aberto;
autorização financeira;
justificativa obrigatória;
política contábil respeitada.

Evento resultante:

financial.accounts_receivable_written_off
RenegotiateAccountsReceivableCommand

Renegocia um título.

Permissão:

financial.accounts_receivable.renegotiate

Payload:

{
  "accounts_receivable_id": "uuid",
  "new_installments": 3,
  "first_due_date": "date",
  "interest_rate": "2.50"
}

Validações:

título aberto;
política de renegociação;
parcelas válidas;
juros permitidos;
histórico preservado.

Eventos resultantes:

financial.accounts_receivable_renegotiated
financial.accounts_receivable_created
CloseAccountsReceivableCommand

Encerra definitivamente um título.

Permissão:

financial.accounts_receivable.close

Payload:

{
  "accounts_receivable_id": "uuid",
  "closure_reason": "FULLY_PAID"
}

Validações:

saldo igual a zero;
nenhuma cobrança pendente;
nenhuma contestação aberta.

Evento resultante:

financial.accounts_receivable_closed

# 99. Comandos de Financial — Contas a Pagar

## `CreateAccountsPayableCommand`

Cria um título de contas a pagar.

Permissão:

```text
financial.accounts_payable.create
```

Payload:

```json
{
  "supplier_id": "uuid",
  "origin_type": "PURCHASE_ORDER",
  "origin_id": "uuid",
  "document_number": "PAG-000001",
  "issue_date": "date",
  "due_date": "date",
  "amount": "1850.00",
  "currency": "BRL",
  "description": "Compra de MDF"
}
```

Validações:

- fornecedor ativo;
- valor maior que zero;
- documento único por Tenant;
- vencimento válido;
- origem existente quando informada;
- moeda suportada.

Evento resultante:

```text
financial.accounts_payable_created
```

---

## `UpdateAccountsPayableCommand`

Atualiza um título ainda não liquidado.

Permissão:

```text
financial.accounts_payable.update
```

Payload:

```json
{
  "accounts_payable_id": "uuid",
  "due_date": "date",
  "description": "Compra de MDF Branco TX",
  "notes": "Prazo renegociado"
}
```

Validações:

- título aberto;
- concorrência otimista;
- alterações permitidas pela política financeira.

Evento resultante:

```text
financial.accounts_payable_updated
```

---

## `CancelAccountsPayableCommand`

Cancela um título a pagar.

Permissão:

```text
financial.accounts_payable.cancel
```

Payload:

```json
{
  "accounts_payable_id": "uuid",
  "reason_code": "PURCHASE_CANCELLED",
  "reason": "Compra cancelada"
}
```

Validações:

- título não liquidado;
- nenhuma baixa registrada;
- autorização financeira.

Evento resultante:

```text
financial.accounts_payable_cancelled
```

---

## `SchedulePaymentCommand`

Agenda um pagamento.

Permissão:

```text
financial.accounts_payable.schedule_payment
```

Payload:

```json
{
  "accounts_payable_id": "uuid",
  "scheduled_date": "date",
  "bank_account_id": "uuid"
}
```

Validações:

- conta bancária ativa;
- vencimento válido;
- título aberto;
- saldo disponível conforme política.

Evento resultante:

```text
financial.payment_scheduled
```

---

## `RegisterOutgoingPaymentCommand`

Registra um pagamento realizado.

Permissão:

```text
financial.payment_out.register
```

Payload:

```json
{
  "accounts_payable_id": "uuid",
  "payment_method": "PIX",
  "paid_amount": "1850.00",
  "paid_at": "datetime",
  "bank_account_id": "uuid",
  "external_reference": "string"
}
```

Validações:

- título aberto;
- valor positivo;
- conta bancária válida;
- impedir pagamentos duplicados;
- permitir pagamento parcial conforme configuração.

Evento resultante:

```text
financial.payment_sent
```

---

## `ReverseOutgoingPaymentCommand`

Estorna um pagamento.

Permissão:

```text
financial.payment_out.reverse
```

Payload:

```json
{
  "payment_id": "uuid",
  "reason": "Pagamento realizado incorretamente"
}
```

Validações:

- pagamento existente;
- período financeiro aberto;
- autorização especial;
- preservar auditoria.

Evento resultante:

```text
financial.payment_sent_reversed
```

---

## `ApplySupplierCreditCommand`

Aplica crédito do fornecedor.

Permissão:

```text
financial.supplier_credit.apply
```

Payload:

```json
{
  "accounts_payable_id": "uuid",
  "credit_amount": "250.00",
  "credit_origin": "RETURN"
}
```

Validações:

- fornecedor correspondente;
- crédito disponível;
- valor compatível;
- impedir utilização duplicada.

Evento resultante:

```text
financial.supplier_credit_applied
```

---

## `RegisterAdvancePaymentCommand`

Registra adiantamento ao fornecedor.

Permissão:

```text
financial.advance_payment.register
```

Payload:

```json
{
  "supplier_id": "uuid",
  "amount": "5000.00",
  "bank_account_id": "uuid",
  "payment_date": "date",
  "description": "Entrada antecipada"
}
```

Validações:

- fornecedor ativo;
- valor positivo;
- conta bancária válida;
- autorização conforme política.

Evento resultante:

```text
financial.advance_payment_registered
```

---

## `AllocateAdvancePaymentCommand`

Vincula um adiantamento a um título.

Permissão:

```text
financial.advance_payment.allocate
```

Payload:

```json
{
  "advance_payment_id": "uuid",
  "accounts_payable_id": "uuid",
  "allocated_amount": "1500.00"
}
```

Validações:

- adiantamento disponível;
- fornecedor correspondente;
- valor compatível;
- impedir saldo negativo.

Evento resultante:

```text
financial.advance_payment_allocated
```

---

## `WriteOffAccountsPayableCommand`

Realiza baixa administrativa.

Permissão:

```text
financial.accounts_payable.write_off
```

Payload:

```json
{
  "accounts_payable_id": "uuid",
  "reason": "Diferença irrelevante"
}
```

Validações:

- política financeira;
- justificativa obrigatória;
- autorização.

Evento resultante:

```text
financial.accounts_payable_written_off
```

---

## `CloseAccountsPayableCommand`

Encerra definitivamente um título.

Permissão:

```text
financial.accounts_payable.close
```

Payload:

```json
{
  "accounts_payable_id": "uuid",
  "closure_reason": "FULLY_PAID"
}
```

Validações:

- saldo zerado;
- nenhuma pendência financeira;
- auditoria concluída.

Evento resultante:

```text
financial.accounts_payable_closed
```

---

**Próxima seção:** **#100. Comandos de Financial — Fluxo de Caixa e Tesouraria**
# 100. Comandos de Financial — Fluxo de Caixa e Tesouraria

## `CreateCashFlowProjectionCommand`

Cria uma projeção de fluxo de caixa.

Permissão:

```text
financial.cash_flow_projection.create
```

Payload:

```json
{
  "projection_name": "Fluxo Agosto/2026",
  "start_date": "date",
  "end_date": "date",
  "currency": "BRL",
  "include_forecast": true,
  "include_scheduled_payments": true,
  "include_accounts_receivable": true,
  "include_accounts_payable": true
}
```

Validações:

- período válido;
- data inicial menor que data final;
- moeda suportada;
- projeção única quando configurado.

Evento resultante:

```text
financial.cash_flow_projection_created
```

---

## `RecalculateCashFlowProjectionCommand`

Recalcula toda a projeção.

Permissão:

```text
financial.cash_flow_projection.recalculate
```

Payload:

```json
{
  "cash_flow_projection_id": "uuid"
}
```

Validações:

- projeção existente;
- período aberto;
- parâmetros válidos.

Evento resultante:

```text
financial.cash_flow_projection_recalculated
```

---

## `CreateCashTransferCommand`

Realiza transferência entre contas internas.

Permissão:

```text
financial.cash_transfer.create
```

Payload:

```json
{
  "source_bank_account_id": "uuid",
  "destination_bank_account_id": "uuid",
  "amount": "5000.00",
  "transfer_date": "date",
  "description": "Transferência para capital de giro"
}
```

Validações:

- contas diferentes;
- contas ativas;
- saldo suficiente;
- valor positivo.

Evento resultante:

```text
financial.cash_transfer_created
```

---

## `ReverseCashTransferCommand`

Estorna uma transferência.

Permissão:

```text
financial.cash_transfer.reverse
```

Payload:

```json
{
  "cash_transfer_id": "uuid",
  "reason": "Transferência incorreta"
}
```

Validações:

- transferência existente;
- período financeiro aberto;
- autorização adequada.

Evento resultante:

```text
financial.cash_transfer_reversed
```

---

## `RegisterCashDepositCommand`

Registra um depósito.

Permissão:

```text
financial.cash.deposit
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "amount": "3500.00",
  "deposit_date": "date",
  "origin": "CASH"
}
```

Validações:

- conta ativa;
- valor positivo;
- origem válida.

Evento resultante:

```text
financial.cash_deposit_registered
```

---

## `RegisterCashWithdrawalCommand`

Registra um saque.

Permissão:

```text
financial.cash.withdrawal
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "amount": "500.00",
  "withdrawal_date": "date",
  "reason": "Pequenas despesas"
}
```

Validações:

- saldo suficiente;
- conta ativa;
- valor positivo.

Evento resultante:

```text
financial.cash_withdrawal_registered
```

---

## `RegisterBankFeeCommand`

Registra uma tarifa bancária.

Permissão:

```text
financial.bank_fee.register
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "amount": "35.90",
  "reference_date": "date",
  "description": "Tarifa de manutenção"
}
```

Validações:

- conta ativa;
- valor positivo;
- categoria financeira configurada.

Evento resultante:

```text
financial.bank_fee_registered
```

---

## `RegisterBankInterestCommand`

Registra rendimento ou juros bancários.

Permissão:

```text
financial.bank_interest.register
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "amount": "27.43",
  "reference_date": "date",
  "interest_type": "POSITIVE"
}
```

Tipos:

```text
POSITIVE
NEGATIVE
```

Validações:

- conta válida;
- valor positivo;
- tipo informado.

Evento resultante:

```text
financial.bank_interest_registered
```

---

## `OpenCashRegisterCommand`

Abre um caixa.

Permissão:

```text
financial.cash_register.open
```

Payload:

```json
{
  "cash_register_id": "uuid",
  "opening_balance": "500.00",
  "opened_at": "datetime"
}
```

Validações:

- caixa fechado;
- saldo inicial informado;
- operador autorizado.

Evento resultante:

```text
financial.cash_register_opened
```

---

## `CloseCashRegisterCommand`

Fecha um caixa.

Permissão:

```text
financial.cash_register.close
```

Payload:

```json
{
  "cash_register_id": "uuid",
  "closing_balance": "2840.25",
  "closed_at": "datetime"
}
```

Validações:

- caixa aberto;
- movimentações encerradas;
- diferenças registradas quando existirem.

Evento resultante:

```text
financial.cash_register_closed
```

---

## `RegisterCashDifferenceCommand`

Registra diferença encontrada no fechamento.

Permissão:

```text
financial.cash_difference.register
```

Payload:

```json
{
  "cash_register_id": "uuid",
  "expected_amount": "2850.00",
  "actual_amount": "2840.25",
  "reason": "Diferença de troco"
}
```

Validações:

- caixa em fechamento;
- justificativa obrigatória;
- diferença calculada automaticamente.

Evento resultante:

```text
financial.cash_difference_registered
```

---

## `ApproveCashDifferenceCommand`

Aprova uma diferença de caixa.

Permissão:

```text
financial.cash_difference.approve
```

Payload:

```json
{
  "cash_difference_id": "uuid",
  "approved_by": "uuid"
}
```

Validações:

- diferença existente;
- usuário autorizado;
- segregação de funções.

Evento resultante:

```text
financial.cash_difference_approved
```

---

## `RejectCashDifferenceCommand`

Rejeita uma diferença de caixa.

Permissão:

```text
financial.cash_difference.reject
```

Payload:

```json
{
  "cash_difference_id": "uuid",
  "reason": "Necessária nova conferência"
}
```

Validações:

- diferença existente;
- justificativa obrigatória.

Evento resultante:

```text
financial.cash_difference_rejected
```

---

**Próxima seção:** **#101. Comandos de Financial — Cobranças Automáticas e Integrações Bancárias**
# 101. Comandos de Financial — Cobranças Automáticas e Integrações Bancárias

## `RegisterBankIntegrationCommand`

Registra uma integração bancária.

Permissão:

```text
financial.bank_integration.create
```

Payload:

```json
{
  "bank_provider": "SICREDI",
  "integration_type": "API",
  "client_id": "string",
  "client_secret": "encrypted",
  "certificate_id": "uuid",
  "environment": "PRODUCTION"
}
```

Validações:

- banco suportado;
- credenciais obrigatórias;
- certificado válido quando exigido;
- ambiente permitido;
- impedir duplicidade da integração.

Evento resultante:

```text
financial.bank_integration_registered
```

---

## `UpdateBankIntegrationCommand`

Atualiza uma integração bancária.

Permissão:

```text
financial.bank_integration.update
```

Payload:

```json
{
  "bank_integration_id": "uuid",
  "client_secret": "encrypted",
  "certificate_id": "uuid"
}
```

Validações:

- integração existente;
- credenciais válidas;
- certificado compatível.

Evento resultante:

```text
financial.bank_integration_updated
```

---

## `EnableBankIntegrationCommand`

Habilita uma integração.

Permissão:

```text
financial.bank_integration.enable
```

Payload:

```json
{
  "bank_integration_id": "uuid"
}
```

Validações:

- integração existente;
- credenciais testadas;
- certificado válido.

Evento resultante:

```text
financial.bank_integration_enabled
```

---

## `DisableBankIntegrationCommand`

Desabilita uma integração.

Permissão:

```text
financial.bank_integration.disable
```

Payload:

```json
{
  "bank_integration_id": "uuid",
  "reason": "Troca de certificado"
}
```

Validações:

- integração existente;
- justificar desativação.

Evento resultante:

```text
financial.bank_integration_disabled
```

---

## `SynchronizePixPaymentsCommand`

Sincroniza pagamentos PIX.

Permissão:

```text
financial.pix.sync
```

Payload:

```json
{
  "bank_integration_id": "uuid",
  "initial_datetime": "datetime",
  "final_datetime": "datetime"
}
```

Validações:

- integração ativa;
- período válido;
- API disponível.

Evento resultante:

```text
financial.pix_payments_synchronized
```

---

## `SynchronizeBankSlipsCommand`

Sincroniza boletos registrados.

Permissão:

```text
financial.bank_slip.sync
```

Payload:

```json
{
  "bank_integration_id": "uuid"
}
```

Validações:

- integração ativa;
- carteira configurada.

Evento resultante:

```text
financial.bank_slips_synchronized
```

---

## `SynchronizeBankAccountsCommand`

Atualiza informações das contas bancárias.

Permissão:

```text
financial.bank_account.sync
```

Payload:

```json
{
  "bank_integration_id": "uuid"
}
```

Validações:

- integração ativa;
- banco disponível.

Evento resultante:

```text
financial.bank_accounts_synchronized
```

---

## `SynchronizeBankStatementCommand`

Importa automaticamente o extrato bancário.

Permissão:

```text
financial.bank_statement.sync
```

Payload:

```json
{
  "bank_account_id": "uuid",
  "start_date": "date",
  "end_date": "date"
}
```

Validações:

- conta ativa;
- integração configurada;
- período válido.

Evento resultante:

```text
financial.bank_statement_synchronized
```

---

## `ProcessWebhookNotificationCommand`

Processa notificações enviadas pelo banco.

Permissão:

```text
financial.webhook.process
```

Payload:

```json
{
  "provider": "SICREDI",
  "event_type": "PIX_RECEIVED",
  "payload": {}
}
```

Validações:

- assinatura digital válida;
- origem confiável;
- impedir processamento duplicado;
- evento suportado.

Evento resultante:

```text
financial.webhook_processed
```

---

## `RetryFailedIntegrationCommand`

Reprocessa integrações que falharam.

Permissão:

```text
financial.integration.retry
```

Payload:

```json
{
  "integration_log_id": "uuid"
}
```

Validações:

- erro existente;
- integração ativa;
- número máximo de tentativas respeitado.

Evento resultante:

```text
financial.integration_reprocessed
```

---

## `ArchiveIntegrationLogCommand`

Arquiva logs antigos.

Permissão:

```text
financial.integration.archive_logs
```

Payload:

```json
{
  "until_date": "date"
}
```

Validações:

- retenção mínima respeitada;
- nenhuma auditoria pendente.

Evento resultante:

```text
financial.integration_logs_archived
```

---

## `DeleteIntegrationLogCommand`

Remove registros conforme política de retenção.

Permissão:

```text
financial.integration.delete_logs
```

Payload:

```json
{
  "integration_log_id": "uuid"
}
```

Validações:

- política LGPD;
- prazo mínimo de retenção cumprido;
- autorização administrativa.

Evento resultante:

```text
financial.integration_log_deleted
```

---

**Próxima seção:** **#102. Comandos de Financial — Orçamentos Financeiros (Budgeting)**
# 102. Comandos de Financial — Orçamentos Financeiros (Budgeting)

## `CreateBudgetCommand`

Cria um orçamento financeiro.

Permissão:

```text
financial.budget.create
```

Payload:

```json
{
  "name": "Orçamento 2027",
  "fiscal_year": 2027,
  "currency": "BRL",
  "description": "Planejamento financeiro anual"
}
```

Validações:

- exercício único por versão;
- moeda suportada;
- nome obrigatório.

Evento resultante:

```text
financial.budget_created
```

---

## `CreateBudgetVersionCommand`

Cria uma nova versão do orçamento.

Permissão:

```text
financial.budget.version.create
```

Payload:

```json
{
  "budget_id": "uuid",
  "version_name": "Revisão 02"
}
```

Validações:

- orçamento existente;
- versão única.

Evento resultante:

```text
financial.budget_version_created
```

---

## `ApproveBudgetVersionCommand`

Aprova uma versão.

Permissão:

```text
financial.budget.version.approve
```

Payload:

```json
{
  "budget_version_id": "uuid"
}
```

Validações:

- versão existente;
- nenhuma inconsistência financeira.

Evento resultante:

```text
financial.budget_version_approved
```

---

## `ArchiveBudgetVersionCommand`

Arquiva uma versão antiga.

Permissão:

```text
financial.budget.version.archive
```

Payload:

```json
{
  "budget_version_id": "uuid"
}
```

Validações:

- versão não ativa.

Evento resultante:

```text
financial.budget_version_archived
```

---

## `CreateBudgetCategoryCommand`

Cria uma categoria orçamentária.

Permissão:

```text
financial.budget.category.create
```

Payload:

```json
{
  "code": "MAT_PRIMA",
  "name": "Matéria-Prima"
}
```

Validações:

- código único;
- nome obrigatório.

Evento resultante:

```text
financial.budget_category_created
```

---

## `UpdateBudgetCategoryCommand`

Atualiza categoria.

Permissão:

```text
financial.budget.category.update
```

Payload:

```json
{
  "budget_category_id": "uuid",
  "name": "Matérias-Primas"
}
```

Evento resultante:

```text
financial.budget_category_updated
```

---

## `ArchiveBudgetCategoryCommand`

Arquiva categoria.

Permissão:

```text
financial.budget.category.archive
```

Payload:

```json
{
  "budget_category_id": "uuid"
}
```

Evento resultante:

```text
financial.budget_category_archived
```

---

## `CreateBudgetEntryCommand`

Cria um lançamento previsto.

Permissão:

```text
financial.budget.entry.create
```

Payload:

```json
{
  "budget_version_id": "uuid",
  "category_id": "uuid",
  "month": 1,
  "planned_amount": "35000.00"
}
```

Validações:

- categoria existente;
- valor positivo;
- mês entre 1 e 12.

Evento resultante:

```text
financial.budget_entry_created
```

---

## `UpdateBudgetEntryCommand`

Atualiza previsão.

Permissão:

```text
financial.budget.entry.update
```

Payload:

```json
{
  "budget_entry_id": "uuid",
  "planned_amount": "38000.00"
}
```

Evento resultante:

```text
financial.budget_entry_updated
```

---

## `DeleteBudgetEntryCommand`

Remove uma previsão.

Permissão:

```text
financial.budget.entry.delete
```

Payload:

```json
{
  "budget_entry_id": "uuid"
}
```

Validações:

- não possuir movimentações realizadas vinculadas.

Evento resultante:

```text
financial.budget_entry_deleted
```

---

## `CalculateBudgetExecutionCommand`

Calcula execução orçamentária.

Permissão:

```text
financial.budget.calculate_execution
```

Payload:

```json
{
  "budget_version_id": "uuid"
}
```

Validações:

- versão existente.

Evento resultante:

```text
financial.budget_execution_calculated
```

---

## `GenerateBudgetVarianceCommand`

Calcula desvios.

Permissão:

```text
financial.budget.generate_variance
```

Payload:

```json
{
  "budget_version_id": "uuid",
  "reference_date": "date"
}
```

Evento resultante:

```text
financial.budget_variance_generated
```

---

## `CloseBudgetPeriodCommand`

Fecha um período orçamentário.

Permissão:

```text
financial.budget.close_period
```

Payload:

```json
{
  "budget_version_id": "uuid",
  "month": 8
}
```

Validações:

- período aberto;
- movimentações processadas.

Evento resultante:

```text
financial.budget_period_closed
```

---

## `ReopenBudgetPeriodCommand`

Reabre período.

Permissão:

```text
financial.budget.reopen_period
```

Payload:

```json
{
  "budget_version_id": "uuid",
  "month": 8
}
```

Validações:

- autorização financeira.

Evento resultante:

```text
financial.budget_period_reopened
```

---

## `PublishBudgetCommand`

Publica orçamento para utilização.

Permissão:

```text
financial.budget.publish
```

Payload:

```json
{
  "budget_version_id": "uuid"
}
```

Validações:

- versão aprovada;
- consistência financeira validada.

Evento resultante:

```text
financial.budget_published
```

---

## `CloneBudgetCommand`

Cria orçamento baseado em outro exercício.

Permissão:

```text
financial.budget.clone
```

Payload:

```json
{
  "source_budget_id": "uuid",
  "target_year": 2028
}
```

Validações:

- orçamento origem existente;
- exercício destino inexistente.

Evento resultante:

```text
financial.budget_cloned
```

---

## `ImportBudgetSpreadsheetCommand`

Importa orçamento através de planilha.

Permissão:

```text
financial.budget.import
```

Payload:

```json
{
  "document_id": "uuid"
}
```

Validações:

- layout válido;
- categorias existentes;
- valores consistentes.

Evento resultante:

```text
financial.budget_imported
```

---

## `ExportBudgetSpreadsheetCommand`

Exporta orçamento.

Permissão:

```text
financial.budget.export
```

Payload:

```json
{
  "budget_version_id": "uuid",
  "format": "XLSX"
}
```

Formatos:

```text
XLSX
CSV
PDF
```

Evento resultante:

```text
financial.budget_exported
```

---

**Próxima seção:** **#103. Comandos de Financial — Centros de Custo e Plano de Contas**
# 103. Comandos de Financial — Centros de Custo e Plano de Contas

## `CreateCostCenterCommand`

Cria um Centro de Custo.

Permissão:

```text
financial.cost_center.create
```

Payload:

```json
{
  "code": "PROD001",
  "name": "Produção",
  "parent_cost_center_id": null,
  "manager_id": "uuid",
  "active": true
}
```

Validações:

- código único por Tenant;
- nome obrigatório;
- centro pai existente quando informado;
- impedir referência circular.

Evento resultante:

```text
financial.cost_center_created
```

---

## `UpdateCostCenterCommand`

Atualiza um Centro de Custo.

Permissão:

```text
financial.cost_center.update
```

Payload:

```json
{
  "cost_center_id": "uuid",
  "name": "Produção Industrial",
  "manager_id": "uuid"
}
```

Validações:

- centro existente;
- nome obrigatório;
- impedir hierarquia inválida.

Evento resultante:

```text
financial.cost_center_updated
```

---

## `ArchiveCostCenterCommand`

Arquiva um Centro de Custo.

Permissão:

```text
financial.cost_center.archive
```

Payload:

```json
{
  "cost_center_id": "uuid"
}
```

Validações:

- não possuir movimentações futuras;
- não possuir filhos ativos.

Evento resultante:

```text
financial.cost_center_archived
```

---

## `ReactivateCostCenterCommand`

Reativa um Centro de Custo.

Permissão:

```text
financial.cost_center.reactivate
```

Payload:

```json
{
  "cost_center_id": "uuid"
}
```

Evento resultante:

```text
financial.cost_center_reactivated
```

---

## `CreateChartOfAccountsCommand`

Cria um Plano de Contas.

Permissão:

```text
financial.chart_of_accounts.create
```

Payload:

```json
{
  "code": "1.1.01",
  "name": "Caixa",
  "account_type": "ASSET",
  "parent_account_id": null
}
```

Tipos:

```text
ASSET
LIABILITY
EQUITY
REVENUE
EXPENSE
RESULT
```

Validações:

- código único;
- tipo válido;
- conta pai compatível.

Evento resultante:

```text
financial.chart_of_accounts_created
```

---

## `UpdateChartOfAccountsCommand`

Atualiza conta contábil.

Permissão:

```text
financial.chart_of_accounts.update
```

Payload:

```json
{
  "chart_account_id": "uuid",
  "name": "Caixa Geral"
}
```

Evento resultante:

```text
financial.chart_of_accounts_updated
```

---

## `ArchiveChartOfAccountsCommand`

Arquiva uma conta contábil.

Permissão:

```text
financial.chart_of_accounts.archive
```

Payload:

```json
{
  "chart_account_id": "uuid"
}
```

Validações:

- não possuir lançamentos futuros;
- não possuir contas filhas ativas.

Evento resultante:

```text
financial.chart_of_accounts_archived
```

---

## `ReactivateChartOfAccountsCommand`

Reativa uma conta contábil.

Permissão:

```text
financial.chart_of_accounts.reactivate
```

Payload:

```json
{
  "chart_account_id": "uuid"
}
```

Evento resultante:

```text
financial.chart_of_accounts_reactivated
```

---

## `MapFinancialCategoryCommand`

Relaciona categoria financeira ao plano de contas.

Permissão:

```text
financial.category.mapping.create
```

Payload:

```json
{
  "financial_category_id": "uuid",
  "chart_account_id": "uuid"
}
```

Validações:

- categoria existente;
- conta existente;
- impedir duplicidade.

Evento resultante:

```text
financial.category_mapping_created
```

---

## `RemoveFinancialCategoryMappingCommand`

Remove relacionamento.

Permissão:

```text
financial.category.mapping.remove
```

Payload:

```json
{
  "mapping_id": "uuid"
}
```

Evento resultante:

```text
financial.category_mapping_removed
```

---

## `MoveChartAccountCommand`

Move uma conta dentro da árvore contábil.

Permissão:

```text
financial.chart_of_accounts.move
```

Payload:

```json
{
  "chart_account_id": "uuid",
  "new_parent_account_id": "uuid"
}
```

Validações:

- impedir ciclos;
- respeitar tipo da conta;
- preservar histórico.

Evento resultante:

```text
financial.chart_of_accounts_moved
```

---

## `GenerateTrialBalanceCommand`

Gera balancete.

Permissão:

```text
financial.trial_balance.generate
```

Payload:

```json
{
  "start_date": "date",
  "end_date": "date"
}
```

Validações:

- período válido.

Evento resultante:

```text
financial.trial_balance_generated
```

---

## `GenerateBalanceSheetCommand`

Gera Balanço Patrimonial.

Permissão:

```text
financial.balance_sheet.generate
```

Payload:

```json
{
  "reference_date": "date"
}
```

Evento resultante:

```text
financial.balance_sheet_generated
```

---

## `GenerateIncomeStatementCommand`

Gera Demonstração do Resultado.

Permissão:

```text
financial.income_statement.generate
```

Payload:

```json
{
  "start_date": "date",
  "end_date": "date"
}
```

Evento resultante:

```text
financial.income_statement_generated
```

---

## `GenerateCashFlowStatementCommand`

Gera Demonstrativo do Fluxo de Caixa.

Permissão:

```text
financial.cash_flow_statement.generate
```

Payload:

```json
{
  "start_date": "date",
  "end_date": "date"
}
```

Evento resultante:

```text
financial.cash_flow_statement_generated
```

---

## `GenerateFinancialIndicatorsCommand`

Calcula indicadores financeiros.

Permissão:

```text
financial.indicators.generate
```

Payload:

```json
{
  "reference_date": "date"
}
```

Indicadores iniciais:

```text
Liquidez Corrente
Liquidez Seca
Liquidez Imediata
Margem Bruta
Margem Líquida
EBITDA
ROI
ROE
ROA
Capital de Giro
Endividamento
```

Evento resultante:

```text
financial.indicators_generated
```

---

## `CloseFinancialPeriodCommand`

Realiza o fechamento financeiro.

Permissão:

```text
financial.period.close
```

Payload:

```json
{
  "start_date": "date",
  "end_date": "date"
}
```

Validações:

- todas as conciliações concluídas;
- títulos processados;
- caixa fechado;
- nenhuma inconsistência crítica.

Evento resultante:

```text
financial.period_closed
```

---

## `ReopenFinancialPeriodCommand`

Reabre um período financeiro.

Permissão:

```text
financial.period.reopen
```

Payload:

```json
{
  "financial_period_id": "uuid",
  "reason": "Correção contábil"
}
```

Validações:

- autorização administrativa;
- período elegível.

Evento resultante:

```text
financial.period_reopened
```

---

## `LockFinancialPeriodCommand`

Bloqueia alterações em um período.

Permissão:

```text
financial.period.lock
```

Payload:

```json
{
  "financial_period_id": "uuid"
}
```

Evento resultante:

```text
financial.period_locked
```

---

## `UnlockFinancialPeriodCommand`

Desbloqueia um período.

Permissão:

```text
financial.period.unlock
```

Payload:

```json
{
  "financial_period_id": "uuid",
  "reason": "Reabertura autorizada"
}
```

Validações:

- autorização administrativa.

Evento resultante:

```text
financial.period_unlocked
```

---

### Fim do módulo Financial

O módulo **Financial** está completo e contempla:

- Contas Bancárias
- Contas a Receber
- Contas a Pagar
- Cobranças (PIX, Boletos, Cartão)
- Fluxo de Caixa
- Tesouraria
- Conciliação Bancária
- Integrações Bancárias
- Orçamentos Financeiros
- Centros de Custo
- Plano de Contas
- Indicadores Financeiros
- Fechamento Financeiro
- Auditoria Financeira
- Eventos Financeiros

# 104. Comandos de Fiscal

## Visão geral

O contexto Fiscal é responsável por:

- documentos fiscais de entrada e saída;
- emissão, autorização, cancelamento e inutilização;
- tributação dos itens;
- séries e numerações fiscais;
- notas de crédito e débito;
- cartas de correção;
- eventos fiscais;
- manifestação do destinatário;
- escrituração;
- apuração tributária;
- obrigações acessórias;
- integração com provedores fiscais;
- armazenamento de XML, PDF e protocolos;
- rastreabilidade entre operação comercial, financeira, logística e fiscal.

O contexto Fiscal não será responsável por:

- confirmar o recebimento financeiro;
- movimentar estoque diretamente;
- alterar pedidos comerciais;
- aprovar compras;
- calcular custos industriais;
- substituir o sistema contábil;
- armazenar certificados digitais em texto puro.

Toda alteração em outros contextos deverá ocorrer por eventos e comandos oficiais.

---

# 105. Configurações fiscais

## `CreateFiscalProfileCommand`

Cria o perfil fiscal de uma empresa ou estabelecimento.

Permissão:

```text
fiscal.profile.create
```

Payload:

```json
{
  "tenant_id": "uuid",
  "branch_id": "uuid",
  "legal_name": "Empresa Exemplo Ltda.",
  "trade_name": "Empresa Exemplo",
  "tax_id": "string",
  "state_registration": "string",
  "municipal_registration": "string",
  "tax_regime": "SIMPLES_NACIONAL",
  "special_tax_regime": null,
  "taxpayer_type": "ICMS_TAXPAYER",
  "fiscal_environment": "HOMOLOGATION",
  "state_code": "SP",
  "municipality_code": "string",
  "address": {},
  "configuration": {}
}
```

Regimes iniciais:

```text
SIMPLES_NACIONAL
SIMPLES_NACIONAL_EXCESS
PRESUMED_PROFIT
REAL_PROFIT
MICRO_ENTREPRENEUR
IMMUNE
EXEMPT
OTHER
```

Tipos de contribuinte:

```text
ICMS_TAXPAYER
ICMS_EXEMPT
NON_TAXPAYER
```

Ambientes:

```text
HOMOLOGATION
PRODUCTION
```

Validações:

- Tenant válido;
- filial pertencente ao Tenant;
- documento fiscal válido;
- inscrições compatíveis;
- regime tributário suportado;
- endereço fiscal completo quando exigido;
- código de município válido;
- somente um perfil vigente por estabelecimento e período;
- ambiente de produção exige configuração completa;
- alterações críticas exigem auditoria.

Evento resultante:

```text
fiscal.profile_created
```

---

## `UpdateFiscalProfileCommand`

Atualiza o perfil fiscal.

Permissão:

```text
fiscal.profile.update
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "trade_name": "Nome atualizado",
  "state_registration": "string",
  "municipal_registration": "string",
  "tax_regime": "PRESUMED_PROFIT",
  "taxpayer_type": "ICMS_TAXPAYER",
  "address": {},
  "configuration": {},
  "effective_from": "date",
  "change_reason": "Alteração de regime tributário"
}
```

Validações:

- perfil existente;
- vigência futura quando exigida;
- documentos fiscais emitidos não podem ser alterados retroativamente;
- mudança de regime deve preservar histórico;
- ambiente de produção exige autorização especial;
- concorrência otimista.

Evento resultante:

```text
fiscal.profile_updated
```

---

## `ActivateFiscalProfileCommand`

Ativa o perfil fiscal.

Permissão:

```text
fiscal.profile.activate
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "effective_at": "datetime"
}
```

Validações:

- cadastro completo;
- série fiscal configurada;
- certificado válido quando necessário;
- provedor fiscal disponível;
- tributação mínima configurada;
- ausência de outro perfil incompatível vigente.

Evento resultante:

```text
fiscal.profile_activated
```

---

## `DeactivateFiscalProfileCommand`

Desativa o perfil fiscal.

Permissão:

```text
fiscal.profile.deactivate
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "reason": "Estabelecimento encerrado",
  "effective_at": "datetime"
}
```

Validações:

- nenhum documento pendente de autorização;
- nenhuma contingência aberta;
- séries e numerações avaliadas;
- obrigações acessórias pendentes identificadas;
- histórico preservado.

Evento resultante:

```text
fiscal.profile_deactivated
```

---

## `CreateFiscalDocumentSeriesCommand`

Cria uma série de documentos fiscais.

Permissão:

```text
fiscal.document_series.create
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "document_model": "NFE",
  "series": "1",
  "initial_number": 1,
  "current_number": 0,
  "environment": "HOMOLOGATION",
  "emission_mode": "NORMAL",
  "is_default": true
}
```

Modelos iniciais:

```text
NFE
NFCE
NFSE
CTE
MDFE
NFS
INTERNAL
OTHER
```

Modos de emissão:

```text
NORMAL
CONTINGENCY
OFFLINE_CONTINGENCY
SVC
OTHER
```

Validações:

- perfil fiscal ativo ou configurável;
- modelo suportado;
- série única por perfil, modelo e ambiente;
- numeração positiva;
- somente uma série padrão por modelo;
- ambiente compatível;
- não reutilizar numeração já autorizada.

Evento resultante:

```text
fiscal.document_series_created
```

---

## `UpdateFiscalDocumentSeriesCommand`

Atualiza uma série ainda não utilizada ou seus parâmetros permitidos.

Permissão:

```text
fiscal.document_series.update
```

Payload:

```json
{
  "fiscal_document_series_id": "uuid",
  "is_default": true,
  "emission_mode": "NORMAL",
  "configuration": {}
}
```

Validações:

- série existente;
- número e série não alteráveis após uso;
- somente uma série padrão;
- modo de emissão suportado;
- concorrência otimista.

Evento resultante:

```text
fiscal.document_series_updated
```

---

## `DeactivateFiscalDocumentSeriesCommand`

Desativa uma série.

Permissão:

```text
fiscal.document_series.deactivate
```

Payload:

```json
{
  "fiscal_document_series_id": "uuid",
  "reason": "Série substituída",
  "replacement_series_id": "uuid"
}
```

Validações:

- nenhum documento pendente;
- série substituta quando necessária;
- numerações não utilizadas avaliadas;
- histórico preservado.

Evento resultante:

```text
fiscal.document_series_deactivated
```

---

## `ReserveFiscalDocumentNumberCommand`

Reserva um número fiscal para emissão.

Permissão:

```text
fiscal.document_number.reserve
```

Payload:

```json
{
  "fiscal_document_series_id": "uuid",
  "fiscal_document_id": "uuid",
  "requested_number": null,
  "reservation_id": "uuid"
}
```

Validações:

- série ativa;
- número sequencial;
- número ainda não utilizado;
- reserva única;
- transação com bloqueio adequado;
- idempotência obrigatória;
- reserva expirada deve seguir política explícita.

Evento resultante:

```text
fiscal.document_number_reserved
```

---

## `ReleaseFiscalDocumentNumberCommand`

Libera uma reserva que ainda não gerou documento autorizado.

Permissão:

```text
fiscal.document_number.release
```

Payload:

```json
{
  "fiscal_document_number_reservation_id": "uuid",
  "reason": "Emissão cancelada antes do envio"
}
```

Validações:

- reserva existente;
- documento não autorizado;
- número não reutilizável quando a legislação impedir;
- poderá exigir inutilização;
- histórico preservado.

Eventos possíveis:

```text
fiscal.document_number_released
fiscal.document_number_inutilization_required
```

---

# 106. Certificados e credenciais fiscais

## `RegisterFiscalCertificateCommand`

Registra a referência segura de um certificado digital.

Permissão:

```text
fiscal.certificate.register
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "certificate_type": "A1",
  "certificate_reference": "secure-secret-reference",
  "certificate_subject": "string",
  "serial_number": "masked-string",
  "valid_from": "datetime",
  "valid_until": "datetime",
  "issuer": "string",
  "environment": "PRODUCTION"
}
```

Tipos:

```text
A1
A3
CLOUD
PROVIDER_MANAGED
OTHER
```

Validações:

- certificado válido;
- titular compatível com o perfil fiscal;
- prazo válido;
- senha e conteúdo não podem ser registrados em logs;
- arquivo deve permanecer em armazenamento seguro;
- referência única;
- permissões administrativas;
- política de rotação.

Evento resultante:

```text
fiscal.certificate_registered
```

---

## `ValidateFiscalCertificateCommand`

Valida um certificado registrado.

Permissão:

```text
fiscal.certificate.validate
```

Payload:

```json
{
  "fiscal_certificate_id": "uuid",
  "validation_scope": "FULL",
  "validated_at": "datetime"
}
```

Escopos:

```text
METADATA
SIGNATURE
CHAIN
EXPIRATION
PROVIDER_CONNECTION
FULL
```

Validações:

- certificado ativo;
- cadeia de certificação;
- período;
- titularidade;
- acesso ao segredo;
- comunicação com provedor quando exigida.

Eventos possíveis:

```text
fiscal.certificate_validated
fiscal.certificate_validation_failed
```

---

## `RotateFiscalCertificateCommand`

Substitui o certificado vigente.

Permissão:

```text
fiscal.certificate.rotate
```

Payload:

```json
{
  "current_certificate_id": "uuid",
  "new_certificate_reference": "secure-secret-reference",
  "new_valid_from": "datetime",
  "new_valid_until": "datetime",
  "reason": "Renovação do certificado"
}
```

Validações:

- novo certificado válido;
- titularidade;
- sobreposição de vigência permitida;
- documentos pendentes avaliados;
- segredo anterior preservado conforme retenção;
- teste antes da ativação.

Eventos resultantes:

```text
fiscal.certificate_rotated
fiscal.certificate_registered
```

---

## `RevokeFiscalCertificateCommand`

Revoga o uso interno do certificado.

Permissão:

```text
fiscal.certificate.revoke
```

Payload:

```json
{
  "fiscal_certificate_id": "uuid",
  "reason_code": "COMPROMISED",
  "reason": "Suspeita de comprometimento",
  "revoked_at": "datetime"
}
```

Validações:

- certificado ativo;
- autorização administrativa;
- impedir novas emissões;
- sessões e integrações relacionadas invalidadas;
- notificação crítica;
- revogação externa tratada conforme provedor.

Eventos resultantes:

```text
fiscal.certificate_revoked
fiscal.emission_blocked
```

---

## `ArchiveFiscalCertificateCommand`

Arquiva certificado expirado ou revogado.

Permissão:

```text
fiscal.certificate.archive
```

Payload:

```json
{
  "fiscal_certificate_id": "uuid",
  "reason": "Certificado expirado e substituído"
}
```

Validações:

- certificado não vigente;
- retenção legal respeitada;
- nenhuma operação ativa;
- segredo removido ou arquivado conforme política.

Evento resultante:

```text
fiscal.certificate_archived
```

---

# 107. Regras tributárias

## `CreateTaxRuleCommand`

Cria uma regra de tributação.

Permissão:

```text
fiscal.tax_rule.create
```

Payload:

```json
{
  "code": "SALE_WITHIN_SP",
  "name": "Venda interna em São Paulo",
  "operation_type": "SALE",
  "tax_regime": "SIMPLES_NACIONAL",
  "origin_state": "SP",
  "destination_state": "SP",
  "customer_taxpayer_type": "ICMS_TAXPAYER",
  "product_fiscal_category_id": "uuid",
  "priority": 100,
  "effective_from": "date",
  "effective_until": null,
  "conditions": {},
  "tax_configuration": {
    "cfop": "5102",
    "csosn": "102",
    "icms": {},
    "pis": {},
    "cofins": {},
    "ipi": {}
  }
}
```

Operações iniciais:

```text
SALE
PURCHASE
RETURN
TRANSFER
BONUS
REMITTANCE
SERVICE
IMPORT
EXPORT
INDUSTRIALIZATION
ASSET
CONSUMPTION
OTHER
```

Validações:

- código único;
- vigência coerente;
- prioridade válida;
- regime compatível;
- CFOP e códigos tributários válidos;
- estados válidos;
- categoria fiscal existente;
- condições sem referências quebradas;
- impedir ambiguidades não resolvíveis;
- regras de maior prioridade devem ser determinísticas.

Evento resultante:

```text
fiscal.tax_rule_created
```

---

## `UpdateTaxRuleCommand`

Atualiza uma regra em rascunho ou cria nova vigência.

Permissão:

```text
fiscal.tax_rule.update
```

Payload:

```json
{
  "tax_rule_id": "uuid",
  "name": "Venda interna atualizada",
  "priority": 110,
  "effective_from": "date",
  "effective_until": null,
  "conditions": {},
  "tax_configuration": {}
}
```

Validações:

- regra existente;
- documentos emitidos não são recalculados;
- alteração retroativa proibida sem processo de correção;
- vigência e prioridade;
- concorrência otimista;
- versão anterior preservada.

Evento resultante:

```text
fiscal.tax_rule_updated
```

---

## `ActivateTaxRuleCommand`

Ativa uma regra tributária.

Permissão:

```text
fiscal.tax_rule.activate
```

Payload:

```json
{
  "tax_rule_id": "uuid",
  "effective_at": "datetime"
}
```

Validações:

- regra completa;
- códigos válidos;
- inexistência de conflito bloqueante;
- simulação tributária aprovada;
- vigência válida.

Evento resultante:

```text
fiscal.tax_rule_activated
```

---

## `DeactivateTaxRuleCommand`

Desativa uma regra.

Permissão:

```text
fiscal.tax_rule.deactivate
```

Payload:

```json
{
  "tax_rule_id": "uuid",
  "reason": "Regra substituída",
  "replacement_tax_rule_id": "uuid",
  "effective_at": "datetime"
}
```

Validações:

- regra substituta quando necessária;
- documentos futuros afetados;
- vigência;
- histórico preservado.

Evento resultante:

```text
fiscal.tax_rule_deactivated
```

---

## `CreateProductFiscalCategoryCommand`

Cria uma categoria fiscal de produto ou material.

Permissão:

```text
fiscal.product_category.create
```

Payload:

```json
{
  "code": "MDF_PANEL",
  "name": "Painéis de MDF",
  "description": "Chapas e painéis de fibras de madeira",
  "ncm": "string",
  "cest": null,
  "origin_code": "0",
  "default_unit": "UN",
  "tax_attributes": {}
}
```

Validações:

- código único;
- NCM válido quando obrigatório;
- CEST compatível quando informado;
- origem válida;
- unidade suportada;
- atributos tributários coerentes.

Evento resultante:

```text
fiscal.product_category_created
```

---

## `UpdateProductFiscalCategoryCommand`

Atualiza categoria fiscal.

Permissão:

```text
fiscal.product_category.update
```

Payload:

```json
{
  "product_fiscal_category_id": "uuid",
  "name": "Painéis derivados de madeira",
  "ncm": "string",
  "cest": null,
  "origin_code": "0",
  "tax_attributes": {},
  "effective_from": "date"
}
```

Validações:

- categoria ativa;
- vigência;
- alterações não recalculam documentos passados;
- produtos vinculados devem ser reavaliados;
- concorrência otimista.

Evento resultante:

```text
fiscal.product_category_updated
```

---

## `ArchiveProductFiscalCategoryCommand`

Arquiva categoria fiscal.

Permissão:

```text
fiscal.product_category.archive
```

Payload:

```json
{
  "product_fiscal_category_id": "uuid",
  "reason": "Classificação substituída",
  "replacement_category_id": "uuid"
}
```

Validações:

- produtos ativos vinculados;
- regras tributárias;
- categoria substituta;
- histórico preservado.

Evento resultante:

```text
fiscal.product_category_archived
```

---

## `AssignProductFiscalCategoryCommand`

Vincula uma categoria fiscal a um produto ou material.

Permissão:

```text
fiscal.product_category.assign
```

Payload:

```json
{
  "entity_type": "MATERIAL",
  "entity_id": "uuid",
  "product_fiscal_category_id": "uuid",
  "effective_from": "date",
  "effective_until": null
}
```

Validações:

- entidade válida;
- categoria ativa;
- mesma empresa;
- vigência sem sobreposição incompatível;
- classificação obrigatória para emissão.

Evento resultante:

```text
fiscal.product_category_assigned
```

---

## `RemoveProductFiscalCategoryAssignmentCommand`

Encerra um vínculo fiscal.

Permissão:

```text
fiscal.product_category.assignment.remove
```

Payload:

```json
{
  "product_fiscal_category_assignment_id": "uuid",
  "effective_at": "date",
  "reason": "Produto reclassificado"
}
```

Validações:

- vínculo existente;
- nova classificação quando obrigatória;
- não alterar documentos passados.

Evento resultante:

```text
fiscal.product_category_assignment_removed
```

---

## `SimulateTaxCalculationCommand`

Simula a tributação de uma operação.

Permissão:

```text
fiscal.tax_calculation.simulate
```

Payload:

```json
{
  "operation_type": "SALE",
  "fiscal_profile_id": "uuid",
  "customer_id": "uuid",
  "origin_address": {},
  "destination_address": {},
  "issue_date": "date",
  "items": [
    {
      "reference_type": "MATERIAL",
      "reference_id": "uuid",
      "quantity": "1.0000",
      "unit_price": "1000.00",
      "discount_amount": "0.00",
      "freight_amount": "0.00",
      "insurance_amount": "0.00",
      "other_amount": "0.00"
    }
  ]
}
```

Validações:

- perfil fiscal;
- destinatário;
- endereços;
- classificações fiscais;
- regras vigentes;
- valores válidos;
- simulação não gera obrigação;
- resultado deve indicar todas as regras aplicadas.

Evento técnico opcional:

```text
fiscal.tax_calculation_simulated
```

---

## `OverrideTaxCalculationCommand`

Aplica ajuste tributário excepcional antes da autorização.

Permissão:

```text
fiscal.tax_calculation.override
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "fiscal_document_item_id": "uuid",
  "tax_type": "ICMS",
  "override_data": {},
  "reason_code": "TAX_ADVISOR_INSTRUCTION",
  "reason": "Orientação formal da assessoria tributária",
  "evidence_document_id": "uuid"
}
```

Validações:

- documento ainda não autorizado;
- permissão especial;
- justificativa;
- evidência;
- códigos e valores válidos;
- diferença em relação ao cálculo automático registrada;
- auditoria reforçada.

Evento resultante:

```text
fiscal.tax_calculation_overridden
```

---

# 108. Documentos fiscais de saída

## `CreateOutgoingFiscalDocumentCommand`

Cria um documento fiscal de saída em rascunho.

Permissão:

```text
fiscal.outgoing_document.create
```

Payload:

```json
{
  "document_model": "NFE",
  "fiscal_profile_id": "uuid",
  "fiscal_document_series_id": "uuid",
  "operation_type": "SALE",
  "purpose": "NORMAL",
  "customer_id": "uuid",
  "sales_order_id": "uuid",
  "contract_id": "uuid",
  "delivery_id": "uuid",
  "issue_date": "datetime",
  "departure_date": "datetime",
  "currency": "BRL",
  "destination_address": {},
  "billing_data": {},
  "transport_data": {},
  "additional_information": null,
  "items": [
    {
      "reference_type": "SALES_ORDER_ITEM",
      "reference_id": "uuid",
      "product_id": "uuid",
      "description": "Móvel planejado",
      "ncm": "string",
      "cfop": "5102",
      "unit": "UN",
      "quantity": "1.0000",
      "unit_price": "25000.00",
      "discount_amount": "0.00",
      "freight_amount": "0.00",
      "insurance_amount": "0.00",
      "other_amount": "0.00",
      "tax_data": {}
    }
  ]
}
```

Finalidades:

```text
NORMAL
COMPLEMENTARY
ADJUSTMENT
RETURN
CREDIT
DEBIT
```

Validações:

- perfil fiscal ativo;
- série válida;
- cliente e destinatário;
- pedido correspondente;
- itens e quantidades;
- classificações fiscais;
- valores;
- endereços;
- natureza da operação;
- regras tributárias;
- duplicidade por origem;
- documento inicia como rascunho;
- idempotência quando derivado de evento.

Evento resultante:

```text
fiscal.outgoing_document_created
```

---

## `UpdateOutgoingFiscalDocumentDraftCommand`

Atualiza um documento de saída em rascunho.

Permissão:

```text
fiscal.outgoing_document.update
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "issue_date": "datetime",
  "departure_date": "datetime",
  "destination_address": {},
  "billing_data": {},
  "transport_data": {},
  "additional_information": "Informações complementares",
  "items": []
}
```

Validações:

- documento em rascunho ou rejeitado corrigível;
- número ainda não autorizado;
- totais recalculados;
- impostos recalculados;
- origem preservada;
- concorrência otimista;
- alterações após rejeição registradas.

Evento resultante:

```text
fiscal.outgoing_document_draft_updated
```

---

## `AddOutgoingFiscalDocumentItemCommand`

Adiciona item ao rascunho.

Permissão:

```text
fiscal.outgoing_document.item.create
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "reference_type": "SALES_ORDER_ITEM",
  "reference_id": "uuid",
  "product_id": "uuid",
  "description": "Serviço de instalação",
  "ncm": null,
  "service_code": "string",
  "cfop": null,
  "unit": "SV",
  "quantity": "1.0000",
  "unit_price": "1500.00",
  "discount_amount": "0.00",
  "tax_data": {}
}
```

Validações:

- documento editável;
- item válido;
- quantidade e valor positivos;
- classificação fiscal;
- origem não faturada acima do permitido;
- totais e impostos recalculados.

Evento resultante:

```text
fiscal.outgoing_document_item_added
```

---

## `UpdateOutgoingFiscalDocumentItemCommand`

Atualiza item do rascunho.

Permissão:

```text
fiscal.outgoing_document.item.update
```

Payload:

```json
{
  "fiscal_document_item_id": "uuid",
  "description": "Descrição fiscal revisada",
  "quantity": "1.0000",
  "unit_price": "1550.00",
  "discount_amount": "50.00",
  "freight_amount": "0.00",
  "other_amount": "0.00",
  "tax_data": {}
}
```

Validações:

- documento editável;
- item pertencente ao documento;
- quantidades e valores;
- saldo faturável;
- tributação;
- concorrência otimista.

Evento resultante:

```text
fiscal.outgoing_document_item_updated
```

---

## `RemoveOutgoingFiscalDocumentItemCommand`

Remove item do rascunho.

Permissão:

```text
fiscal.outgoing_document.item.remove
```

Payload:

```json
{
  "fiscal_document_item_id": "uuid",
  "reason": "Item não será faturado neste documento"
}
```

Validações:

- documento editável;
- documento permanece válido;
- justificativa;
- liberar saldo faturável na origem;
- preservar auditoria.

Evento resultante:

```text
fiscal.outgoing_document_item_removed
```

---

## `CalculateOutgoingFiscalDocumentTaxesCommand`

Calcula os tributos do documento.

Permissão:

```text
fiscal.outgoing_document.calculate_taxes
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "calculation_date": "date",
  "recalculate_all_items": true
}
```

Validações:

- documento em rascunho;
- perfil fiscal;
- destinatário;
- regras tributárias vigentes;
- itens classificados;
- totais consistentes;
- cálculo reproduzível.

Eventos possíveis:

```text
fiscal.outgoing_document_taxes_calculated
fiscal.tax_calculation_failed
```

---

## `ValidateOutgoingFiscalDocumentCommand`

Executa validação completa antes da emissão.

Permissão:

```text
fiscal.outgoing_document.validate
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "validation_scope": "FULL"
}
```

Validações mínimas:

- emitente;
- destinatário;
- série e numeração;
- itens;
- totais;
- tributos;
- endereços;
- transporte;
- cobrança;
- referências;
- certificado;
- provedor;
- schema oficial;
- regras internas.

Eventos possíveis:

```text
fiscal.outgoing_document_validated
fiscal.outgoing_document_validation_failed
```

---

## `IssueOutgoingFiscalDocumentCommand`

Prepara, assina e envia um documento fiscal de saída.

Permissão:

```text
fiscal.outgoing_document.issue
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "idempotency_key": "string",
  "issue_mode": "NORMAL",
  "requested_at": "datetime"
}
```

Validações:

- documento validado;
- número reservado;
- certificado válido;
- perfil e série ativos;
- ambiente correto;
- provedor disponível;
- documento ainda não enviado com sucesso;
- conteúdo imutável durante o processamento;
- idempotência obrigatória;
- assinatura digital.

Eventos possíveis:

```text
fiscal.outgoing_document_issuance_requested
fiscal.outgoing_document_submitted
fiscal.outgoing_document_authorized
fiscal.outgoing_document_rejected
fiscal.outgoing_document_issuance_failed
```

---

## `AuthorizeOutgoingFiscalDocumentCommand`

Registra a autorização retornada pelo órgão fiscal.

Permissão:

```text
fiscal.outgoing_document.authorize
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "access_key": "masked-string",
  "protocol_number": "string",
  "authorized_at": "datetime",
  "authorization_status_code": "string",
  "authorization_message": "Autorizado o uso",
  "xml_document_id": "uuid",
  "provider_response_reference": "secure-reference"
}
```

Validações:

- retorno autêntico;
- documento enviado;
- chave de acesso compatível;
- protocolo não duplicado;
- assinatura e schema;
- autorização idempotente;
- XML preservado de forma imutável.

Evento resultante:

```text
fiscal.outgoing_document_authorized
```

Consumidores:

- Commercial;
- Inventory;
- Financial;
- Documents;
- Notifications;
- Analytics.

---

## `RejectOutgoingFiscalDocumentCommand`

Registra rejeição fiscal.

Permissão:

```text
fiscal.outgoing_document.reject
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "rejection_code": "string",
  "rejection_message": "Descrição segura",
  "rejected_at": "datetime",
  "provider_response_reference": "secure-reference",
  "is_correctable": true
}
```

Validações:

- retorno autêntico;
- documento enviado;
- código suportado;
- não registrar dados sensíveis;
- classificação entre corrigível e definitiva;
- número fiscal tratado conforme regra aplicável.

Evento resultante:

```text
fiscal.outgoing_document_rejected
```

---

## `CorrectRejectedOutgoingFiscalDocumentCommand`

Corrige um documento rejeitado.

Permissão:

```text
fiscal.outgoing_document.rejection.correct
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "corrections": {},
  "reason": "Correção do código tributário",
  "recalculate_taxes": true
}
```

Validações:

- documento rejeitado e corrigível;
- nenhuma autorização;
- campos alteráveis;
- nova validação obrigatória;
- histórico de tentativa preservado;
- concorrência otimista.

Evento resultante:

```text
fiscal.outgoing_document_rejection_corrected
```

---

## `GenerateFiscalDocumentPdfCommand`

Gera o documento auxiliar em PDF.

Permissão:

```text
fiscal.document.pdf.generate
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "document_layout": "DANFE_PORTRAIT",
  "include_additional_information": true
}
```

Validações:

- documento autorizado ou permitido para pré-visualização;
- layout compatível;
- dados provenientes do XML autorizado;
- PDF vinculado à versão correta;
- documento auxiliar não substitui o XML.

Evento resultante:

```text
fiscal.document_pdf_generated
```

---

## `SendFiscalDocumentToCustomerCommand`

Envia XML e documento auxiliar ao destinatário.

Permissão:

```text
fiscal.outgoing_document.send_to_customer
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "recipient_contact_id": "uuid",
  "channels": [
    "EMAIL"
  ],
  "include_xml": true,
  "include_pdf": true,
  "sent_at": "datetime"
}
```

Validações:

- documento autorizado;
- destinatário correto;
- contato válido;
- arquivos disponíveis;
- canais autorizados;
- proteção de dados;
- idempotência.

Evento resultante:

```text
fiscal.outgoing_document_sent_to_customer
```

---

## `CancelOutgoingFiscalDocumentCommand`

Solicita o cancelamento de documento autorizado.

Permissão:

```text
fiscal.outgoing_document.cancel
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "cancellation_reason": "Operação cancelada antes da circulação",
  "requested_at": "datetime",
  "evidence_document_id": "uuid"
}
```

Validações:

- documento autorizado;
- prazo legal;
- motivo com tamanho e formato válidos;
- operação permite cancelamento;
- circulação, estoque, financeiro e entrega avaliados;
- certificado válido;
- idempotência;
- aprovação especial quando necessária.

Eventos possíveis:

```text
fiscal.outgoing_document_cancellation_requested
fiscal.outgoing_document_cancelled
fiscal.outgoing_document_cancellation_rejected
```

---

## `RegisterOutgoingFiscalDocumentCancellationCommand`

Registra a autorização do cancelamento.

Permissão:

```text
fiscal.outgoing_document.cancellation.register
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "cancellation_protocol": "string",
  "cancelled_at": "datetime",
  "event_xml_document_id": "uuid",
  "provider_response_reference": "secure-reference"
}
```

Validações:

- retorno autêntico;
- solicitação aberta;
- protocolo;
- não duplicar cancelamento;
- eventos compensatórios devem ser publicados.

Evento resultante:

```text
fiscal.outgoing_document_cancelled
```

---

## `CreateCorrectionLetterCommand`

Cria uma carta de correção eletrônica.

Permissão:

```text
fiscal.correction_letter.create
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "correction_text": "Texto da correção permitida",
  "sequence_number": 1,
  "requested_at": "datetime"
}
```

Validações:

- documento autorizado;
- correção legalmente permitida;
- não alterar valores, destinatário ou elementos proibidos;
- sequência correta;
- tamanho e formato;
- certificado válido;
- idempotência.

Eventos possíveis:

```text
fiscal.correction_letter_requested
fiscal.correction_letter_authorized
fiscal.correction_letter_rejected
```

---

## `RegisterCorrectionLetterAuthorizationCommand`

Registra a autorização da carta de correção.

Permissão:

```text
fiscal.correction_letter.authorization.register
```

Payload:

```json
{
  "fiscal_correction_letter_id": "uuid",
  "protocol_number": "string",
  "authorized_at": "datetime",
  "event_xml_document_id": "uuid"
}
```

Evento resultante:

```text
fiscal.correction_letter_authorized
```

---

## `CreateComplementaryFiscalDocumentCommand`

Cria documento complementar.

Permissão:

```text
fiscal.complementary_document.create
```

Payload:

```json
{
  "original_fiscal_document_id": "uuid",
  "complement_type": "TAX",
  "reason": "Complemento de ICMS",
  "items": [],
  "additional_amounts": {}
}
```

Tipos:

```text
PRICE
QUANTITY
TAX
FREIGHT
OTHER
```

Validações:

- documento original autorizado;
- complemento permitido;
- referência fiscal obrigatória;
- valores complementares positivos;
- não duplicar complemento equivalente;
- tributação específica.

Evento resultante:

```text
fiscal.complementary_document_created
```

---

## `CreateReturnFiscalDocumentCommand`

Cria uma nota fiscal de devolução.

Permissão:

```text
fiscal.return_document.create
```

Payload:

```json
{
  "original_fiscal_document_id": "uuid",
  "return_type": "CUSTOMER_RETURN",
  "return_reason": "Produto devolvido",
  "items": [
    {
      "original_fiscal_document_item_id": "uuid",
      "quantity": "1.0000"
    }
  ],
  "return_date": "date"
}
```

Tipos:

```text
CUSTOMER_RETURN
SUPPLIER_RETURN
PARTIAL_RETURN
TOTAL_RETURN
SYMBOLIC_RETURN
OTHER
```

Validações:

- documento original autorizado;
- quantidades não superiores ao saldo retornável;
- itens correspondentes;
- natureza e CFOP;
- impostos devolvidos;
- estoque e financeiro tratados por eventos;
- idempotência.

Evento resultante:

```text
fiscal.return_document_created
```

---

# 109. Documentos fiscais de entrada

## `ImportIncomingFiscalDocumentCommand`

Importa um documento fiscal de entrada.

Permissão:

```text
fiscal.incoming_document.import
```

Payload:

```json
{
  "source_type": "XML_UPLOAD",
  "document_id": "uuid",
  "provider_reference": null,
  "purchase_order_id": "uuid",
  "purchase_receipt_id": "uuid",
  "imported_at": "datetime"
}
```

Origens:

```text
XML_UPLOAD
PROVIDER_DOWNLOAD
MANIFESTATION_SERVICE
EMAIL_ATTACHMENT
MANUAL_ENTRY
INTEGRATION
```

Validações:

- XML íntegro;
- assinatura;
- schema;
- destinatário corresponde ao perfil fiscal;
- chave de acesso não duplicada;
- fornecedor;
- ambiente;
- documento original preservado;
- idempotência pela chave de acesso.

Eventos possíveis:

```text
fiscal.incoming_document_imported
fiscal.incoming_document_import_failed
```

---

## `CreateIncomingFiscalDocumentManuallyCommand`

Cria documento de entrada manual quando autorizado.

Permissão:

```text
fiscal.incoming_document.manual_create
```

Payload:

```json
{
  "document_model": "OTHER",
  "supplier_id": "uuid",
  "document_number": "string",
  "series": "string",
  "access_key": null,
  "issue_date": "date",
  "entry_date": "date",
  "total_amount": "1500.00",
  "currency": "BRL",
  "items": [],
  "reason": "Documento não eletrônico permitido"
}
```

Validações:

- modelo permite cadastro manual;
- fornecedor;
- número e série;
- duplicidade;
- valores;
- justificativa;
- documento comprobatório;
- autorização conforme política.

Evento resultante:

```text
fiscal.incoming_document_created
```

---

## `LinkIncomingFiscalDocumentToPurchaseCommand`

Vincula documento a pedido e recebimento.

Permissão:

```text
fiscal.incoming_document.link_purchase
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "purchase_order_id": "uuid",
  "purchase_receipt_id": "uuid",
  "link_strategy": "MATCH_BY_ITEMS"
}
```

Estratégias:

```text
MATCH_BY_ITEMS
MATCH_BY_TOTAL
MANUAL
PROVIDER_REFERENCE
```

Validações:

- fornecedor correspondente;
- itens compatíveis;
- quantidades;
- valores e tolerâncias;
- documento e compra do mesmo Tenant;
- não duplicar vínculo;
- divergências registradas.

Eventos possíveis:

```text
fiscal.incoming_document_linked_to_purchase
fiscal.incoming_document_divergence_detected
```

---

## `MatchIncomingFiscalDocumentItemsCommand`

Relaciona itens fiscais aos itens comprados ou materiais.

Permissão:

```text
fiscal.incoming_document.items.match
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "matches": [
    {
      "incoming_fiscal_document_item_id": "uuid",
      "purchase_order_item_id": "uuid",
      "material_id": "uuid",
      "matched_quantity": "2.0000"
    }
  ]
}
```

Validações:

- itens pertencentes às entidades;
- fornecedor;
- quantidades;
- unidade e conversão;
- nenhum item excedido;
- classificação fiscal preservada;
- correspondência parcial permitida quando configurada.

Evento resultante:

```text
fiscal.incoming_document_items_matched
```

---

## `ValidateIncomingFiscalDocumentCommand`

Valida documento de entrada.

Permissão:

```text
fiscal.incoming_document.validate
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "validation_scope": "FULL"
}
```

Validações:

- assinatura e XML;
- emitente;
- destinatário;
- chave;
- itens;
- totais;
- impostos;
- pedido;
- recebimento;
- tolerâncias;
- duplicidade;
- situação do documento no órgão fiscal quando configurado.

Eventos possíveis:

```text
fiscal.incoming_document_validated
fiscal.incoming_document_validation_failed
fiscal.incoming_document_divergence_detected
```

---

## `ApproveIncomingFiscalDocumentCommand`

Aprova o documento de entrada para escrituração.

Permissão:

```text
fiscal.incoming_document.approve
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Pedido, recebimento e documento conferidos"
}
```

Validações:

- documento validado;
- divergências bloqueantes resolvidas;
- recebimento quando exigido;
- pedido;
- fornecedor;
- valores;
- tributação;
- alçada e segregação de funções.

Evento resultante:

```text
fiscal.incoming_document_approved
```

---

## `RejectIncomingFiscalDocumentCommand`

Rejeita internamente o documento.

Permissão:

```text
fiscal.incoming_document.reject
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "reason_code": "VALUE_DIVERGENCE",
  "reason": "Valor divergente do pedido",
  "rejected_at": "datetime"
}
```

Validações:

- documento pendente;
- motivo;
- fornecedor notificado quando configurado;
- manifestação fiscal avaliada;
- financeiro e estoque não alterados diretamente.

Evento resultante:

```text
fiscal.incoming_document_rejected
```

---

## `OpenIncomingFiscalDocumentDivergenceCommand`

Registra divergência fiscal.

Permissão:

```text
fiscal.incoming_document.divergence.open
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "divergence_type": "PRICE",
  "description": "Preço superior ao pedido",
  "expected_value": "1400.00",
  "document_value": "1500.00",
  "severity": "HIGH",
  "assigned_user_id": "uuid"
}
```

Tipos:

```text
SUPPLIER
DOCUMENT_NUMBER
ITEM
QUANTITY
UNIT
PRICE
TOTAL
TAX
PURCHASE_ORDER
RECEIPT
DUPLICATE
OTHER
```

Validações:

- documento existente;
- divergência verificável;
- valores seguros;
- não duplicar divergência aberta equivalente;
- responsável.

Evento resultante:

```text
fiscal.incoming_document_divergence_opened
```

---

## `ResolveIncomingFiscalDocumentDivergenceCommand`

Resolve divergência.

Permissão:

```text
fiscal.incoming_document.divergence.resolve
```

Payload:

```json
{
  "fiscal_divergence_id": "uuid",
  "resolution_code": "ACCEPTED_WITH_APPROVAL",
  "resolution": "Diferença aprovada pelo comprador",
  "resolved_at": "datetime",
  "approval_document_id": "uuid"
}
```

Resoluções:

```text
DOCUMENT_CORRECTED
PURCHASE_ORDER_CORRECTED
RECEIPT_CORRECTED
ACCEPTED_WITH_APPROVAL
RETURN_TO_SUPPLIER
CANCELLED
OTHER
```

Validações:

- divergência aberta;
- ação correspondente concluída;
- alçada;
- evidência;
- documento revalidado quando necessário.

Evento resultante:

```text
fiscal.incoming_document_divergence_resolved
```

---

## `PostIncomingFiscalDocumentCommand`

Escritura o documento fiscal de entrada.

Permissão:

```text
fiscal.incoming_document.post
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "posting_date": "date",
  "fiscal_period_id": "uuid",
  "recognize_tax_credits": true
}
```

Validações:

- documento aprovado;
- período fiscal aberto;
- documento não escriturado;
- tributos;
- créditos elegíveis;
- classificações;
- idempotência.

Eventos resultantes:

```text
fiscal.incoming_document_posted
fiscal.tax_credit_recognized
```

---

## `ReverseIncomingFiscalDocumentPostingCommand`

Estorna a escrituração.

Permissão:

```text
fiscal.incoming_document.posting.reverse
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "reason": "Documento escriturado incorretamente",
  "reversed_at": "datetime",
  "evidence_document_id": "uuid"
}
```

Validações:

- documento escriturado;
- período aberto ou autorização especial;
- obrigação acessória ainda corrigível;
- créditos estornados;
- não excluir lançamento original;
- auditoria.

Eventos resultantes:

```text
fiscal.incoming_document_posting_reversed
fiscal.tax_credit_reversed
```

---

# 110. Manifestação do destinatário

## `RegisterRecipientAwarenessCommand`

Registra ciência da operação.

Permissão:

```text
fiscal.recipient_manifestation.awareness
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "access_key": "masked-string",
  "manifested_at": "datetime"
}
```

Validações:

- documento destinado ao perfil fiscal;
- manifestação permitida;
- certificado válido;
- não duplicar evento equivalente;
- idempotência.

Eventos possíveis:

```text
fiscal.recipient_awareness_requested
fiscal.recipient_awareness_registered
fiscal.recipient_awareness_rejected
```

---

## `ConfirmRecipientOperationCommand`

Confirma a operação.

Permissão:

```text
fiscal.recipient_manifestation.confirm_operation
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "manifested_at": "datetime",
  "justification": null
}
```

Validações:

- documento válido;
- operação reconhecida;
- manifestação final compatível;
- prazo;
- certificado;
- idempotência.

Evento resultante:

```text
fiscal.recipient_operation_confirmed
```

---

## `ReportUnknownRecipientOperationCommand`

Declara desconhecimento da operação.

Permissão:

```text
fiscal.recipient_manifestation.unknown_operation
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "manifested_at": "datetime",
  "justification": "Operação não reconhecida"
}
```

Validações:

- documento destinado ao estabelecimento;
- justificativa;
- prazo;
- ator autorizado;
- análise de segurança;
- não confirmar recebimento ou compra.

Evento resultante:

```text
fiscal.recipient_operation_reported_unknown
```

---

## `ReportUnperformedRecipientOperationCommand`

Declara operação não realizada.

Permissão:

```text
fiscal.recipient_manifestation.operation_not_performed
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "manifested_at": "datetime",
  "justification": "Mercadoria não recebida"
}
```

Validações:

- documento;
- justificativa conforme requisitos;
- prazo;
- recebimento e compra avaliados;
- autorização.

Evento resultante:

```text
fiscal.recipient_operation_reported_not_performed
```

---

## `DownloadIncomingFiscalDocumentXmlCommand`

Solicita o XML após manifestação autorizada.

Permissão:

```text
fiscal.incoming_document.xml.download
```

Payload:

```json
{
  "incoming_fiscal_document_id": "uuid",
  "provider": "FISCAL_AUTHORITY",
  "requested_at": "datetime"
}
```

Validações:

- manifestação ou condição necessária;
- certificado;
- documento destinado ao estabelecimento;
- XML ainda não armazenado;
- idempotência.

Eventos possíveis:

```text
fiscal.incoming_document_xml_downloaded
fiscal.incoming_document_xml_download_failed
```

---

# 111. Inutilização de numeração

## `RequestFiscalDocumentNumberInutilizationCommand`

Solicita inutilização de faixa numérica.

Permissão:

```text
fiscal.document_number.inutilization.request
```

Payload:

```json
{
  "fiscal_document_series_id": "uuid",
  "document_model": "NFE",
  "year": 2026,
  "initial_number": 125,
  "final_number": 130,
  "justification": "Quebra de sequência causada por falha de integração",
  "requested_at": "datetime"
}
```

Validações:

- série e modelo;
- faixa válida;
- números não autorizados;
- números não inutilizados;
- justificativa conforme formato legal;
- certificado;
- ambiente;
- autorização administrativa;
- idempotência.

Eventos possíveis:

```text
fiscal.document_number_inutilization_requested
fiscal.document_number_inutilized
fiscal.document_number_inutilization_rejected
```

---

## `RegisterFiscalDocumentNumberInutilizationCommand`

Registra a autorização.

Permissão:

```text
fiscal.document_number.inutilization.register
```

Payload:

```json
{
  "fiscal_number_inutilization_id": "uuid",
  "protocol_number": "string",
  "authorized_at": "datetime",
  "event_xml_document_id": "uuid"
}
```

Validações:

- retorno autêntico;
- faixa correspondente;
- protocolo;
- não duplicar;
- números marcados como inutilizados permanentemente.

Evento resultante:

```text
fiscal.document_number_inutilized
```

---

# 112. Contingência fiscal

## `ActivateFiscalContingencyCommand`

Ativa emissão em contingência.

Permissão:

```text
fiscal.contingency.activate
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "document_model": "NFE",
  "contingency_type": "SVC",
  "reason_code": "AUTHORITY_UNAVAILABLE",
  "reason": "Serviço de autorização indisponível",
  "activated_at": "datetime"
}
```

Tipos:

```text
SVC
OFFLINE
FS_DA
EPEC
PROVIDER_FALLBACK
OTHER
```

Validações:

- contingência permitida para o modelo;
- falha comprovada ou autorização;
- série e configuração;
- certificado;
- início registrado;
- impedir múltiplas contingências incompatíveis;
- notificar responsáveis.

Evento resultante:

```text
fiscal.contingency_activated
```

---

## `DeactivateFiscalContingencyCommand`

Encerra contingência.

Permissão:

```text
fiscal.contingency.deactivate
```

Payload:

```json
{
  "fiscal_contingency_id": "uuid",
  "deactivated_at": "datetime",
  "reason": "Serviço normalizado"
}
```

Validações:

- contingência ativa;
- documentos pendentes identificados;
- transmissão posterior planejada;
- período registrado.

Evento resultante:

```text
fiscal.contingency_deactivated
```

---

## `IssueFiscalDocumentInContingencyCommand`

Emite documento no modo de contingência.

Permissão:

```text
fiscal.document.issue_in_contingency
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "fiscal_contingency_id": "uuid",
  "contingency_issued_at": "datetime",
  "idempotency_key": "string"
}
```

Validações:

- contingência ativa;
- documento validado;
- modo compatível;
- número reservado;
- justificativa e timestamp;
- impressão quando exigida;
- idempotência;
- transmissão posterior obrigatória.

Eventos possíveis:

```text
fiscal.document_issued_in_contingency
fiscal.document_pending_transmission
```

---

## `TransmitPendingContingencyDocumentCommand`

Transmite documento emitido em contingência.

Permissão:

```text
fiscal.contingency_document.transmit
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "transmitted_at": "datetime",
  "idempotency_key": "string"
}
```

Validações:

- documento pendente;
- serviço normalizado;
- prazo;
- certificado;
- documento não alterado;
- idempotência.

Eventos possíveis:

```text
fiscal.contingency_document_submitted
fiscal.outgoing_document_authorized
fiscal.outgoing_document_rejected
```

---

# 113. Períodos fiscais

## `CreateFiscalPeriodCommand`

Cria um período fiscal.

Permissão:

```text
fiscal.period.create
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "period_type": "MONTHLY",
  "start_date": "date",
  "end_date": "date",
  "reference": "2026-08"
}
```

Tipos:

```text
MONTHLY
QUARTERLY
ANNUAL
CUSTOM
```

Validações:

- perfil fiscal;
- período válido;
- não sobreposição incompatível;
- referência única;
- timezone e competência.

Evento resultante:

```text
fiscal.period_created
```

---

## `OpenFiscalPeriodCommand`

Abre o período para escrituração.

Permissão:

```text
fiscal.period.open
```

Payload:

```json
{
  "fiscal_period_id": "uuid",
  "opened_at": "datetime"
}
```

Validações:

- período criado;
- período anterior conforme política;
- configurações fiscais completas;
- não encerrado definitivamente.

Evento resultante:

```text
fiscal.period_opened
```

---

## `CloseFiscalPeriodCommand`

Fecha o período fiscal.

Permissão:

```text
fiscal.period.close
```

Payload:

```json
{
  "fiscal_period_id": "uuid",
  "closed_at": "datetime",
  "closing_notes": "Período conferido e apurado"
}
```

Validações:

- período aberto;
- documentos de entrada e saída processados;
- divergências resolvidas;
- cancelamentos;
- inutilizações;
- contingências;
- apurações concluídas;
- obrigações geradas;
- nenhuma pendência crítica;
- auditoria.

Evento resultante:

```text
fiscal.period_closed
```

---

## `ReopenFiscalPeriodCommand`

Reabre período fechado.

Permissão:

```text
fiscal.period.reopen
```

Payload:

```json
{
  "fiscal_period_id": "uuid",
  "reason": "Documento de entrada recebido após o fechamento",
  "reopened_at": "datetime",
  "approval_document_id": "uuid"
}
```

Validações:

- autorização especial;
- obrigação acessória corrigível;
- período não bloqueado legalmente;
- justificativa;
- impacto em apurações;
- histórico preservado.

Evento resultante:

```text
fiscal.period_reopened
```

---

## `LockFiscalPeriodCommand`

Bloqueia definitivamente alterações ordinárias.

Permissão:

```text
fiscal.period.lock
```

Payload:

```json
{
  "fiscal_period_id": "uuid",
  "locked_at": "datetime",
  "reason": "Obrigações acessórias transmitidas"
}
```

Validações:

- período fechado;
- obrigações transmitidas;
- nenhuma pendência;
- desbloqueio somente por processo excepcional.

Evento resultante:

```text
fiscal.period_locked
```

---

## `UnlockFiscalPeriodCommand`

Desbloqueia excepcionalmente o período.

Permissão:

```text
fiscal.period.unlock
```

Payload:

```json
{
  "fiscal_period_id": "uuid",
  "reason": "Retificação autorizada",
  "unlocked_at": "datetime",
  "approval_document_id": "uuid"
}
```

Validações:

- permissão de alto nível;
- justificativa e documento;
- obrigação acessória retificadora planejada;
- auditoria reforçada;
- prazo legal.

Evento resultante:

```text
fiscal.period_unlocked
```

---

# 114. Apuração tributária

## `CreateTaxAssessmentCommand`

Cria uma apuração de tributo.

Permissão:

```text
fiscal.tax_assessment.create
```

Payload:

```json
{
  "fiscal_period_id": "uuid",
  "tax_type": "ICMS",
  "assessment_type": "REGULAR",
  "calculation_method": "DEBIT_CREDIT",
  "created_at": "datetime"
}
```

Tributos iniciais:

```text
ICMS
ICMS_ST
DIFAL
FCP
IPI
ISS
PIS
COFINS
IRPJ
CSLL
SIMPLES_NACIONAL
INSS
IRRF
OTHER
```

Tipos de apuração:

```text
REGULAR
COMPLEMENTARY
RECTIFYING
SPECIAL
```

Validações:

- período fiscal;
- tributo aplicável;
- apuração única por tipo e versão;
- método válido;
- documentos processados.

Evento resultante:

```text
fiscal.tax_assessment_created
```

---

## `CalculateTaxAssessmentCommand`

Calcula a apuração.

Permissão:

```text
fiscal.tax_assessment.calculate
```

Payload:

```json
{
  "tax_assessment_id": "uuid",
  "calculation_date": "datetime",
  "include_adjustments": true,
  "include_credits": true,
  "include_carry_forward": true
}
```

Validações:

- apuração aberta;
- documentos escriturados;
- regras;
- ajustes;
- créditos;
- cálculo reproduzível;
- versão dos dados registrada.

Eventos possíveis:

```text
fiscal.tax_assessment_calculated
fiscal.tax_assessment_calculation_failed
```

---

## `AddTaxAssessmentAdjustmentCommand`

Adiciona ajuste à apuração.

Permissão:

```text
fiscal.tax_assessment.adjustment.create
```

Payload:

```json
{
  "tax_assessment_id": "uuid",
  "adjustment_type": "DEBIT",
  "adjustment_code": "string",
  "description": "Ajuste de débito",
  "amount": "500.00",
  "legal_basis": "string",
  "evidence_document_id": "uuid"
}
```

Tipos:

```text
DEBIT
CREDIT
DEDUCTION
ADDITION
REVERSAL
CARRY_FORWARD
OTHER
```

Validações:

- apuração aberta;
- código válido;
- valor positivo;
- base legal;
- evidência;
- não duplicar ajuste;
- alçada.

Evento resultante:

```text
fiscal.tax_assessment_adjustment_added
```

---

## `RemoveTaxAssessmentAdjustmentCommand`

Remove ajuste ainda não consolidado.

Permissão:

```text
fiscal.tax_assessment.adjustment.remove
```

Payload:

```json
{
  "tax_assessment_adjustment_id": "uuid",
  "reason": "Ajuste incluído incorretamente"
}
```

Validações:

- apuração aberta;
- ajuste não transmitido;
- justificativa;
- histórico preservado.

Evento resultante:

```text
fiscal.tax_assessment_adjustment_removed
```

---

## `ApproveTaxAssessmentCommand`

Aprova a apuração.

Permissão:

```text
fiscal.tax_assessment.approve
```

Payload:

```json
{
  "tax_assessment_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Valores conferidos"
}
```

Validações:

- apuração calculada;
- documentos e ajustes;
- alçada;
- segregação;
- nenhuma inconsistência;
- resultado final;
- guia quando aplicável.

Evento resultante:

```text
fiscal.tax_assessment_approved
```

---

## `RejectTaxAssessmentCommand`

Rejeita a apuração para correção.

Permissão:

```text
fiscal.tax_assessment.reject
```

Payload:

```json
{
  "tax_assessment_id": "uuid",
  "reason": "Crédito tributário precisa ser revisado"
}
```

Evento resultante:

```text
fiscal.tax_assessment_rejected
```

---

## `CloseTaxAssessmentCommand`

Encerra a apuração.

Permissão:

```text
fiscal.tax_assessment.close
```

Payload:

```json
{
  "tax_assessment_id": "uuid",
  "closed_at": "datetime",
  "payment_reference_id": "uuid"
}
```

Validações:

- apuração aprovada;
- obrigação gerada;
- pagamento ou reconhecimento;
- período;
- nenhuma pendência.

Evento resultante:

```text
fiscal.tax_assessment_closed
```

---

## `ReopenTaxAssessmentCommand`

Reabre apuração.

Permissão:

```text
fiscal.tax_assessment.reopen
```

Payload:

```json
{
  "tax_assessment_id": "uuid",
  "reason": "Retificação necessária",
  "reopened_at": "datetime"
}
```

Validações:

- autorização;
- período;
- obrigação acessória;
- pagamento;
- versão anterior preservada.

Evento resultante:

```text
fiscal.tax_assessment_reopened
```

---

## `GenerateTaxPaymentCommand`

Gera obrigação financeira do tributo.

Permissão:

```text
fiscal.tax_payment.generate
```

Payload:

```json
{
  "tax_assessment_id": "uuid",
  "due_date": "date",
  "principal_amount": "5000.00",
  "interest_amount": "0.00",
  "penalty_amount": "0.00",
  "payment_code": "string",
  "guide_document_id": "uuid"
}
```

Validações:

- apuração aprovada;
- valor;
- vencimento;
- código;
- não duplicar obrigação;
- integração com Financial por evento e comando oficial.

Eventos resultantes:

```text
fiscal.tax_payment_generated
financial.payable_created
```

---

# 115. Obrigações acessórias

## `CreateFiscalObligationCommand`

Cria uma obrigação acessória.

Permissão:

```text
fiscal.obligation.create
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "fiscal_period_id": "uuid",
  "obligation_type": "SPED_FISCAL",
  "reference": "2026-08",
  "due_date": "date",
  "submission_environment": "PRODUCTION"
}
```

Tipos iniciais:

```text
SPED_FISCAL
SPED_CONTRIBUTIONS
EFD_REINF
DCTFWEB
DEFIS
DAS
GIA
SINTEGRA
NFSE_DECLARATION
MUNICIPAL_DECLARATION
STATE_DECLARATION
CUSTOM
```

Validações:

- perfil fiscal;
- período;
- obrigação aplicável;
- referência única;
- vencimento;
- ambiente.

Evento resultante:

```text
fiscal.obligation_created
```

---

## `GenerateFiscalObligationFileCommand`

Gera o arquivo da obrigação.

Permissão:

```text
fiscal.obligation.file.generate
```

Payload:

```json
{
  "fiscal_obligation_id": "uuid",
  "layout_version": "string",
  "generation_options": {},
  "generated_at": "datetime"
}
```

Validações:

- período fechado ou estado permitido;
- documentos;
- apurações;
- cadastros;
- layout válido;
- registros obrigatórios;
- consistência;
- arquivo reproduzível;
- hash armazenado.

Eventos possíveis:

```text
fiscal.obligation_file_generated
fiscal.obligation_file_generation_failed
```

---

## `ValidateFiscalObligationFileCommand`

Valida o arquivo gerado.

Permissão:

```text
fiscal.obligation.file.validate
```

Payload:

```json
{
  "fiscal_obligation_file_id": "uuid",
  "validator_type": "INTERNAL_AND_OFFICIAL",
  "validated_at": "datetime"
}
```

Validações:

- arquivo existente;
- layout;
- estrutura;
- totais;
- referências;
- regras oficiais disponíveis;
- erros e avisos preservados.

Eventos possíveis:

```text
fiscal.obligation_file_validated
fiscal.obligation_file_validation_failed
```

---

## `ApproveFiscalObligationCommand`

Aprova a obrigação para transmissão.

Permissão:

```text
fiscal.obligation.approve
```

Payload:

```json
{
  "fiscal_obligation_id": "uuid",
  "fiscal_obligation_file_id": "uuid",
  "approved_at": "datetime",
  "approval_notes": "Arquivo validado"
}
```

Validações:

- arquivo válido;
- versão atual;
- alçada;
- nenhuma inconsistência bloqueante;
- certificado e integração.

Evento resultante:

```text
fiscal.obligation_approved
```

---

## `SubmitFiscalObligationCommand`

Transmite a obrigação.

Permissão:

```text
fiscal.obligation.submit
```

Payload:

```json
{
  "fiscal_obligation_id": "uuid",
  "fiscal_obligation_file_id": "uuid",
  "submitted_at": "datetime",
  "idempotency_key": "string"
}
```

Validações:

- obrigação aprovada;
- arquivo imutável;
- prazo;
- certificado;
- provedor;
- ambiente;
- idempotência.

Eventos possíveis:

```text
fiscal.obligation_submitted
fiscal.obligation_submission_failed
```

---

## `RegisterFiscalObligationReceiptCommand`

Registra recibo de transmissão.

Permissão:

```text
fiscal.obligation.receipt.register
```

Payload:

```json
{
  "fiscal_obligation_id": "uuid",
  "receipt_number": "string",
  "received_at": "datetime",
  "status": "ACCEPTED",
  "receipt_document_id": "uuid",
  "provider_response_reference": "secure-reference"
}
```

Estados:

```text
ACCEPTED
ACCEPTED_WITH_WARNINGS
REJECTED
PROCESSING
RECTIFICATION_REQUIRED
```

Validações:

- retorno autêntico;
- obrigação submetida;
- recibo não duplicado;
- arquivo correspondente;
- documento preservado.

Eventos possíveis:

```text
fiscal.obligation_accepted
fiscal.obligation_rejected
fiscal.obligation_processing
```

---

## `CreateFiscalObligationRectificationCommand`

Cria retificação.

Permissão:

```text
fiscal.obligation.rectification.create
```

Payload:

```json
{
  "original_fiscal_obligation_id": "uuid",
  "reason": "Inclusão de documento recebido posteriormente",
  "rectification_reference": "string"
}
```

Validações:

- obrigação original transmitida;
- prazo e regra de retificação;
- motivo;
- recibo original;
- nova versão;
- histórico preservado.

Evento resultante:

```text
fiscal.obligation_rectification_created
```

---

## `CancelFiscalObligationCommand`

Cancela obrigação ainda não transmitida.

Permissão:

```text
fiscal.obligation.cancel
```

Payload:

```json
{
  "fiscal_obligation_id": "uuid",
  "reason": "Obrigação criada para perfil incorreto"
}
```

Validações:

- não transmitida;
- justificativa;
- histórico.

Evento resultante:

```text
fiscal.obligation_cancelled
```

---

# 116. Integrações fiscais

## `RegisterFiscalProviderCommand`

Registra um provedor fiscal.

Permissão:

```text
fiscal.provider.register
```

Payload:

```json
{
  "provider_code": "FISCAL_PROVIDER",
  "name": "Provedor Fiscal",
  "supported_services": [
    "NFE",
    "NFSE",
    "DISTRIBUTION",
    "MANIFESTATION"
  ],
  "environment": "HOMOLOGATION",
  "credential_reference": "secure-secret-reference",
  "certificate_id": "uuid",
  "configuration": {}
}
```

Validações:

- provedor suportado;
- credenciais seguras;
- serviços;
- ambiente;
- certificado;
- conexão;
- não registrar segredos em logs.

Evento resultante:

```text
fiscal.provider_registered
```

---

## `UpdateFiscalProviderCommand`

Atualiza configuração do provedor.

Permissão:

```text
fiscal.provider.update
```

Payload:

```json
{
  "fiscal_provider_id": "uuid",
  "credential_reference": "secure-secret-reference",
  "certificate_id": "uuid",
  "configuration": {}
}
```

Validações:

- provedor existente;
- credenciais;
- teste de conexão;
- concorrência otimista;
- rotação segura.

Evento resultante:

```text
fiscal.provider_updated
```

---

## `EnableFiscalProviderCommand`

Habilita o provedor.

Permissão:

```text
fiscal.provider.enable
```

Payload:

```json
{
  "fiscal_provider_id": "uuid",
  "enabled_at": "datetime"
}
```

Validações:

- configuração completa;
- credenciais;
- certificado;
- teste;
- serviços.

Evento resultante:

```text
fiscal.provider_enabled
```

---

## `DisableFiscalProviderCommand`

Desabilita o provedor.

Permissão:

```text
fiscal.provider.disable
```

Payload:

```json
{
  "fiscal_provider_id": "uuid",
  "reason": "Manutenção da integração",
  "disabled_at": "datetime"
}
```

Validações:

- emissões pendentes;
- provedor alternativo;
- contingência;
- justificativa.

Evento resultante:

```text
fiscal.provider_disabled
```

---

## `TestFiscalProviderConnectionCommand`

Testa comunicação.

Permissão:

```text
fiscal.provider.connection.test
```

Payload:

```json
{
  "fiscal_provider_id": "uuid",
  "services": [
    "NFE",
    "DISTRIBUTION"
  ]
}
```

Validações:

- provedor configurado;
- segredo acessível;
- certificado;
- timeout;
- resultado seguro sem exposição de credenciais.

Eventos possíveis:

```text
fiscal.provider_connection_succeeded
fiscal.provider_connection_failed
```

---

## `SynchronizeFiscalDocumentStatusCommand`

Consulta e sincroniza a situação de um documento.

Permissão:

```text
fiscal.document.status.synchronize
```

Payload:

```json
{
  "fiscal_document_id": "uuid",
  "provider_id": "uuid",
  "requested_at": "datetime"
}
```

Validações:

- documento enviado ou autorizado;
- provedor;
- chave;
- idempotência;
- transições válidas;
- divergência de status gera alerta.

Eventos possíveis:

```text
fiscal.document_status_synchronized
fiscal.document_status_divergence_detected
```

---

## `SynchronizeIncomingFiscalDocumentsCommand`

Busca documentos destinados ao estabelecimento.

Permissão:

```text
fiscal.incoming_documents.synchronize
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "provider_id": "uuid",
  "last_sequence_number": "string",
  "requested_at": "datetime"
}
```

Validações:

- perfil;
- certificado;
- provedor;
- sequência;
- limites de consulta;
- idempotência;
- documentos duplicados ignorados com rastreabilidade.

Eventos possíveis:

```text
fiscal.incoming_documents_synchronized
fiscal.incoming_document_imported
fiscal.incoming_documents_synchronization_failed
```

---

## `ProcessFiscalWebhookCommand`

Processa webhook fiscal.

Permissão:

```text
fiscal.webhook.process
```

Payload:

```json
{
  "provider_id": "uuid",
  "provider_event_id": "string",
  "event_type": "DOCUMENT_AUTHORIZED",
  "received_at": "datetime",
  "payload_reference": "secure-reference",
  "signature": "string"
}
```

Validações:

- assinatura;
- origem;
- provedor;
- evento suportado;
- idempotência por evento externo;
- payload armazenado de forma segura;
- não confiar em Tenant informado livremente no payload.

Eventos possíveis:

```text
fiscal.webhook_processed
fiscal.webhook_rejected
```

---

## `RetryFiscalIntegrationCommand`

Reprocessa operação fiscal falha.

Permissão:

```text
fiscal.integration.retry
```

Payload:

```json
{
  "fiscal_integration_attempt_id": "uuid",
  "reason": "Serviço normalizado",
  "requested_at": "datetime"
}
```

Validações:

- tentativa falha;
- erro recuperável;
- limite de tentativas;
- documento ainda elegível;
- idempotência;
- não duplicar autorização ou cancelamento.

Evento resultante:

```text
fiscal.integration_retry_requested
```

---

## `MoveFiscalIntegrationToDeadLetterCommand`

Move uma operação definitivamente falha para tratamento manual.

Permissão:

```text
fiscal.integration.dead_letter
```

Payload:

```json
{
  "fiscal_integration_attempt_id": "uuid",
  "reason_code": "MAX_ATTEMPTS_EXCEEDED",
  "reason": "Falha persistente de integração",
  "dead_lettered_at": "datetime"
}
```

Evento resultante:

```text
fiscal.integration_dead_lettered
```

---

## `RequeueFiscalDeadLetterCommand`

Reprocessa após correção manual.

Permissão:

```text
fiscal.integration.dead_letter.requeue
```

Payload:

```json
{
  "fiscal_dead_letter_id": "uuid",
  "reason": "Certificado atualizado",
  "scheduled_at": "datetime"
}
```

Validações:

- causa corrigida;
- documento elegível;
- autorização;
- nova tentativa registrada;
- idempotência.

Evento resultante:

```text
fiscal.integration_dead_letter_requeued
```

---

# 117. Relatórios e livros fiscais

## `GenerateFiscalDocumentReportCommand`

Gera relatório de documentos fiscais.

Permissão:

```text
fiscal.report.documents.generate
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "period_start": "date",
  "period_end": "date",
  "direction": "BOTH",
  "document_models": [
    "NFE",
    "NFSE"
  ],
  "statuses": [],
  "format": "XLSX"
}
```

Direções:

```text
INCOMING
OUTGOING
BOTH
```

Validações:

- período;
- perfil;
- filtros;
- formato;
- permissão de dados;
- processamento assíncrono para grandes volumes.

Evento resultante:

```text
fiscal.document_report_generated
```

---

## `GenerateTaxBookCommand`

Gera livro fiscal.

Permissão:

```text
fiscal.tax_book.generate
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "fiscal_period_id": "uuid",
  "book_type": "OUTGOING_DOCUMENTS",
  "format": "PDF"
}
```

Tipos:

```text
INCOMING_DOCUMENTS
OUTGOING_DOCUMENTS
INVENTORY
ICMS_ASSESSMENT
IPI_ASSESSMENT
ISS_SERVICES
OTHER
```

Validações:

- período;
- documentos processados;
- apuração;
- formato;
- layout;
- dados consistentes.

Evento resultante:

```text
fiscal.tax_book_generated
```

---

## `GenerateFiscalAuditReportCommand`

Gera relatório de auditoria fiscal.

Permissão:

```text
fiscal.audit_report.generate
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "period_start": "date",
  "period_end": "date",
  "checks": [
    "MISSING_NUMBERS",
    "DUPLICATE_ACCESS_KEYS",
    "TAX_DIVERGENCES",
    "UNPOSTED_DOCUMENTS",
    "PENDING_EVENTS"
  ]
}
```

Validações:

- período;
- verificações suportadas;
- acesso;
- dados atuais;
- relatório não corrige automaticamente registros.

Eventos possíveis:

```text
fiscal.audit_report_generated
fiscal.audit_issue_detected
```

---

## `ExportFiscalDocumentsCommand`

Exporta documentos e arquivos fiscais.

Permissão:

```text
fiscal.documents.export
```

Payload:

```json
{
  "fiscal_profile_id": "uuid",
  "period_start": "date",
  "period_end": "date",
  "include_xml": true,
  "include_pdf": true,
  "include_events": true,
  "package_format": "ZIP"
}
```

Validações:

- período;
- permissões;
- retenção;
- volume;
- arquivos existentes;
- pacote protegido quando necessário;
- auditoria do download.

Evento resultante:

```text
fiscal.documents_exported
```

---

# 118. Integrações de Fiscal

## Eventos consumidos

O contexto Fiscal deverá consumir inicialmente:

```text
commercial.sales_order_released
commercial.contract_signed
commercial.sales_order_cancelled
purchasing.material_received
purchasing.purchase_order_closed
purchasing.material_returned
inventory.stock_transferred
inventory.material_consumed
financial.receivable_created
financial.payable_created
organization.tenant_updated
organization.branch_updated
```

---

## Reação a `commercial.sales_order_released`

Poderá preparar:

```text
CreateOutgoingFiscalDocumentCommand
```

quando:

- a operação exigir documento fiscal;
- o perfil fiscal estiver ativo;
- os itens possuírem classificação;
- o faturamento automático estiver habilitado.

A emissão não deverá ocorrer sem:

- validação;
- condição operacional;
- autorização prevista na política;
- idempotência.

---

## Reação a `purchasing.material_received`

Poderá:

- localizar documento fiscal de entrada;
- vincular pedido e recebimento;
- abrir divergência;
- solicitar manifestação;
- criar pendência de escrituração.

---

## Reação a `purchasing.material_returned`

Poderá iniciar:

```text
CreateReturnFiscalDocumentCommand
```

quando a devolução exigir documento fiscal.

---

## Reação a `commercial.sales_order_cancelled`

Se houver documento fiscal autorizado, o contexto deverá avaliar:

- cancelamento fiscal;
- devolução;
- nota de crédito;
- impossibilidade legal de cancelamento;
- prazo;
- circulação;
- estoque;
- financeiro.

---

# 119. Regras de integridade de Fiscal

## 119.1 Documento fiscal autorizado é imutável

Após autorização, não alterar:

- emitente;
- destinatário;
- número;
- série;
- chave de acesso;
- itens;
- quantidades;
- valores;
- tributos;
- XML;
- protocolo.

Correções deverão ocorrer por:

- cancelamento;
- carta de correção;
- nota complementar;
- devolução;
- evento fiscal;
- retificação;
- outro procedimento legal aplicável.

---

## 119.2 XML é a fonte fiscal oficial

O PDF auxiliar não substitui o XML autorizado.

O sistema deverá preservar:

```text
xml_original
xml_signed
xml_authorized
event_xml
protocol
content_hash
provider_reference
```

---

## 119.3 Segredos e certificados

Nunca armazenar em logs:

- senha do certificado;
- chave privada;
- token do provedor;
- segredo de webhook;
- credencial bancária;
- conteúdo integral de segredo.

---

## 119.4 Multi-Tenant

Toda entidade fiscal deve possuir:

```text
tenant_id
```

e, quando aplicável:

```text
branch_id
fiscal_profile_id
```

Nenhum documento poderá ser consultado por outro Tenant.

---

## 119.5 Numeração

A numeração fiscal deverá ser:

- transacional;
- sequencial conforme regra;
- única no escopo;
- protegida contra concorrência;
- não reutilizada quando proibida;
- inutilizada quando necessário;
- auditável.

---

## 119.6 Cálculo tributário

O cálculo deverá registrar:

```text
tax_rule_id
tax_rule_version
calculation_date
input_snapshot
calculation_result
manual_overrides
actor
```

Isso permitirá reproduzir o cálculo posteriormente.

---

## 119.7 Provedores externos

O domínio conhece:

```text
FiscalService
FiscalDocument
FiscalEvent
```

A infraestrutura conhece:

```text
ProviderA
ProviderB
OfficialAuthorityAdapter
MunicipalAdapter
```

Nenhuma regra central deverá depender diretamente de um fornecedor específico.

---

## 119.8 Idempotência

Comandos críticos exigem idempotência:

```text
IssueOutgoingFiscalDocumentCommand
CancelOutgoingFiscalDocumentCommand
CreateCorrectionLetterCommand
RequestFiscalDocumentNumberInutilizationCommand
SubmitFiscalObligationCommand
ProcessFiscalWebhookCommand
ImportIncomingFiscalDocumentCommand
```

---

## 119.9 Correções

Correções não devem apagar:

- tentativa anterior;
- rejeição;
- payload;
- retorno;
- número reservado;
- evento;
- ator;
- timestamp.

---

## 119.10 Datas

Diferenciar:

```text
issue_date
authorization_date
entry_date
departure_date
competence_date
posting_date
cancellation_date
manifestation_date
```

Todas as datas com horário devem ser armazenadas com timezone.

---

## 119.11 Integração financeira

Fiscal não registra pagamento.

Fiscal poderá publicar:

```text
fiscal.tax_payment_generated
fiscal.incoming_document_approved
fiscal.outgoing_document_authorized
```

Financial decidirá como criar:

- contas a pagar;
- contas a receber;
- tributos;
- ajustes;
- estornos.

---

## 119.12 Integração com estoque

Fiscal não movimenta estoque diretamente.

Documentos autorizados poderão desencadear comandos no Inventory conforme:

- entrada;
- saída;
- devolução;
- transferência;
- remessa;
- retorno.

---

## 119.13 Auditoria

Auditar obrigatoriamente:

- alteração de perfil;
- certificado;
- regra tributária;
- cálculo manual;
- emissão;
- cancelamento;
- carta de correção;
- inutilização;
- contingência;
- escrituração;
- reabertura de período;
- retificação;
- exportação de documentos.

---

## 119.14 Retenção

A retenção deve considerar:

- legislação;
- tipo de documento;
- jurisdição;
- contrato;
- auditoria;
- política de privacidade;
- litígio;
- obrigação acessória.

Arquivamento não significa exclusão física imediata.

---

## 119.15 Offline

Emissão fiscal completa não deverá depender exclusivamente do cliente offline.

Quando contingência offline for permitida, preservar:

```text
command_id
idempotency_key
device_id
fiscal_document_id
fiscal_contingency_id
occurred_at
document_hash
certificate_reference
sequence
```

A transmissão posterior será obrigatória.

---

# 120. Eventos resultantes de Fiscal

Eventos principais:

```text
fiscal.profile_created
fiscal.profile_updated
fiscal.profile_activated
fiscal.profile_deactivated
fiscal.document_series_created
fiscal.document_number_reserved
fiscal.document_number_released
fiscal.certificate_registered
fiscal.certificate_validated
fiscal.certificate_rotated
fiscal.certificate_revoked
fiscal.tax_rule_created
fiscal.tax_rule_updated
fiscal.tax_rule_activated
fiscal.product_category_created
fiscal.product_category_assigned
fiscal.tax_calculation_simulated
fiscal.tax_calculation_overridden
fiscal.outgoing_document_created
fiscal.outgoing_document_draft_updated
fiscal.outgoing_document_taxes_calculated
fiscal.outgoing_document_validated
fiscal.outgoing_document_issuance_requested
fiscal.outgoing_document_submitted
fiscal.outgoing_document_authorized
fiscal.outgoing_document_rejected
fiscal.outgoing_document_cancelled
fiscal.correction_letter_authorized
fiscal.complementary_document_created
fiscal.return_document_created
fiscal.incoming_document_imported
fiscal.incoming_document_created
fiscal.incoming_document_linked_to_purchase
fiscal.incoming_document_validated
fiscal.incoming_document_approved
fiscal.incoming_document_rejected
fiscal.incoming_document_posted
fiscal.incoming_document_divergence_opened
fiscal.incoming_document_divergence_resolved
fiscal.recipient_awareness_registered
fiscal.recipient_operation_confirmed
fiscal.recipient_operation_reported_unknown
fiscal.document_number_inutilized
fiscal.contingency_activated
fiscal.contingency_deactivated
fiscal.document_issued_in_contingency
fiscal.period_created
fiscal.period_opened
fiscal.period_closed
fiscal.period_reopened
fiscal.period_locked
fiscal.tax_assessment_created
fiscal.tax_assessment_calculated
fiscal.tax_assessment_approved
fiscal.tax_assessment_closed
fiscal.tax_payment_generated
fiscal.obligation_created
fiscal.obligation_file_generated
fiscal.obligation_approved
fiscal.obligation_submitted
fiscal.obligation_accepted
fiscal.obligation_rejected
fiscal.provider_registered
fiscal.provider_enabled
fiscal.document_status_synchronized
fiscal.incoming_documents_synchronized
fiscal.webhook_processed
fiscal.integration_dead_lettered
fiscal.document_report_generated
fiscal.tax_book_generated
fiscal.audit_report_generated
fiscal.documents_exported
```

Consumidores principais:

- Commercial;
- Purchasing;
- Inventory;
- Financial;
- Documents;
- Notifications;
- Timeline;
- Audit;
- Analytics;
- Automation;
- Administration.

---

# 121. Continuação

A próxima seção deverá continuar com:

```text
Configuration
Automation
AI
Synchronization
Regras globais finais
Índice consolidado de comandos
Critérios para evolução do catálogo
```

Fim da seção Fiscal.
# 122. Configuration

## Visão Geral

O contexto **Configuration** é responsável por centralizar toda a parametrização do OrganizeG3.

**Regra arquitetural obrigatória:**

> Nenhum módulo poderá possuir configurações hardcoded.

Toda configuração deverá estar cadastrada neste contexto ou ser derivada dele.

O Configuration é responsável por:

- parâmetros globais;
- parâmetros por Tenant;
- parâmetros por Filial;
- branding;
- design system;
- temas;
- idiomas;
- moedas;
- calendários;
- numerações;
- feature flags;
- preferências do usuário;
- preferências da empresa;
- integrações;
- backup;
- sincronização;
- IA;
- segurança;
- auditoria.

---

# 123. Configurações Gerais

## CreateSystemConfigurationCommand

Cria uma configuração global.

Permissão

```text
configuration.system.create
```

Payload

```json
{
  "key": "system.default_timezone",
  "value": "America/Sao_Paulo",
  "scope": "GLOBAL",
  "description": "Timezone padrão"
}
```

Escopos

```text
GLOBAL
TENANT
BRANCH
USER
DEVICE
```

Validações

- chave única
- formato válido
- tipo conhecido
- escopo permitido

Evento

```text
configuration.system_created
```

---

## UpdateSystemConfigurationCommand

Atualiza configuração.

Permissão

```text
configuration.system.update
```

Payload

```json
{
    "configuration_id":"uuid",
    "value":"America/Sao_Paulo"
}
```

Evento

```text
configuration.system_updated
```

---

## DeleteSystemConfigurationCommand

Remove configuração.

Evento

```text
configuration.system_deleted
```

---

# 124. Tenant Configuration

## CreateTenantConfigurationCommand

Cria configuração específica da empresa.

Permissão

```text
configuration.tenant.create
```

Payload

```json
{
    "tenant_id":"uuid",
    "key":"sales.default_validity_days",
    "value":"10"
}
```

Evento

```text
configuration.tenant_created
```

---

## UpdateTenantConfigurationCommand

Evento

```text
configuration.tenant_updated
```

---

## DeleteTenantConfigurationCommand

Evento

```text
configuration.tenant_deleted
```

---

# 125. Branch Configuration

## CreateBranchConfigurationCommand

Permissão

```text
configuration.branch.create
```

Payload

```json
{
    "branch_id":"uuid",
    "key":"warehouse.default",
    "value":"MAIN"
}
```

Evento

```text
configuration.branch_created
```

---

## UpdateBranchConfigurationCommand

Evento

```text
configuration.branch_updated
```

---

## DeleteBranchConfigurationCommand

Evento

```text
configuration.branch_deleted
```

---

# 126. User Preferences

## CreateUserPreferenceCommand

Cria preferência do usuário.

Exemplos

```text
Tema

Idioma

Tela Inicial

Sidebar

Última tela

Densidade

Modo Escuro

Zoom

Notificações

Dashboard
```

Evento

```text
configuration.user_preference_created
```

---

## UpdateUserPreferenceCommand

Evento

```text
configuration.user_preference_updated
```

---

## ResetUserPreferencesCommand

Evento

```text
configuration.user_preferences_reset
```

---

# 127. Branding

O Branding nunca deverá estar hardcoded.

Tudo deverá ser configurável.

## UpdateBrandCommand

Payload

```json
{
    "company_name":"OrganizeG3",
    "logo_light":"document_id",
    "logo_dark":"document_id",
    "favicon":"document_id",
    "login_background":"document_id"
}
```

Evento

```text
configuration.brand_updated
```

---

# 128. Theme

Toda a identidade visual será controlada pelo Theme Engine.

Nunca utilizar:

```python
QColor("#1A73E8")
```

ou

```css
background:#1A73E8;
```

Os módulos deverão utilizar somente Design Tokens.

Exemplo

```text
theme.primary

theme.secondary

theme.success

theme.warning

theme.error

theme.surface

theme.background

theme.border

theme.text.primary

theme.text.secondary
```

---

## UpdateThemeCommand

Evento

```text
configuration.theme_updated
```

---

## PublishThemeCommand

Publica uma nova versão.

Evento

```text
configuration.theme_published
```

---

## RollbackThemeCommand

Retorna para versão anterior.

Evento

```text
configuration.theme_rollback
```

---

# 129. Design System

Todo componente visual deverá vir do Theme Design.

Nunca poderá existir botão desenhado diretamente em telas.

Componentes

```text
Buttons

Cards

Inputs

Select

Checkbox

Switch

Tables

Dialogs

Menus

Tabs

Accordions

Badges

Avatars

Timeline

Kanban

Charts

Icons

Typography

Spacing

Elevation

Radius

Animations
```

---

## PublishDesignSystemVersionCommand

Evento

```text
configuration.design_system_published
```

---

# 130. Typography

Configurações

```text
Fonte

Peso

Espaçamento

Escala

Tamanho

Line Height
```

Comandos

```text
UpdateTypographyCommand

PublishTypographyCommand
```

---

# 131. Icon Library

O sistema utilizará biblioteca centralizada.

Nunca SVG espalhados.

Comandos

```text
RegisterIconCommand

UpdateIconCommand

ArchiveIconCommand

PublishIconLibraryCommand
```

---

# 132. Color Palette

Toda cor pertence ao Theme.

Categorias

```text
Primary

Secondary

Accent

Neutral

Success

Warning

Danger

Info

Gray Scale
```

Comandos

```text
CreateColorPaletteCommand

UpdateColorPaletteCommand

PublishColorPaletteCommand
```

---

# 133. Calendars

Calendários empresariais.

Comandos

```text
CreateCalendarCommand

UpdateCalendarCommand

ArchiveCalendarCommand

AssignCalendarCommand
```

---

# 134. Working Hours

Horários.

Exemplo

```text
Segunda

07:30

12:00

13:00

17:30
```

Comandos

```text
CreateWorkingHoursCommand

UpdateWorkingHoursCommand

AssignWorkingHoursCommand
```

---

# 135. Holidays

Comandos

```text
CreateHolidayCommand

UpdateHolidayCommand

ArchiveHolidayCommand
```

Tipos

```text
Nacional

Estadual

Municipal

Empresa

Departamento
```

---

# 136. Languages

Idiomas suportados.

```text
pt-BR

en-US

es-ES
```

Comandos

```text
RegisterLanguageCommand

PublishLanguageCommand

SetDefaultLanguageCommand
```

---

# 137. Currency

Moedas.

```text
BRL

USD

EUR
```

Comandos

```text
RegisterCurrencyCommand

UpdateExchangeRateCommand

PublishExchangeRateCommand
```

---

# 138. Units of Measure

Comandos

```text
CreateUnitCommand

UpdateUnitCommand

ArchiveUnitCommand
```

Exemplos

```text
UN

KG

M²

M³

CX

PAR

KIT
```

---

# 139. Numbering

Numeração automática.

Exemplos

```text
Pedidos

Compras

Produção

Notas

Financeiro

Projetos
```

Comandos

```text
CreateNumberingRuleCommand

UpdateNumberingRuleCommand

ResetSequenceCommand

ReserveSequenceCommand
```

---

# 140. Tags

Comandos

```text
CreateTagCommand

UpdateTagCommand

ArchiveTagCommand
```

---

# 141. Categories

Categorias configuráveis.

Comandos

```text
CreateCategoryCommand

UpdateCategoryCommand

ArchiveCategoryCommand
```

---

# 142. Backup

Configuração.

Exemplos

```text
Destino

Horário

Retenção

Compressão

Criptografia
```

Comandos

```text
ConfigureBackupCommand

RunBackupCommand

RestoreBackupCommand

DeleteBackupCommand
```

---

# 143. Synchronization Settings

Configurações.

```text
Offline

Retry

Compression

Encryption

Batch

Timeout
```

Comandos

```text
ConfigureSynchronizationCommand

UpdateSynchronizationCommand
```

---

# 144. Security Settings

Configurações

```text
MFA

Senha

JWT

Sessão

Timeout

Bloqueio

IP

Device
```

Comandos

```text
ConfigureSecurityCommand

UpdatePasswordPolicyCommand

UpdateSessionPolicyCommand
```

---

# 145. Audit Settings

Comandos

```text
ConfigureAuditCommand

UpdateAuditRetentionCommand

ArchiveAuditLogsCommand
```

---

# 146. AI Settings

Configurações da IA.

```text
Modelo

Temperatura

Tokens

Ferramentas

RAG

Embeddings
```

Comandos

```text
ConfigureAICommand

UpdateAIModelCommand

PublishAIConfigurationCommand
```

---

# 147. Feature Flags

Toda funcionalidade nova deverá utilizar Feature Flags.

Comandos

```text
CreateFeatureFlagCommand

EnableFeatureFlagCommand

DisableFeatureFlagCommand

ArchiveFeatureFlagCommand
```

---

# 148. Licensing

Comandos

```text
ConfigureLicenseCommand

ActivateLicenseCommand

SuspendLicenseCommand

RenewLicenseCommand
```

---

# 149. Configuration Events

Eventos principais

```text
configuration.system_created

configuration.system_updated

configuration.tenant_created

configuration.branch_created

configuration.theme_updated

configuration.design_system_published

configuration.brand_updated

configuration.language_published

configuration.currency_updated

configuration.calendar_created

configuration.working_hours_updated

configuration.holiday_created

configuration.backup_configured

configuration.security_updated

configuration.audit_updated

configuration.ai_updated

configuration.feature_flag_enabled

configuration.feature_flag_disabled

configuration.license_activated

configuration.license_suspended
```

---

# 150. Regras do Configuration

Toda configuração deve possuir:

```text
tenant_id

version

created_at

updated_at

created_by

updated_by
```

Toda alteração gera auditoria.

Toda configuração pode ser versionada.

Toda configuração pode ser exportada.

Toda configuração pode ser importada.

Nenhuma configuração poderá ser hardcoded nos módulos do sistema.

O Desktop, Web, API e Mobile deverão consumir exatamente a mesma configuração.

O Theme Design será a única fonte de verdade para:

- cores;
- fontes;
- ícones;
- componentes;
- espaçamentos;
- sombras;
- bordas;
- animações;
- imagens institucionais.

# 151. Automation

## Visão Geral

O contexto **Automation** é responsável por toda a automação do OrganizeG3.

Nenhum módulo deverá executar ações automáticas diretamente.

Toda automação deverá ser cadastrada, versionada, auditada e executada pela Automation Engine.

A engine deverá permitir:

- gatilhos (Triggers);
- condições (Conditions);
- ações (Actions);
- expressões;
- variáveis;
- agendamentos;
- filas;
- webhooks;
- workflows;
- notificações;
- integrações;
- IA;
- scripts futuros;
- versionamento;
- rollback.

---

# 152. Arquitetura da Engine

A Automation Engine será composta por:

```text
Trigger Engine

Condition Engine

Expression Engine

Workflow Engine

Action Engine

Queue Engine

Retry Engine

Scheduler

Webhook Engine

Event Bus

Execution History

Dead Letter Queue
```

Todo workflow deverá seguir:

```text
Evento

↓

Trigger

↓

Condições

↓

Ações

↓

Eventos

↓

Logs
```

---

# 153. Triggers

Os gatilhos poderão ser:

```text
Event Trigger

Cron Trigger

Webhook Trigger

Manual Trigger

Time Trigger

Interval Trigger

AI Trigger

System Trigger
```

---

## RegisterTriggerCommand

Evento

```text
automation.trigger_registered
```

---

## EnableTriggerCommand

Evento

```text
automation.trigger_enabled
```

---

## DisableTriggerCommand

Evento

```text
automation.trigger_disabled
```

---

## DeleteTriggerCommand

Evento

```text
automation.trigger_deleted
```

---

# 154. Event Triggers

Exemplos

```text
Pedido aprovado

Cliente criado

Fornecedor criado

Material recebido

Pagamento recebido

NF autorizada

Produção concluída

Estoque abaixo do mínimo

Backup concluído

Usuário criado

Documento assinado

Projeto finalizado
```

Todos os eventos publicados poderão iniciar automações.

---

# 155. Time Triggers

Exemplos

```text
Todo dia

Toda hora

Todo minuto

Toda segunda-feira

Todo mês

Todo trimestre

Todo ano

Primeiro dia útil

Último dia útil

10 minutos antes

5 dias depois
```

---

## CreateScheduleCommand

Evento

```text
automation.schedule_created
```

---

## UpdateScheduleCommand

Evento

```text
automation.schedule_updated
```

---

## DeleteScheduleCommand

Evento

```text
automation.schedule_deleted
```

---

# 156. Conditions

Uma automação poderá possuir:

```text
1 condição

10 condições

100 condições
```

Operadores

```text
AND

OR

NOT

XOR
```

Comparações

```text
=

!=

>

<

>=

<=

contains

startsWith

endsWith

exists

empty

between

in
```

---

## CreateConditionCommand

Evento

```text
automation.condition_created
```

---

## UpdateConditionCommand

Evento

```text
automation.condition_updated
```

---

## DeleteConditionCommand

Evento

```text
automation.condition_deleted
```

---

# 157. Expressions

Expressões suportadas

```text
Matemática

Texto

Datas

Boolean

JSON

Arrays

UUID

Regex
```

Exemplos

```text
today()

now()

addDays()

upper()

lower()

length()

sum()

avg()

count()

uuid()

if()
```

---

# 158. Variables

Tipos

```text
Workflow Variables

System Variables

Context Variables

User Variables

Tenant Variables

Temporary Variables
```

Exemplos

```text
CurrentUser

CurrentTenant

Today

Now

CorrelationId

WorkflowId

OrderId

CustomerId
```

---

## CreateVariableCommand

Evento

```text
automation.variable_created
```

---

# 159. Actions

Toda automação termina executando uma ou mais ações.

Exemplos

```text
Criar Pedido

Atualizar Pedido

Criar Cliente

Criar Compra

Criar Produção

Criar Financeiro

Enviar Email

Enviar WhatsApp

Enviar Push

Criar Documento

Mover Kanban

Executar IA

Executar Webhook

Executar Integração

Gerar PDF

Gerar Relatório

Criar Evento

Agendar Processo
```

---

## RegisterActionCommand

Evento

```text
automation.action_registered
```

---

# 160. Workflow

Um Workflow representa uma automação completa.

Estados

```text
Draft

Published

Paused

Archived
```

---

## CreateWorkflowCommand

Evento

```text
automation.workflow_created
```

---

## PublishWorkflowCommand

Evento

```text
automation.workflow_published
```

---

## PauseWorkflowCommand

Evento

```text
automation.workflow_paused
```

---

## ArchiveWorkflowCommand

Evento

```text
automation.workflow_archived
```

---

# 161. Workflow Steps

Cada workflow poderá possuir:

```text
Trigger

↓

Condition

↓

Action

↓

Condition

↓

Action

↓

End
```

Também poderá possuir:

```text
Loops

Branches

Parallel

Delay

Wait

Retry

Decision
```

---

## AddWorkflowStepCommand

Evento

```text
automation.workflow_step_added
```

---

## UpdateWorkflowStepCommand

Evento

```text
automation.workflow_step_updated
```

---

## DeleteWorkflowStepCommand

Evento

```text
automation.workflow_step_deleted
```

---

# 162. Delay

Exemplos

```text
Esperar 5 minutos

Esperar 1 hora

Esperar 3 dias

Esperar até segunda

Esperar até pagamento
```

---

## AddDelayCommand

Evento

```text
automation.delay_added
```

---

# 163. Retry

Toda ação poderá possuir Retry.

Configurações

```text
Tentativas

Backoff

Timeout

Retry Delay

Retry Forever

Maximum Attempts
```

---

## ConfigureRetryCommand

Evento

```text
automation.retry_configured
```

---

# 164. Dead Letter Queue

Caso uma automação falhe definitivamente.

Ela será enviada para:

```text
Dead Letter Queue
```

Permitindo:

```text
Reprocessar

Cancelar

Ignorar

Editar

Duplicar
```

---

## MoveToDeadLetterCommand

Evento

```text
automation.dead_letter_created
```

---

## ReprocessDeadLetterCommand

Evento

```text
automation.dead_letter_reprocessed
```

---

# 165. Scheduler

O Scheduler executará:

```text
Cron

Intervalos

Data específica

Recorrência

Calendários

Feriados

Dias úteis
```

---

## CreateSchedulerJobCommand

Evento

```text
automation.scheduler_job_created
```

---

## PauseSchedulerJobCommand

Evento

```text
automation.scheduler_job_paused
```

---

## ResumeSchedulerJobCommand

Evento

```text
automation.scheduler_job_resumed
```

---

# 166. Webhooks

Uma automação poderá:

```text
Receber Webhook

Enviar Webhook

Transformar Payload

Validar Assinatura

Responder HTTP
```

---

## RegisterWebhookCommand

Evento

```text
automation.webhook_registered
```

---

## ExecuteWebhookCommand

Evento

```text
automation.webhook_executed
```

---

# 167. Integrações

Uma automação poderá executar:

```text
REST API

GraphQL

gRPC

RabbitMQ

Kafka

Azure Queue

SQS

FTP

SFTP

Email

WhatsApp

SMS
```

---

## ExecuteIntegrationCommand

Evento

```text
automation.integration_executed
```

---

# 168. Notificações

Uma automação poderá enviar:

```text
Email

WhatsApp

Push

Desktop

SMS

Teams

Slack

Discord
```

---

## SendNotificationCommand

Evento

```text
automation.notification_sent
```

---

# 169. IA

Uma automação poderá utilizar IA.

Exemplos

```text
Classificar documento

Responder cliente

Criar resumo

Extrair dados

Traduzir

Gerar texto

Gerar descrição

Gerar código

Classificar imagens
```

---

## ExecuteAIActionCommand

Evento

```text
automation.ai_action_executed
```

---

# 170. Histórico

Toda execução deverá armazenar:

```text
Workflow

Trigger

Tempo

Usuário

Tenant

Resultado

Logs

Inputs

Outputs

Retries

Erros
```

---

## QueryExecutionHistory

Permite consultar todo histórico.

Filtros

```text
Workflow

Data

Usuário

Tenant

Status

Trigger

Evento
```

---

# 171. Logs

Cada etapa armazenará:

```text
Started

Executing

Finished

Duration

Memory

CPU

CorrelationId

EventId

WorkflowId
```

---

# 172. Versionamento

Cada Workflow possuirá:

```text
Versão

Autor

Data

Descrição

Rollback

Histórico
```

---

## PublishWorkflowVersionCommand

Evento

```text
automation.workflow_version_published
```

---

## RollbackWorkflowCommand

Evento

```text
automation.workflow_rollback
```

---

# 173. Eventos da Automation

```text
automation.workflow_created

automation.workflow_published

automation.workflow_paused

automation.workflow_archived

automation.trigger_registered

automation.trigger_enabled

automation.trigger_disabled

automation.condition_created

automation.action_registered

automation.workflow_step_added

automation.execution_started

automation.execution_completed

automation.execution_failed

automation.retry_started

automation.retry_completed

automation.dead_letter_created

automation.dead_letter_reprocessed

automation.notification_sent

automation.integration_executed

automation.webhook_executed

automation.ai_action_executed
```

---

# 174. Regras da Automation

Toda automação deverá possuir:

```text
workflow_id

tenant_id

version

created_at

updated_at

created_by

updated_by

correlation_id
```

Nenhuma automação poderá alterar diretamente outro módulo.

Toda comunicação deverá ocorrer por:

- Commands;
- Events;
- Queries.

Toda execução deverá ser:

- auditável;
- idempotente quando necessário;
- versionada;
- reprocessável;
- rastreável.

Toda falha deverá ser registrada.

Toda execução deverá possuir histórico completo.

Nenhuma automação poderá executar código arbitrário diretamente.

Scripts personalizados deverão utilizar uma Sandbox específica em versões futuras.

# 175. Artificial Intelligence (AI)

## Visão Geral

O contexto **Artificial Intelligence (AI)** é responsável por toda a inteligência artificial do OrganizeG3.

Nenhum módulo do sistema deverá acessar diretamente provedores de IA.

Todos os módulos deverão utilizar exclusivamente o contexto **AI**, garantindo:

- desacoplamento;
- auditoria;
- troca futura de modelos;
- controle de custos;
- versionamento;
- segurança;
- observabilidade.

---

# 176. Arquitetura

A AI Engine será composta pelos seguintes serviços:

```text
AI Gateway

Prompt Engine

Agent Engine

Tool Engine

Memory Engine

Context Engine

Embedding Engine

OCR Engine

Speech Engine

Vision Engine

Classification Engine

Recommendation Engine

RAG Engine

Model Router

Safety Engine

Cost Monitor
```

Fluxo básico:

```text
Módulo

↓

AI Gateway

↓

Model Router

↓

Prompt

↓

Tools

↓

Modelo

↓

Resposta

↓

Eventos

↓

Histórico
```

---

# 177. AI Providers

O sistema nunca dependerá diretamente de um fornecedor.

Adaptadores previstos:

```text
OpenAI

Azure OpenAI

Anthropic

Google Gemini

Mistral

DeepSeek

Local LLM

Ollama

Future Providers
```

---

## RegisterAIProviderCommand

Evento

```text
ai.provider_registered
```

---

## EnableAIProviderCommand

Evento

```text
ai.provider_enabled
```

---

## DisableAIProviderCommand

Evento

```text
ai.provider_disabled
```

---

## TestAIProviderCommand

Evento

```text
ai.provider_tested
```

---

# 178. Model Router

O Model Router decidirá automaticamente qual modelo utilizar.

Critérios:

```text
Custo

Velocidade

Precisão

Idioma

Quantidade de Tokens

Visão

OCR

Embeddings

Imagem

Áudio

Ferramentas
```

Nunca o Desktop escolherá diretamente um modelo.

Sempre solicitará uma capacidade.

Exemplo

```text
GenerateText

Summarize

Translate

AnalyzeDocument

GenerateSQL

GenerateCode

VisionAnalysis
```

---

# 179. Prompts

Todos os prompts serão cadastrados.

Nunca hardcoded.

Categorias

```text
Sistema

Usuário

Assistente

Internos

Templates

RAG

OCR

Classificação
```

---

## CreatePromptCommand

Evento

```text
ai.prompt_created
```

---

## UpdatePromptCommand

Evento

```text
ai.prompt_updated
```

---

## PublishPromptCommand

Evento

```text
ai.prompt_published
```

---

## ArchivePromptCommand

Evento

```text
ai.prompt_archived
```

---

# 180. Prompt Versioning

Cada Prompt possuirá:

```text
Version

Author

Created

Description

Rollback

Variables

Model Compatibility
```

---

## PublishPromptVersionCommand

Evento

```text
ai.prompt_version_published
```

---

## RollbackPromptVersionCommand

Evento

```text
ai.prompt_version_rollback
```

---

# 181. AI Agents

Os agentes representam especialistas.

Exemplos

```text
Finance Agent

Production Agent

Purchasing Agent

Sales Agent

Inventory Agent

Quality Agent

Engineering Agent

Support Agent

Architecture Agent

Coding Agent

Document Agent
```

Cada agente poderá possuir:

```text
Prompt

Ferramentas

Memória

Objetivo

Limites

Temperatura

Modelo

Conhecimento
```

---

## CreateAgentCommand

Evento

```text
ai.agent_created
```

---

## UpdateAgentCommand

Evento

```text
ai.agent_updated
```

---

## PublishAgentCommand

Evento

```text
ai.agent_published
```

---

## ArchiveAgentCommand

Evento

```text
ai.agent_archived
```

---

# 182. Agent Memory

Tipos

```text
Conversation

Session

Tenant

User

Global

Temporary
```

A memória poderá utilizar:

```text
Redis

PostgreSQL

Vector Database

Future Storage
```

---

## StoreMemoryCommand

Evento

```text
ai.memory_stored
```

---

## DeleteMemoryCommand

Evento

```text
ai.memory_deleted
```

---

## ClearConversationMemoryCommand

Evento

```text
ai.memory_cleared
```

---

# 183. AI Tools

Ferramentas disponíveis aos agentes.

Exemplos

```text
Search Customer

Create Customer

Create Production Order

Generate Report

Search Inventory

Query Financial

Generate PDF

OCR Document

Translate

Summarize

Execute Workflow

Execute Automation

Generate SQL

Generate Code
```

---

## RegisterAIToolCommand

Evento

```text
ai.tool_registered
```

---

## EnableAIToolCommand

Evento

```text
ai.tool_enabled
```

---

## DisableAIToolCommand

Evento

```text
ai.tool_disabled
```

---

# 184. Tool Permissions

Cada ferramenta poderá definir:

```text
Allowed Roles

Allowed Tenants

Allowed Departments

Rate Limit

Timeout

Cost Limit
```

Nenhum agente poderá executar uma ferramenta sem autorização.

---

# 185. RAG Engine

A recuperação contextual utilizará:

```text
Embeddings

Vector Database

Chunking

Ranking

Re-ranking

Metadata

Filters
```

Fontes possíveis

```text
Documentos

Procedimentos

Contratos

Projetos

Normas

ERP

Histórico

Conhecimento interno
```

---

## IndexDocumentCommand

Evento

```text
ai.document_indexed
```

---

## ReindexDocumentCommand

Evento

```text
ai.document_reindexed
```

---

## DeleteEmbeddingCommand

Evento

```text
ai.embedding_deleted
```

---

# 186. OCR

Tipos

```text
PDF

Imagem

Scanner

Nota Fiscal

Contrato

Projeto

Desenho Técnico
```

---

## ExecuteOCRCommand

Evento

```text
ai.ocr_completed
```

---

# 187. Vision

A IA poderá analisar:

```text
Fotos

Renderizações

Projetos

Croquis

QR Code

Código de Barras

Peças

Produtos

Ambientes
```

---

## AnalyzeImageCommand

Evento

```text
ai.image_analyzed
```

---

# 188. Speech

Suporte futuro.

```text
Speech To Text

Text To Speech

Voice Commands
```

Comandos

```text
TranscribeAudioCommand

GenerateSpeechCommand
```

---

# 189. Classification

A IA poderá classificar automaticamente:

```text
Documentos

Emails

Chamados

Produtos

Clientes

Fornecedores

Projetos

Tickets
```

---

## ClassifyDocumentCommand

Evento

```text
ai.document_classified
```

---

# 190. Recommendations

Sugestões automáticas.

Exemplos

```text
Comprar Material

Aumentar Estoque

Cobrar Cliente

Enviar Proposta

Gerar Backup

Atualizar Contrato

Treinar Funcionário
```

---

## GenerateRecommendationCommand

Evento

```text
ai.recommendation_generated
```

---

# 191. Chat Sessions

Cada conversa possuirá:

```text
SessionId

UserId

TenantId

Messages

Context

Prompt Version

Model

Temperature

Cost

Duration
```

---

## StartChatSessionCommand

Evento

```text
ai.chat_started
```

---

## FinishChatSessionCommand

Evento

```text
ai.chat_finished
```

---

# 192. Cost Monitor

A AI Engine acompanhará:

```text
Tokens

Input Tokens

Output Tokens

Preço

Modelo

Tempo

Usuário

Tenant

Departamento
```

---

## GenerateAICostReportCommand

Evento

```text
ai.cost_report_generated
```

---

# 193. Safety

Toda requisição deverá passar pelo Safety Engine.

Verificações

```text
Prompt Injection

SQL Injection

PII

Segredos

Dados Sensíveis

Código Malicioso

Prompt Leak
```

---

## ValidatePromptCommand

Evento

```text
ai.prompt_validated
```

---

# 194. Observabilidade

Registrar:

```text
CorrelationId

Prompt

Modelo

Ferramentas

Tempo

Custo

Tokens

Usuário

Tenant

Resposta

Erros
```

---

# 195. Eventos da AI

```text
ai.provider_registered

ai.provider_enabled

ai.prompt_created

ai.prompt_updated

ai.prompt_published

ai.agent_created

ai.agent_updated

ai.agent_published

ai.memory_stored

ai.tool_registered

ai.document_indexed

ai.ocr_completed

ai.image_analyzed

ai.document_classified

ai.recommendation_generated

ai.chat_started

ai.chat_finished

ai.cost_report_generated

ai.prompt_validated
```

---

# 196. Regras da AI

Toda operação deverá possuir:

```text
tenant_id

user_id

correlation_id

prompt_version

provider

model

created_at
```

Regras obrigatórias:

- nenhum provedor externo será chamado diretamente pelos módulos;
- todos os prompts deverão ser versionados;
- todas as respostas deverão ser auditáveis;
- ferramentas deverão possuir autorização explícita;
- memória deverá respeitar o isolamento por Tenant;
- custos deverão ser registrados por execução;
- o sistema deverá permitir troca de provedor sem alterar o domínio;
- nenhuma credencial poderá ser registrada em logs;
- o histórico de conversas poderá ser utilizado pelo RAG apenas quando autorizado pela política de privacidade.

# 197. Synchronization

## Visão Geral

O contexto **Synchronization** é responsável por toda sincronização entre os clientes do OrganizeG3.

Ele garante que Desktop, API, Mobile e futuras aplicações compartilhem exatamente o mesmo estado dos dados.

Nenhum módulo deverá implementar sincronização própria.

Toda sincronização deverá passar pela Synchronization Engine.

---

# 198. Arquitetura

A Synchronization Engine será composta por:

```text
Sync Gateway

Upload Queue

Download Queue

Conflict Resolver

Snapshot Engine

Delta Engine

Version Engine

Device Registry

Offline Engine

Compression Engine

Encryption Engine

Sync Monitor
```

Fluxo

```text
Desktop

↓

Local Queue

↓

API

↓

Event Bus

↓

Outros Clientes

↓

Sincronização
```

---

# 199. Device Registry

Cada dispositivo deverá ser registrado.

Tipos

```text
Desktop

Notebook

Servidor

Tablet

Mobile

Web Browser
```

---

## RegisterDeviceCommand

Evento

```text
sync.device_registered
```

---

## UpdateDeviceCommand

Evento

```text
sync.device_updated
```

---

## DisableDeviceCommand

Evento

```text
sync.device_disabled
```

---

# 200. Offline Mode

O sistema deverá funcionar offline.

Enquanto offline deverá permitir:

```text
Criar registros

Editar registros

Excluir registros

Consultar cache

Executar workflows locais

Imprimir

Gerar documentos
```

Ao reconectar:

```text
Enviar alterações

Receber alterações

Resolver conflitos
```

---

## EnableOfflineModeCommand

Evento

```text
sync.offline_enabled
```

---

## DisableOfflineModeCommand

Evento

```text
sync.offline_disabled
```

---

# 201. Local Queue

Toda alteração realizada offline será registrada.

Cada item possuirá:

```text
QueueId

Command

Payload

CorrelationId

CreatedAt

RetryCount

Status
```

Estados

```text
Pending

Uploading

Completed

Failed

Cancelled
```

---

## EnqueueSyncCommand

Evento

```text
sync.command_queued
```

---

## RemoveQueuedCommand

Evento

```text
sync.command_removed
```

---

# 202. Upload Engine

Responsável por enviar alterações locais.

Critérios

```text
Lotes

Compressão

Prioridade

Retry

Timeout

Checksum
```

---

## UploadChangesCommand

Evento

```text
sync.upload_completed
```

---

# 203. Download Engine

Responsável por baixar alterações.

Critérios

```text
Delta

Snapshot

Version

Checksum

Tenant

Branch
```

---

## DownloadChangesCommand

Evento

```text
sync.download_completed
```

---

# 204. Delta Sync

Sempre que possível utilizar sincronização incremental.

Nunca baixar novamente registros inalterados.

Estratégias

```text
Timestamp

Version

Sequence

Event

Snapshot
```

---

## GenerateDeltaCommand

Evento

```text
sync.delta_generated
```

---

# 205. Snapshot

Snapshots poderão ser utilizados para:

```text
Primeira sincronização

Novo dispositivo

Recuperação

Restauração

Migração
```

---

## GenerateSnapshotCommand

Evento

```text
sync.snapshot_generated
```

---

## RestoreSnapshotCommand

Evento

```text
sync.snapshot_restored
```

---

# 206. Version Engine

Cada registro possuirá:

```text
Version

UpdatedAt

UpdatedBy

CorrelationId

DeviceId
```

Toda alteração incrementará:

```text
Version +1
```

---

# 207. Conflict Resolution

Conflitos poderão ocorrer quando:

```text
Desktop altera

↓

API altera

↓

Mobile altera
```

Antes da sincronização.

Tipos

```text
Update x Update

Delete x Update

Delete x Delete

Insert x Insert
```

---

## ResolveConflictCommand

Evento

```text
sync.conflict_resolved
```

---

## RejectConflictCommand

Evento

```text
sync.conflict_rejected
```

---

# 208. Estratégias de Conflito

O sistema deverá suportar:

```text
Last Write Wins

Server Wins

Client Wins

Manual Merge

Custom Resolver

Domain Resolver
```

Cada Aggregate poderá definir sua própria estratégia.

---

# 209. Retry

Toda sincronização poderá utilizar Retry.

Configurações

```text
Maximum Attempts

Delay

Backoff

Timeout

Circuit Breaker
```

---

## RetrySynchronizationCommand

Evento

```text
sync.retry_started
```

---

# 210. Compression

Suporte

```text
GZIP

Brotli

Future Compression
```

A sincronização poderá compactar:

```text
JSON

Arquivos

Snapshots

Eventos
```

---

# 211. Encryption

Toda comunicação deverá utilizar:

```text
TLS

HTTPS

JWT

Refresh Token

Encrypted Payload
```

Arquivos poderão utilizar:

```text
AES

Future Encryption
```

---

# 212. Sync Monitor

Registrar

```text
Tempo

Bytes

Velocidade

Uploads

Downloads

Retries

Conflitos

Falhas
```

---

## GenerateSynchronizationReportCommand

Evento

```text
sync.report_generated
```

---

# 213. Sincronização de Arquivos

Arquivos deverão possuir:

```text
Checksum

Version

MimeType

Compression

Encryption

StorageId
```

Nunca sincronizar arquivos duplicados.

Sempre utilizar hash.

---

## SynchronizeDocumentCommand

Evento

```text
sync.document_synchronized
```

---

# 214. Device Policies

Cada dispositivo poderá possuir:

```text
Maximum Cache

Offline Days

Bandwidth Limit

Priority

Synchronization Interval
```

---

## UpdateDevicePolicyCommand

Evento

```text
sync.device_policy_updated
```

---

# 215. Eventos da Synchronization

```text
sync.device_registered

sync.device_updated

sync.offline_enabled

sync.offline_disabled

sync.command_queued

sync.command_removed

sync.upload_completed

sync.download_completed

sync.delta_generated

sync.snapshot_generated

sync.snapshot_restored

sync.conflict_detected

sync.conflict_resolved

sync.retry_started

sync.retry_completed

sync.document_synchronized

sync.report_generated
```

---

# 216. Regras da Synchronization

Toda sincronização deverá possuir:

```text
tenant_id

device_id

user_id

correlation_id

version

created_at
```

Regras obrigatórias

- toda sincronização deverá ser idempotente;
- nenhum Aggregate poderá ser sincronizado parcialmente;
- conflitos deverão ser registrados antes da resolução;
- arquivos deverão utilizar checksum;
- snapshots deverão possuir versão;
- deltas deverão ser preferidos sempre que possível;
- nenhuma sincronização poderá ignorar o isolamento por Tenant;
- dispositivos revogados não poderão sincronizar;
- toda operação deverá ser auditável;
- a sincronização deverá suportar milhões de registros sem necessidade de snapshots completos.
# 217. Regras Globais da Plataforma

## Visão Geral

As regras desta seção são obrigatórias para todos os módulos do OrganizeG3.

Nenhum contexto poderá descumpri-las.

Essas regras possuem prioridade superior às regras específicas de cada módulo.

---

# 218. Arquitetura

Toda implementação deverá seguir:

```text
DDD

Clean Architecture

CQRS

Event Driven

SOLID

Repository Pattern

Specification Pattern

Factory Pattern

Dependency Injection

Unit Of Work
```

Nunca será permitido:

```text
SQL direto na UI

Regras de negócio na interface

Acesso direto ao banco

Dependência circular

Imports cruzados entre Contextos
```

---

# 219. Bounded Contexts

Cada contexto é responsável exclusivamente pelo seu domínio.

Exemplos

```text
Financial

Inventory

CRM

Sales

Purchasing

Production

Quality

Projects

Documents

Workflow

Automation

AI

Synchronization

Configuration

Identity

Audit
```

Nenhum contexto poderá modificar diretamente os dados de outro.

Sempre deverá utilizar:

```text
Commands

Events

Queries
```

---

# 220. Multi-Tenant

Todo registro deverá possuir:

```text
tenant_id
```

Quando aplicável:

```text
branch_id

department_id
```

Nunca será permitido consultar dados de outro Tenant.

Toda Query deverá aplicar isolamento.

---

# 221. Auditoria

Toda alteração deverá registrar:

```text
Who

When

Where

Device

CorrelationId

Old Values

New Values

Command

Aggregate

Version
```

Jamais apagar auditoria.

---

# 222. Soft Delete

Nenhum registro importante será removido fisicamente.

Utilizar:

```text
is_deleted

deleted_at

deleted_by
```

Exceções somente para:

```text
Cache

Tokens

Logs Temporários

Filas Transitórias
```

---

# 223. Versionamento

Todos os Aggregates deverão possuir:

```text
version
```

Atualizações:

```text
Version++

```

Objetivos

```text
Concorrência

Sincronização

Auditoria

Rollback
```

---

# 224. Concurrency

Utilizar:

```text
Optimistic Lock
```

Sempre que possível.

Quando necessário:

```text
Pessimistic Lock
```

Casos

```text
Sequências fiscais

Numeração

Saldo Financeiro

Reserva de Estoque
```

---

# 225. Transactions

Toda operação crítica deverá utilizar transação.

Exemplos

```text
Pagamento

Recebimento

Produção

Emissão Fiscal

Movimentação

Transferência
```

Nunca realizar:

```text
Commit parcial
```

---

# 226. Idempotência

Comandos críticos deverão aceitar:

```text
Idempotency Key
```

Exemplos

```text
Emitir Nota

Receber Pagamento

Criar Pedido

Criar Produção

Executar Workflow

Webhook

Integrações
```

---

# 227. Eventos

Todo evento deverá possuir:

```text
EventId

AggregateId

OccurredAt

CorrelationId

TenantId

Version

Payload
```

Eventos são imutáveis.

Nunca editar um evento.

---

# 228. Commands

Todo Command deverá possuir:

```text
CommandId

CorrelationId

TenantId

UserId

OccurredAt
```

Commands não retornam entidades.

Retornam apenas:

```text
Success

Failure

Validation

Ids
```

---

# 229. Queries

Queries nunca modificam dados.

Queries:

```text
Read Only
```

Poderão utilizar:

```text
Views

Materialized Views

Read Models

Cache
```

---

# 230. Eventos x Commands

Commands

```text
Intent
```

Eventos

```text
Fact
```

Exemplo

```text
CreateSalesOrderCommand

↓

sales_order_created
```

---

# 231. Time

Todo horário deverá utilizar:

```text
UTC
```

Na apresentação:

```text
Timezone do Usuário
```

Nunca utilizar horário local para persistência.

---

# 232. Datas

Separar claramente:

```text
CreatedAt

UpdatedAt

DeletedAt

OccurredAt

ExecutedAt

DueDate

IssueDate

ApprovalDate
```

---

# 233. UUID

Todos os IDs deverão utilizar:

```text
UUID v4
```

Nunca:

```text
Auto Increment
```

Como chave pública.

---

# 234. Arquivos

Todos os arquivos deverão possuir:

```text
Hash

MimeType

Version

StorageId

Size

CreatedAt
```

Nunca armazenar arquivos diretamente no banco.

---

# 235. Logs

Toda aplicação deverá utilizar logs estruturados.

Campos mínimos

```text
CorrelationId

Tenant

User

Device

Service

Module

Duration

Level

Exception
```

Nunca utilizar:

```python
print()
```

Para logs de produção.

---

# 236. Configurações

Nenhum módulo poderá possuir:

```python
URL = "..."

COR = "#2196F3"

API_KEY = "..."

TIMEOUT = 30
```

Tudo deverá vir do Configuration.

---

# 237. Theme

Toda UI deverá utilizar exclusivamente:

```text
Theme Design
```

Nunca:

```text
Cor fixa

Fonte fixa

Ícone fixo

Espaçamento fixo
```

---

# 238. Componentes

Desktop

Web

Mobile

Utilizarão os mesmos:

```text
Tokens

Tipografia

Ícones

Paleta

Radius

Elevation

Spacing
```

---

# 239. Segurança

Nunca armazenar:

```text
Senha

JWT

Refresh Token

Segredo

Private Key

Certificado
```

Em texto puro.

Sempre utilizar:

```text
Vault

Secrets

Encrypted Storage
```

---

# 240. Permissões

Toda operação deverá verificar:

```text
Tenant

Role

Permission

Policy
```

Nunca confiar na interface.

---

# 241. API

Toda API deverá possuir:

```text
Version

OpenAPI

Swagger

Health

Metrics

CorrelationId
```

---

# 242. Health Checks

Serviços

```text
Database

Redis

Storage

Email

Queue

Supabase

AI

Webhook
```

Estados

```text
Healthy

Degraded

Unhealthy
```

---

# 243. Observabilidade

Utilizar:

```text
Metrics

Logs

Tracing

Health

Alerts
```

Sempre com CorrelationId.

---

# 244. Performance

Prioridades

```text
Cache

Lazy Loading

Pagination

Streaming

Compression

Indexes
```

Evitar

```text
N+1

Queries desnecessárias

Carga completa
```

---

# 245. Cache

Tipos

```text
Memory

Redis

Read Model

Query Cache
```

Nunca cachear:

```text
Permissões críticas

Saldo financeiro

Autenticação
```

Sem invalidação.

---

# 246. Internacionalização

Toda string deverá permitir tradução.

Nunca escrever diretamente:

```python
"Salvar"

"Excluir"

"Cancelar"
```

Utilizar:

```text
Localization Keys
```

---

# 247. Feature Flags

Toda funcionalidade nova deverá possuir:

```text
Feature Flag
```

Permitindo:

```text
Ativar

Desativar

Rollback

Canary

Beta
```

---

# 248. Testes

Toda funcionalidade deverá possuir:

```text
Unit Test

Integration Test

Application Test

Contract Test
```

Quando aplicável.

---

# 249. Qualidade

Todo código deverá seguir:

```text
Ruff

Black

MyPy

Pytest

Pre-Commit
```

---

# 250. Eventos da Plataforma

```text
platform.started

platform.stopped

platform.updated

platform.backup_created

platform.restore_completed

platform.health_changed

platform.maintenance_started

platform.maintenance_finished

platform.version_published

platform.feature_enabled

platform.feature_disabled
```

---

# 251. Roadmap Arquitetural

A arquitetura foi projetada para suportar futuramente:

```text
Desktop

Web

Android

iOS

PWA

API Pública

Marketplace

Plugins

BI

Machine Learning

IoT

MES

WMS

CRM Completo

APS

MRP II

SCM

Integrações Bancárias

Assinatura Digital

Multi Empresa

Multi País

Multi Idioma

Multi Moeda

Multi Banco de Dados

Cluster

Microservices
```

---

# 252. Princípio Fundamental

Todo desenvolvimento do OrganizeG3 deverá obedecer aos seguintes princípios:

1. **Nenhuma regra de negócio na interface.**
2. **Nenhuma configuração hardcoded.**
3. **Nenhum acesso direto entre Contextos.**
4. **Tudo auditável.**
5. **Tudo versionável.**
6. **Tudo orientado a eventos.**
7. **Tudo preparado para sincronização offline.**
8. **Tudo preparado para IA.**
9. **Tudo preparado para múltiplos Tenants.**
10. **Toda decisão arquitetural deve priorizar escalabilidade, manutenibilidade e desacoplamento acima da conveniência imediata.**

---

# 253. Próxima Etapa

A documentação funcional do OrganizeG3 está praticamente concluída.

A próxima fase deverá ser a **Especificação Técnica**, contemplando:

```text
Models (Domínio)

Aggregates

Entities

Value Objects

Repositories

Domain Services

Application Services

Commands

Queries

Handlers

Events

Policies

Validators

DTOs

Mappers

Use Cases

API Contracts

Database Schema

Indexes

Migrations

Event Bus

Queues

Workers

Desktop Architecture

Web Architecture

Mobile Architecture

CI/CD

Deploy

Observability

Performance Benchmarks
```

Essa especificação servirá como base definitiva para a implementação do sistema.
