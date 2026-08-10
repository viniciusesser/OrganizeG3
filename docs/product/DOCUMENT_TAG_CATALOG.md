# OrganizeG3 — Catálogo Oficial de Tags Documentais

**Status:** Especificação funcional oficial  
**Versão inicial:** 2026-08-10  
**Escopo:** Tags disponíveis para templates e geração documental do OrganizeG3.

---

# 1. Objetivo

Este documento define o catálogo oficial de dados que podem ser utilizados pelo Document Engine.

Ele estabelece:

- nomes oficiais das tags;
- namespaces;
- tipos de dados;
- disponibilidade por contexto;
- campos derivados;
- listas;
- imagens;
- regras de segurança;
- regras de evolução.

Nenhum módulo deverá criar tags documentais fora deste catálogo.

---

# 2. Convenção oficial

A sintaxe base será:

```text
{{namespace.campo}}

Exemplos:

{{empresa.nome}}
{{cliente.nome}}
{{projeto.codigo}}
{{orcamento.valor_total}}
{{documento.data}}
3. Convenção de nomes

As tags devem:

utilizar letras minúsculas;
utilizar português;
utilizar snake_case quando houver mais de uma palavra;
utilizar ponto para separar namespace;
representar significado de negócio, não nome de coluna física;
permanecer estáveis mesmo se o banco mudar internamente.

Exemplo correto:

{{cliente.documento}}

Exemplo inadequado:

{{customer.document_number_db}}
4. Princípio de independência do banco

A tag não representa diretamente uma coluna SQL.

Exemplo:

{{cliente.endereco_completo}}

pode ser produzido a partir de:

logradouro;
número;
complemento;
bairro;
cidade;
estado;
CEP.

O Document Engine é responsável por resolver o valor final.

5. Tipos de tag

Tipos oficiais iniciais:

text
integer
decimal
money
percentage
date
datetime
boolean
document
phone
email
address
image
list
identifier
6. Regras para valores ausentes

Uma tag sem valor:

nunca renderiza None;
nunca renderiza null;
nunca renderiza undefined;
não deve quebrar o documento.

Por padrão:

valor ausente → string vazia

Exceções podem ser definidas pelo tipo documental.

7. Namespaces oficiais

Namespaces iniciais:

empresa
filial
cliente
fornecedor
projeto
orcamento
pagamento
recibo
compra
material
funcionario
folha
ponto
financeiro
documento
usuario
entrega

Namespaces futuros podem ser adicionados mediante atualização deste catálogo.

8. Namespace empresa

Representa a empresa/tenant responsável pelo documento.

8.1 Identificação
{{empresa.id}}

Tipo:

identifier

Uso:

interno e administrativo.

{{empresa.nome}}

Tipo:

text

Nome principal utilizado comercialmente.

{{empresa.razao_social}}

Tipo:

text
{{empresa.nome_fantasia}}

Tipo:

text
9. Documentos da empresa
{{empresa.cnpj}}

Tipo:

document
{{empresa.inscricao_estadual}}

Tipo:

text
10. Contato da empresa
{{empresa.email}}

Tipo:

email
{{empresa.telefone}}

Tipo:

phone
{{empresa.site}}

Tipo:

text
11. Endereço da empresa
{{empresa.logradouro}}
{{empresa.numero}}
{{empresa.complemento}}
{{empresa.bairro}}
{{empresa.cidade}}
{{empresa.estado}}
{{empresa.cep}}

Tipos:

text

com exceção de CEP, tratado como endereço formatado.

{{empresa.endereco_completo}}

Tipo:

address

Campo derivado.

12. Identidade visual da empresa
{{empresa.logo}}

Tipo:

image

O motor deve inserir a imagem autorizada da empresa.

13. Namespace filial

Disponível quando o contexto possuir filial.

{{filial.id}}
{{filial.codigo}}
{{filial.nome}}
{{filial.razao_social}}
{{filial.documento}}
{{filial.inscricao_estadual}}
{{filial.email}}
{{filial.telefone}}
{{filial.site}}
{{filial.logradouro}}
{{filial.numero}}
{{filial.bairro}}
{{filial.cidade}}
{{filial.estado}}
{{filial.cep}}
{{filial.endereco_completo}}
14. Namespace cliente

Representa o cliente associado ao documento.

14.1 Identificação
{{cliente.id}}
{{cliente.nome}}
{{cliente.tipo}}
14.2 Documento
{{cliente.documento}}

Tipo:

document

Deve apresentar CPF ou CNPJ conforme o tipo do cliente.

{{cliente.cpf}}
{{cliente.cnpj}}

Status:

DERIVADOS / USO ESPECÍFICO

Preferência geral:

{{cliente.documento}}
15. Dados complementares do cliente
{{cliente.rg}}
{{cliente.inscricao_estadual}}
{{cliente.nacionalidade}}
{{cliente.estado_civil}}
{{cliente.profissao}}

Status:

FUTURO / DEPENDE DO DOMÍNIO

Essas informações já são necessárias para alguns modelos contratuais.

16. Contato do cliente
{{cliente.email}}
{{cliente.telefone}}
{{cliente.telefone_secundario}}
17. Endereço do cliente
{{cliente.logradouro}}
{{cliente.numero}}
{{cliente.complemento}}
{{cliente.bairro}}
{{cliente.cidade}}
{{cliente.estado}}
{{cliente.cep}}
{{cliente.endereco_completo}}

Tipo:

address

Campo derivado.

18. Namespace fornecedor
18.1 Identificação
{{fornecedor.id}}
{{fornecedor.nome}}
{{fornecedor.razao_social}}
{{fornecedor.nome_fantasia}}
{{fornecedor.documento}}
{{fornecedor.inscricao_estadual}}
18.2 Contato
{{fornecedor.contato_nome}}
{{fornecedor.email}}
{{fornecedor.telefone}}
{{fornecedor.site}}
18.3 Endereço
{{fornecedor.logradouro}}
{{fornecedor.numero}}
{{fornecedor.complemento}}
{{fornecedor.bairro}}
{{fornecedor.cidade}}
{{fornecedor.estado}}
{{fornecedor.cep}}
{{fornecedor.endereco_completo}}
19. Dados bancários do fornecedor
{{fornecedor.banco.nome}}
{{fornecedor.banco.agencia}}
{{fornecedor.banco.conta}}
{{fornecedor.banco.pix}}

Status:

DADO SENSÍVEL

Somente disponível em contextos autorizados.

Exemplo:

ordem de compra;
pagamento.

Não deve estar disponível em qualquer template genérico.

20. Namespace projeto
20.1 Identificação
{{projeto.id}}
{{projeto.codigo}}
{{projeto.nome}}
{{projeto.descricao}}
{{projeto.status}}
21. Dados comerciais do projeto
{{projeto.valor_total}}
{{projeto.valor_total_extenso}}
{{projeto.condicao_pagamento}}

Status:

alguns desses dados poderão futuramente pertencer oficialmente ao orçamento/venda.

Enquanto houver separação clara entre Projeto e Orçamento:

dados técnicos → projeto.*;
dados comerciais → orcamento.*.
22. Local do projeto
{{projeto.local_entrega}}

Tipo:

address
{{projeto.data_inicio}}
{{projeto.data_prevista_entrega}}
{{projeto.data_conclusao}}

Tipo:

date
23. Namespace orcamento
23.1 Identificação
{{orcamento.id}}
{{orcamento.codigo}}
{{orcamento.numero}}
{{orcamento.nome}}
{{orcamento.descricao}}
{{orcamento.status}}
24. Datas do orçamento
{{orcamento.data_emissao}}
{{orcamento.data_validade}}
{{orcamento.data_aprovacao}}
25. Valores do orçamento
{{orcamento.subtotal}}
{{orcamento.desconto}}
{{orcamento.acrescimo}}
{{orcamento.valor_total}}
{{orcamento.valor_total_extenso}}
{{orcamento.valor_entrada}}
{{orcamento.valor_saldo}}

Tipos:

money
26. Percentuais do orçamento
{{orcamento.desconto_percentual}}
{{orcamento.entrada_percentual}}

Tipo:

percentage
27. Condições do orçamento
{{orcamento.condicao_pagamento}}
{{orcamento.prazo}}
{{orcamento.observacoes}}
28. Endereço de entrega do orçamento
{{orcamento.entrega.logradouro}}
{{orcamento.entrega.numero}}
{{orcamento.entrega.complemento}}
{{orcamento.entrega.bairro}}
{{orcamento.entrega.cidade}}
{{orcamento.entrega.estado}}
{{orcamento.entrega.cep}}
{{orcamento.entrega.endereco_completo}}
29. Itens comerciais do orçamento

Coleção oficial:

{{#orcamento.itens}}
...
{{/orcamento.itens}}

Cada item disponibilizará:

{{item.id}}
{{item.nome}}
{{item.descricao}}
{{item.quantidade}}
{{item.unidade}}
{{item.valor_unitario}}
{{item.valor_total}}
30. Anexos do orçamento

Coleção:

{{#orcamento.anexos}}
...
{{/orcamento.anexos}}

Campos previstos:

{{anexo.id}}
{{anexo.nome}}
{{anexo.tipo}}
{{anexo.imagem}}

Uso principal:

perspectivas;
imagens;
anexos comerciais.
31. Namespace pagamento

Representa condição ou evento de pagamento.

{{pagamento.id}}
{{pagamento.descricao}}
{{pagamento.forma}}
{{pagamento.valor}}
{{pagamento.valor_extenso}}
{{pagamento.data}}
{{pagamento.vencimento}}
{{pagamento.status}}
32. Namespace recibo

Representa especificamente um recibo emitido.

{{recibo.id}}
{{recibo.numero}}
{{recibo.valor}}
{{recibo.valor_extenso}}
{{recibo.referente}}
{{recibo.data}}
33. Pagador do recibo
{{recibo.pagador.nome}}
{{recibo.pagador.documento}}

O pagador pode ser diferente do cliente do projeto.

34. Namespace compra
34.1 Identificação
{{compra.id}}
{{compra.numero}}
{{compra.status}}
{{compra.data_emissao}}
{{compra.data_prevista}}
35. Valores da compra
{{compra.subtotal}}
{{compra.desconto}}
{{compra.frete}}
{{compra.valor_total}}
36. Observações da compra
{{compra.observacoes}}
{{compra.condicao_pagamento}}
37. Itens da compra

Coleção:

{{#compra.itens}}
...
{{/compra.itens}}

Campos:

{{item.id}}
{{item.numero}}
{{item.material}}
{{item.descricao}}
{{item.quantidade}}
{{item.unidade}}
{{item.valor_unitario}}
{{item.valor_total}}
38. Namespace material

Representa um material individual quando o documento tiver esse contexto.

{{material.id}}
{{material.codigo}}
{{material.nome}}
{{material.descricao}}
{{material.unidade}}
{{material.marca}}
{{material.categoria}}
39. Material em listas de projeto/orçamento

Coleção recomendada:

{{#materiais}}
...
{{/materiais}}

Cada item:

{{material.nome}}
{{material.descricao}}
{{material.fornecedor_sugerido}}
{{material.quantidade}}
{{material.unidade}}
{{material.valor_unitario}}
{{material.valor_total}}
40. Fornecedor sugerido
{{material.fornecedor_sugerido}}

Status:

DERIVADO

A origem poderá utilizar a lógica futura de melhor condição de compra.

O template não decide qual fornecedor é melhor.

41. Namespace funcionario
41.1 Identificação
{{funcionario.id}}
{{funcionario.codigo}}
{{funcionario.nome}}
{{funcionario.documento}}
{{funcionario.matricula}}
42. Dados funcionais
{{funcionario.cargo}}
{{funcionario.departamento}}
{{funcionario.filial}}
{{funcionario.data_admissao}}
{{funcionario.data_demissao}}
{{funcionario.status}}
43. Namespace folha

Representa folha/holerite.

{{folha.competencia}}
{{folha.mes}}
{{folha.ano}}
{{folha.mensagem}}
44. Valores da folha
{{folha.salario_base}}
{{folha.total_vencimentos}}
{{folha.total_descontos}}
{{folha.liquido}}

Tipo:

money
45. Bases da folha
{{folha.base_inss}}
{{folha.base_fgts}}
{{folha.fgts_mes}}
{{folha.base_irrf}}
{{folha.faixa_irrf}}
46. Eventos da folha

Coleção:

{{#folha.eventos}}
...
{{/folha.eventos}}

Campos:

{{evento.codigo}}
{{evento.descricao}}
{{evento.referencia}}
{{evento.vencimento}}
{{evento.desconto}}
47. Namespace ponto

Representa espelho/apuração de ponto.

{{ponto.competencia}}
{{ponto.periodo_inicio}}
{{ponto.periodo_fim}}
{{ponto.total_horas}}
{{ponto.horas_extras}}
{{ponto.horas_faltantes}}
{{ponto.saldo_banco_horas}}
48. Registros de ponto

Coleção:

{{#ponto.registros}}
...
{{/ponto.registros}}

Campos previstos:

{{registro.data}}
{{registro.dia_semana}}
{{registro.entrada_1}}
{{registro.saida_1}}
{{registro.entrada_2}}
{{registro.saida_2}}
{{registro.horas_trabalhadas}}
{{registro.horas_extras}}
{{registro.observacao}}
49. Namespace financeiro

Utilizado em relatórios financeiros.

{{financeiro.periodo_inicio}}
{{financeiro.periodo_fim}}
50. Indicadores financeiros
{{financeiro.receita_bruta}}
{{financeiro.total_despesas}}
{{financeiro.resultado}}
{{financeiro.lucro_operacional}}

Tipos:

money
51. Receitas

Coleção:

{{#financeiro.receitas}}
...
{{/financeiro.receitas}}

Campos:

{{lancamento.data}}
{{lancamento.data_vencimento}}
{{lancamento.data_pagamento}}
{{lancamento.descricao}}
{{lancamento.categoria}}
{{lancamento.cliente}}
{{lancamento.valor}}
{{lancamento.status}}
52. Despesas

Coleção:

{{#financeiro.despesas}}
...
{{/financeiro.despesas}}

Campos:

{{lancamento.data}}
{{lancamento.data_vencimento}}
{{lancamento.data_pagamento}}
{{lancamento.descricao}}
{{lancamento.categoria}}
{{lancamento.fornecedor}}
{{lancamento.valor}}
{{lancamento.status}}
53. Namespace entrega

Representa entrega/conclusão.

{{entrega.id}}
{{entrega.data}}
{{entrega.endereco}}
{{entrega.responsavel}}
{{entrega.observacoes}}
54. Aceite da entrega

Campos derivados previstos:

{{entrega.data_aceite}}
{{entrega.aceite_por}}
55. Namespace documento

Representa o próprio documento em geração.

{{documento.id}}
{{documento.tipo}}
{{documento.numero}}
{{documento.nome}}
{{documento.data}}
{{documento.data_extenso}}
{{documento.data_hora}}
56. Paginação

Para renderizadores que suportarem paginação:

{{documento.pagina_atual}}
{{documento.total_paginas}}

O suporte depende do renderer.

57. Namespace usuario

Representa o usuário responsável pela ação.

{{usuario.id}}
{{usuario.nome}}
{{usuario.email}}
58. Responsabilidade documental
{{documento.gerado_por}}

Pode ser derivado de:

{{usuario.nome}}
59. Tags derivadas

Tags derivadas não precisam existir fisicamente no banco.

Exemplos:

{{empresa.endereco_completo}}
{{cliente.endereco_completo}}
{{projeto.valor_total_extenso}}
{{orcamento.valor_total_extenso}}
{{recibo.valor_extenso}}
{{documento.data_extenso}}
60. Formatação monetária

Tags money devem ser formatadas no padrão de apresentação configurado.

Padrão brasileiro inicial:

R$ 1.234,56

O template não deve executar lógica como:

format(valor, ".2f")
replace(".", ",")

Essa responsabilidade pertence ao renderer.

61. Valores por extenso

Valores monetários por extenso devem ser resolvidos pelo Document Engine.

Exemplo:

{{orcamento.valor_total_extenso}}

Resultado:

doze mil quatrocentos e cinquenta reais
62. Formatação de datas

Tag:

{{documento.data}}

Exemplo:

10/08/2026

Tag:

{{documento.data_extenso}}

Exemplo:

10 de agosto de 2026
63. Formatação de documentos

CPF/CNPJ devem ser formatados para apresentação.

O template não deve formatar manualmente.

64. Formatação de telefone

Telefone deve utilizar formatação de apresentação apropriada quando possível.

65. Formatação de CEP

CEP deve utilizar formatação de apresentação apropriada.

66. Listas

A primeira sintaxe oficial proposta será:

{{#namespace.colecao}}
...
{{/namespace.colecao}}

Exemplo:

{{#orcamento.itens}}
{{item.nome}}
{{item.quantidade}}
{{item.valor_total}}
{{/orcamento.itens}}
67. Escopo dentro de listas

Dentro de uma lista deve existir um namespace local.

Exemplos:

item.*
material.*
evento.*
registro.*
lancamento.*
anexo.*
68. Condicionais

Sintaxe definitiva será definida na implementação.

Conceito previsto:

{{?cliente.email}}
E-mail: {{cliente.email}}
{{/cliente.email}}

Status:

FUTURO

A primeira versão DOCX pode operar somente com campos escalares.

69. Condicionais HTML

Templates HTML poderão possuir sistema controlado de condicionais.

Entretanto:

não acessar objetos ORM;
não executar métodos arbitrários;
não executar Python;
não acessar banco;
não acessar filesystem.
70. Imagens em listas

Anexos poderão ser utilizados em relatórios estruturados.

Exemplo conceitual:

{{#orcamento.anexos}}
{{anexo.imagem}}
{{/orcamento.anexos}}
71. Contextos documentais

Cada tipo documental possuirá um conjunto autorizado de namespaces.

72. contract_individual

Namespaces previstos:

empresa
filial
cliente
projeto
orcamento
documento
usuario
73. contract_corporate

Namespaces previstos:

empresa
filial
cliente
projeto
orcamento
documento
usuario
74. project_acceptance

Namespaces:

empresa
filial
cliente
projeto
entrega
documento
usuario
75. warranty

Namespaces:

empresa
filial
cliente
projeto
documento
usuario
76. receipt

Namespaces:

empresa
filial
cliente
projeto
pagamento
recibo
documento
usuario
77. budget

Namespaces:

empresa
filial
cliente
projeto
orcamento
documento
usuario
78. commercial_proposal

Namespaces:

empresa
filial
cliente
projeto
orcamento
documento
usuario
79. material_list

Namespaces:

empresa
filial
cliente
projeto
orcamento
material
documento
usuario

Coleção adicional:

materiais
80. purchase_order

Namespaces:

empresa
filial
fornecedor
compra
projeto
documento
usuario
81. delivery_term

Namespaces:

empresa
filial
cliente
projeto
orcamento
entrega
documento
usuario
82. pay_stub

Namespaces:

empresa
filial
funcionario
folha
documento
usuario
83. timesheet

Namespaces:

empresa
filial
funcionario
ponto
documento
usuario
84. financial_report

Namespaces:

empresa
filial
financeiro
documento
usuario
85. Dados restritos por contexto

Tags sensíveis não podem ser liberadas apenas porque existem no catálogo.

Exemplos:

fornecedor.banco.*
funcionario.documento
folha.*
financeiro.*

A liberação depende de:

tipo documental;
permissão;
tenant;
contexto.
86. Tags obrigatórias

Cada tipo documental poderá definir tags obrigatórias.

Exemplo futuro:

contract_individual

empresa.nome
cliente.nome
cliente.documento
projeto.codigo
documento.data

A lista definitiva ficará vinculada à especificação de cada tipo.

87. Tags opcionais

Exemplos:

cliente.email
cliente.complemento
empresa.site
projeto.observacoes

Ausência não invalida necessariamente o template.

88. Tags desconhecidas

Exemplo:

{{cliente.apelido_super_especial}}

Se não existir no catálogo:

validation_error:
unknown_document_tag
89. Tags indisponíveis no contexto

Exemplo:

um contrato tenta utilizar:

{{folha.liquido}}

Resultado:

validation_error:
tag_not_available_for_document_type
90. Campos computados

Campos computados devem ser resolvidos pela aplicação.

O template nunca deve realizar regras de negócio.

Exemplo incorreto:

valor_unitario * quantidade

Exemplo correto:

{{item.valor_total}}
91. Regra de cálculos

Nenhum template deve ser responsável por:

calcular orçamento;
calcular imposto;
calcular folha;
calcular saldo;
escolher fornecedor;
calcular total financeiro;
calcular banco de horas.

Templates apenas apresentam resultados já determinados pelo domínio/aplicação.

92. Migração das tags legadas

Exemplos de equivalência:

{{EMPRESA_NOME}}
→ {{empresa.nome}}

{{EMPRESA_CNPJ}}
→ {{empresa.cnpj}}

{{CLIENTE_NOME}}
→ {{cliente.nome}}

{{CLIENTE_CPF_CNPJ}}
→ {{cliente.documento}}

{{PROJETO_CODIGO}}
→ {{projeto.codigo}}

{{PROJETO_VALOR_TOTAL}}
→ {{orcamento.valor_total}}

{{PROJETO_VALOR_POR_EXTENSO}}
→ {{orcamento.valor_total_extenso}}

{{PROJETO_COND_PAGAMENTO}}
→ {{orcamento.condicao_pagamento}}

{{DATA_ATUAL}}
→ {{documento.data}}

{{DATA_ATUAL_EXTENSO}}
→ {{documento.data_extenso}}

{{RECIBO_VALOR}}
→ {{recibo.valor}}

{{RECIBO_VALOR_EXTENSO}}
→ {{recibo.valor_extenso}}

Esses aliases servem apenas como mapa de migração.

Não precisam ser suportados permanentemente pelo novo motor.

93. Objetos legados HTML

Exemplos atuais como:

marcenaria.empresa_nome
marcenaria.empresa_logo_path
data_atual
data_hoje
valor_final
materiais
receitas
despesas
dre
folha
oc

não serão expostos diretamente na nova API documental.

Serão convertidos para contextos oficiais.

94. Exemplo de proposta comercial nova
{{empresa.logo}}

PROPOSTA COMERCIAL
Nº {{orcamento.codigo}}

Emitida em {{documento.data}}

Cliente:
{{cliente.nome}}

Local:
{{orcamento.entrega.endereco_completo}}

{{#orcamento.itens}}
{{item.nome}}
{{item.descricao}}
{{item.valor_total}}
{{/orcamento.itens}}

TOTAL:
{{orcamento.valor_total}}
95. Exemplo de recibo novo
RECIBO

Recebemos de {{recibo.pagador.nome}},
documento {{recibo.pagador.documento}},
o valor de {{recibo.valor}}
({{recibo.valor_extenso}}).

Referente a:
{{recibo.referente}}

Projeto:
{{projeto.codigo}}

Data:
{{recibo.data}}
96. Exemplo de contrato novo
CONTRATADA

{{empresa.razao_social}}
{{empresa.cnpj}}
{{empresa.endereco_completo}}

CONTRATANTE

{{cliente.nome}}
{{cliente.documento}}
{{cliente.endereco_completo}}

OBJETO

{{projeto.descricao}}

VALOR

{{orcamento.valor_total}}
({{orcamento.valor_total_extenso}})

PAGAMENTO

{{orcamento.condicao_pagamento}}
97. Exemplo de ordem de compra nova
ORDEM DE COMPRA
Nº {{compra.numero}}

Fornecedor:
{{fornecedor.nome_fantasia}}
{{fornecedor.documento}}

{{#compra.itens}}
{{item.material}}
{{item.quantidade}}
{{item.unidade}}
{{item.valor_unitario}}
{{item.valor_total}}
{{/compra.itens}}

TOTAL:
{{compra.valor_total}}
98. Exemplo de holerite novo
HOLERITE

Funcionário:
{{funcionario.nome}}

Competência:
{{folha.competencia}}

{{#folha.eventos}}
{{evento.codigo}}
{{evento.descricao}}
{{evento.referencia}}
{{evento.vencimento}}
{{evento.desconto}}
{{/folha.eventos}}

Total de vencimentos:
{{folha.total_vencimentos}}

Total de descontos:
{{folha.total_descontos}}

Líquido:
{{folha.liquido}}
99. Compatibilidade futura

Novas tags poderão ser adicionadas.

Tags existentes não deverão:

mudar de significado;
mudar silenciosamente de tipo;
ser reutilizadas para outra finalidade.

Caso uma tag precise ser removida:

marcar como deprecated;
indicar substituta;
manter período de migração;
remover somente em mudança de versão incompatível.
100. Catálogo implementável

No código futuro, cada tag deverá possuir metadados semelhantes a:

code
label
namespace
data_type
description
available_document_types
is_sensitive
is_derived
is_collection
status
101. Exemplo conceitual
code:
cliente.nome

label:
Nome do cliente

type:
text

contexts:
contract_individual
contract_corporate
budget
commercial_proposal
receipt
delivery_term

sensitive:
false

derived:
false
102. Relação com permissões

Visualizar uma tag na lista de tags não significa necessariamente ter acesso ao dado real.

Na geração:

permissão do usuário
+
tipo documental
+
tenant
+
contexto
=
dados liberados
103. Relação com auditoria

Geração documental deve registrar:

tipo;
template;
versão;
entidade;
usuário;
tenant.

Não é necessário registrar individualmente cada tag resolvida, salvo necessidade futura de auditoria avançada.

104. Relação com snapshot

O snapshot poderá utilizar chaves do catálogo oficial.

Exemplo:

{
  "cliente.nome": "João da Silva",
  "cliente.documento": "...",
  "orcamento.valor_total": "...",
  "documento.data": "..."
}

A estrutura técnica definitiva poderá ser hierárquica.

105. Relação com migração do legado

O migrador documental deverá possuir tabela explícita:

tag_legada
→
tag_oficial

Nenhuma substituição deve depender de tentativa heurística silenciosa.

106. Primeiro escopo implementado

Quando o Document Engine entrar em desenvolvimento, a primeira versão deve priorizar tags escalares de:

empresa
cliente
projeto
orcamento
recibo
documento
usuario

Isso cobre:

contrato;
aceite;
garantia;
recibo.
107. Segundo escopo

Depois:

fornecedor
compra
material

para:

ordem de compra;
lista de materiais.
108. Terceiro escopo

Depois:

funcionario
folha
ponto
financeiro

para:

holerite;
espelho de ponto;
relatório financeiro.
109. Regra final

O catálogo oficial é o contrato entre:

domínio
↓
application
↓
Document Context Resolver
↓
Document Engine
↓
template

Templates não conhecem:

ORM;
SQL;
repositories;
serviços internos;
modelos físicos do banco.

Eles conhecem apenas o catálogo oficial de tags.