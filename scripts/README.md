# Scripts

Utility scripts for managing the DevSecOps CI pipeline.

## Label Creation Scripts

These scripts create all the necessary GitHub labels for the repository.

### Prerequisites

Install GitHub CLI: https://cli.github.com/

**Windows:**
```powershell
winget install --id GitHub.cli
```

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh
```

### Authenticate with GitHub

```bash
gh auth login
```

### Usage

**Windows (PowerShell):**
```powershell
.\scripts\create-labels.ps1
```

**Linux/macOS (Bash):**
```bash
chmod +x scripts/create-labels.sh
./scripts/create-labels.sh
```

### Alternative: GitHub Actions

You can also create labels using the GitHub Actions workflow:

1. Go to **Actions** tab in your repository
2. Select **"Setup Repository Labels"** workflow
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"**

## Labels Created

The scripts create the following labels:

### CI/CD Labels
- `ci-passed` - All CI checks passed
- `ci-failed` - CI checks failed
- `ci-cd` - CI/CD pipeline changes

### Security Labels
- `security` - Security related changes
- `security-review-needed` - Requires security team review
- `security-findings` - Security scan found issues
- `semgrep-failed` - Semgrep scan failed

### Priority Labels
- `priority: critical` - Critical priority
- `priority: high` - High priority
- `priority: medium` - Medium priority
- `priority: low` - Low priority

### Type Labels
- `hotfix` - Emergency hotfix
- `bug` - Bug fix
- `enhancement` - New feature or enhancement
- `dependencies` - Dependency updates

### Component Labels
- `python` - Python code changes
- `tests` - Test related changes
- `documentation` - Documentation changes
- `configuration` - Configuration changes

### Status Labels
- `ready-for-review` - Ready for code review
- `work-in-progress` - Work in progress
- `blocked` - Blocked by dependencies
- `needs-testing` - Needs testing
