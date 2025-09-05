#!/usr/bin/env python3
"""
Enhanced CV File Organizer with Nested ALL Folder
Creates timestamped subfolders inside ALL folder for each generation
"""

import os
import shutil
from datetime import datetime

def create_enhanced_organization():
    """Create enhanced CV organization with nested ALL folder."""
    
    # Create main timestamped folder
    main_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_folder = f"ALL_CV_FILES_{main_timestamp}"
    
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        print(f"📁 Created main folder: {main_folder}")
    
    # Create standard subfolders
    standard_folders = ['PDF', 'DOCX', 'JSON', 'MARKDOWN', 'TEXT']
    for folder in standard_folders:
        folder_path = os.path.join(main_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # Create the special ALL folder
    all_folder = os.path.join(main_folder, "ALL")
    if not os.path.exists(all_folder):
        os.makedirs(all_folder)
        print(f"📁 Created ALL folder: {all_folder}")
    
    # Create date/time subfolder inside ALL
    current_time = datetime.now()
    date_time_folder = current_time.strftime("%Y-%m-%d_%I%p").replace("_", "/")  # e.g., "2025-01-09/4PM"
    date_time_path = os.path.join(all_folder, date_time_folder)
    
    if not os.path.exists(date_time_path):
        os.makedirs(date_time_path)
        print(f"📁 Created date/time folder: {date_time_folder}")
    
    # Create subfolders inside date/time folder
    for folder in standard_folders:
        subfolder_path = os.path.join(date_time_path, folder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    
    # Search for CV files
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
            continue
        for file in files:
            if file.startswith('cv_'):
                cv_files_found.append((root, file))
                print(f"  Found: {root}/{file}")
    
    print(f"\n🎯 Total CV files found: {len(cv_files_found)}")
    
    # Move files to both locations:
    # 1. Main organized folders (PDF/, DOCX/, etc.)
    # 2. ALL/date-time/subfolders with timestamped filenames
    
    moved_count = 0
    
    for root, file in cv_files_found:
        try:
            # Determine file type
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
                dest_folder = 'TEXT'
            
            # 1. Copy to main organized folders
            source_path = os.path.join(root, file)
            main_dest_path = os.path.join(main_folder, dest_folder, file)
            shutil.copy2(source_path, main_dest_path)
            
            # 2. Copy to ALL/date-time/subfolders with timestamped filename
            file_name, file_ext = os.path.splitext(file)
            timestamped_filename = f"{file_name}_{main_timestamp}{file_ext}"
            all_dest_path = os.path.join(date_time_path, dest_folder, timestamped_filename)
            shutil.copy2(source_path, all_dest_path)
            
            print(f"  ✅ Organized: {file}")
            print(f"     → Main: {dest_folder}/{file}")
            print(f"     → ALL: {dest_folder}/{timestamped_filename}")
            
            moved_count += 1
            
        except Exception as e:
            print(f"  ❌ Failed to organize {file}: {e}")
    
    # Create summary files
    create_summary_files(main_folder, all_folder, date_time_folder, moved_count, cv_files_found)
    
    print(f"\n🎉 Enhanced organization completed!")
    print(f"📁 Main folder: {main_folder}")
    print(f"📁 ALL folder: {all_folder}/{date_time_folder}")
    print(f"📊 Files organized: {moved_count}")
    
    # Show final structure
    print(f"\n📁 Final folder structure:")
    show_folder_structure(main_folder)

def create_summary_files(main_folder, all_folder, date_time_folder, moved_count, cv_files_found):
    """Create summary files in both locations."""
    
    # Main summary
    main_summary = os.path.join(main_folder, "MAIN_SUMMARY.txt")
    main_content = f"""CV Files Organization - Main Summary
{'='*50}

Organized at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Main folder: {main_folder}
Files organized: {moved_count}

Standard organization:
• PDF/ - All PDF CV files
• DOCX/ - All DOCX CV files  
• JSON/ - All JSON CV files
• MARKDOWN/ - All Markdown CV files
• TEXT/ - All text CV files

Special organization:
• ALL/ - Contains date/time subfolders with timestamped files
  └── {date_time_folder}/
      ├── PDF/ - Timestamped PDF files
      ├── DOCX/ - Timestamped DOCX files
      ├── JSON/ - Timestamped JSON files
      ├── MARKDOWN/ - Timestamped Markdown files
      └── TEXT/ - Timestamped text files

All CV files are organized in both standard and timestamped formats.
"""
    
    with open(main_summary, 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    # ALL folder summary
    all_summary = os.path.join(all_folder, date_time_folder, "GENERATION_SUMMARY.txt")
    all_content = f"""CV Generation Summary - {date_time_folder}
{'='*50}

Generated at: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Date/Time folder: {date_time_folder}
Files organized: {moved_count}

This folder contains timestamped versions of all CV files.
Each file has been renamed with the generation timestamp.

File organization:
• PDF/ - Timestamped PDF CV files
• DOCX/ - Timestamped DOCX CV files
• JSON/ - Timestamped JSON data files
• MARKDOWN/ - Timestamped Markdown files
• TEXT/ - Timestamped text files

Example filenames:
• cv_frontend_20250109_174725.pdf
• cv_backend_20250109_174725.docx
• cv_fullstack_20250109_174725.json

This allows you to track different versions of your CVs over time.
"""
    
    with open(all_summary, 'w', encoding='utf-8') as f:
        f.write(all_content)
    
    print(f"📋 Main summary: {main_summary}")
    print(f"📋 ALL summary: {all_summary}")

def show_folder_structure(folder_path, level=0):
    """Show the folder structure with proper indentation."""
    indent = "  " * level
    
    if os.path.isdir(folder_path):
        print(f"{indent}{os.path.basename(folder_path)}/")
        
        try:
            items = os.listdir(folder_path)
            # Sort: folders first, then files
            folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]
            files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
            
            # Show folders first
            for folder in sorted(folders):
                show_folder_structure(os.path.join(folder_path, folder), level + 1)
            
            # Show files
            for file in sorted(files):
                print(f"{indent}  {file}")
                
        except PermissionError:
            print(f"{indent}  [Access Denied]")

if __name__ == "__main__":
    create_enhanced_organization()

