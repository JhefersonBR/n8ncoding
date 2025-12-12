---
layout: default
lang: en
redirect_from:
  - /docs/
---

# n8ncoding Documentation

Welcome to the n8ncoding documentation! This tool converts n8n workflows into reusable code classes in multiple languages.

## Quick Start

1. [Installation Guide]({{ site.baseurl }}/en/installation/)
2. [Usage Examples]({{ site.baseurl }}/en/usage/)
3. [Contributing]({{ site.baseurl }}/en/contributing/)

## Available Languages

- [English (en)]({{ site.baseurl }}/en/) - Default
- [Português (pt)]({{ site.baseurl }}/pt/)

<script>
  // Redirect to English by default
  if (window.location.pathname === '{{ site.baseurl }}/' || window.location.pathname === '{{ site.baseurl }}') {
    window.location.href = '{{ site.baseurl }}/en/';
  }
</script>

