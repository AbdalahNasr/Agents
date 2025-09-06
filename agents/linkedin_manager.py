#!/usr/bin/env python3
"""
LinkedIn Manager Agent - Manages LinkedIn profile and job hunting
Input: LinkedIn API credentials and actions
Process: Profile updates, job search, networking automation
Output: Profile optimizations, job opportunities, networking actions
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import AgentLogger
from utils.notifications import NotificationManager
from config import Config
from openai import OpenAI
from dotenv import load_dotenv

class LinkedInManager:
    def __init__(self):
        """Initialize the LinkedIn Manager Agent"""
        load_dotenv('config.env')
        
        self.logger = AgentLogger("linkedin_manager")
        self.notifications = NotificationManager("linkedin_manager")
        
        # Initialize OpenAI client for content optimization
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # LinkedIn API configuration
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID', '')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', '')
        self.redirect_uri = "http://localhost:8000/callback"
        self.api_base_url = "https://api.linkedin.com/v2"
        
        # Get access token from config
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN if hasattr(Config, 'LINKEDIN_ACCESS_TOKEN') else None
        
        # OAuth scopes needed
        self.scopes = [
            "r_liteprofile",
            "r_emailaddress", 
            "w_member_social",
            "r_organization_social"
        ]
        
        self.logger.info("LinkedIn Manager Agent initialized successfully")
    
    def get_authorization_url(self) -> str:
        """Generate LinkedIn OAuth authorization URL"""
        scope_string = "%20".join(self.scopes)
        
        auth_url = (
            f"https://www.linkedin.com/oauth/v2/authorization?"
            f"response_type=code&"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"scope={scope_string}&"
            f"state=random_state_string"
        )
        
        return auth_url
    
    def exchange_code_for_token(self, authorization_code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for access token"""
        try:
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            
            data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            response = requests.post(token_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.logger.info("Successfully obtained LinkedIn access token")
                return token_data
            else:
                self.logger.error(f"Failed to get access token: {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error exchanging code for token: {e}")
            return None
    
    def get_profile(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get LinkedIn profile information"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Get basic profile
            profile_url = f"{self.api_base_url}/me"
            response = requests.get(profile_url, headers=headers)
            
            if response.status_code == 200:
                profile_data = response.json()
                self.logger.info("Successfully retrieved LinkedIn profile")
                return profile_data
            else:
                self.logger.error(f"Failed to get profile: {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting profile: {e}")
            return None
    
    def update_profile_headline(self, access_token: str, new_headline: str) -> bool:
        """Update LinkedIn profile headline"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # LinkedIn API endpoint for profile updates
            update_url = f"{self.api_base_url}/me"
            
            update_data = {
                "localizedHeadline": new_headline
            }
            
            response = requests.patch(update_url, headers=headers, json=update_data)
            
            if response.status_code == 200:
                self.logger.info(f"Successfully updated headline to: {new_headline}")
                return True
            else:
                self.logger.error(f"Failed to update headline: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating headline: {e}")
            return False
    
    def search_jobs(self, access_token: str, keywords: List[str], location: str = "Cairo, Egypt") -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            jobs = []
            
            for keyword in keywords[:3]:  # Limit to 3 keywords
                # LinkedIn job search endpoint
                search_url = f"{self.api_base_url}/jobSearch"
                
                params = {
                    "keywords": keyword,
                    "location": location,
                    "count": 10
                }
                
                response = requests.get(search_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    job_data = response.json()
                    if 'elements' in job_data:
                        for job in job_data['elements']:
                            jobs.append({
                                "id": job.get('id'),
                                "title": job.get('title'),
                                "company": job.get('company', {}).get('name'),
                                "location": job.get('location', {}).get('city'),
                                "description": job.get('description'),
                                "url": f"https://linkedin.com/jobs/view/{job.get('id')}",
                                "keyword_matched": keyword,
                                "scraped_at": datetime.now().isoformat()
                            })
                
                time.sleep(1)  # Rate limiting
            
            self.logger.info(f"Found {len(jobs)} jobs on LinkedIn")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error searching LinkedIn jobs: {e}")
            return []
    
    def optimize_profile_for_ats(self, current_headline: str) -> str:
        """Optimize profile headline for ATS systems using AI"""
        try:
            prompt = f"""
            Optimize this LinkedIn headline for Applicant Tracking Systems (ATS):
            
            Current: "{current_headline}"
            
            Create a new headline that:
            1. Includes key technical skills (React, Angular, Node.js, Full Stack)
            2. Uses industry-standard job titles
            3. Incorporates relevant keywords for developer roles
            4. Is professional and compelling
            5. Maximum 220 characters
            
            Return only the optimized headline, nothing else.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a LinkedIn profile optimization expert specializing in tech careers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            optimized_headline = response.choices[0].message.content.strip()
            self.logger.info("Profile headline optimized using AI")
            return optimized_headline
            
        except Exception as e:
            self.logger.error(f"Error optimizing headline with AI: {e}")
            # Fallback optimization
            return "Full Stack Developer | React, Angular, Node.js | Modern Web Technologies"
    
    def create_networking_message(self, connection_name: str, company: str, role: str) -> str:
        """Generate personalized networking messages using AI"""
        try:
            prompt = f"""
            Create a professional LinkedIn connection request message for:
            
            Name: {connection_name}
            Company: {company}
            Role: {role}
            
            The sender is Abdallah Nasr Ali, a Full Stack Developer looking to:
            1. Connect with professionals in the tech industry
            2. Learn about opportunities at {company}
            3. Build professional relationships
            
            Requirements:
            - Professional and friendly tone
            - Mention specific interest in their company/role
            - Keep it under 300 characters
            - Include a clear call to action
            
            Return only the message, nothing else.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional networking expert who writes compelling LinkedIn connection messages."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            message = response.choices[0].message.content.strip()
            self.logger.info("Networking message generated using AI")
            return message
            
        except Exception as e:
            self.logger.error(f"Error generating networking message: {e}")
            # Fallback message
            return f"Hi {connection_name}, I'm impressed by your work at {company} and would love to connect. I'm a Full Stack Developer passionate about modern web technologies. Would love to learn more about your experience!"
    
    def send_networking_notification(self, connection_info: Dict[str, Any]) -> None:
        """Send notification about networking opportunities"""
        subject = f"Networking Opportunity - {connection_info['name']} at {connection_info['company']}"
        
        message = f"""
        New networking opportunity identified:
        
        Name: {connection_info['name']}
        Company: {connection_info['company']}
        Role: {connection_info['role']}
        
        Suggested connection message:
        {connection_info['suggested_message']}
        
        This could be valuable for:
        - Learning about {connection_info['company']}
        - Understanding the {connection_info['role']} role
        - Building professional relationships
        - Potential job opportunities
        
        Consider sending a connection request with the suggested message.
        """
        
        # Send notification
        self.notifications.notify(message, "INFO", subject=subject)
        self.logger.info(f"Networking notification sent for {connection_info['name']}")
    
    def run_profile_optimization(self, access_token: str) -> Dict[str, Any]:
        """Run profile optimization process"""
        self.logger.info("Starting LinkedIn profile optimization")
        
        try:
            # Get current profile
            profile = self.get_profile(access_token)
            if not profile:
                return {"success": False, "error": "Could not retrieve profile"}
            
            # Optimize headline
            current_headline = profile.get('localizedHeadline', '')
            optimized_headline = self.optimize_profile_for_ats(current_headline)
            
            # Update headline if different
            if optimized_headline != current_headline:
                success = self.update_profile_headline(access_token, optimized_headline)
                if success:
                    self.logger.info("Profile headline updated successfully")
                else:
                    self.logger.warning("Failed to update profile headline")
            
            return {
                "success": True,
                "current_headline": current_headline,
                "optimized_headline": optimized_headline,
                "updated": optimized_headline != current_headline
            }
            
        except Exception as e:
            self.logger.error(f"Error in profile optimization: {e}")
            return {"success": False, "error": str(e)}
    
    def run_job_search(self, access_token: str, keywords: List[str] = None, location: str = "Cairo, Egypt") -> List[Dict[str, Any]]:
        """Run LinkedIn job search"""
        if keywords is None:
            keywords = ["full stack developer", "frontend developer", "react developer"]
        
        self.logger.info(f"Starting LinkedIn job search for: {keywords}")
        
        try:
            jobs = self.search_jobs(access_token, keywords, location)
            
            if jobs:
                # Send notification about found jobs
                subject = f"LinkedIn Job Search Results - {len(jobs)} opportunities found"
                
                message = f"""
                LinkedIn job search completed successfully!
                
                Found {len(jobs)} job opportunities:
                
                """
                
                for i, job in enumerate(jobs[:5], 1):  # Show first 5
                    message += f"{i}. {job['title']} at {job['company']}\n"
                    message += f"   Location: {job['location']}\n"
                    message += f"   URL: {job['url']}\n\n"
                
                message += f"Total jobs found: {len(jobs)}"
                
                self.notifications.notify(message, "INFO", subject=subject)
                self.logger.info(f"Job search notification sent for {len(jobs)} jobs")
            
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error in job search: {e}")
            return []

def main():
    """Main function to demonstrate LinkedIn Manager capabilities"""
    manager = LinkedInManager()
    
    print("🔗 LinkedIn Manager Agent")
    print("=" * 50)
    
    if manager.access_token:
        print(f"\n✅ LinkedIn Access Token Found!")
        print(f"   Token: {manager.access_token[:20]}...")
        
        print(f"\n🚀 Testing LinkedIn System...")
        
        # Test profile retrieval
        print(f"\n📋 Testing Profile Retrieval...")
        profile = manager.get_profile(manager.access_token)
        if profile:
            print(f"   ✅ Profile Retrieved Successfully!")
            print(f"   Name: {profile.get('localizedFirstName', '')} {profile.get('localizedLastName', '')}")
            print(f"   Headline: {profile.get('localizedHeadline', 'N/A')}")
        else:
            print(f"   ❌ Failed to retrieve profile")
        
        # Test job search
        print(f"\n🔍 Testing Job Search...")
        jobs = manager.run_job_search(manager.access_token)
        if jobs:
            print(f"   ✅ Found {len(jobs)} jobs!")
            for i, job in enumerate(jobs[:3], 1):
                print(f"   {i}. {job['title']} at {job['company']}")
        else:
            print(f"   ❌ No jobs found or search failed")
        
        # Test profile optimization
        print(f"\n⚡ Testing Profile Optimization...")
        if profile:
            optimization = manager.run_profile_optimization(manager.access_token)
            if optimization['success']:
                print(f"   ✅ Profile optimization completed!")
                print(f"   Current: {optimization['current_headline']}")
                print(f"   Optimized: {optimization['optimized_headline']}")
                print(f"   Updated: {optimization['updated']}")
            else:
                print(f"   ❌ Profile optimization failed: {optimization.get('error', 'Unknown error')}")
        
    else:
        print(f"\n❌ No LinkedIn Access Token Found!")
        print(f"   Please add LINKEDIN_ACCESS_TOKEN to your config.env file")
        
        print(f"\n📋 Your LinkedIn API Credentials:")
        print(f"   Client ID: {manager.client_id}")
        print(f"   Client Secret: {manager.client_secret[:10]}...")
        print(f"   Redirect URI: {manager.redirect_uri}")
    
    print(f"\n🎯 What I Can Do:")
    print("   - Optimize your LinkedIn profile for ATS systems")
    print("   - Search for relevant job opportunities")
    print("   - Generate personalized networking messages")
    print("   - Track job applications and follow-ups")
    print("   - Automate profile updates and engagement")

if __name__ == "__main__":
    main()
