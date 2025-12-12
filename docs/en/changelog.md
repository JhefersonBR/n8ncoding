---
layout: page
title: Changelog
lang: en
ref: changelog
permalink: /en/changelog/
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for environment variables via `.env` file
- Automated test scripts (`tests/test.py`)
- Test documentation (`TESTES.md`)
- GitFlow pattern with helper scripts
- GitFlow guide (`.gitflow.md`)
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

[1.0.0]: https://github.com/seu-usuario/n8ncoding/releases/tag/v1.0.0

