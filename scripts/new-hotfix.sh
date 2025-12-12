#!/bin/bash

# Script para criar nova hotfix branch

if [ -z "$1" ]; then
    echo "Erro: Nome do hotfix é obrigatório"
    echo "Uso: ./scripts/new-hotfix.sh nome-do-hotfix"
    exit 1
fi

HOTFIX_NAME=$1
BRANCH_NAME="hotfix/$HOTFIX_NAME"

echo "============================================================"
echo "Criando hotfix: $HOTFIX_NAME"
echo "============================================================"

# Atualiza main
echo ""
echo "Atualizando branch main..."
git checkout main || {
    echo "Erro: Branch main não encontrada!"
    exit 1
}

git pull origin main

# Cria hotfix branch
echo ""
echo "Criando branch: $BRANCH_NAME"
git checkout -b $BRANCH_NAME

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Hotfix branch criada com sucesso!"
    echo ""
    echo "Você está agora na branch: $BRANCH_NAME"
    echo ""
    echo "Próximos passos:"
    echo "  1. Corrija o problema urgente"
    echo "  2. Faça commits: git add . && git commit -m 'fix: descrição da correção'"
    echo "  3. Quando terminar, execute: ./scripts/finish-hotfix.sh $HOTFIX_NAME"
else
    echo ""
    echo "Erro ao criar branch!"
    exit 1
fi
