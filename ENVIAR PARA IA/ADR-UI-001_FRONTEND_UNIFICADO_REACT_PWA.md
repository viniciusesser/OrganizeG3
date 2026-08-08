# ADR-UI-001 — Frontend unificado React/PWA

| Propriedade | Valor |
|---|---|
| Status | Aprovado |
| Data | 2026-08-08 |
| Escopo | UI/UX, frontend, distribuição desktop/mobile |
| Substitui | PySide6/Qt Widgets como UI principal e a separação Desktop + PWA |
| Preserva | FastAPI, Application Layer, Domain, SQLAlchemy, Alembic, PostgreSQL/Supabase |

## 1. Contexto

A interface principal do OrganizeG3 era planejada como Desktop Windows em PySide6/Qt Widgets, com uma PWA React construída posteriormente.

Essa estratégia criaria duas implementações visuais independentes e aumentaria o custo de manutenção. Também dificultaria garantir comportamento consistente de tabelas, ícones, densidade e responsividade entre resoluções, escalas de DPI, notebooks, tablets e celulares.

## 2. Decisão

O OrganizeG3 adotará um único frontend oficial:

```text
React 19
TypeScript
Vite
PWA
```

A mesma aplicação será utilizada em:

```text
Desktop
Notebook
Tablet
Celular
```

O frontend deverá ser responsivo e adaptativo. A mesma informação pode usar representações diferentes conforme o espaço disponível; por exemplo, uma grade tabular no desktop poderá virar lista ou cards no mobile.

Python deixa de ser tecnologia de apresentação. Python permanece no backend, domínio, aplicação, persistência, workers, integrações e automações.

## 3. Stack de frontend

```text
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
CSS Custom Properties + Design Tokens
Vitest
React Testing Library
Playwright
```

Dependências adicionais exigem justificativa e atualização do Stack Tecnológico Oficial.

## 4. Design System

Toda definição visual continua centralizada em `theme_design`.

É proibido espalhar pelas páginas valores visuais independentes para:

- cores;
- tipografia;
- espaçamento;
- tamanhos;
- breakpoints;
- bordas;
- raios;
- sombras;
- z-index;
- ícones;
- estados;
- densidade;
- estilos de componentes.

Componentes de feature devem consumir tokens e componentes compartilhados.

## 5. Responsividade

Breakpoints oficiais:

```text
sm   640 px
md   768 px
lg   1024 px
xl   1280 px
2xl  1536 px
```

As regras são adaptativas, não apenas redimensionáveis:

- tabelas largas podem ocultar colunas secundárias ou mudar para lista/card;
- sidebar pode virar drawer;
- dialogs extensos podem virar página ou tela cheia;
- filtros podem virar painel;
- ações primárias devem permanecer acessíveis;
- touch targets devem respeitar ergonomia móvel;
- nenhuma tela poderá depender de largura fixa absoluta para funcionar.

## 6. Tabelas e dados densos

`TanStack Table` será a base oficial para tabelas de dados.

As páginas devem definir explicitamente:

- colunas essenciais;
- colunas opcionais;
- prioridade por breakpoint;
- ordenação;
- filtros;
- paginação;
- seleção;
- ações de linha;
- estratégia mobile.

Virtualização poderá ser adicionada quando volume real justificar.

## 7. Iconografia

`Lucide React` será a biblioteca padrão de ícones da aplicação.

Os ícones serão SVG vetoriais, dimensionados por tokens de `theme_design`.

Não usar emoji como ícone de interface.

Ícones sem texto devem possuir nome acessível e tooltip quando necessário.

## 8. Comunicação com backend

O frontend não acessará SQLAlchemy nem tabelas PostgreSQL diretamente para regras de negócio.

Fluxo oficial:

```text
React/PWA
   ↓ HTTPS
FastAPI
   ↓
Application Layer
   ↓
Domain
   ↓
Infrastructure
```

Supabase Auth e Storage poderão ser utilizados conforme contratos oficiais, sem contornar casos de uso de negócio.

## 9. Offline

A aplicação PWA deverá possuir cache de shell e estratégia offline controlada.

Quando persistência local de dados de negócio for necessária no navegador, utilizar IndexedDB por um adapter próprio. SQLite não será uma dependência do frontend web.

Sincronização offline de escrita somente será ativada por fluxos explicitamente projetados para idempotência, conflito e auditoria.

## 10. Desktop

A instalação desktop inicial será a própria PWA instalada pelo navegador/sistema operacional compatível.

Tauri poderá ser adotado futuramente somente por ADR caso seja necessário acesso nativo a recursos como:

- impressão especializada;
- filesystem local controlado;
- dispositivos;
- atualização nativa;
- integrações específicas do Windows.

A adoção de Tauri não poderá criar uma segunda UI.

## 11. Consequências

### Positivas

- uma única UI para desktop e mobile;
- menor duplicação;
- responsividade nativa da plataforma web;
- SVG consistente;
- componentes compartilhados;
- evolução mais rápida da experiência;
- possibilidade de instalação como PWA.

### Custos

- criação da fundação frontend TypeScript;
- migração de qualquer UI PySide6 legada;
- redefinição da estratégia offline que dependia de SQLite local;
- novos testes de frontend e E2E.

## 12. Regra de precedência

Este ADR prevalece sobre referências anteriores que determinem PySide6/Qt Widgets como interface principal, PWA como cliente futuro separado, `pytest-qt` como teste principal de UI ou PyInstaller/Inno Setup como empacotamento da interface principal.
