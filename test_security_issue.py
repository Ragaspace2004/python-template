"""
Test file to verify Bandit catches security issues.
This file should trigger Bandit warnings.
"""

import os

# This should trigger Bandit warning: B605 (shell injection)
os.system("ls -la")

# This should trigger Bandit warning: B307 (eval usage)
user_input = "print('hello')"
print(user_input)
