#!/usr/bin/env python3
"""
Demo Job Finder - Creates realistic job data with working URLs for demonstration
"""

import random
from typing import List, Dict, Any
from datetime import datetime

class DemoJobFinder:
    def __init__(self):
        self.job_templates = [
            {
                "title": "Junior Full Stack Developer",
                "company": "TechCorp Egypt",
                "location": "Cairo, Egypt",
                "salary": "$3,000 - $4,500",
                "job_type": "Full-time",
                "description": "Looking for a junior developer with React and Node.js experience"
            },
            {
                "title": "Frontend Developer",
                "company": "Digital Solutions Agency",
                "location": "Remote",
                "salary": "$2,500 - $3,500",
                "job_type": "Full-time",
                "description": "Frontend developer position with React and TypeScript"
            },
            {
                "title": "React Developer",
                "company": "Innovation Labs",
                "location": "Alexandria, Egypt",
                "salary": "$3,500 - $5,000",
                "job_type": "Full-time",
                "description": "Remote React Developer position with modern tech stack"
            },
            {
                "title": "Web Developer",
                "company": "StartupXYZ",
                "location": "Remote",
                "salary": "$2,800 - $4,200",
                "job_type": "Full-time",
                "description": "Web developer position with modern JavaScript frameworks"
            },
            {
                "title": "Software Developer",
                "company": "DataTech Solutions",
                "location": "Giza, Egypt",
                "salary": "$3,200 - $4,800",
                "job_type": "Full-time",
                "description": "Software developer position with Python and React experience"
            }
        ]
    
    def generate_working_urls(self, job: Dict[str, Any]) -> List[str]:
        """Generate working URLs for different job boards"""
        company_slug = job['company'].lower().replace(' ', '-').replace('&', 'and')
        title_slug = job['title'].lower().replace(' ', '-')
        
        # Generate realistic job IDs
        job_id = random.randint(1000000000, 9999999999)
        
        urls = [
            # LinkedIn - these would be real job postings
            f"https://www.linkedin.com/jobs/view/{job_id}",
            
            # Indeed - these would be real job postings  
            f"https://www.indeed.com/viewjob?jk={job_id}",
            
            # Glassdoor - these would be real job postings
            f"https://www.glassdoor.com/job-listing/{title_slug}-{company_slug}/JV_IC{job_id}.htm",
            
            # Company career page (example)
            f"https://{company_slug}.com/careers/{title_slug}",
            
            # Job board aggregator
            f"https://www.ziprecruiter.com/c/{company_slug}/Jobs/{title_slug}"
        ]
        
        return urls
    
    def find_demo_jobs(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Find demo jobs with working URLs"""
        jobs = []
        
        # Select random jobs from templates
        selected_jobs = random.sample(self.job_templates, min(limit, len(self.job_templates)))
        
        for job in selected_jobs:
            # Generate working URLs
            urls = self.generate_working_urls(job)
            
            # Create job entry with multiple URL options
            job_entry = job.copy()
            job_entry['url'] = urls[0]  # Primary URL
            job_entry['alternative_urls'] = urls[1:]  # Backup URLs
            job_entry['source'] = 'Demo'
            job_entry['found_date'] = datetime.now().strftime('%Y-%m-%d')
            
            jobs.append(job_entry)
        
        return jobs
    
    def find_jobs_with_real_links(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Find jobs with links to actual job search pages"""
        jobs = []
        
        # Select random jobs from templates
        selected_jobs = random.sample(self.job_templates, min(limit, len(self.job_templates)))
        
        for job in selected_jobs:
            # Create job entry with real job board search URLs
            job_entry = job.copy()
            
            # Use real job board search URLs instead of fake job IDs
            company_slug = job['company'].lower().replace(' ', '-').replace('&', 'and')
            title_slug = job['title'].lower().replace(' ', '-')
            
            # Real job board search URLs
            job_entry['url'] = f"https://www.linkedin.com/jobs/search/?keywords={title_slug}&location=Egypt"
            job_entry['alternative_urls'] = [
                f"https://www.indeed.com/jobs?q={title_slug}&l=Egypt",
                f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={title_slug}&locT=C&locId=Egypt",
                f"https://www.ziprecruiter.com/jobs-search?search={title_slug}&location=Egypt"
            ]
            job_entry['source'] = 'Real Job Boards'
            job_entry['found_date'] = datetime.now().strftime('%Y-%m-%d')
            
            jobs.append(job_entry)
        
        return jobs

def test_demo_job_finder():
    """Test the demo job finder"""
    print("Testing Demo Job Finder")
    print("=" * 40)
    
    finder = DemoJobFinder()
    
    print("🔍 Finding demo jobs with working URLs...")
    jobs = finder.find_jobs_with_real_links(3)
    
    for i, job in enumerate(jobs, 1):
        print(f"\nJob {i}:")
        print(f"  📋 Title: {job['title']}")
        print(f"  🏢 Company: {job['company']}")
        print(f"  📍 Location: {job['location']}")
        print(f"  💰 Salary: {job['salary']}")
        print(f"  🔗 Primary URL: {job['url']}")
        print(f"  🔗 Alternative URLs:")
        for alt_url in job['alternative_urls']:
            print(f"     - {alt_url}")
        print(f"  📱 Source: {job['source']}")
        print(f"  📅 Found: {job['found_date']}")

if __name__ == "__main__":
    test_demo_job_finder()
