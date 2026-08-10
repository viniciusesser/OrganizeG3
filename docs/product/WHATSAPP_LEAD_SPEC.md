# OrganizeG3 — WhatsApp Lead Specification

**Status:** Especificação funcional oficial  
**Versão inicial:** 2026-08-10  
**Escopo:** Entrada comercial simples por WhatsApp e transformação de contatos em leads dentro do OrganizeG3.

---

# 1. Objetivo

O OrganizeG3 deverá permitir que empresas utilizem o WhatsApp como principal porta de entrada comercial sem exigir que o cliente preencha formulários extensos.

O objetivo é:

- reduzir atrito para o cliente;
- facilitar primeiro contato;
- acelerar cadastro do lead;
- organizar internamente contatos recebidos;
- evitar perda de oportunidades;
- manter histórico comercial;
- preparar o lead para futura conversão em cliente.

---

# 2. Princípio central

O cliente não precisa conhecer o OrganizeG3.

Fluxo principal:

```text
cliente
↓
WhatsApp
↓
empresa recebe contato
↓
cadastro rápido do lead
↓
funil comercial
↓
qualificação
↓
cliente / oportunidade
3. WhatsApp como canal, não como banco

O WhatsApp é um canal de comunicação.

O OrganizeG3 é o sistema oficial de organização comercial.

Não depender do histórico do WhatsApp como única fonte de informação.

4. Primeiro contato

Um contato pode chegar por:

WhatsApp;
telefone;
indicação;
Instagram;
presencial;
site;
outro canal.

WhatsApp será priorizado pela facilidade de uso.

5. Cadastro rápido de lead

O primeiro cadastro deve exigir o mínimo possível.

Campos iniciais recomendados:

nome
telefone
interesse
observacao
origem
responsavel
6. Campos obrigatórios iniciais

Inicialmente:

nome
telefone

ou, quando o nome ainda não for conhecido:

telefone

A regra final poderá aceitar cadastro provisório somente pelo número.

7. Campos opcionais

Podem ser preenchidos depois:

email
cidade
endereco
tipo_de_projeto
prazo_desejado
orcamento_estimado
observacoes
origem_detalhada
8. Não exigir formulário do cliente

O fluxo principal não deve obrigar o cliente a preencher:

CPF;
endereço completo;
profissão;
medidas;
orçamento desejado;
questionário longo;
cadastro no sistema.

Esses dados serão coletados progressivamente quando realmente necessários.

9. Cadastro progressivo

O lead pode começar assim:

Maria
(18) 99999-9999
Cozinha

Depois evoluir para:

Maria da Silva
telefone
endereço
visita
medidas
necessidades
orçamento
10. Origem

Todo lead poderá registrar origem.

Valores iniciais sugeridos:

whatsapp
instagram
facebook
site
indicacao
telefone
presencial
outro
11. Origem detalhada

Campo opcional:

origin_detail

Exemplo:

Indicação de João da Silva
12. Responsável

Um lead poderá possuir responsável comercial.

Exemplo:

responsible_user_id
13. Empresas pequenas

Empresas sem vendedor dedicado poderão:

deixar responsável vazio;
atribuir ao administrador;
utilizar fila comercial compartilhada.
14. Status do lead

Estados conceituais iniciais:

new
contacted
qualified
unqualified
converted
lost

A máquina definitiva será definida no módulo comercial.

15. new

Lead cadastrado e ainda não tratado.

16. contacted

A empresa já iniciou contato.

17. qualified

Existe interesse real e informações mínimas suficientes para avançar.

18. unqualified

O contato não está pronto ou não se encaixa no atendimento atual.

Não significa necessariamente perda definitiva.

19. converted

O lead foi convertido para entidade comercial seguinte.

Pode resultar em:

cliente;
oportunidade;
visita;
projeto comercial.
20. lost

O lead foi encerrado sem conversão.

21. Motivo de perda

Perda deverá registrar motivo.

Exemplos:

sem_retorno
preco
prazo
fora_da_area
nao_atendemos_servico
desistiu
fechou_com_concorrente
duplicado
outro
22. Observação de perda

Quando necessário:

lost_reason_notes
23. Lead e cliente são diferentes

Um lead não é automaticamente um cliente.

Lead
↓
qualificação
↓
conversão
↓
Customer
24. Conversão idempotente

Converter o mesmo lead duas vezes não deve criar dois clientes.

A conversão deve ser idempotente.

25. Vínculo após conversão

O lead deverá manter referência ao cliente criado.

Exemplo:

converted_customer_id
26. Histórico preservado

Converter lead não apaga:

origem;
observações;
atividades;
datas;
responsável;
histórico.
27. Duplicidade

Antes de criar lead, verificar possíveis correspondências.

Principalmente por:

telefone

E futuramente:

email
documento
28. Número já cadastrado

Exemplo:

Este telefone já está associado a:
João da Silva

Ações:

Abrir cadastro
Criar novo mesmo assim
Cancelar

A possibilidade de criar duplicado pode depender de permissão/regra.

29. Normalização de telefone

Telefone deve ser normalizado.

Exemplo de armazenamento lógico:

5518999999999

Apresentação:

+55 (18) 99999-9999

A regra definitiva deverá seguir o mecanismo central de telefone da plataforma.

30. WhatsApp URL

A primeira integração pode ser simples:

abrir conversa

usando o número já cadastrado.

Não exige API oficial do WhatsApp.

31. Ação Abrir WhatsApp

Disponível em:

lead;
cliente;
fornecedor quando útil;
contato.
32. Mensagem vazia

A ação poderá simplesmente abrir a conversa sem texto pré-preenchido.

33. Mensagens-modelo

Futuramente poderá existir:

Olá {{cliente.nome}}, tudo bem?

ou:

Olá {{lead.nome}}, conforme conversamos...
34. Templates de mensagem

Os modelos poderão ser configuráveis por empresa.

Exemplos:

primeiro contato
confirmacao de visita
orcamento enviado
lembrete
agendamento
pos-venda
35. Não transformar WhatsApp em automação invasiva

O OrganizeG3 não deve enviar mensagens em massa automaticamente sem necessidade clara.

Prioridade:

ação humana assistida
36. Integração oficial futura

Caso exista demanda:

WhatsApp Business Platform;
provedor oficial;
webhooks;
mensagens aprovadas.

Isso é evolução futura.

37. Não depender de integração oficial inicialmente

A primeira versão comercial deve funcionar mesmo sem API do WhatsApp.

38. Cadastro durante conversa

Fluxo desejado:

WhatsApp aberto
↓
cliente conversa
↓
funcionário abre OrganizeG3
↓
Novo Lead
↓
nome + telefone + interesse
↓
Salvar

Tempo esperado: poucos segundos.

39. Cadastro rápido global

O sistema poderá oferecer atalho:

+ Novo Lead

em:

dashboard;
comercial;
menu de ações rápidas.
40. Clipboard

Futuramente o desktop poderá facilitar colagem de telefone copiado.

Não é requisito inicial.

41. Observações comerciais

Lead pode receber observações livres.

Exemplo:

Quer cozinha e lavanderia.
Prefere atendimento depois das 18h.
Foi indicação do Marcos.
42. Atividades

Futuramente:

lead_activity

Tipos:

call
whatsapp
visit
note
follow_up
status_change
43. Histórico de atividades

Exemplo:

10/08 09:10 — Lead criado
10/08 09:15 — WhatsApp aberto
11/08 14:00 — Visita agendada
12/08 18:30 — Lead qualificado
44. Follow-up

O lead poderá possuir:

next_follow_up_at
45. Pendência comercial

Follow-up vencido poderá alimentar:

Central de Pendências
46. Exemplo de pendência
Lead Maria da Silva
Retorno previsto para ontem
47. Agenda

Uma atividade comercial poderá gerar compromisso.

Exemplo:

Visita técnica
48. Visita

Após qualificação, lead poderá avançar para visita.

Dados possíveis:

data
horario
endereco
responsavel
observacoes
49. Funil comercial

O fluxo comercial inicial conhecido é:

Lead
↓
Visita
↓
Orçamento
↓
Aguardando Aprovação

O módulo comercial futuro poderá tornar etapas intermediárias configuráveis.

50. Não misturar lead com produção

Lead não deve criar:

ordem de produção;
reserva de estoque;
compra;
financeiro.
51. Conversão comercial

Somente após avanço apropriado surgem entidades posteriores.

52. Lead sem cliente

É permitido.

53. Cliente sem lead

Também é permitido.

Exemplos:

cadastro manual;
cliente legado;
órgão público;
relacionamento anterior.
54. Histórico de origem

Se um cliente veio de lead:

customer.source_lead_id

ou relacionamento equivalente poderá preservar a origem.

55. Cliente recorrente

Novo interesse de cliente existente não precisa criar outro Customer.

Pode criar:

nova oportunidade

ou novo projeto/orçamento.

56. Oportunidade

Conceito futuro recomendado:

Opportunity

Representa uma intenção comercial específica.

Exemplo:

Cliente João
↓
Oportunidade 1 — Cozinha
Oportunidade 2 — Quarto
57. Lead x oportunidade

Inicialmente podemos manter fluxo simples.

Futuramente:

Lead
↓
Customer
↓
Opportunity
↓
Budget

A implementação definitiva será feita no módulo Comercial.

58. Informações do interesse

Campos futuros possíveis:

project_type
environments
desired_deadline
location
notes
59. Não coletar cedo demais

Esses campos não precisam ser obrigatórios no primeiro contato.

60. Local de instalação

Quando conhecido:

cidade
bairro
endereco

Pode ajudar a decidir viabilidade da visita.

61. Área de atendimento

Futuramente empresa poderá configurar região atendida.

Lead fora da área poderá gerar aviso.

62. Privacidade

Lead contém dados pessoais.

Aplicar:

tenant isolation;
permissões;
acesso controlado;
auditoria quando apropriado.
63. Permissões

Permissões futuras sugeridas:

leads.read
leads.create
leads.update
leads.convert
leads.assign
leads.close
64. Perfil vendedor

Vendedor poderá visualizar:

leads atribuídos;
atividades;
contatos;
próximos retornos.

Dependendo da configuração da empresa.

65. Perfil administrador

Pode visualizar todo o funil.

66. Empresas sem equipe comercial

Podem operar sem complexidade de atribuição.

67. Auditoria

Eventos sugeridos:

lead.created
lead.updated
lead.assigned
lead.status_changed
lead.converted
lead.lost
68. Notificações

Futuramente:

novo lead atribuído
follow-up vencendo
visita próxima
lead sem retorno
69. Push

Pode ser usado no PWA quando houver contexto.

70. WhatsApp e auditoria

Abrir WhatsApp não precisa ser tratado inicialmente como prova de que houve contato.

Se quisermos histórico confiável:

usuário registra atividade

ou integração futura confirma evento.

71. Não presumir envio

Clicar:

Abrir WhatsApp

não significa:

mensagem enviada
72. Notion

A integração com Notion não fará parte do fluxo principal.

73. Motivo

O fluxo externo cria atrito para o cliente e duplica organização que deve pertencer ao OrganizeG3.

74. Integração futura opcional

Se uma empresa quiser:

exportar/sincronizar dados

poderá existir integração futura.

Não deve influenciar o modelo principal.

75. Formulário público

Pode existir futuramente como canal opcional.

Não será requisito para entrada de lead.

76. QR Code

Futuramente poderá haver QR Code que abre WhatsApp da empresa.

Isso independe da lógica de lead.

77. Link direto

A empresa poderá divulgar link:

Fale conosco pelo WhatsApp
78. Conversão manual

Na primeira implementação:

Cadastrar Lead

será manual.

Isso é suficiente.

79. Automação futura de captura

Somente com integração oficial:

mensagem recebida
↓
sugestão de novo lead
80. Não criar lead para toda mensagem

Mesmo com integração futura, não criar automaticamente registros para:

spam;
fornecedores;
funcionários;
mensagens internas.

Pode existir fila de triagem.

81. Central comercial

Futuramente:

Novos
Aguardando retorno
Visitas
Orçamentos
Aguardando aprovação
Perdidos
82. Dashboard comercial

Indicadores possíveis:

novos leads
leads sem retorno
visitas próximas
orçamentos enviados
taxa de conversão
motivos de perda
83. Métricas

Futuramente:

lead → visita
visita → orçamento
orçamento → aprovação
tempo médio por etapa
84. Não gamificar prematuramente

Métricas devem apoiar decisão, não gerar pressão artificial sobre equipe.

85. Campos técnicos iniciais

Modelo futuro pode possuir:

id
tenant_id
name
phone
email
interest
notes
source
source_detail
responsible_user_id
status
lost_reason
lost_reason_notes
converted_customer_id
next_follow_up_at
created_at
updated_at
is_active

A modelagem definitiva será feita quando o domínio Comercial for implementado.

86. Multitenancy

Todo lead pertence a um tenant.

Nunca compartilhar lead entre empresas.

87. Filial

Lead poderá possuir filial opcional.

Útil para empresas com:

regiões;
lojas;
unidades.
88. Branch assignment

Pode ser feito:

manualmente;
pelo responsável;
por regra futura.
89. API futura

Operações mínimas:

list
get
create
update
assign
change_status
convert
close
reactivate quando aplicável
90. Busca

Buscar por:

nome
telefone
interesse
91. Filtros

Filtros futuros:

status
responsavel
origem
periodo
filial
follow_up
92. Ordenação

Prioridades úteis:

mais recentes
follow-up mais próximo
mais antigos sem contato
93. Lead perdido não é apagado

Preservar histórico.

94. Reativação

Um lead perdido pode voltar a demonstrar interesse.

Opções futuras:

reativar lead

ou:

criar nova oportunidade

A regra será definida no CRM.

95. Dados vindos do legado

Leads antigos, se existirem, poderão ser migrados.

Notion IDs antigos:

ignorar ou preservar apenas como metadado legado

não devem ser requisito funcional novo.

96. Migração

O migrador deverá mapear:

lead antigo
→
lead novo

quando existir dado suficientemente confiável.

97. Primeiro escopo futuro

Quando o módulo Comercial for implementado:

1. criar lead
2. listar
3. editar
4. buscar
5. status
6. responsável
7. abrir WhatsApp
8. converter para cliente
9. registrar motivo de perda
98. Segunda evolução
atividades
follow-up
agenda
pendências
templates de mensagem
indicadores
99. Terceira evolução
WhatsApp Business
captura assistida
automação de mensagens
integrações externas
100. Regra final

A experiência comercial deve ser simples para o cliente e organizada para a empresa.

Princípio:

cliente conversa onde já está acostumado
↓
empresa registra o necessário
↓
OrganizeG3 organiza o processo

O OrganizeG3 não deve transformar o primeiro contato em burocracia.