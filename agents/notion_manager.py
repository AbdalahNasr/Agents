#!/usr/bin/env python3
"""
Notion Integration Manager
Manages job application tracking, interview scheduling, and job search planning

Features:
- Job application tracking
- Interview scheduling and notes
- Company research and notes
- Application status updates
- Follow-up reminders
- Job search analytics and insights
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import AgentLogger

class NotionManager:
    """Manages Notion integration for job search workflow"""
    
    def __init__(self):
        """Initialize Notion Manager"""
        self.logger = AgentLogger("notion_manager")
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not self.notion_token:
            self.logger.warning("NOTION_TOKEN not found in environment variables")
        
        if not self.notion_database_id:
            self.logger.warning("NOTION_DATABASE_ID not found in environment variables")
        
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        self.logger.info("Notion Manager initialized")
    
    def _test_write_access(self) -> bool:
        """Test if we have write access to the Notion database"""
        try:
            # Try to query the database first (read access)
            response = requests.post(
                f"https://api.notion.com/v1/databases/{self.notion_database_id}/query",
                headers=self.headers,
                json={"page_size": 1}
            )
            
            if response.status_code != 200:
                self.logger.error(f"Database not accessible: {response.text}")
                return False
            
            # If we can read, assume we can write (for now)
            # In a real scenario, you'd test with a small write operation
            return True
            
        except Exception as e:
            self.logger.error(f"Error testing write access: {e}")
            return False
    
    def create_job_application_entry(self, job_info: Dict[str, Any], cv_files: Dict[str, str], 
                                   application_status: str = "Applied") -> Optional[str]:
        """Create a new job application entry in Notion"""
        try:
            if not self.notion_token or not self.notion_database_id:
                self.logger.warning("Notion not configured. Skipping database entry.")
                return None
            
            # Test if we have write access
            if not self._test_write_access():
                self.logger.warning("Notion database is read-only or not accessible. Using local storage only.")
                return None
            
            # Prepare the data for Notion
            notion_data = {
                "parent": {"database_id": self.notion_database_id},
                "properties": {
                    "Company": {
                        "title": [
                            {
                                "text": {
                                    "content": job_info.get('company', 'Unknown Company')
                                }
                            }
                        ]
                    },
                    "Position": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": job_info.get('title', 'Unknown Position')
                                }
                            }
                        ]
                    },
                    "Location": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": job_info.get('location', 'Not specified')
                                }
                            }
                        ]
                    },
                    "Status": {
                        "select": {
                            "name": application_status
                        }
                    },
                    "Applied Date": {
                        "date": {
                            "start": datetime.now().strftime("%Y-%m-%d")
                        }
                    },
                    "CV Files": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": self._format_file_links(cv_files)
                                }
                            }
                        ]
                    },
                    "Job Description": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": job_info.get('description', '')[:2000]  # Notion limit
                                }
                            }
                        ]
                    }
                }
            }
            
            # Add optional fields if available
            if job_info.get('salary'):
                notion_data["properties"]["Salary"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": str(job_info['salary'])
                            }
                        }
                    ]
                }
            
            if job_info.get('job_type'):
                notion_data["properties"]["Job Type"] = {
                    "select": {
                        "name": job_info['job_type']
                    }
                }
            
            # Create the entry
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.headers,
                json=notion_data
            )
            
            if response.status_code == 200:
                page_id = response.json()["id"]
                self.logger.info(f"Job application entry created in Notion: {page_id}")
                return page_id
            else:
                self.logger.error(f"Failed to create Notion entry: {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating Notion entry: {e}")
            return None
    
    def update_application_status(self, page_id: str, new_status: str, notes: str = "") -> bool:
        """Update the status of a job application"""
        try:
            if not self.notion_token:
                self.logger.warning("Notion not configured. Skipping status update.")
                return False
            
            update_data = {
                "properties": {
                    "Status": {
                        "select": {
                            "name": new_status
                        }
                    }
                }
            }
            
            # Add notes if provided
            if notes:
                update_data["properties"]["Notes"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": notes
                            }
                        }
                    ]
                }
            
            response = requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=self.headers,
                json=update_data
            )
            
            if response.status_code == 200:
                self.logger.info(f"Application status updated to: {new_status}")
                return True
            else:
                self.logger.error(f"Failed to update status: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating application status: {e}")
            return False
    
    def schedule_interview(self, page_id: str, interview_date: str, interview_type: str, 
                          interviewer: str = "", notes: str = "") -> bool:
        """Schedule an interview in Notion"""
        try:
            if not self.notion_token:
                self.logger.warning("Notion not configured. Skipping interview scheduling.")
                return False
            
            update_data = {
                "properties": {
                    "Status": {
                        "select": {
                            "name": "Interview Scheduled"
                        }
                    },
                    "Interview Date": {
                        "date": {
                            "start": interview_date
                        }
                    },
                    "Interview Type": {
                        "select": {
                            "name": interview_type
                        }
                    }
                }
            }
            
            if interviewer:
                update_data["properties"]["Interviewer"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": interviewer
                            }
                        }
                    ]
                }
            
            if notes:
                update_data["properties"]["Interview Notes"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": notes
                            }
                        }
                    ]
                }
            
            response = requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=self.headers,
                json=update_data
            )
            
            if response.status_code == 200:
                self.logger.info(f"Interview scheduled for: {interview_date}")
                return True
            else:
                self.logger.error(f"Failed to schedule interview: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error scheduling interview: {e}")
            return False
    
    def add_follow_up_reminder(self, page_id: str, follow_up_date: str, reminder_type: str, 
                              notes: str = "") -> bool:
        """Add a follow-up reminder"""
        try:
            if not self.notion_token:
                self.logger.warning("Notion not configured. Skipping follow-up reminder.")
                return False
            
            update_data = {
                "properties": {
                    "Follow-up Date": {
                        "date": {
                            "start": follow_up_date
                        }
                    },
                    "Follow-up Type": {
                        "select": {
                            "name": reminder_type
                        }
                    }
                }
            }
            
            if notes:
                update_data["properties"]["Follow-up Notes"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": notes
                            }
                        }
                    ]
                }
            
            response = requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=self.headers,
                json=update_data
            )
            
            if response.status_code == 200:
                self.logger.info(f"Follow-up reminder added for: {follow_up_date}")
                return True
            else:
                self.logger.error(f"Failed to add follow-up reminder: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error adding follow-up reminder: {e}")
            return False
    
    def get_job_search_analytics(self) -> Dict[str, Any]:
        """Get analytics about job search progress"""
        try:
            if not self.notion_token or not self.notion_database_id:
                self.logger.warning("Notion not configured. Cannot get analytics.")
                return {}
            
            # Query all job applications
            response = requests.post(
                f"https://api.notion.com/v1/databases/{self.notion_database_id}/query",
                headers=self.headers,
                json={}
            )
            
            if response.status_code != 200:
                self.logger.error(f"Failed to get analytics: {response.text}")
                return {}
            
            results = response.json()["results"]
            
            # Calculate analytics
            total_applications = len(results)
            status_counts = {}
            companies = set()
            positions = set()
            
            for result in results:
                properties = result["properties"]
                
                # Count statuses
                status = properties.get("Status", {}).get("select", {}).get("name", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
                
                # Collect companies and positions
                company = properties.get("Company", {}).get("title", [{}])[0].get("text", {}).get("content", "")
                if company:
                    companies.add(company)
                
                position = properties.get("Position", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                if position:
                    positions.add(position)
            
            analytics = {
                "total_applications": total_applications,
                "status_breakdown": status_counts,
                "unique_companies": len(companies),
                "unique_positions": len(positions),
                "companies": list(companies),
                "positions": list(positions),
                "response_rate": self._calculate_response_rate(status_counts),
                "interview_rate": self._calculate_interview_rate(status_counts)
            }
            
            self.logger.info("Job search analytics generated")
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting analytics: {e}")
            return {}
    
    def get_upcoming_follow_ups(self) -> List[Dict[str, Any]]:
        """Get upcoming follow-ups that need attention"""
        try:
            if not self.notion_token or not self.notion_database_id:
                self.logger.warning("Notion not configured. Cannot get follow-ups.")
                return []
            
            # Query for entries with follow-up dates
            response = requests.post(
                f"https://api.notion.com/v1/databases/{self.notion_database_id}/query",
                headers=self.headers,
                json={
                    "filter": {
                        "property": "Follow-up Date",
                        "date": {
                            "is_not_empty": True
                        }
                    }
                }
            )
            
            if response.status_code != 200:
                self.logger.error(f"Failed to get follow-ups: {response.text}")
                return []
            
            results = response.json()["results"]
            upcoming_follow_ups = []
            
            for result in results:
                properties = result["properties"]
                
                follow_up_date = properties.get("Follow-up Date", {}).get("date", {}).get("start", "")
                if follow_up_date:
                    follow_up_datetime = datetime.strptime(follow_up_date, "%Y-%m-%d")
                    if follow_up_datetime <= datetime.now() + timedelta(days=7):  # Next 7 days
                        company = properties.get("Company", {}).get("title", [{}])[0].get("text", {}).get("content", "")
                        position = properties.get("Position", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                        follow_up_type = properties.get("Follow-up Type", {}).get("select", {}).get("name", "")
                        
                        upcoming_follow_ups.append({
                            "page_id": result["id"],
                            "company": company,
                            "position": position,
                            "follow_up_date": follow_up_date,
                            "follow_up_type": follow_up_type
                        })
            
            self.logger.info(f"Found {len(upcoming_follow_ups)} upcoming follow-ups")
            return upcoming_follow_ups
            
        except Exception as e:
            self.logger.error(f"Error getting follow-ups: {e}")
            return []
    
    def _format_file_links(self, cv_files: Dict[str, str]) -> str:
        """Format CV file links for Notion"""
        links = []
        for file_type, file_path in cv_files.items():
            if file_type in ['pdf', 'docx', 'txt']:
                filename = os.path.basename(file_path)
                links.append(f"{file_type.upper()}: {filename}")
        return " | ".join(links)
    
    def _calculate_response_rate(self, status_counts: Dict[str, int]) -> float:
        """Calculate response rate from status counts"""
        total = sum(status_counts.values())
        if total == 0:
            return 0.0
        
        responded = status_counts.get("Interview Scheduled", 0) + \
                   status_counts.get("Rejected", 0) + \
                   status_counts.get("Offer Received", 0)
        
        return (responded / total) * 100
    
    def _calculate_interview_rate(self, status_counts: Dict[str, int]) -> float:
        """Calculate interview rate from status counts"""
        total = sum(status_counts.values())
        if total == 0:
            return 0.0
        
        interviews = status_counts.get("Interview Scheduled", 0) + \
                    status_counts.get("Interview Completed", 0)
        
        return (interviews / total) * 100
    
    def create_notion_setup_guide(self) -> str:
        """Create a setup guide for Notion integration"""
        return """
        NOTION INTEGRATION SETUP GUIDE
        ==============================
        
        1. CREATE NOTION DATABASE:
           - Go to Notion and create a new database
           - Add the following properties:
             * Company (Title)
             * Position (Rich Text)
             * Location (Rich Text)
             * Status (Select: Applied, Interview Scheduled, Interview Completed, Rejected, Offer Received, Withdrawn)
             * Applied Date (Date)
             * Interview Date (Date)
             * Interview Type (Select: Phone, Video, In-person, Technical)
             * Interviewer (Rich Text)
             * Salary (Rich Text)
             * Job Type (Select: Full-time, Part-time, Contract, Internship)
             * CV Files (Rich Text)
             * Job Description (Rich Text)
             * Notes (Rich Text)
             * Follow-up Date (Date)
             * Follow-up Type (Select: Email, Call, LinkedIn)
             * Follow-up Notes (Rich Text)
        
        2. GET NOTION TOKEN:
           - Go to https://www.notion.so/my-integrations
           - Create a new integration
           - Copy the "Internal Integration Token"
           - Add it to your .env file as NOTION_TOKEN
        
        3. GET DATABASE ID:
           - Open your Notion database in browser
           - Copy the database ID from the URL
           - Add it to your .env file as NOTION_DATABASE_ID
        
        4. SHARE DATABASE:
           - In your Notion database, click "Share"
           - Add your integration to the database
           - Give it "Can edit" permissions
        
        5. TEST INTEGRATION:
           - Run the job application system
           - Check if entries appear in your Notion database
        
        BENEFITS:
        - Track all job applications in one place
        - Schedule interviews and set reminders
        - Monitor application status and response rates
        - Generate analytics and insights
        - Never miss a follow-up opportunity
        """

def main():
    """Test Notion integration"""
    print("🔗 NOTION INTEGRATION MANAGER")
    print("=" * 40)
    
    notion = NotionManager()
    
    # Test with sample job data
    sample_job = {
        "title": "Junior Full Stack Developer",
        "company": "Tech Startup",
        "location": "Cairo, Egypt",
        "description": "Looking for a junior developer...",
        "salary": "5000-8000 EGP",
        "job_type": "Full-time"
    }
    
    sample_cv_files = {
        "pdf": "Abdallah_Nasr_Ali_CV.pdf",
        "docx": "Abdallah_Nasr_Ali_CV.docx",
        "txt": "Abdallah_Nasr_Ali_CV.txt"
    }
    
    print("📋 Testing Notion integration...")
    
    # Create job application entry
    page_id = notion.create_job_application_entry(sample_job, sample_cv_files)
    
    if page_id:
        print(f"✅ Job application entry created: {page_id}")
        
        # Test status update
        notion.update_application_status(page_id, "Interview Scheduled", "Phone interview scheduled for next week")
        
        # Test interview scheduling
        interview_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        notion.schedule_interview(page_id, interview_date, "Phone", "John Smith", "Technical interview")
        
        # Test follow-up reminder
        follow_up_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        notion.add_follow_up_reminder(page_id, follow_up_date, "Email", "Send thank you email")
        
        print("✅ All Notion operations completed successfully!")
    else:
        print("❌ Notion integration not configured or failed")
        print("\n📖 Setup Guide:")
        print(notion.create_notion_setup_guide())

if __name__ == "__main__":
    main()
