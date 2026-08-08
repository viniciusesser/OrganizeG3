# Estrutura atual do projeto

> Revisão arquitetural de UI/UX — 2026-08-08.
>
> A estrutura-alvo de apresentação foi consolidada em `apps/web`, com React + TypeScript + Vite + PWA para desktop, notebook, tablet e celular. `apps/desktop` e `apps/pwa` deixam de representar clientes oficiais separados. Código PySide6 legado, se ainda existir fisicamente no workspace durante a migração, deve ser tratado como legado temporário e removido apenas após não possuir consumidores.


```text
PROGRAMA/
├── apps
│   ├── api
│   │   ├── src
│   │   │   └── organizeg3_api
│   │   │       ├── application
│   │   │       │   └── customer
│   │   │       │       ├── use_cases
│   │   │       │       │   ├── create_customer.py
│   │   │       │       │   └── list_customers.py
│   │   │       │       └── schemas.py
│   │   │       ├── core
│   │   │       │   ├── __init__.py
│   │   │       │   ├── base.py
│   │   │       │   ├── exceptions.py
│   │   │       │   └── logging.py
│   │   │       ├── domain
│   │   │       │   └── customer
│   │   │       │       ├── entity.py
│   │   │       │       └── repository.py
│   │   │       ├── infrastructure
│   │   │       │   ├── database
│   │   │       │   │   ├── models
│   │   │       │   │   │   └── __init__.py
│   │   │       │   │   ├── repositories
│   │   │       │   │   │   └── __init__.py
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── base.py
│   │   │       │   │   └── session.py
│   │   │       │   ├── http
│   │   │       │   │   ├── api
│   │   │       │   │   │   └── v1
│   │   │       │   │   │       └── customers.py
│   │   │       │   │   └── dependencies.py
│   │   │       │   ├── persistence
│   │   │       │   │   ├── models
│   │   │       │   │   │   └── customer.py
│   │   │       │   │   └── repositories
│   │   │       │   │       └── customer_repository.py
│   │   │       │   └── __init__.py
│   │   │       ├── middleware
│   │   │       │   ├── __init__.py
│   │   │       │   ├── correlation_id.py
│   │   │       │   └── error_handler.py
│   │   │       ├── __init__.py
│   │   │       ├── config.py
│   │   │       └── main.py
│   │   ├── tests
│   │   └── pyproject.toml
│   └── web
│       ├── src
│       │   ├── app
│       │   ├── components
│       │   ├── features
│       │   ├── layouts
│       │   ├── lib
│       │   └── theme_design
│       ├── public
│       ├── tests
│       ├── package.json
│       ├── tsconfig.json
│       └── vite.config.ts
├── database
│   ├── functions
│   ├── migrations
│   │   ├── versions
│   │   │   ├── 0439fdabfa05_add_customer_columns.py
│   │   │   ├── 62bc842a4881_baseline_legado.py
│   │   │   └── acc9bffaedbc_baseline.py
│   │   ├── env.py
│   │   ├── README
│   │   └── script.py.mako
│   ├── policies
│   └── seeds
├── docs
│   ├── architecure
│   │   ├── domain
│   │   │   ├── 001-domain-overview.md
│   │   │   ├── 002-aggregate-design.md
│   │   │   ├── 003-entity-design.md
│   │   │   ├── 004-value-objects.md
│   │   │   ├── 005-domain-events.md
│   │   │   ├── 006-domain-services.md
│   │   │   ├── 007-specifications.md
│   │   │   ├── 008-policies.md
│   │   │   ├── 009-factories.md
│   │   │   ├── 010-repositories.md
│   │   │   ├── 011-unit-of-work.md
│   │   │   ├── 012-application-layer.md
│   │   │   ├── 013-commands.md
│   │   │   ├── 014-command-handlers.md
│   │   │   ├── 015-queries.md
│   │   │   ├── 016-query-handlers.md
│   │   │   ├── 017-dtos.md
│   │   │   ├── 018-validators.md
│   │   │   ├── 019-mappers.md
│   │   │   └── 020-application-services.md
│   │   └── infrastructure
│   │       ├── 021-infrastructure-overview.md
│   │       ├── 022-database-architecture.md
│   │       ├── 023-sqlalchemy-models.md
│   │       ├── 024-repository-implementations.md
│   │       ├── 025-database-session.md
│   │       ├── 026-alembic-migrations.md
│   │       ├── 027-outbox-pattern.md
│   │       ├── 028-event-bus.md
│   │       ├── 029-background-workers.md
│   │       ├── 030-scheduler.md
│   │       ├── 031-storage-architecture.md
│   │       ├── 032-cache-architecture.md
│   │       ├── 033-logging-architecture.md
│   │       ├── 034-configuration-architecture.md
│   │       ├── 035-authentication-architecture.md
│   │       ├── 036-authorization-architecture.md
│   │       ├── 037-synchronization-architecture.md
│   │       ├── 038-sync-queue.md
│   │       ├── 039-delta-synchronization.md
│   │       ├── 040-conflict-resolution.md
│   │       ├── 041-snapshot-architecture.md
│   │       ├── 042-offline-first-strategy.md
│   │       ├── 043-observability-architecture.md
│   │       ├── 044-metrics-architecture.md
│   │       ├── 045-health-check-architecture.md
│   │       ├── 046-monitoring-architecture.md
│   │       ├── 047-distributed-tracing.md
│   │       ├── 048-audit-architecture.md
│   │       ├── 049-backup-architecture.md
│   │       ├── 050-disaster-recovery.md
│   │       └── infrastructure.zip
│   ├── functional
│   │   └── ORGANIZEG3_MASTER_FUNCTIONAL_MAP.md
│   ├── DOMAIN_ARCHITECTURE.md
│   ├── DOMAIN_COMMANDS_CATALOG.md
│   ├── DOMAIN_EVENTS_CATALOG.md
│   └── DOMAIN_RELATIONSHIPS.md
├── ENVIAR PARA IA
│   ├── AI_DEVELOPMENT_GUIDE.md
│   ├── ORGANIZEG3_DESIGN_SYSTEM_VISUAL_OFICIAL.md
│   ├── ORGANIZEG3_ESPECIFICACAO_MESTRA_UNICA.md
│   ├── ORGANIZEG3_GALERIA_VISUAL.html
│   ├── ORGANIZEG3_ORDEM_OFICIAL_DE_IMPLEMENTACAO.md
│   └── ORGANIZEG3_STACK_TECNOLOGICO_OFICIAL.md
├── packages
│   ├── application
│   │   ├── src
│   │   │   └── organizeg3_application
│   │   │       └── __init__.py
│   │   └── pyproject.toml
│   ├── contracts
│   │   ├── src
│   │   │   └── organizeg3_contracts
│   │   │       └── __init__.py
│   │   └── pyproject.toml
│   ├── domain
│   │   ├── src
│   │   │   └── organizeg3_domain
│   │   │       ├── __init__.py
│   │   │       ├── aggregate.py
│   │   │       ├── domain_event.py
│   │   │       ├── entity.py
│   │   │       └── value_object.py
│   │   └── pyproject.toml
│   └── shared
│       ├── src
│       │   └── organizeg3_shared
│       │       ├── __init__.py
│       │       ├── datetime.py
│       │       ├── errors.py
│       │       ├── ids.py
│       │       ├── pagination.py
│       │       ├── result.py
│       │       └── types.py
│       └── pyproject.toml
├── scripts
├── tests
├── theme_design
│   ├── assets
│   │   ├── illustrations
│   │   ├── images
│   │   ├── logos
│   │   └── placeholders
│   ├── components
│   │   ├── __init__.py
│   │   ├── buttons.py
│   │   ├── cards.py
│   │   ├── dialogs.py
│   │   ├── feedback.py
│   │   ├── inputs.py
│   │   ├── kanban.py
│   │   ├── navigation.py
│   │   └── tables.py
│   ├── icons
│   │   ├── __init__.py
│   │   ├── aliases.py
│   │   └── registry.py
│   ├── themes
│   │   ├── __init__.py
│   │   └── dark.py
│   ├── tokens
│   │   ├── __init__.py
│   │   ├── animations.py
│   │   ├── breakpoints.py
│   │   ├── colors.py
│   │   ├── radius.py
│   │   ├── shadows.py
│   │   ├── sizes.py
│   │   ├── spacing.py
│   │   └── typography.py
│   ├── __init__.py
│   ├── README.md
│   └── theme.py
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── ESTRUTURA_ATUAL_DO_PROJETO.md
├── ESTRUTURA_ATUAL_DO_PROJETO_02.txt
├── pyproject.toml
├── README.md
└── requirements.txt
```


---

## Decisão de frontend vigente

```text
apps/web
    ↓ HTTPS
apps/api
    ↓
Application Layer
    ↓
Domain
    ↓
Infrastructure
```

Referência normativa:

```text
ADR-UI-001_FRONTEND_UNIFICADO_REACT_PWA.md
```

Regras:

- uma única base React para desktop e mobile;
- responsividade adaptativa;
- `theme_design` centralizado no frontend;
- sem valores visuais hardcoded em páginas;
- TanStack Table para tabelas de dados;
- Lucide React para iconografia;
- TanStack Query para estado de servidor;
- Zustand apenas para estado local de interface;
- PWA como forma inicial de instalação desktop;
- Tauri apenas por ADR futuro se houver necessidade nativa real.
