#!/usr/bin/env python3
"""
Script para criar arquivos .md em inglês na raiz do projeto
a partir dos arquivos em docs/en/, removendo o front matter do Jekyll.
"""

from pathlib import Path

# Mapeamento de arquivos docs/en/ para arquivos na raiz
MAPPINGS = {
    'docs/en/usage.md': 'USAGE.md',
    'docs/en/env-setup.md': 'ENV_SETUP.md',
    'docs/en/contributing.md': 'CONTRIBUTING.md',
    'docs/en/gitflow.md': 'GITFLOW.md',
    'docs/en/testing.md': 'TESTING.md',
    'docs/en/changelog.md': 'CHANGELOG.md',
    'docs/en/examples/ai-agent.md': 'AI_AGENT_EXAMPLE.md',
    'docs/en/examples/credentials-constructor.md': 'CREDENTIALS_CONSTRUCTOR_EXAMPLE.md',
}

def extract_content_without_front_matter(content: str) -> str:
    """
    Remove o front matter (YAML entre ---) do conteúdo.
    Retorna apenas o corpo do documento.
    """
    lines = content.split('\n')
    body_lines = []
    in_front_matter = False
    front_matter_count = 0
    
    for line in lines:
        if line.strip() == '---':
            front_matter_count += 1
            if front_matter_count == 1:
                in_front_matter = True
                continue
            elif front_matter_count == 2:
                in_front_matter = False
                continue
        elif not in_front_matter:
            body_lines.append(line)
    
    return '\n'.join(body_lines).strip()

def main():
    """Função principal."""
    base_dir = Path(__file__).parent.parent
    
    for source_file, dest_file in MAPPINGS.items():
        source_path = base_dir / source_file
        dest_path = base_dir / dest_file
        
        if not source_path.exists():
            print(f'[AVISO] Arquivo fonte nao existe: {source_file}')
            continue
        
        # Ler conteúdo original
        try:
            original_content = source_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f'[ERRO] Erro ao ler {source_file}: {e}')
            continue
        
        # Remover front matter
        content_without_front_matter = extract_content_without_front_matter(original_content)
        
        # Escrever arquivo
        try:
            dest_path.write_text(content_without_front_matter, encoding='utf-8')
            print(f'[OK] Criado: {dest_file}')
        except Exception as e:
            print(f'[ERRO] Erro ao escrever {dest_file}: {e}')

if __name__ == '__main__':
    main()

