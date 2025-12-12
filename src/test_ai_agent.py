"""
Teste específico para o nó AI Agent.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xml_loader import XMLLoader
from node_mapper import NodeMapper
from generator import Generator


def create_ai_agent_workflow():
    """Cria um workflow de teste com nó AI Agent."""
    return {
        'id': 'test-ai-agent',
        'name': 'Teste AI Agent',
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
                'name': 'AI Agent',
                'type': 'n8n-nodes-aiAgent',
                'parameters': {
                    'prompt': 'Analise este texto e extraia as informações principais',
                    'model': 'gpt-4',
                    'temperature': 0.7,
                    'maxTokens': 2000
                },
                'connections': {}
            }
        ]
    }


def test_ai_agent_template():
    """Testa o template do AI Agent."""
    print("=" * 60)
    print("TESTE: AI Agent Template")
    print("=" * 60)
    
    loader = XMLLoader()
    template = loader.load_node_template('aiAgent')
    
    if template:
        print("✓ Template AI Agent carregado com sucesso")
        print(f"  Nome: {template.get('name')}")
        print(f"  Tamanho do método: {len(template.get('method', ''))} caracteres")
    else:
        print("❌ Erro ao carregar template AI Agent")
        return False
    
    return True


def test_ai_agent_mapping():
    """Testa o mapeamento do nó AI Agent."""
    print("\n" + "=" * 60)
    print("TESTE: AI Agent Node Mapping")
    print("=" * 60)
    
    loader = XMLLoader()
    mapper = NodeMapper(loader)
    
    ai_node = {
        'id': 'node-ai',
        'name': 'AI Agent',
        'type': 'n8n-nodes-aiAgent',
        'parameters': {
            'prompt': 'Analise este texto',
            'model': 'gpt-4',
            'temperature': 0.7,
            'maxTokens': 2000
        }
    }
    
    method_code = mapper.map_node_to_method(ai_node)
    
    if method_code:
        print("✓ Método gerado com sucesso")
        print(f"  Tamanho: {len(method_code)} caracteres")
        print("\n  Preview do código gerado:")
        print("  " + "-" * 56)
        lines = method_code.split('\n')[:15]
        for line in lines:
            print("  " + line)
        print("  " + "-" * 56)
        
        # Verifica se contém elementos esperados
        checks = [
            ('prompt', 'prompt' in method_code.lower()),
            ('model', 'model' in method_code.lower()),
            ('temperature', 'temperature' in method_code.lower()),
            ('api', 'api' in method_code.lower()),
            ('curl', 'curl' in method_code.lower())
        ]
        
        print("\n  Verificações:")
        for check_name, result in checks:
            status = "✓" if result else "⚠"
            print(f"    {status} {check_name}")
        
        return True
    else:
        print("❌ Erro ao gerar método")
        return False


def test_ai_agent_full_workflow():
    """Testa geração completa com AI Agent."""
    print("\n" + "=" * 60)
    print("TESTE: Workflow Completo com AI Agent")
    print("=" * 60)
    
    loader = XMLLoader()
    generator = Generator(loader, 'php')
    
    workflow = create_ai_agent_workflow()
    
    generated_code = generator.generate_class(workflow)
    
    if generated_code:
        print("✓ Classe gerada com sucesso")
        print(f"  Tamanho: {len(generated_code)} caracteres")
        
        # Verifica se contém o método do AI Agent
        if 'ai_agent' in generated_code.lower() or 'aiAgent' in generated_code:
            print("✓ Método do AI Agent encontrado no código")
        
        # Mostra preview
        print("\n  Preview do código gerado:")
        print("  " + "-" * 56)
        lines = generated_code.split('\n')[:25]
        for line in lines:
            print("  " + line)
        if len(generated_code.split('\n')) > 25:
            print("  ...")
        print("  " + "-" * 56)
        
        return True
    else:
        print("❌ Erro ao gerar classe")
        return False


def main():
    """Executa todos os testes."""
    print("\n" + "=" * 60)
    print("TESTES DO NÓ AI AGENT")
    print("=" * 60)
    
    tests = [
        ("Template AI Agent", test_ai_agent_template),
        ("Mapeamento AI Agent", test_ai_agent_mapping),
        ("Workflow Completo", test_ai_agent_full_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Erro no teste '{test_name}': {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 60)
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

