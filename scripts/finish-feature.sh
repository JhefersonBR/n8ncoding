#!/bin/bash

# Script para finalizar feature branch

if [ -z "$1" ]; then
    echo "Erro: Nome da feature é obrigatório"
    echo "Uso: ./scripts/finish-feature.sh nome-da-feature"
    exit 1
fi

FEATURE_NAME=$1
BRANCH_NAME="feature/$FEATURE_NAME"

echo "============================================================"
echo "Finalizando feature: $FEATURE_NAME"
echo "============================================================"

# Verifica se está na branch correta
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
    echo "Aviso: Você não está na branch $BRANCH_NAME"
    echo "Mudando para a branch $BRANCH_NAME..."
    git checkout $BRANCH_NAME || {
        echo "Erro: Branch $BRANCH_NAME não encontrada!"
        exit 1
    }
fi

# Verifica se há mudanças não commitadas
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "Aviso: Há mudanças não commitadas!"
    read -p "Deseja fazer commit agora? (S/N): " response
    if [ "$response" = "S" ] || [ "$response" = "s" ]; then
        read -p "Digite a mensagem do commit: " message
        git add .
        git commit -m "$message"
    else
        echo "Por favor, faça commit das mudanças antes de finalizar a feature."
        exit 1
    fi
fi

# Faz merge para develop
echo ""
echo "Fazendo merge para develop..."
git checkout develop || {
    echo "Erro: Branch develop não encontrada!"
    exit 1
}

git pull origin develop
git merge $BRANCH_NAME --no-ff -m "Merge branch '$BRANCH_NAME' into develop"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Merge realizado com sucesso!"
    
    # Pergunta se deseja fazer push
    read -p "Deseja fazer push para origin/develop? (S/N): " push_response
    if [ "$push_response" = "S" ] || [ "$push_response" = "s" ]; then
        git push origin develop
        echo "✓ Push realizado!"
    fi
    
    # Remove branch local
    echo ""
    echo "Removendo branch local..."
    git branch -d $BRANCH_NAME
    
    echo ""
    echo "✓ Feature finalizada com sucesso!"
    echo ""
    echo "Você está agora na branch: develop"
else
    echo ""
    echo "Erro ao fazer merge! Resolva os conflitos e tente novamente."
    exit 1
fi
