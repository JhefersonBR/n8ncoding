"""
Módulo para gerar classes de código a partir de workflows do n8n.
"""
from typing import List, Dict, Optional
from xml_loader import XMLLoader
from node_mapper import NodeMapper
from folder_structure import FolderStructure


class Generator:
    """Classe para gerar código a partir de workflows."""
    
    def __init__(self, xml_loader: XMLLoader, language: str = "php"):
        """
        Inicializa o gerador.
        
        Args:
            xml_loader: Instância do XMLLoader
            language: Linguagem de destino
        """
        self.xml_loader = xml_loader
        self.node_mapper = NodeMapper(xml_loader)
        self.folder_structure = FolderStructure()
        self.language = language
    
    def generate_class(self, workflow: Dict) -> Optional[str]:
        """
        Gera uma classe completa a partir de um workflow.
        
        Args:
            workflow: Dados completos do workflow
            
        Returns:
            Código da classe gerada ou None em caso de erro
        """
        # Carrega o template da linguagem
        class_template = self.xml_loader.load_language_template(self.language)
        
        if not class_template:
            print(f"Erro: Template de linguagem '{self.language}' não encontrado.")
            return None
        
        # Obtém os nós do workflow
        nodes = workflow.get('nodes', [])
        
        if not nodes:
            print("Workflow não contém nós.")
            return None
        
        # Determina a ordem de execução dos nós
        ordered_nodes = self._determine_execution_order(nodes)
        
        # Gera métodos para cada nó
        methods = []
        method_calls = []
        
        for node in ordered_nodes:
            method_code = self.node_mapper.map_node_to_method(node)
            if method_code:
                methods.append(method_code)
                method_name = self.node_mapper.generate_method_name(node)
                method_calls.append(f"$this->{method_name}();")
        
        # Substitui placeholders no template
        class_name = self._generate_class_name(workflow)
        steps_methods = '\n\n    '.join(methods)
        steps_calls = '\n'.join(method_calls)
        
        generated_code = class_template.replace('{{class_name}}', class_name)
        generated_code = generated_code.replace('{{steps_methods}}', steps_methods)
        generated_code = generated_code.replace('{{steps_calls}}', steps_calls)
        
        return generated_code
    
    def _determine_execution_order(self, nodes: List[Dict]) -> List[Dict]:
        """
        Determina a ordem de execução dos nós baseado nas conexões.
        Usa ordenação topológica para garantir que os nós sejam executados
        na ordem correta (dependências primeiro).
        
        Args:
            nodes: Lista de nós do workflow
            
        Returns:
            Lista de nós ordenada pela sequência de execução
        """
        if not nodes:
            return []
        
        # Mapeia nós por ID para acesso rápido
        nodes_by_id = {node.get('id'): node for node in nodes}
        
        # Encontra o nó inicial (Start node ou nó sem conexões de entrada)
        start_nodes = []
        for node in nodes:
            node_id = node.get('id')
            has_input_connections = False
            
            # Verifica se algum outro nó aponta para este
            for other_node in nodes:
                connections = other_node.get('connections', {})
                for output_key, output_connections in connections.items():
                    # output_connections pode ser dict ou list
                    if isinstance(output_connections, dict):
                        connection_lists = output_connections.values()
                    elif isinstance(output_connections, list):
                        connection_lists = output_connections
                    else:
                        continue
                    
                    for connection_list in connection_lists:
                        if not isinstance(connection_list, list):
                            connection_list = [connection_list]
                        for connection in connection_list:
                            if isinstance(connection, dict):
                                if connection.get('node') == node_id:
                                    has_input_connections = True
                                    break
                            elif isinstance(connection, str) and connection == node_id:
                                has_input_connections = True
                                break
                        if has_input_connections:
                            break
                    if has_input_connections:
                        break
                if has_input_connections:
                    break
            
            # Se é um nó Start ou não tem entradas, é um nó inicial
            node_type = node.get('type', '')
            if node_type.endswith('.start') or node_type == 'n8n-nodes-start' or not has_input_connections:
                start_nodes.append(node)
        
        # Se não encontrou nó inicial, usa o primeiro
        if not start_nodes:
            start_nodes = [nodes[0]] if nodes else []
        
        # Ordenação topológica: visita nós na ordem correta
        ordered = []
        visited = set()
        
        def visit_node(node_id: str):
            """Visita um nó e seus dependentes em ordem topológica."""
            if node_id in visited:
                return
            
            node = nodes_by_id.get(node_id)
            if not node:
                return
            
            # Marca como visitado antes de processar dependências
            visited.add(node_id)
            
            # Primeiro adiciona o nó atual
            ordered.append(node)
            
            # Depois visita os nós conectados (próximos na sequência)
            connections = node.get('connections', {})
            for output_key, output_connections in connections.items():
                # output_connections pode ser dict ou list
                if isinstance(output_connections, dict):
                    connection_lists = output_connections.values()
                elif isinstance(output_connections, list):
                    connection_lists = output_connections
                else:
                    continue
                
                for connection_list in connection_lists:
                    if not isinstance(connection_list, list):
                        connection_list = [connection_list]
                    for connection in connection_list:
                        # connection pode ser dict ou string (node_id direto)
                        if isinstance(connection, dict):
                            target_node_id = connection.get('node')
                            if target_node_id and target_node_id not in visited:
                                visit_node(target_node_id)
                        elif isinstance(connection, str) and connection not in visited:
                            visit_node(connection)
        
        # Visita todos os nós iniciais
        for start_node in start_nodes:
            node_id = start_node.get('id')
            if node_id not in visited:
                visit_node(node_id)
        
        # Adiciona nós não visitados (caso haja desconexões)
        for node in nodes:
            node_id = node.get('id')
            if node_id not in visited:
                ordered.append(node)
        
        return ordered
    
    def _generate_class_name(self, workflow: Dict) -> str:
        """
        Gera um nome de classe baseado no workflow.
        
        Args:
            workflow: Dados do workflow
            
        Returns:
            Nome da classe em PascalCase
        """
        workflow_name = workflow.get('name', 'Workflow')
        
        # Remove caracteres especiais e normaliza
        class_name = ''.join(c for c in workflow_name if c.isalnum() or c.isspace())
        class_name = ' '.join(class_name.split())
        
        # Converte para PascalCase
        words = class_name.split()
        class_name = ''.join(word.capitalize() for word in words)
        
        # Garante que começa com letra
        if class_name and not class_name[0].isalpha():
            class_name = 'Workflow' + class_name
        
        # Se estiver vazio, usa nome padrão
        if not class_name:
            class_name = 'Workflow'
        
        return class_name
    
    def save_generated_code(self, workflow: Dict, code: str) -> bool:
        """
        Salva o código gerado no arquivo apropriado.
        
        Args:
            workflow: Dados do workflow
            code: Código gerado
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            output_path = self.folder_structure.get_output_file_path(workflow, self.language)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f"✓ Arquivo gerado: {output_path}")
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            return False

