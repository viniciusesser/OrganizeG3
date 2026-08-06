# OrganizeG3 — Relatório de estabilização da fatia de Clientes

## Escopo executado

Esta entrega estabiliza somente a fundação técnica e os fluxos existentes de criação e listagem de clientes. O módulo de Funcionários não foi iniciado.

## Correções aplicadas

1. Padronização de todos os `pyproject.toml` para Python `>=3.13,<3.14`.
2. Ruff configurado para `py313` e mypy configurado para Python 3.13.
3. Consolidação da `Base` SQLAlchemy em `infrastructure/database/base.py`.
4. `core/base.py` mantido apenas como compatibilidade por reexportação.
5. Remoção da segunda criação de engine em `infrastructure/http/dependencies.py`.
6. Conversão da infraestrutura SQLAlchemy de assíncrona para síncrona.
7. Repositório de Clientes convertido para `Session` síncrona.
8. Casos de uso convertidos para execução síncrona.
9. Registro das rotas em `/api/v1/customers`.
10. Remoção de `tenant_id` do payload de criação.
11. Inclusão da dependência temporária central `X-Tenant-ID`.
12. Validação de UUID ausente, inválido ou nulo.
13. Aplicação de filtro de tenant em leitura e atualização.
14. Bloqueio de atualização entre tenants.
15. Repositório sem `commit`; a transação pertence à infraestrutura de sessão.
16. Verificação explícita de versão otimista antes da atualização.
17. Validações mínimas da entidade: tenant, código, nome, tipo e versão.
18. Inclusão de `X-Tenant-ID` no CORS e no `.env.example`.
19. Alembic convertido para engine síncrona.
20. Criação da suíte de testes de domínio, aplicação, persistência, API e migrations.

## Correção crítica da baseline

A migration `acc9bffaedbc_baseline.py` estava invertida: o método `upgrade()` continha dezenas de operações `DROP TABLE` e apagaria o banco legado caso fosse executado.

Ela foi transformada em uma baseline intencionalmente vazia e não destrutiva. A estratégia agora é:

1. partir de um banco legado existente;
2. marcar esse banco na baseline;
3. aplicar apenas migrations incrementais e não destrutivas posteriores.

A revisão e seu identificador foram preservados. Como o banco informado já estava em `0439fdabfa05 (head)`, essa mudança não executa DDL retroativo no banco atual.

## Testes criados

- entidade de domínio;
- criação de cliente;
- listagem de clientes;
- isolamento entre tenants;
- filtros de ativos e excluídos;
- persistência ORM;
- atualização segura;
- concorrência otimista;
- rotas FastAPI;
- cabeçalho de tenant;
- resposta padronizada de validação;
- cadeia e head do Alembic;
- geração de SQL PostgreSQL para upgrade e downgrade;
- proteção não destrutiva da baseline;
- correspondência entre modelo ORM e colunas mapeadas.

## Resultado obtido neste ambiente

```text
38 passed
Cobertura total: 75,44%
Cobertura mínima configurada: 70%
Alembic head: 0439fdabfa05
Rota registrada: /api/v1/customers
Compilação Python: aprovada
```

A suíte foi executada com `TEST_DATABASE_URL=sqlite+pysqlite:///:memory:`. Os testes nunca usam `DATABASE_URL` como fallback e falham quando `TEST_DATABASE_URL` está ausente ou é igual a `DATABASE_URL`.

## Validações não executadas neste ambiente

Ruff e mypy estão configurados no projeto, mas os executáveis não estavam disponíveis no ambiente isolado usado para esta correção, e o repositório de pacotes desse ambiente não os forneceu. O script `scripts/validate_customer_slice.ps1` executa ambos no ambiente local do projeto, onde essas dependências já estão instaladas.

Não foi executado upgrade real contra PostgreSQL porque não foi fornecido um banco PostgreSQL descartável. As funções das migrations foram executadas em modo SQL offline com o dialeto PostgreSQL. Nenhum acesso foi feito ao banco de desenvolvimento.

## Situação do `requirements.txt`

O arquivo foi preservado para não eliminar informação do ambiente anterior, mas não é a fonte oficial de dependências. Ele contém um congelamento antigo em UTF-16 e versões incompatíveis com os intervalos definidos nos `pyproject.toml`. A instalação oficial deve continuar sendo feita pelos `pyproject.toml`; o arquivo poderá ser regenerado ou removido em uma etapa posterior controlada.

## Arquivos principais modificados

- `pyproject.toml`
- todos os `pyproject.toml` dos apps e packages
- `.env.example`
- `alembic.ini`
- `database/migrations/env.py`
- `database/migrations/versions/acc9bffaedbc_baseline.py`
- `organizeg3_api/core/base.py`
- `organizeg3_api/domain/customer/entity.py`
- `organizeg3_api/domain/customer/repository.py`
- `organizeg3_api/application/customer/schemas.py`
- casos de uso de Clientes
- `infrastructure/database/session.py`
- `infrastructure/http/dependencies.py`
- modelo e repositório SQLAlchemy de Clientes
- rotas de Clientes
- agregador de rotas v1
- `main.py`

## Arquivos principais criados

- arquivos `__init__.py` necessários para os pacotes da fatia;
- `apps/api/tests/conftest.py`;
- testes unitários de domínio e aplicação;
- testes de persistência;
- testes de API;
- testes de migrations;
- `scripts/validate_customer_slice.ps1`;
- este relatório.

## O que ainda falta para declarar Clientes funcionalmente concluído

- consultar cliente por ID;
- editar cliente;
- pesquisa e filtros completos;
- arquivar;
- reativar;
- value objects de CPF/CNPJ, e-mail e telefone;
- política formal de duplicidade;
- permissões;
- auditoria;
- eventos de domínio;
- ViewModels;
- interface PySide6;
- feature flag;
- comparação funcional com o sistema legado.

## Portão atual

A fundação de criação e listagem está testada, mas Clientes ainda não deve ser declarado completamente concluído e Funcionários ainda não deve ser iniciado até que os fluxos restantes sejam implementados e validados.
