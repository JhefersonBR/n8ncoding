---
layout: page
title: Exemplo Construtor de Credenciais
lang: pt
ref: credentials-constructor
permalink: /pt/examples/credentials-constructor/
---

# Exemplo: Construtor com Parâmetros e Classes de Credenciais

Este documento explica as novas funcionalidades implementadas.

## 🎯 Funcionalidades Implementadas

### 1. Construtor com Parâmetros do Primeiro Nó

O sistema agora extrai automaticamente os parâmetros do primeiro nó do workflow (geralmente um webhook ou start) e os transforma em parâmetros do construtor da classe.

**Antes:**
```php
class Workflow {
    public function run(array $params = []) {
        $this->context = $params;
        // ...
    }
}

// Uso
$workflow = new Workflow();
$workflow->run(['msg' => 'teste']);
```

**Depois:**
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

// Uso - muito mais claro e type-safe
$workflow = new Workflow(msg: 'teste', id: '123');
$workflow->run();
```

### 2. Parser de Expressões n8n

O sistema agora identifica e substitui expressões do n8n como `={{ $json.body.msg }}` por código PHP que acessa os parâmetros do construtor.

**Expressões Suportadas:**
- `={{ $json.body.msg }}` → `$this->params['msg']`
- `={{ $json.query.id }}` → `$this->params['id']`
- `={{ $json.headers.authorization }}` → `$this->params['authorization']`
- `={{ $json.body.data.name }}` → `$this->params['data']['name']`

**Exemplo no Código Gerado:**
```php
private function ai_agent(): void
{
    // Antes: $prompt = "={{ $json.body.msg }}";
    // Depois:
    $prompt = $this->params['msg'] ?? null;
    // ...
}
```

### 3. Classes de Credenciais

Em vez de usar `getenv()` diretamente no código, agora são geradas classes de credenciais reutilizáveis.

**Estrutura Criada:**
```
templates/credentials/
└── Credentials.php
    ├── Credentials (classe base)
    ├── OpenAICredentials
    ├── AnthropicCredentials
    └── OpenRouterCredentials
```

**Uso no Código Gerado:**
```php
// Antes:
$apiKey = getenv('OPENAI_API_KEY') ?: '';

// Depois:
use OpenAICredentials;

$credentials = new OpenAICredentials();
$apiKey = $credentials->getApiKey();
```

**Vantagens:**
- ✅ Validação automática de credenciais
- ✅ Mensagens de erro claras
- ✅ Possibilidade de injetar credenciais via construtor
- ✅ Fallback para variáveis de ambiente
- ✅ Código mais testável e reutilizável

## 📝 Exemplo Completo

### Workflow no n8n

```
Webhook → AI Agent → End
```

**Webhook recebe:**
- Body: `{ "msg": "Olá" }`
- Query: `{ "id": "123" }`

**AI Agent usa:**
- Prompt: `={{ $json.body.msg }}`

### Código PHP Gerado

```php
<?php

require_once __DIR__ . '/../credentials/Credentials.php';

use OpenAICredentials;

class MeuWorkflow {

    private array $context = [];
    private array $params = [];

    /**
     * Construtor da classe
     *
     * @param mixed $msg Parâmetro msg
     * @param mixed $id Parâmetro id
     * @param array $params Parâmetros adicionais (opcional)
     */
    public function __construct(mixed $msg = null, mixed $id = null, array $params = [])
    {
        // Parâmetros nomeados
        $this->params = [];
        $this->params['msg'] = $msg;
        $this->params['id'] = $id;

        // Parâmetros adicionais
        $this->params = array_merge($this->params, $params);
    }

    public function run(array $additionalParams = []): mixed
    {
        try {
            $this->context = array_merge([
                'start_time' => microtime(true),
                'workflow_name' => 'MeuWorkflow',
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
        // Expressão substituída automaticamente!
        $prompt = $this->params['msg'] ?? null;
        
        $credentials = new OpenAICredentials();
        $apiKey = $credentials->getApiKey();
        
        // ... resto do código
    }
}
```

### Uso do Código Gerado

```php
// Opção 1: Parâmetros nomeados (PHP 8+)
$workflow = new MeuWorkflow(msg: 'Olá mundo', id: '123');
$result = $workflow->run();

// Opção 2: Parâmetros posicionais
$workflow = new MeuWorkflow('Olá mundo', '123');
$result = $workflow->run();

// Opção 3: Array de parâmetros
$workflow = new MeuWorkflow(null, null, ['msg' => 'Olá', 'id' => '123']);
$result = $workflow->run();

// Opção 4: Parâmetros adicionais no run()
$workflow = new MeuWorkflow('Olá');
$result = $workflow->run(['id' => '123']);
```

## 🔧 Configuração de Credenciais

### Opção 1: Variáveis de Ambiente (Recomendado)

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
```

### Opção 2: Injeção via Construtor

```php
// Para testes ou ambientes específicos
$credentials = new OpenAICredentials('sk-custom-key');
$workflow = new MeuWorkflow(msg: 'teste');
```

## 🎨 Benefícios

1. **Type Safety**: Parâmetros tipados no construtor
2. **Clareza**: Fica óbvio quais parâmetros o workflow precisa
3. **Reutilização**: Classes de credenciais podem ser usadas em outros lugares
4. **Testabilidade**: Fácil mockar credenciais em testes
5. **Manutenibilidade**: Código mais organizado e profissional

## 📚 Arquivos Criados

- `src/parameter_extractor.py` - Extrai parâmetros do primeiro nó
- `src/expression_parser.py` - Faz parsing de expressões n8n
- `templates/credentials/Credentials.php` - Classes de credenciais
- `tests/test_expression_parser.py` - Testes do parser
- `tests/test_complete_feature.py` - Testes completos

## 🚀 Próximos Passos

- [ ] Suporte para mais tipos de expressões n8n
- [ ] Validação de tipos de parâmetros
- [ ] Geração de interfaces para parâmetros
- [ ] Suporte para credenciais customizadas

