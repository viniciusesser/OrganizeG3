# OrganizeG3 — primeiro acesso no Supabase

## Diagnóstico confirmado

O banco do projeto Supabase é novo, mas a cadeia Alembic atual começa a partir
de tabelas do sistema legado. Portanto, não execute `alembic upgrade head` em
um banco vazio: a revisão `0439fdabfa05` tenta alterar `clientes` antes que essa
tabela exista.

O arquivo `bootstrap_fresh_database.py` cria o esquema atual a partir dos modelos
SQLAlchemy, marca o banco no head Alembic e cria o tenant, usuário local, vínculo
ativo, perfil administrativo e todas as permissões. O comando recusa schemas
parciais ou desconhecidos.

## 1. Colocar os arquivos no projeto

Crie a pasta, caso ainda não exista:

```powershell
New-Item -ItemType Directory `
    -Path "apps/api/src/organizeg3_api/cli" `
    -Force
```

Salve os arquivos nestes caminhos:

```text
apps/api/src/organizeg3_api/cli/__init__.py
apps/api/src/organizeg3_api/cli/bootstrap_fresh_database.py
```

## 2. Configurar as chaves de assinatura

No Supabase, abra as configurações de assinatura JWT e confirme que o projeto
usa uma chave assimétrica `ES256` ou `RS256`. O backend atual consulta o JWKS e
aceita esses dois algoritmos; ele não aceita tokens `HS256`.

## 3. Criar o usuário no Supabase Auth

No painel do projeto, abra `Authentication > Users`, adicione o primeiro usuário
com e-mail e senha e confirme o e-mail pelo painel quando essa opção estiver
disponível. Guarde o UUID do usuário exibido na lista. Esse UUID não é senha.

## 4. Configurar o backend

Na raiz do repositório, crie o `.env` local se ainda não existir:

```powershell
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

notepad .env
```

Preencha localmente:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres.PROJECT_REF:SENHA@HOST_DO_SESSION_POOLER:5432/postgres?sslmode=require
SUPABASE_URL=https://PROJECT_REF.supabase.co
SUPABASE_ANON_KEY=sb_publishable_SUBSTITUA_LOCALMENTE
```

Use a conexão `Session pooler`, porta `5432`, obtida pelo botão `Connect` no
Supabase. Nunca envie a senha do banco pelo chat.

## 5. Configurar o PWA

Crie o arquivo local do PWA:

```powershell
if (-not (Test-Path "apps/pwa/.env.local")) {
    Copy-Item "apps/pwa/.env.example" "apps/pwa/.env.local"
}

notepad apps/pwa/.env.local
```

Preencha:

```dotenv
VITE_API_BASE_URL=/api
VITE_SUPABASE_URL=https://PROJECT_REF.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_SUBSTITUA_LOCALMENTE
```

A chave publicável pode estar no PWA. Não coloque `sb_secret`, `service_role`,
senha do banco ou JWT secret em arquivos `VITE_*`.

## 6. Executar o bootstrap

Na raiz do repositório, com o ambiente virtual ativo:

```powershell
python -m organizeg3_api.cli.bootstrap_fresh_database `
    --auth-user-id "UUID_COPIADO_DO_SUPABASE" `
    --email "SEU_EMAIL_DE_LOGIN" `
    --display-name "Vinícius Esser" `
    --tenant-name "Marcenaria Galdino"
```

O e-mail informado deve ser exatamente o mesmo criado no Supabase Auth.

## 7. Validar

Inicie a API:

```powershell
uvicorn organizeg3_api.main:app --reload
```

Em outro terminal, inicie o PWA:

```powershell
Push-Location "apps/pwa"
npm run dev
```

Entre com o e-mail e a senha criados no Supabase Auth. Depois valide
`Cadastros > Máquinas`.

## Segurança

- Não execute o bootstrap contra um banco legado.
- Não envie `.env`, senha, chave secreta ou `service_role` pelo chat.
- Não execute `alembic upgrade head` no Supabase vazio antes deste bootstrap.
- Guarde a senha do banco e a senha do usuário em um gerenciador de senhas.
