#!/usr/bin/env python3
"""
CV File Organizer
Organizes all CV files into a single timestamped folder
"""

import os
import shutil
from datetime import datetime

def organize_cv_files():
    """Organize all CV files into a single timestamped folder."""
    
    # Create timestamp for folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"cv_files_{timestamp}"
    
    # Create the main folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Created folder: {folder_name}")
    
    # CV file patterns to organize
    cv_patterns = [
        "cv_frontend.*",
        "cv_backend.*", 
        "cv_fullstack.*",
        "cv_devops.*",
        "cv_*.pdf",
        "cv_*.docx",
        "cv_*.json",
        "cv_*.md",
        "cv_*.txt"
    ]
    
    # Get all files in current directory
    all_files = os.listdir('.')
    
    # Find CV files
    cv_files = []
    for file in all_files:
        if any(pattern.replace('*', '') in file for pattern in cv_patterns):
            cv_files.append(file)
    
    print(f"🎯 Found {len(cv_files)} CV files to organize")
    
    # Move files to organized folder
    moved_count = 0
    for file in cv_files:
        if os.path.isfile(file):
            try:
                # Create subfolder based on file type
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext == '.pdf':
                    subfolder = 'pdf_files'
                elif file_ext == '.docx':
                    subfolder = 'docx_files'
                elif file_ext == '.json':
                    subfolder = 'json_files'
                elif file_ext == '.md':
                    subfolder = 'markdown_files'
                elif file_ext == '.txt':
                    subfolder = 'text_files'
                else:
                    subfolder = 'other_files'
                
                # Create subfolder if it doesn't exist
                subfolder_path = os.path.join(folder_name, subfolder)
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                
                # Move file
                source = file
                destination = os.path.join(subfolder_path, file)
                shutil.move(source, destination)
                print(f"  ✅ Moved {file} → {subfolder}/{file}")
                moved_count += 1
                
            except Exception as e:
                print(f"  ❌ Failed to move {file}: {e}")
    
    # Create summary file
    summary_file = os.path.join(folder_name, "ORGANIZATION_SUMMARY.txt")
    summary_content = f"""CV Files Organization Summary
{'='*40}

Organized at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Main folder: {folder_name}
Total files moved: {moved_count}

File organization:
• PDF files: pdf_files/
• DOCX files: docx_files/
• JSON files: json_files/
• Markdown files: markdown_files/
• Text files: text_files/
• Other files: other_files/

Original files have been moved from root directory to keep it clean.
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"\n📋 Summary file created: {summary_file}")
    print(f"🎉 Organization completed! {moved_count} files moved to {folder_name}/")
    
    # Show final structure
    print(f"\n📁 Final folder structure:")
    for root, dirs, files in os.walk(folder_name):
        level = root.replace(folder_name, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '  ' * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

if __name__ == "__main__":
    organize_cv_files()

