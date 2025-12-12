# Script para criar nova release branch
param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Criando release: $Version" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Verifica formato da versão (básico)
if ($Version -notmatch '^\d+\.\d+\.\d+') {
    Write-Host "Aviso: Formato de versão recomendado: X.Y.Z (ex: 1.0.0)" -ForegroundColor Yellow
}

# Atualiza develop
Write-Host "`nAtualizando branch develop..." -ForegroundColor Yellow
git checkout develop
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro: Branch develop não encontrada!" -ForegroundColor Red
    exit 1
}

git pull origin develop

# Cria release branch
$branchName = "release/$Version"
Write-Host "`nCriando branch: $branchName" -ForegroundColor Yellow
git checkout -b $branchName

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Release branch criada com sucesso!" -ForegroundColor Green
    Write-Host "`nVocê está agora na branch: $branchName" -ForegroundColor Cyan
    Write-Host "`nPróximos passos:" -ForegroundColor Yellow
    Write-Host "  1. Atualize a versão nos arquivos necessários"
    Write-Host "  2. Atualize o CHANGELOG.md"
    Write-Host "  3. Faça commits: git add . && git commit -m 'chore: atualiza versão para $Version'"
    Write-Host "  4. Quando terminar, execute: .\scripts\finish-release.ps1 $Version"
} else {
    Write-Host "`nErro ao criar branch!" -ForegroundColor Red
    exit 1
}

