\# AI Development Guide — OrganizeG3



> Instruções obrigatórias para qualquer agente de Inteligência Artificial que crie, altere, revise ou analise código do OrganizeG3.



\---



| Propriedade            | Valor                           |

| ---------------------- | ------------------------------- |

| Documento              | AI\_DEVELOPMENT\_GUIDE.md         |

| Status                 | Obrigatório — revisado para frontend React/PWA |

| Prioridade             | Máxima                          |

| Abrangência            | Todo o repositório              |

| Público                | Agentes de IA e desenvolvedores |

| Idioma da documentação | Português                       |

| Idioma do código       | Inglês                          |



\---



\# 1. Objetivo



Este documento estabelece as regras obrigatórias para desenvolvimento assistido por Inteligência Artificial no OrganizeG3.

A partir de 2026-08-08, `ADR-UI-001_FRONTEND_UNIFICADO_REACT_PWA.md` é obrigatório para qualquer trabalho de UI/UX e prevalece sobre referências antigas a PySide6/Qt Widgets como interface principal.




Antes de criar ou modificar qualquer arquivo, o agente deverá:



1\. compreender o objetivo da tarefa;

2\. identificar o domínio afetado;

3\. localizar os contratos existentes;

4\. verificar as regras arquiteturais;

5\. analisar impactos em banco, API, eventos, permissões, sincronização e testes;

6\. alterar somente o necessário.



O agente não deverá escolher o caminho mais curto quando esse caminho comprometer a arquitetura ou a manutenção futura.



\---



\# 2. Contexto do produto



O OrganizeG3 é uma plataforma operacional inteligente para empresas orientadas a processos.



A plataforma deverá atender inicialmente empresas que trabalham sob encomenda, mas não poderá depender de um segmento específico.



Conceitos centrais:



\* empresa;

\* filial;

\* setor;

\* usuário;

\* funcionário;

\* cliente;

\* orçamento;

\* workflow;

\* etapa;

\* operação;

\* execução;

\* checklist;

\* documento;

\* ocorrência;

\* máquina;

\* estoque;

\* evento;

\* auditoria;

\* notificação;

\* automação;

\* capacidade.



\---



\# 3. Arquitetura obrigatória



O projeto utiliza separação entre:



```text

Presentation

&#x20;   ↓

Platform API

&#x20;   ↓

Application Layer

&#x20;   ↓

Domain

&#x20;   ↓

Ports

&#x20;   ↓

Infrastructure

```



As dependências devem apontar para dentro.



\## 3.1 Domain



O domínio contém:



\* entidades;

\* agregados;

\* objetos de valor;

\* regras;

\* políticas;

\* eventos de domínio;

\* exceções de negócio.



O domínio não pode importar:



\* FastAPI;

\* SQLAlchemy;

\* Supabase;

\* PySide6;

\* React;

\* TypeScript;

\* bibliotecas visuais;

\* implementações de banco;

\* clientes HTTP.



\## 3.2 Application Layer



A camada de aplicação contém:



\* comandos;

\* consultas;

\* handlers;

\* portas;

\* unidade de trabalho;

\* autorização;

\* coordenação de transações;

\* publicação de eventos.



Ela orquestra o domínio, mas não substitui suas regras.



\## 3.3 Infrastructure



A infraestrutura implementa:



\* repositórios;

\* persistência;

\* mensageria;

\* Storage;

\* Supabase;

\* notificações;

\* provedores externos;

\* integrações.



A infraestrutura depende dos contratos internos. O domínio nunca depende dela.



\## 3.4 Presentation

A Presentation oficial é o frontend unificado React/PWA e a API HTTP.

```text
React 19 + TypeScript
    ↓ HTTPS
FastAPI
    ↓
Application Layer
```

Desktop, notebook, tablet e celular utilizam a mesma aplicação React responsiva.

A Presentation não pode conter regras de negócio e não pode acessar SQLAlchemy, repositórios internos ou banco diretamente.

Regras obrigatórias para frontend:

\* utilizar `theme_design` como autoridade visual;

\* não utilizar valores visuais hardcoded em páginas ou componentes de feature;

\* utilizar componentes compartilhados antes de criar variações locais;

\* tabelas devem possuir comportamento responsivo explícito;

\* layouts não podem depender de largura fixa para funcionar;

\* ícones devem ser SVG vetoriais da biblioteca oficial;

\* estado de servidor deve ser tratado pelo mecanismo oficial de server state;

\* estado local de interface não deve duplicar dados de servidor;

\* autenticação, autorização e Tenant devem ser validados pelo backend;

\* nenhuma ação crítica pode existir somente no frontend.

PySide6/Qt Widgets deixa de ser a tecnologia da interface principal. Código PySide6 legado, quando ainda existir, é tratado apenas como legado de transição e não deve receber novas funcionalidades visuais sem decisão explícita.

A decisão arquitetural está formalizada em:

```text
ADR-UI-001_FRONTEND_UNIFICADO_REACT_PWA.md
```

\# 4. Regras de domínio



\## 4.1 Domínio antes da tabela



Não criar uma tabela apenas porque uma tela precisa armazenar determinado valor.



Antes de modelar persistência, identificar:



\* qual conceito está sendo representado;

\* quem é seu proprietário;

\* qual seu ciclo de vida;

\* quais invariantes possui;

\* qual agregado controla sua alteração;

\* quais eventos são gerados.



\## 4.2 Agregados



Toda alteração de negócio deve ocorrer através do agregado responsável.



Não alterar diretamente entidades internas de um agregado por repositórios, endpoints ou componentes visuais.



\## 4.3 Comandos explícitos



Operações de negócio devem utilizar comandos claros.



Preferir:



```text

StartExecutionCommand

PauseExecutionCommand

ResumeExecutionCommand

FinishExecutionCommand

MoveWorkflowInstanceCommand

RequestMaterialCommand

SubmitChecklistCommand

```



Evitar comandos genéricos:



```text

UpdateRecordCommand

ChangeStatusCommand

SaveEntityCommand

```



\## 4.4 Queries não alteram estado



Consultas devem ser livres de efeitos colaterais.



Nunca publicar evento de negócio ou alterar entidade durante uma query.



\---



\# 5. Multiempresa



Toda informação empresarial pertence a exatamente um Tenant.



Regras obrigatórias:



\* toda tabela empresarial possui `tenant\_id`;

\* o contexto do Tenant vem da sessão autenticada;

\* o cliente não escolhe livremente o `tenant\_id`;

\* consultas devem ser filtradas por Tenant;

\* políticas RLS devem reforçar o isolamento;

\* dados de diferentes Tenants nunca podem aparecer juntos sem permissão de plataforma explícita.



Não confiar apenas em filtros na interface.



\---



\# 6. Identidade e permissões



Usuário e Funcionário são conceitos diferentes.



\* `User`: identidade autenticada.

\* `Employee`: pessoa vinculada à operação da empresa.

\* `Membership`: vínculo do usuário com uma empresa.

\* `Role`: conjunto reutilizável de permissões.

\* `Permission`: autorização específica.



Nenhuma ação crítica deve depender apenas do nome de um cargo ou role.



A autorização deve validar permissões e escopos.



\---



\# 7. Workflow e Kanban



Workflow representa o processo.



Kanban representa apenas uma visualização.



A entidade principal não deve ser chamada de `WorkflowCard`.



Utilizar:



```text

WorkflowDefinition

WorkflowVersion

WorkflowStageDefinition

WorkflowTransitionDefinition

WorkflowInstance

```



Uma `WorkflowInstance` pode ser exibida como:



\* Kanban;

\* lista;

\* timeline;

\* calendário;

\* Gantt;

\* dashboard.



As etapas configuradas devem ser versionadas.



Alterações em um Workflow publicado não podem modificar silenciosamente processos existentes.



\---



\# 8. Operações e execuções



Etapa representa estado.



Operação representa trabalho.



Execução representa a realização concreta de uma operação.



Estrutura conceitual:



```text

WorkflowInstance

&#x20;   └── OperationInstance

&#x20;           └── OperationExecution

&#x20;                   ├── ExecutionParticipant

&#x20;                   ├── ExecutionPause

&#x20;                   └── ExecutionMachine

```



Uma operação pode:



\* possuir várias execuções;

\* ser executada novamente;

\* ter participantes simultâneos;

\* ser interrompida;

\* ser retomada;

\* gerar retrabalho;

\* ser ignorada com justificativa.



O tempo trabalhado e o tempo parado devem ser registrados separadamente.



\---



\# 9. Eventos e auditoria



\## 9.1 Eventos



Eventos representam fatos do domínio.



Exemplos:



```text

execution.started

execution.paused

execution.resumed

execution.finished

workflow.stage\_changed

incident.created

document.version\_uploaded

material.requested

```



Eventos devem ser:



\* imutáveis;

\* append-only;

\* versionados;

\* associados ao agregado;

\* associados a `correlation\_id`;

\* associados a `causation\_id` quando aplicável.



\## 9.2 Auditoria



Auditoria registra:



\* quem executou;

\* qual ação foi executada;

\* quando;

\* de onde;

\* qual entidade foi afetada;

\* estado anterior;

\* estado posterior;

\* justificativa.



Eventos e auditorias não são substitutos um do outro.



\## 9.3 Publicação segura



Eventos de integração devem utilizar o padrão Transactional Outbox.



Não publicar eventos externos antes da confirmação da transação.



\---



\# 10. Banco de dados



\## 10.1 SQLAlchemy



Utilizar SQLAlchemy 2.x com:



\* `DeclarativeBase`;

\* `Mapped`;

\* `mapped\_column`;

\* type hints;

\* UUID;

\* timestamps com timezone.



\## 10.2 Migrações



Toda alteração de schema deve possuir migração Alembic.



É proibido:



\* alterar banco manualmente e não registrar;

\* criar tabela em runtime com lógica improvisada;

\* adicionar coluna por verificação manual na inicialização;

\* executar `Base.metadata.create\_all()` em produção como sistema de migração.



\## 10.3 JSONB



JSONB deve ser usado somente quando os dados forem:



\* dinâmicos;

\* configuráveis;

\* extensíveis;

\* sem necessidade frequente de integridade relacional.



Não utilizar JSONB para evitar modelar entidades e relacionamentos conhecidos.



\## 10.4 Exclusão



Exclusão física não é o padrão.



Utilizar, conforme o caso:



\* `archived\_at`;

\* `deleted\_at`;

\* status de domínio.



Eventos, auditorias e versões publicadas devem ser protegidos contra alteração e exclusão.



\---



\# 11. API



A API é uma interface da Application Layer.



Endpoints de alteração devem representar intenções de negócio.



Preferir:



```http

POST /api/v1/executions/{id}/start

POST /api/v1/executions/{id}/pause

POST /api/v1/executions/{id}/resume

POST /api/v1/executions/{id}/finish

POST /api/v1/workflow-instances/{id}/move

```



Evitar depender exclusivamente de:



```http

PATCH /api/v1/executions/{id}

```



Operações críticas devem aceitar uma chave de idempotência.



Todas as respostas de erro devem possuir código estável.



\---



\# 12. Sincronização offline



A PWA deve enviar comandos, não atualizações arbitrárias de registros.



Todo comando offline deverá possuir:



\* `command\_id`;

\* `idempotency\_key`;

\* `device\_id`;

\* `actor\_user\_id`;

\* `tenant\_id` derivado da sessão;

\* timestamp;

\* payload;

\* versão do contrato.



Reenvios não podem duplicar efeitos.



Conflitos devem ser explícitos e auditáveis.



\---



\# 13. Documentos



Documento não é sinônimo de arquivo.



Estrutura:



```text

Document

&#x20;   └── DocumentVersion

&#x20;           └── StorageObject

```



O banco armazena metadados.



O arquivo físico permanece no Storage.



Arquivos de programas pesados, como SKP, DWG, RVT, CNC e equivalentes, não devem ser armazenados por padrão.



Documentos antigos devem permanecer acessíveis e identificados como:



\* desatualizados;

\* obsoletos;

\* arquivados.



\---



\# 14. Forms e checklists



Checklist é um tipo especializado de formulário.



Separar:



```text

FormDefinition

FormVersion

FormBinding

FormSubmission

```



Uma resposta deve permanecer vinculada à versão exata do formulário utilizada no preenchimento.



Respostas concluídas não devem mudar quando o modelo for atualizado.



\---



\# 15. Inteligência Artificial



A IA é uma capacidade transversal.



Ela pode:



\* consultar;

\* localizar;

\* explicar;

\* resumir;

\* comparar;

\* prever;

\* recomendar;

\* preparar comandos.



A IA não deve alterar diretamente o banco ou ignorar a Application Layer.



Toda ação proposta pela IA deve:



\* respeitar permissões;

\* utilizar os casos de uso oficiais;

\* ser auditável;

\* exigir confirmação quando aplicável.



Não armazenar dados sensíveis em prompts ou logs sem necessidade e autorização.



\---



\# 16. Design System



Esta regra é obrigatória.



Nenhum arquivo de tela, página ou componente poderá conter valores visuais hardcoded.



É proibido definir diretamente fora do sistema de design:



\* valores hexadecimais;

\* cores RGB;

\* nomes de fontes;

\* tamanhos de fontes;

\* espaçamentos;

\* margens;

\* paddings;

\* raios;

\* sombras;

\* ícones;

\* caminhos de imagens;

\* animações;

\* durações;

\* breakpoints;

\* estilos de estados.



\## 16.1 Fonte oficial



Toda informação visual deve vir de:



```text

packages/design\_tokens

```



ou da implementação:



```text

theme\_design

```



\## 16.2 Intenção visual



Telas devem declarar intenção.



Correto:



```python

PrimaryButton(

&#x20;   text="Salvar",

&#x20;   icon=Icons.SAVE,

)

```



Incorreto:



```python

button.setStyleSheet(

&#x20;   "background-color: #3B82F6; color: white; padding: 12px;"

)

```



\## 16.3 Imagens



Não utilizar caminhos absolutos.



Incorreto:



```python
"C:/Users/engvi/Desktop/ORGANIZEG3/logo.png"
```



Correto:



```python

Assets.LOGO\_PRIMARY

```



\## 16.4 Alteração visual



Mudanças visuais devem ser feitas nos tokens, temas ou componentes oficiais.



Não corrigir aparência diretamente em uma tela isolada.



\---



\# 17. Código



\## 17.1 Idioma



\* Código: inglês.

\* Documentação: português.

\* Nomes oficiais do domínio podem ser explicados em português, mas representados em inglês no código.



\## 17.2 Nomenclatura



\* classes: `PascalCase`;

\* funções: `snake\_case`;

\* variáveis: `snake\_case`;

\* constantes: `UPPER\_CASE`;

\* módulos: `snake\_case`;

\* tabelas: `snake\_case`.



\## 17.3 Tipagem



Todo código novo deve utilizar type hints.



Evitar `Any`, salvo em limites dinâmicos bem definidos.



\## 17.4 Funções



Funções devem:



\* possuir uma responsabilidade;

\* ter nomes explícitos;

\* evitar efeitos colaterais ocultos;

\* validar suas pré-condições;

\* retornar tipos previsíveis.



\## 17.5 Comentários



Comentários devem explicar por que determinada decisão existe.



Não repetir em comentários aquilo que o código já demonstra.



\---



\# 18. Erros



Utilizar erros específicos.



Exemplos:



```text

DomainError

ValidationError

NotFoundError

ConflictError

PermissionDeniedError

InvalidTransitionError

ConcurrencyError

IdempotencyConflictError

```



Não utilizar `None` para representar falhas inesperadas.



Não retornar mensagens internas de banco para o cliente.



\---



\# 19. Logging



Logs devem ser estruturados.



Quando aplicável, incluir:



\* `correlation\_id`;

\* `tenant\_id`;

\* `user\_id`;

\* `device\_id`;

\* operação;

\* duração;

\* resultado.



Nunca registrar:



\* senha;

\* token;

\* chave secreta;

\* conteúdo sensível desnecessário;

\* arquivos completos;

\* credenciais externas.



\---



\# 20. Testes



Código novo deve possuir testes compatíveis com seu risco.



\## Domínio



Testar:



\* invariantes;

\* transições;

\* eventos;

\* objetos de valor;

\* erros.



\## Aplicação



Testar:



\* comandos;

\* queries;

\* autorização;

\* transações;

\* idempotência.



\## Infraestrutura



Testar:



\* repositórios;

\* banco;

\* Storage;

\* Outbox;

\* integrações.



\## Interface



Testar os principais fluxos de usuário.



Toda correção de bug deve incluir teste de regressão.



\---



\# 21. Alterações em arquivos existentes



Antes de alterar um arquivo:



1\. leia seu conteúdo;

2\. identifique sua responsabilidade;

3\. procure implementações semelhantes;

4\. avalie dependências;

5\. preserve contratos públicos;

6\. evite reescrever partes não relacionadas;

7\. atualize testes;

8\. atualize documentação quando necessário.



Não criar duplicações com nomes diferentes.



\---



\# 22. Dependências



Antes de adicionar uma biblioteca:



\* verificar se a funcionalidade já existe no projeto;

\* avaliar manutenção e segurança;

\* avaliar compatibilidade;

\* justificar sua necessidade;

\* registrar decisão relevante em ADR.



Não adicionar dependências apenas para reduzir poucas linhas de código.



\---



\# 23. Checklist obrigatório antes da conclusão



Antes de declarar uma tarefa concluída, verificar:



\* \[ ] A alteração respeita a arquitetura?

\* \[ ] O domínio permanece independente?

\* \[ ] A regra está na camada correta?

\* \[ ] O Tenant está protegido?

\* \[ ] As permissões foram consideradas?

\* \[ ] Eventos foram gerados quando necessários?

\* \[ ] Auditoria foi considerada?

\* \[ ] Idempotência foi considerada?

\* \[ ] Funcionamento offline foi considerado?

\* \[ ] Não há estilo visual hardcoded?

\* \[ ] Não há credenciais no código?

\* \[ ] Migrações foram criadas quando necessárias?

\* \[ ] Testes foram criados ou atualizados?

\* \[ ] A documentação continua coerente?

\* \[ ] O código é sustentável no longo prazo?



\---



\# 24. Regra final



O objetivo não é apenas fazer o código funcionar.



O objetivo é preservar uma plataforma:



\* clara;

\* modular;

\* configurável;

\* segura;

\* auditável;

\* testável;

\* reutilizável;

\* preparada para evoluir.



Quando houver conflito entre velocidade imediata e sustentabilidade arquitetural, escolher a solução sustentável, salvo decisão explícita e documentada em contrário.



