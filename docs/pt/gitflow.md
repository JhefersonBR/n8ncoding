---
layout: page
title: Guia GitFlow
lang: pt
ref: gitflow
permalink: /pt/gitflow/
---

# GitFlow - Guia Completo para n8ncoding

Este documento fornece um guia detalhado sobre como usar o GitFlow no projeto **n8ncoding**.

## 📋 Índice

1. [O que é GitFlow?](#o-que-é-gitflow)
2. [Estrutura de Branches](#estrutura-de-branches)
3. [Fluxo de Trabalho Detalhado](#fluxo-de-trabalho-detalhado)
4. [Scripts Auxiliares](#scripts-auxiliares)
5. [Exemplos Práticos Passo a Passo](#exemplos-práticos-passo-a-passo)
6. [Boas Práticas](#boas-práticas)
7. [Troubleshooting](#troubleshooting)

---

## 🌿 O que é GitFlow?

GitFlow é um modelo de branching para Git que organiza o desenvolvimento em diferentes tipos de branches, cada uma com um propósito específico. Isso facilita o gerenciamento de releases, features e hotfixes.

### Vantagens

- ✅ Histórico limpo e organizado
- ✅ Facilita releases e versionamento
- ✅ Isola features em desenvolvimento
- ✅ Permite correções urgentes sem afetar desenvolvimento
- ✅ Facilita colaboração em equipe

---

## 🌳 Estrutura de Branches

### Branches Principais (Permanentes)

#### `main` (ou `master`)

- **Propósito:** Código em produção
- **Características:**
  - Sempre estável e testado
  - Cada commit deve gerar uma tag de versão
  - Protegida contra commits diretos
  - Histórico linear (apenas merges de release/hotfix)

#### `develop`

- **Propósito:** Branch principal de desenvolvimento
- **Características:**
  - Código que está sendo desenvolvido e testado
  - Branch base para novas funcionalidades
  - Recebe merges de `feature/*`, `release/*` e `hotfix/*`
  - Pode ter commits diretos (não recomendado)

### Branches de Suporte (Temporárias)

#### `feature/*`

- **Origem:** `develop`
- **Destino:** `develop`
- **Propósito:** Desenvolver novas funcionalidades
- **Exemplos:**
  - `feature/suporte-python`
  - `feature/template-code-node`
  - `feature/melhorar-parser-expressoes`

#### `release/*`

- **Origem:** `develop`
- **Destino:** `main` + `develop`
- **Propósito:** Preparar uma nova versão para produção
- **Características:**
  - Apenas correções de bugs
  - Atualização de versão
  - Ajustes finais
  - **NÃO** adiciona novas features
- **Exemplos:**
  - `release/v1.0.0`
  - `release/v1.1.0`

#### `hotfix/*`

- **Origem:** `main`
- **Destino:** `main` + `develop`
- **Propósito:** Correções urgentes em produção
- **Características:**
  - Criada a partir de `main` (código em produção)
  - Correções críticas que não podem esperar
  - Merge imediato para `main` e `develop`
- **Exemplos:**
  - `hotfix/corrigir-bug-critico`
  - `hotfix/vulnerabilidade-seguranca`

---

## 🔄 Fluxo de Trabalho Detalhado

### Visualização do Fluxo

```
main     ●────────●────────●────────●────────● (tags: v1.0.0, v1.0.1)
          \      /         \      /
           \    /           \    /
develop     ●──●──●──●──●──●──●──●──●
             \    /  \    /     \
              \  /    \  /       \
feature/      ●──●    ●──●       ●──●
release/                    ●──●
hotfix/                              ●──●
```

### Ciclo de Vida de uma Feature

```
1. Criar branch: develop → feature/nome
2. Desenvolver: commits na feature
3. Atualizar: merge develop → feature (periodicamente)
4. Finalizar: merge feature → develop
5. Deletar: branch feature (após merge)
```

### Ciclo de Vida de uma Release

```
1. Criar branch: develop → release/v1.0.0
2. Preparar: ajustes finais, versão, changelog
3. Finalizar: merge release → main (tag) + develop
4. Deletar: branch release
```

### Ciclo de Vida de um Hotfix

```
1. Criar branch: main → hotfix/nome
2. Corrigir: commit da correção
3. Finalizar: merge hotfix → main (tag) + develop
4. Deletar: branch hotfix
```

---

## 🛠️ Scripts Auxiliares

O projeto inclui scripts para facilitar o uso do GitFlow.

### Windows (PowerShell)

#### Criar Nova Feature

```powershell
# Sintaxe
.\scripts\new-feature.ps1 nome-da-feature

# Exemplo
.\scripts\new-feature.ps1 suporte-python

# O que faz:
# 1. Atualiza develop
# 2. Cria branch feature/suporte-python
# 3. Faz checkout para a nova branch
```

#### Finalizar Feature

```powershell
# Sintaxe
.\scripts\finish-feature.ps1 nome-da-feature

# Exemplo
.\scripts\finish-feature.ps1 suporte-python

# O que faz:
# 1. Atualiza develop
# 2. Faz merge da feature em develop
# 3. Faz push para origin
# 4. Deleta branch local (opcional)
```

#### Criar Release

```powershell
.\scripts\new-release.ps1 1.0.0
# Cria branch release/v1.0.0
```

#### Finalizar Release

```powershell
.\scripts\finish-release.ps1 1.0.0
# Faz merge em main e develop, cria tag, deleta branch
```

#### Criar Hotfix

```powershell
.\scripts\new-hotfix.ps1 corrigir-bug
# Cria branch hotfix/corrigir-bug a partir de main
```

#### Finalizar Hotfix

```powershell
.\scripts\finish-hotfix.ps1 corrigir-bug
# Faz merge em main e develop, cria tag, deleta branch
```

### Linux/Mac (Bash)

```bash
# Feature
./scripts/new-feature.sh nome-da-feature
./scripts/finish-feature.sh nome-da-feature

# Release
./scripts/new-release.sh 1.0.0
./scripts/finish-release.sh 1.0.0

# Hotfix
./scripts/new-hotfix.sh nome-do-hotfix
./scripts/finish-hotfix.sh nome-do-hotfix
```

---

## 📖 Exemplos Práticos Passo a Passo

### Exemplo 1: Adicionar Suporte para Python

#### Passo 1: Preparar Ambiente

```bash
# Certifique-se de estar atualizado
git checkout develop
git pull upstream develop
```

#### Passo 2: Criar Branch de Feature

```bash
# Usando script (recomendado)
./scripts/new-feature.sh suporte-python

# Ou manualmente
git checkout -b feature/suporte-python
```

#### Passo 3: Desenvolver

```bash
# Criar template de linguagem Python
# Arquivo: templates/languages/python.xml

# Criar templates de nós Python
# Arquivo: templates/nodes/python/aiAgent.xml
# Arquivo: templates/nodes/python/httpRequest.xml
# etc.

# Atualizar generator.py para suportar Python
# Atualizar node_mapper.py
```

#### Passo 4: Commits Incrementais

```bash
# Commit 1: Template de linguagem
git add templates/languages/python.xml
git commit -m "feat: adiciona template de linguagem Python

- Cria template base para classes Python
- Suporta type hints e docstrings
- Compatível com Python 3.8+"

# Commit 2: Templates de nós
git add templates/nodes/python/
git commit -m "feat: adiciona templates de nós Python

- Cria templates para aiAgent, httpRequest, set, function, if
- Segue padrões PEP 8
- Inclui tratamento de erros"

# Commit 3: Atualizar gerador
git add src/generator.py src/node_mapper.py
git commit -m "feat: atualiza gerador para suportar Python

- Adiciona lógica de geração Python
- Atualiza mapeamento de nós
- Suporta múltiplas linguagens"
```

#### Passo 5: Manter Branch Atualizada

```bash
# Periodicamente, atualize com develop
git checkout develop
git pull upstream develop
git checkout feature/suporte-python
git merge develop
# Resolva conflitos se houver
```

#### Passo 6: Testar

```bash
# Execute testes
python tests/test.py

# Teste manual
python src/main.py
# Selecione um workflow
# Escolha Python como linguagem
# Verifique o código gerado
```

#### Passo 7: Finalizar Feature

```bash
# Usando script
./scripts/finish-feature.sh suporte-python

# Ou manualmente
git checkout develop
git pull upstream develop
git merge feature/suporte-python
git push upstream develop
git branch -d feature/suporte-python
```

---

### Exemplo 2: Preparar Release v1.0.0

#### Passo 1: Criar Branch de Release

```bash
git checkout develop
git pull upstream develop
git checkout -b release/v1.0.0
```

#### Passo 2: Preparar Release

```bash
# 1. Atualizar CHANGELOG.md
# Adicione todas as mudanças desde última release

# 2. Atualizar versão em arquivos
# Exemplo: config/settings.json, README.md

# 3. Fazer ajustes finais
# Apenas correções de bugs, sem novas features!

git add CHANGELOG.md
git commit -m "chore: prepara release v1.0.0

- Atualiza CHANGELOG.md com todas as mudanças
- Marca versão 1.0.0 como estável
- Atualiza documentação"
```

#### Passo 3: Testar Release

```bash
# Execute todos os testes
python tests/test.py

# Teste de integração completo
python src/main.py
# Teste com diferentes workflows
# Teste com diferentes linguagens
```

#### Passo 4: Finalizar Release

```bash
# Merge para main
git checkout main
git pull upstream main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0

- Suporte completo para PHP, Python e JavaScript
- Templates para principais tipos de nós
- Sistema de credenciais
- Seleção múltipla de linguagens"
git push upstream main --tags

# Merge para develop
git checkout develop
git pull upstream develop
git merge release/v1.0.0
git push upstream develop

# Deletar branch
git branch -d release/v1.0.0
```

---

### Exemplo 3: Hotfix Urgente

#### Passo 1: Identificar Bug em Produção

```bash
# Bug reportado: IndexError ao processar workflows sem conexões
# Versão afetada: v1.0.0 (em produção)
```

#### Passo 2: Criar Hotfix

```bash
git checkout main
git pull upstream main
git checkout -b hotfix/corrigir-indexerror-ordencao
```

#### Passo 3: Corrigir Bug

```bash
# Arquivo: src/generator.py
# Linha 145: IndexError quando connections está vazio

# Adicionar validação:
# if not connections or len(connections) == 0:
#     continue

git add src/generator.py
git commit -m "fix: corrige IndexError na ordenação de nós

- Adiciona validação para nós sem conexões
- Evita IndexError quando connections está vazio
- Adiciona tratamento para casos edge"
```

#### Passo 4: Testar

```bash
# Criar teste específico
python tests/test.py

# Testar com workflow sem conexões
python src/main.py
```

#### Passo 5: Finalizar Hotfix

```bash
# Merge para main
git checkout main
git merge hotfix/corrigir-indexerror-ordencao
git tag -a v1.0.1 -m "Hotfix v1.0.1 - Corrige IndexError na ordenação"
git push upstream main --tags

# Merge para develop
git checkout develop
git merge hotfix/corrigir-indexerror-ordencao
git push upstream develop

# Deletar branch
git branch -d hotfix/corrigir-indexerror-ordencao
```

---

## ✅ Boas Práticas

### Commits

1. **Faça commits pequenos e frequentes**
   ```bash
   # ✅ Bom: commits pequenos e focados
   git commit -m "feat: adiciona template sendEmail"
   git commit -m "feat: adiciona mapeamento no node_mapper"
   
   # ❌ Ruim: commit gigante
   git commit -m "feat: adiciona suporte completo para email"
   ```

2. **Use mensagens descritivas**
   ```bash
   # ✅ Bom
   git commit -m "fix: corrige erro ao processar expressões n8n vazias"
   
   # ❌ Ruim
   git commit -m "fix bug"
   ```

3. **Siga a convenção de commits**
   ```bash
   # ✅ Bom
   git commit -m "feat: adiciona suporte para Python"
   git commit -m "fix: corrige caminho relativo para credenciais"
   
   # ❌ Ruim
   git commit -m "adiciona python"
   git commit -m "corrige bug"
   ```

### Branches

1. **Mantenha branches atualizadas**
   ```bash
   # Periodicamente, atualize sua branch com develop
   git checkout develop
   git pull upstream develop
   git checkout feature/sua-feature
   git merge develop
   ```

2. **Delete branches após merge**
   ```bash
   # Após fazer merge, delete a branch
   git branch -d feature/sua-feature
   git push origin --delete feature/sua-feature
   ```

3. **Use nomes descritivos**
   ```bash
   # ✅ Bom
   feature/suporte-python
   feature/template-send-email
   hotfix/corrigir-bug-ordencao
   
   # ❌ Ruim
   feature/teste
   feature/novo
   hotfix/bug
   ```

### Pull Requests

1. **Crie PRs pequenos e focados**
   - Um PR por feature/fix
   - Fácil de revisar
   - Menos conflitos

2. **Descreva bem o PR**
   - O que foi feito?
   - Por que foi feito?
   - Como testar?

3. **Mantenha PR atualizado**
   - Atualize com develop antes de pedir revisão
   - Resolva conflitos rapidamente

---

## 🔧 Troubleshooting

### Problema: Conflitos ao fazer merge

**Solução:**
```bash
# 1. Identifique os arquivos com conflito
git status

# 2. Abra cada arquivo e resolva manualmente
# Procure por: <<<<<<< HEAD

# 3. Após resolver, adicione os arquivos
git add arquivo-resolvido.py

# 4. Complete o merge
git commit -m "merge: resolve conflitos com develop"
```

### Problema: Commit na branch errada

**Solução:**
```bash
# Se ainda não fez push:
git reset HEAD~1  # Remove último commit, mantém mudanças
git checkout branch-correta
git add .
git commit -m "mensagem"

# Se já fez push (cuidado!):
git checkout branch-correta
git cherry-pick commit-hash
git checkout branch-errada
git reset --hard HEAD~1
git push --force-with-lease
```

### Problema: Branch desatualizada

**Solução:**
```bash
# Atualize sua branch com develop
git checkout develop
git pull upstream develop
git checkout sua-branch
git merge develop
# Ou use rebase (mais limpo):
git rebase develop
```

### Problema: Tag já existe

**Solução:**
```bash
# Se tag já existe localmente:
git tag -d v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"

# Se tag já existe no remoto:
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

---

## 📊 Resumo Visual

### Fluxo Completo

```
┌─────────────────────────────────────────────────────────┐
│                    DESENVOLVIMENTO                      │
└─────────────────────────────────────────────────────────┘

develop ──┐
          │
          ├──> feature/nova-funcionalidade ──┐
          │                                   │
          ├──> feature/outra-feature ────────┤
          │                                   │
          └──> feature/mais-uma ─────────────┤
                                             │
                                             ▼
                                          develop
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────┐
│                    PREPARAÇÃO RELEASE                    │
└─────────────────────────────────────────────────────────┘

                                          release/v1.0.0
                                             │
                                             │ (apenas bugs)
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────┐
│                      PRODUÇÃO                            │
└─────────────────────────────────────────────────────────┘

                                          main (v1.0.0)
                                             │
                                             │ (bug crítico)
                                             │
                                             ▼
                                          hotfix/bug
                                             │
                                             ▼
                                    main (v1.0.1) + develop
```

---

## 📚 Referências

- [GitFlow Workflow - Atlassian](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Documentation](https://git-scm.com/doc)

---

## 🤝 Precisa de Ajuda?

- Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para guia completo de contribuição
- Abra uma [Issue](https://github.com/JhefersonBR/n8ncoding/issues)
- Entre em contato com os mantenedores

---

**Última atualização:** 2024
