"""
Módulo para replicar a estrutura de pastas do n8n.
"""
import os
from pathlib import Path
from typing import Optional


class FolderStructure:
    """Classe para gerenciar a estrutura de pastas de saída."""
    
    def __init__(self, output_base: str = "output"):
        """
        Inicializa o gerenciador de estrutura de pastas.
        
        Args:
            output_base: Diretório base de saída
        """
        self.output_base = Path(output_base)
        self.output_base.mkdir(exist_ok=True)
    
    def get_workflow_folder_path(self, workflow: dict) -> Path:
        """
        Obtém o caminho da pasta para um workflow baseado na estrutura do n8n.
        
        Args:
            workflow: Dados do workflow
            
        Returns:
            Caminho da pasta onde o arquivo deve ser salvo
        """
        # Tenta obter a pasta do workflow do n8n
        folder = workflow.get('folder', {})
        folder_name = folder.get('name', '') if isinstance(folder, dict) else ''
        
        if folder_name:
            # Se o workflow está em uma pasta, cria a estrutura
            folder_path = self.output_base / folder_name
        else:
            # Se não está em pasta, usa a raiz do output
            folder_path = self.output_base
        
        # Cria a pasta se não existir
        folder_path.mkdir(parents=True, exist_ok=True)
        
        return folder_path
    
    def get_output_file_path(self, workflow: dict, language: str = "php") -> Path:
        """
        Obtém o caminho completo do arquivo de saída.
        
        Args:
            workflow: Dados do workflow
            language: Linguagem de destino (ex: 'php')
            
        Returns:
            Caminho completo do arquivo de saída
        """
        folder_path = self.get_workflow_folder_path(workflow)
        
        # Gera nome do arquivo baseado no nome do workflow
        workflow_name = workflow.get('name', 'workflow')
        safe_name = self._sanitize_filename(workflow_name)
        
        # Extensão baseada na linguagem
        extensions = {
            'php': '.php',
            'python': '.py',
            'javascript': '.js'
        }
        extension = extensions.get(language, '.txt')
        
        return folder_path / f"{safe_name}{extension}"
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitiza um nome de arquivo removendo caracteres inválidos.
        
        Args:
            filename: Nome original
            
        Returns:
            Nome sanitizado
        """
        # Remove caracteres inválidos para nomes de arquivo
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove espaços múltiplos
        filename = ' '.join(filename.split())
        
        # Substitui espaços por underscores
        filename = filename.replace(' ', '_')
        
        return filename

