# OrganizeG3 — Roadmap Atual

**Status:** Vigente  
**Atualizado em:** 2026-08-12
**Objetivo:** Registrar o estado atual do desenvolvimento e a próxima sequência operacional.

---

# 1. Estado macro

```text
PHASE 01 — PLATFORM FOUNDATION             100% ✅
PHASE 02 — CORE DOMAIN                     100% ✅
PHASE 03 — APPLICATION & API               100% ✅
PHASE 04 — WEB / PWA INTEGRATION           100% ✅
PHASE 05 — UX/UI                           0% — PRÓXIMO
PHASE 06 — MODULE IMPLEMENTATION           0%
PHASE 07 — QUALITY & SECURITY              0%
PHASE 08 — RELEASE ENGINEERING             0%
PHASE 09 — DISTRIBUTION                    0%
```

**Progresso macro:** 44% — 4 de 9 fases concluídas.

O percentual macro considera as nove fases principais com o mesmo peso. O progresso interno de cada fase permanece registrado separadamente.

---

# 2. Phase 04 — Web / PWA Integration

```text
04.1 Frontend Foundation                   100% ✅
04.2 Theme Design Foundation               100% ✅
04.3 App Shell                             100% ✅
04.4 Authentication Integration            100% ✅
04.5 First Real Screens                    100% ✅
04.6 Shared UI Patterns                    100% ✅
04.7 PWA Integration                       100% ✅
04.8 Integration Gates                     100% ✅
```

**Status da Phase 04:** 100% — 8 de 8 blocos concluídos.

---

# 3. Escopo concluído na Phase 04

## 3.1 Fundação frontend

- aplicação React/PWA estruturada;
- configuração de ambiente centralizada;
- comunicação autenticada com a API;
- tratamento comum de erros HTTP;
- navegação desktop e móvel;
- rotas públicas e protegidas;
- contexto da empresa ativa.

## 3.2 Autenticação e autorização

- autenticação integrada ao Supabase Auth;
- descoberta dos tenants do usuário;
- seleção e persistência do tenant ativo;
- consulta da identidade autenticada;
- proteção das rotas do aplicativo;
- navegação orientada por permissões;
- tratamento de sessão expirada e acesso indisponível.

## 3.3 Primeiras telas reais

- [x] 04.5.1 — Clientes
- [x] 04.5.2 — Fornecedores
- [x] 04.5.3 — Materiais
- [x] 04.5.4 — Serviços
- [x] 04.5.5 — Máquinas
- [x] 04.5.6 — Marcas
- [x] 04.5.7 — Funcionários
- [x] 04.5.8 — Empresa
- [x] 04.5.9 — Filiais

As telas validaram, quando aplicável:

- listagem real;
- paginação;
- pesquisa e filtros;
- loading, erro e estado vazio;
- criação e edição;
- visualização;
- ativação e inativação;
- permissões;
- feedback;
- responsividade.

## 3.4 Padrões compartilhados

- layouts de página;
- tabelas responsivas;
- paginação;
- filtros;
- diálogos;
- estados de loading, erro e vazio;
- ações protegidas por permissão;
- estilos centralizados no `theme_design`.

## 3.5 PWA

- manifesto reconhecido pelo navegador;
- identidade e ícones instaláveis;
- modo `standalone`;
- service worker registrado e ativo;
- shell carregado pelo cache;
- indicador `Online` e `Offline`;
- comportamento offline validado;
- dados autenticados não apresentados como atualizados durante falha de rede.

---

# 4. Gates finais da Phase 04

## 4.1 API

- [x] Compilação aprovada
- [x] Ruff aprovado
- [x] mypy aprovado em 258 arquivos
- [x] 1.390 testes aprovados
- [x] 21 revisões Alembic reconhecidas
- [x] Uma única head Alembic

## 4.2 PWA

- [x] Lint aprovado
- [x] TypeScript aprovado
- [x] 39 arquivos de teste aprovados
- [x] 218 testes aprovados
- [x] Build aprovado
- [x] Manifesto, service worker e Workbox gerados

## 4.3 Banco e integração real

- [x] Código na revisão `b7c2a91d4e6f`
- [x] PostgreSQL na revisão `b7c2a91d4e6f`
- [x] `/api/v1/auth/tenants` respondendo `200`
- [x] `/api/v1/auth/me` respondendo `200`
- [x] `/health` respondendo `200`
- [x] `/api/v1/customers` respondendo `200`
- [x] Cliente real carregado pelo PWA a partir do tenant autenticado

---

# 5. Regras arquiteturais preservadas

## 5.1 Design system

Toda definição visual permanece centralizada em:

```text
theme_design
```

Nenhuma tela ou componente deve introduzir valores visuais hardcoded.

## 5.2 Multitenancy

- toda operação protegida deve considerar o tenant ativo;
- o usuário acessa somente tenants autorizados;
- permissões devem ser verificadas no backend e refletidas no frontend;
- falhas de autenticação ou tenant não podem expor dados.

## 5.3 Qualidade

Nenhum bloco será marcado como concluído sem os gates correspondentes.

Quando aplicável:

- pytest;
- Ruff;
- mypy;
- testes de API e integração;
- Vitest;
- lint;
- TypeScript;
- build;
- validação manual;
- validação responsiva;
- validação PWA.

## 5.4 Migração do legado

A migração definitiva do legado ainda não deve ser executada.

Para cada módulo estabilizado:

```text
modelo novo
↓
comparação com legado
↓
mapa de migração
↓
dry-run futuro
```

---

# 6. Próxima etapa oficial

A próxima etapa macro é:

```text
PHASE 05 — UX/UI
```

A fundação visual começou antecipadamente na Phase 04. A Phase 05 não deve refazer o design system sem necessidade comprovada.

---

# 7. Objetivos da Phase 05

A Phase 05 deverá consolidar:

- arquitetura da informação;
- padrões de navegação;
- experiência dos módulos complexos;
- acessibilidade;
- feedback;
- consistência;
- fluxos avançados;
- estados responsivos;
- coerência entre desktop e dispositivos móveis.

O primeiro passo será decompor a Phase 05 em blocos verificáveis antes de alterar código.

---

# 8. Próxima sequência operacional

1. Registrar a conclusão integral da Phase 04.
2. Revisar e versionar os documentos oficiais.
3. Definir a decomposição interna da Phase 05.
4. Auditar arquitetura da informação e navegação.
5. Auditar acessibilidade, contraste e feedback.
6. Mapear fluxos complexos e estados responsivos.
7. Implementar uma fatia por vez.
8. Executar os gates correspondentes a cada fatia.

---

# 9. Referência histórica da autenticação

Commit de referência da conclusão da integração de autenticação:

```text
90c455b
feat: implement authentication integration
```

Esse commit permanece como referência histórica da Phase 04.4 e não representa, isoladamente, o fechamento integral da Phase 04.

---

# 10. Fonte de verdade

Para progresso:

```text
ORGANIZEG3_ROADMAP_CURRENT.md
```

Para ordem de execução:

```text
ORGANIZEG3_IMPLEMENTATION_ORDER.md
```

Para escopo funcional:

```text
ORGANIZEG3_FUNCTIONAL_MAP.md
```

Para detalhes especializados:

```text
*_SPEC.md
DOCUMENT_TAG_CATALOG.md
```

Esses documentos possuem responsabilidades diferentes e não devem competir entre si.
