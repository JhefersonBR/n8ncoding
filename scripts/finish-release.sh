#!/bin/bash
# Script para finalizar uma release e fazer merge em main e develop

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se a versão foi fornecida
if [ -z "$1" ]; then
    echo -e "${RED}Erro: Versão não fornecida${NC}"
    echo "Uso: ./scripts/finish-release.sh versao"
    echo "Exemplo: ./scripts/finish-release.sh 1.0.0"
    exit 1
fi

VERSION="$1"
BRANCH_NAME="release/v$VERSION"
TAG_NAME="v$VERSION"

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

# Verifica se main existe
if ! git show-ref --verify --quiet refs/heads/main; then
    echo -e "${YELLOW}Aviso: Branch main não existe. Criando...${NC}"
    git checkout -b main
    git push -u origin main
fi

# Atualiza develop
echo -e "${GREEN}Atualizando branch develop...${NC}"
git checkout develop
git pull origin develop

# Faz merge da release em develop
echo -e "${GREEN}Fazendo merge de $BRANCH_NAME em develop...${NC}"
git merge --no-ff "$BRANCH_NAME" -m "Merge branch '$BRANCH_NAME' into develop"
git push origin develop

# Faz merge da release em main
echo -e "${GREEN}Fazendo merge de $BRANCH_NAME em main...${NC}"
git checkout main
git pull origin main
git merge --no-ff "$BRANCH_NAME" -m "Release $TAG_NAME"

# Cria tag
echo -e "${GREEN}Criando tag $TAG_NAME...${NC}"
git tag -a "$TAG_NAME" -m "Release $TAG_NAME"
git push origin main
git push origin "$TAG_NAME"

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

# Volta para develop
git checkout develop

echo -e "${GREEN}✓ Release $VERSION finalizada com sucesso!${NC}"
echo -e "${YELLOW}Tag $TAG_NAME criada em main${NC}"
echo -e "${YELLOW}Você está agora na branch develop${NC}"

