#!/bin/bash
# Script to create GitHub labels locally using GitHub CLI (gh)
# Usage: ./scripts/create-labels.sh

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed. Please install it first:"
    echo "https://cli.github.com/"
    exit 1
fi

echo "Creating GitHub labels..."

# CI/CD Labels
gh label create "ci-passed" --color "0e8a16" --description "All CI checks passed" --force
gh label create "ci-failed" --color "d73a4a" --description "CI checks failed" --force

# Security Labels
gh label create "security" --color "b60205" --description "Security related changes" --force
gh label create "security-review-needed" --color "d93f0b" --description "Requires security team review" --force
gh label create "security-findings" --color "e99695" --description "Security scan found issues" --force
gh label create "semgrep-failed" --color "f9d0c4" --description "Semgrep scan failed" --force

# Priority Labels
gh label create "priority: critical" --color "b60205" --description "Critical priority" --force
gh label create "priority: high" --color "d93f0b" --description "High priority" --force
gh label create "priority: medium" --color "fbca04" --description "Medium priority" --force
gh label create "priority: low" --color "0e8a16" --description "Low priority" --force

# Type Labels
gh label create "hotfix" --color "d73a4a" --description "Emergency hotfix" --force
gh label create "bug" --color "d73a4a" --description "Bug fix" --force
gh label create "enhancement" --color "a2eeef" --description "New feature or enhancement" --force
gh label create "dependencies" --color "0366d6" --description "Dependency updates" --force

# Component Labels
gh label create "python" --color "3572A5" --description "Python code changes" --force
gh label create "tests" --color "c5def5" --description "Test related changes" --force
gh label create "ci-cd" --color "1d76db" --description "CI/CD pipeline changes" --force
gh label create "documentation" --color "0075ca" --description "Documentation changes" --force
gh label create "configuration" --color "fef2c0" --description "Configuration changes" --force

# Status Labels
gh label create "ready-for-review" --color "0e8a16" --description "Ready for code review" --force
gh label create "work-in-progress" --color "fbca04" --description "Work in progress" --force
gh label create "blocked" --color "d73a4a" --description "Blocked by dependencies" --force
gh label create "needs-testing" --color "f9d0c4" --description "Needs testing" --force

echo "✅ All labels created successfully!"
