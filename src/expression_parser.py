"""
Módulo para fazer parsing de expressões do n8n e substituí-las por código PHP.
"""
import re
from typing import Dict, List, Optional, Set


class ExpressionParser:
    """Classe para fazer parsing de expressões do n8n."""
    
    def __init__(self, constructor_params: Dict[str, str] = None):
        """
        Inicializa o parser de expressões.
        
        Args:
            constructor_params: Dicionário com parâmetros do construtor (nome => tipo)
        """
        self.constructor_params = constructor_params or {}
        self.used_params: Set[str] = set()
    
    def parse_expression(self, expression: str) -> str:
        """
        Faz parsing de uma expressão do n8n e converte para PHP.
        
        Expressões suportadas:
        - ={{ $json.body.msg }} -> $this->params['msg']
        - ={{ $json.body.data.name }} -> $this->params['data']['name']
        - ={{ $json.query.id }} -> $this->params['id']
        - ={{ $json.headers.authorization }} -> $this->params['authorization']
        
        Args:
            expression: Expressão do n8n
            
        Returns:
            Código PHP equivalente
        """
        if not isinstance(expression, str):
            return expression
        
        # Remove espaços extras
        expression = expression.strip()
        
        # Se não é uma expressão n8n, retorna como está
        if not expression.startswith('={{') or not expression.endswith('}}'):
            return f'"{expression}"'
        
        # Remove marcadores de expressão
        inner = expression[3:-2].strip()
        
        # Padrão para $json.body.xxx ou $json.query.xxx ou $json.headers.xxx
        # Tenta diferentes variações do padrão (com e sem escape)
        patterns = [
            r'\$json\.(body|query|headers)\.(.+)',  # Padrão normal
            r'\\\$json\.(body|query|headers)\.(.+)',  # Com escape
            r'json\.(body|query|headers)\.(.+)',  # Sem $
        ]
        
        match = None
        for pattern in patterns:
            match = re.search(pattern, inner)
            if match:
                break
        
        # Se não encontrou com regex, tenta extração manual
        if not match:
            # Procura por padrões conhecidos
            if '.body.' in inner:
                path = inner.split('.body.')[-1].strip()
                return self._build_php_access(path)
            elif '.query.' in inner:
                path = inner.split('.query.')[-1].strip()
                return self._build_php_access(path)
            elif '.headers.' in inner:
                path = inner.split('.headers.')[-1].strip()
                return self._build_php_access(path)
        
        if match:
            source_type = match.group(1)  # body, query, headers
            path = match.group(2)  # msg, data.name, etc.
            
            # Converte caminho para acesso PHP
            parts = path.split('.')
            
            # Registra parâmetro usado
            param_name = parts[0]
            self.used_params.add(param_name)
            
            # Adiciona ao construtor se não existir
            if param_name not in self.constructor_params:
                self.constructor_params[param_name] = 'mixed'
            
            # Constrói acesso PHP
            if len(parts) == 1:
                # Acesso simples: $this->params['msg']
                return f"$this->params['{param_name}']"
            else:
                # Acesso aninhado: $this->params['data']['name']
                php_path = f"$this->params['{parts[0]}']"
                for part in parts[1:]:
                    php_path += f"['{part}']"
                return php_path
        
        # Padrão para $json.xxx (acesso direto)
        pattern = r'\$json\.(.+)'
        match = re.match(pattern, inner)
        if match:
            path = match.group(1)
            parts = path.split('.')
            
            param_name = parts[0]
            self.used_params.add(param_name)
            
            if param_name not in self.constructor_params:
                self.constructor_params[param_name] = 'mixed'
            
            if len(parts) == 1:
                return f"$this->params['{param_name}']"
            else:
                php_path = f"$this->params['{parts[0]}']"
                for part in parts[1:]:
                    php_path += f"['{part}']"
                return php_path
        
        # Se não conseguiu fazer parsing, retorna como string literal
        return f'"{expression}"'
    
    def parse_string_value(self, value: str) -> str:
        """
        Faz parsing de um valor string que pode conter expressões.
        
        Args:
            value: Valor que pode conter expressões n8n
            
        Returns:
            Código PHP com expressões substituídas
        """
        if not isinstance(value, str):
            return value
        
        # Se contém expressões, processa
        if '={{' in value and '}}' in value:
            # Encontra todas as expressões
            pattern = r'=\{\{([^}]+)\}\}'
            matches = re.findall(pattern, value)
            
            if matches:
                # Substitui cada expressão
                result = value
                for match in matches:
                    expr = f'={{{{{match}}}}}'
                    parsed = self.parse_expression(expr)
                    result = result.replace(expr, parsed)
                
                # Se sobrou texto, concatena
                if result != value:
                    # Verifica se precisa concatenar strings
                    if result.startswith('$'):
                        return result
                    else:
                        return f'"{result}"'
        
        # Se é uma expressão completa
        if value.strip().startswith('={{') and value.strip().endswith('}}'):
            return self.parse_expression(value)
        
        # Caso contrário, retorna como string
        return f'"{value}"'
    
    def get_constructor_params(self) -> Dict[str, str]:
        """
        Retorna os parâmetros necessários para o construtor.
        
        Returns:
            Dicionário com nome => tipo dos parâmetros
        """
        return self.constructor_params.copy()
    
    def get_used_params(self) -> Set[str]:
        """
        Retorna os parâmetros que foram usados.
        
        Returns:
            Set com nomes dos parâmetros usados
        """
        return self.used_params.copy()

