"""
Classes de credenciais para APIs de IA

Este módulo fornece classes para gerenciar credenciais de diferentes
provedores de IA (OpenAI, Anthropic, OpenRouter, etc.)
"""
import os
from abc import ABC, abstractmethod
from typing import Optional


class Credentials(ABC):
    """Classe base abstrata para credenciais de API"""
    
    @abstractmethod
    def get_api_key(self) -> str:
        """
        Obtém a chave da API
        
        Returns:
            Chave da API ou string vazia se não configurada
        """
        pass


class OpenAICredentials(Credentials):
    """Credenciais para OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa credenciais OpenAI
        
        Args:
            api_key: Chave da API (opcional, usa variável de ambiente se não fornecida)
        """
        self._api_key = api_key
    
    def get_api_key(self) -> str:
        """
        Obtém a chave da API OpenAI
        
        Returns:
            Chave da API ou string vazia se não configurada
        """
        if self._api_key:
            return self._api_key
        return os.getenv('OPENAI_API_KEY', '')


class AnthropicCredentials(Credentials):
    """Credenciais para Anthropic (Claude)"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa credenciais Anthropic
        
        Args:
            api_key: Chave da API (opcional, usa variável de ambiente se não fornecida)
        """
        self._api_key = api_key
    
    def get_api_key(self) -> str:
        """
        Obtém a chave da API Anthropic
        
        Returns:
            Chave da API ou string vazia se não configurada
        """
        if self._api_key:
            return self._api_key
        return os.getenv('ANTHROPIC_API_KEY', '')


class OpenRouterCredentials(Credentials):
    """Credenciais para OpenRouter"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa credenciais OpenRouter
        
        Args:
            api_key: Chave da API (opcional, usa variável de ambiente se não fornecida)
        """
        self._api_key = api_key
    
    def get_api_key(self) -> str:
        """
        Obtém a chave da API OpenRouter
        
        Returns:
            Chave da API ou string vazia se não configurada
        """
        if self._api_key:
            return self._api_key
        return os.getenv('OPENROUTER_API_KEY', '')

