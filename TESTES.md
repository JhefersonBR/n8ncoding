# Guia de Testes do n8ncoding

Este documento explica como executar testes da aplicação n8ncoding.

## 🧪 Tipos de Teste

### 1. Teste Automatizado (Recomendado)

Execute o script de teste que valida todos os componentes:

```bash
python src/test.py
```

Este script executa:
- ✅ Teste do XML Loader (carregamento de templates)
- ✅ Teste do Node Mapper (mapeamento de nós)
- ✅ Teste do Generator (geração de código)
- ✅ Teste do Fluxo Completo (geração e salvamento)

**Vantagens:**
- Não precisa de servidor n8n rodando
- Testa todos os componentes isoladamente
- Mostra resultados detalhados
- Gera um arquivo de teste na pasta `output/`

### 2. Teste com n8n Real

Para testar com um servidor n8n real:

1. **Configure o arquivo `.env`:**
   ```env
   N8N_URL=http://localhost:5678
   N8N_API_KEY=sua-api-key-aqui
   ```

2. **Execute a aplicação principal:**
   ```bash
   python src/main.py
   ```

3. **Siga as instruções no terminal:**
   - O programa tentará conectar ao n8n
   - Listará os workflows disponíveis
   - Você poderá selecionar quais converter

### 3. Teste de Componentes Individuais

Você também pode testar componentes específicos usando Python interativo:

```python
# Teste do XML Loader
from src.xml_loader import XMLLoader
loader = XMLLoader()
template = loader.load_language_template('php')
print(template)

# Teste do Node Mapper
from src.node_mapper import NodeMapper
mapper = NodeMapper(loader)
# ... etc
```

## 📊 Interpretando os Resultados

### Teste Automatizado

O script `test.py` mostra:

```
============================================================
TESTE 1: XML Loader
============================================================
✓ Template PHP carregado com sucesso
  Tamanho: 234 caracteres
✓ Template de nó 'function' carregado
✓ Template de nó 'httpRequest' carregado

============================================================
RESUMO DOS TESTES
============================================================
✓ PASSOU: XML Loader
✓ PASSOU: Node Mapper
✓ PASSOU: Generator
✓ PASSOU: Fluxo Completo

Total: 4/4 testes passaram
🎉 Todos os testes passaram!
```

### Teste com n8n Real

Se tudo estiver funcionando, você verá:

```
============================================================
n8ncoding - Conversor de Workflows n8n para Código
============================================================

Conectando ao n8n em: http://localhost:5678
✓ Conexão estabelecida com sucesso!

Buscando workflows...
✓ 5 workflow(s) encontrado(s).

Escolha os workflows que deseja converter:
============================================================
[1] Workflow 1 (ID: abc123)
[2] Workflow 2 (ID: def456)
...
```

## 🔧 Solução de Problemas

### Erro: "Template não encontrado"

**Causa:** Arquivos de template faltando ou caminho incorreto.

**Solução:**
- Verifique se a pasta `templates/` existe
- Verifique se os arquivos `php.xml`, `function.xml`, etc. existem
- Execute `python src/test.py` para verificar

### Erro: "Não foi possível conectar ao n8n"

**Causa:** Servidor n8n não está rodando ou credenciais incorretas.

**Solução:**
- Verifique se o n8n está rodando: `http://localhost:5678`
- Verifique o arquivo `.env` com as credenciais corretas
- Use `python src/test.py` para testar sem n8n

### Erro: "ModuleNotFoundError: No module named 'dotenv'"

**Causa:** Dependência não instalada.

**Solução:**
```bash
pip install -r requirements.txt
```

## 📝 Exemplo de Execução Completa

```bash
# 1. Instalar dependências (se ainda não instalou)
pip install -r requirements.txt

# 2. Executar testes automatizados
python src/test.py

# 3. Se os testes passarem, testar com n8n real
# (Configure o .env primeiro)
python src/main.py
```

## 🎯 Checklist de Testes

Antes de fazer commit, certifique-se de que:

- [ ] `python src/test.py` executa sem erros
- [ ] Todos os testes passam (4/4)
- [ ] Arquivo de teste é gerado em `output/`
- [ ] Templates XML são carregados corretamente
- [ ] Código PHP gerado está válido

## 💡 Dicas

1. **Execute os testes sempre antes de fazer commit**
2. **Use `test.py` para desenvolvimento rápido** (não precisa de n8n)
3. **Use `main.py` para testar integração completa** (precisa de n8n)
4. **Verifique os arquivos gerados em `output/`** após os testes

