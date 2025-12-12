# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Adicionado
- Suporte para variáveis de ambiente via arquivo `.env`
- Scripts de teste automatizados (`tests/test.py`)
- Documentação de testes (`TESTES.md`)
- Padrão GitFlow com scripts auxiliares
- Guia de GitFlow (`.gitflow.md`)
- **Template PHP completo para nó AI Agent** (`templates/nodes/aiAgent.xml`)
  - Geração de código PHP profissional com PHPDoc
  - Suporte para múltiplos provedores: OpenAI, Anthropic, OpenRouter
  - Suporte para system messages e tools/funções
  - Tratamento robusto de erros com try/catch
  - Suporte a diferentes formatos de resposta da API
  - Logging e debug opcional
  - Timeout configurável
  - Suporte para tipos LangChain (`@n8n/n8n-nodes-langchain.agent`)
- Template PHP melhorado (`templates/languages/php.xml`)
  - Documentação PHPDoc completa
  - Métodos helper (getContext, setContext, etc.)
  - Tratamento de erros no método run()
  - Rastreamento de tempo de execução

### Alterado
- `config/settings.json` agora usa referências a variáveis de ambiente
- `.gitignore` atualizado para ignorar apenas arquivos gerados em `output/`

## [1.0.0] - 2024-12-04

### Adicionado
- Conversão de workflows do n8n para classes PHP
- Cliente para API do n8n (`n8n_client.py`)
- Seletor interativo de workflows no terminal
- Sistema de templates XML para nós e linguagens
- Mapeador de nós para métodos de código
- Gerador de código com ordenação topológica
- Preservação da estrutura de pastas do n8n
- Templates para nós: function, httpRequest, set, if
- Template base para PHP

[1.0.0]: https://github.com/seu-usuario/n8ncoding/releases/tag/v1.0.0

