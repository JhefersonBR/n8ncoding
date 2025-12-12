---
layout: page
title: Home
lang: en
ref: index
permalink: /en/
---

# n8ncoding

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

## 📚 Documentation

- [Installation Guide]({{ site.baseurl }}/en/installation/)
- [Usage Examples]({{ site.baseurl }}/en/usage/)
- [Environment Setup]({{ site.baseurl }}/en/env-setup/)
- [Contributing Guide]({{ site.baseurl }}/en/contributing/)
- [GitFlow Guide]({{ site.baseurl }}/en/gitflow/)
- [Testing Guide]({{ site.baseurl }}/en/testing/)
- [Changelog]({{ site.baseurl }}/en/changelog/)

## 🎯 Examples

- [AI Agent Example]({{ site.baseurl }}/en/examples/ai-agent/)
- [Credentials Constructor Example]({{ site.baseurl }}/en/examples/credentials-constructor/)

## 📖 Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
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

4. Run the program:
```bash
python src/main.py
```

## 🤝 Contributing

Contributions are welcome! Please read the [Contributing Guide]({{ site.baseurl }}/en/contributing/) before submitting pull requests.

## 📄 License

This project is open-source. See the LICENSE file for details.

