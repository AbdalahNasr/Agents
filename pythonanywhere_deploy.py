#!/usr/bin/env python3
"""
PythonAnywhere FREE Deployment - 100% FREE
"""

import os

def create_pythonanywhere_config():
    """Create PythonAnywhere configuration"""
    print("🆓 Creating PythonAnywhere FREE deployment configuration...")
    
    # Create requirements.txt for PythonAnywhere
    requirements = """python-dotenv==1.0.0
requests==2.31.0
schedule==1.2.0
openai==1.3.0
beautifulsoup4==4.12.2
selenium==4.15.0
reportlab==4.0.4
python-docx==0.8.11
PyPDF2==3.0.1
google-auth==2.23.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
notion-client==2.2.1
"""
    
    with open('requirements_pythonanywhere.txt', 'w') as f:
        f.write(requirements)
    
    # Create startup script
    startup_script = """#!/usr/bin/env python3
import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.append(os.getcwd())

# Import and run automation
try:
    from continuous_job_automation_robust import main
    print("🚀 Starting job automation...")
    main()
except Exception as e:
    print(f"❌ Error starting automation: {e}")
    time.sleep(60)  # Wait before retrying
"""
    
    with open('start_automation.py', 'w') as f:
        f.write(startup_script)
    
    print("✅ Created PythonAnywhere configuration files")
    return True

def create_pythonanywhere_instructions():
    """Create deployment instructions"""
    instructions = """# 🆓 PythonAnywhere FREE Deployment Guide

## ✅ 100% FREE - No Credit Card Required!

### Step 1: Create PythonAnywhere Account
1. Visit: https://www.pythonanywhere.com
2. Click "Create a Beginner account" (free)
3. Sign up with email

### Step 2: Upload Your Code
1. Go to "Files" tab
2. Create folder: `job_automation`
3. Upload all your Python files
4. Upload `requirements_pythonanywhere.txt`

### Step 3: Install Dependencies
1. Go to "Consoles" tab
2. Start a "Bash" console
3. Run: `cd job_automation`
4. Run: `pip3.10 install --user -r requirements_pythonanywhere.txt`

### Step 4: Set Environment Variables
1. Go to "Files" tab
2. Create file: `job_automation/.env`
3. Add your environment variables:
   ```
   GMAIL_USER=your-email@gmail.com
   GMAIL_APP_PASSWORD=your-app-password
   NOTION_TOKEN=your-notion-token
   NOTION_DATABASE_ID=your-database-id
   CV_PRIMARY_URL=your-cv-link
   OPENAI_API_KEY=your-openai-key
   ```

### Step 5: Create Always-On Task
1. Go to "Tasks" tab
2. Click "Create a new task"
3. Command: `cd /home/yourusername/job_automation && python3.10 start_automation.py`
4. Click "Create task"
5. Your automation will run continuously!

## 🎉 That's it!
- ✅ **Completely FREE** forever
- ✅ **No credit card required**
- ✅ **Runs 24/7**
- ✅ **Always-on tasks**
- ✅ **Perfect for job automation**

## 📊 Monitor Your Automation
- View task logs in "Tasks" tab
- Check email notifications
- Monitor Notion database

## 🔧 Features
- Automatic job searching
- Humanized applications
- Email notifications
- Notion tracking
- Continuous operation

## ⚠️ Free Tier Limitations
- 1 always-on task
- 3 months CPU seconds per month
- Perfect for job automation!

Your job automation will start applying to jobs immediately!
"""
    
    with open('PYTHONANYWHERE_DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created PythonAnywhere deployment guide")
    return True

def main():
    """Main function"""
    print("🆓 PythonAnywhere FREE Deployment Setup")
    print("=" * 45)
    print("✅ 100% FREE - No credit card required")
    print("✅ Always-on tasks for free")
    print("✅ Perfect for job automation")
    print("✅ No payment ever required")
    print()
    
    if create_pythonanywhere_config() and create_pythonanywhere_instructions():
        print("\n🎉 SUCCESS!")
        print("PythonAnywhere configuration created!")
        print("\n📋 Next steps:")
        print("1. Go to https://www.pythonanywhere.com")
        print("2. Create free Beginner account")
        print("3. Upload your code")
        print("4. Install dependencies")
        print("5. Create always-on task")
        print("6. Your automation runs 24/7 for FREE!")
        print("\n📖 See PYTHONANYWHERE_DEPLOYMENT_GUIDE.md for details")
        return True
    else:
        print("\n❌ Setup failed")
        return False

if __name__ == "__main__":
    main()
