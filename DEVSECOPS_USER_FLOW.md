# Python DevSecOps CI Pipeline - User Flow Documentation

## Overview
This document describes the complete user flow for the Python DevSecOps CI pipeline, including normal operations, edge cases, and emergency override procedures.

---

## 1. Normal Development Flow

### 1.1 Developer Writes Code
**Actor:** Developer
**Action:** Creates or modifies Python code in local environment

**Next Steps:**
- Developer commits code locally
- Pre-commit hooks are triggered automatically

---

### 1.2 Pre-commit Hooks Execution (Local)
**Trigger:** `git commit`
**Location:** Developer's local machine
**Configuration:** `.pre-commit-config.yaml`

#### Checks Performed (Sequential):

1. **Universal Checks** (BLOCKING)
   - Trailing whitespace removal
   - End-of-file fixer
   - YAML validation
   - XML validation

2. **Black Formatter** (BLOCKING)
   - Auto-formats Python code
   - Ensures consistent code style
   - **Failure Action:** Commit blocked, files auto-formatted, developer must re-stage

3. **Pylint** (NON-BLOCKING - Optional)
   - Code quality analysis
   - Uses `.pylintrc` configuration
   - **Failure Action:** Warning displayed, commit proceeds (`--exit-zero`)

4. **Bandit Security Scan** (BLOCKING)
   - Scans for security vulnerabilities
   - Severity: Low-Low (`-ll`)
   - **Failure Action:** Commit blocked if security issues found

5. **Gitleaks Secret Detection** (BLOCKING)
   - Scans for hardcoded secrets, API keys, tokens
   - Uses `.gitleaks.toml` configuration
   - **Failure Action:** Commit blocked if secrets detected

6. **Pytest** (BLOCKING)
   - Runs all Python tests
   - **Failure Action:** Commit blocked if tests fail

#### Outcomes:
- ✅ **PASS:** All checks pass → Commit successful → Developer pushes code
- ❌ **FAIL:** Any blocking check fails → Commit blocked → Developer fixes issues

---

### 1.3 Push Code to Repository
**Actor:** Developer
**Action:** `git push origin <branch>`


**Triggers:**
- GitHub Actions CI workflows
- Dependabot checks (if dependencies modified)

---

### 1.4 GitHub Actions CI Pipeline

#### Workflow 1: Pre-commit CI (`precommit.yml`)
**Trigger:** Push or Pull Request to any branch
**Timeout:** 10 minutes

**Auto-Labeling:**
- ✅ Success: Adds `ci-passed`, `ready-for-review` labels
- ❌ Failure: Adds `ci-failed`, `security-review-needed` labels

**Steps:**

1. **Checkout Code**
   - Fetches full git history (`fetch-depth: 0`)

2. **Setup Python 3.11**
   - Installs Python environment

3. **Install Dependencies**
   - Upgrades pip
   - Installs: `pre-commit`, `pylint`, `black`, `bandit`, `pytest`
   - Installs project dependencies from `requirements.txt` and `requirements-dev.txt` (if exist)

4. **Cache Pre-commit Hooks**
   - Speeds up subsequent runs

5. **Run Pre-commit on All Files**
   - Re-validates all checks from local pre-commit
   - **Failure Action:** CI fails, blocks merge

6. **Run Bandit Security Scan**
   - Generates JSON report (`bandit-report.json`)
   - **Continue on error:** Yes (won't block CI)
   - Uploads security report as artifact

7. **Upload Security Report**
   - Always runs (even if Bandit fails)
   - Artifact: `bandit-security-report`

#### Workflow 2: Semgrep Security Scan (`semgrep.yml`)
**Trigger:** Push or PR to `main`, `dev`, or `uat` branches

**Auto-Labeling:**
- ❌ Failure: Adds `security-findings`, `semgrep-failed` labels
- Adds comment with security scan details

**Steps:**

1. **Checkout Code**

2. **Setup Python**

3. **Install Semgrep**

4. **Run Semgrep**
   - Config: `--config auto` (automatic rule detection)
   - Mode: `--error` (fails on findings)
   - **Failure Action:** CI fails, blocks merge

#### CI Outcomes:
- ✅ **PASS:** All workflows pass → Ready for code review
- ❌ **FAIL:** Any workflow fails → Fix issues locally → Push again

---

### 1.5 Dependabot Dependency Checks
**Trigger:** Weekly schedule or new dependency detected
**Configuration:** `.github/dependabot.yml`

**Auto-Labeling:**
- Adds `dependencies` label
- Adds ecosystem-specific labels (`python`, `github-actions`)

**Monitored Ecosystems:**
- Python packages (`pip`)
- GitHub Actions

**Behavior:**
- Opens PRs for dependency updates
- Limit: 1 open PR per ecosystem
- Automated security vulnerability patches

**Flow:**
- Dependabot creates PR → CI runs → Code review → Merge

---

### 1.6 Code Review
**Trigger:** Pull Request opened
**Configuration:** `.github/CODEOWNERS`

**Required Reviewers (based on files changed):**
- **Global:** `@your-team`
- **DevSecOps/CI:** `@devops-team`
- **Security configs:** `@security-team`
- **Python code:** `@python-team`
- **Tests:** `@qa-team` + `@python-team`

**Review Process:**
1. Reviewer examines code changes
2. CI status checks must pass
3. Reviewer approves or requests changes

**Outcomes:**
- ✅ **Approved:** Ready to merge
- 🔄 **Changes Requested:** Developer fixes → Push → CI re-runs → Re-review

---

### 1.7 Merge to Main Branch
**Actor:** Developer or Maintainer
**Action:** Merge approved PR

**Post-Merge:**
- CI runs on `main` branch
- Semgrep scans merged code
- Deployment pipeline triggered (if configured)

---

## 2. Edge Cases & Handling

### 2.1 Pre-commit Hook Failures

#### Edge Case: Black Formatter Conflicts
**Scenario:** Black reformats code differently than developer's style

**Handling:**
1. Let Black auto-format the code
2. Review changes: `git diff`
3. Re-stage files: `git add <files>`
4. Commit again

**Prevention:** Configure editor to use Black on save

---

#### Edge Case: Pylint False Positives
**Scenario:** Pylint flags valid code patterns

**Handling:**
1. Review Pylint output (non-blocking)
2. If false positive, add inline comment: `# pylint: disable=<rule-id>`
3. Or update `.pylintrc` to disable rule globally
4. Commit proceeds regardless

---

#### Edge Case: Bandit False Positives
**Scenario:** Bandit flags safe code as security risk

**Handling:**
1. Review Bandit output carefully
2. If false positive, add inline comment: `# nosec`
3. Document why it's safe in code comment
4. Re-commit

**Warning:** Use `# nosec` sparingly, only for verified false positives

---

#### Edge Case: Gitleaks False Positives
**Scenario:** Gitleaks detects fake/test secrets

**Handling:**
1. Review detected secret
2. If false positive, add to `.gitleaks.toml` allowlist:
   ```toml
   [allowlist]
   regexes = [
       '''your-false-positive-pattern'''
   ]
   ```
3. Re-commit

**Best Practice:** Use environment variables for all secrets

---

#### Edge Case: Test Failures
**Scenario:** Pytest fails on commit

**Handling:**
1. Review test output
2. Fix failing tests or code
3. Run tests locally: `pytest`
4. Re-commit when tests pass

**Emergency:** See Section 3.1 for bypass procedures

---

### 2.2 CI Pipeline Failures

#### Edge Case: Timeout (>10 minutes)
**Scenario:** Pre-commit CI exceeds 10-minute timeout

**Handling:**
1. Check for infinite loops or hanging tests
2. Optimize slow tests
3. Consider splitting test suite
4. Increase timeout in `.github/workflows/precommit.yml`:
   ```yaml
   timeout-minutes: 20
   ```

---

#### Edge Case: Dependency Installation Failures
**Scenario:** `pip install` fails in CI

**Handling:**
1. Check `requirements.txt` for invalid packages
2. Verify package versions exist on PyPI
3. Check for network issues (retry workflow)
4. Pin dependency versions to avoid conflicts

---

#### Edge Case: Semgrep False Positives
**Scenario:** Semgrep flags safe code patterns

**Handling:**
1. Review Semgrep findings
2. If false positive, create `.semgrepignore`:
   ```
   # Ignore specific files
   path/to/file.py

   # Ignore specific rules
   # ruleid: rule-name
   ```
3. Or add inline comment: `# nosemgrep: rule-id`
4. Push changes

---

#### Edge Case: Artifact Upload Failures
**Scenario:** Bandit report upload fails

**Handling:**
- Non-critical, CI continues
- Check GitHub Actions logs
- Manually run Bandit locally if needed: `bandit -r . -ll -f json -o report.json`

---

### 2.3 Code Review Edge Cases

#### Edge Case: No Available Reviewers
**Scenario:** Required code owners unavailable

**Handling:**
1. Contact team lead for alternate reviewer
2. Temporarily update `.github/CODEOWNERS`
3. Document exception in PR description

---

#### Edge Case: Conflicting Review Feedback
**Scenario:** Multiple reviewers disagree

**Handling:**
1. Schedule sync meeting with reviewers
2. Reach consensus on approach
3. Document decision in PR comments
4. Implement agreed changes

---

### 2.4 Dependabot Edge Cases

#### Edge Case: Breaking Dependency Update
**Scenario:** Dependabot PR breaks tests

**Handling:**
1. Review breaking changes in dependency changelog
2. Update code to accommodate changes
3. Or pin to previous version in `requirements.txt`
4. Close Dependabot PR with explanation

---

#### Edge Case: Security Vulnerability in Dependency
**Scenario:** Dependabot alerts on critical CVE

**Handling:**
1. **Priority:** Immediate action required
2. Review vulnerability details
3. Update dependency ASAP
4. If no patch available:
   - Find alternative package
   - Or implement workaround
   - Document risk acceptance if no option

---

## 3. Emergency Override Procedures

### 3.1 Bypassing Pre-commit Hooks (LOCAL)

#### ⚠️ CRITICAL: Use Only in Genuine Emergencies

**Valid Emergency Scenarios:**
- Production outage requiring immediate hotfix
- Security vulnerability patch needed urgently
- Pre-commit infrastructure failure (not code issue)

**Command:**
```bash
git commit --no-verify -m "Emergency fix: <description>"
```

**Mandatory Requirements:**
1. Document reason in commit message
2. Create follow-up ticket to fix properly
3. Notify team lead immediately
4. CI checks still run on push (cannot bypass)

**Example:**
```bash
git commit --no-verify -m "EMERGENCY: Fix critical auth bypass CVE-2024-XXXX

Bypassing pre-commit due to production security incident.
Follow-up ticket: JIRA-1234
Approved by: @security-lead"
```

---

### 3.2 Bypassing CI Checks (GITHUB)

#### ⚠️ EXTREME CAUTION: Requires Admin Privileges

**Valid Emergency Scenarios:**
- CI infrastructure outage (GitHub Actions down)
- False positive blocking critical hotfix
- Regulatory compliance deadline

**Procedure:**

1. **Obtain Approval:**
   - Security team lead approval required
   - Document in incident ticket
   - Record in audit log

2. **Temporary Branch Protection Override:**
   - Repository Settings → Branches → Edit protection rule
   - Temporarily disable "Require status checks to pass"
   - Merge PR
   - **IMMEDIATELY re-enable protection**

3. **Alternative: Admin Force Merge:**
   - Use admin privileges to merge despite failing checks
   - GitHub logs this action automatically

4. **Post-Merge Actions (MANDATORY):**
   - Create high-priority ticket to fix issues
   - Run all checks manually on merged code
   - Schedule post-incident review
   - Update runbook with lessons learned

---

### 3.3 Emergency Hotfix Workflow

**Scenario:** Critical production bug requiring immediate fix

**Fast-Track Procedure:**

1. **Create Hotfix Branch:**
   ```bash
   git checkout main
   git pull
   git checkout -b hotfix/critical-issue-description
   ```

2. **Implement Minimal Fix:**
   - Fix ONLY the critical issue
   - No refactoring or additional features

3. **Run Local Checks:**
   ```bash
   # Run tests
   pytest

   # Run security scan
   bandit -r . -ll

   # Check for secrets
   gitleaks detect --verbose
   ```

4. **Commit and Push:**
   ```bash
   git add <files>
   git commit -m "HOTFIX: <description>"
   git push origin hotfix/critical-issue-description
   ```

5. **Expedited Review:**
   - Tag reviewers in PR: "URGENT: Hotfix required"
   - Request immediate review
   - Parallel review (multiple reviewers simultaneously)

6. **Fast-Track Merge:**
   - If CI passes: Merge immediately
   - If CI fails on non-critical: Document and use override (Section 3.2)

7. **Post-Deployment:**
   - Monitor production
   - Create follow-up ticket for proper fix
   - Schedule retrospective

---

### 3.4 Disabling Specific Security Checks

#### Temporary Bandit Disable

**When:** Bandit blocking valid code pattern

**Local Pre-commit:**
Edit `.pre-commit-config.yaml`:
```yaml
- id: bandit
  args: ["-ll", "--skip", "B101,B601"]  # Skip specific tests
```

**CI Workflow:**
Edit `.github/workflows/precommit.yml`:
```yaml
- name: Run Bandit security scan
  run: bandit -r . -ll --skip B101,B601
```

**Approval Required:** Security team lead

---

#### Temporary Gitleaks Disable

**When:** Gitleaks infrastructure issue (not actual secrets)

**Local Pre-commit:**
```bash
SKIP=gitleaks git commit -m "message"
```

**CI:** Not recommended - fix allowlist instead

---

#### Temporary Semgrep Disable

**When:** Semgrep service outage

**Edit `.github/workflows/semgrep.yml`:**
```yaml
- name: Run Semgrep
  run: semgrep --config auto --error
  continue-on-error: true  # Add this line
```

**Approval Required:** DevOps team lead

---

### 3.5 Emergency Rollback Procedures

#### Scenario: Merged code causes production issues

**Immediate Actions:**

1. **Revert Commit:**
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

2. **Bypass CI if Needed:**
   - Revert commits typically pass CI
   - If CI fails, use override (Section 3.2)

3. **Deploy Rollback:**
   - Trigger deployment of reverted code
   - Monitor production recovery

4. **Post-Incident:**
   - Root cause analysis
   - Update tests to catch issue
   - Implement fix properly
   - Re-deploy with full CI validation

---

## 4. Audit & Compliance

### 4.1 Audit Trail

**Tracked Events:**
- All commits (git history)
- Pre-commit hook executions (local logs)
- CI pipeline runs (GitHub Actions logs)
- Security scan results (artifacts)
- Code review approvals (GitHub PR history)
- Emergency overrides (commit messages + GitHub audit log)

**Retention:**
- Git history: Permanent
- CI logs: 90 days (GitHub default)
- Security reports: Stored as artifacts (90 days)

---

### 4.2 Compliance Reporting

**Weekly:**
- Dependabot security alerts review
- Failed CI runs analysis
- Emergency override audit

**Monthly:**
- Security scan trends (Bandit, Semgrep, Gitleaks)
- Code review metrics
- Pre-commit bypass incidents

**Quarterly:**
- DevSecOps process review
- Tool effectiveness assessment
- Training needs identification

---

## 5. Troubleshooting Guide

### 5.1 "Pre-commit hook failed" - General

**Diagnosis:**
```bash
# Run pre-commit manually to see detailed output
pre-commit run --all-files --verbose
```

**Common Fixes:**
- Update pre-commit hooks: `pre-commit autoupdate`
- Clear cache: `pre-commit clean`
- Reinstall hooks: `pre-commit install --install-hooks`

---

### 5.2 "CI failing but local pre-commit passes"

**Causes:**
- Different Python versions
- Missing dependencies in CI
- Environment-specific issues

**Diagnosis:**
1. Check Python version in CI vs local
2. Review CI logs for missing packages
3. Check for environment variables

**Fix:**
- Match local Python version to CI (3.11)
- Ensure all dependencies in `requirements.txt`

---

### 5.3 "Gitleaks detecting false positives repeatedly"

**Solution:**
Create comprehensive allowlist in `.gitleaks.toml`:
```toml
[allowlist]
description = "Project-specific allowlist"
paths = [
    '''tests/fixtures/.*''',  # Test data
    '''docs/examples/.*'''     # Documentation examples
]
regexes = [
    '''(?i)test[-_]?key''',    # Test keys
    '''(?i)example[-_]?token''' # Example tokens
]
```

---

### 5.4 "Bandit blocking safe code"

**Solution:**
Add inline suppression with justification:
```python
# This is safe because we're using parameterized queries
cursor.execute(query, params)  # nosec B608
```

Or update `.pylintrc` to adjust severity:
```ini
[bandit]
exclude = /tests/
```

---

### 5.5 "Tests pass locally but fail in CI"

**Common Causes:**
- Timezone differences
- File path separators (Windows vs Linux)
- Missing test dependencies
- Race conditions in parallel tests

**Diagnosis:**
```bash
# Run tests with same settings as CI
pytest -v --tb=short
```

**Fix:**
- Use `pathlib` for cross-platform paths
- Mock time-dependent functions
- Add missing test dependencies to `requirements-dev.txt`

---

## 6. Best Practices

### 6.1 For Developers

✅ **DO:**
- Run tests locally before committing
- Keep commits small and focused
- Write descriptive commit messages
- Fix pre-commit issues immediately
- Review security scan results carefully
- Use environment variables for secrets
- Document emergency overrides thoroughly

❌ **DON'T:**
- Use `--no-verify` without valid emergency
- Commit commented-out secrets
- Ignore security warnings
- Push directly to `main` branch
- Disable checks without approval
- Use `# nosec` without justification

---

### 6.2 For Reviewers

✅ **DO:**
- Verify CI checks passed
- Review security scan artifacts
- Check for proper error handling
- Validate test coverage
- Ensure documentation updated
- Verify no hardcoded secrets
- Approve emergency overrides only when justified

❌ **DON'T:**
- Approve PRs with failing CI
- Skip security review
- Ignore Dependabot alerts
- Rubber-stamp reviews

---

### 6.3 For DevOps/Security Teams

✅ **DO:**
- Monitor emergency override usage
- Review security scan trends
- Keep security tools updated
- Audit allowlists regularly
- Document all exceptions
- Conduct regular training
- Test rollback procedures

❌ **DON'T:**
- Disable checks permanently
- Ignore repeated false positives
- Skip post-incident reviews
- Allow untracked overrides

---

## 7. Contacts & Escalation

### 7.1 Team Contacts

- **DevOps Team:** `@devops-team` - CI/CD issues
- **Security Team:** `@security-team` - Security scan issues, override approvals
- **Python Team:** `@python-team` - Code quality, linting issues
- **QA Team:** `@qa-team` - Test failures, coverage issues

### 7.2 Escalation Path

**Level 1:** Team lead (immediate team)
**Level 2:** Engineering manager
**Level 3:** Security officer (for security overrides)
**Level 4:** CTO (for compliance/regulatory issues)

### 7.3 Emergency Contacts

**Production Incidents:**
- On-call engineer: [Contact method]
- Incident commander: [Contact method]

**Security Incidents:**
- Security team lead: [Contact method]
- CISO: [Contact method]

---

## 8. Appendix

### 8.1 Available Labels

#### CI/CD Labels
- `ci-passed` - All CI checks passed
- `ci-failed` - CI checks failed
- `ci-cd` - CI/CD pipeline changes

#### Security Labels
- `security` - Security related changes
- `security-review-needed` - Requires security team review
- `security-findings` - Security scan found issues
- `semgrep-failed` - Semgrep scan failed

#### Priority Labels
- `priority: critical` - Critical priority
- `priority: high` - High priority (hotfixes)
- `priority: medium` - Medium priority
- `priority: low` - Low priority

#### Type Labels
- `hotfix` - Emergency hotfix
- `bug` - Bug fix
- `enhancement` - New feature or enhancement
- `dependencies` - Dependency updates

#### Component Labels
- `python` - Python code changes
- `tests` - Test related changes
- `documentation` - Documentation changes
- `configuration` - Configuration changes

#### Status Labels
- `ready-for-review` - Ready for code review
- `work-in-progress` - Work in progress
- `blocked` - Blocked by dependencies
- `needs-testing` - Needs testing

### 8.2 Tool Versions

- Python: 3.11
- Pre-commit: Latest
- Black: 23.7.0
- Pylint: Latest
- Bandit: Latest
- Pytest: Latest
- Gitleaks: v8.18.2
- Semgrep: Latest

### 8.2 Configuration Files Reference

- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `.pylintrc` - Pylint rules and settings
- `.gitleaks.toml` - Secret detection patterns
- `.github/workflows/precommit.yml` - CI pre-commit workflow
- `.github/workflows/semgrep.yml` - CI security scan workflow
- `.github/CODEOWNERS` - Code review assignments
- `.github/dependabot.yml` - Dependency update configuration

### 8.3 Useful Commands

```bash
# Run all pre-commit hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run <hook-id> --all-files

# Update pre-commit hooks
pre-commit autoupdate

# Run tests
pytest

# Run security scan
bandit -r . -ll

# Check for secrets
gitleaks detect --verbose

# Format code
black .

# Lint code
pylint **/*.py

# Emergency commit (use sparingly!)
git commit --no-verify -m "EMERGENCY: description"
```

---

## Document Control

**Version:** 1.0
**Last Updated:** 2024
**Owner:** DevOps Team
**Review Cycle:** Quarterly
**Next Review:** [Date]

---

**END OF DOCUMENT**
