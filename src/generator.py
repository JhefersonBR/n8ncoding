"""
Módulo para gerar classes de código a partir de workflows do n8n.
"""
from typing import List, Dict, Optional
from xml_loader import XMLLoader
from node_mapper import NodeMapper
from folder_structure import FolderStructure
from parameter_extractor import ParameterExtractor
from expression_parser import ExpressionParser


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
        self.node_mapper = NodeMapper(xml_loader, language)
        self.folder_structure = FolderStructure()
        self.language = language
        self.parameter_extractor = ParameterExtractor()
    
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
        
        # Extrai parâmetros do primeiro nó (webhook, start, etc.)
        constructor_params = self.parameter_extractor.extract_from_workflow(workflow)
        
        # Encontra todas as expressões n8n usadas no workflow
        used_expressions = self.parameter_extractor.find_expressions_in_workflow(workflow)
        
        # Adiciona parâmetros encontrados nas expressões
        for param_name in used_expressions:
            if param_name not in constructor_params:
                constructor_params[param_name] = 'mixed'
        
        # Inicializa parser de expressões com os parâmetros encontrados
        expression_parser = ExpressionParser(constructor_params)
        
        # Atualiza o node_mapper para usar o parser
        self.node_mapper.set_expression_parser(expression_parser)
        
        # Determina a ordem de execução dos nós
        ordered_nodes = self._determine_execution_order(nodes)
        
        # Gera métodos para cada nó (agora com parsing de expressões)
        methods = []
        method_calls = []
        
        for node in ordered_nodes:
            method_code = self.node_mapper.map_node_to_method(node)
            if method_code:
                methods.append(method_code)
                method_name = self.node_mapper.generate_method_name(node)
                method_calls.append(f"$this->{method_name}();")
        
        # Atualiza parâmetros do construtor com os usados pelo parser
        final_params = expression_parser.get_constructor_params()
        if not final_params:
            final_params = constructor_params
        
        # Gera código do construtor
        constructor_code = self._generate_constructor(final_params)
        
        # Gera código de use statements para credenciais
        credentials_use = self._generate_credentials_use(workflow)
        
        # Calcula caminho relativo para credenciais
        credentials_relative_path = self.folder_structure.get_relative_path_from_workflow_to_credentials(workflow, self.language)
        
        # Substitui placeholders no template
        class_name = self._generate_class_name(workflow)
        workflow_name = workflow.get('name', 'Workflow sem nome')
        steps_methods = '\n\n    '.join(methods)
        indented_calls = '\n            '.join(method_calls)
        
        generated_code = class_template.replace('{{class_name}}', class_name)
        generated_code = generated_code.replace('{{workflow_name}}', workflow_name)
        generated_code = generated_code.replace('{{steps_methods}}', steps_methods)
        generated_code = generated_code.replace('{{steps_calls}}', indented_calls)
        generated_code = generated_code.replace('{{constructor}}', constructor_code)
        
        # Gera código de credenciais
        credentials_code = self._generate_credentials_code(workflow)
        generated_code = generated_code.replace('{{credentials_use}}', credentials_code)
        generated_code = generated_code.replace('{{credentials_import}}', credentials_code)
        generated_code = generated_code.replace('{{credentials_require}}', credentials_code)
        generated_code = generated_code.replace('{{credentials_path}}', credentials_relative_path)
        generated_code = generated_code.replace('{{version}}', '1.0.0')
        
        # Placeholders específicos por linguagem
        if self.language == "javascript":
            # Remove o nome do arquivo do caminho para usar como base
            credentials_path_base = credentials_relative_path.rsplit('/', 1)[0] if '/' in credentials_relative_path else 'credentials'
            # Substitui em todo o código gerado (incluindo métodos)
            generated_code = generated_code.replace('{{credentials_path_base}}', credentials_path_base)
            generated_code = generated_code.replace('{{module_export}}', f'module.exports = {class_name};')
        
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
    
    def _generate_constructor(self, params: Dict[str, str]) -> str:
        """
        Gera código do construtor com parâmetros para a linguagem específica.
        
        Args:
            params: Dicionário com nome => tipo dos parâmetros
            
        Returns:
            Código do construtor
        """
        if self.language == "python":
            return self._generate_constructor_python(params)
        elif self.language == "javascript":
            return self._generate_constructor_javascript(params)
        else:  # PHP (padrão)
            return self._generate_constructor_php(params)
    
    def _generate_constructor_php(self, params: Dict[str, str]) -> str:
        """Gera construtor PHP"""
        if not params:
            return """    /**
     * Construtor da classe
     * 
     * @param array $params Parâmetros do workflow
     */
    public function __construct(array $params = [])
    {
        $this->params = $params;
    }"""
        
        param_docs = []
        param_list = []
        
        for param_name, param_type in params.items():
            param_docs.append(f"     * @param {param_type} ${param_name} Parâmetro {param_name}")
            param_list.append(f"{param_type} ${param_name} = null")
        
        constructor = f"""    /**
     * Construtor da classe
     *
{chr(10).join(param_docs)}
     * @param array $params Parâmetros adicionais (opcional)
     */
    public function __construct({', '.join(param_list)}, array $params = [])
    {{
        // Parâmetros nomeados
        $this->params = [];
"""
        
        for param_name in params.keys():
            constructor += f"        $this->params['{param_name}'] = ${param_name};\n"
        
        constructor += """        
        // Parâmetros adicionais
        $this->params = array_merge($this->params, $params);
    }"""
        
        return constructor
    
    def _generate_constructor_python(self, params: Dict[str, str]) -> str:
        """Gera construtor Python"""
        constructor_body = []
        constructor_body.append("        \"\"\"")
        constructor_body.append("        Inicializa a classe do workflow.")
        
        if params:
            constructor_body.append("")
            for param_name, param_type in params.items():
                constructor_body.append(f"        {param_name}: {param_type} - Parâmetro {param_name}")
        
        constructor_body.append("        \"\"\"")
        constructor_body.append("        self.context: Dict[str, Any] = {}")
        constructor_body.append("        self.params: Dict[str, Any] = {}")
        
        if params:
            constructor_body.append("")
            for param_name in params.keys():
                constructor_body.append(f"        self.params['{param_name}'] = kwargs.get('{param_name}')")
        
        return '\n'.join(constructor_body)
    
    def _generate_constructor_javascript(self, params: Dict[str, str]) -> str:
        """Gera construtor JavaScript"""
        if not params:
            return """     /**
      * Construtor da classe
      */
     constructor() {
         this.context = {};
         this.params = {};
     }"""
        
        param_list = []
        param_docs = []
        constructor_body = []
        
        for param_name, param_type in params.items():
            param_list.append(f"{param_name} = null")
            param_docs.append(f"      * @param {{{param_type}}} {param_name} - Parâmetro {param_name}")
            constructor_body.append(f"         this.params['{param_name}'] = {param_name};")
        
        constructor = f"""     /**
      * Construtor da classe
      *
{chr(10).join(param_docs)}
      */
     constructor({', '.join(param_list)}) {{
         this.context = {{}};
         this.params = {{}};
         
{chr(10).join(constructor_body)}
     }}"""
        
        return constructor
    
    def _generate_credentials_code(self, workflow: Dict) -> str:
        """
        Gera código de import/use statements para classes de credenciais necessárias.
        Suporta PHP, Python e JavaScript.
        
        Args:
            workflow: Dados do workflow
            
        Returns:
            Código de import/use statements
        """
        nodes = workflow.get('nodes', [])
        credentials_needed = set()
        
        for node in nodes:
            node_type = node.get('type', '').lower()
            params = node.get('parameters', {})
            
            if 'aiagent' in node_type or 'langchain' in node_type:
                provider = params.get('provider', 'openai')
                if isinstance(provider, dict):
                    provider = provider.get('value', 'openai')
                
                if 'anthropic' in provider.lower() or 'claude' in provider.lower():
                    credentials_needed.add('AnthropicCredentials')
                elif 'openrouter' in provider.lower():
                    credentials_needed.add('OpenRouterCredentials')
                else:
                    credentials_needed.add('OpenAICredentials')
        
        if not credentials_needed:
            return ''
        
        if self.language == "python":
            # Python imports
            imports = []
            for cred_class in sorted(list(credentials_needed)):
                imports.append(f"from {cred_class} import {cred_class}")
            return '\n'.join(imports)
        elif self.language == "javascript":
            # JavaScript requires - o caminho será ajustado no template
            requires = []
            for cred_class in sorted(list(credentials_needed)):
                # Usa placeholder que será substituído com o caminho relativo correto
                requires.append(f"const {{ {cred_class} }} = require('{{credentials_path_base}}/{cred_class}.js');")
            return '\n'.join(requires)
        else:  # PHP
            # PHP use statements
            use_statements = []
            for cred_class in sorted(list(credentials_needed)):
                use_statements.append(f"use {cred_class};")
            return '\n'.join(use_statements)
    
    def _generate_credentials_use(self, workflow: Dict) -> str:
        """Alias para compatibilidade"""
        return self._generate_credentials_code(workflow) + '\n'
    
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
            # Garante que o arquivo de credenciais existe para a linguagem específica
            self.folder_structure.ensure_credentials_file(self.language)
            
            output_path = self.folder_structure.get_output_file_path(workflow, self.language)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f"✓ Arquivo gerado: {output_path}")
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            import traceback
            traceback.print_exc()
            return False

