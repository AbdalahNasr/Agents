#!/usr/bin/env python3
"""
Railway Deployment Script - Completely FREE
"""

import os
import subprocess
import sys

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI is installed")
            return True
        else:
            print("❌ Railway CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI not found")
        return False

def install_railway_cli():
    """Install Railway CLI"""
    print("📦 Installing Railway CLI...")
    try:
        # Install via npm
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        print("✅ Railway CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Railway CLI")
        print("💡 Please install Node.js first: https://nodejs.org/")
        return False

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    
    try:
        # Login to Railway
        print("🔐 Logging in to Railway...")
        subprocess.run(['railway', 'login'], check=True)
        
        # Initialize project
        print("📁 Initializing Railway project...")
        subprocess.run(['railway', 'init'], check=True)
        
        # Set environment variables
        print("🔧 Setting environment variables...")
        env_vars = [
            'GMAIL_USER',
            'GMAIL_APP_PASSWORD', 
            'NOTION_TOKEN',
            'NOTION_DATABASE_ID',
            'CV_PRIMARY_URL',
            'OPENAI_API_KEY'
        ]
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                subprocess.run(['railway', 'variables', 'set', f'{var}={value}'], check=True)
                print(f"  ✅ Set {var}")
            else:
                print(f"  ⚠️ {var} not found in environment")
        
        # Deploy
        print("🚀 Deploying application...")
        subprocess.run(['railway', 'up'], check=True)
        
        print("✅ Deployment successful!")
        print("🌐 Your job automation is now running on Railway!")
        print("📊 Check status: railway status")
        print("📋 View logs: railway logs")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🆓 Railway Free Deployment")
    print("=" * 40)
    print("✅ Completely FREE - No credit card required")
    print("✅ 500 hours/month free")
    print("✅ Perfect for job automation")
    print()
    
    # Check if Railway CLI is installed
    if not check_railway_cli():
        if not install_railway_cli():
            return False
    
    # Deploy to Railway
    if deploy_to_railway():
        print("\n🎉 SUCCESS!")
        print("Your job automation is now running on Railway for FREE!")
        print("\n📋 Next steps:")
        print("1. Check your Railway dashboard")
        print("2. Monitor logs: railway logs")
        print("3. Update environment variables as needed")
        return True
    else:
        print("\n❌ Deployment failed")
        return False

if __name__ == "__main__":
    main()
