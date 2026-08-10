# OrganizeG3 — Project Workspace Specification

**Status:** Especificação funcional oficial  
**Versão inicial:** 2026-08-10  
**Escopo:** Criação, organização e gerenciamento do workspace local dos projetos.

---

# 1. Objetivo

O Project Workspace é o mecanismo responsável por preparar e organizar o diretório local utilizado pela empresa para desenvolver um projeto.

Seu objetivo principal é:

- reduzir trabalho manual;
- padronizar nomes;
- evitar arquivos salvos no local errado;
- facilitar abertura dos arquivos corretos;
- preparar automaticamente a estrutura usada no dia a dia;
- integrar projeto, orçamento e documentos sem acoplar o banco ao filesystem.

---

# 2. Contexto operacional

O Project Workspace existe principalmente para empresas que utilizam softwares locais de projeto.

Exemplos:

- SketchUp;
- AutoCAD;
- softwares de renderização;
- softwares de plano de corte;
- editores de imagem;
- outros programas técnicos.

O OrganizeG3 não deve substituir esses softwares.

Ele deve facilitar a preparação e organização dos arquivos usados neles.

---

# 3. Responsabilidade por plataforma

## 3.1 Desktop

O desktop será responsável por operações locais como:

- criar diretórios;
- copiar arquivos-modelo;
- renomear arquivos;
- localizar workspace;
- abrir diretório;
- abrir projeto;
- verificar existência de arquivos;
- registrar referências locais.

## 3.2 PWA

O PWA não deve manipular diretamente diretórios locais do computador.

O PWA poderá:

- visualizar metadados;
- visualizar documentos autorizados;
- visualizar fotos;
- visualizar PDFs;
- consultar arquivos sincronizados;
- realizar uploads permitidos.

---

# 4. Princípio de separação

O banco de dados não deve depender da existência física de um diretório local.

O projeto existe no OrganizeG3 independentemente do workspace.

Fluxo:

```text
Project
    ↓
Project Workspace Metadata
    ↓
Workspace Service
    ↓
filesystem local

Se o diretório for movido ou estiver temporariamente indisponível, o projeto continua existindo no banco.

5. Workspace por projeto

Cada projeto poderá possuir um workspace associado.

Exemplo:

Cliente: João da Silva
Projeto: Cozinha
Código: PRJ-2027-0042

Workspace:

João da Silva - Cozinha
6. Diretório base

Cada empresa poderá definir seu diretório base.

Exemplo:

D:\Marcenaria\Projetos

Outro exemplo:

C:\Projetos\OrganizeG3

O caminho é configuração local/desktop.

Não deve ser presumido pelo backend cloud.

7. Configuração por dispositivo

O caminho físico pode ser diferente em computadores diferentes.

Exemplo:

Computador A
D:\Projetos

Computador B
E:\Projetos

Portanto:

tenant define padrão lógico;
dispositivo pode definir caminho físico local.
8. Identificador lógico do workspace

O sistema deve separar:

workspace logical name

de:

absolute filesystem path

Exemplo:

logical:
João da Silva - Cozinha

physical:
D:\Marcenaria\Projetos\João da Silva - Cozinha
9. Padrão de nome

O nome do workspace deve ser configurável.

Exemplo:

{{cliente.nome}} - {{projeto.nome}}

Outro exemplo:

{{projeto.codigo}} - {{cliente.nome}}
10. Tags permitidas para nome do workspace

O padrão de nome poderá utilizar conjunto limitado de tags seguras.

Inicialmente:

{{cliente.nome}}
{{projeto.codigo}}
{{projeto.nome}}

Futuramente:

{{filial.codigo}}
{{documento.ano}}

Não utilizar catálogo documental inteiro para nomes de filesystem.

11. Sanitização

O nome final deve ser sanitizado.

Caracteres inválidos de filesystem devem ser:

removidos;
substituídos;
normalizados.

Também devem ser tratados:

espaços duplicados;
nomes reservados;
nomes vazios;
comprimento excessivo.
12. Estabilidade do caminho

Renomear cliente ou projeto no banco não deve mover automaticamente o diretório existente.

Motivo:

mover automaticamente arquivos pode:

quebrar atalhos;
quebrar referências externas;
causar perda;
interromper arquivos abertos.
13. Renomear workspace

Quando houver mudança relevante:

Cliente antigo → Cliente novo

o OrganizeG3 poderá informar:

O nome sugerido do workspace mudou.

Ações possíveis:

Manter nome atual
Renomear workspace

A decisão deve ser explícita.

14. Estrutura padrão inicial

A estrutura padrão sugerida será:

Cliente - Projeto
│
├── 01 Projeto
├── 02 Renderizações
├── 03 Orçamento
├── 04 Plano de Corte
├── 05 Documentos
└── 06 Entrega
15. Estrutura configurável

A empresa poderá futuramente personalizar:

nomes;
ordem;
existência das pastas.

Exemplo:

01 SketchUp
02 Imagens
03 Executivo
04 Corte
05 Contratos
06 Fotos Finais
16. Estrutura de template do workspace

A configuração poderá ser representada logicamente como:

workspace_template
    ├── folders
    └── files
17. Arquivos-modelo

O workspace poderá copiar arquivos padrão.

Exemplo:

Projeto_Base.skp

Ao criar:

João da Silva - Cozinha

gerar:

01 Projeto
└── João da Silva - Cozinha.skp
18. Arquivos-modelo por empresa

Cada tenant poderá possuir seus próprios arquivos-modelo.

Exemplos:

SketchUp;
planilha;
checklist;
arquivo CAD;
documento auxiliar.
19. Template de arquivo

Um arquivo-modelo deverá possuir:

nome;
origem;
destino;
regra de renomeação;
status;
tipo;
programa associado quando aplicável.
20. Nome de arquivo gerado

Exemplo de configuração:

{{cliente.nome}} - {{projeto.nome}}.skp
21. Não sobrescrever silenciosamente

Se o arquivo já existir:

João da Silva - Cozinha.skp

o sistema não deve sobrescrevê-lo automaticamente.

Opções futuras:

Abrir existente
Cancelar
Criar cópia
22. Criação idempotente

Executar:

Criar workspace

mais de uma vez não deve duplicar toda a estrutura.

O serviço deve:

verificar o existente;
criar somente o ausente;
não sobrescrever arquivos;
produzir relatório.
23. Resultado da criação

Exemplo:

Workspace criado

✓ 01 Projeto
✓ 02 Renderizações
✓ 03 Orçamento
✓ 04 Plano de Corte
✓ 05 Documentos
✓ 06 Entrega

✓ João da Silva - Cozinha.skp

0 arquivos sobrescritos
24. Estado parcial

Caso parte exista:

✓ 01 Projeto já existia
+ 02 Renderizações criada
+ 03 Orçamento criada
✓ arquivo SKP já existia

O estado parcial não deve ser tratado automaticamente como erro.

25. Abrir pasta

A aplicação desktop deverá possuir ação:

Abrir pasta do projeto
26. Abrir arquivo principal

A aplicação poderá possuir:

Abrir projeto

Essa ação utiliza a referência do arquivo principal.

Exemplo:

João da Silva - Cozinha.skp
27. Programa associado

O sistema operacional deve abrir o arquivo com:

aplicativo padrão;
ou aplicativo configurado pela empresa/dispositivo.

Não é requisito inicial controlar diretamente a instalação do SketchUp.

28. Arquivo principal

Um workspace poderá possuir arquivo principal.

Exemplo:

project_file

O banco guarda uma referência lógica/local.

Não deve armazenar necessariamente o arquivo pesado em cloud.

29. Arquivos pesados

Arquivos como:

.skp
.dwg
.psd

não devem ser enviados automaticamente para storage cloud.

Motivos:

tamanho;
custo;
sincronização;
velocidade;
conflitos.
30. Documentos leves

Arquivos como:

PDF;
JPG;
PNG;
DOCX;
documentos de entrega;

podem ser sincronizados quando houver funcionalidade própria.

31. Integração com Document Engine

Documentos gerados relacionados ao projeto poderão ser enviados para:

05 Documentos

Exemplos:

contrato;
proposta;
recibo;
garantia;
aceite.
32. Integração com orçamento

Documentos comerciais poderão ser enviados para:

03 Orçamento

Exemplos:

orçamento;
proposta;
revisão.
33. Integração com plano de corte

Planos de corte poderão ser enviados para:

04 Plano de Corte
34. Integração com entrega

Documentos e fotos finais poderão ser enviados para:

06 Entrega
35. Project Workspace Service

A arquitetura deverá possuir serviço específico.

Nome conceitual:

ProjectWorkspaceService

Ele será responsável por:

montar paths;
sanitizar nomes;
criar estrutura;
copiar templates;
verificar workspace;
abrir arquivos;
registrar resultado.
36. O serviço não pertence à UI

Exemplo incorreto:

ProjectPage
    ↓
os.mkdir(...)

Exemplo correto:

ProjectPage
    ↓
ProjectWorkspaceUseCase
    ↓
ProjectWorkspaceService
37. O serviço não pertence ao repository

Repository é responsável por persistência de dados.

Filesystem é infraestrutura separada.

Não colocar criação de pastas dentro de:

ProjectRepository
38. Configuração do workspace

Conceitualmente:

WorkspaceConfiguration

pode conter:

base_path
directory_name_pattern
folders
file_templates
39. Configuração local e cloud

Parte da configuração é empresarial:

estrutura
padrões de nome
arquivos-modelo

Parte é local:

base_path
software_path

Essa separação é obrigatória.

40. Configuração empresarial

Pode ficar no backend:

workspace_template
folder_definitions
filename_patterns
41. Configuração de dispositivo

Pode ficar localmente:

local_base_path
preferred_application

Futuramente poderá existir registro cloud do dispositivo, mas senhas ou informações sensíveis não devem ser necessárias.

42. Primeiro uso

Se o desktop ainda não possuir diretório configurado:

Workspace não configurado neste computador.

A aplicação solicita:

Selecionar pasta de projetos
43. Validação do diretório base

Antes de usar:

verificar existência;
verificar permissão de escrita;
verificar acesso;
verificar caminho válido.
44. Diretório indisponível

Exemplo:

D:\Projetos

está em disco externo desconectado.

O sistema deve informar:

Diretório de projetos indisponível.

O projeto no banco permanece acessível.

45. Armazenamento de caminho

Não armazenar o caminho absoluto como única referência universal do projeto.

O caminho é específico do ambiente local.

46. Referência relativa

Quando possível:

workspace_relative_path

Exemplo:

João da Silva - Cozinha
47. Metadados possíveis

Um vínculo de workspace poderá registrar:

project_id
workspace_template_id
relative_path
main_file_relative_path
created_at
last_verified_at

Valores locais específicos podem ficar no dispositivo.

48. Auditoria

Eventos sugeridos:

project_workspace.created
project_workspace.verified
project_workspace.renamed
project_workspace.template_applied
project_workspace.main_file_opened

A abertura de arquivo pode não precisar de auditoria obrigatória na primeira versão.

49. Falhas

Falhas possíveis:

base_directory_unavailable
write_permission_denied
invalid_workspace_name
template_file_missing
destination_file_exists
filesystem_error
50. Segurança

O serviço deve trabalhar apenas dentro de diretórios autorizados.

Nunca aceitar path arbitrário vindo diretamente de:

template;
usuário web;
API externa.
51. Path traversal

Entradas como:

..\..\Windows

devem ser bloqueadas.

52. Template seguro

Nomes de pastas e arquivos são resolvidos a partir de tokens permitidos.

Não executar:

comandos;
scripts;
código do template.
53. Arquivos executáveis

Arquivos-modelo executáveis não devem ser aceitos por padrão.

Exemplos:

.exe
.bat
.cmd
.ps1

Caso exista necessidade futura, deve ser uma decisão explícita de segurança.

54. Migração do workspace atual

Os diretórios de projetos já existentes não devem ser reorganizados automaticamente durante a primeira migração.

Estratégia:

descobrir
↓
registrar
↓
validar
↓
manter localização
55. Projeto legado já existente

Se um projeto antigo possui diretório:

D:\Projetos Antigos\Cliente X

o migrador poderá registrar essa localização sem mover os arquivos.

56. Padronização progressiva

Projetos novos usam o padrão novo.

Projetos antigos podem:

permanecer onde estão;
ser associados manualmente;
ser reorganizados posteriormente.
57. Migração opcional de diretórios

Uma ferramenta futura poderá oferecer:

Reorganizar workspace legado

Ela nunca deverá ser executada automaticamente.

58. Backup antes de movimentação

Qualquer ferramenta futura que mova arquivos deverá:

validar origem;
validar destino;
impedir sobrescrita;
gerar relatório;
recomendar backup.
59. Relação com código do projeto

O código deve ser estável.

Exemplo:

PRJ-2027-0042

Esse identificador pode ser usado para facilitar localização mesmo que o nome do cliente mude.

60. Estratégia recomendada de nomenclatura

Padrão inicial sugerido:

{{projeto.codigo}} - {{cliente.nome}} - {{projeto.nome}}

Exemplo:

PRJ-2027-0042 - João da Silva - Cozinha

Isso é mais robusto do que depender somente do nome do cliente.

61. Empresa poderá alterar padrão

A configuração poderá escolher:

{{cliente.nome}} - {{projeto.nome}}

se preferir.

O OrganizeG3 apenas fornece um padrão recomendado.

62. Projeto sem nome

O projeto deve possuir identificação suficiente antes de criar workspace.

Se o nome ainda não existir:

bloquear criação;
ou utilizar código + descrição padrão.

A regra definitiva será definida no módulo Projetos.

63. Momento de criação

O workspace não precisa ser criado ao cadastrar um lead.

Possíveis momentos:

criação do projeto
aprovação do orçamento
ação manual
64. Regra inicial recomendada

Criar workspace quando um Projeto real for criado.

Não criar para:

lead;
cliente sem projeto;
orçamento preliminar sem projeto.
65. Criação automática configurável

Futuramente:

Criar workspace automaticamente ao criar projeto

Configuração:

sim / não
66. Ação manual sempre disponível

Mesmo com automação desligada:

Criar workspace

deve estar disponível no desktop.

67. Relação com produção

Produção não deve depender diretamente do filesystem.

Produção usa:

project_id;
documentos sincronizados;
PDFs autorizados;
plano de corte quando disponível.
68. PWA e chão de fábrica

O funcionário no celular não deve receber path como:

D:\Projetos\...

Ele deve receber documentos acessíveis via plataforma.

69. Referências cloud

Quando um documento local precisar ser utilizado no PWA:

arquivo local
↓
upload autorizado
↓
storage
↓
document reference
↓
PWA
70. Não sincronizar tudo

O sistema não deve tentar transformar o workspace inteiro em Dropbox/Google Drive.

Não é objetivo do OrganizeG3.

71. Integrações futuras

Pode ser avaliado no futuro:

OneDrive;
Google Drive;
Dropbox;
NAS;
servidor interno.

Não faz parte da primeira implementação.

72. Conflitos

Se dois computadores tiverem cópias diferentes do mesmo arquivo local, o OrganizeG3 não deve tentar fazer merge automático.

A sincronização de arquivos pesados não faz parte do escopo inicial.

73. File fingerprint

Futuramente poderá existir:

size
modified_at
hash

para ajudar a identificar:

arquivo alterado;
arquivo ausente;
arquivo diferente.

Não é requisito inicial.

74. Workspace status

Status conceituais possíveis:

not_configured
not_created
available
partial
unavailable
error
75. UI futura

No Projeto:

Workspace
Status: Disponível

Pasta:
PRJ-2027-0042 - João da Silva - Cozinha

[Abrir projeto]
[Abrir pasta]
[Verificar]
76. UI quando não criado
Workspace ainda não criado.

[Criar workspace]
77. UI quando indisponível
Workspace não encontrado neste computador.

[Localizar]
[Verificar]
78. Relocalizar

A aplicação poderá permitir selecionar um workspace existente.

Depois deve validar:

diretório;
projeto;
arquivo principal quando houver.
79. Associação manual

Projetos legados poderão usar:

Associar pasta existente

Isso será especialmente útil na migração.

80. Templates de workspace

A empresa poderá possuir mais de um template.

Exemplos:

Móveis planejados
Manutenção
Projeto arquitetônico
Projeto interno
81. Template padrão

Um template poderá ser definido como padrão.

82. Escolha ao criar

Futuramente:

Criar workspace

Template:
[ Móveis planejados ▼ ]
83. Versionamento de template de workspace

Alterar estrutura padrão não deve modificar automaticamente projetos existentes.

Novo template vale para novas criações.

84. Evolução da estrutura

Projeto existente pode receber:

Aplicar pastas novas

sem apagar ou sobrescrever conteúdo.

85. Exemplo de evolução

Template antigo:

01 Projeto
02 Documentos

Template novo:

01 Projeto
02 Renderizações
03 Orçamento
04 Plano de Corte
05 Documentos
06 Entrega

Ao aplicar atualização:

cria pastas ausentes;
mantém existentes;
não move arquivos automaticamente.
86. Integração com documentos padrão

Quando Document Engine gerar:

Contrato

ele poderá receber destino lógico:

workspace.documents
87. Destinos lógicos

O template de workspace poderá declarar aliases:

project
renders
budget
cut_plan
documents
delivery
88. Benefício dos aliases

O Document Engine não precisa saber que:

documents

fisicamente significa:

05 Documentos

Ele apenas solicita:

workspace destination: documents
89. Exemplo de alias
documents → 05 Documentos
budget → 03 Orçamento
cut_plan → 04 Plano de Corte
90. Arquitetura recomendada
Project
        ↓
ProjectWorkspaceUseCase
        ↓
WorkspaceConfiguration
        ↓
ProjectWorkspaceService
        ↓
LocalFilesystemAdapter
91. Adaptador de filesystem

O acesso físico deve ficar atrás de abstração.

Exemplo conceitual:

FilesystemGateway

Isso melhora:

testes;
Windows;
futuras plataformas;
segurança.
92. Sistema operacional inicial

O desktop principal será Windows.

Portanto a primeira implementação poderá priorizar Windows.

Mesmo assim:

paths devem usar abstrações;
regras de negócio não devem depender de C:\.
93. Testes futuros

Devem existir testes para:

sanitização;
criação;
idempotência;
arquivo já existente;
pasta parcialmente criada;
caminho inválido;
path traversal;
template ausente;
diretório indisponível.
94. Testes de integração

Usar diretório temporário.

Nunca utilizar a pasta real do usuário em testes automatizados.

95. Não remover conteúdo

O serviço não terá função genérica de:

delete_workspace()

na primeira versão.

Excluir projetos do banco não deve apagar arquivos físicos automaticamente.

96. Exclusão segura futura

Se algum dia houver exclusão:

ação separada;
confirmação;
permissões;
auditoria;
nunca implícita.
97. Projeto cancelado

Cancelar projeto não remove workspace.

Ele permanece como histórico.

98. Projeto concluído

Projeto concluído não remove workspace.

Futuramente poderá:

arquivar;
mover;
compactar;

mas somente por ação/configuração explícita.

99. Arquivamento futuro

Pode existir:

Projetos Ativos
Projetos Arquivados

Não implementar na primeira versão.

100. Regra de ouro

O Project Workspace deve facilitar a organização do trabalho.

Ele nunca deve colocar arquivos do usuário em risco.

Prioridades:

1. não apagar
2. não sobrescrever
3. não mover silenciosamente
4. validar antes de alterar
5. manter relatório das operações
101. Primeira implementação futura

Quando o módulo for desenvolvido, o escopo inicial será:

1. configurar diretório base
2. definir padrão de nome
3. criar estrutura padrão
4. copiar arquivo SKP base
5. associar arquivo principal
6. abrir pasta
7. abrir arquivo principal
8. verificar workspace
102. Segunda evolução

Depois:

templates configuráveis
aliases de destino
múltiplos arquivos-modelo
associação de workspace legado
integração automática com Document Engine
103. Terceira evolução

Depois:

armazenamento cloud seletivo
integrações externas
fingerprints
arquivamento
reorganização assistida
104. Relação com migração

A especificação de migração deverá tratar:

detecção de pastas existentes;
associação projeto → pasta;
arquivo principal;
arquivos documentais;
ausência de pasta;
duplicidade.

Isso será detalhado em:

docs/product/LEGACY_MIGRATION_SPEC.md

105. Regra final

Workspace local é uma facilidade operacional.

O OrganizeG3 deve continuar funcional para dados empresariais mesmo se:

workspace local estiver indisponível

A plataforma não pode depender do filesystem para preservar o estado de negócio.