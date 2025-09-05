"""
Job Application Agent - Personal Automation Agent

This agent scrapes job postings from various job sites, auto-fills application drafts
using AI, and requires your approval before submitting any applications.

Features:
- Scrapes job postings from LinkedIn, Indeed, Glassdoor, and other sites
- Uses AI to analyze job requirements and match with your profile
- Auto-fills application forms with relevant information
- Requires approval before submitting applications
- Sends notifications about new job opportunities
- Logs all actions and maintains application history

Usage:
    python agents/job_agent.py
    
    # Or import and use programmatically:
    from agents.job_agent import JobAgent
    agent = JobAgent()
    agent.scrape_jobs()
    agent.process_applications()
"""

import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config import Config
from utils.logger import AgentLogger
from utils.notifications import NotificationManager
from utils.approval import ApprovalManager

class JobAgent:
    """Job application automation agent for scraping and processing job opportunities."""
    
    def __init__(self):
        """Initialize the Job Agent with logging, notifications, and approval systems."""
        self.logger = AgentLogger("job_agent")
        self.notifications = NotificationManager("job_agent")
        self.approval = ApprovalManager("job_agent")
        
        # Job sites configuration
        self.job_sites = {
            'linkedin': {
                'base_url': 'https://linkedin.com/jobs',
                'search_pattern': '/jobs/search/',
                'job_selector': '.job-search-card',
                'title_selector': '.job-search-card__title',
                'company_selector': '.job-search-card__subtitle',
                'location_selector': '.job-search-card__location',
                'description_selector': '.job-search-card__description'
            },
            'indeed': {
                'base_url': 'https://indeed.com',
                'search_pattern': '/jobs',
                'job_selector': '.job_seen_beacon',
                'title_selector': '.jobTitle',
                'company_selector': '.companyName',
                'location_selector': '.companyLocation',
                'description_selector': '.job-snippet'
            },
            'glassdoor': {
                'base_url': 'https://glassdoor.com',
                'search_pattern': '/Job/',
                'job_selector': '.react-job-listing',
                'title_selector': '.jobLink',
                'company_selector': '.employerName',
                'location_selector': '.location',
                'description_selector': '.jobDescriptionContent'
            }
        }
        
        # User profile for job matching
        self.user_profile = {
            'skills': ['python', 'javascript', 'react', 'node.js', 'sql', 'aws'],
            'experience_years': 5,
            'preferred_locations': ['remote', 'new york', 'san francisco', 'london'],
            'preferred_companies': ['google', 'microsoft', 'amazon', 'netflix'],
            'salary_range': {'min': 80000, 'max': 150000},
            'job_titles': ['software engineer', 'full stack developer', 'backend developer', 'devops engineer']
        }
        
        # Application history
        self.applications = []
        
        # Web driver
        self.driver = None
        
        self.logger.info("Job Agent initialized", job_sites=list(self.job_sites.keys()))
    
    def setup_webdriver(self):
        """Setup Chrome webdriver for web scraping."""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Use webdriver manager to handle driver installation
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            self.logger.info("WebDriver setup completed")
            return True
            
        except Exception as e:
            self.logger.error("Failed to setup WebDriver", error=e)
            return False
    
    def close_webdriver(self):
        """Safely close the webdriver."""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.logger.info("WebDriver closed")
            except Exception as e:
                self.logger.error("Error closing WebDriver", error=e)
    
    def scrape_jobs(self, keywords: List[str] = None, location: str = "remote", 
                    max_jobs: int = 20) -> List[Dict]:
        """
        Scrape job postings from configured job sites.
        
        Args:
            keywords: List of job keywords to search for
            location: Location to search for jobs
            max_jobs: Maximum number of jobs to scrape per site
            
        Returns:
            List[Dict]: List of scraped job postings
        """
        if not self.setup_webdriver():
            return []
        
        try:
            self.logger.action("scrape_jobs", target=f"{len(self.job_sites)}_sites", status="started")
            
            keywords = keywords or self.user_profile['job_titles']
            all_jobs = []
            
            for site_name, site_config in self.job_sites.items():
                try:
                    self.logger.info(f"Scraping jobs from {site_name}")
                    site_jobs = self._scrape_site(site_name, site_config, keywords, location, max_jobs)
                    all_jobs.extend(site_jobs)
                    
                    # Be respectful with delays
                    time.sleep(2)
                    
                except Exception as e:
                    self.logger.error(f"Failed to scrape {site_name}", error=e)
                    continue
            
            # Remove duplicates and filter
            unique_jobs = self._deduplicate_jobs(all_jobs)
            filtered_jobs = self._filter_jobs_by_profile(unique_jobs)
            
            self.logger.action("scrape_jobs", target=f"{len(self.job_sites)}_sites", status="completed", 
                             total_found=len(all_jobs), unique=len(unique_jobs), filtered=len(filtered_jobs))
            
            return filtered_jobs
            
        except Exception as e:
            self.logger.error("Failed to scrape jobs", error=e)
            return []
        
        finally:
            self.close_webdriver()
    
    def _scrape_site(self, site_name: str, site_config: Dict, keywords: List[str], 
                     location: str, max_jobs: int) -> List[Dict]:
        """Scrape jobs from a specific site."""
        jobs = []
        
        for keyword in keywords[:3]:  # Limit to top 3 keywords to avoid overwhelming
            try:
                # Construct search URL
                search_url = self._build_search_url(site_config, keyword, location)
                
                self.driver.get(search_url)
                time.sleep(3)  # Wait for page to load
                
                # Find job listings
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, site_config['job_selector'])
                
                for job_element in job_elements[:max_jobs]:
                    try:
                        job_data = self._extract_job_data(job_element, site_config, site_name)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        self.logger.warning(f"Failed to extract job data from {site_name}", error=str(e))
                        continue
                
            except Exception as e:
                self.logger.error(f"Failed to scrape {site_name} for keyword {keyword}", error=e)
                continue
        
        return jobs
    
    def _build_search_url(self, site_config: Dict, keyword: str, location: str) -> str:
        """Build search URL for a job site."""
        base_url = site_config['base_url']
        
        if 'linkedin' in base_url:
            return f"{base_url}/search/?keywords={keyword.replace(' ', '%20')}&location={location}"
        elif 'indeed' in base_url:
            return f"{base_url}/jobs?q={keyword.replace(' ', '+')}&l={location}"
        elif 'glassdoor' in base_url:
            return f"{base_url}search?sc.keyword={keyword.replace(' ', '%20')}&locT=N&locId=1"
        else:
            return base_url
    
    def _extract_job_data(self, job_element, site_config: Dict, site_name: str) -> Optional[Dict]:
        """Extract job data from a job element."""
        try:
            # Extract basic information
            title = self._safe_extract_text(job_element, site_config['title_selector'])
            company = self._safe_extract_text(job_element, site_config['company_selector'])
            location = self._safe_extract_text(job_element, site_config['location_selector'])
            description = self._safe_extract_text(job_element, site_config['description_selector'])
            
            if not title or not company:
                return None
            
            # Try to extract job URL
            job_url = self._extract_job_url(job_element, site_config)
            
            job_data = {
                'title': title.strip(),
                'company': company.strip(),
                'location': location.strip() if location else 'Unknown',
                'description': description.strip() if description else '',
                'url': job_url,
                'site': site_name,
                'scraped_at': datetime.now().isoformat(),
                'match_score': 0  # Will be calculated later
            }
            
            return job_data
            
        except Exception as e:
            self.logger.warning("Failed to extract job data", error=str(e))
            return None
    
    def _safe_extract_text(self, element, selector: str) -> str:
        """Safely extract text from an element using a selector."""
        try:
            found_element = element.find_element(By.CSS_SELECTOR, selector)
            return found_element.text
        except:
            return ""
    
    def _extract_job_url(self, job_element, site_config: Dict) -> str:
        """Extract job URL from job element."""
        try:
            # Try to find a link element
            link_element = job_element.find_element(By.CSS_SELECTOR, 'a')
            return link_element.get_attribute('href')
        except:
            return ""
    
    def _deduplicate_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on title and company."""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique key based on title and company
            key = f"{job['title'].lower()}_{job['company'].lower()}"
            
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _filter_jobs_by_profile(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs based on user profile and calculate match scores."""
        filtered_jobs = []
        
        for job in jobs:
            match_score = self._calculate_match_score(job)
            job['match_score'] = match_score
            
            # Only include jobs with reasonable match score
            if match_score >= 30:  # Minimum 30% match
                filtered_jobs.append(job)
        
        # Sort by match score
        filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        return filtered_jobs
    
    def _calculate_match_score(self, job: Dict) -> int:
        """Calculate how well a job matches the user profile."""
        score = 0
        max_score = 100
        
        # Check title match
        job_title_lower = job['title'].lower()
        for preferred_title in self.user_profile['job_titles']:
            if preferred_title.lower() in job_title_lower:
                score += 25
                break
        
        # Check skills match
        job_desc_lower = job['description'].lower()
        skills_found = 0
        for skill in self.user_profile['skills']:
            if skill.lower() in job_desc_lower:
                skills_found += 1
        
        score += min(skills_found * 10, 30)  # Max 30 points for skills
        
        # Check location preference
        job_location_lower = job['location'].lower()
        for preferred_location in self.user_profile['preferred_locations']:
            if preferred_location.lower() in job_location_lower:
                score += 20
                break
        
        # Check company preference
        company_lower = job['company'].lower()
        for preferred_company in self.user_profile['preferred_companies']:
            if preferred_company.lower() in company_lower:
                score += 15
                break
        
        return min(score, max_score)
    
    def create_application_draft(self, job: Dict) -> Dict:
        """
        Create an application draft for a job using AI assistance.
        
        Args:
            job: Job data dictionary
            
        Returns:
            Dict: Application draft with cover letter and filled form
        """
        try:
            self.logger.action("create_application_draft", target=job['title'], status="started")
            
            # Generate cover letter using AI (placeholder - would use OpenAI API)
            cover_letter = self._generate_cover_letter(job)
            
            # Prepare application form data
            form_data = self._prepare_form_data(job)
            
            application_draft = {
                'job_id': f"{job['site']}_{job['company']}_{job['title']}".replace(' ', '_'),
                'job_title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'job_url': job['url'],
                'cover_letter': cover_letter,
                'form_data': form_data,
                'match_score': job['match_score'],
                'created_at': datetime.now().isoformat(),
                'status': 'draft'
            }
            
            self.logger.action("create_application_draft", target=job['title'], status="completed")
            return application_draft
            
        except Exception as e:
            self.logger.error("Failed to create application draft", error=e)
            return {}
    
    def _generate_cover_letter(self, job: Dict) -> str:
        """Generate a cover letter for the job using AI (placeholder implementation)."""
        # This would use OpenAI API to generate personalized cover letter
        # For now, return a template-based cover letter
        
        template = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {job['title']} position at {job['company']}. With my background in software development and passion for creating innovative solutions, I believe I would be an excellent fit for your team.

Based on the job description, I am particularly excited about the opportunity to work on challenging projects and contribute to {job['company']}'s continued success. My experience with technologies like Python, JavaScript, and cloud platforms aligns well with the requirements for this role.

I am confident that my technical skills, problem-solving abilities, and collaborative approach would make me a valuable addition to your team. I would welcome the opportunity to discuss how my background, skills, and enthusiasm would benefit {job['company']}.

Thank you for considering my application. I look forward to the possibility of contributing to your team.

Best regards,
[Your Name]
        """
        
        return template.strip()
    
    def _prepare_form_data(self, job: Dict) -> Dict:
        """Prepare form data for job application."""
        # This would be customized based on the specific job site's form
        return {
            'first_name': '[Your First Name]',
            'last_name': '[Your Last Name]',
            'email': '[Your Email]',
            'phone': '[Your Phone]',
            'current_company': '[Current Company]',
            'years_experience': str(self.user_profile['experience_years']),
            'linkedin_url': '[Your LinkedIn URL]',
            'portfolio_url': '[Your Portfolio URL]',
            'salary_expectation': f"${self.user_profile['salary_range']['min']:,} - ${self.user_profile['salary_range']['max']:,}",
            'availability': 'Immediate',
            'relocation': 'Yes' if 'remote' not in job['location'].lower() else 'No'
        }
    
    def submit_application(self, application_draft: Dict) -> bool:
        """
        Submit a job application (requires approval).
        
        Args:
            application_draft: Application draft to submit
            
        Returns:
            bool: True if submission successful
        """
        # Check if approval is required
        if self.approval.require_approval('job_application', 
                                        f"Submit application for {application_draft['job_title']} at {application_draft['company']}",
                                        application_draft):
            
            # Request approval
            approval_id = self.approval.request_approval(
                'job_application',
                f"Submit application for {application_draft['job_title']} at {application_draft['company']}",
                application_draft
            )
            
            self.logger.info("Approval requested for job application", approval_id=approval_id)
            self.notifications.warning(
                f"Approval required for job application: {application_draft['job_title']} at {application_draft['company']}",
                approval_id=approval_id
            )
            
            # Wait for approval
            if self.approval.wait_for_approval(approval_id):
                return self._execute_submission(application_draft)
            else:
                self.logger.info("Job application denied or timed out", job_title=application_draft['job_title'])
                return False
        
        else:
            # No approval required, submit directly
            return self._execute_submission(application_draft)
    
    def _execute_submission(self, application_draft: Dict) -> bool:
        """Execute the actual job application submission."""
        try:
            self.logger.action("submit_application", target=application_draft['job_title'], status="started")
            
            # This would contain the actual submission logic
            # For now, we'll simulate the submission
            
            # Update application status
            application_draft['status'] = 'submitted'
            application_draft['submitted_at'] = datetime.now().isoformat()
            
            # Add to applications history
            self.applications.append(application_draft)
            
            # Send success notification
            self.notifications.success(
                f"Job application submitted successfully for {application_draft['job_title']} at {application_draft['company']}",
                job_title=application_draft['job_title'],
                company=application_draft['company']
            )
            
            self.logger.action("submit_application", target=application_draft['job_title'], status="completed")
            return True
            
        except Exception as e:
            self.logger.error("Failed to submit application", error=e)
            self.notifications.error(f"Failed to submit application: {str(e)}")
            return False
    
    def process_applications(self, max_applications: int = 5) -> Dict:
        """
        Main method to process job applications.
        
        Args:
            max_applications: Maximum number of applications to process
            
        Returns:
            Dict: Processing results
        """
        start_time = time.time()
        
        try:
            self.logger.action("process_applications", target="main_process", status="started")
            
            # Scrape new jobs
            jobs = self.scrape_jobs(max_jobs=10)
            
            if not jobs:
                self.notifications.info("No suitable jobs found")
                return {'success': True, 'jobs_found': 0, 'applications_created': 0}
            
            # Create application drafts for top jobs
            applications_created = 0
            for job in jobs[:max_applications]:
                if job['match_score'] >= 50:  # Only process high-match jobs
                    draft = self.create_application_draft(job)
                    if draft:
                        applications_created += 1
                        
                        # Try to submit if match score is very high
                        if job['match_score'] >= 80:
                            self.submit_application(draft)
                        else:
                            # Store for manual review
                            self.applications.append(draft)
            
            # Send summary notification
            self.notifications.info(
                f"Job processing completed: {len(jobs)} jobs found, {applications_created} applications created",
                jobs_found=len(jobs),
                applications_created=applications_created
            )
            
            duration = time.time() - start_time
            self.logger.performance("process_applications", duration, 
                                  jobs_found=len(jobs), applications_created=applications_created)
            
            return {
                'success': True,
                'jobs_found': len(jobs),
                'applications_created': applications_created,
                'duration': duration
            }
            
        except Exception as e:
            self.logger.error("Failed to process applications", error=e)
            self.notifications.error(f"Failed to process applications: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_application_stats(self) -> Dict:
        """Get statistics about job applications."""
        total = len(self.applications)
        drafts = len([a for a in self.applications if a['status'] == 'draft'])
        submitted = len([a for a in self.applications if a['status'] == 'submitted'])
        
        return {
            'total': total,
            'drafts': drafts,
            'submitted': submitted,
            'last_updated': datetime.now().isoformat()
        }


def main():
    """Main function to run the Job Agent standalone."""
    print("🚀 Starting Job Application Agent...")
    
    # Validate configuration
    missing_config = Config.validate()
    if missing_config:
        print(f"❌ Missing configuration: {', '.join(missing_config)}")
        print("Please check your .env file and env_example.txt for required values.")
        return
    
    # Create and run agent
    agent = JobAgent()
    result = agent.process_applications()
    
    if result['success']:
        print(f"✅ Job processing completed successfully!")
        print(f"💼 Found {result['jobs_found']} jobs, created {result['applications_created']} applications")
        
        # Show stats
        stats = agent.get_application_stats()
        print(f"📊 Application Stats: {stats['total']} total, {stats['drafts']} drafts, {stats['submitted']} submitted")
    else:
        print(f"❌ Job processing failed: {result['error']}")


if __name__ == "__main__":
    main()
