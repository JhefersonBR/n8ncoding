# n8ncoding

Conversor de workflows do n8n para classes de código em várias linguagens.

## 📋 Descrição

O **n8ncoding** é uma ferramenta open-source que permite converter workflows do n8n em classes de código reutilizáveis. Atualmente suporta PHP, com planos para expandir para outras linguagens.

## 🚀 Funcionalidades

- ✅ Conexão com API do n8n
- ✅ Listagem de workflows disponíveis
- ✅ Seleção interativa de workflows no terminal
- ✅ Conversão de workflows em classes PHP
- ✅ Preservação da estrutura de pastas do n8n
- ✅ Templates XML configuráveis para diferentes tipos de nós
- ✅ Geração de código com métodos privados para cada nó
- ✅ Sistema de contexto interno para gerenciar dados entre nós

## 📁 Estrutura do Projeto

```
n8ncoding/
│
├── config/
│   └── settings.json          # Configurações do n8n e saída
│
├── templates/
│   ├── nodes/                 # Templates de tipos de nós
│   │   ├── httpRequest.xml
│   │   ├── function.xml
│   │   ├── aiAgent.xml
│   │   └── ...
│   └── languages/             # Templates de linguagens
│       ├── php.xml
│
├── src/
│   ├── main.py                # Ponto de entrada principal
│   ├── n8n_client.py          # Cliente para API do n8n
│   ├── xml_loader.py          # Carregador de templates XML
│   ├── node_mapper.py         # Mapeador de nós para métodos
│   ├── generator.py           # Gerador de código
│   ├── folder_structure.py    # Gerenciador de estrutura de pastas
│   └── workflow_selector.py   # Seletor interativo de workflows
│
└── output/                    # Arquivos gerados
```

## 🛠️ Instalação

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
   
   O arquivo `config/settings.json` já está configurado para usar essas variáveis.
   
   📖 Veja mais detalhes em [ENV_SETUP.md](ENV_SETUP.md)

## 📖 Uso

Execute o programa principal:

```bash
python src/main.py
```

O programa irá:
1. Conectar ao n8n usando as credenciais configuradas
2. Listar todos os workflows disponíveis
3. Permitir que você selecione quais workflows converter
4. Gerar as classes PHP correspondentes na pasta `output/`

### Exemplo de Seleção

```
Escolha os workflows que deseja converter:
============================================================
[1] Enviar Email Automático (ID: abc123)
[2] Atualizar CRM (ID: def456)
[3] Extrair Dados do Google Sheets (ID: ghi789)
============================================================

Digite os números separados por vírgula (Ex: 1,3,4): 1,3
```

## 📝 Templates

### Template de Linguagem (php.xml)

Define a estrutura da classe gerada:

```xml
<language>
    <class>
        <![CDATA[
<?php

class {{class_name}} {
    private array $context = [];
    
    public function run(array $params = []): mixed
    {
        $this->context = $params;
        {{steps_calls}}
        return $this->context;
    }
    
    {{steps_methods}}
}
        ]]>
    </class>
</language>
```

### Template de Nó (function.xml)

Define como um tipo específico de nó é convertido:

```xml
<node>
    <name>function</name>
    <method>
        <![CDATA[
private function {{method_name}}(): void
{
    {{generated_code}}
}
        ]]>
    </method>
</node>
```

## 🔧 Desenvolvimento

### Adicionar Novos Tipos de Nós

1. Crie um novo arquivo XML em `templates/nodes/`
2. Defina a estrutura do método usando placeholders
3. O `node_mapper.py` automaticamente carregará o template

### Adicionar Novas Linguagens

1. Crie um novo arquivo XML em `templates/languages/`
2. Use os placeholders `{{class_name}}`, `{{steps_calls}}` e `{{steps_methods}}`
3. Atualize a configuração para usar a nova linguagem

## 🌿 GitFlow

Este projeto utiliza o padrão **GitFlow** para gerenciamento de branches e releases.

### Estrutura de Branches

- **`main`** - Código em produção (sempre estável)
- **`develop`** - Código em desenvolvimento (branch principal)
- **`feature/*`** - Novas funcionalidades
- **`release/*`** - Preparação para releases
- **`hotfix/*`** - Correções urgentes em produção

### Scripts Auxiliares

**Windows (PowerShell):**
```powershell
.\scripts\new-feature.ps1 nome-da-feature
.\scripts\finish-feature.ps1 nome-da-feature
.\scripts\new-release.ps1 1.0.0
.\scripts\finish-release.ps1 1.0.0
.\scripts\new-hotfix.ps1 nome-do-hotfix
.\scripts\finish-hotfix.ps1 nome-do-hotfix
```

**Linux/Mac (Bash):**
```bash
./scripts/new-feature.sh nome-da-feature
./scripts/finish-feature.sh nome-da-feature
./scripts/new-release.sh 1.0.0
./scripts/finish-release.sh 1.0.0
./scripts/new-hotfix.sh nome-do-hotfix
./scripts/finish-hotfix.sh nome-do-hotfix
```

### Documentação Completa

- 📖 **[GITFLOW.md](GITFLOW.md)** - Guia completo do GitFlow com exemplos práticos
- 📖 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia detalhado de como contribuir com o projeto

## 📄 Licença

Este projeto é open-source. Consulte o arquivo LICENSE para mais detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

**Antes de contribuir:**
1. Leia o guia completo em [CONTRIBUTING.md](CONTRIBUTING.md)
2. Leia o guia de GitFlow em [GITFLOW.md](GITFLOW.md)
3. Crie uma branch `feature/nome-da-feature` a partir de `develop`
4. Siga a convenção de commits (feat:, fix:, docs:, etc.)
5. Certifique-se de que os testes passam (`python src/test.py`)
6. Faça merge de volta para `develop`

## 📌 Roadmap

- [ ] Suporte para mais tipos de nós do n8n
- [ ] Suporte para Python
- [ ] Suporte para JavaScript/TypeScript
- [ ] Melhorias na conversão de código JavaScript para outras linguagens
- [ ] Validação de workflows antes da conversão
- [ ] Modo batch para processar múltiplos workflows sem interação

