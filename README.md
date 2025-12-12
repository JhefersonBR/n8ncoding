# n8ncoding

Converter n8n workflows to code classes in multiple languages.

## 📚 Documentation

Full multilingual documentation is available on GitHub Pages:
- **Home:** [https://jhefersonbr.github.io/n8ncoding/](https://jhefersonbr.github.io/n8ncoding/)
- **English (default):** [https://jhefersonbr.github.io/n8ncoding/en/](https://jhefersonbr.github.io/n8ncoding/en/)
- **Português:** [https://jhefersonbr.github.io/n8ncoding/pt/](https://jhefersonbr.github.io/n8ncoding/pt/)

---

## 📋 Description

**n8ncoding** is an open-source tool that converts n8n workflows into reusable code classes. Currently supports PHP, Python, and JavaScript, with plans to expand to other languages.

## 🚀 Features

- ✅ Connection with n8n API
- ✅ List available workflows
- ✅ Interactive workflow selection in terminal
- ✅ Convert workflows to PHP, Python, and JavaScript classes
- ✅ Preserve n8n folder structure
- ✅ Configurable XML templates for different node types
- ✅ Code generation with private methods for each node
- ✅ Internal context system to manage data between nodes

## 📁 Project Structure

```
n8ncoding/
│
├── config/
│   └── settings.json          # n8n and output configurations
│
├── templates/
│   ├── nodes/                 # Node type templates
│   │   ├── httpRequest.xml
│   │   ├── function.xml
│   │   ├── aiAgent.xml
│   │   └── ...
│   └── languages/             # Language templates
│       ├── php.xml
│       ├── python.xml
│       └── javascript.xml
│
├── src/
│   ├── main.py                # Main entry point
│   ├── n8n_client.py          # n8n API client
│   ├── xml_loader.py          # XML template loader
│   ├── node_mapper.py         # Node to method mapper
│   ├── generator.py           # Code generator
│   ├── folder_structure.py    # Folder structure manager
│   └── workflow_selector.py   # Interactive workflow selector
│
└── output/                    # Generated files
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/JhefersonBR/n8ncoding.git
cd n8ncoding
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Edit the `.env` file and fill in your credentials:
   ```env
   N8N_URL=http://localhost:5678
   N8N_API_KEY=your-api-key-here
   ```
   
   The `config/settings.json` file is already configured to use these variables.
   
   📖 See more details in [ENV_SETUP.md](ENV_SETUP.md)

## 📖 Usage

Run the main program:

```bash
python src/main.py
```

The program will:
1. Connect to n8n using the configured credentials
2. List all available workflows
3. Allow you to select which workflows to convert
4. Allow you to select target languages (multiple choice)
5. Generate the corresponding classes in the `output/` folder

### Selection Example

```
Choose the workflows you want to convert:
============================================================
[1] Send Automatic Email (ID: abc123)
[2] Update CRM (ID: def456)
[3] Extract Data from Google Sheets (ID: ghi789)
============================================================

Enter numbers separated by commas (Ex: 1,3,4): 1,3
```

## 📝 Templates

### Language Template (php.xml)

Defines the structure of the generated class:

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

### Node Template (function.xml)

Defines how a specific node type is converted:

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

## 🔧 Development

### Adding New Node Types

1. Create a new XML file in `templates/nodes/`
2. Define the method structure using placeholders
3. The `node_mapper.py` will automatically load the template

### Adding New Languages

1. Create a new XML file in `templates/languages/`
2. Use the placeholders `{{class_name}}`, `{{steps_calls}}` and `{{steps_methods}}`
3. Update the configuration to use the new language

## 🌿 GitFlow

This project uses the **GitFlow** pattern for branch and release management.

### Branch Structure

- **`main`** - Production code (always stable)
- **`develop`** - Development code (main branch)
- **`feature/*`** - New features
- **`release/*`** - Release preparation
- **`hotfix/*`** - Urgent production fixes

### Helper Scripts

**Windows (PowerShell):**
```powershell
.\scripts\new-feature.ps1 feature-name
.\scripts\finish-feature.ps1 feature-name
.\scripts\new-release.ps1 1.0.0
.\scripts\finish-release.ps1 1.0.0
.\scripts\new-hotfix.ps1 hotfix-name
.\scripts\finish-hotfix.ps1 hotfix-name
```

**Linux/Mac (Bash):**
```bash
./scripts/new-feature.sh feature-name
./scripts/finish-feature.sh feature-name
./scripts/new-release.sh 1.0.0
./scripts/finish-release.sh 1.0.0
./scripts/new-hotfix.sh hotfix-name
./scripts/finish-hotfix.sh hotfix-name
```

### Complete Documentation

- 📖 **[GITFLOW.md](GITFLOW.md)** - Complete GitFlow guide with practical examples
- 📖 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Detailed guide on how to contribute to the project

## 📄 License

This project is open-source. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request.

**Before contributing:**
1. Read the complete guide in [CONTRIBUTING.md](CONTRIBUTING.md)
2. Read the GitFlow guide in [GITFLOW.md](GITFLOW.md)
3. Create a `feature/feature-name` branch from `develop`
4. Follow commit conventions (feat:, fix:, docs:, etc.)
5. Make sure tests pass (`python tests/test.py`)
6. Merge back to `develop`

## 📌 Roadmap

- [ ] Support for more n8n node types
- [x] Support for Python
- [x] Support for JavaScript/TypeScript
- [ ] Improvements in JavaScript to other languages code conversion
- [ ] Workflow validation before conversion
- [ ] Batch mode to process multiple workflows without interaction
