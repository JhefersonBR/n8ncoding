# Exemplo: Template AI Agent para PHP

Este documento mostra como o template do nó **AI Agent** gera código PHP completo e funcional.

## 🎯 Funcionalidades do Template

O template PHP para AI Agent inclui:

- ✅ **Suporte a múltiplos provedores**: OpenAI, Anthropic, OpenRouter
- ✅ **Documentação PHPDoc completa**
- ✅ **Tratamento robusto de erros**
- ✅ **Suporte a system messages**
- ✅ **Configuração de tools/funções**
- ✅ **Logging e debug**
- ✅ **Múltiplos formatos de resposta**
- ✅ **Timeout configurável**

## 📝 Exemplo de Código Gerado

### Workflow no n8n

```
Start → AI Agent (LangChain) → End
```

### Código PHP Gerado

```php
<?php

class ConselheiroBíblico {

    private array $context = [];

    public function run(array $params = []): mixed
    {
        $this->context = $params;
        $this->ai_agent();
        return $this->context;
    }

    /**
     * Executa um agente de IA
     * 
     * Este método executa um agente de IA usando o prompt e modelo configurados.
     * Suporta múltiplos provedores de IA (OpenAI, Anthropic, OpenRouter, etc.)
     * 
     * @return void
     * @throws \Exception Se houver erro na comunicação com a API de IA
     */
    private function ai_agent(): void
    {
        try {
            // Parâmetros do agente
            $prompt = "Você é um conselheiro bíblico. Responda com sabedoria.";
            $model = "gpt-4";
            $temperature = 0.7;
            $maxTokens = 2000;
            $systemMessage = "Você é um assistente útil e respeitoso.";
            
            // Obtém configurações da API
            $apiProvider = "openai";
            $apiKey = getenv('OPENAI_API_KEY') ?: '';
            $apiUrl = 'https://api.openai.com/v1/chat/completions';
            
            // Prepara headers
            $headers = [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $apiKey
            ];
            
            // Prepara mensagens
            $messages = [];
            
            // Adiciona mensagem do sistema se fornecida
            if (!empty($systemMessage)) {
                $messages[] = [
                    'role' => 'system',
                    'content' => $systemMessage
                ];
            }
            
            // Adiciona mensagem do usuário
            $messages[] = [
                'role' => 'user',
                'content' => $prompt
            ];
            
            // Prepara body da requisição
            $body = [
                'model' => $model,
                'messages' => $messages,
                'temperature' => (float)$temperature,
                'max_tokens' => (int)$maxTokens
            ];
            
            // Executa requisição para API de IA
            $ch = curl_init($apiUrl);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
            curl_setopt($ch, CURLOPT_TIMEOUT, 60);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
            
            $response = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $curlError = curl_error($ch);
            curl_close($ch);
            
            // Processa resposta
            if ($httpCode === 200 && !empty($response)) {
                $responseData = json_decode($response, true);
                
                if (json_last_error() !== JSON_ERROR_NONE) {
                    throw new \Exception('Erro ao decodificar resposta JSON: ' . json_last_error_msg());
                }
                
                // Extrai resposta baseado no formato da API
                $aiResponse = '';
                if (isset($responseData['choices'][0]['message']['content'])) {
                    // Formato OpenAI
                    $aiResponse = $responseData['choices'][0]['message']['content'];
                } elseif (isset($responseData['content'][0]['text'])) {
                    // Formato Anthropic
                    $aiResponse = $responseData['content'][0]['text'];
                }
                
                // Armazena resultado no contexto
                $this->context['ai_agent_output'] = [
                    'success' => true,
                    'response' => $aiResponse,
                    'model' => $model,
                    'provider' => $apiProvider,
                    'usage' => $responseData['usage'] ?? [],
                    'finish_reason' => $responseData['choices'][0]['finish_reason'] ?? null,
                    'raw_response' => $responseData
                ];
            } else {
                // Tratamento de erro...
            }
        } catch (\Exception $e) {
            // Tratamento de exceção...
        }
    }
}
```

## 🔧 Configuração

### Variáveis de Ambiente

Configure a chave da API conforme o provedor:

```env
# Para OpenAI
OPENAI_API_KEY=sk-...

# Para Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Para OpenRouter
OPENROUTER_API_KEY=sk-or-...
```

### Uso do Código Gerado

```php
$workflow = new ConselheiroBíblico();

// Executa o workflow
$result = $workflow->run([
    'user_input' => 'Preciso de conselho sobre...'
]);

// Acessa a resposta da IA
if ($result['ai_agent_output']['success']) {
    echo $result['ai_agent_output']['response'];
} else {
    echo "Erro: " . $result['ai_agent_output']['error'];
}
```

## 🎨 Recursos Avançados

### Suporte a Tools/Funções

Se o workflow tiver tools configuradas, o código gerado incluirá:

```php
// Tools disponíveis para o agente
$tools = [];
$tools[] = ['name' => 'search_bible', 'description' => 'Busca versículos'];
$tools[] = ['name' => 'get_commentary', 'description' => 'Obtém comentários'];
$body['tools'] = $tools;
```

### System Messages

O template suporta system messages para definir o comportamento do agente:

```php
$systemMessage = "Você é um conselheiro bíblico sábio e compassivo.";
```

### Múltiplos Provedores

O template detecta automaticamente o provedor e configura a URL correta:

- **OpenAI**: `https://api.openai.com/v1/chat/completions`
- **Anthropic**: `https://api.anthropic.com/v1/messages`
- **OpenRouter**: `https://openrouter.ai/api/v1/chat/completions`

## 📊 Estrutura de Resposta

O contexto armazena informações completas:

```php
[
    'success' => true,
    'response' => 'Resposta da IA...',
    'model' => 'gpt-4',
    'provider' => 'openai',
    'usage' => [
        'prompt_tokens' => 100,
        'completion_tokens' => 200,
        'total_tokens' => 300
    ],
    'finish_reason' => 'stop',
    'raw_response' => [...] // Resposta completa da API
]
```

## 🐛 Tratamento de Erros

O template inclui tratamento robusto:

- Validação de resposta JSON
- Tratamento de erros HTTP
- Captura de exceções
- Logging opcional (quando `debug` está ativo)
- Informações detalhadas de erro no contexto

## 🔄 Tipos de Nós Suportados

O template funciona com diferentes tipos de nós AI Agent:

- `n8n-nodes-aiAgent`
- `@n8n/n8n-nodes-langchain.agent`
- Qualquer nó que contenha "agent" no tipo

## 📚 Referências

- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [Anthropic API](https://docs.anthropic.com/claude/reference)
- [OpenRouter API](https://openrouter.ai/docs)

