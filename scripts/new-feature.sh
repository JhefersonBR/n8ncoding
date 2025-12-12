#!/bin/bash

# Script para criar nova feature branch

if [ -z "$1" ]; then
    echo "Erro: Nome da feature é obrigatório"
    echo "Uso: ./scripts/new-feature.sh nome-da-feature"
    exit 1
fi

FEATURE_NAME=$1
BRANCH_NAME="feature/$FEATURE_NAME"

echo "============================================================"
echo "Criando nova feature: $FEATURE_NAME"
echo "============================================================"

# Verifica se está em um repositório git
if [ ! -d .git ]; then
    echo "Erro: Não é um repositório Git!"
    exit 1
fi

# Atualiza develop
echo ""
echo "Atualizando branch develop..."
git checkout develop || {
    echo "Erro: Branch develop não encontrada. Crie-a primeiro com: git checkout -b develop"
    exit 1
}

git pull origin develop || echo "Aviso: Não foi possível fazer pull. Continuando..."

# Cria nova feature branch
echo ""
echo "Criando branch: $BRANCH_NAME"
git checkout -b $BRANCH_NAME

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Feature branch criada com sucesso!"
    echo ""
    echo "Você está agora na branch: $BRANCH_NAME"
    echo ""
    echo "Próximos passos:"
    echo "  1. Desenvolva sua feature"
    echo "  2. Faça commits: git add . && git commit -m 'feat: descrição'"
    echo "  3. Quando terminar, execute: ./scripts/finish-feature.sh $FEATURE_NAME"
else
    echo ""
    echo "Erro ao criar branch!"
    exit 1
fi
