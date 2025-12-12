---
layout: page
title: Início
lang: pt
ref: index
permalink: /pt/
---

# n8ncoding

**n8ncoding** é uma ferramenta open-source que converte workflows do n8n em classes de código reutilizáveis. Atualmente suporta PHP, Python e JavaScript, com planos para expandir para outras linguagens.

## 🚀 Funcionalidades

- ✅ Conexão com API do n8n
- ✅ Listagem de workflows disponíveis
- ✅ Seleção interativa de workflows no terminal
- ✅ Conversão de workflows em classes PHP, Python e JavaScript
- ✅ Preservação da estrutura de pastas do n8n
- ✅ Templates XML configuráveis para diferentes tipos de nós
- ✅ Geração de código com métodos privados para cada nó
- ✅ Sistema de contexto interno para gerenciar dados entre nós

## 📚 Documentação

- [Guia de Instalação]({{ site.baseurl }}/pt/installation/)
- [Exemplos de Uso]({{ site.baseurl }}/pt/usage/)
- [Configuração de Ambiente]({{ site.baseurl }}/pt/env-setup/)
- [Guia de Contribuição]({{ site.baseurl }}/pt/contributing/)
- [Guia GitFlow]({{ site.baseurl }}/pt/gitflow/)
- [Guia de Testes]({{ site.baseurl }}/pt/testing/)
- [Changelog]({{ site.baseurl }}/pt/changelog/)

## 🎯 Exemplos

- [Exemplo AI Agent]({{ site.baseurl }}/pt/examples/ai-agent/)
- [Exemplo Construtor de Credenciais]({{ site.baseurl }}/pt/examples/credentials-constructor/)

## 📖 Início Rápido

1. Clone o repositório:
```bash
git clone <repository-url>
cd n8ncoding
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   - Copie `.env.example` para `.env`
   - Edite o arquivo `.env` e preencha suas credenciais:
   ```env
   N8N_URL=http://localhost:5678
   N8N_API_KEY=sua-api-key-aqui
   ```

4. Execute o programa:
```bash
python src/main.py
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o [Guia de Contribuição]({{ site.baseurl }}/pt/contributing/) antes de enviar pull requests.

## 📄 Licença

Este projeto é open-source. Consulte o arquivo LICENSE para mais detalhes.

