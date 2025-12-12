"""Teste do parser de expressões."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from expression_parser import ExpressionParser

def test_parser():
    parser = ExpressionParser()
    
    test_cases = [
        '={{ $json.body.msg }}',
        '={{ $json.query.id }}',
        '={{ $json.headers.authorization }}',
        '={{ $json.body.data.name }}',
        'Texto normal',
        '={{ $json.body }}',
    ]
    
    print("=" * 60)
    print("TESTE: Expression Parser")
    print("=" * 60)
    
    for test in test_cases:
        result = parser.parse_expression(test)
        print(f"\nInput:  {test}")
        print(f"Output: {result}")
    
    print("\n" + "=" * 60)
    print("Parâmetros encontrados:", parser.get_used_params())
    print("Parâmetros do construtor:", parser.get_constructor_params())
    print("=" * 60)

if __name__ == "__main__":
    test_parser()

