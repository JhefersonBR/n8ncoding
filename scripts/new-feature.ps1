# Script para criar nova feature branch
param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Criando nova feature: $FeatureName" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Verifica se está em um repositório git
if (-not (Test-Path .git)) {
    Write-Host "Erro: Não é um repositório Git!" -ForegroundColor Red
    exit 1
}

# Atualiza develop
Write-Host "`nAtualizando branch develop..." -ForegroundColor Yellow
git checkout develop
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro: Branch develop não encontrada. Crie-a primeiro com: git checkout -b develop" -ForegroundColor Red
    exit 1
}

git pull origin develop
if ($LASTEXITCODE -ne 0) {
    Write-Host "Aviso: Não foi possível fazer pull. Continuando..." -ForegroundColor Yellow
}

# Cria nova feature branch
$branchName = "feature/$FeatureName"
Write-Host "`nCriando branch: $branchName" -ForegroundColor Yellow
git checkout -b $branchName

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Feature branch criada com sucesso!" -ForegroundColor Green
    Write-Host "`nVocê está agora na branch: $branchName" -ForegroundColor Cyan
    Write-Host "`nPróximos passos:" -ForegroundColor Yellow
    Write-Host "  1. Desenvolva sua feature"
    Write-Host "  2. Faça commits: git add . && git commit -m 'feat: descrição'"
    Write-Host "  3. Quando terminar, execute: .\scripts\finish-feature.ps1 $FeatureName"
} else {
    Write-Host "`nErro ao criar branch!" -ForegroundColor Red
    exit 1
}
