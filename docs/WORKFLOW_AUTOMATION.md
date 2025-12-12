# Automação do Workflow - GitHub Pages

Este documento explica como funciona a automação que atualiza a documentação do GitHub Pages quando arquivos `.md` da raiz são alterados.

## 🔄 Como Funciona

### Fluxo Automatizado

1. **Detecção de Mudanças**
   - O workflow monitora arquivos `.md` na raiz do projeto
   - Especificamente monitora os arquivos mapeados:
     - `EXEMPLO_USO.md`
     - `ENV_SETUP.md`
     - `CONTRIBUTING.md`
     - `GITFLOW.md`
     - `TESTES.md`
     - `CHANGELOG.md`
     - `EXEMPLO_AI_AGENT.md`
     - `EXEMPLO_CONSTRUTOR_CREDENCIAIS.md`

2. **Atualização Automática**
   - Quando um arquivo mapeado é alterado, o script `copy-docs-to-jekyll.py` é executado
   - O script copia o conteúdo atualizado para os arquivos correspondentes em `docs/pt/`
   - Preserva o front matter (metadados) dos arquivos Jekyll

3. **Commit Automático**
   - Se houver mudanças, um commit é feito automaticamente
   - Mensagem: `docs: atualiza documentação em português a partir dos arquivos .md da raiz`
   - Tag `[skip ci]` evita loops infinitos de workflows

4. **Build e Deploy**
   - Após atualizar a documentação, o Jekyll faz o build
   - O site é publicado automaticamente no GitHub Pages

## 📋 Arquivos Monitorados

O workflow é acionado quando há mudanças em:

- `docs/**` - Qualquer arquivo na pasta docs
- `*.md` - Qualquer arquivo `.md` na raiz
- `.github/workflows/pages.yml` - O próprio workflow
- `scripts/copy-docs-to-jekyll.py` - O script de cópia

## 🔧 Configuração

### Permissões Necessárias

O workflow precisa de permissões de escrita (`contents: write`) para:
- Fazer commit das atualizações automáticas
- Fazer push das mudanças

### Token de Acesso

O workflow usa `${{ secrets.GITHUB_TOKEN }}` que é fornecido automaticamente pelo GitHub Actions.

## 📝 Exemplo de Uso

### Cenário 1: Atualizar EXEMPLO_USO.md

1. Você edita `EXEMPLO_USO.md` na raiz do projeto
2. Faz commit e push:
   ```bash
   git add EXEMPLO_USO.md
   git commit -m "docs: atualiza guia de uso"
   git push
   ```

3. O workflow detecta a mudança
4. Executa `copy-docs-to-jekyll.py`
5. Atualiza `docs/pt/usage.md` automaticamente
6. Faz commit da atualização
7. Faz build e deploy do GitHub Pages

### Cenário 2: Atualizar Documentação Diretamente

Se você editar diretamente arquivos em `docs/pt/` ou `docs/en/`:
- O workflow também será acionado
- Mas não executará o script de cópia (não há arquivo mapeado alterado)
- Apenas fará o build e deploy normalmente

## ⚙️ Detalhes Técnicos

### Verificação de Mudanças

O workflow usa `git diff` para detectar quais arquivos foram alterados:

```bash
git diff --name-only ${{ github.event.before }} ${{ github.sha }}
```

### Execução Condicional

O script só é executado se:
- Um arquivo `.md` mapeado foi alterado
- O workflow não está sendo executado por um commit automático (`[skip ci]`)

### Prevenção de Loops

- Commits automáticos incluem `[skip ci]` na mensagem
- Isso evita que o workflow seja acionado novamente pelo commit automático

## 🐛 Troubleshooting

### O workflow não está atualizando a documentação

**Possíveis causas:**
1. O arquivo alterado não está na lista de arquivos mapeados
2. O commit inclui `[skip ci]` (isso é esperado para commits automáticos)
3. Erro no script Python

**Solução:**
- Verifique os logs do workflow em **Actions**
- Verifique se o arquivo está no mapeamento em `scripts/copy-docs-to-jekyll.py`

### Erro de permissão

**Causa:** O workflow não tem permissão para fazer commit/push

**Solução:**
- Verifique se `contents: write` está configurado no workflow
- Verifique se o token `GITHUB_TOKEN` está disponível

### Commit automático não está sendo feito

**Possíveis causas:**
1. Não há mudanças reais (conteúdo idêntico)
2. Erro no script Python
3. Problema com git config

**Solução:**
- Verifique os logs do workflow
- Execute o script localmente: `python scripts/copy-docs-to-jekyll.py`

## 📚 Arquivos Relacionados

- `.github/workflows/pages.yml` - Workflow do GitHub Actions
- `scripts/copy-docs-to-jekyll.py` - Script de cópia
- `docs/_config.yml` - Configuração do Jekyll

## 💡 Dicas

1. **Sempre edite os arquivos originais** na raiz do projeto
2. **Deixe o workflow fazer o trabalho** de atualizar a documentação Jekyll
3. **Verifique os logs** se algo não funcionar como esperado
4. **Use `[skip ci]`** apenas em commits automáticos (já incluído automaticamente)

---

**Última atualização:** 2024

