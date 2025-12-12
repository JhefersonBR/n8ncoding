---
layout: page
title: Credentials Constructor Example
lang: en
ref: credentials-constructor
permalink: /en/examples/credentials-constructor/
---

# Example: Constructor with Parameters and Credential Classes

This document explains the new features implemented.

## 🎯 Implemented Features

### 1. Constructor with First Node Parameters

The system now automatically extracts parameters from the first node of the workflow (usually a webhook or start) and transforms them into class constructor parameters.

**Before:**
```php
class Workflow {
    public function run(array $params = []) {
        $this->context = $params;
        // ...
    }
}

// Usage
$workflow = new Workflow();
$workflow->run(['msg' => 'test']);
```

**After:**
```php
class Workflow {
    public function __construct(mixed $msg = null, mixed $id = null, array $params = []) {
        $this->params = [];
        $this->params['msg'] = $msg;
        $this->params['id'] = $id;
        $this->params = array_merge($this->params, $params);
    }
    
    public function run(array $additionalParams = []) {
        $this->context = array_merge($this->params, $additionalParams);
        // ...
    }
}

// Usage - much clearer and type-safe
$workflow = new Workflow(msg: 'test', id: '123');
$workflow->run();
```

### 2. n8n Expression Parser

The system now identifies and replaces n8n expressions like `={{ $json.body.msg }}` with PHP code that accesses constructor parameters.

**Supported Expressions:**
- `={{ $json.body.msg }}` → `$this->params['msg']`
- `={{ $json.query.id }}` → `$this->params['id']`
- `={{ $json.headers.authorization }}` → `$this->params['authorization']`
- `={{ $json.body.data.name }}` → `$this->params['data']['name']`

**Example in Generated Code:**
```php
private function ai_agent(): void
{
    // Before: $prompt = "={{ $json.body.msg }}";
    // After:
    $prompt = $this->params['msg'] ?? null;
    // ...
}
```

### 3. Credential Classes

Instead of using `getenv()` directly in code, reusable credential classes are now generated.

**Created Structure:**
```
templates/credentials/
└── Credentials.php
    ├── Credentials (base class)
    ├── OpenAICredentials
    ├── AnthropicCredentials
    └── OpenRouterCredentials
```

**Usage in Generated Code:**
```php
// Before:
$apiKey = getenv('OPENAI_API_KEY') ?: '';

// After:
use OpenAICredentials;

$credentials = new OpenAICredentials();
$apiKey = $credentials->getApiKey();
```

**Advantages:**
- ✅ Automatic credential validation
- ✅ Clear error messages
- ✅ Possibility to inject credentials via constructor
- ✅ Fallback to environment variables
- ✅ More testable and reusable code

## 📝 Complete Example

### Workflow in n8n

```
Webhook → AI Agent → End
```

**Webhook receives:**
- Body: `{ "msg": "Hello" }`
- Query: `{ "id": "123" }`

**AI Agent uses:**
- Prompt: `={{ $json.body.msg }}`

### Generated PHP Code

```php
<?php

require_once __DIR__ . '/../credentials/Credentials.php';

use OpenAICredentials;

class MyWorkflow {

    private array $context = [];
    private array $params = [];

    /**
     * Class constructor
     *
     * @param mixed $msg Parameter msg
     * @param mixed $id Parameter id
     * @param array $params Additional parameters (optional)
     */
    public function __construct(mixed $msg = null, mixed $id = null, array $params = [])
    {
        // Named parameters
        $this->params = [];
        $this->params['msg'] = $msg;
        $this->params['id'] = $id;

        // Additional parameters
        $this->params = array_merge($this->params, $params);
    }

    public function run(array $additionalParams = []): mixed
    {
        try {
            $this->context = array_merge([
                'start_time' => microtime(true),
                'workflow_name' => 'MyWorkflow',
            ], $this->params, $additionalParams);

            $this->webhook();
            $this->ai_agent();

            return $this->context;
        } catch (\Exception $e) {
            // ...
        }
    }

    private function ai_agent(): void
    {
        // Expression automatically replaced!
        $prompt = $this->params['msg'] ?? null;
        
        $credentials = new OpenAICredentials();
        $apiKey = $credentials->getApiKey();
        
        // ... rest of code
    }
}
```

### Usage of Generated Code

```php
// Option 1: Named parameters (PHP 8+)
$workflow = new MyWorkflow(msg: 'Hello world', id: '123');
$result = $workflow->run();

// Option 2: Positional parameters
$workflow = new MyWorkflow('Hello world', '123');
$result = $workflow->run();

// Option 3: Array of parameters
$workflow = new MyWorkflow(null, null, ['msg' => 'Hello', 'id' => '123']);
$result = $workflow->run();

// Option 4: Additional parameters in run()
$workflow = new MyWorkflow('Hello');
$result = $workflow->run(['id' => '123']);
```

## 🔧 Credential Configuration

### Option 1: Environment Variables (Recommended)

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
```

### Option 2: Injection via Constructor

```php
// For tests or specific environments
$credentials = new OpenAICredentials('sk-custom-key');
$workflow = new MyWorkflow(msg: 'test');
```

## 🎨 Benefits

1. **Type Safety**: Typed parameters in constructor
2. **Clarity**: It's obvious which parameters the workflow needs
3. **Reusability**: Credential classes can be used elsewhere
4. **Testability**: Easy to mock credentials in tests
5. **Maintainability**: More organized and professional code

