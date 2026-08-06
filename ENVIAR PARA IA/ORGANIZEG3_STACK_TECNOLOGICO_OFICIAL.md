# ORGANIZEG3 — STACK TECNOLÓGICO OFICIAL

> Documento normativo para implementação, manutenção, testes, empacotamento e evolução técnica do OrganizeG3.

---

| Propriedade | Valor |
|---|---|
| Documento | `ORGANIZEG3_STACK_TECNOLOGICO_OFICIAL.md` |
| Versão | `1.0.0` |
| Data da decisão | 2026-08-05 |
| Status | Stack oficial aprovada para implementação |
| Autoridade | Complementar à Especificação Mestra Única |
| Aplicação inicial | OrganizeG3 Desktop para Windows |
| Arquitetura-alvo | Desktop offline-first + API + PostgreSQL/Supabase |
| Idioma da documentação | Português |
| Idioma do código | Inglês |
| Fuso de exibição padrão | America/Sao_Paulo |
| Armazenamento de instantes | UTC |

---

# 1. Finalidade

Este documento define, sem ambiguidades, quais tecnologias serão utilizadas no OrganizeG3.

Ele existe para impedir que:

- cada módulo utilize bibliotecas diferentes;
- o Claude crie uma arquitetura paralela;
- sejam adicionadas dependências sem necessidade;
- regras de negócio sejam colocadas na interface;
- o Desktop acesse o banco remoto de forma descontrolada;
- tecnologias experimentais sejam introduzidas sem decisão arquitetural;
- versões de dependências variem entre máquinas;
- uma funcionalidade funcione no ambiente de desenvolvimento, mas falhe no executável;
- o projeto seja reescrito integralmente sem necessidade.

Este documento deverá ser entregue ao Claude junto da Especificação Mestra Única e dos arquivos atuais do projeto.

---

# 2. Autoridade e precedência

Em assuntos estritamente tecnológicos, este documento prevalece sobre referências genéricas ou contraditórias existentes em documentos anteriores.

A ordem de precedência será:

```text
1. ADR específico aprovado posteriormente
2. Este documento de Stack Tecnológico
3. Especificação Mestra Única
4. Documentos técnicos DOC-100 a DOC-130
5. Padrões de desenvolvimento
6. Código legado
```

Este documento não substitui:

- regras de negócio;
- mapa funcional;
- modelo de domínio;
- políticas de permissão;
- Design System;
- requisitos de auditoria;
- contratos de sincronização.

Ele define a tecnologia usada para implementar esses contratos.

---

# 3. Decisão executiva

A stack oficial do OrganizeG3 será:

```text
Linguagem principal
Python 3.13

Desktop
PySide6 / Qt 6 Widgets

Arquitetura
Modular Monolith
Clean Architecture
Domain-Driven Design
CQRS leve
Event-driven interno
Offline-first

ORM
SQLAlchemy 2

Migrations
Alembic

Banco local
SQLite

Banco compartilhado
PostgreSQL 17 no Supabase

API
FastAPI

Validação de fronteira
Pydantic 2

Autenticação
Supabase Auth

Arquivos em nuvem
Supabase Storage

Sincronização
API própria + Outbox/Inbox + idempotência

Dependências Python
uv + pyproject.toml + uv.lock

Qualidade
Ruff + mypy

Testes
pytest + pytest-qt

Empacotamento Windows
PyInstaller em modo onedir

Instalador Windows
Inno Setup

Backend
Container Docker Linux

PWA futura
React 19 + TypeScript + Vite 8

CI
GitHub Actions
```

---

# 4. Decisões fundamentais

## 4.1 O produto inicial é Desktop

A primeira aplicação oficial será:

```text
OrganizeG3 Desktop
Sistema operacional inicial: Windows 10 e Windows 11
Interface: Qt Widgets
Framework Python: PySide6
```

O Desktop deverá funcionar mesmo quando a internet estiver temporariamente indisponível.

A PWA será construída posteriormente utilizando a mesma API e os mesmos contratos de negócio.

---

## 4.2 Python será a linguagem principal

A linguagem oficial do núcleo, Desktop, API, workers, integrações e automações será Python.

Versão-alvo:

```text
Python 3.13.x
```

Restrição no projeto:

```toml
requires-python = ">=3.13,<3.14"
```

### Motivo da escolha

Embora Python 3.14 já exista, o OrganizeG3 adotará Python 3.13 durante a fundação para:

- reduzir risco de incompatibilidade com bibliotecas;
- preservar compatibilidade com o código existente;
- facilitar empacotamento com PyInstaller;
- evitar migração de linguagem durante a refatoração inicial;
- utilizar uma linha estável e amplamente suportada.

A migração para Python 3.14 deverá ocorrer apenas após:

- execução completa dos testes;
- validação do PyInstaller;
- validação do PySide6;
- validação dos drivers de banco;
- criação de ADR;
- geração de novo `uv.lock`.

---

## 4.3 Arquitetura modular monolítica

O OrganizeG3 será inicialmente um monólito modular.

Isso significa:

```text
Um repositório principal
Um núcleo arquitetural
Módulos funcionalmente separados
Contratos internos explícitos
Sem microserviços prematuros
```

Não deverão ser criados microserviços separados para:

- clientes;
- projetos;
- estoque;
- produção;
- financeiro;
- RH;
- fiscal;
- BI.

Separações físicas somente poderão ocorrer quando existirem evidências operacionais, técnicas ou de escala que justifiquem a mudança.

Toda separação futura deverá possuir ADR.

---

# 5. Arquitetura oficial por camadas

```text
Presentation
    ↓
Application
    ↓
Domain
    ↓
Infrastructure
```

## 5.1 Presentation

Responsável por:

- widgets;
- páginas;
- dialogs;
- view models;
- controllers de apresentação;
- navegação;
- formatação visual;
- coleta de entrada;
- apresentação de erros.

Tecnologias:

```text
PySide6
Qt Widgets
Qt Model/View
Signals e Slots
QThreadPool
QRunnable
```

Presentation não poderá importar modelos ORM.

---

## 5.2 Application

Responsável por:

- casos de uso;
- comandos;
- consultas;
- transações;
- permissões;
- orquestração;
- publicação de eventos;
- integração entre módulos;
- DTOs de entrada e saída.

Tecnologias:

```text
Python
Pydantic 2 para DTOs de fronteira
Protocol e ABC para contratos
Dataclasses quando apropriado
```

Application não poderá depender de PySide6.

---

## 5.3 Domain

Responsável por:

- entidades;
- agregados;
- value objects;
- regras de negócio;
- invariantes;
- eventos de domínio;
- políticas;
- especificações;
- transições de estado.

Tecnologias permitidas:

```text
Python Standard Library
dataclasses
enum
decimal
datetime
uuid
typing
collections
```

O Domain não poderá importar:

```text
PySide6
SQLAlchemy
FastAPI
Pydantic BaseModel
Supabase
psycopg
sqlite3
httpx
Celery
Redis
```

Pydantic não será utilizado para definir entidades de domínio.

---

## 5.4 Infrastructure

Responsável por:

- SQLAlchemy;
- bancos;
- migrations;
- autenticação externa;
- arquivos;
- rede;
- email;
- filas;
- logging;
- integrações;
- implementação dos repositórios.

Tecnologias:

```text
SQLAlchemy 2
Alembic
SQLite
PostgreSQL
psycopg 3
FastAPI
httpx
Supabase
Redis
Celery
```

Redis e Celery somente serão introduzidos na fase prevista neste documento.

---

# 6. Gerenciamento de dependências

## 6.1 Ferramenta oficial

A ferramenta oficial será:

```text
uv
```

Arquivos obrigatórios:

```text
pyproject.toml
uv.lock
.python-version
```

O `uv.lock` deverá ser versionado no Git.

Não será permitido manter versões divergentes em:

```text
requirements.txt
requirements-dev.txt
Pipfile
poetry.lock
conda.yaml
```

Arquivos `requirements.txt` poderão ser gerados apenas para compatibilidade de implantação, nunca como fonte oficial.

---

## 6.2 Comandos oficiais

Criar ambiente:

```bash
uv sync
```

Executar aplicação:

```bash
uv run python -m organizeg3
```

Executar testes:

```bash
uv run pytest
```

Verificar lock:

```bash
uv lock --check
```

Executar com lock sem atualização:

```bash
uv run --locked pytest
```

Adicionar dependência:

```bash
uv add nome-do-pacote
```

Adicionar dependência de desenvolvimento:

```bash
uv add --dev nome-do-pacote
```

Atualizar uma dependência específica:

```bash
uv lock --upgrade-package nome-do-pacote
```

O Claude não poderá editar manualmente o `uv.lock`.

---

# 7. Política de versões

## 7.1 Regra geral

O `pyproject.toml` definirá a família compatível.

O `uv.lock` fixará a versão exata.

Exemplo:

```toml
dependencies = [
    "sqlalchemy>=2.0,<2.1",
]
```

O ambiente real utilizará a versão exata registrada no `uv.lock`.

---

## 7.2 Atualizações

Atualizações patch poderão ser propostas em lote após testes.

Atualizações minor ou major deverão:

1. ser feitas em branch específica;
2. atualizar o lock;
3. executar todos os testes;
4. gerar o executável;
5. testar instalação limpa;
6. testar atualização de banco;
7. registrar decisão;
8. validar compatibilidade com dados existentes.

Nenhuma ferramenta deverá atualizar dependências automaticamente em produção.

---

# 8. Stack Python oficial

## 8.1 Núcleo

```text
Python 3.13.x
typing
dataclasses
enum
decimal.Decimal
datetime com timezone
uuid.UUID
pathlib
logging
```

---

## 8.2 Dependências principais

```text
PySide6 >=6.10,<6.11
SQLAlchemy >=2.0,<2.1
Alembic >=1.19,<2
Pydantic >=2,<3
pydantic-settings >=2,<3
FastAPI >=0.115,<1
Uvicorn >=0.30,<1
httpx >=0.28,<1
psycopg >=3.2,<4
Jinja2 >=3.1,<4
```

Os limites acima representam famílias aprovadas.

A versão exata será definida pelo `uv.lock`.

---

# 9. Desktop — PySide6

## 9.1 Framework

A interface Desktop utilizará:

```text
PySide6
Qt 6
Qt Widgets
```

Não utilizar:

```text
PyQt5
PyQt6
PySide2
Tkinter
Kivy
Flet
Electron para o Desktop principal
QML como stack principal
```

QML somente poderá ser introduzido mediante ADR e caso de uso específico.

---

## 9.2 Padrão de interface

O Desktop seguirá:

```text
View
ViewModel
Application Service
```

A View será um `QWidget`, `QDialog`, `QMainWindow` ou componente Qt equivalente.

O ViewModel poderá utilizar `QObject`, signals e properties quando necessário.

A ViewModel não poderá acessar o banco diretamente.

---

## 9.3 Threading

A thread principal será reservada à interface.

Operações que poderão bloquear deverão utilizar:

```text
QThreadPool
QRunnable
Signals
Cancellation Token próprio
```

Exemplos:

- sincronização;
- exportação;
- geração de PDF;
- consultas extensas;
- backup;
- restauração;
- upload;
- download;
- processamento de imagens;
- relatórios.

Não utilizar `threading.Thread` diretamente em cada página.

Deverá existir um serviço central de execução de tarefas.

---

## 9.4 Async no Desktop

Não será utilizado `asyncio` como base do Desktop na primeira fase.

Não utilizar:

```text
qasync
AsyncSession
loops asyncio misturados ao Qt
```

O cliente HTTP poderá ser executado de forma síncrona dentro de workers Qt.

Essa decisão reduz a complexidade entre o event loop do Qt e o event loop do Python.

---

## 9.5 Model/View

Listas e tabelas relevantes deverão utilizar:

```text
QAbstractTableModel
QAbstractListModel
QSortFilterProxyModel
```

Evitar preencher manualmente milhares de células em `QTableWidget`.

`QTableWidget` será permitido apenas em telas pequenas e estáticas.

---

## 9.6 Design System

A aparência será obtida exclusivamente por:

```text
ThemeManager
theme_design
Design Tokens
IconManager
Component Factory
```

Proibido em páginas:

```python
widget.setStyleSheet("background: #ffffff;")
```

Proibido:

- cores hexadecimais espalhadas;
- fontes definidas por módulo;
- margens fixas não tokenizadas;
- ícones carregados por caminhos aleatórios;
- emojis como ícones;
- estilos duplicados.

Os ícones oficiais serão baseados em Material Symbols/Material Icons no estilo definido pelo Design System.

---

# 10. Domínio e tipos fundamentais

## 10.1 Identificadores

Identificadores públicos e de sincronização utilizarão:

```text
UUID versão 4
```

Tipo no Python:

```python
uuid.UUID
```

Tipo no PostgreSQL:

```text
uuid
```

No SQLite:

```text
TEXT canônico no formato UUID
```

Não utilizar IDs sequenciais como identificador exposto entre aplicações.

IDs internos sequenciais somente poderão existir por necessidade de desempenho e não substituirão o UUID público.

---

## 10.2 Dinheiro

Nunca utilizar `float` para dinheiro.

No domínio:

```python
Decimal
Money value object
Currency code
```

No PostgreSQL:

```text
NUMERIC(19,4)
```

No SQLite local, a persistência utilizará um `TypeDecorator` oficial que preserve exatidão.

Estratégia preferencial:

```text
valor escalado em inteiro
escala definida
conversão centralizada
```

Nenhuma página poderá arredondar valores de negócio por conta própria.

---

## 10.3 Quantidades

Quantidades técnicas utilizarão `Decimal`.

Exemplos:

- metros;
- metros quadrados;
- milímetros;
- quilogramas;
- horas;
- quantidade fracionada;
- consumo.

Contagens inteiras utilizarão `int`.

---

## 10.4 Datas e horas

Instantes deverão ser armazenados em UTC.

No Python:

```python
datetime com tzinfo
```

No PostgreSQL:

```text
TIMESTAMPTZ
```

Datas sem horário utilizarão:

```python
date
```

A conversão para `America/Sao_Paulo` ocorrerá apenas na apresentação.

Proibido salvar datetime ingênuo em novos fluxos.

---

## 10.5 Enums

Enums de domínio serão definidos em Python.

Na persistência, utilizar preferencialmente:

```text
VARCHAR com validação
```

Evitar criar enums nativos do PostgreSQL para estados de negócio que mudam com frequência.

Enums nativos somente poderão ser utilizados após decisão específica.

---

# 11. Persistência — SQLAlchemy

## 11.1 Versão

```text
SQLAlchemy 2.0.x
```

Utilizar API declarativa moderna e consultas no estilo SQLAlchemy 2.

---

## 11.2 Sessões

A aplicação utilizará sessões síncronas.

Não misturar no mesmo módulo:

```text
Session
AsyncSession
```

A unidade de trabalho será explícita.

Padrão:

```text
Application Service
    ↓
Unit of Work
    ↓
Repositories
    ↓
SQLAlchemy Session
```

---

## 11.3 Modelos ORM

Modelos SQLAlchemy pertencem à Infrastructure.

Entidades de domínio não herdarão de `DeclarativeBase`.

Proibido:

```text
Domain Entity = ORM Model
```

Serão utilizados mappers ou factories de conversão entre:

```text
ORM Model
Domain Entity
DTO
```

---

## 11.4 Repositórios

A interface do repositório pertence a Application ou Domain, conforme o caso.

A implementação SQLAlchemy pertence a Infrastructure.

Exemplo:

```python
class CustomerRepository(Protocol):
    def get(self, customer_id: UUID) -> Customer | None: ...
    def add(self, customer: Customer) -> None: ...
```

---

## 11.5 Consultas

Consultas complexas de leitura poderão utilizar read models específicos.

O CQRS será leve:

```text
Commands alteram estado
Queries leem dados
```

Não será criada infraestrutura distribuída de CQRS.

---

# 12. Migrations — Alembic

## 12.1 Ferramenta

```text
Alembic
```

Toda mudança estrutural deverá gerar migration.

Proibido em código de inicialização:

```text
verificar se coluna existe e executar ALTER TABLE manual
```

---

## 12.2 Estrutura

```text
migrations/
├── env.py
├── script.py.mako
└── versions/
```

Migrações deverão ser testadas contra:

```text
SQLite
PostgreSQL
```

Quando houver recurso exclusivo do PostgreSQL, a migration deverá verificar o dialeto e documentar o comportamento local.

---

## 12.3 Autogenerate

`--autogenerate` poderá criar um rascunho.

O Claude deverá revisar a migration inteira.

Nunca aceitar migration autogerada sem análise.

---

## 12.4 Reversão

Toda migration deverá possuir `downgrade()` quando a reversão não causar perda inevitável de dados.

Migrações destrutivas deverão:

- criar backup;
- copiar dados;
- validar contagens;
- preservar rollback quando possível;
- exigir aprovação.

---

# 13. Banco local — SQLite

## 13.1 Função

O SQLite será utilizado para:

- operação offline;
- cache controlado;
- fila de sincronização;
- dados locais ainda não sincronizados;
- configurações locais;
- sessões de trabalho;
- transição do legado.

O SQLite não será a fonte compartilhada oficial após a implantação da nuvem.

---

## 13.2 Configuração obrigatória

Ao abrir cada conexão:

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
```

O código deverá validar se os pragmas foram aplicados.

---

## 13.3 Arquivo

O banco local deverá ficar em diretório de dados da aplicação, nunca ao lado do executável.

Exemplo Windows:

```text
%LOCALAPPDATA%\OrganizeG3\data\organizeg3.db
```

Backups locais:

```text
%LOCALAPPDATA%\OrganizeG3\backups\
```

Logs:

```text
%LOCALAPPDATA%\OrganizeG3\logs\
```

Arquivos temporários:

```text
%LOCALAPPDATA%\OrganizeG3\temp\
```

---

## 13.4 Concorrência

O Desktop deverá utilizar sessões curtas.

Não manter transações abertas enquanto dialogs aguardam interação do usuário.

Operações em background deverão criar sua própria sessão.

Sessões SQLAlchemy não deverão ser compartilhadas entre threads.

---

# 14. Banco compartilhado — PostgreSQL no Supabase

## 14.1 Versão-alvo

```text
PostgreSQL 17
```

PostgreSQL 17 será a linha de compatibilidade do projeto no Supabase.

Uma futura atualização para PostgreSQL 18 exigirá:

- verificação da versão oferecida pelo Supabase;
- teste de extensões;
- teste de RLS;
- teste de migrations;
- teste de índices;
- teste de backup e restauração;
- ADR.

---

## 14.2 Driver

```text
psycopg 3
```

Não utilizar `psycopg2` em novos módulos.

---

## 14.3 Fonte oficial

O PostgreSQL será a fonte oficial de:

- dados compartilhados;
- usuários associados ao negócio;
- permissões;
- documentos e metadados;
- eventos;
- auditoria;
- sincronização;
- configurações compartilhadas;
- informações dos módulos.

---

## 14.4 Multi-tenant

Toda tabela de negócio deverá possuir escopo de Tenant ou Empresa.

Padrão preferencial:

```text
tenant_id
company_id
branch_id quando aplicável
```

O filtro deverá ser aplicado:

```text
na API
na Application Layer
nos repositórios
nas políticas RLS
```

RLS será defesa adicional, não substituto da autorização da aplicação.

---

## 14.5 Extensões aprovadas

Inicialmente:

```text
pgcrypto quando necessário
pg_trgm
uuid-ossp somente se necessário
pg_stat_statements
```

Não adicionar extensões sem registrar:

- necessidade;
- disponibilidade no Supabase;
- impacto em backup;
- impacto em migração;
- alternativa sem extensão.

---

# 15. Supabase

## 15.1 Serviços utilizados

```text
Supabase PostgreSQL
Supabase Auth
Supabase Storage
Row Level Security
Backups da plataforma
```

Uso futuro e controlado:

```text
Realtime
Edge Functions
Vector
```

---

## 15.2 Serviços que não serão usados como camada de negócio

O Desktop não deverá utilizar PostgREST diretamente para executar regras críticas.

O Desktop não deverá gravar diretamente em tabelas compartilhadas.

O caminho oficial será:

```text
Desktop
    ↓ HTTPS
OrganizeG3 API
    ↓
Application Layer
    ↓
Repositories
    ↓
PostgreSQL/Supabase
```

Exceção:

```text
autenticação pelo provedor de identidade
```

Mesmo a autenticação deverá passar por um adapter central.

---

## 15.3 Storage

Arquivos binários serão armazenados no Supabase Storage.

O PostgreSQL armazenará apenas:

- identificador;
- bucket;
- caminho;
- nome;
- tipo MIME;
- tamanho;
- hash;
- proprietário;
- Tenant;
- entidade vinculada;
- versão;
- datas;
- status.

Não armazenar PDFs, fotos e anexos como BLOB na base principal.

---

# 16. API — FastAPI

## 16.1 Framework

```text
FastAPI
Pydantic 2
Uvicorn
SQLAlchemy 2 síncrono
```

---

## 16.2 Estilo da API

A API será:

```text
REST
JSON
OpenAPI
Versionada
Orientada a comandos explícitos
```

Prefixo:

```text
/api/v1
```

Exemplos:

```text
POST /api/v1/customers
GET  /api/v1/customers
GET  /api/v1/customers/{id}
POST /api/v1/production-orders/{id}/release
POST /api/v1/installations/{id}/check-in
POST /api/v1/payables/{id}/approve
```

Não utilizar endpoints genéricos como:

```text
POST /update-status
POST /execute
POST /save-anything
```

---

## 16.3 Sync versus async

A API utilizará casos de uso e repositórios síncronos na primeira fase.

Rotas que chamam serviços síncronos deverão preferir:

```python
def endpoint(...):
    ...
```

Não utilizar `async def` para depois executar operações bloqueantes diretamente.

Tarefas longas serão enviadas ao worker quando essa infraestrutura estiver ativa.

---

## 16.4 DTOs

Pydantic será utilizado para:

- request;
- response;
- validação de API;
- configuração;
- serialização;
- integração.

Pydantic não será utilizado para:

- substituir entidades;
- concentrar regras de negócio;
- executar transições de estado;
- acessar repositórios.

---

## 16.5 Documentação

FastAPI gerará OpenAPI.

Em produção, `/docs` e `/redoc` deverão:

- estar desativados; ou
- exigir autenticação administrativa.

O arquivo OpenAPI versionado deverá ser utilizado para gerar clientes.

---

## 16.6 Cliente Desktop

O Desktop utilizará um adapter HTTP central baseado em:

```text
httpx
```

A UI não deverá construir URLs diretamente.

Deverá existir:

```text
ApiClient
AuthenticationClient
SyncClient
DocumentClient
```

---

# 17. Autenticação e identidade

## 17.1 Provedor

```text
Supabase Auth
```

---

## 17.2 Fluxo

```text
Usuário informa credenciais
    ↓
IdentityProvider Adapter
    ↓
Supabase Auth
    ↓
Access Token + Refresh Token
    ↓
Desktop guarda tokens com segurança
    ↓
API valida JWT
    ↓
API resolve Tenant, usuário, perfis e permissões
```

---

## 17.3 Armazenamento de tokens

No Desktop, refresh tokens deverão utilizar o cofre de credenciais do sistema operacional.

Biblioteca aprovada:

```text
keyring
```

Proibido armazenar:

- senha;
- access token;
- refresh token;
- chave de API;

em:

```text
SQLite em texto puro
arquivo JSON
arquivo INI
arquivo .env distribuído
log
```

---

## 17.4 Autorização

A autorização será implementada pela Application Layer.

Modelo:

```text
RBAC
+ permissões granulares
+ escopo de Tenant
+ escopo de Empresa
+ escopo de Filial
+ regras contextuais
```

Ocultar botão não será considerado segurança suficiente.

---

# 18. Offline-first e sincronização

## 18.1 Estratégia

A sincronização será própria do OrganizeG3.

Não dependerá exclusivamente de Supabase Realtime.

Componentes:

```text
Local Change Log
Outbox
Inbox
Sync Queue
Idempotency Keys
Version Field
Conflict Resolver
Retry Policy
Tombstones
Sync Cursor
```

---

## 18.2 Campos de sincronização

Aplicar quando necessário:

```text
id
tenant_id
version
created_at
updated_at
deleted_at
sync_status
server_version
last_synced_at
origin_device_id
correlation_id
idempotency_key
```

Não adicionar todos os campos automaticamente a toda tabela.

Aplicar conforme o papel da entidade.

---

## 18.3 Fonte oficial

Após sincronização confirmada:

```text
PostgreSQL = fonte oficial compartilhada
SQLite = réplica local controlada
```

Registros ainda não enviados permanecerão na Outbox local.

---

## 18.4 Conflitos

Estratégias permitidas:

```text
Versionamento otimista
Rejeição por versão
Merge específico por agregado
Evento compensatório
Revisão manual
```

Proibido:

```text
last write wins universal
sobrescrever silenciosamente
ignorar conflito
```

---

## 18.5 Idempotência

Toda operação repetível deverá possuir `idempotency_key`.

A API deverá reconhecer uma repetição e retornar o resultado anterior quando apropriado.

---

# 19. Eventos, Outbox e auditoria

## 19.1 Event Bus

A primeira fase utilizará um Event Bus interno em Python.

Tecnologia:

```text
implementação própria e pequena
handlers explícitos
registro no composition root
```

Não introduzir Kafka, RabbitMQ ou NATS na fundação.

---

## 19.2 Outbox

Eventos que precisam sobreviver ao processo deverão ser gravados na mesma transação do agregado.

Fluxo:

```text
Alterar agregado
    ↓
Salvar agregado
    ↓
Salvar evento na Outbox
    ↓
Commit
    ↓
Dispatcher publica
    ↓
Marca como processado
```

---

## 19.3 Auditoria

A auditoria utilizará tabelas próprias append-only.

Ela registrará:

```text
tenant_id
user_id
action
entity_type
entity_id
timestamp
old_values permitidos
new_values permitidos
reason
correlation_id
device_id
ip quando aplicável
```

Dados secretos não poderão ser inseridos na auditoria.

---

# 20. Background jobs

## 20.1 Fase inicial

Na fundação, tarefas locais utilizarão:

```text
QThreadPool no Desktop
serviços síncronos na API
```

FastAPI `BackgroundTasks` somente poderá ser usado para tarefas pequenas e não críticas.

Não utilizar `BackgroundTasks` para:

- folha;
- sincronização crítica;
- envio garantido;
- processamento fiscal;
- geração longa;
- backups;
- importações grandes.

---

## 20.2 Fase de escala

Quando houver servidor compartilhado e necessidade real:

```text
Celery 5.x
Redis 7.x
Celery Beat
```

Usos:

- relatórios agendados;
- notificações;
- emails;
- importações;
- exportações;
- processamento de documentos;
- rotinas de sincronização;
- indicadores;
- automações;
- webhooks.

O Claude não deverá introduzir Celery e Redis antes da fase autorizada.

---

# 21. Workflow e automações

O Workflow Engine será implementado internamente no monólito modular.

Tecnologia:

```text
Python
SQLAlchemy
PostgreSQL
Event Bus
Celery apenas quando ativado
```

Não utilizar inicialmente:

```text
Camunda
Temporal
Airflow
n8n como motor central
Zapier como motor central
```

Integrações externas poderão acionar webhooks, mas não serão a fonte oficial do workflow.

---

# 22. Arquivos e documentos

## 22.1 Templates

```text
Jinja2
```

Será utilizado para:

- contratos;
- orçamentos;
- termos;
- relatórios;
- emails;
- textos configuráveis.

---

## 22.2 PDF

Biblioteca principal:

```text
ReportLab
```

Uso:

- documentos oficiais;
- relatórios;
- recibos;
- termos;
- etiquetas;
- romaneios;
- fichas.

Não utilizar `wkhtmltopdf` como dependência obrigatória.

PDFs deverão ser testados após empacotamento.

---

## 22.3 DOCX

```text
python-docx
```

Uso:

- modelos editáveis;
- contratos;
- documentos exportáveis.

---

## 22.4 Planilhas

```text
openpyxl
```

Uso:

- exportações XLSX;
- relatórios;
- importações controladas;
- modelos de trabalho.

A planilha não será a fonte oficial dos dados.

---

## 22.5 Imagens

```text
Pillow
```

Uso:

- leitura;
- redimensionamento;
- thumbnail;
- conversão;
- validação básica.

---

## 22.6 Hash

Arquivos deverão possuir hash:

```text
SHA-256
```

O hash será utilizado para:

- integridade;
- duplicidade;
- cache;
- versionamento;
- sincronização.

---

# 23. Relatórios, gráficos e BI

## 23.1 Desktop

Para gráficos padrão:

```text
PySide6.QtCharts
```

Para relatórios estáticos e exportações específicas:

```text
matplotlib
```

Matplotlib não deverá controlar o estilo geral do Desktop.

---

## 23.2 Consultas analíticas

A primeira fase utilizará:

```text
SQLAlchemy
PostgreSQL
views
materialized views quando necessário
read models
```

Não introduzir data warehouse na fundação.

---

## 23.3 BI futuro

Quando volume e uso justificarem:

```text
PostgreSQL analítico
materialized views
jobs Celery
cache Redis
```

Uma ferramenta externa de BI poderá ser conectada somente após avaliação de segurança por Tenant.

---

# 24. Pesquisa

## 24.1 Local

```text
SQLite FTS5
```

---

## 24.2 Servidor

```text
PostgreSQL Full Text Search
pg_trgm
GIN indexes
```

Não utilizar inicialmente:

```text
Elasticsearch
OpenSearch
Meilisearch
Typesense
```

Esses serviços somente serão avaliados quando PostgreSQL não atender aos requisitos medidos.

---

# 25. Logs e observabilidade

## 25.1 Desktop

Utilizar:

```text
logging da Standard Library
RotatingFileHandler
formato estruturado
correlation_id
user_id quando permitido
tenant_id
module
event
```

Diretório:

```text
%LOCALAPPDATA%\OrganizeG3\logs\
```

---

## 25.2 API

Utilizar:

```text
logging
JSON estruturado
request_id
correlation_id
tempo de resposta
status
rota
```

Biblioteca opcional aprovada:

```text
structlog
```

Não adicionar `structlog` se o logging padrão já atender à fase atual.

---

## 25.3 Monitoramento futuro

A stack deverá permitir:

```text
OpenTelemetry
Sentry
métricas de infraestrutura
health checks
```

Esses serviços não são obrigatórios na fundação local.

---

# 26. Tratamento de erros

Deverá existir hierarquia própria:

```text
OrganizeGError
DomainError
ValidationError
PermissionDeniedError
NotFoundError
ConflictError
ConcurrencyError
PersistenceError
IntegrationError
SyncError
AuthenticationError
InfrastructureError
```

Erros de infraestrutura não deverão aparecer diretamente para o usuário.

A UI receberá um erro de aplicação com:

```text
code
user_message
technical_reference
recoverable
suggested_action
```

---

# 27. Configurações

## 27.1 Biblioteca

```text
pydantic-settings
```

---

## 27.2 Fontes

Ordem:

```text
defaults seguros
arquivo local não secreto
variáveis de ambiente
secret store
parâmetros de execução
```

---

## 27.3 Segredos

Produção:

```text
variáveis seguras do host
Supabase secrets
cofre do sistema operacional
```

Desenvolvimento:

```text
.env não versionado
.env.example sem segredos
```

---

# 28. PWA futura

## 28.1 Stack

```text
TypeScript 5.x
React 19
Vite 8
TanStack Query 5
Zustand
React Router
PWA Plugin/Workbox
CSS variables e Design Tokens
```

---

## 28.2 Comunicação

A PWA utilizará a mesma API FastAPI.

Não acessará tabelas do Supabase diretamente para comandos de negócio.

---

## 28.3 Estado

```text
TanStack Query = estado do servidor
Zustand = estado local da interface
```

Não duplicar dados de servidor no Zustand.

---

## 28.4 Design System

Desktop e PWA compartilharão:

- nomes dos tokens;
- paleta;
- tipografia;
- espaçamentos;
- status;
- iconografia;
- regras de componentes.

Eles não compartilharão o mesmo código de widget, pois utilizam tecnologias diferentes.

---

## 28.5 Offline

A PWA utilizará:

```text
Service Worker
IndexedDB
fila local
sincronização pela API
```

A mesma semântica de idempotência e conflitos será preservada.

---

# 29. Inteligência Artificial

## 29.1 Arquitetura

A IA utilizará adapters de provedor.

Interface:

```text
AIProvider
PromptRepository
AIActionService
AIApprovalService
```

---

## 29.2 Decisão de dependência

O núcleo não dependerá diretamente de:

```text
LangChain
LlamaIndex
framework de agentes
SDK proprietário em entidades
```

A primeira integração utilizará chamadas diretas e schemas Pydantic por meio de um adapter.

O provedor poderá ser substituído sem alterar o Domain.

---

## 29.3 Segurança

A IA:

- não acessará banco diretamente;
- não receberá segredos;
- não ultrapassará permissões do usuário;
- não executará comandos sem Application Layer;
- não aprovará ações sensíveis;
- não alterará dados sem confirmação;
- registrará uso, modelo, prompt versionado e resultado;
- deverá permitir desativação por Tenant.

---

# 30. Testes

## 30.1 Framework

```text
pytest
pytest-qt
pytest-cov
pytest-mock
pytest-asyncio somente para componentes realmente assíncronos
```

---

## 30.2 Categorias

```text
unit
application
domain
repository
database
migration
api
ui
integration
sync
security
regression
slow
```

---

## 30.3 Bancos de teste

Os testes deverão executar em:

```text
SQLite temporário
PostgreSQL de teste em container
```

Não validar migrations apenas no SQLite.

---

## 30.4 UI

Utilizar `pytest-qt`.

Testar:

- abertura;
- ações;
- permissões;
- validações;
- signals;
- estados vazios;
- erros;
- workers;
- encerramento;
- regressões críticas.

---

## 30.5 Cobertura

Metas iniciais:

```text
Domain: 90%
Application: 85%
Infrastructure crítica: 75%
Projeto total: 80%
```

Cobertura não substitui qualidade dos testes.

---

# 31. Qualidade de código

## 31.1 Formatter e linter

```text
Ruff
```

Comandos:

```bash
uv run ruff format .
uv run ruff check .
```

Não utilizar simultaneamente Black, isort e Flake8.

---

## 31.2 Tipagem

```text
mypy
```

A tipagem será incrementada até modo estrito nas camadas Domain e Application.

Comando:

```bash
uv run mypy src
```

Não utilizar `Any` para evitar modelagem.

---

## 31.3 Segurança de dependências

```text
pip-audit
```

Comando:

```bash
uv run pip-audit
```

Dependências vulneráveis deverão ser avaliadas antes da entrega.

---

# 32. Estrutura do repositório

```text
organizeg3/
├── pyproject.toml
├── uv.lock
├── .python-version
├── README.md
├── src/
│   └── organizeg3/
│       ├── __init__.py
│       ├── __main__.py
│       ├── bootstrap/
│       │   ├── application.py
│       │   ├── composition_root.py
│       │   └── settings.py
│       ├── core/
│       │   ├── auth/
│       │   ├── audit/
│       │   ├── database/
│       │   ├── documents/
│       │   ├── errors/
│       │   ├── events/
│       │   ├── logging/
│       │   ├── permissions/
│       │   ├── sync/
│       │   ├── tasks/
│       │   └── theme_design/
│       ├── modules/
│       │   ├── customers/
│       │   │   ├── domain/
│       │   │   ├── application/
│       │   │   ├── infrastructure/
│       │   │   └── presentation/
│       │   ├── projects/
│       │   ├── budgets/
│       │   ├── purchases/
│       │   ├── inventory/
│       │   ├── pcp/
│       │   ├── production/
│       │   ├── quality/
│       │   ├── shipping/
│       │   ├── installation/
│       │   ├── technical_support/
│       │   ├── finance/
│       │   ├── hr/
│       │   ├── fiscal/
│       │   └── bi/
│       └── shared/
│           ├── domain/
│           ├── application/
│           ├── infrastructure/
│           └── presentation/
├── api/
│   └── organizeg3_api/
├── migrations/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   ├── ui/
│   └── fixtures/
├── scripts/
├── resources/
├── packaging/
│   ├── pyinstaller/
│   └── windows/
└── docs/
```

Não criar uma pasta global de `models` contendo todo o ERP indefinidamente.

Cada módulo deverá possuir seus contratos e implementações.

---

# 33. Composition Root e injeção de dependência

A injeção será explícita.

Não utilizar framework de injeção na fundação.

O `composition_root.py` será responsável por montar:

- settings;
- engine;
- session factory;
- repositories;
- services;
- event bus;
- permission service;
- audit service;
- sync service;
- view models;
- pages.

Proibido instanciar repositórios aleatoriamente dentro de widgets.

---

# 34. Empacotamento Desktop

## 34.1 Ferramenta

```text
PyInstaller
```

Modo oficial:

```text
onedir
```

Não utilizar `onefile` como distribuição principal.

### Motivos

- inicialização mais rápida;
- menos extração temporária;
- melhor diagnóstico;
- atualização de arquivos mais controlável;
- menor complexidade com plugins Qt;
- melhor manutenção.

---

## 34.2 Spec

Deverá existir:

```text
packaging/pyinstaller/organizeg3.spec
```

O `.spec` será versionado.

Ele deverá incluir explicitamente:

- recursos;
- ícones;
- traduções Qt necessárias;
- plugins;
- templates;
- migrations;
- certificados públicos;
- arquivos do Design System.

---

## 34.3 Instalador

```text
Inno Setup
```

O instalador deverá:

- instalar em diretório adequado;
- criar atalhos;
- registrar versão;
- preservar dados do usuário;
- permitir atualização;
- não excluir banco local;
- não armazenar dados dentro de `Program Files`;
- incluir desinstalador;
- verificar arquitetura do Windows.

---

## 34.4 Assinatura

Executáveis e instaladores deverão ser assinados quando o certificado estiver disponível.

O sistema de atualização deverá validar:

- assinatura;
- hash;
- versão;
- canal;
- compatibilidade de banco.

---

# 35. Atualização do Desktop

Deverá existir um `UpdateService`.

Canais:

```text
stable
beta
development
```

Manifesto:

```json
{
  "version": "1.2.3",
  "channel": "stable",
  "minimum_schema_version": "20260805_01",
  "download": "...",
  "sha256": "...",
  "signature": "..."
}
```

O Desktop não poderá atualizar durante:

- backup;
- migration;
- sincronização;
- transação ativa;
- produção crítica configurada.

---

# 36. Backend e implantação

## 36.1 Container

A API será empacotada em:

```text
Docker
```

Sistema base:

```text
Linux
```

---

## 36.2 Processo

```text
Uvicorn
```

A quantidade de workers será definida pelo ambiente de implantação.

---

## 36.3 Serviços

Ambiente inicial de nuvem:

```text
Supabase para dados, autenticação e arquivos
Host Docker gerenciado para API
```

O host da API deverá ser substituível.

O código não poderá depender de APIs proprietárias do host.

---

## 36.4 Ambientes

```text
local
development
staging
production
```

Cada ambiente possuirá:

- banco separado;
- credenciais separadas;
- storage separado;
- URLs separadas;
- chaves separadas;
- logs separados.

Nunca utilizar banco de produção para testes.

---

# 37. CI/CD

## 37.1 Ferramenta

```text
GitHub Actions
```

---

## 37.2 Pipeline de Pull Request

```text
uv lock --check
ruff format --check .
ruff check .
mypy src
pytest
teste de migrations SQLite
teste de migrations PostgreSQL
build de importação do Desktop
```

---

## 37.3 Pipeline de release

```text
testes completos
build PyInstaller em Windows
teste de inicialização
geração do instalador
geração de hashes
assinatura
publicação do artefato
publicação do manifesto
tag Git
release notes
```

---

# 38. Git

Estratégia:

```text
main
develop durante transição, se necessário
feature/*
fix/*
release/*
```

Commits deverão ser pequenos e descrever intenção.

O Claude não deverá:

- reescrever histórico;
- executar force push;
- apagar branches;
- gerar commits gigantes sem motivo;
- incluir segredos;
- incluir banco real;
- incluir arquivos de clientes.

---

# 39. Documentação técnica

Ferramenta recomendada:

```text
MkDocs
Material for MkDocs
```

Documentos fonte permanecerão em Markdown.

Diagramas poderão utilizar:

```text
Mermaid
```

Código e documentação deverão evoluir juntos.

---

# 40. Dependências aprovadas por finalidade

## 40.1 Obrigatórias na fundação

```text
pyside6
sqlalchemy
alembic
pydantic
pydantic-settings
httpx
keyring
jinja2
reportlab
pillow
openpyxl
python-docx
```

---

## 40.2 API

```text
fastapi
uvicorn
psycopg
python-multipart quando necessário
```

---

## 40.3 Desenvolvimento

```text
pytest
pytest-qt
pytest-cov
pytest-mock
ruff
mypy
pip-audit
```

---

## 40.4 Fase posterior

```text
celery
redis
structlog
opentelemetry
sentry-sdk
matplotlib
```

Uma dependência de fase posterior não deverá ser adicionada apenas porque pode ser útil futuramente.

---

# 41. Tecnologias explicitamente não escolhidas

Não utilizar como stack principal:

```text
Django
Flask
Electron
Tauri para o Desktop inicial
PyQt
Flet
Kivy
Tkinter
MongoDB
Firebase como banco principal
Prisma no núcleo Python
GraphQL como API principal
Kafka
RabbitMQ na fundação
Elasticsearch na fundação
Kubernetes na fundação
Microserviços por módulo
LangChain no núcleo
LlamaIndex no núcleo
Airflow como workflow do ERP
Temporal na fundação
```

Isso não significa que essas tecnologias sejam ruins.

Significa que não fazem parte da decisão atual.

---

# 42. Exemplo de `pyproject.toml`

```toml
[project]
name = "organizeg3"
version = "0.1.0"
description = "OrganizeG3 ERP"
requires-python = ">=3.13,<3.14"
dependencies = [
    "pyside6>=6.10,<6.11",
    "sqlalchemy>=2.0,<2.1",
    "alembic>=1.19,<2",
    "pydantic>=2,<3",
    "pydantic-settings>=2,<3",
    "httpx>=0.28,<1",
    "keyring>=25,<26",
    "jinja2>=3.1,<4",
    "reportlab>=4,<5",
    "pillow>=11,<13",
    "openpyxl>=3.1,<4",
    "python-docx>=1.1,<2",
]

[dependency-groups]
api = [
    "fastapi>=0.115,<1",
    "uvicorn[standard]>=0.30,<1",
    "psycopg[binary,pool]>=3.2,<4",
    "python-multipart>=0.0.20,<1",
]
dev = [
    "pytest>=8,<10",
    "pytest-qt>=4.4,<5",
    "pytest-cov>=6,<8",
    "pytest-mock>=3.14,<4",
    "ruff>=0.12,<1",
    "mypy>=1.15,<3",
    "pip-audit>=2.8,<3",
]
jobs = [
    "celery>=5.5,<6",
    "redis>=6,<8",
]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.13"
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
check_untyped_defs = true
disallow_untyped_defs = true
no_implicit_optional = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
markers = [
    "unit: testes unitários",
    "integration: testes de integração",
    "database: testes de banco",
    "migration: testes de migration",
    "api: testes da API",
    "ui: testes PySide6",
    "sync: testes de sincronização",
    "slow: testes demorados",
]
```

As versões exatas deverão ser resolvidas e registradas no `uv.lock`.

O exemplo deverá ser adaptado ao workspace real sem apagar dependências legítimas existentes.

---

# 43. Ordem de adoção da stack

## Fase 0 — Diagnóstico

```text
Ler código atual
Executar aplicação
Executar testes existentes
Mapear imports
Mapear banco
Mapear migrations manuais
Mapear telas
Mapear integrações
Criar backup
```

Nenhuma refatoração estrutural antes do diagnóstico.

---

## Fase 1 — Fundação local

```text
Python 3.13
uv
pyproject.toml
uv.lock
Ruff
mypy
pytest
estrutura src
logging
settings
errors
SQLAlchemy 2
Alembic
SQLite
ThemeManager
Composition Root
```

---

## Fase 2 — Primeira fatia vertical

```text
Clientes
Domain
Application
Repository
Migration
UI
Permissões
Auditoria
Eventos
Testes
```

---

## Fase 3 — API e autenticação compartilhada

```text
FastAPI
Pydantic
Supabase Auth
PostgreSQL 17
psycopg 3
RLS
OpenAPI
ApiClient Desktop
```

---

## Fase 4 — Sincronização

```text
Outbox
Inbox
Versionamento
Idempotência
Conflitos
Retry
Cache local
Arquivos
```

---

## Fase 5 — Jobs compartilhados

```text
Redis
Celery
Relatórios
Notificações
Automações
Agendamentos
```

---

## Fase 6 — PWA

```text
React
TypeScript
Vite
TanStack Query
Zustand
IndexedDB
Service Worker
```

---

## Fase 7 — BI e IA

```text
Read Models
Agregações
Dashboards
AIProvider
Aprovações
Auditoria de IA
```

---

# 44. Instruções diretas para o Claude

## 44.1 Autoridade

Claude, este documento define a stack oficial.

Não escolha outra tecnologia porque parece mais simples ou moderna.

Quando encontrar código legado diferente:

1. identifique;
2. preserve o funcionamento;
3. proponha migração incremental;
4. explique o impacto;
5. não reescreva tudo;
6. siga a stack-alvo.

---

## 44.2 Antes de alterar código

Você deverá:

```text
1. Ler todos os arquivos fornecidos
2. Localizar o entrypoint
3. Localizar database.py
4. Localizar Base e SessionLocal
5. Localizar models
6. Localizar theme_design
7. Localizar autenticação
8. Localizar backup
9. Localizar encerramento da aplicação
10. Executar ou analisar os testes
11. Informar os impactos
```

---

## 44.3 Regras obrigatórias

Você não poderá:

- trocar PySide6 por outro framework;
- colocar SQLAlchemy em widgets;
- introduzir AsyncSession;
- acessar PostgreSQL diretamente pelo Desktop;
- gravar tokens em texto puro;
- adicionar Redis antes da fase autorizada;
- criar microserviços;
- criar uma segunda pasta de arquitetura;
- apagar migrations;
- alterar o banco sem migration;
- usar `float` para dinheiro;
- usar cores hardcoded;
- deixar imports faltando;
- devolver código com reticências;
- simplificar removendo funções existentes;
- criar dependência sem atualizar `pyproject.toml` e `uv.lock`;
- alterar major versions sem ADR;
- misturar entidades de domínio com ORM;
- criar regra de negócio na API route;
- criar regra de negócio no repository;
- executar tarefa longa na thread da UI.

---

## 44.4 Formato da resposta de código

Toda entrega deverá informar:

```text
Objetivo
Diagnóstico
Decisão técnica
Arquivos criados
Arquivos alterados
Migrations
Dependências
Código completo
Testes
Comandos para executar
Resultado esperado
Compatibilidade
Riscos
```

Quando for solicitado arquivo completo, entregar o arquivo inteiro.

---

## 44.5 Dependências

Antes de adicionar uma dependência, responder:

```text
Qual problema ela resolve?
Já existe solução aprovada?
É obrigatória agora?
Funciona com Python 3.13?
Funciona com PyInstaller?
Funciona no Windows?
Possui licença compatível?
Aumenta significativamente o executável?
Existe alternativa na Standard Library?
```

Se a dependência não for necessária, não adicioná-la.

---

## 44.6 Banco

Ao alterar persistência:

1. criar ou atualizar modelo de infraestrutura;
2. criar migration;
3. criar upgrade;
4. criar downgrade quando possível;
5. testar SQLite;
6. testar PostgreSQL;
7. preservar dados existentes;
8. atualizar repository;
9. atualizar testes;
10. documentar impacto de sincronização.

---

## 44.7 UI

Ao alterar uma tela:

1. preservar o Design System;
2. não bloquear a UI;
3. utilizar componentes compartilhados;
4. validar permissões;
5. tratar vazio, loading e erro;
6. manter acessibilidade;
7. fornecer tooltip em ícones;
8. não sobrepor cards;
9. não depender somente de drag and drop;
10. testar abertura e encerramento.

---

# 45. Critérios de conclusão

Uma funcionalidade somente estará pronta quando:

```text
Arquitetura respeitada
Stack respeitada
Domínio implementado
Caso de uso implementado
Persistência implementada
Migration criada
Permissão aplicada
Auditoria aplicada
Evento emitido
UI integrada
Erros tratados
Testes executados
Ruff aprovado
mypy aprovado
PyInstaller avaliado quando aplicável
Documentação atualizada
```

---

# 46. Comandos oficiais de validação

```bash
uv lock --check
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
uv run alembic upgrade head
uv run python -m organizeg3
```

Build Desktop:

```bash
uv run pyinstaller packaging/pyinstaller/organizeg3.spec --clean
```

API local:

```bash
uv run --group api uvicorn organizeg3_api.main:app --reload
```

Os caminhos deverão ser ajustados ao workspace real sem alterar o padrão.

---

# 47. Resumo definitivo para implementação

```text
Desktop:
Python 3.13 + PySide6 Qt Widgets

Arquitetura:
Modular Monolith + Clean Architecture + DDD

Persistência:
SQLAlchemy 2 + Alembic

Offline:
SQLite + Outbox/Inbox

Servidor:
FastAPI + Pydantic 2 + SQLAlchemy síncrono

Banco compartilhado:
PostgreSQL 17 no Supabase

Identidade:
Supabase Auth

Arquivos:
Supabase Storage

HTTP:
httpx

Jobs futuros:
Celery + Redis

Documentos:
Jinja2 + ReportLab + python-docx + openpyxl

Qualidade:
uv + Ruff + mypy

Testes:
pytest + pytest-qt

Empacotamento:
PyInstaller onedir + Inno Setup

PWA futura:
React 19 + TypeScript + Vite 8

CI:
GitHub Actions
```

---

# 48. Fontes oficiais verificadas para a decisão

A definição de versões e compatibilidade foi conferida, em 5 de agosto de 2026, nas documentações oficiais de:

- Python;
- Qt for Python/PySide6;
- SQLAlchemy;
- Alembic;
- FastAPI;
- Pydantic;
- PostgreSQL;
- Supabase;
- uv;
- Ruff;
- pytest;
- mypy;
- PyInstaller;
- React;
- Vite;
- TanStack Query.

Essas fontes servem para validar o estado das tecnologias na data deste documento.

A decisão de usar Python 3.13 e PostgreSQL 17 é deliberadamente conservadora e não representa simplesmente a escolha da versão mais recente disponível.

---

# 49. Próximo documento técnico recomendado

Após a aprovação deste Stack Tecnológico, o próximo documento deverá ser:

```text
ORGANIZEG3_PLANO_DE_IMPLEMENTACAO_E_ORDEM_DE_ARQUIVOS.md
```

Esse documento deverá informar, arquivo por arquivo:

- o que o Claude analisará;
- o que será preservado;
- o que será refatorado;
- a ordem de criação;
- a ordem das migrations;
- a primeira fatia vertical;
- os critérios de aceite de cada entrega.
