#!/usr/bin/env python3
"""
Environment Setup Helper
Interactive setup for all required environment variables
"""

import os
import sys
from dotenv import load_dotenv

def setup_environment():
    """Interactive environment setup"""
    print("🔧 ENVIRONMENT SETUP HELPER")
    print("=" * 35)
    print()
    
    # Load existing config
    load_dotenv('config.env')
    
    print("📋 Current Configuration Status:")
    print(f"   Gmail User: {'✅' if os.getenv('GMAIL_USER') else '❌'}")
    print(f"   Gmail Password: {'✅' if os.getenv('GMAIL_APP_PASSWORD') else '❌'}")
    print(f"   LinkedIn Username: {'✅' if os.getenv('LINKEDIN_USERNAME') else '❌'}")
    print(f"   LinkedIn Password: {'✅' if os.getenv('LINKEDIN_PASSWORD') else '❌'}")
    print(f"   Notion Token: {'✅' if os.getenv('NOTION_TOKEN') else '❌'}")
    print(f"   Notion Database ID: {'✅' if os.getenv('NOTION_DATABASE_ID') else '❌'}")
    print(f"   OpenAI API Key: {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
    print(f"   Drive Credentials: {'✅' if os.path.exists('drive_credentials.json') else '❌'}")
    print()
    
    # Setup instructions
    print("📖 SETUP INSTRUCTIONS:")
    print()
    
    print("1. 📧 GMAIL APP PASSWORD:")
    print("   • Go to: https://myaccount.google.com/")
    print("   • Security → 2-Step Verification (enable if needed)")
    print("   • App passwords → Mail → Other")
    print("   • Enter name: 'Job Application System'")
    print("   • Copy the 16-character password")
    print()
    
    print("2. 🔗 LINKEDIN CREDENTIALS:")
    print("   • Use your regular LinkedIn username/email")
    print("   • Use your regular LinkedIn password")
    print("   • For automation, consider LinkedIn API instead")
    print()
    
    print("3. 📁 GOOGLE DRIVE API:")
    print("   • Go to: https://console.cloud.google.com/")
    print("   • Create new project or select existing")
    print("   • Enable Google Drive API")
    print("   • Credentials → Create Credentials → OAuth 2.0 Client ID")
    print("   • Download JSON as 'drive_credentials.json'")
    print("   • Place in project root directory")
    print()
    
    print("4. 🗄️ NOTION INTEGRATION:")
    print("   • Go to: https://developers.notion.com/")
    print("   • Create new integration")
    print("   • Copy Internal Integration Token")
    print("   • Share your database with the integration")
    print()
    
    print("5. 🤖 OPENAI API:")
    print("   • Go to: https://platform.openai.com/")
    print("   • API Keys → Create new secret key")
    print("   • Copy the key")
    print()
    
    # Interactive setup
    print("🔧 INTERACTIVE SETUP:")
    print("Enter your credentials (press Enter to skip):")
    print()
    
    config_updates = {}
    
    # Gmail setup
    gmail_user = input("Gmail User (your-email@gmail.com): ").strip()
    if gmail_user:
        config_updates['GMAIL_USER'] = gmail_user
    
    gmail_password = input("Gmail App Password (16 characters): ").strip()
    if gmail_password:
        config_updates['GMAIL_APP_PASSWORD'] = gmail_password
    
    # LinkedIn setup
    linkedin_username = input("LinkedIn Username/Email: ").strip()
    if linkedin_username:
        config_updates['LINKEDIN_USERNAME'] = linkedin_username
    
    linkedin_password = input("LinkedIn Password: ").strip()
    if linkedin_password:
        config_updates['LINKEDIN_PASSWORD'] = linkedin_password
    
    # Update config.env
    if config_updates:
        print("\n📝 Updating config.env...")
        
        # Read current config
        with open('config.env', 'r') as f:
            lines = f.readlines()
        
        # Update lines
        for key, value in config_updates.items():
            updated = False
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    updated = True
                    break
            
            if not updated:
                lines.append(f"{key}={value}\n")
        
        # Write updated config
        with open('config.env', 'w') as f:
            f.writelines(lines)
        
        print("✅ Configuration updated!")
    else:
        print("ℹ️ No changes made")
    
    print()
    print("🎯 NEXT STEPS:")
    print("1. Set up Google Drive API credentials")
    print("2. Test email sending: python test_email_application.py")
    print("3. Test LinkedIn integration: python test_complete_application_system.py")
    print("4. Test Notion integration: python test_notion_working.py")

if __name__ == "__main__":
    setup_environment()
