# Example: AI Agent Template for PHP

This document shows how the **AI Agent** node template generates complete and functional PHP code.

## 🎯 Template Features

The PHP template for AI Agent includes:

- ✅ **Multiple provider support**: OpenAI, Anthropic, OpenRouter
- ✅ **Complete PHPDoc documentation**
- ✅ **Robust error handling**
- ✅ **System message support**
- ✅ **Tools/functions configuration**
- ✅ **Logging and debug**
- ✅ **Multiple response formats**
- ✅ **Configurable timeout**

## 📝 Generated Code Example

### Workflow in n8n

```
Start → AI Agent (LangChain) → End
```

### Generated PHP Code

```php
<?php

class BiblicalCounselor {

    private array $context = [];

    public function run(array $params = []): mixed
    {
        $this->context = $params;
        $this->ai_agent();
        return $this->context;
    }

    /**
     * Executes an AI agent
     * 
     * This method executes an AI agent using the configured prompt and model.
     * Supports multiple AI providers (OpenAI, Anthropic, OpenRouter, etc.)
     * 
     * @return void
     * @throws \Exception If there is an error communicating with the AI API
     */
    private function ai_agent(): void
    {
        try {
            // Agent parameters
            $prompt = "You are a biblical counselor. Respond with wisdom.";
            $model = "gpt-4";
            $temperature = 0.7;
            $maxTokens = 2000;
            $systemMessage = "You are a helpful and respectful assistant.";
            
            // Gets API configuration
            $apiProvider = "openai";
            $apiKey = getenv('OPENAI_API_KEY') ?: '';
            $apiUrl = 'https://api.openai.com/v1/chat/completions';
            
            // Prepares headers
            $headers = [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $apiKey
            ];
            
            // Prepares messages
            $messages = [];
            
            // Adds system message if provided
            if (!empty($systemMessage)) {
                $messages[] = [
                    'role' => 'system',
                    'content' => $systemMessage
                ];
            }
            
            // Adds user message
            $messages[] = [
                'role' => 'user',
                'content' => $prompt
            ];
            
            // Prepares request body
            $body = [
                'model' => $model,
                'messages' => $messages,
                'temperature' => (float)$temperature,
                'max_tokens' => (int)$maxTokens
            ];
            
            // Executes request to AI API
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
            
            // Processes response
            if ($httpCode === 200 && !empty($response)) {
                $responseData = json_decode($response, true);
                
                if (json_last_error() !== JSON_ERROR_NONE) {
                    throw new \Exception('Error decoding JSON response: ' . json_last_error_msg());
                }
                
                // Extracts response based on API format
                $aiResponse = '';
                if (isset($responseData['choices'][0]['message']['content'])) {
                    // OpenAI format
                    $aiResponse = $responseData['choices'][0]['message']['content'];
                } elseif (isset($responseData['content'][0]['text'])) {
                    // Anthropic format
                    $aiResponse = $responseData['content'][0]['text'];
                }
                
                // Stores result in context
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
                // Error handling...
            }
        } catch (\Exception $e) {
            // Exception handling...
        }
    }
}
```

## 🔧 Configuration

### Environment Variables

Configure the API key according to the provider:

```env
# For OpenAI
OPENAI_API_KEY=sk-...

# For Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# For OpenRouter
OPENROUTER_API_KEY=sk-or-...
```

### Usage of Generated Code

```php
$workflow = new BiblicalCounselor();

// Executes the workflow
$result = $workflow->run([
    'user_input' => 'I need advice about...'
]);

// Accesses AI response
if ($result['ai_agent_output']['success']) {
    echo $result['ai_agent_output']['response'];
} else {
    echo "Error: " . $result['ai_agent_output']['error'];
}
```

## 🎨 Advanced Features

### Tools/Functions Support

If the workflow has configured tools, the generated code will include:

```php
// Tools available for the agent
$tools = [];
$tools[] = ['name' => 'search_bible', 'description' => 'Search verses'];
$tools[] = ['name' => 'get_commentary', 'description' => 'Get commentaries'];
$body['tools'] = $tools;
```

### System Messages

The template supports system messages to define agent behavior:

```php
$systemMessage = "You are a wise and compassionate biblical counselor.";
```

### Multiple Providers

The template automatically detects the provider and configures the correct URL:

- **OpenAI**: `https://api.openai.com/v1/chat/completions`
- **Anthropic**: `https://api.anthropic.com/v1/messages`
- **OpenRouter**: `https://openrouter.ai/api/v1/chat/completions`

## 📊 Response Structure

The context stores complete information:

```php
[
    'success' => true,
    'response' => 'AI response...',
    'model' => 'gpt-4',
    'provider' => 'openai',
    'usage' => [
        'prompt_tokens' => 100,
        'completion_tokens' => 200,
        'total_tokens' => 300
    ],
    'finish_reason' => 'stop',
    'raw_response' => [...] // Complete API response
]
```

## 🐛 Error Handling

The template includes robust handling:

- JSON response validation
- HTTP error handling
- Exception capture
- Optional logging (when `debug` is active)
- Detailed error information in context

## 🔄 Supported Node Types

The template works with different AI Agent node types:

- `n8n-nodes-aiAgent`
- `@n8n/n8n-nodes-langchain.agent`
- Any node containing "agent" in the type

## 📚 References

- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [Anthropic API](https://docs.anthropic.com/claude/reference)
- [OpenRouter API](https://openrouter.ai/docs)

