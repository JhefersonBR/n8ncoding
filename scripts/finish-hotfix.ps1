# Script para finalizar hotfix branch
param(
    [Parameter(Mandatory=$true)]
    [string]$HotfixName
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Finalizando hotfix: $HotfixName" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$branchName = "hotfix/$HotfixName"

# Verifica se está na branch correta
$currentBranch = git branch --show-current
if ($currentBranch -ne $branchName) {
    Write-Host "Mudando para a branch $branchName..." -ForegroundColor Yellow
    git checkout $branchName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro: Branch $branchName não encontrada!" -ForegroundColor Red
        exit 1
    }
}

# Pede versão para tag
Write-Host "`nDigite a versão do hotfix (ex: 1.0.1): " -NoNewline -ForegroundColor Yellow
$version = Read-Host
$tagName = "v$version"

# Merge para main
Write-Host "`nFazendo merge para main..." -ForegroundColor Yellow
git checkout main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro: Branch main não encontrada!" -ForegroundColor Red
    exit 1
}

git pull origin main
git merge $branchName --no-ff -m "Hotfix $HotfixName"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao fazer merge para main!" -ForegroundColor Red
    exit 1
}

# Cria tag
Write-Host "`nCriando tag: $tagName" -ForegroundColor Yellow
git tag -a $tagName -m "Hotfix $HotfixName - $version"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao criar tag!" -ForegroundColor Red
    exit 1
}

# Push para main com tags
Write-Host "`nDeseja fazer push para origin/main com tags? (S/N): " -NoNewline -ForegroundColor Yellow
$pushResponse = Read-Host
if ($pushResponse -eq "S" -or $pushResponse -eq "s") {
    git push origin main
    git push origin $tagName
    Write-Host "✓ Push realizado!" -ForegroundColor Green
}

# Merge para develop
Write-Host "`nFazendo merge para develop..." -ForegroundColor Yellow
git checkout develop
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro: Branch develop não encontrada!" -ForegroundColor Red
    exit 1
}

git pull origin develop
git merge $branchName --no-ff -m "Merge branch '$branchName' into develop"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Merge para develop realizado!" -ForegroundColor Green
    
    Write-Host "`nDeseja fazer push para origin/develop? (S/N): " -NoNewline -ForegroundColor Yellow
    $pushDevResponse = Read-Host
    if ($pushDevResponse -eq "S" -or $pushDevResponse -eq "s") {
        git push origin develop
        Write-Host "✓ Push realizado!" -ForegroundColor Green
    }
    
    # Remove branch local
    Write-Host "`nRemovendo branch local..." -ForegroundColor Yellow
    git branch -d $branchName
    
    Write-Host "`n✓ Hotfix finalizado com sucesso!" -ForegroundColor Green
    Write-Host "`nVocê está agora na branch: develop" -ForegroundColor Cyan
} else {
    Write-Host "Erro ao fazer merge para develop!" -ForegroundColor Red
    exit 1
}

