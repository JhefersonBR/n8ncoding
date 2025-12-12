#!/usr/bin/env python3
"""
Script para copiar conteúdo dos arquivos de documentação originais
para os arquivos Jekyll em português, preservando o front matter.
"""

import os
from pathlib import Path

# Mapeamento de arquivos originais para arquivos Jekyll
MAPPINGS = {
    'EXEMPLO_USO.md': 'docs/pt/usage.md',
    'ENV_SETUP.md': 'docs/pt/env-setup.md',
    'CONTRIBUTING.md': 'docs/pt/contributing.md',
    'GITFLOW.md': 'docs/pt/gitflow.md',
    'TESTES.md': 'docs/pt/testing.md',
    'CHANGELOG.md': 'docs/pt/changelog.md',
    'EXEMPLO_AI_AGENT.md': 'docs/pt/examples/ai-agent.md',
    'EXEMPLO_CONSTRUTOR_CREDENCIAIS.md': 'docs/pt/examples/credentials-constructor.md',
}

def extract_front_matter(content: str) -> tuple[str, str]:
    """
    Extrai o front matter (YAML entre ---) do conteúdo.
    Retorna (front_matter, body)
    """
    lines = content.split('\n')
    front_matter_lines = []
    body_lines = []
    in_front_matter = False
    front_matter_count = 0
    
    for line in lines:
        if line.strip() == '---':
            front_matter_count += 1
            if front_matter_count == 1:
                in_front_matter = True
                front_matter_lines.append(line)
            elif front_matter_count == 2:
                in_front_matter = False
                front_matter_lines.append(line)
                continue
        elif in_front_matter:
            front_matter_lines.append(line)
        else:
            body_lines.append(line)
    
    front_matter = '\n'.join(front_matter_lines)
    body = '\n'.join(body_lines).strip()
    
    return front_matter, body

def main():
    """Função principal."""
    base_dir = Path(__file__).parent.parent
    
    for source_file, dest_file in MAPPINGS.items():
        source_path = base_dir / source_file
        dest_path = base_dir / dest_file
        
        if not source_path.exists():
            print(f'[AVISO] Arquivo fonte nao existe: {source_file}')
            continue
        
        if not dest_path.exists():
            print(f'[AVISO] Arquivo de destino nao existe: {dest_file}')
            continue
        
        # Ler conteúdo original
        try:
            original_content = source_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f'[ERRO] Erro ao ler {source_file}: {e}')
            continue
        
        # Ler arquivo de destino para extrair front matter
        try:
            dest_content = dest_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f'[ERRO] Erro ao ler {dest_file}: {e}')
            continue
        
        # Extrair front matter do arquivo de destino
        front_matter, _ = extract_front_matter(dest_content)
        
        # Combinar front matter + conteúdo original
        if front_matter:
            new_content = front_matter + '\n\n' + original_content
        else:
            new_content = original_content
        
        # Escrever arquivo
        try:
            dest_path.write_text(new_content, encoding='utf-8')
            print(f'[OK] Atualizado: {dest_file}')
        except Exception as e:
            print(f'[ERRO] Erro ao escrever {dest_file}: {e}')

if __name__ == '__main__':
    main()

