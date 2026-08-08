# ALTERAÇÕES DE ARQUITETURA UI/UX — 2026-08-08

## Decisão

A UI principal do OrganizeG3 passa a ser uma única aplicação React + TypeScript + Vite + PWA para desktop, notebook, tablet e celular.

Python permanece no backend, Application Layer, Domain, persistência, workers, integrações e automações.

## Arquivos alterados

1. AI_DEVELOPMENT_GUIDE.md
2. ESTRUTURA_ATUAL_DO_PROJETO_03.md
3. ORGANIZEG3_DESIGN_SYSTEM_VISUAL_OFICIAL.md
4. ORGANIZEG3_ESPECIFICACAO_MESTRA_UNICA.md
5. ORGANIZEG3_GALERIA_VISUAL.html
6. ORGANIZEG3_ORDEM_OFICIAL_DE_IMPLEMENTACAO.md
7. ORGANIZEG3_STACK_TECNOLOGICO_OFICIAL.md

## Arquivo novo

8. ADR-UI-001_FRONTEND_UNIFICADO_REACT_PWA.md

## Stack frontend oficial consolidada

- React 19
- TypeScript 5.x
- Vite
- React Router
- TanStack Query
- TanStack Table
- Zustand
- Zod
- Lucide React
- PWA Plugin / Workbox
- CSS Custom Properties + Design Tokens
- Vitest
- React Testing Library
- Playwright

## Regras consolidadas

- mesma base React para desktop e mobile;
- responsividade adaptativa;
- tabelas podem mudar de representação no mobile;
- `theme_design` é a única autoridade visual;
- Lucide React substitui iconografia baseada em arquivos baixados;
- PWA é cliente oficial, não etapa futura;
- PWA instalada é a distribuição desktop inicial;
- Tauri somente por ADR futuro e reutilizando a mesma UI;
- frontend não acessa SQLAlchemy nem banco diretamente;
- IndexedDB é a persistência local do navegador quando necessária;
- PySide6 permanece apenas como legado de transição, se ainda houver consumidores.
