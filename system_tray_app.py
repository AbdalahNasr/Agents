#!/usr/bin/env python3
"""
🖥️ SYSTEM TRAY APP - Runs Your Automation Hub in Background
This app runs in the system tray and manages your automation system invisibly
"""
import os
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox
import pystray
from PIL import Image, ImageDraw
import subprocess
from datetime import datetime
import traceback

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from automation_hub import AutomationHub
    print("✅ Automation Hub imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")

class AutomationTrayApp:
    """System Tray Application for Personal Automation Hub"""
    
    def __init__(self):
        self.automation_hub = None
        self.is_running = False
        self.hub_thread = None
        
        # Create system tray icon
        self.icon = self.create_icon()
        
        # Setup menu
        self.menu = pystray.Menu(
            pystray.MenuItem("🚀 Status: Starting...", self.show_status, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("📊 Show Status", self.show_status),
            pystray.MenuItem("🔄 Restart Hub", self.restart_hub),
            pystray.MenuItem("⏸️ Pause Automation", self.pause_automation),
            pystray.MenuItem("▶️ Resume Automation", self.resume_automation),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("📧 Test Email", self.test_email),
            pystray.MenuItem("🔗 Test LinkedIn", self.test_linkedin),
            pystray.MenuItem("📄 Generate CV", self.generate_cv),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Exit", self.stop_app)
        )
        
        self.icon.menu = self.menu
        self.update_menu_status("Starting...")
    
    def create_icon(self):
        """Create system tray icon"""
        # Create a simple icon (you can replace this with your own .ico file)
        width = 64
        height = 64
        color = 'blue'
        
        image = Image.new('RGB', (width, height), color)
        dc = ImageDraw.Draw(image)
        dc.rectangle([width//4, height//4, 3*width//4, 3*height//4], fill='white')
        
        return pystray.Icon("automation_hub", image, "Personal Automation Hub", self.menu)
    
    def update_menu_status(self, status):
        """Update the status menu item"""
        self.menu[0].text = f"🚀 Status: {status}"
    
    def start_automation_hub(self):
        """Start the automation hub in background"""
        try:
            self.automation_hub = AutomationHub()
            self.is_running = True
            self.update_menu_status("Running")
            
            # Start hub in separate thread
            self.hub_thread = threading.Thread(target=self.run_hub_background, daemon=True)
            self.hub_thread.start()
            
            print("✅ Automation Hub started successfully in background")
            
        except Exception as e:
            error_msg = f"Failed to start automation hub: {e}"
            print(f"❌ {error_msg}")
            self.update_menu_status("Error")
            messagebox.showerror("Error", error_msg)
    
    def run_hub_background(self):
        """Run the automation hub in background mode"""
        try:
            # Run initial workflow
            self.update_menu_status("Running Initial Workflow...")
            initial_result = self.automation_hub.run_full_workflow()
            
            if initial_result["success"]:
                self.update_menu_status("Running (All Systems OK)")
            else:
                self.update_menu_status("Running (Some Issues)")
            
            # Start monitoring (this will run continuously)
            self.automation_hub.start_monitoring()
            
        except Exception as e:
            error_msg = f"Automation hub error: {e}"
            print(f"❌ {error_msg}")
            self.update_menu_status("Error")
            traceback.print_exc()
    
    def show_status(self, icon=None, item=None):
        """Show current automation status"""
        if not self.automation_hub:
            messagebox.showinfo("Status", "Automation Hub is not running")
            return
        
        try:
            status = self.automation_hub.get_status_report()
            
            status_text = f"""
🚀 Personal Automation Hub Status

📊 Overall Status: {'Running' if self.is_running else 'Stopped'}
🕐 Last Updated: {status['timestamp']}

🤖 Agent Status:
"""
            
            for agent, info in status['agent_status'].items():
                status_text += f"  • {agent.replace('_', ' ').title()}: {info['status']}\n"
                if info['last_run']:
                    status_text += f"    Last Run: {info['last_run']}\n"
                status_text += f"    Success: {info['success_count']}, Errors: {info['error_count']}\n\n"
            
            status_text += f"""
⏰ Next Scheduled Tasks:
"""
            for task in status['next_scheduled']:
                status_text += f"  • {task}\n"
            
            messagebox.showinfo("Automation Hub Status", status_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get status: {e}")
    
    def restart_hub(self, icon=None, item=None):
        """Restart the automation hub"""
        try:
            if self.automation_hub:
                self.is_running = False
                time.sleep(2)  # Give time to stop
            
            self.update_menu_status("Restarting...")
            self.start_automation_hub()
            messagebox.showinfo("Success", "Automation Hub restarted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart: {e}")
    
    def pause_automation(self, icon=None, item=None):
        """Pause automation temporarily"""
        if self.automation_hub:
            self.is_running = False
            self.update_menu_status("Paused")
            messagebox.showinfo("Paused", "Automation has been paused. Use 'Resume' to continue.")
    
    def resume_automation(self, icon=None, item=None):
        """Resume automation"""
        if not self.is_running:
            self.start_automation_hub()
            messagebox.showinfo("Resumed", "Automation has been resumed!")
    
    def test_email(self, icon=None, item=None):
        """Test email notifications"""
        try:
            if self.automation_hub:
                result = self.automation_hub.run_email_workflow()
                if result["success"]:
                    messagebox.showinfo("Success", "Email test completed successfully!")
                else:
                    messagebox.showerror("Error", f"Email test failed: {result.get('error')}")
            else:
                messagebox.showwarning("Warning", "Automation Hub is not running")
        except Exception as e:
            messagebox.showerror("Error", f"Email test failed: {e}")
    
    def test_linkedin(self, icon=None, item=None):
        """Test LinkedIn system"""
        try:
            if self.automation_hub:
                result = self.automation_hub.test_linkedin_system()
                if result["success"]:
                    profile = result.get("profile", {})
                    messagebox.showinfo("Success", 
                        f"LinkedIn test successful!\n\n"
                        f"Name: {profile.get('name', 'N/A')}\n"
                        f"Headline: {profile.get('headline', 'N/A')}\n"
                        f"Jobs Found: {result.get('jobs_found', 0)}")
                else:
                    messagebox.showerror("Error", f"LinkedIn test failed: {result.get('error')}")
            else:
                messagebox.showwarning("Warning", "Automation Hub is not running")
        except Exception as e:
            messagebox.showerror("Error", f"LinkedIn test failed: {e}")
    
    def generate_cv(self, icon=None, item=None):
        """Generate CV versions"""
        try:
            if self.automation_hub:
                result = self.automation_hub.run_cv_generation()
                if result["success"]:
                    messagebox.showinfo("Success", "CV generation completed successfully!")
                else:
                    messagebox.showerror("Error", f"CV generation failed: {result.get('error')}")
            else:
                messagebox.showwarning("Warning", "Automation Hub is not running")
        except Exception as e:
            messagebox.showerror("Error", f"CV generation failed: {e}")
    
    def stop_app(self, icon=None, item=None):
        """Stop the application"""
        try:
            if self.automation_hub:
                self.is_running = False
                time.sleep(2)  # Give time to stop
            
            self.icon.stop()
            print("👋 Automation Tray App stopped")
            
        except Exception as e:
            print(f"❌ Error stopping app: {e}")
    
    def run(self):
        """Run the system tray application"""
        try:
            print("🚀 Starting Personal Automation Hub in System Tray...")
            print("📱 Look for the blue icon in your system tray (bottom right)")
            print("🖱️ Right-click the icon to access menu options")
            
            # Start automation hub
            self.start_automation_hub()
            
            # Run system tray
            self.icon.run()
            
        except Exception as e:
            print(f"❌ Error running tray app: {e}")
            traceback.print_exc()

def main():
    """Main function"""
    try:
        app = AutomationTrayApp()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
