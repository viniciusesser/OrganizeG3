# ORGANIZEG3 — STACK TECNOLÓGICO OFICIAL

> Documento normativo para implementação, manutenção, testes, empacotamento e evolução técnica do OrganizeG3.

---

| Propriedade | Valor |
|---|---|
| Documento | `ORGANIZEG3_STACK_TECNOLOGICO_OFICIAL.md` |
| Versão | `1.1.0` |
| Data da decisão | 2026-08-08 |
| Status | Stack oficial aprovada para implementação |
| Autoridade | Complementar à Especificação Mestra Única |
| Aplicação de interface | React/PWA unificado para desktop e mobile |
| Arquitetura-alvo | React/PWA + FastAPI + PostgreSQL/Supabase |
| Idioma da documentação | Português |
| Idioma do código | Inglês |
| Fuso de exibição padrão | America/Sao_Paulo |
| Armazenamento de instantes | UTC |


> Decisão vinculante de UI/UX: `ADR-UI-001_FRONTEND_UNIFICADO_REACT_PWA.md`.
> Este ADR substitui PySide6/Qt Widgets como interface principal e elimina a separação entre cliente Desktop e PWA.

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
Backend
Python 3.13
FastAPI
Pydantic 2
SQLAlchemy 2
Alembic
PostgreSQL 17 no Supabase

Frontend
React 19
TypeScript 5.x
Vite
React Router
TanStack Query
TanStack Table
Zustand
Zod
Lucide React
PWA Plugin / Workbox

Arquitetura
Modular Monolith
Clean Architecture
Domain-Driven Design
CQRS leve
Event-driven interno

Autenticação
Supabase Auth

Arquivos em nuvem
Supabase Storage

Frontend offline controlado
Service Worker + IndexedDB adapter quando aplicável

Dependências Python
uv + pyproject.toml + uv.lock

Dependências Frontend
package manager definido no workspace + lockfile obrigatório

Qualidade Python
Ruff + mypy + pytest

Qualidade Frontend
ESLint + TypeScript + Vitest + React Testing Library + Playwright

Backend
Container Docker Linux

Desktop
PWA instalada

Mobile
Mesma PWA responsiva

Desktop nativo futuro
Tauri somente por ADR e sem segunda UI

CI
GitHub Actions
```
# 4. Decisões fundamentais

## 4.1 O produto de interface é único e responsivo

A aplicação visual oficial será:

```text
OrganizeG3 Web App
React 19 + TypeScript + Vite
PWA instalável
```

A mesma base será utilizada em:

```text
Desktop
Notebook
Tablet
Celular
```

Não existirão duas implementações funcionais separadas chamadas “Desktop” e “PWA”.

A interface deverá adaptar representação, densidade e navegação ao espaço disponível sem duplicar regras de negócio.
## 4.2 Python é a linguagem oficial do backend

Python 3.13 é a linguagem oficial para:

- API;
- Application Layer;
- Domain;
- persistência;
- workers;
- integrações;
- automações;
- ferramentas de backend.

TypeScript é a linguagem oficial do frontend.

Versão-alvo do backend:

```text
Python 3.13.x
```

Restrição:

```toml
requires-python = ">=3.13,<3.14"
```

A evolução da versão Python deve seguir testes completos e ADR quando alterar a baseline.
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

- páginas React;
- layouts responsivos;
- navegação;
- formulários;
- tabelas;
- filtros;
- dialogs/sheets;
- feedback visual;
- acessibilidade;
- apresentação de erros;
- integração HTTP com a API.

Tecnologias:

```text
React 19
TypeScript
Vite
React Router
TanStack Query
TanStack Table
Zustand
Zod
Lucide React
PWA Plugin / Workbox
CSS Custom Properties
Design Tokens
```

Presentation não poderá importar modelos ORM, SQLAlchemy ou repositórios internos.

Presentation não contém regra de negócio.
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

Application não poderá depender de React, PySide6 ou qualquer framework de apresentação.

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

## 8.1 Núcleo Python

```text
Python >=3.13,<3.14
SQLAlchemy 2
Alembic
Pydantic 2
pydantic-settings
FastAPI
psycopg 3
httpx
structlog
```

A versão exata será definida pelo lockfile Python.
## 8.2 Dependências Python principais

```text
SQLAlchemy >=2.0,<2.1
Alembic >=1.19,<2
Pydantic >=2,<3
pydantic-settings >=2,<3
httpx >=0.28,<1
Jinja2 >=3.1,<4
ReportLab >=4,<5
Pillow >=11,<13
openpyxl >=3.1,<4
python-docx >=1.1,<2
```

PySide6 não é dependência obrigatória da arquitetura-alvo. Se permanecer no repositório durante a transição, será tratado como legado até a remoção segura.
# 9. Frontend — React/PWA

## 9.1 Framework

```text
React 19
TypeScript 5.x
Vite
```

Não utilizar outra framework principal de frontend sem ADR.

## 9.2 Padrão de aplicação

```text
Route
Page
Feature Components
Shared Components
API Client
Application API
```

Páginas não acessam banco.

## 9.3 Estado

```text
TanStack Query = estado do servidor
Zustand = estado local de interface
React state = estado local simples de componente
```

Não duplicar entidades de servidor no Zustand.

## 9.4 Tabelas

TanStack Table é a base oficial.

Cada tabela deve definir:

- colunas essenciais;
- colunas opcionais;
- comportamento por breakpoint;
- filtros;
- ordenação;
- paginação;
- ações;
- estratégia mobile.

Tabela não é obrigada a permanecer tabela em telas estreitas.

## 9.5 Design System

Toda aparência vem de `theme_design`.

É proibido hardcode visual em páginas e componentes de feature.

## 9.6 Iconografia

Lucide React é a biblioteca oficial.

Ícones são SVG e usam tamanhos/tokens do Design System.

## 9.7 Responsividade

Breakpoints:

```text
sm 640
md 768
lg 1024
xl 1280
2xl 1536
```

Layout deve ser adaptativo, sem sobreposição e sem depender de largura fixa absoluta.

## 9.8 Desktop

A forma inicial de instalação desktop é a PWA.

Tauri poderá ser adotado somente por ADR futuro se houver requisito nativo comprovado, reutilizando a mesma UI React.
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

# 13. Persistência local do frontend

## 13.1 Regra geral

O frontend web não utiliza SQLite diretamente.

Persistência local de dados do navegador, quando necessária, utilizará:

```text
IndexedDB
Service Worker Cache
```

através de adapters próprios.

## 13.2 Offline

Cache de app shell é permitido.

Leitura offline pode ser implementada por feature.

Escrita offline somente poderá ser habilitada quando o fluxo possuir:

- idempotência;
- versionamento;
- detecção de conflito;
- retry;
- auditoria;
- reconciliação.

## 13.3 SQLite

SQLite poderá continuar existindo em ferramentas, migração de legado ou processos Python específicos, mas não é banco local do frontend React/PWA.
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

O frontend não deverá utilizar PostgREST diretamente para executar regras críticas.

O frontend não deverá gravar diretamente em tabelas compartilhadas.

O caminho oficial será:

```text
React/PWA
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

## 16.6 Cliente Frontend

O frontend utilizará um API Client central.

Responsabilidades:

- base URL;
- autenticação;
- correlation id;
- device id quando aplicável;
- parsing padronizado;
- tratamento de erros HTTP;
- cancelamento;
- refresh de sessão;
- tipagem dos contratos.

Páginas não executam `fetch` disperso quando houver client/serviço oficial.
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
Frontend mantém sessão conforme estratégia de autenticação aprovada
    ↓
API valida JWT
    ↓
API resolve Tenant, usuário, perfis e permissões
```

---

## 17.3 Sessão no frontend

Tokens e sessão devem seguir a estratégia suportada pelo Supabase Auth e pelo modelo de segurança aprovado.

Não persistir segredos em código, variáveis globais ou logs.

O armazenamento no navegador deverá considerar XSS, expiração e rotação.

Qualquer uso de cookies HttpOnly ou estratégia alternativa deverá ser documentado na arquitetura de autenticação.
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

# 18. Offline e sincronização

## 18.1 Estratégia

O frontend é PWA e pode operar com capacidades offline controladas.

Não assumir que toda feature é offline-first.

## 18.2 Persistência local

```text
IndexedDB adapter
Service Worker cache
```

## 18.3 Fonte oficial

PostgreSQL/Supabase permanece a fonte compartilhada oficial.

## 18.4 Escrita offline

Somente features explicitamente aprovadas poderão enfileirar comandos offline.

Requisitos:

- command id;
- idempotency key;
- tenant context;
- actor context;
- device context;
- versionamento;
- conflito;
- retry;
- auditoria.

## 18.5 Conflitos

Conflitos não podem ser resolvidos silenciosamente quando houver risco de perda de informação.
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
serviços síncronos/assíncronos controlados na API
workers externos quando a tarefa exigir durabilidade
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

## 23.1 Frontend

Gráficos devem ser renderizados com biblioteca React aprovada e consumir tokens do Design System.

A escolha da biblioteca de gráficos deverá ser registrada quando a primeira tela analítica for implementada.

Não usar imagens estáticas quando o gráfico precisar ser responsivo ou interativo.
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

## 25.1 Frontend

Erros de frontend devem ser observáveis sem expor dados sensíveis.

O frontend deverá possuir:

- Error Boundary;
- correlation id;
- captura de falhas de API;
- logs controlados em desenvolvimento;
- integração futura com ferramenta de monitoramento aprovada.
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

# 28. PWA oficial

## 28.1 Status

A PWA não é futura nem um segundo cliente.

Ela é a forma oficial da aplicação React para desktop e mobile.

## 28.2 Stack

```text
TypeScript
React 19
Vite
TanStack Query
TanStack Table
Zustand
React Router
Zod
Lucide React
PWA Plugin / Workbox
CSS variables e Design Tokens
```

## 28.3 Comunicação

A PWA utiliza a API FastAPI.

Não acessa tabelas PostgreSQL/Supabase diretamente para executar comandos de negócio.

## 28.4 Estado

```text
TanStack Query = estado do servidor
Zustand = estado local da interface
```

## 28.5 Design System

Todos os breakpoints, tamanhos, cores, ícones, tipografia, espaçamentos e estados vêm de `theme_design`.

## 28.6 Offline

```text
Service Worker = app shell/cache
IndexedDB = persistência local quando necessária
```

Fila offline de comandos somente para fluxos aprovados.
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

Ferramentas oficiais:

```text
Vitest
React Testing Library
Playwright
```

Testar:

- renderização;
- estados;
- acessibilidade básica;
- responsividade crítica;
- fluxos E2E;
- permissões visuais sem substituir validação do backend.

`pytest-qt` não faz parte da arquitetura-alvo.
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
PROGRAMA/
├── apps/
│   ├── api/
│   │   ├── src/
│   │   └── tests/
│   └── web/
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   ├── features/
│       │   ├── layouts/
│       │   ├── lib/
│       │   └── theme_design/
│       ├── public/
│       ├── tests/
│       ├── package.json
│       ├── tsconfig.json
│       └── vite.config.ts
├── database/
├── docs/
├── packages/
├── scripts/
└── ADR-UI-001_FRONTEND_UNIFICADO_REACT_PWA.md
```

`apps/desktop` e `apps/pwa` não representam mais clientes oficiais separados.

Código legado pode permanecer temporariamente até a migração e remoção segura.
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

# 34. Build e distribuição do frontend

## 34.1 Build

```text
Vite production build
PWA manifest
Service Worker
asset hashing
```

## 34.2 Desktop

A instalação desktop inicial será a PWA instalada.

## 34.3 Tauri

Tauri não é necessário para a primeira entrega React.

Só poderá ser introduzido mediante ADR quando existir requisito nativo comprovado.

## 34.4 Regra

Mesmo com wrapper nativo futuro, não criar uma segunda UI.
# 35. Atualização do frontend

A atualização da aplicação ocorrerá pelo mecanismo de deploy web/PWA.

Regras:

- assets versionados;
- service worker com política explícita;
- atualização não pode corromper estado local;
- mudanças incompatíveis no IndexedDB precisam de migração;
- rollback de deploy deve ser possível;
- usuário deve receber feedback quando uma atualização exigir reload.
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
build do frontend React/PWA
```

---

## 37.3 Pipeline de release

```text
Backend tests
Frontend lint
Frontend typecheck
Frontend unit tests
Frontend build
Playwright smoke test
PWA validation
Container build da API
Deploy staging
migrations controladas
Deploy frontend
smoke tests
release metadata
```
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

## 40.1 Backend obrigatório

```text
sqlalchemy
alembic
pydantic
pydantic-settings
fastapi
uvicorn
psycopg
httpx
structlog
```

## 40.2 Frontend obrigatório

```text
react
react-dom
typescript
vite
react-router
@tanstack/react-query
@tanstack/react-table
zustand
zod
lucide-react
PWA Plugin / Workbox
```

## 40.3 Desenvolvimento frontend

```text
eslint
vitest
@testing-library/react
@testing-library/jest-dom
playwright
```

Dependências visuais ou de componentes adicionais devem ser justificadas antes da adoção.
# 41. Tecnologias explicitamente não escolhidas

Não utilizar como stack principal sem ADR:

```text
PySide6/Qt Widgets para novas telas
PyQt
Flet
Kivy
Tkinter
Electron
Next.js
Angular
Vue
Svelte
GraphQL como API principal
MongoDB como banco principal
Firebase como banco principal
Prisma no núcleo Python
Kafka na fundação
RabbitMQ na fundação
Elasticsearch na fundação
Kubernetes na fundação
Microserviços por módulo
```

Tauri é permitido somente por ADR futuro para encapsular a mesma aplicação React quando houver necessidade nativa real.
# 42. Exemplos de manifests de dependência

```toml
[project]
name = "organizeg3"
version = "0.1.0"
description = "OrganizeG3 ERP"
requires-python = ">=3.13,<3.14"
dependencies = [
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
    "ui: testes de integração de apresentação quando houver legado",
    "sync: testes de sincronização",
    "slow: testes demorados",
]
```

As versões exatas deverão ser resolvidas e registradas no `uv.lock`.

O exemplo deverá ser adaptado ao workspace real sem apagar dependências legítimas existentes.

---


## Frontend

O frontend possui `package.json` próprio em `apps/web`.

As versões exatas devem ser travadas pelo lockfile do workspace frontend.

Dependências mínimas:

```text
react
react-dom
typescript
vite
react-router
@tanstack/react-query
@tanstack/react-table
zustand
zod
lucide-react
vitest
@testing-library/react
playwright
```

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
API Client frontend
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

## Fase 6 — PWA hardening

```text
manifest
service worker
IndexedDB
offline controlado
installability
push
mobile ergonomics
device tests
```

A PWA já existe desde a fundação do frontend; esta fase apenas amadurece capacidades específicas.
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

- colocar SQLAlchemy em componentes React;
- introduzir AsyncSession;
- acessar PostgreSQL diretamente pelo frontend;
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
Funciona com o runtime/backend ou browser alvo?
Funciona no Windows?
Possui licença compatível?
Aumenta significativamente o bundle ou imagem?
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

Ao alterar frontend:

1. ler o Design System;
2. usar `theme_design`;
3. não hardcodar valores visuais;
4. verificar desktop, tablet e mobile;
5. definir comportamento responsivo das tabelas;
6. usar Lucide React;
7. usar TanStack Query para server state;
8. não colocar regra de negócio em componentes;
9. não acessar banco diretamente;
10. executar testes unitários e E2E aplicáveis.
# 45. Critérios de conclusão

Uma funcionalidade somente estará pronta quando:

```text
Arquitetura respeitada
Stack respeitada
Domínio implementado quando aplicável
Caso de uso implementado
Persistência implementada quando aplicável
Migration criada quando aplicável
Permissão aplicada
Auditoria aplicada
Evento emitido quando aplicável
API integrada
UI React integrada
Responsividade validada
Erros tratados
Testes backend executados
Testes frontend executados
Ruff aprovado
mypy aprovado
TypeScript aprovado
lint frontend aprovado
build Vite aprovado
E2E crítico aprovado
Documentação atualizada
```
# 46. Comandos oficiais de validação

Backend:

```bash
python -m ruff check apps/api/src apps/api/tests
python -m mypy apps/api/src scripts
python -m pytest
python -m alembic upgrade head
python -m alembic check
```

API local:

```bash
uvicorn organizeg3_api.main:app --reload
```

Frontend, usando o package manager oficial do workspace:

```bash
lint
typecheck
test
build
playwright test
```

Os scripts exatos deverão ser definidos em `apps/web/package.json` e executados pelo lockfile oficial.
# 47. Resumo definitivo para implementação

```text
Frontend:
React 19 + TypeScript + Vite + PWA

Desktop:
mesma PWA instalada

Mobile:
mesma PWA responsiva

UI state:
Zustand

Server state:
TanStack Query

Tabelas:
TanStack Table

Validação frontend:
Zod

Ícones:
Lucide React

Design:
theme_design + Design Tokens

Backend:
Python 3.13 + FastAPI + Pydantic 2

Arquitetura:
Modular Monolith + Clean Architecture + DDD

Persistência:
SQLAlchemy 2 + Alembic

Banco compartilhado:
PostgreSQL 17 no Supabase

Offline frontend:
Service Worker + IndexedDB quando aplicável

Identidade:
Supabase Auth

Arquivos:
Supabase Storage

Qualidade backend:
Ruff + mypy + pytest

Qualidade frontend:
ESLint + TypeScript + Vitest + React Testing Library + Playwright

Desktop nativo futuro:
Tauri somente por ADR e reutilizando a mesma UI
```
# 48. Fontes oficiais verificadas para a decisão

A definição de versões e compatibilidade foi conferida, em 5 de agosto de 2026, nas documentações oficiais de:

- Python;
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
