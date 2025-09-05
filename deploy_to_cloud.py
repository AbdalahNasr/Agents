#!/usr/bin/env python3
"""
Cloud Deployment Helper Script
Helps prepare your automation for cloud deployment
"""

import os
import json
from datetime import datetime

def create_deployment_package():
    """Create a deployment package for cloud platforms"""
    print("🚀 Creating Cloud Deployment Package")
    print("=" * 50)
    
    # Check if cloud_automation.py exists
    if not os.path.exists('cloud_automation.py'):
        print("❌ cloud_automation.py not found!")
        print("   Make sure you have the cloud automation script")
        return False
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        print("   Creating basic requirements.txt...")
        create_basic_requirements()
    
    # Check environment variables
    required_vars = [
        'OPENAI_API_KEY',
        'GMAIL_USER', 
        'GMAIL_APP_PASSWORD',
        'NOTION_TOKEN',
        'NOTION_DATABASE_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n   You'll need to set these in your cloud platform")
    else:
        print("✅ All required environment variables found")
    
    # Create deployment info
    deployment_info = {
        "deployment_date": datetime.now().isoformat(),
        "platforms_supported": [
            "Railway",
            "Render", 
            "Google Colab",
            "Replit",
            "Heroku (via Fly.io)"
        ],
        "main_script": "cloud_automation.py",
        "requirements": "requirements.txt",
        "config_files": [
            "railway.json",
            "Procfile"
        ]
    }
    
    with open('deployment_info.json', 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print("\n✅ Deployment package ready!")
    print("📁 Files created:")
    print("   - deployment_info.json")
    print("   - railway.json")
    print("   - Procfile")
    
    return True

def create_basic_requirements():
    """Create a basic requirements.txt if it doesn't exist"""
    requirements = [
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "schedule==1.2.0",
        "openai==1.3.0",
        "beautifulsoup4==4.12.2",
        "selenium==4.15.0",
        "reportlab==4.0.4",
        "python-docx==0.8.11",
        "PyPDF2==3.0.1",
        "google-auth==2.23.0",
        "google-auth-oauthlib==1.1.0",
        "google-auth-httplib2==0.1.1",
        "google-api-python-client==2.108.0"
    ]
    
    with open('requirements.txt', 'w') as f:
        for req in requirements:
            f.write(req + '\n')
    
    print("✅ Created requirements.txt")

def show_deployment_options():
    """Show available deployment options"""
    print("\n🌐 Available Free Cloud Platforms:")
    print("=" * 50)
    
    platforms = [
        {
            "name": "Railway",
            "free_tier": "$5 credit/month",
            "best_for": "24/7 automation",
            "difficulty": "Easy",
            "url": "railway.app"
        },
        {
            "name": "Render", 
            "free_tier": "750 hours/month",
            "best_for": "Background jobs",
            "difficulty": "Easy",
            "url": "render.com"
        },
        {
            "name": "Google Colab",
            "free_tier": "Unlimited",
            "best_for": "Testing & short runs",
            "difficulty": "Very Easy",
            "url": "colab.research.google.com"
        },
        {
            "name": "Replit",
            "free_tier": "Always-on available",
            "best_for": "Quick deployment",
            "difficulty": "Very Easy", 
            "url": "replit.com"
        }
    ]
    
    for i, platform in enumerate(platforms, 1):
        print(f"{i}. {platform['name']}")
        print(f"   Free Tier: {platform['free_tier']}")
        print(f"   Best For: {platform['best_for']}")
        print(f"   Difficulty: {platform['difficulty']}")
        print(f"   URL: {platform['url']}")
        print()

def main():
    """Main deployment helper"""
    print("🚀 Job Application Automation - Cloud Deployment Helper")
    print("=" * 60)
    
    # Create deployment package
    if create_deployment_package():
        show_deployment_options()
        
        print("\n📋 Next Steps:")
        print("1. Choose a platform (Railway recommended)")
        print("2. Create account and connect GitHub")
        print("3. Set environment variables")
        print("4. Deploy and monitor")
        
        print("\n💡 Pro Tip: Start with Railway for the most reliable 24/7 operation!")
        
    else:
        print("❌ Deployment package creation failed")
        return False
    
    return True

if __name__ == "__main__":
    main()

