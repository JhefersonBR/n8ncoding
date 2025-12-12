#!/bin/bash
# Script para configurar GitFlow no repositório

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Configurando GitFlow...${NC}"

# Verifica se estamos no diretório correto
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}Erro: Execute este script da raiz do projeto${NC}"
    exit 1
fi

# Verifica se já é um repositório Git
if [ ! -d ".git" ]; then
    echo -e "${RED}Erro: Este diretório não é um repositório Git${NC}"
    exit 1
fi

# Cria branch develop se não existir
if ! git show-ref --verify --quiet refs/heads/develop; then
    echo -e "${YELLOW}Criando branch develop...${NC}"
    git checkout -b develop
    git push -u origin develop
    echo -e "${GREEN}✓ Branch develop criada${NC}"
else
    echo -e "${GREEN}✓ Branch develop já existe${NC}"
fi

# Verifica se main existe, se não, cria
if ! git show-ref --verify --quiet refs/heads/main; then
    if git show-ref --verify --quiet refs/heads/master; then
        echo -e "${YELLOW}Renomeando master para main...${NC}"
        git branch -m master main
        git push origin -u main
        git push origin --delete master
        echo -e "${GREEN}✓ Branch renomeada para main${NC}"
    else
        echo -e "${YELLOW}Criando branch main...${NC}"
        git checkout -b main
        git push -u origin main
        echo -e "${GREEN}✓ Branch main criada${NC}"
    fi
else
    echo -e "${GREEN}✓ Branch main já existe${NC}"
fi

# Torna scripts executáveis
echo -e "${YELLOW}Tornando scripts executáveis...${NC}"
chmod +x scripts/*.sh
echo -e "${GREEN}✓ Scripts configurados${NC}"

echo ""
echo -e "${GREEN}✓ GitFlow configurado com sucesso!${NC}"
echo ""
echo "Branches disponíveis:"
git branch -a
echo ""
echo "Próximos passos:"
echo "  1. Use ./scripts/new-feature.sh nome para criar uma nova feature"
echo "  2. Use ./scripts/new-release.sh versao para criar uma nova release"
echo "  3. Use ./scripts/new-hotfix.sh nome para criar um hotfix"
echo ""
echo "Veja GITFLOW.md para mais informações"

