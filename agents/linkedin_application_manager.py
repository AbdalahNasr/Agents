#!/usr/bin/env python3
"""
LinkedIn Application Manager
Handles LinkedIn job applications with Drive CV links and portfolio sharing
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.logger import AgentLogger
from agents.notion_manager import NotionManager
from agents.job_history_manager import JobHistoryManager
from agents.cv_manager import CVManager

class LinkedInApplicationManager:
    """Manages LinkedIn job applications with Drive CV links"""
    
    def __init__(self):
        self.logger = AgentLogger("linkedin_application_manager")
        self.notion_manager = NotionManager()
        self.history_manager = JobHistoryManager()
        self.cv_manager = CVManager()
        
        # LinkedIn configuration
        self.linkedin_username = os.getenv('LINKEDIN_USERNAME')
        self.linkedin_password = os.getenv('LINKEDIN_PASSWORD')
        
        # Chrome driver configuration
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = None
        self.logger.info("LinkedIn Application Manager initialized")
    
    def _setup_driver(self) -> bool:
        """Setup Chrome driver for LinkedIn automation"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.logger.info("Chrome driver setup successful")
            return True
        except Exception as e:
            self.logger.error(f"Chrome driver setup failed: {e}")
            return False
    
    def _login_linkedin(self) -> bool:
        """Login to LinkedIn"""
        try:
            if not self.linkedin_username or not self.linkedin_password:
                self.logger.error("LinkedIn credentials not configured")
                return False
            
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for login form
            wait = WebDriverWait(self.driver, 10)
            username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_field = self.driver.find_element(By.ID, "password")
            
            # Enter credentials
            username_field.send_keys(self.linkedin_username)
            password_field.send_keys(self.linkedin_password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for successful login
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "global-nav")))
            
            self.logger.info("LinkedIn login successful")
            return True
            
        except TimeoutException:
            self.logger.error("LinkedIn login timeout")
            return False
        except Exception as e:
            self.logger.error(f"LinkedIn login failed: {e}")
            return False
    
    def comment_on_job_post(self, post_url: str, drive_cv_link: str, 
                           portfolio_links: List[str] = None) -> bool:
        """Comment on LinkedIn job post with Drive CV link"""
        try:
            if not self._setup_driver():
                return False
            
            if not self._login_linkedin():
                return False
            
            # Navigate to the post
            self.driver.get(post_url)
            time.sleep(3)
            
            # Find comment section
            wait = WebDriverWait(self.driver, 10)
            comment_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Comment')]")))
            comment_button.click()
            
            # Find comment text area
            comment_textarea = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")))
            
            # Create comment text
            comment_text = self._create_linkedin_comment(drive_cv_link, portfolio_links)
            
            # Type comment
            comment_textarea.send_keys(comment_text)
            time.sleep(2)
            
            # Submit comment
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Post')]")
            submit_button.click()
            
            self.logger.info(f"LinkedIn comment posted successfully on: {post_url}")
            return True
            
        except TimeoutException:
            self.logger.error("LinkedIn comment timeout")
            return False
        except Exception as e:
            self.logger.error(f"LinkedIn comment failed: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def _create_linkedin_comment(self, drive_cv_link: str, portfolio_links: List[str] = None) -> str:
        """Create professional LinkedIn comment text"""
        comment_text = "#interested\n\n"
        comment_text += "Hi! I'm a junior full-stack developer interested in this opportunity. "
        comment_text += "I have experience with React, Node.js, and modern web technologies.\n\n"
        
        if drive_cv_link:
            comment_text += f"📄 Here's my CV: {drive_cv_link}\n\n"
        
        if portfolio_links:
            comment_text += "🚀 Portfolio & Projects:\n"
            for i, link in enumerate(portfolio_links[:4], 1):  # Limit to 4 links
                comment_text += f"• {link}\n"
        
        comment_text += "\nI'd love to discuss how I can contribute to your team! "
        comment_text += "Feel free to reach out for more details.\n\n"
        comment_text += "#webdevelopment #react #nodejs #javascript #fullstack"
        
        return comment_text
    
    def create_linkedin_application_package(self, job_info: Dict[str, Any], 
                                          post_url: str, drive_cv_link: str,
                                          portfolio_links: List[str] = None) -> Dict[str, Any]:
        """Create complete LinkedIn application package"""
        try:
            self.logger.info(f"Creating LinkedIn application package for: {job_info.get('title', 'Position')}")
            
            # Check CV access permissions
            access_result = self.cv_manager.request_cv_access("LinkedIn Application", job_info)
            
            if not access_result.get("approved", False):
                self.logger.warning("CV access not approved. Waiting for user approval.")
                return {
                    "error": "CV access not approved",
                    "message": access_result.get("message", "Waiting for approval"),
                    "requires_approval": True,
                    "access_result": access_result
                }
            
            # Comment on LinkedIn post
            comment_posted = self.comment_on_job_post(post_url, drive_cv_link, portfolio_links)
            
            # Prepare package
            package = {
                "success": True,
                "application_type": "linkedin",
                "job_info": job_info,
                "post_url": post_url,
                "drive_cv_link": drive_cv_link,
                "comment_posted": comment_posted,
                "portfolio_links": portfolio_links,
                "timestamp": datetime.now().isoformat()
            }
            
            # Track in Notion
            notion_page_id = self.notion_manager.create_job_application_entry(
                job_info, {"linkedin_post": post_url}, "LinkedIn Applied"
            )
            if notion_page_id:
                package["notion_page_id"] = notion_page_id
            
            # Track in local history
            application_id = self.history_manager.add_application(
                job_info, {"linkedin_post": post_url}, "LinkedIn Applied", notion_page_id
            )
            if application_id:
                package["application_id"] = application_id
            
            self.logger.info("LinkedIn application package created successfully")
            return package
            
        except Exception as e:
            self.logger.error(f"Failed to create LinkedIn application package: {e}")
            return {"error": str(e)}
    
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
    """Test the LinkedIn application manager"""
    print("🔗 LINKEDIN APPLICATION MANAGER TEST")
    print("=" * 40)
    
    manager = LinkedInApplicationManager()
    
    # Test job info
    test_job = {
        "title": "Junior Full Stack Developer",
        "company": "Tech Startup",
        "description": "Looking for a junior developer with React and Node.js experience"
    }
    
    # Test post URL (replace with actual LinkedIn post URL)
    test_post_url = "https://www.linkedin.com/posts/example-post"
    test_drive_link = "https://drive.google.com/file/d/1ABC123/view"
    
    # Test portfolio links
    portfolio_links = manager.get_portfolio_links()
    
    print("📝 Creating LinkedIn application package...")
    package = manager.create_linkedin_application_package(
        test_job, test_post_url, test_drive_link, portfolio_links
    )
    
    if package.get("success"):
        print("✅ LinkedIn application package created successfully!")
        print(f"   • Comment Posted: {package.get('comment_posted', False)}")
        print(f"   • Drive Link: {package.get('drive_cv_link', 'Not provided')}")
        print(f"   • Portfolio Links: {len(package.get('portfolio_links', []))}")
    else:
        print(f"❌ Failed: {package.get('error', 'Unknown error')}")
        if package.get("requires_approval"):
            print("🔐 CV access requires approval. Run:")
            print("   python agents/cv_manager.py --approve [request_id]")

if __name__ == "__main__":
    main()
