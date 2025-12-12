---
layout: page
title: Instalação
lang: pt
ref: installation
permalink: /pt/installation/
---

# Guia de Instalação

Este guia ajudará você a instalar e configurar o n8ncoding.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Acesso a uma instância do n8n (local ou remota)

## Passo 1: Clonar o Repositório

```bash
git clone https://github.com/JhefersonBR/n8ncoding.git
cd n8ncoding
```

## Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso instalará todos os pacotes Python necessários:
- `requests` - Para comunicação com API
- `python-dotenv` - Para gerenciamento de variáveis de ambiente
- `lxml` - Para processamento de templates XML

## Passo 3: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o arquivo `.env` e preencha suas credenciais:

```env
N8N_URL=http://localhost:5678
N8N_API_KEY=sua-api-key-aqui
```

**Importante:** O arquivo `.env` não deve ser commitado no Git (já está no `.gitignore`).

## Passo 4: Verificar Instalação

Execute o script de teste para verificar se tudo está funcionando:

```bash
python tests/test.py
```

Se todos os testes passarem, você está pronto para usar o n8ncoding!

## Próximos Passos

- Leia o [Guia de Uso]({{ site.baseurl }}/pt/usage/) para aprender como usar a ferramenta
- Verifique a [Configuração de Ambiente]({{ site.baseurl }}/pt/env-setup/) para opções detalhadas de configuração

