#!/usr/bin/env python3
"""
Enhanced Job Application Agent with ATS Optimization
Integrates ATS optimization with job application workflow

Features:
- ATS-optimized CV generation for each job
- Real-time ATS scoring and recommendations
- Job-specific keyword optimization
- Contact information validation
- Skill gap analysis
- Automated CV customization per job
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import AgentLogger
from utils.notifications import NotificationManager
from config import Config
from agents.ats_optimizer import ATSOptimizer, ATSOptimizationResult
from agents.job_application_agent import JobApplicationAgent

class EnhancedJobApplicationAgent(JobApplicationAgent):
    """Enhanced Job Application Agent with ATS optimization"""
    
    def __init__(self):
        """Initialize the Enhanced Job Application Agent"""
        super().__init__()
        
        # Initialize ATS optimizer
        self.ats_optimizer = ATSOptimizer()
        
        # ATS optimization settings
        self.ats_settings = {
            "min_ats_score": 70,  # Minimum ATS score to auto-apply
            "optimize_for_each_job": True,
            "generate_ats_reports": True,
            "save_optimized_cvs": True
        }
        
        self.logger.info("Enhanced Job Application Agent with ATS optimization initialized")
    
    def create_ats_optimized_application(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an ATS-optimized application for a specific job
        
        Args:
            job: Job information dictionary
            
        Returns:
            Enhanced application draft with ATS optimization
        """
        self.logger.info(f"Creating ATS-optimized application for: {job['title']} at {job['company']}")
        
        try:
            # Get current CV content
            cv_content = self._get_current_cv_content()
            
            # Perform ATS analysis
            ats_result = self.ats_optimizer.analyze_cv_for_ats(
                cv_content=cv_content,
                job_description=job.get('description', ''),
                job_title=job['title'],
                company=job['company']
            )
            
            # Check if ATS score meets minimum threshold
            if ats_result.overall_score < self.ats_settings["min_ats_score"]:
                self.logger.warning(f"ATS score {ats_result.overall_score} below threshold {self.ats_settings['min_ats_score']}")
                # Still create application but flag for review
                requires_manual_review = True
            else:
                requires_manual_review = False
            
            # Generate job-specific optimized CV
            optimized_cv = self._generate_job_specific_cv(cv_content, job, ats_result)
            
            # Create enhanced cover letter with ATS optimization
            cover_letter = self._generate_ats_optimized_cover_letter(job, ats_result)
            
            # Create application draft
            application_draft = {
                "job_id": f"{job['source']}_{job['company']}_{job['title']}".replace(" ", "_"),
                "job_title": job['title'],
                "company": job['company'],
                "location": job['location'],
                "source": job['source'],
                "job_url": job['url'],
                "cover_letter": cover_letter,
                "cv_version": "ats_optimized",
                "ats_score": ats_result.overall_score,
                "ats_breakdown": {
                    "contact_info": ats_result.contact_info_score,
                    "job_title_match": ats_result.job_title_match_score,
                    "skill_match": ats_result.skill_match_score,
                    "formatting": ats_result.formatting_score,
                    "readability": ats_result.readability_score,
                    "web_presence": ats_result.web_presence_score
                },
                "ats_recommendations": ats_result.recommendations,
                "missing_elements": ats_result.missing_elements,
                "keyword_suggestions": ats_result.keyword_suggestions,
                "optimized_cv": optimized_cv,
                "status": "draft",
                "created_at": datetime.now().isoformat(),
                "requires_approval": True,
                "requires_manual_review": requires_manual_review,
                "ats_optimization_completed": True
            }
            
            # Save ATS report if enabled
            if self.ats_settings["generate_ats_reports"]:
                report_filename = f"ats_report_{job['company']}_{job['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                self.ats_optimizer.save_ats_report(ats_result, report_filename)
                application_draft["ats_report_file"] = report_filename
            
            # Save optimized CV if enabled
            if self.ats_settings["save_optimized_cvs"]:
                cv_filename = f"optimized_cv_{job['company']}_{job['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                self._save_optimized_cv(optimized_cv, cv_filename)
                application_draft["optimized_cv_file"] = cv_filename
            
            self.logger.info(f"ATS-optimized application created successfully for {job['company']}")
            self.logger.info(f"ATS Score: {ats_result.overall_score}/100")
            
            return application_draft
            
        except Exception as e:
            self.logger.error(f"Error creating ATS-optimized application: {e}")
            # Fallback to regular application
            return self.create_application_draft(job)
    
    def _get_current_cv_content(self) -> str:
        """Get current CV content from file"""
        try:
            # Try to read from the most recent CV file
            cv_files = [
                "Abdallah Nasr Ali_Cv.pdf",
                "extracted_cv_content.txt",
                "professional_cv_content.txt"
            ]
            
            for cv_file in cv_files:
                if os.path.exists(cv_file):
                    if cv_file.endswith('.pdf'):
                        # For PDF files, we'll use a simplified approach
                        return self._read_pdf_cv(cv_file)
                    else:
                        with open(cv_file, 'r', encoding='utf-8') as f:
                            return f.read()
            
            # Fallback to a basic CV template
            return self._get_basic_cv_template()
            
        except Exception as e:
            self.logger.error(f"Error reading CV content: {e}")
            return self._get_basic_cv_template()
    
    def _read_pdf_cv(self, pdf_file: str) -> str:
        """Read PDF CV content (simplified version)"""
        try:
            import PyPDF2
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except ImportError:
            self.logger.warning("PyPDF2 not available, using basic template")
            return self._get_basic_cv_template()
        except Exception as e:
            self.logger.error(f"Error reading PDF: {e}")
            return self._get_basic_cv_template()
    
    def _get_basic_cv_template(self) -> str:
        """Get basic CV template as fallback"""
        return """
        ABDALLAH NASR ALI
        Full Stack Developer
        
        Email: body16nasr16bn@gmail.com
        Phone: +20 106 950 9757
        Location: Cairo, Egypt
        LinkedIn: https://linkedin.com/in/abdallah-nasr-ali
        GitHub: https://github.com/AbdalahNasr
        Portfolio: https://my-v3-potfolio.vercel.app
        
        SUMMARY
        Passionate Full Stack Developer with expertise in modern web technologies.
        Experienced in building responsive web applications, RESTful APIs, and user-friendly interfaces.
        Strong problem-solving skills and ability to work in fast-paced environments.
        
        EXPERIENCE
        Full Stack Developer Intern - Link Data Center (2024 - Present)
        Working on web application development using modern technologies and best practices.
        
        Frontend Developer - Freelance (2023 - Present)
        Building responsive websites and web applications for various clients.
        
        EDUCATION
        Bachelor's in Computer Science - University (2020 - 2024)
        Focused on software engineering and web development.
        
        SKILLS
        Frontend: React, Angular, Vue.js, JavaScript, TypeScript, HTML5, CSS3, Tailwind CSS
        Backend: Node.js, Python, Java, PHP, Express.js, Django, Spring Boot, Laravel
        Database: MongoDB, MySQL, PostgreSQL, Redis, SQLite
        Tools: Git, Docker, AWS, Vercel, Netlify, Postman, VS Code
        Other: RESTful APIs, GraphQL, JWT, OAuth, CI/CD, Agile, Scrum
        
        PROJECTS
        E-commerce Demo - React Storefront
        A modern e-commerce platform built with React, featuring product catalog, shopping cart, and user authentication.
        Code: https://github.com/AbdalahNasr/E-commerce-demo
        Live Demo: https://abdalahnasr.github.io/E-commerce-demo/
        
        ISTQP Quiz App - Quiz Platform
        A comprehensive quiz application with multilingual support, built using Next.js and TypeScript.
        Code: https://github.com/AbdalahNasr/istqp-quiz
        Live Demo: https://istqp-quiz.vercel.app
        
        CERTIFICATES
        Foundations of UX Design - Google (2024)
        React Basics - Google (2024)
        Full Stack Web Development - Route Academy (2023)
        Angular Developer Internship - Link Data Center (2024)
        
        LANGUAGES
        English - Upper Intermediate
        Arabic - Native
        """
    
    def _generate_job_specific_cv(self, cv_content: str, job: Dict[str, Any], 
                                 ats_result: ATSOptimizationResult) -> str:
        """Generate job-specific optimized CV"""
        try:
            prompt = f"""
            Optimize this CV specifically for the following job:
            
            Job Title: {job['title']}
            Company: {job['company']}
            Job Description: {job.get('description', 'Not provided')}
            
            Current CV:
            {cv_content}
            
            ATS Analysis Results:
            - Overall Score: {ats_result.overall_score}/100
            - Missing Elements: {', '.join(ats_result.missing_elements[:5])}
            - Keyword Suggestions: {', '.join(ats_result.keyword_suggestions[:10])}
            
            Please optimize the CV by:
            1. Including the exact job title in the summary
            2. Adding missing keywords from the job description
            3. Emphasizing relevant skills and experience
            4. Including measurable results and achievements
            5. Ensuring ATS-friendly formatting
            6. Addressing any missing contact information
            
            Return the optimized CV content.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert CV optimizer specializing in ATS compatibility and job-specific customization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            optimized_cv = response.choices[0].message.content.strip()
            self.logger.info("Job-specific CV optimization completed")
            return optimized_cv
            
        except Exception as e:
            self.logger.error(f"Error generating job-specific CV: {e}")
            return ats_result.optimized_cv  # Fallback to general optimization
    
    def _generate_ats_optimized_cover_letter(self, job: Dict[str, Any], 
                                           ats_result: ATSOptimizationResult) -> str:
        """Generate ATS-optimized cover letter"""
        try:
            prompt = f"""
            Write an ATS-optimized cover letter for the following job:
            
            Job Title: {job['title']}
            Company: {job['company']}
            Location: {job['location']}
            Job Description: {job.get('description', 'Not provided')}
            
            ATS Optimization Notes:
            - Include relevant keywords from the job description
            - Mention specific skills and technologies
            - Include measurable achievements
            - Keep paragraphs under 40 words for readability
            - Use professional, positive language
            
            Candidate Profile:
            - Full Stack Developer with React, Angular, Node.js experience
            - Experience with modern web technologies and frameworks
            - Strong problem-solving and collaboration skills
            - Portfolio: https://my-v3-potfolio.vercel.app
            - GitHub: https://github.com/AbdalahNasr
            
            Write a compelling, ATS-friendly cover letter that:
            1. Shows enthusiasm for the specific role
            2. Highlights relevant technical skills
            3. Includes keywords from the job description
            4. Demonstrates value proposition
            5. Is concise and professional (max 300 words)
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional cover letter writer specializing in ATS optimization and technical roles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            cover_letter = response.choices[0].message.content.strip()
            self.logger.info("ATS-optimized cover letter generated")
            return cover_letter
            
        except Exception as e:
            self.logger.error(f"Error generating ATS-optimized cover letter: {e}")
            return self._generate_cover_letter(job)  # Fallback to regular cover letter
    
    def _save_optimized_cv(self, cv_content: str, filename: str) -> None:
        """Save optimized CV to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(cv_content)
            self.logger.info(f"Optimized CV saved to: {filename}")
        except Exception as e:
            self.logger.error(f"Error saving optimized CV: {e}")
    
    def send_enhanced_approval_notification(self, draft: Dict[str, Any]) -> None:
        """Send enhanced approval notification with ATS details"""
        subject = f"🎯 ATS-Optimized Application Ready - {draft['job_title']} at {draft['company']}"
        
        ats_score = draft.get('ats_score', 0)
        ats_breakdown = draft.get('ats_breakdown', {})
        
        message = f"""
        🎯 ATS-OPTIMIZED JOB APPLICATION READY FOR REVIEW
        
        Job Details:
        • Position: {draft['job_title']}
        • Company: {draft['company']}
        • Location: {draft['location']}
        • Source: {draft['source']}
        
        📊 ATS OPTIMIZATION RESULTS:
        • Overall ATS Score: {ats_score}/100
        • Contact Information: {ats_breakdown.get('contact_info', 0)}/100
        • Job Title Match: {ats_breakdown.get('job_title_match', 0)}/100
        • Skill Matching: {ats_breakdown.get('skill_match', 0)}/100
        • Formatting: {ats_breakdown.get('formatting', 0)}/100
        • Readability: {ats_breakdown.get('readability', 0)}/100
        • Web Presence: {ats_breakdown.get('web_presence', 0)}/100
        
        🔧 KEY OPTIMIZATIONS APPLIED:
        """
        
        # Add top recommendations
        recommendations = draft.get('ats_recommendations', [])[:5]
        for i, rec in enumerate(recommendations, 1):
            message += f"        {i}. {rec}\n"
        
        # Add missing elements if any
        missing_elements = draft.get('missing_elements', [])
        if missing_elements:
            message += f"""
        
        ⚠️  MISSING ELEMENTS TO ADDRESS:
        """
            for element in missing_elements[:3]:
                message += f"        • {element}\n"
        
        # Add keyword suggestions
        keyword_suggestions = draft.get('keyword_suggestions', [])
        if keyword_suggestions:
            message += f"""
        
        🎯 KEYWORD SUGGESTIONS:
        """
            for keyword in keyword_suggestions[:5]:
                message += f"        • {keyword}\n"
        
        message += f"""
        
        📁 FILES GENERATED:
        • Application Draft: {draft.get('filepath', 'Not saved')}
        • ATS Report: {draft.get('ats_report_file', 'Not generated')}
        • Optimized CV: {draft.get('optimized_cv_file', 'Not generated')}
        
        🔗 Job URL: {draft['job_url']}
        
        {'⚠️  MANUAL REVIEW REQUIRED - ATS Score below threshold' if draft.get('requires_manual_review', False) else '✅ READY FOR APPLICATION - ATS Score meets threshold'}
        
        ---
        This application has been optimized for ATS compatibility and job-specific requirements.
        """
        
        # Send notification
        self.notifications.notify(message, "INFO", subject=subject)
        self.logger.info(f"Enhanced approval notification sent for {draft['company']}")
    
    def run_enhanced_job_search(self, keywords: List[str] = None, 
                               location: str = "Cairo, Egypt") -> List[Dict[str, Any]]:
        """Run enhanced job search with ATS optimization"""
        self.logger.info("Starting enhanced job search with ATS optimization")
        
        try:
            # Search for jobs using parent class method
            jobs = self.search_jobs(keywords, location)
            
            if not jobs:
                self.logger.warning("No jobs found matching criteria")
                return []
            
            # Create ATS-optimized application drafts
            drafts = []
            for job in jobs[:3]:  # Limit to first 3 jobs for testing
                draft = self.create_ats_optimized_application(job)
                if draft:
                    # Save draft
                    filepath = self.save_application_draft(draft)
                    if filepath:
                        draft['filepath'] = filepath
                        drafts.append(draft)
                        
                        # Send enhanced approval notification
                        self.send_enhanced_approval_notification(draft)
            
            self.logger.info(f"Created {len(drafts)} ATS-optimized application drafts")
            return drafts
            
        except Exception as e:
            self.logger.error(f"Error in enhanced job search process: {e}")
            return []
    
    def get_ats_statistics(self, drafts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get ATS optimization statistics from application drafts"""
        if not drafts:
            return {}
        
        scores = [draft.get('ats_score', 0) for draft in drafts]
        
        stats = {
            "total_applications": len(drafts),
            "average_ats_score": sum(scores) / len(scores) if scores else 0,
            "highest_ats_score": max(scores) if scores else 0,
            "lowest_ats_score": min(scores) if scores else 0,
            "applications_above_threshold": len([s for s in scores if s >= self.ats_settings["min_ats_score"]]),
            "applications_requiring_review": len([d for d in drafts if d.get('requires_manual_review', False)]),
            "common_missing_elements": self._get_common_missing_elements(drafts),
            "top_keyword_suggestions": self._get_top_keyword_suggestions(drafts)
        }
        
        return stats
    
    def _get_common_missing_elements(self, drafts: List[Dict[str, Any]]) -> List[str]:
        """Get most common missing elements across all drafts"""
        all_missing = []
        for draft in drafts:
            all_missing.extend(draft.get('missing_elements', []))
        
        # Count occurrences
        from collections import Counter
        element_counts = Counter(all_missing)
        
        return [element for element, count in element_counts.most_common(5)]
    
    def _get_top_keyword_suggestions(self, drafts: List[Dict[str, Any]]) -> List[str]:
        """Get top keyword suggestions across all drafts"""
        all_keywords = []
        for draft in drafts:
            all_keywords.extend(draft.get('keyword_suggestions', []))
        
        # Count occurrences
        from collections import Counter
        keyword_counts = Counter(all_keywords)
        
        return [keyword for keyword, count in keyword_counts.most_common(10)]

def main():
    """Main function to run the enhanced job application agent"""
    print("🎯 ENHANCED JOB APPLICATION AGENT WITH ATS OPTIMIZATION")
    print("=" * 60)
    
    try:
        agent = EnhancedJobApplicationAgent()
        
        print("✅ Enhanced agent initialized successfully!")
        print("🔧 ATS Optimization Features:")
        print("   • Real-time ATS scoring and analysis")
        print("   • Job-specific CV optimization")
        print("   • Contact information validation")
        print("   • Skill gap analysis")
        print("   • Keyword optimization")
        print("   • Automated recommendations")
        print()
        
        # Run enhanced job search
        drafts = agent.run_enhanced_job_search(
            keywords=["full stack developer", "frontend developer", "react developer"],
            location="Cairo, Egypt"
        )
        
        if drafts:
            print(f"🎉 Enhanced job search completed successfully!")
            print(f"📝 Created {len(drafts)} ATS-optimized application drafts")
            
            # Get and display ATS statistics
            stats = agent.get_ats_statistics(drafts)
            print(f"\n📊 ATS OPTIMIZATION STATISTICS:")
            print(f"   • Average ATS Score: {stats.get('average_ats_score', 0):.1f}/100")
            print(f"   • Applications Above Threshold: {stats.get('applications_above_threshold', 0)}")
            print(f"   • Applications Requiring Review: {stats.get('applications_requiring_review', 0)}")
            
            if stats.get('common_missing_elements'):
                print(f"   • Common Missing Elements: {', '.join(stats['common_missing_elements'][:3])}")
            
            print(f"\n📁 Files created:")
            for draft in drafts:
                print(f"   • {draft['job_title']} at {draft['company']}")
                print(f"     ATS Score: {draft.get('ats_score', 0)}/100")
                print(f"     Files: {draft.get('filepath', 'N/A')}")
                if draft.get('ats_report_file'):
                    print(f"     ATS Report: {draft['ats_report_file']}")
                if draft.get('optimized_cv_file'):
                    print(f"     Optimized CV: {draft['optimized_cv_file']}")
                print()
            
            print("📧 Check your email for detailed ATS optimization reports!")
        else:
            print("❌ No application drafts created")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
