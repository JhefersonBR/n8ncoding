"""
Módulo para carregar e processar templates XML.
"""
import os
import xml.etree.ElementTree as ET
from typing import Optional, Dict
from pathlib import Path


class XMLLoader:
    """Classe para carregar templates XML."""
    
    def __init__(self, templates_dir: str = "templates"):
        """
        Inicializa o carregador de XML.
        
        Args:
            templates_dir: Diretório base dos templates
        """
        self.templates_dir = Path(templates_dir)
    
    def load_language_template(self, language: str) -> Optional[str]:
        """
        Carrega o template XML de uma linguagem.
        
        Args:
            language: Nome da linguagem (ex: 'php')
            
        Returns:
            Conteúdo do template da classe ou None se não encontrado
        """
        template_path = self.templates_dir / "languages" / f"{language}.xml"
        
        if not template_path.exists():
            print(f"Template de linguagem não encontrado: {template_path}")
            return None
        
        try:
            tree = ET.parse(template_path)
            root = tree.getroot()
            
            class_elem = root.find('class')
            if class_elem is not None:
                return class_elem.text.strip()
            
            return None
        except Exception as e:
            print(f"Erro ao carregar template de linguagem: {e}")
            return None
    
    def load_node_template(self, node_type: str) -> Optional[Dict[str, str]]:
        """
        Carrega o template XML de um tipo de nó.
        
        Args:
            node_type: Tipo do nó (ex: 'function', 'httpRequest')
            
        Returns:
            Dicionário com 'name' e 'method' ou None se não encontrado
        """
        template_path = self.templates_dir / "nodes" / f"{node_type}.xml"
        
        if not template_path.exists():
            print(f"Template de nó não encontrado: {template_path}")
            return None
        
        try:
            tree = ET.parse(template_path)
            root = tree.getroot()
            
            name_elem = root.find('name')
            method_elem = root.find('method')
            
            if name_elem is not None and method_elem is not None:
                return {
                    'name': name_elem.text.strip() if name_elem.text else node_type,
                    'method': method_elem.text.strip() if method_elem.text else ''
                }
            
            return None
        except Exception as e:
            print(f"Erro ao carregar template de nó: {e}")
            return None
    
    def list_available_node_templates(self) -> list:
        """
        Lista todos os templates de nós disponíveis.
        
        Returns:
            Lista de nomes de templates disponíveis
        """
        nodes_dir = self.templates_dir / "nodes"
        
        if not nodes_dir.exists():
            return []
        
        templates = []
        for file in nodes_dir.glob("*.xml"):
            templates.append(file.stem)
        
        return templates

