#!/usr/bin/env python3
"""
Render Free Deployment Script - Completely FREE
"""

import os
import json

def create_render_config():
    """Create Render configuration files"""
    print("📝 Creating Render configuration...")
    
    # Create render.yaml
    render_config = {
        "services": [
            {
                "type": "worker",
                "name": "job-automation",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "python continuous_job_automation_robust.py",
                "envVars": [
                    {
                        "key": "GMAIL_USER",
                        "value": os.getenv('GMAIL_USER', '')
                    },
                    {
                        "key": "GMAIL_APP_PASSWORD", 
                        "value": os.getenv('GMAIL_APP_PASSWORD', '')
                    },
                    {
                        "key": "NOTION_TOKEN",
                        "value": os.getenv('NOTION_TOKEN', '')
                    },
                    {
                        "key": "NOTION_DATABASE_ID",
                        "value": os.getenv('NOTION_DATABASE_ID', '')
                    },
                    {
                        "key": "CV_PRIMARY_URL",
                        "value": os.getenv('CV_PRIMARY_URL', '')
                    },
                    {
                        "key": "OPENAI_API_KEY",
                        "value": os.getenv('OPENAI_API_KEY', '')
                    }
                ]
            }
        ]
    }
    
    with open('render.yaml', 'w') as f:
        json.dump(render_config, f, indent=2)
    
    print("✅ Created render.yaml")
    
    # Create deployment instructions
    instructions = """
# 🆓 Render Free Deployment Instructions

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Render deployment config"
git push origin main
```

## Step 2: Connect to Render
1. Go to https://render.com
2. Sign up with GitHub (FREE)
3. Click "New +" → "Background Worker"
4. Connect your GitHub repository
5. Select your repository

## Step 3: Configure
- **Name**: job-automation
- **Environment**: Python 3
- **Build Command**: pip install -r requirements.txt
- **Start Command**: python continuous_job_automation_robust.py

## Step 4: Environment Variables
Add these in Render dashboard:
- GMAIL_USER: your-email@gmail.com
- GMAIL_APP_PASSWORD: your-app-password
- NOTION_TOKEN: your-notion-token
- NOTION_DATABASE_ID: your-database-id
- CV_PRIMARY_URL: your-cv-link
- OPENAI_API_KEY: your-openai-key

## Step 5: Deploy
Click "Create Background Worker" - that's it!

## ✅ Benefits:
- 🆓 Completely FREE
- 🚫 No credit card required
- 📊 750 hours/month free
- 🔄 Auto-deploy on GitHub push
- 📧 Email notifications
- 🔧 Easy environment management

## 📊 Monitoring:
- View logs in Render dashboard
- Check status anytime
- Automatic restarts on failure
"""
    
    with open('RENDER_DEPLOYMENT_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created RENDER_DEPLOYMENT_INSTRUCTIONS.md")
    return True

def main():
    """Main function"""
    print("🆓 Render Free Deployment Setup")
    print("=" * 40)
    print("✅ Completely FREE - No credit card required")
    print("✅ 750 hours/month free")
    print("✅ GitHub integration")
    print("✅ Auto-deploy on push")
    print()
    
    if create_render_config():
        print("\n🎉 SUCCESS!")
        print("Render configuration created!")
        print("\n📋 Next steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Go to https://render.com")
        print("3. Connect GitHub repository")
        print("4. Deploy as Background Worker")
        print("5. Add environment variables")
        print("\n📖 See RENDER_DEPLOYMENT_INSTRUCTIONS.md for details")
        return True
    else:
        print("\n❌ Setup failed")
        return False

if __name__ == "__main__":
    main()
