$ErrorActionPreference = "Stop"

function Invoke-PythonCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha no comando: python $($Arguments -join ' ')"
    }
}

if (-not $env:TEST_DATABASE_URL) {
    throw "Defina TEST_DATABASE_URL para um banco descartavel e exclusivo de testes."
}

if ($env:DATABASE_URL -and ($env:TEST_DATABASE_URL -eq $env:DATABASE_URL)) {
    throw "TEST_DATABASE_URL nao pode ser igual a DATABASE_URL."
}

Write-Host "Python" -ForegroundColor Cyan
Invoke-PythonCommand @("--version")

Write-Host "Dependencias" -ForegroundColor Cyan
Invoke-PythonCommand @("-m", "pip", "check")

Write-Host "Ruff" -ForegroundColor Cyan
Invoke-PythonCommand @("-m", "ruff", "check", ".")

Write-Host "Mypy" -ForegroundColor Cyan
Invoke-PythonCommand @("-m", "mypy", "apps/api/src")

Write-Host "Testes" -ForegroundColor Cyan
Invoke-PythonCommand @("-m", "pytest", "-v")

Write-Host "Cobertura" -ForegroundColor Cyan
Invoke-PythonCommand @(
    "-m",
    "pytest",
    "--cov=apps/api/src",
    "--cov-report=term-missing"
)

Write-Host "Rotas" -ForegroundColor Cyan
Invoke-PythonCommand @(
    "-c",
    "from organizeg3_api.main import app; print(sorted(app.openapi()['paths']))"
)

Write-Host "Alembic" -ForegroundColor Cyan
Invoke-PythonCommand @("-m", "alembic", "current")
Invoke-PythonCommand @("-m", "alembic", "heads")
Invoke-PythonCommand @("-m", "alembic", "history")

Write-Host "Validacao concluida com sucesso." -ForegroundColor Green
