---
layout: page
title: AI Agent Example
lang: en
ref: ai-agent
permalink: /en/examples/ai-agent/
---

# Example: AI Agent Node

This document shows how the n8n **AI Agent** node is converted to PHP code.

## 📋 AI Agent Node Structure

The AI Agent node in n8n allows executing actions using AI models (like GPT-4, Claude, etc.). It generally contains:

- **Prompt**: Instruction for the agent
- **Model**: AI model to be used (e.g., gpt-4, gpt-3.5-turbo)
- **Temperature**: Response creativity (0.0 to 1.0)
- **Max Tokens**: Maximum number of tokens in response
- **Tools**: Tools the agent can use

## 🔄 Conversion to PHP

When a workflow contains an AI Agent node, it is converted to a PHP method that:

1. Configures the request to the AI API (OpenAI by default)
2. Sends the prompt with configured parameters
3. Processes the response and stores it in context

## 📝 Generated Code Example

### Workflow in n8n

```
Start → AI Agent → End
```

### Generated PHP Code

```php
<?php

class WorkflowWithAIAgent {

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
        // Node: Start
        $this->context['start_output'] = [];
    }

    private function ai_agent(): void
    {
        // AI Agent - AI agent execution
        $prompt = "Analyze this text and extract main information";
        $model = "gpt-4";
        $temperature = 0.7;
        $maxTokens = 2000;
        
        // AI API configuration (example using OpenAI)
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
        
        // Execute request to AI API
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
                'error' => 'Error in AI API request',
                'http_code' => $httpCode,
                'response' => $response
            ];
        }
    }
}
```

## 🔧 Configuration

### Environment Variables

To use the generated code, you need to configure the API key:

```env
OPENAI_API_KEY=your-key-here
```

### Usage of Generated Code

```php
$workflow = new WorkflowWithAIAgent();
$result = $workflow->run([
    'input_data' => 'Text for analysis'
]);

// Access AI response
$aiResponse = $result['ai_agent_output']['response'];
echo $aiResponse;
```

## 🎯 Supported Parameters

The AI Agent template supports the following n8n parameters:

- ✅ **prompt**: Instruction text for the agent
- ✅ **model**: AI model (gpt-4, gpt-3.5-turbo, etc.)
- ✅ **temperature**: Creativity level (0.0 to 1.0)
- ✅ **maxTokens**: Maximum number of tokens
- ✅ **tools**: List of available tools (commented in code)

## 🔄 Customization

If you need to use a different API (like Anthropic Claude, Google Gemini, etc.), you can:

1. Edit the template `templates/nodes/aiAgent.xml`
2. Modify the API URL and body structure
3. Adjust response processing

## 📚 References

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [n8n AI Agent Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.aiagent/)

