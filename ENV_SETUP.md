# Configuração de Variáveis de Ambiente

O projeto agora suporta o uso de variáveis de ambiente através de arquivos `.env` para manter as credenciais seguras e fora do controle de versão.

## 📋 Como Configurar

### 1. Criar o arquivo `.env`

Copie o arquivo `.env.example` para `.env`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2. Editar o arquivo `.env`

Abra o arquivo `.env` e preencha com suas credenciais:

```env
N8N_URL=http://localhost:5678
N8N_API_KEY=sua-api-key-real-aqui
```

### 3. O arquivo `config/settings.json`

O arquivo `settings.json` agora usa referências às variáveis de ambiente:

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

As variáveis serão automaticamente resolvidas quando o programa executar.

## 🔒 Segurança

- ✅ O arquivo `.env` está no `.gitignore` e **não será commitado** no Git
- ✅ O arquivo `.env.example` pode ser versionado como template
- ✅ As credenciais ficam apenas no seu ambiente local

## 📝 Variáveis Disponíveis

- `N8N_URL`: URL do servidor n8n (ex: `http://localhost:5678`)
- `N8N_API_KEY`: Chave de API do n8n

## 🚀 Uso

Após configurar o `.env`, execute o programa normalmente:

```bash
python src/main.py
```

O programa carregará automaticamente as variáveis do arquivo `.env` e resolverá as referências no `settings.json`.

## 💡 Dica

Se você não criar o arquivo `.env`, o programa ainda funcionará, mas as variáveis `${N8N_URL}` e `${N8N_API_KEY}` serão resolvidas como strings vazias. Nesse caso, você pode preencher manualmente quando solicitado ou editar diretamente o `settings.json`.

