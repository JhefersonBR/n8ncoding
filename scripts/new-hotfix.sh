#!/bin/bash
# Script para criar uma nova branch de hotfix seguindo GitFlow

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se o nome do hotfix foi fornecido
if [ -z "$1" ]; then
    echo -e "${RED}Erro: Nome do hotfix não fornecido${NC}"
    echo "Uso: ./scripts/new-hotfix.sh nome-do-hotfix"
    echo "Exemplo: ./scripts/new-hotfix.sh corrigir-bug-critico"
    exit 1
fi

HOTFIX_NAME="$1"
BRANCH_NAME="hotfix/$HOTFIX_NAME"

# Verifica se estamos no diretório correto
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}Erro: Execute este script da raiz do projeto${NC}"
    exit 1
fi

# Verifica se main existe
if ! git show-ref --verify --quiet refs/heads/main; then
    echo -e "${RED}Erro: Branch main não existe${NC}"
    exit 1
fi

# Atualiza main
echo -e "${GREEN}Atualizando branch main...${NC}"
git checkout main
git pull origin main

# Verifica se a branch já existe
if git show-ref --verify --quiet refs/heads/"$BRANCH_NAME"; then
    echo -e "${RED}Erro: Branch $BRANCH_NAME já existe${NC}"
    exit 1
fi

# Cria nova branch de hotfix
echo -e "${GREEN}Criando branch $BRANCH_NAME...${NC}"
git checkout -b "$BRANCH_NAME"

echo -e "${GREEN}✓ Branch $BRANCH_NAME criada com sucesso!${NC}"
echo -e "${YELLOW}Você está agora na branch $BRANCH_NAME${NC}"
echo ""
echo "Próximos passos:"
echo "  1. Corrija o bug urgente"
echo "  2. Faça commits: git add . && git commit -m 'fix: descrição do fix'"
echo "  3. Quando terminar, use: ./scripts/finish-hotfix.sh $HOTFIX_NAME [versao]"

