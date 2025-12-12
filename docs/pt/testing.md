---
layout: page
title: Guia de Testes
lang: pt
ref: testing
permalink: /pt/testing/
---

# n8ncoding Testing Guide

This document explains how to run tests for the n8ncoding application.

## 🧪 Test Types

### 1. Automated Test (Recommended)

Run the test script that validates all components:

```bash
python tests/test.py
```

This script runs:
- ✅ XML Loader test (template loading)
- ✅ Node Mapper test (node mapping)
- ✅ Generator test (code generation)
- ✅ Complete Flow test (generation and saving)

**Advantages:**
- No need for n8n server running
- Tests all components in isolation
- Shows detailed results
- Generates a test file in the `output/` folder

### 2. Test with Real n8n

To test with a real n8n server:

1. **Configure the `.env` file:**
   ```env
   N8N_URL=http://localhost:5678
   N8N_API_KEY=your-api-key-here
   ```

2. **Run the main application:**
   ```bash
   python src/main.py
   ```

3. **Follow instructions in terminal:**
   - The program will try to connect to n8n
   - Will list available workflows
   - You can select which ones to convert

### 3. Individual Component Tests

You can also test specific components using interactive Python:

```python
# XML Loader test
from src.xml_loader import XMLLoader
loader = XMLLoader()
template = loader.load_language_template('php')
print(template)

# Node Mapper test
from src.node_mapper import NodeMapper
mapper = NodeMapper(loader)
# ... etc
```

## 📊 Interpreting Results

### Automated Test

The `test.py` script shows:

```
============================================================
TEST 1: XML Loader
============================================================
✓ PHP template loaded successfully
  Size: 234 characters
✓ Node template 'function' loaded
✓ Node template 'httpRequest' loaded

============================================================
TEST SUMMARY
============================================================
✓ PASSED: XML Loader
✓ PASSED: Node Mapper
✓ PASSED: Generator
✓ PASSED: Complete Flow

Total: 4/4 tests passed
🎉 All tests passed!
```

## 🔧 Troubleshooting

### Error: "Template not found"

**Cause:** Missing template files or incorrect path.

**Solution:**
- Check if the `templates/` folder exists
- Check if files `php.xml`, `function.xml`, etc. exist
- Run `python tests/test.py` to verify

### Error: "Could not connect to n8n"

**Cause:** n8n server is not running or incorrect credentials.

**Solution:**
- Check if n8n is running: `http://localhost:5678`
- Check the `.env` file with correct credentials
- Use `python tests/test.py` to test without n8n

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Cause:** Dependency not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

## 📝 Complete Execution Example

```bash
# 1. Install dependencies (if not already installed)
pip install -r requirements.txt

# 2. Run automated tests
python tests/test.py

# 3. If tests pass, test with real n8n
# (Configure .env first)
python src/main.py
```

## 🎯 Testing Checklist

Before committing, make sure:

- [ ] `python tests/test.py` runs without errors
- [ ] All tests pass (4/4)
- [ ] Test file is generated in `output/`
- [ ] XML templates are loaded correctly
- [ ] Generated PHP code is valid

## 💡 Tips

1. **Always run tests before committing**
2. **Use `test.py` for rapid development** (no n8n needed)
3. **Use `main.py` to test complete integration** (needs n8n)
4. **Check generated files in `output/`** after tests