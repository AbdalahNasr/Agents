#!/usr/bin/env python3
"""
Fix CV Generator Script
Removes all problematic references to 'database' and 'features'
"""
import re

def fix_cv_generator():
    """Fix the CV generator file"""
    
    # Read the file
    with open('fixed_pdf_cv_generator.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix database references
    content = re.sub(r'Databases: \{.*?cv_content\[\'skills\'\]\[\'database\'\]\}', '', content)
    content = re.sub(r'Backend: \{.*?cv_content\[\'skills\'\]\[\'backend\'\]\}', 'Backend & Database: {\', \'.join(cv_content[\'skills\'][\'backend\'])}', content)
    
    # Fix features references
    content = re.sub(r'Features: \{.*?cv_content\[\'skills\'\]\[\'features\'\]\}', '', content)
    content = re.sub(r'project_features = f"<b>Features:</b> \{.*?cv_content\[\'skills\'\]\[\'features\'\]\}"', '', content)
    content = re.sub(r'story\.append\(Paragraph\(project_features, normal_style\)\)', '', content)
    
    # Fix other skills references
    content = re.sub(r'Other: \{.*?cv_content\[\'skills\'\]\[\'other\'\]\}', '', content)
    
    # Fix languages references
    content = re.sub(r'LANGUAGES:.*?for lang in cv_content\[\'languages\'\]:.*?lang\[\'level\'\]\}', '', content, flags=re.DOTALL)
    content = re.sub(r'## Languages.*?for lang in cv_content\[\'languages\'\]:.*?lang\[\'level\'\]\}', '', content, flags=re.DOTALL)
    
    # Write the fixed file
    with open('fixed_pdf_cv_generator.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ CV generator fixed!")

if __name__ == "__main__":
    fix_cv_generator()
