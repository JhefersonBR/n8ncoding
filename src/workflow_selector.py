"""
Módulo para seleção interativa de workflows no terminal.
"""
from typing import List, Dict


class WorkflowSelector:
    """Classe para exibir e selecionar workflows no terminal."""
    
    @staticmethod
    def display_workflows(workflows: List[Dict]) -> None:
        """
        Exibe a lista de workflows numerada no terminal.
        
        Args:
            workflows: Lista de workflows para exibir
        """
        if not workflows:
            print("Nenhum workflow encontrado.")
            return
        
        print("\n" + "=" * 60)
        print("Escolha os workflows que deseja converter:")
        print("=" * 60)
        
        for index, workflow in enumerate(workflows, start=1):
            name = workflow.get('name', 'Workflow sem nome')
            workflow_id = workflow.get('id', 'N/A')
            print(f"[{index}] {name} (ID: {workflow_id})")
        
        print("=" * 60)
    
    @staticmethod
    def select_workflows(workflows: List[Dict]) -> List[Dict]:
        """
        Permite que o usuário selecione workflows por índice.
        
        Args:
            workflows: Lista completa de workflows
            
        Returns:
            Lista com apenas os workflows selecionados
        """
        if not workflows:
            return []
        
        WorkflowSelector.display_workflows(workflows)
        
        while True:
            try:
                selection = input("\nDigite os números separados por vírgula (Ex: 1,3,4): ").strip()
                
                if not selection:
                    print("Nenhuma seleção feita. Tente novamente.")
                    continue
                
                # Processa a entrada
                indices = [int(x.strip()) for x in selection.split(',')]
                
                # Valida os índices
                selected_workflows = []
                invalid_indices = []
                
                for idx in indices:
                    if 1 <= idx <= len(workflows):
                        selected_workflows.append(workflows[idx - 1])
                    else:
                        invalid_indices.append(idx)
                
                if invalid_indices:
                    print(f"Índices inválidos: {', '.join(map(str, invalid_indices))}")
                    print(f"Por favor, escolha números entre 1 e {len(workflows)}")
                    continue
                
                if not selected_workflows:
                    print("Nenhum workflow válido selecionado. Tente novamente.")
                    continue
                
                print(f"\n✓ {len(selected_workflows)} workflow(s) selecionado(s).")
                return selected_workflows
                
            except ValueError:
                print("Entrada inválida. Por favor, digite números separados por vírgula (Ex: 1,3,4)")
            except KeyboardInterrupt:
                print("\n\nOperação cancelada pelo usuário.")
                return []
            except Exception as e:
                print(f"Erro ao processar seleção: {e}")
                continue

