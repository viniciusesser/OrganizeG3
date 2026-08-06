# Application Architecture Specification
## 019 - Mappers

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial dos Mappers do OrganizeG3.

Os Mappers são responsáveis por converter objetos entre diferentes camadas da aplicação.

Eles eliminam o acoplamento entre:

- Presentation
- Application
- Domain
- Infrastructure

Nenhuma dessas camadas deverá conhecer diretamente a estrutura interna da outra.

---

# O que é um Mapper?

Um Mapper é um componente responsável por transformar um objeto em outro.

Exemplos

```text
DTO

↓

Aggregate
```

```text
Aggregate

↓

DTO
```

```text
Read Model

↓

Response DTO
```

---

# Objetivos

Os Mappers existem para:

- desacoplar camadas;
- evitar duplicação;
- centralizar conversões;
- facilitar manutenção;
- permitir evolução independente das camadas.

---

# Responsabilidades

Um Mapper poderá:

- converter DTO em Aggregate;
- converter Aggregate em DTO;
- converter Entity em DTO;
- converter Read Model em DTO;
- converter DTO em Value Objects;
- converter DTOs entre versões.

Nunca deverá:

- executar regras de negócio;
- validar domínio;
- persistir dados;
- executar SQL;
- acessar APIs.

---

# Fluxo

```text
Presentation

↓

DTO

↓

Mapper

↓

Domain

↓

Mapper

↓

DTO

↓

Presentation
```

---

# Tipos de Conversão

## Request DTO

↓

Aggregate

---

## Aggregate

↓

Response DTO

---

## Aggregate

↓

Summary DTO

---

## Aggregate

↓

Detail DTO

---

## Read Model

↓

Response DTO

---

## Domain Event

↓

Event DTO

---

## Infrastructure Model

↓

Aggregate

---

# Regras

Toda conversão deverá ser:

```text
Determinística

Reversível quando possível

Sem efeitos colaterais

Sem acesso externo
```

---

# Domain → DTO

Responsabilidade

```text
Aggregate

↓

DTO
```

Nunca retornar o Aggregate diretamente para a interface.

---

# DTO → Domain

Responsabilidade

```text
DTO

↓

Factory

↓

Aggregate
```

O Mapper nunca cria Aggregates diretamente quando houver lógica de construção.

Nesse caso utilizar:

```text
Factory
```

---

# Entity → DTO

Entities poderão ser convertidas.

Exemplo

```text
Customer

↓

CustomerResponse
```

---

# Read Model → DTO

Consultas utilizarão:

```text
Read Model

↓

Mapper

↓

DTO
```

---

# Value Objects

O Mapper poderá construir Value Objects.

Exemplo

```text
CustomerRequest

↓

Email

↓

Phone

↓

Address
```

---

# Collections

Coleções deverão ser convertidas elemento por elemento.

Exemplo

```text
List<Product>

↓

List<ProductSummary>
```

Nunca retornar coleções do domínio diretamente.

---

# Null Safety

Todo Mapper deverá tratar:

```text
Null

Coleções vazias

Campos opcionais
```

Sem lançar exceções inesperadas.

---

# Localização

Datas, moedas e formatos deverão permanecer neutros.

Exemplo

```text
UTC

↓

DTO

↓

Presentation

↓

Formato Local
```

Nunca formatar datas dentro do Mapper.

---

# Conversões Permitidas

```text
DTO → Domain

Domain → DTO

ReadModel → DTO

Infrastructure → Domain

DTO V1 → DTO V2

DTO V2 → DTO V1
```

---

# Conversões Proibidas

Nunca converter:

```text
Repository

↓

DTO
```

```text
HTTP Response

↓

Aggregate
```

```text
Database Connection

↓

Entity
```

---

# Organização

Estrutura

```text
mappers/

    customer/

    supplier/

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

# Shared Mappers

Exemplos

```text
MoneyMapper

AddressMapper

PhoneMapper

EmailMapper

DateMapper

PaginationMapper

EnumMapper
```

---

# Convenções

Nome

```text
<Entity>Mapper
```

Exemplos

```text
CustomerMapper

ProductMapper

InvoiceMapper

SalesOrderMapper

ProjectMapper
```

---

# Performance

Mappers deverão ser extremamente leves.

Nunca:

```text
Consultar banco

Executar SQL

Executar HTTP

Executar IA

Ler Arquivos
```

---

# Testabilidade

Todo Mapper deverá possuir testes.

Casos mínimos

```text
Conversão válida

Campos nulos

Coleções

Enums

Value Objects

Conversão reversa
```

---

# Anti-Patterns

Nunca fazer

```text
Salvar banco

Executar regra

Publicar evento

Consultar Repository

Executar Command

Executar Query
```

---

# Checklist

Antes de implementar verificar:

- apenas converte objetos?
- não possui regra de negócio?
- não depende da infraestrutura?
- trata nulos?
- trata coleções?
- possui testes?

---

# Regras Gerais

Todo Mapper deverá:

- possuir responsabilidade única;
- ser determinístico;
- ser altamente reutilizável;
- não depender da infraestrutura;
- não executar regras de domínio;
- não alterar estado do sistema.

---

# Fluxo Completo

```text
Request DTO

↓

Mapper

↓

Domain

↓

Mapper

↓

Response DTO

↓

Presentation
```

---

# Próximo Documento

```text
020-application-services.md
```