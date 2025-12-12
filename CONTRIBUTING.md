# Guia de Contribuição - n8ncoding

Este guia detalha como contribuir para o projeto **n8ncoding** seguindo o padrão **GitFlow**.

## 📚 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração Inicial](#configuração-inicial)
3. [Fluxo de Trabalho GitFlow](#fluxo-de-trabalho-gitflow)
4. [Cenários Práticos](#cenários-práticos)
5. [Convenções de Commit](#convenções-de-commit)
6. [Checklist de Contribuição](#checklist-de-contribuição)
7. [Resolução de Conflitos](#resolução-de-conflitos)
8. [FAQ](#faq)

---

## 🎯 Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ Git instalado (versão 2.20+)
- ✅ Python 3.8+ instalado
- ✅ Acesso ao repositório (fork ou permissão de escrita)
- ✅ Conhecimento básico de Git (branch, commit, merge)

---

## ⚙️ Configuração Inicial

### 1. Fork e Clone do Repositório

```bash
# 1. Faça fork do repositório no GitHub
# 2. Clone seu fork localmente
git clone https://github.com/SEU-USUARIO/n8ncoding.git
cd n8ncoding

# 3. Adicione o repositório original como upstream
git remote add upstream https://github.com/JhefersonBR/n8ncoding.git

# 4. Verifique os remotes
git remote -v
# Deve mostrar:
# origin    https://github.com/SEU-USUARIO/n8ncoding.git (fetch)
# origin    https://github.com/SEU-USUARIO/n8ncoding.git (push)
# upstream  https://github.com/JhefersonBR/n8ncoding.git (fetch)
# upstream  https://github.com/JhefersonBR/n8ncoding.git (push)
```

### 2. Configurar Branches Principais

```bash
# Certifique-se de estar na branch main
git checkout main

# Atualize a branch main
git pull upstream main

# Crie/atualize a branch develop
git checkout -b develop
git pull upstream develop
git push -u origin develop
```

### 3. Configurar Ambiente de Desenvolvimento

```bash
# Instale as dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

---

## 🔄 Fluxo de Trabalho GitFlow

### Visão Geral

```
main (produção)
  │
  ├── develop (desenvolvimento)
  │     │
  │     ├── feature/nova-funcionalidade
  │     ├── feature/outra-funcionalidade
  │     │
  │     └── release/v1.0.0
  │
  └── hotfix/correcao-urgente
```

### Tipos de Branches

| Tipo | Origem | Destino | Quando Usar |
|------|--------|---------|-------------|
| `feature/*` | `develop` | `develop` | Nova funcionalidade |
| `release/*` | `develop` | `main` + `develop` | Preparar nova versão |
| `hotfix/*` | `main` | `main` + `develop` | Correção urgente em produção |

---

## 🚀 Cenários Práticos

### Cenário 1: Desenvolvendo uma Nova Funcionalidade

**Situação:** Você quer adicionar suporte para o nó "Send Email" do n8n.

#### Passo 1: Criar Branch de Feature

**Opção A - Usando Script (Recomendado):**

```bash
# Linux/Mac
./scripts/new-feature.sh suporte-send-email

# Windows PowerShell
.\scripts\new-feature.ps1 suporte-send-email
```

**Opção B - Manual:**

```bash
# 1. Certifique-se de estar em develop e atualizado
git checkout develop
git pull upstream develop

# 2. Crie a branch de feature
git checkout -b feature/suporte-send-email

# 3. Envie para seu fork (opcional, mas recomendado)
git push -u origin feature/suporte-send-email
```

#### Passo 2: Desenvolver a Funcionalidade

```bash
# Faça suas alterações nos arquivos
# Exemplo: criar templates/nodes/sendEmail.xml

# Adicione os arquivos
git add templates/nodes/sendEmail.xml
git add src/node_mapper.py  # se modificou

# Faça commit seguindo a convenção
git commit -m "feat: adiciona template para nó Send Email

- Cria template sendEmail.xml
- Adiciona mapeamento no node_mapper.py
- Suporta parâmetros: to, subject, body"
```

**💡 Dica:** Faça commits pequenos e frequentes. É melhor ter vários commits pequenos do que um grande.

#### Passo 3: Manter Branch Atualizada

```bash
# Periodicamente, atualize sua branch com develop
git checkout develop
git pull upstream develop
git checkout feature/suporte-send-email
git merge develop
# Ou use rebase (mais limpo, mas requer cuidado):
# git rebase develop
```

#### Passo 4: Testar Localmente

```bash
# Execute os testes
python tests/test.py

# Teste manualmente
python src/main.py
# Selecione um workflow que usa Send Email
# Verifique se o código gerado está correto
```

#### Passo 5: Finalizar Feature

**Opção A - Usando Script:**

```bash
# Linux/Mac
./scripts/finish-feature.sh suporte-send-email

# Windows PowerShell
.\scripts\finish-feature.ps1 suporte-send-email
```

**Opção B - Manual:**

```bash
# 1. Certifique-se de que tudo está commitado
git status

# 2. Atualize develop
git checkout develop
git pull upstream develop

# 3. Merge da feature
git merge feature/suporte-send-email

# 4. Resolva conflitos se houver (veja seção abaixo)

# 5. Envie para upstream
git push upstream develop

# 6. Delete a branch local (opcional)
git branch -d feature/suporte-send-email

# 7. Delete a branch remota (se criou)
git push origin --delete feature/suporte-send-email
```

#### Passo 6: Criar Pull Request (se usando fork)

1. Vá para o GitHub
2. Clique em "New Pull Request"
3. Selecione `develop` como base
4. Selecione sua branch `feature/suporte-send-email`
5. Preencha o template do PR
6. Aguarde revisão e aprovação

---

### Cenário 2: Preparando uma Release

**Situação:** O projeto está pronto para a versão 1.0.0.

#### Passo 1: Criar Branch de Release

```bash
# Opção A - Script
./scripts/new-release.sh 1.0.0

# Opção B - Manual
git checkout develop
git pull upstream develop
git checkout -b release/v1.0.0
```

#### Passo 2: Preparar Release

```bash
# 1. Atualize CHANGELOG.md
# 2. Atualize versão em arquivos de configuração
# 3. Faça ajustes finais (apenas correções de bugs!)

# Exemplo: atualizar versão
git add CHANGELOG.md
git commit -m "chore: atualiza versão para 1.0.0

- Atualiza CHANGELOG.md
- Marca versão 1.0.0 como estável"
```

**⚠️ Importante:** Em branches de release, **NÃO** adicione novas funcionalidades. Apenas:
- Correções de bugs
- Atualização de versão
- Atualização de documentação
- Ajustes finais

#### Passo 3: Finalizar Release

```bash
# Opção A - Script
./scripts/finish-release.sh 1.0.0

# Opção B - Manual
# 1. Merge para main
git checkout main
git pull upstream main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push upstream main --tags

# 2. Merge para develop
git checkout develop
git pull upstream develop
git merge release/v1.0.0
git push upstream develop

# 3. Delete branch de release
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0  # se existir no seu fork
```

---

### Cenário 3: Correção Urgente (Hotfix)

**Situação:** Há um bug crítico em produção que precisa ser corrigido urgentemente.

#### Passo 1: Criar Branch de Hotfix

```bash
# Opção A - Script
./scripts/new-hotfix.sh corrigir-bug-critico

# Opção B - Manual
git checkout main
git pull upstream main
git checkout -b hotfix/corrigir-bug-critico
```

#### Passo 2: Corrigir o Bug

```bash
# Faça a correção necessária
# Exemplo: corrigir bug na ordenação de nós

git add src/generator.py
git commit -m "fix: corrige bug na ordenação topológica de nós

- Corrige erro quando nó não tem conexões
- Adiciona validação para evitar IndexError"
```

#### Passo 3: Testar

```bash
# Teste a correção extensivamente
python tests/test.py
python src/main.py  # teste manual
```

#### Passo 4: Finalizar Hotfix

```bash
# Opção A - Script
./scripts/finish-hotfix.sh corrigir-bug-critico

# Opção B - Manual
# 1. Merge para main
git checkout main
git pull upstream main
git merge hotfix/corrigir-bug-critico
git tag -a v1.0.1 -m "Hotfix v1.0.1 - Corrige bug crítico"
git push upstream main --tags

# 2. Merge para develop
git checkout develop
git pull upstream develop
git merge hotfix/corrigir-bug-critico
git push upstream develop

# 3. Delete branch
git branch -d hotfix/corrigir-bug-critico
```

---

## 📝 Convenções de Commit

Seguimos o padrão **Conventional Commits**. Formato:

```
<tipo>(<escopo>): <descrição curta>

<corpo detalhado (opcional)>

<rodapé (opcional)>
```

### Tipos de Commit

| Tipo | Quando Usar | Exemplo |
|------|-------------|---------|
| `feat` | Nova funcionalidade | `feat: adiciona suporte para Python` |
| `fix` | Correção de bug | `fix: corrige erro na ordenação de nós` |
| `docs` | Documentação | `docs: atualiza guia de contribuição` |
| `style` | Formatação | `style: corrige indentação em generator.py` |
| `refactor` | Refatoração | `refactor: melhora estrutura do NodeMapper` |
| `test` | Testes | `test: adiciona testes para ExpressionParser` |
| `chore` | Tarefas de manutenção | `chore: atualiza dependências` |
| `perf` | Melhoria de performance | `perf: otimiza ordenação topológica` |

### Exemplos de Commits

#### ✅ Bom

```bash
git commit -m "feat: adiciona suporte para múltiplas linguagens

- Implementa templates para Python e JavaScript
- Adiciona LanguageSelector para escolha interativa
- Atualiza generator para suportar múltiplas linguagens
- Cria classes de credenciais para cada linguagem"
```

```bash
git commit -m "fix: corrige caminho relativo para credenciais em subpastas

O caminho relativo estava incorreto quando workflows estavam em subpastas.
Agora calcula corretamente a profundidade e gera o caminho adequado."
```

#### ❌ Ruim

```bash
git commit -m "mudanças"
git commit -m "fix bug"
git commit -m "WIP"
git commit -m "atualiza arquivos"
```

### Regras de Ouro

1. **Uma funcionalidade = um commit** (quando possível)
2. **Mensagem clara e descritiva**
3. **Corpo explicativo** para mudanças complexas
4. **Use o presente do indicativo**: "adiciona" não "adicionou"
5. **Primeira linha com até 50 caracteres** (ideal)
6. **Corpo com até 72 caracteres por linha**

---

## ✅ Checklist de Contribuição

Antes de fazer merge ou criar PR, verifique:

### Código

- [ ] Código segue os padrões do projeto
- [ ] Sem erros de lint (`python -m flake8 src/` ou equivalente)
- [ ] Testes passam (`python tests/test.py`)
- [ ] Testes manuais realizados
- [ ] Sem código comentado ou debug

### Git

- [ ] Commits seguem convenção (feat:, fix:, etc.)
- [ ] Branch atualizada com develop/main
- [ ] Sem conflitos
- [ ] Mensagens de commit claras e descritivas

### Documentação

- [ ] README atualizado (se necessário)
- [ ] CHANGELOG atualizado (se necessário)
- [ ] Comentários no código (se código complexo)
- [ ] Documentação de novas funcionalidades

### Funcionalidade

- [ ] Funcionalidade testada localmente
- [ ] Casos de uso testados
- [ ] Sem regressões introduzidas
- [ ] Compatível com versões anteriores (se aplicável)

---

## 🔧 Resolução de Conflitos

### Durante Merge

Se houver conflitos ao fazer merge:

```bash
# 1. Identifique os arquivos com conflito
git status

# 2. Abra os arquivos e procure por marcadores:
# <<<<<<< HEAD
# código da branch atual
# =======
# código da branch sendo mergeada
# >>>>>>> feature/nome-da-feature

# 3. Resolva manualmente, removendo os marcadores
# 4. Adicione os arquivos resolvidos
git add arquivo-resolvido.py

# 5. Complete o merge
git commit -m "merge: resolve conflitos com develop"
```

### Durante Rebase

```bash
# Se usar rebase e houver conflitos:
git rebase develop

# Resolva conflitos em cada commit
# Após resolver:
git add arquivo-resolvido.py
git rebase --continue

# Se quiser cancelar:
git rebase --abort
```

---

## 🎓 Exemplos Completos

### Exemplo Completo: Adicionar Novo Template de Nó

```bash
# 1. Criar feature
git checkout develop
git pull upstream develop
git checkout -b feature/template-code-node

# 2. Criar template
# Criar arquivo: templates/nodes/code.xml
cat > templates/nodes/code.xml << 'EOF'
<node>
    <name>code</name>
    <method>
        <![CDATA[
private function {{method_name}}(): void
{
    // Código customizado do n8n
    {{generated_code}}
}
        ]]>
    </method>
</node>
EOF

# 3. Adicionar suporte no node_mapper.py
# (editar arquivo manualmente)

# 4. Commit
git add templates/nodes/code.xml src/node_mapper.py
git commit -m "feat: adiciona template para nó Code

- Cria template code.xml
- Adiciona mapeamento no node_mapper.py
- Suporta código JavaScript customizado do n8n"

# 5. Testar
python tests/test.py
python src/main.py  # testar com workflow que usa Code node

# 6. Atualizar branch
git checkout develop
git pull upstream develop
git checkout feature/template-code-node
git merge develop

# 7. Finalizar
git checkout develop
git merge feature/template-code-node
git push upstream develop
git branch -d feature/template-code-node
```

### Exemplo Completo: Corrigir Bug

```bash
# 1. Criar hotfix
git checkout main
git pull upstream main
git checkout -b hotfix/corrigir-ordenacao-nos

# 2. Identificar e corrigir bug
# Bug: IndexError quando nó não tem conexões
# Arquivo: src/generator.py, linha 145

# 3. Corrigir
# Adicionar validação: if not connections: continue

# 4. Commit
git add src/generator.py
git commit -m "fix: corrige IndexError na ordenação de nós

- Adiciona validação para nós sem conexões
- Evita IndexError quando connections está vazio
- Adiciona teste para caso edge"

# 5. Testar
python tests/test.py
# Criar teste específico para o bug

# 6. Finalizar hotfix
git checkout main
git merge hotfix/corrigir-ordenacao-nos
git tag -a v1.0.1 -m "Hotfix v1.0.1 - Corrige IndexError"
git push upstream main --tags

git checkout develop
git merge hotfix/corrigir-ordenacao-nos
git push upstream develop

git branch -d hotfix/corrigir-ordenacao-nos
```

---

## ❓ FAQ

### Posso fazer commit direto em develop?

**Não recomendado.** Use branches de feature para isolar mudanças e facilitar revisão.

### Quando usar rebase vs merge?

- **Merge**: Preserva histórico completo, mais seguro
- **Rebase**: Histórico linear, mais limpo, mas requer cuidado

**Recomendação:** Use merge para começar. Rebase apenas se souber o que está fazendo.

### Como atualizar meu fork?

```bash
git checkout main
git pull upstream main
git push origin main

git checkout develop
git pull upstream develop
git push origin develop
```

### E se eu cometer um erro no commit?

```bash
# Se ainda não fez push:
git commit --amend -m "nova mensagem"

# Se já fez push (cuidado!):
git commit --amend -m "nova mensagem"
git push --force-with-lease origin nome-da-branch
```

### Como ver o histórico de uma branch?

```bash
# Ver commits da branch
git log feature/nome-da-feature

# Ver diferença com develop
git log develop..feature/nome-da-feature

# Ver arquivos modificados
git diff develop..feature/nome-da-feature
```

### Posso deletar uma branch depois do merge?

**Sim!** Após fazer merge, você pode deletar a branch:

```bash
# Deletar local
git branch -d feature/nome-da-feature

# Deletar remota
git push origin --delete feature/nome-da-feature
```

---

## 📚 Recursos Adicionais

- [GitFlow Workflow - Atlassian](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

## 🤝 Precisa de Ajuda?

- Abra uma [Issue](https://github.com/JhefersonBR/n8ncoding/issues)
- Entre em contato com os mantenedores
- Consulte a documentação do projeto

---

**Última atualização:** 2024

