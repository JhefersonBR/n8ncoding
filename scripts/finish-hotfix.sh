#!/bin/bash
# Script para finalizar um hotfix e fazer merge em main e develop

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se o nome do hotfix foi fornecido
if [ -z "$1" ]; then
    echo -e "${RED}Erro: Nome do hotfix não fornecido${NC}"
    echo "Uso: ./scripts/finish-hotfix.sh nome-do-hotfix [versao]"
    echo "Exemplo: ./scripts/finish-hotfix.sh corrigir-bug-critico 1.0.1"
    exit 1
fi

HOTFIX_NAME="$1"
BRANCH_NAME="hotfix/$HOTFIX_NAME"
VERSION="$2"

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

# Verifica se develop existe
if ! git show-ref --verify --quiet refs/heads/develop; then
    echo -e "${YELLOW}Aviso: Branch develop não existe. Criando...${NC}"
    git checkout -b develop
    git push -u origin develop
fi

# Atualiza main
echo -e "${GREEN}Atualizando branch main...${NC}"
git checkout main
git pull origin main

# Faz merge do hotfix em main
echo -e "${GREEN}Fazendo merge de $BRANCH_NAME em main...${NC}"
git merge --no-ff "$BRANCH_NAME" -m "Hotfix: $HOTFIX_NAME"

# Cria tag se versão fornecida
if [ -n "$VERSION" ]; then
    TAG_NAME="v$VERSION"
    echo -e "${GREEN}Criando tag $TAG_NAME...${NC}"
    git tag -a "$TAG_NAME" -m "Hotfix $TAG_NAME: $HOTFIX_NAME"
    git push origin main
    git push origin "$TAG_NAME"
else
    echo -e "${YELLOW}Aviso: Versão não fornecida, tag não criada${NC}"
    git push origin main
fi

# Faz merge do hotfix em develop
echo -e "${GREEN}Fazendo merge de $BRANCH_NAME em develop...${NC}"
git checkout develop
git pull origin develop
git merge --no-ff "$BRANCH_NAME" -m "Merge hotfix '$BRANCH_NAME' into develop"
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

echo -e "${GREEN}✓ Hotfix $HOTFIX_NAME finalizado com sucesso!${NC}"
echo -e "${YELLOW}Você está agora na branch develop${NC}"

