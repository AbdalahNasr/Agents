#!/usr/bin/env python3
"""
Real Job Automation - Actually applies to jobs, not just finds them
"""

import os
import time
import json
import schedule
from datetime import datetime, timedelta
from dotenv import load_dotenv
from agents.real_job_applicator import RealJobApplicator
from agents.notion_manager_robust import RobustNotionManager
from agents.real_linkedin_job_finder import RealLinkedInJobFinder

# Load environment variables
load_dotenv('config.env')

class RealJobAutomation:
    def __init__(self):
        """Initialize the real job automation system"""
        self.applicator = RealJobApplicator()
        self.notion_manager = RobustNotionManager()
        self.job_finder = RealLinkedInJobFinder()
        
        # Configuration
        self.max_applications_per_cycle = int(os.getenv('MAX_APPLICATIONS_PER_CYCLE', '3'))
        self.job_search_interval_hours = int(os.getenv('JOB_SEARCH_INTERVAL_HOURS', '4'))
        self.daily_report_time = os.getenv('DAILY_REPORT_TIME', '18:00')
        
        # Statistics
        self.daily_stats = {
            "jobs_found": 0,
            "applications_made": 0,
            "successful_applications": 0,
            "failed_applications": 0,
            "skipped_applications": 0,
            "errors": 0
        }
        
        # Load automation log
        self.automation_log_file = 'real_automation_log.json'
        self.automation_log_data = self._load_automation_log()
        
        print("🚀 Real Job Automation Initialized")
        print(f"📊 Max applications per cycle: {self.max_applications_per_cycle}")
        print(f"⏰ Job search interval: {self.job_search_interval_hours} hours")
        print(f"📧 Daily report time: {self.daily_report_time}")
        print("⚠️  WARNING: This system will apply to REAL jobs!")
    
    def _load_automation_log(self) -> dict:
        """Load automation log data"""
        try:
            with open(self.automation_log_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "total_cycles": 0,
                "total_applications": 0,
                "total_successful": 0,
                "total_failed": 0,
                "total_skipped": 0,
                "start_date": datetime.now().isoformat(),
                "last_cycle": None
            }
    
    def _save_automation_log(self):
        """Save automation log data"""
        try:
            with open(self.automation_log_file, 'w') as f:
                json.dump(self.automation_log_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save automation log: {e}")
    
    def find_real_jobs(self, limit: int = 10) -> list:
        """Find real job postings from LinkedIn and other sources"""
        print(f"🔍 Searching for real job opportunities...")
        
        # Use the real LinkedIn job finder to get jobs with working URLs
        real_jobs = self.job_finder.find_mixed_job_sources(limit)
        
        # Filter out already applied jobs
        new_jobs = self._filter_new_jobs(real_jobs)
        
        print(f"✅ Found {len(new_jobs)} new job opportunities")
        return new_jobs
    
    def _filter_new_jobs(self, jobs: list) -> list:
        """Filter out jobs that have already been applied to"""
        applied_urls = {app["job_url"] for app in self.applicator.application_history}
        return [job for job in jobs if job["url"] not in applied_urls]
    
    def run_job_application_cycle(self):
        """Run a complete job application cycle"""
        try:
            print(f"\n🎯 Job Application Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # Find real jobs
            jobs = self.find_real_jobs(limit=self.max_applications_per_cycle * 2)
            
            if not jobs:
                print("❌ No new job opportunities found")
                return
            
            # Apply to jobs
            applications_made = 0
            successful_applications = 0
            failed_applications = 0
            skipped_applications = 0
            
            for i, job in enumerate(jobs[:self.max_applications_per_cycle], 1):
                print(f"\n📝 Application {i}/{min(len(jobs), self.max_applications_per_cycle)}")
                
                # Apply to the job
                result = self.applicator.apply_to_job(job["url"], job)
                
                # Update statistics
                applications_made += 1
                
                if result.get("status") == "applied":
                    successful_applications += 1
                    print(f"  ✅ Successfully applied to {job['title']} at {job['company']}")
                    
                    # Show submitted answers
                    if result.get("submitted_answers"):
                        print(f"  📋 Submitted answers:")
                        for field, answer in result["submitted_answers"].items():
                            print(f"    {field}: {answer}")
                    
                    # Show CV information
                    if result.get("cv_uploaded"):
                        print(f"  📄 CV uploaded: {result['cv_uploaded']}")
                    
                    # Store in Notion with application result
                    notion_id = self.notion_manager.create_job_application_entry(job, result)
                    if notion_id:
                        print(f"  📝 Stored in Notion: {notion_id}")
                    
                    # Send notification with application result
                    self.send_application_notification(job, result)
                    
                elif result.get("status") == "skipped":
                    skipped_applications += 1
                    print(f"  ⏭️ Skipped {job['title']} at {job['company']} - {result.get('reason', 'unknown')}")
                    
                else:
                    failed_applications += 1
                    print(f"  ❌ Failed to apply to {job['title']} at {job['company']} - {result.get('error', 'unknown error')}")
                
                # Small delay between applications
                time.sleep(2)
            
            # Update daily statistics
            self.daily_stats["jobs_found"] += len(jobs)
            self.daily_stats["applications_made"] += applications_made
            self.daily_stats["successful_applications"] += successful_applications
            self.daily_stats["failed_applications"] += failed_applications
            self.daily_stats["skipped_applications"] += skipped_applications
            
            # Update automation log
            self.automation_log_data["total_cycles"] += 1
            self.automation_log_data["total_applications"] += applications_made
            self.automation_log_data["total_successful"] += successful_applications
            self.automation_log_data["total_failed"] += failed_applications
            self.automation_log_data["total_skipped"] += skipped_applications
            self.automation_log_data["last_cycle"] = datetime.now().isoformat()
            
            # Save logs
            self._save_automation_log()
            
            print(f"\n✅ Application cycle completed!")
            print(f"📊 Applications made: {applications_made}")
            print(f"✅ Successful: {successful_applications}")
            print(f"❌ Failed: {failed_applications}")
            print(f"⏭️ Skipped: {skipped_applications}")
            
        except Exception as e:
            print(f"❌ Error in job application cycle: {e}")
            self.daily_stats["errors"] += 1
            self.automation_log_data["total_cycles"] += 1
            self._save_automation_log()
    
    def send_daily_report(self):
        """Send daily automation report"""
        try:
            print(f"\n📊 Daily Report - {datetime.now().strftime('%Y-%m-%d')}")
            print("=" * 50)
            
            # Get application statistics
            total_applications = len(self.applicator.application_history)
            successful_applications = len([app for app in self.applicator.application_history if app.get("status") == "applied"])
            
            # Create report
            report = {
                "date": datetime.now().strftime('%Y-%m-%d'),
                "daily_stats": self.daily_stats,
                "total_applications": total_applications,
                "successful_applications": successful_applications,
                "success_rate": f"{(successful_applications/total_applications*100):.1f}%" if total_applications > 0 else "0%",
                "automation_log": self.automation_log_data
            }
            
            # Display report
            print(f"📈 Daily Statistics:")
            print(f"  Jobs found: {self.daily_stats['jobs_found']}")
            print(f"  Applications made: {self.daily_stats['applications_made']}")
            print(f"  Successful applications: {self.daily_stats['successful_applications']}")
            print(f"  Failed applications: {self.daily_stats['failed_applications']}")
            print(f"  Skipped applications: {self.daily_stats['skipped_applications']}")
            print(f"  Errors: {self.daily_stats['errors']}")
            
            print(f"\n📊 Total Statistics:")
            print(f"  Total applications: {total_applications}")
            print(f"  Successful applications: {successful_applications}")
            print(f"  Success rate: {report['success_rate']}")
            print(f"  Total cycles: {self.automation_log_data['total_cycles']}")
            
            # Reset daily stats
            self.daily_stats = {
                "jobs_found": 0,
                "applications_made": 0,
                "successful_applications": 0,
                "failed_applications": 0,
                "skipped_applications": 0,
                "errors": 0
            }
            
            # Save report
            self._save_daily_report(report)
            
        except Exception as e:
            print(f"❌ Error sending daily report: {e}")
    
    def _save_daily_report(self, report: dict):
        """Save daily report to file"""
        try:
            report_file = f"daily_reports/report_{datetime.now().strftime('%Y%m%d')}.json"
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"📄 Report saved: {report_file}")
            
        except Exception as e:
            print(f"Warning: Could not save daily report: {e}")
    
    def send_application_notification(self, job_details: dict, application_result: dict):
        """Send notification about successful application"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Get email credentials
            gmail_user = os.getenv('GMAIL_USER')
            gmail_password = os.getenv('GMAIL_APP_PASSWORD')
            
            if not gmail_user or not gmail_password:
                print("  ⚠️ Email credentials not configured")
                return
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = gmail_user
            msg['Subject'] = f"🎯 Real Job Application: {job_details.get('title', 'Position')} at {job_details.get('company', 'Company')}"
            
            # Build submitted answers section
            submitted_answers_html = ""
            if application_result.get('submitted_answers'):
                submitted_answers_html = "<h3>📋 Submitted Answers:</h3><ul>"
                for field, answer in application_result['submitted_answers'].items():
                    submitted_answers_html += f"<li><strong>{field}:</strong> {answer}</li>"
                submitted_answers_html += "</ul>"
            
            # Build CV information section
            cv_info_html = ""
            if application_result.get('cv_uploaded'):
                cv_info_html = f"<li><strong>CV Uploaded:</strong> {application_result['cv_uploaded']}</li>"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>🎯 Real Job Application Successful!</h2>
                
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
                    <li><strong>Status:</strong> {application_result.get('status', 'Applied')}</li>
                    <li><strong>Method:</strong> {application_result.get('method', 'Automated Application')}</li>
                    {cv_info_html}
                </ul>
                
                {submitted_answers_html}
                
                <p><strong>🎉 Your application was submitted successfully!</strong></p>
                <p>Check your email and LinkedIn for responses from the employer.</p>
                
                <hr>
                <p><em>This application was sent by your Real Job Application System</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()
            
            print(f"  📧 Notification sent to {gmail_user}")
            
        except Exception as e:
            print(f"  ⚠️ Could not send notification: {e}")
    
    def start_automation(self):
        """Start the real job automation"""
        print("🚀 Starting Real Job Automation")
        print("=" * 50)
        print("⚠️  WARNING: This system will apply to REAL jobs!")
        print("⚠️  Make sure your profile and CV are up to date!")
        print()
        
        # Show user profile
        profile = self.applicator.user_profile
        print(f"👤 User Profile:")
        print(f"  Name: {profile['personal_info']['name']}")
        print(f"  Email: {profile['personal_info']['email']}")
        print(f"  Target Roles: {', '.join(profile['professional_info']['target_roles'])}")
        print(f"  Skills: {', '.join(profile['professional_info']['skills'][:5])}...")
        print()
        
        # Ask for confirmation
        response = input("Do you want to start applying to REAL jobs? (yes/no): ").lower().strip()
        
        if response not in ['yes', 'y']:
            print("❌ Automation cancelled by user")
            return
        
        print(f"🎯 Max applications per cycle: {self.max_applications_per_cycle}")
        print(f"⏰ Job search interval: {self.job_search_interval_hours} hours")
        print(f"📧 Daily report time: {self.daily_report_time}")
        print()
        
        # Schedule job application cycles
        schedule.every(self.job_search_interval_hours).hours.do(self.run_job_application_cycle)
        
        # Schedule daily reports
        schedule.every().day.at(self.daily_report_time).do(self.send_daily_report)
        
        print("✅ Automation scheduled!")
        print("📅 Schedule:")
        print(f"   • Job applications: Every {self.job_search_interval_hours} hours")
        print(f"   • Daily reports: Every day at {self.daily_report_time}")
        print()
        print("🔄 Automation started! Press Ctrl+C to stop.")
        print("=" * 50)
        
        # Run initial cycle
        self.run_job_application_cycle()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Automation stopped by user")
            self.send_daily_report()

def main():
    """Main function"""
    print("🚀 Real Job Application Automation")
    print("=" * 50)
    print("⚠️  WARNING: This system applies to REAL jobs!")
    print("⚠️  Make sure your profile and CV are up to date!")
    print("⚠️  Review your application settings before starting!")
    print()
    
    automation = RealJobAutomation()
    automation.start_automation()

if __name__ == "__main__":
    main()
