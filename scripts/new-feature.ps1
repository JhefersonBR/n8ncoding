# Script PowerShell para criar uma nova branch de feature seguindo GitFlow

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName
)

$ErrorActionPreference = "Stop"

$BranchName = "feature/$FeatureName"

# Verifica se estamos no diretório correto
if (-not (Test-Path "src/main.py")) {
    Write-Host "Erro: Execute este script da raiz do projeto" -ForegroundColor Red
    exit 1
}

# Verifica se develop existe
$developExists = git show-ref --verify --quiet refs/heads/develop
if (-not $developExists) {
    Write-Host "Aviso: Branch develop não existe. Criando..." -ForegroundColor Yellow
    git checkout -b develop
    git push -u origin develop
}

# Atualiza develop
Write-Host "Atualizando branch develop..." -ForegroundColor Green
git checkout develop
git pull origin develop

# Verifica se a branch já existe
$branchExists = git show-ref --verify --quiet "refs/heads/$BranchName"
if ($branchExists) {
    Write-Host "Erro: Branch $BranchName já existe" -ForegroundColor Red
    exit 1
}

# Cria nova branch de feature
Write-Host "Criando branch $BranchName..." -ForegroundColor Green
git checkout -b $BranchName

Write-Host "✓ Branch $BranchName criada com sucesso!" -ForegroundColor Green
Write-Host "Você está agora na branch $BranchName" -ForegroundColor Yellow
Write-Host ""
Write-Host "Próximos passos:"
Write-Host "  1. Desenvolva sua funcionalidade"
Write-Host "  2. Faça commits: git add . && git commit -m 'feat: descrição'"
Write-Host "  3. Quando terminar, use: .\scripts\finish-feature.ps1 $FeatureName"

