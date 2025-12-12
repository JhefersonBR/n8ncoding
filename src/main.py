"""
Ponto de entrada principal do n8ncoding.
"""
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

from n8n_client import N8nClient
from workflow_selector import WorkflowSelector
from xml_loader import XMLLoader
from generator import Generator


def resolve_env_variables(value: str) -> str:
    """
    Resolve variáveis de ambiente no formato ${VAR_NAME}.
    
    Args:
        value: String que pode conter referências a variáveis de ambiente
        
    Returns:
        String com variáveis resolvidas
    """
    if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
        var_name = value[2:-1]
        env_value = os.getenv(var_name, '')
        return env_value
    return value


def resolve_config_values(config: dict) -> dict:
    """
    Resolve todas as referências a variáveis de ambiente em um dicionário de configuração.
    
    Args:
        config: Dicionário de configuração
        
    Returns:
        Dicionário com valores resolvidos
    """
    resolved = {}
    for key, value in config.items():
        if isinstance(value, dict):
            resolved[key] = resolve_config_values(value)
        elif isinstance(value, str):
            resolved[key] = resolve_env_variables(value)
        else:
            resolved[key] = value
    return resolved


def load_config() -> dict:
    """
    Carrega as configurações do arquivo settings.json.
    
    Returns:
        Dicionário com as configurações
    """
    config_path = Path(__file__).parent.parent / "config" / "settings.json"
    
    if not config_path.exists():
        print(f"Arquivo de configuração não encontrado: {config_path}")
        print("Criando arquivo de configuração padrão...")
        default_config = {
            "n8n": {
                "url": "${N8N_URL}",
                "api_key": "${N8N_API_KEY}"
            },
            "output": {
                "path": "output",
                "language": "php"
            }
        }
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        # Resolve variáveis de ambiente
        return resolve_config_values(default_config)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Resolve variáveis de ambiente
            return resolve_config_values(config)
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        return {}


def main():
    """Função principal do programa."""
    print("=" * 60)
    print("n8ncoding - Conversor de Workflows n8n para Código")
    print("=" * 60)
    
    # Carrega configurações
    config = load_config()
    
    n8n_config = config.get('n8n', {})
    output_config = config.get('output', {})
    
    n8n_url = n8n_config.get('url', 'http://localhost:5678')
    n8n_api_key = n8n_config.get('api_key', '')
    language = output_config.get('language', 'php')
    
    # Valida configurações
    if not n8n_api_key:
        print("\n⚠ Aviso: API Key do n8n não configurada.")
        print("Por favor, configure a API Key em config/settings.json")
        n8n_api_key = input("Ou digite a API Key agora (Enter para pular): ").strip()
        if not n8n_api_key:
            print("Operação cancelada.")
            return
    
    # Inicializa cliente n8n
    print(f"\nConectando ao n8n em: {n8n_url}")
    client = N8nClient(n8n_url, n8n_api_key)
    
    # Testa conexão
    if not client.test_connection():
        print("❌ Erro: Não foi possível conectar ao n8n.")
        print("Verifique a URL e a API Key nas configurações.")
        return
    
    print("✓ Conexão estabelecida com sucesso!")
    
    # Busca workflows
    print("\nBuscando workflows...")
    workflows = client.get_workflows()
    
    if not workflows:
        print("Nenhum workflow encontrado.")
        return
    
    print(f"✓ {len(workflows)} workflow(s) encontrado(s).")
    
    # Permite seleção de workflows
    selector = WorkflowSelector()
    selected_workflows = selector.select_workflows(workflows)
    
    if not selected_workflows:
        print("Nenhum workflow selecionado. Encerrando.")
        return
    
    # Inicializa componentes de geração
    xml_loader = XMLLoader()
    generator = Generator(xml_loader, language)
    
    # Processa cada workflow selecionado
    print("\n" + "=" * 60)
    print("Gerando código...")
    print("=" * 60)
    
    for workflow in selected_workflows:
        workflow_name = workflow.get('name', 'Workflow sem nome')
        workflow_id = workflow.get('id')
        
        print(f"\nProcessando: {workflow_name}")
        
        # Busca dados completos do workflow
        full_workflow = client.get_workflow(workflow_id)
        
        if not full_workflow:
            print(f"❌ Erro ao buscar dados completos do workflow {workflow_name}")
            continue
        
        # Gera a classe
        generated_code = generator.generate_class(full_workflow)
        
        if not generated_code:
            print(f"❌ Erro ao gerar código para {workflow_name}")
            continue
        
        # Salva o arquivo
        if generator.save_generated_code(full_workflow, generated_code):
            print(f"✓ {workflow_name} convertido com sucesso!")
        else:
            print(f"❌ Erro ao salvar arquivo para {workflow_name}")
    
    print("\n" + "=" * 60)
    print("Conversão concluída!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()

