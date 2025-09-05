# CV Generation Commands Guide

## Quick Start

### 1. Generate All CV Formats (Recommended)
```bash
python fixed_pdf_cv_generator.py
```
**What it does:**
- Creates Markdown CV
- Creates Text CV  
- Creates HTML CV with working links
- Creates PDF CV using Reportlab
- Organizes all files in timestamped folder

### 2. If PDF Fails, Use HTML Method
```bash
python fixed_pdf_cv_generator.py
# Then open the HTML file in browser
# Press Ctrl+P → Save as PDF
```

## File Locations

After running the command, you'll find:
```
RELIABLE_CV_[timestamp]/
├── Abdallah_Nasr_Ali_CV.md
├── Abdallah_Nasr_Ali_CV.txt
├── Abdallah_Nasr_Ali_CV.html
├── Abdallah_Nasr_Ali_CV.pdf
└── UPDATE_GUIDE.txt
```

## Troubleshooting

### PDF Not Working?
- **HTML Method**: Open HTML file in browser → Print → Save as PDF
- **Check Reportlab**: `pip install reportlab` if missing

### Links Not Working?
- HTML file has clickable links
- Open in browser to test

### Need Different CV Content?
- Edit `create_cv_content()` function in the script
- Add new projects, skills, or experience
- Run script again

## Quick Commands

```bash
# Generate CVs
python fixed_pdf_cv_generator.py

# Check if reportlab is installed
python -c "import reportlab; print('✅ Reportlab OK')"

# Install reportlab if needed
pip install reportlab
```

## What Each Format Is For

- **Markdown (.md)**: GitHub, GitLab, documentation
- **Text (.txt)**: Plain text, email, simple sharing
- **HTML (.html)**: Web viewing, browser printing to PDF
- **PDF (.pdf)**: Professional printing, job applications
- **Guide (.txt)**: Instructions for updating CV content
