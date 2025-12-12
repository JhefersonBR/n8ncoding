"""
Módulo para mapear nós do n8n em métodos de código.
"""
import json
from typing import Dict, Optional
from xml_loader import XMLLoader


class NodeMapper:
    """Classe para mapear nós do workflow em métodos de código."""
    
    def __init__(self, xml_loader: XMLLoader, language: str = "php"):
        """
        Inicializa o mapeador de nós.
        
        Args:
            xml_loader: Instância do XMLLoader para carregar templates
            language: Linguagem de destino (ex: 'php', 'python', 'javascript')
        """
        self.xml_loader = xml_loader
        self.language = language
        self.expression_parser = None
    
    def set_expression_parser(self, parser):
        """
        Define o parser de expressões a ser usado.
        
        Args:
            parser: Instância de ExpressionParser
        """
        self.expression_parser = parser
    
    def generate_method_name(self, node: Dict) -> str:
        """
        Gera um nome de método baseado no nome descritivo do nó.
        Converte para camelCase válido em PHP.
        
        Args:
            node: Dados do nó do workflow
            
        Returns:
            Nome do método em formato camelCase (ex: 'aiAgent', 'sendEmail', 'updateCrm')
        """
        # Usa o nome descritivo do nó (não o tipo)
        node_name = node.get('name', 'node')
        
        if not node_name or node_name.strip() == '':
            # Fallback: tenta extrair nome do tipo se não houver nome descritivo
            node_type = node.get('type', 'unknown')
            # Extrai o último segmento do tipo como fallback
            parts = node_type.split('.')
            node_name = parts[-1] if parts else 'node'
        
        # Converte para camelCase
        method_name = self._to_camel_case(node_name)
        
        # Garante que começa com letra minúscula (convenção PHP)
        if method_name and method_name[0].isupper():
            method_name = method_name[0].lower() + method_name[1:]
        
        # Garante que começa com letra
        if not method_name or not method_name[0].isalpha():
            method_name = 'node' + (method_name.capitalize() if method_name else '')
        
        # Evita palavras reservadas do PHP
        php_reserved = {
            'if', 'else', 'elseif', 'while', 'for', 'foreach', 'switch', 'case',
            'default', 'break', 'continue', 'return', 'function', 'class', 'interface',
            'trait', 'namespace', 'use', 'as', 'public', 'private', 'protected', 'static',
            'abstract', 'final', 'const', 'var', 'new', 'clone', 'instanceof', 'try',
            'catch', 'finally', 'throw', 'extends', 'implements', 'self', 'parent',
            'true', 'false', 'null', 'array', 'string', 'int', 'float', 'bool',
            'void', 'mixed', 'object', 'callable', 'iterable'
        }
        
        if method_name.lower() in php_reserved:
            method_name = method_name + 'Node'
        
        return method_name
    
    def _to_camel_case(self, text: str) -> str:
        """
        Converte um texto para camelCase válido em PHP.
        Remove acentos e caracteres especiais.
        
        Exemplos:
        - "AI Agent" -> "aiAgent"
        - "Send Email" -> "sendEmail"
        - "Update CRM" -> "updateCrm"
        - "webhook-start" -> "webhookStart"
        - "Conselheiro Bíblico" -> "conselheiroBiblico"
        
        Args:
            text: Texto a ser convertido
            
        Returns:
            Texto em camelCase válido em PHP
        """
        if not text:
            return 'node'
        
        # Remove acentos e caracteres especiais
        import unicodedata
        import re
        
        # Normaliza para NFD (decompõe caracteres acentuados)
        text = unicodedata.normalize('NFD', text)
        # Remove diacríticos (acentos)
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Substitui caracteres especiais por espaços
        text = re.sub(r'[^\w\s]', ' ', text)
        # Divide por espaços, hífens, underscores
        words = re.split(r'[\s\-_]+', text)
        
        # Remove palavras vazias
        words = [w for w in words if w]
        
        if not words:
            return 'node'
        
        # Primeira palavra em minúscula, demais com primeira letra maiúscula
        result = words[0].lower()
        for word in words[1:]:
            if word:
                # Capitaliza apenas a primeira letra, mantém resto como está
                result += word[0].upper() + word[1:].lower()
        
        # Remove caracteres não alfanuméricos (mantém apenas letras ASCII e números)
        result = ''.join(c for c in result if c.isalnum() and ord(c) < 128)
        
        return result if result else 'node'
    
    def map_node_to_method(self, node: Dict) -> Optional[str]:
        """
        Mapeia um nó do workflow em um método de código.
        
        Args:
            node: Dados do nó do workflow
            
        Returns:
            Código do método gerado ou None em caso de erro
        """
        node_type = node.get('type', '')
        original_type = node_type
        
        # Normaliza tipos de AI Agent
        if 'langchain' in node_type.lower() and 'agent' in node_type.lower():
            # Tipo LangChain Agent: @n8n/n8n-nodes-langchain.agent
            node_type = 'aiAgent'
        elif node_type.startswith('n8n-nodes-'):
            node_type = node_type.replace('n8n-nodes-', '')
        elif node_type.startswith('@n8n/'):
            # Remove prefixo @n8n/ e pega apenas o nome do nó
            parts = node_type.split('.')
            if len(parts) > 1:
                node_type = parts[-1]  # Pega a última parte após o ponto
        
        # Carrega o template do nó para a linguagem específica
        template = self.xml_loader.load_node_template(node_type, self.language)
        
        if not template:
            # Template padrão se não encontrar específico
            return self._generate_default_method(node)
        
        method_name = self.generate_method_name(node)
        method_template = template['method']
        
        # Substitui placeholders básicos
        method_code = method_template.replace('{{method_name}}', method_name)
        
        # Gera código específico baseado no tipo de nó
        generated_code = self._generate_node_code(node, node_type)
        method_code = method_code.replace('{{generated_code}}', generated_code)
        
        # Substitui outros placeholders comuns
        method_code = self._replace_common_placeholders(method_code, node)
        
        # Se o template não tinha {{generated_code}}, adiciona o código gerado
        if '{{generated_code}}' in method_code:
            method_code = method_code.replace('{{generated_code}}', generated_code)
        
        return method_code
    
    def _generate_default_method(self, node: Dict) -> str:
        """
        Gera um método padrão quando não há template específico.
        
        Args:
            node: Dados do nó
            
        Returns:
            Código do método padrão
        """
        method_name = self.generate_method_name(node)
        node_name = node.get('name', 'Node')
        
        return f"""private function {method_name}(): void
{{
    // Nó: {node_name}
    // Tipo: {node.get('type', 'unknown')}
    // TODO: Implementar lógica específica deste nó
    $this->context['{method_name}_output'] = [];
}}"""
    
    def _generate_node_code(self, node: Dict, node_type: str) -> str:
        """
        Gera código específico para um tipo de nó.
        
        Args:
            node: Dados do nó
            node_type: Tipo do nó
            
        Returns:
            Código gerado para o nó
        """
        parameters = node.get('parameters', {})
        method_name = self.generate_method_name(node)
        output_key = f"{method_name}_output"
        
        if node_type == 'function':
            # Para nós function, tenta pegar o código JavaScript
            code = parameters.get('functionCode', '')
            if code:
                # Converte código JavaScript básico para PHP (simplificado)
                # TODO: Implementar conversão mais completa de JS para PHP
                php_code = code.replace('$input', '$this->context')
                php_code = php_code.replace('items', '$this->context')
                return f"// Código convertido do n8n\n    // {code[:100]}...\n    $this->context['{output_key}'] = [];"
            return f"// Função vazia\n    $this->context['{output_key}'] = [];"
        
        elif node_type == 'httpRequest':
            # Para HTTP Request - o template já tem a lógica completa
            # Aqui apenas retornamos um placeholder que será substituído
            return f"// HTTP Request processado pelo template"
        
        # Código genérico para outros tipos
        node_name = node.get('name', 'Node')
        return f"// Processamento do nó {node_type}: {node_name}\n    $this->context['{output_key}'] = [];"
    
    def _replace_common_placeholders(self, code: str, node: Dict) -> str:
        """
        Substitui placeholders comuns no código.
        
        Args:
            code: Código com placeholders
            node: Dados do nó
            
        Returns:
            Código com placeholders substituídos
        """
        method_name = self.generate_method_name(node)
        output_key = f"{method_name}_output"
        parameters = node.get('parameters', {})
        
        # Processa headers se existirem
        headers = parameters.get('options', {}).get('headers', {})
        headers_array = []
        if isinstance(headers, dict):
            for key, value in headers.items():
                if isinstance(value, dict) and 'value' in value:
                    headers_array.append(f"'{key}: {value['value']}'")
                else:
                    headers_array.append(f"'{key}: {value}'")
        headers_str = '[' + ', '.join(headers_array) + ']' if headers_array else '[]'
        
        # Processa body
        body = parameters.get('body', {})
        body_str = 'null'
        if body:
            try:
                body_str = json.dumps(body, ensure_ascii=False, indent=8)
                body_str = body_str.replace('\n', '\n    ')
            except:
                body_str = 'null'
        
        # Processa parâmetros específicos do AI Agent
        prompt = parameters.get('prompt', '') or parameters.get('text', '')
        if isinstance(prompt, dict):
            if 'value' in prompt:
                prompt = prompt['value']
            elif 'text' in prompt:
                prompt = prompt['text']
        prompt_str = f'"{prompt}"' if prompt else '""'
        
        model = parameters.get('model', '') or parameters.get('modelName', 'gpt-3.5-turbo')
        if isinstance(model, dict) and 'value' in model:
            model = model['value']
        model_str = f'"{model}"'
        
        temperature = parameters.get('temperature', 0.7)
        if isinstance(temperature, dict) and 'value' in temperature:
            temperature = temperature['value']
        temperature_str = str(float(temperature))
        
        max_tokens = parameters.get('maxTokens', 1000) or parameters.get('max_tokens', 1000)
        if isinstance(max_tokens, dict) and 'value' in max_tokens:
            max_tokens = max_tokens['value']
        max_tokens_str = str(int(max_tokens))
        
        # System message
        system_message = parameters.get('systemMessage', '') or parameters.get('system_message', '')
        if isinstance(system_message, dict) and 'value' in system_message:
            system_message = system_message['value']
        system_message_str = f'"{system_message}"' if system_message else '""'
        
        # API Provider (OpenAI, Anthropic, OpenRouter, etc.)
        api_provider = parameters.get('provider', 'openai')
        if isinstance(api_provider, dict) and 'value' in api_provider:
            api_provider = api_provider['value']
        api_provider_str = f'"{api_provider}"'
        
        # API Key e URL baseado no provider
        api_key_env = 'OPENAI_API_KEY'
        api_url_default = 'https://api.openai.com/v1/chat/completions'
        
        if 'anthropic' in api_provider.lower() or 'claude' in api_provider.lower():
            api_key_env = 'ANTHROPIC_API_KEY'
            api_url_default = 'https://api.anthropic.com/v1/messages'
        elif 'openrouter' in api_provider.lower():
            api_key_env = 'OPENROUTER_API_KEY'
            api_url_default = 'https://openrouter.ai/api/v1/chat/completions'
        
        api_key_str = f"getenv('{api_key_env}') ?: ''"
        api_url_str = f"'{api_url_default}'"
        
        # Código para tools (se houver)
        tools_code = ''
        tools = parameters.get('tools', []) or parameters.get('availableTools', [])
        if tools and isinstance(tools, list) and len(tools) > 0:
            tools_code = "\n            // Tools disponíveis para o agente\n"
            tools_code += "            $tools = [];\n"
            for i, tool in enumerate(tools):
                tool_name = tool.get('name', f'tool_{i}')
                tool_desc = tool.get('description', '')
                tools_code += f"            $tools[] = ['name' => '{tool_name}', 'description' => '{tool_desc}'];\n"
            tools_code += "            $body['tools'] = $tools;\n"
        
        # Código adicional para ações/tools do agente (se houver)
        additional_code = ''
        if tools and isinstance(tools, list) and len(tools) > 0:
            additional_code = "\n        // Tools configuradas e disponíveis para uso"
        
        replacements = {
            '{{output_key}}': output_key,
            '{{url}}': f'"{parameters.get("url", "")}"',
            '{{method}}': f'"{parameters.get("method", "GET")}"',
            '{{headers}}': headers_str,
            '{{body}}': body_str,
            '{{prompt}}': prompt_str,
            '{{model}}': model_str,
            '{{temperature}}': temperature_str,
            '{{max_tokens}}': max_tokens_str,
            '{{system_message}}': system_message_str,
            '{{api_provider}}': api_provider_str,
            '{{api_key}}': api_key_str,
            '{{api_url}}': api_url_str,
            '{{tools_code}}': tools_code,
            '{{additional_code}}': additional_code
        }
        
        for placeholder, value in replacements.items():
            code = code.replace(placeholder, str(value))
        
        return code

