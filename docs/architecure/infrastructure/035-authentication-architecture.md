# Infrastructure Architecture Specification
## 035 - Authentication Architecture

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do sistema de Autenticação do OrganizeG3.

A autenticação é responsável por identificar usuários, dispositivos e aplicações antes que qualquer operação protegida seja executada.

Seu objetivo é responder uma única pergunta:

```text
Quem está realizando esta operação?
```

A autorização será tratada em documento próprio.

---

# Objetivos

O sistema de autenticação deverá garantir:

- identificação segura;
- autenticação moderna;
- suporte multi-dispositivo;
- escalabilidade;
- auditoria;
- integração com provedores externos.

---

# Arquitetura

```text
Cliente

↓

Authentication Provider

↓

Identity Service

↓

Token Service

↓

Application
```

---

# Responsabilidades

A autenticação deverá:

- validar credenciais;
- emitir Tokens;
- renovar sessões;
- invalidar sessões;
- registrar dispositivos;
- registrar auditoria.

Nunca deverá executar regras de negócio.

---

# Componentes

O sistema será composto por:

```text
Authentication Service

Identity Provider

Token Provider

Password Hasher

Refresh Token Store

Session Manager

Device Manager
```

---

# Fluxo

```text
Login

↓

Validação

↓

Usuário

↓

Senha

↓

Token

↓

Refresh Token

↓

Sessão
```

---

# Métodos Suportados

O OrganizeG3 deverá suportar:

```text
Usuário e Senha

JWT

Refresh Token

API Key

OAuth2

OpenID Connect
```

Futuramente:

```text
Google

Microsoft

GitHub
```

---

# Login Tradicional

Fluxo

```text
Email

↓

Senha

↓

Validação

↓

JWT

↓

Refresh Token
```

---

# Password Hash

Nunca armazenar senha em texto.

Algoritmo oficial

```text
Argon2id
```

Alternativa compatível

```text
bcrypt
```

Nunca utilizar:

```text
MD5

SHA1

SHA256
```

Como algoritmo de senha.

---

# Password Policy

Configuração padrão

```text
Mínimo

12 caracteres
```

Obrigatório conter

```text
Maiúscula

Minúscula

Número

Símbolo
```

Configurável por Tenant.

---

# JWT

O Access Token conterá:

```text
UserId

TenantId

BranchId

Roles

Permissions

SessionId

IssuedAt

ExpiresAt
```

Nunca armazenar informações sensíveis.

---

# Tempo de Vida

Access Token

```text
15 minutos
```

Refresh Token

```text
30 dias
```

Configurável.

---

# Refresh Token

Todo Refresh Token possuirá:

```text
UUID

Hash

Expiração

Dispositivo

Usuário
```

Nunca armazenar Refresh Token em texto puro.

---

# Sessões

Toda autenticação criará uma sessão.

Campos

```text
SessionId

UserId

TenantId

DeviceId

IPAddress

UserAgent

CreatedAt

LastAccess

ExpiresAt
```

---

# Device Manager

Cada dispositivo receberá:

```text
DeviceId
```

Campos

```text
Sistema Operacional

Hostname

Versão

Fingerprint

Último Acesso
```

---

# Multi-Device

O mesmo usuário poderá possuir:

```text
Notebook

Desktop

Celular

Tablet
```

Cada sessão será independente.

---

# Logout

Fluxo

```text
Logout

↓

Invalidar Refresh Token

↓

Encerrar Sessão

↓

Registrar Auditoria
```

---

# Logout Global

Permitirá:

```text
Encerrar todas as sessões
```

Do usuário.

---

# Revogação

O sistema deverá suportar:

```text
Revogar

↓

Refresh Token

↓

Sessão

↓

Dispositivo
```

Independentemente.

---

# API Keys

O sistema suportará autenticação por API Keys.

Campos

```text
KeyId

Hash

TenantId

Permissions

Expiration
```

Nunca armazenar a chave em texto puro.

---

# OAuth

Provedores previstos

```text
Google

Microsoft

GitHub

Apple
```

Implementados através de Interfaces.

---

# MFA

Arquitetura preparada para:

```text
TOTP

Authenticator

Email

SMS

Push
```

---

# Recuperação de Senha

Fluxo

```text
Solicitação

↓

Token Temporário

↓

Validação

↓

Nova Senha
```

O token deverá expirar.

---

# Segurança

Proteções obrigatórias

```text
Rate Limit

Tentativas

Bloqueio Temporário

Detecção de Ataques

IP Suspeito
```

---

# Tentativas

Após

```text
5 tentativas
```

Bloquear temporariamente.

Tempo padrão

```text
15 minutos
```

---

# Auditoria

Registrar

```text
Login

Logout

Falha

Troca de Senha

Reset

Novo Dispositivo

Revogação

Refresh
```

---

# Logging

Campos

```text
UserId

TenantId

DeviceId

IP

UserAgent

CorrelationId

Resultado
```

Nunca registrar senhas.

---

# Health Check

Validar

```text
Token Service

Identity Provider

Refresh Store

Session Store
```

---

# Multi-Tenant

Toda autenticação deverá identificar:

```text
Tenant

↓

Usuário

↓

Permissões
```

Nunca permitir login cruzado entre empresas.

---

# Organização

```text
authentication/

    providers/

    jwt/

    refresh/

    sessions/

    password/

    oauth/

    api_keys/

    devices/

    mfa/
```

---

# Testabilidade

Todo módulo deverá possuir:

```text
Login Tests

Logout Tests

Refresh Tests

Password Tests

JWT Tests

Session Tests

Security Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Senha em texto

JWT sem expiração

Refresh Token reutilizável

Hash fraco

Sessão Global

Credenciais hardcoded
```

---

# Checklist

Antes de implementar verificar:

- utiliza Argon2id?
- JWT possui expiração?
- Refresh Token possui hash?
- registra auditoria?
- suporta múltiplos dispositivos?
- suporta revogação?
- possui testes?

---

# Regras Gerais

Todo sistema de autenticação deverá:

- utilizar Argon2id;
- emitir JWT;
- utilizar Refresh Tokens;
- registrar Sessões;
- registrar Auditoria;
- suportar múltiplos dispositivos;
- ser totalmente desacoplado da Application.

---

# Fluxo Completo

```text
Login

↓

Identity Provider

↓

Password Verification

↓

JWT

↓

Refresh Token

↓

Session

↓

Application
```

---

# Próximo Documento

```text
036-authorization-architecture.md
```