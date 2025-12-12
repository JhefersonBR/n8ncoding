"""
Teste para verificar a geração de nomes de métodos em camelCase.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from node_mapper import NodeMapper
from xml_loader import XMLLoader

def test_method_names():
    print("=" * 60)
    print("TESTE: Geração de Nomes de Métodos em camelCase")
    print("=" * 60)
    print()
    
    mapper = NodeMapper(XMLLoader())
    
    test_cases = [
        {'name': 'AI Agent', 'type': 'n8n-nodes-base.aiAgent'},
        {'name': 'Send Email', 'type': 'n8n-nodes-base.email'},
        {'name': 'Update CRM', 'type': 'n8n-nodes-base.httpRequest'},
        {'name': 'webhook-start', 'type': 'n8n-nodes-base.webhook'},
        {'name': 'Set', 'type': 'n8n-nodes-base.set'},
        {'name': 'Conselheiro Bíblico', 'type': '@n8n/n8n-nodes-langchain.agent'},
        {'name': 'HTTP Request', 'type': 'n8n-nodes-base.httpRequest'},
        {'name': 'IF Condition', 'type': 'n8n-nodes-base.if'},
        {'name': 'Code', 'type': 'n8n-nodes-base.code'},
        {'name': 'if', 'type': 'n8n-nodes-base.if'},  # Palavra reservada
        {'name': 'return', 'type': 'n8n-nodes-base.return'},  # Palavra reservada
        {'name': 'class', 'type': 'n8n-nodes-base.class'},  # Palavra reservada
        {'name': '', 'type': 'n8n-nodes-base.unknown'},  # Teste sem nome
    ]
    
    for node in test_cases:
        method_name = mapper.generate_method_name(node)
        print(f"'{node['name']}' ({node['type']}) -> {method_name}")
    
    print()
    print("=" * 60)
    print("Verificações:")
    print("=" * 60)
    
    # Verifica se todos começam com letra minúscula
    all_valid = True
    for node in test_cases:
        method_name = mapper.generate_method_name(node)
        if method_name and not method_name[0].islower():
            print(f"ERRO: '{method_name}' não começa com letra minúscula")
            all_valid = False
    
    if all_valid:
        print("✓ Todos os nomes começam com letra minúscula")
    
    # Verifica se são válidos em PHP
    import re
    php_valid_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
    all_php_valid = True
    for node in test_cases:
        method_name = mapper.generate_method_name(node)
        if not php_valid_pattern.match(method_name):
            print(f"ERRO: '{method_name}' não é válido em PHP")
            all_php_valid = False
    
    if all_php_valid:
        print("✓ Todos os nomes são válidos em PHP")
    
    print("=" * 60)

if __name__ == "__main__":
    test_method_names()

