# OrganizeG3 — Ordem Oficial de Implementação

**Status:** Documento oficial vigente  
**Versão inicial:** 2026-08-10  
**Atualizado em:** 2026-08-12
**Escopo:** Ordem de desenvolvimento do OrganizeG3 a partir da arquitetura atual.

---

# 1. Objetivo

Este documento define a ordem oficial de implementação do OrganizeG3.

Ele existe para evitar:

- desenvolvimento fora de sequência;
- módulos iniciados sem dependências;
- duplicidade de arquitetura;
- telas construídas antes dos contratos funcionais;
- funcionalidades esquecidas do legado;
- retrabalho entre backend e frontend;
- implementação prematura de funções futuras.

---

# 2. Autoridade

Quando houver conflito entre uma ordem antiga de implementação e este documento:

```text
ORGANIZEG3_IMPLEMENTATION_ORDER.md

prevalece.

Documentos antigos permanecem úteis como referência histórica e funcional, mas não determinam a sequência atual quando estiverem incompatíveis com:

React/PWA atual;
FastAPI;
Supabase;
arquitetura atual;
roadmap vigente;
especificações funcionais atuais.
3. Fontes oficiais complementares

A ordem deve ser utilizada em conjunto com:

ORGANIZEG3_FUNCTIONAL_MAP.md
DOCUMENT_ENGINE_SPEC.md
DOCUMENT_TAG_CATALOG.md
PROJECT_WORKSPACE_SPEC.md
LEGACY_MIGRATION_SPEC.md
FISCAL_XML_DRAFT_SPEC.md
WHATSAPP_LEAD_SPEC.md

Cada documento possui responsabilidade diferente.

4. Hierarquia das decisões

Em caso de dúvida:

1. arquitetura técnica vigente
2. roadmap vigente
3. ordem oficial de implementação
4. especificação funcional especializada
5. mapa funcional
6. documentação histórica
7. código legado como referência

O legado é fonte de requisitos.

Não é fonte automática de arquitetura.

5. Regra principal de implementação

Nenhum módulo novo deve começar apenas pela tela.

A ordem mínima para uma fatia funcional é:

1. objetivo funcional
2. dependências
3. regras
4. domínio
5. application
6. persistência
7. API
8. permissões
9. auditoria
10. frontend
11. testes
12. validação
13. documentação

Nem toda fatia exige novos elementos em todas as camadas.

Não criar abstrações vazias apenas para cumprir estrutura.

6. Fatias verticais

O OrganizeG3 deverá evoluir preferencialmente em fatias verticais completas.

Exemplo:

Cliente

Domain
+
Application
+
Persistence
+
API
+
Permissions
+
Audit
+
Frontend
+
Tests

Evitar:

criar 20 telas vazias
↓
integrar backend depois
7. Estado macro atual
PHASE 01 — PLATFORM FOUNDATION             100%
PHASE 02 — CORE DOMAIN                    100%
PHASE 03 — APPLICATION & API              100%

PHASE 04 — WEB / PWA INTEGRATION          100% — CONCLUÍDA
PHASE 05 — UX/UI                          PRÓXIMO
PHASE 06 — MODULE IMPLEMENTATION          PENDENTE
PHASE 07 — QUALITY & SECURITY             PENDENTE
PHASE 08 — RELEASE ENGINEERING            PENDENTE
PHASE 09 — DISTRIBUTION                   PENDENTE
8. Phase 04 — Web / PWA Integration

Estado:

04.1 Frontend Foundation                  concluído
04.2 Theme Design Foundation              concluído
04.3 App Shell                            concluído
04.4 Authentication Integration           concluído
04.5 First Real Screens                   concluído
04.6 Shared UI Patterns                   concluído
04.7 PWA Integration                      concluído
04.8 Integration Gates                    concluído
9. Regra da Phase 04

A Phase 04 não implementará todos os módulos completos.

Seu objetivo é provar:

integração real frontend/backend;
autenticação;
tenant;
permissões;
navegação;
padrões de tela;
componentes compartilhados;
comportamento responsivo;
infraestrutura PWA.
10. Phase 04.5 — First Real Screens

Status: CONCLUÍDO

A primeira tela real será:

Clientes

Clientes funcionará como referência de implementação frontend para os demais cadastros básicos.

11. Ordem interna do 04.5
04.5.1 Clientes
04.5.2 Fornecedores
04.5.3 Materiais
04.5.4 Serviços
04.5.5 Máquinas
04.5.6 Marcas
04.5.7 Funcionários
04.5.8 Empresa
04.5.9 Filiais
12. O que significa "First Real Screen"

Cada tela deverá possuir, quando aplicável:

listagem real
loading
erro
estado vazio
busca
filtros básicos
paginação
criação
edição
visualização
ativação/desativação
permissões
feedback
responsividade

Não necessariamente todos os recursos entram na primeira fatia de todos os módulos.

13. Clientes como tela de referência

Clientes deverá estabelecer:

arquitetura de feature frontend;
integração autenticada;
tratamento de API errors;
formulário;
listagem;
paginação;
filtros;
estados;
confirmações;
feedback;
permission-aware actions;
responsividade.

Depois disso, os demais cadastros reutilizam o padrão.

14. Clientes não deve implementar agora

Não bloquear o 04.5 com:

orçamento completo;
financeiro completo;
documentos completos;
CRM completo;
WhatsApp Business;
histórico comercial completo;
projetos completos.

A arquitetura deve apenas permitir essas evoluções.

15. Phase 04.6 — Shared UI Patterns

Status: CONCLUÍDO

Depois de Clientes provar o padrão, consolidar componentes compartilhados.

Exemplos:

PageHeader
DataTable
SearchField
FilterBar
Pagination
EmptyState
ErrorState
LoadingState
FormField
FormActions
ConfirmationDialog
StatusBadge
PermissionAction
16. Theme Design

Toda definição visual continuará centralizada em:

theme_design

ou pacote equivalente oficial.

Nenhum componente ou tela deve definir arbitrariamente:

cores;
tipografia;
espaçamentos;
bordas;
sombras;
tamanhos visuais;
estados visuais.
17. Phase 04.7 — PWA Integration

Status: CONCLUÍDO

Após os padrões de tela estarem estabilizados:

manifest
installation
service worker
cache strategy
update strategy
mobile validation
device behavior

Offline avançado não deve ser implementado sem regras claras por módulo.

18. Phase 04.8 — Integration Gates

Status: CONCLUÍDO EM 2026-08-12

Antes de fechar Phase 04:

frontend tests
backend regression
lint
typecheck
build
Ruff
mypy
API integration
authentication
tenant isolation
permission behavior
responsive validation
PWA validation

Evidências finais:

API: 1.390 testes aprovados, compilação, Ruff e mypy aprovados em 258 arquivos.
PWA: 39 arquivos de teste e 218 testes aprovados, lint, typecheck e build aprovados.
Banco: código e PostgreSQL na revisão Alembic b7c2a91d4e6f.
Integração: autenticação, identidade, tenant e consulta real de clientes aprovados.
PWA: instalação standalone, manifesto, service worker, cache e comportamento offline aprovados.
19. Phase 05 — UX/UI

Status: PRÓXIMO

A fundação visual já começou antecipadamente em Phase 04.

A Phase 05 deverá consolidar:

arquitetura da informação;
padrões de navegação;
experiência de módulos complexos;
acessibilidade;
feedback;
consistência;
fluxos avançados;
estados responsivos.

Não refazer o design system sem motivo.

20. Phase 06 — Module Implementation

A Phase 06 será a expansão funcional principal.

A ordem de módulos será guiada por dependências de negócio.

21. Ordem funcional principal da Phase 06
01. Cadastros fundamentais
02. CRM / Comercial
03. Projetos
04. Orçamentos
05. Suprimentos / Compras
06. Estoque
07. PCP
08. Produção
09. Qualidade
10. Expedição
11. Instalação
12. Assistência Técnica
13. Financeiro
14. RH
15. Documentos avançados
16. Fiscal assistido
17. Agenda
18. Dashboard / Pendências
19. Relatórios / BI
20. Workflow / Automações
21. IA

Essa sequência pode receber pequenos ajustes de dependência.

Mudanças relevantes devem ser documentadas.

22. Cadastros fundamentais

Abrange:

Clientes
Fornecedores
Marcas
Materiais
Serviços
Máquinas
Funcionários
Empresa
Filiais
Unidades
Categorias

Parte desses cadastros já possui domínio/API, e as telas de referência foram
validadas na Phase 04. As expansões funcionais permanecem na Phase 06.

23. Fornecedores e catálogo

Ordem recomendada:

1. Suppliers
2. Brands
3. Units
4. Material Categories
5. Materials
6. Supplier Material Offers
7. Material Prices
8. Supplier Price History
24. Inteligência de compra

O modelo deverá suportar futuramente:

material
↓
vários fornecedores
↓
preços
prazos
frete
condições
histórico
↓
melhor condição

A aplicação escolhe/sugere.

O template ou frontend não deve implementar essa regra isoladamente.

25. CRM / Comercial

Ordem recomendada:

1. Leads
2. Contacts
3. Activities
4. Opportunities
5. Follow-ups
6. Sales Pipeline
7. Visits
8. Commercial Proposals
9. Approvals
10. Commercial Orders
26. WhatsApp → Lead

A especificação:

WHATSAPP_LEAD_SPEC.md

é parte oficial do módulo Comercial.

Primeira integração:

cadastro rápido
+
abrir WhatsApp

Não exige API oficial do WhatsApp.

27. Lead e cliente

São entidades diferentes.

Lead
↓
qualificação
↓
conversão
↓
Customer

Conversão deve ser idempotente.

28. Notion

Notion não faz parte do fluxo comercial principal.

Qualquer integração futura será opcional.

29. Projetos

Projetos devem ser implementados antes da consolidação completa de Orçamentos complexos.

Regra:

Projetos = fonte oficial da definição técnica
30. Ordem interna de Projetos
1. Project
2. Project Environment
3. Furniture / Project Item
4. Measurement
5. Technical Revision
6. Technical Checklist
7. Attachments
8. Project Approval
9. Project Timeline
10. Project Workspace
31. Project Workspace

A especificação:

PROJECT_WORKSPACE_SPEC.md

faz parte do módulo Projetos.

O primeiro escopo futuro:

configurar diretório base
criar estrutura
copiar arquivo SKP base
associar arquivo principal
abrir pasta
abrir arquivo
verificar workspace
32. Regra do Workspace

O filesystem local é infraestrutura auxiliar.

O projeto no banco não depende da disponibilidade da pasta local.

33. Orçamentos

Orçamentos vêm após a estrutura técnica de Projetos estar estabilizada.

Ordem:

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
34. Dinheiro

Todos os novos cálculos monetários devem utilizar tipos decimais apropriados.

Não introduzir float em regras financeiras novas.

35. Aprovação do orçamento

A aprovação deverá futuramente emitir evento de negócio.

Exemplo:

BudgetApproved
36. Automações pós-aprovação

Esse evento poderá futuramente alimentar:

Projeto
Compras
Produção
Financeiro
Logística
Documentos

Cada reação deverá possuir regra própria.

Não criar chamadas diretas entre telas.

37. Document Engine

A especificação:

DOCUMENT_ENGINE_SPEC.md

define o serviço documental compartilhado.

38. Catálogo de tags

A especificação:

DOCUMENT_TAG_CATALOG.md

é o contrato oficial dos templates.

Nenhum módulo deverá inventar tags isoladamente.

39. Momento de implementação do Document Engine

A especificação está pronta antes dos módulos para evitar retrabalho.

A implementação completa não bloqueia Clientes.

Ela deve começar quando surgir o primeiro caso real que dependa dela, provavelmente:

Projetos / Orçamentos / Comercial

ou antes, se algum fluxo prioritário exigir documento.

40. Primeira versão do Document Engine

Priorizar:

tags escalares
DOCX
logo
validação
template por tenant
geração
histórico
arquivo editável

Depois:

listas
condicionais
HTML/PDF avançado
preview
versionamento avançado
41. Templates padrão

O OrganizeG3 fornecerá modelos iniciais.

A empresa poderá:

utilizar;
duplicar;
editar;
substituir;
definir padrão.

Documento gerado é independente do template.

42. Compras

Ordem recomendada:

1. Purchase Request
2. Quotation
3. Supplier Proposal
4. Quotation Comparison
5. Approval
6. Purchase Order
7. Purchase Order Item
8. Follow-up
9. Receipt Expectation
10. Receipt
43. Ordem de compra e estoque

Regra:

Purchase Order
≠
Stock Movement

Criar OC não movimenta estoque.

Recebimento é processo separado.

44. Recebimento parcial

Deve ser suportado.

Exemplo:

pedido 100
recebido 70
pendente 30

O estoque recebe somente 70.

45. Remanescente

A quantidade pendente poderá:

continuar na mesma OC;
gerar sugestão de nova OC;
gerar nova OC conforme configuração.

Não automatizar irrevogavelmente sem regra.

46. Estoque

Ordem recomendada:

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
Lot quando aplicável
47. Saldo de estoque

Saldo não será campo livre.

movimentos
↓
saldo

Se houver saldo materializado, deverá ser reconciliável.

48. Estoque por unidade

Preparar para:

tenant
filial
setor
warehouse
location

sem obrigar todas as empresas a utilizar todos os níveis.

49. PCP

PCP é planejamento.

Produção é execução.

Não misturar os dois conceitos.

50. PCP — ordem recomendada
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
51. Produção

Produção executa o plano.

Prioridades:

simplicidade
touch
poucos campos
idempotência
tempo
auditoria
offline quando necessário
52. Produção — capacidades obrigatórias já aprovadas
múltiplos executantes
pausa
retorno
reatribuição
retrabalho
etapa não aplicável
checklists
problemas
tempo parado
motivo da parada
eventos
53. Qualidade

Após execução produtiva básica:

Quality Plan
Inspection
Evidence
Nonconformity
Disposition
Corrective Action
Reinspection
Release
History
54. Expedição

Abranger futuramente:

separação;
volumes;
carregamento;
transporte;
entrega.
55. Instalação

Abranger:

agenda;
equipe;
check-in;
instalação;
ajustes;
testes;
aceite.
56. Termo de aceite

A geração utilizará Document Engine.

Não implementar mecanismo documental específico dentro de Instalação.

57. Assistência Técnica

Abranger:

garantia;
chamados;
manutenção;
visita;
peças;
retrabalho;
histórico.
58. Financeiro

Financeiro entra depois que os eventos comerciais e operacionais principais estiverem suficientemente estáveis.

Abrange:

contas a pagar
contas a receber
receitas
despesas
categorias
centros de custo
contas bancárias
baixas
recorrências
maquininhas
fluxo de caixa
DRE gerencial
financeiro por cliente
59. Financeiro histórico

Resultados históricos fechados não devem ser recalculados silenciosamente por regras novas.

60. RH

Abrange:

funcionários
cargos
departamentos
filiais
dependentes
documentos
histórico funcional
eventos funcionais
jornada
ponto
banco de horas
folha
férias
afastamentos
rescisão
SST
treinamentos
EPI
exames
61. Histórico funcional

Mudanças importantes devem preservar vigência/histórico.

Não simplesmente sobrescrever estado anterior.

62. Documentos avançados

Depois dos principais contextos existirem, expandir Document Engine para:

ordem de compra
holerite
ponto
financeiro
entrega
garantia
relatórios
63. Fiscal assistido

O escopo inicial é:

Rascunho XML Fiscal

regido por:

FISCAL_XML_DRAFT_SPEC.md
64. Fiscal não significa emissão

A primeira versão não inclui:

SEFAZ
transmissão
certificado
protocolo
cancelamento de NF-e
65. Gate do XML fiscal

Antes de considerar pronto:

obter formato real aceito pelo escritório
↓
mapear
↓
gerar
↓
testar importação real
66. Agenda

Agenda deverá integrar:

comercial;
visitas;
produção quando aplicável;
instalação;
RH;
compromissos internos.
67. Feriados

Feriados configuráveis fazem parte da Agenda/calendário corporativo.

68. Dashboard

Dashboard será construído sobre módulos reais.

Não criar dashboard cheio de métricas fictícias.

69. Central de Pendências

Deverá consolidar eventos reais como:

estoque baixo
compra atrasada
conta vencida
produção parada
follow-up vencido
exame vencendo
entrega próxima
checklist incompleto
70. Relatórios / BI

Relatórios entram após os dados de origem estarem estáveis.

Não duplicar regra de cálculo dentro do relatório.

71. Workflow e automações

Somente depois dos eventos de negócio principais existirem.

Exemplos:

BudgetApproved
PurchaseReceived
ProductionCompleted
DeliveryCompleted
PaymentOverdue
72. IA

IA entra depois que:

dados forem confiáveis;
eventos existirem;
permissões estiverem consolidadas;
auditoria estiver disponível.

IA não substitui regras determinísticas.

73. Migração do legado

Regida por:

LEGACY_MIGRATION_SPEC.md

A migração será construída progressivamente por módulo.

74. Regra de migração por módulo

Após estabilizar um módulo:

mapear legado
↓
criar transformações
↓
dry-run
↓
validar
↓
testar

Não esperar o sistema inteiro terminar para começar a estudar a migração.

75. Migração definitiva

O go-live terá:

full dry-run
backup
freeze do legado
migração
validação
liberação
76. Banco legado

Sempre leitura durante migração.

Não alterar o banco de origem.

77. Arquivos legados

Migração de arquivos será separada da migração de dados.

Projetos existentes não serão movidos automaticamente.

78. Qualidade contínua

Cada fatia deverá possuir gates proporcionais ao risco.

Exemplos:

tests
lint
typecheck
build
Ruff
mypy
migration test
API test
tenant isolation
permission check
manual validation
79. Phase 07 — Quality & Security

Phase 07 não significa "começar a testar".

Testes já são obrigatórios antes.

Essa fase consolida:

segurança;
autorização;
isolamento;
performance;
recuperação;
cobertura;
regressão;
hardening.
80. Phase 08 — Release Engineering

Somente após qualidade consolidada:

build
versionamento
environments
CI/CD
update strategy
observability
release candidate
81. Phase 09 — Distribution

Abrange:

implantação;
licenciamento;
onboarding;
atualização;
distribuição;
documentação de uso;
migração final da instalação piloto.
82. Onboarding

Onboarding poderá incluir:

empresa
filial
usuários
funcionários
fluxo
categorias
documentos
workspace
configurações
83. Regra para novas funcionalidades

Antes de incluir nova função, responder:

Resolve um problema real?
Já existe equivalente?
Qual módulo é dono?
Que dados usa?
Que permissões exige?
Que evento gera?
Que módulo depende dela?
Precisa migrar dado legado?
Precisa gerar documento?
Pode ser configurável?
84. Definition of Done funcional

Uma funcionalidade somente pode ser considerada concluída quando, conforme aplicável:

regra implementada
persistência correta
API correta
tenant isolation
permissões
auditoria
erros tratados
frontend integrado
testes verdes
documentação atualizada
migração considerada
fluxo manual validado
85. Não implementar antecipadamente

Evitar:

microserviços
Redis sem necessidade
Celery sem necessidade
offline total prematuro
IA prematura
integração fiscal completa
sincronização de arquivos pesados
automação irreversível
86. Decisões destrutivas

Antes de:

apagar legado
mover arquivos existentes
converter dados financeiros em massa
ativar automação fiscal
executar migração real
remover histórico

exigir validação explícita e backup quando aplicável.

87. Próxima sequência imediata

A partir do estado atual:

1. registrar a conclusão integral da Phase 04
2. revisar e versionar a documentação oficial
3. iniciar a Phase 05 — UX/UI
4. auditar arquitetura da informação e navegação
5. auditar acessibilidade, feedback e estados responsivos
6. consolidar a experiência dos módulos complexos
7. executar os gates definidos para cada fatia da Phase 05
88. Próxima fatia de código

A próxima etapa oficial será:

Phase 05 — UX/UI
89. Preparação da Phase 05

Antes de alterar código:

1. inventariar os fluxos e padrões visuais já implementados
2. comparar navegação desktop e móvel
3. revisar acessibilidade e contraste
4. mapear feedback, loading, erro e estados vazios
5. identificar fluxos complexos que exigem melhoria
6. definir a decomposição interna da Phase 05
7. implementar e validar uma fatia por vez
90. Regra final

O objetivo da ordem oficial não é impedir evolução.

É impedir evolução desordenada.

O OrganizeG3 deverá crescer assim:

fundação confiável
↓
fatia real
↓
padrão reutilizável
↓
módulos dependentes
↓
integrações
↓
automação
↓
inteligência

```

Cada nova camada deve se apoiar em algo já validado.
