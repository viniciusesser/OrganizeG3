# Infrastructure Architecture Specification
## 041 - Snapshot Architecture

Versão: 1.0

Status: Em desenvolvimento

---

# Objetivo

Este documento define a arquitetura oficial de Snapshots do OrganizeG3.

Snapshots representam uma fotografia consistente do estado dos dados em um determinado instante.

Seu principal objetivo é permitir:

- inicialização de novos dispositivos;
- recuperação após falhas;
- reconstrução completa do banco local;
- sincronizações de grande volume;
- recuperação de inconsistências.

O Snapshot nunca substitui a Sincronização Delta.

Os dois mecanismos trabalham em conjunto.

---

# Objetivos

O sistema de Snapshots deverá garantir:

- consistência;
- integridade;
- alta velocidade;
- compressão;
- criptografia;
- versionamento;
- recuperação determinística.

---

# Arquitetura

```text
PostgreSQL

↓

Snapshot Generator

↓

Snapshot Package

↓

Storage

↓

Desktop

↓

SQLite
```

---

# Filosofia

O Snapshot representa:

```text
Estado Completo

↓

Em determinado instante
```

Após restaurado:

```text
Snapshot

+

Delta

=

Base Atualizada
```

---

# Quando Utilizar

Snapshots serão utilizados para:

```text
Primeira sincronização

Novo computador

Recuperação

Corrupção do banco local

Grande volume de alterações

Migração de versão
```

---

# Quando NÃO Utilizar

Não utilizar Snapshot para:

```text
Sincronizações rotineiras

Atualizações pequenas

Operações individuais
```

Nestes casos utilizar:

```text
Delta Synchronization
```

---

# Componentes

O sistema será composto por:

```text
Snapshot Generator

Snapshot Storage

Snapshot Validator

Snapshot Downloader

Snapshot Importer

Snapshot Cleaner
```

---

# Snapshot Generator

Responsável por:

```text
Selecionar dados

↓

Gerar Snapshot

↓

Comprimir

↓

Calcular Hash

↓

Persistir
```

---

# Estrutura

Todo Snapshot possuirá:

```text
SnapshotId

TenantId

GeneratedAt

GeneratedBy

DatabaseVersion

SchemaVersion

Checksum

Compression

Encryption

Size

RecordCount
```

---

# Conteúdo

O Snapshot poderá conter:

```text
Cadastros

Produtos

Clientes

Pedidos

Financeiro

Estoque

Produção

Configurações
```

---

# Exclusões

O Snapshot nunca conterá:

```text
Cache

Logs

Sessões

Filas

Arquivos Temporários

Workers
```

---

# Organização

Estrutura lógica

```text
Snapshot

↓

Módulos

↓

Tabelas

↓

Registros
```

---

# Geração

Fluxo

```text
Selecionar Tenant

↓

Congelar Estado

↓

Exportar Dados

↓

Comprimir

↓

Calcular Hash

↓

Salvar
```

---

# Consistência

Todo Snapshot deverá ser gerado dentro de uma transação consistente.

Objetivo

```text
Nenhum registro parcialmente exportado.
```

---

# Compressão

Formatos suportados

```text
GZIP

Zstandard
```

Padrão

```text
Zstandard
```

---

# Criptografia

Snapshots poderão utilizar

```text
AES-256
```

Quando armazenados externamente.

Durante transmissão utilizar

```text
TLS
```

---

# Checksum

Todo Snapshot possuirá

```text
SHA-256
```

Antes da importação deverá ocorrer validação completa.

---

# Versionamento

Todo Snapshot possuirá:

```text
SchemaVersion

ApplicationVersion

SnapshotVersion
```

Permitindo compatibilidade.

---

# Importação

Fluxo

```text
Download

↓

Validação

↓

Checksum

↓

Descompressão

↓

Importação

↓

SQLite

↓

Confirmação
```

---

# Atualização

Após restaurar:

```text
Snapshot

↓

Delta Synchronization

↓

Banco Atualizado
```

---

# Recuperação

Caso ocorra falha:

```text
Abortar

↓

Rollback

↓

Banco anterior permanece íntegro
```

---

# Incremental

Arquitetura preparada para:

```text
Incremental Snapshot
```

No futuro.

Inicialmente:

```text
Snapshot Completo
```

---

# Armazenamento

Providers suportados

```text
Filesystem

Supabase Storage

Amazon S3

Azure Blob

Google Cloud Storage
```

---

# Multi-Tenant

Cada Snapshot pertence a apenas:

```text
Um Tenant
```

Nunca compartilhar dados entre empresas.

---

# Auditoria

Registrar

```text
SnapshotId

TenantId

DeviceId

GeneratedAt

ImportedAt

Duration

Checksum

User

CorrelationId
```

---

# Logging

Campos

```text
Snapshot

Size

Duration

Compression

Records

Provider
```

---

# Monitoramento

Registrar

```text
Snapshots Gerados

Snapshots Restaurados

Tempo Médio

Tamanho Médio

Falhas

Downloads
```

---

# Health Check

Informar

```text
Último Snapshot

Tamanho

Checksum

Status

Storage
```

---

# Limpeza

Política padrão

```text
Manter

Últimos 30 Snapshots
```

Configurável.

---

# Organização

```text
synchronization/

    snapshot/

        generator.py

        importer.py

        validator.py

        storage.py

        metadata.py

        compression.py

        encryption.py
```

---

# Testabilidade

O Snapshot deverá possuir:

```text
Generation Tests

Import Tests

Recovery Tests

Checksum Tests

Compression Tests

Large Dataset Tests

Performance Tests
```

---

# Anti-Patterns

Nunca fazer

```text
Gerar Snapshot sem transação

Ignorar Checksum

Misturar Tenants

Ignorar Compressão

Sobrescrever banco parcialmente

Importar sem validação
```

---

# Checklist

Antes de implementar verificar:

- possui Checksum?
- possui Compressão?
- possui Criptografia?
- possui Versionamento?
- suporta Rollback?
- respeita Tenant?
- possui Testes?

---

# Regras Gerais

Todo Snapshot deverá:

- representar um estado consistente;
- ser validado antes da restauração;
- possuir Hash;
- possuir Compressão;
- suportar Rollback;
- respeitar Multi-Tenant;
- permitir recuperação completa.

---

# Fluxo Completo

```text
Servidor

↓

Snapshot Generator

↓

Snapshot

↓

Storage

↓

Desktop

↓

Importação

↓

SQLite

↓

Delta Sync

↓

Banco Atualizado
```

---

# Próximo Documento

```text
042-offline-first-strategy.md
```