# Documentação n8ncoding - GitHub Pages

Esta pasta contém a documentação do projeto n8ncoding que será publicada no GitHub Pages.

## Estrutura

```
docs/
├── _config.yml          # Configuração do Jekyll
├── _layouts/            # Templates HTML
├── assets/              # CSS e outros assets
├── en/                  # Documentação em inglês (padrão)
│   ├── index.md
│   ├── installation.md
│   ├── usage.md
│   └── ...
├── pt/                  # Documentação em português
│   ├── index.md
│   ├── installation.md
│   ├── usage.md
│   └── ...
└── Gemfile              # Dependências Ruby/Jekyll
```

## Como Funciona

- **Idioma padrão:** Inglês (`en/`)
- **Idiomas suportados:** Inglês (`en`) e Português (`pt`)
- **Framework:** Jekyll (suportado nativamente pelo GitHub Pages)
- **Deploy:** Automático via GitHub Actions quando arquivos em `docs/` são modificados

## Desenvolvimento Local

Para testar a documentação localmente:

1. Instale o Ruby e o Bundler (se ainda não tiver):
   ```bash
   # Windows (usando Chocolatey)
   choco install ruby

   # Linux/Mac
   # Ruby geralmente já vem instalado
   ```

2. Instale as dependências:
   ```bash
   cd docs
   bundle install
   ```

3. Execute o servidor local:
   ```bash
   bundle exec jekyll serve
   ```

4. Acesse: `http://localhost:4000`

## Adicionando Nova Documentação

### Em Inglês (padrão)

1. Crie o arquivo em `docs/en/nome-do-arquivo.md`
2. Adicione o front matter:
   ```yaml
   ---
   layout: page
   title: Título da Página
   lang: en
   ref: nome-do-arquivo
   permalink: /en/nome-do-arquivo/
   ---
   ```

### Em Português

1. Crie o arquivo em `docs/pt/nome-do-arquivo.md`
2. Adicione o front matter:
   ```yaml
   ---
   layout: page
   title: Título da Página
   lang: pt
   ref: nome-do-arquivo
   permalink: /pt/nome-do-arquivo/
   ---
   ```

**Importante:** O campo `ref` deve ser o mesmo em ambos os idiomas para que o seletor de idioma funcione corretamente.

## Deploy

O deploy é automático via GitHub Actions quando:
- Arquivos em `docs/` são modificados
- Push é feito nas branches `main` ou `develop`

O workflow está configurado em `.github/workflows/pages.yml`.

## Configuração do GitHub Pages

1. Vá em Settings > Pages no repositório
2. Configure:
   - Source: GitHub Actions
   - Branch: Deixe como está (o workflow cuida disso)

## Links

- Documentação em Inglês: `https://jhefersonbr.github.io/n8ncoding/en/`
- Documentação em Português: `https://jhefersonbr.github.io/n8ncoding/pt/`
- Página inicial (redireciona para inglês): `https://jhefersonbr.github.io/n8ncoding/`

