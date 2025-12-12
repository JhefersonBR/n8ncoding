#!/bin/bash
# Script para finalizar uma branch de feature e fazer merge em develop

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se o nome da feature foi fornecido
if [ -z "$1" ]; then
    echo -e "${RED}Erro: Nome da feature não fornecido${NC}"
    echo "Uso: ./scripts/finish-feature.sh nome-da-feature"
    echo "Exemplo: ./scripts/finish-feature.sh adicionar-suporte-python"
    exit 1
fi

FEATURE_NAME="$1"
BRANCH_NAME="feature/$FEATURE_NAME"

# Verifica se estamos no diretório correto
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}Erro: Execute este script da raiz do projeto${NC}"
    exit 1
fi

# Verifica se a branch existe
if ! git show-ref --verify --quiet refs/heads/"$BRANCH_NAME"; then
    echo -e "${RED}Erro: Branch $BRANCH_NAME não existe${NC}"
    exit 1
fi

# Verifica se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}Aviso: Há mudanças não commitadas${NC}"
    read -p "Deseja continuar mesmo assim? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Atualiza develop
echo -e "${GREEN}Atualizando branch develop...${NC}"
git checkout develop
git pull origin develop

# Faz merge da feature
echo -e "${GREEN}Fazendo merge de $BRANCH_NAME em develop...${NC}"
git merge --no-ff "$BRANCH_NAME" -m "Merge branch '$BRANCH_NAME' into develop"

# Push para develop
echo -e "${GREEN}Enviando para origin/develop...${NC}"
git push origin develop

# Deleta branch local
echo -e "${GREEN}Deletando branch local $BRANCH_NAME...${NC}"
git branch -d "$BRANCH_NAME"

# Pergunta se quer deletar branch remota
read -p "Deseja deletar a branch remota também? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    git push origin --delete "$BRANCH_NAME"
    echo -e "${GREEN}✓ Branch remota deletada${NC}"
fi

echo -e "${GREEN}✓ Feature $FEATURE_NAME finalizada com sucesso!${NC}"
echo -e "${YELLOW}Você está agora na branch develop${NC}"

