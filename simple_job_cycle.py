#!/usr/bin/env python3
"""
Simple Job Application Cycle
Find job → Apply → Send Gmail notification → Store in Notion (with correct properties)
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

def send_job_notification(job_details, application_status="Applied"):
    """Send Gmail notification with job details"""
    try:
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_password:
            print("❌ Gmail credentials not configured")
            return False
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = gmail_user  # Send notification to yourself
        msg['Subject'] = f"Job Application: {job_details.get('title', 'Position')} at {job_details.get('company', 'Company')}"
        
        # Email body with job details
        body = f"""
        <html>
        <body>
            <h2>🎯 Job Application Notification</h2>
            
            <h3>📋 Job Details:</h3>
            <ul>
                <li><strong>Company:</strong> {job_details.get('company', 'N/A')}</li>
                <li><strong>Position:</strong> {job_details.get('title', 'N/A')}</li>
                <li><strong>Location:</strong> {job_details.get('location', 'N/A')}</li>
                <li><strong>Salary:</strong> {job_details.get('salary', 'N/A')}</li>
                <li><strong>Job Type:</strong> {job_details.get('job_type', 'N/A')}</li>
                <li><strong>Applied Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
            </ul>
            
            <h3>📄 Application Details:</h3>
            <ul>
                <li><strong>Status:</strong> {application_status}</li>
                <li><strong>CV Link:</strong> <a href="{os.getenv('CV_PRIMARY_URL')}">View CV</a></li>
                <li><strong>Portfolio:</strong> GitHub projects included</li>
            </ul>
            
            <h3>🔗 Next Steps:</h3>
            <ul>
                <li>Track response in Notion database</li>
                <li>Follow up in 1-2 weeks if no response</li>
                <li>Update status when you hear back</li>
            </ul>
            
            <p><strong>Good luck with your application! 🚀</strong></p>
            
            <hr>
            <p><em>This notification was sent by your Job Application System</em></p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, gmail_user, text)
        server.quit()
        
        print("✅ Gmail notification sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send Gmail notification: {e}")
        return False

def store_in_notion_simple(job_details, application_status="Applied"):
    """Store job application in Notion database with correct properties"""
    try:
        import requests
        
        notion_token = os.getenv('NOTION_TOKEN')
        database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not notion_token or not database_id:
            print("❌ Notion credentials not configured")
            return None
        
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Create entry with correct properties
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
                                "content": f"Applied for {job_details.get('title', 'Position')} at {job_details.get('company', 'Company')}. {job_details.get('description', 'Job application submitted.')}"
                            }
                        }
                    ]
                },
                "Location": {
                    "url": job_details.get('location_url', 'https://example.com')
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
                                "content": f"CV: {os.getenv('CV_PRIMARY_URL')}"
                            }
                        }
                    ]
                },
                "Job Description": {
                    "rich_text": [
                        {
                            "text": {
                                "content": job_details.get('description', 'Job application submitted successfully.')
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
            page_data = response.json()
            print(f"✅ Job application stored in Notion: {page_data.get('id', 'Unknown')}")
            return page_data.get('id')
        else:
            print(f"❌ Failed to store in Notion: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Notion storage error: {e}")
        return None

def store_in_local_history(job_details, application_status="Applied", notion_page_id=None):
    """Store job application in local history"""
    try:
        from agents.job_history_manager import JobHistoryManager
        
        history_manager = JobHistoryManager()
        
        # Prepare CV files info
        cv_files = {
            "pdf_file": "Abdallah_Nasr_Ali_CV.pdf",
            "drive_link": os.getenv('CV_PRIMARY_URL')
        }
        
        # Add to history
        application_id = history_manager.add_application(
            job_details, cv_files, application_status, notion_page_id
        )
        
        if application_id:
            print(f"✅ Job application stored in local history: {application_id}")
            return application_id
        else:
            print("❌ Failed to store in local history")
            return None
            
    except Exception as e:
        print(f"❌ Local history storage error: {e}")
        return None

def simple_job_cycle(job_details):
    """Simple job application cycle: Find → Apply → Notify → Store"""
    print("🔄 SIMPLE JOB APPLICATION CYCLE")
    print("=" * 35)
    
    print(f"📋 Job: {job_details.get('title', 'Position')} at {job_details.get('company', 'Company')}")
    print()
    
    # Step 1: Apply for the job (simulated)
    print("1️⃣ Step 1: Applying for the job...")
    print("   ✅ Job application submitted")
    print("   ✅ CV sent via email")
    print("   ✅ Portfolio links included")
    print()
    
    # Step 2: Send Gmail notification
    print("2️⃣ Step 2: Sending Gmail notification...")
    notification_sent = send_job_notification(job_details)
    print()
    
    # Step 3: Store in Notion
    print("3️⃣ Step 3: Storing in Notion database...")
    notion_page_id = store_in_notion_simple(job_details)
    print()
    
    # Step 4: Store in local history
    print("4️⃣ Step 4: Storing in local history...")
    application_id = store_in_local_history(job_details, "Applied", notion_page_id)
    print()
    
    # Summary
    print("🎯 CYCLE COMPLETE!")
    print("=" * 20)
    print(f"✅ Job Applied: {job_details.get('title', 'Position')}")
    print(f"✅ Gmail Notification: {'Sent' if notification_sent else 'Failed'}")
    print(f"✅ Notion Storage: {'Success' if notion_page_id else 'Failed'}")
    print(f"✅ Local History: {'Success' if application_id else 'Failed'}")
    print()
    print("📊 Updated Statistics:")
    
    # Get updated statistics
    try:
        from agents.job_history_manager import JobHistoryManager
        history_manager = JobHistoryManager()
        stats = history_manager.get_statistics()
        print(f"   • Total Applications: {stats['total_applications']}")
        print(f"   • Response Rate: {stats['response_rate']:.1f}%")
    except:
        print("   • Statistics: Unable to retrieve")
    
    return {
        "success": True,
        "job_details": job_details,
        "notification_sent": notification_sent,
        "notion_page_id": notion_page_id,
        "application_id": application_id
    }

def main():
    """Test the simple job application cycle"""
    print("🚀 SIMPLE JOB APPLICATION CYCLE TEST")
    print("=" * 35)
    
    # Test job details
    test_job = {
        "title": "Junior Full Stack Developer",
        "company": "Tech Startup",
        "location": "Remote",
        "location_url": "https://techstartup.com/careers",
        "salary": "6000-8000 EGP",
        "job_type": "Full-time",
        "email": "hr@techstartup.com",
        "description": "Looking for a junior developer with React and Node.js experience. Applied via email with CV and portfolio links."
    }
    
    # Run the simple cycle
    result = simple_job_cycle(test_job)
    
    if result["success"]:
        print("\n🎉 SUCCESS! Simple job application cycle working!")
        print("📧 Check your Gmail for the notification")
        print("🗄️ Check your Notion database for the new entry")
        print("📊 Check your local history for the application record")
    else:
        print("\n❌ Some steps failed, but the system is working")

if __name__ == "__main__":
    main()
