---
layout: page
title: Installation
lang: en
ref: installation
permalink: /en/installation/
---

# Installation Guide

This guide will help you install and configure n8ncoding.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Access to an n8n instance (local or remote)

## Step 1: Clone the Repository

```bash
git clone https://github.com/JhefersonBR/n8ncoding.git
cd n8ncoding
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required Python packages:
- `requests` - For API communication
- `python-dotenv` - For environment variable management
- `lxml` - For XML template processing

## Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit the `.env` file and fill in your credentials:

```env
N8N_URL=http://localhost:5678
N8N_API_KEY=your-api-key-here
```

**Important:** The `.env` file should not be committed to Git (it's already in `.gitignore`).

## Step 4: Verify Installation

Run the test script to verify everything is working:

```bash
python tests/test.py
```

If all tests pass, you're ready to use n8ncoding!

## Next Steps

- Read the [Usage Guide]({{ site.baseurl }}/en/usage/) to learn how to use the tool
- Check the [Environment Setup]({{ site.baseurl }}/en/env-setup/) for detailed configuration options

