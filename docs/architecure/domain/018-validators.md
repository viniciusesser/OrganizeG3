# Application Architecture Specification
## 018 - Validators

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos Validators do OrganizeG3.

Validators são responsáveis por validar dados de entrada antes da execução dos Casos de Uso.

Eles pertencem exclusivamente à camada Application.

Seu objetivo é impedir que dados inválidos cheguem ao Domínio.

---

# O que é um Validator?

Um Validator é um componente responsável por validar um Command ou uma Query.

Ele garante que a estrutura dos dados esteja correta.

Exemplo

```text
CreateCustomerCommand

↓

CreateCustomerValidator

↓

Command Handler
```

---

# Responsabilidades

Um Validator deverá apenas:

- validar obrigatoriedade;
- validar tipos;
- validar formatos;
- validar tamanho;
- validar valores mínimos;
- validar valores máximos;
- validar listas;
- validar enumerações.

Nunca deverá:

- executar regras de negócio;
- acessar banco de dados;
- executar SQL;
- consultar APIs;
- alterar entidades;
- publicar eventos.

---

# Fluxo

```text
Presentation

↓

Command

↓

Validator

↓

Handler

↓

Domain
```

---

# Validação x Domínio

## Validator

Responsável por

```text
Campo obrigatório

Formato

Tipo

Comprimento

Regex

Intervalo

Conversão
```

---

## Domínio

Responsável por

```text
Limite de crédito

Pedido pode ser aprovado?

Estoque suficiente?

Cliente ativo?

Produção pode iniciar?
```

Nunca duplicar regras de domínio dentro do Validator.

---

# Estrutura

Todo Validator deverá possuir:

```text
Objeto

↓

Regras

↓

Mensagens

↓

Resultado
```

---

# Resultado

O Validator deverá retornar:

```text
Success

↓

ou

Validation Errors
```

Cada erro deverá possuir:

```text
Campo

Código

Mensagem

Valor Informado
```

---

# Mensagens

As mensagens deverão utilizar Localization.

Nunca:

```text
"Nome obrigatório"
```

Diretamente.

Sempre:

```text
validation.customer.name.required
```

---

# Validações Básicas

Exemplos

```text
Required

Not Empty

Max Length

Min Length

Regex

Email

Telefone

CPF

CNPJ

UUID

Decimal

Inteiro

Boolean
```

---

# Validação de Datas

Exemplos

```text
Data Inicial

↓

Obrigatória

↓

Data Final

↓

Maior que Inicial
```

Validações simples permanecem no Validator.

Regras complexas pertencem ao Domínio.

---

# Validação de Arquivos

Verificar

```text
Extensão

Mime Type

Tamanho

Quantidade

Nome
```

Nunca verificar regras de negócio.

---

# Validação de Enum

Exemplo

```text
Status

↓

Valor permitido?
```

---

# Validação de Coleções

Exemplo

```text
Itens

↓

Obrigatório

↓

Quantidade mínima

↓

Quantidade máxima
```

---

# Validação de IDs

Todo UUID deverá ser validado.

Nunca aceitar:

```text
UUID vazio

Formato inválido
```

---

# Validação de Valores

Exemplo

```text
Quantidade

↓

Maior que zero
```

```text
Preço

↓

Maior ou igual a zero
```

---

# Validação Condicional

Exemplo

```text
Pagamento Parcelado

↓

Número de Parcelas obrigatório
```

---

# Composição

Validators poderão reutilizar outros Validators.

Exemplo

```text
CreateCustomerValidator

↓

AddressValidator

↓

PhoneValidator

↓

EmailValidator
```

---

# Organização

Estrutura

```text
validators/

    customer/

    product/

    inventory/

    sales/

    purchasing/

    production/

    financial/

    workflow/

    shared/
```

---

# Shared Validators

Validações reutilizáveis

```text
EmailValidator

PhoneValidator

CPFValidator

CNPJValidator

UUIDValidator

MoneyValidator

AddressValidator

PasswordValidator

PaginationValidator

DateRangeValidator
```

---

# Convenções

Nome

```text
<Command>Validator
```

Exemplos

```text
CreateCustomerValidator

ApproveSalesOrderValidator

ReceivePaymentValidator

IssueInvoiceValidator
```

Queries

```text
SearchCustomersValidator

InventoryBalanceValidator

DashboardValidator
```

---

# Performance

Validators deverão ser extremamente rápidos.

Nunca executar:

```text
SQL

HTTP

Redis

Filesystem

Email
```

---

# Segurança

Validators deverão impedir:

```text
Campos inesperados

Tipos inválidos

Objetos nulos

Valores fora do intervalo

Enum inválido
```

Antes da execução.

---

# Auditoria

Erros poderão registrar:

```text
CorrelationId

Campo

Código

Usuário

Tenant

Timestamp
```

Sem armazenar dados sensíveis.

---

# Integração com Pipelines

Fluxo

```text
Pipeline

↓

Validator

↓

Handler
```

Caso existam erros:

```text
↓

Resposta

↓

Fim
```

O Handler nunca será executado.

---

# Testabilidade

Todo Validator deverá possuir testes.

Casos mínimos

```text
Dados válidos

Campo obrigatório

Campo vazio

Valor inválido

Formato inválido

Limites

Coleções

Enums
```

---

# Anti-Patterns

Nunca fazer

```text
Consultar banco

Executar regras de domínio

Executar Commands

Executar Queries

Persistir dados

Enviar Emails
```

---

# Checklist

Antes de criar um Validator verificar:

- valida apenas estrutura?
- não possui regra de negócio?
- não depende da infraestrutura?
- reutiliza Shared Validators?
- possui testes?
- utiliza mensagens localizáveis?

---

# Regras Gerais

Todo Validator deverá:

- validar somente entrada;
- ser independente do domínio;
- ser altamente reutilizável;
- ser determinístico;
- possuir mensagens padronizadas;
- nunca alterar estado;
- nunca acessar infraestrutura.

---

# Fluxo Completo

```text
Request

↓

Command / Query

↓

Validator

↓

Sucesso?

↓

Sim

↓

Handler

↓

Domínio

↓

Resposta

ou

↓

Falha

↓

Validation Result

↓

Response
```

---

# Próximo Documento

```text
019-mappers.md
```