# GitFlow - Complete Guide for n8ncoding

This document provides a detailed guide on how to use GitFlow in the **n8ncoding** project.

## 📋 Table of Contents

1. [What is GitFlow?](#what-is-gitflow)
2. [Branch Structure](#branch-structure)
3. [Detailed Workflow](#detailed-workflow)
4. [Helper Scripts](#helper-scripts)
5. [Step-by-Step Practical Examples](#step-by-step-practical-examples)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)


## 🌿 What is GitFlow?

GitFlow is a Git branching model that organizes development into different types of branches, each with a specific purpose. This facilitates release management, features, and hotfixes.

### Advantages

- ✅ Clean and organized history
- ✅ Facilitates releases and versioning
- ✅ Isolates features in development
- ✅ Allows urgent fixes without affecting development
- ✅ Facilitates team collaboration


## 🌳 Branch Structure

### Main Branches (Permanent)

#### `main` (or `master`)

- **Purpose:** Production code
- **Characteristics:**
  - Always stable and tested
  - Each commit should generate a version tag
  - Protected against direct commits
  - Linear history (only merges from release/hotfix)

#### `develop`

- **Purpose:** Main development branch
- **Characteristics:**
  - Code being developed and tested
  - Base branch for new features
  - Receives merges from `feature/*`, `release/*` and `hotfix/*`
  - Can have direct commits (not recommended)

### Support Branches (Temporary)

#### `feature/*`

- **Origin:** `develop`
- **Destination:** `develop`
- **Purpose:** Develop new features
- **Examples:**
  - `feature/python-support`
  - `feature/code-node-template`
  - `feature/improve-expression-parser`

#### `release/*`

- **Origin:** `develop`
- **Destination:** `main` + `develop`
- **Purpose:** Prepare a new version for production
- **Characteristics:**
  - Only bug fixes
  - Version update
  - Final adjustments
  - **DO NOT** add new features
- **Examples:**
  - `release/v1.0.0`
  - `release/v1.1.0`

#### `hotfix/*`

- **Origin:** `main`
- **Destination:** `main` + `develop`
- **Purpose:** Urgent production fixes
- **Characteristics:**
  - Created from `main` (production code)
  - Critical fixes that cannot wait
  - Immediate merge to `main` and `develop`
- **Examples:**
  - `hotfix/fix-critical-bug`
  - `hotfix/security-vulnerability`


## 🔄 Detailed Workflow

### Feature Lifecycle

```
1. Create branch: develop → feature/name
2. Develop: commits in feature
3. Update: merge develop → feature (periodically)
4. Finish: merge feature → develop
5. Delete: feature branch (after merge)
```

### Release Lifecycle

```
1. Create branch: develop → release/v1.0.0
2. Prepare: final adjustments, version, changelog
3. Finish: merge release → main (tag) + develop
4. Delete: release branch
```

### Hotfix Lifecycle

```
1. Create branch: main → hotfix/name
2. Fix: commit the fix
3. Finish: merge hotfix → main (tag) + develop
4. Delete: hotfix branch
```


## 🛠️ Helper Scripts

The project includes scripts to facilitate GitFlow usage.

### Windows (PowerShell)

```powershell
# Feature
.\scripts\new-feature.ps1 feature-name
.\scripts\finish-feature.ps1 feature-name

# Release
.\scripts\new-release.ps1 1.0.0
.\scripts\finish-release.ps1 1.0.0

# Hotfix
.\scripts\new-hotfix.ps1 fix-name
.\scripts\finish-hotfix.ps1 fix-name
```

### Linux/Mac (Bash)

```bash
# Feature
./scripts/new-feature.sh feature-name
./scripts/finish-feature.sh feature-name

# Release
./scripts/new-release.sh 1.0.0
./scripts/finish-release.sh 1.0.0

# Hotfix
./scripts/new-hotfix.sh fix-name
./scripts/finish-hotfix.sh fix-name
```


## ✅ Best Practices

### Commits

1. **Make small, frequent commits**
2. **Use descriptive messages**
3. **Follow commit convention**

### Branches

1. **Keep branches updated**
2. **Delete branches after merge**
3. **Use descriptive names**


## 🔧 Troubleshooting

### Problem: Conflicts during merge

**Solution:**
```bash
# 1. Identify files with conflicts
git status

# 2. Open each file and resolve manually
# Look for: <<<<<<< HEAD

# 3. After resolving, add files
git add resolved-file.py

# 4. Complete merge
git commit -m "merge: resolve conflicts with develop"
```


**Last updated:** 2024