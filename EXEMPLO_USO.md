# Exemplo de Uso do n8ncoding

## Configuração Inicial

1. Configure o arquivo `config/settings.json`:

```json
{
  "n8n": {
    "url": "http://localhost:5678",
    "api_key": "sua-api-key-aqui"
  },
  "output": {
    "path": "output",
    "language": "php"
  }
}
```

## Executando o Programa

```bash
python src/main.py
```

## Fluxo de Execução

1. **Conexão com n8n**: O programa tenta conectar à API do n8n usando as credenciais configuradas.

2. **Listagem de Workflows**: Todos os workflows disponíveis são listados no terminal.

3. **Seleção Interativa**: O usuário seleciona quais workflows deseja converter:
   ```
   Escolha os workflows que deseja converter:
   ============================================================
   [1] Enviar Email Automático (ID: abc123)
   [2] Atualizar CRM (ID: def456)
   [3] Extrair Dados do Google Sheets (ID: ghi789)
   ============================================================
   
   Digite os números separados por vírgula (Ex: 1,3,4): 1,3
   ```

4. **Geração de Código**: Para cada workflow selecionado:
   - Os nós são ordenados pela sequência de execução
   - Cada nó é mapeado para um método privado
   - A classe PHP é gerada usando os templates
   - O arquivo é salvo na pasta `output/` respeitando a estrutura de pastas do n8n

## Exemplo de Classe Gerada

```php
<?php

class EnviarEmailAutomatico {

    private array $context = [];

    public function run(array $params = []): mixed
    {
        $this->context = $params;

        $this->start_node();
        $this->http_request_node();
        $this->function_node();

        return $this->context;
    }

    private function start_node(): void
    {
        // Nó: Start
        // Tipo: n8n-nodes-start
        // TODO: Implementar lógica específica deste nó
        $this->context['start_node_output'] = [];
    }

    private function http_request_node(): void
    {
        $url = "https://api.example.com/endpoint";
        $method = "POST";
        $headers = [];
        $body = null;
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        if ($body) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
        }
        
        $response = curl_exec($ch);
        $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        $this->context['http_request_node_output'] = json_decode($response, true);
    }

    private function function_node(): void
    {
        // Código convertido do n8n
        $this->context['function_node_output'] = [];
    }
}
```

## Estrutura de Saída

Os arquivos gerados são salvos em `output/`, mantendo a mesma estrutura de pastas do n8n:

```
output/
├── Pasta1/
│   └── Workflow1.php
├── Pasta2/
│   └── Workflow2.php
└── WorkflowSemPasta.php
```

## Adicionando Novos Templates

Para adicionar suporte a um novo tipo de nó:

1. Crie um arquivo XML em `templates/nodes/` com o nome do tipo de nó (ex: `myCustomNode.xml`)

2. Use os placeholders disponíveis:
   - `{{method_name}}`: Nome do método gerado
   - `{{generated_code}}`: Código específico gerado para o nó
   - `{{output_key}}`: Chave para armazenar a saída no contexto
   - `{{url}}`, `{{method}}`, `{{headers}}`, `{{body}}`: Para requisições HTTP

3. O sistema automaticamente carregará o template quando encontrar um nó desse tipo.

## Troubleshooting

### Erro de Conexão
- Verifique se a URL do n8n está correta
- Confirme que a API Key está configurada corretamente
- Verifique se o n8n está rodando e acessível

### Nenhum Workflow Encontrado
- Verifique se há workflows criados no n8n
- Confirme que a API Key tem permissão para listar workflows

### Template Não Encontrado
- Se um tipo de nó não tem template específico, será usado um template padrão
- Crie um template personalizado em `templates/nodes/` se necessário

