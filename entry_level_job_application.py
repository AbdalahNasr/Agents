#!/usr/bin/env python3
"""
Entry-Level Job Application System
Optimized for first-time job seekers with realistic expectations

Features:
- Entry-level appropriate job titles
- Emphasis on code portfolio and GitHub
- Realistic experience descriptions
- Focus on learning potential and growth
- Honest representation of skill level
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.ats_cv_generator import ATSCVGenerator
from agents.ats_optimizer import ATSOptimizer
from agents.notion_manager import NotionManager
from agents.job_history_manager import JobHistoryManager
from agents.cv_manager import CVManager
from utils.logger import AgentLogger

class EntryLevelJobApplication:
    """Entry-level job application system"""
    
    def __init__(self):
        """Initialize the entry-level job application system"""
        self.logger = AgentLogger("entry_level_job_application")
        self.cv_generator = ATSCVGenerator()
        self.ats_optimizer = ATSOptimizer()
        self.notion_manager = NotionManager()
        self.history_manager = JobHistoryManager()
        self.cv_manager = CVManager()
        
        # Entry-level appropriate job titles
        self.entry_level_titles = [
            "Junior Full Stack Developer",
            "Junior Frontend Developer", 
            "Junior Backend Developer",
            "Entry Level Developer",
            "Trainee Developer",
            "Junior Software Engineer",
            "Frontend Developer Intern",
            "Backend Developer Intern",
            "Full Stack Developer Intern",
            "Junior Web Developer"
        ]
        
        self.logger.info("Entry-level job application system initialized")
    
    def create_entry_level_cv(self, job_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create an entry-level appropriate CV"""
        self.logger.info(f"Creating entry-level CV for: {job_info.get('title', 'Unknown')}")
        
        # Ensure job title is appropriate for entry-level
        job_title = job_info.get('title', '')
        if any(senior_word in job_title.lower() for senior_word in ['senior', 'lead', 'principal', 'architect']):
            # If it's a senior position, create a junior version
            job_info['title'] = job_title.replace('Senior', 'Junior').replace('Lead', 'Junior').replace('Principal', 'Junior')
            self.logger.info(f"Adjusted job title from '{job_title}' to '{job_info['title']}' for entry-level")
        
        # Generate CV with entry-level focus
        result = self.cv_generator.generate_job_specific_cv(job_info)
        
        if result:
            # Add entry-level specific enhancements
            result = self._enhance_for_entry_level(result, job_info)
            
            self.logger.info(f"Entry-level CV created successfully. ATS Score: {result['ats_analysis']['overall_score']}/100")
        
        return result
    
    def _enhance_for_entry_level(self, cv_result: Dict[str, Any], job_info: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance CV specifically for entry-level applications"""
        
        # Add GitHub emphasis
        cv_data = cv_result['cv_data']
        
        # Enhance projects section to emphasize code
        for project in cv_data['projects']:
            if 'code_url' in project:
                project['description'] += f" Complete source code available on GitHub with detailed README and documentation."
                project['achievements'].append("Published complete source code with documentation on GitHub")
        
        # Add GitHub skills emphasis
        if 'tools' in cv_data['skills']:
            cv_data['skills']['tools'].insert(0, 'GitHub (Active Portfolio)')
        
        # Ensure only actual technologies are used
        cv_data['skills'] = {
            "frontend": ["React", "Angular", "JavaScript", "TypeScript", "HTML5", "CSS3", "SCSS", "Tailwind CSS", "Bootstrap", "Next.js", "jQuery"],
            "backend": ["Node.js", "Express.js", "REST APIs"],
            "database": ["MongoDB", "Prisma"],
            "tools": ["Git", "GitHub", "Vercel", "Socket.IO", "Redux", "NextAuth"],
            "other": ["JWT", "Swagger", "Cloudinary", "i18n", "PostCSS", "ESLint", "SSR"]
        }
        
        # Enhance summary for entry-level
        cv_data['summary'] = self._create_entry_level_summary(job_info)
        
        # Add learning and growth focus
        cv_data['other_skills'] = [
            "Eager to learn new technologies",
            "Strong problem-solving abilities", 
            "Excellent communication skills",
            "Team collaboration",
            "Continuous learning mindset",
            "Code review and best practices"
        ]
        
        return cv_result
    
    def _create_entry_level_summary(self, job_info: Dict[str, Any]) -> str:
        """Create entry-level appropriate summary"""
        job_title = job_info.get('title', 'Junior Developer')
        
        summary = f"Passionate {job_title} seeking first professional opportunity to apply technical skills in a collaborative environment. "
        summary += "Strong foundation in modern web technologies with hands-on experience building full-stack applications. "
        summary += "Demonstrated coding abilities through personal projects with complete source code available on GitHub. "
        summary += "Eager to learn from experienced developers, contribute to real-world projects, and grow professionally. "
        summary += "Committed to writing clean, maintainable code and following industry best practices."
        
        return summary
    
    def get_entry_level_job_suggestions(self) -> List[Dict[str, Any]]:
        """Get entry-level job suggestions"""
        return [
            {
                "title": "Junior Full Stack Developer",
                "company": "Tech Startup",
                "location": "Cairo, Egypt",
                "description": """
                We are looking for a Junior Full Stack Developer to join our growing team.
                Perfect opportunity for recent graduates or self-taught developers.
                
                Requirements:
                - Basic knowledge of React, Node.js, or similar technologies
                - Understanding of HTML, CSS, JavaScript
                - Eagerness to learn and grow
                - Portfolio of personal projects
                - Strong problem-solving skills
                """
            },
            {
                "title": "Frontend Developer Intern",
                "company": "Digital Agency",
                "location": "Cairo, Egypt", 
                "description": """
                Internship opportunity for Frontend Developer to work on real client projects.
                Great learning environment with mentorship.
                
                Requirements:
                - React or Vue.js knowledge
                - HTML, CSS, JavaScript fundamentals
                - Portfolio with working code
                - Willingness to learn
                - Good communication skills
                """
            },
            {
                "title": "Junior Web Developer",
                "company": "E-commerce Company",
                "location": "Cairo, Egypt",
                "description": """
                Entry-level position for Web Developer to work on our e-commerce platform.
                Opportunity to work with modern technologies and learn from senior developers.
                
                Requirements:
                - JavaScript, HTML, CSS
                - Basic understanding of databases
                - GitHub portfolio
                - Learning mindset
                - Team player attitude
                """
            }
        ]
    
    def generate_entry_level_portfolio_summary(self) -> str:
        """Generate a summary of your portfolio for applications"""
        return """
        PORTFOLIO HIGHLIGHTS:
        
        🧵 Threads App - Social Platform (Next.js)
        • Complete social media platform with authentication
        • Features: Post creation, likes, responsive design, auth system
        • Technologies: Next.js, TypeScript, Tailwind, Node.js
        • Code: https://github.com/AbdalahNasr/threads
        • Live Demo: https://threads-4cls.vercel.app/sign-in
        
        🍕 Order-Food App - Full-Stack Platform (Next.js)
        • Complete food ordering platform with admin dashboard
        • Features: Product management, cart, i18n, Cloudinary integration
        • Technologies: Next.js, TypeScript, Tailwind, Redux, Prisma, NextAuth
        • Code: https://github.com/AbdalahNasr/order-food-app
        
        🧠 ISTQP Quiz App - Quiz Platform (Next.js)
        • Multilingual quiz application with JSON-based quizzes
        • Features: Dynamic quiz generation, SSR, ESLint integration
        • Technologies: Next.js, TypeScript, Tailwind CSS, PostCSS
        • Code: https://github.com/AbdalahNasr/istqp-quiz
        • Live Demo: https://istqp-quiz.vercel.app
        
        💡 Why This Matters:
        • All projects have complete, working source code on GitHub
        • Demonstrates full-stack development capabilities
        • Shows ability to build and deploy modern applications
        • Proves commitment to learning and coding best practices
        • Ready for code review and technical interviews
        • Real projects with live demos showing working applications
        """
    
    def create_application_package(self, job_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create complete application package for entry-level position"""
        self.logger.info(f"Creating complete application package for: {job_info.get('title', 'Unknown')}")
        
        # Check CV access permissions
        access_result = self.cv_manager.request_cv_access("Job Application", job_info)
        
        if not access_result.get("approved", False):
            self.logger.warning("CV access not approved. Waiting for user approval.")
            return {
                "error": "CV access not approved",
                "message": access_result.get("message", "Waiting for approval"),
                "requires_approval": True,
                "access_result": access_result
            }
        
        # Generate entry-level CV
        cv_result = self.create_entry_level_cv(job_info)
        
        if not cv_result:
            return None
        
        # Create application package
        package = {
            "job_info": job_info,
            "cv_result": cv_result,
            "portfolio_summary": self.generate_entry_level_portfolio_summary(),
            "application_notes": self._generate_application_notes(job_info),
            "created_at": datetime.now().isoformat()
        }
        
        # Save files
        saved_files = self.cv_generator.save_cv_files(cv_result)
        package["saved_files"] = saved_files
        
        # Save portfolio summary with professional naming
        portfolio_file = f"Portfolio_Summary_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(portfolio_file, 'w', encoding='utf-8') as f:
            f.write(package["portfolio_summary"])
        package["portfolio_file"] = portfolio_file
        
        # Create Notion entry for tracking
        notion_page_id = self.notion_manager.create_job_application_entry(
            job_info, 
            saved_files, 
            "Applied"
        )
        if notion_page_id:
            package["notion_page_id"] = notion_page_id
            self.logger.info(f"Job application tracked in Notion: {notion_page_id}")
        
        # Add to job application history
        application_id = self.history_manager.add_application(
            job_info,
            saved_files,
            "Applied",
            notion_page_id
        )
        if application_id:
            package["application_id"] = application_id
            self.logger.info(f"Job application added to history: {application_id}")
        
        self.logger.info(f"Application package created successfully")
        return package
    
    def handle_job_response(self, notion_page_id: str, response_type: str, details: Dict[str, Any]) -> bool:
        """Handle different types of job responses"""
        try:
            if response_type == "interview_invitation":
                # Schedule interview
                interview_date = details.get('interview_date')
                interview_type = details.get('interview_type', 'Phone')
                interviewer = details.get('interviewer', '')
                notes = details.get('notes', '')
                
                success = self.notion_manager.schedule_interview(
                    notion_page_id, interview_date, interview_type, interviewer, notes
                )
                
                if success:
                    self.logger.info(f"Interview scheduled for {interview_date}")
                    return True
                    
            elif response_type == "rejection":
                # Update status to rejected
                notes = details.get('notes', 'Thank you for considering my application')
                success = self.notion_manager.update_application_status(
                    notion_page_id, "Rejected", notes
                )
                
                if success:
                    self.logger.info("Application status updated to rejected")
                    return True
                    
            elif response_type == "offer":
                # Update status to offer received
                notes = details.get('notes', 'Offer received - reviewing details')
                success = self.notion_manager.update_application_status(
                    notion_page_id, "Offer Received", notes
                )
                
                if success:
                    self.logger.info("Application status updated to offer received")
                    return True
                    
            elif response_type == "follow_up_needed":
                # Add follow-up reminder
                follow_up_date = details.get('follow_up_date')
                follow_up_type = details.get('follow_up_type', 'Email')
                notes = details.get('notes', '')
                
                success = self.notion_manager.add_follow_up_reminder(
                    notion_page_id, follow_up_date, follow_up_type, notes
                )
                
                if success:
                    self.logger.info(f"Follow-up reminder added for {follow_up_date}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error handling job response: {e}")
            return False
    
    def get_job_search_analytics(self) -> Dict[str, Any]:
        """Get analytics about job search progress"""
        return self.notion_manager.get_job_search_analytics()
    
    def get_upcoming_follow_ups(self) -> List[Dict[str, Any]]:
        """Get upcoming follow-ups that need attention"""
        return self.notion_manager.get_upcoming_follow_ups()
    
    def get_job_application_history(self, limit: int = None, status_filter: str = None, 
                                  company_filter: str = None) -> List[Dict[str, Any]]:
        """Get job application history with optional filters"""
        return self.history_manager.get_application_history(limit, status_filter, company_filter)
    
    def get_application_statistics(self) -> Dict[str, Any]:
        """Get comprehensive job application statistics"""
        return self.history_manager.get_statistics()
    
    def get_application_summary(self) -> str:
        """Get a formatted summary of job applications"""
        return self.history_manager.get_application_summary()
    
    def search_applications(self, query: str) -> List[Dict[str, Any]]:
        """Search job applications by company, position, or notes"""
        return self.history_manager.search_applications(query)
    
    def get_application_by_id(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific application by ID"""
        return self.history_manager.get_application_by_id(application_id)
    
    def export_application_history(self, export_file: str = None) -> str:
        """Export job application history to a file"""
        return self.history_manager.export_history(export_file)
    
    def _generate_application_notes(self, job_info: Dict[str, Any]) -> str:
        """Generate application notes for entry-level position"""
        return f"""
        APPLICATION NOTES FOR: {job_info.get('title', 'Unknown')} at {job_info.get('company', 'Unknown')}
        
        🎯 KEY POINTS TO EMPHASIZE:
        1. Complete source code available on GitHub for all projects
        2. Live demos showing working applications
        3. Eagerness to learn and grow professionally
        4. Strong foundation in modern web technologies
        5. Experience with version control and deployment
        
        💼 WHY YOU'RE A GOOD FIT:
        • Fresh perspective and enthusiasm
        • Up-to-date knowledge of modern technologies
        • Proven ability to build complete applications
        • Strong problem-solving skills demonstrated through projects
        • Ready to contribute from day one
        
        📚 LEARNING GOALS:
        • Gain professional development experience
        • Learn from senior developers
        • Contribute to real-world projects
        • Improve code quality and best practices
        • Understand business requirements and user needs
        
        🚀 NEXT STEPS:
        1. Review the generated CV and customize if needed
        2. Prepare for technical interview with code walkthrough
        3. Be ready to discuss your GitHub projects in detail
        4. Show enthusiasm for learning and growth
        5. Demonstrate problem-solving approach
        """

def main():
    """Main function to run entry-level job application system"""
    print("🎯 ENTRY-LEVEL JOB APPLICATION SYSTEM")
    print("=" * 50)
    print("Optimized for first-time job seekers")
    print("Emphasizes code portfolio and realistic expectations")
    print()
    
    try:
        app_system = EntryLevelJobApplication()
        
        # Get entry-level job suggestions
        job_suggestions = app_system.get_entry_level_job_suggestions()
        
        print("📋 Available Entry-Level Positions:")
        for i, job in enumerate(job_suggestions, 1):
            print(f"{i}. {job['title']} at {job['company']}")
        
        print("\n🚀 Creating application package for first job suggestion...")
        
        # Create application package for first job
        package = app_system.create_application_package(job_suggestions[0])
        
        if package:
            print("✅ Entry-level application package created successfully!")
            print(f"📊 ATS Score: {package['cv_result']['ats_analysis']['overall_score']}/100")
            print(f"🎯 Job: {package['job_info']['title']} at {package['job_info']['company']}")
            
            print(f"\n📁 Files created:")
            for format_type, file_path in package['saved_files'].items():
                print(f"   • {format_type.upper()}: {os.path.basename(file_path)}")
            
            print(f"   • Portfolio Summary: {package['portfolio_file']}")
            
            print(f"\n💡 Key Features:")
            print("   • Realistic entry-level job titles")
            print("   • Emphasis on GitHub code portfolio")
            print("   • Honest representation of experience level")
            print("   • Focus on learning potential and growth")
            print("   • Complete source code availability")
            
            print(f"\n📝 Application Notes:")
            print(package['application_notes'])
            
        else:
            print("❌ Failed to create application package")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
