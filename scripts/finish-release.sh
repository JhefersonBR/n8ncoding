#!/bin/bash

# Script para finalizar release branch

if [ -z "$1" ]; then
    echo "Erro: Versão é obrigatória"
    echo "Uso: ./scripts/finish-release.sh 1.0.0"
    exit 1
fi

VERSION=$1
BRANCH_NAME="release/$VERSION"
TAG_NAME="v$VERSION"

echo "============================================================"
echo "Finalizando release: $VERSION"
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

# Merge para main
echo ""
echo "Fazendo merge para main..."
git checkout main || {
    echo "Erro: Branch main não encontrada!"
    exit 1
}

git pull origin main
git merge $BRANCH_NAME --no-ff -m "Release $VERSION"

if [ $? -ne 0 ]; then
    echo "Erro ao fazer merge para main!"
    exit 1
fi

# Cria tag
echo ""
echo "Criando tag: $TAG_NAME"
git tag -a $TAG_NAME -m "Release $VERSION" || {
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
    echo "✓ Release finalizada com sucesso!"
    echo ""
    echo "Você está agora na branch: develop"
else
    echo "Erro ao fazer merge para develop!"
    exit 1
fi
