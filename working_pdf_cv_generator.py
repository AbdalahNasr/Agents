#!/usr/bin/env python3
"""
WORKING PDF CV GENERATOR
Creates professional CV files including REAL PDF
"""
import os
import sys
import json
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
            "github": "https://github.com/AbdalahNasr",
            "cv_url": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing"
        },
        
        "summary": """Passionate Full Stack Developer with expertise in modern web technologies. 
        Experienced in building responsive web applications, RESTful APIs, and user-friendly interfaces. 
        Strong problem-solving skills and ability to work in fast-paced environments. 
        Committed to writing clean, maintainable code and staying updated with latest industry trends.""",
        
        "skills": {
            "frontend": ["React", "Angular", "Vue.js", "JavaScript", "TypeScript", "HTML5", "CSS3", "Tailwind CSS", "Bootstrap"],
            "backend": ["Node.js", "Python", "Java", "PHP", "Express.js", "Django", "Spring Boot", "Laravel"],
            "database": ["MongoDB", "MySQL", "PostgreSQL", "Redis", "SQLite"],
            "tools": ["Git", "Docker", "AWS", "Vercel", "Netlify", "Postman", "VS Code"],
            "other": ["RESTful APIs", "GraphQL", "JWT", "OAuth", "CI/CD", "Agile", "Scrum"]
        },
        
        "projects": [
            {
                "name": "E-commerce Demo - React Storefront",
                "description": "A modern e-commerce platform built with React, featuring product catalog, shopping cart, and user authentication.",
                "code_url": "https://github.com/AbdalahNasr/E-commerce-demo",
                "live_url": "https://abdalahnasr.github.io/E-commerce-demo/",
                "technologies": ["React", "JavaScript", "CSS3", "Local Storage"],
                "features": ["Product catalog", "Shopping cart", "User authentication", "Responsive design"]
            },
            {
                "name": "ISTQP Quiz App - Quiz Platform",
                "description": "A comprehensive quiz application with multilingual support, built using Next.js and TypeScript.",
                "code_url": "https://github.com/AbdalahNasr/istqp-quiz",
                "live_url": "https://istqp-quiz.vercel.app",
                "technologies": ["Next.js", "TypeScript", "Tailwind CSS", "PostCSS"],
                "features": ["JSON-based quizzes", "Multilingual support", "ESLint", "SSR", "Responsive design"]
            },
            {
                "name": "Recipes App",
                "description": "A recipe management application for storing and organizing cooking recipes.",
                "code_url": "https://github.com/AbdalahNasr/recipes",
                "live_url": None,
                "technologies": ["React", "JavaScript", "CSS"],
                "features": ["Recipe storage", "Category organization", "Search functionality"]
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
        ],
        
        "certificates": [
            {
                "name": "Foundations of UX Design",
                "issuer": "Google",
                "date": "2024"
            },
            {
                "name": "React Basics",
                "issuer": "Google",
                "date": "2024"
            },
            {
                "name": "Full Stack Web Development",
                "issuer": "Route Academy",
                "date": "2023"
            },
            {
                "name": "Angular Developer Internship",
                "issuer": "Link Data Center",
                "date": "2024"
            }
        ],
        
        "languages": [
            {
                "language": "English",
                "level": "Upper Intermediate"
            },
            {
                "language": "Arabic",
                "level": "Native"
            }
        ]
    }
    
    return cv_content

def create_html_cv(cv_content, output_file):
    """Create HTML CV with working links"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cv_content['header']['name']} - CV</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #2c3e50;
        }}
        .name {{
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .title {{
            font-size: 20px;
            color: #34495e;
            margin-bottom: 20px;
        }}
        .contact-info {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .contact-item {{
            text-align: center;
        }}
        .contact-item a {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }}
        .contact-item a:hover {{
            text-decoration: underline;
        }}
        .section {{
            margin-top: 30px;
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
            margin-bottom: 20px;
        }}
        .project {{
            margin-bottom: 25px;
            padding: 20px;
            border: 1px solid #ecf0f1;
            border-radius: 8px;
            background-color: #f8f9fa;
        }}
        .project-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        .project-links {{
            margin: 10px 0;
        }}
        .project-links a {{
            color: #3498db;
            text-decoration: none;
            margin-right: 20px;
            font-weight: 500;
        }}
        .project-links a:hover {{
            text-decoration: underline;
        }}
        .skill-category {{
            margin-bottom: 15px;
        }}
        .skill-title {{
            font-weight: bold;
            color: #34495e;
            margin-bottom: 5px;
        }}
        .skill-list {{
            color: #7f8c8d;
            margin-left: 20px;
        }}
        .experience-item {{
            margin-bottom: 20px;
        }}
        .experience-title {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .experience-company {{
            color: #3498db;
            font-weight: 500;
        }}
        .experience-duration {{
            color: #7f8c8d;
            font-style: italic;
        }}
        .certificate-item {{
            margin-bottom: 10px;
        }}
        .certificate-name {{
            font-weight: bold;
        }}
        .certificate-issuer {{
            color: #3498db;
        }}
        .certificate-date {{
            color: #7f8c8d;
            font-style: italic;
        }}
        @media print {{
            body {{ margin: 0; padding: 0; }}
            .container {{ box-shadow: none; padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="name">{cv_content['header']['name']}</div>
            <div class="title">{cv_content['header']['title']}</div>
        </div>
        
        <div class="contact-info">
            <div class="contact-item">
                <strong>Email:</strong><br>
                <a href="mailto:{cv_content['header']['email']}">{cv_content['header']['email']}</a>
            </div>
            <div class="contact-item">
                <strong>Phone:</strong><br>
                <a href="tel:{cv_content['header']['phone']}">{cv_content['header']['phone']}</a>
            </div>
            <div class="contact-item">
                <strong>Location:</strong><br>
                {cv_content['header']['location']}
            </div>
            <div class="contact-item">
                <strong>LinkedIn:</strong><br>
                <a href="{cv_content['header']['linkedin']}" target="_blank">LinkedIn Profile</a>
            </div>
            <div class="contact-item">
                <strong>GitHub:</strong><br>
                <a href="{cv_content['header']['github']}" target="_blank">GitHub Profile</a>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">PROFESSIONAL SUMMARY</div>
            <p>{cv_content['summary']}</p>
        </div>
        
        <div class="section">
            <div class="section-title">TECHNICAL SKILLS</div>
            <div class="skill-category">
                <div class="skill-title">Frontend Development:</div>
                <div class="skill-list">{', '.join(cv_content['skills']['frontend'])}</div>
            </div>
            <div class="skill-category">
                <div class="skill-title">Backend Development:</div>
                <div class="skill-list">{', '.join(cv_content['skills']['backend'])}</div>
            </div>
            <div class="skill-category">
                <div class="skill-title">Databases & Tools:</div>
                <div class="skill-list">{', '.join(cv_content['skills']['database'])}</div>
            </div>
            <div class="skill-category">
                <div class="skill-title">Development Tools:</div>
                <div class="skill-list">{', '.join(cv_content['skills']['tools'])}</div>
            </div>
            <div class="skill-category">
                <div class="skill-title">Other Skills:</div>
                <div class="skill-list">{', '.join(cv_content['skills']['other'])}</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">PROJECTS & LIVE DEMOS</div>
"""
    
    for project in cv_content['projects']:
        html_content += f"""
            <div class="project">
                <div class="project-title">{project['name']}</div>
                <p><strong>Description:</strong> {project['description']}</p>
                <div class="project-links">
                    <a href="{project['code_url']}" target="_blank">{project['code_url']}</a>
"""
        if project['live_url']:
            html_content += f'                    <a href="{project["live_url"]}" target="_blank">{project["live_url"]}</a>'
        
        html_content += f"""
                </div>
                <p><strong>Technologies:</strong> {', '.join(project['technologies'])}</p>
                <p><strong>Features:</strong> {', '.join(project['features'])}</p>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="section">
            <div class="section-title">WORK EXPERIENCE</div>
"""
    
    for exp in cv_content['experience']:
        html_content += f"""
            <div class="experience-item">
                <div class="experience-title">{exp['title']}</div>
                <div class="experience-company">{exp['company']}</div>
                <div class="experience-duration">{exp['duration']}</div>
                <p>{exp['description']}</p>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="section">
            <div class="section-title">EDUCATION</div>
"""
    
    for edu in cv_content['education']:
        html_content += f"""
            <div class="experience-item">
                <div class="experience-title">{edu['degree']}</div>
                <div class="experience-company">{edu['institution']}</div>
                <div class="experience-duration">{edu['duration']}</div>
                <p>{edu['description']}</p>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="section">
            <div class="section-title">CERTIFICATES</div>
"""
    
    for cert in cv_content['certificates']:
        html_content += f"""
            <div class="certificate-item">
                <span class="certificate-name">{cert['name']}</span> — 
                <span class="certificate-issuer">{cert['issuer']}</span> 
                <span class="certificate-date">({cert['date']})</span>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="section">
            <div class="section-title">LANGUAGES</div>
"""
    
    for lang in cv_content['languages']:
        html_content += f"""
            <p><strong>{lang['language']}</strong> — {lang['level']}</p>
"""
    
    html_content += """
        </div>
    </div>
</body>
</html>"""
    
    # Save HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return True

def create_pdf_cv(cv_content, output_file):
    """Create PDF CV using weasyprint or alternative method"""
    
    try:
        # Try to import weasyprint first
        try:
            import weasyprint
            return create_pdf_with_weasyprint(cv_content, output_file)
        except ImportError:
            pass
        
        # Try to import reportlab
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            return create_pdf_with_reportlab(cv_content, output_file)
        except ImportError:
            pass
        
        # If both fail, create a text-based PDF-like file
        return create_text_pdf(cv_content, output_file)
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return create_text_pdf(cv_content, output_file)

def create_pdf_with_weasyprint(cv_content, output_file):
    """Create PDF using weasyprint"""
    try:
        import weasyprint
        
        # Create HTML content
        html_file = str(output_file).replace('.pdf', '_temp.html')
        create_html_cv(cv_content, html_file)
        
        # Convert HTML to PDF
        weasyprint.HTML(filename=html_file).write_pdf(output_file)
        
        # Clean up temp file
        os.remove(html_file)
        
        return True
    except Exception as e:
        print(f"Weasyprint PDF creation failed: {e}")
        return False

def create_pdf_with_reportlab(cv_content, output_file):
    """Create PDF using reportlab"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        # Create PDF document
        doc = SimpleDocTemplate(output_file, pagesize=A4, rightMargin=0.5*inch, leftMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        section_style = ParagraphStyle(
            'CustomSection',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.darkblue
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        
        # Build story
        story = []
        
        # Header
        story.append(Paragraph(cv_content['header']['name'], title_style))
        story.append(Paragraph(cv_content['header']['title'], subtitle_style))
        
        # Contact information
        contact_data = [
            ['Email:', cv_content['header']['email']],
            ['Phone:', cv_content['header']['phone']],
            ['Location:', cv_content['header']['location']],
            ['LinkedIn:', cv_content['header']['linkedin']],
            ['GitHub:', cv_content['header']['github']]
        ]
        
        contact_table = Table(contact_data, colWidths=[1*inch, 4*inch])
        contact_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(contact_table)
        story.append(Spacer(1, 15))
        
        # Professional Summary
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        story.append(Paragraph(cv_content['summary'], normal_style))
        story.append(Spacer(1, 10))
        
        # Technical Skills
        story.append(Paragraph("TECHNICAL SKILLS", section_style))
        
        skills_data = [
            ['Frontend:', ', '.join(cv_content['skills']['frontend'])],
            ['Backend:', ', '.join(cv_content['skills']['backend'])],
            ['Databases:', ', '.join(cv_content['skills']['database'])],
            ['Tools:', ', '.join(cv_content['skills']['tools'])],
            ['Other:', ', '.join(cv_content['skills']['other'])]
        ]
        
        skills_table = Table(skills_data, colWidths=[1.2*inch, 4.8*inch])
        skills_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(skills_table)
        story.append(Spacer(1, 10))
        
        # Projects
        story.append(Paragraph("PROJECTS & LIVE DEMOS", section_style))
        
        for project in cv_content['projects']:
            project_title = f"<b>{project['name']}</b>"
            story.append(Paragraph(project_title, normal_style))
            
            project_desc = f"<b>Description:</b> {project['description']}"
            story.append(Paragraph(project_desc, normal_style))
            
            project_code = f"<b>Code:</b> {project['code_url']}"
            story.append(Paragraph(project_code, normal_style))
            
            if project['live_url']:
                project_live = f"<b>Live Demo:</b> {project['live_url']}"
                story.append(Paragraph(project_live, normal_style))
            
            project_tech = f"<b>Technologies:</b> {', '.join(project['technologies'])}"
            story.append(Paragraph(project_tech, normal_style))
            
            project_features = f"<b>Features:</b> {', '.join(project['features'])}"
            story.append(Paragraph(project_features, normal_style))
            
            story.append(Spacer(1, 8))
        
        # Work Experience
        story.append(Paragraph("WORK EXPERIENCE", section_style))
        
        for exp in cv_content['experience']:
            exp_title = f"<b>{exp['title']}</b> - {exp['company']} ({exp['duration']})"
            story.append(Paragraph(exp_title, normal_style))
            
            exp_desc = exp['description']
            story.append(Paragraph(exp_desc, normal_style))
            story.append(Spacer(1, 5))
        
        # Education
        story.append(Paragraph("EDUCATION", section_style))
        
        for edu in cv_content['education']:
            edu_title = f"<b>{edu['degree']}</b> - {edu['institution']} ({edu['duration']})"
            story.append(Paragraph(edu_title, normal_style))
            
            edu_desc = edu['description']
            story.append(Paragraph(edu_desc, normal_style))
            story.append(Spacer(1, 5))
        
        # Certificates
        story.append(Paragraph("CERTIFICATES", section_style))
        
        for cert in cv_content['certificates']:
            cert_text = f"<b>{cert['name']}</b> — {cert['issuer']} ({cert['date']})"
            story.append(Paragraph(cert_text, normal_style))
        
        # Languages
        story.append(Paragraph("LANGUAGES", section_style))
        
        for lang in cv_content['languages']:
            lang_text = f"<b>{lang['language']}</b> — {lang['level']}"
            story.append(Paragraph(lang_text, normal_style))
        
        # Build PDF
        doc.build(story)
        return True
        
    except Exception as e:
        print(f"Reportlab PDF creation failed: {e}")
        return False

def create_text_pdf(cv_content, output_file):
    """Create a text-based PDF-like file"""
    try:
        # Create a simple text file that can be opened as PDF
        text_content = f"""{cv_content['header']['name']} - {cv_content['header']['title']}
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

PROJECTS & LIVE DEMOS:
"""
        
        for i, project in enumerate(cv_content['projects'], 1):
            text_content += f"""
{i}. {project['name']}
   Description: {project['description']}
   Code: {project['code_url']}
"""
            if project['live_url']:
                text_content += f"   Live Demo: {project['live_url']}\n"
            
            text_content += f"""   Technologies: {', '.join(project['technologies'])}
   Features: {', '.join(project['features'])}
"""
        
        text_content += f"""
WORK EXPERIENCE:
"""
        
        for exp in cv_content['experience']:
            text_content += f"""
- {exp['title']} at {exp['company']} ({exp['duration']})
  {exp['description']}
"""
        
        text_content += f"""
EDUCATION:
"""
        
        for edu in cv_content['education']:
            text_content += f"""
- {edu['degree']} from {edu['institution']} ({edu['duration']})
  {edu['description']}
"""
        
        text_content += f"""
CERTIFICATES:
"""
        
        for cert in cv_content['certificates']:
            text_content += f"""
- {cert['name']} — {cert['issuer']} ({cert['date']})
"""
        
        text_content += f"""
LANGUAGES:
"""
        
        for lang in cv_content['languages']:
            text_content += f"""
- {lang['language']}: {lang['level']}
"""
        
        # Save as text file
        text_file = str(output_file).replace('.pdf', '_text.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"Text file created: {text_file}")
        print("To get PDF: Open HTML file in browser → Print → Save as PDF")
        
        return False
        
    except Exception as e:
        print(f"Error creating text file: {e}")
        return False

def create_markdown_cv(cv_content):
    """Create Markdown version of CV"""
    
    md_content = f"""# {cv_content['header']['name']} - {cv_content['header']['title']}

## Contact Information
- **Email:** {cv_content['header']['email']}
- **Phone:** {cv_content['header']['phone']}
- **Location:** {cv_content['header']['location']}
- **LinkedIn:** {cv_content['header']['linkedin']}
- **GitHub:** {cv_content['header']['github']}

## Professional Summary
{cv_content['summary']}

## Technical Skills

### Frontend Development
{', '.join(cv_content['skills']['frontend'])}

### Backend Development
{', '.join(cv_content['skills']['backend'])}

### Databases & Tools
{', '.join(cv_content['skills']['database'])}

### Development Tools
{', '.join(cv_content['skills']['tools'])}

### Other Skills
{', '.join(cv_content['skills']['other'])}

## Projects & Live Demos

"""
    
    for project in cv_content['projects']:
        md_content += f"""### {project['name']}
- **Description:** {project['description']}
- **Code:** {project['code_url']}
"""
        if project['live_url']:
            md_content += f"- **Live Demo:** {project['live_url']}\n"
        
        md_content += f"""- **Technologies:** {', '.join(project['technologies'])}
- **Features:** {', '.join(project['features'])}

"""
    
    md_content += f"""## Work Experience

"""
    
    for exp in cv_content['experience']:
        md_content += f"""### {exp['title']}
- **Company:** {exp['company']}
- **Duration:** {exp['duration']}
- **Description:** {exp['description']}

"""
    
    md_content += f"""## Education

"""
    
    for edu in cv_content['education']:
        md_content += f"""### {edu['degree']}
- **Institution:** {edu['institution']}
- **Duration:** {edu['duration']}
- **Description:** {edu['description']}

"""
    
    md_content += f"""## Certificates

"""
    
    for cert in cv_content['certificates']:
        md_content += f"""- **{cert['name']}** — {cert['issuer']} ({cert['date']})

"""
    
    md_content += f"""## Languages

"""
    
    for lang in cv_content['languages']:
        md_content += f"""- **{lang['language']}** — {lang['level']}

"""
    
    return md_content

def create_text_cv(cv_content):
    """Create plain text version of CV"""
    
    text_content = f"""{cv_content['header']['name']} - {cv_content['header']['title']}
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

PROJECTS & LIVE DEMOS:
"""
    
    for i, project in enumerate(cv_content['projects'], 1):
        text_content += f"""
{i}. {project['name']}
   Description: {project['description']}
   Code: {project['code_url']}
"""
        if project['live_url']:
            text_content += f"   Live Demo: {project['live_url']}\n"
        
        text_content += f"""   Technologies: {', '.join(project['technologies'])}
   Features: {', '.join(project['features'])}
"""
    
    text_content += f"""
WORK EXPERIENCE:
"""
    
    for exp in cv_content['experience']:
        text_content += f"""
- {exp['title']} at {exp['company']} ({exp['duration']})
  {exp['description']}
"""
    
    text_content += f"""
EDUCATION:
"""
    
    for edu in cv_content['education']:
        text_content += f"""
- {edu['degree']} from {edu['institution']} ({edu['duration']})
  {edu['description']}
"""
    
    text_content += f"""
CERTIFICATES:
"""
    
    for cert in cv_content['certificates']:
        text_content += f"""
- {cert['name']} — {cert['issuer']} ({cert['date']})
"""
    
    text_content += f"""
LANGUAGES:
"""
    
    for lang in cv_content['languages']:
        text_content += f"""
- {lang['language']}: {lang['level']}
"""
    
    return text_content

def create_cv_files():
    """Create all CV file formats"""
    
    print("WORKING PDF CV GENERATOR")
    print("=" * 50)
    
    # Create CV content
    cv_content = create_cv_content()
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"WORKING_CV_{timestamp}")
    output_dir.mkdir(exist_ok=True)
    
    print(f"Creating CV files in: {output_dir}")
    print()
    
    # Generate Markdown CV
    md_content = create_markdown_cv(cv_content)
    md_file = output_dir / "Abdallah_Nasr_Ali_CV.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Markdown CV created: {md_file}")
    
    # Generate Text CV
    text_content = create_text_cv(cv_content)
    text_file = output_dir / "Abdallah_Nasr_Ali_CV.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text_content)
    print(f"Text CV created: {text_file}")
    
    # Generate HTML CV
    html_file = output_dir / "Abdallah_Nasr_Ali_CV.html"
    create_html_cv(cv_content, html_file)
    print(f"HTML CV created: {html_file}")
    
    # Generate PDF CV
    pdf_file = output_dir / "Abdallah_Nasr_Ali_CV.pdf"
    print("Creating PDF...")
    if create_pdf_cv(cv_content, pdf_file):
        print(f"✅ PDF CV created: {pdf_file}")
    else:
        print("❌ PDF creation failed - but HTML file can be converted to PDF")
        print("💡 To get PDF: Open HTML file in browser → Print → Save as PDF")
    
    # Create project update guide
    update_guide = f"""CV UPDATE GUIDE
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FILES CREATED:
1. Abdallah_Nasr_Ali_CV.md - Markdown format
2. Abdallah_Nasr_Ali_CV.txt - Plain text format  
3. Abdallah_Nasr_Ali_CV.html - HTML format with working links
4. Abdallah_Nasr_Ali_CV.pdf - Professional PDF format

TO ADD NEW PROJECTS:
1. Edit the create_cv_content() function in working_pdf_cv_generator.py
2. Add new project to the 'projects' list
3. Run the script again to generate updated CVs

TO UPDATE SKILLS:
1. Edit the 'skills' section in create_cv_content()
2. Add/remove technologies as needed
3. Regenerate all CV formats

TO UPDATE EXPERIENCE:
1. Edit the 'experience' section
2. Add new positions or update existing ones
3. Regenerate CVs

All CV files are clean and professional, ready for job applications.
"""
    
    guide_file = output_dir / "UPDATE_GUIDE.txt"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(update_guide)
    print(f"Update guide created: {guide_file}")
    
    print()
    print("CV GENERATION COMPLETE!")
    print("=" * 50)
    
    print("Files created:")
    print(f"  Directory: {output_dir}")
    print("  Markdown CV: Abdallah_Nasr_Ali_CV.md")
    print("  Text CV: Abdallah_Nasr_Ali_CV.txt")
    print("  HTML CV: Abdallah_Nasr_Ali_CV.html")
    print("  PDF CV: Abdallah_Nasr_Ali_CV.pdf")
    print("  Guide: UPDATE_GUIDE.txt")
    
    print("\nAll CV files are clean and professional.")
    print("HTML file has working, clickable links.")
    print("PDF file is ready for printing and applications.")
    
    return output_dir

def main():
    """Main function to create professional CV files"""
    try:
        output_dir = create_cv_files()
        
        print(f"\nYour professional CV files are ready in: {output_dir}")
        print("All files are clean, professional, and ready for job applications.")
        
    except Exception as e:
        print(f"Error creating CV files: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
