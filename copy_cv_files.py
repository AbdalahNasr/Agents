#!/usr/bin/env python3
"""
Copy CV Files to Organized Structure
"""

import os
import shutil
from datetime import datetime

def copy_cv_files_to_organized_structure():
    """Copy CV files to the organized structure."""
    
    # Find the most recent organized folder
    organized_folders = [d for d in os.listdir('.') if d.startswith('ALL_CV_FILES_')]
    if not organized_folders:
        print("❌ No organized folders found!")
        return
    
    # Get the most recent one
    latest_folder = max(organized_folders)
    print(f"📁 Using organized folder: {latest_folder}")
    
    # Paths
    main_folder = latest_folder
    all_folder = os.path.join(main_folder, "ALL")
    
    # Find the date/time subfolder
    date_folders = [d for d in os.listdir(all_folder) if os.path.isdir(os.path.join(all_folder, d))]
    if not date_folders:
        print("❌ No date folders found in ALL!")
        return
    
    date_folder = date_folders[0]
    time_folders = [d for d in os.listdir(os.path.join(all_folder, date_folder)) if os.path.isdir(os.path.join(all_folder, date_folder, d))]
    if not time_folders:
        print("❌ No time folders found!")
        return
    
    time_folder = time_folders[0]
    target_path = os.path.join(all_folder, date_folder, time_folder)
    
    print(f"📁 Target path: {target_path}")
    
    # Find CV files in the main organized folders
    cv_files = []
    for folder in ['PDF', 'DOCX', 'JSON', 'MARKDOWN', 'TEXT']:
        folder_path = os.path.join(main_folder, folder)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.startswith('cv_'):
                    cv_files.append((folder, file))
                    print(f"  Found: {folder}/{file}")
    
    print(f"\n🎯 Total CV files found: {len(cv_files)}")
    
    # Copy files to the ALL/date/time structure
    copied_count = 0
    
    for folder_type, file in cv_files:
        try:
            # Source path (from main organized folders)
            source_path = os.path.join(main_folder, folder_type, file)
            
            # Destination path (to ALL/date/time structure)
            dest_folder = os.path.join(target_path, folder_type)
            dest_path = os.path.join(dest_folder, file)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            print(f"  ✅ Copied: {folder_type}/{file}")
            copied_count += 1
            
        except Exception as e:
            print(f"  ❌ Failed to copy {file}: {e}")
    
    print(f"\n🎉 Copy completed! {copied_count} files copied to {target_path}")
    
    # Show final structure
    print(f"\n📁 Final structure:")
    show_structure(target_path)

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
    copy_cv_files_to_organized_structure()

