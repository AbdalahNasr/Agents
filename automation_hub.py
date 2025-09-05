#!/usr/bin/env python3
"""
🚀 AUTOMATION HUB - Your Personal Productivity Command Center
Automatically runs all agents, handles errors, and manages the entire workflow
"""
import os
import sys
import time
import json
import schedule
from datetime import datetime
from typing import Dict, List, Any
import traceback

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    from utils.logger import AgentLogger
    from utils.notifications import NotificationManager
    from config import Config
    from openai import OpenAI
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install missing dependencies: pip install -r requirements.txt")
    sys.exit(1)

class AutomationHub:
    def __init__(self):
        """Initialize the Automation Hub"""
        load_dotenv('config.env')
        
        self.logger = AgentLogger("automation_hub")
        self.notifications = NotificationManager("automation_hub")
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Agent status tracking
        self.agent_status = {
            "linkedin_manager": {"status": "idle", "last_run": None, "success_count": 0, "error_count": 0},
            "cv_generator": {"status": "idle", "last_run": None, "success_count": 0, "error_count": 0},
            "job_application": {"status": "idle", "last_run": None, "success_count": 0, "error_count": 0},
            "email_agent": {"status": "idle", "last_run": None, "success_count": 0, "error_count": 0},
            "ats_optimizer": {"status": "idle", "last_run": None, "success_count": 0, "error_count": 0},
            "enhanced_job_application": {"status": "idle", "last_run": None, "success_count": 0, "error_count": 0}
        }
        
        # Workflow configuration
        self.workflow_config = {
            "linkedin_check_interval": 30,  # minutes
            "cv_update_interval": 60,       # minutes  
            "job_search_interval": 45,      # minutes
            "email_check_interval": 15      # minutes
        }
        
        self.logger.info("🚀 Automation Hub initialized successfully!")
        self.notifications.notify("🚀 Automation Hub is now running and monitoring your productivity!", "INFO")
    
    def test_linkedin_system(self) -> Dict[str, Any]:
        """Test LinkedIn system functionality"""
        self.logger.info("🔗 Testing LinkedIn System...")
        
        try:
            # Import LinkedIn Manager
            from agents.linkedin_manager import LinkedInManager
            
            manager = LinkedInManager()
            
            if not manager.access_token:
                return {"success": False, "error": "No LinkedIn access token found"}
            
            # Test profile retrieval
            profile = manager.get_profile(manager.access_token)
            if not profile:
                return {"success": False, "error": "Failed to retrieve LinkedIn profile"}
            
            # Test job search
            jobs = manager.run_job_search(manager.access_token)
            
            # Test profile optimization
            optimization = manager.run_profile_optimization(manager.access_token)
            
            result = {
                "success": True,
                "profile": {
                    "name": f"{profile.get('localizedFirstName', '')} {profile.get('localizedLastName', '')}",
                    "headline": profile.get('localizedHeadline', 'N/A')
                },
                "jobs_found": len(jobs) if jobs else 0,
                "optimization": optimization
            }
            
            self.logger.success("✅ LinkedIn system test completed successfully!")
            return result
            
        except Exception as e:
            error_msg = f"LinkedIn system test failed: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def run_cv_generation(self) -> Dict[str, Any]:
        """Run CV generation workflow"""
        self.logger.info("📄 Running CV Generation Workflow...")
        
        try:
            from smart_cv_generator import SmartCVGenerator
            
            generator = SmartCVGenerator()
            result = generator.create_cv_structure()
            
            if result:
                self.logger.success("✅ CV generation completed successfully!")
                return {"success": True, "files_created": result}
            else:
                return {"success": False, "error": "CV generation failed"}
                
        except Exception as e:
            error_msg = f"CV generation failed: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def run_job_application_workflow(self) -> Dict[str, Any]:
        """Run job application workflow"""
        self.logger.info("💼 Running Job Application Workflow...")
        
        try:
            from agents.job_application_demo_agent import JobApplicationDemoAgent
            
            agent = JobApplicationDemoAgent()
            drafts = agent.run_demo()
            
            if drafts:
                self.logger.success(f"✅ Job application workflow completed! Created {len(drafts)} drafts")
                return {"success": True, "drafts_created": len(drafts)}
            else:
                return {"success": False, "error": "No job application drafts created"}
                
        except Exception as e:
            error_msg = f"Job application workflow failed: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def run_enhanced_job_application_workflow(self) -> Dict[str, Any]:
        """Run enhanced job application workflow with ATS optimization"""
        self.logger.info("🎯 Running Enhanced Job Application Workflow with ATS Optimization...")
        
        try:
            from agents.enhanced_job_application_agent import EnhancedJobApplicationAgent
            
            agent = EnhancedJobApplicationAgent()
            drafts = agent.run_enhanced_job_search(
                keywords=["full stack developer", "frontend developer", "react developer"],
                location="Cairo, Egypt"
            )
            
            if drafts:
                # Get ATS statistics
                stats = agent.get_ats_statistics(drafts)
                
                self.logger.success(f"✅ Enhanced job application workflow completed! Created {len(drafts)} ATS-optimized drafts")
                return {
                    "success": True, 
                    "drafts_created": len(drafts),
                    "ats_statistics": stats,
                    "average_ats_score": stats.get('average_ats_score', 0),
                    "applications_above_threshold": stats.get('applications_above_threshold', 0)
                }
            else:
                return {"success": False, "error": "No ATS-optimized application drafts created"}
                
        except Exception as e:
            error_msg = f"Enhanced job application workflow failed: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def run_ats_optimization_workflow(self) -> Dict[str, Any]:
        """Run ATS optimization workflow"""
        self.logger.info("🔧 Running ATS Optimization Workflow...")
        
        try:
            from agents.ats_optimizer import ATSOptimizer
            from agents.ats_cv_generator import ATSCVGenerator
            
            # Initialize components
            ats_optimizer = ATSOptimizer()
            cv_generator = ATSCVGenerator()
            
            # Sample job for testing
            sample_job = {
                "title": "Senior Full Stack Developer",
                "company": "TechCorp",
                "location": "Cairo, Egypt",
                "description": """
                We are looking for a Senior Full Stack Developer to join our team.
                The ideal candidate will have experience with React, Node.js, and modern web technologies.
                Experience with mobile development, APIs, and database management is required.
                Strong problem-solving skills and ability to work in fast-paced environments.
                """
            }
            
            # Generate job-specific CV
            cv_result = cv_generator.generate_job_specific_cv(sample_job)
            
            if cv_result:
                # Save CV files
                saved_files = cv_generator.save_cv_files(cv_result)
                
                self.logger.success(f"✅ ATS optimization workflow completed! Generated CV with {cv_result['ats_analysis']['overall_score']}/100 ATS score")
                return {
                    "success": True,
                    "ats_score": cv_result['ats_analysis']['overall_score'],
                    "job_title": cv_result['job_info']['title'],
                    "company": cv_result['job_info']['company'],
                    "files_created": len(saved_files),
                    "recommendations_count": len(cv_result['ats_analysis']['recommendations']),
                    "missing_elements_count": len(cv_result['ats_analysis']['missing_elements'])
                }
            else:
                return {"success": False, "error": "Failed to generate ATS-optimized CV"}
                
        except Exception as e:
            error_msg = f"ATS optimization workflow failed: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def run_email_workflow(self) -> Dict[str, Any]:
        """Run email processing workflow"""
        self.logger.info("📧 Running Email Workflow...")
        
        try:
            # For now, just test email notifications
            test_message = f"""
            🔔 Email Workflow Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            This is an automated test of your email notification system.
            Your automation hub is working correctly!
            
            Next scheduled tasks:
            - LinkedIn check: Every {self.workflow_config['linkedin_check_interval']} minutes
            - CV updates: Every {self.workflow_config['cv_update_interval']} minutes
            - Job search: Every {self.workflow_config['job_search_interval']} minutes
            - Email check: Every {self.workflow_config['email_check_interval']} minutes
            """
            
            self.notifications.notify(test_message, "INFO", subject="🚀 Automation Hub Status Update")
            
            self.logger.success("✅ Email workflow test completed!")
            return {"success": True, "message": "Email notification sent successfully"}
            
        except Exception as e:
            error_msg = f"Email workflow failed: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def run_full_workflow(self) -> Dict[str, Any]:
        """Run the complete automation workflow"""
        self.logger.info("🚀 Starting Full Automation Workflow...")
        
        workflow_results = {}
        start_time = datetime.now()
        
        # 1. Test LinkedIn System
        self.logger.info("Step 1/4: Testing LinkedIn System...")
        linkedin_result = self.test_linkedin_system()
        workflow_results["linkedin"] = linkedin_result
        self.agent_status["linkedin_manager"]["last_run"] = datetime.now()
        
        if linkedin_result["success"]:
            self.agent_status["linkedin_manager"]["success_count"] += 1
        else:
            self.agent_status["linkedin_manager"]["error_count"] += 1
        
        time.sleep(2)  # Brief pause between steps
        
        # 2. Run CV Generation
        self.logger.info("Step 2/4: Running CV Generation...")
        cv_result = self.run_cv_generation()
        workflow_results["cv_generation"] = cv_result
        self.agent_status["cv_generator"]["last_run"] = datetime.now()
        
        if cv_result["success"]:
            self.agent_status["cv_generator"]["success_count"] += 1
        else:
            self.agent_status["cv_generator"]["error_count"] += 1
        
        time.sleep(2)
        
        # 3. Run Job Application Workflow
        self.logger.info("Step 3/4: Running Job Application Workflow...")
        job_result = self.run_job_application_workflow()
        workflow_results["job_application"] = job_result
        self.agent_status["job_application"]["last_run"] = datetime.now()
        
        if job_result["success"]:
            self.agent_status["job_application"]["success_count"] += 1
        else:
            self.agent_status["job_application"]["error_count"] += 1
        
        time.sleep(2)
        
        # 4. Run Email Workflow
        self.logger.info("Step 4/4: Running Email Workflow...")
        email_result = self.run_email_workflow()
        workflow_results["email"] = email_result
        self.agent_status["email_agent"]["last_run"] = datetime.now()
        
        if email_result["success"]:
            self.agent_status["email_agent"]["success_count"] += 1
        else:
            self.agent_status["email_agent"]["error_count"] += 1
        
        # Calculate overall success
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        successful_steps = sum(1 for result in workflow_results.values() if result.get("success", False))
        total_steps = len(workflow_results)
        
        overall_result = {
            "success": successful_steps == total_steps,
            "success_rate": f"{successful_steps}/{total_steps}",
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat(),
            "results": workflow_results
        }
        
        # Send completion notification
        if overall_result["success"]:
            self.logger.success("🎉 Full workflow completed successfully!")
            self.notifications.notify(
                f"🎉 Full automation workflow completed successfully!\n\n"
                f"✅ All {total_steps} steps completed\n"
                f"⏱️ Duration: {duration:.1f} seconds\n"
                f"📊 Success Rate: {successful_steps}/{total_steps}",
                "SUCCESS",
                subject="🎯 Automation Workflow Completed Successfully!"
            )
        else:
            self.logger.warning(f"⚠️ Workflow completed with {total_steps - successful_steps} failures")
            self.notifications.notify(
                f"⚠️ Automation workflow completed with some issues\n\n"
                f"✅ Successful: {successful_steps}/{total_steps}\n"
                f"❌ Failed: {total_steps - successful_steps}/{total_steps}\n"
                f"⏱️ Duration: {duration:.1f} seconds\n\n"
                f"Check logs for details.",
                "WARNING",
                subject="⚠️ Automation Workflow Completed with Issues"
            )
        
        return overall_result
    
    def schedule_workflows(self):
        """Schedule automated workflows"""
        self.logger.info("📅 Setting up automated workflow schedules...")
        
        # Schedule LinkedIn checks
        schedule.every(self.workflow_config["linkedin_check_interval"]).minutes.do(
            lambda: self.run_scheduled_task("linkedin", self.test_linkedin_system)
        )
        
        # Schedule CV updates
        schedule.every(self.workflow_config["cv_update_interval"]).minutes.do(
            lambda: self.run_scheduled_task("cv", self.run_cv_generation)
        )
        
        # Schedule job searches
        schedule.every(self.workflow_config["job_search_interval"]).minutes.do(
            lambda: self.run_scheduled_task("job", self.run_job_application_workflow)
        )
        
        # Schedule email checks
        schedule.every(self.workflow_config["email_check_interval"]).minutes.do(
            lambda: self.run_scheduled_task("email", self.run_email_workflow)
        )
        
        self.logger.info("✅ Workflow schedules configured successfully!")
    
    def run_scheduled_task(self, task_name: str, task_function):
        """Run a scheduled task with error handling"""
        try:
            self.logger.info(f"🕐 Running scheduled task: {task_name}")
            result = task_function()
            
            if result.get("success"):
                self.logger.success(f"✅ Scheduled {task_name} completed successfully")
            else:
                self.logger.warning(f"⚠️ Scheduled {task_name} completed with issues")
                
        except Exception as e:
            self.logger.error(f"❌ Scheduled {task_name} failed: {str(e)}")
    
    def start_monitoring(self):
        """Start the automated monitoring system"""
        self.logger.info("🚀 Starting automated monitoring system...")
        
        # Send startup notification
        self.notifications.notify(
            "🚀 Your Personal Automation Hub is now running!\n\n"
            "I'll automatically:\n"
            "• Check LinkedIn for opportunities every 30 minutes\n"
            "• Update your CV every hour\n"
            "• Search for jobs every 45 minutes\n"
            "• Monitor emails every 15 minutes\n\n"
            "Sit back and let me handle your productivity! 🎯",
            "INFO",
            subject="🚀 Automation Hub is Now Active!"
        )
        
        # Schedule workflows
        self.schedule_workflows()
        
        # Run initial workflow
        self.logger.info("🔄 Running initial workflow...")
        initial_result = self.run_full_workflow()
        
        # Start monitoring loop
        self.logger.info("🔄 Starting monitoring loop...")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Monitoring stopped by user")
            self.notifications.notify(
                "🛑 Automation Hub monitoring has been stopped.\n"
                "To restart, run: python automation_hub.py",
                "INFO",
                subject="🛑 Automation Hub Stopped"
            )
        except Exception as e:
            self.logger.error(f"❌ Monitoring loop error: {str(e)}")
            self.notifications.notify(
                f"❌ Automation Hub encountered an error:\n{str(e)}\n\n"
                "Check logs for details and restart the hub.",
                "ERROR",
                subject="❌ Automation Hub Error"
            )
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get current status report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "hub_status": "running",
            "agent_status": self.agent_status,
            "workflow_config": self.workflow_config,
            "next_scheduled": [
                str(job.next_run) for job in schedule.jobs
            ]
        }

def main():
    """Main function to run the Automation Hub"""
    print("🚀 PERSONAL AUTOMATION HUB WITH ATS OPTIMIZATION")
    print("=" * 60)
    
    try:
        hub = AutomationHub()
        
        print("\n🎯 Available Workflows:")
        print("1. Full Automation Workflow (LinkedIn + CV + Jobs + Email)")
        print("2. Enhanced Job Application with ATS Optimization")
        print("3. ATS Optimization Workflow")
        print("4. Individual Component Testing")
        print("5. Start Automated Monitoring")
        
        choice = input("\nSelect workflow (1-5): ").strip()
        
        if choice == "1":
            print("\n🚀 Running Full Automation Workflow...")
            print("=" * 50)
            
            print("\n🎯 What I'll do automatically:")
            print(f"   • LinkedIn checks: Every {hub.workflow_config['linkedin_check_interval']} minutes")
            print(f"   • CV updates: Every {hub.workflow_config['cv_update_interval']} minutes")
            print(f"   • Job searches: Every {hub.workflow_config['job_search_interval']} minutes")
            print(f"   • Email monitoring: Every {hub.workflow_config['email_check_interval']} minutes")
            
            initial_result = hub.run_full_workflow()
            
            if initial_result["success"]:
                print("✅ Full workflow completed successfully!")
            else:
                print("⚠️ Full workflow completed with some issues")
        
        elif choice == "2":
            print("\n🎯 Running Enhanced Job Application with ATS Optimization...")
            print("=" * 60)
            
            result = hub.run_enhanced_job_application_workflow()
            
            if result["success"]:
                print(f"✅ Enhanced job application completed!")
                print(f"📊 Created {result['drafts_created']} ATS-optimized drafts")
                print(f"📈 Average ATS Score: {result['average_ats_score']:.1f}/100")
                print(f"🎯 Applications above threshold: {result['applications_above_threshold']}")
            else:
                print(f"❌ Enhanced job application failed: {result['error']}")
        
        elif choice == "3":
            print("\n🔧 Running ATS Optimization Workflow...")
            print("=" * 50)
            
            result = hub.run_ats_optimization_workflow()
            
            if result["success"]:
                print(f"✅ ATS optimization completed!")
                print(f"📊 ATS Score: {result['ats_score']}/100")
                print(f"🎯 Job: {result['job_title']} at {result['company']}")
                print(f"📁 Files created: {result['files_created']}")
                print(f"🔧 Recommendations: {result['recommendations_count']}")
                print(f"⚠️ Missing elements: {result['missing_elements_count']}")
            else:
                print(f"❌ ATS optimization failed: {result['error']}")
        
        elif choice == "4":
            print("\n🧪 Individual Component Testing...")
            print("=" * 40)
            
            # Test LinkedIn
            print("Testing LinkedIn Manager...")
            linkedin_result = hub.test_linkedin_system()
            print(f"LinkedIn: {'✅ Success' if linkedin_result['success'] else '❌ Failed'}")
            
            # Test CV Generation
            print("Testing CV Generator...")
            cv_result = hub.run_cv_generation()
            print(f"CV Generation: {'✅ Success' if cv_result['success'] else '❌ Failed'}")
            
            # Test Job Application
            print("Testing Job Application...")
            job_result = hub.run_job_application_workflow()
            print(f"Job Application: {'✅ Success' if job_result['success'] else '❌ Failed'}")
            
            # Test ATS Optimization
            print("Testing ATS Optimization...")
            ats_result = hub.run_ats_optimization_workflow()
            print(f"ATS Optimization: {'✅ Success' if ats_result['success'] else '❌ Failed'}")
        
        elif choice == "5":
            print("\n🔄 Starting Automated Monitoring...")
            print("=" * 40)
            
            print("\n🎯 What I'll do automatically:")
            print(f"   • LinkedIn checks: Every {hub.workflow_config['linkedin_check_interval']} minutes")
            print(f"   • CV updates: Every {hub.workflow_config['cv_update_interval']} minutes")
            print(f"   • Job searches: Every {hub.workflow_config['job_search_interval']} minutes")
            print(f"   • Email monitoring: Every {hub.workflow_config['email_check_interval']} minutes")
            
            print("\nPress Ctrl+C to stop monitoring")
            hub.start_monitoring()
        
        else:
            print("❌ Invalid choice. Please select 1-5.")
        
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
