# Infrastructure Architecture Specification
## 031 - Storage Architecture

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial do sistema de armazenamento de arquivos do OrganizeG3.

Toda manipulação de arquivos deverá ocorrer através da camada Storage.

Nenhum módulo da aplicação poderá acessar diretamente:

- disco;
- diretórios;
- S3;
- Supabase Storage;
- Azure Blob;
- Google Cloud Storage.

Toda operação deverá passar pelas interfaces de Storage.

---

# Objetivos

A arquitetura deverá garantir:

- abstração;
- segurança;
- escalabilidade;
- versionamento;
- auditoria;
- portabilidade.

---

# Arquitetura

```text
Application

↓

Storage Interface

↓

Storage Provider

↓

Filesystem

S3

Supabase

Azure

Google Cloud
```

---

# Responsabilidades

O Storage será responsável por:

- upload;
- download;
- exclusão;
- versionamento;
- geração de URLs;
- organização dos arquivos;
- validação técnica;
- auditoria.

Nunca conter regras de negócio.

---

# Interfaces

Toda implementação deverá implementar:

```text
IStorageProvider
```

Operações mínimas

```text
Upload

Download

Delete

Exists

Copy

Move

GenerateUrl

GenerateTemporaryUrl

ListFiles

GetMetadata
```

---

# Providers previstos

O OrganizeG3 deverá suportar:

```text
Local Storage

Supabase Storage

Amazon S3

Azure Blob

Google Cloud Storage

MinIO
```

A troca do Provider não deverá impactar a Application.

---

# Tipos de Arquivos

O sistema deverá suportar:

```text
Imagens

PDF

DWG

DXF

SKP

Excel

Word

Backup

JSON

CSV

XML

ZIP

Logs

Áudios

Vídeos
```

---

# Organização Física

Estrutura lógica

```text
tenant/

    documents/

    projects/

    customers/

    products/

    backups/

    reports/

    images/

    ai/

    temp/
```

---

# Organização por Tenant

Todo arquivo deverá pertencer a um Tenant.

Exemplo

```text
tenant_id/

↓

categoria/

↓

arquivo
```

Nunca misturar arquivos entre empresas.

---

# Nome dos Arquivos

Nunca utilizar o nome enviado pelo usuário como identificador físico.

Sempre gerar:

```text
UUID
```

Exemplo

```text
4a8fd45f...

.pdf
```

O nome original ficará armazenado nos metadados.

---

# Metadados

Todo arquivo possuirá:

```text
FileId

TenantId

OriginalName

StoredName

MimeType

Extension

Size

Hash

CreatedAt

CreatedBy

Version
```

---

# Hash

Todo arquivo deverá possuir hash.

Algoritmo padrão

```text
SHA-256
```

Objetivos

```text
Integridade

Duplicidade

Validação
```

---

# Versionamento

Arquivos poderão possuir versões.

Exemplo

```text
Projeto.pdf

↓

v1

↓

v2

↓

v3
```

Sem sobrescrever permanentemente versões anteriores.

---

# Upload

Fluxo

```text
Receber Arquivo

↓

Validar

↓

Calcular Hash

↓

Persistir

↓

Registrar Metadados

↓

Retornar FileId
```

---

# Download

Fluxo

```text
Solicitação

↓

Permissão

↓

Storage

↓

Stream

↓

Cliente
```

Nunca carregar arquivos grandes completamente na memória.

---

# Streaming

Arquivos grandes deverão utilizar:

```text
Streaming
```

Exemplos

```text
Backup

Vídeos

ZIP

PDF Grandes
```

---

# URLs Temporárias

Para Providers compatíveis utilizar:

```text
Signed URL

Temporary URL
```

Configuráveis.

---

# Exclusão

Excluir logicamente quando necessário.

Fluxo

```text
Delete Request

↓

Auditoria

↓

Storage

↓

Soft Delete Metadata
```

---

# Backup

Arquivos deverão ser incluídos nas rotinas de backup.

Categorias

```text
Projetos

Documentos

Relatórios

Configurações

Imagens
```

---

# Compressão

Arquivos poderão ser compactados.

Exemplos

```text
ZIP

GZIP

7Z
```

Quando apropriado.

---

# Criptografia

Arquivos sensíveis poderão utilizar:

```text
AES-256
```

Em repouso.

Durante transmissão utilizar:

```text
HTTPS/TLS
```

---

# Segurança

Validar:

```text
Permissões

Tenant

Mime Type

Tamanho

Extensão

Antivírus (futuro)
```

Nunca confiar apenas na extensão.

---

# Limites

Cada categoria poderá possuir limites.

Exemplo

```text
Imagem

20 MB

↓

Backup

20 GB

↓

Documento

100 MB
```

Configurável.

---

# Tipos Permitidos

Lista branca.

Exemplo

```text
PDF

PNG

JPEG

DOCX

XLSX

DWG

DXF

SKP

ZIP
```

Arquivos desconhecidos poderão ser bloqueados.

---

# Miniaturas

Imagens poderão gerar:

```text
Thumbnail

Preview

Medium

Original
```

Automaticamente.

---

# OCR

Documentos poderão iniciar:

```text
Upload

↓

Worker

↓

OCR

↓

Indexação
```

---

# IA

Arquivos poderão iniciar:

```text
Upload

↓

Embeddings

↓

Vetorização

↓

RAG
```

---

# Auditoria

Registrar

```text
Upload

Download

Delete

Rename

Move

Version

User

Timestamp

CorrelationId
```

---

# Logging

Campos mínimos

```text
Storage

Operation

Duration

Size

Provider

Tenant

FileId
```

---

# Monitoramento

Métricas

```text
Uploads

Downloads

Storage Used

Errors

Latency

Bandwidth
```

---

# Health Check

Cada Provider deverá informar:

```text
Disponibilidade

Latência

Espaço

Autenticação

Status
```

---

# Organização

```text
storage/

    providers/

        local.py

        s3.py

        supabase.py

        azure.py

        gcs.py

    services/

    models/

    metadata/

    validators/

    thumbnails/

    encryption/
```

---

# Testabilidade

Todo Provider deverá possuir:

```text
Upload Tests

Download Tests

Delete Tests

Streaming Tests

Performance Tests

Permission Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Salvar arquivos diretamente

Utilizar caminhos absolutos

Misturar arquivos de Tenants

Expor caminhos internos

Ignorar Hash

Ignorar Auditoria
```

---

# Checklist

Antes de implementar verificar:

- utiliza Interface?
- suporta Streaming?
- gera Hash?
- registra Metadados?
- respeita Tenant?
- suporta Versionamento?
- possui Auditoria?
- possui Testes?

---

# Regras Gerais

Todo Storage Provider deverá:

- implementar IStorageProvider;
- ser desacoplado;
- suportar múltiplos backends;
- utilizar Streaming;
- respeitar Multi-Tenant;
- registrar Auditoria;
- ser altamente escalável.

---

# Fluxo Completo

```text
Upload

↓

Storage Interface

↓

Provider

↓

Storage

↓

Metadata

↓

Response
```

---

# Próximo Documento

```text
032-cache-architecture.md
```