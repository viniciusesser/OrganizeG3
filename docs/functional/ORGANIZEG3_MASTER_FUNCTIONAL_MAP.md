# ORGANIZEG3 MASTER FUNCTIONAL MAP

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento representa o mapa funcional completo do OrganizeG3.

Ele será a principal referência para o desenvolvimento do sistema.

Nenhuma tela, funcionalidade, API, entidade ou fluxo deverá ser implementado sem estar definido neste documento.

Este documento responde à pergunta:

> **O que o usuário consegue fazer dentro do OrganizeG3?**

Ele não descreve implementação.

Ele descreve comportamento.

---

# Filosofia

A implementação seguirá sempre esta ordem:

```text
Fluxo de Negócio

↓

Módulo

↓

Página

↓

Subpágina

↓

Dialog

↓

Aba

↓

Componente

↓

Ação

↓

Evento

↓

Regra

↓

Implementação
```

Nunca o contrário.

---

# Objetivos

Este documento deverá definir:

- todos os módulos;
- todas as páginas;
- todas as subpáginas;
- todos os dialogs;
- todos os componentes;
- todas as funcionalidades;
- todos os fluxos;
- todas as permissões;
- todas as integrações;
- todos os relatórios;
- todas as automações;
- todas as ações de IA.

---

# Organização

Toda funcionalidade deverá pertencer à seguinte hierarquia.

```text
Sistema

↓

Módulo

↓

Página

↓

Subpágina

↓

Dialog

↓

Aba

↓

Componente

↓

Ação
```

---

# Estrutura Oficial

Este documento será organizado em quinze grandes etapas.

---

# ETAPA 01

# Mapa Geral do Sistema

Objetivo

Mostrar todos os módulos existentes.

Exemplo

```text
OrganizeG3

Dashboard

CRM

Comercial

Compras

Estoque

Produção

PCP

Financeiro

Fiscal

RH

Projetos

Agenda

Workflow

Documentos

BI

IA

Marketplace

Configurações
```

Resultado esperado

Ter uma visão completa do ERP.

---

# ETAPA 02

# Mapa de Navegação

Objetivo

Mostrar como o usuário navega.

Exemplo

```text
Login

↓

Dashboard

↓

CRM

↓

Clientes

↓

Cadastro
```

Resultado esperado

Todo caminho do sistema documentado.

---

# ETAPA 03

# Mapa das Páginas

Objetivo

Listar todas as páginas existentes.

Cada módulo será expandido.

Exemplo

```text
CRM

Clientes

Leads

Contatos

Empresas

Categorias

Etiquetas
```

Resultado esperado

Nenhuma página esquecida.

---

# ETAPA 04

# Mapa das Subpáginas

Cada página poderá possuir subpáginas.

Exemplo

```text
Cliente

Cadastro

Financeiro

Histórico

Projetos

Pedidos

Anexos

Documentos

Timeline

Observações
```

---

# ETAPA 05

# Mapa dos Dialogs

Cada página poderá possuir diversos dialogs.

Exemplo

```text
Cliente

↓

Novo Endereço

Novo Contato

Nova Observação

Novo Documento

Upload

Exportação

Importação

Alterar Categoria

Alterar Situação
```

Todos deverão ser documentados.

---

# ETAPA 06

# Mapa das Abas

Cada tela poderá possuir abas.

Exemplo

```text
Cadastro Cliente

Geral

Endereços

Contatos

Financeiro

Documentos

Histórico

Timeline

Configurações
```

---

# ETAPA 07

# Componentes

Cada página será decomposta em componentes.

Exemplo

```text
Toolbar

Filtro

Tabela

Cards

Botões

Timeline

Grid

Menu

Formulário

Sidebar
```

---

# ETAPA 08

# Funcionalidades

Cada componente poderá executar ações.

Exemplo

```text
Cadastrar

Editar

Excluir

Duplicar

Cancelar

Aprovar

Reprovar

Pesquisar

Exportar

Importar

Imprimir

Compartilhar
```

Nenhuma funcionalidade ficará implícita.

---

# ETAPA 09

# Fluxos

Todo processo deverá possuir fluxo.

Exemplo

```text
Lead

↓

Cliente

↓

Projeto

↓

Orçamento

↓

Pedido

↓

Contrato

↓

Produção

↓

Entrega

↓

Garantia
```

Resultado esperado

Mapear todos os processos do ERP.

---

# ETAPA 10

# Eventos

Cada ação poderá gerar eventos.

Exemplo

```text
Cliente Criado

↓

CustomerCreated
```

```text
Pedido Aprovado

↓

SalesOrderApproved
```

---

# ETAPA 11

# Permissões

Toda funcionalidade possuirá permissões.

Exemplo

```text
Visualizar

Cadastrar

Editar

Excluir

Exportar

Importar

Financeiro

Administrador
```

Ligadas ao módulo de autorização.

---

# ETAPA 12

# Integrações

Toda página poderá conversar com outros módulos.

Exemplo

```text
Cliente

↓

Financeiro

CRM

Agenda

Produção

BI

IA
```

Nenhuma integração ficará escondida.

---

# ETAPA 13

# Relatórios

Cada página poderá gerar relatórios.

Exemplo

```text
Relatório Geral

Analítico

Sintético

Financeiro

Produção

Indicadores

Dashboard
```

---

# ETAPA 14

# Automações

Toda automação será documentada.

Exemplo

```text
Criar Cliente

↓

Criar Timeline

↓

Criar Auditoria

↓

Criar Sincronização

↓

Atualizar BI

↓

Enviar Notificação
```

---

# ETAPA 15

# Inteligência Artificial

Toda utilização de IA será documentada.

Exemplo

```text
Resumo

Classificação

Sugestões

Previsões

OCR

Chat

Embeddings

Pesquisa Inteligente
```

---

# Estrutura de Cada Página

Toda página seguirá obrigatoriamente este modelo.

```text
Nome

Objetivo

Quem pode acessar

Como acessar

Fluxo

Subpáginas

Dialogs

Abas

Componentes

Campos

Validações

Botões

Funcionalidades

Eventos

Automações

Permissões

Integrações

Relatórios

IA

APIs

Commands

Queries

Domain Events

Aggregates

Repositories

Tabelas

Observações
```

---

# Estrutura dos Dialogs

Todo Dialog seguirá o padrão.

```text
Nome

Objetivo

Campos

Validações

Botões

Eventos

Permissões

Retorno

Integrações
```

---

# Estrutura dos Componentes

Todo componente possuirá.

```text
Tipo

Objetivo

Propriedades

Eventos

Permissões

Reutilização

Dependências
```

---

# Regras Gerais

Nenhuma tela poderá existir sem:

- módulo;
- página;
- fluxo;
- permissão;
- integração;
- eventos;
- documentação.

---

Nenhum Dialog poderá existir sem:

- página;
- objetivo;
- validações;
- retorno;
- eventos.

---

Nenhuma funcionalidade poderá existir sem:

- permissão;
- regra;
- evento;
- fluxo.

---

# Escopo

Este documento representará:

```text
100%

da

Especificação Funcional

do OrganizeG3
```

Ele será utilizado como referência para:

- UX;
- UI;
- Desktop;
- Web;
- API;
- Banco;
- Domínio;
- Testes;
- Documentação;
- Roadmap.

---

# Próxima Etapa

Após finalizar este documento será possível desenvolver qualquer módulo do OrganizeG3 sem necessidade de redefinir requisitos funcionais.

---

# ETAPA 01

# Mapa Geral do Sistema

## Objetivo

Esta etapa define todos os módulos existentes no OrganizeG3.

Nenhuma funcionalidade poderá existir fora de um módulo.

Todo módulo deverá possuir:

- objetivo;
- responsáveis;
- páginas;
- permissões;
- integrações;
- eventos;
- entidades do domínio.

Este mapa representa a visão macro do ERP.

---

# Hierarquia Geral

```text
OrganizeG3

├── Dashboard
├── CRM
├── Comercial
├── Engenharia
├── Projetos
├── Orçamentos
├── Compras
├── Estoque
├── Produção
├── PCP
├── Expedição
├── Assistência Técnica
├── Financeiro
├── Fiscal
├── RH
├── Agenda
├── Documentos
├── Workflow
├── BI
├── Inteligência Artificial
├── Marketplace
├── Administração
├── Configurações
└── Sistema
```

---

# Dashboard

## Objetivo

Centralizar todas as informações importantes para o usuário.

Será a primeira tela após o login.

---

# CRM

## Objetivo

Gerenciar todo o relacionamento com clientes e oportunidades.

Responsável pelo ciclo:

```text
Lead

↓

Contato

↓

Cliente

↓

Pós-venda
```

---

# Comercial

## Objetivo

Gerenciar vendas.

Inclui:

- pedidos;
- contratos;
- tabelas de preço;
- comissões;
- vendedores;
- metas.

---

# Engenharia

## Objetivo

Centralizar toda a engenharia dos produtos.

Inclui:

- projetos;
- desenhos;
- revisões;
- estrutura do produto;
- documentos técnicos.

---

# Projetos

## Objetivo

Gerenciar projetos executivos.

Inclui:

- arquitetura;
- interiores;
- marcenaria;
- acompanhamento;
- cronogramas.

---

# Orçamentos

## Objetivo

Gerenciar propostas comerciais.

Inclui:

- orçamento;
- revisão;
- aprovação;
- histórico;
- versões.

---

# Compras

## Objetivo

Gerenciar fornecedores e aquisições.

Inclui:

- solicitações;
- cotações;
- pedidos;
- recebimentos.

---

# Estoque

## Objetivo

Controlar todos os materiais.

Inclui:

- entradas;
- saídas;
- inventários;
- reservas;
- movimentações.

---

# Produção

## Objetivo

Gerenciar a fabricação.

Inclui:

- ordens;
- etapas;
- apontamentos;
- qualidade;
- finalização.

---

# PCP

## Objetivo

Planejar e controlar a produção.

Inclui:

- capacidade;
- programação;
- carga máquina;
- sequenciamento;
- MRP.

---

# Expedição

## Objetivo

Gerenciar entregas.

Inclui:

- separação;
- conferência;
- carregamento;
- transporte;
- entrega.

---

# Assistência Técnica

## Objetivo

Gerenciar garantia e pós-venda.

Inclui:

- chamados;
- visitas;
- manutenção;
- peças;
- histórico.

---

# Financeiro

## Objetivo

Controlar toda movimentação financeira.

Inclui:

- contas;
- caixa;
- bancos;
- conciliação;
- fluxo de caixa.

---

# Fiscal

## Objetivo

Controlar obrigações fiscais.

Inclui:

- NF-e;
- NFS-e;
- impostos;
- SPED;
- retenções.

---

# RH

## Objetivo

Gerenciar colaboradores.

Inclui:

- cadastro;
- cargos;
- férias;
- ponto;
- treinamentos.

---

# Agenda

## Objetivo

Centralizar compromissos.

Inclui:

- visitas;
- produção;
- entregas;
- reuniões;
- tarefas.

---

# Documentos

## Objetivo

Gerenciar arquivos do sistema.

Inclui:

- contratos;
- projetos;
- imagens;
- PDFs;
- anexos.

---

# Workflow

## Objetivo

Automatizar processos.

Inclui:

- aprovações;
- gatilhos;
- notificações;
- regras;
- filas.

---

# BI

## Objetivo

Fornecer indicadores.

Inclui:

- dashboards;
- KPIs;
- gráficos;
- análises;
- previsões.

---

# Inteligência Artificial

## Objetivo

Disponibilizar recursos inteligentes.

Inclui:

- chat;
- OCR;
- resumos;
- classificação;
- geração de documentos;
- recomendações.

---

# Marketplace

## Objetivo

Centralizar integrações externas.

Inclui:

- APIs;
- plugins;
- marketplaces;
- e-commerce.

---

# Administração

## Objetivo

Gerenciar o ambiente empresarial.

Inclui:

- empresas;
- filiais;
- usuários;
- grupos;
- permissões;
- licenciamento.

---

# Configurações

## Objetivo

Centralizar parâmetros do ERP.

Inclui:

- parâmetros;
- aparência;
- idioma;
- backup;
- sincronização;
- integrações.

---

# Sistema

## Objetivo

Gerenciar recursos internos da plataforma.

Inclui:

- logs;
- auditoria;
- monitoramento;
- cache;
- armazenamento;
- sincronização;
- observabilidade.

---

# Resultado Esperado

Ao final da Etapa 01 teremos:

- todos os módulos identificados;
- escopo de cada módulo definido;
- responsabilidades claras;
- base para construção das páginas;
- base para modelagem dos fluxos.

---

# Próxima Etapa

```text
ETAPA 02

Mapa de Navegação
```

---

# ETAPA 02

# Mapa de Navegação

## Objetivo

Esta etapa define como o usuário navega pelo OrganizeG3.

A navegação deverá seguir o fluxo natural do trabalho da empresa.

O objetivo é reduzir a quantidade de cliques, facilitar o aprendizado e manter uma experiência consistente entre todos os módulos.

A navegação nunca será baseada apenas em menus.

Ela será baseada em processos.

---

# Fluxo Principal do Sistema

```text
Login

↓

Dashboard

↓

Escolha do Processo

↓

Módulo

↓

Página

↓

Subpágina

↓

Dialog

↓

Ação
```

---

# Estrutura de Navegação

```text
Dashboard

├── Comercial
│
├── Operações
│
├── Administrativo
│
├── Inteligência
│
├── Plataforma
│
└── Favoritos
```

---

# Grupo: Comercial

Responsável pelo relacionamento com clientes e geração de negócios.

```text
CRM

↓

Leads

↓

Clientes

↓

Projetos

↓

Orçamentos

↓

Pedidos

↓

Contratos
```

Fluxo principal

```text
Lead

↓

Contato

↓

Cliente

↓

Projeto

↓

Orçamento

↓

Pedido

↓

Contrato
```

---

# Grupo: Operações

Responsável pela execução dos pedidos.

```text
Engenharia

↓

Compras

↓

Estoque

↓

PCP

↓

Produção

↓

Qualidade

↓

Expedição

↓

Entrega

↓

Assistência Técnica
```

Fluxo principal

```text
Pedido

↓

Projeto Executivo

↓

Compras

↓

Separação

↓

Produção

↓

Conferência

↓

Entrega

↓

Garantia
```

---

# Grupo: Administrativo

Responsável pela gestão da empresa.

```text
Financeiro

↓

Fiscal

↓

RH

↓

Agenda

↓

Documentos
```

Fluxo principal

```text
Venda

↓

Financeiro

↓

Fiscal

↓

Recebimento

↓

Indicadores
```

---

# Grupo: Inteligência

Centraliza informações para tomada de decisão.

```text
BI

↓

Dashboards

↓

Indicadores

↓

IA

↓

Previsões
```

---

# Grupo: Plataforma

Gerencia o funcionamento do ERP.

```text
Administração

↓

Configurações

↓

Sistema

↓

Marketplace
```

---

# Dashboard

O Dashboard será o ponto central da navegação.

Ele deverá permitir acesso rápido aos principais recursos.

Exemplo

```text
Agenda do Dia

Produção

Financeiro

Notificações

Tarefas

Indicadores

Favoritos

Pesquisa Global
```

---

# Pesquisa Global

A Pesquisa Global deverá permitir localizar rapidamente qualquer recurso do sistema.

Exemplo

```text
Cliente

Produto

Pedido

Projeto

Nota Fiscal

Documento

Fornecedor

Funcionário
```

A pesquisa deverá abrir diretamente a página correspondente.

---

# Favoritos

Cada usuário poderá definir seus próprios atalhos.

Exemplo

```text
Cadastro de Clientes

Pedidos

Produção

Fluxo de Caixa

Agenda
```

---

# Histórico

O sistema deverá manter uma lista das últimas páginas acessadas.

Objetivo

Facilitar o retorno rápido ao trabalho anterior.

---

# Breadcrumb

Toda página deverá possuir navegação hierárquica.

Exemplo

```text
Dashboard

>

Comercial

>

Clientes

>

Cadastro

>

Financeiro
```

---

# Navegação entre Módulos

Os módulos poderão abrir outros módulos diretamente.

Exemplo

```text
Cliente

↓

Pedidos

↓

Produção

↓

Financeiro

↓

Documentos
```

O usuário nunca deverá precisar retornar ao menu principal para continuar o fluxo.

---

# Navegação Contextual

Sempre que possível, o sistema deverá apresentar informações relacionadas.

Exemplo

```text
Pedido

↓

Cliente

↓

Projeto

↓

Produção

↓

Financeiro

↓

Entrega
```

---

# Abas

As páginas poderão possuir múltiplas abas abertas simultaneamente.

Exemplo

```text
Cliente A

Cliente B

Pedido 1548

Projeto Cozinha

Fluxo de Caixa
```

O usuário poderá alternar rapidamente entre elas.

---

# Navegação por Links

Campos importantes deverão ser clicáveis.

Exemplo

```text
Pedido

↓

Cliente

↓

Fornecedor

↓

Produto

↓

Projeto
```

Cada clique abrirá o cadastro correspondente.

---

# Navegação por Timeline

Sempre que houver histórico, o sistema deverá permitir navegar através da Timeline.

Exemplo

```text
Cliente

↓

Orçamento

↓

Pedido

↓

Produção

↓

Entrega

↓

Garantia
```

---

# Atalhos

Todas as telas importantes deverão possuir atalhos de teclado.

Exemplo

```text
CTRL + N

Novo

CTRL + S

Salvar

CTRL + F

Pesquisar

CTRL + P

Imprimir

CTRL + E

Exportar
```

---

# Resultado Esperado

Ao concluir esta etapa teremos:

- fluxo completo de navegação;
- agrupamento lógico dos módulos;
- padrão de navegação;
- pesquisa global;
- favoritos;
- histórico;
- breadcrumbs;
- navegação contextual.

---

# Próxima Etapa

```text
ETAPA 03

Mapa das Páginas
```

---

# ETAPA 03

# Catálogo Mestre de Páginas

## Objetivo

Esta etapa define todas as páginas existentes no OrganizeG3.

Nenhuma tela poderá existir sem estar cadastrada neste catálogo.

Este catálogo será utilizado como referência para:

- UX;
- UI;
- Desktop;
- Web;
- API;
- Permissões;
- Testes;
- Documentação.

---

# Hierarquia Oficial

Toda interface seguirá obrigatoriamente esta estrutura.

```text
Módulo

↓

Grupo

↓

Página

↓

Subpágina

↓

Dialog

↓

Wizard

↓

Aba

↓

Componente

↓

Ação
```

---

# Estrutura de Cada Página

Toda página deverá possuir obrigatoriamente:

```text
Nome

Objetivo

Descrição

Grupo

Módulo

Fluxo

Página Pai

Subpáginas

Dialogs

Wizards

Abas

Componentes

Permissões

Eventos

Automações

Integrações

IA

Relatórios

APIs

Commands

Queries

Domain Events

Aggregates

Repositories

Entidades

Observações
```

---

# Estrutura de um Dialog

Todo Dialog deverá possuir:

```text
Nome

Objetivo

Página Pai

Tipo

Campos

Validações

Botões

Eventos

Retorno

Permissões
```

---

# Estrutura de um Wizard

Wizard representa uma sequência de passos.

Exemplo

```text
Importação

↓

Selecionar Arquivo

↓

Validar Dados

↓

Corrigir Erros

↓

Importar

↓

Resultado
```

Todo Wizard possuirá:

```text
Passos

Validações

Eventos

Cancelamento

Confirmação
```

---

# Estrutura de uma Aba

Cada aba deverá possuir:

```text
Nome

Objetivo

Componentes

Eventos

Permissões
```

---

# Estrutura dos Componentes

Cada componente deverá possuir:

```text
Tipo

Objetivo

Eventos

Permissões

Reutilização
```

---

# Tipos Oficiais de Página

O OrganizeG3 utilizará os seguintes tipos.

```text
Dashboard

Lista

Cadastro

Consulta

Pesquisa

Assistente (Wizard)

Relatório

Configuração

Painel

Agenda

Kanban

Timeline

Calendário

Dashboard Analítico
```

---

# Tipos Oficiais de Dialog

```text
Cadastro

Pesquisa

Seleção

Confirmação

Importação

Exportação

Anexo

Observação

Filtro

Configuração
```

---

# Tipos Oficiais de Componentes

```text
Toolbar

Sidebar

Ribbon

Menu

Tree

Grid

Tabela

Cards

Formulário

Timeline

Kanban

Calendário

Dashboard

Indicadores

Gráficos

Mapa

Upload

Preview

Chat

Assistente IA
```

---

# Convenção de Nomes

As páginas seguirão:

```text
Substantivo
```

Exemplo

```text
Clientes

Produtos

Pedidos

Produção

Compras
```

Nunca:

```text
Cadastrar Cliente

Editar Produto

Novo Pedido
```

Essas serão ações da página.

---

# Convenção para Dialogs

Sempre iniciar por:

```text
Novo

Editar

Selecionar

Importar

Exportar

Alterar

Confirmar
```

Exemplo

```text
Novo Cliente

Editar Produto

Selecionar Fornecedor

Importar Produtos
```

---

# Convenção para Wizards

Sempre representar um processo completo.

Exemplo

```text
Assistente de Backup

Assistente de Importação

Assistente de Sincronização

Assistente de Configuração Inicial
```

---

# Convenção para Abas

As abas deverão representar grupos de informação.

Exemplo

```text
Geral

Financeiro

Histórico

Documentos

Anexos

Observações

Timeline

Auditoria
```

---

# Convenção para Componentes

Sempre reutilizáveis.

Exemplo

```text
Tabela Padrão

Toolbar Padrão

Timeline Padrão

Upload Padrão

Pesquisa Global

Filtro Avançado
```

---

# Resultado Esperado

Ao final desta etapa teremos:

- catálogo completo de páginas;
- catálogo de dialogs;
- catálogo de wizards;
- catálogo de abas;
- catálogo de componentes;
- padrão oficial de nomenclatura;
- padrão oficial de organização.

---

# Próxima Etapa

```text
ETAPA 03-A

Catálogo Completo de Páginas do Dashboard
```
---

# ETAPA 03-A

# Catálogo Completo de Páginas

# Dashboard

## Objetivo

O Dashboard é a Central de Operações do OrganizeG3.

Toda navegação do sistema deverá partir dele.

Seu principal objetivo é apresentar ao usuário apenas as informações relevantes para seu perfil e permitir acesso rápido às principais funcionalidades do ERP.

O Dashboard nunca será apenas um conjunto de gráficos.

Ele deverá funcionar como um Centro de Controle.

---

# Tipo da Página

```text
Dashboard
```

---

# Fluxo

```text
Login

↓

Dashboard

↓

Escolha do Processo

↓

Módulo

↓

Página
```

---

# Usuários

O Dashboard será personalizado para cada perfil.

Exemplo

```text
Administrador

Gerente

Financeiro

Compras

Produção

Projetista

Comercial

Montador

Vendedor

Diretor
```

---

# Estrutura Geral

```text
Dashboard

├── Página Inicial
├── Pesquisa Global
├── Favoritos
├── Notificações
├── Tarefas
├── Agenda
├── Atividades Recentes
├── Indicadores
├── KPIs
├── Widgets
├── Atalhos
├── Alertas
├── Aprovações Pendentes
├── Timeline
├── IA
└── Configurações do Dashboard
```

---

# Página

## Página Inicial

### Objetivo

Apresentar uma visão resumida da empresa.

---

## Componentes

```text
Indicadores

Resumo Financeiro

Resumo Comercial

Resumo Produção

Resumo Estoque

Agenda

Notificações

Tarefas

Alertas

Favoritos
```

---

# Página

## Pesquisa Global

### Objetivo

Localizar qualquer informação do ERP.

---

## Pesquisar

```text
Cliente

Fornecedor

Produto

Pedido

Projeto

Orçamento

NF

Funcionário

Documento

Conta Financeira

Ordem de Produção

Compra

Arquivo
```

---

## Ações

```text
Abrir Cadastro

Abrir Histórico

Editar

Visualizar

Copiar Link

Adicionar Favorito
```

---

# Página

## Favoritos

### Objetivo

Permitir que cada usuário personalize seu acesso rápido.

---

## Funcionalidades

```text
Adicionar

Remover

Reordenar

Agrupar

Pesquisar Favoritos
```

---

# Página

## Notificações

### Objetivo

Exibir notificações importantes.

---

## Tipos

```text
Sistema

Financeiro

Produção

Compras

Estoque

Agenda

Workflow

IA

Marketplace
```

---

## Funcionalidades

```text
Marcar como Lida

Arquivar

Excluir

Abrir Origem

Filtrar

Pesquisar
```

---

# Página

## Tarefas

### Objetivo

Mostrar tarefas do usuário.

---

## Categorias

```text
Hoje

Atrasadas

Em Andamento

Concluídas

Delegadas

Pendentes
```

---

## Funcionalidades

```text
Criar

Editar

Concluir

Cancelar

Delegar

Abrir
```

---

# Página

## Agenda

### Objetivo

Mostrar compromissos.

---

## Exibir

```text
Hoje

Semana

Mês

Linha do Tempo
```

---

## Funcionalidades

```text
Abrir Evento

Novo Evento

Editar

Cancelar

Ir para Agenda
```

---

# Página

## Atividades Recentes

### Objetivo

Mostrar tudo que ocorreu recentemente.

---

## Exemplo

```text
Cliente criado

Pedido aprovado

Produção iniciada

Compra recebida

Backup realizado
```

---

# Página

## Indicadores

### Objetivo

Mostrar indicadores rápidos.

---

## Indicadores

```text
Clientes

Pedidos

Produção

Compras

Financeiro

Estoque

Lucro

Recebimentos

Pagamentos
```

---

# Página

## KPIs

### Objetivo

Mostrar indicadores estratégicos.

---

## KPIs

```text
Faturamento

Margem

Conversão

Lead Time

OEE

Inadimplência

Fluxo de Caixa

Produtividade
```

---

# Página

## Widgets

### Objetivo

Permitir personalização completa.

---

## Widgets Disponíveis

```text
Gráfico

Tabela

Indicador

Calendário

Kanban

Lista

Timeline

Mapa

IA

Texto

HTML

Atalho
```

---

## Funcionalidades

```text
Adicionar

Remover

Mover

Redimensionar

Ocultar

Duplicar

Salvar Layout
```

---

# Página

## Atalhos

### Objetivo

Abrir rapidamente páginas importantes.

---

## Exemplos

```text
Clientes

Pedidos

Produção

Compras

Financeiro

Agenda

Projetos
```

---

# Página

## Alertas

### Objetivo

Informar situações críticas.

---

## Alertas

```text
Estoque Baixo

Pedido Atrasado

Produção Parada

Pagamento Vencido

Compra Atrasada

Backup Falhou

Sincronização

Licença

Atualização
```

---

# Página

## Aprovações Pendentes

### Objetivo

Centralizar tudo que depende de aprovação.

---

## Aprovações

```text
Compras

Despesas

Pedidos

Contratos

Projetos

Pagamentos

Descontos
```

---

# Página

## Timeline

### Objetivo

Mostrar acontecimentos em ordem cronológica.

---

## Eventos

```text
Clientes

Pedidos

Compras

Produção

Financeiro

Agenda

Sistema
```

---

# Página

## IA

### Objetivo

Assistente Inteligente do ERP.

---

## Recursos

```text
Chat

Resumo Diário

Sugestões

Alertas Inteligentes

Pesquisa Inteligente

Análises

Explicações

Previsões

Comandos Naturais
```

---

# Página

## Configurações do Dashboard

### Objetivo

Permitir personalização.

---

## Configurações

```text
Tema

Widgets

Layout

Página Inicial

Favoritos

Indicadores

Idioma

Densidade

Modo Escuro

Atualização Automática
```

---

# Dialogs

```text
Adicionar Widget

Editar Widget

Selecionar Indicador

Selecionar Atalho

Nova Tarefa

Novo Evento

Nova Notificação Manual

Pesquisar

Filtrar Dashboard

Configurar Layout

Salvar Layout

Restaurar Layout

Exportar Dashboard
```

---

# Wizards

```text
Primeira Configuração

Criar Dashboard

Importar Dashboard

Compartilhar Dashboard
```

---

# Componentes Padrão

```text
Ribbon

Toolbar

Pesquisa Global

Sidebar

Cards

Widgets

Timeline

Calendário

Kanban

Indicadores

KPIs

Gráficos

Tabela

Lista

Mapa

Chat IA

Painel de Alertas

Painel de Tarefas
```

---

# Eventos

```text
DashboardOpened

WidgetAdded

WidgetRemoved

WidgetMoved

WidgetResized

FavoriteAdded

FavoriteRemoved

NotificationRead

TaskCompleted

DashboardCustomized
```

---

# Integrações

```text
Todos os módulos do ERP
```

---

# Permissões

```text
Visualizar Dashboard

Editar Dashboard

Criar Layout

Excluir Layout

Compartilhar Layout

Gerenciar Widgets

Gerenciar KPIs

Gerenciar Indicadores
```

---

# Relatórios

```text
Resumo Executivo

Indicadores

Produtividade

Dashboard Compartilhado

Uso do Dashboard
```

---

# IA

```text
Resumo do Dia

Resumo Financeiro

Resumo Produção

Sugestões

Pergunte ao ERP

Pesquisar Dados

Previsões

Análises

Gerar Relatórios

Explicar Indicadores
```

---

# Observações Arquiteturais

O Dashboard deverá ser totalmente modular.

Nenhum Widget poderá depender diretamente de outro.

Todos deverão ser carregados dinamicamente.

Cada usuário possuirá:

- Layout próprio;
- Favoritos próprios;
- Widgets próprios;
- Indicadores próprios;
- Permissões próprias.

O Dashboard deverá funcionar como um Centro de Operações e nunca apenas como uma tela inicial estática.

---

# Próxima Etapa

```text
ETAPA 03-B

Catálogo Completo de Páginas

CRM
```

---

# ETAPA 03-B

# Catálogo Completo de Páginas

# CRM (Customer Relationship Management)

## Objetivo

O CRM é responsável por gerenciar todo o relacionamento da empresa com seus clientes, potenciais clientes, parceiros e contatos.

Ele acompanha todo o ciclo comercial, desde o primeiro contato até o pós-venda.

Nenhuma negociação deverá acontecer fora do CRM.

---

# Fluxo Principal

```text
Lead

↓

Primeiro Contato

↓

Qualificação

↓

Visita

↓

Projeto

↓

Orçamento

↓

Negociação

↓

Pedido

↓

Contrato

↓

Produção

↓

Entrega

↓

Pós-venda

↓

Relacionamento
```

---

# Estrutura Geral

```text
CRM

├── Dashboard CRM
├── Leads
├── Oportunidades
├── Clientes
├── Contatos
├── Empresas
├── Visitas
├── Atividades
├── Agenda Comercial
├── Pipeline
├── Campanhas
├── Follow-up
├── Metas
├── Indicadores
├── Relatórios
├── Configurações
```

---

# Dashboard CRM

## Objetivo

Apresentar uma visão geral do setor comercial.

---

## Componentes

```text
Novos Leads

Pipeline

Conversão

Metas

Agenda

Últimos Contatos

Negócios em Aberto

Funil

Ranking de Vendedores

Indicadores
```

---

# Leads

## Objetivo

Cadastrar todos os potenciais clientes.

---

## Subpáginas

```text
Lista

Cadastro

Timeline

Anexos

Histórico

Conversas

Observações

Relacionamentos
```

---

## Funcionalidades

```text
Novo Lead

Editar

Excluir

Converter em Cliente

Arquivar

Duplicar

Transferir Vendedor

Adicionar Etiquetas

Adicionar Interesse

Registrar Contato

Registrar Ligação

Registrar WhatsApp

Registrar Email

Agendar Visita
```

---

# Oportunidades

## Objetivo

Controlar todas as negociações.

---

## Pipeline

```text
Novo

Qualificado

Projeto

Orçamento

Negociação

Aguardando

Fechado

Perdido
```

---

## Funcionalidades

```text
Mover Etapa

Alterar Probabilidade

Registrar Motivo

Criar Tarefa

Agendar Retorno

Criar Orçamento

Converter em Pedido
```

---

# Clientes

## Objetivo

Centralizar todas as informações dos clientes.

---

## Subpáginas

```text
Cadastro

Financeiro

Projetos

Pedidos

Contratos

Produção

Garantias

Documentos

Anexos

Timeline

Relacionamentos

Observações
```

---

## Funcionalidades

```text
Cadastrar

Editar

Inativar

Reativar

Duplicar

Exportar

Importar

Enviar Email

Enviar WhatsApp

Ligar

Gerar Projeto

Criar Orçamento

Criar Pedido

Abrir Financeiro

Abrir Produção

Abrir Agenda

Abrir Documentos
```

---

# Contatos

## Objetivo

Gerenciar pessoas vinculadas aos clientes.

---

## Funcionalidades

```text
Novo Contato

Editar

Excluir

Definir Principal

Aniversário

Cargo

Departamento

Relacionamento

Histórico
```

---

# Empresas

## Objetivo

Gerenciar grupos empresariais.

---

## Funcionalidades

```text
Cadastrar

Editar

Relacionar Clientes

Relacionar Filiais

Relacionar Contatos
```

---

# Visitas

## Objetivo

Registrar visitas comerciais.

---

## Funcionalidades

```text
Agendar

Confirmar

Cancelar

Registrar Resultado

Adicionar Fotos

Adicionar Arquivos

Adicionar Medidas

Criar Projeto
```

---

# Atividades

## Objetivo

Registrar todas as ações comerciais.

---

## Tipos

```text
Ligação

WhatsApp

Email

Reunião

Visita

Mensagem

Anotação

Pendência
```

---

# Agenda Comercial

## Objetivo

Organizar compromissos do setor comercial.

---

## Visualizações

```text
Dia

Semana

Mês

Timeline
```

---

# Pipeline

## Objetivo

Visualizar as oportunidades.

---

## Visualizações

```text
Kanban

Tabela

Lista

Timeline
```

---

## Funcionalidades

```text
Mover Cartão

Editar

Filtrar

Pesquisar

Agrupar

Colorir

Ordenar
```

---

# Campanhas

## Objetivo

Gerenciar ações de marketing.

---

## Tipos

```text
Email

WhatsApp

SMS

Telefonema

Redes Sociais
```

---

# Follow-up

## Objetivo

Garantir acompanhamento constante.

---

## Funcionalidades

```text
Criar

Editar

Concluir

Reagendar

Cancelar
```

---

# Metas

## Objetivo

Controlar metas comerciais.

---

## Indicadores

```text
Valor

Quantidade

Conversão

Visitas

Orçamentos

Pedidos
```

---

# Indicadores

## Objetivo

Exibir desempenho comercial.

---

## KPIs

```text
Leads

Conversão

Ticket Médio

Tempo Médio

Vendas

Meta

Faturamento

Clientes Ativos
```

---

# Relatórios

## Disponíveis

```text
Clientes

Leads

Conversão

Pipeline

Visitas

Atividades

Campanhas

Vendedores

Metas

Follow-up
```

---

# Configurações

## Objetivo

Parametrizar o CRM.

---

## Configurações

```text
Categorias

Origens

Etiquetas

Funil

Etapas

Status

Tipos de Atividade

Modelos de Email

Modelos de WhatsApp
```

---

# Dialogs

```text
Novo Lead

Novo Cliente

Novo Contato

Nova Empresa

Nova Visita

Nova Atividade

Novo Follow-up

Nova Campanha

Selecionar Cliente

Selecionar Contato

Selecionar Vendedor

Converter Lead

Transferir Cliente

Exportar CRM

Importar CRM

Enviar Email

Enviar WhatsApp

Registrar Ligação
```

---

# Wizards

```text
Importação de Clientes

Importação de Leads

Conversão de Lead

Cadastro Rápido

Campanha Comercial

Primeiro Atendimento
```

---

# Componentes

```text
Pipeline Kanban

Timeline

Agenda

Tabela

Cards

Mapa

Chat

Histórico

Upload

Anexos

Pesquisa Global

Filtros

Indicadores

Dashboard

Ribbon

Toolbar
```

---

# Eventos

```text
LeadCreated

LeadQualified

LeadConverted

CustomerCreated

CustomerUpdated

VisitScheduled

VisitCompleted

OpportunityWon

OpportunityLost

FollowUpCreated

CampaignStarted
```

---

# Integrações

```text
Projetos

Orçamentos

Comercial

Financeiro

Agenda

Documentos

Workflow

BI

IA

Marketplace
```

---

# Permissões

```text
Visualizar

Cadastrar

Editar

Excluir

Converter

Exportar

Importar

Enviar Email

Enviar WhatsApp

Gerenciar Pipeline

Gerenciar Metas

Gerenciar Campanhas
```

---

# Recursos de IA

```text
Resumo do Cliente

Resumo da Negociação

Classificação Automática de Leads

Probabilidade de Fechamento

Sugestão de Próxima Ação

Análise de Conversas

Geração de Emails

Geração de Mensagens

Resumo de Visitas

Pesquisa Inteligente
```

---

# Observações Arquiteturais

O CRM será o ponto de entrada de praticamente todo relacionamento comercial.

Nenhum cliente deverá nascer diretamente em outro módulo.

Projetos, Orçamentos, Pedidos, Contratos, Agenda e Pós-venda deverão sempre possuir vínculo com o CRM.

Todo o histórico de relacionamento deverá permanecer centralizado no cadastro do cliente, formando uma Timeline única e permanente.

---

# Próxima Etapa

```text
ETAPA 03-C

Catálogo Completo de Páginas

Comercial
```

---

# ETAPA 03-C

# Catálogo Completo de Páginas

# Comercial

## Objetivo

O módulo Comercial é responsável por transformar oportunidades em vendas.

Ele gerencia todo o ciclo comercial após a qualificação do cliente.

O Comercial é o elo entre:

- CRM
- Engenharia
- Orçamentos
- Produção
- Financeiro

Nenhuma venda poderá existir fora deste módulo.

---

# Fluxo Principal

```text
Cliente

↓

Projeto

↓

Orçamento

↓

Negociação

↓

Pedido

↓

Contrato

↓

Aprovação

↓

Produção

↓

Entrega

↓

Financeiro
```

---

# Estrutura Geral

```text
Comercial

├── Dashboard Comercial
├── Pedidos
├── Contratos
├── Tabelas de Preço
├── Condições de Pagamento
├── Descontos
├── Comissões
├── Vendedores
├── Metas
├── Aprovações
├── Histórico Comercial
├── Indicadores
├── Relatórios
└── Configurações
```

---

# Dashboard Comercial

## Objetivo

Centralizar todos os indicadores de vendas.

---

## Componentes

```text
Pedidos do Dia

Orçamentos Pendentes

Pedidos Aprovados

Pedidos Cancelados

Vendas do Mês

Meta

Conversão

Ticket Médio

Comissões

Ranking

Agenda Comercial
```

---

# Pedidos

## Objetivo

Gerenciar todos os pedidos da empresa.

---

## Subpáginas

```text
Lista

Cadastro

Itens

Projeto

Financeiro

Produção

Documentos

Histórico

Timeline

Anexos

Observações
```

---

## Situações

```text
Rascunho

Em Aprovação

Aprovado

Reprovado

Produção

Entregue

Cancelado
```

---

## Funcionalidades

```text
Novo Pedido

Editar

Duplicar

Cancelar

Aprovar

Reprovar

Emitir Contrato

Gerar Produção

Abrir Financeiro

Abrir Projeto

Imprimir

Exportar

Enviar por Email

Enviar por WhatsApp
```

---

# Contratos

## Objetivo

Gerenciar contratos comerciais.

---

## Funcionalidades

```text
Novo

Editar

Gerar PDF

Assinatura Digital

Cancelar

Renovar

Histórico
```

---

# Tabelas de Preço

## Objetivo

Gerenciar políticas comerciais.

---

## Funcionalidades

```text
Cadastrar

Editar

Duplicar

Ativar

Desativar

Importar

Exportar
```

---

# Condições de Pagamento

## Objetivo

Gerenciar formas de pagamento.

---

## Exemplos

```text
À Vista

30 Dias

Entrada + Parcelas

Cartão

PIX

Boleto

Financiamento
```

---

# Descontos

## Objetivo

Controlar descontos comerciais.

---

## Funcionalidades

```text
Percentual

Valor

Limite

Aprovação

Histórico
```

---

# Comissões

## Objetivo

Gerenciar comissão dos vendedores.

---

## Funcionalidades

```text
Cadastrar Regra

Editar

Calcular

Aprovar

Liquidar

Histórico
```

---

# Vendedores

## Objetivo

Gerenciar equipe comercial.

---

## Funcionalidades

```text
Cadastro

Metas

Carteira

Comissões

Agenda

Indicadores
```

---

# Metas

## Objetivo

Gerenciar metas comerciais.

---

## Indicadores

```text
Valor

Quantidade

Conversão

Margem

Ticket Médio

Novos Clientes
```

---

# Aprovações

## Objetivo

Centralizar aprovações comerciais.

---

## Aprovações

```text
Desconto

Condição Especial

Preço

Prazo

Contrato

Cancelamento
```

---

# Histórico Comercial

## Objetivo

Apresentar todo o histórico da negociação.

---

## Informações

```text
Orçamentos

Pedidos

Alterações

Aprovações

Contratos

Financeiro

Produção
```

---

# Indicadores

## KPIs

```text
Faturamento

Margem

Conversão

Pedidos

Ticket Médio

Comissão

Cancelamentos

Prazo Médio
```

---

# Relatórios

## Disponíveis

```text
Pedidos

Vendas

Comissões

Ranking

Margens

Descontos

Contratos

Metas

Conversão
```

---

# Configurações

## Objetivo

Configurar regras comerciais.

---

## Configurações

```text
Numeração

Descontos

Limites

Contratos

Assinaturas

Modelos

Impostos

Comissões
```

---

# Dialogs

```text
Novo Pedido

Selecionar Cliente

Selecionar Projeto

Selecionar Produtos

Selecionar Condição

Selecionar Transportadora

Adicionar Item

Aplicar Desconto

Calcular Comissão

Gerar Contrato

Cancelar Pedido

Aprovar Pedido

Enviar Email

Enviar WhatsApp

Exportar Pedido

Importar Pedido
```

---

# Wizards

```text
Novo Pedido

Conversão de Orçamento

Importação

Renovação de Contrato

Cadastro Comercial
```

---

# Componentes

```text
Ribbon

Toolbar

Tabela

Grid

Cards

Timeline

Histórico

Anexos

Preview PDF

Upload

Indicadores

Dashboard

Pesquisa Global

Filtro Avançado
```

---

# Eventos

```text
SalesOrderCreated

SalesOrderUpdated

SalesOrderApproved

SalesOrderRejected

SalesOrderCancelled

ContractGenerated

CommissionCalculated

DiscountApproved

CommercialGoalReached
```

---

# Integrações

```text
CRM

Projetos

Orçamentos

Engenharia

Compras

Estoque

Produção

Financeiro

Fiscal

Agenda

Workflow

BI

IA
```

---

# Permissões

```text
Visualizar

Cadastrar

Editar

Cancelar

Aprovar

Reprovar

Emitir Contrato

Gerar Produção

Aplicar Desconto

Gerenciar Comissões

Exportar

Importar
```

---

# Recursos de IA

```text
Sugestão de Desconto

Probabilidade de Fechamento

Análise de Margem

Resumo do Pedido

Resumo da Negociação

Análise Comercial

Geração de Contrato

Pesquisa Inteligente

Previsão de Vendas
```

---

# Observações Arquiteturais

O módulo Comercial é responsável exclusivamente pela negociação e formalização da venda.

Ele não deverá controlar produção, estoque ou financeiro diretamente.

Esses módulos apenas responderão aos eventos publicados pelo Comercial.

O Pedido será o Aggregate Root deste módulo.

A aprovação de um pedido deverá publicar eventos para os módulos de Produção, Financeiro, Estoque, Agenda, Workflow, BI e Auditoria.

---

# Próxima Etapa

```text
ETAPA 03-D

Catálogo Completo de Páginas

Engenharia
```

---

# ETAPA 03-D

# Catálogo Completo de Páginas

# Engenharia

## ID do Módulo

```text
ENG
```

---

# Objetivo

O módulo Engenharia é responsável pelo desenvolvimento técnico dos produtos e projetos.

É nele que nasce toda a informação utilizada pelos demais setores da empresa.

A Engenharia transforma necessidades comerciais em informações técnicas para fabricação.

Nenhum produto fabricado poderá existir sem passar pela Engenharia.

---

# Fluxo Principal

```text
Cliente

↓

Projeto

↓

Levantamento

↓

Modelagem

↓

Detalhamento

↓

Revisão

↓

Aprovação

↓

Estrutura do Produto

↓

Produção
```

---

# Estrutura Geral

```text
ENG

├── Dashboard
├── Projetos
├── Ambientes
├── Produtos
├── Estruturas (BOM)
├── Componentes
├── Materiais
├── Ferragens
├── Revisões
├── Bibliotecas
├── Templates
├── Plano de Corte
├── Documentos Técnicos
├── Aprovações
├── Indicadores
├── Relatórios
└── Configurações
```

---

# Página

## Dashboard Engenharia

### ID

```text
ENG-DAS-001
```

### Objetivo

Centralizar todas as informações da Engenharia.

---

## Componentes

```text
Projetos em Andamento

Projetos Atrasados

Projetos Aguardando Aprovação

Revisões Pendentes

Plano de Corte

Indicadores

Agenda

Notificações
```

---

# Página

## Projetos

### ID

```text
ENG-PRO-001
```

### Objetivo

Cadastrar e controlar todos os projetos técnicos.

---

## Subpáginas

```text
Lista

Cadastro

Ambientes

Móveis

Cronograma

Revisões

Arquivos

Anexos

Histórico

Timeline

Observações
```

---

## Funcionalidades

```text
Novo Projeto

Editar

Duplicar

Arquivar

Reativar

Gerar Estrutura

Gerar Plano de Corte

Exportar

Importar

Abrir SketchUp

Abrir AutoCAD

Abrir Produção
```

---

# Página

## Ambientes

### ID

```text
ENG-AMB-001
```

### Objetivo

Organizar os ambientes pertencentes ao projeto.

---

## Exemplos

```text
Cozinha

Sala

Quarto

Closet

Banheiro

Lavanderia

Escritório
```

---

# Página

## Produtos

### ID

```text
ENG-PRD-001
```

### Objetivo

Cadastrar os móveis pertencentes ao projeto.

---

## Funcionalidades

```text
Novo Produto

Duplicar

Mover

Excluir

Alterar Ambiente

Gerar Estrutura

Gerar Plano de Corte
```

---

# Página

## Estruturas (BOM)

### ID

```text
ENG-BOM-001
```

### Objetivo

Definir toda a estrutura técnica do produto.

---

## Informações

```text
Peças

Materiais

Ferragens

Espessuras

Fitas

Usinagens

Observações
```

---

# Página

## Componentes

### ID

```text
ENG-CMP-001
```

### Objetivo

Gerenciar componentes reutilizáveis.

---

## Exemplos

```text
Gavetas

Portas

Nichos

Prateleiras

Tampos

Rodapés
```

---

# Página

## Materiais

### ID

```text
ENG-MAT-001
```

### Objetivo

Definir materiais utilizados.

---

## Exemplos

```text
MDF

Compensado

Vidro

Alumínio

Aço

Pedra
```

---

# Página

## Ferragens

### ID

```text
ENG-FER-001
```

### Objetivo

Cadastrar ferragens utilizadas.

---

## Exemplos

```text
Corrediças

Dobradiças

Puxadores

Pés

Cabideiros

Suportes
```

---

# Página

## Revisões

### ID

```text
ENG-REV-001
```

### Objetivo

Controlar versões dos projetos.

---

## Funcionalidades

```text
Nova Revisão

Comparar

Restaurar

Aprovar

Cancelar
```

---

# Página

## Bibliotecas

### ID

```text
ENG-BIB-001
```

### Objetivo

Gerenciar bibliotecas reutilizáveis.

---

## Conteúdo

```text
Componentes

Materiais

Ferragens

Modelos

Blocos

Detalhes
```

---

# Página

## Templates

### ID

```text
ENG-TMP-001
```

### Objetivo

Criar modelos reutilizáveis.

---

# Página

## Plano de Corte

### ID

```text
ENG-PLC-001
```

### Objetivo

Gerar e visualizar planos de corte.

---

## Funcionalidades

```text
Gerar

Recalcular

Imprimir

Exportar

Comparar

Otimizar
```

---

# Página

## Documentos Técnicos

### ID

```text
ENG-DOC-001
```

### Objetivo

Centralizar documentação técnica.

---

## Conteúdo

```text
PDF

DWG

SKP

DXF

Imagens

Memoriais

Especificações
```

---

# Página

## Aprovações

### ID

```text
ENG-APR-001
```

### Objetivo

Controlar aprovações técnicas.

---

# Página

## Indicadores

### ID

```text
ENG-KPI-001
```

### KPIs

```text
Projetos

Revisões

Tempo Médio

Retrabalho

Plano de Corte

Perdas

Produtividade
```

---

# Página

## Relatórios

### ID

```text
ENG-REL-001
```

### Disponíveis

```text
Projetos

Estruturas

Materiais

Ferragens

Plano de Corte

Revisões

Bibliotecas
```

---

# Página

## Configurações

### ID

```text
ENG-CFG-001
```

### Objetivo

Configurar parâmetros da Engenharia.

---

# Dialogs

```text
ENG-DLG-001 Novo Projeto

ENG-DLG-002 Novo Ambiente

ENG-DLG-003 Novo Produto

ENG-DLG-004 Nova Estrutura

ENG-DLG-005 Nova Ferragem

ENG-DLG-006 Novo Material

ENG-DLG-007 Nova Revisão

ENG-DLG-008 Gerar Plano de Corte

ENG-DLG-009 Exportar Projeto

ENG-DLG-010 Importar Projeto
```

---

# Wizards

```text
ENG-WIZ-001 Assistente Novo Projeto

ENG-WIZ-002 Importação

ENG-WIZ-003 Estrutura do Produto

ENG-WIZ-004 Plano de Corte

ENG-WIZ-005 Revisão Técnica
```

---

# Componentes

```text
Ribbon

Toolbar

Árvore do Projeto

Tabela

Grid

Cards

Timeline

Preview 3D

Visualizador PDF

Upload

Pesquisa

Filtros

Dashboard
```

---

# Eventos

```text
ProjectCreated

ProjectApproved

RevisionCreated

RevisionApproved

BOMGenerated

CuttingPlanGenerated

MaterialAdded

HardwareAdded

EngineeringReleased
```

---

# Integrações

```text
CRM

Comercial

Orçamentos

Compras

Estoque

Produção

PCP

Documentos

Workflow

BI

IA
```

---

# Permissões

```text
Visualizar

Cadastrar

Editar

Excluir

Revisar

Aprovar

Liberar Produção

Exportar

Importar

Gerar Plano de Corte
```

---

# Recursos de IA

```text
Analisar Projeto

Detectar Inconsistências

Sugestão de Materiais

Sugestão de Ferragens

Otimização do Plano de Corte

Resumo Técnico

Pesquisa Inteligente

Estimativa de Produção
```

---

# Observações Arquiteturais

A Engenharia será responsável por gerar toda a estrutura técnica que alimentará Compras, Estoque, PCP e Produção.

Nenhum desses módulos poderá alterar informações técnicas diretamente.

A Engenharia é a única responsável pela definição da estrutura do produto.

As revisões deverão ser versionadas e auditadas.

Toda alteração estrutural deverá gerar uma nova revisão.

---

# Próxima Etapa

```text
ETAPA 03-E

Catálogo Completo de Páginas

Projetos
```

---

# ETAPA 03-D

# Catálogo Completo de Páginas

# Projetos

## ID do Módulo

```text
PRJ
```

---

# Objetivo

O módulo Projetos é responsável por transformar as necessidades do cliente em informações comerciais, técnicas e executivas necessárias para fabricar, instalar e entregar o projeto.

Ele concentra toda a gestão do projeto sob encomenda, incluindo:

* briefing;
* levantamento técnico;
* ambientes;
* modelagem;
* detalhamento;
* móveis;
* componentes;
* peças;
* materiais;
* ferragens;
* revisões;
* aprovações;
* lista de materiais;
* plano de corte;
* documentos técnicos;
* cronograma;
* custos previstos;
* liberação para compras;
* liberação para produção.

Não existirá um módulo separado denominado Engenharia.

Todas as funções técnicas anteriormente previstas para Engenharia pertencem ao módulo Projetos.

---

# Limites do Módulo

O módulo Projetos será responsável por definir:

```text
O que será produzido

Como será produzido

Com quais materiais

Com quais componentes

Com quais dimensões

Com quais revisões

Com quais documentos
```

O módulo Projetos não será responsável por:

```text
Comprar materiais

Controlar saldo de estoque

Programar máquinas

Executar fabricação

Registrar movimentações financeiras

Emitir documentos fiscais
```

Essas responsabilidades pertencem, respectivamente, aos módulos:

```text
Compras

Estoque

PCP

Produção

Financeiro

Fiscal
```

---

# Fluxo Principal

```text
Lead

↓

Cliente

↓

Visita

↓

Briefing

↓

Levantamento Técnico

↓

Criação do Projeto

↓

Ambientes

↓

Modelagem Inicial

↓

Orçamento

↓

Apresentação ao Cliente

↓

Revisões Comerciais

↓

Aprovação

↓

Contrato

↓

Detalhamento Executivo

↓

Estrutura dos Móveis

↓

Lista de Materiais

↓

Plano de Corte

↓

Liberação para Compras

↓

Liberação para Produção

↓

Acompanhamento

↓

Entrega

↓

Projeto Concluído
```

---

# Estrutura Geral

```text
PRJ — Projetos

├── Dashboard de Projetos
├── Projetos
├── Briefings
├── Levantamentos Técnicos
├── Visitas Técnicas
├── Ambientes
├── Móveis
├── Componentes
├── Peças
├── Estruturas de Produto
├── Materiais do Projeto
├── Ferragens do Projeto
├── Fitas de Borda
├── Usinagens e Furações
├── Acabamentos
├── Especificações Técnicas
├── Revisões
├── Aprovações
├── Pendências
├── Cronogramas
├── Responsáveis
├── Custos Previstos
├── Lista de Materiais
├── Plano de Corte
├── Documentos Técnicos
├── Arquivos do Projeto
├── Liberações
├── Histórico
├── Timeline
├── Indicadores
├── Relatórios
├── Bibliotecas
├── Templates
└── Configurações
```

---

# Página

## Dashboard de Projetos

### ID

```text
PRJ-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada de todos os projetos em andamento, seus responsáveis, prazos, revisões, pendências e liberações.

### Componentes

```text
Projetos em Andamento

Projetos Atrasados

Projetos Aguardando Visita

Projetos Aguardando Orçamento

Projetos Aguardando Aprovação

Projetos em Detalhamento

Projetos Liberados para Compras

Projetos Liberados para Produção

Revisões Pendentes

Pendências Técnicas

Carga por Projetista

Cronograma Geral

Agenda de Visitas

Indicadores

Alertas
```

### Filtros

```text
Período

Cliente

Projetista

Responsável

Status

Fase

Prioridade

Data de Entrega

Filial

Tipo de Projeto
```

### Ações

```text
Novo Projeto

Abrir Projeto

Abrir Agenda

Abrir Pendências

Abrir Aprovações

Abrir Cronograma

Exportar Dashboard

Atualizar Indicadores
```

---

# Página

## Projetos

### ID

```text
PRJ-PRO-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar, pesquisar, filtrar e administrar todos os projetos da empresa.

### Visualizações

```text
Tabela

Cards

Kanban

Timeline

Calendário
```

### Colunas Principais

```text
Código

Cliente

Nome do Projeto

Tipo

Responsável

Projetista

Fase Atual

Status

Prioridade

Data de Entrada

Prazo do Projeto

Previsão de Produção

Previsão de Entrega

Valor Orçado

Percentual Concluído
```

### Status

```text
Rascunho

Aguardando Briefing

Aguardando Visita

Em Levantamento

Em Desenvolvimento

Em Orçamento

Aguardando Apresentação

Em Revisão Comercial

Aguardando Aprovação

Aprovado

Em Contrato

Em Detalhamento Executivo

Aguardando Conferência

Aguardando Liberação

Liberado para Compras

Liberado para Produção

Em Produção

Em Instalação

Concluído

Suspenso

Cancelado

Arquivado
```

### Ações

```text
Novo Projeto

Abrir

Editar

Duplicar

Arquivar

Restaurar

Suspender

Cancelar

Alterar Responsável

Alterar Prioridade

Alterar Prazo

Abrir Cliente

Criar Orçamento

Gerar Contrato

Gerar Lista de Materiais

Gerar Plano de Corte

Liberar para Compras

Liberar para Produção

Exportar

Imprimir

Compartilhar
```

---

# Página

## Cadastro do Projeto

### ID

```text
PRJ-PRO-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações comerciais, administrativas e técnicas de um projeto.

### Abas

```text
Geral

Cliente

Briefing

Visitas

Levantamento

Ambientes

Móveis

Materiais

Ferragens

Estruturas

Orçamento

Cronograma

Responsáveis

Revisões

Aprovações

Pendências

Documentos

Arquivos

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Código

Nome do Projeto

Descrição

Cliente

Contato Principal

Endereço da Instalação

Tipo de Projeto

Categoria

Origem

Status

Fase Atual

Prioridade

Responsável

Projetista

Vendedor

Data de Entrada

Prazo Desejado pelo Cliente

Prazo Interno

Previsão de Produção

Previsão de Entrega

Percentual Concluído

Observações Gerais
```

### Aba Cliente

Informações:

```text
Dados do Cliente

Contatos

Endereços

Histórico Comercial

Projetos Anteriores

Pedidos

Financeiro

Documentos
```

### Aba Briefing

Informações:

```text
Necessidades

Preferências

Estilo

Cores

Materiais

Ferragens

Referências

Restrições

Orçamento Pretendido

Prazo Pretendido

Prioridades do Cliente

Observações
```

### Aba Visitas

Informações:

```text
Data

Responsável

Participantes

Objetivo

Status

Resultado

Fotos

Arquivos

Medições

Pendências

Próximas Ações
```

### Aba Levantamento

Informações:

```text
Medidas

Paredes

Pé-direito

Esquadros

Desníveis

Rodapés

Portas

Janelas

Pontos Elétricos

Pontos Hidráulicos

Pontos de Gás

Pontos de Iluminação

Equipamentos

Eletrodomésticos

Obstáculos

Fotos

Croquis

Observações Técnicas
```

### Aba Ambientes

Informações:

```text
Ambiente

Descrição

Dimensões

Status

Responsável

Móveis

Fotos

Arquivos

Observações
```

### Aba Móveis

Informações:

```text
Código

Nome

Ambiente

Tipo

Dimensões

Quantidade

Material Principal

Status

Revisão

Estrutura

Custo Previsto

Valor Comercial
```

### Aba Materiais

Informações:

```text
Material

Fabricante

Linha

Cor

Espessura

Acabamento

Quantidade Prevista

Unidade

Perda Prevista

Aplicação

Observações
```

### Aba Ferragens

Informações:

```text
Ferragem

Fabricante

Modelo

Acabamento

Quantidade

Aplicação

Fornecedor Preferencial

Custo Previsto

Observações
```

### Aba Estruturas

Informações:

```text
Móveis

Componentes

Peças

Materiais

Ferragens

Fitas

Usinagens

Furações

Fixações

Montagens

Observações Técnicas
```

### Aba Orçamento

Informações:

```text
Orçamento Atual

Versões

Valor de Materiais

Valor de Ferragens

Mão de Obra

Serviços Terceirizados

Transporte

Montagem

Impostos

Margem

Descontos

Valor Final
```

### Aba Cronograma

Informações:

```text
Fase

Responsável

Data Inicial

Data Final

Duração

Dependências

Percentual

Status

Atraso
```

### Aba Responsáveis

Informações:

```text
Responsável Geral

Vendedor

Projetista

Medidor

Orçamentista

Comprador

Encarregado de Produção

Montador

Terceirizados
```

### Aba Revisões

Informações:

```text
Número da Revisão

Data

Autor

Motivo

Descrição

Arquivos Alterados

Itens Alterados

Impacto em Custo

Impacto em Prazo

Status

Aprovação
```

### Aba Aprovações

Informações:

```text
Aprovação do Cliente

Aprovação Comercial

Aprovação Técnica

Aprovação de Materiais

Aprovação de Ferragens

Aprovação do Detalhamento

Liberação para Compras

Liberação para Produção
```

### Aba Pendências

Informações:

```text
Descrição

Categoria

Responsável

Prioridade

Prazo

Origem

Status

Solução

Data de Conclusão
```

### Aba Documentos

Informações:

```text
Briefing

Proposta

Orçamento

Contrato

Memorial Descritivo

Termo de Aprovação

Lista de Materiais

Plano de Corte

Desenhos Técnicos

Termo de Entrega

Garantia
```

### Aba Arquivos

Tipos:

```text
SKP

DWG

DXF

PDF

XLSX

XLSM

DOCX

Imagens

Vídeos

ZIP

Outros
```

### Aba Histórico

Informações:

```text
Alterações

Mudanças de Status

Mudanças de Prazo

Responsáveis

Revisões

Aprovações

Liberações

Cancelamentos
```

### Aba Timeline

Eventos:

```text
Projeto Criado

Briefing Preenchido

Visita Agendada

Levantamento Concluído

Orçamento Gerado

Projeto Apresentado

Revisão Solicitada

Projeto Aprovado

Contrato Emitido

Detalhamento Concluído

Materiais Definidos

Plano de Corte Gerado

Compras Liberadas

Produção Liberada

Produção Iniciada

Instalação Iniciada

Projeto Concluído
```

---

# Página

## Briefings

### ID

```text
PRJ-BRF-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar os briefings utilizados para entender necessidades, preferências e restrições dos clientes.

### Funcionalidades

```text
Novo Briefing

Editar

Duplicar

Aplicar Template

Enviar ao Cliente

Preencher com Cliente

Importar

Exportar

Gerar PDF

Concluir

Reabrir
```

### Seções do Briefing

```text
Dados Gerais

Objetivos

Necessidades

Estilo

Cores

Materiais

Ferragens

Equipamentos

Iluminação

Ergonomia

Acessibilidade

Orçamento

Prazo

Referências

Restrições

Observações
```

---

# Página

## Levantamentos Técnicos

### ID

```text
PRJ-LEV-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar medições, condições do local e informações necessárias para desenvolver e instalar o projeto.

### Funcionalidades

```text
Novo Levantamento

Editar

Duplicar

Vincular Visita

Adicionar Ambiente

Adicionar Medição

Adicionar Foto

Adicionar Croqui

Registrar Pendência

Concluir

Reabrir

Gerar Relatório
```

---

# Página

## Visitas Técnicas

### ID

```text
PRJ-VIS-001
```

### Tipo

```text
Agenda
```

### Objetivo

Planejar e registrar visitas para briefing, medição, conferência, apresentação e acompanhamento.

### Tipos

```text
Primeiro Atendimento

Briefing

Medição

Conferência

Apresentação

Acompanhamento

Pós-instalação
```

### Status

```text
Planejada

Agendada

Confirmada

Em Deslocamento

Em Andamento

Concluída

Reagendada

Cancelada
```

---

# Página

## Ambientes

### ID

```text
PRJ-AMB-001
```

### Tipo

```text
Lista
```

### Objetivo

Organizar os espaços atendidos em cada projeto.

### Exemplos

```text
Cozinha

Sala

Dormitório

Closet

Banheiro

Lavanderia

Escritório

Área Gourmet

Recepção

Loja

Consultório
```

### Funcionalidades

```text
Novo Ambiente

Editar

Duplicar

Reordenar

Mover entre Projetos

Adicionar Móvel

Adicionar Arquivo

Adicionar Foto

Registrar Pendência

Arquivar
```

---

# Página

## Móveis

### ID

```text
PRJ-MOV-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar e detalhar todos os móveis que compõem um projeto.

### Tipos

```text
Armário

Balcão

Painel

Estante

Mesa

Gaveteiro

Nicho

Prateleira

Torre

Roupeiro

Gabinete

Cabeceira

Outro
```

### Funcionalidades

```text
Novo Móvel

Editar

Duplicar

Mover de Ambiente

Gerar Estrutura

Copiar Estrutura

Aplicar Template

Gerar Lista de Peças

Calcular Materiais

Calcular Ferragens

Gerar Plano de Corte

Arquivar
```

---

# Página

## Componentes

### ID

```text
PRJ-CMP-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar subconjuntos reutilizáveis que compõem os móveis.

### Exemplos

```text
Porta

Gaveta

Prateleira

Nicho

Tampo

Rodapé

Fundo

Lateral

Divisória

Frente

Estrutura Metálica
```

---

# Página

## Peças

### ID

```text
PRJ-PEC-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar cada peça necessária para fabricar os móveis.

### Campos

```text
Código

Nome

Móvel

Componente

Material

Comprimento

Largura

Espessura

Quantidade

Veio

Fita Superior

Fita Inferior

Fita Esquerda

Fita Direita

Usinagem

Furação

Etiqueta

Observação
```

### Funcionalidades

```text
Nova Peça

Editar

Duplicar

Importar

Exportar

Gerar Etiqueta

Agrupar

Recalcular

Validar Dimensões
```

---

# Página

## Estruturas de Produto

### ID

```text
PRJ-BOM-001
```

### Tipo

```text
Árvore
```

### Objetivo

Representar a estrutura completa dos móveis e componentes do projeto.

### Hierarquia

```text
Projeto

↓

Ambiente

↓

Móvel

↓

Componente

↓

Peça

↓

Material / Ferragem / Serviço
```

### Funcionalidades

```text
Criar Estrutura

Editar Estrutura

Copiar Estrutura

Aplicar Template

Comparar Revisões

Expandir

Recolher

Validar

Calcular Custo

Gerar Lista de Materiais
```

---

# Página

## Materiais do Projeto

### ID

```text
PRJ-MAT-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir todos os materiais utilizados no projeto.

### Categorias

```text
MDF

MDP

Compensado

Madeira

Laminado

Vidro

Espelho

Metal

Alumínio

Aço

Pedra

Acrílico

Fita de Borda

Consumíveis

Embalagens
```

---

# Página

## Ferragens do Projeto

### ID

```text
PRJ-FER-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir todas as ferragens e acessórios necessários.

### Categorias

```text
Dobradiças

Corrediças

Puxadores

Sistemas de Porta

Pistões

Pés

Rodízios

Cabideiros

Suportes

Fixadores

Parafusos

Acessórios
```

---

# Página

## Fitas de Borda

### ID

```text
PRJ-FIT-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar aplicação de fita de borda em cada lado das peças.

### Informações

```text
Peça

Lado

Material

Cor

Espessura

Largura

Comprimento

Aplicação

Observação
```

---

# Página

## Usinagens e Furações

### ID

```text
PRJ-USI-001
```

### Tipo

```text
Lista
```

### Objetivo

Especificar operações técnicas realizadas nas peças.

### Tipos

```text
Furação

Rasgo

Canal

Rebaixo

Corte Especial

Usinagem CNC

Recorte

Encaixe

Chanfro
```

---

# Página

## Acabamentos

### ID

```text
PRJ-ACA-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir acabamentos aplicáveis aos móveis, peças, ferragens e componentes.

### Exemplos

```text
MDF BP

Laminado

Vidro

Espelho

Perfil

Pintura Terceirizada

Revestimento

Tamponamento

Fita de Borda
```

---

# Página

## Especificações Técnicas

### ID

```text
PRJ-ESP-001
```

### Tipo

```text
Documento
```

### Objetivo

Consolidar características técnicas e requisitos de fabricação e instalação.

### Conteúdo

```text
Materiais

Ferragens

Dimensões

Acabamentos

Tolerâncias

Fixações

Montagem

Transporte

Instalação

Cuidados

Garantia
```

---

# Página

## Revisões

### ID

```text
PRJ-REV-001
```

### Tipo

```text
Timeline
```

### Objetivo

Controlar versões e alterações realizadas em cada projeto.

### Status

```text
Em Elaboração

Aguardando Conferência

Aguardando Cliente

Aprovada

Reprovada

Substituída

Cancelada
```

### Funcionalidades

```text
Nova Revisão

Comparar Revisões

Visualizar Diferenças

Restaurar Revisão

Solicitar Aprovação

Aprovar

Reprovar

Gerar Relatório
```

---

# Página

## Aprovações

### ID

```text
PRJ-APR-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar todas as aprovações necessárias para o andamento do projeto.

### Tipos

```text
Briefing

Conceito

Layout

Materiais

Cores

Ferragens

Orçamento

Contrato

Detalhamento Executivo

Lista de Materiais

Plano de Corte

Compras

Produção
```

---

# Página

## Pendências

### ID

```text
PRJ-PEN-001
```

### Tipo

```text
Kanban
```

### Objetivo

Registrar, atribuir e acompanhar problemas, dúvidas e informações faltantes.

### Etapas

```text
Nova

Em Análise

Aguardando Cliente

Aguardando Fornecedor

Em Correção

Resolvida

Cancelada
```

---

# Página

## Cronogramas

### ID

```text
PRJ-CRO-001
```

### Tipo

```text
Timeline
```

### Objetivo

Planejar as fases, responsáveis e datas de cada projeto.

### Fases

```text
Atendimento

Briefing

Visita

Levantamento

Projeto Inicial

Orçamento

Apresentação

Revisão

Aprovação

Contrato

Detalhamento

Compras

Produção

Instalação

Conclusão
```

---

# Página

## Responsáveis

### ID

```text
PRJ-RES-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir os responsáveis por cada fase e entrega do projeto.

---

# Página

## Custos Previstos

### ID

```text
PRJ-CUS-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Consolidar custos estimados para apoiar orçamento e controle de margem.

### Composição

```text
Materiais

Ferragens

Serviços

Mão de Obra

Terceirizados

Transporte

Montagem

Impostos

Perdas

Custos Indiretos
```

---

# Página

## Lista de Materiais

### ID

```text
PRJ-LDM-001
```

### Tipo

```text
Lista
```

### Objetivo

Consolidar tudo o que será necessário comprar, reservar ou produzir.

### Grupos

```text
Chapas

Fitas

Ferragens

Perfis

Vidros

Espelhos

Metais

Pedras

Consumíveis

Embalagens

Serviços Terceirizados
```

### Funcionalidades

```text
Gerar

Recalcular

Conferir

Agrupar

Substituir Material

Comparar Estoque

Reservar Estoque

Gerar Solicitação de Compra

Exportar

Imprimir
```

---

# Página

## Plano de Corte

### ID

```text
PRJ-PLC-001
```

### Tipo

```text
Painel
```

### Objetivo

Otimizar a distribuição das peças nas chapas considerando dimensões, veio, apara e espessura de corte.

### Funcionalidades

```text
Gerar Plano

Recalcular

Alterar Parâmetros

Comparar Cenários

Visualizar Chapas

Mover Peças

Bloquear Peças

Adicionar Sobras

Utilizar Sobras

Gerar Etiquetas

Exportar PDF

Exportar DXF

Imprimir
```

### Parâmetros

```text
Largura da Serra

Apara Superior

Apara Inferior

Apara Esquerda

Apara Direita

Sentido do Veio

Rotação Permitida

Prioridade de Sobras

Dimensão Mínima de Sobra
```

---

# Página

## Documentos Técnicos

### ID

```text
PRJ-DOC-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar documentos necessários para fabricar, conferir, transportar e instalar.

### Documentos

```text
Projeto Executivo

Detalhamento

Memorial Descritivo

Lista de Peças

Lista de Materiais

Lista de Ferragens

Plano de Corte

Etiquetas

Plano de Montagem

Plano de Instalação

Checklist de Conferência
```

---

# Página

## Arquivos do Projeto

### ID

```text
PRJ-ARQ-001
```

### Tipo

```text
Gerenciador de Arquivos
```

### Objetivo

Organizar todos os arquivos digitais vinculados ao projeto.

### Funcionalidades

```text
Upload

Download

Visualizar

Versionar

Renomear

Mover

Copiar

Compartilhar

Arquivar

Restaurar

Comparar
```

---

# Página

## Liberações

### ID

```text
PRJ-LIB-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar formalmente quando o projeto está autorizado a seguir para outra etapa.

### Tipos

```text
Liberar para Orçamento

Liberar para Contrato

Liberar para Detalhamento

Liberar para Compras

Liberar para Estoque

Liberar para PCP

Liberar para Produção

Liberar para Instalação
```

### Regras

Nenhuma liberação poderá ocorrer sem os checklists exigidos pela etapa.

---

# Página

## Histórico

### ID

```text
PRJ-HIS-001
```

### Tipo

```text
Consulta
```

### Objetivo

Exibir todo o histórico operacional e administrativo do projeto.

---

# Página

## Timeline

### ID

```text
PRJ-TML-001
```

### Tipo

```text
Timeline
```

### Objetivo

Apresentar os acontecimentos do projeto em ordem cronológica.

---

# Página

## Indicadores

### ID

```text
PRJ-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Projetos Ativos

Projetos por Fase

Projetos Atrasados

Tempo Médio de Desenvolvimento

Quantidade de Revisões

Tempo de Aprovação

Retrabalho

Carga por Projetista

Perda Prevista

Custo Previsto

Margem Prevista

Projetos Liberados
```

---

# Página

## Relatórios

### ID

```text
PRJ-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Projetos por Status

Projetos por Cliente

Projetos por Responsável

Projetos Atrasados

Cronograma

Revisões

Aprovações

Pendências

Materiais por Projeto

Ferragens por Projeto

Lista de Peças

Lista de Materiais

Plano de Corte

Custos Previstos

Carga de Trabalho

Produtividade
```

---

# Página

## Bibliotecas

### ID

```text
PRJ-BIB-001
```

### Tipo

```text
Biblioteca
```

### Objetivo

Armazenar itens técnicos reutilizáveis.

### Conteúdo

```text
Móveis

Componentes

Peças

Materiais

Ferragens

Fitas

Usinagens

Detalhes Construtivos

Documentos

Blocos

Referências
```

---

# Página

## Templates

### ID

```text
PRJ-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para acelerar novos projetos.

### Tipos

```text
Briefing

Levantamento

Projeto

Ambiente

Móvel

Estrutura

Checklist

Documento

Cronograma
```

---

# Página

## Configurações

### ID

```text
PRJ-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Numeração dos Projetos

Status

Fases

Tipos de Projeto

Tipos de Ambiente

Tipos de Móvel

Categorias de Material

Categorias de Ferragem

Regras de Revisão

Regras de Aprovação

Regras de Liberação

Parâmetros do Plano de Corte

Templates

Checklists

Diretórios

Integrações
```

---

# Dialogs

```text
PRJ-DLG-001 Novo Projeto

PRJ-DLG-002 Editar Projeto

PRJ-DLG-003 Duplicar Projeto

PRJ-DLG-004 Alterar Status

PRJ-DLG-005 Alterar Responsável

PRJ-DLG-006 Alterar Prazo

PRJ-DLG-007 Novo Briefing

PRJ-DLG-008 Nova Visita

PRJ-DLG-009 Novo Levantamento

PRJ-DLG-010 Novo Ambiente

PRJ-DLG-011 Novo Móvel

PRJ-DLG-012 Novo Componente

PRJ-DLG-013 Nova Peça

PRJ-DLG-014 Selecionar Material

PRJ-DLG-015 Selecionar Ferragem

PRJ-DLG-016 Configurar Fita de Borda

PRJ-DLG-017 Configurar Usinagem

PRJ-DLG-018 Nova Revisão

PRJ-DLG-019 Comparar Revisões

PRJ-DLG-020 Solicitar Aprovação

PRJ-DLG-021 Aprovar Projeto

PRJ-DLG-022 Reprovar Projeto

PRJ-DLG-023 Nova Pendência

PRJ-DLG-024 Resolver Pendência

PRJ-DLG-025 Gerar Lista de Materiais

PRJ-DLG-026 Substituir Material

PRJ-DLG-027 Gerar Solicitação de Compra

PRJ-DLG-028 Gerar Plano de Corte

PRJ-DLG-029 Configurar Plano de Corte

PRJ-DLG-030 Visualizar Chapa

PRJ-DLG-031 Gerar Etiquetas

PRJ-DLG-032 Liberar para Compras

PRJ-DLG-033 Liberar para Produção

PRJ-DLG-034 Cancelar Liberação

PRJ-DLG-035 Adicionar Documento

PRJ-DLG-036 Upload de Arquivo

PRJ-DLG-037 Exportar Projeto

PRJ-DLG-038 Importar Projeto

PRJ-DLG-039 Arquivar Projeto

PRJ-DLG-040 Cancelar Projeto
```

---

# Wizards

```text
PRJ-WIZ-001 Assistente de Novo Projeto

PRJ-WIZ-002 Assistente de Briefing

PRJ-WIZ-003 Assistente de Levantamento Técnico

PRJ-WIZ-004 Assistente de Estrutura do Móvel

PRJ-WIZ-005 Assistente de Importação de Peças

PRJ-WIZ-006 Assistente de Lista de Materiais

PRJ-WIZ-007 Assistente de Plano de Corte

PRJ-WIZ-008 Assistente de Revisão

PRJ-WIZ-009 Assistente de Aprovação

PRJ-WIZ-010 Assistente de Liberação para Compras

PRJ-WIZ-011 Assistente de Liberação para Produção

PRJ-WIZ-012 Assistente de Encerramento do Projeto
```

---

# Componentes Específicos

```text
PRJ-CPT-001 Árvore do Projeto

PRJ-CPT-002 Editor de Estrutura

PRJ-CPT-003 Tabela de Peças

PRJ-CPT-004 Seletor de Materiais

PRJ-CPT-005 Seletor de Ferragens

PRJ-CPT-006 Editor de Fitas de Borda

PRJ-CPT-007 Editor de Usinagens

PRJ-CPT-008 Comparador de Revisões

PRJ-CPT-009 Visualizador de Plano de Corte

PRJ-CPT-010 Editor de Chapas

PRJ-CPT-011 Gerador de Etiquetas

PRJ-CPT-012 Checklist de Liberação

PRJ-CPT-013 Visualizador 3D

PRJ-CPT-014 Visualizador de PDF

PRJ-CPT-015 Timeline do Projeto

PRJ-CPT-016 Kanban de Pendências

PRJ-CPT-017 Cronograma do Projeto

PRJ-CPT-018 Gerenciador de Arquivos
```

Todos os estilos visuais, cores, fontes, ícones, dimensões, estados e imagens desses componentes deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
ProjectCreated

ProjectUpdated

ProjectDuplicated

ProjectSuspended

ProjectCancelled

ProjectArchived

BriefingCreated

BriefingCompleted

TechnicalVisitScheduled

TechnicalVisitCompleted

TechnicalSurveyCreated

TechnicalSurveyCompleted

EnvironmentCreated

FurnitureCreated

ComponentCreated

PartCreated

ProjectStructureGenerated

ProjectMaterialAdded

ProjectHardwareAdded

EdgeBandConfigured

MachiningConfigured

ProjectRevisionCreated

ProjectRevisionApproved

ProjectRevisionRejected

ProjectApprovalRequested

ProjectApproved

ProjectRejected

ProjectPendingIssueCreated

ProjectPendingIssueResolved

ProjectMaterialListGenerated

ProjectCuttingPlanGenerated

ProjectDocumentGenerated

ProjectReleasedForPurchasing

ProjectReleasedForProduction

ProjectReleaseCancelled

ProjectCompleted
```

---

# Automações

```text
Projeto criado

↓

Criar estrutura inicial de diretórios

↓

Criar timeline

↓

Criar checklist padrão

↓

Criar cronograma padrão

↓

Registrar auditoria
```

```text
Visita concluída

↓

Criar pendências encontradas

↓

Atualizar fase do projeto

↓

Notificar responsável
```

```text
Projeto aprovado

↓

Gerar contrato

↓

Liberar detalhamento executivo

↓

Notificar comercial
```

```text
Lista de materiais gerada

↓

Comparar com estoque

↓

Criar reservas

↓

Sugerir compras
```

```text
Projeto liberado para produção

↓

Criar solicitação ao PCP

↓

Disponibilizar documentos técnicos

↓

Bloquear revisão atual

↓

Notificar produção
```

---

# Integrações

```text
CRM

Comercial

Orçamentos

Contratos

Compras

Estoque

PCP

Produção

Qualidade

Expedição

Instalação

Financeiro

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização
```

---

# Permissões

```text
project.dashboard.read

project.project.read

project.project.create

project.project.update

project.project.duplicate

project.project.suspend

project.project.cancel

project.project.archive

project.briefing.manage

project.visit.manage

project.survey.manage

project.environment.manage

project.furniture.manage

project.component.manage

project.part.manage

project.structure.manage

project.material.manage

project.hardware.manage

project.edge_band.manage

project.machining.manage

project.revision.create

project.revision.compare

project.revision.approve

project.approval.request

project.approval.approve

project.approval.reject

project.pending.manage

project.schedule.manage

project.cost.read

project.material_list.generate

project.cutting_plan.generate

project.cutting_plan.edit

project.document.generate

project.file.manage

project.release.purchasing

project.release.production

project.report.read

project.report.export

project.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Ficha do Projeto

Briefing

Relatório de Visita

Levantamento Técnico

Relação de Ambientes

Relação de Móveis

Estrutura do Projeto

Lista de Componentes

Lista de Peças

Lista de Materiais

Lista de Ferragens

Lista de Fitas

Lista de Usinagens

Memorial Descritivo

Relatório de Revisões

Termo de Aprovação

Relatório de Pendências

Cronograma

Relatório de Custos Previstos

Plano de Corte

Etiquetas

Checklist de Conferência

Checklist de Liberação para Compras

Checklist de Liberação para Produção

Pacote Técnico de Produção
```

---

# Recursos de Inteligência Artificial

```text
Gerar resumo do briefing

Extrair requisitos de conversas

Classificar referências visuais

Sugerir perguntas faltantes

Detectar informações incompletas

Analisar levantamento técnico

Detectar incompatibilidades de medidas

Sugerir materiais

Sugerir ferragens

Comparar revisões

Resumir alterações

Detectar peças duplicadas

Detectar dimensões inconsistentes

Sugerir otimização de materiais

Analisar perdas no plano de corte

Estimar complexidade do projeto

Estimar prazo de desenvolvimento

Estimar prazo de produção

Identificar riscos

Gerar memorial descritivo

Gerar resumo executivo

Pesquisar informações do projeto por linguagem natural
```

A IA nunca poderá aprovar, liberar ou modificar automaticamente um projeto sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Todo projeto deverá estar vinculado a um Tenant.

2. Todo projeto deverá estar vinculado a um cliente antes de ser enviado para orçamento.

3. Um projeto poderá possuir vários ambientes.

4. Um ambiente poderá possuir vários móveis.

5. Um móvel poderá possuir vários componentes.

6. Um componente poderá possuir várias peças.

7. Toda peça deverá possuir material e dimensões válidas antes da geração da lista de materiais.

8. Uma alteração realizada após aprovação deverá gerar nova revisão.

9. Revisões aprovadas nunca poderão ser alteradas diretamente.

10. A liberação para produção deverá bloquear a revisão liberada.

11. Uma nova revisão após liberação deverá avaliar impactos em compras, estoque, prazo e produção.

12. Nenhum projeto poderá ser liberado para produção sem os checklists obrigatórios.

13. A lista de materiais deverá ser derivada da estrutura do projeto.

14. O plano de corte deverá ser derivado exclusivamente de peças válidas.

15. Toda substituição de material deverá registrar justificativa e responsável.

16. Todos os arquivos deverão possuir versionamento e histórico.

17. Nenhuma página do módulo poderá definir cores, fontes, ícones ou estilos fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Projetos passa a concentrar toda a definição comercial, técnica e executiva relacionada ao desenvolvimento do projeto.

Não deverá existir um módulo separado denominado Engenharia.

O módulo Projetos será a fonte oficial para:

```text
Ambientes

Móveis

Componentes

Peças

Materiais

Ferragens

Fitas

Usinagens

Revisões

Documentos Técnicos

Lista de Materiais

Plano de Corte

Liberações
```

Compras, Estoque, PCP e Produção deverão consumir as informações liberadas por Projetos.

Esses módulos nunca poderão modificar diretamente a estrutura técnica do projeto.

Qualquer necessidade de alteração deverá retornar ao módulo Projetos e gerar uma nova revisão.

---

# Próxima Etapa

```text
ETAPA 03-E

Catálogo Completo de Páginas

Orçamentos
```
---

# ETAPA 03-E

# Catálogo Completo de Páginas

# Orçamentos

## ID do Módulo

```text
ORC
```

---

# Objetivo

O módulo Orçamentos é responsável por transformar as informações comerciais e técnicas do projeto em uma proposta financeira clara, auditável e apresentável ao cliente.

Ele deverá calcular e organizar:

* materiais;
* ferragens;
* componentes;
* serviços;
* mão de obra;
* terceirizados;
* transporte;
* instalação;
* despesas;
* impostos;
* comissões;
* perdas;
* margem;
* desconto;
* preço final;
* condições de pagamento;
* prazo estimado.

O orçamento deverá permanecer vinculado ao cliente e, quando aplicável, ao projeto que originou sua composição.

Nenhum preço final deverá ser definido sem rastreabilidade de sua composição.

---

# Limites do Módulo

O módulo Orçamentos será responsável por definir:

```text
Quanto o projeto custa

Quanto será cobrado

Como o preço foi composto

Qual margem foi aplicada

Quais condições comerciais foram oferecidas

Qual versão foi apresentada ao cliente
```

O módulo Orçamentos não será responsável por:

```text
Cadastrar tecnicamente as peças

Comprar os materiais

Reservar estoque

Executar a produção

Registrar o recebimento financeiro

Emitir documentos fiscais
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Compras

Estoque

Produção

Financeiro

Fiscal
```

---

# Fluxo Principal

```text
Cliente

↓

Projeto

↓

Lista de Materiais

↓

Materiais

↓

Ferragens

↓

Mão de Obra

↓

Serviços Terceirizados

↓

Despesas

↓

Impostos

↓

Margem

↓

Preço Final

↓

Revisão

↓

Aprovação Interna

↓

Apresentação ao Cliente

↓

Negociação

↓

Aprovação do Cliente

↓

Conversão em Pedido

↓

Contrato
```

---

# Estrutura Geral

```text
ORC — Orçamentos

├── Dashboard de Orçamentos
├── Orçamentos
├── Cadastro do Orçamento
├── Composição de Custos
├── Materiais
├── Ferragens
├── Componentes
├── Mão de Obra
├── Serviços Terceirizados
├── Transporte
├── Instalação
├── Despesas
├── Impostos
├── Comissões
├── Perdas
├── Margens
├── Descontos
├── Condições de Pagamento
├── Parcelamento
├── Prazos
├── Revisões
├── Aprovações
├── Apresentações
├── Negociações
├── Comparativos
├── Templates
├── Tabelas de Preço
├── Simulações
├── Indicadores
├── Relatórios
└── Configurações
```

---

# Página

## Dashboard de Orçamentos

### ID

```text
ORC-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada da situação dos orçamentos da empresa.

### Componentes

```text
Orçamentos Criados

Orçamentos em Elaboração

Orçamentos Aguardando Aprovação Interna

Orçamentos Aguardando Apresentação

Orçamentos em Negociação

Orçamentos Aprovados

Orçamentos Reprovados

Orçamentos Vencidos

Valor Total Orçado

Valor Total Aprovado

Taxa de Conversão

Ticket Médio

Margem Média

Tempo Médio de Aprovação

Ranking por Vendedor

Orçamentos por Projetista

Alertas
```

### Filtros

```text
Período

Cliente

Projeto

Vendedor

Orçamentista

Status

Faixa de Valor

Margem

Origem

Filial

Tipo de Projeto
```

### Ações

```text
Novo Orçamento

Abrir Orçamento

Abrir Aprovações

Abrir Negociações

Abrir Indicadores

Exportar Dashboard

Atualizar Dados
```

---

# Página

## Orçamentos

### ID

```text
ORC-ORC-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar, pesquisar, filtrar e administrar todos os orçamentos.

### Visualizações

```text
Tabela

Cards

Kanban

Timeline

Calendário
```

### Colunas Principais

```text
Número

Versão

Cliente

Projeto

Responsável

Vendedor

Data de Criação

Data de Validade

Status

Valor de Custo

Valor de Venda

Margem

Desconto

Valor Final

Condição de Pagamento

Probabilidade de Aprovação
```

### Status

```text
Rascunho

Em Elaboração

Aguardando Dados

Aguardando Revisão

Aguardando Aprovação Interna

Aprovado Internamente

Aguardando Apresentação

Apresentado

Em Negociação

Revisão Solicitada

Aprovado pelo Cliente

Reprovado pelo Cliente

Vencido

Convertido em Pedido

Cancelado

Arquivado
```

### Ações

```text
Novo Orçamento

Abrir

Editar

Duplicar

Criar Nova Versão

Recalcular

Solicitar Revisão

Solicitar Aprovação

Aprovar

Reprovar

Apresentar ao Cliente

Registrar Negociação

Aplicar Desconto

Alterar Condição de Pagamento

Gerar Proposta

Gerar PDF

Enviar por Email

Enviar por WhatsApp

Compartilhar Link

Converter em Pedido

Gerar Contrato

Cancelar

Arquivar

Restaurar

Exportar

Imprimir
```

---

# Página

## Cadastro do Orçamento

### ID

```text
ORC-ORC-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações que compõem um orçamento.

### Abas

```text
Geral

Cliente

Projeto

Escopo

Ambientes

Itens

Materiais

Ferragens

Mão de Obra

Serviços

Transporte

Instalação

Despesas

Impostos

Comissões

Custos

Margens

Descontos

Condições de Pagamento

Parcelamento

Prazos

Documentos

Revisões

Aprovações

Negociações

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Versão

Título

Descrição

Cliente

Projeto

Contato Principal

Vendedor

Orçamentista

Responsável

Origem

Tipo de Orçamento

Status

Data de Criação

Data de Apresentação

Data de Validade

Probabilidade de Aprovação

Moeda

Observações Internas

Observações ao Cliente
```

### Aba Cliente

Informações:

```text
Dados do Cliente

Contatos

Endereço

Histórico de Orçamentos

Histórico de Compras

Condição Comercial Padrão

Tabela de Preço

Limite de Crédito

Pendências Financeiras
```

### Aba Projeto

Informações:

```text
Projeto Vinculado

Ambientes

Móveis

Revisão Técnica

Materiais Definidos

Ferragens Definidas

Lista de Materiais

Documentos

Arquivos

Pendências
```

### Aba Escopo

Informações:

```text
Itens Incluídos

Itens Não Incluídos

Serviços Incluídos

Serviços Não Incluídos

Responsabilidades da Empresa

Responsabilidades do Cliente

Premissas

Restrições

Garantias

Observações
```

### Aba Ambientes

Informações:

```text
Ambiente

Descrição

Valor de Custo

Valor de Venda

Margem

Desconto

Valor Final

Status
```

### Aba Itens

Informações:

```text
Código

Descrição

Ambiente

Categoria

Quantidade

Unidade

Custo Unitário

Preço Unitário

Desconto

Total

Margem
```

### Aba Materiais

Informações:

```text
Material

Fabricante

Linha

Cor

Espessura

Quantidade

Unidade

Custo Unitário

Perda

Custo Total

Preço Aplicado
```

### Aba Ferragens

Informações:

```text
Ferragem

Fabricante

Modelo

Quantidade

Custo Unitário

Custo Total

Preço Aplicado

Fornecedor Preferencial
```

### Aba Mão de Obra

Informações:

```text
Serviço

Categoria

Tempo Estimado

Quantidade de Pessoas

Custo por Hora

Custo Total

Preço Aplicado

Responsável
```

### Aba Serviços

Informações:

```text
Serviço

Prestador

Quantidade

Unidade

Custo

Prazo

Margem

Preço Final
```

### Aba Transporte

Informações:

```text
Origem

Destino

Distância

Veículo

Quantidade de Viagens

Pedágios

Combustível

Equipe

Custo Total

Preço Aplicado
```

### Aba Instalação

Informações:

```text
Quantidade de Dias

Quantidade de Pessoas

Hospedagem

Alimentação

Deslocamento

Ferramentas

Custos Adicionais

Custo Total

Preço Aplicado
```

### Aba Despesas

Informações:

```text
Descrição

Categoria

Tipo

Valor

Rateio

Aplicação

Observações
```

### Aba Impostos

Informações:

```text
Tributo

Base de Cálculo

Alíquota

Valor

Regime

Retenção

Observações
```

### Aba Comissões

Informações:

```text
Beneficiário

Tipo

Base de Cálculo

Percentual

Valor

Condição de Liberação

Status
```

### Aba Custos

Informações:

```text
Materiais

Ferragens

Mão de Obra

Serviços

Transporte

Instalação

Despesas

Impostos

Comissões

Perdas

Custos Indiretos

Custo Total
```

### Aba Margens

Informações:

```text
Margem Bruta

Margem de Contribuição

Margem Comercial

Markup

Margem por Ambiente

Margem por Item

Margem Mínima

Margem Aplicada
```

### Aba Descontos

Informações:

```text
Tipo

Motivo

Base

Percentual

Valor

Solicitante

Aprovador

Status

Impacto na Margem
```

### Aba Condições de Pagamento

Informações:

```text
Entrada

Parcelas

Periodicidade

Forma de Pagamento

Vencimentos

Juros

Multa

Desconto por Antecipação

Observações
```

### Aba Parcelamento

Informações:

```text
Parcela

Percentual

Valor

Vencimento

Forma de Pagamento

Evento de Cobrança

Observações
```

### Aba Prazos

Informações:

```text
Validade da Proposta

Prazo para Medição Final

Prazo para Detalhamento

Prazo para Compra

Prazo para Produção

Prazo para Instalação

Prazo Total Estimado

Condições que Alteram o Prazo
```

### Aba Documentos

Informações:

```text
Proposta Comercial

Memorial Descritivo

Resumo do Projeto

Condições Gerais

Termo de Aprovação

Contrato

Anexos

Imagens

Perspectivas
```

### Aba Revisões

Informações:

```text
Versão

Data

Autor

Motivo

Itens Alterados

Valor Anterior

Valor Atual

Impacto na Margem

Impacto no Prazo

Status
```

### Aba Aprovações

Informações:

```text
Aprovação de Custo

Aprovação de Margem

Aprovação de Desconto

Aprovação de Prazo

Aprovação de Condição Especial

Aprovação Comercial

Aprovação do Cliente
```

### Aba Negociações

Informações:

```text
Data

Responsável

Canal

Assunto

Solicitação do Cliente

Proposta da Empresa

Resultado

Próxima Ação

Prazo
```

### Aba Histórico

Informações:

```text
Alterações

Recalculos

Revisões

Aprovações

Apresentações

Negociações

Envios

Conversões

Cancelamentos
```

### Aba Timeline

Eventos:

```text
Orçamento Criado

Custos Calculados

Revisão Criada

Aprovação Solicitada

Aprovação Concedida

Proposta Gerada

Proposta Enviada

Proposta Apresentada

Negociação Registrada

Desconto Solicitado

Desconto Aprovado

Cliente Aprovou

Cliente Reprovou

Orçamento Convertido

Orçamento Vencido
```

---

# Página

## Composição de Custos

### ID

```text
ORC-CUS-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Consolidar e demonstrar todos os custos que compõem o orçamento.

### Grupos

```text
Materiais

Ferragens

Componentes

Mão de Obra

Terceirizados

Transporte

Instalação

Despesas

Impostos

Comissões

Perdas

Custos Indiretos
```

### Funcionalidades

```text
Recalcular

Detalhar

Agrupar

Ratear

Simular

Comparar

Exportar

Bloquear Valor

Desbloquear Valor

Atualizar Custo de Origem
```

---

# Página

## Materiais

### ID

```text
ORC-MAT-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar os materiais utilizados na composição financeira do orçamento.

### Funcionalidades

```text
Importar do Projeto

Adicionar Material

Substituir Material

Alterar Custo

Aplicar Perda

Aplicar Margem

Atualizar Preços

Agrupar por Fabricante

Agrupar por Categoria

Comparar Fornecedores
```

---

# Página

## Ferragens

### ID

```text
ORC-FER-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar as ferragens que compõem o orçamento.

---

# Página

## Componentes

### ID

```text
ORC-CMP-001
```

### Tipo

```text
Lista
```

### Objetivo

Orçar componentes completos ou subconjuntos reutilizáveis.

---

# Página

## Mão de Obra

### ID

```text
ORC-MDO-001
```

### Tipo

```text
Lista
```

### Objetivo

Calcular custos internos de execução.

### Categorias

```text
Medição

Projeto

Detalhamento

Corte

Usinagem

Fitagem

Montagem Interna

Acabamento

Limpeza

Embalagem

Carregamento

Transporte

Instalação

Assistência
```

---

# Página

## Serviços Terceirizados

### ID

```text
ORC-TER-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar serviços executados por terceiros.

### Exemplos

```text
Vidraçaria

Marmoraria

Serralheria

Pintura

Tapeçaria

Elétrica

Hidráulica

Frete

CNC Terceirizado

Instalação Terceirizada
```

---

# Página

## Transporte

### ID

```text
ORC-TRA-001
```

### Tipo

```text
Calculadora
```

### Objetivo

Calcular custos logísticos de entrega e deslocamento.

---

# Página

## Instalação

### ID

```text
ORC-INS-001
```

### Tipo

```text
Calculadora
```

### Objetivo

Calcular custos de montagem e instalação no local.

---

# Página

## Despesas

### ID

```text
ORC-DES-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar despesas diretas e rateios aplicáveis ao orçamento.

---

# Página

## Impostos

### ID

```text
ORC-IMP-001
```

### Tipo

```text
Calculadora
```

### Objetivo

Calcular tributos e retenções aplicáveis.

---

# Página

## Comissões

### ID

```text
ORC-COM-001
```

### Tipo

```text
Calculadora
```

### Objetivo

Calcular comissões comerciais previstas.

---

# Página

## Perdas

### ID

```text
ORC-PER-001
```

### Tipo

```text
Configuração
```

### Objetivo

Definir perdas previstas por categoria de custo.

### Exemplos

```text
Perda de Chapa

Perda de Fita

Perda de Ferragem

Quebra

Retrabalho

Ajustes

Sobra Não Aproveitável
```

---

# Página

## Margens

### ID

```text
ORC-MAR-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Definir e analisar as margens aplicadas ao orçamento.

### Funcionalidades

```text
Aplicar Margem Global

Aplicar Margem por Grupo

Aplicar Margem por Item

Validar Margem Mínima

Simular Cenários

Comparar Margens

Exibir Impacto
```

---

# Página

## Descontos

### ID

```text
ORC-DCT-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar descontos e seus impactos sobre margem e resultado.

---

# Página

## Condições de Pagamento

### ID

```text
ORC-CPG-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar condições comerciais oferecidas ao cliente.

### Exemplos

```text
À Vista

Entrada e Saldo na Entrega

Entrada e Parcelas

Parcelado no Cartão

Boleto

PIX

Financiamento

Condição Personalizada
```

---

# Página

## Parcelamento

### ID

```text
ORC-PAR-001
```

### Tipo

```text
Simulador
```

### Objetivo

Simular e estruturar parcelas do orçamento.

---

# Página

## Prazos

### ID

```text
ORC-PRA-001
```

### Tipo

```text
Configuração
```

### Objetivo

Definir prazos comerciais e operacionais apresentados ao cliente.

---

# Página

## Revisões

### ID

```text
ORC-REV-001
```

### Tipo

```text
Timeline
```

### Objetivo

Controlar versões e alterações do orçamento.

### Regras

```text
Nenhuma versão aprovada poderá ser alterada.

Toda alteração posterior deverá gerar nova versão.

A versão anterior deverá permanecer consultável.
```

---

# Página

## Aprovações

### ID

```text
ORC-APR-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar aprovações internas e externas.

### Tipos

```text
Custo

Margem

Desconto

Prazo

Pagamento

Condição Especial

Proposta

Cliente
```

---

# Página

## Apresentações

### ID

```text
ORC-APT-001
```

### Tipo

```text
Timeline
```

### Objetivo

Registrar cada apresentação realizada ao cliente.

### Informações

```text
Data

Participantes

Responsável

Versão Apresentada

Canal

Resultado

Comentários

Próxima Ação
```

---

# Página

## Negociações

### ID

```text
ORC-NEG-001
```

### Tipo

```text
Timeline
```

### Objetivo

Registrar todo o histórico de negociação do orçamento.

---

# Página

## Comparativos

### ID

```text
ORC-CMP-002
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Comparar versões, cenários e alternativas comerciais.

### Comparações

```text
Versão Anterior x Atual

Material A x Material B

Margem A x Margem B

À Vista x Parcelado

Com Desconto x Sem Desconto

Fornecedor A x Fornecedor B
```

---

# Página

## Templates

### ID

```text
ORC-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar estruturas reutilizáveis de orçamento e proposta.

### Tipos

```text
Orçamento

Proposta

Condição Comercial

Parcelamento

Escopo

Observações

Apresentação
```

---

# Página

## Tabelas de Preço

### ID

```text
ORC-TAB-001
```

### Tipo

```text
Lista
```

### Objetivo

Administrar preços e regras aplicáveis à composição comercial.

---

# Página

## Simulações

### ID

```text
ORC-SIM-001
```

### Tipo

```text
Simulador
```

### Objetivo

Criar cenários sem alterar o orçamento oficial.

### Cenários

```text
Alteração de Material

Alteração de Ferragem

Alteração de Margem

Aplicação de Desconto

Alteração de Prazo

Alteração de Pagamento

Alteração de Escopo
```

---

# Página

## Indicadores

### ID

```text
ORC-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Quantidade de Orçamentos

Valor Orçado

Valor Aprovado

Taxa de Conversão

Ticket Médio

Margem Média

Desconto Médio

Tempo Médio de Elaboração

Tempo Médio de Aprovação

Orçamentos Vencidos

Motivos de Perda

Conversão por Vendedor

Conversão por Origem

Conversão por Tipo de Projeto
```

---

# Página

## Relatórios

### ID

```text
ORC-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Orçamentos por Status

Orçamentos por Cliente

Orçamentos por Projeto

Orçamentos por Vendedor

Orçamentos Aprovados

Orçamentos Reprovados

Orçamentos Vencidos

Composição de Custos

Margens

Descontos

Condições de Pagamento

Conversão

Motivos de Perda

Histórico de Revisões

Comparativo Orçado x Realizado
```

---

# Página

## Configurações

### ID

```text
ORC-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Numeração

Validade Padrão

Margem Mínima

Margem Padrão

Markup Padrão

Perdas Padrão

Impostos

Comissões

Despesas Fixas

Custos Indiretos

Transporte

Mão de Obra

Condições de Pagamento

Regras de Desconto

Regras de Aprovação

Templates

Modelos de Proposta

Casas Decimais

Arredondamentos
```

---

# Dialogs

```text
ORC-DLG-001 Novo Orçamento

ORC-DLG-002 Selecionar Cliente

ORC-DLG-003 Selecionar Projeto

ORC-DLG-004 Importar Estrutura do Projeto

ORC-DLG-005 Adicionar Item

ORC-DLG-006 Adicionar Material

ORC-DLG-007 Substituir Material

ORC-DLG-008 Adicionar Ferragem

ORC-DLG-009 Adicionar Mão de Obra

ORC-DLG-010 Adicionar Serviço Terceirizado

ORC-DLG-011 Calcular Transporte

ORC-DLG-012 Calcular Instalação

ORC-DLG-013 Adicionar Despesa

ORC-DLG-014 Calcular Imposto

ORC-DLG-015 Calcular Comissão

ORC-DLG-016 Aplicar Perda

ORC-DLG-017 Aplicar Margem

ORC-DLG-018 Aplicar Desconto

ORC-DLG-019 Solicitar Aprovação de Desconto

ORC-DLG-020 Selecionar Condição de Pagamento

ORC-DLG-021 Configurar Parcelamento

ORC-DLG-022 Alterar Prazo

ORC-DLG-023 Criar Nova Versão

ORC-DLG-024 Comparar Versões

ORC-DLG-025 Solicitar Aprovação

ORC-DLG-026 Aprovar Orçamento

ORC-DLG-027 Reprovar Orçamento

ORC-DLG-028 Registrar Apresentação

ORC-DLG-029 Registrar Negociação

ORC-DLG-030 Gerar Proposta

ORC-DLG-031 Enviar por Email

ORC-DLG-032 Enviar por WhatsApp

ORC-DLG-033 Compartilhar Link

ORC-DLG-034 Converter em Pedido

ORC-DLG-035 Gerar Contrato

ORC-DLG-036 Cancelar Orçamento

ORC-DLG-037 Arquivar Orçamento

ORC-DLG-038 Exportar Orçamento

ORC-DLG-039 Importar Orçamento

ORC-DLG-040 Simular Cenário
```

---

# Wizards

```text
ORC-WIZ-001 Assistente de Novo Orçamento

ORC-WIZ-002 Assistente de Importação do Projeto

ORC-WIZ-003 Assistente de Composição de Custos

ORC-WIZ-004 Assistente de Formação de Preço

ORC-WIZ-005 Assistente de Condição de Pagamento

ORC-WIZ-006 Assistente de Geração de Proposta

ORC-WIZ-007 Assistente de Revisão

ORC-WIZ-008 Assistente de Aprovação

ORC-WIZ-009 Assistente de Apresentação

ORC-WIZ-010 Assistente de Conversão em Pedido
```

---

# Componentes Específicos

```text
ORC-CPT-001 Resumo Financeiro do Orçamento

ORC-CPT-002 Árvore de Composição de Custos

ORC-CPT-003 Calculadora de Margem

ORC-CPT-004 Calculadora de Markup

ORC-CPT-005 Simulador de Desconto

ORC-CPT-006 Simulador de Parcelamento

ORC-CPT-007 Comparador de Versões

ORC-CPT-008 Comparador de Cenários

ORC-CPT-009 Indicador de Margem Mínima

ORC-CPT-010 Indicador de Validade

ORC-CPT-011 Editor de Escopo

ORC-CPT-012 Gerador de Proposta

ORC-CPT-013 Preview da Proposta

ORC-CPT-014 Timeline de Negociação

ORC-CPT-015 Checklist de Aprovação
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
BudgetCreated

BudgetUpdated

BudgetRecalculated

BudgetVersionCreated

BudgetCostImported

BudgetMaterialAdded

BudgetMaterialReplaced

BudgetLaborCalculated

BudgetThirdPartyServiceAdded

BudgetTransportationCalculated

BudgetInstallationCalculated

BudgetTaxCalculated

BudgetCommissionCalculated

BudgetMarginApplied

BudgetDiscountRequested

BudgetDiscountApproved

BudgetDiscountRejected

BudgetApprovalRequested

BudgetInternallyApproved

BudgetInternallyRejected

BudgetProposalGenerated

BudgetSent

BudgetPresented

BudgetNegotiationRegistered

BudgetCustomerApproved

BudgetCustomerRejected

BudgetExpired

BudgetConvertedToSalesOrder

BudgetContractGenerated

BudgetCancelled

BudgetArchived
```

---

# Automações

```text
Orçamento criado

↓

Carregar parâmetros padrão

↓

Criar versão inicial

↓

Criar timeline

↓

Criar checklist

↓

Registrar auditoria
```

```text
Projeto vinculado

↓

Importar ambientes

↓

Importar materiais

↓

Importar ferragens

↓

Importar serviços

↓

Recalcular custos
```

```text
Desconto solicitado

↓

Validar limite do usuário

↓

Encaminhar para aprovação

↓

Notificar aprovador
```

```text
Proposta enviada

↓

Registrar envio

↓

Agendar follow-up

↓

Atualizar CRM
```

```text
Orçamento aprovado pelo cliente

↓

Bloquear versão aprovada

↓

Converter em pedido

↓

Iniciar contrato

↓

Atualizar CRM

↓

Notificar Projetos e Financeiro
```

```text
Orçamento vencido

↓

Alterar status

↓

Notificar responsável

↓

Criar tarefa de contato
```

---

# Integrações

```text
CRM

Projetos

Comercial

Contratos

Compras

Estoque

Produção

Financeiro

Fiscal

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização
```

---

# Permissões

```text
budget.dashboard.read

budget.budget.read

budget.budget.create

budget.budget.update

budget.budget.duplicate

budget.budget.recalculate

budget.budget.version.create

budget.cost.read

budget.cost.update

budget.material.manage

budget.hardware.manage

budget.labor.manage

budget.third_party.manage

budget.transport.manage

budget.installation.manage

budget.expense.manage

budget.tax.manage

budget.commission.manage

budget.loss.manage

budget.margin.read

budget.margin.update

budget.discount.apply

budget.discount.request

budget.discount.approve

budget.payment_terms.manage

budget.installments.manage

budget.deadline.manage

budget.approval.request

budget.approval.approve

budget.approval.reject

budget.proposal.generate

budget.proposal.send

budget.presentation.register

budget.negotiation.manage

budget.customer_approval.register

budget.sales_order.convert

budget.contract.generate

budget.budget.cancel

budget.budget.archive

budget.report.read

budget.report.export

budget.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Orçamento Detalhado

Orçamento Resumido

Proposta Comercial

Resumo por Ambiente

Resumo por Categoria

Composição de Custos

Lista de Materiais Orçados

Lista de Ferragens Orçadas

Resumo de Mão de Obra

Resumo de Serviços Terceirizados

Simulação de Pagamento

Cronograma Estimado

Memorial Descritivo

Condições Gerais

Termo de Aprovação

Comparativo de Versões

Relatório de Margem

Relatório de Descontos

Histórico de Negociação
```

---

# Recursos de Inteligência Artificial

```text
Gerar descrição comercial

Gerar resumo do orçamento

Gerar proposta comercial

Adaptar linguagem ao perfil do cliente

Detectar itens ausentes

Detectar custos incompatíveis

Detectar margem abaixo do padrão

Sugerir margem

Sugerir desconto máximo

Sugerir condição de pagamento

Comparar versões

Resumir alterações

Analisar probabilidade de aprovação

Identificar riscos da negociação

Sugerir próxima ação

Gerar mensagem de apresentação

Gerar email de follow-up

Explicar composição de preço

Pesquisar orçamentos em linguagem natural
```

A IA nunca poderá aprovar descontos, modificar preços finais, alterar margens ou converter o orçamento em pedido sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Todo orçamento deverá pertencer a um Tenant.

2. Todo orçamento deverá estar vinculado a um cliente.

3. O vínculo com projeto será obrigatório para orçamentos baseados em projetos sob encomenda.

4. Todo orçamento deverá possuir uma versão.

5. Versões aprovadas não poderão ser alteradas diretamente.

6. Qualquer modificação após apresentação deverá gerar nova versão quando alterar escopo, custo, preço, prazo ou condição comercial.

7. Custos importados do projeto deverão manter referência à origem.

8. Valores monetários deverão utilizar `Decimal`.

9. O orçamento deverá registrar custo total, preço total e margem.

10. Margens abaixo do limite configurado deverão exigir aprovação.

11. Descontos acima do limite do usuário deverão exigir aprovação.

12. Nenhum orçamento poderá ser apresentado sem validade definida.

13. Nenhum orçamento poderá ser convertido em pedido sem aprovação do cliente.

14. A conversão em pedido deverá utilizar exclusivamente a versão aprovada.

15. O histórico de versões deverá permanecer imutável.

16. Toda alteração de preço deverá registrar usuário, data, motivo e impacto na margem.

17. Custos de materiais e ferragens deverão indicar a data da última atualização.

18. O orçamento deverá permitir composição por ambiente, móvel, grupo ou item.

19. Nenhum componente visual poderá definir aparência fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Orçamentos será a fonte oficial da formação de preço e das propostas comerciais.

O módulo Projetos fornecerá quantidades, materiais, ferragens, estruturas e serviços previstos.

O módulo Orçamentos será responsável por aplicar:

```text
Custos

Perdas

Despesas

Impostos

Comissões

Margens

Descontos

Condições de Pagamento

Preço Final
```

O módulo Comercial deverá consumir somente a versão aprovada do orçamento para criar o pedido.

Financeiro e Fiscal deverão utilizar as condições e valores formalizados no pedido e no contrato, sem modificar retroativamente o orçamento aprovado.

---

# Próxima Etapa

```text
ETAPA 03-F

Catálogo Completo de Páginas

Compras
```
---

# ETAPA 03-F

# Catálogo Completo de Páginas

# Compras

## ID do Módulo

```text
COM
```

---

# Objetivo

O módulo Compras é responsável por planejar, solicitar, cotar, aprovar, adquirir e acompanhar todos os materiais, ferragens, serviços e recursos necessários para a operação da empresa.

Ele deverá receber demandas originadas por:

* projetos;
* estoque;
* produção;
* manutenção;
* administração;
* solicitações manuais;
* contratos recorrentes;
* necessidades emergenciais.

O módulo deverá garantir rastreabilidade desde a identificação da necessidade até o recebimento, conferência e encerramento da compra.

Nenhuma compra deverá ocorrer sem origem, responsável, justificativa e histórico.

---

# Limites do Módulo

O módulo Compras será responsável por:

```text
Identificar necessidades de aquisição

Consolidar solicitações

Selecionar fornecedores

Solicitar e registrar cotações

Comparar propostas

Conduzir aprovações

Emitir pedidos de compra

Acompanhar prazos

Registrar recebimentos comerciais

Gerenciar devoluções e ocorrências

Avaliar fornecedores
```

O módulo Compras não será responsável por:

```text
Definir tecnicamente o material do projeto

Alterar a estrutura técnica do produto

Controlar o saldo físico oficial do estoque

Realizar pagamento ao fornecedor

Registrar documentos fiscais definitivamente

Executar a produção
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Estoque

Financeiro

Fiscal

Produção
```

---

# Fluxo Principal

```text
Necessidade Identificada

↓

Solicitação de Compra

↓

Consolidação das Necessidades

↓

Validação de Estoque

↓

Seleção de Fornecedores

↓

Solicitação de Cotação

↓

Recebimento das Propostas

↓

Mapa Comparativo

↓

Negociação

↓

Aprovação

↓

Pedido de Compra

↓

Envio ao Fornecedor

↓

Confirmação do Fornecedor

↓

Acompanhamento

↓

Recebimento

↓

Conferência

↓

Entrada no Estoque

↓

Financeiro

↓

Fiscal

↓

Encerramento
```

---

# Estrutura Geral

```text
COM — Compras

├── Dashboard de Compras
├── Necessidades de Compra
├── Solicitações de Compra
├── Consolidação de Demandas
├── Cotações
├── Solicitações de Cotação
├── Propostas de Fornecedores
├── Mapas Comparativos
├── Negociações
├── Aprovações
├── Pedidos de Compra
├── Acompanhamento de Pedidos
├── Recebimentos
├── Conferências
├── Divergências
├── Devoluções
├── Compras Emergenciais
├── Contratos de Fornecimento
├── Fornecedores
├── Contatos de Fornecedores
├── Produtos por Fornecedor
├── Tabelas de Preço
├── Prazos de Fornecimento
├── Avaliação de Fornecedores
├── Histórico de Preços
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
```

---

# Página

## Dashboard de Compras

### ID

```text
COM-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada das demandas, cotações, pedidos, atrasos, recebimentos e desempenho dos fornecedores.

### Componentes

```text
Solicitações Pendentes

Solicitações Urgentes

Cotações em Aberto

Cotações Vencendo

Aprovações Pendentes

Pedidos Aguardando Envio

Pedidos Aguardando Confirmação

Pedidos em Atraso

Recebimentos Previstos

Divergências em Aberto

Compras por Projeto

Compras por Fornecedor

Valor Comprado no Período

Economia em Negociações

Prazo Médio de Entrega

Ranking de Fornecedores

Alertas
```

### Filtros

```text
Período

Fornecedor

Projeto

Solicitante

Comprador

Status

Prioridade

Categoria

Filial

Centro de Custo

Data Prevista
```

### Ações

```text
Nova Solicitação

Nova Cotação

Novo Pedido

Abrir Aprovações

Abrir Atrasos

Abrir Recebimentos

Abrir Divergências

Exportar Dashboard

Atualizar Indicadores
```

---

# Página

## Necessidades de Compra

### ID

```text
COM-NEC-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar todas as necessidades de aquisição identificadas pelo sistema ou pelos usuários.

### Origens

```text
Projeto

Lista de Materiais

Estoque Mínimo

Produção

Manutenção

Solicitação Manual

Contrato Recorrente

Compra Emergencial

Consumo Previsto

Reposição
```

### Colunas

```text
Origem

Documento de Origem

Item

Descrição

Quantidade Necessária

Quantidade Disponível

Quantidade Reservada

Quantidade a Comprar

Unidade

Data Necessária

Prioridade

Solicitante

Projeto

Status
```

### Status

```text
Identificada

Em Análise

Atendida por Estoque

Aguardando Solicitação

Solicitação Criada

Em Cotação

Pedido Emitido

Parcialmente Atendida

Atendida

Cancelada
```

### Ações

```text
Analisar

Agrupar

Criar Solicitação

Atender com Estoque

Alterar Quantidade

Alterar Prioridade

Alterar Data Necessária

Vincular Projeto

Cancelar

Abrir Origem
```

---

# Página

## Solicitações de Compra

### ID

```text
COM-SOL-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar formalmente pedidos internos de aquisição.

### Visualizações

```text
Tabela

Cards

Kanban

Timeline
```

### Colunas

```text
Número

Solicitante

Departamento

Projeto

Centro de Custo

Data

Data Necessária

Prioridade

Quantidade de Itens

Valor Estimado

Status

Aprovador

Comprador
```

### Status

```text
Rascunho

Aguardando Aprovação

Aprovada

Reprovada

Em Cotação

Parcialmente Cotada

Cotada

Convertida em Pedido

Parcialmente Atendida

Atendida

Cancelada

Arquivada
```

### Ações

```text
Nova Solicitação

Abrir

Editar

Duplicar

Adicionar Item

Remover Item

Importar Necessidades

Solicitar Aprovação

Aprovar

Reprovar

Encaminhar para Cotação

Converter em Pedido

Cancelar

Arquivar

Exportar

Imprimir
```

---

# Página

## Cadastro da Solicitação de Compra

### ID

```text
COM-SOL-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações da solicitação de compra.

### Abas

```text
Geral

Itens

Origem

Projeto

Estoque

Aprovações

Cotações

Pedidos

Recebimentos

Documentos

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Solicitante

Departamento

Filial

Centro de Custo

Projeto

Tipo de Compra

Prioridade

Data da Solicitação

Data Necessária

Justificativa

Comprador Responsável

Status

Observações
```

### Aba Itens

Campos:

```text
Item

Descrição

Categoria

Especificação

Quantidade

Unidade

Quantidade Disponível

Quantidade Reservada

Quantidade a Comprar

Data Necessária

Fornecedor Sugerido

Marca Preferencial

Modelo Preferencial

Substituição Permitida

Observações
```

### Aba Origem

Informações:

```text
Tipo de Origem

Documento de Origem

Projeto

Ambiente

Móvel

Ordem de Produção

Manutenção

Solicitação Manual

Responsável pela Origem
```

### Aba Estoque

Informações:

```text
Saldo Atual

Saldo Disponível

Saldo Reservado

Estoque Mínimo

Ponto de Reposição

Pedidos em Aberto

Consumo Médio

Cobertura Estimada
```

### Aba Aprovações

Informações:

```text
Tipo de Aprovação

Solicitante

Aprovador

Data

Status

Motivo

Comentário

Limite de Alçada
```

### Aba Cotações

Informações:

```text
Cotação

Fornecedores

Data de Envio

Prazo de Resposta

Status

Melhor Proposta

Valor
```

### Aba Pedidos

Informações:

```text
Pedido de Compra

Fornecedor

Data

Valor

Status

Previsão de Entrega
```

### Aba Recebimentos

Informações:

```text
Recebimento

Data

Quantidade Recebida

Quantidade Pendente

Situação

Divergências
```

---

# Página

## Consolidação de Demandas

### ID

```text
COM-CON-001
```

### Tipo

```text
Painel
```

### Objetivo

Agrupar necessidades semelhantes para reduzir compras fragmentadas e melhorar o poder de negociação.

### Critérios de Consolidação

```text
Item

Material

Categoria

Fornecedor

Projeto

Prazo

Filial

Centro de Custo

Unidade

Marca

Especificação
```

### Funcionalidades

```text
Agrupar Demandas

Separar Demandas

Consolidar Quantidades

Alterar Data de Compra

Selecionar Solicitações

Criar Cotação

Criar Pedido

Visualizar Origem

Exportar Consolidação
```

---

# Página

## Cotações

### ID

```text
COM-COT-001
```

### Tipo

```text
Lista
```

### Objetivo

Administrar todos os processos de cotação.

### Colunas

```text
Número

Descrição

Comprador

Data de Abertura

Prazo de Resposta

Quantidade de Fornecedores

Quantidade de Itens

Status

Melhor Valor

Economia Estimada

Solicitação de Origem
```

### Status

```text
Rascunho

Preparando

Enviada

Aguardando Respostas

Parcialmente Respondida

Respondida

Em Análise

Em Negociação

Aguardando Aprovação

Aprovada

Convertida em Pedido

Encerrada

Cancelada
```

### Ações

```text
Nova Cotação

Abrir

Editar

Duplicar

Adicionar Fornecedor

Adicionar Item

Enviar Solicitação

Registrar Proposta

Comparar

Negociar

Solicitar Aprovação

Aprovar

Converter em Pedido

Encerrar

Cancelar

Exportar

Imprimir
```

---

# Página

## Cadastro da Cotação

### ID

```text
COM-COT-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Registrar fornecedores, itens, propostas, condições comerciais e decisões do processo de cotação.

### Abas

```text
Geral

Itens

Fornecedores

Propostas

Comparativo

Negociações

Aprovações

Documentos

Histórico

Timeline
```

### Aba Geral

Campos:

```text
Número

Descrição

Comprador

Solicitações Vinculadas

Data de Abertura

Prazo de Resposta

Data Necessária

Prioridade

Moeda

Status

Observações Internas

Mensagem ao Fornecedor
```

### Aba Itens

Campos:

```text
Item

Descrição

Especificação

Quantidade

Unidade

Marca Preferencial

Modelo Preferencial

Substituição Permitida

Data Necessária

Local de Entrega
```

### Aba Fornecedores

Campos:

```text
Fornecedor

Contato

Email

Telefone

Itens Cotados

Data de Envio

Data de Visualização

Prazo de Resposta

Status
```

### Aba Propostas

Campos:

```text
Fornecedor

Item

Marca

Modelo

Quantidade Disponível

Preço Unitário

Desconto

Impostos

Frete

Prazo de Entrega

Condição de Pagamento

Validade

Observações
```

### Aba Comparativo

Informações:

```text
Menor Preço

Menor Custo Total

Melhor Prazo

Melhor Condição de Pagamento

Melhor Avaliação

Atendimento da Especificação

Fornecedor Recomendado

Economia Estimada
```

### Aba Negociações

Informações:

```text
Data

Fornecedor

Responsável

Condição Anterior

Nova Condição

Economia

Prazo Alterado

Resultado

Observações
```

---

# Página

## Solicitações de Cotação

### ID

```text
COM-SCT-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar o envio das demandas aos fornecedores e o retorno das propostas.

### Funcionalidades

```text
Gerar Solicitação

Enviar por Email

Enviar por WhatsApp

Compartilhar Link

Reenviar

Registrar Retorno

Prorrogar Prazo

Cancelar Envio

Visualizar Histórico
```

---

# Página

## Propostas de Fornecedores

### ID

```text
COM-PRF-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar e organizar todas as propostas comerciais recebidas.

### Fontes

```text
Portal do Fornecedor

Email

WhatsApp

Telefone

Documento PDF

Planilha

Registro Manual
```

### Funcionalidades

```text
Registrar Proposta

Importar PDF

Importar Planilha

Vincular Cotação

Validar Dados

Solicitar Correção

Aprovar Proposta

Rejeitar Proposta

Arquivar
```

---

# Página

## Mapas Comparativos

### ID

```text
COM-MAP-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Comparar fornecedores e propostas com base em preço, prazo, qualidade e condições comerciais.

### Critérios

```text
Preço Unitário

Custo Total

Frete

Impostos

Prazo

Pagamento

Validade

Marca

Modelo

Qualidade

Avaliação do Fornecedor

Atendimento da Especificação

Histórico de Atrasos
```

### Funcionalidades

```text
Selecionar Critérios

Aplicar Pesos

Comparar Fornecedores

Dividir Compra

Selecionar Vencedor

Justificar Escolha

Gerar Relatório

Solicitar Aprovação
```

---

# Página

## Negociações

### ID

```text
COM-NEG-001
```

### Tipo

```text
Timeline
```

### Objetivo

Registrar todo o histórico de negociação com fornecedores.

### Informações

```text
Fornecedor

Data

Canal

Responsável

Condição Inicial

Condição Negociada

Economia Obtida

Prazo

Pagamento

Frete

Resultado

Próxima Ação
```

---

# Página

## Aprovações

### ID

```text
COM-APR-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar aprovações de solicitações, cotações, pedidos e condições especiais.

### Tipos

```text
Solicitação de Compra

Fornecedor Único

Compra sem Cotação

Compra Emergencial

Valor Acima da Alçada

Fornecedor Não Homologado

Condição Especial

Antecipação

Pedido de Compra

Cancelamento
```

---

# Página

## Pedidos de Compra

### ID

```text
COM-PED-001
```

### Tipo

```text
Lista
```

### Objetivo

Administrar as compras formalizadas junto aos fornecedores.

### Visualizações

```text
Tabela

Cards

Kanban

Timeline

Calendário de Entregas
```

### Colunas

```text
Número

Fornecedor

Comprador

Data de Emissão

Valor

Condição de Pagamento

Previsão de Entrega

Projeto

Centro de Custo

Status

Percentual Recebido

Atraso
```

### Status

```text
Rascunho

Aguardando Aprovação

Aprovado

Enviado

Aguardando Confirmação

Confirmado

Em Separação

Em Transporte

Parcialmente Recebido

Recebido

Com Divergência

Devolvido Parcialmente

Concluído

Cancelado
```

### Ações

```text
Novo Pedido

Abrir

Editar

Duplicar

Solicitar Aprovação

Aprovar

Reprovar

Enviar ao Fornecedor

Registrar Confirmação

Alterar Previsão

Registrar Ocorrência

Registrar Recebimento

Cancelar

Encerrar

Gerar PDF

Enviar por Email

Enviar por WhatsApp

Exportar

Imprimir
```

---

# Página

## Cadastro do Pedido de Compra

### ID

```text
COM-PED-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as condições comerciais e operacionais do pedido de compra.

### Abas

```text
Geral

Fornecedor

Itens

Entregas

Pagamento

Documentos

Aprovações

Recebimentos

Divergências

Devoluções

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Fornecedor

Comprador

Filial

Centro de Custo

Projeto

Cotação de Origem

Solicitação de Origem

Data de Emissão

Data de Entrega

Prioridade

Moeda

Status

Observações Internas

Observações ao Fornecedor
```

### Aba Fornecedor

Informações:

```text
Razão Social

Nome Fantasia

CNPJ

Contato

Email

Telefone

Endereço

Avaliação

Prazo Médio

Condição Padrão

Histórico de Atrasos
```

### Aba Itens

Campos:

```text
Item

Descrição

Especificação

Marca

Modelo

Quantidade

Unidade

Preço Unitário

Desconto

Impostos

Frete Rateado

Total

Projeto

Ambiente

Data Necessária
```

### Aba Entregas

Informações:

```text
Local de Entrega

Data Prevista

Janela de Recebimento

Responsável

Transportadora

Código de Rastreio

Status

Quantidade Prevista

Quantidade Recebida
```

### Aba Pagamento

Informações:

```text
Condição de Pagamento

Entrada

Parcelas

Vencimentos

Forma de Pagamento

Dados Bancários

Observações
```

### Aba Aprovações

Informações:

```text
Solicitante

Aprovador

Alçada

Data

Status

Motivo

Comentário
```

---

# Página

## Acompanhamento de Pedidos

### ID

```text
COM-ACO-001
```

### Tipo

```text
Kanban
```

### Objetivo

Acompanhar o andamento dos pedidos até a entrega completa.

### Etapas

```text
Aguardando Envio

Enviado

Aguardando Confirmação

Confirmado

Em Produção pelo Fornecedor

Em Separação

Faturado

Em Transporte

Atrasado

Parcialmente Recebido

Recebido

Concluído
```

### Funcionalidades

```text
Atualizar Status

Registrar Contato

Cobrar Fornecedor

Alterar Previsão

Adicionar Rastreio

Registrar Ocorrência

Notificar Projeto

Notificar Produção

Abrir Recebimento
```

---

# Página

## Recebimentos

### ID

```text
COM-REC-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar a chegada dos materiais e serviços comprados.

### Tipos

```text
Recebimento Total

Recebimento Parcial

Recebimento Antecipado

Recebimento com Divergência

Recebimento de Serviço
```

### Status

```text
Aguardando

Em Conferência

Conferido

Com Divergência

Aceito Parcialmente

Recusado

Finalizado
```

### Ações

```text
Novo Recebimento

Selecionar Pedido

Registrar Quantidades

Registrar Lote

Registrar Nota Fiscal

Adicionar Fotos

Conferir

Aceitar

Aceitar Parcialmente

Recusar

Registrar Divergência

Enviar ao Estoque

Enviar ao Fiscal

Finalizar
```

---

# Página

## Conferências

### ID

```text
COM-CNF-001
```

### Tipo

```text
Checklist
```

### Objetivo

Conferir material, quantidade, especificação, qualidade e documentação do recebimento.

### Itens de Conferência

```text
Fornecedor

Pedido

Nota Fiscal

Quantidade

Unidade

Marca

Modelo

Cor

Espessura

Dimensões

Integridade

Qualidade

Lote

Validade

Embalagem

Documentos

Certificados
```

---

# Página

## Divergências

### ID

```text
COM-DIV-001
```

### Tipo

```text
Kanban
```

### Objetivo

Registrar e acompanhar problemas identificados em cotações, pedidos e recebimentos.

### Tipos

```text
Quantidade Incorreta

Item Incorreto

Marca Divergente

Modelo Divergente

Cor Divergente

Dimensão Divergente

Avaria

Defeito

Preço Divergente

Prazo Descumprido

Nota Fiscal Divergente

Falta de Documento
```

### Status

```text
Nova

Em Análise

Aguardando Fornecedor

Aguardando Devolução

Aguardando Reposição

Em Correção

Resolvida

Cancelada
```

---

# Página

## Devoluções

### ID

```text
COM-DEV-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar devoluções totais ou parciais aos fornecedores.

### Motivos

```text
Avaria

Defeito

Item Incorreto

Quantidade Excedente

Especificação Divergente

Cancelamento

Troca

Problema Fiscal
```

### Funcionalidades

```text
Nova Devolução

Selecionar Recebimento

Selecionar Itens

Registrar Motivo

Gerar Documento

Agendar Coleta

Registrar Envio

Acompanhar Reposição

Finalizar
```

---

# Página

## Compras Emergenciais

### ID

```text
COM-EME-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar aquisições urgentes que não podem seguir integralmente o fluxo normal.

### Regras

```text
Justificativa obrigatória

Aprovação obrigatória

Fornecedor identificado

Valor registrado

Origem registrada

Regularização posterior obrigatória
```

---

# Página

## Contratos de Fornecimento

### ID

```text
COM-CTR-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar acordos recorrentes de fornecimento.

### Informações

```text
Fornecedor

Objeto

Produtos

Preços

Reajustes

Vigência

Quantidade Mínima

Quantidade Máxima

Prazo

Pagamento

SLA

Penalidades

Renovação
```

---

# Página

## Fornecedores

### ID

```text
COM-FOR-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar fornecedores de materiais, serviços e recursos.

### Subpáginas

```text
Cadastro

Contatos

Produtos

Preços

Documentos

Certificações

Pedidos

Recebimentos

Divergências

Devoluções

Avaliações

Financeiro

Histórico

Timeline
```

### Status

```text
Em Cadastro

Aguardando Homologação

Homologado

Homologado com Restrição

Bloqueado

Inativo

Arquivado
```

### Ações

```text
Novo Fornecedor

Editar

Homologar

Bloquear

Desbloquear

Inativar

Reativar

Adicionar Contato

Adicionar Produto

Solicitar Cotação

Criar Pedido

Avaliar

Exportar

Importar
```

---

# Página

## Cadastro do Fornecedor

### ID

```text
COM-FOR-002
```

### Tipo

```text
Cadastro
```

### Abas

```text
Geral

Contatos

Endereços

Produtos

Condições Comerciais

Documentos

Certificações

Dados Bancários

Pedidos

Recebimentos

Avaliações

Divergências

Financeiro

Histórico

Timeline

Auditoria
```

---

# Página

## Contatos de Fornecedores

### ID

```text
COM-CTT-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar representantes, vendedores e demais contatos dos fornecedores.

---

# Página

## Produtos por Fornecedor

### ID

```text
COM-PFO-001
```

### Tipo

```text
Lista
```

### Objetivo

Relacionar itens internos aos códigos, marcas, modelos e condições dos fornecedores.

### Campos

```text
Produto Interno

Fornecedor

Código do Fornecedor

Descrição do Fornecedor

Marca

Modelo

Unidade

Embalagem

Quantidade Mínima

Preço Atual

Prazo

Disponibilidade

Última Atualização
```

---

# Página

## Tabelas de Preço

### ID

```text
COM-TAB-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar tabelas comerciais recebidas dos fornecedores.

### Funcionalidades

```text
Nova Tabela

Importar Planilha

Atualizar

Comparar

Definir Vigência

Aplicar Reajuste

Arquivar

Consultar Histórico
```

---

# Página

## Prazos de Fornecimento

### ID

```text
COM-PRA-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Acompanhar prazos prometidos, realizados e médios de cada fornecedor.

---

# Página

## Avaliação de Fornecedores

### ID

```text
COM-AVA-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Avaliar fornecedores com base em desempenho comercial e operacional.

### Critérios

```text
Preço

Prazo

Qualidade

Atendimento

Conformidade

Flexibilidade

Documentação

Índice de Divergência

Índice de Devolução

Cumprimento de SLA
```

### Classificações

```text
Excelente

Bom

Regular

Ruim

Crítico
```

---

# Página

## Histórico de Preços

### ID

```text
COM-HPR-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Acompanhar a evolução dos preços dos itens ao longo do tempo.

### Visualizações

```text
Tabela

Gráfico

Comparativo por Fornecedor

Comparativo por Período

Variação Percentual

Menor Preço Histórico
```

---

# Página

## Indicadores

### ID

```text
COM-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Valor Comprado

Quantidade de Pedidos

Economia em Negociação

Prazo Médio de Compra

Prazo Médio de Entrega

Pedidos em Atraso

Compras Emergenciais

Compras sem Cotação

Índice de Divergência

Índice de Devolução

Fornecedor Mais Utilizado

Fornecedor com Melhor Avaliação

Variação de Preços

Compras por Projeto

Compras por Categoria

Compras por Centro de Custo
```

---

# Página

## Relatórios

### ID

```text
COM-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Necessidades de Compra

Solicitações de Compra

Solicitações Pendentes

Cotações

Mapa Comparativo

Negociações

Pedidos de Compra

Pedidos em Atraso

Recebimentos

Divergências

Devoluções

Compras Emergenciais

Compras por Projeto

Compras por Fornecedor

Compras por Categoria

Compras por Centro de Custo

Histórico de Preços

Avaliação de Fornecedores

Economia em Negociação

Prazo Médio de Entrega
```

---

# Página

## Templates

### ID

```text
COM-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para documentos e comunicações do módulo.

### Tipos

```text
Solicitação de Cotação

Pedido de Compra

Email ao Fornecedor

Mensagem de Cobrança

Mapa Comparativo

Termo de Devolução

Checklist de Recebimento

Avaliação de Fornecedor
```

---

# Página

## Configurações

### ID

```text
COM-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Numeração das Solicitações

Numeração das Cotações

Numeração dos Pedidos

Tipos de Compra

Prioridades

Categorias

Alçadas de Aprovação

Quantidade Mínima de Cotações

Regras de Compra Emergencial

Regras de Fornecedor Único

Critérios de Comparação

Pesos de Avaliação

Prazos Padrão

Templates

Checklists

Notificações

Integrações
```

---

# Dialogs

```text
COM-DLG-001 Nova Necessidade

COM-DLG-002 Nova Solicitação de Compra

COM-DLG-003 Adicionar Item à Solicitação

COM-DLG-004 Importar Necessidades

COM-DLG-005 Consolidar Demandas

COM-DLG-006 Selecionar Fornecedor

COM-DLG-007 Nova Cotação

COM-DLG-008 Adicionar Fornecedor à Cotação

COM-DLG-009 Enviar Solicitação de Cotação

COM-DLG-010 Registrar Proposta

COM-DLG-011 Importar Proposta

COM-DLG-012 Comparar Propostas

COM-DLG-013 Registrar Negociação

COM-DLG-014 Selecionar Proposta Vencedora

COM-DLG-015 Justificar Escolha

COM-DLG-016 Solicitar Aprovação

COM-DLG-017 Aprovar Compra

COM-DLG-018 Reprovar Compra

COM-DLG-019 Novo Pedido de Compra

COM-DLG-020 Enviar Pedido ao Fornecedor

COM-DLG-021 Registrar Confirmação

COM-DLG-022 Alterar Previsão de Entrega

COM-DLG-023 Registrar Contato com Fornecedor

COM-DLG-024 Registrar Ocorrência

COM-DLG-025 Novo Recebimento

COM-DLG-026 Selecionar Pedido para Recebimento

COM-DLG-027 Conferir Item

COM-DLG-028 Registrar Divergência

COM-DLG-029 Aceitar Parcialmente

COM-DLG-030 Recusar Recebimento

COM-DLG-031 Nova Devolução

COM-DLG-032 Agendar Coleta

COM-DLG-033 Registrar Reposição

COM-DLG-034 Nova Compra Emergencial

COM-DLG-035 Novo Fornecedor

COM-DLG-036 Homologar Fornecedor

COM-DLG-037 Bloquear Fornecedor

COM-DLG-038 Adicionar Produto ao Fornecedor

COM-DLG-039 Importar Tabela de Preço

COM-DLG-040 Avaliar Fornecedor
```

---

# Wizards

```text
COM-WIZ-001 Assistente de Solicitação de Compra

COM-WIZ-002 Assistente de Consolidação de Demandas

COM-WIZ-003 Assistente de Cotação

COM-WIZ-004 Assistente de Mapa Comparativo

COM-WIZ-005 Assistente de Aprovação

COM-WIZ-006 Assistente de Pedido de Compra

COM-WIZ-007 Assistente de Recebimento

COM-WIZ-008 Assistente de Devolução

COM-WIZ-009 Assistente de Compra Emergencial

COM-WIZ-010 Assistente de Cadastro de Fornecedor

COM-WIZ-011 Assistente de Homologação

COM-WIZ-012 Assistente de Importação de Tabela de Preço
```

---

# Componentes Específicos

```text
COM-CPT-001 Painel de Necessidades

COM-CPT-002 Consolidador de Demandas

COM-CPT-003 Editor de Solicitação

COM-CPT-004 Editor de Cotação

COM-CPT-005 Matriz Comparativa de Fornecedores

COM-CPT-006 Indicador de Melhor Proposta

COM-CPT-007 Timeline de Negociação

COM-CPT-008 Checklist de Aprovação

COM-CPT-009 Editor de Pedido de Compra

COM-CPT-010 Calendário de Entregas

COM-CPT-011 Kanban de Acompanhamento

COM-CPT-012 Checklist de Recebimento

COM-CPT-013 Painel de Divergências

COM-CPT-014 Painel de Avaliação do Fornecedor

COM-CPT-015 Gráfico de Histórico de Preços

COM-CPT-016 Visualizador de Proposta

COM-CPT-017 Visualizador de Pedido

COM-CPT-018 Portal de Resposta do Fornecedor
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
PurchaseNeedIdentified

PurchaseRequestCreated

PurchaseRequestSubmitted

PurchaseRequestApproved

PurchaseRequestRejected

PurchaseDemandConsolidated

QuotationCreated

QuotationSent

SupplierProposalReceived

SupplierProposalValidated

SupplierNegotiationRegistered

SupplierSelected

PurchaseApprovalRequested

PurchaseApproved

PurchaseRejected

PurchaseOrderCreated

PurchaseOrderApproved

PurchaseOrderSent

PurchaseOrderConfirmed

PurchaseOrderDeliveryUpdated

PurchaseOrderDelayed

PurchaseOrderPartiallyReceived

PurchaseOrderReceived

PurchaseReceiptCreated

PurchaseReceiptChecked

PurchaseDivergenceCreated

PurchaseDivergenceResolved

PurchaseReturnCreated

PurchaseReturnCompleted

EmergencyPurchaseCreated

SupplierCreated

SupplierApproved

SupplierBlocked

SupplierEvaluated

SupplierPriceTableImported

PurchaseOrderCompleted

PurchaseOrderCancelled
```

---

# Automações

```text
Lista de materiais liberada

↓

Comparar com estoque

↓

Identificar faltas

↓

Criar necessidades de compra

↓

Notificar comprador
```

```text
Solicitação aprovada

↓

Consolidar itens compatíveis

↓

Sugerir fornecedores

↓

Criar cotação
```

```text
Cotação enviada

↓

Registrar prazo de resposta

↓

Agendar lembrete

↓

Cobrar fornecedores sem retorno
```

```text
Fornecedor selecionado

↓

Gerar pedido de compra

↓

Vincular solicitações

↓

Atualizar necessidades
```

```text
Pedido confirmado

↓

Atualizar previsão de recebimento

↓

Notificar Projetos

↓

Notificar PCP

↓

Notificar Estoque
```

```text
Pedido atrasado

↓

Gerar alerta

↓

Criar tarefa de cobrança

↓

Notificar comprador e responsável pelo projeto
```

```text
Recebimento concluído

↓

Enviar itens ao Estoque

↓

Enviar documento ao Fiscal

↓

Enviar obrigação ao Financeiro

↓

Atualizar pedido
```

```text
Divergência registrada

↓

Bloquear aceite definitivo

↓

Notificar fornecedor

↓

Criar tarefa de resolução
```

---

# Integrações

```text
Projetos

Orçamentos

Comercial

Estoque

PCP

Produção

Manutenção

Financeiro

Fiscal

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Email

WhatsApp

Portal do Fornecedor
```

---

# Permissões

```text
purchasing.dashboard.read

purchasing.need.read

purchasing.need.manage

purchasing.request.read

purchasing.request.create

purchasing.request.update

purchasing.request.submit

purchasing.request.approve

purchasing.request.reject

purchasing.demand.consolidate

purchasing.quotation.read

purchasing.quotation.create

purchasing.quotation.update

purchasing.quotation.send

purchasing.proposal.register

purchasing.proposal.import

purchasing.comparison.read

purchasing.comparison.manage

purchasing.negotiation.manage

purchasing.supplier.select

purchasing.approval.request

purchasing.approval.approve

purchasing.approval.reject

purchasing.order.read

purchasing.order.create

purchasing.order.update

purchasing.order.approve

purchasing.order.send

purchasing.order.confirm

purchasing.order.cancel

purchasing.order.close

purchasing.follow_up.manage

purchasing.receipt.read

purchasing.receipt.create

purchasing.receipt.check

purchasing.receipt.accept

purchasing.receipt.reject

purchasing.divergence.manage

purchasing.return.manage

purchasing.emergency.create

purchasing.emergency.approve

purchasing.supplier.read

purchasing.supplier.create

purchasing.supplier.update

purchasing.supplier.approve

purchasing.supplier.block

purchasing.supplier.evaluate

purchasing.price_table.manage

purchasing.report.read

purchasing.report.export

purchasing.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Solicitação de Compra

Resumo de Necessidades

Consolidação de Demandas

Solicitação de Cotação

Mapa Comparativo

Relatório de Negociação

Pedido de Compra

Confirmação de Pedido

Programação de Entregas

Checklist de Recebimento

Relatório de Divergência

Termo de Devolução

Relatório de Compra Emergencial

Ficha do Fornecedor

Avaliação do Fornecedor

Histórico de Preços

Compras por Projeto

Compras por Centro de Custo

Compras por Categoria

Compras por Fornecedor

Relatório de Economia
```

---

# Recursos de Inteligência Artificial

```text
Sugerir consolidação de demandas

Sugerir fornecedores

Classificar propostas recebidas

Extrair dados de PDFs e planilhas

Comparar propostas automaticamente

Identificar condições divergentes

Detectar preço fora do histórico

Sugerir melhor proposta

Sugerir divisão de compra

Prever atraso de fornecedor

Analisar desempenho do fornecedor

Resumir negociações

Gerar mensagem de cotação

Gerar cobrança de entrega

Identificar risco de ruptura

Sugerir compra antecipada

Detectar compras recorrentes

Pesquisar compras em linguagem natural
```

A IA nunca poderá selecionar definitivamente um fornecedor, aprovar uma compra, emitir um pedido ou aceitar um recebimento sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Toda compra deverá pertencer a um Tenant.

2. Toda solicitação deverá possuir origem, solicitante e justificativa.

3. Itens originados de projetos deverão manter vínculo com o projeto, ambiente ou móvel correspondente.

4. O sistema deverá consultar o estoque antes de sugerir uma compra.

5. A quantidade a comprar deverá considerar saldo disponível, reservas e pedidos já emitidos.

6. Compras acima do limite configurado deverão exigir aprovação.

7. Compras sem a quantidade mínima de cotações deverão exigir justificativa.

8. Compras com fornecedor único deverão exigir justificativa e aprovação conforme política.

9. Compras emergenciais deverão ser regularizadas posteriormente.

10. Nenhum pedido poderá ser emitido sem fornecedor, itens, quantidades, preços e condição de pagamento.

11. Pedidos aprovados não poderão ser alterados sem revisão ou cancelamento formal.

12. Alterações de preço, quantidade ou prazo após aprovação deverão permanecer auditadas.

13. O recebimento poderá ocorrer de forma parcial.

14. Quantidades recebidas não poderão exceder o pedido sem autorização.

15. Divergências deverão impedir o aceite definitivo dos itens afetados.

16. Materiais aceitos deverão ser encaminhados ao Estoque.

17. Documentos fiscais recebidos deverão ser encaminhados ao Fiscal.

18. Obrigações de pagamento deverão ser encaminhadas ao Financeiro.

19. A avaliação do fornecedor deverá utilizar critérios configuráveis.

20. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Compras será a fonte oficial para solicitações, cotações, negociações, pedidos e relacionamento operacional com fornecedores.

O módulo Projetos deverá informar o que precisa ser adquirido.

O módulo Estoque deverá informar o que já está disponível, reservado ou em trânsito.

O módulo Compras deverá decidir o processo de aquisição, sem alterar a especificação técnica originada em Projetos.

Qualquer substituição de material ou ferragem deverá retornar para validação do módulo Projetos quando impactar o produto.

O recebimento registrado em Compras deverá ser confirmado pelo Estoque e conciliado com os módulos Fiscal e Financeiro.

---

# Próxima Etapa

```text
ETAPA 03-G

Catálogo Completo de Páginas

Estoque
```
---

# ETAPA 03-G

# Catálogo Completo de Páginas

# Estoque

## ID do Módulo

```text
EST
```

---

# Objetivo

O módulo Estoque é responsável por controlar fisicamente e contabilmente todos os materiais, produtos, ferragens, componentes, consumíveis, sobras e recursos armazenados pela empresa.

Ele deverá registrar e rastrear:

* entradas;
* saídas;
* reservas;
* transferências;
* inventários;
* ajustes;
* lotes;
* localizações;
* perdas;
* sobras;
* materiais em trânsito;
* materiais separados;
* materiais consumidos;
* materiais devolvidos.

O estoque deverá representar, com precisão, o que a empresa possui, onde cada item está, quanto está disponível e para qual finalidade foi reservado.

Nenhuma movimentação poderá ocorrer sem origem, responsável, data, quantidade e histórico.

---

# Limites do Módulo

O módulo Estoque será responsável por:

```text
Cadastrar e organizar itens estocáveis

Controlar saldos físicos

Controlar localizações

Registrar movimentações

Reservar materiais

Separar materiais

Controlar lotes

Controlar sobras

Executar inventários

Registrar perdas

Rastrear entradas e saídas

Informar disponibilidade
```

O módulo Estoque não será responsável por:

```text
Definir tecnicamente materiais do projeto

Negociar com fornecedores

Emitir pedidos de compra

Executar pagamentos

Emitir documentos fiscais

Planejar a produção

Modificar estruturas técnicas
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Compras

Financeiro

Fiscal

PCP

Produção
```

---

# Fluxo Principal

```text
Item Cadastrado

↓

Entrada

↓

Conferência

↓

Armazenamento

↓

Saldo Disponível

↓

Reserva

↓

Separação

↓

Consumo ou Saída

↓

Baixa

↓

Rastreabilidade
```

Fluxo de compra:

```text
Pedido de Compra

↓

Recebimento

↓

Conferência

↓

Entrada no Estoque

↓

Armazenamento

↓

Disponibilização
```

Fluxo de produção:

```text
Projeto Liberado

↓

Lista de Materiais

↓

Consulta de Disponibilidade

↓

Reserva

↓

Separação

↓

Entrega à Produção

↓

Consumo

↓

Devolução de Sobras
```

---

# Estrutura Geral

```text
EST — Estoque

├── Dashboard de Estoque
├── Itens de Estoque
├── Materiais
├── Ferragens
├── Componentes
├── Consumíveis
├── Produtos Acabados
├── Almoxarifados
├── Localizações
├── Saldos
├── Disponibilidade
├── Movimentações
├── Entradas
├── Saídas
├── Reservas
├── Separações
├── Transferências
├── Lotes
├── Séries
├── Inventários
├── Ajustes
├── Perdas
├── Sobras de Chapas
├── Retalhos
├── Materiais em Trânsito
├── Materiais de Terceiros
├── Materiais em Poder de Terceiros
├── Devoluções
├── Requisições
├── Consumos
├── Rastreabilidade
├── Histórico
├── Indicadores
├── Relatórios
├── Etiquetas
├── Templates
└── Configurações
```

---

# Página

## Dashboard de Estoque

### ID

```text
EST-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada dos saldos, reservas, faltas, entradas, saídas, inventários, perdas e materiais críticos.

### Componentes

```text
Valor Total em Estoque

Itens com Saldo

Itens sem Saldo

Itens Abaixo do Mínimo

Itens Abaixo do Ponto de Reposição

Itens com Excesso

Reservas Pendentes

Materiais Separados

Materiais em Trânsito

Entradas Previstas

Saídas Previstas

Inventários em Aberto

Divergências de Inventário

Perdas no Período

Sobras Aproveitáveis

Sobras Sem Uso

Giro de Estoque

Cobertura de Estoque

Alertas
```

### Filtros

```text
Período

Almoxarifado

Localização

Categoria

Item

Projeto

Fornecedor

Lote

Status

Filial
```

### Ações

```text
Nova Entrada

Nova Saída

Nova Transferência

Nova Reserva

Novo Inventário

Registrar Perda

Consultar Saldo

Abrir Rastreabilidade

Exportar Dashboard

Atualizar Indicadores
```

---

# Página

## Itens de Estoque

### ID

```text
EST-ITE-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar todos os itens que podem possuir saldo ou movimentação.

### Categorias

```text
Material

Ferragem

Componente

Consumível

Produto Acabado

Embalagem

Ferramenta Controlada

Sobra

Retalho

Item de Terceiro

Outro
```

### Colunas

```text
Código

Descrição

Categoria

Unidade

Marca

Modelo

Cor

Espessura

Saldo Físico

Saldo Reservado

Saldo Disponível

Saldo em Trânsito

Estoque Mínimo

Ponto de Reposição

Custo Médio

Localização Principal

Status
```

### Status

```text
Ativo

Inativo

Bloqueado

Sem Saldo

Abaixo do Mínimo

Em Falta

Descontinuado

Arquivado
```

### Ações

```text
Novo Item

Abrir

Editar

Duplicar

Inativar

Reativar

Bloquear

Desbloquear

Consultar Saldo

Consultar Movimentações

Consultar Reservas

Consultar Lotes

Gerar Etiqueta

Importar

Exportar

Arquivar
```

---

# Página

## Cadastro do Item de Estoque

### ID

```text
EST-ITE-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações cadastrais, físicas, logísticas e financeiras do item.

### Abas

```text
Geral

Classificação

Dimensões

Unidades

Armazenamento

Saldos

Lotes

Fornecedores

Preços

Reservas

Movimentações

Projetos

Produção

Documentos

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Código

Descrição

Descrição Resumida

Categoria

Subcategoria

Tipo de Item

Unidade Principal

Marca

Fabricante

Modelo

Cor

Linha

Referência

Código de Barras

Status

Controla Estoque

Controla Lote

Controla Série

Permite Saldo Negativo

Observações
```

### Aba Classificação

Campos:

```text
Grupo

Subgrupo

Família

Classe

Curva ABC

Criticidade

Origem

Tipo de Consumo

Aplicação

Centro de Custo Padrão
```

### Aba Dimensões

Campos:

```text
Comprimento

Largura

Espessura

Altura

Peso

Volume

Densidade

Formato

Sentido do Veio

Unidade Dimensional
```

### Aba Unidades

Campos:

```text
Unidade Principal

Unidade de Compra

Unidade de Consumo

Fator de Conversão

Quantidade por Embalagem

Quantidade Mínima de Movimentação
```

### Aba Armazenamento

Campos:

```text
Almoxarifado Principal

Localização Padrão

Condição de Armazenamento

Empilhamento Máximo

Validade

Controle de Umidade

Controle de Temperatura

Restrições

Observações
```

### Aba Saldos

Informações:

```text
Saldo Físico

Saldo Reservado

Saldo Separado

Saldo Disponível

Saldo em Trânsito

Saldo Bloqueado

Saldo de Terceiros

Saldo em Terceiros

Custo Médio

Última Entrada

Última Saída
```

---

# Página

## Materiais

### ID

```text
EST-MAT-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar materiais utilizados em projetos e produção.

### Categorias

```text
MDF

MDP

Compensado

Madeira

Laminado

Vidro

Espelho

Acrílico

Alumínio

Aço

Perfil

Pedra

Fita de Borda

Revestimento

Embalagem
```

### Funcionalidades

```text
Cadastrar

Editar

Consultar Saldo

Consultar Sobras

Consultar Projetos

Consultar Consumo

Registrar Entrada

Registrar Saída

Reservar

Transferir

Inventariar
```

---

# Página

## Ferragens

### ID

```text
EST-FER-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar ferragens, acessórios e fixadores utilizados nos projetos.

### Categorias

```text
Dobradiça

Corrediça

Puxador

Pistão

Sistema de Porta

Pé

Rodízio

Cabideiro

Suporte

Fixador

Parafuso

Bucha

Acessório
```

---

# Página

## Componentes

### ID

```text
EST-CMP-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar componentes prontos ou semiprontos armazenados.

### Exemplos

```text
Gaveta Montada

Porta Pronta

Estrutura Metálica

Perfil Cortado

Painel Usinado

Componente Terceirizado
```

---

# Página

## Consumíveis

### ID

```text
EST-CON-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar materiais de consumo recorrente.

### Exemplos

```text
Cola

Lixa

Broca

Serra

Fita Adesiva

Pano

Produto de Limpeza

Lubrificante

Disco de Corte

Embalagem

Proteção
```

---

# Página

## Produtos Acabados

### ID

```text
EST-PAC-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar móveis, componentes ou produtos concluídos e aguardando expedição.

### Status

```text
Aguardando Conferência

Conferido

Embalado

Reservado

Aguardando Expedição

Expedido

Bloqueado
```

---

# Página

## Almoxarifados

### ID

```text
EST-ALM-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar e administrar áreas físicas de armazenamento.

### Exemplos

```text
Almoxarifado Principal

Estoque de Chapas

Estoque de Ferragens

Estoque de Consumíveis

Estoque de Produção

Estoque de Produtos Acabados

Área de Recebimento

Área de Quarentena

Área de Expedição

Estoque Externo
```

### Funcionalidades

```text
Novo Almoxarifado

Editar

Inativar

Reativar

Definir Responsável

Cadastrar Localizações

Consultar Saldos

Transferir Estoque

Executar Inventário
```

---

# Página

## Localizações

### ID

```text
EST-LOC-001
```

### Tipo

```text
Árvore
```

### Objetivo

Representar endereços físicos dentro dos almoxarifados.

### Hierarquia

```text
Almoxarifado

↓

Área

↓

Corredor

↓

Estante

↓

Nível

↓

Posição
```

### Campos

```text
Código

Descrição

Almoxarifado

Área

Capacidade

Peso Máximo

Volume Máximo

Tipo de Item Permitido

Status

Responsável
```

### Ações

```text
Nova Localização

Editar

Mover Item

Bloquear

Desbloquear

Consultar Ocupação

Gerar Etiqueta

Imprimir Mapa
```

---

# Página

## Saldos

### ID

```text
EST-SAL-001
```

### Tipo

```text
Consulta
```

### Objetivo

Consultar saldos por item, almoxarifado, localização, lote, projeto ou status.

### Visualizações

```text
Saldo Consolidado

Saldo por Almoxarifado

Saldo por Localização

Saldo por Lote

Saldo por Projeto

Saldo Reservado

Saldo em Trânsito

Saldo Bloqueado
```

### Campos

```text
Item

Almoxarifado

Localização

Lote

Saldo Físico

Saldo Reservado

Saldo Separado

Saldo Disponível

Saldo em Trânsito

Saldo Bloqueado

Custo Médio

Valor Total
```

---

# Página

## Disponibilidade

### ID

```text
EST-DIS-001
```

### Tipo

```text
Consulta
```

### Objetivo

Informar quanto de cada item pode efetivamente ser utilizado em uma necessidade específica.

### Cálculo

```text
Saldo Físico

-

Saldo Reservado

-

Saldo Bloqueado

-

Saldo Separado

=

Saldo Disponível
```

### Informações Adicionais

```text
Pedidos de Compra em Aberto

Previsões de Recebimento

Consumo Programado

Reservas Futuras

Cobertura Estimada

Data de Disponibilidade
```

---

# Página

## Movimentações

### ID

```text
EST-MOV-001
```

### Tipo

```text
Lista
```

### Objetivo

Consultar todas as movimentações realizadas no estoque.

### Tipos

```text
Entrada

Saída

Transferência

Reserva

Liberação de Reserva

Separação

Consumo

Devolução

Ajuste

Inventário

Perda

Bloqueio

Desbloqueio

Entrada de Terceiro

Saída para Terceiro
```

### Colunas

```text
Número

Data

Tipo

Item

Quantidade

Unidade

Origem

Destino

Projeto

Documento

Responsável

Custo

Status
```

### Ações

```text
Abrir

Consultar Origem

Consultar Destino

Consultar Documento

Estornar

Gerar Comprovante

Exportar

Imprimir
```

---

# Página

## Entradas

### ID

```text
EST-ENT-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar entradas físicas de materiais e produtos.

### Origens

```text
Compra

Devolução de Produção

Devolução de Cliente

Produção Concluída

Transferência

Ajuste

Inventário

Entrada Manual

Entrada de Terceiro

Sobra de Produção
```

### Status

```text
Rascunho

Aguardando Conferência

Conferida

Parcialmente Armazenada

Armazenada

Com Divergência

Cancelada
```

### Ações

```text
Nova Entrada

Selecionar Pedido de Compra

Registrar Quantidades

Registrar Lote

Registrar Localização

Registrar Custo

Conferir

Armazenar

Registrar Divergência

Estornar

Finalizar
```

---

# Página

## Cadastro da Entrada

### ID

```text
EST-ENT-002
```

### Tipo

```text
Cadastro
```

### Abas

```text
Geral

Itens

Origem

Conferência

Lotes

Localizações

Custos

Documentos

Divergências

Histórico

Auditoria
```

### Aba Geral

Campos:

```text
Número

Tipo de Entrada

Data

Almoxarifado

Fornecedor

Projeto

Pedido de Compra

Documento Fiscal

Responsável

Status

Observações
```

### Aba Itens

Campos:

```text
Item

Descrição

Quantidade Esperada

Quantidade Recebida

Unidade

Lote

Validade

Localização

Custo Unitário

Custo Total

Situação
```

---

# Página

## Saídas

### ID

```text
EST-SAI-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar saídas físicas de materiais e produtos.

### Destinos

```text
Produção

Projeto

Instalação

Expedição

Manutenção

Terceiro

Cliente

Descarte

Transferência

Consumo Interno

Ajuste
```

### Status

```text
Rascunho

Aguardando Separação

Em Separação

Separada

Entregue

Consumida

Parcialmente Atendida

Cancelada
```

### Ações

```text
Nova Saída

Selecionar Requisição

Reservar

Separar

Conferir

Entregar

Registrar Consumo

Estornar

Finalizar
```

---

# Página

## Reservas

### ID

```text
EST-RES-001
```

### Tipo

```text
Lista
```

### Objetivo

Garantir que materiais disponíveis sejam destinados a um projeto, pedido, ordem ou finalidade específica.

### Origens

```text
Projeto

Ordem de Produção

Pedido de Venda

Instalação

Manutenção

Solicitação Manual
```

### Status

```text
Solicitada

Confirmada

Parcial

Sem Saldo

Separada

Consumida

Liberada

Expirada

Cancelada
```

### Ações

```text
Nova Reserva

Confirmar

Atender Parcialmente

Substituir Item

Alterar Quantidade

Alterar Prioridade

Separar

Liberar

Cancelar

Renovar
```

---

# Página

## Separações

### ID

```text
EST-SEP-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar a preparação física dos materiais reservados para uso.

### Etapas

```text
Aguardando Separação

Em Separação

Aguardando Conferência

Conferida

Pronta para Retirada

Entregue

Parcialmente Entregue

Cancelada
```

### Funcionalidades

```text
Iniciar Separação

Ler Código de Barras

Confirmar Quantidade

Alterar Localização

Registrar Falta

Registrar Substituição

Conferir

Liberar para Retirada

Entregar
```

---

# Página

## Transferências

### ID

```text
EST-TRF-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar movimentações entre almoxarifados, localizações ou filiais.

### Status

```text
Rascunho

Solicitada

Aprovada

Em Separação

Em Trânsito

Recebida

Com Divergência

Cancelada
```

### Ações

```text
Nova Transferência

Adicionar Itens

Solicitar Aprovação

Aprovar

Separar

Despachar

Receber

Registrar Divergência

Cancelar

Finalizar
```

---

# Página

## Lotes

### ID

```text
EST-LOT-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar grupos de materiais recebidos ou produzidos em condições comuns.

### Campos

```text
Código do Lote

Item

Fornecedor

Data de Entrada

Data de Fabricação

Validade

Quantidade Inicial

Quantidade Atual

Localização

Status

Documento de Origem
```

### Status

```text
Disponível

Reservado

Parcialmente Consumido

Consumido

Bloqueado

Vencido

Em Quarentena

Descartado
```

---

# Página

## Séries

### ID

```text
EST-SER-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar itens individualizados por número de série.

---

# Página

## Inventários

### ID

```text
EST-INV-001
```

### Tipo

```text
Lista
```

### Objetivo

Planejar, executar e conciliar contagens físicas.

### Tipos

```text
Geral

Rotativo

Por Almoxarifado

Por Localização

Por Categoria

Por Item

Por Curva ABC

Extraordinário
```

### Status

```text
Planejado

Em Preparação

Em Contagem

Aguardando Recontagem

Em Conciliação

Aguardando Aprovação

Concluído

Cancelado
```

### Ações

```text
Novo Inventário

Definir Escopo

Gerar Lista de Contagem

Bloquear Movimentações

Iniciar Contagem

Registrar Contagem

Solicitar Recontagem

Conciliar

Gerar Ajustes

Aprovar

Concluir

Cancelar
```

---

# Página

## Cadastro do Inventário

### ID

```text
EST-INV-002
```

### Tipo

```text
Cadastro
```

### Abas

```text
Geral

Escopo

Itens

Contagens

Recontagens

Divergências

Ajustes

Aprovações

Documentos

Histórico
```

---

# Página

## Ajustes

### ID

```text
EST-AJU-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar correções autorizadas de saldo.

### Tipos

```text
Ajuste Positivo

Ajuste Negativo

Correção de Unidade

Correção de Lote

Correção de Localização

Correção de Custo

Resultado de Inventário
```

### Regras

```text
Motivo obrigatório

Usuário obrigatório

Aprovação conforme alçada

Auditoria permanente

Estorno controlado
```

---

# Página

## Perdas

### ID

```text
EST-PER-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar materiais perdidos, danificados, vencidos, descartados ou inutilizados.

### Motivos

```text
Avaria

Quebra

Erro de Corte

Erro de Produção

Umidade

Vencimento

Contaminação

Extravio

Descarte

Obsolescência

Sobra Não Aproveitável
```

### Informações

```text
Item

Quantidade

Valor

Motivo

Projeto

Ordem de Produção

Responsável

Data

Destino

Evidência

Aprovação
```

---

# Página

## Sobras de Chapas

### ID

```text
EST-SOB-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar sobras aproveitáveis provenientes de chapas utilizadas em projetos e produção.

### Campos

```text
Código

Material

Fabricante

Linha

Cor

Espessura

Comprimento

Largura

Área

Sentido do Veio

Origem

Projeto

Plano de Corte

Localização

Status

Data de Entrada
```

### Status

```text
Disponível

Reservada

Separada

Utilizada

Bloqueada

Descartada
```

### Funcionalidades

```text
Nova Sobra

Registrar Automaticamente

Editar Dimensões

Gerar Etiqueta

Reservar

Utilizar em Projeto

Transferir

Descartar

Consultar Aproveitamento
```

---

# Página

## Retalhos

### ID

```text
EST-RET-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar pequenos materiais reaproveitáveis que não se enquadram como chapas completas.

---

# Página

## Materiais em Trânsito

### ID

```text
EST-TRA-001
```

### Tipo

```text
Lista
```

### Objetivo

Acompanhar materiais já adquiridos ou transferidos que ainda não estão disponíveis fisicamente.

### Origens

```text
Pedido de Compra

Transferência

Devolução

Fornecedor

Terceirizado
```

---

# Página

## Materiais de Terceiros

### ID

```text
EST-MTE-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar materiais pertencentes a clientes, fornecedores ou parceiros armazenados pela empresa.

---

# Página

## Materiais em Poder de Terceiros

### ID

```text
EST-MPT-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar materiais da empresa enviados para fornecedores ou prestadores.

### Exemplos

```text
Vidraçaria

Marmoraria

Serralheria

Pintura

Usinagem CNC

Tapeçaria

Terceirização
```

---

# Página

## Devoluções

### ID

```text
EST-DEV-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar retornos de materiais provenientes de produção, instalação, clientes ou terceiros.

### Tipos

```text
Devolução de Produção

Devolução de Instalação

Devolução de Cliente

Devolução de Terceiro

Devolução ao Fornecedor
```

---

# Página

## Requisições

### ID

```text
EST-REQ-001
```

### Tipo

```text
Lista
```

### Objetivo

Formalizar solicitações internas de retirada de materiais.

### Origens

```text
Produção

Instalação

Manutenção

Projeto

Administrativo

Limpeza

Expedição
```

### Status

```text
Rascunho

Solicitada

Aprovada

Reservada

Em Separação

Atendida

Parcialmente Atendida

Rejeitada

Cancelada
```

---

# Página

## Consumos

### ID

```text
EST-CSM-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar consumo efetivo de materiais por projeto, ordem, operação ou setor.

### Informações

```text
Item

Quantidade Prevista

Quantidade Consumida

Diferença

Projeto

Ordem

Operação

Responsável

Data

Sobra

Perda
```

---

# Página

## Rastreabilidade

### ID

```text
EST-RAS-001
```

### Tipo

```text
Timeline
```

### Objetivo

Permitir rastrear toda a vida de um item, lote, sobra ou movimentação.

### Fluxo

```text
Compra

↓

Recebimento

↓

Entrada

↓

Armazenamento

↓

Reserva

↓

Separação

↓

Consumo

↓

Sobra ou Perda
```

### Pesquisas

```text
Item

Lote

Número de Série

Projeto

Ordem

Fornecedor

Documento

Movimentação

Localização
```

---

# Página

## Histórico

### ID

```text
EST-HIS-001
```

### Tipo

```text
Consulta
```

### Objetivo

Consultar alterações cadastrais e operacionais do módulo.

---

# Página

## Indicadores

### ID

```text
EST-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Valor Total em Estoque

Giro de Estoque

Cobertura

Ruptura

Excesso

Obsolescência

Acuracidade

Perdas

Consumo por Projeto

Consumo por Categoria

Itens Parados

Itens sem Movimentação

Tempo Médio de Armazenamento

Reservas Pendentes

Tempo Médio de Separação

Sobras Aproveitadas

Taxa de Aproveitamento de Sobras
```

---

# Página

## Relatórios

### ID

```text
EST-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Posição de Estoque

Saldo por Almoxarifado

Saldo por Localização

Saldo por Lote

Saldo por Projeto

Itens Abaixo do Mínimo

Itens sem Saldo

Itens sem Movimentação

Movimentações

Entradas

Saídas

Reservas

Separações

Transferências

Inventários

Ajustes

Perdas

Sobras de Chapas

Materiais em Trânsito

Materiais de Terceiros

Materiais em Terceiros

Consumo por Projeto

Consumo Previsto x Realizado

Acuracidade de Estoque

Valorização de Estoque

Curva ABC
```

---

# Página

## Etiquetas

### ID

```text
EST-ETQ-001
```

### Tipo

```text
Configuração
```

### Objetivo

Gerar e administrar etiquetas para itens, lotes, localizações, sobras e volumes.

### Tipos

```text
Etiqueta de Item

Etiqueta de Lote

Etiqueta de Localização

Etiqueta de Sobra

Etiqueta de Separação

Etiqueta de Volume

Etiqueta de Produto Acabado
```

### Conteúdo

```text
Código

Descrição

Código de Barras

QR Code

Lote

Quantidade

Dimensões

Projeto

Localização

Data
```

---

# Página

## Templates

### ID

```text
EST-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para documentos e operações do estoque.

### Tipos

```text
Entrada

Saída

Transferência

Inventário

Requisição

Separação

Etiqueta

Checklist de Conferência
```

---

# Página

## Configurações

### ID

```text
EST-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Numeração de Movimentações

Tipos de Item

Categorias

Unidades

Conversões

Almoxarifados

Localizações

Política de Saldo Negativo

Política de Reservas

Política de Validade

Política de Lotes

Política de Inventário

Política de Ajustes

Política de Perdas

Dimensão Mínima de Sobra

Curva ABC

Método de Custeio

Templates

Etiquetas

Checklists

Notificações

Integrações
```

---

# Dialogs

```text
EST-DLG-001 Novo Item

EST-DLG-002 Editar Item

EST-DLG-003 Selecionar Item

EST-DLG-004 Consultar Saldo

EST-DLG-005 Nova Entrada

EST-DLG-006 Selecionar Pedido de Compra

EST-DLG-007 Adicionar Item à Entrada

EST-DLG-008 Informar Lote

EST-DLG-009 Selecionar Localização

EST-DLG-010 Conferir Entrada

EST-DLG-011 Nova Saída

EST-DLG-012 Selecionar Requisição

EST-DLG-013 Reservar Material

EST-DLG-014 Liberar Reserva

EST-DLG-015 Iniciar Separação

EST-DLG-016 Confirmar Separação

EST-DLG-017 Registrar Falta

EST-DLG-018 Substituir Item

EST-DLG-019 Nova Transferência

EST-DLG-020 Despachar Transferência

EST-DLG-021 Receber Transferência

EST-DLG-022 Novo Inventário

EST-DLG-023 Registrar Contagem

EST-DLG-024 Solicitar Recontagem

EST-DLG-025 Conciliar Inventário

EST-DLG-026 Gerar Ajuste

EST-DLG-027 Novo Ajuste

EST-DLG-028 Registrar Perda

EST-DLG-029 Registrar Sobra

EST-DLG-030 Reservar Sobra

EST-DLG-031 Utilizar Sobra

EST-DLG-032 Descartar Sobra

EST-DLG-033 Registrar Devolução

EST-DLG-034 Nova Requisição

EST-DLG-035 Registrar Consumo

EST-DLG-036 Bloquear Estoque

EST-DLG-037 Desbloquear Estoque

EST-DLG-038 Gerar Etiqueta

EST-DLG-039 Exportar Estoque

EST-DLG-040 Importar Itens
```

---

# Wizards

```text
EST-WIZ-001 Assistente de Cadastro de Item

EST-WIZ-002 Assistente de Entrada

EST-WIZ-003 Assistente de Saída

EST-WIZ-004 Assistente de Reserva

EST-WIZ-005 Assistente de Separação

EST-WIZ-006 Assistente de Transferência

EST-WIZ-007 Assistente de Inventário

EST-WIZ-008 Assistente de Ajuste

EST-WIZ-009 Assistente de Cadastro de Almoxarifado

EST-WIZ-010 Assistente de Importação de Itens

EST-WIZ-011 Assistente de Impressão de Etiquetas

EST-WIZ-012 Assistente de Rastreabilidade
```

---

# Componentes Específicos

```text
EST-CPT-001 Consulta de Saldo

EST-CPT-002 Painel de Disponibilidade

EST-CPT-003 Árvore de Localizações

EST-CPT-004 Seletor de Localização

EST-CPT-005 Leitor de Código de Barras

EST-CPT-006 Leitor de QR Code

EST-CPT-007 Editor de Movimentação

EST-CPT-008 Painel de Reserva

EST-CPT-009 Kanban de Separação

EST-CPT-010 Editor de Transferência

EST-CPT-011 Coletor de Inventário

EST-CPT-012 Comparador de Contagens

EST-CPT-013 Painel de Acuracidade

EST-CPT-014 Gerenciador de Sobras

EST-CPT-015 Visualizador de Chapas e Sobras

EST-CPT-016 Timeline de Rastreabilidade

EST-CPT-017 Gerador de Etiquetas

EST-CPT-018 Mapa de Almoxarifado
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
InventoryItemCreated

InventoryItemUpdated

InventoryItemBlocked

InventoryEntryCreated

InventoryEntryConfirmed

InventoryEntryStored

InventoryExitCreated

InventoryExitConfirmed

InventoryReservationRequested

InventoryReserved

InventoryReservationPartiallyFulfilled

InventoryReservationReleased

InventorySeparationStarted

InventorySeparationCompleted

InventoryTransferCreated

InventoryTransferDispatched

InventoryTransferReceived

InventoryLotCreated

InventoryLotBlocked

InventoryCountStarted

InventoryCountRegistered

InventoryRecountRequested

InventoryAdjustmentCreated

InventoryAdjustmentApproved

InventoryLossRegistered

InventoryRemnantCreated

InventoryRemnantReserved

InventoryRemnantConsumed

InventoryRemnantDiscarded

InventoryRequestCreated

InventoryRequestFulfilled

InventoryConsumptionRegistered

InventoryReturnRegistered

InventoryStockBelowMinimum

InventoryStockUnavailable
```

---

# Automações

```text
Recebimento aprovado

↓

Criar entrada

↓

Gerar lotes

↓

Sugerir localizações

↓

Atualizar saldos
```

```text
Projeto liberado

↓

Receber lista de materiais

↓

Consultar disponibilidade

↓

Criar reservas

↓

Sinalizar faltas
```

```text
Reserva sem saldo

↓

Consultar pedidos em aberto

↓

Calcular previsão

↓

Criar necessidade de compra

↓

Notificar Compras e Projeto
```

```text
Separação concluída

↓

Baixar saldo disponível

↓

Disponibilizar para Produção

↓

Registrar responsável
```

```text
Consumo registrado

↓

Comparar previsto x realizado

↓

Registrar sobra

↓

Registrar perda

↓

Atualizar custo
```

```text
Estoque abaixo do mínimo

↓

Gerar alerta

↓

Criar necessidade de compra

↓

Notificar responsável
```

```text
Inventário concluído

↓

Gerar divergências

↓

Criar ajustes

↓

Solicitar aprovação

↓

Atualizar acuracidade
```

---

# Integrações

```text
Projetos

Orçamentos

Compras

Comercial

PCP

Produção

Qualidade

Manutenção

Expedição

Instalação

Financeiro

Fiscal

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Código de Barras

QR Code
```

---

# Permissões

```text
inventory.dashboard.read

inventory.item.read

inventory.item.create

inventory.item.update

inventory.item.block

inventory.item.archive

inventory.balance.read

inventory.availability.read

inventory.movement.read

inventory.entry.create

inventory.entry.confirm

inventory.entry.store

inventory.entry.cancel

inventory.exit.create

inventory.exit.confirm

inventory.exit.cancel

inventory.reservation.read

inventory.reservation.create

inventory.reservation.confirm

inventory.reservation.release

inventory.separation.read

inventory.separation.execute

inventory.separation.confirm

inventory.transfer.read

inventory.transfer.create

inventory.transfer.approve

inventory.transfer.dispatch

inventory.transfer.receive

inventory.lot.read

inventory.lot.manage

inventory.serial.read

inventory.serial.manage

inventory.inventory_count.read

inventory.inventory_count.create

inventory.inventory_count.execute

inventory.inventory_count.reconcile

inventory.inventory_count.approve

inventory.adjustment.read

inventory.adjustment.create

inventory.adjustment.approve

inventory.loss.read

inventory.loss.register

inventory.remnant.read

inventory.remnant.create

inventory.remnant.reserve

inventory.remnant.consume

inventory.remnant.discard

inventory.request.read

inventory.request.create

inventory.request.approve

inventory.request.fulfill

inventory.consumption.read

inventory.consumption.register

inventory.traceability.read

inventory.label.generate

inventory.report.read

inventory.report.export

inventory.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Posição de Estoque

Ficha do Item

Extrato de Movimentações

Comprovante de Entrada

Comprovante de Saída

Comprovante de Transferência

Ficha de Reserva

Lista de Separação

Comprovante de Entrega

Lista de Inventário

Relatório de Contagem

Relatório de Divergências

Termo de Ajuste

Relatório de Perdas

Relação de Sobras

Etiquetas de Sobras

Rastreabilidade de Lote

Rastreabilidade por Projeto

Consumo Previsto x Realizado

Curva ABC

Valorização do Estoque

Relatório de Acuracidade
```

---

# Recursos de Inteligência Artificial

```text
Sugerir classificação de itens

Detectar itens duplicados

Sugerir estoque mínimo

Sugerir ponto de reposição

Prever ruptura

Prever excesso

Classificar curva ABC

Detectar movimentações incomuns

Sugerir localizações

Otimizar ocupação

Sugerir utilização de sobras

Identificar materiais parados

Analisar perdas

Analisar consumo previsto x realizado

Prever consumo por projeto

Detectar divergências de inventário

Resumir rastreabilidade

Pesquisar estoque em linguagem natural
```

A IA nunca poderá executar ajustes, perdas, descartes, transferências ou liberações de estoque sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Todo item deverá pertencer a um Tenant.

2. Toda movimentação deverá possuir origem, destino, responsável, data e quantidade.

3. Nenhuma movimentação poderá possuir quantidade igual ou inferior a zero.

4. O saldo disponível deverá considerar reservas, separações e bloqueios.

5. O sistema não deverá permitir saldo negativo, exceto quando autorizado pela política do Tenant.

6. Toda entrada deverá possuir origem identificada.

7. Toda saída deverá possuir finalidade e responsável.

8. Reservas deverão possuir vínculo com documento ou finalidade.

9. Reservas poderão ser atendidas parcialmente.

10. Materiais bloqueados não poderão ser reservados ou consumidos.

11. Lotes vencidos ou bloqueados não poderão ser utilizados.

12. Toda transferência deverá possuir confirmação de saída e recebimento.

13. Inventários deverão preservar as contagens originais.

14. Ajustes resultantes de inventário deverão exigir aprovação conforme alçada.

15. Toda perda deverá possuir motivo e evidência quando exigida.

16. Sobras somente poderão retornar ao estoque quando atenderem à dimensão mínima configurada.

17. Sobras deverão manter vínculo com material, projeto e plano de corte de origem.

18. O consumo deverá manter vínculo com projeto, ordem ou operação.

19. Entradas e saídas confirmadas não poderão ser excluídas, apenas estornadas.

20. Todo estorno deverá preservar a movimentação original.

21. O custo médio deverá ser recalculado conforme o método configurado.

22. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Estoque será a fonte oficial dos saldos físicos e da disponibilidade dos itens.

Projetos deverá informar o que será necessário.

Compras deverá informar o que foi adquirido e o que está em trânsito.

PCP e Produção deverão consumir materiais por meio de reservas, requisições e movimentações formais.

Nenhum módulo poderá alterar saldos diretamente.

Toda alteração de saldo deverá ocorrer por uma movimentação registrada no módulo Estoque.

---

# Próxima Etapa

```text
ETAPA 03-H

Catálogo Completo de Páginas

PCP
```
---

# ETAPA 03-H

# Catálogo Completo de Páginas

# PCP — Planejamento e Controle da Produção

## ID do Módulo

```text
PCP
```

---

# Objetivo

O módulo PCP é responsável por transformar pedidos e projetos liberados em um plano executável de produção.

Ele deverá planejar:

* o que produzir;
* quando produzir;
* em qual sequência;
* com quais materiais;
* com quais máquinas;
* com quais pessoas;
* em qual setor;
* por quanto tempo;
* com qual prioridade;
* respeitando quais dependências.

O PCP deverá coordenar materiais, capacidade, recursos, prazos e prioridades antes da execução no módulo Produção.

Nenhuma ordem deverá entrar na fábrica sem planejamento ou liberação formal, exceto em processos emergenciais autorizados.

---

# Limites do Módulo

O módulo PCP será responsável por:

```text
Receber demandas de produção

Validar disponibilidade técnica

Validar disponibilidade de materiais

Calcular necessidades

Planejar capacidade

Criar ordens de produção

Programar operações

Sequenciar trabalhos

Definir prioridades

Reservar recursos

Controlar o plano produtivo

Reprogramar atividades

Analisar atrasos e gargalos
```

O módulo PCP não será responsável por:

```text
Criar ou alterar o projeto técnico

Modificar peças ou materiais

Comprar materiais diretamente

Movimentar estoque diretamente

Executar operações fabris

Registrar pagamentos

Realizar faturamento
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Compras

Estoque

Produção

Financeiro

Fiscal
```

---

# Fluxo Principal

```text
Pedido Aprovado

↓

Projeto Liberado para Produção

↓

Validação da Revisão Técnica

↓

Lista de Materiais

↓

Consulta de Estoque

↓

Identificação de Faltas

↓

Reserva de Materiais

↓

Planejamento de Capacidade

↓

Definição de Roteiro

↓

Criação da Ordem de Produção

↓

Programação das Operações

↓

Sequenciamento

↓

Liberação para Produção

↓

Acompanhamento do Plano

↓

Reprogramação quando Necessária

↓

Conclusão do Planejamento
```

---

# Estrutura Geral

```text
PCP — Planejamento e Controle da Produção

├── Dashboard do PCP
├── Demandas de Produção
├── Pedidos Aguardando Planejamento
├── Ordens de Produção
├── Planejamento de Materiais
├── Necessidades de Materiais
├── Disponibilidade de Materiais
├── Reservas Produtivas
├── Planejamento de Capacidade
├── Recursos Produtivos
├── Centros de Trabalho
├── Máquinas
├── Equipes
├── Calendários Produtivos
├── Turnos
├── Roteiros de Produção
├── Operações
├── Programação da Produção
├── Sequenciamento
├── Filas de Produção
├── Carga de Trabalho
├── Gargalos
├── Prioridades
├── Reprogramações
├── Simulações
├── Cronograma Geral
├── Acompanhamento do Plano
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
```

---

# Página

## Dashboard do PCP

### ID

```text
PCP-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada das demandas, ordens, materiais, capacidades, filas, atrasos e gargalos da produção.

### Componentes

```text
Demandas Aguardando Planejamento

Ordens Planejadas

Ordens Liberadas

Ordens Atrasadas

Ordens Bloqueadas

Materiais em Falta

Reservas Pendentes

Carga por Centro de Trabalho

Carga por Máquina

Carga por Equipe

Capacidade Disponível

Capacidade Comprometida

Gargalos Atuais

Fila por Setor

Produção Prevista

Produção Realizada

Aderência ao Plano

Alertas
```

### Filtros

```text
Período

Projeto

Cliente

Pedido

Ordem de Produção

Centro de Trabalho

Máquina

Equipe

Responsável

Status

Prioridade

Filial
```

### Ações

```text
Planejar Demanda

Criar Ordem de Produção

Abrir Programação

Abrir Sequenciamento

Abrir Materiais em Falta

Abrir Gargalos

Reprogramar

Simular Cenário

Exportar Dashboard

Atualizar Indicadores
```

---

# Página

## Demandas de Produção

### ID

```text
PCP-DEM-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar todas as necessidades que poderão originar ordens de produção.

### Origens

```text
Pedido de Venda

Projeto Liberado

Reposição de Estoque

Retrabalho

Assistência Técnica

Amostra

Protótipo

Solicitação Interna

Produção Emergencial
```

### Colunas

```text
Número

Origem

Cliente

Projeto

Pedido

Produto ou Móvel

Quantidade

Data Necessária

Prioridade

Revisão Técnica

Materiais Disponíveis

Capacidade Disponível

Status
```

### Status

```text
Recebida

Em Validação

Aguardando Projeto

Aguardando Materiais

Aguardando Capacidade

Pronta para Planejamento

Planejada

Parcialmente Planejada

Cancelada
```

### Ações

```text
Abrir Origem

Validar

Agrupar

Desagrupar

Alterar Prioridade

Alterar Data Necessária

Planejar

Criar Ordem

Bloquear

Desbloquear

Cancelar
```

---

# Página

## Pedidos Aguardando Planejamento

### ID

```text
PCP-PAP-001
```

### Tipo

```text
Kanban
```

### Objetivo

Visualizar os pedidos que ainda não possuem planejamento produtivo completo.

### Etapas

```text
Aguardando Projeto

Aguardando Aprovação Técnica

Aguardando Materiais

Aguardando Reserva

Aguardando Capacidade

Pronto para Planejamento

Planejado
```

### Funcionalidades

```text
Abrir Pedido

Abrir Projeto

Consultar Materiais

Consultar Capacidade

Criar Pendência

Alterar Prioridade

Planejar
```

---

# Página

## Ordens de Produção

### ID

```text
PCP-ODP-001
```

### Tipo

```text
Lista
```

### Objetivo

Criar, planejar e administrar as ordens que serão executadas pela Produção.

### Visualizações

```text
Tabela

Cards

Kanban

Timeline

Calendário

Gráfico de Gantt
```

### Colunas

```text
Número

Projeto

Pedido

Cliente

Produto ou Móvel

Quantidade

Revisão Técnica

Data Planejada

Data Necessária

Prioridade

Percentual Planejado

Materiais

Capacidade

Status
```

### Status

```text
Rascunho

Em Planejamento

Aguardando Materiais

Aguardando Capacidade

Aguardando Aprovação

Planejada

Liberada

Parcialmente Liberada

Em Produção

Pausada

Concluída

Cancelada

Encerrada
```

### Ações

```text
Nova Ordem

Abrir

Editar

Duplicar

Dividir Ordem

Agrupar Ordens

Planejar Materiais

Planejar Capacidade

Definir Roteiro

Programar

Sequenciar

Solicitar Aprovação

Liberar para Produção

Liberar Parcialmente

Bloquear

Pausar

Cancelar

Reprogramar

Exportar

Imprimir
```

---

# Página

## Cadastro da Ordem de Produção

### ID

```text
PCP-ODP-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações necessárias para planejar e liberar uma ordem de produção.

### Abas

```text
Geral

Origem

Projeto

Estrutura

Materiais

Reservas

Roteiro

Operações

Recursos

Capacidade

Programação

Sequenciamento

Terceirizações

Documentos

Pendências

Aprovações

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Descrição

Tipo de Ordem

Projeto

Pedido

Cliente

Produto ou Móvel

Quantidade

Unidade

Revisão Técnica

Prioridade

Responsável

Data de Criação

Data Planejada de Início

Data Planejada de Término

Data Necessária

Status

Observações
```

### Aba Origem

Informações:

```text
Tipo de Origem

Documento de Origem

Pedido

Projeto

Assistência

Retrabalho

Solicitante

Justificativa
```

### Aba Projeto

Informações:

```text
Projeto

Ambiente

Móvel

Revisão

Documentos Técnicos

Lista de Peças

Lista de Materiais

Plano de Corte

Pendências

Liberação
```

### Aba Estrutura

Informações:

```text
Móveis

Componentes

Peças

Materiais

Ferragens

Serviços

Dependências

Quantidades
```

### Aba Materiais

Informações:

```text
Item

Quantidade Necessária

Quantidade Disponível

Quantidade Reservada

Quantidade em Compra

Quantidade Faltante

Data Prevista

Status
```

### Aba Reservas

Informações:

```text
Reserva

Item

Quantidade

Almoxarifado

Localização

Lote

Status

Data da Reserva
```

### Aba Roteiro

Informações:

```text
Sequência

Operação

Centro de Trabalho

Máquina

Equipe

Tempo de Preparação

Tempo Unitário

Tempo Total

Dependência

Terceirizada
```

### Aba Operações

Informações:

```text
Código

Descrição

Sequência

Quantidade

Unidade

Tempo Previsto

Recurso

Predecessora

Status de Planejamento
```

### Aba Recursos

Informações:

```text
Centro de Trabalho

Máquina

Ferramenta

Equipe

Funcionário

Terceirizado

Disponibilidade

Capacidade
```

### Aba Capacidade

Informações:

```text
Recurso

Carga Necessária

Capacidade Disponível

Capacidade Comprometida

Sobrecarga

Folga

Período
```

### Aba Programação

Informações:

```text
Operação

Data Inicial

Hora Inicial

Data Final

Hora Final

Duração

Recurso

Responsável

Status
```

### Aba Sequenciamento

Informações:

```text
Posição

Operação

Ordem

Prioridade

Data Necessária

Setup

Material

Restrição

Motivo da Posição
```

### Aba Terceirizações

Informações:

```text
Serviço

Fornecedor

Data de Envio

Data Prevista

Quantidade

Custo Previsto

Status

Dependências
```

### Aba Pendências

Informações:

```text
Descrição

Categoria

Responsável

Prioridade

Prazo

Impacto

Status

Solução
```

### Aba Aprovações

Informações:

```text
Planejamento

Materiais

Capacidade

Terceirização

Prioridade Especial

Liberação Parcial

Liberação para Produção
```

---

# Página

## Planejamento de Materiais

### ID

```text
PCP-MRP-001
```

### Tipo

```text
Painel
```

### Objetivo

Calcular as necessidades de materiais para atender às demandas produtivas.

### Entradas

```text
Demandas

Ordens de Produção

Estruturas de Produto

Listas de Materiais

Saldos

Reservas

Pedidos de Compra

Materiais em Trânsito

Estoques Mínimos

Lotes Disponíveis
```

### Saídas

```text
Materiais Disponíveis

Materiais Reserváveis

Materiais em Falta

Necessidades de Compra

Datas de Necessidade

Sugestões de Substituição

Riscos de Ruptura
```

### Funcionalidades

```text
Executar MRP

Recalcular

Selecionar Escopo

Simular Data

Alterar Parâmetros

Explodir Estrutura

Consolidar Necessidades

Criar Reservas

Criar Necessidades de Compra

Exportar Resultado
```

---

# Página

## Necessidades de Materiais

### ID

```text
PCP-NEM-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar materiais necessários para atender ao plano de produção.

### Colunas

```text
Item

Descrição

Projeto

Ordem

Quantidade Necessária

Saldo Disponível

Saldo Reservado

Saldo em Compra

Falta

Data Necessária

Prioridade

Status
```

### Status

```text
Atendida

Atendida por Reserva

Atendida por Compra

Parcialmente Atendida

Em Falta

Aguardando Substituição

Bloqueada
```

---

# Página

## Disponibilidade de Materiais

### ID

```text
PCP-DIM-001
```

### Tipo

```text
Consulta
```

### Objetivo

Analisar se os materiais estarão disponíveis na data planejada de produção.

### Informações

```text
Saldo Atual

Saldo Disponível

Reservas Existentes

Pedidos em Aberto

Datas de Recebimento

Consumos Programados

Cobertura

Data Estimada de Disponibilidade
```

---

# Página

## Reservas Produtivas

### ID

```text
PCP-REP-001
```

### Tipo

```text
Lista
```

### Objetivo

Solicitar e acompanhar reservas de materiais vinculadas às ordens de produção.

### Ações

```text
Criar Reserva

Confirmar Reserva

Alterar Quantidade

Substituir Item

Liberar Reserva

Cancelar Reserva

Abrir Estoque

Abrir Ordem
```

---

# Página

## Planejamento de Capacidade

### ID

```text
PCP-CAP-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Comparar a carga produtiva necessária com a capacidade disponível.

### Dimensões

```text
Centro de Trabalho

Máquina

Equipe

Funcionário

Turno

Dia

Semana

Mês
```

### Informações

```text
Capacidade Teórica

Capacidade Disponível

Capacidade Comprometida

Capacidade Realizada

Sobrecarga

Folga

Eficiência

Disponibilidade
```

### Funcionalidades

```text
Calcular Capacidade

Selecionar Período

Alterar Calendário

Simular Turno Extra

Simular Terceirização

Mover Carga

Redistribuir Operações

Exportar
```

---

# Página

## Recursos Produtivos

### ID

```text
PCP-REC-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar todos os recursos que podem ser utilizados no planejamento produtivo.

### Tipos

```text
Centro de Trabalho

Máquina

Equipamento

Ferramenta

Equipe

Funcionário

Terceirizado

Área Física
```

---

# Página

## Centros de Trabalho

### ID

```text
PCP-CTR-001
```

### Tipo

```text
Lista
```

### Objetivo

Representar setores ou agrupamentos onde operações produtivas são executadas.

### Exemplos

```text
Preparação

Corte

Usinagem

Fitagem

Pré-montagem

Montagem

Acabamento

Limpeza

Embalagem

Expedição
```

### Campos

```text
Código

Descrição

Responsável

Capacidade

Unidade de Capacidade

Calendário

Turno

Eficiência

Status
```

---

# Página

## Máquinas

### ID

```text
PCP-MAQ-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar máquinas consideradas no planejamento.

### Informações

```text
Código

Descrição

Centro de Trabalho

Capacidade

Calendário

Tempo de Setup

Eficiência

Disponibilidade

Manutenções Programadas

Status
```

---

# Página

## Equipes

### ID

```text
PCP-EQP-001
```

### Tipo

```text
Lista
```

### Objetivo

Organizar os grupos de pessoas considerados no planejamento da produção.

### Informações

```text
Equipe

Líder

Integrantes

Habilidades

Centro de Trabalho

Turno

Capacidade

Disponibilidade
```

---

# Página

## Calendários Produtivos

### ID

```text
PCP-CAL-001
```

### Tipo

```text
Calendário
```

### Objetivo

Definir dias e horários disponíveis para produção.

### Elementos

```text
Dias Úteis

Feriados

Folgas

Turnos

Horas Extras

Paradas Programadas

Manutenções

Férias

Bloqueios
```

### Funcionalidades

```text
Novo Calendário

Aplicar a Recursos

Adicionar Exceção

Adicionar Feriado

Adicionar Parada

Adicionar Hora Extra

Duplicar Calendário

Importar

Exportar
```

---

# Página

## Turnos

### ID

```text
PCP-TUR-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir períodos regulares de trabalho utilizados no cálculo de capacidade.

### Campos

```text
Nome

Hora Inicial

Hora Final

Intervalos

Horas Líquidas

Dias da Semana

Centro de Trabalho

Equipe

Status
```

---

# Página

## Roteiros de Produção

### ID

```text
PCP-ROT-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir a sequência padrão de operações necessárias para produzir um item ou projeto.

### Exemplos

```text
Corte

↓

Usinagem

↓

Fitagem

↓

Montagem

↓

Acabamento

↓

Limpeza

↓

Embalagem
```

### Funcionalidades

```text
Novo Roteiro

Editar

Duplicar

Aplicar a Produto

Aplicar a Ordem

Adicionar Operação

Reordenar Operações

Definir Dependências

Calcular Tempo

Versionar

Arquivar
```

---

# Página

## Operações

### ID

```text
PCP-OPE-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar os tipos de trabalho utilizados nos roteiros e programações.

### Exemplos

```text
Separar Material

Cortar

Usinar

Furar

Fitar

Montar

Instalar Ferragens

Conferir

Limpar

Embalar

Carregar

Terceirizar
```

### Campos

```text
Código

Descrição

Centro de Trabalho Padrão

Máquina Padrão

Tempo de Setup

Tempo Unitário

Unidade de Capacidade

Habilidade Necessária

Terceirização Permitida

Status
```

---

# Página

## Programação da Produção

### ID

```text
PCP-PRO-001
```

### Tipo

```text
Gráfico de Gantt
```

### Objetivo

Distribuir operações no tempo, considerando recursos, capacidade, materiais e dependências.

### Visualizações

```text
Gráfico de Gantt

Calendário

Timeline

Tabela

Por Centro de Trabalho

Por Máquina

Por Equipe

Por Ordem
```

### Funcionalidades

```text
Programar Automaticamente

Programar Manualmente

Mover Operação

Redimensionar Duração

Trocar Recurso

Dividir Operação

Bloquear Programação

Recalcular

Validar Conflitos

Publicar Programação

Reprogramar
```

### Restrições

```text
Disponibilidade de Material

Capacidade

Calendário

Turno

Manutenção

Dependências

Prioridade

Data Necessária

Recurso Obrigatório

Habilidade Necessária
```

---

# Página

## Sequenciamento

### ID

```text
PCP-SEQ-001
```

### Tipo

```text
Kanban
```

### Objetivo

Definir a ordem de execução das operações em cada fila produtiva.

### Critérios

```text
Prioridade

Data Necessária

Prazo do Cliente

Disponibilidade de Material

Tempo de Setup

Material

Espessura

Cor

Máquina

Dependência

Projeto

Urgência
```

### Funcionalidades

```text
Sequenciar Automaticamente

Alterar Posição

Fixar Operação

Agrupar por Material

Agrupar por Espessura

Agrupar por Setup

Aplicar Regra

Simular Sequência

Publicar Sequência

Restaurar Sequência
```

---

# Página

## Filas de Produção

### ID

```text
PCP-FIL-001
```

### Tipo

```text
Kanban
```

### Objetivo

Visualizar a fila planejada de cada centro de trabalho ou recurso.

### Etapas

```text
Não Programada

Programada

Aguardando Material

Aguardando Liberação

Pronta para Produção

Liberada

Em Execução

Pausada

Concluída
```

### Ações

```text
Alterar Prioridade

Mover na Fila

Bloquear

Liberar

Abrir Ordem

Abrir Material

Abrir Recurso

Registrar Pendência
```

---

# Página

## Carga de Trabalho

### ID

```text
PCP-CAR-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Analisar a distribuição de horas e atividades entre recursos produtivos.

### Visualizações

```text
Carga por Centro

Carga por Máquina

Carga por Equipe

Carga por Funcionário

Carga por Dia

Carga por Semana

Carga por Projeto
```

### Indicadores

```text
Horas Disponíveis

Horas Planejadas

Horas Comprometidas

Horas Realizadas

Sobrecarga

Ociosidade

Eficiência Planejada
```

---

# Página

## Gargalos

### ID

```text
PCP-GAR-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Identificar recursos ou etapas que limitam o fluxo da produção.

### Tipos de Gargalo

```text
Material

Máquina

Equipe

Funcionário

Ferramenta

Terceirizado

Espaço

Aprovação

Documento Técnico

Capacidade
```

### Funcionalidades

```text
Identificar Gargalo

Analisar Impacto

Abrir Ordens Afetadas

Simular Alternativa

Redistribuir Carga

Criar Ação

Notificar Responsável
```

---

# Página

## Prioridades

### ID

```text
PCP-PRI-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir e controlar prioridades produtivas.

### Níveis

```text
Crítica

Urgente

Alta

Normal

Baixa

Planejada
```

### Campos

```text
Ordem

Prioridade

Motivo

Solicitante

Aprovador

Data Inicial

Validade

Impacto

Status
```

### Regras

```text
Toda prioridade especial deverá possuir justificativa.

Prioridades acima da alçada deverão exigir aprovação.

Alterações deverão permanecer auditadas.
```

---

# Página

## Reprogramações

### ID

```text
PCP-REP-002
```

### Tipo

```text
Timeline
```

### Objetivo

Controlar alterações realizadas após a publicação do plano produtivo.

### Motivos

```text
Falta de Material

Atraso de Compra

Quebra de Máquina

Ausência de Funcionário

Retrabalho

Alteração de Projeto

Prioridade Comercial

Atraso de Terceiro

Problema de Qualidade

Mudança de Prazo
```

### Informações

```text
Plano Anterior

Novo Plano

Motivo

Responsável

Ordens Afetadas

Impacto no Prazo

Impacto na Capacidade

Data

Aprovação
```

---

# Página

## Simulações

### ID

```text
PCP-SIM-001
```

### Tipo

```text
Simulador
```

### Objetivo

Testar cenários produtivos sem alterar o plano oficial.

### Cenários

```text
Turno Extra

Hora Extra

Nova Máquina

Máquina Indisponível

Equipe Reduzida

Terceirização

Mudança de Prioridade

Antecipação de Pedido

Atraso de Material

Alteração de Prazo

Redistribuição de Carga
```

### Resultados

```text
Data de Conclusão

Sobrecarga

Ociosidade

Custo Estimado

Ordens Afetadas

Gargalos

Riscos
```

---

# Página

## Cronograma Geral

### ID

```text
PCP-CRO-001
```

### Tipo

```text
Gráfico de Gantt
```

### Objetivo

Apresentar todas as ordens, operações, projetos e recursos dentro de uma visão temporal única.

### Visualizações

```text
Por Projeto

Por Ordem

Por Centro de Trabalho

Por Máquina

Por Equipe

Por Cliente

Por Data de Entrega
```

---

# Página

## Acompanhamento do Plano

### ID

```text
PCP-ACP-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Comparar o planejamento publicado com a execução registrada na Produção.

### Comparações

```text
Início Planejado x Real

Término Planejado x Real

Tempo Planejado x Real

Quantidade Planejada x Real

Recurso Planejado x Utilizado

Material Previsto x Consumido

Sequência Planejada x Executada
```

### Status

```text
No Prazo

Adiantada

Em Risco

Atrasada

Bloqueada

Reprogramada
```

---

# Página

## Indicadores

### ID

```text
PCP-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Aderência ao Plano

Ordens Planejadas

Ordens Liberadas

Ordens Atrasadas

Capacidade Utilizada

Sobrecarga

Ociosidade

Tempo Médio de Planejamento

Tempo Médio de Fila

Materiais em Falta

Reprogramações

Gargalos

Cumprimento de Prazo

Precisão dos Tempos Planejados

Carga por Centro de Trabalho

Carga por Projeto
```

---

# Página

## Relatórios

### ID

```text
PCP-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Demandas de Produção

Pedidos Aguardando Planejamento

Ordens de Produção

Planejamento de Materiais

Necessidades de Materiais

Materiais em Falta

Reservas Produtivas

Capacidade por Recurso

Carga de Trabalho

Programação da Produção

Sequenciamento

Filas de Produção

Gargalos

Prioridades

Reprogramações

Cronograma Geral

Planejado x Realizado

Aderência ao Plano

Ordens em Risco

Ordens Atrasadas
```

---

# Página

## Templates

### ID

```text
PCP-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para estruturas e processos de planejamento.

### Tipos

```text
Roteiro de Produção

Calendário

Turno

Ordem de Produção

Programação

Checklist de Liberação

Regra de Sequenciamento

Relatório
```

---

# Página

## Configurações

### ID

```text
PCP-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Numeração das Ordens

Tipos de Ordem

Status

Prioridades

Centros de Trabalho

Máquinas

Equipes

Calendários

Turnos

Operações

Roteiros

Unidades de Capacidade

Eficiência Padrão

Tempos de Setup

Regras de MRP

Regras de Capacidade

Regras de Sequenciamento

Regras de Liberação

Regras de Reprogramação

Horizonte de Planejamento

Templates

Checklists

Notificações

Integrações
```

---

# Dialogs

```text
PCP-DLG-001 Nova Demanda

PCP-DLG-002 Validar Demanda

PCP-DLG-003 Nova Ordem de Produção

PCP-DLG-004 Selecionar Projeto

PCP-DLG-005 Selecionar Revisão Técnica

PCP-DLG-006 Dividir Ordem

PCP-DLG-007 Agrupar Ordens

PCP-DLG-008 Executar MRP

PCP-DLG-009 Criar Reservas

PCP-DLG-010 Criar Necessidade de Compra

PCP-DLG-011 Selecionar Roteiro

PCP-DLG-012 Adicionar Operação

PCP-DLG-013 Selecionar Centro de Trabalho

PCP-DLG-014 Selecionar Máquina

PCP-DLG-015 Selecionar Equipe

PCP-DLG-016 Configurar Capacidade

PCP-DLG-017 Programar Operação

PCP-DLG-018 Trocar Recurso

PCP-DLG-019 Dividir Operação

PCP-DLG-020 Sequenciar Operações

PCP-DLG-021 Alterar Prioridade

PCP-DLG-022 Registrar Gargalo

PCP-DLG-023 Simular Cenário

PCP-DLG-024 Solicitar Aprovação

PCP-DLG-025 Aprovar Planejamento

PCP-DLG-026 Liberar para Produção

PCP-DLG-027 Liberar Parcialmente

PCP-DLG-028 Bloquear Ordem

PCP-DLG-029 Reprogramar Ordem

PCP-DLG-030 Registrar Motivo de Reprogramação

PCP-DLG-031 Cancelar Ordem

PCP-DLG-032 Encerrar Planejamento

PCP-DLG-033 Novo Centro de Trabalho

PCP-DLG-034 Nova Máquina

PCP-DLG-035 Nova Equipe

PCP-DLG-036 Novo Calendário

PCP-DLG-037 Novo Turno

PCP-DLG-038 Novo Roteiro

PCP-DLG-039 Nova Operação

PCP-DLG-040 Exportar Plano
```

---

# Wizards

```text
PCP-WIZ-001 Assistente de Planejamento da Demanda

PCP-WIZ-002 Assistente de Ordem de Produção

PCP-WIZ-003 Assistente de MRP

PCP-WIZ-004 Assistente de Reserva de Materiais

PCP-WIZ-005 Assistente de Roteiro de Produção

PCP-WIZ-006 Assistente de Planejamento de Capacidade

PCP-WIZ-007 Assistente de Programação

PCP-WIZ-008 Assistente de Sequenciamento

PCP-WIZ-009 Assistente de Liberação para Produção

PCP-WIZ-010 Assistente de Reprogramação

PCP-WIZ-011 Assistente de Simulação

PCP-WIZ-012 Assistente de Configuração Inicial do PCP
```

---

# Componentes Específicos

```text
PCP-CPT-001 Painel de Demandas

PCP-CPT-002 Editor de Ordem de Produção

PCP-CPT-003 Explosão de Estrutura

PCP-CPT-004 Painel de MRP

PCP-CPT-005 Matriz de Disponibilidade de Materiais

PCP-CPT-006 Matriz de Capacidade

PCP-CPT-007 Mapa de Carga

PCP-CPT-008 Editor de Roteiro

PCP-CPT-009 Gráfico de Gantt Produtivo

PCP-CPT-010 Calendário de Recursos

PCP-CPT-011 Sequenciador de Operações

PCP-CPT-012 Kanban de Filas

PCP-CPT-013 Painel de Gargalos

PCP-CPT-014 Simulador de Cenários

PCP-CPT-015 Comparador Planejado x Realizado

PCP-CPT-016 Checklist de Liberação

PCP-CPT-017 Indicador de Risco de Atraso

PCP-CPT-018 Timeline de Reprogramações
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
ProductionDemandCreated

ProductionDemandValidated

ProductionDemandBlocked

ProductionOrderCreated

ProductionOrderPlanned

ProductionOrderSplit

ProductionOrderGrouped

MaterialRequirementsCalculated

ProductionMaterialShortageDetected

ProductionMaterialsReserved

ProductionCapacityCalculated

ProductionCapacityOverloadDetected

ProductionRouteAssigned

ProductionOperationScheduled

ProductionSequenceGenerated

ProductionPriorityChanged

ProductionBottleneckDetected

ProductionPlanPublished

ProductionOrderReleased

ProductionOrderPartiallyReleased

ProductionOrderBlocked

ProductionOrderRescheduled

ProductionSimulationCreated

ProductionPlanDeviationDetected

ProductionOrderPlanningCompleted

ProductionOrderCancelled
```

---

# Automações

```text
Projeto liberado para produção

↓

Criar demanda de produção

↓

Validar revisão técnica

↓

Importar estrutura

↓

Importar lista de materiais

↓

Criar pendências de planejamento
```

```text
Demanda validada

↓

Executar consulta de disponibilidade

↓

Criar reservas possíveis

↓

Identificar materiais faltantes

↓

Notificar Compras
```

```text
Materiais disponíveis

↓

Calcular capacidade

↓

Sugerir roteiro

↓

Sugerir datas

↓

Criar ordem planejada
```

```text
Sobrecarga detectada

↓

Identificar recurso crítico

↓

Sugerir redistribuição

↓

Sugerir turno extra

↓

Sugerir terceirização
```

```text
Plano publicado

↓

Liberar filas produtivas

↓

Notificar Produção

↓

Disponibilizar documentos

↓

Registrar versão do plano
```

```text
Desvio identificado

↓

Calcular impacto

↓

Marcar ordem em risco

↓

Notificar PCP

↓

Sugerir reprogramação
```

---

# Integrações

```text
CRM

Comercial

Projetos

Orçamentos

Compras

Estoque

Produção

Qualidade

Manutenção

Expedição

Instalação

Financeiro

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização
```

---

# Permissões

```text
pcp.dashboard.read

pcp.demand.read

pcp.demand.create

pcp.demand.validate

pcp.demand.block

pcp.order.read

pcp.order.create

pcp.order.update

pcp.order.split

pcp.order.group

pcp.order.cancel

pcp.material_planning.read

pcp.material_planning.execute

pcp.material_requirement.manage

pcp.material_reservation.create

pcp.material_purchase_need.create

pcp.capacity.read

pcp.capacity.calculate

pcp.capacity.override

pcp.resource.read

pcp.resource.manage

pcp.work_center.manage

pcp.machine.manage

pcp.team.manage

pcp.calendar.manage

pcp.shift.manage

pcp.route.read

pcp.route.create

pcp.route.update

pcp.operation.manage

pcp.scheduling.read

pcp.scheduling.manage

pcp.scheduling.publish

pcp.sequence.read

pcp.sequence.manage

pcp.queue.read

pcp.queue.manage

pcp.workload.read

pcp.bottleneck.read

pcp.bottleneck.manage

pcp.priority.update

pcp.priority.approve

pcp.reschedule.create

pcp.reschedule.approve

pcp.simulation.create

pcp.simulation.read

pcp.production_release.request

pcp.production_release.approve

pcp.production_release.execute

pcp.report.read

pcp.report.export

pcp.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Plano Mestre de Produção

Demanda de Produção

Ordem de Produção Planejada

Lista de Materiais da Ordem

Necessidades de Materiais

Relatório de Faltas

Ficha de Reserva

Roteiro de Produção

Lista de Operações

Programação da Produção

Sequenciamento por Centro

Carga por Recurso

Mapa de Capacidade

Cronograma Produtivo

Relatório de Gargalos

Relatório de Prioridades

Relatório de Reprogramações

Checklist de Liberação

Plano Publicado

Comparativo Planejado x Realizado

Relatório de Aderência ao Plano
```

---

# Recursos de Inteligência Artificial

```text
Sugerir agrupamento de demandas

Sugerir datas de produção

Sugerir roteiro

Estimar tempos de operação

Prever falta de materiais

Prever sobrecarga

Detectar gargalos

Sugerir redistribuição de carga

Sugerir sequenciamento

Reduzir trocas de setup

Prever atraso de ordens

Analisar impacto de prioridade

Sugerir terceirização

Simular cenários

Comparar plano com execução

Identificar padrões de reprogramação

Explicar causas de atraso

Pesquisar o plano em linguagem natural
```

A IA nunca poderá publicar planos, alterar prioridades, liberar ordens ou reprogramar operações sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Toda demanda deverá pertencer a um Tenant.

2. Toda ordem deverá possuir origem identificada.

3. Ordens vinculadas a projetos deverão utilizar uma revisão técnica válida e liberada.

4. Uma ordem não poderá ser liberada sem roteiro ou operações planejadas.

5. A liberação deverá verificar materiais, documentos e recursos obrigatórios.

6. O planejamento deverá considerar calendários, turnos, indisponibilidades e manutenções.

7. A capacidade não poderá ser considerada infinita.

8. Sobrecargas deverão ser sinalizadas antes da publicação do plano.

9. Materiais faltantes deverão bloquear ou restringir a liberação conforme política.

10. Reservas deverão ser solicitadas ao módulo Estoque.

11. Necessidades de compra deverão ser enviadas ao módulo Compras.

12. Nenhuma alteração do PCP poderá modificar a estrutura técnica do projeto.

13. Mudanças técnicas deverão retornar ao módulo Projetos.

14. Uma programação publicada deverá possuir versão.

15. Alterações posteriores deverão gerar reprogramação auditada.

16. Prioridades especiais deverão possuir justificativa.

17. Ordens poderão ser divididas ou agrupadas mantendo rastreabilidade.

18. Operações deverão respeitar dependências técnicas.

19. O sequenciamento deverá considerar restrições reais.

20. O acompanhamento deverá comparar o planejado com o realizado.

21. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O PCP será a fonte oficial do planejamento produtivo.

Projetos deverá definir o que será fabricado.

Estoque deverá informar o que está disponível.

Compras deverá informar o que será recebido.

PCP deverá decidir quando e em qual sequência produzir.

Produção deverá executar e apontar o que foi planejado, sem alterar silenciosamente o plano.

Qualquer desvio deverá retornar ao PCP para análise, reprogramação e atualização dos prazos afetados.

---

# Próxima Etapa

```text
ETAPA 03-I

Catálogo Completo de Páginas

Produção
```
---

# ETAPA 03-H

# Catálogo Completo de Páginas

# PCP — Planejamento e Controle da Produção

## ID do Módulo

```text
PCP
```

---

# Objetivo

O módulo PCP é responsável por transformar pedidos e projetos liberados em um plano executável de produção.

Ele deverá planejar:

* o que produzir;
* quando produzir;
* em qual sequência;
* com quais materiais;
* com quais máquinas;
* com quais pessoas;
* em qual setor;
* por quanto tempo;
* com qual prioridade;
* respeitando quais dependências.

O PCP deverá coordenar materiais, capacidade, recursos, prazos e prioridades antes da execução no módulo Produção.

Nenhuma ordem deverá entrar na fábrica sem planejamento ou liberação formal, exceto em processos emergenciais autorizados.

---

# Limites do Módulo

O módulo PCP será responsável por:

```text
Receber demandas de produção

Validar disponibilidade técnica

Validar disponibilidade de materiais

Calcular necessidades

Planejar capacidade

Criar ordens de produção

Programar operações

Sequenciar trabalhos

Definir prioridades

Reservar recursos

Controlar o plano produtivo

Reprogramar atividades

Analisar atrasos e gargalos
```

O módulo PCP não será responsável por:

```text
Criar ou alterar o projeto técnico

Modificar peças ou materiais

Comprar materiais diretamente

Movimentar estoque diretamente

Executar operações fabris

Registrar pagamentos

Realizar faturamento
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Compras

Estoque

Produção

Financeiro

Fiscal
```

---

# Fluxo Principal

```text
Pedido Aprovado

↓

Projeto Liberado para Produção

↓

Validação da Revisão Técnica

↓

Lista de Materiais

↓

Consulta de Estoque

↓

Identificação de Faltas

↓

Reserva de Materiais

↓

Planejamento de Capacidade

↓

Definição de Roteiro

↓

Criação da Ordem de Produção

↓

Programação das Operações

↓

Sequenciamento

↓

Liberação para Produção

↓

Acompanhamento do Plano

↓

Reprogramação quando Necessária

↓

Conclusão do Planejamento
```

---

# Estrutura Geral

```text
PCP — Planejamento e Controle da Produção

├── Dashboard do PCP
├── Demandas de Produção
├── Pedidos Aguardando Planejamento
├── Ordens de Produção
├── Planejamento de Materiais
├── Necessidades de Materiais
├── Disponibilidade de Materiais
├── Reservas Produtivas
├── Planejamento de Capacidade
├── Recursos Produtivos
├── Centros de Trabalho
├── Máquinas
├── Equipes
├── Calendários Produtivos
├── Turnos
├── Roteiros de Produção
├── Operações
├── Programação da Produção
├── Sequenciamento
├── Filas de Produção
├── Carga de Trabalho
├── Gargalos
├── Prioridades
├── Reprogramações
├── Simulações
├── Cronograma Geral
├── Acompanhamento do Plano
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
```

---

# Página

## Dashboard do PCP

### ID

```text
PCP-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada das demandas, ordens, materiais, capacidades, filas, atrasos e gargalos da produção.

### Componentes

```text
Demandas Aguardando Planejamento

Ordens Planejadas

Ordens Liberadas

Ordens Atrasadas

Ordens Bloqueadas

Materiais em Falta

Reservas Pendentes

Carga por Centro de Trabalho

Carga por Máquina

Carga por Equipe

Capacidade Disponível

Capacidade Comprometida

Gargalos Atuais

Fila por Setor

Produção Prevista

Produção Realizada

Aderência ao Plano

Alertas
```

### Filtros

```text
Período

Projeto

Cliente

Pedido

Ordem de Produção

Centro de Trabalho

Máquina

Equipe

Responsável

Status

Prioridade

Filial
```

### Ações

```text
Planejar Demanda

Criar Ordem de Produção

Abrir Programação

Abrir Sequenciamento

Abrir Materiais em Falta

Abrir Gargalos

Reprogramar

Simular Cenário

Exportar Dashboard

Atualizar Indicadores
```

---

# Página

## Demandas de Produção

### ID

```text
PCP-DEM-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar todas as necessidades que poderão originar ordens de produção.

### Origens

```text
Pedido de Venda

Projeto Liberado

Reposição de Estoque

Retrabalho

Assistência Técnica

Amostra

Protótipo

Solicitação Interna

Produção Emergencial
```

### Colunas

```text
Número

Origem

Cliente

Projeto

Pedido

Produto ou Móvel

Quantidade

Data Necessária

Prioridade

Revisão Técnica

Materiais Disponíveis

Capacidade Disponível

Status
```

### Status

```text
Recebida

Em Validação

Aguardando Projeto

Aguardando Materiais

Aguardando Capacidade

Pronta para Planejamento

Planejada

Parcialmente Planejada

Cancelada
```

### Ações

```text
Abrir Origem

Validar

Agrupar

Desagrupar

Alterar Prioridade

Alterar Data Necessária

Planejar

Criar Ordem

Bloquear

Desbloquear

Cancelar
```

---

# Página

## Pedidos Aguardando Planejamento

### ID

```text
PCP-PAP-001
```

### Tipo

```text
Kanban
```

### Objetivo

Visualizar os pedidos que ainda não possuem planejamento produtivo completo.

### Etapas

```text
Aguardando Projeto

Aguardando Aprovação Técnica

Aguardando Materiais

Aguardando Reserva

Aguardando Capacidade

Pronto para Planejamento

Planejado
```

### Funcionalidades

```text
Abrir Pedido

Abrir Projeto

Consultar Materiais

Consultar Capacidade

Criar Pendência

Alterar Prioridade

Planejar
```

---

# Página

## Ordens de Produção

### ID

```text
PCP-ODP-001
```

### Tipo

```text
Lista
```

### Objetivo

Criar, planejar e administrar as ordens que serão executadas pela Produção.

### Visualizações

```text
Tabela

Cards

Kanban

Timeline

Calendário

Gráfico de Gantt
```

### Colunas

```text
Número

Projeto

Pedido

Cliente

Produto ou Móvel

Quantidade

Revisão Técnica

Data Planejada

Data Necessária

Prioridade

Percentual Planejado

Materiais

Capacidade

Status
```

### Status

```text
Rascunho

Em Planejamento

Aguardando Materiais

Aguardando Capacidade

Aguardando Aprovação

Planejada

Liberada

Parcialmente Liberada

Em Produção

Pausada

Concluída

Cancelada

Encerrada
```

### Ações

```text
Nova Ordem

Abrir

Editar

Duplicar

Dividir Ordem

Agrupar Ordens

Planejar Materiais

Planejar Capacidade

Definir Roteiro

Programar

Sequenciar

Solicitar Aprovação

Liberar para Produção

Liberar Parcialmente

Bloquear

Pausar

Cancelar

Reprogramar

Exportar

Imprimir
```

---

# Página

## Cadastro da Ordem de Produção

### ID

```text
PCP-ODP-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações necessárias para planejar e liberar uma ordem de produção.

### Abas

```text
Geral

Origem

Projeto

Estrutura

Materiais

Reservas

Roteiro

Operações

Recursos

Capacidade

Programação

Sequenciamento

Terceirizações

Documentos

Pendências

Aprovações

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Descrição

Tipo de Ordem

Projeto

Pedido

Cliente

Produto ou Móvel

Quantidade

Unidade

Revisão Técnica

Prioridade

Responsável

Data de Criação

Data Planejada de Início

Data Planejada de Término

Data Necessária

Status

Observações
```

### Aba Origem

Informações:

```text
Tipo de Origem

Documento de Origem

Pedido

Projeto

Assistência

Retrabalho

Solicitante

Justificativa
```

### Aba Projeto

Informações:

```text
Projeto

Ambiente

Móvel

Revisão

Documentos Técnicos

Lista de Peças

Lista de Materiais

Plano de Corte

Pendências

Liberação
```

### Aba Estrutura

Informações:

```text
Móveis

Componentes

Peças

Materiais

Ferragens

Serviços

Dependências

Quantidades
```

### Aba Materiais

Informações:

```text
Item

Quantidade Necessária

Quantidade Disponível

Quantidade Reservada

Quantidade em Compra

Quantidade Faltante

Data Prevista

Status
```

### Aba Reservas

Informações:

```text
Reserva

Item

Quantidade

Almoxarifado

Localização

Lote

Status

Data da Reserva
```

### Aba Roteiro

Informações:

```text
Sequência

Operação

Centro de Trabalho

Máquina

Equipe

Tempo de Preparação

Tempo Unitário

Tempo Total

Dependência

Terceirizada
```

### Aba Operações

Informações:

```text
Código

Descrição

Sequência

Quantidade

Unidade

Tempo Previsto

Recurso

Predecessora

Status de Planejamento
```

### Aba Recursos

Informações:

```text
Centro de Trabalho

Máquina

Ferramenta

Equipe

Funcionário

Terceirizado

Disponibilidade

Capacidade
```

### Aba Capacidade

Informações:

```text
Recurso

Carga Necessária

Capacidade Disponível

Capacidade Comprometida

Sobrecarga

Folga

Período
```

### Aba Programação

Informações:

```text
Operação

Data Inicial

Hora Inicial

Data Final

Hora Final

Duração

Recurso

Responsável

Status
```

### Aba Sequenciamento

Informações:

```text
Posição

Operação

Ordem

Prioridade

Data Necessária

Setup

Material

Restrição

Motivo da Posição
```

### Aba Terceirizações

Informações:

```text
Serviço

Fornecedor

Data de Envio

Data Prevista

Quantidade

Custo Previsto

Status

Dependências
```

### Aba Pendências

Informações:

```text
Descrição

Categoria

Responsável

Prioridade

Prazo

Impacto

Status

Solução
```

### Aba Aprovações

Informações:

```text
Planejamento

Materiais

Capacidade

Terceirização

Prioridade Especial

Liberação Parcial

Liberação para Produção
```

---

# Página

## Planejamento de Materiais

### ID

```text
PCP-MRP-001
```

### Tipo

```text
Painel
```

### Objetivo

Calcular as necessidades de materiais para atender às demandas produtivas.

### Entradas

```text
Demandas

Ordens de Produção

Estruturas de Produto

Listas de Materiais

Saldos

Reservas

Pedidos de Compra

Materiais em Trânsito

Estoques Mínimos

Lotes Disponíveis
```

### Saídas

```text
Materiais Disponíveis

Materiais Reserváveis

Materiais em Falta

Necessidades de Compra

Datas de Necessidade

Sugestões de Substituição

Riscos de Ruptura
```

### Funcionalidades

```text
Executar MRP

Recalcular

Selecionar Escopo

Simular Data

Alterar Parâmetros

Explodir Estrutura

Consolidar Necessidades

Criar Reservas

Criar Necessidades de Compra

Exportar Resultado
```

---

# Página

## Necessidades de Materiais

### ID

```text
PCP-NEM-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar materiais necessários para atender ao plano de produção.

### Colunas

```text
Item

Descrição

Projeto

Ordem

Quantidade Necessária

Saldo Disponível

Saldo Reservado

Saldo em Compra

Falta

Data Necessária

Prioridade

Status
```

### Status

```text
Atendida

Atendida por Reserva

Atendida por Compra

Parcialmente Atendida

Em Falta

Aguardando Substituição

Bloqueada
```

---

# Página

## Disponibilidade de Materiais

### ID

```text
PCP-DIM-001
```

### Tipo

```text
Consulta
```

### Objetivo

Analisar se os materiais estarão disponíveis na data planejada de produção.

### Informações

```text
Saldo Atual

Saldo Disponível

Reservas Existentes

Pedidos em Aberto

Datas de Recebimento

Consumos Programados

Cobertura

Data Estimada de Disponibilidade
```

---

# Página

## Reservas Produtivas

### ID

```text
PCP-REP-001
```

### Tipo

```text
Lista
```

### Objetivo

Solicitar e acompanhar reservas de materiais vinculadas às ordens de produção.

### Ações

```text
Criar Reserva

Confirmar Reserva

Alterar Quantidade

Substituir Item

Liberar Reserva

Cancelar Reserva

Abrir Estoque

Abrir Ordem
```

---

# Página

## Planejamento de Capacidade

### ID

```text
PCP-CAP-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Comparar a carga produtiva necessária com a capacidade disponível.

### Dimensões

```text
Centro de Trabalho

Máquina

Equipe

Funcionário

Turno

Dia

Semana

Mês
```

### Informações

```text
Capacidade Teórica

Capacidade Disponível

Capacidade Comprometida

Capacidade Realizada

Sobrecarga

Folga

Eficiência

Disponibilidade
```

### Funcionalidades

```text
Calcular Capacidade

Selecionar Período

Alterar Calendário

Simular Turno Extra

Simular Terceirização

Mover Carga

Redistribuir Operações

Exportar
```

---

# Página

## Recursos Produtivos

### ID

```text
PCP-REC-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar todos os recursos que podem ser utilizados no planejamento produtivo.

### Tipos

```text
Centro de Trabalho

Máquina

Equipamento

Ferramenta

Equipe

Funcionário

Terceirizado

Área Física
```

---

# Página

## Centros de Trabalho

### ID

```text
PCP-CTR-001
```

### Tipo

```text
Lista
```

### Objetivo

Representar setores ou agrupamentos onde operações produtivas são executadas.

### Exemplos

```text
Preparação

Corte

Usinagem

Fitagem

Pré-montagem

Montagem

Acabamento

Limpeza

Embalagem

Expedição
```

### Campos

```text
Código

Descrição

Responsável

Capacidade

Unidade de Capacidade

Calendário

Turno

Eficiência

Status
```

---

# Página

## Máquinas

### ID

```text
PCP-MAQ-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar máquinas consideradas no planejamento.

### Informações

```text
Código

Descrição

Centro de Trabalho

Capacidade

Calendário

Tempo de Setup

Eficiência

Disponibilidade

Manutenções Programadas

Status
```

---

# Página

## Equipes

### ID

```text
PCP-EQP-001
```

### Tipo

```text
Lista
```

### Objetivo

Organizar os grupos de pessoas considerados no planejamento da produção.

### Informações

```text
Equipe

Líder

Integrantes

Habilidades

Centro de Trabalho

Turno

Capacidade

Disponibilidade
```

---

# Página

## Calendários Produtivos

### ID

```text
PCP-CAL-001
```

### Tipo

```text
Calendário
```

### Objetivo

Definir dias e horários disponíveis para produção.

### Elementos

```text
Dias Úteis

Feriados

Folgas

Turnos

Horas Extras

Paradas Programadas

Manutenções

Férias

Bloqueios
```

### Funcionalidades

```text
Novo Calendário

Aplicar a Recursos

Adicionar Exceção

Adicionar Feriado

Adicionar Parada

Adicionar Hora Extra

Duplicar Calendário

Importar

Exportar
```

---

# Página

## Turnos

### ID

```text
PCP-TUR-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir períodos regulares de trabalho utilizados no cálculo de capacidade.

### Campos

```text
Nome

Hora Inicial

Hora Final

Intervalos

Horas Líquidas

Dias da Semana

Centro de Trabalho

Equipe

Status
```

---

# Página

## Roteiros de Produção

### ID

```text
PCP-ROT-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir a sequência padrão de operações necessárias para produzir um item ou projeto.

### Exemplos

```text
Corte

↓

Usinagem

↓

Fitagem

↓

Montagem

↓

Acabamento

↓

Limpeza

↓

Embalagem
```

### Funcionalidades

```text
Novo Roteiro

Editar

Duplicar

Aplicar a Produto

Aplicar a Ordem

Adicionar Operação

Reordenar Operações

Definir Dependências

Calcular Tempo

Versionar

Arquivar
```

---

# Página

## Operações

### ID

```text
PCP-OPE-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar os tipos de trabalho utilizados nos roteiros e programações.

### Exemplos

```text
Separar Material

Cortar

Usinar

Furar

Fitar

Montar

Instalar Ferragens

Conferir

Limpar

Embalar

Carregar

Terceirizar
```

### Campos

```text
Código

Descrição

Centro de Trabalho Padrão

Máquina Padrão

Tempo de Setup

Tempo Unitário

Unidade de Capacidade

Habilidade Necessária

Terceirização Permitida

Status
```

---

# Página

## Programação da Produção

### ID

```text
PCP-PRO-001
```

### Tipo

```text
Gráfico de Gantt
```

### Objetivo

Distribuir operações no tempo, considerando recursos, capacidade, materiais e dependências.

### Visualizações

```text
Gráfico de Gantt

Calendário

Timeline

Tabela

Por Centro de Trabalho

Por Máquina

Por Equipe

Por Ordem
```

### Funcionalidades

```text
Programar Automaticamente

Programar Manualmente

Mover Operação

Redimensionar Duração

Trocar Recurso

Dividir Operação

Bloquear Programação

Recalcular

Validar Conflitos

Publicar Programação

Reprogramar
```

### Restrições

```text
Disponibilidade de Material

Capacidade

Calendário

Turno

Manutenção

Dependências

Prioridade

Data Necessária

Recurso Obrigatório

Habilidade Necessária
```

---

# Página

## Sequenciamento

### ID

```text
PCP-SEQ-001
```

### Tipo

```text
Kanban
```

### Objetivo

Definir a ordem de execução das operações em cada fila produtiva.

### Critérios

```text
Prioridade

Data Necessária

Prazo do Cliente

Disponibilidade de Material

Tempo de Setup

Material

Espessura

Cor

Máquina

Dependência

Projeto

Urgência
```

### Funcionalidades

```text
Sequenciar Automaticamente

Alterar Posição

Fixar Operação

Agrupar por Material

Agrupar por Espessura

Agrupar por Setup

Aplicar Regra

Simular Sequência

Publicar Sequência

Restaurar Sequência
```

---

# Página

## Filas de Produção

### ID

```text
PCP-FIL-001
```

### Tipo

```text
Kanban
```

### Objetivo

Visualizar a fila planejada de cada centro de trabalho ou recurso.

### Etapas

```text
Não Programada

Programada

Aguardando Material

Aguardando Liberação

Pronta para Produção

Liberada

Em Execução

Pausada

Concluída
```

### Ações

```text
Alterar Prioridade

Mover na Fila

Bloquear

Liberar

Abrir Ordem

Abrir Material

Abrir Recurso

Registrar Pendência
```

---

# Página

## Carga de Trabalho

### ID

```text
PCP-CAR-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Analisar a distribuição de horas e atividades entre recursos produtivos.

### Visualizações

```text
Carga por Centro

Carga por Máquina

Carga por Equipe

Carga por Funcionário

Carga por Dia

Carga por Semana

Carga por Projeto
```

### Indicadores

```text
Horas Disponíveis

Horas Planejadas

Horas Comprometidas

Horas Realizadas

Sobrecarga

Ociosidade

Eficiência Planejada
```

---

# Página

## Gargalos

### ID

```text
PCP-GAR-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Identificar recursos ou etapas que limitam o fluxo da produção.

### Tipos de Gargalo

```text
Material

Máquina

Equipe

Funcionário

Ferramenta

Terceirizado

Espaço

Aprovação

Documento Técnico

Capacidade
```

### Funcionalidades

```text
Identificar Gargalo

Analisar Impacto

Abrir Ordens Afetadas

Simular Alternativa

Redistribuir Carga

Criar Ação

Notificar Responsável
```

---

# Página

## Prioridades

### ID

```text
PCP-PRI-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir e controlar prioridades produtivas.

### Níveis

```text
Crítica

Urgente

Alta

Normal

Baixa

Planejada
```

### Campos

```text
Ordem

Prioridade

Motivo

Solicitante

Aprovador

Data Inicial

Validade

Impacto

Status
```

### Regras

```text
Toda prioridade especial deverá possuir justificativa.

Prioridades acima da alçada deverão exigir aprovação.

Alterações deverão permanecer auditadas.
```

---

# Página

## Reprogramações

### ID

```text
PCP-REP-002
```

### Tipo

```text
Timeline
```

### Objetivo

Controlar alterações realizadas após a publicação do plano produtivo.

### Motivos

```text
Falta de Material

Atraso de Compra

Quebra de Máquina

Ausência de Funcionário

Retrabalho

Alteração de Projeto

Prioridade Comercial

Atraso de Terceiro

Problema de Qualidade

Mudança de Prazo
```

### Informações

```text
Plano Anterior

Novo Plano

Motivo

Responsável

Ordens Afetadas

Impacto no Prazo

Impacto na Capacidade

Data

Aprovação
```

---

# Página

## Simulações

### ID

```text
PCP-SIM-001
```

### Tipo

```text
Simulador
```

### Objetivo

Testar cenários produtivos sem alterar o plano oficial.

### Cenários

```text
Turno Extra

Hora Extra

Nova Máquina

Máquina Indisponível

Equipe Reduzida

Terceirização

Mudança de Prioridade

Antecipação de Pedido

Atraso de Material

Alteração de Prazo

Redistribuição de Carga
```

### Resultados

```text
Data de Conclusão

Sobrecarga

Ociosidade

Custo Estimado

Ordens Afetadas

Gargalos

Riscos
```

---

# Página

## Cronograma Geral

### ID

```text
PCP-CRO-001
```

### Tipo

```text
Gráfico de Gantt
```

### Objetivo

Apresentar todas as ordens, operações, projetos e recursos dentro de uma visão temporal única.

### Visualizações

```text
Por Projeto

Por Ordem

Por Centro de Trabalho

Por Máquina

Por Equipe

Por Cliente

Por Data de Entrega
```

---

# Página

## Acompanhamento do Plano

### ID

```text
PCP-ACP-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Comparar o planejamento publicado com a execução registrada na Produção.

### Comparações

```text
Início Planejado x Real

Término Planejado x Real

Tempo Planejado x Real

Quantidade Planejada x Real

Recurso Planejado x Utilizado

Material Previsto x Consumido

Sequência Planejada x Executada
```

### Status

```text
No Prazo

Adiantada

Em Risco

Atrasada

Bloqueada

Reprogramada
```

---

# Página

## Indicadores

### ID

```text
PCP-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Aderência ao Plano

Ordens Planejadas

Ordens Liberadas

Ordens Atrasadas

Capacidade Utilizada

Sobrecarga

Ociosidade

Tempo Médio de Planejamento

Tempo Médio de Fila

Materiais em Falta

Reprogramações

Gargalos

Cumprimento de Prazo

Precisão dos Tempos Planejados

Carga por Centro de Trabalho

Carga por Projeto
```

---

# Página

## Relatórios

### ID

```text
PCP-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Demandas de Produção

Pedidos Aguardando Planejamento

Ordens de Produção

Planejamento de Materiais

Necessidades de Materiais

Materiais em Falta

Reservas Produtivas

Capacidade por Recurso

Carga de Trabalho

Programação da Produção

Sequenciamento

Filas de Produção

Gargalos

Prioridades

Reprogramações

Cronograma Geral

Planejado x Realizado

Aderência ao Plano

Ordens em Risco

Ordens Atrasadas
```

---

# Página

## Templates

### ID

```text
PCP-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para estruturas e processos de planejamento.

### Tipos

```text
Roteiro de Produção

Calendário

Turno

Ordem de Produção

Programação

Checklist de Liberação

Regra de Sequenciamento

Relatório
```

---

# Página

## Configurações

### ID

```text
PCP-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Numeração das Ordens

Tipos de Ordem

Status

Prioridades

Centros de Trabalho

Máquinas

Equipes

Calendários

Turnos

Operações

Roteiros

Unidades de Capacidade

Eficiência Padrão

Tempos de Setup

Regras de MRP

Regras de Capacidade

Regras de Sequenciamento

Regras de Liberação

Regras de Reprogramação

Horizonte de Planejamento

Templates

Checklists

Notificações

Integrações
```

---

# Dialogs

```text
PCP-DLG-001 Nova Demanda

PCP-DLG-002 Validar Demanda

PCP-DLG-003 Nova Ordem de Produção

PCP-DLG-004 Selecionar Projeto

PCP-DLG-005 Selecionar Revisão Técnica

PCP-DLG-006 Dividir Ordem

PCP-DLG-007 Agrupar Ordens

PCP-DLG-008 Executar MRP

PCP-DLG-009 Criar Reservas

PCP-DLG-010 Criar Necessidade de Compra

PCP-DLG-011 Selecionar Roteiro

PCP-DLG-012 Adicionar Operação

PCP-DLG-013 Selecionar Centro de Trabalho

PCP-DLG-014 Selecionar Máquina

PCP-DLG-015 Selecionar Equipe

PCP-DLG-016 Configurar Capacidade

PCP-DLG-017 Programar Operação

PCP-DLG-018 Trocar Recurso

PCP-DLG-019 Dividir Operação

PCP-DLG-020 Sequenciar Operações

PCP-DLG-021 Alterar Prioridade

PCP-DLG-022 Registrar Gargalo

PCP-DLG-023 Simular Cenário

PCP-DLG-024 Solicitar Aprovação

PCP-DLG-025 Aprovar Planejamento

PCP-DLG-026 Liberar para Produção

PCP-DLG-027 Liberar Parcialmente

PCP-DLG-028 Bloquear Ordem

PCP-DLG-029 Reprogramar Ordem

PCP-DLG-030 Registrar Motivo de Reprogramação

PCP-DLG-031 Cancelar Ordem

PCP-DLG-032 Encerrar Planejamento

PCP-DLG-033 Novo Centro de Trabalho

PCP-DLG-034 Nova Máquina

PCP-DLG-035 Nova Equipe

PCP-DLG-036 Novo Calendário

PCP-DLG-037 Novo Turno

PCP-DLG-038 Novo Roteiro

PCP-DLG-039 Nova Operação

PCP-DLG-040 Exportar Plano
```

---

# Wizards

```text
PCP-WIZ-001 Assistente de Planejamento da Demanda

PCP-WIZ-002 Assistente de Ordem de Produção

PCP-WIZ-003 Assistente de MRP

PCP-WIZ-004 Assistente de Reserva de Materiais

PCP-WIZ-005 Assistente de Roteiro de Produção

PCP-WIZ-006 Assistente de Planejamento de Capacidade

PCP-WIZ-007 Assistente de Programação

PCP-WIZ-008 Assistente de Sequenciamento

PCP-WIZ-009 Assistente de Liberação para Produção

PCP-WIZ-010 Assistente de Reprogramação

PCP-WIZ-011 Assistente de Simulação

PCP-WIZ-012 Assistente de Configuração Inicial do PCP
```

---

# Componentes Específicos

```text
PCP-CPT-001 Painel de Demandas

PCP-CPT-002 Editor de Ordem de Produção

PCP-CPT-003 Explosão de Estrutura

PCP-CPT-004 Painel de MRP

PCP-CPT-005 Matriz de Disponibilidade de Materiais

PCP-CPT-006 Matriz de Capacidade

PCP-CPT-007 Mapa de Carga

PCP-CPT-008 Editor de Roteiro

PCP-CPT-009 Gráfico de Gantt Produtivo

PCP-CPT-010 Calendário de Recursos

PCP-CPT-011 Sequenciador de Operações

PCP-CPT-012 Kanban de Filas

PCP-CPT-013 Painel de Gargalos

PCP-CPT-014 Simulador de Cenários

PCP-CPT-015 Comparador Planejado x Realizado

PCP-CPT-016 Checklist de Liberação

PCP-CPT-017 Indicador de Risco de Atraso

PCP-CPT-018 Timeline de Reprogramações
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
ProductionDemandCreated

ProductionDemandValidated

ProductionDemandBlocked

ProductionOrderCreated

ProductionOrderPlanned

ProductionOrderSplit

ProductionOrderGrouped

MaterialRequirementsCalculated

ProductionMaterialShortageDetected

ProductionMaterialsReserved

ProductionCapacityCalculated

ProductionCapacityOverloadDetected

ProductionRouteAssigned

ProductionOperationScheduled

ProductionSequenceGenerated

ProductionPriorityChanged

ProductionBottleneckDetected

ProductionPlanPublished

ProductionOrderReleased

ProductionOrderPartiallyReleased

ProductionOrderBlocked

ProductionOrderRescheduled

ProductionSimulationCreated

ProductionPlanDeviationDetected

ProductionOrderPlanningCompleted

ProductionOrderCancelled
```

---

# Automações

```text
Projeto liberado para produção

↓

Criar demanda de produção

↓

Validar revisão técnica

↓

Importar estrutura

↓

Importar lista de materiais

↓

Criar pendências de planejamento
```

```text
Demanda validada

↓

Executar consulta de disponibilidade

↓

Criar reservas possíveis

↓

Identificar materiais faltantes

↓

Notificar Compras
```

```text
Materiais disponíveis

↓

Calcular capacidade

↓

Sugerir roteiro

↓

Sugerir datas

↓

Criar ordem planejada
```

```text
Sobrecarga detectada

↓

Identificar recurso crítico

↓

Sugerir redistribuição

↓

Sugerir turno extra

↓

Sugerir terceirização
```

```text
Plano publicado

↓

Liberar filas produtivas

↓

Notificar Produção

↓

Disponibilizar documentos

↓

Registrar versão do plano
```

```text
Desvio identificado

↓

Calcular impacto

↓

Marcar ordem em risco

↓

Notificar PCP

↓

Sugerir reprogramação
```

---

# Integrações

```text
CRM

Comercial

Projetos

Orçamentos

Compras

Estoque

Produção

Qualidade

Manutenção

Expedição

Instalação

Financeiro

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização
```

---

# Permissões

```text
pcp.dashboard.read

pcp.demand.read

pcp.demand.create

pcp.demand.validate

pcp.demand.block

pcp.order.read

pcp.order.create

pcp.order.update

pcp.order.split

pcp.order.group

pcp.order.cancel

pcp.material_planning.read

pcp.material_planning.execute

pcp.material_requirement.manage

pcp.material_reservation.create

pcp.material_purchase_need.create

pcp.capacity.read

pcp.capacity.calculate

pcp.capacity.override

pcp.resource.read

pcp.resource.manage

pcp.work_center.manage

pcp.machine.manage

pcp.team.manage

pcp.calendar.manage

pcp.shift.manage

pcp.route.read

pcp.route.create

pcp.route.update

pcp.operation.manage

pcp.scheduling.read

pcp.scheduling.manage

pcp.scheduling.publish

pcp.sequence.read

pcp.sequence.manage

pcp.queue.read

pcp.queue.manage

pcp.workload.read

pcp.bottleneck.read

pcp.bottleneck.manage

pcp.priority.update

pcp.priority.approve

pcp.reschedule.create

pcp.reschedule.approve

pcp.simulation.create

pcp.simulation.read

pcp.production_release.request

pcp.production_release.approve

pcp.production_release.execute

pcp.report.read

pcp.report.export

pcp.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Plano Mestre de Produção

Demanda de Produção

Ordem de Produção Planejada

Lista de Materiais da Ordem

Necessidades de Materiais

Relatório de Faltas

Ficha de Reserva

Roteiro de Produção

Lista de Operações

Programação da Produção

Sequenciamento por Centro

Carga por Recurso

Mapa de Capacidade

Cronograma Produtivo

Relatório de Gargalos

Relatório de Prioridades

Relatório de Reprogramações

Checklist de Liberação

Plano Publicado

Comparativo Planejado x Realizado

Relatório de Aderência ao Plano
```

---

# Recursos de Inteligência Artificial

```text
Sugerir agrupamento de demandas

Sugerir datas de produção

Sugerir roteiro

Estimar tempos de operação

Prever falta de materiais

Prever sobrecarga

Detectar gargalos

Sugerir redistribuição de carga

Sugerir sequenciamento

Reduzir trocas de setup

Prever atraso de ordens

Analisar impacto de prioridade

Sugerir terceirização

Simular cenários

Comparar plano com execução

Identificar padrões de reprogramação

Explicar causas de atraso

Pesquisar o plano em linguagem natural
```

A IA nunca poderá publicar planos, alterar prioridades, liberar ordens ou reprogramar operações sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Toda demanda deverá pertencer a um Tenant.

2. Toda ordem deverá possuir origem identificada.

3. Ordens vinculadas a projetos deverão utilizar uma revisão técnica válida e liberada.

4. Uma ordem não poderá ser liberada sem roteiro ou operações planejadas.

5. A liberação deverá verificar materiais, documentos e recursos obrigatórios.

6. O planejamento deverá considerar calendários, turnos, indisponibilidades e manutenções.

7. A capacidade não poderá ser considerada infinita.

8. Sobrecargas deverão ser sinalizadas antes da publicação do plano.

9. Materiais faltantes deverão bloquear ou restringir a liberação conforme política.

10. Reservas deverão ser solicitadas ao módulo Estoque.

11. Necessidades de compra deverão ser enviadas ao módulo Compras.

12. Nenhuma alteração do PCP poderá modificar a estrutura técnica do projeto.

13. Mudanças técnicas deverão retornar ao módulo Projetos.

14. Uma programação publicada deverá possuir versão.

15. Alterações posteriores deverão gerar reprogramação auditada.

16. Prioridades especiais deverão possuir justificativa.

17. Ordens poderão ser divididas ou agrupadas mantendo rastreabilidade.

18. Operações deverão respeitar dependências técnicas.

19. O sequenciamento deverá considerar restrições reais.

20. O acompanhamento deverá comparar o planejado com o realizado.

21. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O PCP será a fonte oficial do planejamento produtivo.

Projetos deverá definir o que será fabricado.

Estoque deverá informar o que está disponível.

Compras deverá informar o que será recebido.

PCP deverá decidir quando e em qual sequência produzir.

Produção deverá executar e apontar o que foi planejado, sem alterar silenciosamente o plano.

Qualquer desvio deverá retornar ao PCP para análise, reprogramação e atualização dos prazos afetados.

---

# Próxima Etapa

```text
ETAPA 03-I

Catálogo Completo de Páginas

Produção
```
---

# ETAPA 03-I

# Catálogo Completo de Páginas

# Produção

## ID do Módulo

```text
PRD
```

---

# Objetivo

O módulo Produção é responsável por executar, acompanhar e registrar todas as atividades realizadas no chão de fábrica.

Ele deverá transformar as ordens liberadas pelo PCP em móveis, componentes e produtos concluídos, respeitando:

* projeto aprovado;
* revisão técnica liberada;
* roteiro de produção;
* sequência planejada;
* materiais reservados;
* documentos técnicos;
* critérios de qualidade;
* prazos;
* responsáveis;
* recursos disponíveis.

O módulo deverá registrar o que realmente aconteceu durante a fabricação.

Nenhuma operação produtiva poderá ser concluída sem apontamento, responsável e rastreabilidade.

---

# Limites do Módulo

O módulo Produção será responsável por:

```text
Receber ordens liberadas pelo PCP

Executar operações produtivas

Registrar início, pausa e conclusão

Apontar tempos

Apontar quantidades

Registrar consumo de materiais

Controlar peças

Registrar perdas

Registrar retrabalho

Registrar não conformidades

Controlar montagem

Controlar acabamento

Controlar limpeza

Controlar embalagem

Concluir ordens
```

O módulo Produção não será responsável por:

```text
Modificar o projeto técnico

Alterar a lista de materiais oficial

Comprar materiais

Criar saldos de estoque diretamente

Alterar prioridades sem autorização

Reprogramar o plano produtivo

Emitir documentos fiscais

Registrar pagamentos
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Compras

Estoque

PCP

Fiscal

Financeiro
```

---

# Fluxo Principal

```text
Ordem Liberada pelo PCP

↓

Conferência da Documentação

↓

Conferência dos Materiais

↓

Separação dos Materiais

↓

Preparação

↓

Corte

↓

Usinagem

↓

Fitagem

↓

Pré-montagem

↓

Montagem

↓

Instalação de Ferragens

↓

Acabamento

↓

Conferência de Qualidade

↓

Limpeza

↓

Embalagem

↓

Liberação para Expedição

↓

Conclusão da Ordem
```

---

# Fases Padrão da Marcenaria

```text
Preparação

↓

Corte

↓

Usinagem

↓

Fitagem

↓

Montagem

↓

Acabamento

↓

Limpeza

↓

Embalagem

↓

Expedição
```

As fases poderão ser configuradas conforme o processo da empresa.

---

# Estrutura Geral

```text
PRD — Produção

├── Dashboard da Produção
├── Central do Chão de Fábrica
├── Ordens Liberadas
├── Ordens em Produção
├── Cadastro da Ordem
├── Fases de Produção
├── Operações
├── Filas de Trabalho
├── Postos de Trabalho
├── Painel do Operador
├── Preparação
├── Corte
├── Usinagem
├── Fitagem
├── Pré-montagem
├── Montagem
├── Instalação de Ferragens
├── Acabamento
├── Limpeza
├── Embalagem
├── Controle de Peças
├── Etiquetas
├── Apontamentos
├── Tempos de Produção
├── Consumo de Materiais
├── Perdas
├── Sobras
├── Pausas
├── Paradas
├── Retrabalhos
├── Não Conformidades
├── Pendências
├── Conferências
├── Checklists
├── Terceirizações
├── Produtos Concluídos
├── Liberações
├── Histórico
├── Timeline
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
```

---

# Página

## Dashboard da Produção

### ID

```text
PRD-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada da execução produtiva da empresa.

### Componentes

```text
Ordens Liberadas

Ordens em Produção

Ordens Atrasadas

Ordens Bloqueadas

Ordens Concluídas no Dia

Operações Pendentes

Operações em Execução

Operações Atrasadas

Peças Pendentes

Peças Produzidas

Retrabalhos

Não Conformidades

Perdas

Paradas

Carga Atual por Setor

Produtividade por Equipe

Produtividade por Operador

Planejado x Realizado

Alertas
```

### Filtros

```text
Período

Projeto

Cliente

Pedido

Ordem de Produção

Setor

Centro de Trabalho

Máquina

Equipe

Operador

Fase

Status

Prioridade

Filial
```

### Ações

```text
Abrir Central da Produção

Abrir Ordens Liberadas

Abrir Ordens em Atraso

Abrir Operações

Abrir Não Conformidades

Abrir Retrabalhos

Abrir Indicadores

Exportar Dashboard

Atualizar Dados
```

---

# Página

## Central do Chão de Fábrica

### ID

```text
PRD-CHF-001
```

### Tipo

```text
Painel
```

### Objetivo

Fornecer uma visão operacional em tempo real de tudo o que está acontecendo na fábrica.

### Visualizações

```text
Por Setor

Por Ordem

Por Projeto

Por Máquina

Por Equipe

Por Operador

Por Fase

Por Prioridade
```

### Componentes

```text
Ordens em Execução

Operações Ativas

Operadores Ativos

Máquinas em Uso

Máquinas Paradas

Filas

Pendências

Alertas

Tempos

Produção do Dia
```

### Ações

```text
Abrir Ordem

Abrir Operação

Iniciar Operação

Pausar Operação

Concluir Operação

Registrar Parada

Registrar Pendência

Registrar Não Conformidade

Solicitar Material

Chamar Responsável
```

---

# Página

## Ordens Liberadas

### ID

```text
PRD-ODL-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar as ordens autorizadas pelo PCP e disponíveis para execução.

### Colunas

```text
Número da Ordem

Projeto

Cliente

Pedido

Produto ou Móvel

Revisão Técnica

Prioridade

Data Planejada de Início

Data Planejada de Término

Materiais

Documentos

Responsável

Status
```

### Status

```text
Liberada

Liberada Parcialmente

Aguardando Material

Aguardando Documento

Aguardando Recurso

Pronta para Iniciar

Bloqueada
```

### Ações

```text
Abrir Ordem

Conferir Documentação

Conferir Materiais

Assumir Ordem

Iniciar Produção

Bloquear

Solicitar Correção

Abrir Projeto

Abrir PCP
```

---

# Página

## Ordens em Produção

### ID

```text
PRD-OEP-001
```

### Tipo

```text
Kanban
```

### Objetivo

Acompanhar o andamento das ordens dentro do chão de fábrica.

### Etapas

```text
Preparação

Corte

Usinagem

Fitagem

Pré-montagem

Montagem

Acabamento

Qualidade

Limpeza

Embalagem

Concluída
```

### Informações do Cartão

```text
Número da Ordem

Cliente

Projeto

Ambiente

Móvel

Prioridade

Responsável

Data de Entrega

Fase Atual

Percentual Concluído

Pendências

Atraso
```

### Ações

```text
Abrir Ordem

Iniciar Fase

Pausar

Continuar

Concluir Fase

Mover para Próxima Fase

Registrar Pendência

Registrar Perda

Registrar Retrabalho

Registrar Não Conformidade
```

---

# Página

## Cadastro da Ordem de Produção

### ID

```text
PRD-ODP-001
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações necessárias para executar e acompanhar uma ordem de produção.

### Abas

```text
Geral

Origem

Projeto

Ambientes

Móveis

Peças

Materiais

Ferragens

Roteiro

Operações

Programação

Apontamentos

Consumos

Perdas

Sobras

Pausas

Paradas

Retrabalhos

Não Conformidades

Qualidade

Documentos

Pendências

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Descrição

Tipo de Ordem

Projeto

Pedido

Cliente

Produto ou Móvel

Quantidade

Unidade

Revisão Técnica

Prioridade

Responsável

Equipe

Data Planejada de Início

Data Planejada de Término

Data Real de Início

Data Real de Término

Percentual Concluído

Status

Observações
```

### Aba Origem

Informações:

```text
Tipo de Origem

Pedido

Projeto

Assistência Técnica

Retrabalho

Reposição

Protótipo

Solicitante

Justificativa
```

### Aba Projeto

Informações:

```text
Projeto

Ambiente

Móvel

Revisão

Documentos Técnicos

Lista de Peças

Lista de Materiais

Plano de Corte

Liberação

Pendências
```

### Aba Ambientes

Informações:

```text
Ambiente

Descrição

Móveis

Percentual Concluído

Status

Pendências
```

### Aba Móveis

Informações:

```text
Código

Móvel

Ambiente

Quantidade

Status

Fase Atual

Percentual Concluído

Peças

Responsável
```

### Aba Peças

Informações:

```text
Código

Descrição

Móvel

Componente

Material

Dimensões

Quantidade Prevista

Quantidade Produzida

Quantidade Rejeitada

Quantidade Retrabalhada

Status

Localização
```

### Aba Materiais

Informações:

```text
Item

Quantidade Prevista

Quantidade Reservada

Quantidade Separada

Quantidade Consumida

Quantidade Devolvida

Quantidade Perdida

Diferença

Status
```

### Aba Ferragens

Informações:

```text
Ferragem

Quantidade Prevista

Quantidade Separada

Quantidade Instalada

Quantidade Devolvida

Quantidade Perdida

Status
```

### Aba Roteiro

Informações:

```text
Sequência

Fase

Operação

Centro de Trabalho

Máquina

Equipe

Tempo Previsto

Dependência

Status
```

### Aba Operações

Informações:

```text
Código

Descrição

Sequência

Quantidade

Recurso

Operador

Início Previsto

Término Previsto

Início Real

Término Real

Tempo Previsto

Tempo Real

Status
```

### Aba Programação

Informações:

```text
Operação

Data

Hora Inicial

Hora Final

Recurso Planejado

Recurso Utilizado

Responsável

Prioridade

Status
```

### Aba Apontamentos

Informações:

```text
Data

Operador

Operação

Tipo

Quantidade

Tempo

Resultado

Observação
```

### Aba Consumos

Informações:

```text
Item

Quantidade Prevista

Quantidade Consumida

Diferença

Lote

Localização

Operação

Responsável

Data
```

### Aba Perdas

Informações:

```text
Item

Peça

Quantidade

Motivo

Operação

Responsável

Data

Valor Estimado

Evidência
```

### Aba Sobras

Informações:

```text
Material

Dimensões

Quantidade

Origem

Aproveitável

Destino

Etiqueta

Localização
```

### Aba Pausas

Informações:

```text
Operação

Operador

Início

Fim

Duração

Motivo

Observação
```

### Aba Paradas

Informações:

```text
Recurso

Início

Fim

Duração

Motivo

Impacto

Responsável

Ação Tomada
```

### Aba Retrabalhos

Informações:

```text
Origem

Peça ou Móvel

Motivo

Descrição

Quantidade

Responsável

Tempo

Custo

Status
```

### Aba Não Conformidades

Informações:

```text
Código

Descrição

Tipo

Origem

Gravidade

Responsável

Ação Imediata

Ação Corretiva

Status
```

### Aba Qualidade

Informações:

```text
Checklist

Critério

Resultado

Responsável

Data

Evidência

Observação
```

---

# Página

## Fases de Produção

### ID

```text
PRD-FAS-001
```

### Tipo

```text
Lista
```

### Objetivo

Administrar as fases que estruturam o fluxo produtivo.

### Fases Padrão

```text
Preparação

Corte

Usinagem

Fitagem

Pré-montagem

Montagem

Acabamento

Qualidade

Limpeza

Embalagem
```

### Campos

```text
Código

Nome

Ordem

Centro de Trabalho

Responsável

Cor de Identificação

Operações Permitidas

Checklist Obrigatório

Exige Aprovação

Status
```

### Ações

```text
Nova Fase

Editar

Reordenar

Ativar

Inativar

Vincular Operações

Vincular Checklist
```

---

# Página

## Operações

### ID

```text
PRD-OPE-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar cada atividade executável do processo produtivo.

### Exemplos

```text
Conferir Projeto

Separar Materiais

Cortar Chapa

Identificar Peça

Usinar Peça

Furar Peça

Aplicar Fita

Montar Estrutura

Instalar Corrediça

Instalar Dobradiça

Instalar Puxador

Conferir Esquadro

Limpar

Embalar
```

### Status

```text
Não Iniciada

Pronta

Em Execução

Pausada

Bloqueada

Concluída

Concluída com Ressalva

Cancelada
```

### Ações

```text
Iniciar

Pausar

Continuar

Concluir

Bloquear

Desbloquear

Transferir

Alterar Responsável

Registrar Apontamento

Registrar Perda

Registrar Retrabalho

Registrar Não Conformidade
```

---

# Página

## Filas de Trabalho

### ID

```text
PRD-FIL-001
```

### Tipo

```text
Kanban
```

### Objetivo

Apresentar as operações disponíveis e sua ordem de execução em cada setor.

### Visualizações

```text
Por Fase

Por Centro de Trabalho

Por Máquina

Por Equipe

Por Operador
```

### Colunas

```text
Aguardando Material

Aguardando Liberação

Pronta

Em Execução

Pausada

Bloqueada

Concluída
```

### Ações

```text
Assumir Operação

Iniciar

Pausar

Concluir

Abrir Ordem

Abrir Documentos

Solicitar Material

Registrar Pendência
```

---

# Página

## Postos de Trabalho

### ID

```text
PRD-POS-001
```

### Tipo

```text
Lista
```

### Objetivo

Representar os pontos físicos onde as operações são executadas.

### Exemplos

```text
Serra Esquadrejadeira

Seccionadora

CNC

Coladeira de Borda

Bancada de Montagem 01

Bancada de Montagem 02

Área de Acabamento

Área de Limpeza

Área de Embalagem
```

### Campos

```text
Código

Nome

Centro de Trabalho

Máquina

Responsável

Capacidade

Status

Operações Permitidas

Dispositivo Vinculado
```

---

# Página

## Painel do Operador

### ID

```text
PRD-OPE-002
```

### Tipo

```text
Painel
```

### Objetivo

Fornecer ao operador apenas as informações necessárias para executar sua atividade.

### Componentes

```text
Operação Atual

Próxima Operação

Ordem

Projeto

Cliente

Peças

Materiais

Documentos

Tempo Previsto

Tempo Real

Checklist

Botões de Apontamento
```

### Ações

```text
Iniciar

Pausar

Continuar

Concluir

Registrar Quantidade

Registrar Perda

Registrar Sobra

Registrar Problema

Solicitar Ajuda

Abrir Desenho

Abrir Lista de Peças
```

### Regras

O operador deverá visualizar apenas operações:

```text
Liberadas

Compatíveis com seu posto

Compatíveis com sua permissão

Compatíveis com sua equipe
```

---

# Página

## Preparação

### ID

```text
PRD-PRE-001
```

### Tipo

```text
Kanban
```

### Objetivo

Garantir que projeto, materiais, ferragens, documentos, recursos e ferramentas estejam disponíveis antes da execução.

### Checklist

```text
Projeto Executivo Conferido

Revisão Correta

Materiais Disponíveis

Ferragens Disponíveis

Plano de Corte Disponível

Lista de Peças Disponível

Etiquetas Disponíveis

Máquinas Disponíveis

Ferramentas Disponíveis

Pendências Resolvidas
```

### Ações

```text
Conferir

Registrar Falta

Solicitar Material

Solicitar Documento

Bloquear Ordem

Liberar para Corte
```

---

# Página

## Corte

### ID

```text
PRD-COR-001
```

### Tipo

```text
Painel
```

### Objetivo

Controlar o corte das chapas e demais materiais conforme o plano de corte.

### Informações

```text
Plano de Corte

Chapa

Material

Cor

Espessura

Peças

Sequência de Corte

Veio

Aparas

Sobras

Operador

Máquina
```

### Ações

```text
Iniciar Plano

Selecionar Chapa

Ler Etiqueta

Confirmar Corte

Registrar Peça

Registrar Sobra

Registrar Perda

Registrar Erro

Concluir Chapa

Concluir Plano
```

### Validações

```text
Material correto

Cor correta

Espessura correta

Chapa correta

Quantidade correta

Dimensões corretas

Sentido do veio correto
```

---

# Página

## Usinagem

### ID

```text
PRD-USI-001
```

### Tipo

```text
Painel
```

### Objetivo

Controlar furações, rasgos, recortes, rebaixos e demais usinagens das peças.

### Operações

```text
Furação

Rasgo

Canal

Rebaixo

Recorte

Encaixe

Usinagem CNC

Furação de Ferragens
```

### Ações

```text
Selecionar Peça

Abrir Desenho

Abrir Programa CNC

Iniciar

Confirmar Operação

Registrar Medidas

Registrar Erro

Registrar Retrabalho

Concluir
```

---

# Página

## Fitagem

### ID

```text
PRD-FIT-001
```

### Tipo

```text
Painel
```

### Objetivo

Controlar a aplicação das fitas de borda nas peças.

### Informações

```text
Peça

Lado

Material da Fita

Cor

Espessura

Largura

Comprimento

Máquina

Operador
```

### Ações

```text
Selecionar Peça

Confirmar Fita

Iniciar

Registrar Aplicação

Registrar Falha

Registrar Retrabalho

Concluir
```

### Validações

```text
Fita correta

Cor correta

Espessura correta

Lado correto

Aderência

Acabamento

Excesso de cola

Ausência de lascas
```

---

# Página

## Pré-montagem

### ID

```text
PRD-PMT-001
```

### Tipo

```text
Kanban
```

### Objetivo

Realizar montagem preliminar e conferência antes da montagem definitiva ou transporte.

### Ações

```text
Separar Peças

Conferir Quantidades

Conferir Encaixes

Montar Parcialmente

Registrar Ajustes

Registrar Falta

Registrar Retrabalho

Liberar para Montagem
```

---

# Página

## Montagem

### ID

```text
PRD-MON-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar a montagem estrutural dos móveis.

### Informações

```text
Projeto

Ambiente

Móvel

Componentes

Peças

Ferragens

Responsável

Tempo Previsto

Tempo Real
```

### Ações

```text
Iniciar Montagem

Conferir Peças

Montar Estrutura

Instalar Fundos

Instalar Componentes

Registrar Falta

Registrar Ajuste

Registrar Retrabalho

Concluir Móvel
```

### Checklist

```text
Esquadro

Nivelamento

Alinhamento

Fixações

Encaixes

Medidas

Integridade

Estabilidade
```

---

# Página

## Instalação de Ferragens

### ID

```text
PRD-IFR-001
```

### Tipo

```text
Painel
```

### Objetivo

Controlar a instalação e regulagem das ferragens previstas no projeto.

### Itens

```text
Dobradiças

Corrediças

Pistões

Puxadores

Pés

Rodízios

Cabideiros

Sistemas de Porta

Acessórios
```

### Ações

```text
Selecionar Móvel

Selecionar Ferragem

Confirmar Quantidade

Instalar

Regular

Testar

Registrar Defeito

Substituir

Concluir
```

---

# Página

## Acabamento

### ID

```text
PRD-ACA-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar os acabamentos finais realizados após a montagem.

### Atividades

```text
Tamponamento

Revisão de Fitas

Correção de Bordas

Ajuste de Ferragens

Ajuste de Folgas

Instalação de Puxadores

Aplicação de Perfis

Revestimentos

Correções Finais
```

### Ações

```text
Iniciar

Registrar Atividade

Registrar Material Consumido

Registrar Ajuste

Registrar Retrabalho

Concluir
```

---

# Página

## Limpeza

### ID

```text
PRD-LIM-001
```

### Tipo

```text
Checklist
```

### Objetivo

Garantir que móveis, peças e componentes estejam limpos antes da embalagem.

### Checklist

```text
Remover Poeira

Remover Resíduos de Cola

Limpar Ferragens

Limpar Vidros

Limpar Perfis

Remover Marcações

Remover Etiquetas Temporárias

Conferir Superfícies

Conferir Interior dos Móveis
```

### Ações

```text
Iniciar Limpeza

Registrar Problema

Solicitar Correção

Concluir Limpeza

Liberar para Embalagem
```

---

# Página

## Embalagem

### ID

```text
PRD-EMB-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar proteção, identificação e preparação dos volumes para expedição.

### Informações

```text
Projeto

Cliente

Ambiente

Móvel

Volume

Conteúdo

Peso

Dimensões

Tipo de Proteção

Destino
```

### Ações

```text
Criar Volume

Adicionar Item

Embalar

Fotografar

Pesar

Medir

Gerar Etiqueta

Lacrar

Conferir

Liberar para Expedição
```

---

# Página

## Controle de Peças

### ID

```text
PRD-PEC-001
```

### Tipo

```text
Lista
```

### Objetivo

Rastrear individualmente as peças durante o fluxo produtivo.

### Status

```text
Planejada

Cortada

Usinada

Fitada

Montada

Conferida

Rejeitada

Em Retrabalho

Concluída

Embalada

Expedida
```

### Informações

```text
Código da Peça

Projeto

Ambiente

Móvel

Componente

Material

Dimensões

Quantidade

Fase Atual

Localização

Responsável

Status
```

### Ações

```text
Localizar Peça

Ler Etiqueta

Alterar Fase

Registrar Perda

Registrar Retrabalho

Reimprimir Etiqueta

Abrir Desenho

Consultar Histórico
```

---

# Página

## Etiquetas

### ID

```text
PRD-ETQ-001
```

### Tipo

```text
Configuração
```

### Objetivo

Gerar etiquetas para peças, móveis, volumes, ordens e materiais.

### Tipos

```text
Etiqueta de Peça

Etiqueta de Móvel

Etiqueta de Componente

Etiqueta de Volume

Etiqueta de Ordem

Etiqueta de Retrabalho

Etiqueta de Peça Rejeitada
```

### Conteúdo

```text
Código

Projeto

Cliente

Ambiente

Móvel

Peça

Material

Dimensões

Veio

Fitas

Operação Seguinte

QR Code

Código de Barras
```

---

# Página

## Apontamentos

### ID

```text
PRD-APT-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar todas as ações realizadas pelos operadores.

### Tipos

```text
Início

Pausa

Retomada

Conclusão

Quantidade Produzida

Quantidade Rejeitada

Consumo

Perda

Sobra

Retrabalho

Parada

Observação
```

### Informações

```text
Data

Hora

Operador

Equipe

Ordem

Operação

Recurso

Tipo

Quantidade

Tempo

Resultado

Observação
```

---

# Página

## Tempos de Produção

### ID

```text
PRD-TEM-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Comparar tempos planejados, apontados e efetivamente produtivos.

### Indicadores

```text
Tempo Planejado

Tempo Real

Tempo Produtivo

Tempo de Pausa

Tempo de Parada

Tempo de Retrabalho

Variação

Eficiência
```

### Visualizações

```text
Por Ordem

Por Fase

Por Operação

Por Máquina

Por Equipe

Por Operador

Por Projeto
```

---

# Página

## Consumo de Materiais

### ID

```text
PRD-CSM-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar o consumo real dos materiais utilizados na produção.

### Informações

```text
Item

Ordem

Projeto

Operação

Quantidade Prevista

Quantidade Consumida

Diferença

Lote

Localização

Operador

Data
```

### Ações

```text
Registrar Consumo

Ler Material

Selecionar Lote

Corrigir Apontamento

Registrar Devolução

Registrar Perda

Abrir Estoque
```

---

# Página

## Perdas

### ID

```text
PRD-PER-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar perdas ocorridas durante a produção.

### Motivos

```text
Erro de Corte

Erro de Medição

Erro de Usinagem

Erro de Fitagem

Quebra

Avaria

Defeito de Material

Erro de Projeto

Erro de Operação

Contaminação

Descarte Técnico
```

### Informações

```text
Item ou Peça

Quantidade

Material

Projeto

Ordem

Operação

Responsável

Motivo

Valor Estimado

Evidência

Destino
```

---

# Página

## Sobras

### ID

```text
PRD-SOB-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar sobras geradas durante a produção e encaminhá-las ao estoque quando aproveitáveis.

### Informações

```text
Material

Dimensões

Quantidade

Projeto

Ordem

Plano de Corte

Operação

Aproveitável

Destino

Etiqueta
```

### Ações

```text
Registrar Sobra

Informar Dimensões

Classificar

Gerar Etiqueta

Enviar ao Estoque

Descartar

Vincular a Projeto
```

---

# Página

## Pausas

### ID

```text
PRD-PAU-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar interrupções temporárias realizadas pelo operador.

### Motivos

```text
Intervalo

Troca de Ferramenta

Aguardando Material

Aguardando Informação

Aguardando Aprovação

Ajuste de Máquina

Necessidade Pessoal

Outro
```

---

# Página

## Paradas

### ID

```text
PRD-PAR-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar interrupções que afetam máquinas, setores ou ordens.

### Motivos

```text
Quebra de Máquina

Manutenção

Falta de Energia

Falta de Material

Falta de Operador

Falta de Documento

Problema de Qualidade

Bloqueio de Segurança

Aguardando Terceiro
```

### Informações

```text
Recurso

Setor

Ordem

Início

Fim

Duração

Motivo

Impacto

Responsável

Ação Corretiva
```

---

# Página

## Retrabalhos

### ID

```text
PRD-RET-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar atividades realizadas novamente para corrigir defeitos ou divergências.

### Origens

```text
Produção

Qualidade

Projeto

Montagem

Instalação

Cliente

Assistência Técnica
```

### Status

```text
Identificado

Aguardando Análise

Aguardando Material

Planejado

Em Execução

Aguardando Conferência

Concluído

Rejeitado

Cancelado
```

### Informações

```text
Origem

Peça ou Móvel

Problema

Causa

Responsável

Tempo Previsto

Tempo Real

Material Consumido

Custo Estimado

Status
```

---

# Página

## Não Conformidades

### ID

```text
PRD-NCO-001
```

### Tipo

```text
Kanban
```

### Objetivo

Registrar desvios dos padrões técnicos, produtivos ou de qualidade.

### Tipos

```text
Dimensional

Visual

Material

Ferragem

Montagem

Acabamento

Funcional

Documental

Processo

Segurança
```

### Gravidade

```text
Baixa

Moderada

Alta

Crítica
```

### Status

```text
Aberta

Em Análise

Contenção Aplicada

Aguardando Correção

Em Correção

Aguardando Verificação

Resolvida

Cancelada
```

---

# Página

## Pendências

### ID

```text
PRD-PEN-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar dúvidas, faltas, bloqueios e problemas que impedem a continuidade da produção.

### Categorias

```text
Material

Ferragem

Projeto

Documento

Máquina

Ferramenta

Pessoa

Qualidade

Terceirizado

Aprovação
```

---

# Página

## Conferências

### ID

```text
PRD-CNF-001
```

### Tipo

```text
Checklist
```

### Objetivo

Registrar conferências intermediárias e finais do processo produtivo.

### Tipos

```text
Conferência de Material

Conferência de Corte

Conferência de Usinagem

Conferência de Fitagem

Conferência de Montagem

Conferência de Ferragens

Conferência de Acabamento

Conferência Final

Conferência de Embalagem
```

---

# Página

## Checklists

### ID

```text
PRD-CHK-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar checklists obrigatórios por fase, operação ou produto.

### Funcionalidades

```text
Novo Checklist

Editar

Duplicar

Vincular Fase

Vincular Operação

Vincular Tipo de Produto

Definir Obrigatoriedade

Versionar

Arquivar
```

---

# Página

## Terceirizações

### ID

```text
PRD-TER-001
```

### Tipo

```text
Lista
```

### Objetivo

Acompanhar operações produtivas enviadas a prestadores externos.

### Exemplos

```text
Vidraçaria

Marmoraria

Serralheria

Pintura

CNC

Tapeçaria

Solda

Corte Especial
```

### Status

```text
Aguardando Envio

Enviada

Recebida pelo Terceiro

Em Execução

Aguardando Retorno

Retornada

Em Conferência

Concluída

Com Divergência
```

---

# Página

## Produtos Concluídos

### ID

```text
PRD-PCL-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar móveis, componentes e ordens concluídos e aguardando liberação.

### Status

```text
Aguardando Qualidade

Aprovado

Aprovado com Ressalva

Bloqueado

Embalado

Liberado para Expedição
```

---

# Página

## Liberações

### ID

```text
PRD-LIB-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar formalmente a passagem dos produtos concluídos para expedição ou instalação.

### Tipos

```text
Liberação para Qualidade

Liberação para Embalagem

Liberação para Expedição

Liberação para Instalação
```

### Regras

```text
Checklist obrigatório concluído

Não conformidades críticas resolvidas

Peças conferidas

Volumes identificados

Documentos disponíveis
```

---

# Página

## Histórico

### ID

```text
PRD-HIS-001
```

### Tipo

```text
Consulta
```

### Objetivo

Consultar alterações, apontamentos, movimentações e decisões ocorridas durante a produção.

---

# Página

## Timeline

### ID

```text
PRD-TML-001
```

### Tipo

```text
Timeline
```

### Objetivo

Apresentar os acontecimentos da ordem em sequência cronológica.

### Eventos

```text
Ordem Liberada

Produção Iniciada

Fase Iniciada

Operação Pausada

Material Consumido

Perda Registrada

Retrabalho Aberto

Não Conformidade Aberta

Fase Concluída

Qualidade Aprovada

Embalagem Concluída

Ordem Concluída
```

---

# Página

## Indicadores

### ID

```text
PRD-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Ordens em Produção

Ordens Concluídas

Ordens Atrasadas

Produtividade

Eficiência

Tempo Médio por Fase

Tempo Médio por Operação

Planejado x Realizado

Peças Produzidas

Peças Rejeitadas

Taxa de Retrabalho

Taxa de Perda

Taxa de Não Conformidade

Tempo de Parada

Tempo de Pausa

Consumo Previsto x Real

Produção por Operador

Produção por Equipe

Produção por Máquina

Aderência à Sequência
```

---

# Página

## Relatórios

### ID

```text
PRD-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Ordens Liberadas

Ordens em Produção

Ordens Concluídas

Ordens Atrasadas

Produção por Fase

Produção por Operação

Produção por Operador

Produção por Equipe

Produção por Máquina

Tempos de Produção

Planejado x Realizado

Consumo de Materiais

Perdas

Sobras

Pausas

Paradas

Retrabalhos

Não Conformidades

Peças Produzidas

Peças Rejeitadas

Terceirizações

Produtos Concluídos

Eficiência Produtiva

Produtividade
```

---

# Página

## Templates

### ID

```text
PRD-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para operações e documentos produtivos.

### Tipos

```text
Roteiro de Produção

Checklist de Preparação

Checklist de Fase

Checklist de Qualidade

Etiqueta de Peça

Etiqueta de Volume

Apontamento

Relatório de Produção

Motivo de Pausa

Motivo de Perda

Motivo de Retrabalho
```

---

# Página

## Configurações

### ID

```text
PRD-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Fases de Produção

Operações

Postos de Trabalho

Status

Motivos de Pausa

Motivos de Parada

Motivos de Perda

Motivos de Retrabalho

Tipos de Não Conformidade

Regras de Apontamento

Regras de Consumo

Regras de Conclusão

Regras de Liberação

Checklists

Etiquetas

Tempos Padrão

Tolerâncias

Templates

Notificações

Integrações
```

---

# Dialogs

```text
PRD-DLG-001 Iniciar Ordem

PRD-DLG-002 Assumir Ordem

PRD-DLG-003 Bloquear Ordem

PRD-DLG-004 Iniciar Operação

PRD-DLG-005 Pausar Operação

PRD-DLG-006 Retomar Operação

PRD-DLG-007 Concluir Operação

PRD-DLG-008 Registrar Quantidade

PRD-DLG-009 Registrar Apontamento

PRD-DLG-010 Registrar Consumo

PRD-DLG-011 Selecionar Material

PRD-DLG-012 Selecionar Lote

PRD-DLG-013 Registrar Perda

PRD-DLG-014 Registrar Sobra

PRD-DLG-015 Registrar Pausa

PRD-DLG-016 Registrar Parada

PRD-DLG-017 Registrar Retrabalho

PRD-DLG-018 Registrar Não Conformidade

PRD-DLG-019 Criar Pendência

PRD-DLG-020 Solicitar Material

PRD-DLG-021 Solicitar Correção de Projeto

PRD-DLG-022 Alterar Responsável

PRD-DLG-023 Transferir Operação

PRD-DLG-024 Conferir Material

PRD-DLG-025 Conferir Peça

PRD-DLG-026 Rejeitar Peça

PRD-DLG-027 Aprovar Peça

PRD-DLG-028 Criar Volume

PRD-DLG-029 Adicionar Item ao Volume

PRD-DLG-030 Gerar Etiqueta

PRD-DLG-031 Liberar para Qualidade

PRD-DLG-032 Liberar para Embalagem

PRD-DLG-033 Liberar para Expedição

PRD-DLG-034 Concluir Ordem

PRD-DLG-035 Cancelar Operação

PRD-DLG-036 Estornar Apontamento

PRD-DLG-037 Registrar Terceirização

PRD-DLG-038 Registrar Retorno do Terceiro

PRD-DLG-039 Exportar Produção

PRD-DLG-040 Imprimir Documentos
```

---

# Wizards

```text
PRD-WIZ-001 Assistente de Início da Ordem

PRD-WIZ-002 Assistente de Preparação

PRD-WIZ-003 Assistente de Corte

PRD-WIZ-004 Assistente de Apontamento

PRD-WIZ-005 Assistente de Consumo

PRD-WIZ-006 Assistente de Retrabalho

PRD-WIZ-007 Assistente de Não Conformidade

PRD-WIZ-008 Assistente de Conferência Final

PRD-WIZ-009 Assistente de Embalagem

PRD-WIZ-010 Assistente de Conclusão da Ordem

PRD-WIZ-011 Assistente de Configuração do Posto

PRD-WIZ-012 Assistente de Impressão de Etiquetas
```

---

# Componentes Específicos

```text
PRD-CPT-001 Painel do Operador

PRD-CPT-002 Kanban de Ordens

PRD-CPT-003 Kanban de Operações

PRD-CPT-004 Leitor de Peças

PRD-CPT-005 Leitor de Materiais

PRD-CPT-006 Cronômetro de Operação

PRD-CPT-007 Painel de Apontamento

PRD-CPT-008 Visualizador de Projeto

PRD-CPT-009 Visualizador de Desenho Técnico

PRD-CPT-010 Visualizador de Plano de Corte

PRD-CPT-011 Checklist de Fase

PRD-CPT-012 Editor de Consumo

PRD-CPT-013 Gerenciador de Perdas

PRD-CPT-014 Gerenciador de Sobras

PRD-CPT-015 Painel de Retrabalho

PRD-CPT-016 Painel de Não Conformidades

PRD-CPT-017 Editor de Volumes

PRD-CPT-018 Gerador de Etiquetas

PRD-CPT-019 Timeline da Ordem

PRD-CPT-020 Comparador Planejado x Real
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
ProductionOrderReceived

ProductionOrderStarted

ProductionOrderBlocked

ProductionPhaseStarted

ProductionPhaseCompleted

ProductionOperationStarted

ProductionOperationPaused

ProductionOperationResumed

ProductionOperationCompleted

ProductionQuantityReported

ProductionMaterialConsumed

ProductionMaterialReturned

ProductionLossRegistered

ProductionRemnantRegistered

ProductionDowntimeStarted

ProductionDowntimeEnded

ProductionReworkCreated

ProductionReworkStarted

ProductionReworkCompleted

ProductionNonConformityCreated

ProductionNonConformityResolved

ProductionPartProduced

ProductionPartRejected

ProductionPartApproved

ProductionFurnitureCompleted

ProductionQualityRequested

ProductionPackagingStarted

ProductionPackagingCompleted

ProductionReleasedForShipping

ProductionOrderCompleted

ProductionOrderCancelled
```

---

# Automações

```text
Ordem liberada pelo PCP

↓

Criar fluxo produtivo

↓

Criar operações

↓

Disponibilizar documentos

↓

Notificar setor inicial
```

```text
Operação iniciada

↓

Registrar operador

↓

Registrar recurso

↓

Iniciar cronômetro

↓

Atualizar status da ordem
```

```text
Material consumido

↓

Enviar movimentação ao Estoque

↓

Atualizar consumo da ordem

↓

Comparar previsto x realizado
```

```text
Perda registrada

↓

Baixar material

↓

Calcular custo

↓

Atualizar indicadores

↓

Notificar responsável quando exceder limite
```

```text
Retrabalho criado

↓

Bloquear conclusão do item

↓

Criar operação adicional

↓

Calcular impacto em prazo

↓

Notificar PCP
```

```text
Não conformidade crítica

↓

Bloquear item ou ordem

↓

Notificar Qualidade

↓

Criar ação imediata
```

```text
Ordem concluída

↓

Validar checklists

↓

Validar peças

↓

Validar consumos

↓

Liberar produtos concluídos

↓

Notificar Expedição e PCP
```

---

# Integrações

```text
Projetos

Orçamentos

Comercial

Compras

Estoque

PCP

Qualidade

Manutenção

Expedição

Instalação

Assistência Técnica

Financeiro

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Código de Barras

QR Code

Máquinas CNC
```

---

# Permissões

```text
production.dashboard.read

production.shop_floor.read

production.order.read

production.order.start

production.order.block

production.order.complete

production.order.cancel

production.phase.read

production.phase.start

production.phase.complete

production.operation.read

production.operation.start

production.operation.pause

production.operation.resume

production.operation.complete

production.operation.transfer

production.workstation.read

production.workstation.manage

production.operator_panel.use

production.preparation.execute

production.cutting.execute

production.machining.execute

production.edge_banding.execute

production.assembly.execute

production.hardware_installation.execute

production.finishing.execute

production.cleaning.execute

production.packaging.execute

production.part.read

production.part.update_status

production.part.reject

production.part.approve

production.label.generate

production.report.create

production.report.correct

production.report.reverse

production.material.consume

production.material.return

production.loss.register

production.remnant.register

production.pause.register

production.downtime.register

production.rework.create

production.rework.execute

production.rework.approve

production.non_conformity.create

production.non_conformity.resolve

production.checklist.execute

production.outsourcing.manage

production.release.quality

production.release.packaging

production.release.shipping

production.report.read

production.report.export

production.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Ficha da Ordem de Produção

Roteiro de Produção

Lista de Operações

Lista de Peças

Lista de Materiais

Plano de Corte

Etiquetas de Peças

Etiquetas de Móveis

Etiquetas de Volumes

Ficha de Apontamento

Relatório de Consumo

Relatório de Perdas

Relatório de Sobras

Relatório de Pausas

Relatório de Paradas

Relatório de Retrabalho

Relatório de Não Conformidade

Checklist de Preparação

Checklist de Corte

Checklist de Montagem

Checklist de Qualidade

Checklist de Limpeza

Checklist de Embalagem

Relatório Planejado x Realizado

Relatório de Conclusão da Ordem
```

---

# Recursos de Inteligência Artificial

```text
Resumir ordem de produção

Explicar instruções técnicas

Detectar divergências de apontamento

Detectar consumo anormal

Detectar tempo excessivo

Prever atraso

Sugerir causa de parada

Classificar perdas

Classificar não conformidades

Sugerir ação corretiva

Detectar padrão de retrabalho

Analisar produtividade

Comparar operadores e equipes

Sugerir melhorias de processo

Identificar gargalos operacionais

Resumir histórico da ordem

Pesquisar produção em linguagem natural
```

A IA nunca poderá concluir operações, aprovar peças, liberar ordens, estornar apontamentos ou alterar consumos sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Toda ordem deverá pertencer a um Tenant.

2. A Produção somente poderá executar ordens liberadas pelo PCP.

3. Toda ordem deverá utilizar uma revisão técnica válida.

4. Alterações técnicas deverão retornar ao módulo Projetos.

5. Nenhuma operação poderá ser iniciada sem operador identificado.

6. O início e o término das operações deverão ser registrados.

7. Toda pausa deverá possuir motivo quando exceder o limite configurado.

8. Toda parada deverá identificar o recurso afetado.

9. Consumos deverão estar vinculados à ordem e à operação.

10. Saldos não poderão ser alterados diretamente pela Produção.

11. Movimentações deverão ser enviadas ao módulo Estoque.

12. Perdas deverão possuir motivo, responsável e quantidade.

13. Sobras aproveitáveis deverão ser encaminhadas ao Estoque.

14. Peças rejeitadas não poderão avançar para a fase seguinte.

15. Retrabalhos deverão manter vínculo com a ocorrência original.

16. Não conformidades críticas deverão bloquear o item afetado.

17. Operações concluídas não poderão ser excluídas, apenas corrigidas ou estornadas conforme permissão.

18. Toda correção deverá permanecer auditada.

19. A conclusão de uma fase deverá validar o checklist exigido.

20. A conclusão da ordem deverá validar todas as operações obrigatórias.

21. A embalagem deverá identificar os volumes por projeto, cliente, ambiente e móvel.

22. Uma ordem concluída deverá ser liberada formalmente para Expedição.

23. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Produção será a fonte oficial da execução real do processo produtivo.

O PCP define o plano.

A Produção registra o realizado.

O Estoque controla os materiais.

Projetos controla a definição técnica.

Qualidade controla a aceitação dos resultados.

Toda diferença entre planejado e realizado deverá permanecer registrada e disponível para análise.

A Produção não poderá alterar silenciosamente:

```text
Projeto

Roteiro

Prioridade

Materiais previstos

Sequência publicada

Prazo oficial
```

Os desvios deverão gerar pendências, eventos ou solicitações para os módulos responsáveis.

---

# Próxima Etapa

```text
ETAPA 03-J

Catálogo Completo de Páginas

Qualidade
```
---

# ETAPA 03-J

# Catálogo Completo de Páginas

# Qualidade

## ID do Módulo

```text
QLD
```

---

# Objetivo

O módulo Qualidade é responsável por definir critérios, executar inspeções, registrar desvios, controlar não conformidades e garantir que materiais, peças, móveis, serviços e entregas atendam aos padrões estabelecidos pela empresa.

Ele deverá atuar desde o recebimento de materiais até a inspeção final do produto.

O módulo deverá permitir:

* inspeção de recebimento;
* inspeção durante a produção;
* inspeção de peças;
* inspeção de móveis;
* inspeção de acabamento;
* inspeção de embalagem;
* inspeção de instalação;
* controle de não conformidades;
* controle de retrabalhos;
* ações corretivas;
* ações preventivas;
* avaliação de fornecedores;
* rastreabilidade;
* análise de indicadores.

Nenhum item reprovado deverá avançar no fluxo sem correção, aprovação formal ou autorização de desvio.

---

# Limites do Módulo

O módulo Qualidade será responsável por:

```text
Definir critérios de qualidade

Criar planos de inspeção

Executar inspeções

Aprovar ou reprovar itens

Registrar não conformidades

Controlar ações corretivas

Controlar ações preventivas

Validar retrabalhos

Registrar desvios autorizados

Avaliar qualidade de fornecedores

Liberar produtos inspecionados

Analisar indicadores
```

O módulo Qualidade não será responsável por:

```text
Modificar o projeto técnico

Alterar materiais sem aprovação

Executar a produção

Comprar materiais

Movimentar estoque diretamente

Reprogramar ordens

Definir preços

Emitir documentos fiscais
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Produção

Compras

Estoque

PCP

Orçamentos

Fiscal
```

---

# Fluxo Principal

```text
Critério de Qualidade Definido

↓

Plano de Inspeção Criado

↓

Item Disponível para Inspeção

↓

Inspeção Executada

↓

Resultado Registrado

↓

Aprovado?

├── Sim
│
│   ↓
│
│   Liberar Item
│
└── Não
    ↓
    Registrar Não Conformidade
    ↓
    Aplicar Contenção
    ↓
    Definir Correção
    ↓
    Executar Retrabalho ou Substituição
    ↓
    Reinspecionar
    ↓
    Aprovar ou Rejeitar
```

---

# Estrutura Geral

```text
QLD — Qualidade

├── Dashboard da Qualidade
├── Central de Inspeções
├── Inspeções Pendentes
├── Inspeções de Recebimento
├── Inspeções de Materiais
├── Inspeções de Peças
├── Inspeções de Produção
├── Inspeções de Montagem
├── Inspeções de Acabamento
├── Inspeções Finais
├── Inspeções de Embalagem
├── Inspeções de Instalação
├── Planos de Inspeção
├── Critérios de Qualidade
├── Especificações
├── Amostragens
├── Checklists
├── Não Conformidades
├── Contenções
├── Correções
├── Ações Corretivas
├── Ações Preventivas
├── Retrabalhos
├── Desvios Autorizados
├── Disposições
├── Causas
├── Análise de Causa Raiz
├── Fornecedores
├── Qualidade de Fornecedores
├── Auditorias
├── Evidências
├── Liberações
├── Certificados
├── Histórico
├── Timeline
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
```

---

# Página

## Dashboard da Qualidade

### ID

```text
QLD-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada das inspeções, aprovações, rejeições, não conformidades, retrabalhos, fornecedores e desempenho da qualidade.

### Componentes

```text
Inspeções Pendentes

Inspeções em Andamento

Inspeções Aprovadas

Inspeções Reprovadas

Itens Bloqueados

Não Conformidades Abertas

Não Conformidades Críticas

Retrabalhos Pendentes

Ações Corretivas Vencidas

Ações Preventivas Pendentes

Desvios Autorizados

Reincidências

Índice de Aprovação

Índice de Rejeição

Custo da Não Qualidade

Qualidade por Fornecedor

Qualidade por Setor

Qualidade por Projeto

Alertas
```

### Filtros

```text
Período

Projeto

Cliente

Fornecedor

Ordem de Produção

Produto

Móvel

Peça

Material

Setor

Operação

Inspetor

Status

Gravidade

Origem

Filial
```

### Ações

```text
Nova Inspeção

Abrir Inspeções Pendentes

Abrir Não Conformidades

Abrir Retrabalhos

Abrir Ações Corretivas

Abrir Qualidade de Fornecedores

Abrir Indicadores

Exportar Dashboard

Atualizar Dados
```

---

# Página

## Central de Inspeções

### ID

```text
QLD-INS-001
```

### Tipo

```text
Painel
```

### Objetivo

Centralizar todas as inspeções disponíveis, em andamento e concluídas.

### Visualizações

```text
Por Origem

Por Tipo

Por Projeto

Por Ordem

Por Setor

Por Inspetor

Por Status

Por Prioridade
```

### Status

```text
Aguardando Inspeção

Atribuída

Em Inspeção

Aguardando Evidência

Aguardando Correção

Aguardando Reinspeção

Aprovada

Aprovada com Ressalva

Reprovada

Cancelada
```

### Ações

```text
Assumir Inspeção

Iniciar

Pausar

Retomar

Registrar Resultado

Adicionar Evidência

Criar Não Conformidade

Solicitar Correção

Aprovar

Aprovar com Ressalva

Reprovar

Encerrar
```

---

# Página

## Inspeções Pendentes

### ID

```text
QLD-PEN-001
```

### Tipo

```text
Kanban
```

### Objetivo

Exibir inspeções que ainda precisam ser executadas.

### Etapas

```text
Nova

Aguardando Inspetor

Atribuída

Em Inspeção

Aguardando Correção

Aguardando Reinspeção

Concluída
```

### Informações do Cartão

```text
Código

Tipo

Origem

Projeto

Ordem

Item

Prioridade

Data Limite

Inspetor

Status

Gravidade Potencial
```

---

# Página

## Inspeções de Recebimento

### ID

```text
QLD-REC-001
```

### Tipo

```text
Lista
```

### Objetivo

Inspecionar materiais, ferragens, componentes e serviços recebidos de fornecedores.

### Origem

```text
Pedido de Compra

Recebimento

Fornecedor

Nota Fiscal

Lote

Serviço Terceirizado
```

### Critérios

```text
Quantidade

Unidade

Marca

Modelo

Cor

Espessura

Dimensões

Integridade

Avarias

Defeitos

Acabamento

Lote

Validade

Embalagem

Documentação

Certificados
```

### Resultados

```text
Aprovado

Aprovado com Ressalva

Aprovado Parcialmente

Reprovado

Em Quarentena
```

### Ações

```text
Nova Inspeção

Selecionar Recebimento

Registrar Amostragem

Registrar Medidas

Adicionar Fotos

Aprovar Lote

Aprovar Parcialmente

Reprovar Lote

Bloquear Material

Criar Não Conformidade

Solicitar Devolução
```

---

# Página

## Inspeções de Materiais

### ID

```text
QLD-MAT-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar a conformidade dos materiais antes e durante sua utilização.

### Exemplos

```text
MDF

MDP

Compensado

Madeira

Fita de Borda

Vidro

Espelho

Perfil

Metal

Ferragem

Consumível
```

### Critérios

```text
Cor

Textura

Espessura

Dimensões

Planicidade

Empenamento

Umidade

Riscos

Lascas

Quebras

Oxidação

Validade

Conformidade Visual
```

---

# Página

## Inspeções de Peças

### ID

```text
QLD-PEC-001
```

### Tipo

```text
Lista
```

### Objetivo

Inspecionar peças produzidas antes de avançarem para as próximas fases.

### Critérios

```text
Comprimento

Largura

Espessura

Esquadro

Sentido do Veio

Fitas

Usinagens

Furações

Rasgos

Acabamento

Integridade

Identificação
```

### Status da Peça

```text
Aguardando Inspeção

Aprovada

Aprovada com Ressalva

Reprovada

Em Retrabalho

Descartada
```

### Ações

```text
Selecionar Peça

Ler Etiqueta

Registrar Dimensões

Registrar Defeito

Adicionar Evidência

Aprovar

Reprovar

Enviar para Retrabalho

Descartar

Reimprimir Etiqueta
```

---

# Página

## Inspeções de Produção

### ID

```text
QLD-PRD-001
```

### Tipo

```text
Lista
```

### Objetivo

Executar inspeções durante operações produtivas.

### Operações

```text
Corte

Usinagem

Fitagem

Pré-montagem

Montagem

Ferragens

Acabamento

Limpeza

Embalagem
```

### Tipos

```text
Inspeção Inicial

Inspeção de Processo

Inspeção por Amostragem

Inspeção de Liberação

Inspeção Extraordinária
```

---

# Página

## Inspeções de Montagem

### ID

```text
QLD-MON-001
```

### Tipo

```text
Checklist
```

### Objetivo

Verificar a montagem estrutural e funcional dos móveis.

### Critérios

```text
Esquadro

Nivelamento

Alinhamento

Fixações

Estabilidade

Encaixes

Folgas

Dimensões

Fundos

Prateleiras

Gavetas

Portas

Ferragens
```

---

# Página

## Inspeções de Acabamento

### ID

```text
QLD-ACA-001
```

### Tipo

```text
Checklist
```

### Objetivo

Verificar a qualidade visual e funcional do acabamento final.

### Critérios

```text
Fitas de Borda

Tamponamentos

Emendas

Cola Aparente

Lascas

Riscos

Manchas

Perfis

Puxadores

Alinhamentos

Folgas

Superfícies

Limpeza
```

---

# Página

## Inspeções Finais

### ID

```text
QLD-FIN-001
```

### Tipo

```text
Checklist
```

### Objetivo

Executar a inspeção final antes da embalagem, expedição ou instalação.

### Critérios

```text
Projeto Correto

Revisão Correta

Móveis Completos

Peças Completas

Ferragens Instaladas

Funcionamento

Acabamento

Limpeza

Identificação

Documentos

Pendências

Não Conformidades
```

### Resultados

```text
Liberado

Liberado com Ressalva

Bloqueado

Reprovado
```

---

# Página

## Inspeções de Embalagem

### ID

```text
QLD-EMB-001
```

### Tipo

```text
Checklist
```

### Objetivo

Verificar se os volumes estão corretamente protegidos, identificados e preparados para transporte.

### Critérios

```text
Conteúdo Correto

Proteção Adequada

Volume Identificado

Etiqueta Correta

Cliente Correto

Projeto Correto

Ambiente Correto

Móvel Correto

Peso Registrado

Dimensões Registradas

Lacre

Fotos
```

---

# Página

## Inspeções de Instalação

### ID

```text
QLD-INS-002
```

### Tipo

```text
Checklist
```

### Objetivo

Verificar o resultado da montagem e instalação no local do cliente.

### Critérios

```text
Posicionamento

Nivelamento

Alinhamento

Fixação

Funcionamento

Folgas

Acabamento

Limpeza

Danos

Ajustes

Itens Faltantes

Aceite do Cliente
```

---

# Página

## Cadastro da Inspeção

### ID

```text
QLD-INS-003
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar os dados, critérios, medições, evidências e resultados de uma inspeção.

### Abas

```text
Geral

Origem

Plano de Inspeção

Critérios

Amostragem

Medições

Resultados

Evidências

Não Conformidades

Correções

Reinspeções

Liberações

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Código

Tipo de Inspeção

Origem

Projeto

Pedido

Ordem

Item

Lote

Fornecedor

Setor

Operação

Inspetor

Prioridade

Data Planejada

Data Inicial

Data Final

Status

Resultado Geral

Observações
```

### Aba Critérios

Campos:

```text
Critério

Descrição

Tipo de Verificação

Valor Nominal

Tolerância Mínima

Tolerância Máxima

Unidade

Resultado

Conforme

Observação
```

### Aba Amostragem

Campos:

```text
Tamanho do Lote

Plano de Amostragem

Quantidade Inspecionada

Quantidade Aprovada

Quantidade Reprovada

Critério de Aceitação

Critério de Rejeição
```

### Aba Medições

Campos:

```text
Item

Ponto de Medição

Instrumento

Valor Esperado

Valor Medido

Desvio

Unidade

Resultado

Responsável
```

### Aba Resultados

Informações:

```text
Aprovado

Aprovado com Ressalva

Aprovado Parcialmente

Reprovado

Bloqueado

Em Quarentena

Requer Retrabalho

Requer Substituição
```

---

# Página

## Planos de Inspeção

### ID

```text
QLD-PLA-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir como, quando e por quais critérios cada item ou processo deverá ser inspecionado.

### Aplicações

```text
Material

Ferragem

Fornecedor

Produto

Móvel

Peça

Fase

Operação

Projeto

Recebimento

Embalagem

Instalação
```

### Campos

```text
Código

Nome

Aplicação

Tipo de Inspeção

Frequência

Amostragem

Critérios

Instrumentos

Responsável

Obrigatório

Versão

Status
```

### Funcionalidades

```text
Novo Plano

Editar

Duplicar

Versionar

Ativar

Inativar

Vincular Critérios

Vincular Checklist

Vincular Amostragem

Arquivar
```

---

# Página

## Critérios de Qualidade

### ID

```text
QLD-CRI-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar critérios reutilizáveis de aceitação e rejeição.

### Tipos

```text
Visual

Dimensional

Funcional

Documental

Quantitativo

Qualitativo

Destrutivo

Não Destrutivo
```

### Campos

```text
Código

Descrição

Tipo

Unidade

Valor Nominal

Tolerância

Método

Instrumento

Resultado Esperado

Gravidade em Caso de Falha

Status
```

---

# Página

## Especificações

### ID

```text
QLD-ESP-001
```

### Tipo

```text
Documento
```

### Objetivo

Centralizar padrões e requisitos utilizados como referência nas inspeções.

### Conteúdo

```text
Desenhos Técnicos

Memoriais

Tolerâncias

Padrões Visuais

Padrões Dimensionais

Normas Internas

Normas de Fornecedor

Instruções de Trabalho

Critérios de Aceitação
```

---

# Página

## Amostragens

### ID

```text
QLD-AMO-001
```

### Tipo

```text
Configuração
```

### Objetivo

Definir métodos de amostragem utilizados nas inspeções.

### Métodos

```text
Inspeção 100%

Amostragem Fixa

Amostragem Percentual

Amostragem por Lote

Amostragem por Risco

Amostragem Configurável
```

### Campos

```text
Nome

Tipo

Faixa de Lote

Tamanho da Amostra

Limite de Aceitação

Limite de Rejeição

Aplicação

Status
```

---

# Página

## Checklists

### ID

```text
QLD-CHK-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar checklists utilizados nas inspeções de qualidade.

### Tipos

```text
Recebimento

Material

Corte

Usinagem

Fitagem

Montagem

Acabamento

Inspeção Final

Embalagem

Instalação

Fornecedor
```

### Funcionalidades

```text
Novo Checklist

Editar

Duplicar

Versionar

Vincular Plano

Definir Obrigatoriedade

Definir Evidência Obrigatória

Arquivar
```

---

# Página

## Não Conformidades

### ID

```text
QLD-NCO-001
```

### Tipo

```text
Kanban
```

### Objetivo

Registrar, analisar e controlar desvios identificados em materiais, processos, produtos, serviços e fornecedores.

### Origens

```text
Recebimento

Estoque

Produção

Qualidade

Instalação

Cliente

Fornecedor

Auditoria

Assistência Técnica
```

### Tipos

```text
Material

Dimensional

Visual

Funcional

Montagem

Acabamento

Documental

Processo

Fornecedor

Segurança

Transporte

Instalação
```

### Gravidade

```text
Baixa

Moderada

Alta

Crítica
```

### Etapas

```text
Aberta

Em Triagem

Em Análise

Contenção Aplicada

Aguardando Disposição

Aguardando Correção

Em Correção

Aguardando Verificação

Resolvida

Encerrada

Cancelada
```

### Informações do Cartão

```text
Código

Origem

Item

Projeto

Fornecedor

Gravidade

Responsável

Prazo

Status

Reincidência
```

### Ações

```text
Nova Não Conformidade

Classificar

Definir Gravidade

Aplicar Contenção

Definir Disposição

Criar Correção

Criar Ação Corretiva

Criar Retrabalho

Solicitar Análise

Verificar

Resolver

Encerrar

Reabrir
```

---

# Página

## Cadastro da Não Conformidade

### ID

```text
QLD-NCO-002
```

### Tipo

```text
Cadastro
```

### Abas

```text
Geral

Origem

Item Afetado

Descrição

Evidências

Contenção

Disposição

Causa

Correção

Ação Corretiva

Ação Preventiva

Retrabalho

Custos

Verificação

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Código

Título

Descrição

Origem

Tipo

Gravidade

Projeto

Ordem

Item

Fornecedor

Responsável

Data de Identificação

Prazo

Status

Reincidência

Impacto
```

### Aba Item Afetado

Informações:

```text
Material

Ferragem

Peça

Móvel

Componente

Lote

Quantidade

Unidade

Localização

Fase

Operação
```

### Aba Evidências

Tipos:

```text
Foto

Vídeo

Documento

Medição

Desenho

Relatório

Áudio

Anexo
```

### Aba Custos

Informações:

```text
Material Perdido

Mão de Obra

Retrabalho

Frete

Devolução

Terceirização

Atraso

Desconto

Assistência

Custo Total
```

---

# Página

## Contenções

### ID

```text
QLD-CTN-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar ações imediatas destinadas a impedir que o problema continue ou se espalhe.

### Exemplos

```text
Bloquear Lote

Bloquear Peça

Parar Operação

Separar Material

Suspender Fornecedor

Inspecionar Estoque

Inspecionar Produção

Notificar Cliente

Substituir Item
```

### Campos

```text
Não Conformidade

Ação

Responsável

Data Inicial

Prazo

Resultado

Evidência

Status
```

---

# Página

## Correções

### ID

```text
QLD-COR-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar a correção direta do item ou problema identificado.

### Exemplos

```text
Retrabalhar

Reproduzir

Substituir

Regular

Ajustar

Limpar

Reembalar

Corrigir Documento

Devolver
```

---

# Página

## Ações Corretivas

### ID

```text
QLD-ACO-001
```

### Tipo

```text
Kanban
```

### Objetivo

Eliminar a causa de uma não conformidade para evitar reincidência.

### Etapas

```text
Proposta

Em Análise

Aprovada

Em Execução

Aguardando Verificação

Eficaz

Ineficaz

Encerrada

Cancelada
```

### Campos

```text
Origem

Causa

Ação

Responsável

Prazo

Recursos

Resultado Esperado

Critério de Eficácia

Status
```

---

# Página

## Ações Preventivas

### ID

```text
QLD-APR-001
```

### Tipo

```text
Kanban
```

### Objetivo

Eliminar causas potenciais de não conformidades antes que ocorram.

### Origens

```text
Análise de Risco

Tendência de Indicador

Auditoria

Sugestão

Falha Potencial

Fornecedor

Cliente

Produção
```

---

# Página

## Retrabalhos

### ID

```text
QLD-RET-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar retrabalhos originados pela qualidade.

### Etapas

```text
Criado

Aguardando Planejamento

Aguardando Material

Liberado

Em Execução

Aguardando Reinspeção

Aprovado

Reprovado

Concluído

Cancelado
```

### Informações

```text
Não Conformidade

Item

Descrição do Retrabalho

Responsável

Tempo Previsto

Tempo Real

Material Previsto

Material Consumido

Custo

Resultado
```

---

# Página

## Desvios Autorizados

### ID

```text
QLD-DES-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar autorizações formais para aceitar itens fora do padrão estabelecido.

### Tipos

```text
Desvio Temporário

Concessão

Uso Como Está

Aceite do Cliente

Aceite Interno

Aceite Condicional
```

### Campos

```text
Item

Não Conformidade

Desvio

Justificativa

Risco

Solicitante

Aprovador

Cliente

Validade

Quantidade

Condições

Status
```

### Regras

```text
Justificativa obrigatória

Análise de risco obrigatória

Aprovação conforme alçada

Rastreabilidade obrigatória

Validade definida

Quantidade limitada
```

---

# Página

## Disposições

### ID

```text
QLD-DSP-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir o destino formal dos itens não conformes.

### Tipos

```text
Retrabalho

Reparo

Reprodução

Substituição

Devolução

Descarte

Uso Como Está

Reclassificação

Segregação
```

---

# Página

## Causas

### ID

```text
QLD-CAU-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar e classificar causas utilizadas nas análises de qualidade.

### Categorias

```text
Projeto

Material

Máquina

Método

Mão de Obra

Medição

Meio Ambiente

Fornecedor

Transporte

Comunicação

Gestão
```

---

# Página

## Análise de Causa Raiz

### ID

```text
QLD-ACR-001
```

### Tipo

```text
Painel
```

### Objetivo

Investigar causas fundamentais de problemas recorrentes ou relevantes.

### Métodos

```text
5 Porquês

Diagrama de Ishikawa

Pareto

Árvore de Falhas

Brainstorming

Análise de Processo

Linha do Tempo
```

### Funcionalidades

```text
Criar Análise

Selecionar Método

Adicionar Causas

Classificar Causas

Vincular Evidências

Definir Causa Raiz

Criar Ação Corretiva

Gerar Relatório
```

---

# Página

## Fornecedores

### ID

```text
QLD-FOR-001
```

### Tipo

```text
Lista
```

### Objetivo

Consultar fornecedores sob a perspectiva da qualidade.

### Informações

```text
Fornecedor

Status de Homologação

Índice de Aprovação

Índice de Rejeição

Não Conformidades

Devoluções

Reincidências

Prazo de Resolução

Classificação
```

---

# Página

## Qualidade de Fornecedores

### ID

```text
QLD-QFO-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Avaliar o desempenho da qualidade dos fornecedores.

### Indicadores

```text
Lotes Recebidos

Lotes Aprovados

Lotes Reprovados

Índice de Aprovação

Índice de Devolução

Não Conformidades

Reincidências

Tempo de Resolução

Custo da Não Qualidade

Certificações

Auditorias
```

### Classificação

```text
Aprovado

Aprovado com Restrição

Em Desenvolvimento

Suspenso

Reprovado
```

---

# Página

## Auditorias

### ID

```text
QLD-AUD-001
```

### Tipo

```text
Lista
```

### Objetivo

Planejar e registrar auditorias internas, de processo e de fornecedores.

### Tipos

```text
Auditoria Interna

Auditoria de Processo

Auditoria de Produto

Auditoria de Fornecedor

Auditoria Extraordinária
```

### Status

```text
Planejada

Agendada

Em Execução

Aguardando Relatório

Aguardando Ações

Concluída

Cancelada
```

### Ações

```text
Nova Auditoria

Definir Escopo

Definir Checklist

Agendar

Executar

Registrar Evidências

Registrar Achados

Criar Não Conformidades

Gerar Relatório

Concluir
```

---

# Página

## Evidências

### ID

```text
QLD-EVI-001
```

### Tipo

```text
Gerenciador de Arquivos
```

### Objetivo

Centralizar evidências vinculadas às inspeções, auditorias e não conformidades.

### Tipos

```text
Foto

Vídeo

Documento

Medição

Laudo

Certificado

Desenho

Áudio

Assinatura
```

---

# Página

## Liberações

### ID

```text
QLD-LIB-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar formalmente itens aprovados pela Qualidade.

### Tipos

```text
Liberação de Material

Liberação de Lote

Liberação de Peça

Liberação de Móvel

Liberação de Ordem

Liberação para Embalagem

Liberação para Expedição

Liberação para Instalação
```

### Regras

```text
Inspeção concluída

Critérios obrigatórios atendidos

Não conformidades críticas encerradas

Evidências registradas

Aprovação do inspetor
```

---

# Página

## Certificados

### ID

```text
QLD-CER-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar certificados, laudos e documentos de conformidade.

### Tipos

```text
Certificado de Material

Certificado de Fornecedor

Laudo Técnico

Certificado de Inspeção

Termo de Conformidade

Termo de Liberação
```

---

# Página

## Histórico

### ID

```text
QLD-HIS-001
```

### Tipo

```text
Consulta
```

### Objetivo

Consultar todo o histórico de inspeções, decisões, correções, liberações e auditorias.

---

# Página

## Timeline

### ID

```text
QLD-TML-001
```

### Tipo

```text
Timeline
```

### Objetivo

Apresentar os acontecimentos de qualidade em ordem cronológica.

### Eventos

```text
Inspeção Criada

Inspeção Iniciada

Item Aprovado

Item Reprovado

Não Conformidade Criada

Contenção Aplicada

Correção Executada

Retrabalho Iniciado

Reinspeção Executada

Ação Corretiva Criada

Desvio Autorizado

Item Liberado

Caso Encerrado
```

---

# Página

## Indicadores

### ID

```text
QLD-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Índice de Aprovação

Índice de Rejeição

Não Conformidades Abertas

Não Conformidades por Origem

Não Conformidades por Tipo

Não Conformidades por Gravidade

Reincidência

Tempo Médio de Resolução

Tempo Médio de Inspeção

Taxa de Retrabalho

Taxa de Refugo

Custo da Não Qualidade

Qualidade por Fornecedor

Qualidade por Setor

Qualidade por Operador

Qualidade por Projeto

Ações Corretivas Vencidas

Eficácia das Ações Corretivas
```

---

# Página

## Relatórios

### ID

```text
QLD-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Inspeções Pendentes

Inspeções Realizadas

Inspeções Aprovadas

Inspeções Reprovadas

Inspeções por Projeto

Inspeções por Fornecedor

Não Conformidades

Não Conformidades Críticas

Não Conformidades Reincidentes

Retrabalhos

Ações Corretivas

Ações Preventivas

Desvios Autorizados

Auditorias

Qualidade de Fornecedores

Custo da Não Qualidade

Índice de Aprovação

Índice de Rejeição

Pareto de Defeitos

Pareto de Causas
```

---

# Página

## Templates

### ID

```text
QLD-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para inspeções, checklists e documentos da qualidade.

### Tipos

```text
Plano de Inspeção

Checklist

Não Conformidade

Ação Corretiva

Ação Preventiva

Auditoria

Certificado

Relatório

Termo de Liberação
```

---

# Página

## Configurações

### ID

```text
QLD-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Tipos de Inspeção

Status

Resultados

Critérios

Tolerâncias

Planos de Amostragem

Tipos de Não Conformidade

Gravidades

Causas

Disposições

Tipos de Contenção

Tipos de Correção

Tipos de Ação Corretiva

Tipos de Ação Preventiva

Regras de Liberação

Regras de Aprovação

Checklists

Templates

Instrumentos

Certificados

Notificações

Integrações
```

---

# Dialogs

```text
QLD-DLG-001 Nova Inspeção

QLD-DLG-002 Assumir Inspeção

QLD-DLG-003 Iniciar Inspeção

QLD-DLG-004 Registrar Critério

QLD-DLG-005 Registrar Medição

QLD-DLG-006 Adicionar Evidência

QLD-DLG-007 Aprovar Item

QLD-DLG-008 Aprovar com Ressalva

QLD-DLG-009 Aprovar Parcialmente

QLD-DLG-010 Reprovar Item

QLD-DLG-011 Bloquear Item

QLD-DLG-012 Enviar para Quarentena

QLD-DLG-013 Nova Não Conformidade

QLD-DLG-014 Classificar Não Conformidade

QLD-DLG-015 Definir Gravidade

QLD-DLG-016 Aplicar Contenção

QLD-DLG-017 Definir Disposição

QLD-DLG-018 Registrar Causa

QLD-DLG-019 Iniciar Análise de Causa Raiz

QLD-DLG-020 Criar Correção

QLD-DLG-021 Criar Ação Corretiva

QLD-DLG-022 Criar Ação Preventiva

QLD-DLG-023 Criar Retrabalho

QLD-DLG-024 Registrar Desvio Autorizado

QLD-DLG-025 Solicitar Aprovação de Desvio

QLD-DLG-026 Reinspecionar Item

QLD-DLG-027 Verificar Ação

QLD-DLG-028 Encerrar Não Conformidade

QLD-DLG-029 Reabrir Não Conformidade

QLD-DLG-030 Novo Plano de Inspeção

QLD-DLG-031 Novo Critério

QLD-DLG-032 Novo Checklist

QLD-DLG-033 Nova Auditoria

QLD-DLG-034 Registrar Achado

QLD-DLG-035 Avaliar Fornecedor

QLD-DLG-036 Liberar Material

QLD-DLG-037 Liberar Peça

QLD-DLG-038 Liberar Móvel

QLD-DLG-039 Gerar Certificado

QLD-DLG-040 Exportar Qualidade
```

---

# Wizards

```text
QLD-WIZ-001 Assistente de Inspeção

QLD-WIZ-002 Assistente de Inspeção de Recebimento

QLD-WIZ-003 Assistente de Inspeção de Peça

QLD-WIZ-004 Assistente de Inspeção Final

QLD-WIZ-005 Assistente de Não Conformidade

QLD-WIZ-006 Assistente de Análise de Causa Raiz

QLD-WIZ-007 Assistente de Ação Corretiva

QLD-WIZ-008 Assistente de Retrabalho

QLD-WIZ-009 Assistente de Desvio Autorizado

QLD-WIZ-010 Assistente de Auditoria

QLD-WIZ-011 Assistente de Avaliação de Fornecedor

QLD-WIZ-012 Assistente de Liberação
```

---

# Componentes Específicos

```text
QLD-CPT-001 Painel de Inspeções

QLD-CPT-002 Editor de Plano de Inspeção

QLD-CPT-003 Editor de Critérios

QLD-CPT-004 Tabela de Medições

QLD-CPT-005 Coletor de Evidências

QLD-CPT-006 Leitor de Peças

QLD-CPT-007 Comparador de Tolerâncias

QLD-CPT-008 Kanban de Não Conformidades

QLD-CPT-009 Editor de Contenção

QLD-CPT-010 Editor de Ação Corretiva

QLD-CPT-011 Diagrama de Ishikawa

QLD-CPT-012 Editor de 5 Porquês

QLD-CPT-013 Pareto de Defeitos

QLD-CPT-014 Painel de Retrabalhos

QLD-CPT-015 Painel de Qualidade de Fornecedores

QLD-CPT-016 Checklist de Inspeção

QLD-CPT-017 Gerador de Certificados

QLD-CPT-018 Timeline da Qualidade
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
QualityInspectionCreated

QualityInspectionAssigned

QualityInspectionStarted

QualityInspectionCompleted

QualityItemApproved

QualityItemConditionallyApproved

QualityItemRejected

QualityItemBlocked

QualityLotQuarantined

QualityNonConformityCreated

QualityNonConformityClassified

QualityContainmentApplied

QualityDispositionDefined

QualityRootCauseIdentified

QualityCorrectionCreated

QualityCorrectionCompleted

QualityCorrectiveActionCreated

QualityCorrectiveActionVerified

QualityPreventiveActionCreated

QualityReworkCreated

QualityReworkCompleted

QualityReinspectionRequested

QualityReinspectionCompleted

QualityDeviationRequested

QualityDeviationApproved

QualityDeviationRejected

QualityAuditCreated

QualityAuditCompleted

QualitySupplierEvaluated

QualityCertificateGenerated

QualityItemReleased

QualityCaseClosed
```

---

# Automações

```text
Recebimento registrado

↓

Criar inspeção de recebimento

↓

Aplicar plano de inspeção

↓

Selecionar amostragem

↓

Notificar inspetor
```

```text
Item reprovado

↓

Bloquear item

↓

Criar não conformidade

↓

Aplicar contenção

↓

Notificar origem
```

```text
Não conformidade crítica

↓

Bloquear lote, peça ou ordem

↓

Notificar responsáveis

↓

Criar tarefa urgente

↓

Registrar incidente
```

```text
Retrabalho concluído

↓

Criar reinspeção

↓

Bloquear avanço

↓

Notificar Qualidade
```

```text
Ação corretiva vencida

↓

Gerar alerta

↓

Notificar responsável

↓

Escalonar conforme regra
```

```text
Item aprovado

↓

Registrar liberação

↓

Desbloquear fluxo

↓

Notificar Produção, Estoque ou Expedição
```

```text
Fornecedor com reincidência elevada

↓

Reduzir classificação

↓

Gerar alerta

↓

Solicitar análise de homologação
```

---

# Integrações

```text
Projetos

Compras

Estoque

PCP

Produção

Expedição

Instalação

Assistência Técnica

Manutenção

CRM

Comercial

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Fornecedores
```

---

# Permissões

```text
quality.dashboard.read

quality.inspection.read

quality.inspection.create

quality.inspection.assign

quality.inspection.execute

quality.inspection.approve

quality.inspection.conditionally_approve

quality.inspection.reject

quality.inspection.cancel

quality.receiving_inspection.execute

quality.material_inspection.execute

quality.part_inspection.execute

quality.production_inspection.execute

quality.final_inspection.execute

quality.installation_inspection.execute

quality.plan.read

quality.plan.create

quality.plan.update

quality.plan.version

quality.criteria.manage

quality.sampling.manage

quality.checklist.manage

quality.non_conformity.read

quality.non_conformity.create

quality.non_conformity.classify

quality.non_conformity.update

quality.non_conformity.close

quality.non_conformity.reopen

quality.containment.manage

quality.disposition.manage

quality.correction.manage

quality.corrective_action.create

quality.corrective_action.approve

quality.corrective_action.verify

quality.preventive_action.manage

quality.rework.create

quality.rework.verify

quality.deviation.request

quality.deviation.approve

quality.deviation.reject

quality.root_cause.manage

quality.supplier.read

quality.supplier.evaluate

quality.audit.read

quality.audit.create

quality.audit.execute

quality.release.material

quality.release.part

quality.release.product

quality.release.shipping

quality.certificate.generate

quality.report.read

quality.report.export

quality.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Ficha de Inspeção

Relatório de Inspeção de Recebimento

Relatório de Inspeção de Material

Relatório de Inspeção de Peça

Relatório de Inspeção de Processo

Relatório de Inspeção Final

Relatório de Inspeção de Instalação

Relatório de Não Conformidade

Relatório de Contenção

Relatório de Causa Raiz

Plano de Ação Corretiva

Plano de Ação Preventiva

Ficha de Retrabalho

Termo de Desvio Autorizado

Relatório de Auditoria

Certificado de Inspeção

Termo de Liberação

Relatório de Qualidade do Fornecedor

Pareto de Defeitos

Pareto de Causas

Relatório de Custo da Não Qualidade
```

---

# Recursos de Inteligência Artificial

```text
Classificar defeitos por imagem

Identificar possíveis não conformidades

Comparar imagem com padrão aprovado

Detectar medidas fora da tolerância

Classificar gravidade

Sugerir causa provável

Apoiar análise de causa raiz

Sugerir ação corretiva

Detectar reincidências

Agrupar não conformidades semelhantes

Analisar qualidade de fornecedores

Prever risco de rejeição

Gerar resumo da inspeção

Gerar relatório de não conformidade

Gerar análise de Pareto

Pesquisar qualidade em linguagem natural
```

A IA nunca poderá aprovar itens, encerrar não conformidades, autorizar desvios, liberar produtos ou validar ações corretivas sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Toda inspeção deverá pertencer a um Tenant.

2. Toda inspeção deverá possuir origem identificada.

3. Inspeções obrigatórias não poderão ser ignoradas.

4. Critérios obrigatórios deverão ser respondidos antes da conclusão.

5. Medições deverão registrar valor, unidade, instrumento e responsável.

6. Itens reprovados deverão permanecer bloqueados.

7. Itens em quarentena não poderão ser utilizados ou movimentados para produção.

8. Toda não conformidade deverá possuir origem, descrição, gravidade e item afetado.

9. Não conformidades críticas deverão gerar bloqueio imediato.

10. A contenção deverá ser registrada antes da disposição quando houver risco de propagação.

11. Toda disposição deverá ser formalmente registrada.

12. Retrabalhos deverão exigir reinspeção.

13. Itens retrabalhados não poderão ser liberados sem nova aprovação.

14. Desvios autorizados deverão possuir validade, quantidade e aprovador.

15. Ações corretivas deverão possuir critério de eficácia.

16. A eficácia deverá ser verificada antes do encerramento.

17. Evidências deverão manter vínculo com a inspeção ou ocorrência.

18. Liberações deverão informar o objeto, responsável, data e critérios atendidos.

19. Alterações em planos de inspeção deverão gerar nova versão.

20. Resultados concluídos não poderão ser excluídos, apenas corrigidos ou estornados conforme permissão.

21. O histórico deverá permanecer auditável.

22. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Qualidade será a fonte oficial das decisões de conformidade.

Produção deverá informar o que foi executado.

Projetos deverá fornecer as especificações.

Compras e Estoque deverão fornecer dados de recebimento e lote.

Qualidade deverá decidir se o item:

```text
Pode avançar

Deve ser corrigido

Deve ser retrabalhado

Deve ser substituído

Deve ser devolvido

Deve ser descartado

Pode ser aceito por desvio
```

Nenhum outro módulo poderá aprovar silenciosamente um item reprovado pela Qualidade.

---

# Próxima Etapa

```text
ETAPA 03-K

Catálogo Completo de Páginas

Expedição
```
ETAPA 03-K
Catálogo Completo de Páginas
Expedição

Este módulo será responsável por tudo que acontece depois que a Produção e a Qualidade terminam, até a entrega ao cliente ou envio para instalação.

Estrutura Geral
EXP — Expedição

├── Dashboard
├── Central de Expedição
├── Produtos Liberados
├── Separação
├── Conferência
├── Volumes
├── Etiquetas
├── Embalagens
├── Carregamentos
├── Romaneios
├── Veículos
├── Motoristas
├── Transportadoras
├── Rotas
├── Entregas
├── Instalações Agendadas
├── Ocorrências
├── Devoluções
├── Assinaturas
├── Comprovantes
├── Fotos
├── Rastreamento
├── Histórico
├── Timeline
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
Dashboard
Objetivo

Mostrar toda a situação logística da empresa.

Componentes
Produtos aguardando expedição
Produtos separados
Produtos conferidos
Produtos carregados
Entregas do dia
Entregas atrasadas
Instalações do dia
Entregas concluídas
Entregas com ocorrência
Veículos disponíveis
Veículos em rota
Transportadoras
Alertas
Central de Expedição

Painel operacional.

Visualizações:

Hoje
Amanhã
Semana
Por veículo
Por motorista
Por transportadora
Por região
Por projeto
Por cliente
Produtos Liberados

Lista de tudo que já foi aprovado pela Qualidade.

Informações:

Projeto
Cliente
Pedido
Ordem
Ambiente
Móvel
Quantidade
Volume
Peso
Dimensões
Status
Separação

Lista dos itens que precisam ser separados para carregamento.

Campos:

Localização
Volume
Quantidade
Conferido
Responsável
Data
Conferência

Conferência antes do carregamento.

Checklist:

Projeto correto
Cliente correto
Volumes completos
Quantidade correta
Ferragens
Acessórios
Manual
Garantia
Nota Fiscal
Assinaturas

Resultado:

Aprovado
Aprovado com ressalva
Reprovado
Volumes

Cadastro de volumes.

Cada volume deverá possuir:

QR Code
Código de barras
Peso
Dimensões
Tipo
Conteúdo
Fotos

Status:

Em preparação
Embalado
Conferido
Carregado
Em trânsito
Entregue
Etiquetas

Etiquetas de:

Volume
Móvel
Projeto
Cliente
Ambiente
Fragilidade
Lado superior
Vidro
Espelho
Embalagens

Controle de:

Papelão
Plástico bolha
Cantoneiras
Filme stretch
Mantas
Espuma
Caixas
Madeira
Proteções especiais
Carregamentos

Cadastro dos carregamentos.

Campos:

Veículo
Motorista
Transportadora
Data
Hora
Peso
Volume
Quantidade de móveis
Rota
Romaneios

Documento contendo:

Cliente
Projeto
Volumes
Quantidades
Peso
Observações
Ordem de entrega
Veículos

Cadastro.

Campos:

Placa
Modelo
Capacidade
Peso máximo
Volume máximo
Situação
Documentação
Motoristas

Cadastro.

Campos:

Nome
CNH
Categoria
Contatos
Empresa
Situação
Transportadoras

Cadastro.

Campos:

Razão social
CNPJ
Contato
Região atendida
Avaliação
Histórico
Rotas

Planejamento.

Campos:

Região
Clientes
Distância
Tempo estimado
Veículo
Motorista
Pedágios
Custos
Entregas

Cadastro completo da entrega.

Status:

Agendada
Confirmada
Em carregamento
Em trânsito
Chegou ao cliente
Em instalação
Finalizada
Cancelada
Instalações Agendadas

Integração direta com Agenda.

Campos:

Cliente
Endereço
Equipe
Horário
Duração prevista
Materiais
Ferramentas
Ocorrências

Registro de:

Avarias
Falta de peças
Cliente ausente
Endereço incorreto
Chuva
Trânsito
Veículo quebrado
Acidente
Produto danificado
Devoluções

Controle de retorno.

Motivos:

Produto errado
Cliente recusou
Defeito
Falta de peça
Troca
Garantia
Assinaturas

Assinaturas digitais de:

Entrega
Recebimento
Instalação
Garantia
Comprovantes

Arquivos:

PDF
Fotos
Assinaturas
Termos
Checklists
Fotos

Galeria organizada por:

Projeto
Cliente
Entrega
Instalação
Ocorrência
Rastreamento

Mapa em tempo real.

Status:

Em rota
Próxima entrega
Parado
Finalizado
Histórico

Consulta completa.

Timeline

Eventos:

Produto liberado
Separação
Conferência
Embalagem
Carregamento
Saída
Entrega
Instalação
Aceite
Indicadores

KPIs:

Entregas no prazo
Entregas atrasadas
Avarias
Devoluções
Ocorrências
Tempo médio
Quilometragem
Custo por entrega
Entregas por motorista
Entregas por transportadora
Relatórios
Romaneios
Entregas
Entregas por cliente
Entregas por região
Ocorrências
Avarias
Devoluções
Veículos
Motoristas
Transportadoras
Custos Logísticos
Templates
Romaneio
Checklist
Etiqueta
Comprovante
Termo de Entrega
Termo de Garantia
Configurações
Tipos de veículos
Tipos de embalagens
Status
Ocorrências
Motivos de devolução
Transportadoras
Regiões
Integrações
Templates
Dialogs

São previstos aproximadamente 40 dialogs, incluindo:

Novo carregamento
Nova entrega
Nova ocorrência
Nova devolução
Nova transportadora
Novo veículo
Novo motorista
Gerar romaneio
Gerar etiquetas
Confirmar carregamento
Confirmar entrega
Registrar assinatura
Registrar fotos
Registrar comprovantes
Exportar expedição
Wizards
Assistente de Separação
Assistente de Conferência
Assistente de Embalagem
Assistente de Carregamento
Assistente de Entrega
Assistente de Instalação
Assistente de Devolução
Integrações
Produção
Qualidade
PCP
Estoque
Compras
Financeiro
Agenda
CRM
Instalação
Assistência Técnica
BI
IA
Workflow
Documentos
Recursos de IA

A IA poderá:

otimizar rotas;
prever atrasos;
sugerir agrupamento de entregas;
detectar riscos de atraso;
calcular melhor distribuição por veículo;
analisar ocorrências recorrentes;
prever custos logísticos;
sugerir consolidação de cargas;
gerar automaticamente romaneios;
gerar checklists de carregamento;
resumir ocorrências;
pesquisar entregas em linguagem natural.
Próxima etapa

ETAPA 03-L — Instalação, cobrindo equipes, montagem em obra, checklists de instalação, ajustes, aceite do cliente, pendências, assistência imediata e encerramento do projeto.

---

# ETAPA 03-L

# Catálogo Completo de Páginas

# Instalação

## ID do Módulo

```text
INS
```

---

# Objetivo

O módulo Instalação é responsável por planejar, executar, acompanhar e registrar todas as atividades realizadas no local do cliente para montagem, fixação, regulagem e entrega dos móveis.

Ele deverá garantir que os produtos expedidos sejam instalados conforme:

* projeto aprovado;
* revisão técnica liberada;
* ordem de instalação;
* endereço confirmado;
* condições do local;
* cronograma;
* equipe designada;
* ferramentas necessárias;
* materiais complementares;
* critérios de qualidade;
* orientações de segurança;
* requisitos de aceite.

O módulo deverá registrar o que efetivamente ocorreu durante a instalação, incluindo tempos, responsáveis, ajustes, materiais utilizados, pendências, ocorrências, fotos e aceite do cliente.

Nenhuma instalação poderá ser encerrada sem conferência, checklist e registro do resultado.

---

# Limites do Módulo

O módulo Instalação será responsável por:

```text
Planejar a instalação

Confirmar condições do local

Definir equipe e responsáveis

Conferir volumes e materiais

Controlar deslocamento

Registrar chegada ao cliente

Executar montagem e fixação

Registrar ajustes

Registrar consumo de materiais

Registrar pendências

Registrar ocorrências

Registrar danos

Executar inspeção final

Coletar assinatura do cliente

Formalizar entrega

Encerrar a instalação
```

O módulo Instalação não será responsável por:

```text
Modificar o projeto técnico

Alterar o orçamento aprovado

Reprogramar a produção diretamente

Comprar materiais diretamente

Alterar saldos de estoque diretamente

Emitir documentos fiscais

Registrar recebimentos financeiros

Aprovar garantias ou assistências futuras
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Orçamentos

PCP

Produção

Compras

Estoque

Fiscal

Financeiro

Assistência Técnica
```

---

# Fluxo Principal

```text
Produto Liberado pela Qualidade

↓

Expedição Preparada

↓

Instalação Agendada

↓

Confirmação com o Cliente

↓

Conferência do Local

↓

Definição da Equipe

↓

Separação de Ferramentas e Materiais

↓

Carregamento

↓

Deslocamento

↓

Chegada ao Cliente

↓

Check-in

↓

Conferência dos Volumes

↓

Proteção do Ambiente

↓

Montagem e Fixação

↓

Instalação de Ferragens

↓

Regulagens e Ajustes

↓

Limpeza

↓

Inspeção Final

↓

Apresentação ao Cliente

↓

Registro de Pendências

↓

Aceite e Assinatura

↓

Check-out

↓

Encerramento
```

---

# Estrutura Geral

```text
INS — Instalação

├── Dashboard de Instalações
├── Central de Instalações
├── Instalações Planejadas
├── Instalações Agendadas
├── Instalações em Andamento
├── Instalações Concluídas
├── Cadastro da Instalação
├── Agenda de Instalações
├── Equipes de Instalação
├── Instaladores
├── Ajudantes
├── Terceirizados
├── Disponibilidade das Equipes
├── Endereços de Instalação
├── Condições do Local
├── Vistorias Prévias
├── Check-in
├── Volumes
├── Móveis
├── Ambientes
├── Ferramentas
├── Equipamentos
├── Materiais de Instalação
├── EPIs
├── Veículos
├── Rotas
├── Deslocamentos
├── Montagens
├── Fixações
├── Regulagens
├── Ajustes
├── Recortes em Obra
├── Consumos
├── Sobras
├── Danos
├── Ocorrências
├── Pendências
├── Retrabalhos
├── Não Conformidades
├── Inspeções Finais
├── Checklists
├── Fotos
├── Documentos
├── Assinaturas
├── Termos de Entrega
├── Aceites
├── Check-out
├── Histórico
├── Timeline
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
```

---

# Página

## Dashboard de Instalações

### ID

```text
INS-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada das instalações planejadas, agendadas, em execução, atrasadas, concluídas e pendentes.

### Componentes

```text
Instalações do Dia

Instalações da Semana

Instalações Aguardando Agendamento

Instalações Aguardando Confirmação

Instalações em Andamento

Instalações Atrasadas

Instalações Concluídas

Instalações com Pendências

Instalações com Ocorrências

Equipes Disponíveis

Equipes em Campo

Veículos em Uso

Materiais Pendentes

Aceites Pendentes

Tempo Médio de Instalação

Índice de Conclusão na Primeira Visita

Retrabalhos

Alertas
```

### Filtros

```text
Período

Cliente

Projeto

Pedido

Instalação

Equipe

Instalador

Região

Cidade

Status

Prioridade

Tipo de Projeto

Filial
```

### Ações

```text
Nova Instalação

Abrir Agenda

Abrir Instalações do Dia

Abrir Pendências

Abrir Ocorrências

Abrir Equipes

Reagendar Instalação

Exportar Dashboard

Atualizar Indicadores
```

---

# Página

## Central de Instalações

### ID

```text
INS-CEN-001
```

### Tipo

```text
Painel
```

### Objetivo

Centralizar o acompanhamento operacional das equipes e instalações em tempo real.

### Visualizações

```text
Por Data

Por Equipe

Por Instalador

Por Região

Por Cliente

Por Projeto

Por Status

Por Prioridade
```

### Componentes

```text
Mapa das Equipes

Agenda do Dia

Instalações em Execução

Próximas Instalações

Equipes em Deslocamento

Equipes Atrasadas

Pendências Abertas

Ocorrências Ativas

Alertas

Comunicações
```

### Ações

```text
Abrir Instalação

Abrir Equipe

Alterar Equipe

Alterar Horário

Registrar Contato

Registrar Atraso

Registrar Ocorrência

Solicitar Apoio

Reagendar

Notificar Cliente
```

---

# Página

## Instalações Planejadas

### ID

```text
INS-PLA-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar projetos e pedidos que estão prontos para iniciar o planejamento da instalação.

### Colunas

```text
Projeto

Cliente

Pedido

Endereço

Volumes

Ambientes

Complexidade

Data Desejada

Data Disponível

Duração Estimada

Equipe Necessária

Materiais Pendentes

Status
```

### Status

```text
Aguardando Liberação da Produção

Aguardando Qualidade

Aguardando Expedição

Aguardando Cliente

Aguardando Planejamento

Pronta para Agendamento

Planejada

Cancelada
```

### Ações

```text
Abrir Projeto

Conferir Liberações

Estimar Duração

Definir Equipe

Definir Recursos

Definir Data

Criar Instalação

Bloquear

Cancelar
```

---

# Página

## Instalações Agendadas

### ID

```text
INS-AGE-001
```

### Tipo

```text
Lista
```

### Objetivo

Administrar todas as instalações com data e equipe definidas.

### Visualizações

```text
Tabela

Cards

Calendário

Timeline

Mapa
```

### Colunas

```text
Número

Data

Horário

Cliente

Projeto

Endereço

Equipe

Veículo

Duração Prevista

Status da Confirmação

Materiais

Volumes

Status
```

### Status

```text
Agendada

Aguardando Confirmação

Confirmada

Reagendada

Aguardando Preparação

Pronta para Execução

Cancelada
```

### Ações

```text
Abrir

Editar

Confirmar com Cliente

Alterar Data

Alterar Horário

Alterar Equipe

Alterar Veículo

Enviar Orientações

Gerar Checklist

Gerar Rota

Cancelar

Imprimir
```

---

# Página

## Instalações em Andamento

### ID

```text
INS-AND-001
```

### Tipo

```text
Kanban
```

### Objetivo

Acompanhar as instalações desde o deslocamento até o encerramento.

### Etapas

```text
Preparação

Em Deslocamento

Chegada ao Cliente

Em Conferência

Em Montagem

Em Ajustes

Em Inspeção

Aguardando Cliente

Com Pendências

Concluída
```

### Informações do Cartão

```text
Cliente

Projeto

Equipe

Endereço

Horário Previsto

Horário Real

Fase Atual

Percentual Concluído

Pendências

Ocorrências

Atraso
```

### Ações

```text
Abrir Instalação

Registrar Saída

Registrar Chegada

Iniciar

Pausar

Continuar

Registrar Pendência

Registrar Ocorrência

Solicitar Apoio

Concluir

Encerrar
```

---

# Página

## Instalações Concluídas

### ID

```text
INS-CON-001
```

### Tipo

```text
Lista
```

### Objetivo

Consultar instalações finalizadas, aceites, documentos, fotos e pendências posteriores.

### Colunas

```text
Número

Cliente

Projeto

Equipe

Data

Duração

Resultado

Pendências

Aceite

Assinatura

Garantia Iniciada

Status
```

### Resultados

```text
Concluída sem Pendências

Concluída com Ressalvas

Concluída com Pendências

Parcialmente Concluída

Não Concluída

Cancelada
```

---

# Página

## Cadastro da Instalação

### ID

```text
INS-INS-001
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações necessárias para planejar, executar e concluir uma instalação.

### Abas

```text
Geral

Cliente

Projeto

Endereço

Planejamento

Agenda

Equipe

Veículo

Ambientes

Móveis

Volumes

Ferramentas

Materiais

EPIs

Condições do Local

Vistoria Prévia

Deslocamento

Check-in

Montagem

Fixações

Ajustes

Consumos

Sobras

Danos

Ocorrências

Pendências

Retrabalhos

Qualidade

Fotos

Documentos

Assinaturas

Aceite

Check-out

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Descrição

Tipo de Instalação

Cliente

Projeto

Pedido

Revisão Técnica

Prioridade

Responsável

Equipe

Data Planejada

Hora Planejada

Duração Prevista

Data Real

Hora Inicial Real

Hora Final Real

Percentual Concluído

Resultado

Status

Observações
```

### Aba Cliente

Informações:

```text
Nome

Contato Principal

Telefone

WhatsApp

Email

Pessoa Responsável pelo Recebimento

Restrições de Horário

Observações
```

### Aba Projeto

Informações:

```text
Projeto

Revisão

Ambientes

Móveis

Documentos Técnicos

Memorial Descritivo

Plano de Instalação

Pendências

Liberações
```

### Aba Endereço

Informações:

```text
CEP

Logradouro

Número

Complemento

Bairro

Cidade

Estado

Referência

Coordenadas

Tipo de Imóvel

Andar

Elevador

Acesso de Veículo

Estacionamento

Restrições de Acesso
```

### Aba Planejamento

Informações:

```text
Complexidade

Quantidade de Ambientes

Quantidade de Móveis

Quantidade de Volumes

Duração Estimada

Quantidade de Instaladores

Quantidade de Ajudantes

Veículo Necessário

Ferramentas Especiais

Materiais Complementares

Riscos

Dependências
```

### Aba Agenda

Informações:

```text
Data

Horário

Duração

Status da Confirmação

Data da Confirmação

Confirmado por

Observações do Cliente

Reagendamentos
```

### Aba Equipe

Informações:

```text
Líder

Instaladores

Ajudantes

Terceirizados

Habilidades

Disponibilidade

Contato

Responsabilidades
```

### Aba Veículo

Informações:

```text
Veículo

Motorista

Placa

Capacidade

Data de Saída

Quilometragem Inicial

Quilometragem Final

Combustível

Pedágios
```

### Aba Ambientes

Informações:

```text
Ambiente

Descrição

Móveis

Ordem de Instalação

Status

Responsável

Pendências

Aceite
```

### Aba Móveis

Informações:

```text
Código

Móvel

Ambiente

Volumes

Status

Início

Término

Responsável

Ajustes

Pendências
```

### Aba Volumes

Informações:

```text
Código

Conteúdo

Ambiente

Móvel

Peso

Dimensões

Quantidade

Conferido

Descarregado

Avaria

Status
```

### Aba Ferramentas

Informações:

```text
Ferramenta

Quantidade

Responsável

Conferida na Saída

Conferida no Retorno

Condição

Observação
```

### Aba Materiais

Informações:

```text
Material

Quantidade Prevista

Quantidade Separada

Quantidade Consumida

Quantidade Devolvida

Quantidade Perdida

Diferença

Status
```

### Aba EPIs

Informações:

```text
EPI

Quantidade

Responsável

Obrigatório

Conferido

Condição

Observação
```

### Aba Condições do Local

Informações:

```text
Obra Liberada

Paredes Finalizadas

Piso Finalizado

Pintura Finalizada

Pontos Elétricos Prontos

Pontos Hidráulicos Prontos

Pontos de Gás Prontos

Pedras Instaladas

Eletrodomésticos Disponíveis

Acesso Livre

Ambiente Limpo

Energia Disponível

Água Disponível

Outras Equipes no Local

Restrições
```

### Aba Vistoria Prévia

Informações:

```text
Data

Responsável

Condições Encontradas

Medidas Conferidas

Fotos

Riscos

Pendências

Resultado

Liberação
```

### Aba Deslocamento

Informações:

```text
Hora de Saída

Origem

Destino

Rota

Distância

Tempo Previsto

Tempo Real

Paradas

Ocorrências

Hora de Chegada
```

### Aba Check-in

Informações:

```text
Data

Hora

Responsável no Local

Condições do Ambiente

Volumes Recebidos

Materiais Conferidos

Avarias Identificadas

Fotos Iniciais

Assinatura
```

### Aba Montagem

Informações:

```text
Ambiente

Móvel

Operação

Responsável

Início

Fim

Tempo

Resultado

Observações
```

### Aba Fixações

Informações:

```text
Móvel

Tipo de Parede

Fixador

Quantidade

Posição

Teste

Resultado

Responsável
```

### Aba Ajustes

Informações:

```text
Móvel

Descrição

Tipo

Origem

Responsável

Tempo

Material Utilizado

Resultado
```

### Aba Consumos

Informações:

```text
Item

Quantidade Prevista

Quantidade Consumida

Diferença

Origem

Responsável

Data

Observação
```

### Aba Sobras

Informações:

```text
Item

Quantidade

Condição

Aproveitável

Destino

Responsável

Retorno ao Estoque
```

### Aba Danos

Informações:

```text
Objeto Danificado

Tipo

Descrição

Responsável

Data

Fotos

Gravidade

Ação Imediata

Status
```

### Aba Ocorrências

Informações:

```text
Tipo

Descrição

Data

Responsável

Impacto

Ação Tomada

Fotos

Status
```

### Aba Pendências

Informações:

```text
Descrição

Categoria

Ambiente

Móvel

Responsável

Prioridade

Prazo

Solução Prevista

Status
```

### Aba Retrabalhos

Informações:

```text
Origem

Descrição

Responsável

Material Necessário

Tempo Estimado

Nova Visita

Status

Resultado
```

### Aba Qualidade

Informações:

```text
Checklist

Critério

Resultado

Responsável

Evidência

Não Conformidade

Liberação
```

### Aba Fotos

Categorias:

```text
Antes da Instalação

Condições do Local

Descarregamento

Montagem

Fixações

Ajustes

Danos

Pendências

Resultado Final

Pós-limpeza
```

### Aba Documentos

Informações:

```text
Projeto Executivo

Plano de Instalação

Memorial Descritivo

Romaneio

Checklist

Termo de Entrega

Termo de Garantia

Relatório de Pendências

Comprovantes
```

### Aba Assinaturas

Informações:

```text
Assinatura do Cliente

Assinatura do Instalador

Assinatura do Responsável

Data

Hora

Localização

Documento Assinado
```

### Aba Aceite

Informações:

```text
Resultado

Itens Aprovados

Ressalvas

Pendências

Prazo de Correção

Responsável pelo Aceite

Assinatura

Observações
```

### Aba Check-out

Informações:

```text
Hora de Encerramento

Limpeza Concluída

Ferramentas Conferidas

Materiais Recolhidos

Sobras Recolhidas

Pendências Registradas

Cliente Orientado

Assinaturas Coletadas

Fotos Finais

Equipe Liberada
```

---

# Página

## Agenda de Instalações

### ID

```text
INS-AGD-001
```

### Tipo

```text
Calendário
```

### Objetivo

Planejar datas, horários, equipes e recursos das instalações.

### Visualizações

```text
Dia

Semana

Mês

Linha do Tempo

Por Equipe

Por Veículo

Por Região
```

### Funcionalidades

```text
Nova Instalação

Reagendar

Alterar Equipe

Alterar Horário

Bloquear Período

Visualizar Conflitos

Confirmar Cliente

Enviar Lembrete

Exportar Agenda
```

### Regras

Não deverá existir movimentação por drag and drop.

Alterações de data, horário ou equipe deverão ocorrer por clique e edição controlada.

---

# Página

## Equipes de Instalação

### ID

```text
INS-EQP-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar e administrar equipes responsáveis pelas instalações.

### Campos

```text
Nome

Líder

Instaladores

Ajudantes

Terceirizados

Habilidades

Região

Veículo Padrão

Capacidade

Disponibilidade

Status
```

### Ações

```text
Nova Equipe

Editar

Adicionar Integrante

Remover Integrante

Definir Líder

Definir Habilidades

Consultar Agenda

Bloquear

Inativar
```

---

# Página

## Instaladores

### ID

```text
INS-IST-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar profissionais responsáveis pela instalação.

### Informações

```text
Nome

Contato

Documento

Vínculo

Equipe

Habilidades

Certificações

Ferramentas

Disponibilidade

Avaliação

Status
```

---

# Página

## Ajudantes

### ID

```text
INS-AJU-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar profissionais que auxiliam nas atividades de instalação.

---

# Página

## Terceirizados

### ID

```text
INS-TER-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar equipes ou profissionais externos contratados para instalações.

### Informações

```text
Prestador

CNPJ ou CPF

Contato

Região Atendida

Especialidades

Preço

Documentos

Avaliação

Histórico

Status
```

---

# Página

## Disponibilidade das Equipes

### ID

```text
INS-DIS-001
```

### Tipo

```text
Calendário
```

### Objetivo

Consultar a disponibilidade das equipes, instaladores, veículos e recursos.

### Informações

```text
Instalações Agendadas

Folgas

Férias

Bloqueios

Treinamentos

Manutenções de Veículo

Horas Disponíveis

Horas Comprometidas
```

---

# Página

## Endereços de Instalação

### ID

```text
INS-END-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar os locais onde ocorrerão instalações.

### Informações

```text
Cliente

Endereço

Referência

Coordenadas

Contato no Local

Horários Permitidos

Regras do Condomínio

Andar

Elevador

Estacionamento

Acesso de Carga

Restrições
```

---

# Página

## Condições do Local

### ID

```text
INS-LOC-001
```

### Tipo

```text
Checklist
```

### Objetivo

Validar se o local está pronto para receber a instalação.

### Critérios

```text
Medidas Confirmadas

Paredes Finalizadas

Piso Finalizado

Pintura Finalizada

Pedras Instaladas

Pontos Técnicos Prontos

Eletrodomésticos Disponíveis

Ambiente Livre

Energia Disponível

Acesso Permitido

Cliente Presente

Outras Equipes Concluídas
```

### Resultados

```text
Liberado

Liberado com Ressalvas

Não Liberado

Nova Vistoria Necessária
```

---

# Página

## Vistorias Prévias

### ID

```text
INS-VIS-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar visitas realizadas antes da instalação para confirmar medidas, condições e acessos.

### Ações

```text
Nova Vistoria

Agendar

Confirmar

Registrar Medidas

Adicionar Fotos

Registrar Pendências

Liberar Local

Bloquear Instalação

Gerar Relatório
```

---

# Página

## Check-in

### ID

```text
INS-CHK-001
```

### Tipo

```text
Checklist
```

### Objetivo

Registrar formalmente a chegada da equipe ao local e as condições encontradas.

### Itens

```text
Geolocalização

Data e Hora

Equipe

Responsável no Local

Condição do Ambiente

Volumes Entregues

Avarias Existentes

Proteções Necessárias

Fotos Iniciais

Assinatura
```

---

# Página

## Volumes

### ID

```text
INS-VOL-001
```

### Tipo

```text
Lista
```

### Objetivo

Conferir e rastrear os volumes destinados à instalação.

### Status

```text
Aguardando Conferência

Conferido

Descarregado

Em Montagem

Utilizado

Com Avaria

Com Item Faltante

Retornado
```

### Ações

```text
Ler Etiqueta

Confirmar Volume

Registrar Avaria

Registrar Falta

Adicionar Foto

Vincular Ambiente

Vincular Móvel

Registrar Retorno
```

---

# Página

## Móveis

### ID

```text
INS-MOV-001
```

### Tipo

```text
Kanban
```

### Objetivo

Acompanhar o status de cada móvel durante a instalação.

### Etapas

```text
Aguardando Descarregamento

Aguardando Montagem

Em Montagem

Em Fixação

Em Regulagem

Em Inspeção

Com Pendência

Concluído
```

---

# Página

## Ambientes

### ID

```text
INS-AMB-001
```

### Tipo

```text
Kanban
```

### Objetivo

Acompanhar o progresso da instalação por ambiente.

### Informações

```text
Ambiente

Móveis

Responsável

Percentual Concluído

Pendências

Resultado

Aceite
```

---

# Página

## Ferramentas

### ID

```text
INS-FER-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar ferramentas enviadas, utilizadas e devolvidas pelas equipes.

### Informações

```text
Ferramenta

Código

Responsável

Quantidade

Condição de Saída

Condição de Retorno

Perda

Dano

Observação
```

---

# Página

## Equipamentos

### ID

```text
INS-EQU-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar equipamentos necessários para instalações.

### Exemplos

```text
Furadeira

Parafusadeira

Serra

Nível a Laser

Aspirador

Escada

Extensão

Detector de Tubulação

Equipamento de Elevação
```

---

# Página

## Materiais de Instalação

### ID

```text
INS-MAT-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar consumíveis e materiais complementares utilizados na obra.

### Exemplos

```text
Parafusos

Buchas

Silicone

Cola

Fita

Cantoneiras

Suportes

Calços

Acabamentos

Produtos de Limpeza
```

---

# Página

## EPIs

### ID

```text
INS-EPI-001
```

### Tipo

```text
Checklist
```

### Objetivo

Conferir os equipamentos de proteção individual exigidos para a instalação.

### Exemplos

```text
Óculos

Luvas

Protetor Auricular

Calçado de Segurança

Capacete

Máscara

Cinto de Segurança
```

---

# Página

## Veículos

### ID

```text
INS-VEI-001
```

### Tipo

```text
Lista
```

### Objetivo

Consultar veículos disponíveis para transporte das equipes e ferramentas.

---

# Página

## Rotas

### ID

```text
INS-ROT-001
```

### Tipo

```text
Mapa
```

### Objetivo

Planejar e acompanhar os deslocamentos das equipes.

### Informações

```text
Origem

Destino

Paradas

Distância

Tempo Estimado

Pedágios

Combustível

Restrições

Rota Alternativa
```

---

# Página

## Deslocamentos

### ID

```text
INS-DES-001
```

### Tipo

```text
Timeline
```

### Objetivo

Registrar os deslocamentos realizados pelas equipes.

### Eventos

```text
Saída da Empresa

Parada

Retomada

Chegada ao Cliente

Saída do Cliente

Retorno à Empresa
```

---

# Página

## Montagens

### ID

```text
INS-MON-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar as atividades de montagem executadas no local.

### Ações

```text
Iniciar Móvel

Montar

Registrar Tempo

Registrar Ajuste

Registrar Problema

Pausar

Concluir

Solicitar Conferência
```

---

# Página

## Fixações

### ID

```text
INS-FIX-001
```

### Tipo

```text
Checklist
```

### Objetivo

Registrar e validar as fixações realizadas.

### Critérios

```text
Tipo de Parede

Fixador Correto

Quantidade de Pontos

Profundidade

Alinhamento

Resistência

Segurança

Ausência de Tubulação

Ausência de Fiação
```

---

# Página

## Regulagens

### ID

```text
INS-REG-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar regulagens executadas após a montagem.

### Exemplos

```text
Portas

Gavetas

Dobradiças

Corrediças

Pistões

Nivelamento

Folgas

Alinhamento

Sistemas Deslizantes
```

---

# Página

## Ajustes

### ID

```text
INS-AJS-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar ajustes necessários durante a instalação.

### Tipos

```text
Ajuste de Medida

Recorte

Furação

Reposicionamento

Correção de Parede

Correção de Rodapé

Ajuste de Ferragem

Ajuste de Acabamento
```

---

# Página

## Recortes em Obra

### ID

```text
INS-REC-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar recortes e modificações físicas realizadas no local.

### Regras

```text
Justificativa obrigatória

Responsável identificado

Medidas registradas

Foto antes e depois

Aprovação quando impactar o projeto

Registro do material removido
```

---

# Página

## Consumos

### ID

```text
INS-CSM-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar o consumo real de materiais utilizados na instalação.

---

# Página

## Sobras

### ID

```text
INS-SOB-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar materiais, ferragens e componentes não utilizados.

### Destinos

```text
Retorno ao Estoque

Permanência com o Cliente

Descarte

Uso em Ajuste

Assistência Técnica
```

---

# Página

## Danos

### ID

```text
INS-DAN-001
```

### Tipo

```text
Kanban
```

### Objetivo

Registrar danos ocorridos em produtos, imóvel, ferramentas ou bens de terceiros.

### Tipos

```text
Móvel

Peça

Parede

Piso

Pintura

Vidro

Pedra

Eletrodoméstico

Ferramenta

Veículo

Bem do Cliente
```

### Gravidade

```text
Baixa

Moderada

Alta

Crítica
```

---

# Página

## Ocorrências

### ID

```text
INS-OCO-001
```

### Tipo

```text
Kanban
```

### Objetivo

Registrar fatos que afetem o andamento ou resultado da instalação.

### Tipos

```text
Cliente Ausente

Local Não Liberado

Medida Divergente

Peça Faltante

Peça Danificada

Ferragem Faltante

Material Incorreto

Atraso

Chuva

Falta de Energia

Problema de Acesso

Conflito com Outra Equipe

Acidente

Problema de Segurança
```

### Status

```text
Aberta

Em Análise

Aguardando Cliente

Aguardando Projeto

Aguardando Produção

Aguardando Material

Em Resolução

Resolvida

Cancelada
```

---

# Página

## Pendências

### ID

```text
INS-PEN-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar todos os itens não concluídos durante a instalação.

### Categorias

```text
Peça

Ferragem

Ajuste

Acabamento

Projeto

Cliente

Obra

Terceiro

Documento

Limpeza
```

### Etapas

```text
Nova

Em Análise

Aguardando Responsável

Aguardando Material

Aguardando Produção

Aguardando Cliente

Visita Agendada

Em Execução

Resolvida

Cancelada
```

---

# Página

## Retrabalhos

### ID

```text
INS-RET-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar atividades que precisam ser refeitas durante ou após a instalação.

---

# Página

## Não Conformidades

### ID

```text
INS-NCO-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar desvios de qualidade identificados no local do cliente.

### Integração

Toda não conformidade deverá ser encaminhada ao módulo Qualidade.

---

# Página

## Inspeções Finais

### ID

```text
INS-INF-001
```

### Tipo

```text
Checklist
```

### Objetivo

Verificar a instalação completa antes da apresentação ao cliente.

### Critérios

```text
Posicionamento

Nivelamento

Alinhamento

Fixações

Funcionamento

Portas

Gavetas

Ferragens

Acabamento

Folgas

Limpeza

Danos

Itens Faltantes

Documentação

Orientações ao Cliente
```

### Resultados

```text
Aprovada

Aprovada com Ressalvas

Com Pendências

Reprovada
```

---

# Página

## Checklists

### ID

```text
INS-CLT-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar checklists aplicados durante o processo de instalação.

### Tipos

```text
Preparação

Veículo

Ferramentas

EPIs

Condições do Local

Check-in

Montagem

Fixação

Qualidade

Limpeza

Check-out

Entrega
```

---

# Página

## Fotos

### ID

```text
INS-FOT-001
```

### Tipo

```text
Galeria
```

### Objetivo

Centralizar todas as imagens registradas durante a instalação.

### Funcionalidades

```text
Fotografar

Upload

Classificar

Anotar

Comparar Antes e Depois

Vincular a Pendência

Vincular a Ocorrência

Exportar

Compartilhar
```

---

# Página

## Documentos

### ID

```text
INS-DOC-001
```

### Tipo

```text
Gerenciador de Arquivos
```

### Objetivo

Centralizar todos os documentos utilizados ou gerados na instalação.

---

# Página

## Assinaturas

### ID

```text
INS-ASS-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar assinaturas digitais ou manuscritas relacionadas à instalação.

### Tipos

```text
Check-in

Termo de Entrega

Aceite

Ressalvas

Pendências

Garantia

Check-out
```

---

# Página

## Termos de Entrega

### ID

```text
INS-TER-002
```

### Tipo

```text
Lista
```

### Objetivo

Gerar e armazenar termos formais de entrega e instalação.

### Conteúdo

```text
Cliente

Projeto

Data

Ambientes

Móveis

Itens Entregues

Resultado

Pendências

Ressalvas

Garantia

Orientações

Assinaturas
```

---

# Página

## Aceites

### ID

```text
INS-ACE-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar formalmente a avaliação e aprovação do cliente.

### Resultados

```text
Aceito Integralmente

Aceito com Ressalvas

Aceito Parcialmente

Não Aceito

Cliente Ausente
```

---

# Página

## Check-out

### ID

```text
INS-CKO-001
```

### Tipo

```text
Checklist
```

### Objetivo

Formalizar o encerramento da visita e a saída da equipe.

### Critérios

```text
Instalação Concluída

Limpeza Realizada

Ferramentas Conferidas

Sobras Recolhidas

Pendências Registradas

Fotos Finais

Cliente Orientado

Termo Assinado

Equipe Liberada
```

---

# Página

## Histórico

### ID

```text
INS-HIS-001
```

### Tipo

```text
Consulta
```

### Objetivo

Consultar alterações, reagendamentos, apontamentos, ocorrências e decisões relacionadas à instalação.

---

# Página

## Timeline

### ID

```text
INS-TML-001
```

### Tipo

```text
Timeline
```

### Objetivo

Apresentar os acontecimentos da instalação em ordem cronológica.

### Eventos

```text
Instalação Criada

Instalação Agendada

Cliente Confirmou

Equipe Definida

Veículo Definido

Vistoria Concluída

Equipe Saiu

Equipe Chegou

Check-in Concluído

Montagem Iniciada

Pendência Criada

Ocorrência Registrada

Inspeção Concluída

Cliente Assinou

Check-out Concluído

Instalação Encerrada
```

---

# Página

## Indicadores

### ID

```text
INS-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Instalações Planejadas

Instalações Concluídas

Instalações Atrasadas

Instalações Reagendadas

Conclusão na Primeira Visita

Tempo Médio de Instalação

Tempo Médio de Deslocamento

Produtividade por Equipe

Produtividade por Instalador

Pendências por Instalação

Ocorrências por Instalação

Retrabalhos

Danos

Custo por Instalação

Consumo de Materiais

Satisfação do Cliente

Aceites sem Ressalvas
```

---

# Página

## Relatórios

### ID

```text
INS-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Agenda de Instalações

Instalações Planejadas

Instalações Agendadas

Instalações Concluídas

Instalações Atrasadas

Instalações Reagendadas

Instalações por Equipe

Instalações por Instalador

Instalações por Região

Tempo de Instalação

Tempo de Deslocamento

Consumo de Materiais

Ferramentas Utilizadas

Pendências

Ocorrências

Danos

Retrabalhos

Aceites

Satisfação do Cliente

Conclusão na Primeira Visita
```

---

# Página

## Templates

### ID

```text
INS-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para documentos e processos da instalação.

### Tipos

```text
Checklist de Preparação

Checklist de Vistoria

Checklist de Check-in

Checklist de Instalação

Checklist de Qualidade

Checklist de Check-out

Termo de Entrega

Termo de Aceite

Relatório de Pendências

Relatório de Ocorrências

Orientações ao Cliente
```

---

# Página

## Configurações

### ID

```text
INS-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Tipos de Instalação

Status

Prioridades

Regiões

Equipes

Habilidades

Tipos de Ferramenta

Tipos de EPI

Materiais de Instalação

Tipos de Fixação

Tipos de Parede

Tipos de Ajuste

Tipos de Ocorrência

Tipos de Dano

Categorias de Pendência

Regras de Confirmação

Regras de Reagendamento

Regras de Check-in

Regras de Aceite

Regras de Encerramento

Templates

Checklists

Notificações

Integrações
```

---

# Dialogs

```text
INS-DLG-001 Nova Instalação

INS-DLG-002 Planejar Instalação

INS-DLG-003 Selecionar Projeto

INS-DLG-004 Selecionar Endereço

INS-DLG-005 Selecionar Equipe

INS-DLG-006 Selecionar Veículo

INS-DLG-007 Definir Data e Horário

INS-DLG-008 Confirmar com Cliente

INS-DLG-009 Reagendar Instalação

INS-DLG-010 Cancelar Instalação

INS-DLG-011 Nova Vistoria

INS-DLG-012 Registrar Condições do Local

INS-DLG-013 Liberar Local

INS-DLG-014 Bloquear Instalação

INS-DLG-015 Registrar Saída da Equipe

INS-DLG-016 Registrar Chegada

INS-DLG-017 Executar Check-in

INS-DLG-018 Conferir Volume

INS-DLG-019 Registrar Avaria

INS-DLG-020 Iniciar Montagem

INS-DLG-021 Pausar Instalação

INS-DLG-022 Retomar Instalação

INS-DLG-023 Registrar Ajuste

INS-DLG-024 Registrar Recorte em Obra

INS-DLG-025 Registrar Consumo

INS-DLG-026 Registrar Sobra

INS-DLG-027 Registrar Dano

INS-DLG-028 Registrar Ocorrência

INS-DLG-029 Nova Pendência

INS-DLG-030 Resolver Pendência

INS-DLG-031 Solicitar Material

INS-DLG-032 Solicitar Peça

INS-DLG-033 Registrar Retrabalho

INS-DLG-034 Registrar Não Conformidade

INS-DLG-035 Executar Inspeção Final

INS-DLG-036 Registrar Fotos

INS-DLG-037 Coletar Assinatura

INS-DLG-038 Registrar Aceite

INS-DLG-039 Executar Check-out

INS-DLG-040 Encerrar Instalação
```

---

# Wizards

```text
INS-WIZ-001 Assistente de Planejamento da Instalação

INS-WIZ-002 Assistente de Agendamento

INS-WIZ-003 Assistente de Vistoria Prévia

INS-WIZ-004 Assistente de Preparação da Equipe

INS-WIZ-005 Assistente de Check-in

INS-WIZ-006 Assistente de Instalação

INS-WIZ-007 Assistente de Registro de Pendência

INS-WIZ-008 Assistente de Inspeção Final

INS-WIZ-009 Assistente de Aceite

INS-WIZ-010 Assistente de Check-out

INS-WIZ-011 Assistente de Reagendamento

INS-WIZ-012 Assistente de Encerramento
```

---

# Componentes Específicos

```text
INS-CPT-001 Agenda de Instalações

INS-CPT-002 Mapa das Equipes

INS-CPT-003 Painel da Equipe

INS-CPT-004 Checklist de Condições do Local

INS-CPT-005 Leitor de Volumes

INS-CPT-006 Conferência de Ferramentas

INS-CPT-007 Conferência de EPIs

INS-CPT-008 Cronômetro da Instalação

INS-CPT-009 Kanban de Ambientes

INS-CPT-010 Kanban de Móveis

INS-CPT-011 Editor de Montagem

INS-CPT-012 Editor de Ajustes

INS-CPT-013 Gerenciador de Pendências

INS-CPT-014 Gerenciador de Ocorrências

INS-CPT-015 Galeria Antes e Depois

INS-CPT-016 Captura de Assinatura

INS-CPT-017 Checklist de Inspeção Final

INS-CPT-018 Gerador de Termo de Entrega

INS-CPT-019 Timeline da Instalação

INS-CPT-020 Painel de Aceite
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
InstallationCreated

InstallationPlanned

InstallationScheduled

InstallationCustomerConfirmationRequested

InstallationCustomerConfirmed

InstallationRescheduled

InstallationCancelled

InstallationTeamAssigned

InstallationVehicleAssigned

InstallationSiteInspectionCreated

InstallationSiteApproved

InstallationSiteRejected

InstallationTeamDeparted

InstallationTeamArrived

InstallationCheckInCompleted

InstallationStarted

InstallationPaused

InstallationResumed

InstallationEnvironmentStarted

InstallationFurnitureStarted

InstallationAdjustmentRegistered

InstallationMaterialConsumed

InstallationRemnantRegistered

InstallationDamageRegistered

InstallationOccurrenceCreated

InstallationPendingIssueCreated

InstallationPendingIssueResolved

InstallationReworkCreated

InstallationNonConformityCreated

InstallationFinalInspectionRequested

InstallationFinalInspectionCompleted

InstallationCustomerAcceptanceRegistered

InstallationDocumentSigned

InstallationCheckOutCompleted

InstallationCompleted
```

---

# Automações

```text
Produto liberado para instalação

↓

Criar instalação planejada

↓

Importar ambientes e móveis

↓

Importar volumes

↓

Criar checklist

↓

Notificar responsável
```

```text
Instalação agendada

↓

Reservar equipe

↓

Reservar veículo

↓

Criar evento na agenda

↓

Enviar confirmação ao cliente
```

```text
Cliente confirmou

↓

Atualizar status

↓

Enviar orientações

↓

Gerar lista de preparação

↓

Notificar equipe
```

```text
Check-in concluído

↓

Registrar localização

↓

Registrar condições iniciais

↓

Liberar início da instalação
```

```text
Pendência criada

↓

Classificar origem

↓

Notificar responsável

↓

Calcular impacto

↓

Criar tarefa de resolução
```

```text
Peça faltante ou danificada

↓

Criar solicitação de correção

↓

Notificar Projetos, Produção e PCP

↓

Bloquear conclusão do item afetado
```

```text
Instalação concluída

↓

Executar inspeção final

↓

Gerar termo de entrega

↓

Coletar assinatura

↓

Iniciar garantia

↓

Atualizar projeto

↓

Notificar CRM e Financeiro
```

---

# Integrações

```text
CRM

Comercial

Projetos

Orçamentos

Compras

Estoque

PCP

Produção

Qualidade

Expedição

Assistência Técnica

Financeiro

Fiscal

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Mapas

Geolocalização

Assinatura Digital

WhatsApp

Email
```

---

# Permissões

```text
installation.dashboard.read

installation.central.read

installation.installation.read

installation.installation.create

installation.installation.update

installation.installation.plan

installation.installation.schedule

installation.installation.confirm

installation.installation.reschedule

installation.installation.cancel

installation.team.read

installation.team.manage

installation.installer.read

installation.installer.manage

installation.third_party.manage

installation.availability.read

installation.address.read

installation.address.manage

installation.site_condition.read

installation.site_condition.evaluate

installation.site_inspection.create

installation.site_inspection.approve

installation.site_inspection.reject

installation.check_in.execute

installation.volume.read

installation.volume.check

installation.tool.manage

installation.equipment.manage

installation.material.manage

installation.ppe.check

installation.route.read

installation.route.manage

installation.displacement.register

installation.assembly.execute

installation.fixing.execute

installation.adjustment.register

installation.site_cut.register

installation.material.consume

installation.remnant.register

installation.damage.register

installation.occurrence.create

installation.occurrence.manage

installation.pending_issue.create

installation.pending_issue.resolve

installation.rework.create

installation.non_conformity.create

installation.final_inspection.execute

installation.photo.manage

installation.document.manage

installation.signature.collect

installation.acceptance.register

installation.check_out.execute

installation.installation.complete

installation.report.read

installation.report.export

installation.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Ficha da Instalação

Agenda de Instalações

Plano de Instalação

Relação de Equipe

Relação de Ferramentas

Relação de EPIs

Relação de Materiais

Relação de Volumes

Roteiro de Deslocamento

Checklist de Vistoria

Checklist de Preparação

Checklist de Check-in

Checklist de Montagem

Checklist de Fixação

Checklist de Inspeção Final

Checklist de Check-out

Relatório de Consumo

Relatório de Sobras

Relatório de Danos

Relatório de Ocorrências

Relatório de Pendências

Relatório de Retrabalho

Termo de Entrega

Termo de Aceite

Termo de Ressalvas

Termo de Garantia

Relatório Final da Instalação
```

---

# Recursos de Inteligência Artificial

```text
Estimar duração da instalação

Sugerir quantidade de instaladores

Sugerir equipe mais adequada

Otimizar agenda

Otimizar rotas

Prever atrasos

Analisar riscos do local

Detectar condições não conformes por imagem

Classificar ocorrências

Classificar danos

Sugerir solução para ajustes

Identificar pendências recorrentes

Prever necessidade de retorno

Resumir instalação

Gerar relatório final

Gerar orientações ao cliente

Analisar produtividade das equipes

Pesquisar instalações em linguagem natural
```

A IA nunca poderá alterar datas confirmadas, aprovar condições do local, encerrar pendências, coletar aceite ou concluir a instalação sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Toda instalação deverá pertencer a um Tenant.

2. Toda instalação deverá estar vinculada a um cliente, projeto e endereço.

3. A instalação deverá utilizar uma revisão técnica válida e liberada.

4. A instalação somente poderá ser agendada após liberação dos produtos necessários.

5. Toda instalação deverá possuir equipe responsável.

6. Conflitos de agenda deverão ser sinalizados antes da confirmação.

7. Datas e equipes não poderão ser alteradas por drag and drop.

8. Alterações deverão ocorrer por edição controlada e auditada.

9. O cliente deverá receber confirmação e orientações antes da instalação.

10. O local deverá ser validado conforme política da empresa.

11. Condições impeditivas deverão bloquear o início.

12. O check-in deverá registrar data, hora, equipe e condições iniciais.

13. Volumes faltantes ou avariados deverão gerar ocorrência.

14. Toda instalação deverá registrar início e término.

15. Consumos deverão ser enviados ao módulo Estoque.

16. Sobras aproveitáveis deverão retornar formalmente ao Estoque.

17. Recortes ou alterações relevantes deverão possuir justificativa e evidência.

18. Danos deverão possuir registro fotográfico quando possível.

19. Pendências deverão possuir responsável, prioridade e prazo.

20. Itens pendentes deverão impedir o aceite integral quando aplicável.

21. Não conformidades deverão ser encaminhadas ao módulo Qualidade.

22. A inspeção final deverá ser executada antes do aceite.

23. O aceite deverá registrar resultado, responsável e assinatura.

24. A instalação não poderá ser encerrada sem check-out.

25. A conclusão deverá iniciar o período de garantia quando aplicável.

26. Registros concluídos não poderão ser excluídos, apenas corrigidos ou estornados conforme permissão.

27. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Instalação será a fonte oficial da execução realizada no local do cliente.

Expedição deverá informar o que foi enviado.

Projetos deverá informar o que deverá ser instalado.

Qualidade deverá definir os critérios de aceitação.

Estoque deverá controlar os materiais e ferramentas movimentados.

Assistência Técnica deverá receber as pendências que permanecerem após o encerramento.

A instalação não poderá modificar silenciosamente:

```text
Projeto

Escopo contratado

Materiais especificados

Revisão liberada

Prazo comercial

Condições financeiras
```

Qualquer divergência deverá gerar ocorrência, pendência, não conformidade ou solicitação formal ao módulo responsável.

---

# Próxima Etapa

```text
ETAPA 03-M

Catálogo Completo de Páginas

Assistência Técnica
```
---

# ETAPA 03-M

# Catálogo Completo de Páginas

# Assistência Técnica

## ID do Módulo

```text
AST
```

---

# Objetivo

O módulo Assistência Técnica é responsável por registrar, analisar, planejar, executar e acompanhar atendimentos realizados após a entrega ou instalação.

Ele deverá controlar atendimentos relacionados a:

* garantia;
* manutenção;
* ajustes;
* correções;
* peças faltantes;
* peças danificadas;
* falhas de montagem;
* falhas de instalação;
* defeitos de materiais;
* defeitos de ferragens;
* problemas de funcionamento;
* solicitações fora de garantia;
* visitas preventivas;
* orientações ao cliente.

O módulo deverá preservar a rastreabilidade entre o chamado, o projeto original, os itens afetados, a causa identificada, a responsabilidade, os custos, as peças utilizadas e a solução aplicada.

Nenhum atendimento deverá ser encerrado sem registro da solução, responsável, resultado e aceite quando aplicável.

---

# Limites do Módulo

O módulo Assistência Técnica será responsável por:

```text
Receber solicitações de atendimento

Classificar chamados

Verificar cobertura de garantia

Realizar triagem

Definir prioridade

Planejar visitas

Designar responsáveis

Registrar diagnósticos

Solicitar peças de reposição

Solicitar materiais

Controlar manutenções

Registrar serviços executados

Registrar custos

Determinar responsabilidades

Controlar prazos

Registrar aceite do cliente

Medir satisfação

Encerrar atendimentos
```

O módulo Assistência Técnica não será responsável por:

```text
Modificar silenciosamente o projeto original

Alterar o contrato aprovado

Produzir peças diretamente

Comprar materiais diretamente

Movimentar estoque diretamente

Emitir cobrança sem integração financeira

Emitir documentos fiscais diretamente

Alterar regras de garantia retroativamente
```

Essas responsabilidades pertencem aos módulos:

```text
Projetos

Comercial

Produção

Compras

Estoque

Financeiro

Fiscal

Configurações
```

---

# Fluxo Principal

```text
Solicitação do Cliente

↓

Abertura do Chamado

↓

Identificação do Cliente e Projeto

↓

Classificação

↓

Verificação da Garantia

↓

Triagem

↓

Diagnóstico Inicial

↓

Atendimento Remoto Possível?

├── Sim
│
│   ↓
│
│   Orientação ao Cliente
│
│   ↓
│
│   Confirmação da Solução
│
└── Não
    ↓
    Planejamento da Visita
    ↓
    Definição da Equipe
    ↓
    Verificação de Peças e Materiais
    ↓
    Visita Técnica
    ↓
    Diagnóstico Presencial
    ↓
    Execução do Serviço
    ↓
    Inspeção
    ↓
    Aceite do Cliente
    ↓
    Encerramento
```

Fluxo com necessidade de produção:

```text
Diagnóstico

↓

Peça Necessária

↓

Verificar Estoque

↓

Peça Disponível?

├── Sim
│
│   ↓
│
│   Reservar Peça
│
└── Não
    ↓
    Criar Solicitação de Reposição
    ↓
    Projetos
    ↓
    PCP
    ↓
    Produção
    ↓
    Qualidade
    ↓
    Estoque
    ↓
    Agendar Retorno
```

---

# Estrutura Geral

```text
AST — Assistência Técnica

├── Dashboard da Assistência
├── Central de Atendimento
├── Chamados
├── Cadastro do Chamado
├── Solicitações Recebidas
├── Triagens
├── Diagnósticos
├── Garantias
├── Coberturas
├── Prazos de Garantia
├── Itens em Garantia
├── Atendimentos Remotos
├── Visitas Técnicas
├── Agenda da Assistência
├── Equipes Técnicas
├── Técnicos
├── Terceirizados
├── Ordens de Serviço
├── Serviços
├── Manutenções
├── Ajustes
├── Correções
├── Peças de Reposição
├── Materiais
├── Ferramentas
├── Reservas
├── Solicitações ao Estoque
├── Solicitações à Produção
├── Solicitações de Compra
├── Retrabalhos
├── Não Conformidades
├── Causas
├── Responsabilidades
├── Custos
├── Cobranças
├── Aprovações
├── Prazos
├── SLA
├── Prioridades
├── Pendências
├── Ocorrências
├── Fotos
├── Documentos
├── Assinaturas
├── Aceites
├── Satisfação do Cliente
├── Histórico
├── Timeline
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
```

---

# Página

## Dashboard da Assistência

### ID

```text
AST-DAS-001
```

### Tipo

```text
Dashboard
```

### Objetivo

Apresentar uma visão consolidada dos chamados, garantias, visitas, pendências, custos e desempenho da assistência técnica.

### Componentes

```text
Chamados Abertos

Chamados Novos

Chamados Urgentes

Chamados em Garantia

Chamados Fora de Garantia

Chamados Aguardando Triagem

Chamados Aguardando Visita

Chamados Aguardando Peça

Chamados Aguardando Cliente

Chamados Atrasados

Visitas do Dia

Visitas da Semana

Ordens de Serviço em Aberto

Retrabalhos Pendentes

Não Conformidades

Tempo Médio de Atendimento

Tempo Médio de Solução

Índice de Solução na Primeira Visita

Custo da Assistência

Satisfação do Cliente

Alertas
```

### Filtros

```text
Período

Cliente

Projeto

Chamado

Técnico

Equipe

Tipo

Origem

Garantia

Prioridade

Status

Responsabilidade

Cidade

Filial
```

### Ações

```text
Novo Chamado

Abrir Central de Atendimento

Abrir Chamados Urgentes

Abrir Visitas do Dia

Abrir Pendências

Abrir Garantias

Abrir Indicadores

Exportar Dashboard

Atualizar Dados
```

---

# Página

## Central de Atendimento

### ID

```text
AST-CEN-001
```

### Tipo

```text
Painel
```

### Objetivo

Centralizar a operação diária da assistência técnica.

### Visualizações

```text
Por Status

Por Prioridade

Por Técnico

Por Equipe

Por Região

Por Garantia

Por Responsabilidade

Por Prazo

Por Cliente
```

### Componentes

```text
Fila de Novos Chamados

Atendimentos em Andamento

Visitas Agendadas

Técnicos em Campo

Chamados Atrasados

Chamados Bloqueados

Peças Pendentes

Clientes Aguardando Retorno

Alertas de SLA

Comunicações Recentes
```

### Ações

```text
Abrir Chamado

Assumir Chamado

Transferir Chamado

Registrar Contato

Criar Triagem

Agendar Visita

Solicitar Peça

Alterar Prioridade

Escalonar

Encerrar
```

---

# Página

## Chamados

### ID

```text
AST-CHA-001
```

### Tipo

```text
Lista
```

### Objetivo

Listar, pesquisar, filtrar e administrar todos os chamados de assistência técnica.

### Visualizações

```text
Tabela

Cards

Kanban

Timeline

Calendário

Mapa
```

### Colunas

```text
Número

Cliente

Projeto

Item Afetado

Tipo

Origem

Garantia

Prioridade

Responsável

Data de Abertura

Prazo

Status

Dias em Aberto

Próxima Ação
```

### Status

```text
Novo

Aguardando Triagem

Em Triagem

Aguardando Informações

Aguardando Cliente

Aguardando Diagnóstico

Atendimento Remoto

Aguardando Visita

Visita Agendada

Em Atendimento

Aguardando Peça

Aguardando Material

Aguardando Produção

Aguardando Terceiro

Aguardando Aprovação

Aguardando Retorno

Resolvido

Encerrado

Cancelado
```

### Prioridades

```text
Baixa

Normal

Alta

Urgente

Crítica
```

### Tipos

```text
Garantia

Manutenção

Ajuste

Correção

Peça Faltante

Peça Danificada

Defeito de Material

Defeito de Ferragem

Problema de Montagem

Problema de Instalação

Problema de Funcionamento

Orientação

Visita Preventiva

Atendimento Fora de Garantia
```

### Ações

```text
Novo Chamado

Abrir

Editar

Duplicar

Assumir

Transferir

Classificar

Alterar Prioridade

Verificar Garantia

Criar Triagem

Registrar Diagnóstico

Responder Cliente

Agendar Visita

Criar Ordem de Serviço

Solicitar Peça

Solicitar Material

Solicitar Produção

Solicitar Compra

Registrar Solução

Resolver

Encerrar

Reabrir

Cancelar

Exportar

Imprimir
```

---

# Página

## Cadastro do Chamado

### ID

```text
AST-CHA-002
```

### Tipo

```text
Cadastro
```

### Objetivo

Centralizar todas as informações necessárias para compreender, executar e encerrar um atendimento.

### Abas

```text
Geral

Cliente

Projeto

Pedido

Contrato

Garantia

Item Afetado

Solicitação

Triagem

Diagnóstico

Atendimentos

Visitas

Ordem de Serviço

Peças

Materiais

Serviços

Custos

Responsabilidades

Prazos

SLA

Pendências

Ocorrências

Não Conformidades

Retrabalhos

Fotos

Documentos

Comunicações

Assinaturas

Aceite

Satisfação

Histórico

Timeline

Auditoria
```

### Aba Geral

Campos:

```text
Número

Título

Descrição Resumida

Tipo

Categoria

Origem

Canal de Abertura

Cliente

Projeto

Pedido

Contrato

Prioridade

Responsável

Equipe

Data de Abertura

Prazo Inicial

Prazo Atual

Garantia

Cobertura

Status

Observações Internas
```

### Aba Cliente

Informações:

```text
Nome

Contato Principal

Telefone

WhatsApp

Email

Endereço

Pessoa Responsável

Preferência de Contato

Horários Disponíveis

Histórico de Atendimentos
```

### Aba Projeto

Informações:

```text
Projeto

Revisão Executada

Ambientes

Móveis

Materiais

Ferragens

Data da Instalação

Equipe de Instalação

Pendências Anteriores

Documentos Técnicos
```

### Aba Pedido

Informações:

```text
Pedido

Data

Valor

Itens

Condições Comerciais

Vendedor

Status

Documentos
```

### Aba Contrato

Informações:

```text
Contrato

Data

Prazo de Garantia

Coberturas

Exclusões

Responsabilidades

Condições Especiais

Documento Assinado
```

### Aba Garantia

Informações:

```text
Data Inicial

Data Final

Tipo de Garantia

Item Coberto

Cobertura Aplicável

Exclusões

Status

Resultado da Análise

Responsável pela Análise

Justificativa
```

### Aba Item Afetado

Informações:

```text
Ambiente

Móvel

Componente

Peça

Material

Ferragem

Lote

Código

Descrição

Quantidade

Revisão Técnica

Fotos
```

### Aba Solicitação

Informações:

```text
Descrição do Cliente

Data do Problema

Frequência

Condições de Uso

Impacto

Fotos

Vídeos

Áudios

Arquivos

Resultado Esperado
```

### Aba Triagem

Informações:

```text
Perguntas Realizadas

Respostas

Classificação

Gravidade

Urgência

Risco

Possível Causa

Atendimento Remoto Possível

Visita Necessária

Peça Possivelmente Necessária

Próxima Ação
```

### Aba Diagnóstico

Informações:

```text
Sintoma

Problema Identificado

Causa Provável

Causa Confirmada

Responsabilidade

Solução Recomendada

Peças Necessárias

Materiais Necessários

Serviços Necessários

Tempo Estimado

Custo Estimado
```

### Aba Atendimentos

Informações:

```text
Data

Canal

Responsável

Descrição

Orientação

Resultado

Próxima Ação

Prazo
```

### Aba Visitas

Informações:

```text
Data

Horário

Técnico

Equipe

Objetivo

Resultado

Diagnóstico

Serviços

Peças

Pendências

Assinatura
```

### Aba Ordem de Serviço

Informações:

```text
Número

Tipo

Responsável

Serviços

Peças

Materiais

Data Planejada

Data Executada

Tempo

Resultado

Status
```

### Aba Peças

Informações:

```text
Peça

Descrição

Quantidade

Origem

Estoque

Produção

Compra

Reserva

Data Prevista

Status
```

### Aba Materiais

Informações:

```text
Material

Quantidade Prevista

Quantidade Reservada

Quantidade Consumida

Quantidade Devolvida

Custo

Status
```

### Aba Serviços

Informações:

```text
Serviço

Tipo

Responsável

Quantidade

Unidade

Tempo Previsto

Tempo Real

Custo

Resultado
```

### Aba Custos

Informações:

```text
Mão de Obra

Peças

Materiais

Deslocamento

Frete

Terceirizados

Hospedagem

Alimentação

Descontos

Custo Total

Valor Cobrado

Responsável pelo Custo
```

### Aba Responsabilidades

Informações:

```text
Empresa

Cliente

Fornecedor

Terceirizado

Produção

Instalação

Projeto

Material

Ferragem

Uso Indevido

Indeterminada
```

### Aba Prazos

Informações:

```text
Prazo Inicial

Prazo de Triagem

Prazo de Diagnóstico

Prazo de Visita

Prazo de Peça

Prazo de Solução

Prazo Atual

Motivos de Alteração

Dias em Aberto
```

### Aba SLA

Informações:

```text
Política

Tempo de Primeira Resposta

Tempo de Triagem

Tempo de Atendimento

Tempo de Solução

Prazo Consumido

Prazo Restante

Status do SLA

Violações
```

### Aba Pendências

Informações:

```text
Descrição

Categoria

Responsável

Prioridade

Prazo

Dependência

Status

Solução
```

### Aba Ocorrências

Informações:

```text
Tipo

Descrição

Data

Responsável

Impacto

Evidências

Ação Tomada

Status
```

### Aba Comunicações

Informações:

```text
Data

Canal

Remetente

Destinatário

Assunto

Mensagem

Anexos

Status de Entrega

Confirmação de Leitura
```

### Aba Aceite

Informações:

```text
Resultado

Serviços Executados

Peças Substituídas

Ressalvas

Pendências Restantes

Cliente

Assinatura

Data

Observações
```

### Aba Satisfação

Informações:

```text
Nota Geral

Atendimento

Prazo

Comunicação

Qualidade do Serviço

Técnico

Comentários

Recomendaria a Empresa

Data
```

---

# Página

## Solicitações Recebidas

### ID

```text
AST-SOL-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar solicitações recebidas antes de sua conversão em chamado formal.

### Canais

```text
Telefone

WhatsApp

Email

Site

Portal do Cliente

CRM

Instalação

Comercial

Formulário Interno

Atendimento Presencial
```

### Status

```text
Recebida

Não Classificada

Em Análise

Convertida em Chamado

Duplicada

Descartada

Cancelada
```

### Ações

```text
Abrir Solicitação

Identificar Cliente

Identificar Projeto

Solicitar Informações

Anexar Arquivos

Converter em Chamado

Marcar como Duplicada

Descartar
```

---

# Página

## Triagens

### ID

```text
AST-TRI-001
```

### Tipo

```text
Kanban
```

### Objetivo

Classificar e direcionar os chamados antes da execução.

### Etapas

```text
Aguardando Triagem

Em Análise

Aguardando Informações

Atendimento Remoto

Visita Necessária

Peça Necessária

Encaminhado

Concluído
```

### Critérios

```text
Tipo de Problema

Gravidade

Risco

Urgência

Cobertura

Complexidade

Responsabilidade Provável

Necessidade de Visita

Necessidade de Peça

Necessidade de Produção
```

---

# Página

## Diagnósticos

### ID

```text
AST-DIA-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar hipóteses, verificações, causas e soluções relacionadas aos chamados.

### Status

```text
Inicial

Em Investigação

Aguardando Teste

Aguardando Visita

Aguardando Informação

Confirmado

Inconclusivo

Cancelado
```

### Ações

```text
Novo Diagnóstico

Registrar Sintoma

Registrar Hipótese

Adicionar Teste

Adicionar Evidência

Confirmar Causa

Definir Solução

Solicitar Segunda Análise

Encerrar Diagnóstico
```

---

# Página

## Garantias

### ID

```text
AST-GAR-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar garantias vinculadas a projetos, produtos, materiais, ferragens e serviços.

### Tipos

```text
Garantia Contratual

Garantia Legal

Garantia de Material

Garantia de Ferragem

Garantia de Serviço

Garantia de Instalação

Garantia Estendida

Garantia do Fornecedor
```

### Status

```text
Vigente

Próxima do Vencimento

Vencida

Suspensa

Cancelada

Encerrada
```

### Ações

```text
Nova Garantia

Consultar Cobertura

Prorrogar

Suspender

Cancelar

Vincular Item

Vincular Documento

Abrir Chamado

Gerar Termo
```

---

# Página

## Coberturas

### ID

```text
AST-COB-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir os eventos, itens e serviços cobertos por cada política de garantia.

### Exemplos

```text
Defeito de Fabricação

Defeito de Montagem

Defeito de Instalação

Ferragem com Defeito

Material com Defeito

Regulagem

Peça Faltante

Correção de Acabamento
```

### Exclusões

```text
Uso Indevido

Umidade Externa

Infiltração

Sobrecarga

Alteração por Terceiros

Falta de Manutenção

Desgaste Natural

Danos Acidentais

Mudança de Local
```

---

# Página

## Prazos de Garantia

### ID

```text
AST-PGA-001
```

### Tipo

```text
Configuração
```

### Objetivo

Definir prazos de garantia por item, categoria, serviço ou fornecedor.

### Campos

```text
Categoria

Item

Tipo de Garantia

Prazo

Unidade

Data Inicial

Evento Inicial

Condições

Exclusões

Status
```

---

# Página

## Itens em Garantia

### ID

```text
AST-IGA-001
```

### Tipo

```text
Consulta
```

### Objetivo

Consultar os itens que possuem garantia ativa.

### Pesquisas

```text
Cliente

Projeto

Pedido

Contrato

Móvel

Componente

Peça

Ferragem

Material

Número de Série
```

---

# Página

## Atendimentos Remotos

### ID

```text
AST-REM-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar atendimentos realizados sem visita presencial.

### Canais

```text
Telefone

WhatsApp

Vídeo

Email

Chat

Portal
```

### Ações

```text
Iniciar Atendimento

Enviar Orientação

Solicitar Foto

Solicitar Vídeo

Realizar Videochamada

Registrar Teste

Confirmar Solução

Agendar Visita

Encerrar
```

---

# Página

## Visitas Técnicas

### ID

```text
AST-VIS-001
```

### Tipo

```text
Lista
```

### Objetivo

Planejar e registrar visitas realizadas pela assistência.

### Tipos

```text
Diagnóstico

Manutenção

Correção

Ajuste

Instalação de Peça

Reinspeção

Retorno

Visita Preventiva

Visita Cobrada
```

### Status

```text
Planejada

Aguardando Agendamento

Agendada

Confirmada

Em Deslocamento

Em Atendimento

Pausada

Concluída

Com Pendência

Reagendada

Cancelada
```

### Ações

```text
Nova Visita

Agendar

Confirmar

Alterar Técnico

Alterar Equipe

Registrar Saída

Registrar Chegada

Iniciar Atendimento

Registrar Diagnóstico

Registrar Serviço

Registrar Peça

Criar Pendência

Coletar Assinatura

Concluir

Reagendar

Cancelar
```

---

# Página

## Agenda da Assistência

### ID

```text
AST-AGE-001
```

### Tipo

```text
Calendário
```

### Objetivo

Organizar visitas, retornos e compromissos da assistência técnica.

### Visualizações

```text
Dia

Semana

Mês

Timeline

Por Técnico

Por Equipe

Por Região
```

### Regras

Alterações de data, horário ou responsável deverão ocorrer por clique e edição controlada.

Não deverá ser utilizado drag and drop.

---

# Página

## Equipes Técnicas

### ID

```text
AST-EQP-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar equipes responsáveis pelos atendimentos.

### Campos

```text
Nome

Líder

Técnicos

Ajudantes

Terceirizados

Habilidades

Região

Veículo

Disponibilidade

Status
```

---

# Página

## Técnicos

### ID

```text
AST-TEC-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar profissionais responsáveis por diagnósticos, manutenções e correções.

### Informações

```text
Nome

Contato

Equipe

Especialidades

Habilidades

Certificações

Ferramentas

Região

Disponibilidade

Avaliação

Status
```

---

# Página

## Terceirizados

### ID

```text
AST-TER-001
```

### Tipo

```text
Lista
```

### Objetivo

Gerenciar prestadores externos utilizados nos atendimentos.

---

# Página

## Ordens de Serviço

### ID

```text
AST-ODS-001
```

### Tipo

```text
Lista
```

### Objetivo

Formalizar os serviços que deverão ser executados em um chamado.

### Status

```text
Rascunho

Aguardando Aprovação

Aprovada

Aguardando Agendamento

Agendada

Em Execução

Pausada

Aguardando Peça

Aguardando Cliente

Concluída

Cancelada
```

### Colunas

```text
Número

Chamado

Cliente

Projeto

Tipo

Responsável

Data Planejada

Prazo

Valor

Garantia

Status
```

### Ações

```text
Nova Ordem

Abrir

Editar

Adicionar Serviço

Adicionar Peça

Adicionar Material

Solicitar Aprovação

Aprovar

Agendar

Iniciar

Pausar

Concluir

Cancelar

Gerar PDF

Enviar ao Cliente

Imprimir
```

---

# Página

## Cadastro da Ordem de Serviço

### ID

```text
AST-ODS-002
```

### Tipo

```text
Cadastro
```

### Abas

```text
Geral

Chamado

Cliente

Projeto

Serviços

Peças

Materiais

Equipe

Agenda

Deslocamento

Custos

Cobrança

Checklists

Fotos

Documentos

Assinaturas

Resultado

Histórico

Auditoria
```

---

# Página

## Serviços

### ID

```text
AST-SER-001
```

### Tipo

```text
Lista
```

### Objetivo

Cadastrar os serviços que podem ser executados pela assistência.

### Exemplos

```text
Regulagem de Porta

Regulagem de Gaveta

Troca de Dobradiça

Troca de Corrediça

Troca de Puxador

Correção de Fita

Substituição de Peça

Reinstalação

Nivelamento

Reforço de Fixação

Manutenção Preventiva

Diagnóstico Técnico
```

### Campos

```text
Código

Descrição

Categoria

Tempo Padrão

Preço

Custo

Garantia

Habilidade Necessária

Ferramentas

Materiais

Status
```

---

# Página

## Manutenções

### ID

```text
AST-MAN-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar manutenções corretivas e preventivas realizadas nos produtos instalados.

### Tipos

```text
Preventiva

Corretiva

Preditiva

Emergencial

Periódica

Sob Demanda
```

---

# Página

## Ajustes

### ID

```text
AST-AJS-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar pequenos ajustes executados sem substituição estrutural relevante.

### Exemplos

```text
Alinhamento

Nivelamento

Regulagem

Aperto

Reposicionamento

Correção de Folga

Ajuste de Porta

Ajuste de Gaveta
```

---

# Página

## Correções

### ID

```text
AST-COR-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar correções destinadas a eliminar defeitos ou divergências.

---

# Página

## Peças de Reposição

### ID

```text
AST-PEC-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar peças necessárias para resolver os chamados.

### Origens

```text
Estoque

Produção

Fornecedor

Terceirizado

Reaproveitamento

Cliente
```

### Status

```text
Identificada

Aguardando Validação

Disponível em Estoque

Reservada

Aguardando Produção

Em Produção

Aguardando Compra

Em Compra

Em Trânsito

Recebida

Instalada

Devolvida

Cancelada
```

### Ações

```text
Nova Solicitação

Selecionar Peça Original

Verificar Estoque

Reservar

Solicitar Produção

Solicitar Compra

Acompanhar

Registrar Recebimento

Registrar Instalação

Cancelar
```

---

# Página

## Materiais

### ID

```text
AST-MAT-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar materiais e consumíveis utilizados nos atendimentos.

---

# Página

## Ferramentas

### ID

```text
AST-FER-001
```

### Tipo

```text
Lista
```

### Objetivo

Controlar ferramentas enviadas e utilizadas pelas equipes técnicas.

---

# Página

## Reservas

### ID

```text
AST-RES-001
```

### Tipo

```text
Lista
```

### Objetivo

Acompanhar peças e materiais reservados para chamados e ordens de serviço.

---

# Página

## Solicitações ao Estoque

### ID

```text
AST-EST-001
```

### Tipo

```text
Lista
```

### Objetivo

Solicitar formalmente peças, materiais, ferragens e consumíveis ao Estoque.

---

# Página

## Solicitações à Produção

### ID

```text
AST-PRD-001
```

### Tipo

```text
Lista
```

### Objetivo

Solicitar produção ou reprodução de peças necessárias aos atendimentos.

### Informações

```text
Chamado

Projeto Original

Revisão

Móvel

Peça

Material

Dimensões

Quantidade

Prioridade

Prazo

Motivo

Documentos Técnicos
```

### Regras

Toda solicitação deverá ser validada pelo módulo Projetos quando houver dúvida técnica ou alteração em relação à peça original.

---

# Página

## Solicitações de Compra

### ID

```text
AST-COM-001
```

### Tipo

```text
Lista
```

### Objetivo

Solicitar compras necessárias para concluir atendimentos.

---

# Página

## Retrabalhos

### ID

```text
AST-RET-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar serviços refeitos em razão de falhas anteriores.

### Origens

```text
Projeto

Produção

Qualidade

Instalação

Assistência

Fornecedor
```

### Etapas

```text
Identificado

Em Análise

Aguardando Planejamento

Aguardando Material

Aguardando Produção

Agendado

Em Execução

Aguardando Verificação

Concluído

Cancelado
```

---

# Página

## Não Conformidades

### ID

```text
AST-NCO-001
```

### Tipo

```text
Lista
```

### Objetivo

Consultar e registrar não conformidades identificadas durante atendimentos.

Toda não conformidade deverá ser integrada ao módulo Qualidade.

---

# Página

## Causas

### ID

```text
AST-CAU-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Analisar as causas dos chamados e atendimentos.

### Categorias

```text
Projeto

Medição

Material

Ferragem

Produção

Montagem

Instalação

Transporte

Uso do Cliente

Manutenção

Fornecedor

Desgaste Natural

Causa Indeterminada
```

---

# Página

## Responsabilidades

### ID

```text
AST-RSP-001
```

### Tipo

```text
Lista
```

### Objetivo

Definir quem deverá assumir a responsabilidade operacional e financeira pelo atendimento.

### Responsáveis Possíveis

```text
Empresa

Projetos

Produção

Qualidade

Instalação

Expedição

Fornecedor

Terceirizado

Cliente

Compartilhada

Indeterminada
```

### Informações

```text
Chamado

Responsável

Percentual

Justificativa

Aprovador

Custo Associado

Status
```

---

# Página

## Custos

### ID

```text
AST-CUS-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Consolidar os custos relacionados à assistência técnica.

### Composição

```text
Mão de Obra

Peças

Materiais

Ferragens

Deslocamento

Combustível

Pedágios

Hospedagem

Alimentação

Terceirizados

Frete

Descontos

Reembolsos

Custo Total
```

### Visualizações

```text
Por Chamado

Por Projeto

Por Cliente

Por Causa

Por Responsável

Por Técnico

Por Período
```

---

# Página

## Cobranças

### ID

```text
AST-COB-002
```

### Tipo

```text
Lista
```

### Objetivo

Controlar atendimentos cobrados do cliente quando não cobertos por garantia.

### Status

```text
Não Avaliada

Isenta

Aguardando Orçamento

Orçada

Aguardando Aprovação

Aprovada

Reprovada

Encaminhada ao Financeiro

Recebida

Cancelada
```

### Informações

```text
Chamado

Cliente

Motivo da Cobrança

Serviços

Peças

Materiais

Deslocamento

Valor

Aprovação do Cliente

Financeiro
```

---

# Página

## Aprovações

### ID

```text
AST-APR-001
```

### Tipo

```text
Lista
```

### Objetivo

Centralizar aprovações necessárias ao atendimento.

### Tipos

```text
Cobertura de Garantia

Atendimento Fora de Garantia

Custo Extra

Troca de Peça

Produção de Peça

Desconto

Desvio

Responsabilidade

Encerramento com Pendência
```

---

# Página

## Prazos

### ID

```text
AST-PRA-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Acompanhar prazos e tempos dos atendimentos.

### Indicadores

```text
Primeira Resposta

Triagem

Diagnóstico

Agendamento

Visita

Peça

Produção

Solução

Encerramento
```

---

# Página

## SLA

### ID

```text
AST-SLA-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Controlar níveis de serviço definidos por prioridade, contrato ou tipo de atendimento.

### Estados

```text
Dentro do Prazo

Próximo do Vencimento

Vencido

Suspenso

Encerrado
```

### Regras

```text
Prioridade

Tipo de Chamado

Tipo de Cliente

Contrato

Garantia

Região

Horário Comercial

Dias Úteis
```

---

# Página

## Prioridades

### ID

```text
AST-PRI-001
```

### Tipo

```text
Configuração
```

### Objetivo

Definir regras de prioridade dos chamados.

### Critérios

```text
Risco de Segurança

Impossibilidade de Uso

Impacto no Cliente

Número de Itens Afetados

Prazo Contratual

Reincidência

Cliente Estratégico

Garantia

Urgência Comercial
```

---

# Página

## Pendências

### ID

```text
AST-PEN-001
```

### Tipo

```text
Kanban
```

### Objetivo

Controlar tudo que impede a continuidade ou encerramento do atendimento.

### Categorias

```text
Cliente

Projeto

Peça

Material

Ferragem

Produção

Fornecedor

Técnico

Agenda

Aprovação

Documento

Pagamento
```

### Etapas

```text
Nova

Em Análise

Aguardando Responsável

Aguardando Cliente

Aguardando Material

Aguardando Produção

Aguardando Compra

Aguardando Aprovação

Em Resolução

Resolvida

Cancelada
```

---

# Página

## Ocorrências

### ID

```text
AST-OCO-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar acontecimentos relevantes ocorridos durante o atendimento.

### Exemplos

```text
Cliente Ausente

Local Não Liberado

Peça Incorreta

Material Faltante

Atraso

Dano

Acidente

Falha de Comunicação

Problema de Acesso

Serviço Não Autorizado
```

---

# Página

## Fotos

### ID

```text
AST-FOT-001
```

### Tipo

```text
Galeria
```

### Objetivo

Centralizar imagens vinculadas aos chamados, diagnósticos, visitas e soluções.

### Categorias

```text
Problema Inicial

Diagnóstico

Antes do Serviço

Durante o Serviço

Peça Substituída

Material

Dano

Resultado Final

Pendência

Comprovante
```

---

# Página

## Documentos

### ID

```text
AST-DOC-001
```

### Tipo

```text
Gerenciador de Arquivos
```

### Objetivo

Centralizar documentos relacionados aos atendimentos.

### Tipos

```text
Chamado

Ordem de Serviço

Garantia

Contrato

Laudo

Relatório Técnico

Orçamento

Aprovação

Termo de Atendimento

Termo de Aceite

Nota Fiscal

Comprovante
```

---

# Página

## Assinaturas

### ID

```text
AST-ASS-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar assinaturas relacionadas às visitas e serviços executados.

### Tipos

```text
Chegada

Autorização

Ordem de Serviço

Serviço Executado

Pendência

Aceite

Encerramento
```

---

# Página

## Aceites

### ID

```text
AST-ACE-001
```

### Tipo

```text
Lista
```

### Objetivo

Registrar formalmente a avaliação do cliente sobre o serviço executado.

### Resultados

```text
Aceito Integralmente

Aceito com Ressalvas

Aceito Parcialmente

Não Aceito

Cliente Ausente

Responsável Não Autorizado
```

---

# Página

## Satisfação do Cliente

### ID

```text
AST-SAT-001
```

### Tipo

```text
Dashboard Analítico
```

### Objetivo

Medir a percepção do cliente em relação ao atendimento.

### Critérios

```text
Facilidade de Abertura

Tempo de Resposta

Comunicação

Pontualidade

Profissionalismo

Qualidade da Solução

Limpeza

Resultado Final

Satisfação Geral
```

### Indicadores

```text
Nota Média

NPS

Taxa de Resposta

Índice de Reclamação

Índice de Reabertura

Satisfação por Técnico

Satisfação por Tipo de Chamado
```

---

# Página

## Histórico

### ID

```text
AST-HIS-001
```

### Tipo

```text
Consulta
```

### Objetivo

Consultar alterações, transferências, diagnósticos, visitas, soluções e decisões relacionadas aos atendimentos.

---

# Página

## Timeline

### ID

```text
AST-TML-001
```

### Tipo

```text
Timeline
```

### Objetivo

Apresentar os acontecimentos do atendimento em ordem cronológica.

### Eventos

```text
Solicitação Recebida

Chamado Criado

Triagem Iniciada

Garantia Verificada

Diagnóstico Registrado

Atendimento Remoto Iniciado

Visita Agendada

Técnico Chegou

Serviço Iniciado

Peça Solicitada

Peça Recebida

Serviço Concluído

Cliente Assinou

Satisfação Registrada

Chamado Encerrado

Chamado Reaberto
```

---

# Página

## Indicadores

### ID

```text
AST-KPI-001
```

### Tipo

```text
Dashboard Analítico
```

### Indicadores

```text
Chamados Abertos

Chamados Encerrados

Chamados Reabertos

Chamados em Garantia

Chamados Fora de Garantia

Tempo Médio de Primeira Resposta

Tempo Médio de Triagem

Tempo Médio de Diagnóstico

Tempo Médio de Solução

Solução na Primeira Visita

Chamados por Causa

Chamados por Projeto

Chamados por Cliente

Chamados por Técnico

Chamados por Responsabilidade

Taxa de Retrabalho

Taxa de Reincidência

Custo Médio por Chamado

Custo Total da Assistência

Cumprimento de SLA

Satisfação do Cliente
```

---

# Página

## Relatórios

### ID

```text
AST-REL-001
```

### Tipo

```text
Relatório
```

### Relatórios Disponíveis

```text
Chamados Abertos

Chamados Encerrados

Chamados Atrasados

Chamados por Cliente

Chamados por Projeto

Chamados por Tipo

Chamados por Causa

Chamados por Responsabilidade

Chamados em Garantia

Chamados Fora de Garantia

Visitas Técnicas

Ordens de Serviço

Peças de Reposição

Materiais Consumidos

Retrabalhos

Não Conformidades

Custos

Cobranças

Cumprimento de SLA

Tempo Médio de Solução

Solução na Primeira Visita

Reincidências

Satisfação do Cliente

Desempenho dos Técnicos
```

---

# Página

## Templates

### ID

```text
AST-TMP-001
```

### Tipo

```text
Configuração
```

### Objetivo

Criar modelos reutilizáveis para documentos e comunicações da assistência.

### Tipos

```text
Chamado

Triagem

Diagnóstico

Ordem de Serviço

Checklist de Visita

Relatório Técnico

Solicitação de Peça

Solicitação de Produção

Orçamento de Serviço

Termo de Atendimento

Termo de Aceite

Pesquisa de Satisfação

Email

WhatsApp
```

---

# Página

## Configurações

### ID

```text
AST-CFG-001
```

### Tipo

```text
Configuração
```

### Configurações

```text
Numeração dos Chamados

Numeração das Ordens de Serviço

Tipos de Chamado

Categorias

Prioridades

Status

Canais de Atendimento

Tipos de Garantia

Coberturas

Exclusões

Prazos de Garantia

Políticas de SLA

Tipos de Serviço

Causas

Responsabilidades

Tipos de Ocorrência

Tipos de Pendência

Regras de Cobrança

Regras de Aprovação

Regras de Encerramento

Templates

Checklists

Notificações

Integrações
```

---

# Dialogs

```text
AST-DLG-001 Novo Chamado

AST-DLG-002 Identificar Cliente

AST-DLG-003 Selecionar Projeto

AST-DLG-004 Selecionar Item Afetado

AST-DLG-005 Classificar Chamado

AST-DLG-006 Alterar Prioridade

AST-DLG-007 Assumir Chamado

AST-DLG-008 Transferir Chamado

AST-DLG-009 Verificar Garantia

AST-DLG-010 Solicitar Informações

AST-DLG-011 Registrar Triagem

AST-DLG-012 Registrar Diagnóstico

AST-DLG-013 Registrar Atendimento Remoto

AST-DLG-014 Agendar Visita

AST-DLG-015 Reagendar Visita

AST-DLG-016 Selecionar Técnico

AST-DLG-017 Criar Ordem de Serviço

AST-DLG-018 Adicionar Serviço

AST-DLG-019 Solicitar Peça

AST-DLG-020 Reservar Peça

AST-DLG-021 Solicitar Produção

AST-DLG-022 Solicitar Compra

AST-DLG-023 Registrar Consumo

AST-DLG-024 Registrar Ocorrência

AST-DLG-025 Nova Pendência

AST-DLG-026 Registrar Retrabalho

AST-DLG-027 Registrar Não Conformidade

AST-DLG-028 Definir Responsabilidade

AST-DLG-029 Registrar Custo

AST-DLG-030 Gerar Cobrança

AST-DLG-031 Solicitar Aprovação

AST-DLG-032 Iniciar Serviço

AST-DLG-033 Pausar Serviço

AST-DLG-034 Concluir Serviço

AST-DLG-035 Registrar Solução

AST-DLG-036 Coletar Assinatura

AST-DLG-037 Registrar Aceite

AST-DLG-038 Enviar Pesquisa de Satisfação

AST-DLG-039 Encerrar Chamado

AST-DLG-040 Reabrir Chamado
```

---

# Wizards

```text
AST-WIZ-001 Assistente de Abertura do Chamado

AST-WIZ-002 Assistente de Triagem

AST-WIZ-003 Assistente de Verificação de Garantia

AST-WIZ-004 Assistente de Diagnóstico

AST-WIZ-005 Assistente de Atendimento Remoto

AST-WIZ-006 Assistente de Planejamento da Visita

AST-WIZ-007 Assistente de Ordem de Serviço

AST-WIZ-008 Assistente de Solicitação de Peça

AST-WIZ-009 Assistente de Atendimento Presencial

AST-WIZ-010 Assistente de Cobrança

AST-WIZ-011 Assistente de Encerramento

AST-WIZ-012 Assistente de Pesquisa de Satisfação
```

---

# Componentes Específicos

```text
AST-CPT-001 Central de Atendimento

AST-CPT-002 Kanban de Chamados

AST-CPT-003 Classificador de Chamados

AST-CPT-004 Verificador de Garantia

AST-CPT-005 Roteiro de Triagem

AST-CPT-006 Editor de Diagnóstico

AST-CPT-007 Timeline de Atendimento

AST-CPT-008 Agenda de Visitas

AST-CPT-009 Painel do Técnico

AST-CPT-010 Editor de Ordem de Serviço

AST-CPT-011 Gerenciador de Peças

AST-CPT-012 Gerenciador de Pendências

AST-CPT-013 Calculadora de Custos

AST-CPT-014 Indicador de SLA

AST-CPT-015 Galeria Antes e Depois

AST-CPT-016 Captura de Assinatura

AST-CPT-017 Gerador de Relatório Técnico

AST-CPT-018 Painel de Satisfação
```

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo `theme_design`.

Nenhum componente poderá conter aparência hardcoded.

---

# Eventos

```text
TechnicalSupportRequestReceived

TechnicalSupportTicketCreated

TechnicalSupportTicketClassified

TechnicalSupportTicketAssigned

TechnicalSupportTicketTransferred

TechnicalSupportPriorityChanged

TechnicalSupportWarrantyChecked

TechnicalSupportWarrantyApproved

TechnicalSupportWarrantyRejected

TechnicalSupportTriageStarted

TechnicalSupportTriageCompleted

TechnicalSupportDiagnosisCreated

TechnicalSupportRemoteServiceStarted

TechnicalSupportRemoteServiceCompleted

TechnicalSupportVisitScheduled

TechnicalSupportVisitRescheduled

TechnicalSupportTechnicianAssigned

TechnicalSupportWorkOrderCreated

TechnicalSupportWorkOrderApproved

TechnicalSupportServiceStarted

TechnicalSupportServicePaused

TechnicalSupportPartRequested

TechnicalSupportPartReserved

TechnicalSupportProductionRequested

TechnicalSupportPurchaseRequested

TechnicalSupportOccurrenceCreated

TechnicalSupportPendingIssueCreated

TechnicalSupportReworkCreated

TechnicalSupportNonConformityCreated

TechnicalSupportResponsibilityDefined

TechnicalSupportCostRegistered

TechnicalSupportChargeCreated

TechnicalSupportServiceCompleted

TechnicalSupportCustomerAcceptanceRegistered

TechnicalSupportSatisfactionRegistered

TechnicalSupportTicketResolved

TechnicalSupportTicketClosed

TechnicalSupportTicketReopened
```

---

# Automações

```text
Solicitação recebida

↓

Identificar cliente

↓

Identificar projeto

↓

Sugerir categoria

↓

Criar chamado

↓

Notificar responsável
```

```text
Chamado criado

↓

Verificar garantia

↓

Calcular SLA

↓

Criar timeline

↓

Criar checklist de triagem
```

```text
Garantia aprovada

↓

Marcar atendimento sem cobrança

↓

Definir prazo

↓

Notificar cliente
```

```text
Peça necessária

↓

Consultar estoque

↓

Reservar quando disponível

↓

Solicitar produção ou compra quando indisponível

↓

Atualizar prazo do chamado
```

```text
Visita agendada

↓

Reservar técnico

↓

Criar evento na agenda

↓

Enviar confirmação ao cliente

↓

Gerar ordem de serviço
```

```text
Serviço concluído

↓

Registrar peças e materiais

↓

Registrar custos

↓

Coletar aceite

↓

Enviar pesquisa de satisfação
```

```text
Chamado encerrado

↓

Atualizar garantia

↓

Atualizar histórico do cliente

↓

Atualizar indicadores

↓

Enviar resumo ao cliente
```

```text
SLA próximo do vencimento

↓

Gerar alerta

↓

Notificar responsável

↓

Escalonar conforme política
```

---

# Integrações

```text
CRM

Comercial

Projetos

Orçamentos

Compras

Estoque

PCP

Produção

Qualidade

Expedição

Instalação

Financeiro

Fiscal

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Email

WhatsApp

Assinatura Digital

Mapas

Portal do Cliente
```

---

# Permissões

```text
technical_support.dashboard.read

technical_support.central.read

technical_support.ticket.read

technical_support.ticket.create

technical_support.ticket.update

technical_support.ticket.classify

technical_support.ticket.assign

technical_support.ticket.transfer

technical_support.ticket.change_priority

technical_support.ticket.resolve

technical_support.ticket.close

technical_support.ticket.reopen

technical_support.ticket.cancel

technical_support.warranty.read

technical_support.warranty.check

technical_support.warranty.approve

technical_support.warranty.reject

technical_support.warranty.manage

technical_support.triage.execute

technical_support.diagnosis.create

technical_support.diagnosis.update

technical_support.remote_service.execute

technical_support.visit.read

technical_support.visit.create

technical_support.visit.schedule

technical_support.visit.reschedule

technical_support.visit.execute

technical_support.team.read

technical_support.team.manage

technical_support.technician.manage

technical_support.work_order.read

technical_support.work_order.create

technical_support.work_order.update

technical_support.work_order.approve

technical_support.work_order.execute

technical_support.service.manage

technical_support.maintenance.manage

technical_support.adjustment.register

technical_support.correction.register

technical_support.part.request

technical_support.part.reserve

technical_support.production.request

technical_support.purchase.request

technical_support.material.consume

technical_support.rework.create

technical_support.rework.execute

technical_support.non_conformity.create

technical_support.responsibility.define

technical_support.cost.read

technical_support.cost.register

technical_support.charge.create

technical_support.charge.approve

technical_support.sla.read

technical_support.sla.manage

technical_support.pending_issue.manage

technical_support.occurrence.manage

technical_support.photo.manage

technical_support.document.manage

technical_support.signature.collect

technical_support.acceptance.register

technical_support.satisfaction.read

technical_support.satisfaction.register

technical_support.report.read

technical_support.report.export

technical_support.configuration.manage
```

---

# Relatórios e Documentos Gerados

```text
Ficha do Chamado

Relatório de Triagem

Relatório de Diagnóstico

Ordem de Serviço

Agenda de Visitas

Checklist de Atendimento

Solicitação de Peça

Solicitação de Produção

Solicitação de Compra

Relatório de Consumo

Relatório de Custos

Orçamento de Assistência

Relatório Técnico

Relatório de Retrabalho

Relatório de Não Conformidade

Termo de Atendimento

Termo de Aceite

Termo de Ressalvas

Comprovante de Serviço

Pesquisa de Satisfação

Relatório de Garantias

Relatório de SLA

Relatório de Causas

Relatório de Responsabilidades

Relatório Final do Chamado
```

---

# Recursos de Inteligência Artificial

```text
Classificar chamados automaticamente

Identificar cliente e projeto pela mensagem

Extrair problemas de conversas

Sugerir perguntas de triagem

Sugerir diagnóstico inicial

Localizar chamados semelhantes

Sugerir causa provável

Sugerir solução

Identificar cobertura de garantia

Classificar responsabilidade provável

Estimar prazo de atendimento

Estimar custo

Priorizar chamados

Prever violação de SLA

Detectar reincidências

Analisar fotos do problema

Gerar resposta ao cliente

Gerar relatório técnico

Resumir histórico do atendimento

Pesquisar chamados em linguagem natural
```

A IA nunca poderá aprovar garantia, definir responsabilidade definitiva, autorizar cobrança, encerrar chamado ou registrar aceite sem confirmação explícita de um usuário autorizado.

---

# Regras Funcionais

1. Todo chamado deverá pertencer a um Tenant.

2. Todo chamado deverá possuir cliente identificado antes do encerramento.

3. Quando aplicável, o chamado deverá estar vinculado ao projeto, pedido, contrato ou instalação de origem.

4. Todo chamado deverá possuir tipo, prioridade, responsável e status.

5. A garantia deverá ser verificada com base nas condições vigentes na data da entrega.

6. Regras de garantia não poderão ser alteradas retroativamente para prejudicar ou beneficiar silenciosamente um chamado.

7. Chamados críticos deverão gerar alerta imediato.

8. Toda alteração de prioridade deverá possuir histórico.

9. Chamados transferidos deverão manter o responsável anterior registrado.

10. Toda visita deverá possuir data, técnico e objetivo.

11. Peças solicitadas deverão manter vínculo com o item original.

12. Alterações técnicas deverão ser validadas pelo módulo Projetos.

13. Produções de reposição deverão ser executadas por ordem formal.

14. Movimentações de materiais deverão ocorrer pelo módulo Estoque.

15. Compras deverão ocorrer pelo módulo Compras.

16. Custos deverão permanecer vinculados ao chamado.

17. Atendimentos fora de garantia deverão seguir as regras de cobrança configuradas.

18. A responsabilidade deverá possuir justificativa e aprovador quando impactar custos.

19. Retrabalhos deverão manter vínculo com a ocorrência original.

20. Não conformidades deverão ser encaminhadas ao módulo Qualidade.

21. Chamados não poderão ser encerrados com pendências obrigatórias abertas.

22. O encerramento com ressalvas deverá exigir justificativa.

23. O aceite deverá registrar o responsável e a data.

24. Chamados encerrados não poderão ser excluídos.

25. Reaberturas deverão preservar o encerramento anterior.

26. Toda comunicação com o cliente deverá permanecer no histórico.

27. Nenhum componente visual poderá possuir aparência hardcoded fora do `theme_design`.

---

# Observações Arquiteturais

O módulo Assistência Técnica será a fonte oficial dos atendimentos realizados após a entrega.

CRM deverá preservar o histórico do relacionamento com o cliente.

Projetos deverá fornecer a definição técnica original.

Produção deverá fabricar peças de reposição quando necessário.

Estoque deverá controlar peças e materiais utilizados.

Qualidade deverá receber não conformidades e reincidências.

Financeiro deverá receber cobranças aprovadas.

O módulo Assistência Técnica não poderá alterar silenciosamente:

```text
Projeto original

Contrato

Garantia

Responsabilidade

Custos

Peças utilizadas

Resultado do atendimento
```

Toda alteração deverá possuir origem, responsável, justificativa e auditoria.

---

# Próxima Etapa

```text
ETAPA 03-N

Catálogo Completo de Páginas

Financeiro
```
ETAPA 03-N

Catálogo Completo de Páginas

Financeiro

ID do Módulo

FIN

Objetivo

O módulo Financeiro será responsável por controlar toda amovimentação financeira do ORGANIZEG3, desde a geração automática detítulos pelos demais módulos até a conciliação bancária, fluxo de caixa,DRE gerencial e indicadores financeiros.

Será um dos maiores módulos do ERP e integrará praticamente todos osdemais módulos do sistema.

Escopo Geral

Plano de Contas

Centros de Custo

Centros de Resultado

Contas a Receber

Contas a Pagar

Caixa

Bancos

PIX

Boletos

Cartões

Cheques

Conciliação Bancária

Fluxo de Caixa

Fluxo de Caixa Projetado

Receitas

Despesas

Rateios

Custos

Comissões

Adiantamentos

Reembolsos

Empréstimos

Financiamentos

Parcelamentos

Aplicações Financeiras

Investimentos

Cobranças

Inadimplência

DRE Gerencial

Balancetes

Fechamentos

Auditoria

Dashboards

Indicadores

IA Financeira

Integrações

CRM

Comercial

Orçamentos

Compras

Estoque

Produção

PCP

Expedição

Instalação

Assistência Técnica

RH

Fiscal

Contabilidade

Workflow

Documentos

BI

IA

Estrutura Geral

FIN — Financeiro

├── Dashboard
├── Contas a Receber
├── Contas a Pagar
├── Caixa
├── Bancos
├── Conciliação Bancária
├── Fluxo de Caixa
├── Fluxo Projetado
├── Plano de Contas
├── Centros de Custo
├── Centros de Resultado
├── Receitas
├── Despesas
├── Cobranças
├── Inadimplência
├── Comissões
├── Rateios
├── Adiantamentos
├── Reembolsos
├── Empréstimos
├── Financiamentos
├── Aplicações
├── Investimentos
├── DRE
├── Indicadores
├── Relatórios
├── Auditoria
├── Configurações
└── IA Financeira

Observações

Multi-tenant.

Auditoria obrigatória.

Integração automática com os demais módulos.

Sem alterações financeiras sem rastreabilidade.

Próxima etapa

Detalhamento completo das páginas, dialogs, componentes, permissões,eventos, automações e regras do módulo Financeiro.
ETAPA 03-O
Catálogo Completo de Páginas
Recursos Humanos (RH)

Este módulo será responsável por toda a gestão de pessoas da empresa, integrando-se ao Financeiro, Produção, Agenda, Instalação e Segurança do Trabalho.

Ele contemplará, entre outros:

Dashboard RH
Colaboradores
Cadastro Completo do Funcionário
Cargos
Funções
Departamentos
Equipes
Organograma
Jornada de Trabalho
Escalas
Banco de Horas
Controle de Ponto
Férias
Afastamentos
Licenças
Horas Extras
Folha de Pagamento (integração)
Benefícios
Vale Transporte
Vale Alimentação
Plano de Saúde
Uniformes
EPIs
Treinamentos
Certificações
SST (Saúde e Segurança do Trabalho)
ASO
Exames Periódicos
Documentos
Advertências
Avaliações de Desempenho
Metas
Competências
Recrutamento
Processo Seletivo
Onboarding
Desligamentos
Histórico Funcional
Indicadores de RH
Relatórios
Configurações
IA para RH
Integrações
Financeiro
Produção
PCP
Instalação
Assistência Técnica
Agenda
Workflow
Documentos
BI
IA
# ETAPA 03-O

# Catálogo Completo de Páginas

# Recursos Humanos

## ID do Módulo

```text
RH
Objetivo

O módulo Recursos Humanos é responsável por administrar todo o ciclo de vida das pessoas que trabalham na empresa, desde o recrutamento até o desligamento.

Ele deverá centralizar informações funcionais, documentos, jornadas, escalas, ponto, férias, afastamentos, benefícios, treinamentos, segurança do trabalho, desempenho, remuneração, equipamentos entregues, equipes e histórico profissional.

O módulo deverá atender empresas industriais, marcenarias, prestadores de serviço, equipes administrativas, produção, montagem, instalação, assistência técnica, vendas, projetos e gestão.

Nenhum dado funcional relevante deverá permanecer apenas em planilhas, documentos externos ou registros informais.

Limites do Módulo

O módulo Recursos Humanos será responsável por:

Cadastrar colaboradores

Gerenciar contratos de trabalho

Gerenciar cargos e funções

Gerenciar departamentos e equipes

Gerenciar jornadas e escalas

Registrar ponto

Controlar banco de horas

Controlar horas extras

Controlar férias

Controlar afastamentos

Controlar benefícios

Controlar treinamentos

Controlar certificações

Controlar documentos

Controlar uniformes

Controlar EPIs

Controlar exames ocupacionais

Controlar avaliações de desempenho

Controlar recrutamento

Controlar onboarding

Controlar desligamentos

Gerar informações para folha de pagamento

Gerar indicadores de pessoas

O módulo Recursos Humanos não será responsável por:

Efetuar pagamentos diretamente

Emitir documentos fiscais

Substituir integralmente sistemas governamentais

Executar contabilização oficial

Modificar saldos financeiros diretamente

Modificar escalas produtivas sem integração com PCP e Produção

Essas responsabilidades pertencem aos módulos:

Financeiro

Fiscal

Contabilidade

PCP

Produção
Fluxo Principal
Necessidade de Contratação

↓

Requisição de Pessoal

↓

Recrutamento

↓

Seleção

↓

Proposta

↓

Admissão

↓

Onboarding

↓

Alocação em Cargo e Equipe

↓

Jornada e Escala

↓

Ponto e Frequência

↓

Treinamentos

↓

Avaliações

↓

Férias e Afastamentos

↓

Movimentações Funcionais

↓

Desligamento

↓

Encerramento do Vínculo

↓

Histórico Permanente
Estrutura Geral
RH — Recursos Humanos

├── Dashboard de RH
├── Central de Pessoas
├── Colaboradores
├── Cadastro do Colaborador
├── Dependentes
├── Contatos de Emergência
├── Cargos
├── Funções
├── Departamentos
├── Setores
├── Equipes
├── Organograma
├── Vínculos
├── Contratos de Trabalho
├── Movimentações Funcionais
├── Salários
├── Histórico Salarial
├── Jornadas
├── Escalas
├── Turnos
├── Calendários
├── Controle de Ponto
├── Marcações
├── Espelho de Ponto
├── Banco de Horas
├── Horas Extras
├── Atrasos
├── Faltas
├── Justificativas
├── Férias
├── Afastamentos
├── Licenças
├── Benefícios
├── Vale-Transporte
├── Vale-Alimentação
├── Plano de Saúde
├── Convênios
├── Folha de Pagamento
├── Eventos da Folha
├── Adiantamentos
├── Empréstimos Consignados
├── Reembolsos
├── Comissões
├── Bonificações
├── Descontos
├── Recrutamento
├── Vagas
├── Candidatos
├── Processos Seletivos
├── Entrevistas
├── Propostas
├── Admissões
├── Onboarding
├── Período de Experiência
├── Treinamentos
├── Certificações
├── Competências
├── Avaliações de Desempenho
├── Metas
├── Feedbacks
├── Plano de Desenvolvimento
├── Sucessão
├── Saúde Ocupacional
├── Segurança do Trabalho
├── ASO
├── Exames
├── Atestados
├── Acidentes
├── Incidentes
├── CAT
├── Riscos Ocupacionais
├── EPIs
├── Uniformes
├── Ferramentas Entregues
├── Equipamentos Entregues
├── Documentos
├── Advertências
├── Suspensões
├── Medidas Disciplinares
├── Comunicados
├── Pesquisas Internas
├── Clima Organizacional
├── Desligamentos
├── Entrevistas de Desligamento
├── Homologações
├── Rescisões
├── Histórico Funcional
├── Timeline
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
Página
Dashboard de RH
ID
RH-DAS-001
Tipo
Dashboard
Objetivo

Apresentar uma visão consolidada das pessoas, admissões, desligamentos, frequência, férias, treinamentos, documentos, saúde ocupacional e indicadores do quadro funcional.

Componentes
Total de Colaboradores

Colaboradores Ativos

Colaboradores Afastados

Colaboradores em Férias

Admissões no Período

Desligamentos no Período

Aniversariantes

Experiências Vencendo

Contratos Vencendo

Férias Vencidas

Férias Próximas

Documentos Pendentes

ASOs Vencendo

Treinamentos Vencendo

Certificações Vencendo

Faltas

Atrasos

Horas Extras

Saldo de Banco de Horas

Turnover

Absenteísmo

Custo de Pessoal

Distribuição por Departamento

Distribuição por Cargo

Alertas
Filtros
Período

Empresa

Filial

Departamento

Setor

Equipe

Cargo

Função

Gestor

Tipo de Vínculo

Status

Centro de Custo
Ações
Novo Colaborador

Nova Admissão

Nova Vaga

Registrar Afastamento

Programar Férias

Abrir Ponto

Abrir Documentos Pendentes

Abrir Treinamentos

Abrir Indicadores

Exportar Dashboard

Atualizar Dados
Página
Central de Pessoas
ID
RH-CEN-001
Tipo
Painel
Objetivo

Centralizar as principais operações diárias do RH.

Visualizações
Por Departamento

Por Setor

Por Equipe

Por Gestor

Por Status

Por Pendência

Por Vencimento

Por Unidade
Componentes
Admissões Pendentes

Documentos Pendentes

Férias Pendentes

Afastamentos Ativos

Ajustes de Ponto

Aprovações Pendentes

Treinamentos Pendentes

Avaliações Pendentes

Experiências Vencendo

Alertas Ocupacionais

Comunicados Recentes
Ações
Abrir Colaborador

Criar Pendência

Solicitar Documento

Solicitar Aprovação

Programar Férias

Registrar Afastamento

Agendar Exame

Agendar Treinamento

Enviar Comunicado
Página
Colaboradores
ID
RH-COL-001
Tipo
Lista
Objetivo

Listar, pesquisar, filtrar e administrar todos os colaboradores.

Visualizações
Tabela

Cards

Organograma

Mapa

Timeline
Colunas
Matrícula

Nome

Nome Social

CPF

Cargo

Função

Departamento

Setor

Equipe

Gestor

Data de Admissão

Tipo de Vínculo

Jornada

Status

Centro de Custo
Status
Pré-admissão

Ativo

Em Experiência

Em Férias

Afastado

Licenciado

Suspenso

Em Aviso Prévio

Desligado

Arquivado
Ações
Novo Colaborador

Abrir

Editar

Duplicar Cadastro

Inativar

Reativar

Transferir

Promover

Alterar Cargo

Alterar Função

Alterar Salário

Alterar Jornada

Alterar Equipe

Programar Férias

Registrar Afastamento

Registrar Advertência

Agendar Exame

Agendar Treinamento

Iniciar Desligamento

Exportar

Importar

Imprimir Ficha
Página
Cadastro do Colaborador
ID
RH-COL-002
Tipo
Cadastro
Objetivo

Centralizar todas as informações pessoais, funcionais, contratuais, financeiras, documentais e históricas do colaborador.

Abas
Geral

Dados Pessoais

Documentos

Contatos

Endereços

Dependentes

Emergência

Dados Bancários

Vínculo

Contrato

Cargo e Função

Departamento e Equipe

Jornada

Escala

Ponto

Banco de Horas

Salário

Benefícios

Comissões

Férias

Afastamentos

Saúde Ocupacional

EPIs

Uniformes

Ferramentas

Treinamentos

Certificações

Competências

Avaliações

Metas

Advertências

Documentos Funcionais

Anexos

Histórico

Timeline

Auditoria
Aba Geral

Campos:

Matrícula

Nome Completo

Nome Social

Foto

CPF

Status

Empresa

Filial

Departamento

Setor

Cargo

Função

Equipe

Gestor

Centro de Custo

Data de Admissão

Tipo de Vínculo

Data de Desligamento

Observações
Aba Dados Pessoais

Campos:

Data de Nascimento

Sexo Cadastral

Estado Civil

Nacionalidade

Naturalidade

Nome da Mãe

Nome do Pai

Escolaridade

Profissão

Pessoa com Deficiência

Tipo de Deficiência

Necessidades de Acessibilidade

Tipo Sanguíneo
Aba Documentos

Campos:

CPF

RG

Órgão Emissor

Data de Emissão

PIS/PASEP

Título de Eleitor

Zona Eleitoral

Seção Eleitoral

CNH

Categoria da CNH

Validade da CNH

Carteira de Trabalho

Série da Carteira

Certificado Militar

Passaporte

Registro Profissional
Aba Contatos

Campos:

Telefone Principal

Telefone Secundário

WhatsApp

Email Pessoal

Email Corporativo

Ramal

Preferência de Contato
Aba Endereços

Campos:

CEP

Logradouro

Número

Complemento

Bairro

Cidade

Estado

País

Referência

Coordenadas
Aba Dependentes

Campos:

Nome

CPF

Data de Nascimento

Parentesco

Dependente Financeiro

Dependente de Benefício

Plano de Saúde

Documentos

Status
Aba Emergência

Campos:

Nome

Parentesco

Telefone

WhatsApp

Endereço

Observações Médicas Autorizadas
Aba Dados Bancários

Campos:

Banco

Agência

Conta

Tipo de Conta

Chave PIX

Titular

CPF do Titular

Conta para Pagamento

Status
Aba Vínculo

Campos:

Tipo de Vínculo

Data de Admissão

Data de Registro

Data de Início

Data Prevista de Término

Empresa

Filial

Categoria

Sindicato

Regime

Status
Aba Contrato

Campos:

Número do Contrato

Tipo de Contrato

Data Inicial

Data Final

Período de Experiência

Primeira Prorrogação

Segunda Prorrogação

Carga Horária

Cláusulas

Documento Assinado

Status
Aba Cargo e Função

Campos:

Cargo

Função

Nível

Classe

Faixa Salarial

Descrição

Responsabilidades

Requisitos

Data de Início

Histórico
Aba Departamento e Equipe

Campos:

Departamento

Setor

Equipe

Gestor Direto

Gestor Substituto

Centro de Custo

Local de Trabalho

Posto de Trabalho
Aba Jornada

Campos:

Jornada

Carga Horária Diária

Carga Horária Semanal

Horário de Entrada

Horário de Saída

Intervalos

Tolerância

Banco de Horas

Controle de Ponto

Trabalho aos Sábados

Trabalho aos Domingos

Trabalho em Feriados
Aba Escala

Campos:

Escala

Data Inicial

Ciclo

Turno

Dias Trabalhados

Dias de Folga

Exceções

Substituições

Status
Aba Ponto

Informações:

Marcações

Ajustes

Justificativas

Faltas

Atrasos

Saídas Antecipadas

Horas Extras

Banco de Horas

Espelhos
Aba Salário

Informações:

Salário Base

Tipo de Salário

Valor Hora

Adicionais

Gratificações

Comissões

Bonificações

Descontos Fixos

Data da Última Alteração

Histórico Salarial
Aba Benefícios

Informações:

Benefício

Plano

Data Inicial

Data Final

Valor Empresa

Valor Colaborador

Dependentes

Status
Aba Saúde Ocupacional

Informações:

ASO Admissional

ASO Periódico

ASO de Retorno

ASO de Mudança de Risco

ASO Demissional

Exames

Restrições

Aptidão

Validade
Aba EPIs

Informações:

EPI

CA

Quantidade

Data de Entrega

Validade

Data de Devolução

Condição

Assinatura

Status
Aba Uniformes

Informações:

Item

Tamanho

Quantidade

Data de Entrega

Data de Devolução

Condição

Responsável
Aba Ferramentas

Informações:

Ferramenta

Código Patrimonial

Quantidade

Data de Entrega

Condição de Entrega

Data de Devolução

Condição de Devolução

Responsável
Aba Treinamentos

Informações:

Treinamento

Data

Carga Horária

Instrutor

Resultado

Certificado

Validade

Status
Aba Competências

Informações:

Competência

Nível Esperado

Nível Atual

Última Avaliação

Plano de Desenvolvimento

Status
Aba Avaliações

Informações:

Ciclo

Avaliador

Data

Nota

Resultado

Pontos Fortes

Pontos de Melhoria

Plano de Ação
Aba Advertências

Informações:

Tipo

Data

Motivo

Descrição

Responsável

Testemunhas

Documento

Assinatura

Status
Página
Dependentes
ID
RH-DEP-001
Tipo
Lista
Objetivo

Gerenciar dependentes legais, financeiros e vinculados a benefícios.

Ações
Novo Dependente

Editar

Adicionar Documento

Vincular Benefício

Inativar

Reativar

Exportar
Página
Contatos de Emergência
ID
RH-EME-001
Tipo
Lista
Objetivo

Centralizar contatos que poderão ser acionados em emergências.

Página
Cargos
ID
RH-CAR-001
Tipo
Lista
Objetivo

Cadastrar os cargos existentes na estrutura organizacional.

Campos
Código

Nome

Descrição

Departamento

Nível

Faixa Salarial

Responsabilidades

Requisitos

Competências

Riscos Ocupacionais

Status
Ações
Novo Cargo

Editar

Duplicar

Versionar

Vincular Funções

Vincular Competências

Vincular Treinamentos

Inativar

Arquivar
Página
Funções
ID
RH-FUN-001
Tipo
Lista
Objetivo

Cadastrar atividades efetivamente exercidas pelos colaboradores.

Exemplos
Marceneiro

Montador

Projetista

Orçamentista

Operador de Serra

Operador de CNC

Fitador

Instalador

Auxiliar de Produção

Comprador

Vendedor

Financeiro

Administrativo
Página
Departamentos
ID
RH-DPT-001
Tipo
Lista
Objetivo

Organizar a estrutura administrativa da empresa.

Exemplos
Direção

Comercial

Projetos

Compras

Estoque

PCP

Produção

Qualidade

Expedição

Instalação

Assistência Técnica

Financeiro

Fiscal

Recursos Humanos

Administrativo
Página
Setores
ID
RH-SET-001
Tipo
Lista
Objetivo

Representar subdivisões operacionais dos departamentos.

Página
Equipes
ID
RH-EQP-001
Tipo
Lista
Objetivo

Organizar grupos de colaboradores que atuam em conjunto.

Campos
Nome

Departamento

Setor

Líder

Integrantes

Turno

Capacidade

Habilidades

Status
Página
Organograma
ID
RH-ORG-001
Tipo
Árvore
Objetivo

Representar visualmente a hierarquia da empresa.

Visualizações
Por Empresa

Por Filial

Por Departamento

Por Gestor

Por Cargo

Por Equipe
Ações
Abrir Colaborador

Abrir Cargo

Abrir Departamento

Alterar Gestor

Exportar Organograma

Imprimir
Página
Vínculos
ID
RH-VIN-001
Tipo
Lista
Objetivo

Controlar os tipos de relação profissional mantidos com a empresa.

Tipos
CLT

Aprendiz

Estagiário

Temporário

Autônomo

Prestador

Sócio

Terceirizado

Cooperado
Página
Contratos de Trabalho
ID
RH-CTR-001
Tipo
Lista
Objetivo

Gerenciar contratos, aditivos, prorrogações e encerramentos.

Status
Rascunho

Aguardando Assinatura

Ativo

Em Experiência

Próximo do Vencimento

Vencido

Suspenso

Encerrado

Cancelado
Ações
Novo Contrato

Gerar Documento

Enviar para Assinatura

Prorrogar

Criar Aditivo

Suspender

Encerrar

Cancelar

Exportar
Página
Movimentações Funcionais
ID
RH-MOV-001
Tipo
Timeline
Objetivo

Registrar alterações relevantes na vida funcional do colaborador.

Tipos
Admissão

Promoção

Transferência

Alteração de Cargo

Alteração de Função

Alteração de Salário

Alteração de Jornada

Alteração de Equipe

Alteração de Gestor

Afastamento

Retorno

Férias

Suspensão

Desligamento
Página
Salários
ID
RH-SAL-001
Tipo
Lista
Objetivo

Administrar salários atuais, faixas e alterações autorizadas.

Ações
Alterar Salário

Aplicar Reajuste

Aplicar Dissídio

Simular Alteração

Solicitar Aprovação

Aprovar

Gerar Aditivo

Exportar
Página
Histórico Salarial
ID
RH-HSA-001
Tipo
Timeline
Objetivo

Preservar todas as alterações de remuneração.

Página
Jornadas
ID
RH-JOR-001
Tipo
Lista
Objetivo

Cadastrar regras de carga horária e horários de trabalho.

Campos
Nome

Carga Diária

Carga Semanal

Entrada

Saída

Intervalos

Tolerância

Banco de Horas

Horas Extras Permitidas

Adicional Noturno

Status
Página
Escalas
ID
RH-ESC-001
Tipo
Calendário
Objetivo

Planejar jornadas alternadas, folgas, plantões e turnos.

Exemplos
5x2

6x1

12x36

Segunda a Sexta

Escala Personalizada

Turno Fixo

Turno Alternado
Regras

Alterações deverão ocorrer por edição controlada.

Não deverá ser utilizado drag and drop para alterar escalas confirmadas.

Página
Turnos
ID
RH-TUR-001
Tipo
Lista
Objetivo

Definir períodos de trabalho vinculados às jornadas e equipes.

Página
Calendários
ID
RH-CAL-001
Tipo
Calendário
Objetivo

Controlar dias úteis, feriados, recessos e exceções.

Página
Controle de Ponto
ID
RH-PON-001
Tipo
Dashboard Analítico
Objetivo

Registrar, calcular e acompanhar a frequência dos colaboradores.

Componentes
Marcações do Dia

Colaboradores sem Marcação

Atrasos

Saídas Antecipadas

Faltas

Horas Extras

Banco de Horas

Ajustes Pendentes

Espelhos Pendentes

Alertas
Ações
Registrar Marcação Manual

Importar Marcações

Solicitar Ajuste

Aprovar Ajuste

Fechar Período

Reabrir Período

Gerar Espelho

Exportar para Folha
Página
Marcações
ID
RH-MAR-001
Tipo
Lista
Objetivo

Consultar e administrar registros de entrada, saída e intervalos.

Campos
Colaborador

Data

Hora

Tipo

Origem

Dispositivo

Localização

Foto

Observação

Status
Origens
Relógio de Ponto

Aplicativo

Desktop

Portal

Importação

Registro Manual

Integração
Página
Espelho de Ponto
ID
RH-EPT-001
Tipo
Relatório
Objetivo

Apresentar a apuração consolidada da jornada por período.

Informações
Jornada Prevista

Horas Trabalhadas

Horas Extras

Atrasos

Faltas

Intervalos

Adicional Noturno

Banco de Horas

Justificativas

Assinaturas
Página
Banco de Horas
ID
RH-BHO-001
Tipo
Dashboard Analítico
Objetivo

Controlar créditos, débitos, compensações e vencimentos.

Ações
Consultar Saldo

Lançar Ajuste

Compensar Horas

Programar Folga

Solicitar Aprovação

Aprovar

Exportar
Página
Horas Extras
ID
RH-HEX-001
Tipo
Lista
Objetivo

Controlar horas extraordinárias realizadas ou programadas.

Status
Planejada

Solicitada

Aprovada

Realizada

Apurada

Paga

Compensada

Rejeitada

Cancelada
Página
Atrasos
ID
RH-ATR-001
Tipo
Lista
Objetivo

Registrar e analisar atrasos.

Página
Faltas
ID
RH-FAL-001
Tipo
Lista
Objetivo

Registrar faltas justificadas e injustificadas.

Página
Justificativas
ID
RH-JUS-001
Tipo
Lista
Objetivo

Analisar justificativas de ponto, atrasos, faltas e saídas.

Status
Rascunho

Enviada

Em Análise

Aprovada

Rejeitada

Cancelada
Página
Férias
ID
RH-FER-001
Tipo
Calendário
Objetivo

Planejar, solicitar, aprovar e acompanhar férias.

Informações
Colaborador

Período Aquisitivo

Dias Disponíveis

Dias Programados

Abono Pecuniário

Adiantamento

Data Inicial

Data Final

Retorno

Substituto

Status
Status
Disponível

Planejada

Solicitada

Aguardando Aprovação

Aprovada

Programada

Em Gozo

Concluída

Cancelada
Ações
Programar Férias

Solicitar

Aprovar

Rejeitar

Alterar Período

Cancelar

Gerar Aviso

Gerar Recibo

Registrar Retorno
Página
Afastamentos
ID
RH-AFA-001
Tipo
Lista
Objetivo

Controlar afastamentos temporários.

Tipos
Doença

Acidente

Licença Maternidade

Licença Paternidade

Serviço Militar

Suspensão

Afastamento Previdenciário

Outros
Página
Licenças
ID
RH-LIC-001
Tipo
Lista
Objetivo

Controlar licenças legais, contratuais ou internas.

Página
Benefícios
ID
RH-BEN-001
Tipo
Lista
Objetivo

Administrar benefícios fornecidos aos colaboradores.

Exemplos
Vale-Transporte

Vale-Alimentação

Vale-Refeição

Plano de Saúde

Plano Odontológico

Seguro de Vida

Auxílio Educação

Auxílio Combustível

Cesta Básica

Convênios
Página
Vale-Transporte
ID
RH-VTR-001
Tipo
Lista
Objetivo

Controlar rotas, valores, descontos e recargas.

Página
Vale-Alimentação
ID
RH-VAL-001
Tipo
Lista
Objetivo

Controlar valores, operadoras, créditos e descontos.

Página
Plano de Saúde
ID
RH-PLS-001
Tipo
Lista
Objetivo

Gerenciar planos de saúde de colaboradores e dependentes.

Página
Convênios
ID
RH-CNV-001
Tipo
Lista
Objetivo

Gerenciar benefícios e parcerias complementares.

Página
Folha de Pagamento
ID
RH-FOL-001
Tipo
Dashboard Analítico
Objetivo

Consolidar eventos e informações que serão enviados ao processo de folha.

Componentes
Colaboradores no Período

Salários

Horas Extras

Faltas

Atrasos

Adicionais

Comissões

Bonificações

Benefícios

Descontos

Adiantamentos

Afastamentos

Férias

Rescisões

Pendências
Ações
Abrir Período

Importar Eventos

Calcular Prévia

Validar

Solicitar Aprovação

Aprovar

Exportar para Folha

Fechar Período

Reabrir Período
Observação

O ORGANIZEG3 poderá preparar e consolidar informações para folha, mas a execução legal completa poderá ocorrer por integração com sistema especializado ou contabilidade.

Página
Eventos da Folha
ID
RH-EFO-001
Tipo
Lista
Objetivo

Cadastrar eventos que compõem proventos e descontos.

Tipos
Provento

Desconto

Informativo

Base de Cálculo

Encargo

Benefício
Página
Adiantamentos
ID
RH-ADI-001
Tipo
Lista
Objetivo

Controlar adiantamentos salariais e extraordinários.

Página
Empréstimos Consignados
ID
RH-EMP-001
Tipo
Lista
Objetivo

Controlar parcelas e descontos de empréstimos consignados.

Página
Reembolsos
ID
RH-REE-001
Tipo
Lista
Objetivo

Controlar despesas reembolsáveis de colaboradores.

Página
Comissões
ID
RH-COM-001
Tipo
Dashboard Analítico
Objetivo

Consultar e validar comissões originadas nos módulos Comercial, Produção, Instalação e Assistência Técnica.

Página
Bonificações
ID
RH-BON-001
Tipo
Lista
Objetivo

Administrar premiações e bonificações.

Página
Descontos
ID
RH-DES-001
Tipo
Lista
Objetivo

Controlar descontos autorizados ou legais.

Página
Recrutamento
ID
RH-REC-001
Tipo
Dashboard
Objetivo

Centralizar vagas, candidatos, etapas e indicadores de recrutamento.

Componentes
Vagas Abertas

Vagas Urgentes

Candidatos Ativos

Entrevistas Agendadas

Propostas Pendentes

Tempo Médio de Contratação

Origem dos Candidatos

Taxa de Conversão
Página
Vagas
ID
RH-VAG-001
Tipo
Lista
Objetivo

Cadastrar necessidades de contratação.

Campos
Título

Cargo

Função

Departamento

Gestor

Quantidade

Tipo de Vínculo

Local

Salário

Benefícios

Requisitos

Competências

Data de Abertura

Prazo

Responsável

Status
Status
Rascunho

Aguardando Aprovação

Aprovada

Publicada

Em Seleção

Pausada

Preenchida

Cancelada

Encerrada
Página
Candidatos
ID
RH-CAN-001
Tipo
Lista
Objetivo

Cadastrar e acompanhar candidatos.

Informações
Nome

Contato

Currículo

Pretensão Salarial

Disponibilidade

Experiência

Formação

Competências

Origem

LGPD

Status
Página
Processos Seletivos
ID
RH-SEL-001
Tipo
Kanban
Objetivo

Controlar as etapas de seleção.

Etapas
Inscrito

Triagem

Contato Inicial

Entrevista RH

Entrevista Gestor

Teste

Avaliação Prática

Referências

Proposta

Aprovado

Reprovado

Banco de Talentos
Página
Entrevistas
ID
RH-ENT-001
Tipo
Calendário
Objetivo

Agendar e registrar entrevistas.

Página
Propostas
ID
RH-PRO-001
Tipo
Lista
Objetivo

Gerenciar propostas de contratação.

Status
Rascunho

Aguardando Aprovação

Aprovada

Enviada

Visualizada

Aceita

Recusada

Expirada

Cancelada
Página
Admissões
ID
RH-ADM-001
Tipo
Kanban
Objetivo

Controlar todas as etapas necessárias para efetivar uma admissão.

Etapas
Aprovado

Documentos Solicitados

Documentos Recebidos

Exame Admissional

Cadastro em Andamento

Contrato Gerado

Aguardando Assinatura

Integração Agendada

Admitido
Checklist
Documentos Pessoais

Dados Bancários

Endereço

Dependentes

Exame Admissional

Contrato

Ficha de Registro

Benefícios

Jornada

Escala

EPI

Uniforme

Treinamentos Iniciais

Acessos

Equipamentos
Página
Onboarding
ID
RH-ONB-001
Tipo
Kanban
Objetivo

Planejar e acompanhar a integração de novos colaboradores.

Etapas
Pré-Onboarding

Primeiro Dia

Primeira Semana

Primeiro Mês

Período de Experiência

Integração Concluída
Atividades
Apresentação da Empresa

Apresentação da Equipe

Políticas Internas

Segurança

Treinamentos

Entrega de Equipamentos

Criação de Acessos

Definição de Metas

Acompanhamento do Gestor
Página
Período de Experiência
ID
RH-PEX-001
Tipo
Timeline
Objetivo

Controlar avaliações e vencimentos do contrato de experiência.

Página
Treinamentos
ID
RH-TRE-001
Tipo
Lista
Objetivo

Planejar, executar e registrar treinamentos internos e externos.

Tipos
Integração

Segurança

Operacional

Técnico

Comportamental

Liderança

Qualidade

Obrigatório

Reciclagem
Status
Planejado

Agendado

Inscrições Abertas

Em Andamento

Concluído

Cancelado
Página
Certificações
ID
RH-CER-001
Tipo
Lista
Objetivo

Controlar certificados, autorizações e vencimentos.

Página
Competências
ID
RH-CMP-001
Tipo
Lista
Objetivo

Cadastrar conhecimentos, habilidades e atitudes relevantes.

Categorias
Técnica

Operacional

Comportamental

Liderança

Segurança

Qualidade

Digital

Comercial
Página
Avaliações de Desempenho
ID
RH-AVA-001
Tipo
Dashboard Analítico
Objetivo

Criar ciclos de avaliação e acompanhar resultados.

Tipos
90 Graus

180 Graus

360 Graus

Período de Experiência

Avaliação Técnica

Avaliação por Competências

Avaliação por Metas
Página
Metas
ID
RH-MET-001
Tipo
Lista
Objetivo

Definir e acompanhar metas individuais e de equipe.

Página
Feedbacks
ID
RH-FEE-001
Tipo
Timeline
Objetivo

Registrar feedbacks formais e acompanhamentos.

Página
Plano de Desenvolvimento
ID
RH-PDI-001
Tipo
Kanban
Objetivo

Controlar ações de desenvolvimento individuais.

Página
Sucessão
ID
RH-SUC-001
Tipo
Dashboard Analítico
Objetivo

Mapear posições críticas e possíveis sucessores.

Página
Saúde Ocupacional
ID
RH-SAO-001
Tipo
Dashboard
Objetivo

Centralizar exames, ASOs, atestados, restrições e vencimentos ocupacionais.

Página
Segurança do Trabalho
ID
RH-SST-001
Tipo
Dashboard
Objetivo

Gerenciar informações de saúde e segurança relacionadas ao trabalho.

Componentes
ASOs Vencendo

Treinamentos Obrigatórios

EPIs Pendentes

Acidentes

Incidentes

CATs

Riscos

Ações Pendentes

Alertas
Página
ASO
ID
RH-ASO-001
Tipo
Lista
Objetivo

Controlar Atestados de Saúde Ocupacional.

Tipos
Admissional

Periódico

Retorno ao Trabalho

Mudança de Risco

Demissional
Status
A Agendar

Agendado

Realizado

Apto

Apto com Restrição

Inapto

Vencido

Cancelado
Página
Exames
ID
RH-EXA-001
Tipo
Lista
Objetivo

Controlar exames clínicos e complementares.

Página
Atestados
ID
RH-ATE-001
Tipo
Lista
Objetivo

Registrar atestados e seus efeitos na frequência.

Página
Acidentes
ID
RH-ACI-001
Tipo
Kanban
Objetivo

Registrar e acompanhar acidentes de trabalho.

Informações
Data

Hora

Local

Colaborador

Atividade

Descrição

Lesão

Testemunhas

Atendimento

Afastamento

Causa

Ação Imediata

Evidências

Status
Página
Incidentes
ID
RH-INC-001
Tipo
Kanban
Objetivo

Registrar ocorrências sem lesão que poderiam causar acidentes.

Página
CAT
ID
RH-CAT-001
Tipo
Lista
Objetivo

Controlar Comunicações de Acidente de Trabalho.

Página
Riscos Ocupacionais
ID
RH-RIS-001
Tipo
Lista
Objetivo

Mapear riscos por cargo, função, ambiente e atividade.

Categorias
Físico

Químico

Biológico

Ergonômico

Acidente
Página
EPIs
ID
RH-EPI-001
Tipo
Lista
Objetivo

Gerenciar catálogo, estoque lógico, entregas, substituições e devoluções de EPIs.

Campos
EPI

CA

Fabricante

Validade

Cargo

Função

Risco

Periodicidade

Quantidade

Status
Ações
Cadastrar EPI

Entregar

Substituir

Devolver

Registrar Perda

Registrar Recusa

Coletar Assinatura

Gerar Ficha

Exportar
Página
Uniformes
ID
RH-UNI-001
Tipo
Lista
Objetivo

Controlar entregas, tamanhos, reposições e devoluções de uniformes.

Página
Ferramentas Entregues
ID
RH-FET-001
Tipo
Lista
Objetivo

Rastrear ferramentas sob responsabilidade dos colaboradores.

Página
Equipamentos Entregues
ID
RH-EET-001
Tipo
Lista
Objetivo

Rastrear notebooks, celulares, tablets, chaves, crachás e outros ativos entregues.

Página
Documentos
ID
RH-DOC-001
Tipo
Gerenciador de Arquivos
Objetivo

Centralizar documentos pessoais, contratuais, médicos, funcionais e disciplinares.

Categorias
Pessoais

Admissionais

Contratuais

Benefícios

Férias

Afastamentos

Saúde Ocupacional

Treinamentos

Avaliações

Disciplinares

Desligamento
Página
Advertências
ID
RH-ADV-001
Tipo
Lista
Objetivo

Registrar advertências verbais e escritas.

Página
Suspensões
ID
RH-SUS-001
Tipo
Lista
Objetivo

Registrar suspensões disciplinares.

Página
Medidas Disciplinares
ID
RH-MDI-001
Tipo
Timeline
Objetivo

Preservar o histórico de ações disciplinares.

Página
Comunicados
ID
RH-COM-002
Tipo
Lista
Objetivo

Criar e distribuir comunicados internos.

Públicos
Todos

Empresa

Filial

Departamento

Setor

Equipe

Cargo

Colaboradores Selecionados
Página
Pesquisas Internas
ID
RH-PES-001
Tipo
Lista
Objetivo

Criar pesquisas internas e acompanhar respostas.

Página
Clima Organizacional
ID
RH-CLI-001
Tipo
Dashboard Analítico
Objetivo

Avaliar satisfação, engajamento e percepção dos colaboradores.

Página
Desligamentos
ID
RH-DES-002
Tipo
Kanban
Objetivo

Controlar todas as etapas do desligamento.

Etapas
Solicitado

Aguardando Aprovação

Aprovado

Aviso Prévio

Documentos em Preparação

Devoluções Pendentes

Entrevista Agendada

Rescisão Calculada

Aguardando Assinatura

Concluído
Checklist
Aprovação

Aviso Prévio

Exame Demissional

Devolução de EPIs

Devolução de Uniformes

Devolução de Ferramentas

Devolução de Equipamentos

Bloqueio de Acessos

Rescisão

Documentos

Entrevista de Desligamento

Assinaturas
Página
Entrevistas de Desligamento
ID
RH-EDL-001
Tipo
Lista
Objetivo

Registrar motivos, percepções e feedbacks do colaborador desligado.

Página
Homologações
ID
RH-HOM-001
Tipo
Lista
Objetivo

Controlar formalizações e assinaturas relacionadas ao desligamento.

Página
Rescisões
ID
RH-RES-001
Tipo
Lista
Objetivo

Consolidar dados e eventos necessários à rescisão.

Página
Histórico Funcional
ID
RH-HIS-001
Tipo
Consulta
Objetivo

Consultar todo o histórico do colaborador.

Página
Timeline
ID
RH-TML-001
Tipo
Timeline
Objetivo

Apresentar acontecimentos funcionais em ordem cronológica.

Eventos
Candidato Cadastrado

Admissão Iniciada

Colaborador Admitido

Contrato Assinado

Cargo Alterado

Salário Alterado

Equipe Alterada

Treinamento Concluído

Férias Programadas

Afastamento Registrado

Advertência Aplicada

Avaliação Concluída

Promoção Registrada

Desligamento Iniciado

Colaborador Desligado
Página
Indicadores
ID
RH-KPI-001
Tipo
Dashboard Analítico
Indicadores
Headcount

Admissões

Desligamentos

Turnover

Absenteísmo

Horas Extras

Banco de Horas

Faltas

Atrasos

Custo de Pessoal

Custo por Departamento

Custo por Colaborador

Tempo Médio de Contratação

Vagas em Aberto

Taxa de Aprovação de Candidatos

Férias Vencidas

Treinamentos Pendentes

Avaliações Concluídas

Acidentes

Incidentes

Satisfação Interna

Distribuição por Cargo

Distribuição por Faixa Salarial

Tempo Médio de Empresa
Página
Relatórios
ID
RH-REL-001
Tipo
Relatório
Relatórios Disponíveis
Quadro de Colaboradores

Colaboradores por Departamento

Colaboradores por Cargo

Colaboradores por Equipe

Admissões

Desligamentos

Aniversariantes

Contratos Vencendo

Experiências Vencendo

Férias

Afastamentos

Ponto

Horas Extras

Banco de Horas

Faltas

Atrasos

Benefícios

Folha de Pagamento

Comissões

Treinamentos

Certificações

Avaliações

Competências

ASOs

Exames

Atestados

Acidentes

Incidentes

EPIs

Uniformes

Ferramentas

Equipamentos

Advertências

Turnover

Absenteísmo

Custo de Pessoal
Página
Templates
ID
RH-TMP-001
Tipo
Configuração
Objetivo

Criar modelos reutilizáveis de documentos e processos.

Tipos
Contrato

Aditivo

Ficha de Registro

Aviso de Férias

Recibo

Advertência

Suspensão

Comunicado

Avaliação

PDI

Checklist de Admissão

Checklist de Onboarding

Checklist de Desligamento

Termo de Entrega de EPI

Termo de Entrega de Equipamento
Página
Configurações
ID
RH-CFG-001
Tipo
Configuração
Configurações
Numeração de Matrículas

Tipos de Vínculo

Cargos

Funções

Departamentos

Setores

Equipes

Jornadas

Escalas

Turnos

Calendários

Tolerâncias de Ponto

Banco de Horas

Horas Extras

Férias

Afastamentos

Benefícios

Eventos da Folha

Competências

Avaliações

Treinamentos

Riscos Ocupacionais

EPIs

Tipos de Advertência

Motivos de Desligamento

Templates

Checklists

Notificações

Integrações
Dialogs
RH-DLG-001 Novo Colaborador

RH-DLG-002 Editar Colaborador

RH-DLG-003 Selecionar Cargo

RH-DLG-004 Selecionar Função

RH-DLG-005 Selecionar Departamento

RH-DLG-006 Selecionar Equipe

RH-DLG-007 Alterar Gestor

RH-DLG-008 Alterar Cargo

RH-DLG-009 Alterar Função

RH-DLG-010 Alterar Salário

RH-DLG-011 Alterar Jornada

RH-DLG-012 Transferir Colaborador

RH-DLG-013 Novo Dependente

RH-DLG-014 Novo Contrato

RH-DLG-015 Gerar Aditivo

RH-DLG-016 Registrar Marcação

RH-DLG-017 Solicitar Ajuste de Ponto

RH-DLG-018 Aprovar Ajuste

RH-DLG-019 Registrar Justificativa

RH-DLG-020 Programar Férias

RH-DLG-021 Aprovar Férias

RH-DLG-022 Registrar Afastamento

RH-DLG-023 Registrar Atestado

RH-DLG-024 Adicionar Benefício

RH-DLG-025 Registrar Adiantamento

RH-DLG-026 Nova Vaga

RH-DLG-027 Novo Candidato

RH-DLG-028 Agendar Entrevista

RH-DLG-029 Registrar Avaliação de Candidato

RH-DLG-030 Enviar Proposta

RH-DLG-031 Iniciar Admissão

RH-DLG-032 Solicitar Documentos

RH-DLG-033 Agendar Exame

RH-DLG-034 Criar Onboarding

RH-DLG-035 Novo Treinamento

RH-DLG-036 Registrar Certificação

RH-DLG-037 Nova Avaliação de Desempenho

RH-DLG-038 Registrar Feedback

RH-DLG-039 Criar PDI

RH-DLG-040 Entregar EPI

RH-DLG-041 Entregar Uniforme

RH-DLG-042 Entregar Ferramenta

RH-DLG-043 Entregar Equipamento

RH-DLG-044 Registrar Advertência

RH-DLG-045 Registrar Suspensão

RH-DLG-046 Novo Comunicado

RH-DLG-047 Iniciar Desligamento

RH-DLG-048 Registrar Entrevista de Desligamento

RH-DLG-049 Concluir Desligamento

RH-DLG-050 Exportar Dados de RH
Wizards
RH-WIZ-001 Assistente de Novo Colaborador

RH-WIZ-002 Assistente de Admissão

RH-WIZ-003 Assistente de Onboarding

RH-WIZ-004 Assistente de Jornada e Escala

RH-WIZ-005 Assistente de Fechamento de Ponto

RH-WIZ-006 Assistente de Férias

RH-WIZ-007 Assistente de Afastamento

RH-WIZ-008 Assistente de Benefícios

RH-WIZ-009 Assistente de Folha

RH-WIZ-010 Assistente de Recrutamento

RH-WIZ-011 Assistente de Processo Seletivo

RH-WIZ-012 Assistente de Treinamento

RH-WIZ-013 Assistente de Avaliação

RH-WIZ-014 Assistente de Saúde Ocupacional

RH-WIZ-015 Assistente de Entrega de EPI

RH-WIZ-016 Assistente de Desligamento
Componentes Específicos
RH-CPT-001 Ficha do Colaborador

RH-CPT-002 Organograma Interativo

RH-CPT-003 Calendário de Férias

RH-CPT-004 Calendário de Escalas

RH-CPT-005 Painel de Ponto

RH-CPT-006 Editor de Marcações

RH-CPT-007 Espelho de Ponto

RH-CPT-008 Indicador de Banco de Horas

RH-CPT-009 Simulador de Férias

RH-CPT-010 Painel de Folha

RH-CPT-011 Kanban de Recrutamento

RH-CPT-012 Perfil do Candidato

RH-CPT-013 Checklist de Admissão

RH-CPT-014 Checklist de Onboarding

RH-CPT-015 Matriz de Competências

RH-CPT-016 Editor de Avaliação

RH-CPT-017 Painel de PDI

RH-CPT-018 Painel de Saúde Ocupacional

RH-CPT-019 Gerenciador de EPIs

RH-CPT-020 Checklist de Desligamento

RH-CPT-021 Timeline Funcional

RH-CPT-022 Gerador de Documentos

RH-CPT-023 Captura de Assinatura

RH-CPT-024 Painel de Indicadores de RH

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo theme_design.

Nenhum componente poderá conter aparência hardcoded.

Eventos
EmployeeCandidateCreated

EmployeeVacancyCreated

EmployeeSelectionStarted

EmployeeProposalSent

EmployeeProposalAccepted

EmployeeAdmissionStarted

EmployeeCreated

EmployeeContractCreated

EmployeeContractSigned

EmployeeOnboardingStarted

EmployeeOnboardingCompleted

EmployeePositionChanged

EmployeeRoleChanged

EmployeeDepartmentChanged

EmployeeTeamChanged

EmployeeManagerChanged

EmployeeSalaryChanged

EmployeeScheduleChanged

EmployeeTimeEntryCreated

EmployeeTimeAdjustmentRequested

EmployeeTimeAdjustmentApproved

EmployeeOvertimeRegistered

EmployeeLeaveRequested

EmployeeLeaveApproved

EmployeeVacationScheduled

EmployeeVacationStarted

EmployeeVacationCompleted

EmployeeAbsenceCreated

EmployeeBenefitAdded

EmployeePayrollPeriodOpened

EmployeePayrollPeriodClosed

EmployeeTrainingAssigned

EmployeeTrainingCompleted

EmployeeCertificationCreated

EmployeePerformanceReviewCreated

EmployeePerformanceReviewCompleted

EmployeeDevelopmentPlanCreated

EmployeeMedicalExamScheduled

EmployeeMedicalExamCompleted

EmployeePPEDelivered

EmployeeUniformDelivered

EmployeeToolDelivered

EmployeeEquipmentDelivered

EmployeeWarningRegistered

EmployeeSuspensionRegistered

EmployeeAccidentRegistered

EmployeeDismissalStarted

EmployeeDismissalCompleted
Automações
Candidato aprovado

↓

Criar processo de admissão

↓

Solicitar documentos

↓

Agendar exame admissional

↓

Criar checklist
Colaborador admitido

↓

Criar matrícula

↓

Criar contrato

↓

Vincular cargo e equipe

↓

Criar acessos

↓

Criar onboarding

↓

Notificar gestor
Experiência próxima do vencimento

↓

Criar avaliação

↓

Notificar gestor

↓

Solicitar decisão
Férias próximas do vencimento

↓

Gerar alerta

↓

Notificar RH e gestor

↓

Sugerir períodos disponíveis
Marcação inconsistente

↓

Criar pendência

↓

Notificar colaborador

↓

Solicitar justificativa
ASO próximo do vencimento

↓

Criar alerta

↓

Sugerir agendamento

↓

Notificar RH
Treinamento obrigatório vencendo

↓

Criar convocação

↓

Reservar agenda

↓

Notificar colaborador e gestor
Desligamento iniciado

↓

Criar checklist

↓

Agendar exame demissional

↓

Solicitar devoluções

↓

Bloquear acessos na data definida

↓

Preparar eventos rescisórios
Integrações
Administração

Financeiro

Fiscal

Contabilidade

CRM

Comercial

Projetos

Compras

Estoque

PCP

Produção

Qualidade

Expedição

Instalação

Assistência Técnica

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Email

WhatsApp

Assinatura Digital

Relógio de Ponto

Portal do Colaborador
Permissões
hr.dashboard.read

hr.central.read

hr.employee.read

hr.employee.create

hr.employee.update

hr.employee.archive

hr.employee.personal_data.read

hr.employee.sensitive_data.read

hr.employee.bank_data.read

hr.employee.bank_data.update

hr.employee.document.manage

hr.employee.dependent.manage

hr.employee.contract.read

hr.employee.contract.create

hr.employee.contract.update

hr.employee.contract.terminate

hr.employee.position.change

hr.employee.role.change

hr.employee.department.change

hr.employee.team.change

hr.employee.manager.change

hr.employee.salary.read

hr.employee.salary.update

hr.employee.salary.approve

hr.employee.schedule.read

hr.employee.schedule.manage

hr.time.read

hr.time.entry.create

hr.time.entry.adjust

hr.time.adjustment.approve

hr.time.period.close

hr.time.period.reopen

hr.overtime.read

hr.overtime.request

hr.overtime.approve

hr.vacation.read

hr.vacation.request

hr.vacation.approve

hr.vacation.cancel

hr.absence.read

hr.absence.create

hr.leave.manage

hr.benefit.read

hr.benefit.manage

hr.payroll.read

hr.payroll.prepare

hr.payroll.approve

hr.payroll.export

hr.recruitment.read

hr.recruitment.manage

hr.vacancy.create

hr.vacancy.approve

hr.candidate.read

hr.candidate.manage

hr.interview.manage

hr.proposal.create

hr.proposal.approve

hr.admission.manage

hr.onboarding.manage

hr.training.read

hr.training.manage

hr.certification.manage

hr.competency.manage

hr.performance.read

hr.performance.manage

hr.goal.manage

hr.feedback.manage

hr.development_plan.manage

hr.occupational_health.read

hr.occupational_health.manage

hr.medical_exam.read

hr.medical_exam.manage

hr.accident.read

hr.accident.manage

hr.incident.manage

hr.ppe.read

hr.ppe.manage

hr.uniform.manage

hr.tool_delivery.manage

hr.equipment_delivery.manage

hr.warning.read

hr.warning.create

hr.suspension.create

hr.communication.manage

hr.survey.manage

hr.dismissal.read

hr.dismissal.start

hr.dismissal.approve

hr.dismissal.complete

hr.report.read

hr.report.export

hr.configuration.manage
Relatórios e Documentos Gerados
Ficha do Colaborador

Ficha de Registro

Contrato de Trabalho

Aditivo Contratual

Termo de Experiência

Termo de Alteração Salarial

Termo de Alteração de Cargo

Aviso de Férias

Recibo de Férias

Espelho de Ponto

Relatório de Banco de Horas

Relatório de Horas Extras

Relatório de Faltas

Relatório de Afastamentos

Ficha de Benefícios

Prévia da Folha

Relatório de Comissões

Ficha de Candidato

Relatório de Processo Seletivo

Proposta de Contratação

Checklist de Admissão

Checklist de Onboarding

Certificado de Treinamento

Avaliação de Desempenho

Plano de Desenvolvimento

Ficha de EPI

Termo de Entrega de Uniforme

Termo de Entrega de Ferramenta

Termo de Entrega de Equipamento

Advertência

Suspensão

Relatório de Acidente

Relatório de Incidente

Checklist de Desligamento

Entrevista de Desligamento

Termo de Rescisão

Histórico Funcional
Recursos de Inteligência Artificial
Classificar currículos

Extrair dados de currículos

Comparar candidatos com vagas

Sugerir perguntas de entrevista

Resumir entrevistas

Sugerir plano de onboarding

Detectar documentos faltantes

Prever vencimentos

Analisar padrões de ausência

Detectar risco de turnover

Sugerir treinamentos

Identificar lacunas de competência

Resumir avaliações

Sugerir plano de desenvolvimento

Analisar clima organizacional

Classificar feedbacks

Analisar causas de desligamento

Gerar comunicados

Gerar descrições de cargos

Pesquisar informações de RH em linguagem natural

A IA nunca poderá contratar, demitir, aplicar advertência, alterar salário, aprovar férias, classificar definitivamente desempenho ou acessar dados sensíveis sem autorização e confirmação explícita de um usuário autorizado.

Regras Funcionais
Todo colaborador deverá pertencer a um Tenant.
Todo colaborador ativo deverá possuir matrícula única dentro da empresa.
Dados sensíveis deverão possuir controle de acesso específico.
Alterações funcionais deverão gerar histórico.
Salários não poderão ser alterados sem permissão e auditoria.
Contratos assinados não poderão ser excluídos.
Alterações contratuais deverão ocorrer por aditivo ou nova versão.
Jornadas e escalas deverão respeitar as regras configuradas.
Marcações de ponto confirmadas não poderão ser excluídas, apenas ajustadas com justificativa.
Fechamentos de ponto deverão bloquear alterações comuns.
Reaberturas deverão exigir permissão específica.
Férias não poderão exceder o saldo disponível.
Conflitos de férias com escalas críticas deverão ser sinalizados.
Afastamentos deverão impactar disponibilidade em Agenda, PCP, Produção, Instalação e Assistência Técnica.
Benefícios deverão possuir vigência.
Eventos da folha deverão manter origem e competência.
Documentos obrigatórios pendentes deverão gerar alertas.
Treinamentos obrigatórios vencidos poderão bloquear determinadas atividades conforme política.
EPIs deverão manter histórico de entrega, substituição e devolução.
Equipamentos entregues deverão permanecer vinculados ao responsável.
Avaliações concluídas não poderão ser alteradas sem nova versão ou reabertura autorizada.
Advertências e suspensões deverão manter documentos e responsáveis.
Desligamentos deverão executar checklist obrigatório.
Acessos deverão ser bloqueados conforme a data efetiva de desligamento.
Registros desligados deverão permanecer consultáveis conforme política de retenção.
Informações médicas deverão possuir acesso restrito.
Nenhum componente visual poderá possuir aparência hardcoded fora do theme_design.
Observações Arquiteturais

O módulo Recursos Humanos será a fonte oficial dos dados funcionais e da disponibilidade dos colaboradores.

O PCP e a Produção deverão consultar jornadas, escalas, afastamentos e disponibilidade.

A Agenda deverá considerar férias, folgas, afastamentos e bloqueios.

Instalação e Assistência Técnica deverão consultar equipes, habilidades, certificações e disponibilidade.

Financeiro deverá receber eventos aprovados de folha, benefícios, reembolsos, comissões, adiantamentos e rescisões.

Administração deverá controlar usuários e acessos, mas o vínculo entre usuário e colaborador deverá permanecer registrado.

O módulo Recursos Humanos não poderá alterar silenciosamente:

Dados contratuais

Salários

Jornadas

Férias

Afastamentos

Avaliações

Medidas disciplinares

Desligamentos

Toda alteração deverá possuir usuário, data, motivo, origem e auditoria.

Próxima Etapa
ETAPA 03-P

Catálogo Completo de Páginas

Fiscal

ETAPA 03-P

# Catálogo Completo de Páginas

# Fiscal

## ID do Módulo

```text
FIS
Objetivo

O módulo Fiscal será responsável por organizar, validar, gerar, receber, consultar e acompanhar documentos fiscais e obrigações relacionadas às operações comerciais, compras, estoques, serviços, transportes, devoluções, remessas e movimentações internas da empresa.

Ele deverá funcionar como a camada fiscal do ORGANIZEG3, recebendo fatos geradores dos módulos operacionais e financeiros, aplicando regras tributárias configuradas e produzindo documentos, eventos e informações para integração com autoridades fiscais, contabilidade e prestadores especializados.

O módulo deverá oferecer rastreabilidade completa entre:

pedido;
orçamento;
cliente;
fornecedor;
compra;
recebimento;
estoque;
produção;
expedição;
entrega;
instalação;
assistência técnica;
documento fiscal;
financeiro;
contabilidade.

Nenhum documento fiscal autorizado poderá ser excluído ou alterado silenciosamente.

Limites do Módulo

O módulo Fiscal será responsável por:

Gerenciar cadastros fiscais

Gerenciar regras tributárias

Receber fatos geradores

Validar dados fiscais

Gerar documentos fiscais

Transmitir documentos eletrônicos

Receber autorizações

Registrar rejeições

Registrar cancelamentos

Registrar inutilizações

Registrar cartas de correção

Registrar manifestações

Importar documentos fiscais

Controlar notas de entrada

Controlar notas de saída

Controlar documentos de serviço

Controlar documentos de transporte

Controlar devoluções

Controlar remessas

Controlar retornos

Controlar retenções

Controlar apurações

Gerar livros e relatórios fiscais

Preparar integrações contábeis

Manter auditoria fiscal

O módulo Fiscal não será responsável por:

Definir preços comerciais

Aprovar vendas

Executar compras

Movimentar estoque diretamente sem documento de origem

Realizar pagamentos ou recebimentos

Executar escrituração contábil oficial completa

Substituir consultoria tributária

Alterar regras legais automaticamente sem validação

Essas responsabilidades pertencem aos módulos:

Comercial

Compras

Estoque

Financeiro

Contabilidade

Administração
Fluxo Principal de Saída
Pedido Aprovado

↓

Separação ou Prestação Concluída

↓

Fato Gerador Fiscal Criado

↓

Validação Cadastral

↓

Validação Tributária

↓

Cálculo dos Tributos

↓

Geração do Documento

↓

Pré-visualização

↓

Aprovação Fiscal

↓

Transmissão

↓

Autorização

↓

Geração do XML e Representação Auxiliar

↓

Integração com Financeiro

↓

Integração com Estoque

↓

Integração com Contabilidade

↓

Envio ao Cliente

↓

Arquivamento
Fluxo Principal de Entrada
Documento Recebido

↓

Importação do XML

↓

Identificação do Fornecedor

↓

Validação da Chave

↓

Validação da Operação

↓

Conferência com Pedido de Compra

↓

Conferência com Recebimento

↓

Classificação Fiscal

↓

Apuração dos Tributos

↓

Manifestação quando Aplicável

↓

Escrituração

↓

Integração com Estoque

↓

Integração com Financeiro

↓

Integração com Contabilidade

↓

Arquivamento
Estrutura Geral
FIS — Fiscal

├── Dashboard Fiscal
├── Central Fiscal
├── Pendências Fiscais
├── Fatos Geradores
├── Documentos Fiscais
├── Notas Fiscais de Saída
├── Notas Fiscais de Entrada
├── Documentos de Serviço
├── Documentos de Transporte
├── Cupons e Documentos de Varejo
├── Cadastro do Documento Fiscal
├── Emissão
├── Transmissão
├── Autorizações
├── Rejeições
├── Cancelamentos
├── Inutilizações
├── Cartas de Correção
├── Eventos Fiscais
├── Manifestação do Destinatário
├── Importação de XML
├── Consulta de Chaves
├── Devoluções
├── Remessas
├── Retornos
├── Transferências
├── Industrialização por Terceiros
├── Bonificações
├── Comodatos
├── Demonstrações
├── Consignações
├── Vendas para Entrega Futura
├── Faturamento Antecipado
├── Operações Triangulares
├── Complementos
├── Ajustes
├── Retenções
├── Tributos
├── Regras Tributárias
├── Perfis Fiscais
├── Naturezas de Operação
├── CFOP
├── NCM
├── CEST
├── CST
├── CSOSN
├── Origem da Mercadoria
├── Enquadramentos
├── Benefícios Fiscais
├── Alíquotas
├── Unidades Tributárias
├── Conversões de Unidade
├── Municípios
├── Estados
├── Países
├── Regimes Tributários
├── Estabelecimentos
├── Séries
├── Numerações
├── Certificados Digitais
├── Ambientes
├── Contingência
├── Apurações
├── Livros Fiscais
├── Obrigações Acessórias
├── SPED
├── Integração Contábil
├── Fechamentos Fiscais
├── Auditoria Fiscal
├── Conciliação Fiscal
├── Histórico
├── Timeline
├── Indicadores
├── Relatórios
├── Templates
└── Configurações
Página
Dashboard Fiscal
ID
FIS-DAS-001
Tipo
Dashboard
Objetivo

Apresentar uma visão consolidada da situação fiscal da empresa.

Componentes
Documentos Emitidos no Período

Documentos Autorizados

Documentos Rejeitados

Documentos Cancelados

Documentos Pendentes

Documentos em Contingência

Notas de Entrada Pendentes

XMLs não Importados

Manifestações Pendentes

Cartas de Correção

Inutilizações

Tributos Calculados

Retenções

Apurações Abertas

Fechamentos Pendentes

Certificados Vencendo

Séries Próximas do Limite

Divergências Fiscais

Alertas
Filtros
Período

Empresa

Filial

Estabelecimento

Tipo de Documento

Modelo

Série

Status

Cliente

Fornecedor

Natureza de Operação

Estado

Município

Regime Tributário
Ações
Nova Nota de Saída

Importar XML

Abrir Pendências

Abrir Rejeições

Abrir Certificados

Abrir Apurações

Abrir Fechamentos

Consultar Documentos

Exportar Dashboard

Atualizar Dados
Página
Central Fiscal
ID
FIS-CEN-001
Tipo
Painel
Objetivo

Centralizar as operações diárias do setor fiscal.

Visualizações
Por Documento

Por Status

Por Estabelecimento

Por Série

Por Cliente

Por Fornecedor

Por Natureza

Por Período

Por Responsável
Componentes
Fatos Geradores Pendentes

Documentos em Preparação

Documentos Aguardando Aprovação

Documentos Aguardando Transmissão

Documentos Rejeitados

Documentos em Contingência

Entradas Aguardando Conferência

Manifestações Pendentes

Eventos Pendentes

Fechamentos Abertos

Alertas
Ações
Abrir Documento

Validar Documento

Aprovar Documento

Transmitir

Consultar Autorização

Corrigir Rejeição

Cancelar

Inutilizar

Emitir Carta de Correção

Manifestar

Importar XML

Criar Pendência
Página
Pendências Fiscais
ID
FIS-PEN-001
Tipo
Kanban
Objetivo

Controlar falhas cadastrais, tributárias, documentais ou operacionais que impedem a conclusão fiscal.

Etapas
Nova

Em Análise

Aguardando Cadastro

Aguardando Comercial

Aguardando Compras

Aguardando Estoque

Aguardando Financeiro

Aguardando Cliente

Aguardando Fornecedor

Aguardando Contabilidade

Em Correção

Resolvida

Cancelada
Categorias
Cadastro Incompleto

Classificação Fiscal

Natureza de Operação

CFOP

NCM

CEST

CST

CSOSN

Alíquota

Retenção

Endereço

Inscrição Estadual

Certificado Digital

Numeração

Rejeição

Divergência de XML

Divergência de Valor

Divergência de Quantidade
Página
Fatos Geradores
ID
FIS-FAT-001
Tipo
Lista
Objetivo

Receber e controlar acontecimentos dos demais módulos que poderão originar documentos fiscais.

Origens
Venda

Compra

Recebimento

Expedição

Entrega

Prestação de Serviço

Assistência Técnica

Devolução

Remessa

Retorno

Transferência

Bonificação

Comodato

Demonstração

Industrialização

Ajuste de Estoque

Importação
Status
Recebido

Em Validação

Com Pendência

Pronto para Emissão

Documento Gerado

Cancelado

Ignorado com Justificativa
Ações
Abrir Origem

Validar

Classificar

Agrupar

Desagrupar

Gerar Documento

Criar Pendência

Ignorar

Cancelar
Página
Documentos Fiscais
ID
FIS-DOC-001
Tipo
Lista
Objetivo

Listar todos os documentos fiscais emitidos, recebidos ou importados.

Visualizações
Tabela

Cards

Timeline

Calendário
Colunas
Número

Série

Modelo

Chave

Emissão

Entrada ou Saída

Emitente

Destinatário

Valor Total

Tributos

Natureza

Status

Protocolo

Responsável
Status
Rascunho

Em Validação

Com Pendência

Aguardando Aprovação

Aguardando Transmissão

Transmitido

Autorizado

Rejeitado

Denegado

Cancelado

Inutilizado

Em Contingência

Encerrado
Ações
Novo Documento

Abrir

Editar

Duplicar

Validar

Aprovar

Transmitir

Consultar

Imprimir

Enviar

Cancelar

Emitir Carta de Correção

Exportar XML

Importar XML

Clonar para Devolução

Gerar Complemento

Gerar Ajuste

Arquivar
Página
Notas Fiscais de Saída
ID
FIS-NFS-001
Tipo
Lista
Objetivo

Controlar documentos fiscais emitidos nas operações de saída.

Tipos de Operação
Venda

Venda para Entrega Futura

Remessa

Bonificação

Devolução de Compra

Transferência

Demonstração

Comodato

Industrialização

Complemento

Ajuste
Página
Notas Fiscais de Entrada
ID
FIS-NFE-001
Tipo
Lista
Objetivo

Controlar documentos fiscais recebidos de fornecedores e terceiros.

Ações
Importar XML

Lançar Manualmente

Vincular Pedido de Compra

Vincular Recebimento

Conferir Itens

Conferir Tributos

Manifestar

Escriturar

Criar Financeiro

Criar Estoque

Rejeitar Entrada

Solicitar Correção
Página
Documentos de Serviço
ID
FIS-SRV-001
Tipo
Lista
Objetivo

Controlar documentos relacionados à prestação ou contratação de serviços.

Operações
Prestação de Serviço

Serviço de Instalação

Serviço de Manutenção

Serviço de Assistência Técnica

Serviço Terceirizado

Serviço Tomado

Retenção de Tributos
Página
Documentos de Transporte
ID
FIS-TRA-001
Tipo
Lista
Objetivo

Controlar documentos de transporte vinculados às entregas e recebimentos.

Informações
Transportadora

Remetente

Destinatário

Veículo

Motorista

Volumes

Peso

Valor da Carga

Documento Vinculado

Chave

Status
Página
Cupons e Documentos de Varejo
ID
FIS-CUP-001
Tipo
Lista
Objetivo

Controlar documentos fiscais simplificados quando aplicáveis ao modelo de operação da empresa.

Página
Cadastro do Documento Fiscal
ID
FIS-DOC-002
Tipo
Cadastro
Objetivo

Centralizar todos os dados necessários à geração, validação, transmissão e escrituração de um documento fiscal.

Abas
Geral

Origem

Emitente

Destinatário

Endereço

Itens

Tributos

Totais

Transporte

Volumes

Cobrança

Pagamentos

Referências

Documentos Vinculados

Informações Adicionais

Autorização

Eventos

XML

Representação Auxiliar

Financeiro

Estoque

Contabilidade

Histórico

Timeline

Auditoria
Aba Geral

Campos:

Tipo de Documento

Modelo

Série

Número

Data de Emissão

Data de Saída ou Entrada

Hora de Saída ou Entrada

Tipo de Operação

Finalidade

Natureza de Operação

Estabelecimento

Regime Tributário

Ambiente

Status

Responsável
Aba Origem

Informações:

Módulo de Origem

Documento de Origem

Pedido

Compra

Recebimento

Expedição

Entrega

Instalação

Assistência

Devolução

Remessa

Retorno
Aba Emitente

Informações:

Razão Social

Nome Fantasia

CNPJ ou CPF

Inscrição Estadual

Inscrição Municipal

Regime Tributário

CNAE

Endereço

Contato
Aba Destinatário

Informações:

Tipo de Pessoa

Razão Social ou Nome

CNPJ ou CPF

Inscrição Estadual

Indicador de Inscrição

Inscrição Municipal

Email

Telefone

Consumidor Final

Contribuinte
Aba Endereço

Informações:

CEP

Logradouro

Número

Complemento

Bairro

Município

Código do Município

Estado

País

Código do País
Aba Itens

Informações:

Número do Item

Produto ou Serviço

Descrição Fiscal

Código Interno

NCM

CEST

CFOP

Unidade Comercial

Quantidade Comercial

Valor Unitário

Valor Total

Desconto

Frete

Seguro

Outras Despesas

Unidade Tributária

Quantidade Tributária

Valor Tributário

Origem

CST ou CSOSN

Pedido

Item do Pedido
Aba Tributos

Informações:

ICMS

ICMS ST

DIFAL

FCP

IPI

PIS

COFINS

ISS

IRRF

INSS

CSLL

Outras Retenções

Base de Cálculo

Alíquota

Valor

Benefício Fiscal

Desoneração

Partilha
Aba Totais

Informações:

Total dos Produtos

Total dos Serviços

Total do Desconto

Total do Frete

Total do Seguro

Outras Despesas

Base de ICMS

Valor de ICMS

Base de ICMS ST

Valor de ICMS ST

Valor de IPI

Valor de PIS

Valor de COFINS

Valor de ISS

Retenções

Valor Total do Documento
Aba Transporte

Informações:

Modalidade do Frete

Transportadora

CNPJ ou CPF

Inscrição Estadual

Endereço

Município

Estado

Veículo

Placa

UF da Placa

RNTC

Motorista
Aba Volumes

Informações:

Quantidade

Espécie

Marca

Numeração

Peso Líquido

Peso Bruto

Lacres

Volumes Vinculados
Aba Cobrança

Informações:

Fatura

Número

Valor Original

Desconto

Valor Líquido

Duplicatas

Vencimentos

Valores
Aba Pagamentos

Informações:

Forma de Pagamento

Indicador

Valor

Bandeira

Autorização

Troco

Integração Financeira
Aba Referências

Informações:

Documento Referenciado

Chave

Modelo

Série

Número

Data

Motivo
Aba Informações Adicionais

Informações:

Informações ao Fisco

Informações Complementares

Observações do Contribuinte

Dados de Interesse

Mensagens Automáticas

Fundamentação
Aba Autorização

Informações:

Data de Transmissão

Data de Autorização

Protocolo

Recibo

Status

Código de Retorno

Mensagem

Ambiente
Aba Eventos

Informações:

Tipo de Evento

Sequência

Data

Protocolo

Justificativa

Status

XML
Aba Financeiro

Informações:

Títulos Gerados

Parcelas

Vencimentos

Forma de Pagamento

Valor

Status

Conta Financeira
Aba Estoque

Informações:

Movimentações

Itens

Quantidades

Lotes

Almoxarifados

Status da Integração
Aba Contabilidade

Informações:

Lote Contábil

Contas

Débitos

Créditos

Centros de Custo

Histórico

Status
Página
Emissão
ID
FIS-EMI-001
Tipo
Painel
Objetivo

Conduzir o processo de preparação e geração dos documentos fiscais.

Etapas
Selecionar Origem

Validar Cadastro

Validar Operação

Validar Itens

Calcular Tributos

Validar Totais

Validar Transporte

Validar Financeiro

Gerar XML

Pré-visualizar

Aprovar

Transmitir
Página
Transmissão
ID
FIS-TRM-001
Tipo
Painel
Objetivo

Controlar transmissões para provedores e autoridades fiscais.

Status
Na Fila

Processando

Transmitido

Aguardando Retorno

Autorizado

Rejeitado

Falha de Comunicação

Contingência

Cancelado
Ações
Transmitir

Reenviar

Consultar Recibo

Consultar Chave

Atualizar Status

Entrar em Contingência

Retirar de Contingência

Cancelar Fila
Página
Autorizações
ID
FIS-AUT-001
Tipo
Lista
Objetivo

Consultar documentos autorizados e seus protocolos.

Página
Rejeições
ID
FIS-REJ-001
Tipo
Kanban
Objetivo

Controlar documentos rejeitados e ações corretivas.

Etapas
Nova Rejeição

Em Análise

Aguardando Cadastro

Aguardando Tributação

Aguardando Integração

Em Correção

Pronta para Reenvio

Reenviada

Resolvida

Cancelada
Informações
Documento

Código da Rejeição

Mensagem

Campo Relacionado

Causa Provável

Responsável

Prazo

Solução

Status
Página
Cancelamentos
ID
FIS-CAN-001
Tipo
Lista
Objetivo

Controlar solicitações e autorizações de cancelamento.

Campos
Documento

Chave

Data de Autorização

Prazo

Justificativa

Solicitante

Aprovador

Protocolo

Data do Cancelamento

Status
Página
Inutilizações
ID
FIS-INU-001
Tipo
Lista
Objetivo

Controlar inutilizações de faixas numéricas.

Campos
Modelo

Série

Número Inicial

Número Final

Ano

Justificativa

Protocolo

Status
Página
Cartas de Correção
ID
FIS-CCO-001
Tipo
Lista
Objetivo

Registrar e transmitir cartas de correção quando permitidas.

Campos
Documento

Sequência

Correção

Data

Responsável

Protocolo

Status
Página
Eventos Fiscais
ID
FIS-EVE-001
Tipo
Timeline
Objetivo

Centralizar os eventos vinculados a cada documento.

Tipos
Autorização

Cancelamento

Carta de Correção

Manifestação

Ciência da Operação

Confirmação da Operação

Desconhecimento

Operação não Realizada

EPEC

Encerramento

Outros Eventos
Página
Manifestação do Destinatário
ID
FIS-MAN-001
Tipo
Lista
Objetivo

Controlar manifestações sobre documentos recebidos.

Status
Pendente

Ciência Registrada

Confirmada

Desconhecida

Operação não Realizada

Com Erro

Cancelada
Página
Importação de XML
ID
FIS-XML-001
Tipo
Importador
Objetivo

Importar documentos fiscais eletrônicos e extrair seus dados.

Fontes
Upload Manual

Email

Pasta Monitorada

Provedor Fiscal

Portal

Integração

Distribuição de Documentos
Ações
Selecionar Arquivos

Validar XML

Identificar Documento

Identificar Fornecedor

Verificar Duplicidade

Importar

Criar Entrada

Criar Pendência

Arquivar
Página
Consulta de Chaves
ID
FIS-CHV-001
Tipo
Consulta
Objetivo

Consultar documentos por chave, número, série, emitente ou destinatário.

Página
Devoluções
ID
FIS-DEV-001
Tipo
Lista
Objetivo

Controlar devoluções de vendas e compras.

Tipos
Devolução de Venda

Devolução de Compra

Devolução Parcial

Devolução Total

Devolução Simbólica

Devolução de Assistência
Ações
Nova Devolução

Selecionar Documento Original

Selecionar Itens

Informar Quantidades

Informar Motivo

Calcular Tributos

Gerar Documento

Integrar Estoque

Integrar Financeiro
Página
Remessas
ID
FIS-REM-001
Tipo
Lista
Objetivo

Controlar saídas temporárias sem transferência definitiva de propriedade.

Exemplos
Remessa para Conserto

Remessa para Industrialização

Remessa para Demonstração

Remessa em Comodato

Remessa para Feira

Remessa para Armazenagem

Remessa para Instalação

Remessa de Vasilhame
Página
Retornos
ID
FIS-RET-001
Tipo
Lista
Objetivo

Controlar o retorno de itens enviados em remessa.

Informações
Remessa de Origem

Documento de Origem

Itens

Quantidades

Data Prevista

Data Real

Saldo Pendente

Status
Página
Transferências
ID
FIS-TRF-001
Tipo
Lista
Objetivo

Controlar transferências entre estabelecimentos, filiais ou almoxarifados quando houver impacto fiscal.

Página
Industrialização por Terceiros
ID
FIS-IND-001
Tipo
Painel
Objetivo

Controlar remessas, insumos, retornos, cobranças e documentos envolvidos na industrialização externa.

Página
Bonificações
ID
FIS-BON-001
Tipo
Lista
Objetivo

Controlar operações fiscais de bonificação.

Página
Comodatos
ID
FIS-COM-001
Tipo
Lista
Objetivo

Controlar bens enviados ou recebidos em comodato.

Página
Demonstrações
ID
FIS-DEM-001
Tipo
Lista
Objetivo

Controlar remessas e retornos para demonstração.

Página
Consignações
ID
FIS-CNS-001
Tipo
Lista
Objetivo

Controlar operações de consignação.

Página
Vendas para Entrega Futura
ID
FIS-VEF-001
Tipo
Painel
Objetivo

Controlar faturamento, saldo e entregas de vendas futuras.

Página
Faturamento Antecipado
ID
FIS-FAN-001
Tipo
Painel
Objetivo

Controlar documentos emitidos antes da entrega física.

Página
Operações Triangulares
ID
FIS-TRI-001
Tipo
Painel
Objetivo

Controlar operações que envolvem mais de dois participantes ou entregas em local diverso.

Página
Complementos
ID
FIS-CPL-001
Tipo
Lista
Objetivo

Gerar documentos complementares de valor, quantidade ou tributo.

Página
Ajustes
ID
FIS-AJU-001
Tipo
Lista
Objetivo

Registrar ajustes fiscais devidamente justificados e auditados.

Página
Retenções
ID
FIS-RET-002
Tipo
Dashboard Analítico
Objetivo

Controlar tributos retidos em serviços prestados ou tomados.

Informações
Documento

Prestador

Tomador

Serviço

Base

Alíquota

Valor Retido

Competência

Vencimento

Status
Página
Tributos
ID
FIS-TRI-002
Tipo
Lista
Objetivo

Cadastrar e consultar tributos utilizados nas operações.

Página
Regras Tributárias
ID
FIS-REG-001
Tipo
Lista
Objetivo

Definir regras aplicáveis por operação, produto, serviço, origem, destino, regime, cliente e fornecedor.

Critérios
Empresa

Estabelecimento

Regime Tributário

Tipo de Operação

Natureza

Produto

Categoria

NCM

CEST

Serviço

Cliente

Fornecedor

Estado de Origem

Estado de Destino

Município

Contribuinte

Consumidor Final

Finalidade

Vigência
Saídas da Regra
CFOP

CST

CSOSN

Alíquotas

Bases

Reduções

Benefícios

Diferimentos

Retenções

Mensagens

Contas Contábeis
Página
Perfis Fiscais
ID
FIS-PER-001
Tipo
Lista
Objetivo

Agrupar regras fiscais reutilizáveis por tipo de cliente, fornecedor, produto ou operação.

Página
Naturezas de Operação
ID
FIS-NAT-001
Tipo
Lista
Objetivo

Cadastrar naturezas utilizadas nos documentos fiscais.

Campos
Código

Descrição

Tipo

Finalidade

Movimenta Estoque

Gera Financeiro

Gera Contabilidade

Permite Devolução

Permite Remessa

Regras Tributárias

Mensagens

Status
Página
CFOP
ID
FIS-CFO-001
Tipo
Lista
Objetivo

Gerenciar códigos de operação utilizados nas regras fiscais.

Página
NCM
ID
FIS-NCM-001
Tipo
Lista
Objetivo

Classificar fiscalmente mercadorias.

Informações
Código

Descrição

Vigência

Exceções

CEST

Tributos Relacionados

Observações

Status
Página
CEST
ID
FIS-CES-001
Tipo
Lista
Objetivo

Gerenciar códigos de substituição tributária quando aplicáveis.

Página
CST
ID
FIS-CST-001
Tipo
Lista
Objetivo

Gerenciar códigos de situação tributária.

Página
CSOSN
ID
FIS-CSO-001
Tipo
Lista
Objetivo

Gerenciar códigos de situação tributária do regime simplificado quando aplicáveis.

Página
Origem da Mercadoria
ID
FIS-ORI-001
Tipo
Lista
Objetivo

Gerenciar códigos de origem utilizados na tributação dos itens.

Página
Enquadramentos
ID
FIS-ENQ-001
Tipo
Lista
Objetivo

Gerenciar enquadramentos legais e tributários configuráveis.

Página
Benefícios Fiscais
ID
FIS-BEF-001
Tipo
Lista
Objetivo

Controlar benefícios, reduções, isenções, diferimentos e códigos relacionados.

Campos
Código

Descrição

Tributo

Estado

Operação

Produto

Vigência

Fundamentação

Mensagem

Status
Página
Alíquotas
ID
FIS-ALI-001
Tipo
Lista
Objetivo

Cadastrar alíquotas por tributo, jurisdição, operação e vigência.

Página
Unidades Tributárias
ID
FIS-UNT-001
Tipo
Lista
Objetivo

Controlar unidades comerciais e tributárias.

Página
Conversões de Unidade
ID
FIS-CON-001
Tipo
Lista
Objetivo

Definir fatores de conversão entre unidades comerciais e tributárias.

Página
Municípios
ID
FIS-MUN-001
Tipo
Lista
Objetivo

Gerenciar códigos e informações municipais utilizados em documentos e serviços.

Página
Estados
ID
FIS-UF-001
Tipo
Lista
Objetivo

Gerenciar dados estaduais e parâmetros fiscais.

Página
Países
ID
FIS-PAI-001
Tipo
Lista
Objetivo

Gerenciar códigos de países para operações nacionais e internacionais.

Página
Regimes Tributários
ID
FIS-RTB-001
Tipo
Lista
Objetivo

Cadastrar os regimes aplicáveis a cada empresa e estabelecimento.

Página
Estabelecimentos
ID
FIS-EST-001
Tipo
Lista
Objetivo

Gerenciar dados fiscais por empresa, filial ou estabelecimento.

Campos
Razão Social

Nome Fantasia

CNPJ

Inscrição Estadual

Inscrição Municipal

Regime Tributário

CNAE

Endereço

Certificado

Séries

Ambiente

Status
Página
Séries
ID
FIS-SER-001
Tipo
Lista
Objetivo

Gerenciar séries por estabelecimento, modelo e ambiente.

Página
Numerações
ID
FIS-NUM-001
Tipo
Lista
Objetivo

Controlar faixas numéricas utilizadas, disponíveis, inutilizadas e reservadas.

Página
Certificados Digitais
ID
FIS-CER-001
Tipo
Lista
Objetivo

Controlar certificados utilizados nas transmissões.

Informações
Empresa

Estabelecimento

Tipo

Titular

Emissor

Número de Série

Data Inicial

Data Final

Dias para Vencimento

Status
Regras

Senhas e chaves deverão ser armazenadas de forma segura e nunca exibidas integralmente.

Página
Ambientes
ID
FIS-AMB-001
Tipo
Configuração
Objetivo

Gerenciar ambientes de homologação, produção e contingência.

Página
Contingência
ID
FIS-CTG-001
Tipo
Painel
Objetivo

Controlar emissões realizadas quando o serviço principal estiver indisponível.

Ações
Ativar Contingência

Selecionar Modalidade

Registrar Motivo

Emitir

Consultar Pendências

Regularizar

Encerrar Contingência
Página
Apurações
ID
FIS-APU-001
Tipo
Dashboard Analítico
Objetivo

Consolidar bases, débitos, créditos, retenções e ajustes por competência.

Dimensões
Empresa

Estabelecimento

Competência

Tributo

Operação

Estado

Município

Produto

Serviço
Status
Aberta

Em Processamento

Em Conferência

Com Divergência

Aguardando Aprovação

Fechada

Reaberta
Página
Livros Fiscais
ID
FIS-LIV-001
Tipo
Relatório
Objetivo

Gerar livros e demonstrativos fiscais conforme configuração e necessidade.

Página
Obrigações Acessórias
ID
FIS-OBR-001
Tipo
Lista
Objetivo

Controlar obrigações, competências, prazos, arquivos e entregas.

Campos
Obrigação

Empresa

Competência

Prazo

Responsável

Arquivo

Protocolo

Data de Entrega

Status
Página
SPED
ID
FIS-SPD-001
Tipo
Painel
Objetivo

Preparar, validar e exportar informações estruturadas para integrações fiscais e contábeis.

Ações
Selecionar Competência

Validar Cadastros

Validar Documentos

Validar Blocos

Gerar Arquivo

Executar Pré-validação

Corrigir Pendências

Exportar

Registrar Protocolo
Página
Integração Contábil
ID
FIS-CTB-001
Tipo
Painel
Objetivo

Preparar lançamentos, contas, históricos e centros de custo para o módulo ou sistema contábil.

Informações
Origem

Documento

Conta Débito

Conta Crédito

Valor

Centro de Custo

Histórico

Lote

Competência

Status
Página
Fechamentos Fiscais
ID
FIS-FEC-001
Tipo
Lista
Objetivo

Controlar o encerramento de competências fiscais.

Checklist
Documentos de Saída Conferidos

Documentos de Entrada Conferidos

Serviços Conferidos

Cancelamentos Conferidos

Inutilizações Conferidas

Manifestações Conferidas

Retenções Conferidas

Apurações Conferidas

Divergências Resolvidas

Integração Contábil Gerada

Relatórios Gerados

Aprovação Registrada
Regras

Períodos fechados deverão bloquear alterações comuns.

Reaberturas deverão exigir permissão específica e justificativa.

Página
Auditoria Fiscal
ID
FIS-AUD-001
Tipo
Dashboard Analítico
Objetivo

Identificar inconsistências, riscos, divergências e alterações relevantes.

Análises
Numeração Quebrada

Documentos Duplicados

Chaves Duplicadas

Cadastro Incompleto

NCM Ausente

CFOP Incompatível

CST Incompatível

Divergência de Tributos

Divergência de Totais

Documento sem Financeiro

Documento sem Estoque

Documento sem Contabilidade

Cancelamento Fora da Política

Alteração após Fechamento
Página
Conciliação Fiscal
ID
FIS-CNC-001
Tipo
Dashboard Analítico
Objetivo

Comparar informações fiscais com os módulos Comercial, Compras, Estoque, Financeiro e Contabilidade.

Comparações
Pedido x Nota

Compra x Entrada

Recebimento x XML

Nota x Estoque

Nota x Financeiro

Nota x Contabilidade

Documento x Autorização

Documento x Manifestação

Totais x Tributos
Página
Histórico
ID
FIS-HIS-001
Tipo
Consulta
Objetivo

Consultar alterações, transmissões, retornos, eventos e integrações fiscais.

Página
Timeline
ID
FIS-TML-001
Tipo
Timeline
Objetivo

Apresentar os acontecimentos de um documento fiscal em ordem cronológica.

Eventos
Fato Gerador Criado

Documento Criado

Documento Validado

Documento Aprovado

XML Gerado

Documento Transmitido

Documento Autorizado

Documento Rejeitado

Documento Corrigido

Documento Reenviado

Carta de Correção Emitida

Documento Cancelado

Financeiro Gerado

Estoque Movimentado

Contabilidade Integrada

Documento Enviado ao Destinatário
Página
Indicadores
ID
FIS-KPI-001
Tipo
Dashboard Analítico
Indicadores
Documentos Emitidos

Documentos Recebidos

Documentos Autorizados

Taxa de Rejeição

Tempo Médio de Autorização

Documentos Cancelados

Documentos em Contingência

Entradas Pendentes

XMLs Importados

Manifestações Pendentes

Tributos por Competência

Retenções

Divergências

Pendências por Origem

Pendências por Responsável

Fechamentos no Prazo

Certificados Vencendo

Documentos sem Integração

Risco Fiscal
Página
Relatórios
ID
FIS-REL-001
Tipo
Relatório
Relatórios Disponíveis
Documentos Fiscais Emitidos

Documentos Fiscais Recebidos

Notas de Saída

Notas de Entrada

Documentos de Serviço

Documentos de Transporte

Documentos por Cliente

Documentos por Fornecedor

Documentos por Natureza

Documentos por CFOP

Documentos por NCM

Documentos por CST

Documentos Cancelados

Documentos Rejeitados

Cartas de Correção

Inutilizações

Manifestações

Devoluções

Remessas

Retornos

Transferências

Retenções

Tributos por Competência

Apurações

Obrigações Acessórias

Conciliação Fiscal

Auditoria Fiscal

Pendências Fiscais

Certificados Digitais

Integração Contábil
Página
Templates
ID
FIS-TMP-001
Tipo
Configuração
Objetivo

Criar modelos reutilizáveis de documentos, mensagens e relatórios fiscais.

Tipos
Documento Fiscal

Natureza de Operação

Mensagem Fiscal

Informação Adicional

Carta de Correção

Justificativa de Cancelamento

Relatório Fiscal

Email de Envio

Representação Auxiliar
Página
Configurações
ID
FIS-CFG-001
Tipo
Configuração
Configurações
Empresas

Estabelecimentos

Regimes Tributários

Séries

Numerações

Modelos de Documento

Certificados Digitais

Ambientes

Provedores

Naturezas de Operação

Perfis Fiscais

Regras Tributárias

Tributos

CFOP

NCM

CEST

CST

CSOSN

Origem da Mercadoria

Benefícios Fiscais

Alíquotas

Unidades Tributárias

Conversões

Mensagens

Regras de Aprovação

Regras de Cancelamento

Regras de Contingência

Regras de Fechamento

Integrações

Templates

Notificações

Auditoria
Dialogs
FIS-DLG-001 Novo Documento Fiscal

FIS-DLG-002 Selecionar Origem

FIS-DLG-003 Selecionar Estabelecimento

FIS-DLG-004 Selecionar Natureza de Operação

FIS-DLG-005 Selecionar Cliente

FIS-DLG-006 Selecionar Fornecedor

FIS-DLG-007 Adicionar Item

FIS-DLG-008 Editar Tributação do Item

FIS-DLG-009 Selecionar CFOP

FIS-DLG-010 Selecionar NCM

FIS-DLG-011 Selecionar CST

FIS-DLG-012 Selecionar CSOSN

FIS-DLG-013 Selecionar Benefício Fiscal

FIS-DLG-014 Calcular Tributos

FIS-DLG-015 Validar Documento

FIS-DLG-016 Aprovar Documento

FIS-DLG-017 Transmitir Documento

FIS-DLG-018 Consultar Autorização

FIS-DLG-019 Corrigir Rejeição

FIS-DLG-020 Cancelar Documento

FIS-DLG-021 Inutilizar Numeração

FIS-DLG-022 Emitir Carta de Correção

FIS-DLG-023 Importar XML

FIS-DLG-024 Vincular Pedido de Compra

FIS-DLG-025 Vincular Recebimento

FIS-DLG-026 Manifestar Documento

FIS-DLG-027 Criar Devolução

FIS-DLG-028 Criar Remessa

FIS-DLG-029 Registrar Retorno

FIS-DLG-030 Criar Transferência

FIS-DLG-031 Criar Complemento

FIS-DLG-032 Criar Ajuste Fiscal

FIS-DLG-033 Registrar Retenção

FIS-DLG-034 Criar Regra Tributária

FIS-DLG-035 Criar Natureza de Operação

FIS-DLG-036 Cadastrar Certificado

FIS-DLG-037 Ativar Contingência

FIS-DLG-038 Encerrar Contingência

FIS-DLG-039 Fechar Competência

FIS-DLG-040 Reabrir Competência

FIS-DLG-041 Gerar Arquivo Fiscal

FIS-DLG-042 Exportar Integração Contábil

FIS-DLG-043 Enviar Documento por Email

FIS-DLG-044 Gerar Representação Auxiliar

FIS-DLG-045 Criar Pendência Fiscal

FIS-DLG-046 Resolver Pendência

FIS-DLG-047 Duplicar Documento

FIS-DLG-048 Arquivar Documento

FIS-DLG-049 Importar Cadastros Fiscais

FIS-DLG-050 Exportar Dados Fiscais
Wizards
FIS-WIZ-001 Assistente de Emissão Fiscal

FIS-WIZ-002 Assistente de Nota de Entrada

FIS-WIZ-003 Assistente de Importação de XML

FIS-WIZ-004 Assistente de Devolução

FIS-WIZ-005 Assistente de Remessa e Retorno

FIS-WIZ-006 Assistente de Transferência

FIS-WIZ-007 Assistente de Regra Tributária

FIS-WIZ-008 Assistente de Configuração do Estabelecimento

FIS-WIZ-009 Assistente de Certificado Digital

FIS-WIZ-010 Assistente de Contingência

FIS-WIZ-011 Assistente de Apuração

FIS-WIZ-012 Assistente de Fechamento Fiscal

FIS-WIZ-013 Assistente de Obrigação Acessória

FIS-WIZ-014 Assistente de Integração Contábil

FIS-WIZ-015 Assistente de Auditoria Fiscal

FIS-WIZ-016 Assistente de Configuração Inicial Fiscal
Componentes Específicos
FIS-CPT-001 Central Fiscal

FIS-CPT-002 Editor de Documento Fiscal

FIS-CPT-003 Grade de Itens Fiscais

FIS-CPT-004 Calculadora Tributária

FIS-CPT-005 Validador Fiscal

FIS-CPT-006 Visualizador de XML

FIS-CPT-007 Comparador de XML

FIS-CPT-008 Visualizador de Representação Auxiliar

FIS-CPT-009 Painel de Transmissão

FIS-CPT-010 Painel de Rejeições

FIS-CPT-011 Editor de Carta de Correção

FIS-CPT-012 Importador de XML

FIS-CPT-013 Conciliador de Entrada

FIS-CPT-014 Editor de Regra Tributária

FIS-CPT-015 Matriz Tributária

FIS-CPT-016 Painel de Certificados

FIS-CPT-017 Painel de Contingência

FIS-CPT-018 Painel de Apuração

FIS-CPT-019 Validador de Fechamento

FIS-CPT-020 Painel de Auditoria Fiscal

FIS-CPT-021 Conciliador Fiscal

FIS-CPT-022 Timeline Fiscal

FIS-CPT-023 Gerador de Arquivos

FIS-CPT-024 Painel de Indicadores Fiscais

Todos os estilos visuais, cores, fontes, ícones, imagens, espaçamentos, estados e dimensões deverão ser obtidos exclusivamente pelo theme_design.

Nenhum componente poderá conter aparência hardcoded.

Eventos
FiscalSourceEventCreated

FiscalDocumentCreated

FiscalDocumentValidated

FiscalDocumentValidationFailed

FiscalDocumentApprovalRequested

FiscalDocumentApproved

FiscalDocumentRejectedInternally

FiscalXMLGenerated

FiscalDocumentTransmissionQueued

FiscalDocumentTransmitted

FiscalDocumentAuthorized

FiscalDocumentRejected

FiscalDocumentDenied

FiscalDocumentConsulted

FiscalDocumentContingencyActivated

FiscalDocumentContingencyRegularized

FiscalDocumentCancellationRequested

FiscalDocumentCancelled

FiscalNumberRangeInvalidated

FiscalCorrectionLetterCreated

FiscalCorrectionLetterAuthorized

FiscalManifestationRequested

FiscalManifestationRegistered

FiscalXMLImported

FiscalIncomingDocumentCreated

FiscalIncomingDocumentMatched

FiscalIncomingDocumentBookkept

FiscalReturnCreated

FiscalRemittanceCreated

FiscalReturnMatched

FiscalTransferCreated

FiscalTaxCalculated

FiscalRetentionCreated

FiscalTaxRuleCreated

FiscalTaxRuleUpdated

FiscalCertificateExpiring

FiscalPeriodOpened

FiscalPeriodValidationStarted

FiscalPeriodClosed

FiscalPeriodReopened

FiscalAccountingIntegrationGenerated

FiscalObligationGenerated

FiscalObligationDelivered

FiscalAuditIssueCreated

FiscalAuditIssueResolved
Automações
Pedido liberado para faturamento

↓

Criar fato gerador

↓

Validar cliente

↓

Validar itens

↓

Selecionar natureza

↓

Calcular tributos

↓

Criar documento em rascunho
Documento aprovado

↓

Gerar XML

↓

Assinar

↓

Transmitir

↓

Consultar retorno
Documento autorizado

↓

Salvar XML e protocolo

↓

Gerar representação auxiliar

↓

Criar integração financeira

↓

Criar movimentação de estoque

↓

Criar integração contábil

↓

Enviar ao destinatário
Documento rejeitado

↓

Criar pendência

↓

Classificar rejeição

↓

Notificar responsável

↓

Bloquear conclusão fiscal
XML recebido

↓

Validar assinatura e chave

↓

Identificar fornecedor

↓

Verificar duplicidade

↓

Vincular pedido de compra

↓

Criar entrada pendente
Documento de entrada conferido

↓

Escriturar

↓

Criar estoque

↓

Criar financeiro

↓

Criar contabilidade
Certificado próximo do vencimento

↓

Criar alerta

↓

Notificar responsáveis

↓

Bloquear risco de transmissão conforme política
Competência próxima do fechamento

↓

Executar validações

↓

Listar divergências

↓

Notificar fiscal e contabilidade
Integrações
Administração

CRM

Comercial

Orçamentos

Projetos

Compras

Estoque

PCP

Produção

Qualidade

Expedição

Instalação

Assistência Técnica

Financeiro

Recursos Humanos

Contabilidade

Agenda

Documentos

Workflow

BI

IA

Auditoria

Sincronização

Email

Provedores Fiscais

Autoridades Fiscais

Certificados Digitais
Permissões
fiscal.dashboard.read

fiscal.central.read

fiscal.pending.read

fiscal.pending.manage

fiscal.source_event.read

fiscal.source_event.manage

fiscal.document.read

fiscal.document.create

fiscal.document.update

fiscal.document.validate

fiscal.document.approve

fiscal.document.transmit

fiscal.document.consult

fiscal.document.print

fiscal.document.send

fiscal.document.archive

fiscal.document.cancel.request

fiscal.document.cancel.approve

fiscal.document.cancel.execute

fiscal.document.invalidate_number

fiscal.document.correction_letter.create

fiscal.document.correction_letter.transmit

fiscal.document.xml.read

fiscal.document.xml.export

fiscal.document.xml.import

fiscal.incoming.read

fiscal.incoming.create

fiscal.incoming.match

fiscal.incoming.bookkeep

fiscal.manifestation.read

fiscal.manifestation.execute

fiscal.return.read

fiscal.return.create

fiscal.remittance.read

fiscal.remittance.create

fiscal.transfer.create

fiscal.complement.create

fiscal.adjustment.create

fiscal.retention.read

fiscal.retention.manage

fiscal.tax.read

fiscal.tax_rule.read

fiscal.tax_rule.create

fiscal.tax_rule.update

fiscal.tax_rule.approve

fiscal.nature.read

fiscal.nature.manage

fiscal.cfop.read

fiscal.cfop.manage

fiscal.ncm.read

fiscal.ncm.manage

fiscal.cest.manage

fiscal.cst.manage

fiscal.csosn.manage

fiscal.tax_benefit.manage

fiscal.establishment.read

fiscal.establishment.manage

fiscal.series.manage

fiscal.numbering.manage

fiscal.certificate.read

fiscal.certificate.manage

fiscal.environment.manage

fiscal.contingency.activate

fiscal.contingency.close

fiscal.assessment.read

fiscal.assessment.manage

fiscal.obligation.read

fiscal.obligation.manage

fiscal.sped.generate

fiscal.accounting_integration.generate

fiscal.period.read

fiscal.period.close

fiscal.period.reopen

fiscal.audit.read

fiscal.audit.manage

fiscal.reconciliation.read

fiscal.report.read

fiscal.report.export

fiscal.configuration.manage
Relatórios e Documentos Gerados
Documento Fiscal Eletrônico

XML do Documento Fiscal

Protocolo de Autorização

Representação Auxiliar

Carta de Correção

Protocolo de Cancelamento

Protocolo de Inutilização

Manifestação do Destinatário

Relatório de Documentos Emitidos

Relatório de Documentos Recebidos

Relatório de Rejeições

Relatório de Cancelamentos

Relatório de Devoluções

Relatório de Remessas

Relatório de Retornos

Relatório de Tributos

Relatório de Retenções

Livro Fiscal

Relatório de Apuração

Relatório de Obrigações

Arquivo de Integração Contábil

Arquivo Fiscal Estruturado

Relatório de Conciliação Fiscal

Relatório de Auditoria Fiscal

Relatório de Fechamento Fiscal
Recursos de Inteligência Artificial
Identificar inconsistências cadastrais

Sugerir natureza de operação

Sugerir CFOP

Sugerir classificação fiscal

Detectar NCM possivelmente incorreto

Detectar divergências de tributação

Explicar rejeições em linguagem simples

Sugerir correção para rejeição

Comparar XML com pedido de compra

Comparar nota com recebimento

Detectar documentos duplicados

Detectar anomalias em valores fiscais

Resumir documento fiscal

Resumir competência fiscal

Identificar riscos de fechamento

Sugerir pendências prioritárias

Pesquisar documentos em linguagem natural

Gerar explicação de auditoria

Apoiar classificação de operações

A IA nunca poderá transmitir, cancelar, inutilizar, manifestar, fechar competência, alterar regra tributária ou aprovar documento sem confirmação explícita de usuário autorizado.

Toda sugestão tributária deverá ser tratada como apoio e exigir validação humana.

Regras Funcionais
Todo documento fiscal deverá pertencer a um Tenant e a um estabelecimento.
Todo documento deverá possuir origem identificada, salvo lançamentos manuais autorizados.
Documentos autorizados não poderão ser editados.
Correções posteriores deverão ocorrer por evento, documento complementar, ajuste ou cancelamento permitido.
Chaves de acesso não poderão ser duplicadas.
A numeração deverá ser única por estabelecimento, modelo, série e ambiente.
Documentos rejeitados não deverão gerar movimentações definitivas.
Documentos autorizados deverão preservar XML, protocolo e representação auxiliar.
Cancelamentos deverão exigir justificativa e aprovação conforme alçada.
Inutilizações deverão preservar faixa, ano, justificativa e protocolo.
Cartas de correção deverão respeitar campos permitidos pela configuração.
Entradas importadas deverão ser verificadas contra duplicidade.
Documentos de entrada deverão ser conciliados com compras e recebimentos quando aplicável.
Divergências relevantes deverão gerar pendência.
Alterações em regras tributárias deverão possuir vigência e histórico.
Regras retroativas não poderão alterar documentos já autorizados.
Cálculos tributários deverão registrar a regra aplicada.
Certificados deverão possuir controle de validade e acesso restrito.
Senhas e segredos não poderão ser armazenados em texto legível.
Períodos fiscais fechados deverão bloquear alterações comuns.
Reaberturas deverão exigir autorização e justificativa.
Integrações financeiras, de estoque e contábeis deverão manter vínculo com o documento fiscal.
Estornos de integração deverão preservar rastreabilidade.
Documentos e eventos não poderão ser excluídos após transmissão.
Obrigações acessórias deverão manter arquivo, responsável, protocolo e data de entrega.
Informações legais e tributárias configuráveis deverão ser validadas por profissional responsável.
Nenhum componente visual poderá possuir aparência hardcoded fora do theme_design.
Observações Arquiteturais

O módulo Fiscal será a fonte oficial dos documentos fiscais e eventos tributários do ORGANIZEG3.

Os módulos Comercial, Compras, Estoque, Expedição, Instalação e Assistência Técnica deverão produzir fatos geradores.

O módulo Fiscal deverá transformar esses fatos em documentos e registros tributários válidos conforme a configuração da empresa.

O Financeiro deverá receber títulos e retenções originados dos documentos fiscais.

O Estoque deverá receber movimentações somente após o evento fiscal ou operacional definido pela política da empresa.

A Contabilidade deverá receber os lançamentos ou arquivos de integração.

O módulo Fiscal não poderá alterar silenciosamente:

Cadastro do emitente

Cadastro do destinatário

Classificação fiscal

Natureza de operação

Tributação

Numeração

Documento autorizado

Eventos fiscais

Competências fechadas

Toda alteração deverá possuir:

Usuário

Data

Hora

Origem

Justificativa

Valor anterior

Valor posterior

Aprovação quando necessária
Próxima Etapa
ETAPA 03-Q

Catálogo Completo de Páginas

Business Intelligence — BI

# ORGANIZEG3 — MAPA FUNCIONAL MESTRE

# ETAPA 03-Q

# Catálogo Completo de Páginas

# Business Intelligence — BI

## ID do Módulo

```text
BI
1. Objetivo

O módulo Business Intelligence será responsável por consolidar, organizar, analisar e apresentar informações gerenciais de todos os módulos do ORGANIZEG3.

O BI deverá transformar dados operacionais em indicadores, comparações, tendências, alertas, projeções e informações para tomada de decisão.

Ele deverá atender diferentes níveis de gestão:

Operacional

Supervisão

Coordenação

Gerência

Direção

Administradores do Tenant

O módulo deverá permitir análises sobre:

Comercial

CRM

Projetos

Orçamentos

Compras

Estoque

PCP

Produção

Qualidade

Expedição

Instalação

Assistência Técnica

Financeiro

Recursos Humanos

Fiscal

Administração

Auditoria

Sincronização

O BI não deverá alterar diretamente os registros operacionais analisados.

Toda informação apresentada deverá preservar sua origem, período, filtros, moeda, unidade, empresa, filial e Tenant.

2. Limites do Módulo
2.1 Responsabilidades

O módulo BI será responsável por:

Consolidar dados dos módulos

Calcular indicadores

Criar dashboards

Criar relatórios analíticos

Comparar períodos

Analisar tendências

Analisar metas

Analisar desvios

Criar segmentações

Criar rankings

Criar alertas gerenciais

Criar projeções

Gerar exportações

Controlar acesso aos dados analíticos

Registrar versões das definições de indicadores

Disponibilizar consultas em linguagem natural

Manter rastreabilidade da origem dos números
2.2 Fora do Escopo

O módulo BI não será responsável por:

Editar pedidos

Alterar projetos

Movimentar estoque

Liberar ordens

Registrar produção

Aprovar pagamentos

Modificar folha

Transmitir documentos fiscais

Substituir os módulos operacionais

Corrigir automaticamente dados de origem

Quando uma inconsistência for encontrada, o BI deverá:

Identificar o dado

Informar a origem

Apresentar o impacto

Criar alerta ou pendência

Direcionar o usuário ao módulo responsável
3. Princípios Funcionais
Todo dado deverá pertencer a um Tenant.
Os filtros de Tenant, empresa e filial deverão ser obrigatórios no processamento interno.
Indicadores financeiros deverão informar moeda e regime de reconhecimento.
Indicadores de quantidade deverão informar unidade.
Indicadores temporais deverão informar período e fuso horário.
Nenhum indicador poderá utilizar dados de outro Tenant.
Dados sensíveis deverão respeitar as permissões do módulo de origem.
Um usuário sem acesso a salários não poderá visualizar salários por meio do BI.
Um usuário sem acesso a custos não poderá inferir custos por relatórios analíticos.
Todo indicador deverá possuir definição funcional documentada.
Toda fórmula deverá possuir versão.
Mudanças de fórmula não poderão alterar silenciosamente relatórios históricos já publicados.
Dashboards publicados deverão possuir proprietário e público autorizado.
Exportações deverão respeitar as mesmas permissões da visualização.
A origem dos dados deverá ser consultável.
Valores consolidados deverão permitir detalhamento até os registros de origem quando autorizado.
O BI não deverá executar consultas pesadas diretamente na interface principal.
Processamentos extensos deverão utilizar agregações, cache ou estruturas analíticas apropriadas.
O BI deverá indicar quando os dados foram atualizados.
Dados desatualizados deverão ser sinalizados.
4. Fluxo Principal
Dados Operacionais

↓

Validação de Origem

↓

Extração

↓

Normalização

↓

Consolidação

↓

Agregação

↓

Cálculo de Indicadores

↓

Aplicação de Permissões

↓

Atualização de Dashboards

↓

Análise

↓

Detalhamento

↓

Exportação ou Alerta
5. Estrutura Geral
BI — Business Intelligence

├── Visão Executiva
├── Central de BI
├── Meus Dashboards
├── Dashboards Compartilhados
├── Catálogo de Dashboards
├── Indicadores
├── Catálogo de Indicadores
├── Metas
├── Alertas Gerenciais
├── Consultas Analíticas
├── Exploração de Dados
├── Comparação de Períodos
├── Análise de Tendências
├── Rankings
├── Projeções
├── Cenários
├── Relatórios Gerenciais
├── Relatórios Agendados
├── Exportações
├── Dados Analíticos
├── Fontes de Dados
├── Atualizações
├── Qualidade dos Dados
├── Dicionário de Dados
├── Linhagem de Dados
├── Permissões Analíticas
├── Auditoria do BI
├── BI Comercial
├── BI de Projetos
├── BI de Orçamentos
├── BI de Compras
├── BI de Estoque
├── BI de PCP
├── BI de Produção
├── BI de Qualidade
├── BI de Expedição
├── BI de Instalação
├── BI de Assistência Técnica
├── BI Financeiro
├── BI de Recursos Humanos
├── BI Fiscal
├── Templates
└── Configurações
6. Página — Visão Executiva
ID
BI-EXE-001
Tipo
Dashboard Executivo
Objetivo

Apresentar aos gestores uma visão consolidada da situação da empresa.

Componentes
Receita

Receita Realizada

Receita Prevista

Margem Bruta

Margem de Contribuição

Resultado Operacional

Fluxo de Caixa

Saldo Disponível

Contas a Receber

Contas a Pagar

Inadimplência

Vendas no Período

Conversão Comercial

Ticket Médio

Projetos em Andamento

Projetos Atrasados

Compras Pendentes

Materiais em Falta

Ordens em Produção

Aderência ao Plano

Produtividade

Retrabalho

Não Conformidades

Entregas no Prazo

Instalações no Prazo

Chamados de Assistência

Headcount

Absenteísmo

Turnover

Pendências Fiscais

Alertas Críticos
Filtros
Período

Empresa

Filial

Unidade de Negócio

Centro de Resultado

Centro de Custo

Responsável

Cliente

Projeto
Ações
Alterar Período

Comparar Período

Abrir Indicador

Detalhar Origem

Adicionar Favorito

Exportar PDF

Exportar Planilha

Compartilhar

Agendar Envio

Atualizar
7. Página — Central de BI
ID
BI-CEN-001
Tipo
Painel
Objetivo

Centralizar dashboards, indicadores, consultas, alertas e relatórios.

Componentes
Dashboards Recentes

Dashboards Favoritos

Indicadores Favoritos

Alertas Ativos

Relatórios Agendados

Consultas Recentes

Atualizações Pendentes

Falhas de Processamento

Qualidade dos Dados

Sugestões de Análise
8. Página — Meus Dashboards
ID
BI-DAS-001
Tipo
Lista
Colunas
Nome

Descrição

Proprietário

Categoria

Última Atualização

Último Acesso

Compartilhado

Status
Status
Rascunho

Publicado

Desatualizado

Com Erro

Arquivado
Ações
Novo Dashboard

Abrir

Editar

Duplicar

Publicar

Compartilhar

Agendar

Exportar

Arquivar

Excluir Rascunho
9. Página — Editor de Dashboard
ID
BI-DAS-002
Tipo
Editor
Objetivo

Permitir a composição controlada de dashboards.

Abas
Geral

Layout

Componentes

Filtros

Indicadores

Permissões

Atualização

Compartilhamento

Agendamentos

Histórico

Auditoria
Tipos de Componentes
Indicador Numérico

Cartão Comparativo

Gráfico de Linha

Gráfico de Colunas

Gráfico de Barras

Gráfico de Área

Gráfico de Pizza

Gráfico de Rosca

Gráfico de Dispersão

Funil

Medidor

Mapa

Tabela

Matriz

Ranking

Timeline

Texto

Imagem

Alerta

Lista de Pendências
Regras de Layout
Grade Responsiva

Posições Persistidas

Larguras Configuráveis

Alturas Configuráveis

Sem Sobreposição

Componentes Alinhados

Modo Claro e Escuro

Estilos Exclusivamente pelo theme_design
Ações
Adicionar Componente

Editar Componente

Duplicar Componente

Mover por Controles

Redimensionar por Controles

Remover

Visualizar

Salvar Rascunho

Publicar Nova Versão

Restaurar Versão

Não deverá ser obrigatório utilizar drag and drop.

Todas as alterações deverão possuir alternativa por clique, seleção e controles de posição.

10. Página — Dashboards Compartilhados
ID
BI-DAS-003
Tipo
Lista
Objetivo

Consultar dashboards compartilhados com o usuário, equipe, departamento ou perfil.

11. Página — Catálogo de Dashboards
ID
BI-CAT-001
Tipo
Galeria
Categorias
Executivo

Comercial

Projetos

Suprimentos

Produção

Qualidade

Logística

Pós-venda

Financeiro

RH

Fiscal

Operacional

Personalizado
12. Página — Indicadores
ID
BI-KPI-001
Tipo
Dashboard Analítico
Objetivo

Consultar indicadores autorizados e acompanhar resultados.

Informações
Código

Nome

Descrição

Categoria

Valor Atual

Meta

Variação

Tendência

Período

Última Atualização

Responsável

Status
13. Página — Catálogo de Indicadores
ID
BI-KPI-002
Tipo
Lista
Objetivo

Manter a definição oficial dos indicadores.

Campos
Código

Nome

Descrição

Objetivo

Categoria

Módulo de Origem

Entidade de Origem

Métrica

Fórmula

Unidade

Moeda

Periodicidade

Dimensões

Filtros Permitidos

Regime de Reconhecimento

Responsável

Versão

Vigência

Status
Status
Rascunho

Em Validação

Aprovado

Publicado

Substituído

Arquivado
Ações
Novo Indicador

Editar

Duplicar

Validar

Aprovar

Publicar

Criar Nova Versão

Comparar Versões

Testar Cálculo

Arquivar
14. Página — Cadastro do Indicador
ID
BI-KPI-003
Tipo
Cadastro
Abas
Geral

Definição

Fonte

Fórmula

Dimensões

Filtros

Metas

Permissões

Validação

Versões

Utilização

Histórico

Auditoria
Aba Definição
Nome Técnico

Nome de Exibição

Descrição

Pergunta Gerencial Respondida

Interpretação

Unidade

Sentido Favorável

Casas Decimais

Formato

Periodicidade
Aba Fonte
Módulo

Entidade

Tabela Analítica

Campo de Data

Campo de Valor

Relacionamentos

Condições de Inclusão

Condições de Exclusão
Aba Fórmula
Expressão

Numerador

Denominador

Agregação

Tratamento de Nulos

Tratamento de Divisão por Zero

Arredondamento

Regime

Versão
Aba Validação
Período de Teste

Resultado Esperado

Resultado Calculado

Diferença

Amostra

Responsável

Aprovação
15. Página — Metas
ID
BI-MET-001
Tipo
Lista
Campos
Indicador

Período

Empresa

Filial

Departamento

Equipe

Responsável

Valor da Meta

Faixa de Atenção

Faixa Crítica

Status
Ações
Nova Meta

Editar

Distribuir Meta

Importar

Solicitar Aprovação

Aprovar

Revisar

Cancelar

Exportar
16. Página — Alertas Gerenciais
ID
BI-ALE-001
Tipo
Kanban
Etapas
Novo

Reconhecido

Em Análise

Ação Criada

Monitorando

Resolvido

Ignorado com Justificativa
Tipos
Meta não Atingida

Desvio Crítico

Tendência Negativa

Prazo em Risco

Valor Anormal

Dado Desatualizado

Falha de Integração

Inconsistência de Dados
Ações
Reconhecer

Abrir Indicador

Abrir Origem

Criar Tarefa

Notificar Responsável

Definir Prazo

Resolver

Ignorar
17. Página — Consultas Analíticas
ID
BI-CON-001
Tipo
Consulta
Objetivo

Permitir consultas controladas sobre dados autorizados.

Elementos
Fonte

Métricas

Dimensões

Filtros

Ordenação

Agrupamento

Limite

Período

Visualização
Ações
Executar

Salvar Consulta

Duplicar

Adicionar ao Dashboard

Exportar

Compartilhar

Agendar
18. Página — Exploração de Dados
ID
BI-EXP-001
Tipo
Painel Analítico
Objetivo

Permitir exploração progressiva dos dados sem alterar a origem.

Recursos
Detalhamento

Agrupamento

Segmentação

Comparação

Ordenação

Filtros Encadeados

Drill-down

Drill-through

Visualização da Origem

Amostragem

Exportação
19. Página — Comparação de Períodos
ID
BI-CMP-001
Tipo
Dashboard Analítico
Comparações
Período Atual x Anterior

Mês x Mês Anterior

Ano x Ano Anterior

Realizado x Meta

Realizado x Orçado

Planejado x Realizado

Empresa x Empresa

Filial x Filial

Equipe x Equipe
20. Página — Análise de Tendências
ID
BI-TEN-001
Tipo
Dashboard Analítico
Objetivo

Identificar direção, ritmo e estabilidade dos indicadores.

Informações
Série Histórica

Média Móvel

Variação

Sazonalidade

Tendência

Pontos Anormais

Projeção

Intervalo de Confiança quando Aplicável
21. Página — Rankings
ID
BI-RAN-001
Tipo
Lista Analítica
Exemplos
Clientes por Receita

Clientes por Margem

Vendedores por Conversão

Projetos por Rentabilidade

Fornecedores por Desempenho

Materiais por Consumo

Produtos por Venda

Equipes por Produtividade

Operadores por Eficiência

Técnicos por Solução

Centros de Custo por Despesa
22. Página — Projeções
ID
BI-PRJ-001
Tipo
Dashboard Analítico
Objetivo

Apresentar projeções calculadas com base em dados históricos, planos e premissas autorizadas.

Tipos
Receita

Fluxo de Caixa

Demanda

Compras

Consumo de Materiais

Carga Produtiva

Entregas

Inadimplência

Custos

Headcount
Regras

Projeções deverão informar:

Método

Período Base

Premissas

Data do Cálculo

Margem de Incerteza

Responsável

Versão
23. Página — Cenários
ID
BI-CEN-002
Tipo
Simulador
Exemplos
Crescimento de Vendas

Alteração de Margem

Aumento de Custos

Mudança de Prazo

Aumento de Capacidade

Contratação de Equipe

Compra de Máquina

Redução de Perdas

Redução de Inadimplência

Alteração de Preços
Regra

Cenários não deverão alterar dados oficiais.

24. Página — Relatórios Gerenciais
ID
BI-REL-001
Tipo
Lista
Ações
Novo Relatório

Abrir

Executar

Editar

Duplicar

Compartilhar

Agendar

Exportar PDF

Exportar Planilha

Arquivar
25. Página — Relatórios Agendados
ID
BI-AGE-001
Tipo
Lista
Campos
Relatório

Destinatários

Formato

Periodicidade

Dia

Hora

Fuso Horário

Filtros Fixos

Última Execução

Próxima Execução

Status
26. Página — Exportações
ID
BI-EXR-001
Tipo
Lista
Formatos
PDF

XLSX

CSV

JSON

Imagem
Status
Solicitada

Na Fila

Processando

Concluída

Com Erro

Expirada

Cancelada
27. Página — Dados Analíticos
ID
BI-DAD-001
Tipo
Lista Técnica
Objetivo

Consultar conjuntos analíticos disponíveis sem expor detalhes não autorizados da infraestrutura.

Informações
Nome

Domínio

Descrição

Granularidade

Período Disponível

Última Atualização

Responsável

Qualidade

Status
28. Página — Fontes de Dados
ID
BI-FON-001
Tipo
Lista Técnica
Tipos
Módulo Interno

Banco Operacional

Tabela Analítica

Visão Materializada

Arquivo Importado

API Autorizada

Integração Externa
Status
Ativa

Em Validação

Desatualizada

Com Falha

Suspensa

Arquivada
29. Página — Atualizações
ID
BI-ATU-001
Tipo
Painel Técnico
Objetivo

Acompanhar atualizações dos conjuntos analíticos.

Informações
Fonte

Processo

Início

Término

Duração

Registros Lidos

Registros Processados

Registros Rejeitados

Última Atualização

Próxima Atualização

Status

Erro
30. Página — Qualidade dos Dados
ID
BI-QLD-001
Tipo
Dashboard Analítico
Indicadores
Completude

Consistência

Atualidade

Unicidade

Validade

Integridade Referencial

Registros Rejeitados

Campos Nulos

Duplicidades

Divergências
Ações
Abrir Ocorrência

Abrir Origem

Atribuir Responsável

Definir Prazo

Reprocessar

Resolver

Ignorar com Justificativa
31. Página — Dicionário de Dados
ID
BI-DIC-001
Tipo
Catálogo
Informações
Domínio

Entidade

Campo

Nome de Exibição

Descrição

Tipo

Unidade

Sensibilidade

Origem

Responsável

Status
32. Página — Linhagem de Dados
ID
BI-LIN-001
Tipo
Diagrama
Objetivo

Mostrar o caminho entre a origem operacional e o indicador final.

Fluxo
Módulo de Origem

↓

Entidade

↓

Extração

↓

Transformação

↓

Conjunto Analítico

↓

Indicador

↓

Dashboard ou Relatório
33. Página — Permissões Analíticas
ID
BI-PER-001
Tipo
Matriz
Dimensões
Usuário

Perfil

Equipe

Departamento

Empresa

Filial

Dashboard

Indicador

Conjunto de Dados

Campo Sensível

Exportação
34. Página — Auditoria do BI
ID
BI-AUD-001
Tipo
Lista
Eventos Auditados
Dashboard Criado

Dashboard Editado

Dashboard Publicado

Indicador Criado

Fórmula Alterada

Meta Alterada

Permissão Alterada

Relatório Exportado

Consulta Executada

Dado Sensível Acessado

Agendamento Criado

Processamento Reexecutado
35. BI Comercial
ID
BI-COM-001
Indicadores
Leads Criados

Leads Qualificados

Oportunidades

Taxa de Conversão

Tempo Médio de Conversão

Propostas Enviadas

Propostas Aprovadas

Propostas Perdidas

Motivos de Perda

Valor do Pipeline

Receita por Vendedor

Receita por Cliente

Ticket Médio

Margem por Venda

Prazo Médio de Fechamento

Previsão de Vendas
36. BI de Projetos
ID
BI-PRO-001
Indicadores
Projetos Ativos

Projetos Atrasados

Tempo por Etapa

Revisões por Projeto

Pendências Técnicas

Horas Planejadas

Horas Realizadas

Projetos por Responsável

Projetos por Ambiente

Alterações após Aprovação

Impacto das Alterações
37. BI de Orçamentos
ID
BI-ORC-001
Indicadores
Orçamentos Criados

Orçamentos Enviados

Orçamentos Aprovados

Taxa de Aprovação

Prazo de Elaboração

Valor Orçado

Margem Prevista

Descontos

Revisões

Orçamentos Expirados

Diferença Orçado x Realizado
38. BI de Compras
ID
BI-CMP-002
Indicadores
Compras no Período

Economia de Negociação

Prazo Médio de Compra

Atrasos de Fornecedores

Compras Emergenciais

Compras sem Cotação

Variação de Preços

Desempenho por Fornecedor

Itens Pendentes

Valor Comprometido
39. BI de Estoque
ID
BI-EST-001
Indicadores
Valor do Estoque

Giro

Cobertura

Rupturas

Excessos

Materiais sem Movimento

Perdas

Sobras

Acuracidade

Reservas

Itens em Quarentena

Consumo por Projeto

Consumo Previsto x Real
40. BI de PCP
ID
BI-PCP-001
Indicadores
Ordens Planejadas

Ordens Liberadas

Aderência ao Plano

Carga por Recurso

Capacidade Utilizada

Sobrecarga

Ociosidade

Gargalos

Reprogramações

Materiais em Falta

Ordens em Risco
41. BI de Produção
ID
BI-PRD-001
Indicadores
Ordens em Produção

Ordens Concluídas

Produtividade

Eficiência

Tempo por Fase

Tempo por Operação

Perdas

Retrabalhos

Paradas

Pausas

Peças Produzidas

Peças Rejeitadas

Planejado x Realizado
42. BI de Qualidade
ID
BI-QUA-001
Indicadores
Inspeções

Aprovações

Reprovações

Não Conformidades

Reincidências

Retrabalhos

Refugos

Tempo de Resolução

Custo da Não Qualidade

Qualidade por Fornecedor

Qualidade por Setor
43. BI de Expedição
ID
BI-EXP-002
Indicadores
Entregas Planejadas

Entregas Realizadas

Entregas no Prazo

Atrasos

Avarias

Devoluções

Ocorrências

Custo por Entrega

Quilometragem

Desempenho por Veículo

Desempenho por Transportadora
44. BI de Instalação
ID
BI-INS-001
Indicadores
Instalações Planejadas

Instalações Concluídas

Conclusão na Primeira Visita

Tempo de Instalação

Tempo de Deslocamento

Pendências

Danos

Retrabalhos

Produtividade por Equipe

Custo por Instalação

Satisfação do Cliente
45. BI de Assistência Técnica
ID
BI-AST-001
Indicadores
Chamados Abertos

Chamados Encerrados

Tempo de Primeira Resposta

Tempo de Solução

Solução na Primeira Visita

Reincidência

Causas

Responsabilidades

Custos

Cumprimento de SLA

Satisfação do Cliente
46. BI Financeiro
ID
BI-FIN-001
Indicadores
Receita

Despesa

Resultado

Fluxo de Caixa

Saldo

Contas a Receber

Contas a Pagar

Inadimplência

Margem

DRE

Orçado x Realizado

Custo por Centro

Rentabilidade por Projeto

Prazo Médio de Recebimento

Prazo Médio de Pagamento

Necessidade de Capital
47. BI de Recursos Humanos
ID
BI-RH-001
Indicadores
Headcount

Admissões

Desligamentos

Turnover

Absenteísmo

Horas Extras

Banco de Horas

Faltas

Atrasos

Custo de Pessoal

Treinamentos

Avaliações

Acidentes

Incidentes

Satisfação Interna
48. BI Fiscal
ID
BI-FIS-001
Indicadores
Documentos Emitidos

Documentos Recebidos

Taxa de Rejeição

Cancelamentos

Pendências

Tributos

Retenções

Apurações

Obrigações

Divergências

Fechamentos

Risco Fiscal
49. Templates
ID
BI-TMP-001
Tipos
Dashboard Executivo

Dashboard Operacional

Dashboard Financeiro

Dashboard Comercial

Relatório Gerencial

Relatório Comparativo

Ranking

Análise de Tendência

Alerta

Agendamento
50. Configurações
ID
BI-CFG-001
Configurações
Categorias de Dashboard

Categorias de Indicador

Unidades

Moedas

Casas Decimais

Períodos Padrão

Comparações Padrão

Atualizações

Cache

Limites de Consulta

Limites de Exportação

Retenção de Exportações

Permissões

Campos Sensíveis

Alertas

Agendamentos

Templates

Notificações

Integrações
51. Dialogs
BI-DLG-001 Novo Dashboard

BI-DLG-002 Editar Dashboard

BI-DLG-003 Adicionar Componente

BI-DLG-004 Configurar Componente

BI-DLG-005 Selecionar Indicador

BI-DLG-006 Selecionar Fonte

BI-DLG-007 Configurar Filtro

BI-DLG-008 Configurar Período

BI-DLG-009 Comparar Períodos

BI-DLG-010 Compartilhar Dashboard

BI-DLG-011 Publicar Dashboard

BI-DLG-012 Restaurar Versão

BI-DLG-013 Novo Indicador

BI-DLG-014 Editar Fórmula

BI-DLG-015 Testar Indicador

BI-DLG-016 Aprovar Indicador

BI-DLG-017 Publicar Indicador

BI-DLG-018 Nova Meta

BI-DLG-019 Distribuir Meta

BI-DLG-020 Aprovar Meta

BI-DLG-021 Novo Alerta

BI-DLG-022 Reconhecer Alerta

BI-DLG-023 Criar Ação

BI-DLG-024 Nova Consulta

BI-DLG-025 Salvar Consulta

BI-DLG-026 Adicionar ao Dashboard

BI-DLG-027 Criar Cenário

BI-DLG-028 Editar Premissas

BI-DLG-029 Nova Projeção

BI-DLG-030 Novo Relatório

BI-DLG-031 Agendar Relatório

BI-DLG-032 Exportar PDF

BI-DLG-033 Exportar Planilha

BI-DLG-034 Selecionar Destinatários

BI-DLG-035 Registrar Fonte

BI-DLG-036 Executar Atualização

BI-DLG-037 Reprocessar Dados

BI-DLG-038 Criar Ocorrência de Qualidade

BI-DLG-039 Editar Dicionário

BI-DLG-040 Configurar Permissão

BI-DLG-041 Solicitar Acesso

BI-DLG-042 Aprovar Acesso

BI-DLG-043 Arquivar Dashboard

BI-DLG-044 Arquivar Indicador

BI-DLG-045 Importar Metas

BI-DLG-046 Exportar Dados

BI-DLG-047 Cancelar Processamento

BI-DLG-048 Limpar Cache

BI-DLG-049 Gerar Link Interno

BI-DLG-050 Duplicar Relatório
52. Wizards
BI-WIZ-001 Assistente de Dashboard

BI-WIZ-002 Assistente de Indicador

BI-WIZ-003 Assistente de Meta

BI-WIZ-004 Assistente de Alerta

BI-WIZ-005 Assistente de Consulta Analítica

BI-WIZ-006 Assistente de Relatório

BI-WIZ-007 Assistente de Agendamento

BI-WIZ-008 Assistente de Projeção

BI-WIZ-009 Assistente de Cenário

BI-WIZ-010 Assistente de Fonte de Dados

BI-WIZ-011 Assistente de Permissões

BI-WIZ-012 Assistente de Configuração Inicial
53. Componentes Específicos
BI-CPT-001 Grade de Dashboard

BI-CPT-002 Cartão de Indicador

BI-CPT-003 Cartão Comparativo

BI-CPT-004 Gráfico Temporal

BI-CPT-005 Gráfico de Categorias

BI-CPT-006 Funil

BI-CPT-007 Medidor

BI-CPT-008 Mapa Analítico

BI-CPT-009 Tabela Analítica

BI-CPT-010 Matriz Analítica

BI-CPT-011 Ranking

BI-CPT-012 Editor de Filtros

BI-CPT-013 Seletor de Período

BI-CPT-014 Comparador de Períodos

BI-CPT-015 Editor de Fórmula

BI-CPT-016 Testador de Indicador

BI-CPT-017 Painel de Metas

BI-CPT-018 Painel de Alertas

BI-CPT-019 Explorador de Dados

BI-CPT-020 Simulador de Cenários

BI-CPT-021 Painel de Atualizações

BI-CPT-022 Painel de Qualidade dos Dados

BI-CPT-023 Diagrama de Linhagem

BI-CPT-024 Matriz de Permissões

Todos os componentes deverão utilizar exclusivamente o theme_design.

Não será permitido hardcode de:

Cores

Fontes

Tamanhos

Margens

Espaçamentos

Bordas

Sombras

Ícones

Estilos de gráficos

Estados
54. Eventos
BIDashboardCreated

BIDashboardUpdated

BIDashboardPublished

BIDashboardShared

BIDashboardArchived

BIIndicatorCreated

BIIndicatorValidated

BIIndicatorApproved

BIIndicatorPublished

BIIndicatorVersionCreated

BIMetricCalculated

BIMetricCalculationFailed

BITargetCreated

BITargetApproved

BITargetUpdated

BIAlertCreated

BIAlertAcknowledged

BIAlertResolved

BIQueryCreated

BIQueryExecuted

BIQueryFailed

BIReportCreated

BIReportGenerated

BIReportScheduled

BIReportDelivered

BIExportRequested

BIExportCompleted

BIExportFailed

BIDataSourceRegistered

BIDataRefreshStarted

BIDataRefreshCompleted

BIDataRefreshFailed

BIDataQualityIssueCreated

BIDataQualityIssueResolved

BIPermissionGranted

BIPermissionRevoked

BISensitiveDataAccessed

BICacheRefreshed
55. Automações
Dado operacional alterado

↓

Registrar necessidade de atualização

↓

Atualizar conjunto analítico conforme política

↓

Recalcular indicadores afetados

↓

Atualizar dashboards
Indicador ultrapassa faixa crítica

↓

Criar alerta

↓

Identificar responsáveis

↓

Enviar notificação

↓

Registrar evento
Relatório agendado

↓

Aplicar permissões do proprietário

↓

Executar consulta

↓

Gerar arquivo

↓

Enviar aos destinatários autorizados

↓

Registrar entrega
Falha de atualização

↓

Registrar erro

↓

Marcar dados como desatualizados

↓

Notificar responsáveis

↓

Agendar nova tentativa
Problema de qualidade detectado

↓

Criar ocorrência

↓

Vincular fonte

↓

Calcular impacto

↓

Notificar responsável pelo dado
56. Integrações
Todos os Módulos Operacionais

Administração

Usuários

Permissões

Auditoria

Workflow

Notificações

Documentos

Agenda

IA

Sincronização

Exportações

Email
57. Permissões
bi.dashboard.read

bi.dashboard.create

bi.dashboard.update

bi.dashboard.publish

bi.dashboard.share

bi.dashboard.archive

bi.dashboard.manage_layout

bi.indicator.read

bi.indicator.create

bi.indicator.update

bi.indicator.validate

bi.indicator.approve

bi.indicator.publish

bi.indicator.manage_version

bi.target.read

bi.target.create

bi.target.update

bi.target.approve

bi.alert.read

bi.alert.manage

bi.query.read

bi.query.create

bi.query.execute

bi.query.share

bi.exploration.use

bi.projection.read

bi.projection.create

bi.scenario.read

bi.scenario.create

bi.report.read

bi.report.create

bi.report.update

bi.report.schedule

bi.report.export

bi.export.request

bi.export.download

bi.data_source.read

bi.data_source.manage

bi.data_refresh.read

bi.data_refresh.execute

bi.data_quality.read

bi.data_quality.manage

bi.dictionary.read

bi.dictionary.manage

bi.lineage.read

bi.permission.read

bi.permission.manage

bi.audit.read

bi.sensitive_data.read

bi.financial_data.read

bi.salary_data.read

bi.cost_data.read

bi.configuration.manage
58. Relatórios e Documentos Gerados
Dashboard Executivo

Relatório Gerencial

Relatório Comercial

Relatório de Projetos

Relatório de Orçamentos

Relatório de Compras

Relatório de Estoque

Relatório de PCP

Relatório de Produção

Relatório de Qualidade

Relatório de Expedição

Relatório de Instalação

Relatório de Assistência

Relatório Financeiro

Relatório de RH

Relatório Fiscal

Relatório de Metas

Relatório de Alertas

Relatório Comparativo

Relatório de Tendências

Relatório de Projeções

Relatório de Qualidade dos Dados

Dicionário de Indicadores

Dicionário de Dados

Relatório de Auditoria do BI
59. Recursos de Inteligência Artificial
Interpretar perguntas em linguagem natural

Sugerir indicadores

Sugerir filtros

Sugerir visualizações

Resumir dashboards

Explicar variações

Detectar anomalias

Detectar tendências

Identificar correlações

Sugerir causas prováveis

Gerar narrativas gerenciais

Sugerir alertas

Ajudar a criar consultas

Ajudar a localizar dados

Comparar períodos

Resumir relatórios

Criar rascunhos de apresentações

Explicar fórmulas

A IA não poderá:

Conceder acesso

Expor dados sensíveis

Alterar dados operacionais

Publicar indicador sem aprovação

Alterar fórmula publicada

Criar meta oficial sem confirmação

Executar ação operacional automaticamente

Apresentar projeção como fato confirmado
60. Regras de Segurança
O BI deverá reutilizar o sistema central de autenticação.
O BI deverá reutilizar o sistema central de permissões.
O BI deverá aplicar segurança por linha quando necessário.
O BI deverá aplicar segurança por campo para dados sensíveis.
Filtros de Tenant não poderão ser removidos pelo usuário.
Exportações deverão ser auditadas.
Acesso a salários deverá exigir permissão específica.
Acesso a custos deverá exigir permissão específica.
Acesso a dados pessoais deverá respeitar as permissões do RH.
Dashboards compartilhados não poderão ampliar permissões do destinatário.
Links internos deverão exigir autenticação.
Arquivos exportados deverão possuir prazo de retenção configurável.
61. Regras de Desempenho
Dashboards deverão utilizar paginação e carregamento controlado.
Consultas extensas deverão possuir limites.
Agregações frequentes deverão ser pré-calculadas quando necessário.
Atualizações não deverão bloquear a interface.
Falhas de atualização não deverão apagar o último resultado válido.
O usuário deverá ser informado sobre a data da última atualização.
Consultas canceladas deverão liberar recursos.
Gráficos não deverão carregar milhões de pontos diretamente.
Detalhamentos deverão ser paginados.
Exportações extensas deverão ser processadas por fila.
62. Observações Arquiteturais

O BI deverá ser uma camada de leitura e análise.

A interface não deverá consultar modelos operacionais de maneira desorganizada.

Deverão existir contratos analíticos claros entre:

Módulo de Origem

Serviço de Extração

Modelo Analítico

Serviço de Indicadores

API ou Serviço de Consulta

Interface do BI

O BI deverá suportar inicialmente o banco local e a arquitetura desktop, mas a solução não deverá impedir futura utilização de:

PostgreSQL

Supabase

Data Warehouse

API Analítica

Processamento em Servidor

Painéis Web

A implementação inicial deverá evitar dependência obrigatória de infraestrutura externa.

63. INSTRUÇÕES DIRETAS PARA O CLAUDE — IMPLEMENTAÇÃO
63.1 Papel do Claude

Você atuará como desenvolvedor responsável por implementar o módulo conforme este documento e a arquitetura técnica oficial do ORGANIZEG3.

Você não deverá reinterpretar o escopo livremente.

Você deverá seguir os contratos, nomes, padrões e restrições do projeto.

63.2 Regras Obrigatórias
Antes de alterar qualquer arquivo, leia o arquivo inteiro.
Não remova funções existentes sem demonstrar que estão obsoletas e sem substituir todas as chamadas.
Não entregue trechos incompletos quando for solicitado um arquivo completo.
Quando alterar um arquivo, devolva o arquivo inteiro atualizado.
Preserve compatibilidade com o código existente sempre que tecnicamente possível.
Não crie uma segunda arquitetura paralela.
Não acesse o banco diretamente pelas páginas.
Utilize as camadas oficiais:
Page ou View

Controller ou ViewModel

Application Service

Repository

Domain Model

Database
Utilize SQLAlchemy conforme o padrão oficial do projeto.
Utilize migrations para alterações no banco.
Todas as entidades deverão possuir os campos-base definidos na arquitetura.
Todas as consultas deverão respeitar tenant_id.
Utilize UUID quando definido pela arquitetura.
Utilize exclusão lógica quando definida.
Utilize versionamento otimista quando definido.
Registre eventos por meio do barramento central.
Registre auditoria pelo serviço central.
Utilize o serviço central de permissões.
Utilize o serviço central de logs.
Utilize o tratamento central de erros.
Não coloque regras de negócio complexas dentro de widgets PySide6.
Não use estilos hardcoded.
Obtenha todos os estilos pelo theme_design.
Não crie cores diretamente em páginas ou componentes.
Não altere datas, filtros ou registros por drag and drop como única forma de interação.
Toda ação importante deverá possuir alternativa por clique e formulário.
Não execute consultas analíticas pesadas na thread principal da interface.
Use worker ou serviço assíncrono compatível com o projeto para processamentos extensos.
Não exponha dados sem verificar permissões.
Não permita que dashboards compartilhados ampliem acesso.
63.3 Ordem de Implementação do BI

O BI não deverá ser implementado antes da fundação técnica.

Quando autorizado, implementar nesta ordem:

1. Modelos e migrations do catálogo de indicadores

2. Repositórios

3. Serviços de consulta

4. Serviço de cálculo de indicadores

5. Serviço de permissões analíticas

6. Componentes visuais básicos

7. Catálogo de indicadores

8. Dashboard simples

9. Metas

10. Alertas

11. Exportações

12. Relatórios agendados

13. Qualidade dos dados

14. Linhagem

15. Recursos de IA
63.4 Primeira Entrega Vertical do BI

A primeira entrega deverá conter:

Cadastro de Indicador

Lista de Indicadores

Visualização do Indicador

Cálculo de um Indicador Simples

Filtro por Período

Filtro por Tenant

Filtro por Empresa

Permissões

Auditoria

Testes

Migration

Dados de Demonstração Opcionais

O indicador inicial deverá ser simples e rastreável, por exemplo:

Quantidade de Clientes Ativos

ou:

Quantidade de Orçamentos no Período

Não iniciar pelo dashboard executivo completo.

63.5 Formato das Entregas do Claude

Cada entrega deverá informar:

Objetivo da alteração

Arquivos criados

Arquivos alterados

Migrations criadas

Dependências adicionadas

Decisões técnicas

Riscos

Como testar

Resultado esperado

Quando o usuário pedir código completo:

Entregar cada arquivo completo

Informar o caminho exato

Não usar reticências

Não omitir imports

Não omitir classes auxiliares necessárias

Não remover recursos existentes

Não responder somente com diff
63.6 Critérios de Aceite

Uma funcionalidade somente estará concluída quando possuir:

Modelo

Migration

Repository

Service

Permissões

Auditoria

Interface

Validações

Tratamento de Erros

Testes

Documentação Breve

Integração com Navegação
64. Próxima Etapa
ETAPA 03-R

Catálogo Completo de Páginas

Workflow e Automações