"""
Script de teste do n8ncoding com dados simulados.
Permite testar a aplicação sem precisar de um servidor n8n rodando.
"""
import json
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

from xml_loader import XMLLoader
from generator import Generator
from node_mapper import NodeMapper


def create_test_workflow():
    """Cria um workflow de teste simulado."""
    return {
        'id': 'test-1',
        'name': 'Workflow de Teste',
        'nodes': [
            {
                'id': 'node-1',
                'name': 'Start',
                'type': 'n8n-nodes-start',
                'parameters': {},
                'connections': {
                    'main': {
                        '0': [[{'node': 'node-2'}]]
                    }
                }
            },
            {
                'id': 'node-2',
                'name': 'HTTP Request',
                'type': 'n8n-nodes-httpRequest',
                'parameters': {
                    'url': 'https://api.example.com/test',
                    'method': 'POST',
                    'body': {
                        'message': 'Teste',
                        'status': 'active'
                    },
                    'options': {
                        'headers': {
                            'Content-Type': {'value': 'application/json'},
                            'Authorization': {'value': 'Bearer test-token'}
                        }
                    }
                },
                'connections': {
                    'main': {
                        '0': [[{'node': 'node-3'}]]
                    }
                }
            },
            {
                'id': 'node-3',
                'name': 'Processar Dados',
                'type': 'n8n-nodes-function',
                'parameters': {
                    'functionCode': 'const data = $input.item.json;\nreturn { processed: true, data: data };'
                },
                'connections': {}
            }
        ]
    }


def test_xml_loader():
    """Testa o carregador de templates XML."""
    print("=" * 60)
    print("TESTE 1: XML Loader")
    print("=" * 60)
    
    loader = XMLLoader()
    
    # Testa carregamento de template de linguagem
    php_template = loader.load_language_template('php')
    if php_template:
        print("✓ Template PHP carregado com sucesso")
        print(f"  Tamanho: {len(php_template)} caracteres")
    else:
        print("❌ Erro ao carregar template PHP")
        return False
    
    # Testa carregamento de templates de nós
    node_types = ['function', 'httpRequest']
    for node_type in node_types:
        template = loader.load_node_template(node_type)
        if template:
            print(f"✓ Template de nó '{node_type}' carregado")
        else:
            print(f"⚠ Template de nó '{node_type}' não encontrado")
    
    print()
    return True


def test_node_mapper():
    """Testa o mapeador de nós."""
    print("=" * 60)
    print("TESTE 2: Node Mapper")
    print("=" * 60)
    
    loader = XMLLoader()
    mapper = NodeMapper(loader)
    
    # Cria um nó de teste
    test_node = {
        'id': 'test-node',
        'name': 'Test HTTP Request',
        'type': 'n8n-nodes-httpRequest',
        'parameters': {
            'url': 'https://api.test.com',
            'method': 'GET'
        }
    }
    
    # Testa geração de nome de método
    method_name = mapper.generate_method_name(test_node)
    print(f"✓ Nome de método gerado: {method_name}")
    
    # Testa mapeamento completo
    method_code = mapper.map_node_to_method(test_node)
    if method_code:
        print("✓ Método gerado com sucesso")
        print(f"  Tamanho: {len(method_code)} caracteres")
        # Mostra preview
        preview = method_code.split('\n')[:5]
        print("  Preview:")
        for line in preview:
            print(f"    {line}")
    else:
        print("❌ Erro ao gerar método")
        return False
    
    print()
    return True


def test_generator():
    """Testa o gerador de código."""
    print("=" * 60)
    print("TESTE 3: Generator")
    print("=" * 60)
    
    loader = XMLLoader()
    generator = Generator(loader, 'php')
    
    workflow = create_test_workflow()
    
    # Testa ordenação de nós
    ordered_nodes = generator._determine_execution_order(workflow['nodes'])
    print(f"✓ Nós ordenados: {len(ordered_nodes)} nós")
    print("  Ordem de execução:")
    for i, node in enumerate(ordered_nodes, 1):
        print(f"    {i}. {node.get('name')} ({node.get('type')})")
    
    # Testa geração de classe
    generated_code = generator.generate_class(workflow)
    if generated_code:
        print("✓ Classe gerada com sucesso")
        print(f"  Tamanho: {len(generated_code)} caracteres")
        
        # Verifica se contém elementos esperados
        checks = [
            ('class', 'class' in generated_code.lower()),
            ('run', 'function run' in generated_code),
            ('context', '$context' in generated_code),
            ('methods', 'private function' in generated_code)
        ]
        
        print("  Verificações:")
        for check_name, result in checks:
            status = "✓" if result else "❌"
            print(f"    {status} {check_name}")
        
        # Mostra preview
        print("\n  Preview do código gerado:")
        print("  " + "-" * 56)
        lines = generated_code.split('\n')[:20]
        for line in lines:
            print("  " + line)
        if len(generated_code.split('\n')) > 20:
            print("  ...")
        print("  " + "-" * 56)
    else:
        print("❌ Erro ao gerar classe")
        return False
    
    print()
    return True


def test_full_workflow():
    """Testa o fluxo completo de geração."""
    print("=" * 60)
    print("TESTE 4: Fluxo Completo")
    print("=" * 60)
    
    loader = XMLLoader()
    generator = Generator(loader, 'php')
    
    workflow = create_test_workflow()
    
    # Gera código
    generated_code = generator.generate_class(workflow)
    
    if not generated_code:
        print("❌ Erro ao gerar código")
        return False
    
    # Salva arquivo de teste
    output_path = generator.save_generated_code(workflow, generated_code)
    
    if output_path:
        print(f"✓ Arquivo salvo: {output_path}")
        
        # Verifica se arquivo existe
        if Path(output_path).exists():
            file_size = Path(output_path).stat().st_size
            print(f"✓ Arquivo existe ({file_size} bytes)")
        else:
            print("❌ Arquivo não encontrado")
            return False
    else:
        print("❌ Erro ao salvar arquivo")
        return False
    
    print()
    return True


def main():
    """Executa todos os testes."""
    print("\n" + "=" * 60)
    print("TESTES DO N8NCODING")
    print("=" * 60)
    print()
    
    tests = [
        ("XML Loader", test_xml_loader),
        ("Node Mapper", test_node_mapper),
        ("Generator", test_generator),
        ("Fluxo Completo", test_full_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste '{test_name}': {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Resumo
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram!")
        return 0
    else:
        print(f"\n⚠ {total - passed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTestes cancelados pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

