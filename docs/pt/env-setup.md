---
layout: page
title: Configuração de Ambiente
lang: pt
ref: env-setup
permalink: /pt/env-setup/
---

# Environment Variables Setup

The project now supports the use of environment variables through `.env` files to keep credentials secure and out of version control.

## 📋 How to Configure

### 1. Create the `.env` file

Copy the `.env.example` file to `.env`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2. Edit the `.env` file

Open the `.env` file and fill in your credentials:

```env
N8N_URL=http://localhost:5678
N8N_API_KEY=your-real-api-key-here
```

### 3. The `config/settings.json` file

The `settings.json` file now uses references to environment variables:

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

Variables will be automatically resolved when the program runs.

## 🔒 Security

- ✅ The `.env` file is in `.gitignore` and **will not be committed** to Git
- ✅ The `.env.example` file can be versioned as a template
- ✅ Credentials stay only in your local environment

## 📝 Available Variables

- `N8N_URL`: n8n server URL (e.g., `http://localhost:5678`)
- `N8N_API_KEY`: n8n API key

## 🚀 Usage

After configuring `.env`, run the program normally:

```bash
python src/main.py
```

The program will automatically load variables from the `.env` file and resolve references in `settings.json`.

## 💡 Tip

If you don't create the `.env` file, the program will still work, but the `${N8N_URL}` and `${N8N_API_KEY}` variables will be resolved as empty strings. In that case, you can fill them manually when prompted or edit `settings.json` directly.