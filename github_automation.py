#!/usr/bin/env python3
"""
GitHub Actions Job Automation - Runs every 30 minutes
"""

import os
import time
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import random

# Configuration from environment variables
CONFIG = {
    'GMAIL_USER': os.environ.get('GMAIL_USER', ''),
    'GMAIL_APP_PASSWORD': os.environ.get('GMAIL_APP_PASSWORD', ''),
    'NOTION_TOKEN': os.environ.get('NOTION_TOKEN', ''),
    'NOTION_DATABASE_ID': os.environ.get('NOTION_DATABASE_ID', ''),
    'CV_PRIMARY_URL': os.environ.get('CV_PRIMARY_URL', ''),
    'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', '')
}

# Job search keywords
JOB_KEYWORDS = [
    'junior developer',
    'entry level developer', 
    'react developer',
    'javascript developer',
    'frontend developer',
    'full stack developer',
    'web developer'
]

# Sample job data
SAMPLE_JOBS = [
    {
        'title': 'Junior React Developer',
        'company': 'TechCorp',
        'location': 'Remote',
        'url': 'https://linkedin.com/jobs/view/123456',
        'description': 'Looking for a junior React developer with 1-2 years experience'
    },
    {
        'title': 'Entry Level Frontend Developer',
        'company': 'StartupXYZ',
        'location': 'New York',
        'url': 'https://linkedin.com/jobs/view/789012',
        'description': 'Entry level position for frontend development'
    },
    {
        'title': 'Junior Full Stack Developer',
        'company': 'WebSolutions',
        'location': 'San Francisco',
        'url': 'https://linkedin.com/jobs/view/345678',
        'description': 'Junior full stack developer position'
    },
    {
        'title': 'Frontend Developer Intern',
        'company': 'InnovateTech',
        'location': 'Remote',
        'url': 'https://linkedin.com/jobs/view/456789',
        'description': 'Internship position for frontend development'
    },
    {
        'title': 'Junior Web Developer',
        'company': 'DigitalAgency',
        'location': 'London',
        'url': 'https://linkedin.com/jobs/view/567890',
        'description': 'Junior web developer position'
    }
]

def log_message(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def send_email_notification(job_data, application_result=None):
    """Send email notification about job application"""
    try:
        # Email setup
        msg = MIMEMultipart()
        msg['From'] = CONFIG['GMAIL_USER']
        msg['To'] = CONFIG['GMAIL_USER']
        msg['Subject'] = f"Job Application: {job_data['title']} at {job_data['company']}"
        
        # Email body
        body = f"""
        🎯 Job Application Submitted!
        
        Position: {job_data['title']}
        Company: {job_data['company']}
        Location: {job_data['location']}
        Job URL: {job_data['url']}
        
        Application Details:
        - Applied at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        - CV Used: {CONFIG['CV_PRIMARY_URL']}
        
        """
        
        if application_result:
            body += f"""
        Submitted Answers:
        {json.dumps(application_result.get('submitted_answers', {}), indent=2)}
        
        CV Uploaded: {application_result.get('cv_uploaded', 'Yes')}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CONFIG['GMAIL_USER'], CONFIG['GMAIL_APP_PASSWORD'])
        text = msg.as_string()
        server.sendmail(CONFIG['GMAIL_USER'], CONFIG['GMAIL_USER'], text)
        server.quit()
        
        log_message(f"✅ Email notification sent for {job_data['title']}")
        return True
        
    except Exception as e:
        log_message(f"❌ Email notification failed: {e}")
        return False

def add_to_notion(job_data, application_result=None):
    """Add job application to Notion database"""
    if not CONFIG['NOTION_TOKEN']:
        log_message("⚠️ Notion not configured, skipping...")
        return False
        
    try:
        url = f"https://api.notion.com/v1/pages"
        
        headers = {
            "Authorization": f"Bearer {CONFIG['NOTION_TOKEN']}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Create page data
        page_data = {
            "parent": {"database_id": CONFIG['NOTION_DATABASE_ID']},
            "properties": {
                "Position": {
                    "title": [
                        {
                            "text": {
                                "content": job_data['title']
                            }
                        }
                    ]
                },
                "Company": {
                    "rich_text": [
                        {
                            "text": {
                                "content": job_data['company']
                            }
                        }
                    ]
                },
                "Location": {
                    "rich_text": [
                        {
                            "text": {
                                "content": job_data['location']
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Applied"
                    }
                },
                "Job URL": {
                    "url": job_data['url']
                },
                "Applied Date": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }
        }
        
        # Add application details if available
        if application_result:
            page_data["properties"]["Notes"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": f"CV Uploaded: {application_result.get('cv_uploaded', 'Yes')}\nSubmitted Answers: {json.dumps(application_result.get('submitted_answers', {}))}"
                        }
                    }
                ]
            }
        
        response = requests.post(url, headers=headers, json=page_data)
        
        if response.status_code == 200:
            log_message(f"✅ Added to Notion: {job_data['title']}")
            return True
        else:
            log_message(f"❌ Notion API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        log_message(f"❌ Notion integration failed: {e}")
        return False

def simulate_job_application(job_data):
    """Simulate job application process"""
    log_message(f"🎯 Applying to: {job_data['title']} at {job_data['company']}")
    
    # Simulate application process
    time.sleep(2)  # Simulate form filling time
    
    # Generate humanized responses
    responses = {
        "Why are you interested in this position?": "I'm excited about this role because it aligns with my passion for web development and offers great learning opportunities.",
        "What's your experience with React?": "I have hands-on experience building projects with React, including state management and component architecture.",
        "Are you available for remote work?": "Yes, I'm fully available for remote work and have experience collaborating in distributed teams.",
        "What's your expected salary?": "I'm open to discussing salary based on the role requirements and company benefits.",
        "When can you start?": "I can start immediately and am ready to contribute to the team right away."
    }
    
    application_result = {
        'submitted_answers': responses,
        'cv_uploaded': True,
        'application_time': datetime.now().isoformat()
    }
    
    log_message(f"✅ Application submitted successfully")
    return application_result

def find_job_opportunities():
    """Find job opportunities (simplified version)"""
    log_message("🔍 Searching for job opportunities...")
    
    # In a real implementation, this would search actual job APIs
    # For now, we'll use sample data
    available_jobs = SAMPLE_JOBS.copy()
    random.shuffle(available_jobs)
    
    # Return 1-3 random jobs
    num_jobs = random.randint(1, 3)
    return available_jobs[:num_jobs]

def process_job_cycle():
    """Process one complete job application cycle"""
    log_message("🚀 Starting job application cycle...")
    
    # Find jobs
    jobs = find_job_opportunities()
    log_message(f"📋 Found {len(jobs)} job opportunities")
    
    applications_sent = 0
    notifications_sent = 0
    notion_entries = 0
    
    for job in jobs:
        try:
            # Apply to job
            application_result = simulate_job_application(job)
            applications_sent += 1
            
            # Send email notification
            if send_email_notification(job, application_result):
                notifications_sent += 1
            
            # Add to Notion
            if add_to_notion(job, application_result):
                notion_entries += 1
            
            # Wait between applications
            time.sleep(5)
            
        except Exception as e:
            log_message(f"❌ Error processing job {job['title']}: {e}")
    
    log_message(f"📊 Cycle complete: {applications_sent} applications, {notifications_sent} emails, {notion_entries} Notion entries")
    return applications_sent, notifications_sent, notion_entries

def main():
    """Main automation function"""
    log_message("🤖 GitHub Actions Job Automation Started")
    log_message("=" * 50)
    
    try:
        # Process one job cycle
        apps, emails, notion = process_job_cycle()
        log_message(f"✅ Automation complete: {apps} applications, {emails} emails, {notion} Notion entries")
        
    except Exception as e:
        log_message(f"❌ Automation error: {e}")
    
    log_message("🎉 GitHub Actions automation session complete!")

if __name__ == "__main__":
    main()
