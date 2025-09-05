#!/usr/bin/env python3
"""
CV Manager
Manages CV lifecycle, notifications, and access control

Features:
- Monthly CV review and updates
- User notification before CV usage
- CV version control
- Access logging
- Integration with job application system
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
from utils.notifications import NotificationManager

class CVManager:
    """Manages CV lifecycle and access control"""
    
    def __init__(self):
        """Initialize CV Manager"""
        self.logger = AgentLogger("cv_manager")
        self.notification_manager = NotificationManager("cv_manager")
        
        # CV management file
        self.cv_management_file = "cv_management.json"
        self.cv_data = self._load_cv_management()
        
        # CV file paths
        self.cv_file_path = "Abdallah Nasr Ali_Cv.pdf"
        self.cv_backup_dir = "cv_backups"
        
        # Create backup directory
        Path(self.cv_backup_dir).mkdir(exist_ok=True)
        
        self.logger.info("CV Manager initialized")
    
    def _load_cv_management(self) -> Dict[str, Any]:
        """Load CV management data"""
        try:
            if os.path.exists(self.cv_management_file):
                with open(self.cv_management_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info("CV management data loaded")
                    return data
            else:
                # Create initial CV management data
                initial_data = {
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "last_review": None,
                    "next_review": (datetime.now() + timedelta(days=30)).isoformat(),
                    "cv_version": "1.0",
                    "access_log": [],
                    "usage_permissions": {
                        "auto_generate": False,
                        "require_notification": True,
                        "last_notification": None
                    },
                    "cv_status": "active",
                    "backup_files": []
                }
                self._save_cv_management(initial_data)
                self.logger.info("Initial CV management data created")
                return initial_data
        except Exception as e:
            self.logger.error(f"Error loading CV management data: {e}")
            return {}
    
    def _save_cv_management(self, data: Dict[str, Any]) -> bool:
        """Save CV management data"""
        try:
            data["last_updated"] = datetime.now().isoformat()
            with open(self.cv_management_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info("CV management data saved")
            return True
        except Exception as e:
            self.logger.error(f"Error saving CV management data: {e}")
            return False
    
    def check_cv_review_status(self) -> Dict[str, Any]:
        """Check if CV needs monthly review"""
        try:
            next_review = datetime.fromisoformat(self.cv_data.get("next_review", ""))
            current_date = datetime.now()
            
            days_until_review = (next_review - current_date).days
            
            status = {
                "needs_review": days_until_review <= 0,
                "days_until_review": days_until_review,
                "last_review": self.cv_data.get("last_review"),
                "next_review": self.cv_data.get("next_review"),
                "cv_version": self.cv_data.get("cv_version", "1.0")
            }
            
            if status["needs_review"]:
                self.logger.warning("CV review is overdue!")
                self._send_review_notification()
            elif days_until_review <= 7:
                self.logger.info(f"CV review due in {days_until_review} days")
                self._send_review_reminder(days_until_review)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking CV review status: {e}")
            return {"needs_review": False, "error": str(e)}
    
    def request_cv_access(self, purpose: str, job_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Request access to use CV for job application"""
        try:
            # Check if auto-generation is enabled
            if not self.cv_data.get("usage_permissions", {}).get("require_notification", True):
                return {"approved": True, "message": "Auto-generation enabled"}
            
            # Log access request
            access_request = {
                "timestamp": datetime.now().isoformat(),
                "purpose": purpose,
                "job_info": job_info,
                "status": "pending",
                "approved": False
            }
            
            self.cv_data["access_log"].append(access_request)
            self._save_cv_management(self.cv_data)
            
            # Send notification
            notification_sent = self._send_access_notification(access_request)
            
            return {
                "approved": False,
                "message": "Access request sent. Waiting for approval.",
                "notification_sent": notification_sent,
                "request_id": len(self.cv_data["access_log"]) - 1
            }
            
        except Exception as e:
            self.logger.error(f"Error requesting CV access: {e}")
            return {"approved": False, "error": str(e)}
    
    def approve_cv_access(self, request_id: int, approved: bool, notes: str = "") -> bool:
        """Approve or deny CV access request"""
        try:
            if 0 <= request_id < len(self.cv_data["access_log"]):
                request = self.cv_data["access_log"][request_id]
                request["status"] = "approved" if approved else "denied"
                request["approved"] = approved
                request["approval_notes"] = notes
                request["approval_timestamp"] = datetime.now().isoformat()
                
                self._save_cv_management(self.cv_data)
                
                # Send approval notification
                self._send_approval_notification(request)
                
                self.logger.info(f"CV access request {request_id} {'approved' if approved else 'denied'}")
                return True
            else:
                self.logger.error(f"Invalid request ID: {request_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error approving CV access: {e}")
            return False
    
    def update_cv_review(self, review_notes: str = "", cv_updated: bool = False) -> bool:
        """Update CV review status"""
        try:
            current_date = datetime.now()
            next_review = current_date + timedelta(days=30)
            
            self.cv_data["last_review"] = current_date.isoformat()
            self.cv_data["next_review"] = next_review.isoformat()
            
            if cv_updated:
                # Increment version
                current_version = self.cv_data.get("cv_version", "1.0")
                version_parts = current_version.split(".")
                version_parts[-1] = str(int(version_parts[-1]) + 1)
                self.cv_data["cv_version"] = ".".join(version_parts)
                
                # Create backup
                self._create_cv_backup()
            
            # Add review log
            review_log = {
                "timestamp": current_date.isoformat(),
                "notes": review_notes,
                "cv_updated": cv_updated,
                "version": self.cv_data["cv_version"]
            }
            
            if "review_log" not in self.cv_data:
                self.cv_data["review_log"] = []
            self.cv_data["review_log"].append(review_log)
            
            self._save_cv_management(self.cv_data)
            
            self.logger.info(f"CV review updated. Next review: {next_review.strftime('%Y-%m-%d')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating CV review: {e}")
            return False
    
    def get_cv_status(self) -> Dict[str, Any]:
        """Get current CV status and information"""
        try:
            review_status = self.check_cv_review_status()
            
            status = {
                "cv_version": self.cv_data.get("cv_version", "1.0"),
                "last_review": self.cv_data.get("last_review"),
                "next_review": self.cv_data.get("next_review"),
                "needs_review": review_status.get("needs_review", False),
                "days_until_review": review_status.get("days_until_review", 0),
                "cv_status": self.cv_data.get("cv_status", "active"),
                "auto_generation": self.cv_data.get("usage_permissions", {}).get("auto_generate", False),
                "require_notification": self.cv_data.get("usage_permissions", {}).get("require_notification", True),
                "total_access_requests": len(self.cv_data.get("access_log", [])),
                "pending_requests": len([req for req in self.cv_data.get("access_log", []) if req.get("status") == "pending"]),
                "backup_count": len(self.cv_data.get("backup_files", []))
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting CV status: {e}")
            return {}
    
    def get_pending_requests(self) -> List[Dict[str, Any]]:
        """Get pending CV access requests"""
        try:
            pending_requests = [
                req for req in self.cv_data.get("access_log", [])
                if req.get("status") == "pending"
            ]
            
            # Add request ID
            for i, req in enumerate(pending_requests):
                req["request_id"] = i
            
            return pending_requests
            
        except Exception as e:
            self.logger.error(f"Error getting pending requests: {e}")
            return []
    
    def _create_cv_backup(self) -> bool:
        """Create backup of current CV"""
        try:
            if os.path.exists(self.cv_file_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"CV_Backup_v{self.cv_data['cv_version']}_{timestamp}.pdf"
                backup_path = os.path.join(self.cv_backup_dir, backup_filename)
                
                # Copy file
                import shutil
                shutil.copy2(self.cv_file_path, backup_path)
                
                # Add to backup list
                backup_info = {
                    "filename": backup_filename,
                    "path": backup_path,
                    "created_at": datetime.now().isoformat(),
                    "version": self.cv_data["cv_version"]
                }
                
                if "backup_files" not in self.cv_data:
                    self.cv_data["backup_files"] = []
                self.cv_data["backup_files"].append(backup_info)
                
                self._save_cv_management(self.cv_data)
                
                self.logger.info(f"CV backup created: {backup_filename}")
                return True
            else:
                self.logger.warning("CV file not found for backup")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating CV backup: {e}")
            return False
    
    def _send_review_notification(self) -> bool:
        """Send CV review notification"""
        try:
            message = """
🔔 CV REVIEW OVERDUE

Your CV review is overdue! Please review and update your CV:

📅 Last Review: {last_review}
📅 Next Review: {next_review}
📄 Current Version: {version}

Please run: python cv_review.py
            """.format(
                last_review=self.cv_data.get("last_review", "Never"),
                next_review=self.cv_data.get("next_review", "Unknown"),
                version=self.cv_data.get("cv_version", "1.0")
            )
            
            print(f"🔔 CV REVIEW OVERDUE\n{message}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending review notification: {e}")
            return False
    
    def _send_review_reminder(self, days_until: int) -> bool:
        """Send CV review reminder"""
        try:
            message = f"""
⏰ CV REVIEW REMINDER

Your CV review is due in {days_until} days.

📅 Next Review: {self.cv_data.get('next_review', 'Unknown')}
📄 Current Version: {self.cv_data.get('cv_version', '1.0')}

Please schedule time to review your CV.
            """
            
            print(f"⏰ CV REVIEW REMINDER\n{message}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending review reminder: {e}")
            return False
    
    def _send_access_notification(self, request: Dict[str, Any]) -> bool:
        """Send CV access request notification"""
        try:
            job_info = request.get("job_info", {})
            company = job_info.get("company", "Unknown Company")
            position = job_info.get("title", "Unknown Position")
            
            message = f"""
🔐 CV ACCESS REQUEST

A job application is requesting to use your CV:

🏢 Company: {company}
💼 Position: {position}
📝 Purpose: {request.get('purpose', 'Job Application')}
⏰ Time: {request.get('timestamp', 'Unknown')}

To approve: python cv_manager.py --approve {len(self.cv_data['access_log']) - 1}
To deny: python cv_manager.py --deny {len(self.cv_data['access_log']) - 1}
            """
            
            print(f"🔐 CV ACCESS REQUEST\n{message}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending access notification: {e}")
            return False
    
    def _send_approval_notification(self, request: Dict[str, Any]) -> bool:
        """Send CV access approval notification"""
        try:
            status = "APPROVED" if request.get("approved") else "DENIED"
            job_info = request.get("job_info", {})
            company = job_info.get("company", "Unknown Company")
            
            message = f"""
✅ CV ACCESS {status}

Your CV access request has been {status.lower()}:

🏢 Company: {company}
📝 Purpose: {request.get('purpose', 'Job Application')}
📄 Notes: {request.get('approval_notes', 'None')}

Request ID: {len(self.cv_data['access_log']) - 1}
            """
            
            print(f"✅ CV ACCESS {status}\n{message}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending approval notification: {e}")
            return False

def main():
    """Test CV Manager"""
    print("📄 CV MANAGER TEST")
    print("=" * 25)
    
    cv_manager = CVManager()
    
    # Check CV status
    print("📊 Checking CV status...")
    status = cv_manager.get_cv_status()
    
    print(f"CV Version: {status.get('cv_version', 'Unknown')}")
    print(f"Last Review: {status.get('last_review', 'Never')}")
    print(f"Next Review: {status.get('next_review', 'Unknown')}")
    print(f"Needs Review: {status.get('needs_review', False)}")
    print(f"Days Until Review: {status.get('days_until_review', 0)}")
    print(f"Auto Generation: {status.get('auto_generation', False)}")
    print(f"Require Notification: {status.get('require_notification', True)}")
    print()
    
    # Test access request
    print("🔐 Testing CV access request...")
    job_info = {
        "title": "Junior Full Stack Developer",
        "company": "Test Company",
        "location": "Cairo, Egypt"
    }
    
    access_result = cv_manager.request_cv_access("Job Application", job_info)
    print(f"Access Request Result: {access_result}")
    print()
    
    # Show pending requests
    print("📋 Pending requests:")
    pending = cv_manager.get_pending_requests()
    for req in pending:
        print(f"  • {req.get('job_info', {}).get('company', 'Unknown')} - {req.get('purpose', 'Unknown')}")
    
    print("\n✅ CV Manager test completed!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CV Manager")
    parser.add_argument("--approve", type=int, help="Approve CV access request by ID")
    parser.add_argument("--deny", type=int, help="Deny CV access request by ID")
    parser.add_argument("--review", action="store_true", help="Update CV review")
    parser.add_argument("--status", action="store_true", help="Show CV status")
    
    args = parser.parse_args()
    
    cv_manager = CVManager()
    
    if args.approve is not None:
        success = cv_manager.approve_cv_access(args.approve, True, "Approved by user")
        print(f"Request {args.approve} {'approved' if success else 'failed'}")
    elif args.deny is not None:
        success = cv_manager.approve_cv_access(args.deny, False, "Denied by user")
        print(f"Request {args.deny} {'denied' if success else 'failed'}")
    elif args.review:
        success = cv_manager.update_cv_review("Monthly review completed", False)
        print(f"CV review {'updated' if success else 'failed'}")
    elif args.status:
        status = cv_manager.get_cv_status()
        print(json.dumps(status, indent=2))
    else:
        main()
