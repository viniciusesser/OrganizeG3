# OrganizeG3 — Roadmap Atual

**Status:** Vigente  
**Atualizado em:** 2026-08-10  
**Objetivo:** Registrar o estado atual do desenvolvimento e a próxima sequência operacional.

---

# 1. Estado macro

```text
PHASE 01 — PLATFORM FOUNDATION             100% ✅
PHASE 02 — CORE DOMAIN                    100% ✅
PHASE 03 — APPLICATION & API              100% ✅
PHASE 04 — WEB / PWA INTEGRATION          EM ANDAMENTO 🚧
PHASE 05 — UX/UI                          0%
PHASE 06 — MODULE IMPLEMENTATION          0%
PHASE 07 — QUALITY & SECURITY             0%
PHASE 08 — RELEASE ENGINEERING            0%
PHASE 09 — DISTRIBUTION                   0%
2. Phase 04 — Web / PWA Integration
04.1 Frontend Foundation                  100% ✅
04.2 Theme Design Foundation              100% ✅
04.3 App Shell                            100% ✅
04.4 Authentication Integration           100% ✅
04.5 First Real Screens                   PRÓXIMO
04.6 Shared UI Patterns                   PENDENTE
04.7 PWA Integration                      PENDENTE
04.8 Integration Gates                    PENDENTE

A Phase 04 está funcionalmente na metade de seus oito blocos principais.

3. Authentication Integration

Concluído:

04.4A — Auth Infrastructure               ✅
04.4B1 — Tenant Discovery Backend         ✅
04.4B2 — Frontend Tenant Resolution       ✅
04.4C — Login Experience                  ✅
04.4D — Protected Application             ✅
04.4E — Permission-Aware Navigation       ✅
04.4F — Authentication Gates              ✅

Gate final registrado:

Backend
1390 testes aprovados
Ruff aprovado
mypy aprovado em 256 arquivos

Frontend
20 arquivos de teste aprovados
75 testes aprovados
ESLint aprovado
TypeScript aprovado
Build aprovado

Commit de referência:

90c455b
feat: implement authentication integration
4. Planejamento funcional consolidado

Antes de iniciar o 04.5, foram consolidadas as decisões funcionais recuperadas do sistema legado e as novas decisões de produto.

Documentos vigentes:

ORGANIZEG3_FUNCTIONAL_MAP.md
ORGANIZEG3_IMPLEMENTATION_ORDER.md

DOCUMENT_ENGINE_SPEC.md
DOCUMENT_TAG_CATALOG.md

PROJECT_WORKSPACE_SPEC.md
LEGACY_MIGRATION_SPEC.md

FISCAL_XML_DRAFT_SPEC.md
WHATSAPP_LEAD_SPEC.md
5. Decisões consolidadas

Foram formalmente preservados ou aprovados:

Document Engine
Templates personalizáveis por empresa
Catálogo oficial de tags
DOCX editável
HTML/PDF estruturado

Workspace automático de projetos
Arquivos-modelo
Integração operacional com SketchUp

Migração segura do banco legado
Dry-run
Mapeamento de IDs
Migração separada de arquivos

Rascunho XML fiscal
Sem emissão automática de NF-e

WhatsApp como entrada comercial simples
Lead separado de Cliente
Notion removido do fluxo principal

Preços por fornecedor
Histórico de preços
Melhor condição de compra

Recebimento parcial de compras
Quantidade remanescente

Automações pós-aprovação
Central de Pendências

Histórico funcional de RH
Banco de horas
Dependentes
Férias
Afastamentos
Rescisão

Financeiro recorrente
Contas bancárias
Maquininhas
DRE gerencial
Financeiro por cliente

Onboarding
Feriados configuráveis
6. Próxima etapa oficial

A próxima etapa de código é:

04.5.1 — Clientes

Clientes será utilizado como primeira tela real de referência.

7. Objetivos do 04.5.1 — Clientes

A fatia deverá validar:

API real
autenticação
tenant
permissões
listagem
paginação
busca
filtros
loading
estado vazio
erro
criação
edição
visualização
ativação/desativação
feedback
responsividade
testes

O escopo definitivo dependerá do contrato já existente no backend.

8. O que Clientes não implementará agora

Não bloquear a primeira tela com:

CRM completo
Orçamentos completos
Projetos completos
Financeiro completo
Document Engine completo
Histórico completo
WhatsApp Business API

A arquitetura deverá apenas permitir essas integrações futuras.

9. Ordem do 04.5
04.5.1 Clientes
04.5.2 Fornecedores
04.5.3 Materiais
04.5.4 Serviços
04.5.5 Máquinas
04.5.6 Marcas
04.5.7 Funcionários
04.5.8 Empresa
04.5.9 Filiais
10. Após Clientes

Depois que Clientes provar o padrão:

Clientes
↓
Shared UI Patterns
↓
demais telas reais

O objetivo é evitar duplicação de:

tabelas
paginação
filtros
estados vazios
erros
formulários
confirmações
feedback
ações protegidas por permissão
11. Regra de arquitetura visual

Toda definição visual permanece centralizada em:

theme_design

Nenhuma tela nova deverá introduzir valores visuais hardcoded.

12. Regra de qualidade

Nenhum bloco será marcado como concluído sem os gates correspondentes.

Quando aplicável:

pytest
Ruff
mypy
API tests
integration tests
Vitest
ESLint
TypeScript
build
validação manual
13. Regra de migração

A migração definitiva do legado não acontece durante o 04.5.

Porém, sempre que um módulo novo estabilizar:

modelo novo
↓
comparação com legado
↓
mapa de migração
↓
dry-run futuro

deve ser considerado.

14. Próxima sequência operacional
1. Commit da documentação funcional
2. Auditar contrato atual de Clientes
3. Definir fatia 04.5.1
4. Implementar Clientes
5. Executar gates
6. Validar visualmente
7. Consolidar padrões compartilhados
8. Continuar 04.5
15. Fonte de verdade

Para progresso:

ORGANIZEG3_ROADMAP_CURRENT.md

Para ordem de execução:

ORGANIZEG3_IMPLEMENTATION_ORDER.md

Para escopo funcional:

ORGANIZEG3_FUNCTIONAL_MAP.md

Para detalhes especializados:

*_SPEC.md
DOCUMENT_TAG_CATALOG.md

Esses documentos possuem responsabilidades diferentes e não devem competir entre si.