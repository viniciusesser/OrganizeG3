# OrganizeG3 — Legacy Migration Specification

**Status:** Especificação funcional oficial  
**Versão inicial:** 2026-08-10  
**Escopo:** Migração segura de dados e arquivos do sistema legado para o OrganizeG3.

---

# 1. Objetivo

A migração do legado deverá permitir que os dados do sistema atual sejam levados para o novo OrganizeG3 sem:

- perda de informação relevante;
- corrupção de relacionamento;
- alteração do banco original;
- sobrescrita silenciosa;
- criação de duplicidades desnecessárias;
- descarte não documentado.

A migração deve ser tratada como processo controlado, auditável e repetível.

---

# 2. Princípio central

O banco legado será tratado como:

```text
fonte somente leitura

O processo deverá:

ler
↓
normalizar
↓
mapear
↓
validar
↓
transformar
↓
importar
↓
verificar

O banco antigo nunca deverá ser alterado pelo migrador.

3. Escopo

A migração poderá envolver:

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
anexos;
estoque;
compras;
financeiro;
RH;
agenda;
documentos;
históricos;
arquivos externos;
referências locais de projetos.
4. Migração não é cópia de tabela

O novo OrganizeG3 possui arquitetura diferente.

Portanto:

tabela antiga
≠
tabela nova

A migração deve preservar significado de negócio, não estrutura física antiga.

5. Exemplo de transformação

Exemplo legado:

clientes.id = 14
clientes.nome = João da Silva

Exemplo novo:

customer.id = UUID(...)
customer.tenant_id = UUID(...)
customer.name = João da Silva

O migrador deverá registrar:

legacy_table = clientes
legacy_id = 14
new_entity = customer
new_id = UUID(...)
6. Identificadores

IDs legados não serão utilizados como IDs oficiais no OrganizeG3.

O sistema novo continuará utilizando UUID.

7. Mapa de identidade legado → novo

Durante a migração será necessário manter mapeamento explícito.

Exemplo:

clientes:14
→
customers:5f7d...

Esse mapa será utilizado para reconstruir relacionamentos.

8. Entidades dependentes

Exemplo:

cliente antigo 14
    ↓
novo customer UUID
    ↓
orçamento
projeto
financeiro
documentos

Nenhum relacionamento deverá depender de tentativa heurística quando existir ID legado confiável.

9. Estratégia de mapeamento

Cada domínio migrado deverá possuir especificação contendo:

source_table
source_field
target_entity
target_field
transform
validation
fallback
discard_rule
10. Dados descartados

Nenhum dado relevante poderá ser descartado silenciosamente.

Todo campo sem destino deve receber uma decisão:

MIGRAR
TRANSFORMAR
ARQUIVAR
IGNORAR
REMOVER

E o motivo deverá ser registrado.

11. Relatório de campos não migrados

O processo de análise deverá produzir relatório como:

Tabela: clientes

campo legado: observacao_antiga
decisão: MIGRAR
destino: customer.notes

campo legado: sync_notion_id
decisão: IGNORAR
motivo: integração Notion removida
12. Fases da migração

A migração deverá possuir quatro fases principais:

1. análise
2. dry-run
3. execução
4. validação pós-migração
13. Fase 1 — análise

Objetivo:

entender o conteúdo real do banco antes de importar.

Deve coletar:

tabelas;
quantidade de registros;
campos;
valores nulos;
relacionamentos;
duplicidades;
dados inválidos;
registros órfãos;
arquivos referenciados.
14. Análise por entidade

Exemplo:

CLIENTES

registros: 142
ativos: 131
inativos: 11
sem documento: 7
CPF inválido: 1
CNPJ inválido: 0
telefone inválido: 4
duplicidade possível: 3
15. Fase 2 — dry-run

Dry-run é obrigatório.

O dry-run executa toda a lógica de:

leitura;
normalização;
transformação;
validação;
mapeamento;

sem persistir definitivamente no banco de produção.

16. Objetivo do dry-run

Identificar:

dados incompatíveis;
campos ausentes;
duplicidades;
relacionamento quebrado;
conversões incorretas;
perda potencial;
diferenças financeiras.
17. Resultado do dry-run

Exemplo:

MIGRAÇÃO — CLIENTES

Encontrados: 142
Convertíveis: 140
Com erro: 2
Duplicidades possíveis: 3
Ignorados por regra: 0
18. Registros com erro

Um registro inválido não deve necessariamente interromper toda a migração.

O comportamento depende da criticidade.

Exemplo:

cliente com telefone inválido
→ importar sem telefone
→ warning

Exemplo:

orçamento sem cliente obrigatório
→ bloquear registro
→ error
19. Severidades

Problemas devem ser classificados como:

info
warning
error
fatal
20. Fase 3 — execução

A execução definitiva só ocorre após dry-run aprovado.

Ela deve:

criar registros;
preservar relacionamentos;
registrar mapeamentos;
evitar duplicação;
gerar relatório;
permitir reexecução controlada.
21. Idempotência

Sempre que possível, a migração deve ser idempotente.

Executar novamente não deve criar cópias duplicadas dos mesmos registros legados.

22. Estratégias de idempotência

Possibilidades:

tabela de migration mapping;
legacy_id explícito;
chave externa de migração;
hash determinístico;
combinação de origem + ID.
23. Identificador de origem

Cada execução deverá possuir origem definida.

Exemplo:

source_system = organizeg_legacy
24. Migration batch

Cada execução deverá possuir identificador.

Exemplo:

migration_batch_id

Isso permite:

auditoria;
comparação;
diagnóstico;
rollback assistido quando aplicável.
25. Tabela conceitual de mapeamento

Exemplo:

legacy_migration_map

id
migration_batch_id
source_system
source_table
source_id
target_entity
target_id
status
created_at

A definição física será feita na implementação.

26. Ordem de migração

A ordem deve respeitar dependências.

Estratégia inicial:

1. Tenant / empresa
2. Filiais
3. Usuários
4. Funcionários
5. Clientes
6. Fornecedores
7. Marcas
8. Materiais
9. Serviços
10. Máquinas
11. Configurações
12. Orçamentos
13. Projetos
14. Itens de orçamento
15. Anexos
16. Estoque
17. Compras
18. Financeiro
19. RH detalhado
20. Agenda
21. Documentos
22. Históricos
23. Arquivos externos

A ordem definitiva dependerá dos modelos finais.

27. Tenant

Como existe apenas uma instalação piloto hoje, a migração inicial deverá associar todos os dados ao tenant correto da empresa atual.

O tenant deve existir antes da importação das entidades empresariais.

28. Empresa

Migrar:

razão social;
nome fantasia;
documento;
inscrição estadual;
contatos;
endereço;
logo;
parâmetros úteis.
29. Filiais

Quando existirem:

mapear filial;
associar funcionários;
associar dados operacionais;
associar estoques quando aplicável.
30. Usuários e autenticação

Usuários legados não devem ter senha copiada diretamente para Supabase.

A autenticação nova utiliza mecanismo próprio.

Migração poderá preservar:

nome;
e-mail;
vínculo com funcionário;
perfil lógico.

Credenciais deverão seguir fluxo seguro separado.

31. Funcionários

Migrar:

dados pessoais;
dados funcionais;
cargo;
departamento;
filial;
admissão;
status;
contatos;
documentos quando existentes.
32. Histórico funcional

Quando o legado possuir apenas estado atual, migrar o estado conhecido.

Quando possuir eventos históricos, preservar:

mudança de cargo;
salário;
afastamento;
promoção;
outras alterações.
33. Clientes

Migrar:

tipo;
nome;
documento;
contatos;
endereço;
observações;
status.
34. Normalização de clientes

Aplicar regras novas para:

CPF;
CNPJ;
telefone;
e-mail;
CEP;
UF.

Dados inválidos devem ser reportados.

35. Duplicidade de clientes

Não mesclar automaticamente registros somente por nome.

Possíveis critérios:

documento;
telefone;
e-mail;
combinação de campos.

Resultado deve ser reportado para decisão quando houver ambiguidade.

36. Fornecedores

Migrar:

identificação;
contatos;
endereço;
dados bancários;
documentos;
status.
37. Dados bancários

Devem manter restrição de acesso no novo sistema.

Migração não altera a sensibilidade do dado.

38. Marcas

Migrar marcas existentes antes dos materiais.

39. Materiais

Migrar:

código;
nome;
descrição;
unidade;
marca;
categoria;
características;
status.
40. Preços de materiais

Quando existir histórico ou múltiplos preços:

preservar fornecedor;
preço;
data;
origem.

Não reduzir histórico a um único preço atual.

41. Serviços

Migrar catálogo útil de serviços.

Registros obsoletos poderão ser:

inativos

em vez de excluídos.

42. Máquinas

Migrar:

identificação;
status;
dados úteis conhecidos.
43. Configurações

Cada configuração antiga deverá ser avaliada individualmente.

Classificação:

MIGRAR
CONVERTER
SUBSTITUIR
IGNORAR
44. Configurações removidas

Exemplo:

HWID legacy

não deve ser migrado como mecanismo de licença.

45. Orçamentos

Orçamentos exigem cuidado especial.

Migrar:

identificação;
cliente;
datas;
descrição;
itens;
valores;
condições;
status;
anexos;
aprovação;
observações.
46. Valores monetários

Valores financeiros deverão ser convertidos para representação decimal segura.

Evitar carregar Float legado como verdade absoluta sem validação.

47. Gate financeiro de orçamento

Antes da migração definitiva, comparar:

total legado
x
total calculado/migrado

Diferenças devem ser relatadas.

48. Tolerância

Qualquer tolerância monetária aceitável deve ser definida explicitamente antes da migração final.

49. Projetos

Projetos serão migrados respeitando:

cliente;
orçamento;
código;
nome;
descrição;
situação;
arquivos;
datas;
relacionamentos.
50. Projeto e orçamento

Não assumir automaticamente que são a mesma entidade.

O migrador deverá respeitar o modelo final do OrganizeG3.

51. Anexos

Anexos do banco deverão ser classificados:

arquivo local
storage
referência ausente
52. Estoque

Migrar somente quando o modelo de estoque novo estiver estável.

Itens a validar:

saldo;
unidade;
local;
material;
movimentações.
53. Saldo sem histórico

Se o legado possui saldo atual, mas não histórico completo:

criar saldo inicial migrado

Não inventar movimentações passadas.

54. Compras

Migrar:

ordens;
fornecedores;
itens;
valores;
status;
recebimentos;
previsões;
observações.
55. Recebimentos

Recebimento deve permanecer separado de ordem de compra.

Quando houver dados de recebimento parcial:

preservar quantidade recebida;
preservar saldo pendente.
56. Financeiro

Migrar:

receitas;
despesas;
categorias;
vencimentos;
pagamentos;
clientes;
fornecedores;
orçamento relacionado;
funcionário relacionado;
formas de pagamento;
observações.
57. Financeiro e Decimal

Todos os valores devem ser convertidos para Decimal/tipo monetário adequado no novo sistema.

58. Recorrências

Se houver recorrências legadas:

migrar regra;
não duplicar lançamentos já materializados.

A estratégia final dependerá do domínio financeiro novo.

59. Maquininhas

Migrar quando o módulo financeiro novo suportar:

operadora;
taxa;
parcelamento;
prazo.
60. RH

A migração de RH deverá considerar:

funcionário;
jornada;
ponto;
banco de horas;
folha;
dependentes;
férias;
afastamentos;
SST;
documentos.
61. Folha

Folhas históricas fechadas devem ser tratadas como histórico.

Não recalcular silenciosamente folha antiga usando parâmetros novos.

62. Encargos históricos

Quando existirem valores fechados:

preservar resultado

em vez de recalcular.

63. Agenda

Migrar eventos úteis quando o módulo Agenda novo estiver disponível.

64. Documentos

Documentos gerados existentes devem ser tratados separadamente dos templates.

65. Templates antigos

Templates atuais poderão ser:

convertidos;
substituídos pelos novos padrões;
mantidos apenas como referência.

Não é obrigatório preservar sintaxe de tags legadas.

66. Documentos gerados antigos

Quando houver arquivos reais:

preservar arquivo;
associar à entidade quando possível;
registrar origem legada.
67. Arquivos externos

Arquivos não armazenados no banco precisam de inventário próprio.

Exemplos:

SKP;
DWG;
imagens;
PDFs;
DOCX;
contratos;
recibos;
logos;
anexos.
68. Estratégia de arquivos

Arquivos e banco serão migrados por processos distintos.

DataMigration
FileMigration
69. Não mover automaticamente projetos legados

Diretórios existentes não deverão ser reorganizados na primeira migração.

70. Workspace legado

Para cada projeto legado, tentar identificar:

workspace_path
main_project_file
documents_path
71. Associação de workspace

Quando houver correspondência confiável:

legacy project
→
existing local workspace

registrar a associação.

72. Workspace não encontrado

Não bloquear migração de projeto.

Resultado:

workspace_status = not_found

O usuário poderá associar depois.

73. Duplicidade de diretórios

Se múltiplos diretórios parecerem corresponder ao mesmo projeto:

warning
manual_review_required

Não escolher arbitrariamente.

74. Arquivo principal

Quando possível, detectar o arquivo .skp principal.

Critérios podem considerar:

nome;
projeto;
data;
diretório.

A associação deve ser confirmável.

75. Documentos legados

Quando um PDF/DOCX puder ser associado a:

orçamento;
projeto;
cliente;
financeiro;

registrar referência.

76. Hash de arquivo

Futuramente o migrador poderá calcular hash para:

detectar duplicidade;
verificar cópia;
validar integridade.
77. Logs

Cada execução deverá produzir logs estruturados.

Exemplo:

migration_started
entity_started
record_converted
record_skipped
record_failed
entity_completed
migration_completed
78. Correlation ID

Quando aplicável, o processo poderá utilizar correlation id para rastreamento.

79. Relatório final

A migração deve produzir resumo por entidade.

Exemplo:

CLIENTES
encontrados: 142
migrados: 140
warnings: 2
errors: 0

FORNECEDORES
encontrados: 28
migrados: 28
warnings: 1
errors: 0
80. Relatório de integridade

Depois da migração, validar:

contagens;
relacionamentos;
totais;
referências;
documentos;
arquivos.
81. Comparação pré e pós

Para cada entidade:

quantidade origem
quantidade destino
diferença
motivo
82. Integridade referencial

Validar:

orçamento sem cliente;
projeto sem cliente;
compra sem fornecedor quando obrigatório;
item sem pai;
documento sem contexto;
lançamento com referência quebrada.
83. Integridade financeira

Validar pelo menos:

total de orçamentos;
total de compras;
total financeiro;
contas pagas;
contas em aberto.
84. Reexecução

Em ambiente de desenvolvimento, deve ser possível:

reset database
↓
run migration
↓
inspect
↓
adjust mapping
↓
run again
85. Migração de produção

A migração final de produção deve ocorrer apenas uma vez após preparação completa.

86. Freeze operacional

No momento da migração final será necessário definir período em que o sistema antigo não recebe novos dados.

Exemplo:

encerrar uso legado
↓
backup
↓
migração final
↓
validação
↓
liberar novo OrganizeG3
87. Backup obrigatório

Antes da migração final:

backup do banco;
backup dos arquivos;
cópia externa recomendada.
88. Banco legado preservado

Mesmo após migração:

não apagar

Guardar como histórico por período apropriado.

89. Rollback operacional

Se a validação final falhar:

não liberar novo sistema

O banco antigo permanece disponível para retorno operacional controlado.

90. Segurança

O migrador deve:

usar credenciais mínimas;
não expor secrets em logs;
não registrar documentos sensíveis completos desnecessariamente;
respeitar tenant;
proteger dados pessoais.
91. Ambiente

Migração deve diferenciar:

development
staging
production
92. Nunca testar primeiro em produção

Toda migração deverá ser executada previamente em ambiente não produtivo.

93. Base real anonimizada

Quando possível, testes podem utilizar cópia anonimizada.

Entretanto, para validação final será necessário testar contra cópia fiel do banco real.

94. Ferramenta de migração

Estrutura futura sugerida:

tools/
└── legacy_migration/
    ├── analyze.py
    ├── dry_run.py
    ├── migrate.py
    ├── validate.py
    ├── mappings/
    ├── transformers/
    ├── validators/
    └── reports/
95. Separação de responsabilidades
analyzer
→ entende origem

transformer
→ transforma

validator
→ valida

writer
→ persiste

reporter
→ relata
96. Não depender de UI

A migração deve poder ser executada por ferramenta administrativa/CLI.

Uma UI poderá existir depois.

97. Migração assistida futura

Como existe apenas uma instalação legado hoje, a primeira migração será controlada.

Não é necessário construir inicialmente um produto genérico de migração para clientes externos.

98. Primeiro cliente piloto

A instalação atual será tratada como:

reference legacy migration

O processo criado para ela servirá como base para qualquer necessidade futura.

99. Regra de conservação

Dado que não possui destino imediato no novo sistema pode ser preservado em:

snapshot;
arquivo de exportação;
tabela temporária de legado;
relatório.

Não deve ser descartado sem decisão.

100. Campos temporários de migração

Algumas entidades novas poderão temporariamente possuir referência como:

legacy_customer_id
legacy_supplier_id

somente se isso facilitar migração segura.

Esses campos não devem ser usados como identidade de negócio futura.

101. Remoção de campos legados

Campos auxiliares podem ser removidos futuramente após:

validação;
encerramento da migração;
preservação do mapa histórico.
102. Regras específicas por módulo

Cada módulo complexo deverá possuir seu próprio anexo de migração antes da execução.

Principalmente:

Orçamentos
Projetos
Financeiro
RH
Estoque
Compras
103. Gate antes de migrar um módulo

Um módulo só pode receber migração definitiva quando:

modelo estável
API estável
regras principais estáveis
migração testada
validação definida
104. Não migrar antecipadamente

Não migrar dados para estruturas provisórias que sabemos que serão remodeladas.

105. Sequência durante desenvolvimento
novo módulo estabiliza
↓
mapa legado é atualizado
↓
migrador daquele módulo é criado
↓
dry-run
↓
testes
106. Migração incremental de desenvolvimento

Durante desenvolvimento poderá existir migração parcial para testes.

Exemplo:

clientes
fornecedores
materiais

sem significar que ocorreu migração definitiva.

107. Migração final única

Antes do lançamento:

full dry-run
↓
full validation
↓
backup
↓
freeze
↓
full migration
↓
post-validation
↓
go-live
108. Critério de sucesso

Migração é considerada bem-sucedida quando:

dados relevantes foram preservados;
relacionamentos estão íntegros;
totais relevantes conferem;
erros estão resolvidos;
arquivos críticos estão localizáveis;
relatório final foi aprovado.
109. Critério de bloqueio

Não liberar novo sistema se houver:

perda financeira sem explicação;
relacionamento crítico quebrado;
cliente/projeto/orçamento ausente;
erro estrutural em volume relevante;
migração incompleta não documentada.
110. Regra final

O objetivo da migração não é reproduzir o banco antigo.

O objetivo é:

preservar os dados e o histórico úteis
dentro da arquitetura correta do OrganizeG3 novo

O sistema legado permanece a referência até que a migração final tenha sido validada.