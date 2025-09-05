#!/usr/bin/env python3
"""
System Status Checker - Quick overview of all automation systems
"""

import os
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv

def check_python_processes():
    """Check if automation is running"""
    try:
        result = subprocess.run(['tasklist', '/fi', 'imagename eq python.exe'], 
                              capture_output=True, text=True)
        python_processes = result.stdout.count('python.exe')
        return python_processes > 0, python_processes
    except:
        return False, 0

def check_application_history():
    """Check application history file"""
    try:
        if os.path.exists('real_application_history.json'):
            with open('real_application_history.json', 'r') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    return True, len(data)
                else:
                    return True, 0
        return False, 0
    except:
        return False, 0

def check_automation_log():
    """Check automation log file"""
    try:
        if os.path.exists('production_automation_log.json'):
            with open('production_automation_log.json', 'r') as f:
                data = json.load(f)
                return True, data
        return False, None
    except:
        return False, None

def check_config():
    """Check configuration files"""
    config_files = ['config.env', 'production_config.env']
    status = {}
    
    for file in config_files:
        if os.path.exists(file):
            status[file] = "✅ Found"
        else:
            status[file] = "❌ Missing"
    
    return status

def check_notion_connection():
    """Test Notion connection"""
    try:
        load_dotenv('config.env')
        notion_token = os.getenv('NOTION_TOKEN')
        notion_database_id = os.getenv('NOTION_DATABASE_ID')
        
        if notion_token and notion_database_id:
            return True, "✅ Configured"
        else:
            return False, "❌ Missing credentials"
    except:
        return False, "❌ Error loading config"

def check_email_config():
    """Test email configuration"""
    try:
        load_dotenv('config.env')
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if gmail_user and gmail_password:
            return True, "✅ Configured"
        else:
            return False, "❌ Missing credentials"
    except:
        return False, "❌ Error loading config"

def main():
    """Main status check function"""
    print("🔍 Job Automation System Status Check")
    print("=" * 50)
    print(f"📅 Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check Python processes
    print("🔄 Process Status:")
    is_running, process_count = check_python_processes()
    if is_running:
        print(f"  ✅ Automation is running ({process_count} Python processes)")
    else:
        print("  ❌ No automation processes found")
    print()
    
    # Check application history
    print("📊 Application History:")
    has_history, app_count = check_application_history()
    if has_history:
        print(f"  ✅ History file exists ({app_count} applications)")
    else:
        print("  ❌ No application history found")
    print()
    
    # Check automation log
    print("📝 Automation Log:")
    has_log, log_data = check_automation_log()
    if has_log and log_data:
        print(f"  ✅ Log file exists")
        print(f"  📈 Total cycles: {log_data.get('total_cycles', 0)}")
        print(f"  📈 Total applications: {log_data.get('total_applications', 0)}")
        print(f"  📈 Total jobs found: {log_data.get('total_jobs_found', 0)}")
        if log_data.get('last_cycle'):
            print(f"  🕐 Last cycle: {log_data['last_cycle']}")
    else:
        print("  ❌ No automation log found")
    print()
    
    # Check configuration
    print("⚙️ Configuration Files:")
    config_status = check_config()
    for file, status in config_status.items():
        print(f"  {status} {file}")
    print()
    
    # Check Notion connection
    print("🗄️ Notion Integration:")
    notion_ok, notion_status = check_notion_connection()
    print(f"  {notion_status}")
    print()
    
    # Check email configuration
    print("📧 Email Configuration:")
    email_ok, email_status = check_email_config()
    print(f"  {email_status}")
    print()
    
    # Overall status
    print("🎯 Overall Status:")
    if is_running and has_history and notion_ok and email_ok:
        print("  ✅ System is fully operational")
        print("  🚀 Automation is running successfully")
    elif is_running:
        print("  ⚠️ System is running with some issues")
        print("  🔧 Check configuration and connections")
    else:
        print("  ❌ System is not running")
        print("  🚀 Start automation with: python continuous_job_automation_robust.py")
    
    print()
    print("📋 Quick Commands:")
    print("  Start automation: python continuous_job_automation_robust.py")
    print("  Test system: python agents/real_job_application_system.py")
    print("  Check Notion: python test_notion_working.py")
    print("  Stop automation: Press Ctrl+C in running terminal")

if __name__ == "__main__":
    main()
