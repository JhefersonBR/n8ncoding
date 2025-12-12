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
        
        # Cria pasta para credenciais
        self.credentials_dir = self.output_base / "credentials"
        self.credentials_dir.mkdir(exist_ok=True)
    
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
            # Se o workflow está em uma pasta, cria a estrutura em output/
            folder_path = self.output_base / folder_name
        else:
            # Se não está em pasta, usa output/ diretamente
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
    
    def get_credentials_path(self) -> Path:
        """
        Obtém o caminho do arquivo de credenciais.
        
        Returns:
            Caminho completo do arquivo Credentials.php
        """
        return self.credentials_dir / "Credentials.php"
    
    def ensure_credentials_file(self) -> bool:
        """
        Garante que o arquivo de credenciais existe na pasta de output.
        Copia do template se necessário.
        
        Returns:
            True se o arquivo existe ou foi criado com sucesso
        """
        credentials_path = self.get_credentials_path()
        
        # Se já existe, não precisa fazer nada
        if credentials_path.exists():
            return True
        
        # Tenta copiar do template
        template_path = Path("templates/credentials/Credentials.php")
        if template_path.exists():
            import shutil
            shutil.copy2(template_path, credentials_path)
            return True
        
        return False
    
    def get_relative_path_from_workflow_to_credentials(self, workflow: dict) -> str:
        """
        Calcula o caminho relativo de um workflow para o arquivo de credenciais.
        
        Os workflows ficam em output/ (ou subpastas) e as credenciais em output/credentials/
        
        Args:
            workflow: Dados do workflow
            
        Returns:
            Caminho relativo (ex: 'credentials/Credentials.php' ou '../credentials/Credentials.php')
        """
        workflow_folder = self.get_workflow_folder_path(workflow)
        
        # Calcula profundidade da pasta do workflow em relação ao output_base
        # Exemplo: output/Pasta1 -> depth = 1 (Pasta1)
        # Exemplo: output -> depth = 0 (raiz)
        try:
            relative_path = workflow_folder.relative_to(self.output_base)
            depth = len(relative_path.parts) if relative_path.parts else 0
        except ValueError:
            # Se workflow_folder == output_base, depth = 0
            depth = 0
        
        # Gera caminho relativo: subir 'depth' níveis até output/, depois entrar em credentials/
        if depth == 0:
            # Workflow está na raiz de output/, então credentials está em credentials/
            return 'credentials/Credentials.php'
        else:
            # Workflow está em uma subpasta, precisa subir 'depth' níveis até output/
            return '../' * depth + 'credentials/Credentials.php'
