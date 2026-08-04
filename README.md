\# OrganizeG3



> Plataforma operacional inteligente para empresas orientadas a processos.



\---



| Propriedade            | Valor                                        |

| ---------------------- | -------------------------------------------- |

| Produto                | OrganizeG3                                   |

| Geração                | Next                                         |

| Status                 | Em desenvolvimento                           |

| Arquitetura            | Domain-Driven, modular e orientada a eventos |

| Backend inicial        | Python                                       |

| Banco de dados         | PostgreSQL / Supabase                        |

| Aplicações             | API, Desktop e PWA                           |

| Tema visual            | Exclusivamente escuro                        |

| Idioma da documentação | Português                                    |

| Convenção do código    | Inglês                                       |



\---



\# 1. Visão geral



O OrganizeG3 é uma plataforma de gestão operacional criada inicialmente para empresas que trabalham com produção sob encomenda.



A plataforma conecta:



\* pessoas;

\* processos;

\* clientes;

\* documentos;

\* operações;

\* máquinas;

\* estoques;

\* eventos;

\* indicadores;

\* automações;

\* Inteligência Artificial.



O OrganizeG3 não deverá ser limitado a um único segmento industrial. Sua arquitetura deve permitir adaptação por configuração para marcenarias, serralherias, marmorarias, fábricas de móveis, pequenas indústrias e outras empresas organizadas por processos.



\---



\# 2. Objetivo desta geração



Esta geração do OrganizeG3 está sendo construída a partir de uma nova base arquitetural.



O objetivo é substituir gradualmente a arquitetura anterior por uma plataforma:



\* multiempresa;

\* configurável;

\* modular;

\* auditável;

\* orientada a eventos;

\* preparada para funcionamento offline;

\* preparada para Desktop e PWA;

\* preparada para integrações;

\* preparada para Inteligência Artificial.



O OrganizeG3 anterior deverá ser preservado como referência funcional e como origem para futura migração de dados.



\---



\# 3. Princípios fundamentais



\## 3.1 Domínio antes da tecnologia



As regras do negócio devem ser modeladas antes das telas, tabelas ou integrações.



O domínio não poderá depender de:



\* FastAPI;

\* SQLAlchemy;

\* Supabase;

\* PySide6;

\* React;

\* navegador;

\* sistema operacional.



Tecnologias podem ser substituídas. O domínio permanece.



\## 3.2 Uma única regra de negócio



Desktop, PWA, API, automações, integrações e agentes de IA deverão utilizar os mesmos casos de uso.



Nenhuma interface poderá implementar regras de negócio exclusivas.



\## 3.3 Configuração acima de customização



Sempre que possível, diferenças entre empresas deverão ser resolvidas por configuração.



Exemplos:



\* workflows;

\* etapas;

\* operações;

\* checklists;

\* formulários;

\* motivos de pausa;

\* perfis;

\* permissões;

\* filiais;

\* setores;

\* estoques;

\* máquinas.



\## 3.4 Eventos e auditoria são distintos



Eventos registram fatos do domínio.



Auditorias registram ações administrativas e técnicas.



Esses registros possuem propósitos diferentes e não poderão ser tratados como a mesma entidade.



\## 3.5 Capabilities acima de módulos



O OrganizeG3 evolui através de capacidades reutilizáveis.



Exemplos:



\* Workflow;

\* Forms;

\* Documents;

\* Search;

\* Scheduling;

\* Automation;

\* Analytics;

\* AI Skills.



Uma capacidade poderá ser utilizada por diferentes áreas da empresa.



\## 3.6 Nenhum estilo visual hardcoded



Toda definição visual deve ser centralizada no sistema oficial de design.



Telas e componentes não poderão declarar diretamente:



\* cores;

\* fontes;

\* ícones;

\* imagens;

\* espaçamentos;

\* tamanhos;

\* bordas;

\* sombras;

\* animações;

\* estilos de estado.



Essas definições deverão vir dos tokens e componentes oficiais do projeto.



\---



\# 4. Estrutura do repositório



```text

PROGRAMA/

├── apps/

│   ├── api/

│   ├── desktop/

│   └── pwa/

├── packages/

│   ├── application/

│   ├── contracts/

│   ├── design\_tokens/

│   ├── domain/

│   └── shared/

├── database/

│   ├── functions/

│   ├── migrations/

│   ├── policies/

│   └── seeds/

├── theme\_design/

│   ├── assets/

│   ├── components/

│   ├── icons/

│   ├── themes/

│   └── tokens/

├── docs/

├── scripts/

├── tests/

├── .env.example

├── .gitignore

├── AI\_DEVELOPMENT\_GUIDE.md

├── alembic.ini

├── docker-compose.yml

├── pyproject.toml

└── README.md

```



\---



\# 5. Responsabilidades principais



\## `apps/api`



Interface HTTP oficial da plataforma.



Responsável por:



\* receber requisições;

\* autenticar;

\* identificar o contexto da empresa;

\* validar contratos;

\* executar casos de uso;

\* converter resultados em respostas HTTP.



A API não contém regras de negócio.



\## `apps/desktop`



Aplicação administrativa para Windows.



Responsável inicialmente por:



\* cadastros;

\* configurações;

\* gestão comercial;

\* gestão produtiva;

\* relatórios;

\* administração.



O Desktop consome a Platform API.



\## `apps/pwa`



Aplicação operacional para celulares, tablets e navegadores.



Responsável inicialmente por:



\* consultar atividades atribuídas;

\* iniciar operações;

\* pausar operações;

\* retomar operações;

\* finalizar operações;

\* preencher checklists;

\* consultar documentos;

\* registrar ocorrências;

\* enviar fotos;

\* receber notificações.



\## `packages/domain`



Contém o domínio puro.



Inclui:



\* entidades;

\* agregados;

\* objetos de valor;

\* regras de negócio;

\* eventos de domínio;

\* políticas;

\* especificações.



Não poderá importar código de infraestrutura ou de interface.



\## `packages/application`



Contém os casos de uso.



Inclui:



\* comandos;

\* consultas;

\* handlers;

\* portas;

\* autorização;

\* unidade de trabalho;

\* coordenação de transações.



\## `packages/contracts`



Contém contratos compartilháveis.



Inclui:



\* DTOs;

\* schemas;

\* mensagens;

\* eventos de integração;

\* contratos públicos.



\## `packages/shared`



Contém recursos técnicos pequenos e reutilizáveis que não pertencem a um domínio específico.



Não deverá se transformar em um local para código sem responsabilidade definida.



\## `packages/design\_tokens`



Contém tokens visuais independentes da tecnologia.



Os mesmos tokens deverão orientar Desktop e PWA.



\## `theme\_design`



Contém a implementação visual oficial da aplicação Desktop.



O PWA terá uma implementação própria baseada nos mesmos design tokens.



\## `database`



Contém todos os artefatos oficiais de banco:



\* migrações;

\* funções;

\* políticas RLS;

\* seeds.



Alterações manuais no banco não serão consideradas parte oficial do projeto.



\---



\# 6. Tecnologias iniciais



\## Backend e domínio



\* Python 3.12 ou superior;

\* FastAPI;

\* Pydantic;

\* SQLAlchemy 2;

\* Alembic;

\* PostgreSQL;

\* Supabase.



\## Qualidade



\* Ruff;

\* mypy;

\* pytest;

\* pytest-cov.



\## Aplicações



\* Desktop: PySide6;

\* PWA: tecnologia a ser definida em documento próprio;

\* API: FastAPI.



As escolhas poderão ser revisadas por ADR.



\---



\# 7. Ambiente de desenvolvimento



\## Criar o ambiente virtual



```powershell

python -m venv .venv

```



\## Ativar no PowerShell



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\## Atualizar o instalador



```powershell

python -m pip install --upgrade pip

```



\## Instalar o projeto em modo de desenvolvimento



```powershell

pip install -e ".\[dev]"

```



\---



\# 8. Execução inicial da API



Após a criação dos arquivos básicos:



```powershell

uvicorn organizeg3\_api.main:app --reload

```



A API deverá disponibilizar inicialmente:



```text

GET /health

```



Resposta esperada:



```json

{

&#x20; "status": "healthy",

&#x20; "service": "organizeg3-api"

}

```



\---



\# 9. Configuração



Credenciais e configurações sensíveis deverão ser fornecidas por variáveis de ambiente.



Copie:



```text

.env.example

```



para:



```text

.env

```



Nunca versionar o arquivo `.env`.



\---



\# 10. Banco de dados



O banco oficial será PostgreSQL hospedado no Supabase.



Princípios obrigatórios:



\* UUID como identificador;

\* isolamento por `tenant\_id`;

\* Row Level Security;

\* migrações formais;

\* eventos imutáveis;

\* auditoria independente;

\* armazenamento de arquivos fora do banco;

\* concorrência otimista;

\* exclusão lógica quando aplicável.



\---



\# 11. Design System



O OrganizeG3 utilizará exclusivamente tema escuro.



Nenhum arquivo de página, tela ou componente poderá conter valores visuais hardcoded.



Exemplo proibido:



```python

button.setStyleSheet(

&#x20;   "background-color: #3B82F6; color: #FFFFFF; border-radius: 8px;"

)

```



Exemplo esperado:



```python

button = PrimaryButton(

&#x20;   text="Salvar",

&#x20;   icon=Icons.SAVE,

)

```



A aparência do componente será definida pelo sistema oficial de design.



\---



\# 12. Desenvolvimento assistido por IA



Agentes de IA deverão ler obrigatoriamente:



```text

AI\_DEVELOPMENT\_GUIDE.md

```



antes de criar ou alterar código.



Código gerado por IA deverá:



\* respeitar a arquitetura;

\* utilizar os contratos existentes;

\* evitar duplicação;

\* incluir testes;

\* não criar estilos hardcoded;

\* não alterar o banco sem migração;

\* não contornar a Application Layer;

\* não acessar dados de outra empresa;

\* documentar decisões relevantes.



\---



\# 13. Estado atual



A estrutura inicial do repositório está sendo criada.



Primeiras entregas:



1\. configuração do projeto;

2\. recursos compartilhados;

3\. base do domínio;

4\. organização multiempresa;

5\. identidade e permissões;

6\. persistência;

7\. autenticação;

8\. eventos e auditoria;

9\. workflow;

10\. operações e execuções.



\---



\# 14. Licença



A licença do OrganizeG3 será definida em documento próprio.



Até a definição formal, o código deverá ser tratado como proprietário e não poderá ser distribuído sem autorização.



