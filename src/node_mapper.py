"""
Módulo para mapear nós do n8n em métodos de código.
"""
import json
from typing import Dict, Optional
from xml_loader import XMLLoader


class NodeMapper:
    """Classe para mapear nós do workflow em métodos de código."""
    
    def __init__(self, xml_loader: XMLLoader):
        """
        Inicializa o mapeador de nós.
        
        Args:
            xml_loader: Instância do XMLLoader para carregar templates
        """
        self.xml_loader = xml_loader
    
    def generate_method_name(self, node: Dict) -> str:
        """
        Gera um nome de método baseado no nó.
        
        Args:
            node: Dados do nó do workflow
            
        Returns:
            Nome do método em formato camelCase
        """
        node_name = node.get('name', 'node')
        node_type = node.get('type', 'unknown')
        
        # Remove caracteres especiais e normaliza
        method_name = node_name.lower().replace(' ', '_').replace('-', '_')
        method_name = ''.join(c for c in method_name if c.isalnum() or c == '_')
        
        # Garante que começa com letra
        if method_name and not method_name[0].isalpha():
            method_name = 'node_' + method_name
        
        # Se estiver vazio, usa o tipo
        if not method_name:
            method_name = node_type.replace('.', '_')
        
        return method_name
    
    def map_node_to_method(self, node: Dict) -> Optional[str]:
        """
        Mapeia um nó do workflow em um método de código.
        
        Args:
            node: Dados do nó do workflow
            
        Returns:
            Código do método gerado ou None em caso de erro
        """
        node_type = node.get('type', '')
        
        # Remove prefixo 'n8n-nodes-' se existir
        if node_type.startswith('n8n-nodes-'):
            node_type = node_type.replace('n8n-nodes-', '')
        
        # Carrega o template do nó
        template = self.xml_loader.load_node_template(node_type)
        
        if not template:
            # Template padrão se não encontrar específico
            return self._generate_default_method(node)
        
        method_name = self.generate_method_name(node)
        method_template = template['method']
        
        # Substitui placeholders básicos
        method_code = method_template.replace('{{method_name}}', method_name)
        
        # Gera código específico baseado no tipo de nó
        generated_code = self._generate_node_code(node, node_type)
        method_code = method_code.replace('{{generated_code}}', generated_code)
        
        # Substitui outros placeholders comuns
        method_code = self._replace_common_placeholders(method_code, node)
        
        # Se o template não tinha {{generated_code}}, adiciona o código gerado
        if '{{generated_code}}' in method_code:
            method_code = method_code.replace('{{generated_code}}', generated_code)
        
        return method_code
    
    def _generate_default_method(self, node: Dict) -> str:
        """
        Gera um método padrão quando não há template específico.
        
        Args:
            node: Dados do nó
            
        Returns:
            Código do método padrão
        """
        method_name = self.generate_method_name(node)
        node_name = node.get('name', 'Node')
        
        return f"""private function {method_name}(): void
{{
    // Nó: {node_name}
    // Tipo: {node.get('type', 'unknown')}
    // TODO: Implementar lógica específica deste nó
    $this->context['{method_name}_output'] = [];
}}"""
    
    def _generate_node_code(self, node: Dict, node_type: str) -> str:
        """
        Gera código específico para um tipo de nó.
        
        Args:
            node: Dados do nó
            node_type: Tipo do nó
            
        Returns:
            Código gerado para o nó
        """
        parameters = node.get('parameters', {})
        method_name = self.generate_method_name(node)
        output_key = f"{method_name}_output"
        
        if node_type == 'function':
            # Para nós function, tenta pegar o código JavaScript
            code = parameters.get('functionCode', '')
            if code:
                # Converte código JavaScript básico para PHP (simplificado)
                # TODO: Implementar conversão mais completa de JS para PHP
                php_code = code.replace('$input', '$this->context')
                php_code = php_code.replace('items', '$this->context')
                return f"// Código convertido do n8n\n    // {code[:100]}...\n    $this->context['{output_key}'] = [];"
            return f"// Função vazia\n    $this->context['{output_key}'] = [];"
        
        elif node_type == 'httpRequest':
            # Para HTTP Request - o template já tem a lógica completa
            # Aqui apenas retornamos um placeholder que será substituído
            return f"// HTTP Request processado pelo template"
        
        # Código genérico para outros tipos
        node_name = node.get('name', 'Node')
        return f"// Processamento do nó {node_type}: {node_name}\n    $this->context['{output_key}'] = [];"
    
    def _replace_common_placeholders(self, code: str, node: Dict) -> str:
        """
        Substitui placeholders comuns no código.
        
        Args:
            code: Código com placeholders
            node: Dados do nó
            
        Returns:
            Código com placeholders substituídos
        """
        method_name = self.generate_method_name(node)
        output_key = f"{method_name}_output"
        parameters = node.get('parameters', {})
        
        # Processa headers se existirem
        headers = parameters.get('options', {}).get('headers', {})
        headers_array = []
        if isinstance(headers, dict):
            for key, value in headers.items():
                if isinstance(value, dict) and 'value' in value:
                    headers_array.append(f"'{key}: {value['value']}'")
                else:
                    headers_array.append(f"'{key}: {value}'")
        headers_str = '[' + ', '.join(headers_array) + ']' if headers_array else '[]'
        
        # Processa body
        body = parameters.get('body', {})
        body_str = 'null'
        if body:
            try:
                body_str = json.dumps(body, ensure_ascii=False, indent=8)
                body_str = body_str.replace('\n', '\n    ')
            except:
                body_str = 'null'
        
        replacements = {
            '{{output_key}}': output_key,
            '{{url}}': f'"{parameters.get("url", "")}"',
            '{{method}}': f'"{parameters.get("method", "GET")}"',
            '{{headers}}': headers_str,
            '{{body}}': body_str
        }
        
        for placeholder, value in replacements.items():
            code = code.replace(placeholder, str(value))
        
        return code

