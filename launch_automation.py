#!/usr/bin/env python3
"""
🚀 LAUNCHER SCRIPT - Starts your Personal Automation Hub
This script handles any import issues and starts the automation system
"""
import sys
import os

def main():
    print("🚀 Personal Automation Hub Launcher")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required. Current version:", sys.version)
        input("Press Enter to exit...")
        return
    
    print(f"✅ Python version: {sys.version}")
    
    # Check if we're in the right directory
    if not os.path.exists("config.env"):
        print("❌ config.env not found. Please run this from your project directory.")
        input("Press Enter to exit...")
        return
    
    print("✅ config.env found")
    
    # Try to import dependencies
    print("\n🔍 Checking dependencies...")
    
    try:
        import dotenv
        print("✅ python-dotenv")
    except ImportError:
        print("❌ python-dotenv - Install with: pip install python-dotenv")
    
    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests - Install with: pip install requests")
    
    try:
        import openai
        print("✅ openai")
    except ImportError:
        print("❌ openai - Install with: pip install openai")
    
    try:
        import schedule
        print("✅ schedule")
    except ImportError:
        print("❌ schedule - Install with: pip install schedule")
    
    try:
        import colorlog
        print("✅ colorlog")
    except ImportError:
        print("❌ colorlog - Install with: pip install colorlog")
    
    # Try to start the automation hub
    print("\n🚀 Starting Automation Hub...")
    
    try:
        # Import and run the automation hub
        from automation_hub import AutomationHub
        
        print("✅ Automation Hub imported successfully!")
        print("\n🎯 Starting your personal productivity system...")
        
        # Create and run the hub
        hub = AutomationHub()
        
        # Run initial test
        print("\n🔄 Running initial system test...")
        test_result = hub.test_linkedin_system()
        
        if test_result.get("success"):
            print("✅ LinkedIn system test passed!")
            if "profile" in test_result:
                profile = test_result["profile"]
                print(f"   Name: {profile.get('name', 'N/A')}")
                print(f"   Headline: {profile.get('headline', 'N/A')}")
            print(f"   Jobs found: {test_result.get('jobs_found', 0)}")
        else:
            print(f"⚠️ LinkedIn test had issues: {test_result.get('error', 'Unknown error')}")
        
        # Ask user if they want to continue
        print("\n🤔 What would you like to do?")
        print("1. 🚀 Start full automation (runs continuously)")
        print("2. 🔄 Run one complete workflow")
        print("3. 🔗 Test LinkedIn only")
        print("4. 📄 Generate CV only")
        print("5. 💼 Job application workflow only")
        print("6. 📧 Test email notifications only")
        print("7. ❌ Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting full automation system...")
            print("This will run continuously. Press Ctrl+C to stop.")
            hub.start_monitoring()
            
        elif choice == "2":
            print("\n🔄 Running complete workflow...")
            result = hub.run_full_workflow()
            if result["success"]:
                print("✅ Complete workflow finished successfully!")
            else:
                print("⚠️ Workflow completed with some issues")
            
        elif choice == "3":
            print("\n🔗 Testing LinkedIn system...")
            result = hub.test_linkedin_system()
            if result["success"]:
                print("✅ LinkedIn test successful!")
            else:
                print(f"❌ LinkedIn test failed: {result.get('error')}")
                
        elif choice == "4":
            print("\n📄 Generating CV...")
            result = hub.run_cv_generation()
            if result["success"]:
                print("✅ CV generation successful!")
            else:
                print(f"❌ CV generation failed: {result.get('error')}")
                
        elif choice == "5":
            print("\n💼 Running job application workflow...")
            result = hub.run_job_application_workflow()
            if result["success"]:
                print("✅ Job application workflow successful!")
            else:
                print(f"❌ Job application workflow failed: {result.get('error')}")
                
        elif choice == "6":
            print("\n📧 Testing email notifications...")
            result = hub.run_email_workflow()
            if result["success"]:
                print("✅ Email test successful!")
            else:
                print(f"❌ Email test failed: {result.get('error')}")
                
        elif choice == "7":
            print("👋 Goodbye!")
            return
            
        else:
            print("❌ Invalid choice. Exiting.")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Try installing missing dependencies:")
        print("   pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error starting automation hub: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n👋 Automation Hub launcher finished.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
