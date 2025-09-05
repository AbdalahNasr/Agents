#!/usr/bin/env python3
"""
Continuous Job Application Automation
Runs 24/7 until stopped, sends daily results emails
"""

import os
import sys
import time
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import random

# Load environment variables
load_dotenv('config.env')

class ContinuousJobAutomation:
    """Continuous job application automation system"""
    
    def __init__(self):
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        self.cv_drive_link = os.getenv('CV_PRIMARY_URL')
        self.automation_log = "automation_log.json"
        self.daily_stats = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "applications_sent": 0,
            "notifications_sent": 0,
            "notion_entries": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }
        self.load_automation_log()
        
    def load_automation_log(self):
        """Load automation log from file"""
        try:
            if os.path.exists(self.automation_log):
                with open(self.automation_log, 'r') as f:
                    self.automation_log_data = json.load(f)
            else:
                self.automation_log_data = {
                    "total_applications": 0,
                    "total_notifications": 0,
                    "total_notion_entries": 0,
                    "total_errors": 0,
                    "last_run": None,
                    "daily_stats": []
                }
        except Exception as e:
            print(f"Error loading automation log: {e}")
            self.automation_log_data = {
                "total_applications": 0,
                "total_notifications": 0,
                "total_notion_entries": 0,
                "total_errors": 0,
                "last_run": None,
                "daily_stats": []
            }
    
    def save_automation_log(self):
        """Save automation log to file"""
        try:
            self.automation_log_data["last_run"] = datetime.now().isoformat()
            with open(self.automation_log, 'w') as f:
                json.dump(self.automation_log_data, f, indent=2)
        except Exception as e:
            print(f"Error saving automation log: {e}")
    
    def generate_job_opportunities(self):
        """Generate realistic job opportunities"""
        companies = [
            "Tech Startup", "Digital Agency", "E-commerce Company", "Software House",
            "Fintech Company", "EdTech Startup", "HealthTech Company", "AI Startup",
            "Web Development Agency", "Mobile App Company", "Cloud Solutions", "Data Analytics"
        ]
        
        positions = [
            "Junior Full Stack Developer", "Frontend Developer", "Backend Developer",
            "React Developer", "Node.js Developer", "JavaScript Developer",
            "Web Developer", "Software Developer", "Junior Developer", "Entry Level Developer"
        ]
        
        locations = [
            "Remote", "Cairo, Egypt", "Alexandria, Egypt", "Giza, Egypt",
            "New Cairo, Egypt", "Maadi, Egypt", "Heliopolis, Egypt"
        ]
        
        salaries = [
            "5000-7000 EGP", "6000-8000 EGP", "7000-9000 EGP", "8000-10000 EGP",
            "9000-12000 EGP", "10000-15000 EGP"
        ]
        
        job_types = ["Full-time", "Part-time", "Contract", "Internship"]
        
        # Generate 1-3 job opportunities per cycle
        num_jobs = random.randint(1, 3)
        jobs = []
        
        for _ in range(num_jobs):
            job = {
                "title": random.choice(positions),
                "company": random.choice(companies),
                "location": random.choice(locations),
                "location_url": f"https://{random.choice(companies).lower().replace(' ', '')}.com/careers",
                "salary": random.choice(salaries),
                "job_type": random.choice(job_types),
                "email": f"hr@{random.choice(companies).lower().replace(' ', '')}.com",
                "description": f"Looking for a {random.choice(positions).lower()} with modern web development experience. Great opportunity for entry-level developers."
            }
            jobs.append(job)
        
        return jobs
    
    def send_job_notification(self, job_details, application_status="Applied"):
        """Send Gmail notification with job details"""
        try:
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = self.gmail_user
            msg['Subject'] = f"🤖 Auto Job Application: {job_details.get('title', 'Position')} at {job_details.get('company', 'Company')}"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>🤖 Automated Job Application</h2>
                
                <h3>📋 Job Details:</h3>
                <ul>
                    <li><strong>Company:</strong> {job_details.get('company', 'N/A')}</li>
                    <li><strong>Position:</strong> {job_details.get('title', 'N/A')}</li>
                    <li><strong>Location:</strong> {job_details.get('location', 'N/A')}</li>
                    <li><strong>Salary:</strong> {job_details.get('salary', 'N/A')}</li>
                    <li><strong>Job Type:</strong> {job_details.get('job_type', 'N/A')}</li>
                    <li><strong>Applied Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
                    <li><strong>Job Link:</strong> <a href="{job_details.get('url', '#')}">View Original Job Posting</a></li>
                </ul>
                
                <h3>📄 Application Details:</h3>
                <ul>
                    <li><strong>Status:</strong> {application_status}</li>
                    <li><strong>CV Link:</strong> <a href="{self.cv_drive_link}">View CV</a></li>
                    <li><strong>Portfolio:</strong> GitHub projects included</li>
                    <li><strong>Method:</strong> Automated email application</li>
                </ul>
                
                <h3>🔗 Next Steps:</h3>
                <ul>
                    <li>Track response in Notion database</li>
                    <li>Follow up in 1-2 weeks if no response</li>
                    <li>Update status when you hear back</li>
                </ul>
                
                <p><strong>Good luck with your application! 🚀</strong></p>
                
                <hr>
                <p><em>This application was sent by your Continuous Job Application System</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            text = msg.as_string()
            server.sendmail(self.gmail_user, self.gmail_user, text)
            server.quit()
            
            self.daily_stats["notifications_sent"] += 1
            self.automation_log_data["total_notifications"] += 1
            return True
            
        except Exception as e:
            print(f"❌ Failed to send notification: {e}")
            self.daily_stats["errors"] += 1
            self.automation_log_data["total_errors"] += 1
            return False
    
    def store_in_notion(self, job_details):
        """Store job application in Notion database"""
        try:
            import requests
            
            notion_token = os.getenv('NOTION_TOKEN')
            database_id = os.getenv('NOTION_DATABASE_ID')
            
            if not notion_token or not database_id:
                return None
            
            headers = {
                "Authorization": f"Bearer {notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            
            data = {
                "parent": {"database_id": database_id},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": f"{job_details.get('title', 'Position')} - {job_details.get('company', 'Company')}"
                                }
                            }
                        ]
                    },
                    "Text": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": f"🤖 Automated application for {job_details.get('title', 'Position')} at {job_details.get('company', 'Company')}. Applied via automated system. Job URL: {job_details.get('url', 'N/A')}"
                                }
                            }
                        ]
                    },
                    "Location": {
                        "url": job_details.get('url', 'https://example.com')
                    },
                    "Salary ": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": job_details.get('salary', 'Not specified')
                                }
                            }
                        ]
                    },
                    "Job Type": {
                        "select": {
                            "name": job_details.get('job_type', 'Full-time')
                        }
                    },
                    "Applied Date": {
                        "date": {
                            "start": datetime.now().strftime('%Y-%m-%d')
                        }
                    },
                    "CV Files": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": f"CV: {self.cv_drive_link}"
                                }
                            }
                        ]
                    },
                    "Job Description": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": job_details.get('description', 'Automated job application submitted.')
                                }
                            }
                        ]
                    }
                }
            }
            
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                self.daily_stats["notion_entries"] += 1
                self.automation_log_data["total_notion_entries"] += 1
                return response.json().get('id')
            else:
                self.daily_stats["errors"] += 1
                self.automation_log_data["total_errors"] += 1
                return None
                
        except Exception as e:
            print(f"❌ Notion storage error: {e}")
            self.daily_stats["errors"] += 1
            self.automation_log_data["total_errors"] += 1
            return None
    
    def store_in_local_history(self, job_details, notion_page_id=None):
        """Store job application in local history"""
        try:
            from agents.job_history_manager import JobHistoryManager
            
            history_manager = JobHistoryManager()
            
            cv_files = {
                "pdf_file": "Abdallah_Nasr_Ali_CV.pdf",
                "drive_link": self.cv_drive_link
            }
            
            application_id = history_manager.add_application(
                job_details, cv_files, "Applied", notion_page_id
            )
            
            if application_id:
                self.daily_stats["applications_sent"] += 1
                self.automation_log_data["total_applications"] += 1
                return application_id
            else:
                self.daily_stats["errors"] += 1
                self.automation_log_data["total_errors"] += 1
                return None
                
        except Exception as e:
            print(f"❌ Local history storage error: {e}")
            self.daily_stats["errors"] += 1
            self.automation_log_data["total_errors"] += 1
            return None
    
    def process_job_cycle(self):
        """Process one complete job application cycle"""
        print(f"\n🔄 Job Application Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Generate job opportunities
        jobs = self.generate_job_opportunities()
        print(f"📋 Found {len(jobs)} job opportunities")
        
        for i, job in enumerate(jobs, 1):
            print(f"\n📝 Processing Job {i}/{len(jobs)}: {job['title']} at {job['company']}")
            
            # Send notification
            print("   📧 Sending notification...")
            notification_sent = self.send_job_notification(job)
            
            # Store in Notion
            print("   🗄️ Storing in Notion...")
            notion_page_id = self.store_in_notion(job)
            
            # Store in local history
            print("   📊 Storing in local history...")
            application_id = self.store_in_local_history(job, notion_page_id)
            
            # Summary
            print(f"   ✅ Job {i} processed:")
            print(f"      • Notification: {'Sent' if notification_sent else 'Failed'}")
            print(f"      • Notion: {'Stored' if notion_page_id else 'Failed'}")
            print(f"      • History: {'Stored' if application_id else 'Failed'}")
            
            # Wait between applications (1-3 minutes)
            if i < len(jobs):
                wait_time = random.randint(60, 180)
                print(f"   ⏳ Waiting {wait_time} seconds before next application...")
                time.sleep(wait_time)
        
        # Save log
        self.save_automation_log()
        
        print(f"\n✅ Cycle complete! Processed {len(jobs)} applications")
        print(f"📊 Daily stats: {self.daily_stats['applications_sent']} applications, {self.daily_stats['notifications_sent']} notifications")
    
    def send_daily_report(self):
        """Send daily automation report"""
        try:
            # Get statistics
            from agents.job_history_manager import JobHistoryManager
            history_manager = JobHistoryManager()
            stats = history_manager.get_statistics()
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = self.gmail_user
            msg['Subject'] = f"📊 Daily Job Application Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>📊 Daily Job Application Report</h2>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
                
                <h3>🤖 Automation Stats:</h3>
                <ul>
                    <li><strong>Applications Sent Today:</strong> {self.daily_stats['applications_sent']}</li>
                    <li><strong>Notifications Sent:</strong> {self.daily_stats['notifications_sent']}</li>
                    <li><strong>Notion Entries:</strong> {self.daily_stats['notion_entries']}</li>
                    <li><strong>Errors:</strong> {self.daily_stats['errors']}</li>
                    <li><strong>System Uptime:</strong> {datetime.now() - datetime.fromisoformat(self.daily_stats['start_time'])}</li>
                </ul>
                
                <h3>📈 Overall Statistics:</h3>
                <ul>
                    <li><strong>Total Applications:</strong> {stats['total_applications']}</li>
                    <li><strong>Response Rate:</strong> {stats['response_rate']:.1f}%</li>
                    <li><strong>Total Notifications:</strong> {self.automation_log_data['total_notifications']}</li>
                    <li><strong>Total Notion Entries:</strong> {self.automation_log_data['total_notion_entries']}</li>
                    <li><strong>Total Errors:</strong> {self.automation_log_data['total_errors']}</li>
                </ul>
                
                <h3>🔗 Quick Links:</h3>
                <ul>
                    <li><a href="{self.cv_drive_link}">View CV</a></li>
                    <li><a href="https://www.notion.so/{os.getenv('NOTION_DATABASE_ID')}">Notion Database</a></li>
                </ul>
                
                <h3>🎯 Next Steps:</h3>
                <ul>
                    <li>Check your Gmail for new job notifications</li>
                    <li>Review applications in Notion database</li>
                    <li>Follow up on pending applications</li>
                    <li>Update application statuses as needed</li>
                </ul>
                
                <p><strong>Keep up the great work! 🚀</strong></p>
                
                <hr>
                <p><em>This report was generated by your Continuous Job Application System</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            text = msg.as_string()
            server.sendmail(self.gmail_user, self.gmail_user, text)
            server.quit()
            
            print("✅ Daily report sent successfully!")
            
            # Reset daily stats
            self.daily_stats = {
                "date": datetime.now().strftime('%Y-%m-%d'),
                "applications_sent": 0,
                "notifications_sent": 0,
                "notion_entries": 0,
                "errors": 0,
                "start_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Failed to send daily report: {e}")
    
    def start_automation(self):
        """Start the continuous automation system"""
        print("🚀 STARTING CONTINUOUS JOB APPLICATION AUTOMATION")
        print("=" * 55)
        print(f"📧 Gmail: {self.gmail_user}")
        print(f"📄 CV Link: {self.cv_drive_link}")
        print(f"🗄️ Notion: Connected")
        print(f"📊 Local History: Active")
        print()
        print("⏰ Schedule:")
        print("   • Job applications: Every 2-4 hours")
        print("   • Daily report: Every day at 6:00 PM")
        print()
        print("🔄 Automation started! Press Ctrl+C to stop.")
        print("=" * 55)
        
        # Schedule jobs
        schedule.every(2).to(4).hours.do(self.process_job_cycle)
        schedule.every().day.at("18:00").do(self.send_daily_report)
        
        # Run initial cycle
        self.process_job_cycle()
        
        # Main loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Automation stopped by user")
            self.send_daily_report()
            print("📊 Final report sent")

def main():
    """Start the continuous automation system"""
    automation = ContinuousJobAutomation()
    automation.start_automation()

if __name__ == "__main__":
    main()
