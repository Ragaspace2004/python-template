# Workflow-Specific Labels

## Overview

PRs are now automatically labeled based on which workflow runs, making it easy to see which checks have been performed.

## Label Behavior

### Pre-commit CI Workflow

When the Pre-commit CI workflow runs on a PR, it adds:

**On Success:**
- ✅ `pre-commit` - Indicates this workflow ran
- ✅ `ci-passed` - All checks passed
- ✅ `ready-for-review` - PR is ready for review

**On Failure:**
- ❌ `pre-commit` - Indicates this workflow ran
- ❌ `ci-failed` - Checks failed

### Semgrep Security Scan Workflow

When the Semgrep workflow runs on a PR, it adds:

**On Success:**
- ✅ `semgrep` - Indicates this workflow ran
- ✅ `security-passed` - Security scan passed

**On Failure:**
- ❌ `semgrep` - Indicates this workflow ran
- ❌ `security-findings` - Security issues found
- ❌ `semgrep-failed` - Semgrep scan failed
- 💬 Adds a comment with details

## Example PR Labels

### Scenario 1: All Checks Pass
A PR that passes both workflows will have:
- `pre-commit`
- `ci-passed`
- `ready-for-review`
- `semgrep`
- `security-passed`

### Scenario 2: Pre-commit Fails
A PR where pre-commit fails will have:
- `pre-commit`
- `ci-failed`
- `semgrep`
- `security-passed` (if Semgrep passed)

### Scenario 3: Security Issues Found
A PR with security issues will have:
- `pre-commit`
- `ci-passed` (if pre-commit passed)
- `ready-for-review`
- `semgrep`
- `security-findings`
- `semgrep-failed`

## Filtering PRs

You can filter PRs by workflow:

**View all PRs checked by Pre-commit:**
```
label:pre-commit
```

**View all PRs scanned by Semgrep:**
```
label:semgrep
```

**View PRs with security issues:**
```
label:security-findings
```

**View PRs ready for review:**
```
label:ready-for-review
```

## Available Labels

### Workflow Labels
- `pre-commit` (blue) - Pre-commit CI workflow ran
- `semgrep` (red) - Semgrep security scan workflow ran

### Status Labels
- `ci-passed` (green) - All CI checks passed
- `ci-failed` (red) - CI checks failed
- `security-passed` (green) - Security scan passed
- `security-findings` (pink) - Security issues found
- `semgrep-failed` (light pink) - Semgrep scan failed
- `ready-for-review` (green) - PR is ready for review

### Other Labels
- `python` - Python code changes
- `tests` - Test related changes
- `ci-cd` - CI/CD pipeline changes
- `documentation` - Documentation changes
- `configuration` - Configuration changes
- `dependencies` - Dependency updates
- `bug` - Bug fix
- `enhancement` - New feature
- `hotfix` - Emergency hotfix
- `priority: critical/high/medium/low` - Priority levels

## Setup

To create all labels in your repository:

1. Go to **Actions** tab
2. Select **"Setup Repository Labels"** workflow
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"**

This will create all the labels with proper colors and descriptions.

## Benefits

✅ **Easy filtering** - Quickly find PRs by workflow
✅ **Clear visibility** - See which checks ran at a glance
✅ **Better organization** - Categorize PRs by check type
✅ **Audit trail** - Track which workflows processed each PR
✅ **Team coordination** - Know which checks need attention

## Workflow Run Names

In addition to PR labels, workflow runs also show which workflow ran:

- "Pre-commit CI [Bot] - pull_request by username"
- "Semgrep Security Scan [Bot] - pull_request by username"

This makes it easy to identify workflows in the Actions tab.
