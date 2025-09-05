#!/usr/bin/env python3
"""
Create CV Structure Directly
CVs → ALL → Date/Time → JSON → file.json
"""

import os
import shutil
from datetime import datetime

def create_cv_structure():
    """Create the CV structure directly."""
    
    # Create main folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_folder = f"CV_STRUCTURE_{timestamp}"
    
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        print(f"📁 Created main folder: {main_folder}")
    
    # Create ALL folder
    all_folder = os.path.join(main_folder, "ALL")
    if not os.path.exists(all_folder):
        os.makedirs(all_folder)
        print(f"📁 Created ALL folder")
    
    # Create date/time folder
    current_time = datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%I%p")  # e.g., "6PM"
    
    date_time_folder = os.path.join(all_folder, date_str, time_str)
    if not os.path.exists(date_time_folder):
        os.makedirs(date_time_folder)
        print(f"📁 Created date/time folder: {date_str}/{time_str}")
    
    # Create subfolders
    subfolders = ['JSON', 'PDF', 'DOCX', 'MARKDOWN', 'TEXT']
    for subfolder in subfolders:
        subfolder_path = os.path.join(date_time_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    
    # Create sample CV files
    create_sample_cv_files(date_time_folder, timestamp)
    
    # Create summary
    create_summary(main_folder, date_str, time_str, timestamp)
    
    print(f"\n🎉 CV structure created successfully!")
    print(f"📁 Main folder: {main_folder}")
    print(f"📁 Structure: ALL/{date_str}/{time_str}/")
    
    # Show structure
    print(f"\n📁 Final structure:")
    show_structure(main_folder)

def create_sample_cv_files(base_path, timestamp):
    """Create sample CV files in each folder."""
    
    # JSON files
    json_folder = os.path.join(base_path, "JSON")
    cv_data = {
        "frontend": {"role": "Frontend Developer", "skills": ["React", "Vue", "JavaScript"]},
        "backend": {"role": "Backend Developer", "skills": ["Python", "Java", "Node.js"]},
        "fullstack": {"role": "Full-Stack Developer", "skills": ["React", "Node.js", "Python"]},
        "devops": {"role": "DevOps Engineer", "skills": ["Docker", "Kubernetes", "AWS"]}
    }
    
    for stack, data in cv_data.items():
        json_file = os.path.join(json_folder, f"cv_{stack}_{timestamp}.json")
        import json
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"  ✅ Created: JSON/cv_{stack}_{timestamp}.json")
    
    # PDF files (create text files as placeholders)
    pdf_folder = os.path.join(base_path, "PDF")
    for stack in cv_data.keys():
        pdf_file = os.path.join(pdf_folder, f"cv_{stack}_{timestamp}.pdf")
        with open(pdf_file, 'w', encoding='utf-8') as f:
            f.write(f"CV for {stack} - Generated at {timestamp}")
        print(f"  ✅ Created: PDF/cv_{stack}_{timestamp}.pdf")
    
    # DOCX files (create text files as placeholders)
    docx_folder = os.path.join(base_path, "DOCX")
    for stack in cv_data.keys():
        docx_file = os.path.join(docx_folder, f"cv_{stack}_{timestamp}.docx")
        with open(docx_file, 'w', encoding='utf-8') as f:
            f.write(f"CV for {stack} - Generated at {timestamp}")
        print(f"  ✅ Created: DOCX/cv_{stack}_{timestamp}.docx")
    
    # Markdown files
    md_folder = os.path.join(base_path, "MARKDOWN")
    for stack in cv_data.keys():
        md_file = os.path.join(md_folder, f"cv_{stack}_{timestamp}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# CV for {stack}\n\nGenerated at: {timestamp}\n\n## Skills\n")
            for skill in cv_data[stack]["skills"]:
                f.write(f"- {skill}\n")
        print(f"  ✅ Created: MARKDOWN/cv_{stack}_{timestamp}.md")
    
    # Text files
    text_folder = os.path.join(base_path, "TEXT")
    for stack in cv_data.keys():
        text_file = os.path.join(text_folder, f"cv_{stack}_{timestamp}.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"CV for {stack}\nGenerated at: {timestamp}\n\nSkills:\n")
            for skill in cv_data[stack]["skills"]:
                f.write(f"- {skill}\n")
        print(f"  ✅ Created: TEXT/cv_{stack}_{timestamp}.txt")

def create_summary(main_folder, date_str, time_str, timestamp):
    """Create summary file."""
    summary_file = os.path.join(main_folder, "STRUCTURE_SUMMARY.txt")
    
    summary_content = f"""CV Structure Summary
{'='*30}

Created at: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Main folder: {main_folder}
Structure: ALL/{date_str}/{time_str}/

This structure follows the pattern:
CVs → ALL → Date/Time → JSON → file.json

Folder breakdown:
• ALL/ - Contains all CV generations
  └── {date_str}/ - Date folder
      └── {time_str}/ - Time folder
          ├── JSON/ - CV data files with timestamps
          ├── PDF/ - CV PDF files with timestamps
          ├── DOCX/ - CV DOCX files with timestamps
          ├── MARKDOWN/ - CV markdown files with timestamps
          └── TEXT/ - CV text files with timestamps

Example files:
• cv_frontend_{timestamp}.json
• cv_backend_{timestamp}.pdf
• cv_fullstack_{timestamp}.docx

Each time you run this, a new timestamped folder will be created.
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"📋 Summary created: STRUCTURE_SUMMARY.txt")

def show_structure(folder_path, level=0):
    """Show the folder structure."""
    indent = "  " * level
    
    if os.path.isdir(folder_path):
        print(f"{indent}{os.path.basename(folder_path)}/")
        
        try:
            items = os.listdir(folder_path)
            folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]
            files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
            
            # Show folders first
            for folder in sorted(folders):
                show_structure(os.path.join(folder_path, folder), level + 1)
            
            # Show files
            for file in sorted(files):
                print(f"{indent}  {file}")
                
        except PermissionError:
            print(f"{indent}  [Access Denied]")

if __name__ == "__main__":
    create_cv_structure()

