# OrganizeG3 — Document Engine Specification

**Status:** Especificação funcional oficial  
**Versão inicial:** 2026-08-10  
**Escopo:** Geração, personalização, validação e armazenamento de documentos do OrganizeG3.

---

# 1. Objetivo

O Document Engine é o mecanismo central responsável por gerar documentos a partir dos dados existentes no OrganizeG3.

Ele deve permitir:

- templates padrão fornecidos pelo sistema;
- templates personalizados por empresa;
- preenchimento automático por tags;
- documentos editáveis;
- relatórios estruturados;
- validação de templates;
- histórico de documentos gerados;
- segurança e permissões;
- evolução futura sem quebrar documentos existentes.

---

# 2. Princípio central

O OrganizeG3 controla:

- os dados;
- as tags disponíveis;
- a validação;
- a geração;
- o histórico.

A empresa controla:

- aparência;
- textos;
- cláusulas;
- fontes;
- cores;
- logotipo;
- disposição visual;
- escolha do template padrão.

---

# 3. Template e documento gerado

Template e documento gerado são entidades diferentes.

## 3.1 Template

É um modelo reutilizável.

Exemplos:

- contrato padrão;
- termo de garantia;
- recibo;
- proposta comercial;
- orçamento;
- holerite.

Pode ser:

- fornecido pelo OrganizeG3;
- criado pela empresa;
- duplicado;
- alterado;
- ativado;
- desativado;
- definido como padrão.

## 3.2 Documento gerado

É uma cópia produzida a partir de:

- template;
- dados;
- contexto;
- usuário;
- data.

Após a geração:

- pode ser editado quando o formato permitir;
- não altera o template de origem;
- deve manter vínculo histórico com a versão utilizada.

---

# 4. Tipos de documento suportados

O Document Engine possuirá dois mecanismos principais.

---

## 4.1 DOCX editável

Indicado para documentos cujo conteúdo textual pode ser alterado após a geração.

Exemplos:

- contrato PF;
- contrato PJ;
- termo de aceite;
- termo de garantia;
- recibo;
- declarações;
- termos personalizados.

Características:

- empresa pode editar no Word;
- mantém formatação do template;
- tags são substituídas automaticamente;
- documento gerado continua editável;
- pode posteriormente ser convertido para PDF.

---

## 4.2 HTML estruturado → PDF

Indicado para relatórios e documentos altamente estruturados.

Exemplos:

- orçamento;
- proposta comercial;
- lista de materiais;
- ordem de compra;
- relatório financeiro;
- holerite;
- espelho de ponto;
- termo de entrega estruturado.

Características:

- suporta tabelas;
- listas;
- totais;
- repetição de itens;
- condicionais;
- paginação;
- geração previsível de PDF.

---

# 5. Templates padrão do OrganizeG3

O OrganizeG3 fornecerá modelos iniciais.

Os modelos atualmente conhecidos são:

- contrato PF;
- contrato PJ;
- termo de aceite;
- termo de garantia;
- recibo;
- orçamento;
- proposta comercial;
- lista de materiais;
- ordem de compra;
- termo de entrega;
- holerite;
- espelho de ponto;
- relatório financeiro.

Os arquivos atuais servem como referência funcional.

A nomenclatura técnica das tags poderá ser alterada.

---

# 6. Templates por tenant

Todo template empresarial deve pertencer a um tenant.

Um tenant não pode:

- visualizar templates privados de outro tenant;
- editar templates de outro tenant;
- gerar documentos com template de outro tenant.

Templates padrão do OrganizeG3 podem ser globais e somente leitura.

---

# 7. Tipos de propriedade do template

Um template deve possuir pelo menos:

- id;
- tenant_id quando personalizado;
- document_type;
- name;
- description;
- format;
- source;
- version;
- is_system_template;
- is_default;
- is_active;
- created_at;
- updated_at;
- created_by;
- updated_by.

---

# 8. Tipo documental

O tipo documental identifica a finalidade do template.

Exemplos:

```text
contract_individual
contract_corporate
project_acceptance
warranty
receipt
budget
commercial_proposal
material_list
purchase_order
delivery_term
pay_stub
timesheet
financial_report

O tipo não deve depender do nome do arquivo.

9. Mais de um template por tipo

Uma empresa poderá possuir múltiplos templates do mesmo tipo.

Exemplo:

Contrato padrão
Contrato simplificado
Contrato para reforma
Contrato para órgão público

Somente um poderá ser o padrão por contexto, quando aplicável.

10. Template padrão

Para cada tipo documental, a empresa poderá definir um template padrão.

Se não possuir template próprio:

usar template padrão do OrganizeG3;
permitir duplicação;
permitir personalização da cópia.
11. Versionamento

Templates deverão ser preparados para versionamento desde a arquitetura inicial.

Exemplo:

Contrato padrão

v1
criado em 01/01/2027
inativo

v2
criado em 15/07/2027
ativo

Documento já gerado deve registrar a versão usada.

Alterações futuras no template não podem alterar documentos históricos.

12. Geração

Fluxo conceitual:

usuário solicita documento
        ↓
sistema identifica contexto
        ↓
seleciona template
        ↓
resolve tags
        ↓
valida dados
        ↓
gera documento
        ↓
registra histórico
        ↓
entrega arquivo
13. Contexto de geração

A geração sempre ocorre dentro de um contexto.

Exemplos:

cliente
projeto
orçamento
compra
funcionário
folha
financeiro
entrega

O contexto define quais tags estão disponíveis.

14. Catálogo oficial de tags

Todas as tags deverão existir em catálogo central.

Nenhum módulo pode inventar tags diretamente dentro do código.

Exemplos de namespaces:

empresa.*
filial.*
cliente.*
fornecedor.*
projeto.*
orcamento.*
pagamento.*
recibo.*
compra.*
material.*
funcionario.*
folha.*
ponto.*
financeiro.*
documento.*
usuario.*

A especificação completa ficará em:

DOCUMENT_TAG_CATALOG.md

15. Convenção de nomenclatura

A nova convenção será:

{{namespace.campo}}

Exemplos:

{{empresa.nome}}
{{empresa.cnpj}}
{{cliente.nome}}
{{projeto.codigo}}
{{orcamento.valor_total}}
{{documento.data}}

Não existe obrigação de preservar tags legadas em letras maiúsculas.

Os templates atuais poderão ser migrados para a convenção oficial.

16. Tipo de dado da tag

Cada tag deverá declarar seu tipo.

Tipos iniciais:

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
17. Formatação

A tag representa um dado lógico.

A formatação pode ser resolvida automaticamente.

Exemplo:

{{orcamento.valor_total}}

Pode renderizar:

R$ 12.450,00

quando a tag tiver tipo money.

18. Formatações derivadas

Alguns valores poderão possuir variações oficiais.

Exemplo:

{{documento.data}}
{{documento.data_extenso}}

{{orcamento.valor_total}}
{{orcamento.valor_total_extenso}}

Essas variações devem existir no catálogo, não serem implementadas arbitrariamente nos templates.

19. Campos opcionais

Uma tag pode ser:

obrigatória;
opcional;
condicional.

Quando um valor opcional estiver ausente:

o motor não deve inserir None;
não deve inserir null;
não deve quebrar o documento;
deve utilizar representação vazia ou comportamento definido pelo tipo documental.
20. Validação de template

Antes de um template personalizado ser ativado, o sistema deve conseguir validá-lo.

A validação deve identificar:

tags reconhecidas;
tags desconhecidas;
tags indisponíveis para aquele tipo;
tags obrigatórias ausentes quando aplicável;
sintaxe inválida;
blocos não fechados;
problemas de imagem;
problemas estruturais relevantes.
21. Resultado da validação

Exemplo:

Template: Contrato padrão

✓ {{empresa.nome}}
✓ {{cliente.nome}}
✓ {{projeto.codigo}}

⚠ {{cliente.apelido}}
Tag desconhecida

✗ bloco {{#orcamento.itens}}
não foi fechado
22. Níveis de validação

O validador deverá classificar problemas como:

info
warning
error

Template com erro estrutural não poderá ser ativado.

Warnings poderão ser aceitos dependendo da situação.

23. Teste de geração

A empresa deverá futuramente poder executar:

Testar template

O sistema utilizará dados fictícios seguros para gerar uma prévia.

Isso evita necessidade de usar dados reais de clientes.

24. Preview

Quando tecnicamente possível, o OrganizeG3 poderá oferecer:

preview de DOCX;
preview de PDF;
download do teste.

Preview não é requisito da primeira implementação do motor.

25. Imagens

Templates poderão utilizar tags do tipo imagem.

Exemplo:

{{empresa.logo}}

O motor deverá:

localizar arquivo autorizado;
validar existência;
limitar tamanho;
inserir imagem;
preservar proporção quando possível.
26. Listas

Documentos estruturados precisam suportar coleções.

Exemplos:

itens de orçamento;
itens de compra;
materiais;
eventos de folha;
apontamentos de ponto;
lançamentos financeiros.

Conceito:

{{#orcamento.itens}}

{{descricao}}
{{quantidade}}
{{valor_unitario}}
{{valor_total}}

{{/orcamento.itens}}

A sintaxe definitiva será definida antes da implementação.

27. Condicionais

HTML estruturado poderá utilizar condições controladas.

Exemplo conceitual:

se desconto existir
    exibir desconto

Templates não deverão executar código arbitrário.

28. Segurança do template

Templates personalizados são dados potencialmente não confiáveis.

O motor não deve permitir:

execução arbitrária de Python;
acesso livre ao filesystem;
execução de comandos;
acesso a variáveis internas não autorizadas;
consultas diretas ao banco;
leitura de dados de outro tenant.
29. Resolver de dados

O template não acessa repositories diretamente.

Fluxo:

DocumentGenerationUseCase
        ↓
DocumentContextResolver
        ↓
DTO seguro de documento
        ↓
TemplateRenderer

Isso separa:

banco;
regra de negócio;
template;
renderização.
30. Snapshot de dados

Quando necessário, o documento gerado deverá preservar os dados utilizados na geração.

Exemplo:

um contrato emitido hoje não deve mudar porque amanhã o cliente alterou o endereço.

Possíveis estratégias:

snapshot JSON;
dados materializados no arquivo;
ambos.

A definição técnica ocorrerá na implementação do módulo documental.

31. Histórico do documento

Um documento gerado deverá poder registrar:

id;
tenant_id;
document_type;
template_id;
template_version;
entity_type;
entity_id;
filename;
storage_reference;
generated_at;
generated_by;
metadata;
optional data snapshot.
32. Documento editado após geração

Documentos DOCX poderão ser alterados depois de gerados.

O sistema não precisa interpretar novamente todas as alterações feitas manualmente.

A cópia editada passa a ser o documento operacional final.

33. Documento imutável quando necessário

Alguns documentos poderão futuramente possuir estado:

draft
generated
final
cancelled

Após estado final, substituições devem gerar nova versão, não sobrescrever silenciosamente o arquivo.

34. Armazenamento

O mecanismo deverá suportar referência a documentos em:

storage cloud;
workspace local;
ambos, dependendo do documento.

A política será definida por tipo.

35. Integração com Workspace

Quando existir workspace local:

Projeto
└── 05 Documentos

documentos relacionados ao projeto poderão ser copiados para esse diretório.

O banco continuará mantendo a referência e o histórico.

36. Nomenclatura de arquivo

O nome do arquivo gerado deve ser determinístico e sanitizado.

Exemplo:

Contrato - João da Silva - PRJ-2027-0042.docx

Não utilizar caracteres inválidos para filesystem.

37. Auditoria

Eventos relevantes:

document_template.created
document_template.updated
document_template.activated
document_template.deactivated
document_template.set_default
document.generated
document.regenerated
document.finalized
document.cancelled
38. Permissões

Permissões futuras sugeridas:

documents.read
documents.generate
documents.manage
document_templates.read
document_templates.create
document_templates.update
document_templates.delete
document_templates.set_default

O catálogo definitivo será integrado ao catálogo geral de permissões.

39. Templates de sistema

Templates fornecidos pelo OrganizeG3:

não pertencem a um tenant;
são somente leitura;
podem ser duplicados;
podem receber atualizações em novas versões do sistema.

Atualizar template de sistema não pode alterar cópia personalizada da empresa.

40. Templates personalizados

Templates personalizados:

pertencem ao tenant;
podem ser editados;
podem ser desativados;
podem ser versionados;
podem ser definidos como padrão;
nunca são compartilhados implicitamente com outro tenant.
41. Migração dos templates atuais

Os modelos atuais serão utilizados como base funcional.

Não é necessário preservar:

nomes antigos das tags;
mecanismos internos antigos;
sintaxe inconsistente;
dados hardcoded.

Deve ser preservado:

finalidade do documento;
conteúdo útil;
campos necessários;
possibilidade de personalização.
42. Inconsistências do legado

Durante a migração dos templates deverão ser corrigidos:

campos de empresa escritos diretamente;
tags diferentes para o mesmo conceito;
duplicidade de nomenclatura;
HTML com acesso excessivo a objetos;
placeholders incompatíveis;
codificação inconsistente;
valores visuais não reutilizáveis quando isso afetar templates padrão.

A empresa continuará livre para formatar seus documentos personalizados.

43. Rascunho XML fiscal

O gerador de rascunho XML não deve reutilizar templates livres.

Ele terá estrutura própria e validada.

Motivo:

XML possui contrato estrutural e não deve aceitar texto arbitrário.

44. Relatórios

Relatórios estruturados poderão utilizar o mesmo motor de contexto e tags, mas renderizadores específicos.

Exemplos:

HTML renderer
DOCX renderer
PDF renderer
XML draft renderer
45. Falha de geração

Em caso de falha:

nenhum documento incompleto deve ser marcado como final;
erro deve possuir correlation id;
evento de auditoria deve registrar falha quando apropriado;
arquivo parcial deve ser descartado ou explicitamente marcado como temporário.
46. Compatibilidade

A primeira implementação nova não precisa manter compatibilidade sintática com os templates legados.

A migração será feita uma vez para o novo catálogo.

Isso evita carregar dívida técnica permanentemente.

47. Primeira versão funcional

A primeira implementação deverá priorizar:

1. catálogo central de tags
2. DOCX simples
3. substituição de campos escalares
4. logo
5. validação
6. template padrão por tenant
7. geração
8. histórico
9. arquivo final editável

Loops complexos e condicionais avançadas podem entrar depois.

48. Evolução posterior

Depois da primeira versão:

listas
condicionais
preview
versionamento avançado
templates duplicáveis pela interface
editor de metadados
mais renderizadores
assinatura
fluxo de aprovação documental
49. Princípio final

O Document Engine deve ser um serviço de plataforma.

Nenhum módulo deve implementar geração documental isoladamente.

Exemplo incorreto:

CustomerPage → gera recibo diretamente

Exemplo correto:

Finance / Receipt UseCase
        ↓
Document Engine
        ↓
Receipt Context
        ↓
Template
        ↓
Documento