# Guia de Deploy - GitHub Pages

Este documento explica como configurar e fazer deploy da documentação no GitHub Pages.

## Configuração Inicial

### 1. Habilitar GitHub Pages

1. Vá para **Settings** > **Pages** no seu repositório GitHub
2. Em **Source**, selecione **GitHub Actions**
3. Salve as alterações

### 2. Verificar Workflow

O arquivo `.github/workflows/pages.yml` já está configurado para:
- Fazer deploy automaticamente quando arquivos em `docs/` são modificados
- Fazer deploy nas branches `main` e `develop`
- Usar Jekyll para gerar o site estático

### 3. Primeiro Deploy

Após fazer commit e push das alterações em `docs/`:

1. O GitHub Actions executará automaticamente
2. Você pode acompanhar o progresso em **Actions** no GitHub
3. Após o sucesso, a documentação estará disponível em:
   - `https://jhefersonbr.github.io/n8ncoding/` (redireciona para `/en/`)
   - `https://jhefersonbr.github.io/n8ncoding/en/` (Inglês - padrão)
   - `https://jhefersonbr.github.io/n8ncoding/pt/` (Português)

## Estrutura de URLs

- `/` → Redireciona para `/en/`
- `/en/` → Documentação em inglês (padrão)
- `/pt/` → Documentação em português
- `/en/installation/` → Página de instalação em inglês
- `/pt/installation/` → Página de instalação em português

## Testando Localmente

Antes de fazer commit, teste localmente:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Acesse `http://localhost:4000/n8ncoding/` para ver a documentação.

## Troubleshooting

### Erro: "Page build failed"

- Verifique se o `Gemfile` está correto
- Verifique se todos os arquivos Markdown têm front matter válido
- Verifique os logs do GitHub Actions

### Erro: "Liquid syntax error"

- Verifique se há erros de sintaxe nos templates
- Verifique se os arquivos têm front matter válido

### Documentação não aparece

- Verifique se o GitHub Pages está habilitado em Settings > Pages
- Verifique se o workflow foi executado com sucesso em Actions
- Aguarde alguns minutos (pode levar até 10 minutos para aparecer)

## Atualizando Documentação

1. Edite os arquivos em `docs/en/` ou `docs/pt/`
2. Faça commit e push
3. O GitHub Actions fará o deploy automaticamente
4. Aguarde alguns minutos e verifique o site

## Estrutura de Arquivos

```
docs/
├── _config.yml          # Configuração do Jekyll
├── _layouts/            # Templates HTML
│   ├── default.html
│   └── page.html
├── assets/              # CSS e assets
│   └── css/
│       └── style.css
├── en/                  # Inglês (padrão)
│   ├── index.md
│   ├── installation.md
│   └── ...
├── pt/                  # Português
│   ├── index.md
│   ├── installation.md
│   └── ...
├── Gemfile              # Dependências Ruby
└── README.md            # Este arquivo
```

## Suporte a Múltiplos Idiomas

O sistema suporta múltiplos idiomas através de:
- Pastas separadas por idioma (`en/`, `pt/`)
- Front matter com `lang` e `ref` para identificar páginas correspondentes
- Seletor de idioma no layout que permite alternar entre idiomas

Para adicionar um novo idioma:
1. Crie uma nova pasta (ex: `docs/es/` para espanhol)
2. Adicione o idioma em `_config.yml` em `languages:`
3. Crie as páginas correspondentes com o mesmo `ref`

