# Script para finalizar feature branch
param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Finalizando feature: $FeatureName" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$branchName = "feature/$FeatureName"

# Verifica se está na branch correta
$currentBranch = git branch --show-current
if ($currentBranch -ne $branchName) {
    Write-Host "Aviso: Você não está na branch $branchName" -ForegroundColor Yellow
    Write-Host "Mudando para a branch $branchName..." -ForegroundColor Yellow
    git checkout $branchName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro: Branch $branchName não encontrada!" -ForegroundColor Red
        exit 1
    }
}

# Verifica se há mudanças não commitadas
$status = git status --porcelain
if ($status) {
    Write-Host "`nAviso: Há mudanças não commitadas!" -ForegroundColor Yellow
    Write-Host "Deseja fazer commit agora? (S/N): " -NoNewline -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "S" -or $response -eq "s") {
        Write-Host "Digite a mensagem do commit: " -NoNewline -ForegroundColor Yellow
        $message = Read-Host
        git add .
        git commit -m $message
    } else {
        Write-Host "Por favor, faça commit das mudanças antes de finalizar a feature." -ForegroundColor Red
        exit 1
    }
}

# Faz merge para develop
Write-Host "`nFazendo merge para develop..." -ForegroundColor Yellow
git checkout develop
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro: Branch develop não encontrada!" -ForegroundColor Red
    exit 1
}

git pull origin develop
git merge $branchName --no-ff -m "Merge branch '$branchName' into develop"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Merge realizado com sucesso!" -ForegroundColor Green
    
    # Pergunta se deseja fazer push
    Write-Host "`nDeseja fazer push para origin/develop? (S/N): " -NoNewline -ForegroundColor Yellow
    $pushResponse = Read-Host
    if ($pushResponse -eq "S" -or $pushResponse -eq "s") {
        git push origin develop
        Write-Host "✓ Push realizado!" -ForegroundColor Green
    }
    
    # Remove branch local
    Write-Host "`nRemovendo branch local..." -ForegroundColor Yellow
    git branch -d $branchName
    
    Write-Host "`n✓ Feature finalizada com sucesso!" -ForegroundColor Green
    Write-Host "`nVocê está agora na branch: develop" -ForegroundColor Cyan
} else {
    Write-Host "`nErro ao fazer merge! Resolva os conflitos e tente novamente." -ForegroundColor Red
    exit 1
}
