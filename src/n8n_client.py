"""
Módulo para comunicação com a API do n8n.
"""
import requests
import json
from typing import List, Dict, Optional


class N8nClient:
    """Cliente para interagir com a API do n8n."""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Inicializa o cliente n8n.
        
        Args:
            base_url: URL base do n8n (ex: http://localhost:5678)
            api_key: Chave de API do n8n
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'X-N8N-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
    
    def get_workflows(self) -> List[Dict]:
        """
        Busca todos os workflows disponíveis.
        
        Returns:
            Lista de workflows com informações básicas
        """
        try:
            url = f"{self.base_url}/api/v1/workflows"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar workflows: {e}")
            return []
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """
        Busca um workflow específico pelo ID.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            Dados completos do workflow ou None em caso de erro
        """
        try:
            url = f"{self.base_url}/api/v1/workflows/{workflow_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar workflow {workflow_id}: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o n8n.
        
        Returns:
            True se a conexão foi bem-sucedida, False caso contrário
        """
        try:
            url = f"{self.base_url}/api/v1/workflows"
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

