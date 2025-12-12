#!/bin/bash

# Script para finalizar hotfix branch

if [ -z "$1" ]; then
    echo "Erro: Nome do hotfix é obrigatório"
    echo "Uso: ./scripts/finish-hotfix.sh nome-do-hotfix"
    exit 1
fi

HOTFIX_NAME=$1
BRANCH_NAME="hotfix/$HOTFIX_NAME"

echo "============================================================"
echo "Finalizando hotfix: $HOTFIX_NAME"
echo "============================================================"

# Verifica se está na branch correta
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
    echo "Mudando para a branch $BRANCH_NAME..."
    git checkout $BRANCH_NAME || {
        echo "Erro: Branch $BRANCH_NAME não encontrada!"
        exit 1
    }
fi

# Pede versão para tag
read -p "Digite a versão do hotfix (ex: 1.0.1): " version
TAG_NAME="v$version"

# Merge para main
echo ""
echo "Fazendo merge para main..."
git checkout main || {
    echo "Erro: Branch main não encontrada!"
    exit 1
}

git pull origin main
git merge $BRANCH_NAME --no-ff -m "Hotfix $HOTFIX_NAME"

if [ $? -ne 0 ]; then
    echo "Erro ao fazer merge para main!"
    exit 1
fi

# Cria tag
echo ""
echo "Criando tag: $TAG_NAME"
git tag -a $TAG_NAME -m "Hotfix $HOTFIX_NAME - $version" || {
    echo "Erro ao criar tag!"
    exit 1
}

# Push para main com tags
read -p "Deseja fazer push para origin/main com tags? (S/N): " push_response
if [ "$push_response" = "S" ] || [ "$push_response" = "s" ]; then
    git push origin main
    git push origin $TAG_NAME
    echo "✓ Push realizado!"
fi

# Merge para develop
echo ""
echo "Fazendo merge para develop..."
git checkout develop || {
    echo "Erro: Branch develop não encontrada!"
    exit 1
}

git pull origin develop
git merge $BRANCH_NAME --no-ff -m "Merge branch '$BRANCH_NAME' into develop"

if [ $? -eq 0 ]; then
    echo "✓ Merge para develop realizado!"
    
    read -p "Deseja fazer push para origin/develop? (S/N): " push_dev_response
    if [ "$push_dev_response" = "S" ] || [ "$push_dev_response" = "s" ]; then
        git push origin develop
        echo "✓ Push realizado!"
    fi
    
    # Remove branch local
    echo ""
    echo "Removendo branch local..."
    git branch -d $BRANCH_NAME
    
    echo ""
    echo "✓ Hotfix finalizado com sucesso!"
    echo ""
    echo "Você está agora na branch: develop"
else
    echo "Erro ao fazer merge para develop!"
    exit 1
fi
