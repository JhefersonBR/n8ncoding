# Script para criar nova hotfix branch
param(
    [Parameter(Mandatory=$true)]
    [string]$HotfixName
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Criando hotfix: $HotfixName" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Atualiza main
Write-Host "`nAtualizando branch main..." -ForegroundColor Yellow
git checkout main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro: Branch main não encontrada!" -ForegroundColor Red
    exit 1
}

git pull origin main

# Cria hotfix branch
$branchName = "hotfix/$HotfixName"
Write-Host "`nCriando branch: $branchName" -ForegroundColor Yellow
git checkout -b $branchName

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Hotfix branch criada com sucesso!" -ForegroundColor Green
    Write-Host "`nVocê está agora na branch: $branchName" -ForegroundColor Cyan
    Write-Host "`nPróximos passos:" -ForegroundColor Yellow
    Write-Host "  1. Corrija o problema urgente"
    Write-Host "  2. Faça commits: git add . && git commit -m 'fix: descrição da correção'"
    Write-Host "  3. Quando terminar, execute: .\scripts\finish-hotfix.ps1 $HotfixName"
} else {
    Write-Host "`nErro ao criar branch!" -ForegroundColor Red
    exit 1
}

