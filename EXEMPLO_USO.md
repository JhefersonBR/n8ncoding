# Exemplo de Uso do n8ncoding

Este guia mostra como usar o **n8ncoding** para converter workflows do n8n em classes de código em múltiplas linguagens.

## 📋 Índice

1. [Configuração Inicial](#configuração-inicial)
2. [Executando o Programa](#executando-o-programa)
3. [Fluxo de Execução Completo](#fluxo-de-execução-completo)
4. [Seleção de Linguagens](#seleção-de-linguagens)
5. [Estrutura de Saída](#estrutura-de-saída)
6. [Exemplos de Código Gerado](#exemplos-de-código-gerado)
7. [Classes de Credenciais](#classes-de-credenciais)
8. [Parâmetros no Construtor](#parâmetros-no-construtor)
9. [Troubleshooting](#troubleshooting)

---

## ⚙️ Configuração Inicial

### 1. Variáveis de Ambiente (Recomendado)

O projeto utiliza variáveis de ambiente para configurações sensíveis. Crie um arquivo `.env` na raiz do projeto:

```env
N8N_URL=http://localhost:5678
N8N_API_KEY=sua-api-key-aqui
```

**Importante:** O arquivo `.env` não deve ser commitado no Git (já está no `.gitignore`).

### 2. Arquivo de Configuração

O arquivo `config/settings.json` já está configurado para usar variáveis de ambiente:

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

**Nota:** A linguagem padrão em `settings.json` é apenas uma sugestão. Você poderá escolher múltiplas linguagens durante a execução.

---

## 🚀 Executando o Programa

```bash
python src/main.py
```

O programa irá:
1. ✅ Carregar configurações do `.env` e `config/settings.json`
2. ✅ Conectar à API do n8n
3. ✅ Listar todos os workflows disponíveis
4. ✅ Permitir seleção de workflows
5. ✅ Permitir seleção de linguagens (múltipla escolha)
6. ✅ Gerar classes para cada workflow em cada linguagem selecionada

---

## 🔄 Fluxo de Execução Completo

### Passo 1: Conexão com n8n

```
============================================================
n8ncoding - Conversor de Workflows n8n para Código
============================================================

Conectando ao n8n em: http://localhost:5678
✓ Conexão estabelecida com sucesso!
```

### Passo 2: Listagem de Workflows

```
Buscando workflows...
✓ 5 workflow(s) encontrado(s).

Escolha os workflows que deseja converter:
============================================================
[1] Enviar Email Automático (ID: abc123)
[2] Atualizar CRM (ID: def456)
[3] Extrair Dados do Google Sheets (ID: ghi789)
[4] Processar Webhook (ID: jkl012)
[5] Conselheiro Bíblico (ID: mno345)
============================================================

Digite os números separados por vírgula (Ex: 1,3,4): 1,3,5
```

### Passo 3: Seleção de Linguagens

```
============================================================
Escolha as linguagens de destino:
============================================================
[1] PHP - PHP 8.0+
[2] Python - Python 3.8+
[3] JavaScript - Node.js 14+
============================================================

Linguagem padrão configurada: PHP
Pressione Enter para usar apenas a padrão ou escolha múltiplas opções.

Digite os números separados por vírgula (Ex: 1,3) ou Enter para padrão: 1,2
```

**Resultado:**
```
✓ 2 linguagem(s) selecionada(s): PHP, Python
```

### Passo 4: Geração de Código

```
============================================================
Gerando código...
============================================================

============================================================
Processando: Enviar Email Automático
============================================================

  → Gerando código em PHP...
  ✓ Enviar Email Automático convertido para PHP com sucesso!

  → Gerando código em Python...
  ✓ Enviar Email Automático convertido para Python com sucesso!

============================================================
Processando: Extrair Dados do Google Sheets
============================================================
...
```

---

## 🌐 Seleção de Linguagens

O n8ncoding suporta **múltiplas linguagens** simultaneamente:

### Linguagens Disponíveis

| Linguagem | Versão Mínima | Descrição |
|-----------|---------------|-----------|
| **PHP** | 8.0+ | Classes PHP com type hints e PHPDoc |
| **Python** | 3.8+ | Classes Python com type hints e docstrings |
| **JavaScript** | Node.js 14+ | Classes ES6+ com JSDoc |

### Seleção Múltipla

Você pode gerar código para múltiplas linguagens ao mesmo tempo:

```bash
# Exemplo: Gerar PHP e JavaScript
Digite os números separados por vírgula (Ex: 1,3): 1,3

✓ 2 linguagem(s) selecionada(s): PHP, JavaScript
```

**Resultado:** O mesmo workflow será gerado em ambas as linguagens.

---

## 📁 Estrutura de Saída

### Organização por Linguagem

Os arquivos gerados são organizados por linguagem:

```
output/
├── php/                          # Classes PHP
│   ├── EnviarEmailAutomatico.php
│   ├── ExtrairDadosGoogleSheets.php
│   └── ConselheiroBiblico.php
│
├── python/                        # Classes Python
│   ├── EnviarEmailAutomatico.py
│   ├── ExtrairDadosGoogleSheets.py
│   └── ConselheiroBiblico.py
│
├── javascript/                    # Classes JavaScript
│   ├── EnviarEmailAutomatico.js
│   ├── ExtrairDadosGoogleSheets.js
│   └── ConselheiroBiblico.js
│
└── credentials/                   # Classes de Credenciais (compartilhadas)
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

**Nota:** As classes de credenciais são geradas automaticamente quando necessário (ex: ao usar nós AI Agent).

---

## 💻 Exemplos de Código Gerado

### PHP

```php
<?php

require_once __DIR__ . '/../credentials/Credentials.php';

use OpenAICredentials;

/**
 * Classe gerada automaticamente pelo n8ncoding
 *
 * Esta classe representa o workflow "Enviar Email Automático" convertido do n8n.
 *
 * @package Generated
 * @author n8ncoding
 * @version 1.0.0
 */
class EnviarEmailAutomatico {

    /**
     * Contexto interno para armazenar dados entre nós
     *
     * @var array
     */
    private array $context = [];

    /**
     * Parâmetros do workflow (passados no construtor)
     *
     * @var array
     */
    private array $params = [];

    /**
     * Construtor da classe
     *
     * @param string|null $mensagem Parâmetro mensagem
     * @param string|null $destinatario Parâmetro destinatario
     */
    public function __construct(?string $mensagem = null, ?string $destinatario = null)
    {
        $this->context = [];
        $this->params = [];
        
        $this->params['mensagem'] = $mensagem;
        $this->params['destinatario'] = $destinatario;
    }

    /**
     * Executa o workflow
     *
     * @param array $params Parâmetros adicionais (opcional)
     * @return mixed Resultado final do workflow
     */
    public function run(array $params = []): mixed
    {
        // Mescla parâmetros adicionais com os do construtor
        $this->context = array_merge($this->params, $params);

        $this->startNode();
        $this->httpRequestNode();
        $this->sendEmailNode();

        return $this->context;
    }

    private function startNode(): void
    {
        // Usa parâmetros do construtor
        $mensagem = $this->params['mensagem'] ?? null;
        $this->context['start_output'] = ['mensagem' => $mensagem];
    }

    private function httpRequestNode(): void
    {
        $url = "https://api.example.com/send";
        $method = "POST";
        $headers = ['Content-Type: application/json'];
        $body = [
            'message' => $this->context['start_output']['mensagem']
        ];
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
        
        $response = curl_exec($ch);
        $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        $this->context['http_request_output'] = json_decode($response, true);
    }

    private function sendEmailNode(): void
    {
        // Implementação do envio de email
        $this->context['email_sent'] = true;
    }
}
```

### Python

```python
"""
Classe gerada automaticamente pelo n8ncoding

Esta classe representa o workflow "Enviar Email Automático" convertido do n8n.

@author n8ncoding
@version 1.0.0
"""
import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

# Adiciona o diretório de credenciais ao path
credentials_path = Path(__file__).parent.parent.parent / 'credentials'
sys.path.insert(0, str(credentials_path))

from OpenAICredentials import OpenAICredentials

class EnviarEmailAutomatico:
    """
    Classe gerada automaticamente pelo n8ncoding

    Esta classe representa o workflow "Enviar Email Automático" convertido do n8n.
    """

    def __init__(self, mensagem: str = None, destinatario: str = None):
        """
        Inicializa a classe do workflow.

        mensagem: str - Parâmetro mensagem
        destinatario: str - Parâmetro destinatario
        """
        self.context: Dict[str, Any] = {}
        self.params: Dict[str, Any] = {}

        self.params['mensagem'] = mensagem
        self.params['destinatario'] = destinatario

    def run(self, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executa o workflow.

        Args:
            additional_params: Parâmetros adicionais (opcional)

        Returns:
            Resultado final do workflow (geralmente o contexto completo)
        """
        if additional_params:
            self.context.update(additional_params)
        self.context.update(self.params)

        self.startNode()
        self.httpRequestNode()
        self.sendEmailNode()

        return self.context

    def startNode(self) -> None:
        """Nó: Start"""
        mensagem = self.params.get('mensagem')
        self.context['start_output'] = {'mensagem': mensagem}

    def httpRequestNode(self) -> None:
        """Nó: HTTP Request"""
        import requests
        
        url = "https://api.example.com/send"
        method = "POST"
        headers = {'Content-Type': 'application/json'}
        body = {
            'message': self.context['start_output']['mensagem']
        }
        
        response = requests.request(method, url, headers=headers, json=body)
        self.context['http_request_output'] = response.json()

    def sendEmailNode(self) -> None:
        """Nó: Send Email"""
        self.context['email_sent'] = True
```

### JavaScript

```javascript
/**
 * Classe gerada automaticamente pelo n8ncoding
 *
 * Esta classe representa o workflow "Enviar Email Automático" convertido do n8n.
 *
 * @author n8ncoding
 * @version 1.0.0
 */

const { OpenAICredentials } = require('../credentials/OpenAICredentials.js');

class EnviarEmailAutomatico {
    /**
     * Construtor da classe
     *
     * @param {string} mensagem - Parâmetro mensagem
     * @param {string} destinatario - Parâmetro destinatario
     */
    constructor(mensagem = null, destinatario = null) {
        /**
         * Contexto interno para armazenar dados entre nós
         * @type {Object}
         */
        this.context = {};

        /**
         * Parâmetros do workflow (passados no construtor)
         * @type {Object}
         */
        this.params = {};

        this.params['mensagem'] = mensagem;
        this.params['destinatario'] = destinatario;
    }

    /**
     * Executa o workflow
     *
     * @param {Object} additionalParams - Parâmetros adicionais (opcional)
     * @returns {Promise<Object>} Resultado final do workflow
     */
    async run(additionalParams = {}) {
        this.context = { ...this.params, ...additionalParams };

        await this.startNode();
        await this.httpRequestNode();
        await this.sendEmailNode();

        return this.context;
    }

    async startNode() {
        const mensagem = this.params['mensagem'] || null;
        this.context['start_output'] = { mensagem };
    }

    async httpRequestNode() {
        const axios = require('axios');
        
        const url = "https://api.example.com/send";
        const method = "POST";
        const headers = { 'Content-Type': 'application/json' };
        const body = {
            message: this.context['start_output']['mensagem']
        };
        
        const response = await axios({ method, url, headers, data: body });
        this.context['http_request_output'] = response.data;
    }

    async sendEmailNode() {
        this.context['email_sent'] = true;
    }
}

module.exports = EnviarEmailAutomatico;
```

---

## 🔐 Classes de Credenciais

O n8ncoding gera automaticamente classes de credenciais quando necessário (ex: ao usar nós AI Agent).

### Estrutura

As classes de credenciais são salvas em `output/credentials/` e são compartilhadas entre todos os workflows.

### Exemplo: OpenAICredentials (PHP)

```php
<?php

class OpenAICredentials {
    public function getApiKey(): string {
        $apiKey = getenv('OPENAI_API_KEY');
        if (!$apiKey) {
            throw new \Exception('OPENAI_API_KEY não configurada nas variáveis de ambiente');
        }
        return $apiKey;
    }
}
```

### Uso nas Classes Geradas

```php
use OpenAICredentials;

// Dentro de um método
$credentials = new OpenAICredentials();
$apiKey = $credentials->getApiKey();
```

---

## 🎯 Parâmetros no Construtor

O n8ncoding identifica automaticamente parâmetros do primeiro nó do workflow e os adiciona como parâmetros do construtor.

### Como Funciona

1. **Identificação:** O sistema analisa expressões n8n no primeiro nó (ex: `={{ $json.body.msg }}`)
2. **Extração:** Extrai os caminhos de dados (ex: `body.msg` → parâmetro `msg`)
3. **Geração:** Adiciona como parâmetros do construtor

### Exemplo

**Workflow n8n:**
- Primeiro nó recebe: `={{ $json.body.msg }}` e `={{ $json.query.id }}`

**Classe gerada:**
```php
public function __construct(?string $msg = null, ?string $id = null)
{
    $this->params['msg'] = $msg;
    $this->params['id'] = $id;
}
```

**Uso:**
```php
$workflow = new EnviarEmailAutomatico(
    mensagem: "Olá!",
    destinatario: "user@example.com"
);

$resultado = $workflow->run();
```

---

## 🔧 Troubleshooting

### Erro de Conexão com n8n

**Sintomas:**
```
❌ Erro ao conectar ao n8n: Connection refused
```

**Soluções:**
- Verifique se a URL do n8n está correta no `.env`
- Confirme que a API Key está configurada corretamente
- Verifique se o n8n está rodando e acessível
- Teste a conexão manualmente: `curl http://localhost:5678/api/v1/workflows`

### Nenhum Workflow Encontrado

**Sintomas:**
```
✓ 0 workflow(s) encontrado(s).
```

**Soluções:**
- Verifique se há workflows criados no n8n
- Confirme que a API Key tem permissão para listar workflows
- Verifique se os workflows não estão em modo "ativo" (alguns n8n só listam workflows ativos)

### Template Não Encontrado

**Sintomas:**
```
Template de nó não encontrado: templates/nodes/myCustomNode.xml
```

**Soluções:**
- Se um tipo de nó não tem template específico, será usado um template padrão
- Crie um template personalizado em `templates/nodes/` se necessário
- Para múltiplas linguagens, crie em `templates/nodes/{language}/myCustomNode.xml`

### Erro ao Gerar Código

**Sintomas:**
```
❌ Erro ao gerar código Python para WorkflowX
```

**Soluções:**
- Verifique se os templates da linguagem existem em `templates/languages/`
- Verifique se os templates de nós existem em `templates/nodes/{language}/`
- Execute `python tests/test.py` para verificar se há problemas nos componentes

### Erro de Import/Require

**Sintomas:**
```
Fatal error: Uncaught Error: Class 'OpenAICredentials' not found
```

**Soluções:**
- Verifique se as classes de credenciais foram geradas em `output/credentials/`
- Verifique o caminho relativo no `require_once` ou `import`
- Execute o gerador novamente para garantir que as credenciais foram criadas

---

## 📚 Próximos Passos

Após gerar as classes:

1. **Revise o código gerado** em `output/{language}/`
2. **Configure variáveis de ambiente** para credenciais (ex: `OPENAI_API_KEY`)
3. **Teste a classe gerada** com dados reais
4. **Customize conforme necessário** (os arquivos gerados são seus para modificar)

---

## 💡 Dicas

- ✅ Use **seleção múltipla de linguagens** para comparar implementações
- ✅ **Revise sempre** o código gerado antes de usar em produção
- ✅ **Configure variáveis de ambiente** para credenciais sensíveis
- ✅ **Execute testes** (`python tests/test.py`) antes de fazer commit
- ✅ **Documente workflows complexos** no n8n para facilitar a conversão

---

**Última atualização:** 2024
