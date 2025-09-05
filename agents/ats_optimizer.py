#!/usr/bin/env python3
"""
ATS Optimizer - Comprehensive ATS Optimization Module
Integrates with job application agent to optimize CVs for ATS systems

Features:
- Contact information validation and optimization
- Job title matching and keyword optimization
- Date formatting standardization
- Skill matching and gap analysis
- Paragraph length optimization
- Web presence validation
- Font and layout optimization
- ATS compatibility scoring
"""

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import AgentLogger
from config import Config

@dataclass
class ATSOptimizationResult:
    """Result of ATS optimization analysis"""
    overall_score: int
    contact_info_score: int
    job_title_match_score: int
    skill_match_score: int
    formatting_score: int
    readability_score: int
    web_presence_score: int
    recommendations: List[str]
    optimized_cv: str
    missing_elements: List[str]
    keyword_suggestions: List[str]

class ATSOptimizer:
    """Comprehensive ATS optimization system"""
    
    def __init__(self):
        """Initialize the ATS Optimizer"""
        load_dotenv('config.env')
        
        self.logger = AgentLogger("ats_optimizer")
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # ATS optimization rules and standards
        self.ats_standards = {
            "contact_info": {
                "required_fields": ["email", "phone", "address"],
                "email_pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "phone_pattern": r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                "address_indicators": ["street", "avenue", "road", "city", "state", "zip", "country"]
            },
            "date_formats": [
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{2}/\d{4}',        # MM/YYYY
                r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b',  # Month YYYY
                r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'  # Full Month YYYY
            ],
            "section_headings": [
                "summary", "experience", "education", "skills", "projects", 
                "certificates", "languages", "contact", "objective"
            ],
            "paragraph_length": {
                "max_words": 40,
                "recommended_words": 25
            },
            "font_standards": {
                "recommended_fonts": ["Arial", "Calibri", "Times New Roman", "Helvetica"],
                "min_size": 10,
                "max_size": 12
            }
        }
        
        # Common ATS keywords by industry
        self.industry_keywords = {
            "software_development": [
                "software development", "programming", "coding", "debugging", "testing",
                "agile", "scrum", "version control", "git", "ci/cd", "devops",
                "api", "rest", "graphql", "microservices", "cloud computing"
            ],
            "web_development": [
                "frontend", "backend", "full stack", "responsive design", "user experience",
                "html", "css", "javascript", "react", "angular", "vue", "node.js",
                "database", "sql", "mongodb", "postgresql", "mysql"
            ],
            "mobile_development": [
                "mobile development", "ios", "android", "react native", "flutter",
                "swift", "kotlin", "java", "mobile app", "cross platform"
            ],
            "data_science": [
                "data analysis", "machine learning", "python", "r", "sql", "statistics",
                "data visualization", "pandas", "numpy", "scikit-learn", "tensorflow"
            ]
        }
        
        self.logger.info("ATS Optimizer initialized successfully")
    
    def analyze_cv_for_ats(self, cv_content: str, job_description: str = None, 
                          job_title: str = None, company: str = None) -> ATSOptimizationResult:
        """
        Comprehensive ATS analysis of CV content
        
        Args:
            cv_content: CV text content
            job_description: Job description text (optional)
            job_title: Target job title (optional)
            company: Company name (optional)
            
        Returns:
            ATSOptimizationResult with scores and recommendations
        """
        self.logger.info("Starting comprehensive ATS analysis")
        
        # Analyze different aspects
        contact_score, contact_issues = self._analyze_contact_information(cv_content)
        job_title_score, job_title_issues = self._analyze_job_title_match(cv_content, job_title)
        skill_score, skill_issues = self._analyze_skill_matching(cv_content, job_description)
        format_score, format_issues = self._analyze_formatting(cv_content)
        readability_score, readability_issues = self._analyze_readability(cv_content)
        web_presence_score, web_issues = self._analyze_web_presence(cv_content)
        
        # Calculate overall score
        scores = [contact_score, job_title_score, skill_score, format_score, readability_score, web_presence_score]
        overall_score = sum(scores) // len(scores)
        
        # Collect all issues and recommendations
        all_issues = contact_issues + job_title_issues + skill_issues + format_issues + readability_issues + web_issues
        recommendations = self._generate_recommendations(all_issues, cv_content, job_description)
        
        # Generate optimized CV
        optimized_cv = self._optimize_cv_content(cv_content, recommendations, job_description)
        
        # Generate keyword suggestions
        keyword_suggestions = self._generate_keyword_suggestions(cv_content, job_description)
        
        result = ATSOptimizationResult(
            overall_score=overall_score,
            contact_info_score=contact_score,
            job_title_match_score=job_title_score,
            skill_match_score=skill_score,
            formatting_score=format_score,
            readability_score=readability_score,
            web_presence_score=web_presence_score,
            recommendations=recommendations,
            optimized_cv=optimized_cv,
            missing_elements=all_issues,
            keyword_suggestions=keyword_suggestions
        )
        
        self.logger.info(f"ATS analysis completed. Overall score: {overall_score}/100")
        return result
    
    def _analyze_contact_information(self, cv_content: str) -> Tuple[int, List[str]]:
        """Analyze contact information completeness and format"""
        issues = []
        score = 100
        
        # Check for email
        email_match = re.search(self.ats_standards["contact_info"]["email_pattern"], cv_content)
        if not email_match:
            issues.append("Email address not found in resume")
            score -= 30
        else:
            self.logger.info(f"Email found: {email_match.group()}")
        
        # Check for phone number
        phone_match = re.search(self.ats_standards["contact_info"]["phone_pattern"], cv_content)
        if not phone_match:
            issues.append("Phone number not found in resume")
            score -= 25
        else:
            self.logger.info(f"Phone found: {phone_match.group()}")
        
        # Check for address
        has_address = any(indicator in cv_content.lower() for indicator in 
                         self.ats_standards["contact_info"]["address_indicators"])
        if not has_address:
            issues.append("Address not found in resume")
            score -= 20
        
        # Check for LinkedIn URL
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, cv_content, re.IGNORECASE)
        if not linkedin_match:
            issues.append("LinkedIn profile URL not found")
            score -= 15
        else:
            self.logger.info(f"LinkedIn found: {linkedin_match.group()}")
        
        # Check for GitHub URL
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, cv_content, re.IGNORECASE)
        if not github_match:
            issues.append("GitHub profile URL not found")
            score -= 10
        
        return max(0, score), issues
    
    def _analyze_job_title_match(self, cv_content: str, job_title: str = None) -> Tuple[int, List[str]]:
        """Analyze job title matching"""
        issues = []
        score = 100
        
        if not job_title:
            return score, issues
        
        job_title_lower = job_title.lower()
        cv_lower = cv_content.lower()
        
        # Check if exact job title appears in CV
        if job_title_lower not in cv_lower:
            issues.append(f"Job title '{job_title}' not found in resume")
            score -= 40
            
            # Check for similar titles
            title_words = job_title_lower.split()
            matches = sum(1 for word in title_words if word in cv_lower)
            if matches > 0:
                score += (matches / len(title_words)) * 20
                issues.append(f"Only {matches}/{len(title_words)} words from job title found")
        
        # Check for job title in summary section
        summary_section = self._extract_section(cv_content, "summary")
        if summary_section and job_title_lower not in summary_section.lower():
            issues.append("Job title not mentioned in summary section")
            score -= 15
        
        return max(0, score), issues
    
    def _analyze_skill_matching(self, cv_content: str, job_description: str = None) -> Tuple[int, List[str]]:
        """Analyze skill matching between CV and job description"""
        issues = []
        score = 100
        
        if not job_description:
            return score, issues
        
        # Extract skills from job description
        job_skills = self._extract_skills_from_text(job_description)
        cv_skills = self._extract_skills_from_text(cv_content)
        
        # Find missing skills
        missing_skills = []
        for skill in job_skills:
            if not any(skill.lower() in cv_skill.lower() for cv_skill in cv_skills):
                missing_skills.append(skill)
        
        if missing_skills:
            issues.append(f"Missing skills from job description: {', '.join(missing_skills[:5])}")
            score -= min(50, len(missing_skills) * 5)
        
        # Check for measurable results
        measurable_patterns = [
            r'\d+%', r'\d+\+', r'\$\d+', r'\d+\s*(years?|months?)',
            r'increased by \d+', r'reduced by \d+', r'improved by \d+'
        ]
        
        measurable_count = sum(len(re.findall(pattern, cv_content, re.IGNORECASE)) 
                              for pattern in measurable_patterns)
        
        if measurable_count < 5:
            issues.append(f"Only {measurable_count} measurable results found (recommended: 5+)")
            score -= 10
        
        return max(0, score), issues
    
    def _analyze_formatting(self, cv_content: str) -> Tuple[int, List[str]]:
        """Analyze CV formatting for ATS compatibility"""
        issues = []
        score = 100
        
        # Check date formatting
        date_patterns = self.ats_standards["date_formats"]
        dates_found = []
        for pattern in date_patterns:
            dates_found.extend(re.findall(pattern, cv_content, re.IGNORECASE))
        
        if not dates_found:
            issues.append("No properly formatted dates found")
            score -= 20
        else:
            self.logger.info(f"Found {len(dates_found)} properly formatted dates")
        
        # Check for tables (not ATS-friendly)
        if '<table' in cv_content.lower() or '|' in cv_content and cv_content.count('|') > 10:
            issues.append("Tables detected - may not be ATS-friendly")
            score -= 15
        
        # Check for images
        if '<img' in cv_content.lower() or 'image' in cv_content.lower():
            issues.append("Images detected - not ATS-friendly")
            score -= 20
        
        # Check for headers/footers
        if 'header' in cv_content.lower() or 'footer' in cv_content.lower():
            issues.append("Headers/footers detected - may cause ATS issues")
            score -= 10
        
        # Check section headings
        section_headings = self.ats_standards["section_headings"]
        found_sections = []
        for section in section_headings:
            if section in cv_content.lower():
                found_sections.append(section)
        
        if len(found_sections) < 4:
            issues.append(f"Only {len(found_sections)} standard sections found")
            score -= 15
        
        return max(0, score), issues
    
    def _analyze_readability(self, cv_content: str) -> Tuple[int, List[str]]:
        """Analyze CV readability and paragraph length"""
        issues = []
        score = 100
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in cv_content.split('\n\n') if p.strip()]
        
        long_paragraphs = []
        for i, paragraph in enumerate(paragraphs):
            word_count = len(paragraph.split())
            if word_count > self.ats_standards["paragraph_length"]["max_words"]:
                long_paragraphs.append(f"Paragraph {i+1}: {word_count} words")
        
        if long_paragraphs:
            issues.append(f"Long paragraphs found: {', '.join(long_paragraphs[:3])}")
            score -= min(30, len(long_paragraphs) * 5)
        
        # Check for negative phrases
        negative_phrases = [
            "unfortunately", "failed", "mistake", "error", "problem",
            "difficult", "struggled", "weak", "limited", "lack"
        ]
        
        negative_found = []
        for phrase in negative_phrases:
            if phrase in cv_content.lower():
                negative_found.append(phrase)
        
        if negative_found:
            issues.append(f"Negative phrases found: {', '.join(negative_found)}")
            score -= 15
        
        return max(0, score), issues
    
    def _analyze_web_presence(self, cv_content: str) -> Tuple[int, List[str]]:
        """Analyze web presence and professional URLs"""
        issues = []
        score = 100
        
        # Check for LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        if not re.search(linkedin_pattern, cv_content, re.IGNORECASE):
            issues.append("LinkedIn profile URL not found")
            score -= 30
        
        # Check for GitHub
        github_pattern = r'github\.com/[\w-]+'
        if not re.search(github_pattern, cv_content, re.IGNORECASE):
            issues.append("GitHub profile URL not found")
            score -= 25
        
        # Check for portfolio website
        portfolio_patterns = [
            r'https?://[\w.-]+\.(com|net|org|io|dev)',
            r'portfolio', r'website', r'personal site'
        ]
        
        has_portfolio = any(re.search(pattern, cv_content, re.IGNORECASE) 
                           for pattern in portfolio_patterns)
        
        if not has_portfolio:
            issues.append("Portfolio website not found")
            score -= 20
        
        # Check for professional email domain
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cv_content)
        if email_match:
            email_domain = email_match.group().split('@')[1]
            unprofessional_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
            if email_domain.lower() in unprofessional_domains:
                issues.append(f"Consider using a professional email domain instead of {email_domain}")
                score -= 10
        
        return max(0, score), issues
    
    def _extract_section(self, cv_content: str, section_name: str) -> str:
        """Extract a specific section from CV content"""
        lines = cv_content.split('\n')
        section_content = []
        in_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            if line_lower == section_name.lower():
                in_section = True
                continue
            elif in_section and line_lower in [s.lower() for s in self.ats_standards["section_headings"]]:
                break
            elif in_section:
                section_content.append(line)
        
        return '\n'.join(section_content)
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        # Common technical skills patterns
        skill_patterns = [
            r'\b(?:JavaScript|Python|Java|C\+\+|C#|PHP|Ruby|Go|Swift|Kotlin)\b',
            r'\b(?:React|Angular|Vue|Node\.js|Express|Django|Flask|Laravel|Spring)\b',
            r'\b(?:HTML|CSS|SQL|MongoDB|PostgreSQL|MySQL|Redis)\b',
            r'\b(?:Git|Docker|AWS|Azure|GCP|Kubernetes|Jenkins)\b',
            r'\b(?:Agile|Scrum|DevOps|CI/CD|REST|GraphQL|Microservices)\b'
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        
        return list(skills)
    
    def _generate_recommendations(self, issues: List[str], cv_content: str, 
                                 job_description: str = None) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        for issue in issues:
            if "Email address not found" in issue:
                recommendations.append("Add a professional email address in the contact section")
            elif "Phone number not found" in issue:
                recommendations.append("Include a phone number in the contact information")
            elif "Address not found" in issue:
                recommendations.append("Add your location/address for recruiter validation")
            elif "LinkedIn profile URL not found" in issue:
                recommendations.append("Include your LinkedIn profile URL to build web credibility")
            elif "GitHub profile URL not found" in issue:
                recommendations.append("Add your GitHub profile URL to showcase your code")
            elif "Job title" in issue and "not found" in issue:
                recommendations.append("Include the exact job title in your resume, preferably in the summary")
            elif "Missing skills" in issue:
                recommendations.append("Add missing skills from the job description to your skills section")
            elif "Long paragraphs" in issue:
                recommendations.append("Shorten paragraphs to under 40 words for better readability")
            elif "Negative phrases" in issue:
                recommendations.append("Remove negative language and focus on positive achievements")
            elif "Tables detected" in issue:
                recommendations.append("Remove tables and use simple text formatting for ATS compatibility")
            elif "Images detected" in issue:
                recommendations.append("Remove images as they are not ATS-friendly")
            elif "No properly formatted dates" in issue:
                recommendations.append("Use standard date formats: MM/YYYY, Month YYYY, or MM/DD/YYYY")
            elif "Portfolio website not found" in issue:
                recommendations.append("Add a link to your portfolio website or GitHub profile")
        
        # Add general ATS recommendations
        recommendations.extend([
            "Use standard section headings: Summary, Experience, Education, Skills, Projects",
            "Include 5+ measurable results with numbers and percentages",
            "Use a clean, simple font like Arial or Calibri",
            "Keep the resume to 1-2 pages maximum",
            "Use bullet points for easy scanning",
            "Include relevant keywords from the job description"
        ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _optimize_cv_content(self, cv_content: str, recommendations: List[str], 
                           job_description: str = None) -> str:
        """Generate optimized CV content based on recommendations"""
        try:
            prompt = f"""
            Optimize this CV content for ATS (Applicant Tracking System) compatibility:
            
            Current CV:
            {cv_content}
            
            Job Description (if provided):
            {job_description or "Not provided"}
            
            Key optimization requirements:
            1. Ensure all contact information is present and properly formatted
            2. Include relevant keywords from the job description
            3. Use standard date formats (MM/YYYY or Month YYYY)
            4. Keep paragraphs under 40 words
            5. Use standard section headings
            6. Include measurable results with numbers
            7. Remove any negative language
            8. Ensure ATS-friendly formatting (no tables, images, or complex layouts)
            
            Return the optimized CV content that addresses these requirements.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an ATS optimization expert. Optimize CVs for maximum ATS compatibility while maintaining professional quality."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            optimized_content = response.choices[0].message.content.strip()
            self.logger.info("CV content optimized using AI")
            return optimized_content
            
        except Exception as e:
            self.logger.error(f"Error optimizing CV with AI: {e}")
            return cv_content  # Return original if optimization fails
    
    def _generate_keyword_suggestions(self, cv_content: str, job_description: str = None) -> List[str]:
        """Generate keyword suggestions for better ATS matching"""
        suggestions = []
        
        if not job_description:
            return suggestions
        
        # Extract keywords from job description
        job_keywords = self._extract_skills_from_text(job_description)
        cv_keywords = self._extract_skills_from_text(cv_content)
        
        # Find missing keywords
        missing_keywords = [kw for kw in job_keywords if kw.lower() not in cv_content.lower()]
        suggestions.extend(missing_keywords[:10])  # Top 10 missing keywords
        
        # Add industry-specific suggestions
        if any(word in job_description.lower() for word in ["software", "developer", "programming"]):
            suggestions.extend(["software development", "programming", "coding", "debugging"])
        
        if any(word in job_description.lower() for word in ["web", "frontend", "backend"]):
            suggestions.extend(["web development", "responsive design", "user experience"])
        
        return list(set(suggestions))  # Remove duplicates
    
    def generate_ats_report(self, result: ATSOptimizationResult) -> str:
        """Generate a comprehensive ATS optimization report"""
        report = f"""
ATS OPTIMIZATION REPORT
{'=' * 50}

OVERALL SCORE: {result.overall_score}/100

DETAILED SCORES:
• Contact Information: {result.contact_info_score}/100
• Job Title Match: {result.job_title_match_score}/100
• Skill Matching: {result.skill_match_score}/100
• Formatting: {result.formatting_score}/100
• Readability: {result.readability_score}/100
• Web Presence: {result.web_presence_score}/100

MISSING ELEMENTS:
"""
        
        for issue in result.missing_elements:
            report += f"• {issue}\n"
        
        report += f"""
KEYWORD SUGGESTIONS:
"""
        
        for keyword in result.keyword_suggestions[:10]:
            report += f"• {keyword}\n"
        
        report += f"""
RECOMMENDATIONS:
"""
        
        for i, rec in enumerate(result.recommendations[:15], 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
OPTIMIZED CV CONTENT:
{result.optimized_cv}

---
Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def save_ats_report(self, result: ATSOptimizationResult, filename: str = None) -> str:
        """Save ATS optimization report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ats_optimization_report_{timestamp}.txt"
        
        report = self.generate_ats_report(result)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"ATS report saved to: {filename}")
        return filename

def main():
    """Test the ATS Optimizer"""
    print("ATS OPTIMIZER - Testing Module")
    print("=" * 40)
    
    # Sample CV content for testing
    sample_cv = """
    ABDALLAH NASR ALI
    Full Stack Developer
    
    Email: body16nasr16bn@gmail.com
    Phone: +20 106 950 9757
    Location: Cairo, Egypt
    GitHub: https://github.com/AbdalahNasr
    Portfolio: https://my-v3-potfolio.vercel.app
    
    SUMMARY
    Passionate Full Stack Developer with expertise in modern web technologies.
    Experienced in building responsive web applications and RESTful APIs.
    
    EXPERIENCE
    Full Stack Developer Intern - Link Data Center (2024 - Present)
    Working on web application development using modern technologies.
    
    Frontend Developer - Freelance (2023 - Present)
    Building responsive websites for various clients.
    
    EDUCATION
    Bachelor's in Computer Science - University (2020 - 2024)
    Focused on software engineering and web development.
    
    SKILLS
    Frontend: React, Angular, JavaScript, TypeScript, HTML5, CSS3
    Backend: Node.js, Python, Express.js, Django
    Database: MongoDB, MySQL, PostgreSQL
    Tools: Git, Docker, AWS, Vercel
    """
    
    # Sample job description
    sample_job = """
    Senior Product Manager - Mobile Commerce
    
    We are looking for a Senior Product Manager to lead our mobile commerce initiatives.
    The ideal candidate will have experience with mobile platforms, product management,
    and customer experience. Experience with Android, iOS, and mobile commerce
    platforms is required. Strong technical background and management experience
    preferred.
    
    Requirements:
    - 5+ years product management experience
    - Experience with mobile platforms (Android, iOS)
    - Strong technical background
    - Customer experience focus
    - Mobile commerce experience
    """
    
    try:
        optimizer = ATSOptimizer()
        
        # Analyze CV
        result = optimizer.analyze_cv_for_ats(
            cv_content=sample_cv,
            job_description=sample_job,
            job_title="Senior Product Manager",
            company="Tech Company"
        )
        
        # Generate and save report
        report_file = optimizer.save_ats_report(result)
        
        print(f"✅ ATS analysis completed!")
        print(f"📊 Overall Score: {result.overall_score}/100")
        print(f"📄 Report saved to: {report_file}")
        print(f"🔧 Recommendations: {len(result.recommendations)}")
        print(f"🎯 Missing elements: {len(result.missing_elements)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
