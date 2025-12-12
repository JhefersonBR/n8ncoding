# Script PowerShell para finalizar uma branch de feature e fazer merge em develop

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

# Verifica se a branch existe
$branchExists = git show-ref --verify --quiet "refs/heads/$BranchName"
if (-not $branchExists) {
    Write-Host "Erro: Branch $BranchName não existe" -ForegroundColor Red
    exit 1
}

# Verifica se há mudanças não commitadas
$hasChanges = git diff-index --quiet HEAD --
if (-not $hasChanges) {
    Write-Host "Aviso: Há mudanças não commitadas" -ForegroundColor Yellow
    $response = Read-Host "Deseja continuar mesmo assim? (s/N)"
    if ($response -ne "s" -and $response -ne "S") {
        exit 1
    }
}

# Atualiza develop
Write-Host "Atualizando branch develop..." -ForegroundColor Green
git checkout develop
git pull origin develop

# Faz merge da feature
Write-Host "Fazendo merge de $BranchName em develop..." -ForegroundColor Green
git merge --no-ff $BranchName -m "Merge branch '$BranchName' into develop"

# Push para develop
Write-Host "Enviando para origin/develop..." -ForegroundColor Green
git push origin develop

# Deleta branch local
Write-Host "Deletando branch local $BranchName..." -ForegroundColor Green
git branch -d $BranchName

# Pergunta se quer deletar branch remota
$response = Read-Host "Deseja deletar a branch remota também? (s/N)"
if ($response -eq "s" -or $response -eq "S") {
    git push origin --delete $BranchName
    Write-Host "✓ Branch remota deletada" -ForegroundColor Green
}

Write-Host "✓ Feature $FeatureName finalizada com sucesso!" -ForegroundColor Green
Write-Host "Você está agora na branch develop" -ForegroundColor Yellow

