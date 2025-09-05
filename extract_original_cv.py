#!/usr/bin/env python3
"""
Extract Original CV Content
Reads the user's original CV PDF and extracts the exact details
"""
import PyPDF2
import re
from pathlib import Path

def extract_pdf_text(pdf_path):
    """Extract text from PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def analyze_cv_content(text):
    """Analyze the CV content and extract key information"""
    if not text:
        return None
    
    print("=== ORIGINAL CV CONTENT ===")
    print(text)
    print("=" * 50)
    
    # Extract key sections
    sections = {}
    
    # Look for contact information
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        sections['email'] = email_match.group()
    
    phone_match = re.search(r'\+?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}', text)
    if phone_match:
        sections['phone'] = phone_match.group()
    
    # Look for skills
    skills_pattern = r'(?:Skills?|Technologies?|Technologies?|Tools?)[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)'
    skills_match = re.search(skills_pattern, text, re.IGNORECASE | re.DOTALL)
    if skills_match:
        sections['skills'] = skills_match.group(1).strip()
    
    # Look for experience
    exp_pattern = r'(?:Experience|Work History|Employment)[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)'
    exp_match = re.search(exp_pattern, text, re.IGNORECASE | re.DOTALL)
    if exp_match:
        sections['experience'] = exp_match.group(1).strip()
    
    # Look for education
    edu_pattern = r'(?:Education|Academic|Degree)[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)'
    edu_match = re.search(edu_pattern, text, re.IGNORECASE | re.DOTALL)
    if exp_match:
        sections['education'] = edu_match.group(1).strip()
    
    return sections

def main():
    """Main function"""
    original_cv = "Abdallah Nasr Ali_Cv.pdf"
    
    if not Path(original_cv).exists():
        print(f"❌ Original CV not found: {original_cv}")
        return
    
    print(f"📄 Reading original CV: {original_cv}")
    
    # Extract text from PDF
    text = extract_pdf_text(original_cv)
    if not text:
        print("❌ Failed to extract text from PDF")
        return
    
    # Analyze content
    sections = analyze_cv_content(text)
    
    # Save extracted content
    output_file = "extracted_cv_content.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== EXTRACTED CV CONTENT ===\n")
        f.write(text)
        f.write("\n\n=== EXTRACTED SECTIONS ===\n")
        for section, content in sections.items():
            f.write(f"\n{section.upper()}:\n{content}\n")
    
    print(f"✅ Extracted content saved to: {output_file}")
    print("\nNow you can update the CV generator with these exact details!")

if __name__ == "__main__":
    main()
