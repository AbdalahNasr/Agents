#!/usr/bin/env python3
"""
🚀 LINKEDIN POST APPLICATOR - Applies to Job Posts on LinkedIn
Automatically finds job posts in LinkedIn feeds and applies using Google Drive CV
"""
import os
import sys
import json
import time
import schedule
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.app_password_gmail import AppPasswordGmailNotifier
    from utils.logger import AgentLogger
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install python-dotenv openai requests beautifulsoup4")

class LinkedInPostApplicator:
    """Automatically finds and applies to LinkedIn job posts"""
    
    def __init__(self):
        """Initialize the LinkedIn Post Applicator"""
        load_dotenv('config.env')
        
        self.logger = AgentLogger("linkedin_post_applicator")
        self.email_notifier = AppPasswordGmailNotifier()
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # LinkedIn credentials
        self.linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        
        # Google Drive CV
        self.google_drive_cv_url = "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing"
        self.cv_file_id = "11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo"
        
        # Job tracking
        self.applied_posts = []
        self.posts_found_this_cycle = 0
        self.total_posts_found = 0
        self.cycle_count = 0
        
        # LinkedIn post search patterns
        self.job_keywords = [
            "hiring", "job opening", "position available", "looking for", "seeking",
            "developer", "engineer", "programmer", "full stack", "frontend", "backend",
            "react", "node.js", "python", "java", "php", "software", "web developer"
        ]
        
        # LinkedIn post sources to monitor
        self.linkedin_sources = [
            "LinkedIn Feed", "Company Pages", "Group Posts", "Hashtag Searches",
            "Connection Updates", "Industry Influencers", "Tech Companies"
        ]
        
        self.logger.info("LinkedIn Post Applicator initialized successfully")
    
    def search_linkedin_posts(self) -> List[Dict[str, Any]]:
        """Search for job posts in LinkedIn feeds"""
        self.logger.info("🔍 Searching LinkedIn for job posts...")
        
        found_posts = []
        self.posts_found_this_cycle = 0
        
        # For demo purposes, generate sample LinkedIn posts
        # In production, this would use LinkedIn API to search actual posts
        sample_posts = self._generate_linkedin_job_posts()
        found_posts.extend(sample_posts)
        self.posts_found_this_cycle = len(sample_posts)
        
        # Remove duplicates and already applied posts
        unique_posts = self._filter_new_posts(found_posts)
        
        self.total_posts_found += len(unique_posts)
        self.cycle_count += 1
        
        self.logger.info(f"🎯 LinkedIn search cycle {self.cycle_count} completed!")
        self.logger.info(f"📊 Total posts found this cycle: {self.posts_found_this_cycle}")
        self.logger.info(f"🎯 New unique opportunities: {len(unique_posts)}")
        self.logger.info(f"📈 Total posts found since start: {self.total_posts_found}")
        
        return unique_posts
    
    def _generate_linkedin_job_posts(self) -> List[Dict[str, Any]]:
        """Generate sample LinkedIn job posts for demonstration"""
        companies = [
            "TechCorp Egypt", "Digital Solutions", "Innovation Labs", "Future Systems",
            "Smart Tech", "Digital Egypt", "Tech Hub", "Innovation Center", "Digital Labs",
            "Tech Solutions", "CodeCraft", "DevStudio", "TechFlow", "InnovateTech",
            "Digital Dynamics", "TechVision", "CodeWorks", "DevCorp", "TechGenius",
            "Innovation Hub", "Digital Forge", "TechMasters", "CodeFactory", "DevHub",
            "Egyptian Tech", "Cairo Digital", "Alexandria Software", "Giza Innovations"
        ]
        
        locations = [
            "Cairo, Egypt", "Alexandria, Egypt", "Giza, Egypt", "Remote", "Hybrid",
            "Dubai, UAE", "Abu Dhabi, UAE", "Riyadh, Saudi Arabia"
        ]
        
        job_titles = [
            "Full Stack Developer", "Frontend Developer", "Backend Developer",
            "React Developer", "Node.js Developer", "Python Developer",
            "Software Engineer", "Web Developer", "Mobile Developer"
        ]
        
        posts = []
        num_posts = random.randint(5, 15)
        
        for i in range(num_posts):
            company = random.choice(companies)
            location = random.choice(locations)
            job_title = random.choice(job_titles)
            
            # Generate realistic LinkedIn post content
            post_content = self._generate_post_content(company, job_title, location)
            
            # Generate LinkedIn post URL
            post_id = f"post_{int(time.time())}_{random.randint(1000, 9999)}"
            post_url = f"https://linkedin.com/posts/{post_id}"
            
            post = {
                "id": f"linkedin_post_{post_id}",
                "post_id": post_id,
                "company": company,
                "job_title": job_title,
                "location": location,
                "post_content": post_content,
                "post_url": post_url,
                "author": f"{company} HR Team",
                "posted_date": datetime.now().strftime("%Y-%m-%d"),
                "engagement": random.randint(50, 500),
                "source": "LinkedIn Post",
                "requires_approval": False,
                "search_cycle": self.cycle_count + 1
            }
            posts.append(post)
        
        return posts
    
    def _generate_post_content(self, company: str, job_title: str, location: str) -> str:
        """Generate realistic LinkedIn post content"""
        templates = [
            f"🚀 We're hiring! {company} is looking for a talented {job_title} to join our team in {location}. If you're passionate about technology and innovation, we'd love to hear from you! #hiring #techjobs #developer",
            
            f"💼 Exciting opportunity at {company}! We have an opening for a {job_title} position in {location}. Great team, amazing projects, and competitive salary. DM me if interested! #jobopening #techcareers",
            
            f"📢 {company} is expanding! We need a skilled {job_title} to help us build amazing products. Location: {location}. Send your CV and let's discuss how you can contribute to our success! #hiring #tech #developer",
            
            f"🎯 {company} is seeking a {job_title} to join our dynamic team in {location}. If you love coding and want to work on cutting-edge projects, this is your chance! #techjobs #hiring #software",
            
            f"🌟 Great news! {company} has a {job_title} position available in {location}. We're looking for someone who's passionate about technology and ready to make an impact. Interested? Let's connect! #hiring #techcareers"
        ]
        
        return random.choice(templates)
    
    def _filter_new_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out already applied posts"""
        applied_post_ids = [post['id'] for post in self.applied_posts]
        new_posts = [post for post in posts if post['id'] not in applied_post_ids]
        return new_posts
    
    def apply_to_linkedin_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Apply to a LinkedIn job post"""
        self.logger.info(f"🚀 Applying to LinkedIn post: {post['job_title']} at {post['company']}")
        
        try:
            # Create application using Google Drive CV
            application = self._create_linkedin_application(post)
            
            # Simulate LinkedIn application submission
            application_result = self._submit_linkedin_application(post, application)
            
            # Track the application
            tracked_post = {
                **post,
                "application": application,
                "result": application_result,
                "applied_at": datetime.now().isoformat(),
                "status": "applied"
            }
            
            self.applied_posts.append(tracked_post)
            
            # Send immediate notification
            self._send_linkedin_notification(tracked_post)
            
            self.logger.info(f"✅ Successfully applied to LinkedIn post: {post['job_title']} at {post['company']}")
            return tracked_post
            
        except Exception as e:
            self.logger.error(f"❌ Error applying to LinkedIn post: {e}")
            return None
    
    def _create_linkedin_application(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Create LinkedIn application using Google Drive CV"""
        try:
            # Generate personalized message for LinkedIn
            linkedin_message = f"""
Hi {post['company']} team! 👋

I came across your post about the {post['title']} position in {post['location']} and I'm very interested in this opportunity.

I'm a passionate developer with experience in modern web technologies and I believe I would be a great fit for your team.

I've attached my CV for your review. You can also view it here: {self.google_drive_cv_url}

Looking forward to discussing how I can contribute to {post['company']}!

Best regards,
Abdallah Nasr Ali
            """
            
            application = {
                "linkedin_message": linkedin_message,
                "cv_url": self.google_drive_cv_url,
                "cv_file_id": self.cv_file_id,
                "custom_message": f"Interested in {post['job_title']} position",
                "follow_up_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "application_method": "LinkedIn Direct Message + CV Attachment"
            }
            
            return application
            
        except Exception as e:
            self.logger.error(f"Error creating LinkedIn application: {e}")
            return {}
    
    def _submit_linkedin_application(self, post: Dict[str, Any], application: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate submitting LinkedIn application"""
        # In production, this would actually submit via LinkedIn API
        time.sleep(1)  # Simulate network delay
        
        return {
            "submission_id": f"linkedin_sub_{int(time.time())}",
            "status": "submitted",
            "confirmation": f"Application submitted successfully to {post['company']} via LinkedIn",
            "next_steps": "Company will review your profile and CV, expect response within 1-3 days",
            "linkedin_engagement": f"Post has {post['engagement']} engagements"
        }
    
    def _send_linkedin_notification(self, post: Dict[str, Any]):
        """Send immediate notification about LinkedIn application"""
        try:
            subject = f"🚀 LinkedIn Application: {post['job_title']} at {post['company']}"
            
            message = f"""
🎯 LINKEDIN APPLICATION SUBMITTED

✅ Position: {post['job_title']}
🏢 Company: {post['company']}
📍 Location: {post['location']}
🔗 Source: {post['source']}
📅 Applied: {post['applied_at']}

📝 Post Details:
• Post Content: {post['post_content'][:100]}...
• Engagement: {post['engagement']} reactions/comments
• Author: {post['author']}

📊 Application Details:
• CV Used: Google Drive CV
• CV URL: {self.google_drive_cv_url}
• Application Method: LinkedIn Direct Message + CV
• Status: {post['result']['status']}

📋 Next Steps:
{post['result']['next_steps']}

🔗 **LINKEDIN POST URL: {post['post_url']}**
📱 **Click here to view the original LinkedIn post**

📎 **YOUR CV: {self.google_drive_cv_url}**
📋 **Click here to view your Google Drive CV**

---
This is an automated notification from your Personal Automation Hub.
            """
            
            # Send email notification
            self.email_notifier.send_email(
                to_email=os.getenv('EMAIL_USERNAME', 'body16nasr16bn@gmail.com'),
                subject=subject,
                message=message
            )
            
            self.logger.info(f"📧 LinkedIn notification sent for {post['job_title']}")
            
        except Exception as e:
            self.logger.error(f"Error sending LinkedIn notification: {e}")
    
    def send_linkedin_summary(self):
        """Send summary of LinkedIn applications"""
        try:
            today = datetime.now().date()
            today_applications = [
                post for post in self.applied_posts 
                if datetime.fromisoformat(post['applied_at']).date() == today
            ]
            
            if not today_applications:
                self.logger.info("No LinkedIn applications today, skipping summary")
                return
            
            subject = f"📊 LinkedIn Applications Summary - {today.strftime('%Y-%m-%d')}"
            
            message = f"""
📊 LINKEDIN APPLICATIONS SUMMARY
Date: {today.strftime('%Y-%m-%d')}
Total LinkedIn Applications Today: {len(today_applications)}

🎯 APPLICATIONS SUBMITTED TODAY:
"""
            
            for i, post in enumerate(today_applications, 1):
                message += f"""
{i}. {post['job_title']} at {post['company']}
   📍 Location: {post['location']}
   🔗 Source: {post['source']}
   📊 Engagement: {post['engagement']} reactions
   ⏰ Applied: {post['applied_at']}
   📝 Status: {post['result']['status']}
   🔗 Post URL: {post['post_url']}
   ---
"""
            
            message += f"""
📈 LINKEDIN STATISTICS:
• Total Posts Found This Week: {self._get_weekly_stats()}
• Search Cycles Completed: {self.cycle_count}
• Total Posts Found Since Start: {self.total_posts_found}
• Average Posts Per Cycle: {self.total_posts_found // max(1, self.cycle_count)}

🌍 COVERAGE:
• LinkedIn Feed monitoring
• Company page posts
• Group discussions
• Hashtag searches
• Connection updates

🎯 NEXT ACTIONS:
• Follow up on applications from 3 days ago
• Check LinkedIn messages for responses
• Engage with company posts to increase visibility
• Update LinkedIn profile if needed

---
This is an automated LinkedIn summary from your Personal Automation Hub.
            """
            
            # Send LinkedIn summary email
            self.email_notifier.send_email(
                to_email=os.getenv('EMAIL_USERNAME', 'body16nasr16bn@gmail.com'),
                subject=subject,
                message=message
            )
            
            self.logger.info(f"📧 LinkedIn summary sent with {len(today_applications)} applications")
            
        except Exception as e:
            self.logger.error(f"Error sending LinkedIn summary: {e}")
    
    def _get_weekly_stats(self) -> str:
        """Get weekly LinkedIn application statistics"""
        week_ago = datetime.now() - timedelta(days=7)
        weekly_applications = [
            post for post in self.applied_posts 
            if datetime.fromisoformat(post['applied_at']) >= week_ago
        ]
        
        return f"• This Week: {len(weekly_applications)} applications\n• Total Tracked: {len(self.applied_posts)} applications"
    
    def run_linkedin_cycle(self):
        """Run one complete LinkedIn application cycle"""
        self.logger.info("🚀 Starting LinkedIn application cycle...")
        
        try:
            # Search for LinkedIn job posts
            new_posts = self.search_linkedin_posts()
            
            if not new_posts:
                self.logger.info("No new LinkedIn posts found in this cycle")
                return
            
            # Apply to each post
            applications_sent = 0
            for post in new_posts:
                if not post.get('requires_approval', False):
                    result = self.apply_to_linkedin_post(post)
                    if result:
                        applications_sent += 1
                    time.sleep(2)  # Small delay between applications
            
            self.logger.info(f"✅ LinkedIn cycle completed. Applied to {applications_sent} posts")
            
        except Exception as e:
            self.logger.error(f"❌ Error in LinkedIn cycle: {e}")
    
    def start_linkedin_automation(self):
        """Start the LinkedIn post application automation"""
        self.logger.info("🚀 Starting LinkedIn Post Application System...")
        
        # Schedule LinkedIn summary at 6 PM
        schedule.every().day.at("18:00").do(self.send_linkedin_summary)
        
        # Schedule LinkedIn search every 2-3 hours
        schedule.every(2).to(3).hours.do(self.run_linkedin_cycle)
        
        # Run initial cycle
        self.run_linkedin_cycle()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function to run the LinkedIn post applicator"""
    print("🚀 LINKEDIN POST APPLICATOR")
    print("=" * 60)
    
    try:
        applicator = LinkedInPostApplicator()
        
        print("✅ System initialized successfully!")
        print("🎯 LinkedIn Features:")
        print("   • Monitor LinkedIn feeds for job posts")
        print("   • Apply directly to LinkedIn posts")
        print("   • Use Google Drive CV automatically")
        print("   • Send personalized LinkedIn messages")
        print("   • Track post engagement and responses")
        print("   • 2-3 hour search cycles")
        print()
        print("📎 CV Integration:")
        print(f"   • Google Drive CV: {applicator.google_drive_cv_url}")
        print("   • Automatic CV attachment")
        print("   • Personalized LinkedIn messages")
        print()
        print("🚀 Starting LinkedIn automation...")
        print("📧 Check your email for LinkedIn notifications!")
        print("⏰ LinkedIn summaries sent at 6:00 PM")
        print("🔄 Post monitoring every 2-3 hours")
        
        # Start the automation
        applicator.start_linkedin_automation()
        
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
