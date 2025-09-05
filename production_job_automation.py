#!/usr/bin/env python3
"""
Production Job Automation - Real Job Applications for Real Users
"""

import os
import time
import json
import schedule
from datetime import datetime, timedelta
from dotenv import load_dotenv
from agents.real_job_application_system import RealJobApplicationSystem
from agents.notion_manager_robust import RobustNotionManager

# Load environment variables
load_dotenv('config.env')

class ProductionJobAutomation:
    def __init__(self):
        """Initialize the production automation system"""
        self.job_system = RealJobApplicationSystem()
        self.notion_manager = RobustNotionManager()
        
        # Configuration
        self.max_applications_per_cycle = int(os.getenv('MAX_APPLICATIONS_PER_CYCLE', '3'))
        self.job_search_interval_hours = int(os.getenv('JOB_SEARCH_INTERVAL_HOURS', '4'))
        self.daily_report_time = os.getenv('DAILY_REPORT_TIME', '18:00')
        
        # Statistics
        self.daily_stats = {
            "jobs_found": 0,
            "applications_made": 0,
            "successful_applications": 0,
            "errors": 0
        }
        
        # Load automation log
        self.automation_log_file = 'production_automation_log.json'
        self.automation_log_data = self._load_automation_log()
        
        print("🚀 Production Job Automation Initialized")
        print(f"📊 Max applications per cycle: {self.max_applications_per_cycle}")
        print(f"⏰ Job search interval: {self.job_search_interval_hours} hours")
        print(f"📧 Daily report time: {self.daily_report_time}")
    
    def _load_automation_log(self) -> dict:
        """Load automation log data"""
        try:
            with open(self.automation_log_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "total_cycles": 0,
                "total_applications": 0,
                "total_jobs_found": 0,
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
    
    def run_job_search_cycle(self):
        """Run a complete job search and application cycle"""
        try:
            print(f"\n🔍 Job Search Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # Run the real job application system
            result = self.job_system.run_job_search_cycle(
                max_applications=self.max_applications_per_cycle
            )
            
            # Update statistics
            self.daily_stats["jobs_found"] += result.get("total_jobs_found", 0)
            self.daily_stats["applications_made"] += result.get("applications_made", 0)
            self.daily_stats["successful_applications"] += result.get("applications_made", 0)
            
            # Update automation log
            self.automation_log_data["total_cycles"] += 1
            self.automation_log_data["total_applications"] += result.get("applications_made", 0)
            self.automation_log_data["total_jobs_found"] += result.get("total_jobs_found", 0)
            self.automation_log_data["last_cycle"] = datetime.now().isoformat()
            
            # Store successful applications in Notion
            if result.get("applications_made", 0) > 0:
                self._store_applications_in_notion(result.get("results", []))
            
            # Save logs
            self._save_automation_log()
            
            print(f"\n✅ Cycle completed successfully!")
            print(f"📊 Applications made: {result.get('applications_made', 0)}")
            print(f"🔍 Jobs found: {result.get('total_jobs_found', 0)}")
            
        except Exception as e:
            print(f"❌ Error in job search cycle: {e}")
            self.daily_stats["errors"] += 1
            self.automation_log_data["total_cycles"] += 1
            self._save_automation_log()
    
    def _store_applications_in_notion(self, results: list):
        """Store successful applications in Notion"""
        for result in results:
            if result.get("status") == "applied":
                # Get the job details from the application history
                job_details = self._get_job_details_from_result(result)
                if job_details:
                    notion_id = self.notion_manager.create_job_application_entry(job_details)
                    if notion_id:
                        print(f"  📝 Stored in Notion: {notion_id}")
    
    def _get_job_details_from_result(self, result: dict) -> dict:
        """Get job details from application result"""
        # This would extract job details from the application result
        # For now, we'll create a basic job details structure
        return {
            "title": "Applied Position",
            "company": "Applied Company",
            "location": "Applied Location",
            "salary": "Not specified",
            "job_type": "Full-time",
            "url": "https://example.com",
            "description": f"Application submitted via {result.get('method', 'unknown')} method"
        }
    
    def send_daily_report(self):
        """Send daily automation report"""
        try:
            print(f"\n📊 Daily Report - {datetime.now().strftime('%Y-%m-%d')}")
            print("=" * 50)
            
            # Get application statistics
            stats = self.job_system.get_application_statistics()
            
            # Create report
            report = {
                "date": datetime.now().strftime('%Y-%m-%d'),
                "daily_stats": self.daily_stats,
                "total_stats": stats,
                "automation_log": self.automation_log_data
            }
            
            # Display report
            print(f"📈 Daily Statistics:")
            print(f"  Jobs found: {self.daily_stats['jobs_found']}")
            print(f"  Applications made: {self.daily_stats['applications_made']}")
            print(f"  Successful applications: {self.daily_stats['successful_applications']}")
            print(f"  Errors: {self.daily_stats['errors']}")
            
            print(f"\n📊 Total Statistics:")
            print(f"  Total applications: {stats['total_applications']}")
            print(f"  Success rate: {stats['success_rate']}")
            print(f"  Companies applied to: {len(stats['companies_applied_to'])}")
            
            # Reset daily stats
            self.daily_stats = {
                "jobs_found": 0,
                "applications_made": 0,
                "successful_applications": 0,
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
    
    def start_automation(self):
        """Start the production automation"""
        print("🚀 Starting Production Job Automation")
        print("=" * 50)
        print(f"👤 User: {self.job_system.user_profile['name']}")
        print(f"🎯 Target Roles: {', '.join(self.job_system.user_profile['target_roles'])}")
        print(f"📍 Location: {self.job_system.user_profile['location']}")
        print(f"💼 Max applications per cycle: {self.max_applications_per_cycle}")
        print(f"⏰ Job search interval: {self.job_search_interval_hours} hours")
        print(f"📧 Daily report time: {self.daily_report_time}")
        print()
        
        # Schedule job search cycles
        schedule.every(self.job_search_interval_hours).hours.do(self.run_job_search_cycle)
        
        # Schedule daily reports
        schedule.every().day.at(self.daily_report_time).do(self.send_daily_report)
        
        print("✅ Automation scheduled!")
        print("📅 Schedule:")
        print(f"   • Job search cycles: Every {self.job_search_interval_hours} hours")
        print(f"   • Daily reports: Every day at {self.daily_report_time}")
        print()
        print("🔄 Automation started! Press Ctrl+C to stop.")
        print("=" * 50)
        
        # Run initial cycle
        self.run_job_search_cycle()
        
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
    print("🚀 Production Job Automation System")
    print("=" * 50)
    print("⚠️  WARNING: This system will apply to REAL jobs!")
    print("⚠️  Make sure your profile and CV are up to date!")
    print("⚠️  Review your application settings before starting!")
    print()
    
    # Ask for confirmation
    response = input("Do you want to start the automation? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        automation = ProductionJobAutomation()
        automation.start_automation()
    else:
        print("❌ Automation cancelled by user")

if __name__ == "__main__":
    main()
