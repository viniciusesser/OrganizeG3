# Domain Model Specification
## 004 - Value Objects

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define o padrão oficial para implementação dos Value Objects do OrganizeG3.

Todo Value Object deverá seguir exatamente estas regras.

Os Value Objects representam conceitos do domínio que não possuem identidade própria.

Eles são utilizados para aumentar a expressividade do código, eliminar duplicação de regras e tornar o domínio mais seguro.

---

# O que é um Value Object?

Um Value Object representa um valor.

Ele não possui identidade.

Ele é definido exclusivamente pelos seus atributos.

Exemplo

```text
Money

Address

Email

Phone

CPF

CNPJ

Dimensions

Weight

Percentage

Coordinates
```

Dois Value Objects com os mesmos valores representam exatamente o mesmo objeto.

---

# Características

Todo Value Object deverá ser:

```text
Imutável

Comparável por valor

Sem identidade

Autossuficiente

Validado na criação

Livre de infraestrutura
```

---

# Identidade

Value Objects nunca possuem:

```text
Id

UUID

Código

Número sequencial
```

Caso exista identidade, provavelmente trata-se de uma Entity.

---

# Imutabilidade

Após criado, um Value Object nunca poderá ser alterado.

Errado

```python
money.value = Decimal("200")
```

Correto

```python
money = money.add(Decimal("50"))
```

O método retorna uma nova instância.

---

# Igualdade

Value Objects são comparados pelos seus valores.

Exemplo

```text
Money(100.00, BRL)

==

Money(100.00, BRL)
```

Resultado

```text
True
```

Mesmo que sejam objetos diferentes em memória.

---

# Responsabilidades

Um Value Object deve:

- validar seus próprios dados;
- garantir consistência;
- encapsular lógica relacionada ao valor;
- impedir estados inválidos.

---

# Não Responsabilidades

Um Value Object nunca deverá:

- acessar banco de dados;
- consultar APIs;
- enviar emails;
- acessar arquivos;
- utilizar SQL;
- conhecer o Tenant.

---

# Criação

Todo Value Object deverá validar seus dados no construtor.

Exemplo

```text
Email

↓

Formato válido
```

Caso contrário

```text
DomainException
```

---

# Exemplos

## Email

Responsável por

- validar formato;
- normalizar;
- comparar.

---

## Phone

Responsável por

- remover caracteres;
- validar DDD;
- validar comprimento;
- formatar exibição.

---

## CPF

Responsável por

- validar dígitos;
- remover máscara;
- normalizar.

---

## CNPJ

Responsável por

- validar;
- normalizar;
- formatar.

---

## Money

Responsável por

- moeda;
- precisão;
- operações matemáticas;
- comparação.

Operações

```text
Add

Subtract

Multiply

Divide

Compare
```

Nunca utilizar:

```text
float
```

Utilizar sempre:

```text
Decimal
```

---

## Percentage

Representa porcentagens.

Exemplo

```text
15%

2.5%

100%
```

Operações

```text
Apply()

Increase()

Decrease()
```

---

## Quantity

Representa quantidade.

Exemplos

```text
10 unidades

15 kg

3 caixas

5 metros
```

Nunca permitir:

```text
Quantidade negativa
```

Quando não fizer sentido.

---

## Weight

Representa peso.

Unidades

```text
g

kg

ton
```

---

## Dimensions

Representa dimensões físicas.

Campos

```text
Length

Width

Height
```

Operações

```text
Volume()

Area()
```

---

## Address

Campos

```text
Street

Number

District

City

State

Country

ZipCode
```

Métodos

```text
Formatted()

Short()

Complete()
```

---

## Coordinates

Campos

```text
Latitude

Longitude
```

Operações

```text
Distance()

IsValid()
```

---

## DateRange

Representa intervalo.

Campos

```text
Start

End
```

Métodos

```text
Contains()

Overlap()

Duration()
```

---

## TimeRange

Campos

```text
Start

End
```

Métodos

```text
Contains()

Intersect()
```

---

## RGBColor

Representa uma cor.

Campos

```text
R

G

B
```

Métodos

```text
Hex()

Lighten()

Darken()
```

---

## ThemeColor

Representa um Token do Theme Design.

Nunca armazenará hexadecimal diretamente.

Exemplo

```text
primary

secondary

surface

background

danger

success
```

---

# Composição

Value Objects podem conter outros Value Objects.

Exemplo

```text
Address

↓

ZipCode

City

State
```

---

# Reutilização

Um Value Object deverá ser reutilizado em todo o sistema.

Exemplo

```text
Email
```

Será utilizado em:

```text
Customer

Supplier

Employee

User

Contact
```

Nunca criar múltiplas implementações.

---

# Serialização

Todo Value Object deverá suportar:

```text
JSON

DTO

Banco

Eventos
```

Sem perda de informação.

---

# Persistência

A Infrastructure será responsável por persistir o Value Object.

O Value Object desconhece completamente como isso ocorrerá.

---

# Eventos

Value Objects nunca publicam eventos.

Quem publica eventos é o Aggregate Root.

---

# Herança

Evitar herança.

Preferir:

```text
Composição
```

---

# Testabilidade

Todo Value Object deverá possuir testes unitários.

Casos mínimos

- criação válida;
- criação inválida;
- igualdade;
- operações;
- serialização.

---

# Lista inicial de Value Objects

```text
Money

Currency

Percentage

Quantity

Weight

Volume

Dimensions

Address

ZipCode

City

State

Country

Email

Phone

CPF

CNPJ

RG

InscricaoEstadual

InscricaoMunicipal

PixKey

BankAccount

Barcode

QRCode

SKU

NCM

CFOP

CST

Coordinates

DateRange

TimeRange

BusinessHours

RGBColor

ThemeColor

PasswordHash

FileHash

MimeType

Url

Version

DocumentNumber
```

---

# Checklist

Antes de implementar verificar:

- possui identidade?
- é imutável?
- valida seus próprios dados?
- representa apenas um conceito?
- não depende da infraestrutura?
- pode ser reutilizado?
- possui testes?

Caso alguma resposta seja "não", provavelmente não é um Value Object.

---

# Convenções

Todo Value Object deverá:

- ser imutável;
- possuir igualdade por valor;
- validar seus próprios dados;
- ser pequeno;
- representar um único conceito;
- ser reutilizável;
- ser independente da infraestrutura.

---

# Próximo Documento

```text
005-domain-events.md
```