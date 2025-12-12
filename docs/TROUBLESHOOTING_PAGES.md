# Troubleshooting GitHub Pages

## Problema: Documentação não está visível no GitHub Pages

### Verificações Necessárias

#### 1. Verificar Configuração do GitHub Pages

1. Vá para **Settings** > **Pages** no repositório GitHub
2. Verifique se está configurado:
   - **Source:** Deve estar como **GitHub Actions** (não "Deploy from a branch")
   - Se não estiver, selecione **GitHub Actions** e salve

#### 2. Verificar se o Workflow Foi Executado

1. Vá para **Actions** no GitHub
2. Procure pelo workflow "Deploy GitHub Pages"
3. Verifique se foi executado e se passou com sucesso
4. Se falhou, verifique os logs para identificar o problema

#### 3. Verificar baseurl no _config.yml

O arquivo `docs/_config.yml` tem:
```yaml
baseurl: "/n8ncoding"
```

**Importante:** O `baseurl` deve corresponder ao nome do repositório.

- Se o repositório é `n8ncoding`, o baseurl deve ser `/n8ncoding`
- Se o repositório é outro nome, ajuste o baseurl

#### 4. Verificar URL do Repositório

A URL do GitHub Pages segue o padrão:
```
https://{username}.github.io/{repository-name}/
```

Para este projeto:
```
https://jhefersonbr.github.io/n8ncoding/
```

### Soluções Comuns

#### Problema: Workflow não executa

**Solução:**
- Verifique se o arquivo `.github/workflows/pages.yml` existe
- Verifique se está na branch `main` ou `develop`
- Faça um commit vazio para forçar execução:
  ```bash
  git commit --allow-empty -m "chore: trigger GitHub Pages workflow"
  git push
  ```

#### Problema: Build falha

**Solução:**
- Verifique os logs do workflow em **Actions**
- Erros comuns:
  - Gemfile faltando ou incorreto
  - Erros de sintaxe nos arquivos Markdown
  - Problemas com front matter do Jekyll

#### Problema: Página 404

**Solução:**
- Aguarde alguns minutos (pode levar até 10 minutos para aparecer)
- Verifique se o baseurl está correto
- Tente acessar diretamente:
  - `https://jhefersonbr.github.io/n8ncoding/en/`
  - `https://jhefersonbr.github.io/n8ncoding/pt/`

#### Problema: baseurl incorreto

**Solução:**
1. Edite `docs/_config.yml`
2. Ajuste o `baseurl` para corresponder ao nome do repositório
3. Faça commit e push
4. O workflow será executado automaticamente

### Testar Localmente

Para testar antes de fazer deploy:

```bash
cd docs
bundle install
bundle exec jekyll serve --baseurl /n8ncoding
```

Acesse: `http://localhost:4000/n8ncoding/`

### Verificar Status do Deploy

1. Vá para **Settings** > **Pages**
2. Verifique a seção "Build and deployment"
3. Deve mostrar: "Your site is published at..."
4. Clique no link para acessar

### Forçar Novo Deploy

Se necessário, você pode forçar um novo deploy:

1. Vá para **Actions**
2. Selecione o workflow "Deploy GitHub Pages"
3. Clique em "Run workflow"
4. Selecione a branch (main ou develop)
5. Clique em "Run"

---

**Última atualização:** 2024

