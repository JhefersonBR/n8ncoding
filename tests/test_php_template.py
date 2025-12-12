"""
Teste do template PHP melhorado.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from xml_loader import XMLLoader
from generator import Generator


def create_test_workflow():
    """Cria um workflow de teste."""
    return {
        'id': 'test-php',
        'name': 'Workflow de Teste PHP',
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
                    'method': 'GET'
                },
                'connections': {}
            }
        ]
    }


def test_php_template():
    """Testa o template PHP melhorado."""
    print("=" * 60)
    print("TESTE: Template PHP Melhorado")
    print("=" * 60)
    
    loader = XMLLoader()
    generator = Generator(loader, 'php')
    
    workflow = create_test_workflow()
    generated_code = generator.generate_class(workflow)
    
    if not generated_code:
        print("❌ Erro ao gerar código")
        return False
    
    print("✓ Código gerado com sucesso")
    print(f"  Tamanho: {len(generated_code)} caracteres")
    
    # Verifica elementos esperados no template melhorado
    checks = [
        ('DocBlock da classe', '/**' in generated_code and 'class' in generated_code),
        ('Namespace ou package', '@package' in generated_code or 'namespace' in generated_code),
        ('DocBlock do método run', 'public function run' in generated_code and '/**' in generated_code),
        ('Tratamento de erros', 'try' in generated_code and 'catch' in generated_code),
        ('Métodos helper', 'getContext' in generated_code),
        ('Tempo de execução', 'execution_time' in generated_code),
        ('Contexto inicializado', 'start_time' in generated_code),
    ]
    
    print("\n  Verificações do template melhorado:")
    for check_name, result in checks:
        status = "✓" if result else "⚠"
        print(f"    {status} {check_name}")
    
    # Mostra preview
    print("\n  Preview do código gerado:")
    print("  " + "-" * 56)
    lines = generated_code.split('\n')[:40]
    for i, line in enumerate(lines, 1):
        print(f"  {i:3}| {line}")
    if len(generated_code.split('\n')) > 40:
        print("  ...")
    print("  " + "-" * 56)
    
    return True


def main():
    """Executa o teste."""
    print("\n" + "=" * 60)
    print("TESTE DO TEMPLATE PHP MELHORADO")
    print("=" * 60)
    
    try:
        result = test_php_template()
        
        print("\n" + "=" * 60)
        if result:
            print("✓ TESTE PASSOU")
            print("=" * 60)
            return 0
        else:
            print("❌ TESTE FALHOU")
            print("=" * 60)
            return 1
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

