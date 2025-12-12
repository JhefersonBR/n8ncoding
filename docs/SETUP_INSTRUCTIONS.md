# Instruções de Configuração - GitHub Pages

## ✅ O que já foi criado

1. ✅ Estrutura de pastas `docs/` com suporte a múltiplos idiomas
2. ✅ Configuração do Jekyll (`_config.yml`)
3. ✅ Templates HTML (`_layouts/`)
4. ✅ CSS personalizado (`assets/css/style.css`)
5. ✅ Workflow do GitHub Actions (`.github/workflows/pages.yml`)
6. ✅ Documentação completa em inglês (`docs/en/`)
7. ✅ Estrutura de documentação em português (`docs/pt/`)

## ⚠️ O que precisa ser feito

### 1. Completar arquivos em português

Os arquivos em `docs/pt/` que usam `include_relative` precisam ter o conteúdo copiado diretamente. 

**Arquivos que precisam ser atualizados:**
- `docs/pt/usage.md` - Copiar conteúdo de `EXEMPLO_USO.md`
- `docs/pt/env-setup.md` - Copiar conteúdo de `ENV_SETUP.md`
- `docs/pt/contributing.md` - Copiar conteúdo de `CONTRIBUTING.md`
- `docs/pt/gitflow.md` - Copiar conteúdo de `GITFLOW.md`
- `docs/pt/testing.md` - Copiar conteúdo de `TESTES.md`
- `docs/pt/changelog.md` - Copiar conteúdo de `CHANGELOG.md`
- `docs/pt/examples/ai-agent.md` - Copiar conteúdo de `EXEMPLO_AI_AGENT.md`
- `docs/pt/examples/credentials-constructor.md` - Copiar conteúdo de `EXEMPLO_CONSTRUTOR_CREDENCIAIS.md`

**Solução rápida:** Você pode criar um script Python para fazer isso automaticamente:

```python
# scripts/copy-docs-to-jekyll.py
import os
from pathlib import Path

mappings = {
    'EXEMPLO_USO.md': 'docs/pt/usage.md',
    'ENV_SETUP.md': 'docs/pt/env-setup.md',
    'CONTRIBUTING.md': 'docs/pt/contributing.md',
    'GITFLOW.md': 'docs/pt/gitflow.md',
    'TESTES.md': 'docs/pt/testing.md',
    'CHANGELOG.md': 'docs/pt/changelog.md',
    'EXEMPLO_AI_AGENT.md': 'docs/pt/examples/ai-agent.md',
    'EXEMPLO_CONSTRUTOR_CREDENCIAIS.md': 'docs/pt/examples/credentials-constructor.md',
}

for source, dest in mappings.items():
    source_path = Path(source)
    dest_path = Path(dest)
    
    if source_path.exists():
        # Ler conteúdo original
        content = source_path.read_text(encoding='utf-8')
        
        # Ler front matter do arquivo de destino
        if dest_path.exists():
            dest_content = dest_path.read_text(encoding='utf-8')
            # Extrair front matter (linhas entre ---)
            lines = dest_content.split('\n')
            front_matter = []
            in_front_matter = False
            for line in lines:
                if line.strip() == '---':
                    if not in_front_matter:
                        in_front_matter = True
                        front_matter.append(line)
                    else:
                        front_matter.append(line)
                        break
                elif in_front_matter:
                    front_matter.append(line)
            
            # Combinar front matter + conteúdo original
            new_content = '\n'.join(front_matter) + '\n\n' + content
            
            # Escrever arquivo
            dest_path.write_text(new_content, encoding='utf-8')
            print(f'✅ Atualizado: {dest}')
        else:
            print(f'⚠️  Arquivo de destino não existe: {dest}')
    else:
        print(f'⚠️  Arquivo fonte não existe: {source}')
```

### 2. Configurar GitHub Pages

1. Vá para **Settings** > **Pages** no repositório GitHub
2. Em **Source**, selecione **GitHub Actions**
3. Salve as alterações

### 3. Testar localmente (opcional)

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Acesse `http://localhost:4000/n8ncoding/`

### 4. Fazer commit e push

```bash
git add docs/
git add .github/workflows/pages.yml
git commit -m "docs: adiciona estrutura do GitHub Pages com suporte a múltiplos idiomas"
git push
```

## 📋 Checklist Final

- [ ] Completar arquivos em português (copiar conteúdo dos arquivos originais)
- [ ] Configurar GitHub Pages em Settings > Pages
- [ ] Testar localmente (opcional)
- [ ] Fazer commit e push
- [ ] Verificar deploy em Actions
- [ ] Acessar documentação em `https://jhefersonbr.github.io/n8ncoding/`

## 🌐 URLs Finais

Após o deploy:
- Inglês (padrão): `https://jhefersonbr.github.io/n8ncoding/en/`
- Português: `https://jhefersonbr.github.io/n8ncoding/pt/`
- Página inicial: `https://jhefersonbr.github.io/n8ncoding/` (redireciona para inglês)

## 📝 Notas

- O idioma padrão é inglês (`en`)
- O seletor de idioma aparece no topo de cada página
- Todas as páginas têm o mesmo `ref` em ambos os idiomas para facilitar a navegação
- O GitHub Actions faz deploy automaticamente quando arquivos em `docs/` são modificados

