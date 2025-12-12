---
layout: page
title: Exemplo AI Agent
lang: pt
ref: ai-agent
permalink: /pt/examples/ai-agent/
---

# Exemplo: Nó AI Agent

Este documento mostra como o nó **AI Agent** do n8n é convertido para código PHP.

## 📋 Estrutura do Nó AI Agent

O nó AI Agent no n8n permite executar ações usando modelos de IA (como GPT-4, Claude, etc.). Ele geralmente contém:

- **Prompt**: Instrução para o agente
- **Model**: Modelo de IA a ser usado (ex: gpt-4, gpt-3.5-turbo)
- **Temperature**: Criatividade da resposta (0.0 a 1.0)
- **Max Tokens**: Número máximo de tokens na resposta
- **Tools**: Ferramentas que o agente pode usar

## 🔄 Conversão para PHP

Quando um workflow contém um nó AI Agent, ele é convertido para um método PHP que:

1. Configura a requisição para a API de IA (OpenAI por padrão)
2. Envia o prompt com os parâmetros configurados
3. Processa a resposta e armazena no contexto

## 📝 Exemplo de Código Gerado

### Workflow no n8n

```
Start → AI Agent → End
```

### Código PHP Gerado

```php
<?php

class WorkflowComAIAgent {

    private array $context = [];

    public function run(array $params = []): mixed
    {
        $this->context = $params;

        $this->start();
        $this->ai_agent();

        return $this->context;
    }

    private function start(): void
    {
        // Nó: Start
        $this->context['start_output'] = [];
    }

    private function ai_agent(): void
    {
        // AI Agent - Execução de agente de IA
        $prompt = "Analise este texto e extraia as informações principais";
        $model = "gpt-4";
        $temperature = 0.7;
        $maxTokens = 2000;
        
        // Configuração da API de IA (exemplo usando OpenAI)
        $apiKey = getenv('OPENAI_API_KEY') ?: '';
        $apiUrl = 'https://api.openai.com/v1/chat/completions';
        
        $headers = [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $apiKey
        ];
        
        $body = [
            'model' => $model,
            'messages' => [
                [
                    'role' => 'system',
                    'content' => 'You are a helpful assistant.'
                ],
                [
                    'role' => 'user',
                    'content' => $prompt
                ]
            ],
            'temperature' => $temperature,
            'max_tokens' => $maxTokens
        ];
        
        // Executa requisição para API de IA
        $ch = curl_init($apiUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode === 200) {
            $responseData = json_decode($response, true);
            $aiResponse = $responseData['choices'][0]['message']['content'] ?? '';
            
            $this->context['ai_agent_output'] = [
                'response' => $aiResponse,
                'model' => $model,
                'usage' => $responseData['usage'] ?? []
            ];
        } else {
            $this->context['ai_agent_output'] = [
                'error' => 'Erro na requisição à API de IA',
                'http_code' => $httpCode,
                'response' => $response
            ];
        }
    }
}
```

## 🔧 Configuração

### Variáveis de Ambiente

Para usar o código gerado, você precisa configurar a chave da API:

```env
OPENAI_API_KEY=sua-chave-aqui
```

### Uso do Código Gerado

```php
$workflow = new WorkflowComAIAgent();
$result = $workflow->run([
    'input_data' => 'Texto para análise'
]);

// Acessar resposta da IA
$aiResponse = $result['ai_agent_output']['response'];
echo $aiResponse;
```

## 🎯 Parâmetros Suportados

O template do AI Agent suporta os seguintes parâmetros do n8n:

- ✅ **prompt**: Texto da instrução para o agente
- ✅ **model**: Modelo de IA (gpt-4, gpt-3.5-turbo, etc.)
- ✅ **temperature**: Nível de criatividade (0.0 a 1.0)
- ✅ **maxTokens**: Número máximo de tokens
- ✅ **tools**: Lista de ferramentas disponíveis (comentadas no código)

## 🔄 Personalização

Se você precisar usar uma API diferente (como Anthropic Claude, Google Gemini, etc.), você pode:

1. Editar o template `templates/nodes/aiAgent.xml`
2. Modificar a URL da API e estrutura do body
3. Ajustar o processamento da resposta

## 📚 Referências

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [n8n AI Agent Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.aiagent/)

