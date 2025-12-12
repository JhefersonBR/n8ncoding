"""
Teste completo da nova funcionalidade: construtor com parâmetros e classes de credenciais.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from xml_loader import XMLLoader
from generator import Generator
from expression_parser import ExpressionParser
from parameter_extractor import ParameterExtractor


def create_test_workflow_with_expressions():
    """Cria um workflow de teste com expressões n8n."""
    return {
        'id': 'test-complete',
        'name': 'Workflow Completo com Expressões',
        'nodes': [
            {
                'id': 'node-1',
                'name': 'Webhook',
                'type': 'n8n-nodes-base.webhook',
                'parameters': {
                    'body': {
                        'msg': 'teste'
                    },
                    'query': {
                        'id': '123'
                    }
                },
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
                    'prompt': '={{ $json.body.msg }}',
                    'model': 'gpt-4',
                    'temperature': 0.7,
                    'maxTokens': 1000
                },
                'connections': {}
            }
        ]
    }


def test_complete_feature():
    """Testa a funcionalidade completa."""
    print("=" * 60)
    print("TESTE: Funcionalidade Completa")
    print("=" * 60)
    
    loader = XMLLoader()
    generator = Generator(loader, 'php')
    
    workflow = create_test_workflow_with_expressions()
    
    # Testa extração de parâmetros
    extractor = ParameterExtractor()
    params = extractor.extract_from_workflow(workflow)
    print(f"\n[OK] Parametros extraidos: {params}")
    
    # Testa parser de expressões
    parser = ExpressionParser(params)
    test_expr = '={{ $json.body.msg }}'
    parsed = parser.parse_expression(test_expr)
    print(f"\n[OK] Expressao '{test_expr}' -> {parsed}")
    
    # Gera classe completa
    generated_code = generator.generate_class(workflow)
    
    if generated_code:
        print("\n[OK] Classe gerada com sucesso")
        print(f"  Tamanho: {len(generated_code)} caracteres")
        
        # Verifica elementos esperados
        checks = [
            ('Construtor', '__construct' in generated_code),
            ('Parâmetros', '$this->params' in generated_code),
            ('Expressão substituída', '$this->params[\'msg\']' in generated_code),
            ('Classes de credenciais', 'OpenAICredentials' in generated_code or 'use' in generated_code),
            ('Require credentials', 'require_once' in generated_code or 'Credentials.php' in generated_code),
        ]
        
        print("\n  Verificacoes:")
        for check_name, result in checks:
            status = "[OK]" if result else "[AVISO]"
            print(f"    {status} {check_name}")
        
        # Mostra preview
        print("\n  Preview do código gerado:")
        print("  " + "-" * 56)
        lines = generated_code.split('\n')[:60]
        for i, line in enumerate(lines, 1):
            print(f"  {i:3}| {line}")
        if len(generated_code.split('\n')) > 60:
            print("  ...")
        print("  " + "-" * 56)
        
        return True
    else:
        print("\n[ERRO] Erro ao gerar classe")
        return False


if __name__ == "__main__":
    try:
        result = test_complete_feature()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n[ERRO] Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

