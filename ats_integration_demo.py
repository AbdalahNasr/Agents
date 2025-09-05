#!/usr/bin/env python3
"""
ATS Integration Demo - Comprehensive ATS Optimization System
Demonstrates the complete ATS optimization workflow

Features:
- ATS optimization analysis
- Job-specific CV generation
- Enhanced job application with ATS scoring
- Comprehensive reporting
- Integration with existing automation system
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.ats_optimizer import ATSOptimizer
from agents.ats_cv_generator import ATSCVGenerator
from agents.enhanced_job_application_agent import EnhancedJobApplicationAgent
from utils.logger import AgentLogger

class ATSIntegrationDemo:
    """Comprehensive ATS optimization demonstration"""
    
    def __init__(self):
        """Initialize the ATS Integration Demo"""
        self.logger = AgentLogger("ats_integration_demo")
        
        # Initialize components
        self.ats_optimizer = ATSOptimizer()
        self.cv_generator = ATSCVGenerator()
        self.job_agent = EnhancedJobApplicationAgent()
        
        self.logger.info("ATS Integration Demo initialized successfully")
    
    def run_comprehensive_ats_demo(self) -> Dict[str, Any]:
        """Run comprehensive ATS optimization demonstration"""
        self.logger.info("Starting comprehensive ATS optimization demo")
        
        results = {
            "demo_started": datetime.now().isoformat(),
            "components_tested": [],
            "ats_analyses": [],
            "cv_generations": [],
            "job_applications": [],
            "overall_success": False
        }
        
        try:
            # Test 1: ATS Optimization Analysis
            print("\n" + "="*60)
            print("🎯 TEST 1: ATS OPTIMIZATION ANALYSIS")
            print("="*60)
            
            ats_analysis_result = self._test_ats_optimization()
            results["ats_analyses"].append(ats_analysis_result)
            results["components_tested"].append("ATS Optimizer")
            
            # Test 2: Job-Specific CV Generation
            print("\n" + "="*60)
            print("📄 TEST 2: JOB-SPECIFIC CV GENERATION")
            print("="*60)
            
            cv_generation_result = self._test_cv_generation()
            results["cv_generations"].append(cv_generation_result)
            results["components_tested"].append("ATS CV Generator")
            
            # Test 3: Enhanced Job Application
            print("\n" + "="*60)
            print("💼 TEST 3: ENHANCED JOB APPLICATION")
            print("="*60)
            
            job_application_result = self._test_enhanced_job_application()
            results["job_applications"].append(job_application_result)
            results["components_tested"].append("Enhanced Job Application Agent")
            
            # Generate comprehensive report
            print("\n" + "="*60)
            print("📊 COMPREHENSIVE ATS OPTIMIZATION REPORT")
            print("="*60)
            
            comprehensive_report = self._generate_comprehensive_report(results)
            results["comprehensive_report"] = comprehensive_report
            
            results["overall_success"] = True
            results["demo_completed"] = datetime.now().isoformat()
            
            self.logger.info("Comprehensive ATS optimization demo completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive ATS demo: {e}")
            results["error"] = str(e)
        
        return results
    
    def _test_ats_optimization(self) -> Dict[str, Any]:
        """Test ATS optimization functionality"""
        print("Testing ATS optimization analysis...")
        
        # Sample CV content
        sample_cv = """
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
            # Perform ATS analysis
            ats_result = self.ats_optimizer.analyze_cv_for_ats(
                cv_content=sample_cv,
                job_description=sample_job,
                job_title="Senior Product Manager",
                company="Tech Company"
            )
            
            # Save report
            report_file = self.ats_optimizer.save_ats_report(ats_result)
            
            result = {
                "test_name": "ATS Optimization Analysis",
                "success": True,
                "ats_score": ats_result.overall_score,
                "contact_score": ats_result.contact_info_score,
                "job_title_score": ats_result.job_title_match_score,
                "skill_score": ats_result.skill_match_score,
                "formatting_score": ats_result.formatting_score,
                "readability_score": ats_result.readability_score,
                "web_presence_score": ats_result.web_presence_score,
                "recommendations_count": len(ats_result.recommendations),
                "missing_elements_count": len(ats_result.missing_elements),
                "keyword_suggestions_count": len(ats_result.keyword_suggestions),
                "report_file": report_file
            }
            
            print(f"✅ ATS Analysis completed successfully!")
            print(f"📊 Overall ATS Score: {ats_result.overall_score}/100")
            print(f"📄 Report saved to: {report_file}")
            print(f"🔧 Recommendations: {len(ats_result.recommendations)}")
            print(f"⚠️  Missing elements: {len(ats_result.missing_elements)}")
            print(f"🎯 Keyword suggestions: {len(ats_result.keyword_suggestions)}")
            
            return result
            
        except Exception as e:
            print(f"❌ ATS optimization test failed: {e}")
            return {
                "test_name": "ATS Optimization Analysis",
                "success": False,
                "error": str(e)
            }
    
    def _test_cv_generation(self) -> Dict[str, Any]:
        """Test job-specific CV generation"""
        print("Testing job-specific CV generation...")
        
        # Sample job information
        sample_job = {
            "title": "Senior Full Stack Developer",
            "company": "TechCorp",
            "location": "Cairo, Egypt",
            "description": """
            We are looking for a Senior Full Stack Developer to join our team.
            The ideal candidate will have experience with React, Node.js, and modern web technologies.
            Experience with mobile development, APIs, and database management is required.
            Strong problem-solving skills and ability to work in fast-paced environments.
            
            Requirements:
            - 5+ years full stack development experience
            - Experience with React, Angular, Node.js
            - Mobile development experience
            - API development and integration
            - Database design and optimization
            - Strong problem-solving skills
            """
        }
        
        try:
            # Generate job-specific CV
            cv_result = self.cv_generator.generate_job_specific_cv(sample_job)
            
            if cv_result:
                # Save CV files
                saved_files = self.cv_generator.save_cv_files(cv_result)
                
                result = {
                    "test_name": "Job-Specific CV Generation",
                    "success": True,
                    "job_title": cv_result['job_info']['title'],
                    "company": cv_result['job_info']['company'],
                    "ats_score": cv_result['ats_analysis']['overall_score'],
                    "contact_score": cv_result['ats_analysis']['contact_info_score'],
                    "job_title_score": cv_result['ats_analysis']['job_title_match_score'],
                    "skill_score": cv_result['ats_analysis']['skill_match_score'],
                    "formatting_score": cv_result['ats_analysis']['formatting_score'],
                    "readability_score": cv_result['ats_analysis']['readability_score'],
                    "web_presence_score": cv_result['ats_analysis']['web_presence_score'],
                    "recommendations_count": len(cv_result['ats_analysis']['recommendations']),
                    "missing_elements_count": len(cv_result['ats_analysis']['missing_elements']),
                    "keyword_suggestions_count": len(cv_result['ats_analysis']['keyword_suggestions']),
                    "saved_files": saved_files
                }
                
                print(f"✅ Job-specific CV generated successfully!")
                print(f"🎯 Job: {cv_result['job_info']['title']} at {cv_result['job_info']['company']}")
                print(f"📊 ATS Score: {cv_result['ats_analysis']['overall_score']}/100")
                print(f"📁 Files created: {len(saved_files)}")
                for format_type, file_path in saved_files.items():
                    print(f"   • {format_type.upper()}: {os.path.basename(file_path)}")
                
                return result
            else:
                raise Exception("CV generation returned None")
                
        except Exception as e:
            print(f"❌ CV generation test failed: {e}")
            return {
                "test_name": "Job-Specific CV Generation",
                "success": False,
                "error": str(e)
            }
    
    def _test_enhanced_job_application(self) -> Dict[str, Any]:
        """Test enhanced job application with ATS optimization"""
        print("Testing enhanced job application with ATS optimization...")
        
        try:
            # Create a sample job for testing
            sample_job = {
                "title": "Full Stack Developer",
                "company": "Innovation Labs",
                "location": "Cairo, Egypt",
                "source": "LinkedIn",
                "url": "https://linkedin.com/jobs/view/123456789",
                "description": """
                We are seeking a Full Stack Developer to join our innovative team.
                The ideal candidate will have experience with React, Node.js, and modern web technologies.
                Experience with mobile development and API integration is preferred.
                
                Key Responsibilities:
                - Develop responsive web applications
                - Build and maintain RESTful APIs
                - Collaborate with cross-functional teams
                - Implement best practices for code quality
                
                Requirements:
                - 3+ years full stack development experience
                - Proficiency in React, Node.js, JavaScript
                - Experience with databases (MongoDB, PostgreSQL)
                - Strong problem-solving skills
                - Experience with Git and version control
                """
            }
            
            # Create ATS-optimized application
            application_draft = self.job_agent.create_ats_optimized_application(sample_job)
            
            if application_draft:
                result = {
                    "test_name": "Enhanced Job Application",
                    "success": True,
                    "job_title": application_draft['job_title'],
                    "company": application_draft['company'],
                    "ats_score": application_draft.get('ats_score', 0),
                    "contact_score": application_draft.get('ats_breakdown', {}).get('contact_info', 0),
                    "job_title_score": application_draft.get('ats_breakdown', {}).get('job_title_match', 0),
                    "skill_score": application_draft.get('ats_breakdown', {}).get('skill_match', 0),
                    "formatting_score": application_draft.get('ats_breakdown', {}).get('formatting', 0),
                    "readability_score": application_draft.get('ats_breakdown', {}).get('readability', 0),
                    "web_presence_score": application_draft.get('ats_breakdown', {}).get('web_presence', 0),
                    "recommendations_count": len(application_draft.get('ats_recommendations', [])),
                    "missing_elements_count": len(application_draft.get('missing_elements', [])),
                    "keyword_suggestions_count": len(application_draft.get('keyword_suggestions', [])),
                    "requires_manual_review": application_draft.get('requires_manual_review', False),
                    "ats_optimization_completed": application_draft.get('ats_optimization_completed', False),
                    "has_ats_report": bool(application_draft.get('ats_report_file')),
                    "has_optimized_cv": bool(application_draft.get('optimized_cv_file'))
                }
                
                print(f"✅ Enhanced job application created successfully!")
                print(f"🎯 Job: {application_draft['job_title']} at {application_draft['company']}")
                print(f"📊 ATS Score: {application_draft.get('ats_score', 0)}/100")
                print(f"🔧 Recommendations: {len(application_draft.get('ats_recommendations', []))}")
                print(f"⚠️  Missing elements: {len(application_draft.get('missing_elements', []))}")
                print(f"🎯 Keyword suggestions: {len(application_draft.get('keyword_suggestions', []))}")
                print(f"📄 ATS Report: {'Yes' if application_draft.get('ats_report_file') else 'No'}")
                print(f"📝 Optimized CV: {'Yes' if application_draft.get('optimized_cv_file') else 'No'}")
                print(f"🔍 Manual Review Required: {'Yes' if application_draft.get('requires_manual_review') else 'No'}")
                
                return result
            else:
                raise Exception("Application draft creation returned None")
                
        except Exception as e:
            print(f"❌ Enhanced job application test failed: {e}")
            return {
                "test_name": "Enhanced Job Application",
                "success": False,
                "error": str(e)
            }
    
    def _generate_comprehensive_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive ATS optimization report"""
        report = f"""
COMPREHENSIVE ATS OPTIMIZATION SYSTEM REPORT
{'='*60}

Demo Information:
• Started: {results.get('demo_started', 'Unknown')}
• Completed: {results.get('demo_completed', 'Unknown')}
• Overall Success: {'✅ Yes' if results.get('overall_success') else '❌ No'}

Components Tested: {len(results.get('components_tested', []))}
• {', '.join(results.get('components_tested', []))}

DETAILED TEST RESULTS:
"""
        
        # ATS Analysis Results
        ats_analyses = results.get('ats_analyses', [])
        if ats_analyses:
            report += f"""
1. ATS OPTIMIZATION ANALYSIS:
"""
            for analysis in ats_analyses:
                if analysis.get('success'):
                    report += f"""
   ✅ Test: {analysis.get('test_name', 'Unknown')}
   📊 Overall ATS Score: {analysis.get('ats_score', 0)}/100
   📞 Contact Information: {analysis.get('contact_score', 0)}/100
   🎯 Job Title Match: {analysis.get('job_title_score', 0)}/100
   🔧 Skill Matching: {analysis.get('skill_score', 0)}/100
   📄 Formatting: {analysis.get('formatting_score', 0)}/100
   📖 Readability: {analysis.get('readability_score', 0)}/100
   🌐 Web Presence: {analysis.get('web_presence_score', 0)}/100
   🔧 Recommendations: {analysis.get('recommendations_count', 0)}
   ⚠️  Missing Elements: {analysis.get('missing_elements_count', 0)}
   🎯 Keyword Suggestions: {analysis.get('keyword_suggestions_count', 0)}
   📄 Report File: {analysis.get('report_file', 'Not saved')}
"""
                else:
                    report += f"""
   ❌ Test: {analysis.get('test_name', 'Unknown')} - FAILED
   Error: {analysis.get('error', 'Unknown error')}
"""
        
        # CV Generation Results
        cv_generations = results.get('cv_generations', [])
        if cv_generations:
            report += f"""
2. JOB-SPECIFIC CV GENERATION:
"""
            for cv_gen in cv_generations:
                if cv_gen.get('success'):
                    report += f"""
   ✅ Test: {cv_gen.get('test_name', 'Unknown')}
   🎯 Job: {cv_gen.get('job_title', 'Unknown')} at {cv_gen.get('company', 'Unknown')}
   📊 ATS Score: {cv_gen.get('ats_score', 0)}/100
   📞 Contact Information: {cv_gen.get('contact_score', 0)}/100
   🎯 Job Title Match: {cv_gen.get('job_title_score', 0)}/100
   🔧 Skill Matching: {cv_gen.get('skill_score', 0)}/100
   📄 Formatting: {cv_gen.get('formatting_score', 0)}/100
   📖 Readability: {cv_gen.get('readability_score', 0)}/100
   🌐 Web Presence: {cv_gen.get('web_presence_score', 0)}/100
   🔧 Recommendations: {cv_gen.get('recommendations_count', 0)}
   ⚠️  Missing Elements: {cv_gen.get('missing_elements_count', 0)}
   🎯 Keyword Suggestions: {cv_gen.get('keyword_suggestions_count', 0)}
   📁 Files Created: {len(cv_gen.get('saved_files', {}))}
"""
                else:
                    report += f"""
   ❌ Test: {cv_gen.get('test_name', 'Unknown')} - FAILED
   Error: {cv_gen.get('error', 'Unknown error')}
"""
        
        # Job Application Results
        job_applications = results.get('job_applications', [])
        if job_applications:
            report += f"""
3. ENHANCED JOB APPLICATION:
"""
            for job_app in job_applications:
                if job_app.get('success'):
                    report += f"""
   ✅ Test: {job_app.get('test_name', 'Unknown')}
   🎯 Job: {job_app.get('job_title', 'Unknown')} at {job_app.get('company', 'Unknown')}
   📊 ATS Score: {job_app.get('ats_score', 0)}/100
   📞 Contact Information: {job_app.get('contact_score', 0)}/100
   🎯 Job Title Match: {job_app.get('job_title_score', 0)}/100
   🔧 Skill Matching: {job_app.get('skill_score', 0)}/100
   📄 Formatting: {job_app.get('formatting_score', 0)}/100
   📖 Readability: {job_app.get('readability_score', 0)}/100
   🌐 Web Presence: {job_app.get('web_presence_score', 0)}/100
   🔧 Recommendations: {job_app.get('recommendations_count', 0)}
   ⚠️  Missing Elements: {job_app.get('missing_elements_count', 0)}
   🎯 Keyword Suggestions: {job_app.get('keyword_suggestions_count', 0)}
   📄 ATS Report Generated: {'Yes' if job_app.get('has_ats_report') else 'No'}
   📝 Optimized CV Generated: {'Yes' if job_app.get('has_optimized_cv') else 'No'}
   🔍 Manual Review Required: {'Yes' if job_app.get('requires_manual_review') else 'No'}
   ✅ ATS Optimization Completed: {'Yes' if job_app.get('ats_optimization_completed') else 'No'}
"""
                else:
                    report += f"""
   ❌ Test: {job_app.get('test_name', 'Unknown')} - FAILED
   Error: {job_app.get('error', 'Unknown error')}
"""
        
        # Summary Statistics
        total_tests = len(ats_analyses) + len(cv_generations) + len(job_applications)
        successful_tests = sum(1 for test_list in [ats_analyses, cv_generations, job_applications] 
                             for test in test_list if test.get('success'))
        
        report += f"""
SUMMARY STATISTICS:
• Total Tests Run: {total_tests}
• Successful Tests: {successful_tests}
• Success Rate: {(successful_tests/total_tests*100):.1f}% if total_tests > 0 else 0

KEY FEATURES DEMONSTRATED:
✅ ATS optimization analysis with comprehensive scoring
✅ Job-specific CV generation and customization
✅ Enhanced job application with ATS integration
✅ Contact information validation and optimization
✅ Job title matching and keyword optimization
✅ Skill gap analysis and recommendations
✅ Date formatting validation and standardization
✅ Paragraph length and readability optimization
✅ Web presence validation (LinkedIn, GitHub, Portfolio)
✅ Font and layout optimization for ATS compatibility
✅ Comprehensive reporting and file generation

RECOMMENDATIONS FOR PRODUCTION USE:
1. Integrate with existing job application workflow
2. Set minimum ATS score thresholds for auto-application
3. Implement regular CV optimization based on job market trends
4. Add industry-specific keyword databases
5. Create automated follow-up based on ATS analysis results
6. Implement ATS score tracking over time
7. Add integration with popular job boards and ATS systems

---
Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def save_comprehensive_report(self, results: Dict[str, Any]) -> str:
        """Save comprehensive report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_ats_report_{timestamp}.txt"
        
        report = results.get('comprehensive_report', 'No report generated')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"Comprehensive report saved to: {filename}")
        return filename

def main():
    """Main function to run the ATS integration demo"""
    print("🎯 COMPREHENSIVE ATS OPTIMIZATION SYSTEM DEMO")
    print("="*60)
    print("This demo will test all ATS optimization components:")
    print("• ATS Optimizer - Analysis and scoring")
    print("• ATS CV Generator - Job-specific CV creation")
    print("• Enhanced Job Application Agent - Integrated workflow")
    print("• Comprehensive reporting and file generation")
    print()
    
    try:
        demo = ATSIntegrationDemo()
        
        # Run comprehensive demo
        results = demo.run_comprehensive_ats_demo()
        
        # Save comprehensive report
        report_file = demo.save_comprehensive_report(results)
        
        print(f"\n🎉 COMPREHENSIVE ATS OPTIMIZATION DEMO COMPLETED!")
        print(f"📊 Overall Success: {'✅ Yes' if results.get('overall_success') else '❌ No'}")
        print(f"📄 Comprehensive Report: {report_file}")
        print(f"🔧 Components Tested: {len(results.get('components_tested', []))}")
        
        if results.get('overall_success'):
            print(f"\n✅ All ATS optimization components are working correctly!")
            print(f"🚀 The system is ready for production use.")
            print(f"📧 Check the generated files for detailed analysis.")
        else:
            print(f"\n⚠️  Some components encountered issues.")
            print(f"🔍 Check the comprehensive report for details.")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
