#!/usr/bin/env python3
"""
Email Application Manager
Handles email-based job applications with Drive CV upload and portfolio sharing
"""

import os
import json
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

from utils.logger import AgentLogger
from agents.notion_manager import NotionManager
from agents.job_history_manager import JobHistoryManager
from agents.cv_manager import CVManager

class EmailApplicationManager:
    """Manages email-based job applications with Drive integration"""
    
    def __init__(self):
        self.logger = AgentLogger("email_application_manager")
        self.notion_manager = NotionManager()
        self.history_manager = JobHistoryManager()
        self.cv_manager = CVManager()
        
        # Email configuration
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        self.outlook_user = os.getenv('OUTLOOK_USER')
        self.outlook_password = os.getenv('OUTLOOK_PASSWORD')
        
        # Drive configuration
        self.drive_service = None
        self.default_drive_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID', 'root')
        
        # LinkedIn configuration
        self.linkedin_username = os.getenv('LINKEDIN_USERNAME')
        
        self.logger.info("Email Application Manager initialized")
    
    def _authenticate_drive(self) -> bool:
        """Authenticate with Google Drive API using client credentials"""
        try:
            # Get client credentials from environment or config
            client_id = os.getenv('GOOGLE_CLIENT_ID', '1016691344560-rmndu0na3casjhqqujt1cm8jsgf8b8t2.apps.googleusercontent.com')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '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')
            
            if not client_id or not client_secret:
                self.logger.error("Google client credentials not found in environment")
                return False
            
            SCOPES = [
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/drive.metadata'
            ]
            
            # Create credentials object directly
            from google.oauth2.credentials import Credentials
            
            # Check for existing token
            creds = None
            if os.path.exists('drive_token.pickle'):
                with open('drive_token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            
            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Use OAuth flow with your desktop app credentials
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'drive_credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials for next run
                with open('drive_token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
            self.drive_service = build('drive', 'v3', credentials=creds)
            self.logger.info("Google Drive authentication successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Drive authentication failed: {e}")
            return False
    
    def _create_job_folder(self, job_title: str, company: str, parent_folder_id: str = None) -> str:
        """Create organized folder structure for job applications"""
        try:
            # Create folder structure: Job Applications/Company/Job Title
            timestamp = datetime.now().strftime("%Y-%m")
            
            # Main folder: Job Applications
            main_folder_name = "Job Applications"
            main_folder_id = self._find_or_create_folder(main_folder_name, parent_folder_id or self.default_drive_folder_id)
            
            # Company folder: Company Name
            company_folder_name = f"{company} - {timestamp}"
            company_folder_id = self._find_or_create_folder(company_folder_name, main_folder_id)
            
            # Job folder: Job Title
            job_folder_name = f"{job_title} - {datetime.now().strftime('%Y%m%d')}"
            job_folder_id = self._find_or_create_folder(job_folder_name, company_folder_id)
            
            self.logger.info(f"Created folder structure: {main_folder_name}/{company_folder_name}/{job_folder_name}")
            return job_folder_id
            
        except Exception as e:
            self.logger.error(f"Failed to create job folder: {e}")
            return parent_folder_id or self.default_drive_folder_id
    
    def _find_or_create_folder(self, folder_name: str, parent_folder_id: str) -> str:
        """Find existing folder or create new one"""
        try:
            # Search for existing folder
            query = f"name='{folder_name}' and parents in '{parent_folder_id}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
            folders = results.get('files', [])
            
            if folders:
                # Folder exists, return its ID
                return folders[0]['id']
            else:
                # Create new folder
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parent_folder_id] if parent_folder_id != 'root' else None
                }
                folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
                self.logger.info(f"Created folder: {folder_name} (ID: {folder['id']})")
                return folder['id']
                
        except Exception as e:
            self.logger.error(f"Failed to find/create folder '{folder_name}': {e}")
            return parent_folder_id
    
    def upload_cv_to_drive(self, cv_file_path: str, job_title: str, company: str, folder_id: str = None) -> Optional[str]:
        """Upload CV to Google Drive and return shareable link"""
        try:
            if not self._authenticate_drive():
                return None
            
            # Create organized folder structure
            target_folder = self._create_job_folder(job_title, company, folder_id)
            
            # Create filename with job details
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"Abdallah_Nasr_Ali_CV_{job_title}_{company}_{timestamp}.pdf"
            
            # Upload file to Drive
            file_metadata = {
                'name': filename,
                'parents': [target_folder] if target_folder != 'root' else None
            }
            
            media = MediaFileUpload(cv_file_path, mimetype='application/pdf')
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()
            
            # Make file publicly viewable
            self.drive_service.permissions().create(
                fileId=file['id'],
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            
            drive_link = file['webViewLink']
            self.logger.info(f"CV uploaded to Drive: {drive_link}")
            return drive_link
            
        except Exception as e:
            self.logger.error(f"Failed to upload CV to Drive: {e}")
            return None
    
    def send_cv_email(self, job_info: Dict[str, Any], cv_file_path: str, 
                     portfolio_links: List[str] = None, test_email: str = None) -> bool:
        """Send CV via email (Gmail or Outlook)"""
        try:
            # Use test email if provided, otherwise use job email
            recipient_email = test_email or job_info.get('email', job_info.get('contact_email'))
            
            if not recipient_email:
                self.logger.error("No recipient email found")
                return False
            
            # Choose email service
            if self.gmail_user and self.gmail_password:
                return self._send_gmail(cv_file_path, job_info, portfolio_links, recipient_email)
            elif self.outlook_user and self.outlook_password:
                return self._send_outlook(cv_file_path, job_info, portfolio_links, recipient_email)
            else:
                self.logger.error("No email credentials configured")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send CV email: {e}")
            return False
    
    def _send_gmail(self, cv_file_path: str, job_info: Dict[str, Any], 
                   portfolio_links: List[str], recipient_email: str) -> bool:
        """Send CV via Gmail"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = recipient_email
            msg['Subject'] = f"Application for {job_info.get('title', 'Position')} - {job_info.get('company', 'Company')}"
            
            # Create email body
            body = self._create_email_body(job_info, portfolio_links)
            msg.attach(MIMEText(body, 'html'))
            
            # Attach CV
            with open(cv_file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= Abdallah_Nasr_Ali_CV.pdf'
            )
            msg.attach(part)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            text = msg.as_string()
            server.sendmail(self.gmail_user, recipient_email, text)
            server.quit()
            
            self.logger.info(f"CV sent via Gmail to {recipient_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Gmail send failed: {e}")
            return False
    
    def _send_outlook(self, cv_file_path: str, job_info: Dict[str, Any], 
                     portfolio_links: List[str], recipient_email: str) -> bool:
        """Send CV via Outlook"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.outlook_user
            msg['To'] = recipient_email
            msg['Subject'] = f"Application for {job_info.get('title', 'Position')} - {job_info.get('company', 'Company')}"
            
            # Create email body
            body = self._create_email_body(job_info, portfolio_links)
            msg.attach(MIMEText(body, 'html'))
            
            # Attach CV
            with open(cv_file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= Abdallah_Nasr_Ali_CV.pdf'
            )
            msg.attach(part)
            
            # Send email
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(self.outlook_user, self.outlook_password)
            text = msg.as_string()
            server.sendmail(self.outlook_user, recipient_email, text)
            server.quit()
            
            self.logger.info(f"CV sent via Outlook to {recipient_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Outlook send failed: {e}")
            return False
    
    def _create_email_body(self, job_info: Dict[str, Any], portfolio_links: List[str] = None) -> str:
        """Create professional email body"""
        company = job_info.get('company', 'Company')
        position = job_info.get('title', 'Position')
        
        portfolio_section = ""
        if portfolio_links:
            portfolio_section = f"""
            <h3>Portfolio & Projects:</h3>
            <ul>
            """
            for link in portfolio_links:
                portfolio_section += f"<li><a href='{link}'>{link}</a></li>"
            portfolio_section += "</ul>"
        
        body = f"""
        <html>
        <body>
            <h2>Job Application - {position}</h2>
            
            <p>Dear Hiring Manager,</p>
            
            <p>I am writing to express my interest in the {position} position at {company}. 
            I am a junior full-stack developer with experience in modern web technologies 
            and a passion for creating innovative solutions.</p>
            
            <h3>About Me:</h3>
            <ul>
                <li>Junior Full Stack Developer with hands-on experience in React, Node.js, and modern web technologies</li>
                <li>Strong foundation in HTML, CSS, JavaScript, and responsive design</li>
                <li>Experience with version control (Git) and collaborative development</li>
                <li>Passionate about learning new technologies and solving complex problems</li>
                <li>Excellent communication skills and team collaboration experience</li>
            </ul>
            
            {portfolio_section}
            
            <h3>Why I'm a Great Fit:</h3>
            <ul>
                <li>Entry-level enthusiasm with a strong foundation in modern web development</li>
                <li>Quick learner with a passion for technology and innovation</li>
                <li>Strong problem-solving skills and attention to detail</li>
                <li>Excellent communication skills and team collaboration experience</li>
                <li>Committed to continuous learning and professional growth</li>
            </ul>
            
            <p>I have attached my CV for your review. I would welcome the opportunity to 
            discuss how my skills and enthusiasm can contribute to your team.</p>
            
            <p>Thank you for considering my application. I look forward to hearing from you.</p>
            
            <p>Best regards,<br>
            Abdallah Nasr Ali<br>
            Junior Full Stack Developer<br>
            Email: abdallah.nasr.ali@example.com<br>
            Phone: +20 123 456 7890</p>
        </body>
        </html>
        """
        return body
    
    def create_email_application_package(self, job_info: Dict[str, Any], 
                                       portfolio_links: List[str] = None,
                                       test_email: str = None) -> Dict[str, Any]:
        """Create complete email application package"""
        try:
            self.logger.info(f"Creating email application package for: {job_info.get('title', 'Position')}")
            
            # Check CV access permissions
            access_result = self.cv_manager.request_cv_access("Email Application", job_info)
            
            if not access_result.get("approved", False):
                self.logger.warning("CV access not approved. Waiting for user approval.")
                return {
                    "error": "CV access not approved",
                    "message": access_result.get("message", "Waiting for approval"),
                    "requires_approval": True,
                    "access_result": access_result
                }
            
            # Generate CV
            from agents.ats_cv_generator import ATSCVGenerator
            cv_generator = ATSCVGenerator()
            cv_result = cv_generator.generate_job_specific_cv(job_info)
            
            if not cv_result.get('success', False):
                return {"error": "CV generation failed", "details": cv_result.get('error')}
            
            # Get CV file path
            cv_files = cv_result.get('saved_files', {})
            cv_file_path = cv_files.get('pdf_file')
            
            if not cv_file_path or not os.path.exists(cv_file_path):
                return {"error": "CV file not found"}
            
            # Upload CV to Drive
            drive_link = self.upload_cv_to_drive(
                cv_file_path, 
                job_info.get('title', 'Position'),
                job_info.get('company', 'Company')
            )
            
            # Send email
            email_sent = self.send_cv_email(job_info, cv_file_path, portfolio_links, test_email)
            
            # Prepare package
            package = {
                "success": True,
                "application_type": "email",
                "job_info": job_info,
                "cv_result": cv_result,
                "drive_link": drive_link,
                "email_sent": email_sent,
                "portfolio_links": portfolio_links,
                "saved_files": cv_files,
                "timestamp": datetime.now().isoformat()
            }
            
            # Track in Notion
            notion_page_id = self.notion_manager.create_job_application_entry(
                job_info, cv_files, "Email Applied"
            )
            if notion_page_id:
                package["notion_page_id"] = notion_page_id
            
            # Track in local history
            application_id = self.history_manager.add_application(
                job_info, cv_files, "Email Applied", notion_page_id
            )
            if application_id:
                package["application_id"] = application_id
            
            self.logger.info("Email application package created successfully")
            return package
            
        except Exception as e:
            self.logger.error(f"Failed to create email application package: {e}")
            return {"error": str(e)}
    
    def comment_on_linkedin_post(self, post_url: str, drive_cv_link: str, 
                               portfolio_links: List[str] = None) -> bool:
        """Comment on LinkedIn post with Drive CV link"""
        try:
            # This would require LinkedIn API integration
            # For now, we'll create the comment text
            comment_text = f"#interested\n\nHi! I'm a junior full-stack developer interested in this opportunity. "
            
            if drive_cv_link:
                comment_text += f"Here's my CV: {drive_cv_link}\n\n"
            
            if portfolio_links:
                comment_text += "Portfolio links:\n"
                for link in portfolio_links:
                    comment_text += f"• {link}\n"
            
            comment_text += "\nI'd love to discuss how I can contribute to your team!"
            
            self.logger.info(f"LinkedIn comment prepared: {comment_text}")
            # In a real implementation, you would use LinkedIn API here
            
            return True
            
        except Exception as e:
            self.logger.error(f"LinkedIn comment failed: {e}")
            return False
    
    def get_portfolio_links(self) -> List[str]:
        """Get portfolio project links"""
        return [
            "https://github.com/abdallah-nasr-ali/project1",
            "https://abdallah-nasr-ali.github.io/project1-demo",
            "https://github.com/abdallah-nasr-ali/project2", 
            "https://abdallah-nasr-ali.github.io/project2-demo",
            "https://github.com/abdallah-nasr-ali/project3",
            "https://abdallah-nasr-ali.github.io/project3-demo"
        ]

def main():
    """Test the email application manager"""
    print("📧 EMAIL APPLICATION MANAGER TEST")
    print("=" * 35)
    
    manager = EmailApplicationManager()
    
    # Test job info
    test_job = {
        "title": "Junior Full Stack Developer",
        "company": "Tech Startup",
        "email": "hr@techstartup.com",
        "description": "Looking for a junior developer with React and Node.js experience"
    }
    
    # Test portfolio links
    portfolio_links = manager.get_portfolio_links()
    
    print("📝 Creating email application package...")
    package = manager.create_email_application_package(test_job, portfolio_links)
    
    if package.get("success"):
        print("✅ Email application package created successfully!")
        print(f"   • Drive Link: {package.get('drive_link', 'Not uploaded')}")
        print(f"   • Email Sent: {package.get('email_sent', False)}")
        print(f"   • Portfolio Links: {len(package.get('portfolio_links', []))}")
    else:
        print(f"❌ Failed: {package.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
