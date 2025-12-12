---
layout: page
title: Changelog
lang: pt
ref: changelog
permalink: /pt/changelog/
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.1] - 2025-12-12

### Added
- **License file (LGPL-3.0)**
  - Added LICENSE file with GNU Lesser General Public License v3.0
  - Updated README.md with license information
  - LGPL-3.0 allows use in proprietary projects while keeping the code open-source

## [1.2.0] - 2025-12-12

### Changed
- **All root `.md` files translated to English**
  - `README.md` - Fully translated to English
  - `USAGE.md` (formerly `EXEMPLO_USO.md`) - Translated to English
  - `ENV_SETUP.md` - Translated to English
  - `CONTRIBUTING.md` - Translated to English
  - `GITFLOW.md` - Translated to English
  - `TESTING.md` (formerly `TESTES.md`) - Translated to English
  - `AI_AGENT_EXAMPLE.md` (formerly `EXEMPLO_AI_AGENT.md`) - Translated to English
  - `CREDENTIALS_CONSTRUCTOR_EXAMPLE.md` (formerly `EXEMPLO_CONSTRUTOR_CREDENCIAIS.md`) - Translated to English
  - `AI_AGENT_PHP_TEMPLATE.md` (formerly `EXEMPLO_AI_AGENT_PHP.md`) - Translated to English
  - Portuguese translations maintained in GitHub Pages (`docs/pt/`)

## [1.1.0] - 2024-12-04

### Added
- **Multilingual documentation on GitHub Pages**
  - Complete Jekyll structure with support for multiple languages (English and Portuguese)
  - Automatic GitHub Actions workflow for deployment
  - Automation to synchronize root `.md` files with Jekyll documentation
  - HTML templates with language selector
  - Custom CSS for better presentation
  - Complete documentation for installation, usage, contribution, and examples
- Support for environment variables via `.env` file
- Automated test scripts (`tests/test.py`)
- Test documentation (`TESTING.md`)
- GitFlow pattern with helper scripts
- GitFlow guide (`GITFLOW.md`)
- **Complete PHP template for AI Agent node** (`templates/nodes/aiAgent.xml`)
  - Professional PHP code generation with PHPDoc
  - Support for multiple providers: OpenAI, Anthropic, OpenRouter
  - Support for system messages and tools/functions
  - Robust error handling with try/catch
  - Support for different API response formats
  - Optional logging and debug
  - Configurable timeout
  - Support for LangChain types (`@n8n/n8n-nodes-langchain.agent`)
- Improved PHP template (`templates/languages/php.xml`)
  - Complete PHPDoc documentation
  - Helper methods (getContext, setContext, etc.)
  - Error handling in run() method
  - Execution time tracking

### Changed
- `config/settings.json` now uses environment variable references
- `.gitignore` updated to ignore only generated files in `output/`

## [1.0.0] - 2024-12-04

### Added
- Conversion of n8n workflows to PHP classes
- n8n API client (`n8n_client.py`)
- Interactive workflow selector in terminal
- XML template system for nodes and languages
- Node to code method mapper
- Code generator with topological ordering
- Preservation of n8n folder structure
- Templates for nodes: function, httpRequest, set, if
- Base template for PHP

[1.2.1]: https://github.com/JhefersonBR/n8ncoding/releases/tag/v1.2.1
[1.2.0]: https://github.com/JhefersonBR/n8ncoding/releases/tag/v1.2.0
[1.1.0]: https://github.com/JhefersonBR/n8ncoding/releases/tag/v1.1.0
[1.0.0]: https://github.com/JhefersonBR/n8ncoding/releases/tag/v1.0.0