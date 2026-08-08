# ORGANIZEG3 — ORDEM OFICIAL DE IMPLEMENTAÇÃO

> Plano normativo de execução para transformar o código atual no OrganizeG3 definido pela Especificação Mestra e pelo Stack Tecnológico Oficial.

---

| Propriedade | Valor |
|---|---|
| Documento | `ORGANIZEG3_ORDEM_OFICIAL_DE_IMPLEMENTACAO.md` |
| Versão | `1.1.0` |
| Data | `2026-08-08` |
| Status | Aprovado para orientar a implementação |
| Público | Proprietário, desenvolvedores e agentes de IA |
| Aplicação de interface | React/PWA responsivo para desktop e mobile |
| Estratégia | Backend preservado; frontend unificado React/PWA por migração incremental |
| Stack vinculada | `ORGANIZEG3_STACK_TECNOLOGICO_OFICIAL.md` |
| Especificação vinculada | `ORGANIZEG3_ESPECIFICACAO_MESTRA_UNICA.md` |
| Código legado | Preservado e migrado por fatias verticais |


> Decisão vigente de UI/UX: `ADR-UI-001_FRONTEND_UNIFICADO_REACT_PWA.md`.
> PySide6/Qt Widgets deixa de ser a interface principal. A UI oficial passa a ser React + TypeScript + Vite + PWA, compartilhada entre desktop e mobile.

---

# 1. Finalidade

Este documento determina a ordem exata de implementação do OrganizeG3.

Ele responde:

- o que deve ser feito primeiro;
- o que depende de quê;
- quais arquivos deverão ser criados;
- quais arquivos legados deverão ser preservados;
- quando uma migration poderá ser criada;
- quando a API e o Supabase entrarão;
- qual módulo deverá ser migrado primeiro;
- quais testes são obrigatórios;
- quando o Claude deverá parar e pedir validação;
- quais critérios autorizam o avanço para a etapa seguinte.

Este plano não autoriza uma reescrita integral.

A estratégia oficial é:

```text
Estabilizar
    ↓
Caracterizar o comportamento atual
    ↓
Criar a fundação arquitetural
    ↓
Encapsular o legado
    ↓
Migrar um fluxo completo por vez
    ↓
Remover o legado somente quando não houver mais consumidores
```

---

# 2. Documentos obrigatórios para o Claude

Antes de qualquer alteração, o Claude deverá receber e ler:

```text
1. ORGANIZEG3_ESPECIFICACAO_MESTRA_UNICA.md
2. ORGANIZEG3_STACK_TECNOLOGICO_OFICIAL.md
3. ORGANIZEG3_ORDEM_OFICIAL_DE_IMPLEMENTACAO.md
4. DOC-125 — Development Standards
5. DOC-126 — Testing Strategy
6. DOC-121 — UIUX Design System
7. ADENDO_DESIGN_SYSTEM_v2_3.md
8. DOMAIN_COMMANDS_CATALOG.md
9. Código atual completo
10. Banco de dados de teste anonimizado
```

Quando houver divergência:

```text
ADR aprovado
    > Stack Tecnológico Oficial
    > Ordem Oficial de Implementação
    > Especificação Mestra
    > Documentos auxiliares
    > Código legado
```

---

# 3. Diagnóstico do ponto de partida conhecido

Os arquivos históricos indicam a existência de uma aplicação PySide6 com SQLAlchemy e SQLite. A partir de 2026-08-08, essa UI é legado de transição; novas interfaces serão implementadas no frontend React/PWA.

Foram identificados, no snapshot analisado:

## 3.1 Banco atual

O arquivo indicado como `app/database/database.py` contém:

- `Base` global;
- `SessionLocal` global;
- `engine` global;
- migrações manuais por `ALTER TABLE`;
- `NullPool`;
- `check_same_thread=False`;
- fallback silencioso para SQLite em memória;
- inicialização do banco durante o import do módulo;
- dependência de `app.core.get_db_path()`.

## 3.2 Modelos atuais

O snapshot `models(2).py`, que deverá ter seu caminho real confirmado no workspace, concentra dezenas de classes SQLAlchemy em um único arquivo.

Foram observados:

- chaves primárias inteiras;
- campos financeiros com `Float`;
- `datetime.now()` sem timezone;
- entidades de diferentes módulos no mesmo arquivo;
- status como strings livres;
- relacionamento direto entre diversos contextos;
- ausência generalizada de `tenant_id`;
- ausência de migrations Alembic como autoridade única;
- modelos ORM utilizados como modelo central da aplicação.

## 3.3 Documentação técnica já existente

Já existem documentos de:

- domínio;
- aggregates;
- entities;
- value objects;
- commands;
- queries;
- repositories;
- Unit of Work;
- infraestrutura;
- database;
- Outbox;
- Event Bus;
- synchronization;
- audit;
- backup;
- API;
- testes;
- roadmap.

Esses documentos deverão orientar a implementação, mas não significam que todo o código correspondente já exista.

## 3.4 Refatoração visual em andamento

A refatoração visual já possui trabalho concluído em:

- `theme_manager.py`;
- `icon_manager.py`;
- `components.py`;
- vários dialogs.

Esse trabalho não deverá ser descartado.

A migração arquitetural deverá preservar:

- Design System existente;
- caminhos reais dos componentes;
- tooltips;
- estilos claros e escuros;
- correções visuais já aplicadas;
- comportamento das telas existentes.

---

# 4. Regras de execução

## 4.1 Regra de lote

Cada entrega do Claude deverá modificar um lote pequeno e coerente.

Limite recomendado:

```text
1 migration por entrega
ou
1 fatia vertical pequena
ou
3 a 8 arquivos fortemente relacionados
```

Exceções somente quando um arquivo completo exigir auxiliares inseparáveis.

## 4.2 Regra de parada

O Claude deverá parar ao final de cada lote e apresentar:

```text
Arquivos criados
Arquivos alterados
Migration criada
Testes executados
Resultado dos testes
Como validar manualmente
Riscos conhecidos
Próximo lote recomendado
```

Ele não deverá avançar automaticamente para a fase seguinte.

## 4.3 Regra de preservação

Antes de apagar, mover ou substituir um símbolo, o Claude deverá localizar:

- imports;
- chamadas;
- subclasses;
- sinais;
- slots;
- referências em templates;
- referências em testes;
- referências em migrations;
- referências no empacotamento.

## 4.4 Regra de compatibilidade

Durante a migração, adaptadores de compatibilidade são permitidos.

Exemplo:

```text
import legado
    ↓
facade compatível
    ↓
nova implementação
```

A facade somente será removida quando não houver consumidores.

## 4.5 Regra de banco

Nenhuma alteração estrutural poderá ser executada por código comum da aplicação após a implantação do Alembic.

## 4.6 Regra de validação

Uma fase somente estará concluída quando:

```text
Aplicação abre
Login funciona quando aplicável
Banco atual abre
Migration funciona em banco novo
Migration funciona em cópia do banco legado
Testes passam
Ruff passa
mypy não piora a baseline
Fluxo manual crítico funciona
Backup e restauração continuam válidos
```

---

# 5. Visão geral da ordem

| Ordem | Fase | Resultado principal |
|---:|---|---|
| 00 | Congelamento e segurança | Ponto de retorno confiável |
| 01 | Diagnóstico executável | Inventário real do workspace |
| 02 | Estabilização crítica | Aplicação fecha, salva e recupera corretamente |
| 03 | Ferramentas e qualidade | `uv`, `pyproject`, Ruff, mypy e pytest |
| 04 | Estrutura arquitetural | Pacote `src/organizeg3` e Composition Root |
| 05 | Persistência e Alembic | Migrations oficiais sem perda de dados |
| 06 | Core transversal | Settings, errors, logging, UoW e task runner |
| 07 | Tenant, empresa e filial | Escopo organizacional consistente |
| 08 | Identidade, permissões e auditoria | Segurança local preparada para nuvem |
| 09 | Frontend Foundation, App Shell e Design System | React/PWA responsivo e componentes compartilhados |
| 10 | Primeira fatia vertical — Clientes | Modelo de implementação validado |
| 11 | Fornecedores e catálogo | Base de suprimentos |
| 12 | CRM e Comercial | Leads, oportunidades e pedidos |
| 13 | Projetos | Definição técnica central |
| 14 | Orçamentos | Precificação e aprovação |
| 15 | Compras | Solicitações, cotações e ordens |
| 16 | Estoque | Movimentações, reservas e inventário |
| 17 | PCP | Planejamento e capacidade |
| 18 | Produção | Execução e apontamentos |
| 19 | Qualidade | Inspeções e não conformidades |
| 20 | Expedição | Volumes, cargas e entregas |
| 21 | Instalação | Execução em campo e aceite |
| 22 | Assistência Técnica | Pós-venda e garantia |
| 23 | Financeiro | Recebimentos, pagamentos e fluxo |
| 24 | Recursos Humanos | Pessoas, ponto e SST |
| 25 | Fiscal | Documentos e regras fiscais |
| 26 | Documentos, busca e relatórios | Serviços compartilhados |
| 27 | Workflow, agenda e notificações | Orquestração transversal |
| 28 | API e Supabase | Operação compartilhada |
| 29 | Sincronização offline-first | SQLite ↔ API ↔ PostgreSQL |
| 30 | BI | Indicadores e dashboards |
| 31 | Inteligência Artificial | Assistência controlada |
| 32 | PWA, offline e dispositivos | Instalação, cache, IndexedDB e adaptações mobile |
| 33 | Build e release | Build web/PWA e implantação confiável |
| 34 | Hardening e produção | Segurança, performance e recuperação |

---

# 6. FASE 00 — Congelamento e segurança

## Objetivo

Criar um ponto de retorno antes de qualquer mudança arquitetural.

## Ordem

### 00.01 — Congelar mudanças paralelas

Não executar simultaneamente:

- migração de arquitetura;
- alteração de banco;
- grande refatoração visual;
- mudança de empacotamento;
- troca de autenticação.

Correções críticas poderão entrar em branch separada.

### 00.02 — Criar repositório limpo

Executar:

```bash
git status
git add .
git commit -m "chore: snapshot anterior à migração arquitetural"
git tag pre-architecture-migration
```

### 00.03 — Gerar backup

Criar:

```text
backup do código
backup do banco SQLite
backup dos documentos de usuário
backup das configurações
backup dos assets
```

Calcular SHA-256 do banco e registrar.

### 00.04 — Criar banco de teste anonimizado

Nunca utilizar o banco real do usuário em testes automatizados.

O banco de teste deverá preservar:

- schema;
- relacionamentos;
- casos importantes;
- dados fictícios;
- volumes representativos.

### 00.05 — Registrar versões atuais

Criar:

```text
docs/baseline/CURRENT_RUNTIME_BASELINE.md
```

Conteúdo:

```text
Python
React + TypeScript
SQLAlchemy
Windows
Caminho do banco
Tamanho do banco
Quantidade de tabelas
Quantidade de registros por tabela
Comando de inicialização
Comando de build
Problemas conhecidos
```

## Critério de saída

- commit criado;
- tag criada;
- backup restaurado com sucesso;
- hash validado;
- banco de teste disponível.

## Instrução ao Claude

```text
Não altere o código nesta etapa. Apenas produza o inventário, os comandos e a documentação da baseline. Não crie arquitetura nova ainda.
```

---

# 7. FASE 01 — Diagnóstico executável

## Objetivo

Descobrir o estado real do workspace antes de seguir os nomes previstos nos documentos.

## Entregas

```text
docs/diagnostics/WORKSPACE_INVENTORY.md
docs/diagnostics/IMPORT_GRAPH_SUMMARY.md
docs/diagnostics/DATABASE_SCHEMA_CURRENT.md
docs/diagnostics/UI_PAGE_MAP.md
docs/diagnostics/LEGACY_RISK_REGISTER.md
docs/diagnostics/MIGRATION_CANDIDATES.md
```

## Ordem de análise

### 01.01 — Entry points

Localizar:

```text
main.py
__main__.py
QApplication
MainWindow
login
onboarding
logout
troca de usuário
encerramento
```

### 01.02 — Banco

Localizar:

```text
get_db_path
create_engine
Base
SessionLocal
create_all
migrações manuais
backup
restore
pragmas
conexões sqlite3 diretas
```

### 01.03 — Modelos

Listar:

- todas as classes ORM;
- tabelas;
- relações;
- campos `Float`;
- datas ingênuas;
- campos de status;
- chaves únicas;
- índices;
- cascades;
- dependências circulares.

### 01.04 — UI

Listar:

- páginas;
- dialogs;
- componentes;
- tabelas;
- formulários;
- acesso direto ao banco;
- criação direta de sessões;
- regras de negócio em widgets;
- QSS hardcoded;
- tarefas bloqueantes.

### 01.05 — Build

Localizar:

```text
.spec
Build Vite/PWA
assets
icons
templates
migrations
paths especiais de sys._MEIPASS
installer
```

### 01.06 — Testes

Executar ou registrar ausência de:

```text
pytest
testes manuais
scripts de diagnóstico
teste de banco
teste de backup
teste de encerramento
```

## Proibição

Nesta fase, o Claude não deverá “corrigir enquanto analisa”.

## Critério de saída

O inventário deverá responder exatamente:

1. Qual arquivo inicia o sistema?
2. Qual arquivo cria o `QApplication`?
3. Qual é o caminho real de `models(2).py`?
4. Quantas sessões são abertas diretamente nas telas?
5. Quais tabelas existem no banco real?
6. Qual é a versão atual do schema?
7. Como o backup é executado?
8. Como o programa encerra?
9. Qual é o processo de build?
10. Quais fluxos críticos não possuem teste?

---

# 8. FASE 02 — Estabilização crítica do legado

## Objetivo

Remover riscos que podem corromper dados ou impedir a migração.

## Ordem obrigatória

### 02.01 — Ciclo de vida da aplicação

Corrigir e testar:

```text
Fechar pelo X
Fechar pelo botão do sistema
Logout
Trocar usuário
Backup antes do fechamento
Cancelamento de fechamento
Threads em execução
QApplication.quit()
sys.exit(app.exec())
```

A solução deverá possuir um coordenador único de encerramento.

Arquivo-alvo a criar ou consolidar:

```text
app/services/application_lifecycle_service.py
```

Não colocar encerramento distribuído em várias páginas.

### 02.02 — Threads e workers

Mapear threads vivas no fechamento.

Criar protocolo:

```text
request_stop
wait
timeout
log
force only as last resort
```

Nenhum worker deverá ficar sem referência ou sem sinal de encerramento.

### 02.03 — Backup

Separar:

```text
BackupService
RestoreService
BackupValidator
```

O backup deverá:

- fechar ou coordenar transações;
- utilizar cópia consistente;
- gerar hash;
- gerar manifesto;
- validar arquivo;
- informar sucesso real;
- nunca marcar sucesso apenas porque o arquivo foi criado.

### 02.04 — Fallback de banco em memória

O fallback silencioso de `database.py` para `sqlite:///:memory:` deverá ser removido somente depois de existir uma tela de erro de inicialização e recuperação.

Comportamento correto:

```text
falha ao abrir banco
    ↓
registrar erro
    ↓
mostrar modo de recuperação
    ↓
oferecer abrir backup ou selecionar banco
    ↓
não iniciar operação em banco vazio fingindo sucesso
```

### 02.05 — Logging mínimo

Antes de grandes mudanças, criar logs para:

- startup;
- shutdown;
- banco;
- backup;
- migrations;
- login;
- erro não tratado;
- worker.

## Testes obrigatórios

```text
test_application_close_by_window
test_application_close_after_backup
test_logout_does_not_leave_process
test_worker_stops_on_shutdown
test_backup_can_be_restored
test_database_failure_does_not_open_memory_database
```

## Critério de saída

O programa deverá fechar sem processo residual em cinco execuções consecutivas.

---

# 9. FASE 03 — Ferramentas e qualidade

## Objetivo

Adotar a stack de desenvolvimento sem mover todo o código.

## Arquivos

```text
pyproject.toml
uv.lock
.python-version
.env.example
.gitignore
README.md
ruff.toml ou configuração no pyproject
mypy.ini ou configuração no pyproject
pytest.ini ou configuração no pyproject
```

## Ordem

### 03.01 — Importar dependências atuais

O Claude deverá detectar todas as dependências usadas pelo código.

Não remover dependências ainda.

### 03.02 — Criar `pyproject.toml`

Incluir:

- metadados;
- Python `>=3.13,<3.14`;
- dependências de runtime;
- grupos `dev`, `api` e `jobs`;
- comandos documentados.

### 03.03 — Criar `uv.lock`

Executar:

```bash
uv lock
uv sync
```

### 03.04 — Ruff

Primeiro rodar sem formatar o projeto inteiro.

Criar baseline de erros.

Corrigir apenas:

- imports quebrados;
- erros de sintaxe;
- nomes indefinidos;
- problemas críticos.

A formatação geral deverá ocorrer por lotes.

### 03.05 — mypy

Ativar primeiro em:

```text
novo core
novo domain
nova application layer
```

O legado poderá ficar temporariamente fora do modo estrito.

### 03.06 — pytest

Configurar markers e diretórios.

## Critério de saída

```bash
uv sync --locked
uv run python <entrypoint atual>
uv run pytest
uv run ruff check <novos arquivos>
```

deverão funcionar.

---

# 10. FASE 04 — Estrutura arquitetural e ponte com o legado

## Objetivo

Criar a nova arquitetura sem mover todas as funcionalidades de uma vez.

## Estrutura inicial

```text
src/organizeg3/
├── __init__.py
├── __main__.py
├── bootstrap/
│   ├── application.py
│   ├── composition_root.py
│   └── settings.py
├── core/
│   ├── errors/
│   ├── logging/
│   ├── database/
│   ├── events/
│   ├── permissions/
│   ├── audit/
│   ├── tasks/
│   └── theme_design/
├── modules/
└── legacy/
```

## Estratégia de ponte

A aplicação atual continuará funcionando.

O novo entrypoint poderá inicialmente chamar o entrypoint legado por adapter.

Exemplo conceitual:

```text
python -m organizeg3
    ↓
bootstrap
    ↓
LegacyApplicationAdapter
    ↓
janela atual
```

Isso permite introduzir:

- settings;
- logging;
- lifecycle;
- composition root;

antes de migrar todas as páginas.

## Proibições

Não:

- mover todos os arquivos em uma única entrega;
- alterar todos os imports;
- duplicar `QApplication`;
- manter dois `ThemeManager` concorrentes;
- manter dois engines apontando ao mesmo banco sem coordenação.

## Critério de saída

O novo comando deverá iniciar a aplicação atual:

```bash
uv run python -m organizeg3
```

---

# 11. FASE 05 — Persistência e Alembic

## Objetivo

Transformar Alembic na autoridade única do schema sem perder bancos existentes.

## 11.1 Inventário e comparação

Gerar:

```text
schema SQL do banco legado
metadata SQLAlchemy atual
diferenças
tabelas órfãs
colunas ausentes
índices ausentes
constraints ausentes
```

## 11.2 Baseline Alembic

Criar:

```text
migrations/versions/0001_legacy_baseline.py
```

A baseline deverá representar o schema atual completo.

### Banco novo

```bash
alembic upgrade head
```

deverá criar o mesmo schema esperado pelo legado.

### Banco existente

O processo será:

```text
backup
    ↓
inspeção de schema
    ↓
validação contra baseline
    ↓
correções controladas quando necessárias
    ↓
alembic stamp 0001_legacy_baseline
```

Nunca executar `stamp` sem verificar o schema.

## 11.3 Retirar migrações manuais

A função `verificar_e_atualizar_banco()` deverá permanecer temporariamente desativável por feature flag.

Depois que os bancos suportados estiverem na baseline:

- converter alterações em revisions Alembic;
- remover os `ALTER TABLE` manuais;
- manter uma verificação de versão, não uma migration improvisada.

## 11.4 Sessão e engine

Criar:

```text
src/organizeg3/core/database/base.py
src/organizeg3/core/database/engine.py
src/organizeg3/core/database/session.py
src/organizeg3/core/database/unit_of_work.py
src/organizeg3/core/database/types.py
```

A sessão será criada sob demanda.

Não criar conexão no import.

## 11.5 Pragmas SQLite

Aplicar por event listener:

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
```

## 11.6 IDs

Não substituir todas as PKs inteiras imediatamente.

Estratégia:

```text
manter id legado
adicionar public_id UUID por módulo
preencher UUID para registros existentes
criar unique index
usar public_id em novos contratos
migrar FKs somente quando justificado
```

## 11.7 Dinheiro

Não converter todos os `Float` em uma única migration.

Ordem por módulo:

```text
introduzir Money/Decimal na Application Layer
validar valores atuais
criar coluna NUMERIC ou inteira escalada
copiar e comparar
mudar leitura
mudar escrita
remover coluna antiga em migration posterior
```

## 11.8 Datas

Novos campos de instante utilizarão UTC.

Campos antigos serão convertidos por módulo após definição da interpretação histórica.

## Testes

```text
test_new_database_upgrade_to_head
test_legacy_database_can_be_stamped_after_validation
test_sqlite_pragmas
test_session_closed_after_use
test_migration_upgrade_and_downgrade
test_no_schema_change_during_normal_startup
```

---

# 12. FASE 06 — Core transversal

## Objetivo

Criar serviços que todos os módulos utilizarão.

## Ordem de arquivos

### 06.01 — Settings

```text
core/settings/models.py
core/settings/loader.py
core/settings/paths.py
```

### 06.02 — Errors

```text
core/errors/base.py
core/errors/domain.py
core/errors/application.py
core/errors/infrastructure.py
core/errors/presenter.py
```

### 06.03 — Logging

```text
core/logging/configuration.py
core/logging/context.py
core/logging/handlers.py
```

### 06.04 — Clock e IDs

```text
core/time/clock.py
core/ids/id_generator.py
```

Testes deverão permitir clock e IDs determinísticos.

### 06.05 — Unit of Work

```text
core/database/unit_of_work.py
```

### 06.06 — Event Bus

```text
core/events/event.py
core/events/bus.py
core/events/registry.py
```

### 06.07 — Outbox

```text
core/events/outbox_model.py
core/events/outbox_repository.py
core/events/outbox_dispatcher.py
```

### 06.08 — Task Runner

```text
core/tasks/task_runner.py
core/tasks/qt_worker.py
core/tasks/cancellation.py
```

### 06.09 — Feature flags

```text
core/features/flags.py
```

Usos:

- migration manual legada;
- nova página de clientes;
- nova autenticação;
- sincronização;
- API;
- novo financeiro.

## Critério de saída

Os serviços deverão possuir testes unitários e não depender de páginas concretas.

---

# 13. FASE 07 — Tenant, empresa e filial

## Objetivo

Criar o escopo organizacional antes de novos módulos.

## Entidades

```text
Tenant
Company
Branch
CompanySettings
```

## Decisão para instalação atual

A instalação local existente receberá:

```text
Tenant padrão
Empresa padrão
Filial padrão
```

Esses registros serão criados por migration ou bootstrap idempotente.

## Migration

Adicionar progressivamente:

```text
tenant_id
company_id
branch_id quando aplicável
public_id
created_at
updated_at
```

Não adicionar tudo a todas as tabelas em uma única revision.

Começar por:

```text
usuarios
clientes
fornecedores
materiais
orcamentos
```

## Regras

- toda consulta nova deverá receber escopo;
- toda criação deverá definir Tenant;
- nenhum filtro de Tenant virá da UI sem validação;
- a sessão do usuário resolverá o Tenant ativo.

---

# 14. FASE 08 — Identidade, permissões e auditoria

## Objetivo

Encapsular o login atual e preparar Supabase Auth.

## Ordem

### 08.01 — Identity Provider

```text
core/auth/identity_provider.py
core/auth/local_identity_provider.py
core/auth/session.py
```

O login legado será encapsulado por `LocalIdentityProvider`.

### 08.02 — Password hashing

Confirmar algoritmo atual.

Se inadequado, migrar no próximo login sem invalidar todos os usuários.

Biblioteca somente após avaliação e inclusão aprovada.

### 08.03 — Permission Service

```text
core/permissions/permission.py
core/permissions/service.py
core/permissions/guard.py
```

Permissões deverão seguir códigos da Especificação Mestra.

### 08.04 — Auditoria

```text
core/audit/audit_entry.py
core/audit/service.py
core/audit/repository.py
```

Novos casos de uso deverão registrar auditoria automaticamente.

### 08.05 — UI guards

Botões poderão ser ocultados ou desabilitados, mas o caso de uso deverá verificar novamente.

## Testes

```text
usuário sem permissão não executa comando
usuário de outro Tenant não acessa registro
evento sensível é auditado
senha não aparece no log
```

---

# 15. FASE 09 — Frontend Foundation, App Shell e Design System

## Objetivo

Criar a fundação visual oficial em React antes da implementação das páginas funcionais.

## Ordem

```text
apps/web
TypeScript
Vite
React
React Router
TanStack Query
Zustand
Zod
PWA Plugin / Workbox
theme_design
AppShell
ResponsiveLayout
Sidebar / Drawer
TopBar
RouteGuard
PermissionGuard
ErrorBoundary
PageHeader
FilterBar
DataTable
ResponsiveList
StatusBadge
EmptyState
LoadingState
ErrorState
Pagination
Dialog / Sheet
Toast / NotificationPresenter
```

## Regras

- desktop, notebook, tablet e celular usam a mesma base React;
- nenhuma página acessa SQLAlchemy ou banco diretamente;
- nenhuma regra de negócio reside em componentes;
- todo valor visual vem de `theme_design`;
- TanStack Table é a base de tabelas;
- tabelas precisam declarar comportamento por breakpoint;
- Lucide React é a iconografia oficial;
- TanStack Query controla estado de servidor;
- Zustand é reservado a estado local de interface;
- nenhum componente de feature pode criar uma linguagem visual própria;
- PySide6 legado não recebe novas telas, salvo correção necessária durante a transição.

## Critério de saída

- build React abre sem erros;
- PWA manifest válido;
- tema claro e escuro;
- navegação responsiva;
- login shell;
- layout desktop;
- layout tablet;
- layout mobile;
- pelo menos uma tabela responsiva;
- estados vazio, loading e erro;
- testes unitários de componentes;
- teste E2E do shell;
- zero valor visual hardcoded nas páginas de referência.
# 16. FASE 10 — Primeira fatia vertical: Clientes

## Objetivo

Criar o padrão oficial que será copiado pelos demais módulos.

## Por que Clientes primeiro

Clientes:

- já existem no banco;
- possuem dependências relativamente simples;
- são necessários por CRM, projetos, orçamentos, financeiro e assistência;
- permitem testar lista, cadastro, validação, pesquisa e auditoria;
- possuem valor imediato.

## Ordem exata de arquivos

```text
modules/customers/
├── domain/
│   ├── entities/customer.py
│   ├── value_objects/customer_document.py
│   ├── value_objects/contact.py
│   ├── value_objects/address.py
│   ├── events/customer_created.py
│   ├── events/customer_updated.py
│   └── repositories/customer_repository.py
├── application/
│   ├── commands/create_customer.py
│   ├── commands/update_customer.py
│   ├── commands/archive_customer.py
│   ├── handlers/create_customer_handler.py
│   ├── handlers/update_customer_handler.py
│   ├── handlers/archive_customer_handler.py
│   ├── queries/get_customer.py
│   ├── queries/list_customers.py
│   ├── handlers/get_customer_handler.py
│   ├── handlers/list_customers_handler.py
│   ├── dto/customer_dto.py
│   └── validators/customer_validator.py
├── infrastructure/
│   ├── orm/customer_model.py
│   ├── mappers/customer_mapper.py
│   └── repositories/sqlalchemy_customer_repository.py
└── presentation/
    ├── viewmodels/customer_list_viewmodel.py
    ├── viewmodels/customer_form_viewmodel.py
    ├── pages/customer_list_page.py
    └── dialogs/customer_form_dialog.py
```

## Compatibilidade com `clientes`

A primeira implementação deverá reutilizar a tabela existente.

Não renomear colunas ainda sem necessidade.

Adicionar somente:

```text
public_id
tenant_id
company_id
updated_at
deleted_at
version
```

em migrations pequenas e testadas.

## Casos de uso

```text
Criar cliente
Editar cliente
Consultar cliente
Listar clientes
Pesquisar
Filtrar ativos
Arquivar
Reativar
```

## Validações

```text
nome obrigatório
tipo de pessoa válido
CPF/CNPJ normalizado quando informado
email válido quando informado
estado normalizado
duplicidade configurável
Tenant obrigatório
```

## UI

A nova tela deverá:

- reutilizar `ThemeManager`;
- usar tabela model/view;
- não abrir sessão diretamente;
- exibir loading;
- exibir erro;
- preservar o dialog atual por feature flag;
- permitir rollback para página legada.

## Testes

```text
test_create_customer
test_update_customer
test_archive_customer
test_customer_document_normalization
test_duplicate_customer_policy
test_customer_repository_sqlite
test_customer_tenant_isolation
test_customer_permissions
test_customer_audit
test_customer_list_viewmodel
test_customer_form_validation
```

## Gate de saída

A feature flag será ativada apenas após comparação com o fluxo legado.

Depois de uma versão estável, a página legada poderá ser removida em entrega separada.

---

# 17. Modelo obrigatório para cada módulo seguinte

Cada módulo deverá repetir esta ordem:

```text
1. Especificação funcional da fatia
2. Estado e transições
3. Entidades e value objects
4. Contratos de repository
5. Commands e queries
6. Handlers
7. DTOs e validators
8. ORM models
9. Mappers
10. Repository SQLAlchemy
11. Migration
12. Permission codes
13. Audit events
14. Domain/Application events
15. ViewModels
16. Pages e dialogs
17. Navegação
18. Testes unitários
19. Testes de integração
20. Testes de UI
21. Migração de dados legados
22. Feature flag
23. Comparação com legado
24. Ativação
25. Remoção posterior do legado
```

Nenhum módulo deverá começar pela tela.

---

# 18. FASE 11 — Fornecedores e catálogo

## Ordem interna

```text
1. Suppliers
2. Brands
3. Units
4. Material Categories
5. Materials
6. Material Prices
7. Supplier Price History
```

## Dependências

```text
Tenant
Company
Permissions
Audit
Customers pattern
```

## Cuidados

- dados bancários com permissão própria;
- preço com Decimal;
- NCM/CFOP mantidos como dados fiscais, sem lógica fiscal completa ainda;
- histórico de preço append-only;
- material inativo não poderá ser usado em novas operações.

---

# 19. FASE 12 — CRM e Comercial

## Ordem interna

```text
1. Leads
2. Contacts
3. Opportunities
4. Activities
5. Sales Pipeline
6. Proposals
7. Approvals
8. Commercial Orders
```

## Regras

- Cliente e Lead serão conceitos distintos;
- conversão de Lead deverá ser idempotente;
- pipeline deverá possuir máquina de estados;
- perda deverá exigir motivo;
- aprovação comercial deverá registrar usuário e data;
- não implementar faturamento nesta fase.

---

# 20. FASE 13 — Projetos

## Ordem interna

```text
1. Project
2. Project Environment
3. Furniture
4. Technical Revision
5. Measurement
6. Technical Checklist
7. Attachments
8. Project Approval
9. Project Timeline
```

## Regra central

Projetos será a fonte oficial da definição técnica.

Não criar módulo separado de Engenharia.

## Cuidados

- revisões imutáveis após aprovação;
- alterações geram nova revisão;
- anexos via DocumentService;
- ambientes e móveis possuem UUID;
- nenhum módulo poderá alterar projeto silenciosamente.

---

# 21. FASE 14 — Orçamentos

## Ordem interna

```text
1. Budget
2. Budget Items
3. Commercial Items
4. Cost Calculation
5. Pricing Policy
6. Taxes Estimate
7. Payment Plan
8. Revision
9. Approval
10. Document Generation
```

## Migração de dinheiro

Orçamentos será o primeiro módulo complexo a concluir a migração dos `Float` financeiros.

O Claude deverá produzir relatório de comparação antes de trocar colunas.

## Gate

```text
100 orçamentos de amostra
total antigo x novo
diferença aceitável definida
documento PDF comparado
```

---

# 22. FASE 15 — Compras

## Ordem interna

```text
Purchase Request
Quotation
Supplier Proposal
Quotation Comparison
Approval
Purchase Order
Purchase Order Item
Follow-up
Receipt Expectation
```

## Regras

- Ordem de Compra não movimenta estoque;
- recebimento é processo separado;
- aprovações usam Permission Service;
- histórico de preço recebe evento;
- compras emergenciais exigem justificativa.

---

# 23. FASE 16 — Estoque

## Ordem interna

```text
Warehouse
Location
Stock Item
Stock Balance
Stock Movement
Reservation
Receipt
Issue
Transfer
Inventory Count
Adjustment
Loss
Remnant
Lot when applicable
```

## Regra contábil operacional

Saldo não será campo livre editável.

Saldo será consequência de movimentos.

Se um saldo materializado existir, deverá ser atualizado transacionalmente e reconciliável.

## Testes críticos

```text
não permitir saldo negativo conforme política
reserva idempotente
dupla baixa não ocorre
transferência é atômica
inventário gera ajuste auditado
```

---

# 24. FASE 17 — PCP

## Ordem interna

```text
Production Demand
Production Order
Routing
Operation
Work Center
Capacity
Calendar
Planning
Scheduling
Material Requirement
Release
Reschedule
Block
```

## Regras

- PCP planeja;
- Produção executa;
- Estoque reserva;
- Projetos define;
- Qualidade inspeciona.

Não misturar responsabilidades.

---

# 25. FASE 18 — Produção

## Ordem interna

```text
Execution
Operation Start
Pause
Resume
Completion
Production Time Entry
Material Consumption
Machine Use
Occurrence
Rework
Scrap
Production Checklist
Shift Board
```

## Interface

Operações de chão de fábrica deverão priorizar:

- botões grandes;
- poucos campos;
- leitura rápida;
- uso em touch quando aplicável;
- funcionamento offline;
- idempotência.

---

# 26. FASE 19 — Qualidade

## Ordem interna

```text
Quality Plan
Inspection
Inspection Item
Evidence
Nonconformity
Disposition
Corrective Action
Reinspection
Release
Quality History
```

## Regra

Qualidade libera; Produção não autoaprova sua própria conclusão quando a inspeção for obrigatória.

---

# 27. FASE 20 — Expedição

## Ordem interna

```text
Released Product
Package
Volume
Label
Staging
Picking
Checking
Shipment Order
Load
Manifest
Vehicle
Route
Delivery
Occurrence
Proof
Release to Installation
```

## Cuidados

- múltiplas viagens;
- entrega parcial;
- sequência de descarga;
- fragilidade;
- itens terceirizados;
- kits de ferragens;
- comprovante e assinatura.

---

# 28. FASE 21 — Instalação

## Ordem interna

```text
Installation Plan
Site Inspection
Schedule
Team
Tools
Materials
Check-in
Furniture Execution
Adjustment
Occurrence
Pending Issue
Final Inspection
Acceptance
Check-out
```

## Offline

A instalação deverá ser uma das primeiras áreas de campo testadas com fila local.

A sincronização completa somente entra na Fase 29, mas os comandos deverão nascer idempotentes.

---

# 29. FASE 22 — Assistência Técnica

## Ordem interna

```text
Support Request
Ticket
Triage
Warranty Check
Diagnosis
Remote Service
Visit
Work Order
Replacement Part
Responsibility
Cost
SLA
Acceptance
Satisfaction
Closure
```

## Regra

Não alterar projeto original.

Correções técnicas devem gerar nova revisão ou solicitação formal.

---

# 30. FASE 23 — Financeiro

## Ordem interna

```text
Chart of Accounts
Financial Category
Cost Center
Bank Account
Receivable
Receipt
Payable
Payment
Cash
Bank Movement
Reconciliation
Cash Flow
Commission
Advance
Reimbursement
Loan
Budget
DRE
Closing
```

## Estratégia

Financeiro será implementado após os módulos que geram fatos financeiros.

Primeiro migrar:

```text
Contas a Receber
Recebimentos
Contas a Pagar
Pagamentos
Contas Bancárias
```

## Segurança

Separar permissões de:

```text
visualizar valores
criar
editar
aprovar
pagar
receber
conciliar
fechar
reabrir
exportar
```

## Dinheiro

Todos os fluxos novos deverão usar Decimal/Money.

---

# 31. FASE 24 — Recursos Humanos

## Ordem interna

```text
Employee
Employment Contract
Department
Position
Team
Schedule
Time Entry
Overtime
Vacation
Leave
Benefit
Training
Occupational Health
PPE
Performance
Disciplinary Action
Offboarding
```

## Segurança

Dados pessoais, bancários, médicos e salariais terão permissões independentes.

Não usar BI para contornar essa proteção.

---

# 32. FASE 25 — Fiscal

## Pré-condição

A implementação fiscal somente começará depois de:

- cadastro estável;
- comercial estável;
- compras estáveis;
- estoque estável;
- financeiro estável;
- revisão com profissional fiscal.

## Ordem interna

```text
Tax Profile
Operation Nature
Tax Rule
Fiscal Classification
Outgoing Document
Incoming Document
XML
Transmission Adapter
Events
Returns
Remittances
Withholdings
Assessment
Closing
Accounting Export
```

## Regra

Integrações fiscais reais ficarão atrás de adapters.

O ambiente de homologação será obrigatório antes de produção.

---

# 33. FASE 26 — Documentos, busca e relatórios

## Ordem

```text
Document Metadata
Local Storage Adapter
Supabase Storage Adapter
Template Engine
PDF Service
DOCX Service
Spreadsheet Export
Search Index
Viewer
Reporting Engine
Scheduled Export Contract
```

## Estratégia

O serviço local deverá funcionar antes do Storage remoto.

---

# 34. FASE 27 — Workflow, agenda e notificações

## Ordem

```text
Task
Notification
Calendar
Schedule
Workflow Definition
Workflow Instance
Step
Approval
Rule
Automation
Webhook Contract
```

## Introdução gradual

Primeiro migrar aprovações já existentes para o motor.

Não construir editor BPMN completo na primeira entrega.

---

# 35. FASE 28 — API e Supabase

## Pré-condições

```text
casos de uso desacoplados da UI
repositories por contrato
Tenant implementado
permissões implementadas
auditoria implementada
migrations PostgreSQL testadas
```

## Ordem

```text
FastAPI bootstrap
settings de servidor
health check
JWT validation
Tenant resolution
exception mapping
OpenAPI
customers endpoints
suppliers endpoints
projects endpoints
commands explícitos
Supabase Auth adapter
Supabase Storage adapter
RLS
staging
```

## Primeira API vertical

Clientes deverá ser o primeiro módulo exposto.

A API deverá executar os mesmos handlers/casos de uso utilizados pelo frontend React/PWA.

Não duplicar regra de negócio.

---

# 36. FASE 29 — Sincronização offline-first

## Ordem

```text
Device Registration
Sync Cursor
Local Outbox
Server Inbox
Idempotency
Push
Pull
Version Check
Conflict Detection
Conflict Resolution
Tombstone
Attachment Queue
Retry
Monitoring
```

## Piloto

Executar primeiro com Clientes.

Depois:

```text
Fornecedores
Projetos
Orçamentos
Agenda
Instalação
Assistência
```

Financeiro e Fiscal somente após o motor demonstrar confiabilidade.

## Testes

```text
offline create
offline update
duplicate push
out-of-order messages
network timeout
process interruption
conflict
delete
attachment retry
two devices
```

---

# 37. FASE 30 — BI

## Pré-condições

- dados estáveis;
- permissions field-level;
- consultas de leitura;
- timestamps confiáveis;
- Tenant;
- eventos e audit.

## Ordem

```text
Indicator Catalog
Read Models
Simple Metric
Period Filter
Targets
Alerts
Dashboard
Exports
Refresh Jobs
Data Quality
Lineage
```

Primeiro indicador:

```text
Quantidade de Clientes Ativos
```

Não começar pelo dashboard executivo completo.

---

# 38. FASE 31 — Inteligência Artificial

## Ordem

```text
AIProvider
Prompt Registry
Prompt Versioning
Permission Check
Redaction
AI Request
AI Response
Approval
Audit
First Read-only Use Case
```

## Primeiro caso

```text
Resumir histórico de cliente autorizado
```

ou:

```text
Sugerir perguntas de triagem para chamado
```

Não iniciar com ações automáticas.

---

# 39. FASE 32 — PWA, offline e adaptações de dispositivo

A PWA já é o cliente oficial desde a fundação do frontend. Esta fase não cria um segundo cliente; ela endurece capacidades de instalação e operação em dispositivos.

## Pré-condições

```text
Frontend React estável
API estável
OpenAPI versionado
autenticação
Design Tokens
permissões
observabilidade
```

## Ordem

```text
PWA Manifest
Service Worker
cache do app shell
Installability
IndexedDB adapter
offline read quando aplicável
offline queue somente para fluxos aprovados
idempotência
reconciliação
push notifications
adaptações touch
safe areas
testes em tablet e celular
```

## Regra

Não duplicar páginas ou regras para criar uma versão mobile. A adaptação ocorre por layout e componentes responsivos na mesma base React.
# 40. FASE 33 — Build, distribuição e release

## Ordem

```text
npm/pnpm install reproduzível
typecheck
lint
unit tests
build Vite
PWA asset validation
manifest validation
service worker validation
E2E smoke test
deploy staging
deploy production
hash de artefatos
release manifest
channels
rollback
```

## Desktop

A distribuição desktop inicial será a instalação da PWA.

Tauri somente será adotado mediante ADR futuro se surgir necessidade nativa que a PWA não atenda. Mesmo nesse caso, a UI React será reutilizada.

## Matrizes

Testar em:

```text
Windows 10/11 com navegador suportado
desktop largo
notebook
tablet
celular
instalação PWA
atualização
sem internet para o app shell
tema claro
tema escuro
```
# 41. FASE 34 — Hardening

## Áreas

```text
Security review
Tenant isolation
Permission review
Backup restore drill
Disaster recovery
Performance
Large database
Network failure
Long-running jobs
Log retention
Privacy
Fiscal review
Financial reconciliation
Release rollback
```

---

# 42. Ordem das migrations

A numeração real será gerada pelo Alembic, mas a sequência conceitual será:

```text
0001 legacy baseline
0002 schema version metadata
0003 default tenant company branch
0004 users tenant scope
0005 customers public id and tenant
0006 suppliers public id and tenant
0007 materials public id and tenant
0008 budgets public id and tenant
0009 audit v2
0010 outbox
0011 customer soft delete and version
0012 supplier soft delete and version
0013 material precision preparation
0014 budget money precision phase 1
0015 inventory foundations
...
```

## Regras

- uma migration não deverá misturar vários módulos sem necessidade;
- dados devem ser migrados em etapas;
- constraints entram depois da limpeza dos dados quando necessário;
- índices entram após análise de consulta;
- colunas `NOT NULL` em tabela populada exigem backfill;
- renomear exige compatibilidade temporária;
- excluir coluna ocorre em revision posterior à troca de leitura e escrita.

---

# 43. Ordem de remoção do monólito de modelos

O arquivo monolítico de modelos não será dividido todo de uma vez.

Ordem:

```text
1. Cliente
2. Fornecedor
3. Marca e Material
4. Orçamento
5. Kanban e Agenda
6. Compras
7. Estoque
8. Financeiro
9. RH
10. Configurações e Usuários
```

Para cada grupo:

```text
criar modelo no módulo
manter import de compatibilidade
atualizar consumidores
executar testes
buscar imports antigos
remover export antigo somente quando zerado
```

O arquivo legado poderá se tornar uma facade temporária:

```python
from organizeg3.modules.customers.infrastructure.orm.customer_model import CustomerModel
```

Não duplicar o mesmo `__tablename__` em dois models carregados no mesmo metadata.

---

# 44. Ordem de modernização dos tipos

## IDs

```text
public UUID primeiro
PK física depois, se realmente necessário
```

## Money

```text
Financeiro
Orçamentos
Compras
Estoque
Produção
Fiscal
RH
```

## Datetime

```text
Audit e eventos
Auth
Clientes
Projetos
Orçamentos
Operações
Financeiro
RH
Fiscal
```

## Status

```text
criar enum de domínio
validar strings legadas
mapear aliases
migrar valores
adicionar constraint
```

---

# 45. Ordem de testes

## Antes da migração

Testes de caracterização:

```text
login
clientes
fornecedores
materiais
orçamento
financeiro básico
backup
encerramento
```

## Fundação

```text
settings
paths
logging
database
migrations
unit of work
event bus
task runner
permissions
audit
```

## Por módulo

```text
domain
handlers
repositories SQLite
repositories PostgreSQL
permissions
audit
UI viewmodels
UI smoke
migration
regression
```

## Antes de release

```text
end-to-end
offline
sync
backup restore
upgrade
installer
performance
security
```

---

# 46. Branches e commits

## Branches

```text
feature/foundation-tooling
feature/database-baseline
feature/core-services
feature/customers-vertical-slice
feature/<module>-<slice>
fix/<problem>
```

## Commits

Um commit deverá representar uma intenção.

Exemplos:

```text
chore: adiciona uv e baseline de qualidade
test: caracteriza encerramento pós-backup
fix: coordena shutdown de workers
db: cria baseline alembic do schema legado
core: adiciona unit of work
customers: implementa criação de cliente
customers: integra nova página por feature flag
```

---

# 47. Formato de solicitação ao Claude

Usar este cabeçalho em todas as solicitações:

```text
Você está trabalhando no OrganizeG3.

Documentos obrigatórios:
- ORGANIZEG3_ESPECIFICACAO_MESTRA_UNICA.md
- ORGANIZEG3_STACK_TECNOLOGICO_OFICIAL.md
- ORGANIZEG3_ORDEM_OFICIAL_DE_IMPLEMENTACAO.md

Etapa autorizada:
[INFORMAR FASE E LOTE]

Objetivo:
[INFORMAR OBJETIVO ÚNICO]

Arquivos fornecidos:
[LISTAR]

Restrições:
- leia os arquivos completos;
- não remova funções sem localizar consumidores;
- não crie arquitetura paralela;
- não avance para a próxima etapa;
- não altere arquivos fora do lote sem justificar;
- use a stack oficial;
- preserve compatibilidade;
- devolva arquivos completos quando solicitado;
- crie testes;
- informe comandos de validação.
```

---

# 48. Prompt 00 — Diagnóstico inicial para o Claude

```text
Realize somente o diagnóstico da Fase 01.

Não altere nenhum arquivo.

Leia todo o workspace e produza:
1. entrypoints;
2. grafo resumido de imports;
3. mapa de páginas e dialogs;
4. inventário de acesso ao banco;
5. inventário dos models e tabelas;
6. migrações manuais;
7. threads e workers;
8. backup e restauração;
9. build e empacotamento;
10. testes existentes;
11. riscos;
12. sequência recomendada dentro da Fase 02.

Cite caminho e linha para cada conclusão.
Não proponha reescrita completa.
```

---

# 49. Prompt 01 — Caracterização do encerramento

```text
Implemente apenas os testes de caracterização do ciclo de vida atual.

Cubra:
- fechar pelo X;
- fechar pelo botão;
- logout;
- troca de usuário;
- encerramento após backup;
- worker ativo;
- ausência de processo residual.

Não refatore ainda.
Primeiro registre o comportamento atual.
Entregue os arquivos de teste completos e como executá-los.
```

---

# 50. Prompt 02 — Correção do ciclo de vida

```text
Com base nos testes aprovados, crie um coordenador único de encerramento.

Preserve o backup.
Preserve logout e troca de usuário.
Não use os.kill como solução normal.
Não force terminate de QThread como primeira opção.
Garanta request_stop, wait e timeout.
Atualize todos os pontos de saída para utilizar o serviço.
Entregue os arquivos completos e os testes.
```

---

# 51. Prompt 03 — Tooling

```text
Implemente somente a Fase 03.

Crie pyproject.toml, .python-version e uv.lock com base nas dependências realmente usadas.

Não mova arquivos.
Não formate todo o legado.
Configure Ruff, mypy e pytest de forma incremental.
Garanta que o entrypoint atual continue abrindo.
```

---

# 52. Prompt 04 — Baseline Alembic

```text
Implemente somente a baseline de persistência.

Compare metadata e banco de teste.
Crie a revision 0001_legacy_baseline.
Não aplique stamp automaticamente.
Crie um validador de schema anterior ao stamp.
Converta as migrações manuais apenas depois de reproduzi-las em revisions.
Não altere tipos financeiros nesta etapa.
```

---

# 53. Prompt 05 — Primeira fatia de Clientes

```text
Implemente a Fase 10 em lotes.

Lote atual:
[domain/application/infrastructure/presentation]

Reutilize a tabela clientes.
Não renomeie colunas sem migration.
Não remova o dialog legado.
Use feature flag.
A UI não acessa SQLAlchemy.
Crie testes em cada camada.
Pare após concluir o lote.
```

---

# 54. Modelo de relatório de entrega do Claude

```markdown
# Entrega

## Etapa
FASE XX — Lote XX

## Objetivo
...

## Diagnóstico
...

## Arquivos criados
- ...

## Arquivos alterados
- ...

## Migration
- revisão:
- upgrade:
- downgrade:
- risco:

## Compatibilidade
...

## Testes
- comando:
- resultado:

## Validação manual
1. ...
2. ...

## Riscos restantes
...

## Próximo lote recomendado
...
```

---

# 55. Portões de aprovação do proprietário

O proprietário deverá confirmar explicitamente antes de:

```text
aplicar migration em banco real
remover arquivo legado
converter dinheiro
trocar autenticação
ativar Supabase
ativar sincronização
alterar build
publicar atualização
ativar integração fiscal
ativar IA com escrita
```

---

# 56. O que não deve ser feito agora

Enquanto a Fase 10 não estiver concluída, não iniciar:

```text
PWA
microserviços
Celery
Redis
BI completo
IA
integração fiscal real
sincronização de todos os módulos
conversão global de IDs
conversão global de dinheiro
redesign total
```

---

# 57. Primeira sequência prática de entregas

A sequência imediata recomendada é:

```text
Entrega 01 — Diagnóstico sem alteração

Entrega 02 — Testes de caracterização de startup/shutdown/backup

Entrega 03 — Correção do encerramento

Entrega 04 — uv, pyproject e testes baseline

Entrega 05 — Novo bootstrap e logging

Entrega 06 — Alembic baseline

Entrega 07 — Engine/session sem side effect de import

Entrega 08 — Unit of Work e repositories contracts

Entrega 09 — Tenant/Company padrão

Entrega 10 — Permissões e auditoria

Entrega 11 — App Shell e feature flags

Entrega 12 — Clientes Domain

Entrega 13 — Clientes Application

Entrega 14 — Clientes Infrastructure e migration

Entrega 15 — Clientes Presentation

Entrega 16 — Clientes integração, regressão e ativação

Entrega 17 — Fornecedores

Entrega 18 — Materiais

Entrega 19 — CRM

Entrega 20 — Projetos

Entrega 21 — Orçamentos
```

Depois dessas entregas, a equipe deverá revisar o ritmo, a arquitetura e o impacto antes de continuar.

---

# 58. Critério para considerar a fundação concluída

A fundação estará concluída quando:

```text
o app inicia por python -m organizeg3
uv.lock é reproduzível
o app fecha sem processo residual
backup e restore foram testados
Alembic controla o schema
não existem ALTER TABLE em startup
sessões não são criadas por import
core possui settings/logging/errors
Unit of Work funciona
permissões e audit funcionam
Tenant padrão existe
Design System está integrado
Clientes funciona de ponta a ponta
SQLite novo e legado são suportados
testes automatizados cobrem a fatia
build React/PWA abre a aplicação e o smoke test E2E passa
```

---

# 59. Critério para começar o segundo módulo

O segundo módulo somente deverá começar após:

- Clientes passar por uma semana de uso ou ciclo de validação equivalente;
- nenhum bug crítico de dados;
- nenhum lock recorrente;
- migration validada;
- padrão de arquivos aprovado;
- padrão de UI aprovado;
- documentação atualizada.

---

# 60. Resultado esperado

Seguindo esta ordem, o OrganizeG3 evoluirá sem depender de uma reescrita arriscada.

O código atual continuará utilizável durante a transição.

Cada módulo migrado deixará um padrão repetível para o seguinte.

A arquitetura futura será introduzida onde agrega segurança e manutenção, sem interromper o trabalho diário da empresa.

A primeira ação de código autorizada após este documento é:

```text
FASE 01 — Diagnóstico executável
```

A primeira alteração de código autorizada será:

```text
FASE 02 — Testes de caracterização e estabilização do ciclo de vida
```
