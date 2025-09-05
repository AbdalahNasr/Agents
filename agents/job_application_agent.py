#!/usr/bin/env python3
"""
Job Application Agent - Scrapes job postings and creates application drafts
Input: Job search criteria
Process: Scrape jobs, create drafts, AI enhancement
Output: Application drafts with approval notifications
"""

import os
import json
import time
import re
from datetime import datetime
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import AgentLogger
from utils.notifications import NotificationManager
from config import Config

class JobApplicationAgent:
    def __init__(self):
        """Initialize the Job Application Agent"""
        load_dotenv('config.env')
        
        self.logger = AgentLogger("job_application_agent")
        self.notifications = NotificationManager("job_application_agent")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Job search criteria
        self.search_criteria = {
            "keywords": ["full stack developer", "frontend developer", "react developer", "angular developer"],
            "locations": ["Cairo", "Egypt", "Remote"],
            "experience_level": ["entry", "mid-level"],
            "job_types": ["full-time", "contract"]
        }
        
        # Job sites to scrape
        self.job_sites = {
            "linkedin": "https://linkedin.com/jobs",
            "indeed": "https://indeed.com",
            "glassdoor": "https://glassdoor.com"
        }
        
        self.logger.info("Job Application Agent initialized successfully")

    def search_jobs(self, keywords: List[str] = None, location: str = "Cairo, Egypt") -> List[Dict[str, Any]]:
        """Search for jobs based on criteria"""
        if keywords is None:
            keywords = self.search_criteria["keywords"]
        
        self.logger.info(f"Searching for jobs with keywords: {keywords} in {location}")
        
        all_jobs = []
        
        # Search LinkedIn jobs
        try:
            linkedin_jobs = self._search_linkedin_jobs(keywords, location)
            all_jobs.extend(linkedin_jobs)
            self.logger.info(f"Found {len(linkedin_jobs)} jobs on LinkedIn")
        except Exception as e:
            self.logger.error(f"Error searching LinkedIn: {e}")
        
        # Search Indeed jobs
        try:
            indeed_jobs = self._search_indeed_jobs(keywords, location)
            all_jobs.extend(indeed_jobs)
            self.logger.info(f"Found {len(indeed_jobs)} jobs on Indeed")
        except Exception as e:
            self.logger.error(f"Error searching Indeed: {e}")
        
        # Remove duplicates based on job title and company
        unique_jobs = self._remove_duplicates(all_jobs)
        
        self.logger.info(f"Total unique jobs found: {len(unique_jobs)}")
        return unique_jobs

    def _search_linkedin_jobs(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        """Search LinkedIn for jobs"""
        jobs = []
        
        try:
            # Setup Chrome driver
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Search for each keyword
            for keyword in keywords[:2]:  # Limit to first 2 keywords for testing
                search_url = f"https://linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
                
                self.logger.info(f"Searching LinkedIn: {search_url}")
                driver.get(search_url)
                
                # Wait for jobs to load
                time.sleep(3)
                
                # Find job listings
                job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
                
                for card in job_cards[:5]:  # Limit to first 5 jobs per keyword
                    try:
                        job_title = card.find_element(By.CSS_SELECTOR, ".job-search-card__title").text
                        company = card.find_element(By.CSS_SELECTOR, ".job-search-card__subtitle").text
                        location_text = card.find_element(By.CSS_SELECTOR, ".job-search-card__location").text
                        
                        # Get job link
                        job_link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        jobs.append({
                            "title": job_title,
                            "company": company,
                            "location": location_text,
                            "source": "LinkedIn",
                            "url": job_link,
                            "keyword_matched": keyword,
                            "scraped_at": datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        self.logger.warning(f"Error parsing LinkedIn job card: {e}")
                        continue
            
            driver.quit()
            
        except Exception as e:
            self.logger.error(f"Error in LinkedIn job search: {e}")
        
        return jobs

    def _search_indeed_jobs(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        """Search Indeed for jobs"""
        jobs = []
        
        try:
            # Setup Chrome driver
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Search for each keyword
            for keyword in keywords[:2]:  # Limit to first 2 keywords for testing
                search_url = f"https://indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"
                
                self.logger.info(f"Searching Indeed: {search_url}")
                driver.get(search_url)
                
                # Wait for jobs to load
                time.sleep(3)
                
                # Find job listings
                job_cards = driver.find_elements(By.CSS_SELECTOR, ".job_seen_beacon")
                
                for card in job_cards[:5]:  # Limit to first 5 jobs per keyword
                    try:
                        job_title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text
                        company = card.find_element(By.CSS_SELECTOR, ".companyName").text
                        location_text = card.find_element(By.CSS_SELECTOR, ".companyLocation").text
                        
                        # Get job link
                        job_link = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a").get_attribute("href")
                        job_link = urljoin("https://indeed.com", job_link)
                        
                        jobs.append({
                            "title": job_title,
                            "company": company,
                            "location": location_text,
                            "source": "Indeed",
                            "url": job_link,
                            "keyword_matched": keyword,
                            "scraped_at": datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        self.logger.warning(f"Error parsing Indeed job card: {e}")
                        continue
            
            driver.quit()
            
        except Exception as e:
            self.logger.error(f"Error in Indeed job search: {e}")
        
        return jobs

    def _remove_duplicates(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate jobs based on title and company"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique identifier
            identifier = f"{job['title'].lower()}_{job['company'].lower()}"
            
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        return unique_jobs

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

I am particularly drawn to {job['company']} because of [company-specific reason - research needed]. I am excited about the opportunity to contribute to your team and would welcome the chance to discuss how my skills and experience align with your needs.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
Abdallah Nasr Ali
        """.strip()

    def _select_cv_version(self, job: Dict[str, Any]) -> str:
        """Select the appropriate CV version for the job"""
        job_title_lower = job['title'].lower()
        
        if any(keyword in job_title_lower for keyword in ['ats', 'applicant tracking', 'recruitment']):
            return "ats"
        elif any(keyword in job_title_lower for keyword in ['senior', 'lead', 'manager', 'architect']):
            return "professional"
        else:
            return "concise"

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

    def run_job_search(self, keywords: List[str] = None, location: str = "Cairo, Egypt") -> List[Dict[str, Any]]:
        """Main method to run job search and create application drafts"""
        self.logger.info("Starting job search and application draft creation")
        
        try:
            # Search for jobs
            jobs = self.search_jobs(keywords, location)
            
            if not jobs:
                self.logger.warning("No jobs found matching criteria")
                return []
            
            # Create application drafts for each job
            drafts = []
            for job in jobs[:3]:  # Limit to first 3 jobs for testing
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
            self.logger.error(f"Error in job search process: {e}")
            return []

def main():
    """Main function to run the job application agent"""
    agent = JobApplicationAgent()
    
    # Run job search
    drafts = agent.run_job_search(
        keywords=["full stack developer", "frontend developer"],
        location="Cairo, Egypt"
    )
    
    if drafts:
        print(f"\n🎉 Job Application Agent completed successfully!")
        print(f"📝 Created {len(drafts)} application drafts")
        print(f"📁 Drafts saved in: job_application_drafts/")
        print(f"📧 Check your email for approval notifications")
        
        for draft in drafts:
            print(f"\n📋 Draft: {draft['job_title']} at {draft['company']}")
            print(f"   Status: {draft['status']}")
            print(f"   CV Version: {draft['cv_version']}")
            print(f"   File: {draft['filepath']}")
    else:
        print("\n❌ No application drafts created")

if __name__ == "__main__":
    main()
