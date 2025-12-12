#!/bin/bash
# Script para criar uma nova branch de release seguindo GitFlow

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se a versão foi fornecida
if [ -z "$1" ]; then
    echo -e "${RED}Erro: Versão não fornecida${NC}"
    echo "Uso: ./scripts/new-release.sh versao"
    echo "Exemplo: ./scripts/new-release.sh 1.0.0"
    exit 1
fi

VERSION="$1"
BRANCH_NAME="release/v$VERSION"

# Verifica formato da versão (básico)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Erro: Versão deve estar no formato X.Y.Z (ex: 1.0.0)${NC}"
    exit 1
fi

# Verifica se estamos no diretório correto
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}Erro: Execute este script da raiz do projeto${NC}"
    exit 1
fi

# Verifica se develop existe
if ! git show-ref --verify --quiet refs/heads/develop; then
    echo -e "${RED}Erro: Branch develop não existe${NC}"
    exit 1
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

# Cria nova branch de release
echo -e "${GREEN}Criando branch $BRANCH_NAME...${NC}"
git checkout -b "$BRANCH_NAME"

echo -e "${GREEN}✓ Branch $BRANCH_NAME criada com sucesso!${NC}"
echo -e "${YELLOW}Você está agora na branch $BRANCH_NAME${NC}"
echo ""
echo "Próximos passos:"
echo "  1. Atualize a versão nos arquivos necessários"
echo "  2. Atualize o CHANGELOG.md"
echo "  3. Faça apenas correções de bugs (sem novas features)"
echo "  4. Quando pronto, use: ./scripts/finish-release.sh $VERSION"

