#!/usr/bin/env python3
"""
Job Application Agent Demo - Shows the concept without complex web scraping
Input: Job search criteria
Process: Create sample job drafts, AI enhancement
Output: Application drafts with approval notifications
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import AgentLogger
from utils.notifications import NotificationManager
from config import Config
from openai import OpenAI
from dotenv import load_dotenv

class JobApplicationDemoAgent:
    def __init__(self):
        """Initialize the Job Application Demo Agent"""
        load_dotenv('config.env')
        
        self.logger = AgentLogger("job_application_demo")
        self.notifications = NotificationManager("job_application_demo")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Sample job postings for demo
        self.sample_jobs = [
            {
                "title": "Full Stack Developer",
                "company": "TechCorp Egypt",
                "location": "Cairo, Egypt",
                "source": "LinkedIn",
                "url": "https://linkedin.com/jobs/view/123456",
                "description": "We are looking for a Full Stack Developer with experience in React, Node.js, and MongoDB."
            },
            {
                "title": "Frontend Developer",
                "company": "Digital Solutions",
                "location": "Cairo, Egypt", 
                "source": "Indeed",
                "url": "https://indeed.com/jobs/view/789012",
                "description": "Frontend Developer needed for Angular and React projects."
            },
            {
                "title": "React Developer",
                "company": "Innovation Labs",
                "location": "Remote",
                "source": "Glassdoor",
                "url": "https://glassdoor.com/jobs/view/345678",
                "description": "Remote React Developer position with modern tech stack."
            }
        ]
        
        self.logger.info("Job Application Demo Agent initialized successfully")

    def create_application_draft(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Create an application draft for a specific job"""
        self.logger.info(f"Creating application draft for: {job['title']} at {job['company']}")
        
        try:
            # Generate cover letter using AI
            cover_letter = self._generate_cover_letter(job)
            
            # Create application draft
            application_draft = {
                "job_id": f"{job['source']}_{job['company']}_{job['title']}".replace(" ", "_"),
                "job_title": job['title'],
                "company": job['company'],
                "location": job['location'],
                "source": job['source'],
                "job_url": job['url'],
                "job_description": job['description'],
                "cover_letter": cover_letter,
                "cv_version": self._select_cv_version(job),
                "status": "draft",
                "created_at": datetime.now().isoformat(),
                "requires_approval": True
            }
            
            self.logger.info(f"Application draft created successfully for {job['company']}")
            return application_draft
            
        except Exception as e:
            self.logger.error(f"Error creating application draft: {e}")
            return None

    def _generate_cover_letter(self, job: Dict[str, Any]) -> str:
        """Generate a cover letter using OpenAI"""
        try:
            prompt = f"""
            Write a professional cover letter for the following job:
            
            Job Title: {job['title']}
            Company: {job['company']}
            Location: {job['location']}
            Description: {job['description']}
            
            The candidate is Abdallah Nasr Ali, a full-stack developer with:
            - Full Stack Web Development Diploma from Route Academy
            - Experience with Angular, React, Next.js, Node.js
            - Skills in JavaScript, TypeScript, MongoDB, and modern web technologies
            - Portfolio at https://my-v3-potfolio.vercel.app
            - GitHub at https://github.com/AbdalahNasr
            
            Write a compelling, professional cover letter that:
            1. Shows enthusiasm for the role
            2. Highlights relevant skills and experience
            3. Explains why they're a good fit
            4. Is concise (max 300 words)
            5. Ends with a call to action
            
            Make it specific to the job title and company.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional cover letter writer. Write compelling, personalized cover letters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            cover_letter = response.choices[0].message.content.strip()
            self.logger.info("Cover letter generated successfully using AI")
            return cover_letter
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter with AI: {e}")
            # Fallback to template
            return self._generate_fallback_cover_letter(job)

    def _generate_fallback_cover_letter(self, job: Dict[str, Any]) -> str:
        """Generate a fallback cover letter template"""
        return f"""
Dear Hiring Manager,

I am writing to express my interest in the {job['title']} position at {job['company']}. With my background in full-stack web development and experience with modern technologies, I believe I would be a valuable addition to your team.

My experience includes building responsive web applications using Angular, React, and Node.js, along with expertise in JavaScript, TypeScript, and database technologies. I have successfully delivered projects including e-commerce platforms, social media applications, and real-time messaging systems.

I am particularly drawn to {job['company']} because of the opportunity to work on innovative projects and contribute to a dynamic team. I am excited about the possibility of joining your organization and would welcome the chance to discuss how my skills and experience align with your needs.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
Abdallah Nasr Ali
        """.strip()

    def _select_cv_version(self, job: Dict[str, Any]) -> str:
        """Select the appropriate CV version for the job"""
        job_title_lower = job['title'].lower()
        
        if any(keyword in job_title_lower for keyword in ['senior', 'lead', 'manager', 'architect']):
            return "professional"
        elif any(keyword in job_title_lower for keyword in ['junior', 'entry', 'intern']):
            return "concise"
        else:
            return "ats"

    def save_application_draft(self, draft: Dict[str, Any]) -> str:
        """Save application draft to file"""
        try:
            # Create drafts folder if it doesn't exist
            drafts_folder = "job_application_drafts"
            if not os.path.exists(drafts_folder):
                os.makedirs(drafts_folder)
            
            # Create timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{draft['job_id']}_{timestamp}.json"
            filepath = os.path.join(drafts_folder, filename)
            
            # Save draft
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(draft, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Application draft saved to: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving application draft: {e}")
            return None

    def send_approval_notification(self, draft: Dict[str, Any]) -> None:
        """Send notification for application approval"""
        subject = f"Job Application Draft Ready - {draft['job_title']} at {draft['company']}"
        
        message = f"""
        A new job application draft has been created and requires your approval:
        
        Job: {draft['job_title']}
        Company: {draft['company']}
        Location: {draft['location']}
        Source: {draft['source']}
        
        The draft includes:
        - AI-generated cover letter
        - Recommended CV version: {draft['cv_version']}
        - Job details and application link
        
        Please review the draft and approve/reject the application.
        The draft has been saved and can be found in the job_application_drafts folder.
        
        Job URL: {draft['job_url']}
        """
        
        # Send notification
        self.notifications.notify(message, "INFO", subject=subject)
        self.logger.info(f"Approval notification sent for {draft['company']}")

    def run_demo(self) -> List[Dict[str, Any]]:
        """Run the demo job application process"""
        self.logger.info("Starting demo job application process")
        
        try:
            drafts = []
            
            # Create application drafts for sample jobs
            for job in self.sample_jobs:
                draft = self.create_application_draft(job)
                if draft:
                    # Save draft
                    filepath = self.save_application_draft(draft)
                    if filepath:
                        draft['filepath'] = filepath
                        drafts.append(draft)
                        
                        # Send approval notification
                        self.send_approval_notification(draft)
            
            self.logger.info(f"Created {len(drafts)} application drafts")
            return drafts
            
        except Exception as e:
            self.logger.error(f"Error in demo process: {e}")
            return []

def main():
    """Main function to run the job application demo agent"""
    agent = JobApplicationDemoAgent()
    
    # Run demo
    drafts = agent.run_demo()
    
    if drafts:
        print(f"\n🎉 Job Application Demo Agent completed successfully!")
        print(f"📝 Created {len(drafts)} application drafts")
        print(f"📁 Drafts saved in: job_application_drafts/")
        print(f"📧 Check your email for approval notifications")
        
        for draft in drafts:
            print(f"\n📋 Draft: {draft['job_title']} at {draft['company']}")
            print(f"   Status: {draft['status']}")
            print(f"   CV Version: {draft['cv_version']}")
            print(f"   File: {draft['filepath']}")
            print(f"   Cover Letter Preview: {draft['cover_letter'][:100]}...")
    else:
        print("\n❌ No application drafts created")

if __name__ == "__main__":
    main()
