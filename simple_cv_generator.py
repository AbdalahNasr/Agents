#!/usr/bin/env python3
"""
SIMPLE CV GENERATOR - Creates PDF without external libraries
"""
import os
from datetime import datetime
from pathlib import Path

def create_cv_content():
    """Create professional CV content"""
    
    cv_content = {
        "header": {
            "name": "ABDALLAH NASR ALI",
            "title": "FULL STACK DEVELOPER",
            "email": "body16nasr16bn@gmail.com",
            "phone": "+20 106 950 9757",
            "location": "Cairo, Egypt",
            "linkedin": "https://linkedin.com/in/abdallah-nasr-ali",
            "github": "https://github.com/AbdalahNasr"
        },
        
        "summary": """Passionate Full Stack Developer with expertise in modern web technologies. 
        Experienced in building responsive web applications, RESTful APIs, and user-friendly interfaces. 
        Strong problem-solving skills and ability to work in fast-paced environments. 
        Committed to writing clean, maintainable code and staying updated with latest industry trends.""",
        
        "skills": {
            "frontend": ["React", "Angular", "Vue.js", "JavaScript", "TypeScript", "HTML5", "CSS3", "Tailwind CSS", "Bootstrap"],
            "backend": ["Node.js", "Python", "Java", "PHP", "Express.js", "Django", "Spring Boot", "Laravel"],
            "database": ["MongoDB", "MySQL", "PostgreSQL", "Redis", "SQLite"],
            "tools": ["Git", "Docker", "AWS", "Vercel", "Netlify", "Postman", "VS Code"]
        },
        
        "projects": [
            {
                "name": "E-commerce Demo - React Storefront",
                "description": "A modern e-commerce platform built with React, featuring product catalog, shopping cart, and user authentication.",
                "code_url": "https://github.com/AbdalahNasr/E-commerce-demo",
                "live_url": "https://abdalahnasr.github.io/E-commerce-demo/",
                "technologies": ["React", "JavaScript", "CSS3", "Local Storage"]
            },
            {
                "name": "ISTQP Quiz App - Quiz Platform",
                "description": "A comprehensive quiz application with multilingual support, built using Next.js and TypeScript.",
                "code_url": "https://github.com/AbdalahNasr/istqp-quiz",
                "live_url": "https://istqp-quiz.vercel.app",
                "technologies": ["Next.js", "TypeScript", "Tailwind CSS", "PostCSS"]
            },
            {
                "name": "Recipes App",
                "description": "A recipe management application for storing and organizing cooking recipes.",
                "code_url": "https://github.com/AbdalahNasr/recipes",
                "live_url": None,
                "technologies": ["React", "JavaScript", "CSS"]
            }
        ],
        
        "experience": [
            {
                "title": "Full Stack Developer Intern",
                "company": "Link Data Center",
                "duration": "2024 - Present",
                "description": "Working on web application development using modern technologies and best practices."
            },
            {
                "title": "Frontend Developer",
                "company": "Freelance",
                "duration": "2023 - Present",
                "description": "Building responsive websites and web applications for various clients."
            }
        ],
        
        "education": [
            {
                "degree": "Bachelor's in Computer Science",
                "institution": "University",
                "duration": "2020 - 2024",
                "description": "Focused on software engineering and web development."
            }
        ]
    }
    
    return cv_content

def create_simple_pdf(cv_content, output_file):
    """Create a simple PDF-like file using basic text formatting"""
    try:
        # Create a formatted text file that looks like a CV
        content = f"""
{cv_content['header']['name']}
{cv_content['header']['title']}
{'=' * 60}

CONTACT INFORMATION:
Email: {cv_content['header']['email']}
Phone: {cv_content['header']['phone']}
Location: {cv_content['header']['location']}
LinkedIn: {cv_content['header']['linkedin']}
GitHub: {cv_content['header']['github']}

PROFESSIONAL SUMMARY:
{cv_content['summary']}

TECHNICAL SKILLS:
Frontend: {', '.join(cv_content['skills']['frontend'])}
Backend: {', '.join(cv_content['skills']['backend'])}
Databases: {', '.join(cv_content['skills']['database'])}
Tools: {', '.join(cv_content['skills']['tools'])}

PROJECTS:
"""
        
        for i, project in enumerate(cv_content['projects'], 1):
            content += f"""
{i}. {project['name']}
   Description: {project['description']}
   Code: {project['code_url']}
"""
            if project['live_url']:
                content += f"   Live Demo: {project['live_url']}\n"
            
            content += f"   Technologies: {', '.join(project['technologies'])}\n"
        
        content += f"""
WORK EXPERIENCE:
"""
        
        for exp in cv_content['experience']:
            content += f"""
- {exp['title']} at {exp['company']} ({exp['duration']})
  {exp['description']}
"""
        
        content += f"""
EDUCATION:
"""
        
        for edu in cv_content['education']:
            content += f"""
- {edu['degree']} from {edu['institution']} ({edu['duration']})
  {edu['description']}
"""
        
        # Save as text file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Simple CV created: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating simple CV: {e}")
        return False

def create_cv_files():
    """Create CV files"""
    
    print("SIMPLE CV GENERATOR - NO EXTERNAL LIBRARIES NEEDED")
    print("=" * 60)
    
    # Create CV content
    cv_content = create_cv_content()
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"SIMPLE_CV_{timestamp}")
    output_dir.mkdir(exist_ok=True)
    
    print(f"Creating CV files in: {output_dir}")
    print()
    
    # Generate Simple CV (text-based)
    cv_file = output_dir / "Abdallah_Nasr_Ali_CV.txt"
    if create_simple_pdf(cv_content, cv_file):
        print(f"✅ Simple CV created: {cv_file}")
    
    # Create instructions file
    instructions = f"""CV CREATED SUCCESSFULLY!
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FILE CREATED:
- Abdallah_Nasr_Ali_CV.txt - Clean, formatted CV ready for job applications

TO CONVERT TO PDF:
1. Open the .txt file in Word or Google Docs
2. Format as needed
3. Save as PDF

TO UPDATE CV CONTENT:
1. Edit the create_cv_content() function in simple_cv_generator.py
2. Run the script again

This CV is clean, professional, and ready for job applications!
"""
    
    guide_file = output_dir / "INSTRUCTIONS.txt"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    print(f"✅ Instructions created: {guide_file}")
    
    print()
    print("🎉 CV GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📁 Directory: {output_dir}")
    print("📄 CV File: Abdallah_Nasr_Ali_CV.txt")
    print("📋 Instructions: INSTRUCTIONS.txt")
    print("\n✅ Your CV is ready for job applications!")
    
    return output_dir

def main():
    """Main function"""
    try:
        output_dir = create_cv_files()
        print(f"\n🎯 Your CV is ready in: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
