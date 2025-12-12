#!/bin/bash

# Script para criar nova release branch

if [ -z "$1" ]; then
    echo "Erro: Versão é obrigatória"
    echo "Uso: ./scripts/new-release.sh 1.0.0"
    exit 1
fi

VERSION=$1
BRANCH_NAME="release/$VERSION"

echo "============================================================"
echo "Criando release: $VERSION"
echo "============================================================"

# Atualiza develop
echo ""
echo "Atualizando branch develop..."
git checkout develop || {
    echo "Erro: Branch develop não encontrada!"
    exit 1
}

git pull origin develop

# Cria release branch
echo ""
echo "Criando branch: $BRANCH_NAME"
git checkout -b $BRANCH_NAME

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Release branch criada com sucesso!"
    echo ""
    echo "Você está agora na branch: $BRANCH_NAME"
    echo ""
    echo "Próximos passos:"
    echo "  1. Atualize a versão nos arquivos necessários"
    echo "  2. Atualize o CHANGELOG.md"
    echo "  3. Faça commits: git add . && git commit -m 'chore: atualiza versão para $VERSION'"
    echo "  4. Quando terminar, execute: ./scripts/finish-release.sh $VERSION"
else
    echo ""
    echo "Erro ao criar branch!"
    exit 1
fi
