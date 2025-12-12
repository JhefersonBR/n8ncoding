#!/bin/bash
# Script para criar uma nova branch de feature seguindo GitFlow

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se o nome da feature foi fornecido
if [ -z "$1" ]; then
    echo -e "${RED}Erro: Nome da feature não fornecido${NC}"
    echo "Uso: ./scripts/new-feature.sh nome-da-feature"
    echo "Exemplo: ./scripts/new-feature.sh adicionar-suporte-python"
    exit 1
fi

FEATURE_NAME="$1"
BRANCH_NAME="feature/$FEATURE_NAME"

# Verifica se estamos no diretório correto
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}Erro: Execute este script da raiz do projeto${NC}"
    exit 1
fi

# Verifica se develop existe
if ! git show-ref --verify --quiet refs/heads/develop; then
    echo -e "${YELLOW}Aviso: Branch develop não existe. Criando...${NC}"
    git checkout -b develop
    git push -u origin develop
fi

# Atualiza develop
echo -e "${GREEN}Atualizando branch develop...${NC}"
git checkout develop
git pull origin develop

# Verifica se a branch já existe
if git show-ref --verify --quiet refs/heads/"$BRANCH_NAME"; then
    echo -e "${RED}Erro: Branch $BRANCH_NAME já existe${NC}"
    exit 1
fi

# Cria nova branch de feature
echo -e "${GREEN}Criando branch $BRANCH_NAME...${NC}"
git checkout -b "$BRANCH_NAME"

echo -e "${GREEN}✓ Branch $BRANCH_NAME criada com sucesso!${NC}"
echo -e "${YELLOW}Você está agora na branch $BRANCH_NAME${NC}"
echo ""
echo "Próximos passos:"
echo "  1. Desenvolva sua funcionalidade"
echo "  2. Faça commits: git add . && git commit -m 'feat: descrição'"
echo "  3. Quando terminar, use: ./scripts/finish-feature.sh $FEATURE_NAME"

