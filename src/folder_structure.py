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
    
    def get_workflow_folder_path(self, workflow: dict, language: str = "php") -> Path:
        """
        Obtém o caminho da pasta para um workflow baseado na linguagem.
        Todos os workflows são salvos diretamente na pasta da linguagem, sem subpastas.
        
        Args:
            workflow: Dados do workflow
            language: Linguagem de destino (ex: 'php')
            
        Returns:
            Caminho da pasta onde o arquivo deve ser salvo (output/{language}/)
        """
        # Cria pasta base para a linguagem
        language_dir = self.output_base / language
        language_dir.mkdir(exist_ok=True)
        
        # Todos os workflows são salvos diretamente na pasta da linguagem
        return language_dir
    
    def get_output_file_path(self, workflow: dict, language: str = "php") -> Path:
        """
        Obtém o caminho completo do arquivo de saída.
        
        Args:
            workflow: Dados do workflow
            language: Linguagem de destino (ex: 'php')
            
        Returns:
            Caminho completo do arquivo de saída
        """
        folder_path = self.get_workflow_folder_path(workflow, language)
        
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
    
    def get_credentials_path(self, language: str = "php") -> Path:
        """
        Obtém o caminho do arquivo de credenciais para uma linguagem específica.
        
        Args:
            language: Linguagem de destino (ex: 'php')
            
        Returns:
            Caminho completo do arquivo de credenciais
        """
        extensions = {
            'php': '.php',
            'python': '.py',
            'javascript': '.js'
        }
        extension = extensions.get(language, '.php')
        return self.credentials_dir / f"Credentials{extension}"
    
    def ensure_credentials_file(self, language: str = "php") -> bool:
        """
        Garante que o arquivo de credenciais existe na pasta de output.
        Copia do template se necessário.
        
        Args:
            language: Linguagem de destino (ex: 'php')
        
        Returns:
            True se o arquivo existe ou foi criado com sucesso
        """
        credentials_path = self.get_credentials_path(language)
        
        # Se já existe, não precisa fazer nada
        if credentials_path.exists():
            return True
        
        # Tenta copiar do template
        extensions = {
            'php': '.php',
            'python': '.py',
            'javascript': '.js'
        }
        extension = extensions.get(language, '.php')
        template_path = Path(f"templates/credentials/Credentials{extension}")
        
        if template_path.exists():
            import shutil
            # Copia o arquivo de credenciais para a pasta de output
            shutil.copy2(template_path, credentials_path)
            return True
        
        # Se não encontrou template específico, tenta copiar o PHP como fallback
        if language != 'php':
            php_template = Path("templates/credentials/Credentials.php")
            if php_template.exists():
                import shutil
                shutil.copy2(php_template, credentials_path)
                return True
        
        return False
    
    def get_relative_path_from_workflow_to_credentials(self, workflow: dict, language: str = "php") -> str:
        """
        Calcula o caminho relativo de um workflow para o arquivo de credenciais.
        
        Os workflows ficam em output/{language}/ e as credenciais em output/credentials/
        
        Args:
            workflow: Dados do workflow
            language: Linguagem de destino (ex: 'php')
            
        Returns:
            Caminho relativo (ex: '../credentials/Credentials.php')
        """
        # Extensão do arquivo de credenciais
        extensions = {
            'php': '.php',
            'python': '.py',
            'javascript': '.js'
        }
        extension = extensions.get(language, '.php')
        credentials_file = f'Credentials{extension}'
        
        # Workflow está em output/{language}/, então precisa subir 1 nível para chegar em output/
        return f'../credentials/{credentials_file}'
