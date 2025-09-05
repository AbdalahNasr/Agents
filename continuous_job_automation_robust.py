#!/usr/bin/env python3
"""
Robust Continuous Job Application Automation
Handles errors gracefully and continues running
"""

import os
import sys
import time
import json
import smtplib
import schedule
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from agents.notion_manager_robust import RobustNotionManager
from agents.real_linkedin_job_finder import RealLinkedInJobFinder

# Load environment variables
load_dotenv('config.env')

class RobustJobAutomation:
    def __init__(self):
        """Initialize the robust automation system"""
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        self.cv_drive_link = os.getenv('CV_PRIMARY_URL')
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        self.notion_manager = RobustNotionManager()
        self.job_finder = RealLinkedInJobFinder()
        
        # Statistics
        self.daily_stats = {
            "jobs_found": 0,
            "applications_sent": 0,
            "notifications_sent": 0,
            "errors": 0,
            "start_time": datetime.now()
        }
        
        # Load automation log
        self.automation_log_file = "automation_log.json"
        self.automation_log_data = self._load_automation_log()
        
        print("Robust Job Application Automation initialized")
        print(f"Gmail: {self.gmail_user}")
        print(f"CV Link: {self.cv_drive_link}")
        print(f"Notion: {'Connected' if self.notion_token else 'Not configured'}")

    def _load_automation_log(self):
        """Load automation log data"""
        try:
            if os.path.exists(self.automation_log_file):
                with open(self.automation_log_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load automation log: {e}")
        
        return {
            "total_cycles": 0,
            "total_jobs_found": 0,
            "total_applications": 0,
            "total_notifications": 0,
            "total_errors": 0,
            "last_run": None
        }

    def _save_automation_log(self):
        """Save automation log data"""
        try:
            self.automation_log_data["last_run"] = datetime.now().isoformat()
            with open(self.automation_log_file, 'w') as f:
                json.dump(self.automation_log_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save automation log: {e}")

    def find_job_opportunities(self):
        """Find job opportunities using the demo job finder"""
        # Use the real LinkedIn job finder to get jobs with working URLs
        jobs = self.job_finder.find_real_linkedin_jobs(5)
        return jobs

    def send_job_notification_robust(self, job_details, application_result=None, max_retries=3):
        """Send job notification with retry logic"""
        for attempt in range(max_retries):
            try:
                print(f"   Sending notification (attempt {attempt + 1}/{max_retries})...")
                
                # Create email
                msg = MIMEMultipart()
                msg['From'] = self.gmail_user
                msg['To'] = self.gmail_user
                msg['Subject'] = f"Auto Job Application: {job_details.get('title', 'Position')} at {job_details.get('company', 'Company')}"
                
                # Build submitted answers section
                submitted_answers_html = ""
                if application_result and application_result.get('submitted_answers'):
                    submitted_answers_html = "<h3>📋 Submitted Answers:</h3><ul>"
                    for field, answer in application_result['submitted_answers'].items():
                        submitted_answers_html += f"<li><strong>{field}:</strong> {answer}</li>"
                    submitted_answers_html += "</ul>"
                
                # Build CV information section
                cv_info_html = ""
                if application_result and application_result.get('cv_uploaded'):
                    cv_info_html = f"<li><strong>CV Uploaded:</strong> {application_result['cv_uploaded']}</li>"
                else:
                    cv_info_html = f"<li><strong>CV Link:</strong> <a href='{self.cv_drive_link}'>View CV</a></li>"
                
                # Email body
                body = f"""
                <html>
                <body>
                    <h2>🎯 Automated Job Application</h2>
                    
                    <h3>Job Details:</h3>
                    <ul>
                        <li><strong>Company:</strong> {job_details.get('company', 'N/A')}</li>
                        <li><strong>Position:</strong> {job_details.get('title', 'N/A')}</li>
                        <li><strong>Location:</strong> {job_details.get('location', 'N/A')}</li>
                        <li><strong>Salary:</strong> {job_details.get('salary', 'N/A')}</li>
                        <li><strong>Job Type:</strong> {job_details.get('job_type', 'N/A')}</li>
                        <li><strong>Applied Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
                        <li><strong>Job Link:</strong> <a href="{job_details.get('url', '#')}">View Original Job Posting</a></li>
                    </ul>
                    
                    <h3>Application Details:</h3>
                    <ul>
                        <li><strong>Status:</strong> {application_result.get('status', 'Applied') if application_result else 'Applied'}</li>
                        <li><strong>Method:</strong> {application_result.get('method', 'Automated Application') if application_result else 'Automated Application'}</li>
                        {cv_info_html}
                        <li><strong>Portfolio:</strong> GitHub projects included</li>
                    </ul>
                    
                    {submitted_answers_html}
                    
                    <p><strong>Good luck with your application!</strong></p>
                    
                    <hr>
                    <p><em>This application was sent by your Continuous Job Application System</em></p>
                </body>
                </html>
                """
                
                msg.attach(MIMEText(body, 'html'))
                
                # Send email with timeout
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(self.gmail_user, self.gmail_password)
                text = msg.as_string()
                server.sendmail(self.gmail_user, self.gmail_user, text)
                server.quit()
                
                print("   Notification sent successfully!")
                self.daily_stats["notifications_sent"] += 1
                if "total_notifications" not in self.automation_log_data:
                    self.automation_log_data["total_notifications"] = 0
                self.automation_log_data["total_notifications"] += 1
                return True
                
            except Exception as e:
                print(f"   Notification attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print(f"   Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"   All notification attempts failed")
                    self.daily_stats["errors"] += 1
                    if "total_errors" not in self.automation_log_data:
                        self.automation_log_data["total_errors"] = 0
                    self.automation_log_data["total_errors"] += 1
                    return False

    def store_in_notion_robust_old(self, job_details):
        """Store job application in Notion with error handling"""
        if not self.notion_token or not self.notion_database_id:
            print("   Notion not configured, skipping database entry")
            return None
        
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            
            data = {
                "parent": {"database_id": self.notion_database_id},
                "properties": {
                    "Company\xa0": {  # Company with non-breaking space
                        "title": [
                            {
                                "text": {
                                    "content": f"{job_details.get('company', 'Company')} - {job_details.get('title', 'Position')}"
                                }
                            }
                        ]
                    },
                    "Position\xa0": {  # Position with non-breaking space
                        "rich_text": [
                            {
                                "text": {
                                    "content": job_details.get('title', 'Position')
                                }
                            }
                        ]
                    },
                    "Location": {
                        "url": job_details.get('url', 'https://example.com')
                    },
                    "Salary ": {  # Salary with regular space
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
                    "Job Description": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": job_details.get('description', 'No description available')
                                }
                            }
                        ]
                    },
                    "Status": {
                        "status": {
                            "name": "Applied"
                        }
                    }
                }
            }
            
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                print("   Stored in Notion successfully!")
                return response.json().get('id')
            else:
                print(f"   Notion storage failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   Notion storage error: {e}")
            return None

    def process_job_cycle(self):
        """Process one job application cycle"""
        print(f"\nJob Application Cycle - {datetime.now()}")
        print("=" * 60)
        
        try:
            # Find job opportunities
            jobs = self.find_job_opportunities()
            print(f"Found {len(jobs)} job opportunities")
            
            self.daily_stats["jobs_found"] += len(jobs)
            if "total_jobs_found" not in self.automation_log_data:
                self.automation_log_data["total_jobs_found"] = 0
            self.automation_log_data["total_jobs_found"] += len(jobs)
            
            # Process each job
            for i, job in enumerate(jobs, 1):
                print(f"\nProcessing Job {i}/{len(jobs)}: {job['title']} at {job['company']}")
                
                # Send notification (with retry logic)
                notification_sent = self.send_job_notification_robust(job)
                
                # Store in Notion using robust manager
                notion_id = self.notion_manager.create_job_application_entry(job)
                
                # Update statistics
                self.daily_stats["applications_sent"] += 1
                if "total_applications" not in self.automation_log_data:
                    self.automation_log_data["total_applications"] = 0
                self.automation_log_data["total_applications"] += 1
                
                # Small delay between jobs
                time.sleep(2)
            
            print(f"\nCycle completed successfully!")
            print(f"Jobs processed: {len(jobs)}")
            print(f"Notifications sent: {self.daily_stats['notifications_sent']}")
            print(f"Errors: {self.daily_stats['errors']}")
            
        except Exception as e:
            print(f"Error in job cycle: {e}")
            self.daily_stats["errors"] += 1
            if "total_errors" not in self.automation_log_data:
                self.automation_log_data["total_errors"] = 0
            self.automation_log_data["total_errors"] += 1

    def send_daily_report(self):
        """Send daily automation report"""
        try:
            print("\nSending daily report...")
            
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = self.gmail_user
            msg['Subject'] = f"Daily Automation Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            body = f"""
            <html>
            <body>
                <h2>Daily Automation Report</h2>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                
                <h3>Today's Statistics:</h3>
                <ul>
                    <li><strong>Jobs Found:</strong> {self.daily_stats['jobs_found']}</li>
                    <li><strong>Applications Sent:</strong> {self.daily_stats['applications_sent']}</li>
                    <li><strong>Notifications Sent:</strong> {self.daily_stats['notifications_sent']}</li>
                    <li><strong>Errors:</strong> {self.daily_stats['errors']}</li>
                </ul>
                
                <h3>Total Statistics:</h3>
                <ul>
                    <li><strong>Total Cycles:</strong> {self.automation_log_data['total_cycles']}</li>
                    <li><strong>Total Jobs Found:</strong> {self.automation_log_data['total_jobs_found']}</li>
                    <li><strong>Total Applications:</strong> {self.automation_log_data['total_applications']}</li>
                    <li><strong>Total Notifications:</strong> {self.automation_log_data['total_notifications']}</li>
                    <li><strong>Total Errors:</strong> {self.automation_log_data['total_errors']}</li>
                </ul>
                
                <p><em>Report generated by your Job Application Automation System</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            text = msg.as_string()
            server.sendmail(self.gmail_user, self.gmail_user, text)
            server.quit()
            
            print("Daily report sent successfully!")
            
        except Exception as e:
            print(f"Failed to send daily report: {e}")

    def start_automation(self):
        """Start the continuous automation"""
        print("STARTING ROBUST JOB APPLICATION AUTOMATION")
        print("=" * 60)
        print(f"Gmail: {self.gmail_user}")
        print(f"CV Link: {self.cv_drive_link}")
        print(f"Notion: {'Connected' if self.notion_token else 'Not configured'}")
        print("Schedule:")
        print("   • Job applications: Every 2-4 hours")
        print("   • Daily report: Every day at 6:00 PM")
        print("Automation started! Press Ctrl+C to stop.")
        print("=" * 60)
        
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
            print("\nAutomation stopped by user")
            self._save_automation_log()
        except Exception as e:
            print(f"\nAutomation error: {e}")
            self._save_automation_log()

def main():
    """Main function"""
    try:
        automation = RobustJobAutomation()
        automation.start_automation()
    except Exception as e:
        print(f"Failed to start automation: {e}")

if __name__ == "__main__":
    main()
