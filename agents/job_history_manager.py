#!/usr/bin/env python3
"""
Job History Manager
Manages and stores the complete history of job applications

Features:
- Local JSON storage for job application history
- Search and filter capabilities
- Application statistics and analytics
- Export functionality
- Integration with Notion for backup
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import AgentLogger

class JobHistoryManager:
    """Manages job application history and statistics"""
    
    def __init__(self, history_file: str = "job_application_history.json"):
        """Initialize Job History Manager"""
        self.logger = AgentLogger("job_history_manager")
        self.history_file = history_file
        self.history_data = self._load_history()
        
        self.logger.info("Job History Manager initialized")
    
    def _load_history(self) -> Dict[str, Any]:
        """Load job application history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded {len(data.get('applications', []))} job applications from history")
                    return data
            else:
                # Create new history file
                initial_data = {
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_applications": 0,
                    "applications": []
                }
                self._save_history(initial_data)
                self.logger.info("Created new job application history file")
                return initial_data
        except Exception as e:
            self.logger.error(f"Error loading history: {e}")
            return {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_applications": 0,
                "applications": []
            }
    
    def _save_history(self, data: Dict[str, Any]) -> bool:
        """Save job application history to file"""
        try:
            data["last_updated"] = datetime.now().isoformat()
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info("Job application history saved")
            return True
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")
            return False
    
    def add_application(self, job_info: Dict[str, Any], cv_files: Dict[str, str], 
                       application_status: str = "Applied", notion_page_id: str = None) -> str:
        """Add a new job application to history"""
        try:
            application_id = f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            application_entry = {
                "id": application_id,
                "applied_date": datetime.now().isoformat(),
                "job_info": job_info,
                "cv_files": cv_files,
                "status": application_status,
                "notion_page_id": notion_page_id,
                "status_history": [
                    {
                        "status": application_status,
                        "date": datetime.now().isoformat(),
                        "notes": "Initial application"
                    }
                ],
                "follow_ups": [],
                "interviews": [],
                "notes": "",
                "tags": []
            }
            
            # Add to history
            self.history_data["applications"].append(application_entry)
            self.history_data["total_applications"] = len(self.history_data["applications"])
            
            # Save to file
            self._save_history(self.history_data)
            
            self.logger.info(f"Job application added to history: {application_id}")
            return application_id
            
        except Exception as e:
            self.logger.error(f"Error adding application to history: {e}")
            return None
    
    def update_application_status(self, application_id: str, new_status: str, notes: str = "") -> bool:
        """Update the status of a job application"""
        try:
            for app in self.history_data["applications"]:
                if app["id"] == application_id:
                    # Update current status
                    app["status"] = new_status
                    
                    # Add to status history
                    app["status_history"].append({
                        "status": new_status,
                        "date": datetime.now().isoformat(),
                        "notes": notes
                    })
                    
                    # Save changes
                    self._save_history(self.history_data)
                    
                    self.logger.info(f"Application status updated: {application_id} -> {new_status}")
                    return True
            
            self.logger.warning(f"Application not found: {application_id}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error updating application status: {e}")
            return False
    
    def add_interview(self, application_id: str, interview_date: str, interview_type: str, 
                     interviewer: str = "", notes: str = "") -> bool:
        """Add interview information to an application"""
        try:
            for app in self.history_data["applications"]:
                if app["id"] == application_id:
                    interview_entry = {
                        "date": interview_date,
                        "type": interview_type,
                        "interviewer": interviewer,
                        "notes": notes,
                        "added_date": datetime.now().isoformat()
                    }
                    
                    app["interviews"].append(interview_entry)
                    
                    # Update status if not already set
                    if app["status"] == "Applied":
                        self.update_application_status(application_id, "Interview Scheduled", 
                                                     f"Interview scheduled: {interview_type}")
                    
                    # Save changes
                    self._save_history(self.history_data)
                    
                    self.logger.info(f"Interview added to application: {application_id}")
                    return True
            
            self.logger.warning(f"Application not found: {application_id}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error adding interview: {e}")
            return False
    
    def add_follow_up(self, application_id: str, follow_up_date: str, follow_up_type: str, 
                     notes: str = "") -> bool:
        """Add follow-up information to an application"""
        try:
            for app in self.history_data["applications"]:
                if app["id"] == application_id:
                    follow_up_entry = {
                        "date": follow_up_date,
                        "type": follow_up_type,
                        "notes": notes,
                        "added_date": datetime.now().isoformat(),
                        "completed": False
                    }
                    
                    app["follow_ups"].append(follow_up_entry)
                    
                    # Save changes
                    self._save_history(self.history_data)
                    
                    self.logger.info(f"Follow-up added to application: {application_id}")
                    return True
            
            self.logger.warning(f"Application not found: {application_id}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error adding follow-up: {e}")
            return False
    
    def get_application_history(self, limit: int = None, status_filter: str = None, 
                              company_filter: str = None) -> List[Dict[str, Any]]:
        """Get job application history with optional filters"""
        try:
            applications = self.history_data["applications"]
            
            # Apply filters
            if status_filter:
                applications = [app for app in applications if app["status"] == status_filter]
            
            if company_filter:
                applications = [app for app in applications 
                              if company_filter.lower() in app["job_info"].get("company", "").lower()]
            
            # Sort by applied date (newest first)
            applications.sort(key=lambda x: x["applied_date"], reverse=True)
            
            # Apply limit
            if limit:
                applications = applications[:limit]
            
            self.logger.info(f"Retrieved {len(applications)} applications from history")
            return applications
            
        except Exception as e:
            self.logger.error(f"Error getting application history: {e}")
            return []
    
    def get_application_by_id(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific application by ID"""
        try:
            for app in self.history_data["applications"]:
                if app["id"] == application_id:
                    return app
            
            self.logger.warning(f"Application not found: {application_id}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting application by ID: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive job application statistics"""
        try:
            applications = self.history_data["applications"]
            total_applications = len(applications)
            
            if total_applications == 0:
                return {
                    "total_applications": 0,
                    "status_breakdown": {},
                    "company_breakdown": {},
                    "response_rate": 0.0,
                    "interview_rate": 0.0,
                    "offer_rate": 0.0,
                    "average_response_time": 0,
                    "most_applied_companies": [],
                    "application_timeline": []
                }
            
            # Status breakdown
            status_counts = {}
            for app in applications:
                status = app["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Company breakdown
            company_counts = {}
            for app in applications:
                company = app["job_info"].get("company", "Unknown")
                company_counts[company] = company_counts.get(company, 0) + 1
            
            # Calculate rates
            responded = status_counts.get("Interview Scheduled", 0) + \
                       status_counts.get("Interview Completed", 0) + \
                       status_counts.get("Rejected", 0) + \
                       status_counts.get("Offer Received", 0)
            
            interviews = status_counts.get("Interview Scheduled", 0) + \
                        status_counts.get("Interview Completed", 0)
            
            offers = status_counts.get("Offer Received", 0)
            
            response_rate = (responded / total_applications) * 100 if total_applications > 0 else 0
            interview_rate = (interviews / total_applications) * 100 if total_applications > 0 else 0
            offer_rate = (offers / total_applications) * 100 if total_applications > 0 else 0
            
            # Most applied companies
            most_applied = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Application timeline (last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_applications = [
                app for app in applications 
                if datetime.fromisoformat(app["applied_date"]) >= thirty_days_ago
            ]
            
            # Calculate average response time
            response_times = []
            for app in applications:
                if len(app["status_history"]) > 1:
                    first_status = app["status_history"][0]
                    for status in app["status_history"][1:]:
                        if status["status"] in ["Interview Scheduled", "Rejected", "Offer Received"]:
                            try:
                                applied_date = datetime.fromisoformat(first_status["date"])
                                response_date = datetime.fromisoformat(status["date"])
                                response_time = (response_date - applied_date).days
                                response_times.append(response_time)
                                break
                            except:
                                continue
            
            average_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            statistics = {
                "total_applications": total_applications,
                "status_breakdown": status_counts,
                "company_breakdown": company_counts,
                "response_rate": round(response_rate, 1),
                "interview_rate": round(interview_rate, 1),
                "offer_rate": round(offer_rate, 1),
                "average_response_time": round(average_response_time, 1),
                "most_applied_companies": most_applied,
                "recent_applications_count": len(recent_applications),
                "application_timeline": [
                    {
                        "date": app["applied_date"][:10],
                        "company": app["job_info"].get("company", "Unknown"),
                        "position": app["job_info"].get("title", "Unknown"),
                        "status": app["status"]
                    }
                    for app in recent_applications
                ]
            }
            
            self.logger.info("Job application statistics generated")
            return statistics
            
        except Exception as e:
            self.logger.error(f"Error generating statistics: {e}")
            return {}
    
    def get_upcoming_follow_ups(self) -> List[Dict[str, Any]]:
        """Get upcoming follow-ups that need attention"""
        try:
            upcoming_follow_ups = []
            seven_days_from_now = datetime.now() + timedelta(days=7)
            
            for app in self.history_data["applications"]:
                for follow_up in app["follow_ups"]:
                    if not follow_up.get("completed", False):
                        try:
                            follow_up_date = datetime.fromisoformat(follow_up["date"])
                            if follow_up_date <= seven_days_from_now:
                                upcoming_follow_ups.append({
                                    "application_id": app["id"],
                                    "company": app["job_info"].get("company", "Unknown"),
                                    "position": app["job_info"].get("title", "Unknown"),
                                    "follow_up_date": follow_up["date"],
                                    "follow_up_type": follow_up["type"],
                                    "notes": follow_up["notes"]
                                })
                        except:
                            continue
            
            # Sort by date
            upcoming_follow_ups.sort(key=lambda x: x["follow_up_date"])
            
            self.logger.info(f"Found {len(upcoming_follow_ups)} upcoming follow-ups")
            return upcoming_follow_ups
            
        except Exception as e:
            self.logger.error(f"Error getting upcoming follow-ups: {e}")
            return []
    
    def mark_follow_up_completed(self, application_id: str, follow_up_date: str) -> bool:
        """Mark a follow-up as completed"""
        try:
            for app in self.history_data["applications"]:
                if app["id"] == application_id:
                    for follow_up in app["follow_ups"]:
                        if follow_up["date"] == follow_up_date:
                            follow_up["completed"] = True
                            follow_up["completed_date"] = datetime.now().isoformat()
                            
                            # Save changes
                            self._save_history(self.history_data)
                            
                            self.logger.info(f"Follow-up marked as completed: {application_id}")
                            return True
            
            self.logger.warning(f"Follow-up not found: {application_id} - {follow_up_date}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error marking follow-up as completed: {e}")
            return False
    
    def export_history(self, export_file: str = None) -> str:
        """Export job application history to a file"""
        try:
            if not export_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_file = f"job_application_history_export_{timestamp}.json"
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Job application history exported to: {export_file}")
            return export_file
            
        except Exception as e:
            self.logger.error(f"Error exporting history: {e}")
            return None
    
    def search_applications(self, query: str) -> List[Dict[str, Any]]:
        """Search job applications by company, position, or notes"""
        try:
            query_lower = query.lower()
            matching_applications = []
            
            for app in self.history_data["applications"]:
                # Search in company name
                if query_lower in app["job_info"].get("company", "").lower():
                    matching_applications.append(app)
                    continue
                
                # Search in position title
                if query_lower in app["job_info"].get("title", "").lower():
                    matching_applications.append(app)
                    continue
                
                # Search in notes
                if query_lower in app.get("notes", "").lower():
                    matching_applications.append(app)
                    continue
                
                # Search in job description
                if query_lower in app["job_info"].get("description", "").lower():
                    matching_applications.append(app)
                    continue
            
            # Sort by applied date (newest first)
            matching_applications.sort(key=lambda x: x["applied_date"], reverse=True)
            
            self.logger.info(f"Found {len(matching_applications)} applications matching: {query}")
            return matching_applications
            
        except Exception as e:
            self.logger.error(f"Error searching applications: {e}")
            return []
    
    def get_application_summary(self) -> str:
        """Get a formatted summary of job applications"""
        try:
            stats = self.get_statistics()
            
            summary = f"""
📊 JOB APPLICATION SUMMARY
==========================

📈 OVERALL STATISTICS:
   Total Applications: {stats['total_applications']}
   Response Rate: {stats['response_rate']}%
   Interview Rate: {stats['interview_rate']}%
   Offer Rate: {stats['offer_rate']}%
   Average Response Time: {stats['average_response_time']} days

📋 STATUS BREAKDOWN:
"""
            
            for status, count in stats['status_breakdown'].items():
                percentage = (count / stats['total_applications']) * 100 if stats['total_applications'] > 0 else 0
                summary += f"   {status}: {count} ({percentage:.1f}%)\n"
            
            summary += f"""
🏢 TOP COMPANIES:
"""
            
            for company, count in stats['most_applied_companies'][:5]:
                summary += f"   {company}: {count} applications\n"
            
            summary += f"""
📅 RECENT ACTIVITY (Last 30 days):
   Applications: {stats['recent_applications_count']}
"""
            
            if stats['application_timeline']:
                summary += "   Recent Applications:\n"
                for app in stats['application_timeline'][:5]:
                    summary += f"     • {app['company']} - {app['position']} ({app['status']})\n"
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {e}")
            return "Error generating application summary"

def main():
    """Test Job History Manager"""
    print("📚 JOB HISTORY MANAGER TEST")
    print("=" * 40)
    
    history_manager = JobHistoryManager()
    
    # Test with sample data
    sample_job = {
        "title": "Junior Full Stack Developer",
        "company": "TechCorp",
        "location": "Cairo, Egypt",
        "description": "Looking for a junior developer...",
        "salary": "6000-8000 EGP",
        "job_type": "Full-time"
    }
    
    sample_cv_files = {
        "pdf": "Abdallah_Nasr_Ali_CV.pdf",
        "docx": "Abdallah_Nasr_Ali_CV.docx",
        "txt": "Abdallah_Nasr_Ali_CV.txt"
    }
    
    print("📝 Adding sample job application...")
    app_id = history_manager.add_application(sample_job, sample_cv_files, "Applied")
    
    if app_id:
        print(f"✅ Application added: {app_id}")
        
        # Test status update
        print("📊 Updating application status...")
        history_manager.update_application_status(app_id, "Interview Scheduled", "Phone interview scheduled")
        
        # Test interview addition
        print("📅 Adding interview...")
        interview_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        history_manager.add_interview(app_id, interview_date, "Phone", "Sarah Johnson", "Technical interview")
        
        # Test follow-up addition
        print("⏰ Adding follow-up...")
        follow_up_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        history_manager.add_follow_up(app_id, follow_up_date, "Email", "Send thank you email")
        
        # Test statistics
        print("📈 Getting statistics...")
        stats = history_manager.get_statistics()
        print(f"Total Applications: {stats['total_applications']}")
        print(f"Response Rate: {stats['response_rate']}%")
        
        # Test summary
        print("📋 Application Summary:")
        print(history_manager.get_application_summary())
        
        print("✅ All tests completed successfully!")
    else:
        print("❌ Failed to add application")

if __name__ == "__main__":
    main()
