# OrganizeG3 — Fiscal XML Draft Specification

**Status:** Especificação funcional oficial  
**Versão inicial:** 2026-08-10  
**Escopo:** Geração assistida de arquivo XML fiscal para conferência e utilização em sistema externo.

---

# 1. Objetivo

O OrganizeG3 poderá gerar um rascunho estruturado em XML contendo dados comerciais e fiscais já existentes no sistema.

O objetivo é:

- reduzir redigitação;
- diminuir erros manuais;
- facilitar o trabalho administrativo;
- facilitar o envio das informações ao escritório contábil;
- permitir utilização dos dados em software fiscal externo.

O OrganizeG3 não será, inicialmente, um emissor de NF-e.

---

# 2. Princípio central

O fluxo será:

```text
dados existentes no OrganizeG3
        ↓
pré-validação
        ↓
prévia fiscal
        ↓
geração do rascunho XML
        ↓
download/exportação
        ↓
escritório ou sistema fiscal externo
3. O que esta funcionalidade faz

A funcionalidade poderá:

reunir dados da empresa;
reunir dados do cliente;
reunir dados da venda;
reunir itens;
reunir valores;
reunir informações fiscais previamente cadastradas;
validar presença de informações necessárias;
mostrar uma prévia;
gerar arquivo XML estruturado;
permitir download;
registrar histórico da geração.
4. O que esta funcionalidade não faz inicialmente

Não fará:

transmissão para SEFAZ;
emissão automática de NF-e;
assinatura digital fiscal;
consulta de autorização;
consulta de protocolo;
cancelamento de NF-e;
carta de correção;
inutilização de numeração;
contingência fiscal;
armazenamento de certificado digital para transmissão;
comunicação direta obrigatória com Receita ou SEFAZ.
5. Natureza do arquivo

O XML será tratado como:

rascunho / arquivo de apoio fiscal

Não deve ser apresentado ao usuário como:

NF-e emitida

ou:

documento fiscal autorizado
6. Responsabilidade

O OrganizeG3 auxilia na preparação dos dados.

A conferência e o processamento fiscal definitivo continuam sendo realizados no sistema fiscal utilizado pela empresa ou pelo escritório responsável.

7. Origem dos dados

Os dados devem vir, sempre que possível, das entidades já existentes no OrganizeG3.

Exemplos:

empresa
cliente
venda
orçamento
itens
produtos
serviços
valores
frete
descontos
informações fiscais cadastradas
8. Evitar redigitação

A tela fiscal não deve solicitar novamente informações que já existem no sistema.

Exemplo incorreto:

cliente já possui CNPJ no cadastro
↓
usuário precisa digitar CNPJ novamente

Exemplo correto:

cliente possui CNPJ
↓
sistema preenche automaticamente
↓
usuário apenas confere
9. Prévia antes da geração

Antes de gerar o XML, o usuário deve visualizar uma prévia estruturada.

Exemplo:

DADOS DA EMPRESA

Razão social:
...

CNPJ:
...

DADOS DO CLIENTE

Nome / Razão social:
...

CPF/CNPJ:
...

ITENS

1. ...
2. ...
3. ...

VALORES

Produtos:
R$ ...

Serviços:
R$ ...

Frete:
R$ ...

Desconto:
R$ ...

Total:
R$ ...
10. Status da prévia

Campos poderão ser classificados como:

✓ válido
⚠ revisar
✗ obrigatório ausente
11. Bloqueio de geração

O sistema poderá bloquear geração quando faltar dado considerado obrigatório para o formato configurado.

Exemplo:

CNPJ da empresa ausente

Resultado:

Não foi possível gerar o rascunho.
Complete os dados fiscais da empresa.
12. Warning não bloqueante

Algumas situações podem gerar aviso sem impedir exportação.

Exemplo:

Inscrição Estadual não cadastrada.

O comportamento definitivo dependerá do perfil e formato do rascunho.

13. Dados da empresa

Campos previstos:

empresa.razao_social
empresa.nome_fantasia
empresa.cnpj
empresa.inscricao_estadual
empresa.endereco
empresa.numero
empresa.complemento
empresa.bairro
empresa.cidade
empresa.estado
empresa.cep
empresa.telefone
empresa.email
14. Dados do cliente

Campos previstos:

cliente.nome
cliente.razao_social
cliente.documento
cliente.inscricao_estadual
cliente.email
cliente.telefone
cliente.logradouro
cliente.numero
cliente.complemento
cliente.bairro
cliente.cidade
cliente.estado
cliente.cep
15. Pessoa física e jurídica

O gerador deverá respeitar:

cliente pessoa física
→ CPF

cliente pessoa jurídica
→ CNPJ

Não deve exigir CNPJ para pessoa física.

16. Venda de origem

O rascunho deve estar relacionado a uma origem comercial.

Preferencialmente:

venda

ou entidade equivalente definida no domínio comercial futuro.

Enquanto essa entidade não existir, poderá ser derivado de:

orçamento aprovado

desde que a regra seja explícita.

17. Não gerar a partir de orçamento preliminar

Um orçamento ainda em elaboração não deve produzir documento fiscal definitivo ou rascunho apresentado como venda concluída.

18. Itens

Cada item poderá conter:

codigo
descricao
quantidade
unidade
valor_unitario
valor_total
desconto
tipo
19. Dados fiscais do item

Futuramente poderão existir informações como:

NCM
CFOP sugerido/configurado
origem
unidade fiscal
classificação fiscal

Esses dados devem pertencer ao domínio apropriado.

O XML não deve inventar informações fiscais.

20. NCM

Quando o material/produto possuir NCM cadastrado:

item
↓
material/produto
↓
NCM

o gerador poderá reutilizá-lo.

21. CFOP

O OrganizeG3 poderá armazenar ou sugerir CFOP conforme configuração futura.

Entretanto:

CFOP

não deve ser inferido silenciosamente por regra simplista.

Se necessário:

utilizar configuração explícita;
permitir conferência;
permitir ajuste antes da exportação.
22. Serviços

Itens de serviço devem poder ser diferenciados de itens de produto quando isso for necessário ao arquivo de apoio.

23. Material interno não é item fiscal automaticamente

O orçamento pode possuir:

MDF;
ferragens;
insumos;
mão de obra interna.

Isso não significa que todos esses componentes devam aparecer individualmente no documento fiscal.

A composição fiscal deve seguir o item comercial/vendido.

24. Separação importante
estrutura de custo
≠
estrutura fiscal

O orçamento interno pode possuir dezenas de componentes.

A venda pode possuir apenas:

Móveis planejados sob medida

ou outra composição comercial definida pela empresa.

25. Fonte dos itens fiscais

O módulo Comercial deverá futuramente definir quais itens representam efetivamente o que será informado no rascunho fiscal.

26. Valores

Campos previstos:

subtotal
desconto
acrescimo
frete
outras_despesas
valor_produtos
valor_servicos
valor_total
27. Decimal

Todos os valores devem utilizar representação monetária segura.

Não utilizar float como base de cálculo fiscal.

28. Arredondamento

Regras de arredondamento deverão ser centralizadas.

O template/XML não realiza cálculos livres.

29. Totais

O gerador deve receber valores já determinados pelo domínio.

Exemplo incorreto:

XML soma itens por conta própria

Exemplo correto:

domínio/application determina total
↓
gerador valida consistência
↓
XML apresenta total
30. Validação de consistência

Antes da exportação:

soma de itens
x
total informado

pode ser comparada.

Diferenças relevantes devem gerar erro ou warning.

31. Observações

O rascunho poderá conter campos como:

observacoes
informacoes_complementares
referencia_do_projeto
numero_do_orcamento
numero_do_pedido
32. Referência ao projeto

O XML de apoio poderá carregar referência interna como:

PRJ-2027-0042

quando houver campo apropriado para observação/referência.

33. Número do documento interno

O OrganizeG3 poderá possuir:

draft_number

para controle interno.

Esse número não deve ser confundido com número oficial de NF-e.

34. Estado do rascunho

Estados conceituais:

draft
ready
exported
cancelled
35. draft

Dados ainda podem ser corrigidos.

36. ready

Validações obrigatórias foram satisfeitas.

37. exported

Arquivo foi gerado/exportado.

Isso não significa que uma NF-e foi emitida.

38. cancelled

Rascunho não será mais utilizado.

39. Arquivo gerado

Nome sugerido:

Rascunho Fiscal - Cliente - Projeto - 2027-0042.xml

O filename deve ser sanitizado.

40. Histórico

Registrar:

id
tenant_id
source_entity_type
source_entity_id
draft_number
generated_at
generated_by
filename
storage_reference quando aplicável
status
41. Snapshot

O rascunho exportado deve preservar os dados usados naquele momento.

Alteração posterior do cliente não deve modificar o XML já gerado.

42. Nova geração

Se os dados forem corrigidos depois:

gerar novo rascunho

não sobrescrever silenciosamente o histórico anterior quando ele já tiver sido exportado.

43. Versionamento

Pode existir:

Rascunho 1
Rascunho 2

para a mesma venda.

44. Document Engine

O XML fiscal não deve ser tratado como template livre DOCX/HTML.

Ele poderá reutilizar componentes do Document Engine, como:

histórico;
storage;
geração;
auditoria.

Porém utilizará renderer estrutural próprio.

45. Renderer

Nome conceitual:

FiscalXmlDraftRenderer
46. Contrato estrutural

O renderer deve receber DTO seguro.

Exemplo conceitual:

FiscalDraftContext

Ele não deve receber:

Session SQLAlchemy;
repository;
ORM models;
request HTTP.
47. Fluxo arquitetural
CreateFiscalDraftUseCase
        ↓
FiscalDraftContextResolver
        ↓
FiscalDraftValidator
        ↓
FiscalXmlDraftRenderer
        ↓
XML
48. Validação antes do renderer

O renderer não deve decidir regras comerciais ou fiscais de alto nível.

Ele apenas serializa um contexto já validado.

49. Estrutura própria

A estrutura XML será definida tecnicamente quando a integração com o software utilizado pelo escritório for estudada.

Esta especificação não define agora:

schema definitivo;
namespaces XML definitivos;
versão de layout;
campos específicos de um fornecedor de software.
50. Perfis de exportação

Futuramente poderá existir:

Perfil de exportação fiscal

Exemplo:

Escritório Contábil A
Sistema Fiscal B
Formato Genérico
51. Motivo dos perfis

Softwares externos podem exigir formatos diferentes.

Não acoplar todo o OrganizeG3 a um único importador.

52. Primeiro formato

Antes da implementação real, deverá ser analisado o formato aceito pelo sistema utilizado pelo escritório da empresa piloto.

53. Importador externo

Se o escritório fornecer:

documentação;
exemplo XML;
schema;
arquivo modelo;

esse material passa a ser a referência técnica da primeira integração.

54. Não presumir padrão

Não assumir que qualquer XML criado será automaticamente aceito por um software fiscal.

A compatibilidade deverá ser validada com o sistema real de destino.

55. Teste de importação

Gate obrigatório antes de considerar o recurso pronto:

gerar arquivo
↓
importar no software externo
↓
verificar campos
↓
corrigir mapeamentos
↓
repetir
56. Dados fiscais configuráveis

Alguns campos poderão precisar de configuração empresarial.

Exemplos:

natureza_da_operacao
regime
observacao_padrao
CFOP padrão quando aplicável

A lista definitiva será definida posteriormente.

57. Não hardcodar dados da empresa

Nenhum dado fiscal da empresa deverá ser escrito diretamente no gerador.

Sempre utilizar configuração/dados do tenant.

58. Multi-tenant

Cada empresa possui seus próprios:

dados fiscais;
configurações;
perfis de exportação;
históricos.

Nunca cruzar dados entre tenants.

59. Filial

Quando a operação ocorrer por filial:

filial

pode ser o emitente/contexto empresarial relevante conforme configuração do negócio.

A regra definitiva dependerá do módulo fiscal/comercial.

60. Permissões

Permissões futuras sugeridas:

fiscal_drafts.read
fiscal_drafts.create
fiscal_drafts.export
fiscal_drafts.cancel
fiscal_settings.read
fiscal_settings.manage
61. Dados sensíveis

CPF/CNPJ, endereço e informações fiscais devem respeitar políticas de acesso da plataforma.

62. Auditoria

Eventos sugeridos:

fiscal_draft.created
fiscal_draft.validated
fiscal_draft.exported
fiscal_draft.regenerated
fiscal_draft.cancelled
63. Falhas

Códigos conceituais:

fiscal_draft.missing_required_data
fiscal_draft.invalid_customer_document
fiscal_draft.invalid_company_data
fiscal_draft.total_mismatch
fiscal_draft.export_failed
fiscal_draft.unsupported_profile
64. Correção de dados

Quando faltar informação, o sistema deve indicar onde corrigir.

Exemplo:

CNPJ da empresa ausente.

[Ir para Empresa]

Outro:

NCM do item não informado.

[Ir para Material]
65. Não duplicar cadastro

A tela fiscal não deve virar um segundo cadastro de:

empresa;
cliente;
material.

Ela deve apontar para a origem oficial do dado.

66. Override excepcional

Futuramente pode existir ajuste específico do rascunho.

Exemplo:

observação desta operação

Mas dados mestres devem preferencialmente ser corrigidos na origem.

67. Dados históricos

Quando um rascunho já foi exportado, ele deve preservar seu snapshot mesmo que o cadastro mestre seja alterado.

68. Ligação com orçamento

No futuro:

Orçamento
↓
Aprovação
↓
Venda/Pedido
↓
Rascunho fiscal

O rascunho não deve ser o responsável por aprovar venda.

69. Ligação com financeiro

Gerar rascunho fiscal não deve automaticamente alterar:

contas a receber;
pagamento;
fluxo de caixa.

Esses eventos pertencem aos respectivos módulos.

70. Ligação com produção

A geração fiscal não deve alterar estado de produção.

71. Arquivo local ou cloud

O rascunho poderá:

ser baixado diretamente;
ser armazenado no histórico;
ser copiado para workspace quando fizer sentido.
72. Workspace

Quando relacionado a projeto, poderá ser salvo em destino lógico como:

documents

ou futura pasta:

Fiscal

A empresa poderá definir essa organização.

73. Primeiro uso recomendado

Fluxo de UI futuro:

Venda / Projeto
        ↓
Gerar rascunho fiscal
        ↓
Prévia
        ↓
Validar
        ↓
Gerar XML
        ↓
Abrir pasta / baixar
74. Tela de prévia

Seções recomendadas:

Empresa
Cliente
Operação
Itens
Totais
Dados fiscais
Observações
Validação
75. Correções

A prévia deve mostrar claramente:

campo
valor atual
origem
status
76. Exemplo
Cliente.documento
12.345.678/0001-90
Origem: Cadastro do Cliente
✓
77. Validação central

Não espalhar validação fiscal em componentes React.

Regras pertencem ao backend/application/domínio apropriado.

78. PWA

O PWA poderá futuramente:

visualizar rascunho;
solicitar geração;
baixar arquivo;

se o usuário possuir permissão.

79. Desktop

O desktop poderá facilitar:

salvar localmente;
abrir pasta;
copiar para workspace.
80. Migração

Não é necessário migrar rascunhos XML antigos se não existirem arquivos históricos relevantes.

Se existirem:

preservar arquivo;
classificar como documento legado;
associar quando possível.
81. Templates antigos

Qualquer gerador XML legado deve servir somente como referência funcional.

Não copiar lógica antiga sem revisão.

82. Segurança XML

O renderer deverá impedir:

XML inválido;
conteúdo não escapado;
injeção estrutural;
leitura arbitrária de arquivo;
entidades externas inseguras.
83. Encoding

O arquivo deverá utilizar encoding explícito e consistente.

Preferência:

UTF-8

salvo exigência comprovada do importador externo.

84. Determinismo

Para os mesmos dados e mesma versão de perfil, o conteúdo estrutural deve ser previsível.

85. Perfil versionado

Quando existir perfil de exportação:

profile_version

deve ser registrado no rascunho gerado.

Assim alterações futuras no formato podem ser rastreadas.

86. Compatibilidade

Se o software externo mudar seu layout:

criar nova versão;
não alterar silenciosamente XML histórico;
manter rastreabilidade.
87. Testes unitários futuros

Cobrir:

empresa válida;
empresa inválida;
cliente PF;
cliente PJ;
documento inválido;
item sem campo obrigatório;
valores;
arredondamento;
caracteres especiais;
XML escapado;
geração determinística.
88. Testes de integração

Cobrir:

contexto completo;
storage;
auditoria;
tenant isolation;
permissões.
89. Teste externo

O teste mais importante será:

arquivo real
↓
software do escritório
↓
importação aceita
90. Gate de implementação

A funcionalidade somente será considerada pronta quando:

contexto de dados definido
validação definida
perfil de exportação definido
arquivo XML válido
teste automatizado verde
importação externa validada
91. Escopo da primeira implementação

Quando chegar a fase desta funcionalidade:

1. identificar software/importador utilizado
2. obter exemplo/documentação do formato
3. mapear dados OrganizeG3 → formato
4. criar contexto
5. validar
6. gerar XML
7. exportar
8. testar importação
92. Evoluções futuras possíveis

Somente se houver necessidade real:

mais perfis de exportação
integração com contador
validação fiscal mais avançada
integração direta com emissor externo
93. Emissão direta futura

Uma eventual emissão direta de NF-e seria outro projeto funcional.

Ela exigiria tratamento próprio de:

legislação;
certificados;
segurança;
transmissão;
contingência;
protocolos;
eventos fiscais.

Não deve ser confundida com esta funcionalidade.

94. Regra final

O OrganizeG3 não precisa substituir o sistema fiscal utilizado pelo escritório.

Ele deve eliminar trabalho repetitivo.

Objetivo:

dados já cadastrados
↓
reaproveitar
↓
validar
↓
exportar
↓
escritório trabalha com menos redigitação

Essa é a finalidade do Rascunho XML Fiscal.