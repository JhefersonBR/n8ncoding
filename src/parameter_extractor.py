"""
Módulo para extrair parâmetros do primeiro nó do workflow.
"""
from typing import Dict, List, Optional, Set
import re


class ParameterExtractor:
    """Classe para extrair parâmetros do primeiro nó do workflow."""
    
    def __init__(self):
        """Inicializa o extrator de parâmetros."""
        pass
    
    def extract_from_node(self, node: Dict) -> Dict[str, str]:
        """
        Extrai parâmetros de um nó (webhook, start, etc.).
        
        Args:
            node: Dados do nó
            
        Returns:
            Dicionário com nome => tipo dos parâmetros encontrados
        """
        parameters = {}
        node_params = node.get('parameters', {})
        node_type = node.get('type', '').lower()
        
        # Para webhooks, extrai parâmetros do body, query, headers
        if 'webhook' in node_type:
            # Body parameters
            body = node_params.get('body', {})
            if isinstance(body, dict):
                for key in body.keys():
                    parameters[key] = 'mixed'
            
            # Query parameters
            query = node_params.get('query', {})
            if isinstance(query, dict):
                for key in query.keys():
                    parameters[key] = 'mixed'
            
            # Headers
            headers = node_params.get('headers', {})
            if isinstance(headers, dict):
                for key in headers.keys():
                    parameters[key] = 'mixed'
        
        # Procura por expressões n8n nos parâmetros do nó
        self._extract_from_dict(node_params, parameters)
        
        return parameters
    
    def _extract_from_dict(self, data: Dict, parameters: Dict[str, str], prefix: str = ''):
        """
        Extrai parâmetros recursivamente de um dicionário.
        
        Args:
            data: Dicionário para processar
            parameters: Dicionário onde armazenar parâmetros encontrados
            prefix: Prefixo para chaves aninhadas
        """
        for key, value in data.items():
            if isinstance(value, str):
                # Procura por expressões n8n
                if '={{' in value and '$json.' in value:
                    # Extrai nome do parâmetro da expressão
                    pattern = r'\$json\.(?:body|query|headers)\.([a-zA-Z_][a-zA-Z0-9_]*)'
                    match = re.search(pattern, value)
                    if match:
                        param_name = match.group(1)
                        if prefix:
                            param_name = f"{prefix}_{param_name}"
                        parameters[param_name] = 'mixed'
            
            elif isinstance(value, dict):
                # Processa recursivamente
                new_prefix = f"{prefix}_{key}" if prefix else key
                self._extract_from_dict(value, parameters, new_prefix)
            
            elif isinstance(value, list):
                # Processa itens da lista
                for item in value:
                    if isinstance(item, dict):
                        self._extract_from_dict(item, parameters, prefix)
    
    def extract_from_workflow(self, workflow: Dict) -> Dict[str, str]:
        """
        Extrai parâmetros do primeiro nó do workflow.
        
        Args:
            workflow: Dados completos do workflow
            
        Returns:
            Dicionário com nome => tipo dos parâmetros
        """
        nodes = workflow.get('nodes', [])
        if not nodes:
            return {}
        
        # Encontra o primeiro nó (geralmente webhook ou start)
        first_node = None
        for node in nodes:
            node_type = node.get('type', '').lower()
            if 'webhook' in node_type or 'start' in node_type:
                first_node = node
                break
        
        if not first_node:
            # Se não encontrou, usa o primeiro nó
            first_node = nodes[0]
        
        return self.extract_from_node(first_node)
    
    def find_expressions_in_workflow(self, workflow: Dict) -> Set[str]:
        """
        Encontra todas as expressões n8n usadas no workflow.
        
        Args:
            workflow: Dados completos do workflow
            
        Returns:
            Set com nomes de parâmetros encontrados
        """
        expressions = set()
        nodes = workflow.get('nodes', [])
        
        for node in nodes:
            params = node.get('parameters', {})
            self._find_expressions_in_dict(params, expressions)
        
        return expressions
    
    def _find_expressions_in_dict(self, data: Dict, expressions: Set[str]):
        """
        Encontra expressões recursivamente em um dicionário.
        
        Args:
            data: Dicionário para processar
            expressions: Set onde armazenar expressões encontradas
        """
        for value in data.values():
            if isinstance(value, str):
                # Procura por expressões n8n
                if '={{' in value and '$json.' in value:
                    pattern = r'\$json\.(?:body|query|headers)\.([a-zA-Z_][a-zA-Z0-9_]*)'
                    matches = re.findall(pattern, value)
                    expressions.update(matches)
            
            elif isinstance(value, dict):
                self._find_expressions_in_dict(value, expressions)
            
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._find_expressions_in_dict(item, expressions)

