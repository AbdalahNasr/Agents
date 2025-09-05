#!/usr/bin/env python3
"""
Real Job Applicator - Actually applies to jobs with form filling and LinkedIn integration
"""

import os
import time
import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RealJobApplicator:
    def __init__(self):
        load_dotenv('config.env')
        self.user_profile = self._load_user_profile()
        self.application_history = self._load_application_history()
        self.driver = None
        
    def _load_user_profile(self) -> Dict[str, Any]:
        """Load comprehensive user profile for applications"""
        return {
            "personal_info": {
                "name": "Abdallah Nasr Ali",
                "email": os.getenv('GMAIL_USER', ''),
                "phone": "+20 123 456 7890",
                "location": "Cairo, Egypt",
                "linkedin_url": "https://linkedin.com/in/abdallah-nasr-ali",
                "github_url": "https://github.com/abdallah-nasr-ali",
                "portfolio_url": "https://abdallah-nasr-ali.dev"
            },
            "professional_info": {
                "experience_level": "Junior",
                "years_experience": "1-2 years",
                "current_role": "Junior Full Stack Developer",
                "target_roles": [
                    "Junior Full Stack Developer",
                    "Frontend Developer", 
                    "React Developer",
                    "Web Developer"
                ],
                "skills": [
                    "React", "Node.js", "JavaScript", "TypeScript",
                    "HTML", "CSS", "SCSS", "Next.js", "Prisma",
                    "Socket.IO", "Redux", "NextAuth", "Swagger",
                    "Cloudinary", "i18n", "PostCSS", "ESLint", "SSR"
                ],
                "languages": ["English (Fluent)", "Arabic (Native)"],
                "education": "Bachelor's in Computer Science",
                "certifications": ["AWS Cloud Practitioner", "React Developer Certification"]
            },
            "application_responses": {
                "why_interested": "I love building web apps and this role looks perfect for my React/Node.js skills. Excited to learn and contribute!",
                "salary_expectation": "$3,000 - $4,500",
                "availability": "Available immediately",
                "remote_preference": "Open to remote or on-site",
                "notice_period": "Available now",
                "relocation": "Open to relocation",
                "strengths": "Good problem solver, detail-oriented, love learning new tech. Work well in teams.",
                "challenges": "Always looking to improve and take on new challenges. Love continuous learning.",
                "questions_for_company": "What tech stack do you use? Any growth opportunities? How's the team culture?",
                "cover_letter_short": "Hi! I'm a junior developer with React/Node.js experience. I'm passionate about building great web apps and would love to contribute to your team. Available to start immediately!",
                "experience_summary": "1-2 years building web apps with React, Node.js, and modern JavaScript. Love clean code and user-friendly interfaces.",
                "why_this_company": "Your company seems to be doing exciting work in web development. I'd love to be part of that!",
                "what_can_you_bring": "Fresh perspective, strong technical skills, and eagerness to learn and grow with the team."
            }
        }
    
    def _load_application_history(self) -> List[Dict[str, Any]]:
        """Load application history to avoid duplicates"""
        try:
            with open('real_application_history.json', 'r') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_application_history(self):
        """Save application history"""
        try:
            with open('real_application_history.json', 'w') as f:
                json.dump(self.application_history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save application history: {e}")
    
    def _setup_driver(self):
        """Setup Chrome driver for web automation"""
        if self.driver:
            return
            
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Make it look more human
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def _humanize_typing(self, element, text: str, delay: float = 0.1):
        """Type text with human-like delays"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(delay + (0.05 * (1 if char == ' ' else 0)))  # Longer pause for spaces
    
    def _humanize_mouse_movement(self):
        """Simulate human-like mouse movements"""
        # Random small delays
        time.sleep(0.5 + (0.3 * (1 if datetime.now().second % 2 == 0 else 0)))
    
    def apply_to_linkedin_job(self, job_url: str) -> Dict[str, Any]:
        """Apply to a LinkedIn job with external redirect"""
        print(f"🔗 Applying to LinkedIn job: {job_url}")
        
        try:
            self._setup_driver()
            
            # Navigate to LinkedIn job
            self.driver.get(job_url)
            self._humanize_mouse_movement()
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check if it's an external application
            if "zohorecruit.com" in self.driver.current_url or "external" in self.driver.current_url.lower():
                print("  📋 External application form detected")
                return self._handle_external_application()
            
            # Handle LinkedIn Easy Apply
            elif self._is_linkedin_easy_apply():
                print("  📱 LinkedIn Easy Apply detected")
                return self._handle_linkedin_easy_apply()
            
            else:
                print("  🌐 Standard LinkedIn application")
                return self._handle_standard_linkedin_application()
                
        except Exception as e:
            print(f"  ❌ Error applying to LinkedIn job: {e}")
            return {"status": "failed", "error": str(e)}
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def _is_linkedin_easy_apply(self) -> bool:
        """Check if this is a LinkedIn Easy Apply job"""
        try:
            easy_apply_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Easy Apply')]")
            return easy_apply_button.is_displayed()
        except NoSuchElementException:
            return False
    
    def _handle_external_application(self) -> Dict[str, Any]:
        """Handle external application forms (like Zoho Recruit)"""
        print("  🔄 Handling external application form...")
        
        try:
            # Wait for form to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # Fill out the application form
            form_data = self._fill_external_form()
            
            # Submit the application
            submit_result = self._submit_external_form()
            
            # Update LinkedIn if possible
            linkedin_update = self._update_linkedin_application_status()
            
            return {
                "status": "applied",
                "method": "external_form",
                "form_data": form_data,
                "submitted_answers": form_data.get("submitted_answers", {}),
                "cv_uploaded": form_data.get("cv_uploaded"),
                "submit_result": submit_result,
                "linkedin_updated": linkedin_update,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  ❌ Error with external application: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _fill_external_form(self) -> Dict[str, Any]:
        """Fill out external application form with humanized responses"""
        print("  📝 Filling external application form...")
        
        filled_fields = {}
        submitted_answers = {}  # Track what we actually submit
        
        try:
            # Common form field mappings
            field_mappings = {
                "name": ["name", "full_name", "applicant_name", "first_name"],
                "email": ["email", "email_address", "contact_email"],
                "phone": ["phone", "phone_number", "mobile", "contact_phone"],
                "location": ["location", "city", "address", "residence"],
                "experience": ["experience", "years_experience", "work_experience"],
                "skills": ["skills", "technical_skills", "programming_skills"],
                "salary": ["salary", "expected_salary", "salary_expectation"],
                "availability": ["availability", "start_date", "when_available"],
                "cover_letter": ["cover_letter", "message", "additional_info", "why_interested"]
            }
            
            # Find and fill form fields
            for field_type, possible_names in field_mappings.items():
                for name in possible_names:
                    try:
                        # Try different selectors
                        selectors = [
                            f"input[name*='{name}']",
                            f"input[id*='{name}']",
                            f"textarea[name*='{name}']",
                            f"textarea[id*='{name}']",
                            f"select[name*='{name}']",
                            f"select[id*='{name}']"
                        ]
                        
                        for selector in selectors:
                            try:
                                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                                if element.is_displayed() and element.is_enabled():
                                    value = self._get_field_value(field_type)
                                    self._humanize_typing(element, value)
                                    filled_fields[name] = value
                                    submitted_answers[name] = value
                                    print(f"    ✅ Filled {name}: {value}")
                                    break
                            except NoSuchElementException:
                                continue
                                
                    except Exception as e:
                        continue
            
            # Handle file uploads (CV)
            cv_uploaded = self._handle_file_upload()
            
            # Show what we submitted
            print(f"\n  📋 SUBMITTED ANSWERS:")
            for field, answer in submitted_answers.items():
                print(f"    {field}: {answer}")
            
            if cv_uploaded:
                print(f"    CV: {cv_uploaded}")
            
            return {
                "filled_fields": filled_fields,
                "submitted_answers": submitted_answers,
                "cv_uploaded": cv_uploaded
            }
            
        except Exception as e:
            print(f"  ⚠️ Error filling form: {e}")
            return filled_fields
    
    def _get_field_value(self, field_type: str) -> str:
        """Get appropriate value for form field"""
        profile = self.user_profile
        
        if field_type == "name":
            return profile["personal_info"]["name"]
        elif field_type == "email":
            return profile["personal_info"]["email"]
        elif field_type == "phone":
            return profile["personal_info"]["phone"]
        elif field_type == "location":
            return profile["personal_info"]["location"]
        elif field_type == "experience":
            return profile["professional_info"]["years_experience"]
        elif field_type == "skills":
            return ", ".join(profile["professional_info"]["skills"][:10])
        elif field_type == "salary":
            return profile["application_responses"]["salary_expectation"]
        elif field_type == "availability":
            return profile["application_responses"]["availability"]
        elif field_type == "cover_letter":
            return profile["application_responses"]["why_interested"]
        else:
            return ""
    
    def _handle_file_upload(self):
        """Handle CV file upload"""
        try:
            # Look for file upload inputs
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            
            for file_input in file_inputs:
                if file_input.is_displayed():
                    # Use the CV file path
                    cv_path = os.path.abspath("Abdallah_Nasr_Ali_CV.pdf")
                    if os.path.exists(cv_path):
                        file_input.send_keys(cv_path)
                        print(f"    ✅ CV uploaded: {cv_path}")
                        return cv_path
                    else:
                        print(f"    ⚠️ CV file not found: {cv_path}")
                        return None
                        
        except Exception as e:
            print(f"    ⚠️ Could not upload CV: {e}")
            return None
    
    def _submit_external_form(self) -> Dict[str, Any]:
        """Submit the external application form"""
        print("  📤 Submitting application form...")
        
        try:
            # Look for submit button
            submit_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Submit')",
                "button:contains('Apply')",
                "button:contains('Send')",
                ".submit-button",
                ".apply-button"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        self._humanize_mouse_movement()
                        submit_button.click()
                        
                        # Wait for submission confirmation
                        time.sleep(3)
                        
                        # Check for success indicators
                        success_indicators = [
                            "thank you",
                            "application submitted",
                            "success",
                            "confirmation"
                        ]
                        
                        page_text = self.driver.page_source.lower()
                        success = any(indicator in page_text for indicator in success_indicators)
                        
                        return {
                            "status": "submitted" if success else "unknown",
                            "page_url": self.driver.current_url,
                            "success_indicators_found": success
                        }
                        
                except NoSuchElementException:
                    continue
            
            return {"status": "no_submit_button_found"}
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _update_linkedin_application_status(self) -> bool:
        """Update LinkedIn to mark job as applied"""
        print("  🔄 Updating LinkedIn application status...")
        
        try:
            # Go back to LinkedIn if possible
            if "linkedin.com" in self.driver.current_url:
                # Look for "Applied" button or status
                applied_selectors = [
                    "button:contains('Applied')",
                    ".applied-button",
                    "[data-test-id='applied-button']"
                ]
                
                for selector in applied_selectors:
                    try:
                        applied_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if applied_button.is_displayed():
                            print("    ✅ LinkedIn already shows as applied")
                            return True
                    except NoSuchElementException:
                        continue
                
                # If not already marked, try to find and click apply button
                apply_selectors = [
                    "button:contains('Apply')",
                    ".apply-button",
                    "[data-test-id='apply-button']"
                ]
                
                for selector in apply_selectors:
                    try:
                        apply_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if apply_button.is_displayed() and apply_button.is_enabled():
                            apply_button.click()
                            time.sleep(2)
                            print("    ✅ LinkedIn application status updated")
                            return True
                    except NoSuchElementException:
                        continue
            
            return False
            
        except Exception as e:
            print(f"    ⚠️ Could not update LinkedIn status: {e}")
            return False
    
    def _handle_linkedin_easy_apply(self) -> Dict[str, Any]:
        """Handle LinkedIn Easy Apply process"""
        print("  📱 Processing LinkedIn Easy Apply...")
        
        try:
            # Click Easy Apply button
            easy_apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Easy Apply')]"))
            )
            easy_apply_button.click()
            self._humanize_mouse_movement()
            
            # Fill out Easy Apply form
            form_result = self._fill_linkedin_easy_apply_form()
            
            # Submit application
            submit_result = self._submit_linkedin_easy_apply()
            
            return {
                "status": "applied",
                "method": "linkedin_easy_apply",
                "form_result": form_result,
                "submit_result": submit_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  ❌ Error with LinkedIn Easy Apply: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _fill_linkedin_easy_apply_form(self) -> Dict[str, Any]:
        """Fill out LinkedIn Easy Apply form"""
        print("  📝 Filling LinkedIn Easy Apply form...")
        
        filled_fields = {}
        
        try:
            # LinkedIn Easy Apply typically has multiple steps
            step = 1
            while step <= 5:  # Usually max 5 steps
                try:
                    # Look for form fields in current step
                    form_fields = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
                    
                    for field in form_fields:
                        if field.is_displayed() and field.is_enabled():
                            field_name = field.get_attribute("name") or field.get_attribute("id") or "unknown"
                            field_type = field.get_attribute("type") or "text"
                            
                            # Skip if already filled
                            if field.get_attribute("value"):
                                continue
                            
                            # Fill based on field type and name
                            value = self._get_linkedin_field_value(field_name, field_type)
                            if value:
                                self._humanize_typing(field, value)
                                filled_fields[field_name] = value
                                print(f"    ✅ Filled {field_name}: {value[:50]}...")
                    
                    # Look for Next button
                    next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                    if next_button.is_displayed() and next_button.is_enabled():
                        next_button.click()
                        self._humanize_mouse_movement()
                        step += 1
                    else:
                        break
                        
                except NoSuchElementException:
                    break
                except Exception as e:
                    print(f"    ⚠️ Error in step {step}: {e}")
                    break
            
            return filled_fields
            
        except Exception as e:
            print(f"  ⚠️ Error filling LinkedIn form: {e}")
            return filled_fields
    
    def _get_linkedin_field_value(self, field_name: str, field_type: str) -> str:
        """Get appropriate value for LinkedIn form field"""
        profile = self.user_profile
        
        field_name_lower = field_name.lower()
        
        if "phone" in field_name_lower:
            return profile["personal_info"]["phone"]
        elif "email" in field_name_lower:
            return profile["personal_info"]["email"]
        elif "location" in field_name_lower or "city" in field_name_lower:
            return profile["personal_info"]["location"]
        elif "experience" in field_name_lower:
            return profile["professional_info"]["years_experience"]
        elif "salary" in field_name_lower:
            return profile["application_responses"]["salary_expectation"]
        elif "availability" in field_name_lower:
            return profile["application_responses"]["availability"]
        elif "cover" in field_name_lower or "message" in field_name_lower:
            return profile["application_responses"]["why_interested"]
        elif "question" in field_name_lower:
            return profile["application_responses"]["questions_for_company"]
        else:
            return ""
    
    def _submit_linkedin_easy_apply(self) -> Dict[str, Any]:
        """Submit LinkedIn Easy Apply application"""
        print("  📤 Submitting LinkedIn Easy Apply...")
        
        try:
            # Look for Submit button
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
            )
            submit_button.click()
            self._humanize_mouse_movement()
            
            # Wait for confirmation
            time.sleep(3)
            
            # Check for success
            success_indicators = [
                "application submitted",
                "thank you",
                "success",
                "applied"
            ]
            
            page_text = self.driver.page_source.lower()
            success = any(indicator in page_text for indicator in success_indicators)
            
            return {
                "status": "submitted" if success else "unknown",
                "success_indicators_found": success
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _handle_standard_linkedin_application(self) -> Dict[str, Any]:
        """Handle standard LinkedIn application (external redirect)"""
        print("  🌐 Handling standard LinkedIn application...")
        
        try:
            # Look for Apply button
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply')]"))
            )
            apply_button.click()
            self._humanize_mouse_movement()
            
            # Wait for redirect or new window
            time.sleep(3)
            
            # Check if redirected to external site
            if "linkedin.com" not in self.driver.current_url:
                print("  🔄 Redirected to external application site")
                return self._handle_external_application()
            else:
                print("  📱 Stayed on LinkedIn - Easy Apply")
                return self._handle_linkedin_easy_apply()
                
        except Exception as e:
            print(f"  ❌ Error with standard LinkedIn application: {e}")
            return {"status": "failed", "error": str(e)}
    
    def apply_to_job(self, job_url: str, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to apply to a job"""
        print(f"\n🎯 Applying to: {job_details.get('title', 'Unknown')} at {job_details.get('company', 'Unknown')}")
        print(f"🔗 URL: {job_url}")
        
        # Check if already applied
        if self._already_applied(job_url):
            print("  ⚠️ Already applied to this job - skipping")
            return {"status": "skipped", "reason": "already_applied"}
        
        # Apply based on job source
        if "linkedin.com" in job_url:
            result = self.apply_to_linkedin_job(job_url)
        else:
            result = self.apply_to_generic_job(job_url)
        
        # Record application
        if result.get("status") == "applied":
            self._record_application(job_url, job_details, result)
        
        return result
    
    def _already_applied(self, job_url: str) -> bool:
        """Check if already applied to this job"""
        for app in self.application_history:
            if app.get("job_url") == job_url:
                return True
        return False
    
    def _record_application(self, job_url: str, job_details: Dict[str, Any], result: Dict[str, Any]):
        """Record the application in history"""
        application_record = {
            "job_url": job_url,
            "job_title": job_details.get("title", "Unknown"),
            "company": job_details.get("company", "Unknown"),
            "application_date": datetime.now().isoformat(),
            "application_method": result.get("method", "unknown"),
            "status": result.get("status", "unknown"),
            "result": result
        }
        
        self.application_history.append(application_record)
        self._save_application_history()
        
        print(f"  ✅ Application recorded: {result.get('method', 'unknown')} method")
    
    def apply_to_generic_job(self, job_url: str) -> Dict[str, Any]:
        """Apply to generic job posting"""
        print(f"  🌐 Applying to generic job: {job_url}")
        
        try:
            self._setup_driver()
            self.driver.get(job_url)
            self._humanize_mouse_movement()
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Try to find and fill application form
            form_result = self._fill_external_form()
            submit_result = self._submit_external_form()
            
            return {
                "status": "applied",
                "method": "generic_form",
                "form_result": form_result,
                "submit_result": submit_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  ❌ Error applying to generic job: {e}")
            return {"status": "failed", "error": str(e)}
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

def test_real_job_applicator():
    """Test the real job applicator"""
    print("Testing Real Job Applicator")
    print("=" * 50)
    
    applicator = RealJobApplicator()
    
    # Test with the Bruntwork job
    test_job = {
        "title": "Web Developer",
        "company": "Bruntwork",
        "location": "Remote",
        "url": "https://bruntwork.zohorecruit.com/jobs/Careers/655395000219439793/Web-developer?source=LinkedInRecELR"
    }
    
    print("🎯 Testing with real job application...")
    result = applicator.apply_to_job(test_job["url"], test_job)
    
    print(f"\n📊 Application Result:")
    print(f"  Status: {result.get('status', 'unknown')}")
    print(f"  Method: {result.get('method', 'unknown')}")
    print(f"  Timestamp: {result.get('timestamp', 'unknown')}")
    
    if result.get("status") == "applied":
        print("  ✅ Application successful!")
    else:
        print(f"  ❌ Application failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_real_job_applicator()
