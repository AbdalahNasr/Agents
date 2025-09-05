#!/usr/bin/env python3
"""
Replit Free Deployment - 100% FREE
"""

import os
import subprocess
import sys

def create_replit_config():
    """Create Replit configuration files"""
    print("🆓 Creating Replit FREE deployment configuration...")
    
    # Create .replit file
    replit_config = """[run]
command = "python continuous_job_automation_robust.py"

[env]
PYTHONPATH = "${PYTHONPATH}:."
PYTHONUNBUFFERED = "1"

[gitHubImport]
requiredFiles = [".replit", "replit.nix", ".replitignore"]

[deployment]
run = ["sh", "-c", "python continuous_job_automation_robust.py"]
"""
    
    with open('.replit', 'w') as f:
        f.write(replit_config)
    
    # Create replit.nix
    replit_nix = """{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
  ];
}"""
    
    with open('replit.nix', 'w') as f:
        f.write(replit_nix)
    
    # Create .replitignore
    replit_ignore = """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
.DS_Store
*.pdf
*.docx
*.txt
config.env
drive_credentials.json
drive_token.pickle
CV_*/
job_application_history.json
cv_management.json
automation_log.json
daily_reports/
real_application_history.json
"""
    
    with open('.replitignore', 'w') as f:
        f.write(replit_ignore)
    
    print("✅ Created Replit configuration files")
    return True

def create_replit_instructions():
    """Create deployment instructions"""
    instructions = """# 🆓 Replit FREE Deployment Guide

## ✅ 100% FREE - No Credit Card Required!

### Step 1: Go to Replit
1. Visit: https://replit.com
2. Click "Sign up" (free)
3. Sign up with GitHub

### Step 2: Import Your Repository
1. Click "Create Repl"
2. Select "Import from GitHub"
3. Enter: `AbdalahNasr/Agents`
4. Click "Import"

### Step 3: Set Environment Variables
1. Click the "Secrets" tab (lock icon)
2. Add these secrets:
   - `GMAIL_USER` = your-email@gmail.com
   - `GMAIL_APP_PASSWORD` = your-app-password
   - `NOTION_TOKEN` = your-notion-token
   - `NOTION_DATABASE_ID` = your-database-id
   - `CV_PRIMARY_URL` = your-cv-link
   - `OPENAI_API_KEY` = your-openai-key

### Step 4: Run Your Automation
1. Click "Run" button
2. Your automation will start immediately!
3. It will run continuously for FREE

## 🎉 That's it!
- ✅ **Completely FREE** forever
- ✅ **No credit card required**
- ✅ **Runs 24/7**
- ✅ **Auto-restarts**
- ✅ **Perfect for job automation**

## 📊 Monitor Your Automation
- View console output in Replit
- Check email notifications
- Monitor Notion database

## 🔧 Features
- Automatic job searching
- Humanized applications
- Email notifications
- Notion tracking
- Continuous operation

Your job automation will start applying to jobs immediately!
"""
    
    with open('REPLIT_DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created Replit deployment guide")
    return True

def main():
    """Main function"""
    print("🆓 Replit FREE Deployment Setup")
    print("=" * 40)
    print("✅ 100% FREE - No credit card required")
    print("✅ Always-on for free users")
    print("✅ Perfect for job automation")
    print("✅ No payment ever required")
    print()
    
    if create_replit_config() and create_replit_instructions():
        print("\n🎉 SUCCESS!")
        print("Replit configuration created!")
        print("\n📋 Next steps:")
        print("1. Go to https://replit.com")
        print("2. Sign up with GitHub (free)")
        print("3. Import repository: AbdalahNasr/Agents")
        print("4. Add environment variables in Secrets")
        print("5. Click Run - your automation starts immediately!")
        print("\n📖 See REPLIT_DEPLOYMENT_GUIDE.md for details")
        return True
    else:
        print("\n❌ Setup failed")
        return False

if __name__ == "__main__":
    main()
