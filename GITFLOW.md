# GitFlow - Guia de Uso

Este projeto utiliza o padrão **GitFlow** para gerenciamento de branches e releases.

## 🌿 Estrutura de Branches

### Branches Principais

- **`main`** (ou `master`)
  - Código em produção
  - Sempre estável e pronto para deploy
  - Protegida contra commits diretos
  - Cada commit aqui deve gerar uma tag de versão

- **`develop`**
  - Branch principal de desenvolvimento
  - Código que está sendo desenvolvido e testado
  - Branch base para novas funcionalidades
  - Merge de `feature/`, `release/` e `hotfix/`

### Branches de Suporte

- **`feature/nome-da-funcionalidade`**
  - Novas funcionalidades
  - Criada a partir de `develop`
  - Merge de volta para `develop` quando completa
  - Exemplo: `feature/adicionar-suporte-python`

- **`release/versao`**
  - Preparação para uma nova release
  - Criada a partir de `develop`
  - Apenas correções de bugs e ajustes finais
  - Merge para `main` e `develop` quando pronto
  - Exemplo: `release/v1.0.0`

- **`hotfix/nome-do-fix`**
  - Correções urgentes em produção
  - Criada a partir de `main`
  - Merge para `main` e `develop`
  - Exemplo: `hotfix/corrigir-bug-critico`

## 📋 Workflow Básico

### 1. Iniciando o GitFlow

```bash
# Criar branch develop se não existir
git checkout -b develop
git push -u origin develop

# Configurar GitFlow (opcional, se usar git-flow extension)
git flow init
```

### 2. Desenvolvendo uma Nova Funcionalidade

```bash
# Criar branch de feature
git checkout develop
git pull origin develop
git checkout -b feature/minha-funcionalidade

# Desenvolver e commitar
git add .
git commit -m "feat: adiciona nova funcionalidade"

# Quando terminar, fazer merge em develop
git checkout develop
git pull origin develop
git merge feature/minha-funcionalidade
git push origin develop

# Deletar branch local (opcional)
git branch -d feature/minha-funcionalidade
```

### 3. Preparando uma Release

```bash
# Criar branch de release
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Fazer ajustes finais, atualizar versão, etc.
# Apenas correções de bugs, sem novas features

# Quando pronto, merge em main e develop
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags

git checkout develop
git merge release/v1.0.0
git push origin develop

# Deletar branch de release
git branch -d release/v1.0.0
```

### 4. Correção Urgente (Hotfix)

```bash
# Criar branch de hotfix a partir de main
git checkout main
git pull origin main
git checkout -b hotfix/corrigir-bug-critico

# Corrigir o bug
git add .
git commit -m "fix: corrige bug crítico"

# Merge em main e develop
git checkout main
git merge hotfix/corrigir-bug-critico
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin main --tags

git checkout develop
git merge hotfix/corrigir-bug-critico
git push origin develop

# Deletar branch de hotfix
git branch -d hotfix/corrigir-bug-critico
```

## 🔖 Convenções de Commit

Seguimos o padrão **Conventional Commits**:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Mudanças na documentação
- `style:` Formatação, ponto e vírgula faltando, etc
- `refactor:` Refatoração de código
- `test:` Adicionar ou corrigir testes
- `chore:` Mudanças em build, dependências, etc

**Exemplos:**
```
feat: adiciona suporte para Python
fix: corrige erro na ordenação de nós
docs: atualiza README com instruções de instalação
refactor: melhora estrutura do generator
```

## 📝 Scripts Auxiliares

Veja a pasta `scripts/` para scripts que facilitam o uso do GitFlow:

- `scripts/new-feature.sh` - Cria nova branch de feature
- `scripts/new-release.sh` - Cria nova branch de release
- `scripts/new-hotfix.sh` - Cria nova branch de hotfix
- `scripts/finish-feature.sh` - Finaliza e merge feature
- `scripts/finish-release.sh` - Finaliza e merge release
- `scripts/finish-hotfix.sh` - Finaliza e merge hotfix

## 🚀 Setup Inicial

### 1. Criar branch develop

```bash
git checkout -b develop
git push -u origin develop
```

### 2. Configurar proteção de branches (GitHub/GitLab)

- Proteger `main` e `develop` contra commits diretos
- Exigir Pull Requests para merge
- Exigir revisão de código (opcional)

### 3. Configurar Git Hooks (opcional)

```bash
# Instalar hooks de pré-commit
cp scripts/git-hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

## 📊 Visualização do Fluxo

```
main     ●────────●────────●────────●────────● (tags: v1.0.0, v1.0.1)
          \      /         \      /
           \    /           \    /
develop     ●──●──●──●──●──●──●──●──●
             \    /  \    /
              \  /    \  /
feature/      ●──●    ●──●
```

## ✅ Checklist para Pull Requests

Antes de fazer merge:

- [ ] Código segue os padrões do projeto
- [ ] Testes passam (`python src/test.py`)
- [ ] Documentação atualizada (se necessário)
- [ ] Commits seguem convenção (feat:, fix:, etc)
- [ ] Branch atualizada com develop
- [ ] Sem conflitos

## 🔗 Referências

- [GitFlow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

