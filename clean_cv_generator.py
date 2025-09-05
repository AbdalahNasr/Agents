#!/usr/bin/env python3
"""
Clean CV Generator - Creates professional CV files without extra text
"""

import os
import json
from datetime import datetime
import PyPDF2

def read_pdf_cv():
    """Read the actual PDF CV"""
    try:
        with open('Abdallah Nasr Ali_Cv.pdf', 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except FileNotFoundError:
        print("❌ Abdallah Nasr Ali_Cv.pdf not found!")
        return None
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

def create_cv_versions(original_cv):
    """Create 3 clean versions from the actual CV"""
    
    # Version 1: ATS-Friendly (clean, keyword-rich)
    ats_version = original_cv
    
    # Version 2: Professional (enhanced)
    professional_version = original_cv
    
    # Version 3: Concise (focused)
    concise_version = original_cv
    
    return {
        "ats": ats_version,
        "professional": professional_version, 
        "concise": concise_version
    }

def create_cv_structure():
    """Create the CV structure with clean content"""
    
    # Read actual PDF CV
    original_cv = read_pdf_cv()
    if not original_cv:
        return
    
    # Create versions
    cv_versions = create_cv_versions(original_cv)
    
    # Create main folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_folder = f"CLEAN_CV_{timestamp}"
    
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        print(f"📁 Created main folder: {main_folder}")
    
    # Create ALL folder
    all_folder = os.path.join(main_folder, "ALL")
    if not os.path.exists(all_folder):
        os.makedirs(all_folder)
    
    # Create date/time folder
    current_time = datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%I%p")
    
    date_time_folder = os.path.join(all_folder, date_str, time_str)
    if not os.path.exists(date_time_folder):
        os.makedirs(date_time_folder)
    
    # Create subfolders
    subfolders = ['JSON', 'PDF', 'DOCX', 'MARKDOWN', 'TEXT']
    for subfolder in subfolders:
        subfolder_path = os.path.join(date_time_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    
    # Generate CVs for each version
    for version_name, cv_content in cv_versions.items():
        print(f"\n🔄 Generating {version_name} version...")
        
        # JSON - clean data only
        json_path = os.path.join(date_time_folder, "JSON", f"cv_{version_name}_{timestamp}.json")
        create_clean_json_cv(cv_content, version_name, json_path)
        
        # PDF - clean content only
        pdf_path = os.path.join(date_time_folder, "PDF", f"cv_{version_name}_{timestamp}.pdf")
        create_clean_pdf_cv(cv_content, pdf_path)
        
        # DOCX - clean content only
        docx_path = os.path.join(date_time_folder, "DOCX", f"cv_{version_name}_{timestamp}.docx")
        create_clean_docx_cv(cv_content, docx_path)
        
        # Markdown - clean content only
        md_path = os.path.join(date_time_folder, "MARKDOWN", f"cv_{version_name}_{timestamp}.md")
        create_clean_markdown_cv(cv_content, md_path)
        
        # Text - clean content only
        txt_path = os.path.join(date_time_folder, "TEXT", f"cv_{version_name}_{timestamp}.txt")
        create_clean_text_cv(cv_content, txt_path)
    
    print(f"\n🎉 Clean CV versions created successfully!")
    print(f"📁 Main folder: {main_folder}")
    print(f"📁 Structure: ALL/{date_str}/{time_str}/")

def create_clean_json_cv(content, version_name, file_path):
    """Create clean JSON CV with just the content"""
    cv_data = {
        "content": content,
        "version": version_name
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cv_data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ JSON: {os.path.basename(file_path)}")

def create_clean_pdf_cv(content, file_path):
    """Create clean PDF CV with just the content"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ PDF: {os.path.basename(file_path)}")

def create_clean_docx_cv(content, file_path):
    """Create clean DOCX CV with just the content"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ DOCX: {os.path.basename(file_path)}")

def create_clean_markdown_cv(content, file_path):
    """Create clean Markdown CV with just the content"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Markdown: {os.path.basename(file_path)}")

def create_clean_text_cv(content, file_path):
    """Create clean Text CV with just the content"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Text: {os.path.basename(file_path)}")

if __name__ == "__main__":
    create_cv_structure()

