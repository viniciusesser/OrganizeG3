# OrganizeG3 — Correção de validação da fatia de Clientes (REV2)

Data: 2026-08-05

## Motivo

A execução local do script `scripts/validate_customer_slice.ps1` identificou:

- 6 erros do Ruff;
- 3 erros do mypy;
- ausência da dependência `httpx2` para o `TestClient` do Starlette atual;
- incompatibilidade do comando de inspeção de rotas com a estrutura interna atual do FastAPI;
- continuidade indevida do script após comandos externos retornarem erro.

## Correções aplicadas

### Ruff

- Ordenação dos imports e de `__all__` em `core/base.py`.
- Uso de `TypeError` para tipo inválido de `tenant_id`.
- Separação correta dos grupos de importação em `database/session.py`.
- Substituição de `zip()` por `itertools.pairwise()` no teste das migrations.
- Remoção do import não utilizado de `datetime`.

### Mypy

- Estreitamento explícito de tipo antes de converter `CustomerType`.
- `cast()` explícito no retorno de `structlog.get_logger()`.
- Separação de `existing_model` no repositório para eliminar atribuição opcional incompatível.

### Dependências de teste

- Substituição da dependência de desenvolvimento `httpx` por `httpx2`.
- Inclusão do extra `test` em `apps/api/pyproject.toml`.

### Script de validação

- Mensagens em ASCII para evitar caracteres corrompidos no Windows PowerShell legado.
- Validação fail-fast: qualquer comando externo com código diferente de zero encerra o script.
- Inspeção de rotas por `app.openapi()["paths"]`.
- Inclusão de `alembic current`.
- Criação de `scripts/validate_customer_slice.cmd`, que executa o PowerShell com `ExecutionPolicy Bypass` apenas para o processo.

## Validação executada neste ambiente

- Compilação de todos os arquivos Python: aprovada.
- Pytest: 38 testes aprovados.
- Cobertura: 75,35%.
- Rotas OpenAPI:
  - `/health`
  - `/api/v1/customers`
- TOML dos dois `pyproject.toml`: válido.

## Comandos locais após atualizar o projeto

```powershell
python -m pip install -e ".[dev]"
python -m pip install -e ".\apps\api[test]"

$env:TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
.\scripts\validate_customer_slice.cmd
```

O arquivo `.env` não faz parte do pacote distribuído e deve permanecer local.
