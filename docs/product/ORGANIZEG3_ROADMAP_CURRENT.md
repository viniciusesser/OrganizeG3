# OrganizeG3 — Roadmap Atual

**Status:** Vigente
**Atualizado em:** 2026-08-13
**Objetivo:** Registrar o estado atual do desenvolvimento e a próxima sequência operacional.

---

# 1. Estado macro

```text
PHASE 01 — PLATFORM FOUNDATION             100% ✅
PHASE 02 — CORE DOMAIN                     100% ✅
PHASE 03 — APPLICATION & API               100% ✅
PHASE 04 — WEB / PWA INTEGRATION           100% ✅
PHASE 05 — UX/UI                            43% 🚧
PHASE 06 — MODULE IMPLEMENTATION             0%
PHASE 07 — QUALITY & SECURITY                0%
PHASE 08 — RELEASE ENGINEERING               0%
PHASE 09 — DISTRIBUTION                      0%

Progresso macro: aproximadamente 49% — quatro fases completas e 43% da Phase 05.

O percentual macro considera as nove fases principais com o mesmo peso. O progresso interno de cada fase permanece registrado separadamente.

2. Phase 04 — Web / PWA Integration
04.1 Frontend Foundation                   100% ✅
04.2 Theme Design Foundation               100% ✅
04.3 App Shell                             100% ✅
04.4 Authentication Integration            100% ✅
04.5 First Real Screens                    100% ✅
04.6 Shared UI Patterns                    100% ✅
04.7 PWA Integration                       100% ✅
04.8 Integration Gates                     100% ✅

Status da Phase 04: 100% — 8 de 8 blocos concluídos.

3. Escopo concluído na Phase 04
3.1 Fundação frontend
aplicação React/PWA estruturada;
configuração de ambiente centralizada;
comunicação autenticada com a API;
tratamento comum de erros HTTP;
navegação desktop e móvel;
rotas públicas e protegidas;
contexto da empresa ativa.
3.2 Autenticação e autorização
autenticação integrada ao Supabase Auth;
descoberta dos tenants do usuário;
seleção e persistência do tenant ativo;
consulta da identidade autenticada;
proteção das rotas do aplicativo;
navegação orientada por permissões;
tratamento de sessão expirada e acesso indisponível.
3.3 Primeiras telas reais
 04.5.1 — Clientes
 04.5.2 — Fornecedores
 04.5.3 — Materiais
 04.5.4 — Serviços
 04.5.5 — Máquinas
 04.5.6 — Marcas
 04.5.7 — Funcionários
 04.5.8 — Empresa
 04.5.9 — Filiais

As telas validaram, quando aplicável:

listagem real;
paginação;
pesquisa e filtros;
loading, erro e estado vazio;
criação e edição;
visualização;
ativação e inativação;
permissões;
feedback;
responsividade.
3.4 Padrões compartilhados
layouts de página;
tabelas responsivas;
paginação;
filtros;
diálogos;
estados de loading, erro e vazio;
ações protegidas por permissão;
estilos centralizados no theme_design.
3.5 PWA
manifesto reconhecido pelo navegador;
identidade e ícones instaláveis;
modo standalone;
service worker registrado e ativo;
shell carregado pelo cache;
indicador Online e Offline;
comportamento offline validado;
dados autenticados não apresentados como atualizados durante falha de rede.
4. Gates finais da Phase 04
4.1 API
 Compilação aprovada
 Ruff aprovado
 mypy aprovado em 258 arquivos
 1.390 testes aprovados
 21 revisões Alembic reconhecidas
 Uma única head Alembic
4.2 PWA
 Lint aprovado
 TypeScript aprovado
 39 arquivos de teste aprovados
 218 testes aprovados
 Build aprovado
 Manifesto, service worker e Workbox gerados
4.3 Banco e integração real
 Código na revisão b7c2a91d4e6f
 PostgreSQL na revisão b7c2a91d4e6f
 /api/v1/auth/tenants respondendo 200
 /api/v1/auth/me respondendo 200
 /health respondendo 200
 /api/v1/customers respondendo 200
 Cliente real carregado pelo PWA a partir do tenant autenticado
5. Phase 05 — UX/UI
05.1 Auditoria UX/UI e arquitetura         100% ✅
05.2 Fundação acessível de overlays        100% ✅
05.3 Navegação e hierarquia                100% ✅
05.4 Formulários, estados e feedback         0% — PRÓXIMO
05.5 Responsividade e experiência móvel      0%
05.6 Consistência entre módulos              0%
05.7 Gates finais e documentação             0%

Status da Phase 05: 43% — 3 de 7 blocos concluídos.

A Phase 05 consolida a experiência construída antecipadamente na Phase 04. O design system existente deve ser evoluído somente quando houver necessidade comprovada.

6. Escopo concluído na Phase 05
6.1 Auditoria UX/UI e arquitetura

Foram auditados:

arquitetura da informação;
navegação desktop e móvel;
estrutura do App Shell;
formulários e painéis de detalhes;
diálogos de confirmação;
estados e regiões vivas;
comportamento responsivo;
centralização dos valores visuais;
operação por teclado;
foco e rolagem em overlays.

A auditoria confirmou:

ausência de valores visuais hardcoded nas telas analisadas;
padrões visuais centralizados no theme_design;
regiões vivas já presentes nos principais fluxos;
19 overlays existentes;
ausência inicial de gerenciamento compartilhado de foco;
fechamento com Escape implementado apenas parcialmente;
fuga de foco para o conteúdo ao fundo;
ausência de restauração uniforme do foco;
problema de rolagem no menu móvel.

Os achados foram convertidos em tarefas verificáveis para os blocos seguintes.

6.2 Fundação acessível de overlays

Foi criada uma infraestrutura compartilhada para:

mover o foco ao abrir um overlay;
selecionar o foco inicial adequado;
conter Tab e Shift+Tab;
fechar com Escape;
restaurar o foco ao elemento acionador;
bloquear a rolagem da página ao fundo;
suportar overlays empilhados;
impedir que overlays inferiores processem eventos;
respeitar operações em andamento;
manter rolagem interna em formulários extensos;
oferecer comportamento reutilizável para futuros módulos.

Foram migrados:

menu móvel;
diálogo de confirmação;
oito painéis de detalhes;
nove formulários de cadastro e edição.

Componentes migrados:

 MobileNavigation
 ConfirmationDialog
 BranchDetails
 BranchForm
 BrandDetails
 BrandForm
 CompanyForm
 CustomerDetails
 CustomerForm
 EmployeeDetails
 EmployeeForm
 MachineDetails
 MachineForm
 MaterialDetails
 MaterialForm
 ServiceDetails
 ServiceForm
 SupplierDetails
 SupplierForm
6.3 Auditoria consolidada dos overlays

A auditoria final comprovou:

Componentes com overlay:                 19
Componentes não migrados:                 0
Componentes com autoFocus nativo:         0
Componentes com listener legado:          0
Overlays com hook acessível:           19/19
Overlays com referência correta:       19/19
Overlays com tabIndex correto:         19/19
6.4 Gates do 05.2
 TypeScript aprovado
 ESLint aprovado
 42 arquivos de teste aprovados
 232 testes aprovados
 Build de produção aprovado
 230 módulos transformados
 Manifesto PWA gerado
 Service worker gerado
 14 entradas adicionadas ao precache
 Auditoria estática dos 19 overlays aprovada
 Validação manual desktop aprovada
 Validação manual móvel aprovada
 Navegação por teclado aprovada
 Rolagem interna e isolamento do fundo aprovados
 Verificação de whitespace aprovada

O aviso de chunk JavaScript acima de 500 kB permanece registrado para divisão futura de código e não reprovou o build atual.


6.5 Navegação e hierarquia

Foram consolidados:

- catálogo centralizado de navegação;
- resolução do grupo e da página atual;
- suporte a subrotas futuras mantendo o módulo pai;
- agrupamento semântico dos módulos;
- indicação visual e acessível da rota ativa;
- contexto da empresa ativa no App Shell;
- contexto da empresa e da página no menu móvel;
- título da aba sincronizado com a página;
- skip link para o conteúdo principal;
- região principal identificada e focável;
- conectividade anunciada de forma acessível;
- relacionamento entre o botão Menu e a região controlada;
- preservação das permissões na navegação;
- operação completa por teclado no desktop e no celular;
- ausência de valores visuais hardcoded no frontend.

6.6 Gates do 05.3

- [x] Auditoria estática com 15 de 15 requisitos aprovados
- [x] Nenhum valor visual hardcoded encontrado
- [x] TypeScript aprovado
- [x] ESLint aprovado
- [x] 43 arquivos de teste aprovados
- [x] 244 testes aprovados
- [x] Build de produção aprovado
- [x] Manifesto e service worker gerados
- [x] Validação manual desktop aprovada
- [x] Validação manual móvel aprovada
- [x] Navegação por teclado aprovada
- [x] Skip link aprovado
- [x] Contexto da empresa e da página aprovado
- [x] Verificação de whitespace aprovada

O aviso de chunk JavaScript acima de 500 kB permanece registrado para divisão futura de código e não reprovou o build atual.

7. Regras arquiteturais preservadas
7.1 Design system

Toda definição visual permanece centralizada em:

theme_design

Nenhuma tela ou componente deve introduzir valores visuais hardcoded.

7.2 Multitenancy
toda operação protegida deve considerar o tenant ativo;
o usuário acessa somente tenants autorizados;
permissões devem ser verificadas no backend e refletidas no frontend;
falhas de autenticação ou tenant não podem expor dados.
7.3 Qualidade

Nenhum bloco será marcado como concluído sem os gates correspondentes.

Quando aplicável:

pytest;
Ruff;
mypy;
testes de API e integração;
Vitest;
lint;
TypeScript;
build;
validação manual;
validação responsiva;
validação PWA.
7.4 Acessibilidade dos overlays

Todo novo overlay deverá utilizar a fundação acessível compartilhada.

Requisitos mínimos:

nome acessível;
foco inicial definido;
contenção de Tab e Shift+Tab;
fechamento com Escape, quando permitido;
restauração do foco;
isolamento da página ao fundo;
rolagem interna quando necessária;
testes automatizados correspondentes.
7.5 Migração do legado

A migração definitiva do legado ainda não deve ser executada.

Para cada módulo estabilizado:

modelo novo
↓
comparação com legado
↓
mapa de migração
↓
dry-run futuro
8. Próxima etapa oficial

A próxima etapa de código é:

05.4 — Formulários, estados e feedback

O bloco deverá revisar e consolidar:

- clareza e consistência dos formulários;
- indicação de campos obrigatórios;
- mensagens de validação;
- estados de envio e ações indisponíveis;
- feedback de sucesso e erro;
- confirmações de ações destrutivas;
- loading, erro e estado vazio;
- consistência entre criação e edição;
- prevenção de submissões duplicadas;
- operação por teclado e leitores de tela.
9. Próxima sequência operacional

1. Registrar e versionar a conclusão do 05.3.
2. Excluir referências temporárias da auditoria.
3. Auditar formulários, estados e feedback.
4. Definir os lotes verificáveis do 05.4.
5. Implementar uma fatia por vez.
6. Executar gates automatizados e manuais.
7. Atualizar o progresso oficial.
8. Prosseguir para o 05.5.
10. Referência histórica da autenticação

Commit de referência da conclusão da integração de autenticação:

90c455b
feat: implement authentication integration

Esse commit permanece como referência histórica da Phase 04.4 e não representa, isoladamente, o fechamento integral da Phase 04.

11. Fonte de verdade

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