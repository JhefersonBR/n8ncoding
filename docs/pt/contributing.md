---
layout: page
title: Guia de Contribuição
lang: pt
ref: contributing
permalink: /pt/contributing/
---

# Contributing Guide - n8ncoding

This guide details how to contribute to the **n8ncoding** project following the **GitFlow** pattern.

## 📚 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [GitFlow Workflow](#gitflow-workflow)
4. [Practical Scenarios](#practical-scenarios)
5. [Commit Conventions](#commit-conventions)
6. [Contribution Checklist](#contribution-checklist)
7. [Conflict Resolution](#conflict-resolution)
8. [FAQ](#faq)


## 🎯 Prerequisites

Before starting, make sure you have:

- ✅ Git installed (version 2.20+)
- ✅ Python 3.8+ installed
- ✅ Repository access (fork or write permission)
- ✅ Basic Git knowledge (branch, commit, merge)


## ⚙️ Initial Setup

### 1. Fork and Clone Repository

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork locally
git clone https://github.com/YOUR-USERNAME/n8ncoding.git
cd n8ncoding

# 3. Add the original repository as upstream
git remote add upstream https://github.com/JhefersonBR/n8ncoding.git

# 4. Verify remotes
git remote -v
# Should show:
# origin    https://github.com/YOUR-USERNAME/n8ncoding.git (fetch)
# origin    https://github.com/YOUR-USERNAME/n8ncoding.git (push)
# upstream  https://github.com/JhefersonBR/n8ncoding.git (fetch)
# upstream  https://github.com/JhefersonBR/n8ncoding.git (push)
```

### 2. Configure Main Branches

```bash
# Make sure you're on the main branch
git checkout main

# Update the main branch
git pull upstream main

# Create/update the develop branch
git checkout -b develop
git pull upstream develop
git push -u origin develop
```

### 3. Setup Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit the .env file with your credentials
```


## 🔄 GitFlow Workflow

### Overview

```
main (production)
  │
  ├── develop (development)
  │     │
  │     ├── feature/new-feature
  │     ├── feature/another-feature
  │     │
  │     └── release/v1.0.0
  │
  └── hotfix/urgent-fix
```

### Branch Types

| Type | Origin | Destination | When to Use |
|------|--------|-------------|-------------|
| `feature/*` | `develop` | `develop` | New feature |
| `release/*` | `develop` | `main` + `develop` | Prepare new version |
| `hotfix/*` | `main` | `main` + `develop` | Urgent production fix |


## 🚀 Practical Scenarios

### Scenario 1: Developing a New Feature

**Situation:** You want to add support for the n8n "Send Email" node.

#### Step 1: Create Feature Branch

**Option A - Using Script (Recommended):**

```bash
# Linux/Mac
./scripts/new-feature.sh support-send-email

# Windows PowerShell
.\scripts\new-feature.ps1 support-send-email
```

**Option B - Manual:**

```bash
# 1. Make sure you're on develop and updated
git checkout develop
git pull upstream develop

# 2. Create the feature branch
git checkout -b feature/support-send-email

# 3. Push to your fork (optional, but recommended)
git push -u origin feature/support-send-email
```

#### Step 2: Develop Feature

```bash
# Make your changes to files
# Example: create templates/nodes/sendEmail.xml

# Add files
git add templates/nodes/sendEmail.xml
git add src/node_mapper.py  # if modified

# Commit following convention
git commit -m "feat: add template for Send Email node

- Create sendEmail.xml template
- Add mapping in node_mapper.py
- Support parameters: to, subject, body"
```

**💡 Tip:** Make small, frequent commits. It's better to have several small commits than one large one.

#### Step 3: Keep Branch Updated

```bash
# Periodically, update your branch with develop
git checkout develop
git pull upstream develop
git checkout feature/support-send-email
git merge develop
# Or use rebase (cleaner, but requires care):
# git rebase develop
```

#### Step 4: Test Locally

```bash
# Run tests
python tests/test.py

# Manual test
python src/main.py
# Select a workflow that uses Send Email
# Verify generated code is correct
```

#### Step 5: Finish Feature

**Option A - Using Script:**

```bash
# Linux/Mac
./scripts/finish-feature.sh support-send-email

# Windows PowerShell
.\scripts\finish-feature.ps1 support-send-email
```

**Option B - Manual:**

```bash
# 1. Make sure everything is committed
git status

# 2. Update develop
git checkout develop
git pull upstream develop

# 3. Merge feature
git merge feature/support-send-email

# 4. Resolve conflicts if any (see section below)

# 5. Push to upstream
git push upstream develop

# 6. Delete local branch (optional)
git branch -d feature/support-send-email

# 7. Delete remote branch (if created)
git push origin --delete feature/support-send-email
```

#### Step 6: Create Pull Request (if using fork)

1. Go to GitHub
2. Click "New Pull Request"
3. Select `develop` as base
4. Select your `feature/support-send-email` branch
5. Fill in the PR template
6. Wait for review and approval


## 📝 Commit Conventions

We follow the **Conventional Commits** pattern. Format:

```
<type>(<scope>): <short description>

<detailed body (optional)>

<footer (optional)>
```

### Commit Types

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add Python support` |
| `fix` | Bug fix | `fix: fix error in node ordering` |
| `docs` | Documentation | `docs: update contributing guide` |
| `style` | Formatting | `style: fix indentation in generator.py` |
| `refactor` | Refactoring | `refactor: improve NodeMapper structure` |
| `test` | Tests | `test: add tests for ExpressionParser` |
| `chore` | Maintenance tasks | `chore: update dependencies` |
| `perf` | Performance improvement | `perf: optimize topological ordering` |

### Examples of Commits

#### ✅ Good

```bash
git commit -m "feat: add support for multiple languages

- Implement templates for Python and JavaScript
- Add LanguageSelector for interactive choice
- Update generator to support multiple languages
- Create credential classes for each language"
```

#### ❌ Bad

```bash
git commit -m "changes"
git commit -m "fix bug"
git commit -m "WIP"
git commit -m "update files"
```


## ✅ Contribution Checklist

Before making merge or creating PR, verify:

### Code

- [ ] Code follows project standards
- [ ] No lint errors (`python -m flake8 src/` or equivalent)
- [ ] Tests pass (`python tests/test.py`)
- [ ] Manual tests performed
- [ ] No commented or debug code

### Git

- [ ] Commits follow convention (feat:, fix:, etc.)
- [ ] Branch updated with develop/main
- [ ] No conflicts
- [ ] Clear and descriptive commit messages

### Documentation

- [ ] README updated (if necessary)
- [ ] CHANGELOG updated (if necessary)
- [ ] Code comments (if complex code)
- [ ] Documentation of new features

### Functionality

- [ ] Feature tested locally
- [ ] Use cases tested
- [ ] No regressions introduced
- [ ] Compatible with previous versions (if applicable)


## 🔧 Conflict Resolution

### During Merge

If there are conflicts during merge:

```bash
# 1. Identify files with conflicts
git status

# 2. Open files and look for markers:
# <<<<<<< HEAD
# code from current branch
# =======
# code from branch being merged
# >>>>>>> feature/name-of-feature

# 3. Resolve manually, removing markers
# 4. Add resolved files
git add resolved-file.py

# 5. Complete merge
git commit -m "merge: resolve conflicts with develop"
```


## ❓ FAQ

### Can I commit directly to develop?

**Not recommended.** Use feature branches to isolate changes and facilitate review.

### When to use rebase vs merge?

- **Merge**: Preserves complete history, safer
- **Rebase**: Linear history, cleaner, but requires care

**Recommendation:** Use merge to start. Rebase only if you know what you're doing.

### How to update my fork?

```bash
git checkout main
git pull upstream main
git push origin main

git checkout develop
git pull upstream develop
git push origin develop
```


**Last updated:** 2024