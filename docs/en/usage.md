---
layout: page
title: Usage Guide
lang: en
ref: usage
permalink: /en/usage/
---

# Usage Guide

This guide shows how to use **n8ncoding** to convert n8n workflows into code classes in multiple languages.

## 📋 Table of Contents

1. [Initial Configuration](#initial-configuration)
2. [Running the Program](#running-the-program)
3. [Complete Execution Flow](#complete-execution-flow)
4. [Language Selection](#language-selection)
5. [Output Structure](#output-structure)
6. [Generated Code Examples](#generated-code-examples)
7. [Credential Classes](#credential-classes)
8. [Constructor Parameters](#constructor-parameters)
9. [Troubleshooting](#troubleshooting)

---

## ⚙️ Initial Configuration

### 1. Environment Variables (Recommended)

The project uses environment variables for sensitive configurations. Create a `.env` file in the project root:

```env
N8N_URL=http://localhost:5678
N8N_API_KEY=your-api-key-here
```

**Important:** The `.env` file should not be committed to Git (already in `.gitignore`).

### 2. Configuration File

The `config/settings.json` file is already configured to use environment variables:

```json
{
  "n8n": {
    "url": "${N8N_URL}",
    "api_key": "${N8N_API_KEY}"
  },
  "output": {
    "path": "output",
    "language": "php"
  }
}
```

**Note:** The default language in `settings.json` is just a suggestion. You can choose multiple languages during execution.

---

## 🚀 Running the Program

```bash
python src/main.py
```

The program will:
1. ✅ Load settings from `.env` and `config/settings.json`
2. ✅ Connect to the n8n API
3. ✅ List all available workflows
4. ✅ Allow workflow selection
5. ✅ Allow language selection (multiple choice)
6. ✅ Generate classes for each workflow in each selected language

---

## 🔄 Complete Execution Flow

### Step 1: Connection with n8n

```
============================================================
n8ncoding - n8n Workflow to Code Converter
============================================================

Connecting to n8n at: http://localhost:5678
✓ Connection established successfully!
```

### Step 2: Workflow Listing

```
Searching workflows...
✓ 5 workflow(s) found.

Choose the workflows you want to convert:
============================================================
[1] Send Automatic Email (ID: abc123)
[2] Update CRM (ID: def456)
[3] Extract Data from Google Sheets (ID: ghi789)
[4] Process Webhook (ID: jkl012)
[5] Biblical Counselor (ID: mno345)
============================================================

Enter numbers separated by commas (Ex: 1,3,4): 1,3,5
```

### Step 3: Language Selection

```
============================================================
Choose target languages:
============================================================
[1] PHP - PHP 8.0+
[2] Python - Python 3.8+
[3] JavaScript - Node.js 14+
============================================================

Default language configured: PHP
Press Enter to use only the default or choose multiple options.

Enter numbers separated by commas (Ex: 1,3) or Enter for default: 1,2
```

**Result:**
```
✓ 2 language(s) selected: PHP, Python
```

### Step 4: Code Generation

```
============================================================
Generating code...
============================================================

============================================================
Processing: Send Automatic Email
============================================================

  → Generating PHP code...
  ✓ Send Automatic Email converted to PHP successfully!

  → Generating Python code...
  ✓ Send Automatic Email converted to Python successfully!

============================================================
Processing: Extract Data from Google Sheets
============================================================
...
```

---

## 🌐 Language Selection

n8ncoding supports **multiple languages** simultaneously:

### Available Languages

| Language | Minimum Version | Description |
|----------|----------------|-------------|
| **PHP** | 8.0+ | PHP classes with type hints and PHPDoc |
| **Python** | 3.8+ | Python classes with type hints and docstrings |
| **JavaScript** | Node.js 14+ | ES6+ classes with JSDoc |

### Multiple Selection

You can generate code for multiple languages at the same time:

```bash
# Example: Generate PHP and JavaScript
Enter numbers separated by commas (Ex: 1,3): 1,3

✓ 2 language(s) selected: PHP, JavaScript
```

**Result:** The same workflow will be generated in both languages.

---

## 📁 Output Structure

### Organization by Language

Generated files are organized by language:

```
output/
├── php/                          # PHP Classes
│   ├── SendAutomaticEmail.php
│   ├── ExtractDataGoogleSheets.php
│   └── BiblicalCounselor.php
│
├── python/                        # Python Classes
│   ├── SendAutomaticEmail.py
│   ├── ExtractDataGoogleSheets.py
│   └── BiblicalCounselor.py
│
├── javascript/                    # JavaScript Classes
│   ├── SendAutomaticEmail.js
│   ├── ExtractDataGoogleSheets.js
│   └── BiblicalCounselor.js
│
└── credentials/                   # Credential Classes (shared)
    ├── Credentials.php
    ├── Credentials.py
    ├── Credentials.js
    ├── OpenAICredentials.php
    ├── OpenAICredentials.py
    ├── OpenAICredentials.js
    ├── AnthropicCredentials.php
    ├── AnthropicCredentials.py
    ├── AnthropicCredentials.js
    ├── OpenRouterCredentials.php
    ├── OpenRouterCredentials.py
    └── OpenRouterCredentials.js
```

**Note:** Credential classes are automatically generated when needed (e.g., when using AI Agent nodes).

---

## 💻 Generated Code Examples

See the [AI Agent Example]({{ site.baseurl }}/en/examples/ai-agent/) and [Credentials Constructor Example]({{ site.baseurl }}/en/examples/credentials-constructor/) for detailed code examples.

---

## 🔐 Credential Classes

n8ncoding automatically generates credential classes when needed (e.g., when using AI Agent nodes).

### Structure

Credential classes are saved in `output/credentials/` and are shared among all workflows.

### Example: OpenAICredentials (PHP)

```php
<?php

class OpenAICredentials {
    public function getApiKey(): string {
        $apiKey = getenv('OPENAI_API_KEY');
        if (!$apiKey) {
            throw new \Exception('OPENAI_API_KEY not configured in environment variables');
        }
        return $apiKey;
    }
}
```

### Usage in Generated Classes

```php
use OpenAICredentials;

// Inside a method
$credentials = new OpenAICredentials();
$apiKey = $credentials->getApiKey();
```

---

## 🎯 Constructor Parameters

n8ncoding automatically identifies parameters from the first node of the workflow and adds them as constructor parameters.

### How It Works

1. **Identification:** The system analyzes n8n expressions in the first node (e.g., `={{ $json.body.msg }}`)
2. **Extraction:** Extracts data paths (e.g., `body.msg` → parameter `msg`)
3. **Generation:** Adds as constructor parameters

### Example

**n8n Workflow:**
- First node receives: `={{ $json.body.msg }}` and `={{ $json.query.id }}`

**Generated Class:**
```php
public function __construct(?string $msg = null, ?string $id = null)
{
    $this->params['msg'] = $msg;
    $this->params['id'] = $id;
}
```

**Usage:**
```php
$workflow = new SendAutomaticEmail(
    message: "Hello!",
    recipient: "user@example.com"
);

$result = $workflow->run();
```

---

## 🔧 Troubleshooting

### Connection Error with n8n

**Symptoms:**
```
❌ Error connecting to n8n: Connection refused
```

**Solutions:**
- Check if the n8n URL is correct in `.env`
- Confirm that the API Key is configured correctly
- Verify that n8n is running and accessible
- Test connection manually: `curl http://localhost:5678/api/v1/workflows`

### No Workflows Found

**Symptoms:**
```
✓ 0 workflow(s) found.
```

**Solutions:**
- Check if there are workflows created in n8n
- Confirm that the API Key has permission to list workflows
- Check if workflows are not in "active" mode (some n8n only list active workflows)

### Template Not Found

**Symptoms:**
```
Template node not found: templates/nodes/myCustomNode.xml
```

**Solutions:**
- If a node type doesn't have a specific template, a default template will be used
- Create a custom template in `templates/nodes/` if needed
- For multiple languages, create in `templates/nodes/{language}/myCustomNode.xml`

### Code Generation Error

**Symptoms:**
```
❌ Error generating Python code for WorkflowX
```

**Solutions:**
- Check if language templates exist in `templates/languages/`
- Check if node templates exist in `templates/nodes/{language}/`
- Run `python tests/test.py` to check for component issues

### Import/Require Error

**Symptoms:**
```
Fatal error: Uncaught Error: Class 'OpenAICredentials' not found
```

**Solutions:**
- Check if credential classes were generated in `output/credentials/`
- Check the relative path in `require_once` or `import`
- Run the generator again to ensure credentials were created

---

## 📚 Next Steps

After generating classes:

1. **Review generated code** in `output/{language}/`
2. **Configure environment variables** for credentials (e.g., `OPENAI_API_KEY`)
3. **Test the generated class** with real data
4. **Customize as needed** (generated files are yours to modify)

---

## 💡 Tips

- ✅ Use **multiple language selection** to compare implementations
- ✅ **Always review** generated code before using in production
- ✅ **Configure environment variables** for sensitive credentials
- ✅ **Run tests** (`python tests/test.py`) before committing
- ✅ **Document complex workflows** in n8n to facilitate conversion

---

**Last updated:** 2024

