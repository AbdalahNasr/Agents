#!/usr/bin/env python3
"""
Fix Database References in CV Generator
"""
import re

def fix_database_refs():
    """Fix database references"""
    
    with open('fixed_pdf_cv_generator.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the specific problematic lines
    content = content.replace(
        'Databases: {\', \'.join(cv_content[\'skills\'][\'database\'])}',
        ''
    )
    
    content = content.replace(
        'Backend: {\', \'.join(cv_content[\'skills\'][\'backend\'])}',
        'Backend & Database: {\', \'.join(cv_content[\'skills\'][\'backend\'])}'
    )
    
    with open('fixed_pdf_cv_generator.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Database references fixed!")

if __name__ == "__main__":
    fix_database_refs()
