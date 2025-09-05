#!/usr/bin/env python3
"""
Simple CV File Organizer - Finds and organizes ALL CV files
"""

import os
import shutil
from datetime import datetime

def find_and_organize_cv_files():
    """Find all CV files and organize them into one folder."""
    
    # Create timestamped folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_folder = f"ALL_CV_FILES_{timestamp}"
    
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        print(f"📁 Created main folder: {main_folder}")
    
    # Create subfolders
    subfolders = ['PDF', 'DOCX', 'JSON', 'MARKDOWN', 'TEXT']
    for subfolder in subfolders:
        subfolder_path = os.path.join(main_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    
    # Search for CV files in current directory and subdirectories
    cv_files_found = []
    
    print("🔍 Searching for CV files...")
    
    # Search current directory
    for file in os.listdir('.'):
        if os.path.isfile(file) and file.startswith('cv_'):
            cv_files_found.append(('.', file))
            print(f"  Found: {file}")
    
    # Search subdirectories
    for root, dirs, files in os.walk('.'):
        if root == '.':
            continue  # Skip current directory (already searched)
        
        for file in files:
            if file.startswith('cv_'):
                cv_files_found.append((root, file))
                print(f"  Found: {root}/{file}")
    
    print(f"\n🎯 Total CV files found: {len(cv_files_found)}")
    
    # Move files to organized folders
    moved_count = 0
    
    for root, file in cv_files_found:
        try:
            # Determine file type and destination
            file_ext = os.path.splitext(file)[1].lower()
            
            if file_ext == '.pdf':
                dest_folder = 'PDF'
            elif file_ext == '.docx':
                dest_folder = 'DOCX'
            elif file_ext == '.json':
                dest_folder = 'JSON'
            elif file_ext == '.md':
                dest_folder = 'MARKDOWN'
            elif file_ext == '.txt':
                dest_folder = 'TEXT'
            else:
                dest_folder = 'TEXT'  # Default to text
            
            # Source and destination paths
            source_path = os.path.join(root, file)
            dest_path = os.path.join(main_folder, dest_folder, file)
            
            # Move file
            shutil.move(source_path, dest_path)
            print(f"  ✅ Moved: {file} → {dest_folder}/")
            moved_count += 1
            
        except Exception as e:
            print(f"  ❌ Failed to move {file}: {e}")
    
    # Create summary
    summary_file = os.path.join(main_folder, "SUMMARY.txt")
    summary_content = f"""CV Files Organization Summary
{'='*40}

Organized at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Main folder: {main_folder}
Files found: {len(cv_files_found)}
Files moved: {moved_count}

Folder structure:
• PDF/ - All PDF CV files
• DOCX/ - All DOCX CV files  
• JSON/ - All JSON CV files
• MARKDOWN/ - All Markdown CV files
• TEXT/ - All text CV files

All CV files have been organized and moved from their original locations.
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"\n📋 Summary created: {summary_file}")
    print(f"🎉 Organization completed! {moved_count} files moved to {main_folder}/")
    
    # Show final structure
    print(f"\n📁 Final folder structure:")
    for root, dirs, files in os.walk(main_folder):
        level = root.replace(main_folder, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '  ' * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

if __name__ == "__main__":
    find_and_organize_cv_files()

