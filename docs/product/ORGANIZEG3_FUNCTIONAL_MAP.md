# OrganizeG3 — Mapa Funcional Oficial

**Status:** Documento vivo  
**Versão inicial:** 2026-08-10  
**Objetivo:** Consolidar as funcionalidades previstas para o OrganizeG3, incluindo recursos do sistema legado, novas decisões de produto e funcionalidades futuras.

---

# 1. Objetivo deste documento

Este documento é a referência funcional oficial do OrganizeG3.

Ele existe para evitar:

- perda de funcionalidades úteis do sistema anterior;
- implementação duplicada;
- decisões contraditórias;
- criação de telas que dificultem evoluções futuras;
- esquecimento de integrações entre módulos;
- descarte acidental de dados durante a migração.

Toda funcionalidade relevante deve possuir uma decisão explícita.

---

# 2. Classificação funcional

Cada funcionalidade pode receber uma das seguintes classificações.

## AGORA

Necessária para a etapa atual do desenvolvimento.

## PRÓXIMO

Necessária em curto prazo, após a fundação atual.

## FUTURO

Aprovada para o produto, mas não deve bloquear as fases atuais.

## OPCIONAL

Pode ser implementada dependendo da necessidade real das empresas.

## MELHORAR

Existe no sistema anterior ou já foi planejada, mas deve ser redesenhada antes de ser implementada.

## REMOVER

Não fará parte do fluxo principal do OrganizeG3.

---

# 3. Princípios funcionais

## 3.1 Preservação do legado

Nenhuma funcionalidade relevante do sistema atual deve ser descartada sem decisão registrada.

O sistema antigo é tratado como:

> fonte de requisitos funcionais, não como arquitetura a ser copiada.

O OrganizeG3 novo pode implementar o mesmo comportamento com arquitetura diferente.

---

## 3.2 Implementação progressiva

Nem todas as funcionalidades aprovadas serão implementadas imediatamente.

O princípio será:

1. implementar o necessário;
2. preparar a arquitetura para evoluções já conhecidas;
3. evitar abstrações prematuras;
4. evitar soluções descartáveis.

---

## 3.3 Multitenancy

Todas as funcionalidades empresariais devem respeitar o contexto da empresa/tenant.

Quando aplicável, também devem respeitar:

- filial;
- setor;
- estoque;
- usuário;
- permissões.

---

## 3.4 Segurança

A interface pode esconder ações não permitidas para melhorar a experiência do usuário.

Entretanto:

> a autorização real pertence ao backend.

Toda operação protegida deve continuar validada pela API.

---

# 4. Plataforma e administração

## 4.1 Empresas

**Status:** PRÓXIMO

Funcionalidades:

- cadastro da empresa;
- razão social;
- nome fantasia;
- CNPJ;
- inscrição estadual;
- endereço;
- telefone;
- e-mail;
- logo;
- redes sociais;
- dados comerciais;
- dados documentais;
- configurações operacionais.

### Futuro

- preferências documentais;
- workspace padrão;
- parametrizações financeiras;
- parametrizações de produção.

---

## 4.2 Filiais

**Status:** PRÓXIMO

Funcionalidades:

- múltiplas filiais;
- filial opcional;
- usuários vinculados;
- funcionários vinculados;
- estoques por filial;
- operações por filial;
- relatórios por filial.

---

## 4.3 Usuários

**Status:** PARCIALMENTE IMPLEMENTADO

Funcionalidades:

- autenticação;
- usuário ativo/inativo;
- membership por empresa;
- seleção de empresa;
- sessão;
- login;
- logout.

---

## 4.4 Permissões

**Status:** PARCIALMENTE IMPLEMENTADO

Funcionalidades:

- permissões por módulo;
- permissões de leitura;
- permissões de criação;
- permissões de alteração;
- permissões administrativas;
- navegação baseada em permissões;
- validação obrigatória no backend.

### Futuro

- perfis de permissão configuráveis;
- permissões documentais;
- permissões por fluxo de produção.

---

## 4.5 Onboarding

**Status:** FUTURO

Assistente inicial para configurar:

1. empresa;
2. filial;
3. usuários;
4. funcionários;
5. parâmetros;
6. fluxo de produção;
7. categorias;
8. estoque;
9. documentos;
10. workspace de projetos.

---

# 5. Comercial

## 5.1 Leads

**Status:** FUTURO

Entrada simples.

Campos iniciais:

- nome;
- telefone;
- interesse;
- observação;
- origem;
- responsável.

O cliente não deve ser obrigado a preencher formulários extensos.

---

## 5.2 WhatsApp

**Status:** FUTURO / PRIORIDADE COMERCIAL

Funcionalidades previstas:

- abrir conversa com cliente;
- abrir conversa com lead;
- cadastro rápido de lead;
- modelos de mensagens;
- ações de contato direto.

### Decisão

WhatsApp será priorizado como porta de entrada comercial simples.

---

## 5.3 Notion para leads

**Status:** REMOVER DO FLUXO PRINCIPAL

A sincronização obrigatória com Notion não fará parte do fluxo comercial padrão.

### Futuro opcional

Integrações externas poderão ser reavaliadas caso exista demanda.

---

# 6. Clientes

## 6.1 Cadastro de clientes

**Status:** AGORA — primeira tela real planejada

Funcionalidades iniciais:

- listar;
- criar;
- visualizar;
- editar;
- buscar;
- ativar/desativar;
- validar dados;
- respeitar tenant;
- respeitar permissões.

---

## 6.2 Relacionamentos futuros do cliente

**Status:** FUTURO

O cadastro deve estar preparado para:

- leads;
- orçamentos;
- propostas;
- projetos;
- vendas;
- financeiro;
- pagamentos;
- recibos;
- contratos;
- garantias;
- documentos;
- entregas;
- assistência;
- histórico;
- WhatsApp.

---

## 6.3 Financeiro por cliente

**Status:** FUTURO

Visualização:

- total vendido;
- total recebido;
- saldo;
- valores vencidos;
- contas a receber;
- recibos;
- histórico financeiro.

---

# 7. Fornecedores

## 7.1 Cadastro

**Status:** PRÓXIMO

Funcionalidades:

- listar;
- criar;
- editar;
- visualizar;
- ativar/desativar;
- contatos;
- documentos;
- endereço.

---

## 7.2 Relação fornecedor × material

**Status:** FUTURO — APROVADO

Um material pode possuir preços diferentes em diversos fornecedores.

Dados previstos:

- fornecedor;
- preço;
- data da cotação;
- prazo;
- unidade;
- condição;
- observação.

---

## 7.3 Histórico de preços

**Status:** FUTURO — APROVADO

Registrar evolução dos preços por:

- material;
- fornecedor;
- período.

---

## 7.4 Melhor condição de compra

**Status:** FUTURO — MELHORAR

O OrganizeG3 poderá sugerir a melhor condição atual considerando:

- preço;
- prazo;
- disponibilidade;
- histórico;
- frete;
- condições comerciais.

Não deve considerar somente o menor preço.

---

# 8. Marcas

**Status:** PRÓXIMO

Funcionalidades:

- cadastro;
- edição;
- ativação;
- vínculo com materiais;
- vínculo com fornecedores quando necessário.

---

# 9. Materiais

## 9.1 Cadastro

**Status:** PRÓXIMO

Funcionalidades:

- identificação;
- descrição;
- unidade;
- categoria;
- marca;
- dimensões;
- características técnicas;
- status.

---

## 9.2 Preços

**Status:** FUTURO

Não haverá apenas um preço absoluto no material.

Os preços poderão ser associados a:

- fornecedor;
- data;
- compra;
- cotação.

---

## 9.3 Histórico de preços

**Status:** FUTURO — APROVADO

---

## 9.4 Estoque

**Status:** FUTURO

Funcionalidades:

- saldo;
- estoque mínimo;
- localização;
- movimentações;
- entradas;
- saídas;
- ajustes;
- perdas;
- reservas.

---

## 9.5 Estoque por unidade/setor

**Status:** FUTURO

Possibilidade de estoque separado por:

- filial;
- setor;
- área produtiva.

Exemplos:

- corte;
- pintura;
- almoxarifado.

---

# 10. Serviços

**Status:** PRÓXIMO

Cadastro de serviços/mão de obra.

Exemplos:

- corte;
- fitagem;
- montagem;
- instalação;
- manutenção;
- furação;
- acabamento;
- limpeza;
- entrega.

### Futuro

- tempo padrão;
- custo padrão;
- capacidade;
- vínculo com máquinas;
- terceirização.

---

# 11. Terceirizados

**Status:** FUTURO

Cadastro e utilização de serviços terceirizados.

Possibilidades:

- pintura;
- serralheria;
- vidro;
- pedra;
- transporte;
- instalação;
- serviços especializados.

---

# 12. Máquinas

**Status:** PRÓXIMO

Funcionalidades:

- cadastro;
- status;
- localização;
- capacidade.

### Futuro

- vínculo com atividades;
- manutenção;
- disponibilidade;
- capacidade produtiva;
- paradas.

---

# 13. Orçamentos

**Status:** FUTURO — MÓDULO PRINCIPAL

Funcionalidades previstas:

- criação;
- edição;
- itens;
- materiais;
- serviços;
- custos;
- margens;
- impostos;
- transporte;
- mão de obra;
- valores;
- condições de pagamento;
- prazo;
- observações;
- anexos;
- imagens;
- aprovação;
- revisão;
- histórico.

---

## 13.1 Proposta comercial

**Status:** FUTURO

Gerada a partir do orçamento.

Pode possuir:

- template padrão;
- template personalizado;
- PDF;
- dados da empresa;
- dados do cliente;
- ambientes;
- valores;
- condições;
- prazo.

---

## 13.2 Aprovação

**Status:** FUTURO

A aprovação deve produzir evento de negócio.

Exemplo conceitual:

`BudgetApproved`

Esse evento poderá disparar outras operações.

---

# 14. Automações pós-aprovação

**Status:** FUTURO — APROVADO

Uma venda/orçamento aprovado poderá gerar:

- demanda de produção;
- demanda de compra;
- conta a receber;
- projeto;
- workspace;
- logística;
- documentos.

A automação não deve criar acoplamento direto entre telas.

---

# 15. Projetos

**Status:** FUTURO — MÓDULO PRINCIPAL

Projeto representa o trabalho real executado para um cliente.

Pode possuir:

- cliente;
- orçamento;
- código;
- descrição;
- ambientes;
- responsáveis;
- prazo;
- arquivos;
- documentos;
- produção;
- entrega.

---

# 16. Workspace de Projetos

**Status:** FUTURO — APROVADO E IMPORTANTE

Função destinada principalmente ao desktop.

Objetivo:

- criar automaticamente estrutura local de projeto;
- reduzir erros de nome;
- reduzir erros de localização;
- facilitar trabalho no SketchUp.

---

## 16.1 Diretório base

Configurável por empresa.

Exemplo:

`D:\Marcenaria\Projetos`

---

## 16.2 Nome do projeto

Configurável.

Exemplo:

`{{cliente.nome}} - {{projeto.nome}}`

---

## 16.3 Estrutura

Exemplo inicial:

```text
Cliente - Projeto
├── 01 Projeto
├── 02 Renderizações
├── 03 Orçamento
├── 04 Plano de Corte
├── 05 Documentos
└── 06 Entrega

A estrutura poderá ser configurável.

16.4 Arquivos-modelo

Status: FUTURO

A empresa poderá configurar arquivos-base.

Exemplo:

Projeto_Base.skp

Ao criar o workspace:

Projeto_Base.skp

poderá ser copiado e renomeado para:

Cliente - Cozinha.skp

16.5 Abrir projeto

Status: FUTURO

A aplicação desktop poderá possuir ação:

Abrir projeto

para abrir o arquivo associado no software correspondente.

16.6 Segurança

O PWA não deve manipular diretamente diretórios locais do computador.

Responsabilidades:

Desktop
criar;
localizar;
abrir;
copiar;
organizar arquivos locais.
PWA
consultar informações;
visualizar arquivos autorizados;
fazer uploads leves quando permitido.
17. Produção

Status: FUTURO — MÓDULO PRINCIPAL

Estrutura:

Tarefa → Etapas → Checklist → Eventos

17.1 Fluxo configurável

Entrada e saída fixas.

Etapas intermediárias configuráveis por empresa.

17.2 Execução

Funcionalidades aprovadas:

múltiplos executantes;
execução individual;
reatribuição;
pausa;
ajuda em outro serviço;
retorno de etapa;
retrabalho;
etapa não aplicável;
observação;
responsável;
timestamps.
17.3 Tempo

Registrar:

início;
fim;
pausa;
tempo produtivo;
tempo parado;
motivo da parada.
17.4 Problemas

Registrar eventos como:

falta de material;
erro;
defeito;
retrabalho;
ajuste;
dependência externa.
17.5 Checklists

Aplicáveis principalmente a:

corte;
fitagem;
montagem;
acabamento;
limpeza;
entrega.
17.6 Produção em partes

Permitir execução parcial.

Exemplo:

cortar metade;
interromper;
retornar;
cortar restante.
18. Kanban

Status: FUTURO

Fluxo conceitual inicial:

Comercial
Lead
Visita
Orçamento
Aguardando Aprovação
Produção
Preparação
Corte
Montagem
Acabamento
Limpeza
Entrega
Concluído

Etapas intermediárias deverão ser configuráveis.

19. Compras

Status: FUTURO

Funcionalidades:

demanda de compra;
ordem de compra;
fornecedor;
itens;
quantidades;
valores;
previsão;
recebimento;
histórico;
documentos.
19.1 Recebimento parcial

Status: FUTURO — APROVADO

Exemplo:

Pedido: 100
Recebido: 70
Pendente: 30

O estoque recebe somente a quantidade efetivamente recebida.

19.2 Quantidade remanescente

Status: FUTURO — CONFIGURÁVEL

O sistema pode:

manter pendência na mesma OC;
sugerir nova OC;
criar nova OC conforme configuração.

Não deve gerar automaticamente em todos os casos.

19.3 Previsão de entrega

Status: FUTURO

Registrar e acompanhar previsão do fornecedor.

19.4 Arquivamento

Status: FUTURO

Ordens encerradas poderão ser arquivadas sem perda de histórico.

20. Estoque

Status: FUTURO

Funcionalidades:

entradas;
saídas;
ajustes;
reservas;
perdas;
recebimentos;
consumo;
estoque mínimo;
alertas;
inventário.
20.1 Baixa automática

Status: MELHORAR

Não deve ocorrer simplesmente porque o orçamento foi aprovado.

A baixa deve refletir o evento operacional correto.

Possibilidades futuras:

separação;
produção;
consumo;
conclusão de etapa.
21. Financeiro

Status: FUTURO — MÓDULO PRINCIPAL

Funcionalidades:

receitas;
despesas;
contas a pagar;
contas a receber;
categorias;
centros de custo;
contas bancárias;
baixas;
conciliação;
impostos;
fluxo de caixa.
21.1 Recorrências

Status: FUTURO — APROVADO

21.2 Maquininhas e cartões

Status: FUTURO

Cadastro de:

operadora;
taxas;
parcelamentos;
prazo de recebimento.
21.3 Contas bancárias

Status: FUTURO — APROVADO

21.4 DRE gerencial

Status: FUTURO — APROVADO

Não necessariamente contábil.

Objetivo:

gestão;
análise de resultado;
receitas;
custos;
despesas;
margem.
21.5 Financeiro por cliente

Status: FUTURO — APROVADO

22. RH

Status: FUTURO — MÓDULO PRINCIPAL

22.1 Funcionários

Status: PRÓXIMO

Cadastro base:

dados pessoais;
contato;
admissão;
cargo;
departamento;
filial;
situação.
22.2 Dependentes

Status: FUTURO — APROVADO

22.3 Documentos

Status: FUTURO

Anexos vinculados ao funcionário.

22.4 Histórico funcional

Status: FUTURO — APROVADO

Não sobrescrever informações históricas importantes.

Exemplo:

2026 — Marceneiro
2027 — Marceneiro II
2028 — Encarregado
22.5 Eventos funcionais

Status: FUTURO

Exemplos:

promoção;
mudança de cargo;
mudança salarial;
transferência;
afastamento;
retorno.
22.6 Jornada

Status: FUTURO

Permitir jornada diferente por dia da semana.

22.7 Ponto

Status: FUTURO

Funcionalidades:

registros;
ajustes;
apuração;
espelho;
horários.
22.8 Banco de horas

Status: FUTURO — APROVADO

Registrar:

créditos;
débitos;
origem;
saldo;
ajustes.
22.9 Folha

Status: FUTURO

22.10 Encargos

Status: FUTURO

Parâmetros devem permitir vigência histórica.

Alterar um parâmetro atual não pode alterar cálculo histórico já fechado.

22.11 Férias

Status: FUTURO — APROVADO

22.12 Afastamentos

Status: FUTURO — APROVADO

22.13 Rescisão

Status: FUTURO — APROVADO

22.14 SST

Status: FUTURO

Inclui:

EPI;
exames;
treinamentos;
vencimentos;
relatórios.
23. Agenda

Status: FUTURO

Funcionalidades:

compromissos;
eventos;
agenda diária;
calendário;
responsáveis.
23.1 Feriados

Status: FUTURO — APROVADO

Permitir:

feriados nacionais;
feriados locais;
feriados configuráveis;
datas fixas;
datas móveis quando necessário.
24. Dashboard

Status: FUTURO

Objetivo:

fornecer uma visão operacional do dia.

Exemplos:

compromissos;
entregas;
produção;
contas;
estoque;
compras;
pendências.
25. Central de Pendências

Status: FUTURO — APROVADO

Centralizar situações que exigem atenção.

Exemplos:

materiais abaixo do mínimo;
compra atrasada;
conta vencida;
exame próximo do vencimento;
treinamento vencendo;
produção parada;
entrega próxima;
checklist incompleto;
problema reportado.

A central poderá alimentar:

dashboard;
notificações;
push;
alertas desktop.
26. Notificações

Status: FUTURO

Canais previstos:

PWA;
desktop;
push.

Tipos:

falta de material;
problema de produção;
pendência;
atribuição;
alteração importante;
prazo.
27. Document Engine

Status: PRÓXIMO — ESPECIFICAÇÃO ANTES DAS TELAS REAIS

O OrganizeG3 terá um mecanismo central de documentos.

27.1 Templates padrão

O OrganizeG3 fornecerá modelos iniciais.

Exemplos atuais existentes:

contrato PF;
contrato PJ;
aceite;
garantia;
recibo;
proposta;
orçamento;
lista de materiais;
ordem de compra;
termo de entrega;
holerite;
espelho de ponto;
relatório financeiro.
27.2 Personalização

Cada empresa poderá alterar seus próprios modelos.

O OrganizeG3 não deve impor:

cores;
fontes;
textos;
cláusulas;
disposição visual.
27.3 Template x documento gerado

São objetos diferentes.

Template

Modelo reutilizável.

Documento gerado

Cópia preenchida com dados reais.

Alterar o documento gerado não altera o template.

27.4 DOCX

Status: APROVADO

Indicado principalmente para documentos textuais editáveis.

Exemplos:

contratos;
recibos;
garantias;
aceite.
27.5 HTML/PDF

Status: APROVADO

Indicado principalmente para documentos estruturados e relatórios.

Exemplos:

orçamento;
proposta;
lista de materiais;
ordem de compra;
holerite;
espelho de ponto;
relatório financeiro.
27.6 Catálogo oficial de tags

Status: PRÓXIMO

Será definida uma convenção única.

Exemplo:

{{empresa.nome}}
{{empresa.cnpj}}
{{cliente.nome}}
{{cliente.documento}}
{{projeto.codigo}}
{{orcamento.valor_total}}
{{documento.data}}

Não existe obrigação de manter a nomenclatura antiga.

Os templates atuais podem ser reformatados.

27.7 Validação

O sistema deverá conseguir detectar:

tag válida;
tag desconhecida;
tag indisponível naquele tipo de documento;
problema de template.
27.8 Prévia

Status: FUTURO

Permitir testar um template antes de torná-lo padrão.

27.9 Template padrão da empresa

Status: FUTURO

Cada tipo poderá possuir um template padrão ativo.

27.10 Versionamento

Status: FUTURO — PREPARAR ARQUITETURA

Alterar template não deve alterar documento histórico já gerado.

28. Rascunho XML fiscal

Status: FUTURO — APROVADO

Objetivo:

facilitar o trabalho do escritório contábil.

O OrganizeG3 poderá gerar um rascunho estruturado usando dados já cadastrados.

28.1 Faz parte
coletar dados da venda;
coletar dados do cliente;
coletar itens;
coletar valores;
validar campos;
gerar XML;
permitir download/exportação.
28.2 Não faz parte inicialmente
emissão automática de NF-e;
transmissão;
autorização SEFAZ;
assinatura digital fiscal;
consulta automática de protocolo.

O arquivo será utilizado externamente pelo escritório/sistema fiscal.

29. Arquivos e anexos

Status: FUTURO

Permitidos no PWA:

fotos;
PDF;
documentos leves.

Arquivos pesados de projeto não devem ser enviados indiscriminadamente para o PWA.

30. Documentos do projeto

Status: FUTURO

Um projeto poderá reunir referências para:

contrato;
proposta;
orçamento;
plano de corte;
recibos;
garantia;
aceite;
fotos;
arquivos auxiliares.
31. Auditoria

Status: IMPLEMENTADO COMO FUNDAÇÃO

Registrar eventos relevantes com:

tenant;
usuário;
correlation id;
data/hora;
entidade;
operação.
Futuro

Ampliar para todos os módulos operacionais.

32. Migração do sistema legado

Status: FUTURO — OBRIGATÓRIO ANTES DO LANÇAMENTO

O banco atual não será descartado.

O OrganizeG3 terá processo específico de migração.

32.1 Fonte

Sistema atual utilizado pela empresa piloto.

32.2 Estratégia
Banco antigo
    ↓
leitura
    ↓
normalização
    ↓
validação
    ↓
mapeamento
    ↓
novo OrganizeG3
32.3 Regra de segurança

O migrador nunca deve modificar o banco legado durante a leitura.

32.4 IDs

IDs antigos não serão utilizados como identificadores oficiais do novo sistema.

Será criado mapeamento:

legacy_id
    ↓
UUID novo
32.5 Dry-run

Status: OBRIGATÓRIO

Antes da migração definitiva:

analisar;
simular;
validar;
gerar relatório.
32.6 Relatório

Exemplo:

Clientes encontrados: 142
Convertidos: 140
Com inconsistência: 2
Duplicidades possíveis: 3
32.7 Ordem

A migração deverá respeitar dependências.

Exemplo geral:

empresa;
filiais;
usuários;
funcionários;
clientes;
fornecedores;
marcas;
materiais;
serviços;
máquinas;
configurações;
orçamentos;
projetos;
estoque;
compras;
financeiro;
RH;
agenda;
documentos;
históricos.

A ordem definitiva dependerá dos modelos finais.

32.8 Arquivos

Arquivos externos serão tratados separadamente dos registros do banco.

Exemplos:

SketchUp;
imagens;
PDFs;
contratos;
recibos;
logos;
anexos.
32.9 Migração final

A migração definitiva só deve ocorrer quando os módulos de destino estiverem estáveis.

Até lá, o sistema atual continua sendo a fonte operacional real.

33. Funcionalidades explicitamente não priorizadas
33.1 Notion como entrada obrigatória de lead

Status: REMOVER

33.2 Emissão fiscal automática

Status: NÃO FAZ PARTE DO ESCOPO INICIAL

O OrganizeG3 gera somente rascunho/exportação quando implementado.

33.3 Hardware ID como arquitetura principal de licença

Status: REMOVER

O novo sistema utilizará estratégia de licenciamento compatível com plataforma/tenant.

33.4 SQLite como banco principal da plataforma

Status: REMOVER DA NOVA ARQUITETURA CENTRAL**

SQLite pode continuar existindo apenas onde houver uma necessidade técnica específica futura.

O banco principal do OrganizeG3 será PostgreSQL/Supabase.

34. Inteligência artificial

Status: FUTURO

Possibilidades:

assistente operacional;
análise de produtividade;
análise de problemas;
sugestões de compra;
interpretação de indicadores;
apoio a orçamento;
apoio administrativo.

IA não deve substituir as regras determinísticas do ERP.

35. Princípio de evolução modular

Antes de implementar cada módulo, responder:

O que precisa funcionar agora?
Com quais módulos precisará conversar futuramente?
Que funcionalidade do legado precisa ser preservada?
Que dados precisarão ser migrados?
Que permissões se aplicam?
Que eventos precisam ser auditados?
Que documentos dependem desses dados?
Que integrações futuras dependem dele?
36. Próxima sequência de trabalho

A ordem aprovada após a conclusão da autenticação é:

1. Consolidar Mapa Funcional Oficial
2. Especificar Document Engine
3. Especificar Catálogo Oficial de Tags
4. Especificar Workspace de Projetos
5. Especificar Migração Legado → OrganizeG3
6. Especificar Rascunho XML
7. Especificar WhatsApp → Lead
8. Atualizar roadmap oficial
9. Retomar Phase 04.5 — First Real Screens
10. Iniciar 04.5.1 — Clientes
37. Regra de decisão final

Uma funcionalidade do sistema anterior somente pode ter um dos destinos:

MANTER
MELHORAR
ADIAR
SUBSTITUIR
REMOVER

Nenhuma funcionalidade relevante deve desaparecer por esquecimento.

38. Estado atual do desenvolvimento
PHASE 01 — PLATFORM FOUNDATION             100%
PHASE 02 — CORE DOMAIN                    100%
PHASE 03 — APPLICATION & API              100%

PHASE 04 — WEB / PWA INTEGRATION          EM ANDAMENTO

04.1 Frontend Foundation                  100%
04.2 Theme Design Foundation              100%
04.3 App Shell                            100%
04.4 Authentication Integration           100%
04.5 First Real Screens                   pendente
04.6 Shared UI Patterns                   pendente
04.7 PWA Integration                      pendente
04.8 Integration Gates                    pendente
39. Observação

Este mapa deve permanecer um documento vivo.

Novas decisões devem ser incorporadas aqui ou referenciadas por documentos funcionais especializados.

Os documentos especializados previstos são:

DOCUMENT_ENGINE_SPEC.md
DOCUMENT_TAG_CATALOG.md
PROJECT_WORKSPACE_SPEC.md
LEGACY_MIGRATION_SPEC.md
FISCAL_XML_DRAFT_SPEC.md
WHATSAPP_LEAD_SPEC.md

Esses documentos detalharão os contratos funcionais sem sobrecarregar este mapa.
