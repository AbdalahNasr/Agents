#!/usr/bin/env python3
"""
🔧 GITHUB REPOSITORY FIXER - Fixes repository names and deployment issues
Helps rename repositories and fix GitHub Pages deployment
"""
import os
import sys
import json
import requests
from datetime import datetime

def analyze_github_issues():
    """Analyze GitHub repository issues"""
    print("🔧 GITHUB REPOSITORY ISSUE ANALYZER")
    print("=" * 60)
    
    # Current problematic repositories
    problematic_repos = {
        "E-commerce -demo": {
            "current_name": "E-commerce -demo",
            "fixed_name": "E-commerce-demo",
            "issues": [
                "Extra space in repository name",
                "Broken GitHub Pages URL",
                "Invalid URL characters"
            ],
            "current_url": "https://abdalahnasr.github.io/E-commerce -demo/",
            "fixed_url": "https://abdalahnasr.github.io/E-commerce-demo/"
        },
        "istqp -quiz": {
            "current_name": "istqp -quiz", 
            "fixed_name": "istqp-quiz",
            "issues": [
                "Extra space in repository name",
                "Broken GitHub Pages URL",
                "Invalid URL characters"
            ],
            "current_url": "https://abdalahnasr.github.io/istqp -quiz/",
            "fixed_url": "https://abdalahnasr.github.io/istqp-quiz/"
        }
    }
    
    print("🔍 PROBLEMATIC REPOSITORIES IDENTIFIED:")
    print()
    
    for repo, info in problematic_repos.items():
        print(f"📁 {repo}:")
        print(f"   ❌ Current Name: {info['current_name']}")
        print(f"   ✅ Fixed Name: {info['fixed_name']}")
        print(f"   🔗 Current URL: {info['current_url']}")
        print(f"   🔗 Fixed URL: {info['fixed_url']}")
        print(f"   ⚠️ Issues:")
        for issue in info['issues']:
            print(f"      • {issue}")
        print()
    
    return problematic_repos

def create_fix_instructions():
    """Create step-by-step fix instructions"""
    print("=" * 60)
    print("🔧 STEP-BY-STEP FIX INSTRUCTIONS")
    print("=" * 60)
    
    instructions = """
📋 STEP 1: RENAME REPOSITORIES ON GITHUB

1. **Go to GitHub.com and sign in**
2. **Navigate to each problematic repository:**
   - E-commerce -demo
   - istqp -quiz

3. **Click Settings tab**
4. **Scroll down to "Repository name" section**
5. **Click "Rename" button**
6. **Enter new name without spaces:**
   - E-commerce -demo → E-commerce-demo
   - istqp -quiz → istqp-quiz
7. **Click "Rename this repository"**
8. **Confirm the change**

📋 STEP 2: UPDATE PACKAGE.JSON FILES

1. **Clone the renamed repositories locally:**
   ```bash
   git clone https://github.com/AbdalahNasr/E-commerce-demo.git
   git clone https://github.com/AbdalahNasr/istqp-quiz.git
   ```

2. **Update package.json in E-commerce-demo:**
   ```json
   {
     "name": "e-commerce-demo",
     "homepage": "https://abdalahnasr.github.io/E-commerce-demo",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```

3. **Update package.json in istqp-quiz:**
   ```json
   {
     "name": "istqp-quiz",
     "homepage": "https://abdalahnasr.github.io/istqp-quiz",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```

📋 STEP 3: UPDATE README.MD FILES

1. **Fix all broken links in README.md**
2. **Use clean URLs without spaces**
3. **Update project descriptions**

📋 STEP 4: REDEPLOY TO GITHUB PAGES

1. **Install gh-pages if not installed:**
   ```bash
   npm install --save-dev gh-pages
   ```

2. **Build and deploy:**
   ```bash
   npm run deploy
   ```

3. **Enable GitHub Pages in repository settings:**
   - Go to Settings → Pages
   - Set Source to "Deploy from a branch"
   - Select "gh-pages" branch
   - Click Save

📋 STEP 5: VERIFY FIXES

1. **Test all links work:**
   - https://abdalahnasr.github.io/E-commerce-demo/
   - https://abdalahnasr.github.io/istqp-quiz/

2. **Check GitHub Pages deployment status**
3. **Update your CV with new working links**
"""
    
    print(instructions)
    return instructions

def create_clean_repository_structure():
    """Create clean repository structure recommendations"""
    print("\n" + "=" * 60)
    print("📁 CLEAN REPOSITORY STRUCTURE")
    print("=" * 60)
    
    structure = """
🚀 RECOMMENDED REPOSITORY STRUCTURE:

📁 E-commerce-demo/
├── README.md (with clean links)
├── package.json (updated homepage)
├── src/
├── public/
└── .github/ (for GitHub Actions)

📁 istqp-quiz/
├── README.md (with clean links)
├── package.json (updated homepage)
├── src/
├── public/
└── .github/ (for GitHub Actions)

📁 recipes/
├── README.md
├── package.json
└── src/

📁 portfolio/ (NEW - Optional)
├── README.md
├── package.json
└── src/
"""
    
    print(structure)
    return structure

def create_automated_fix_script():
    """Create an automated fix script"""
    print("\n" + "=" * 60)
    print("🤖 AUTOMATED FIX SCRIPT")
    print("=" * 60)
    
    script = """
#!/bin/bash
# AUTOMATED GITHUB REPOSITORY FIXER

echo "🔧 Starting GitHub Repository Fix Process..."

# Clone repositories
echo "📥 Cloning repositories..."
git clone https://github.com/AbdalahNasr/E-commerce-demo.git
git clone https://github.com/AbdalahNasr/istqp-quiz.git

# Fix E-commerce-demo
echo "🔧 Fixing E-commerce-demo..."
cd E-commerce-demo
npm install --save-dev gh-pages
npm run build
npm run deploy
cd ..

# Fix istqp-quiz  
echo "🔧 Fixing istqp-quiz..."
cd istqp-quiz
npm install --save-dev gh-pages
npm run build
npm run deploy
cd ..

echo "✅ Repository fixes completed!"
echo "🔗 Check your GitHub Pages deployment status"
"""
    
    print("📝 AUTOMATED FIX SCRIPT:")
    print(script)
    
    print("\n💡 SAVE THIS AS 'fix_github_repos.sh' AND RUN:")
    print("   chmod +x fix_github_repos.sh")
    print("   ./fix_github_repos.sh")
    
    return script

def create_cv_update_guide():
    """Create guide for updating CV with fixed links"""
    print("\n" + "=" * 60)
    print("📝 CV UPDATE GUIDE")
    print("=" * 60)
    
    guide = """
📋 UPDATE YOUR CV WITH FIXED LINKS:

🚀 PROJECTS SECTION:

**E-commerce Demo - React Storefront**
- Code: https://github.com/AbdalahNasr/E-commerce-demo
- Live Demo: https://abdalahnasr.github.io/E-commerce-demo/
- Technologies: React, JavaScript
- Status: ✅ Working - Clean URLs

**ISTQP Quiz App - Quiz Platform**  
- Code: https://github.com/AbdalahNasr/istqp-quiz
- Live Demo: https://istqp-quiz.vercel.app
- Technologies: Next.js, TypeScript, Tailwind CSS, PostCSS
- Features: JSON-based quizzes, multilingual support, ESLint, SSR
- Status: ✅ Working - Clean URLs

**Recipes App**
- Code: https://github.com/AbdalahNasr/recipes
- Status: ✅ Working

📎 CONTACT SECTION:
- CV: https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing
- GitHub: https://github.com/AbdalahNasr
- LinkedIn: [Your LinkedIn Profile]
"""
    
    print(guide)
    return guide

def main():
    """Main function to fix GitHub repositories"""
    print("🔧 GITHUB REPOSITORY FIXER")
    print("=" * 60)
    
    try:
        # Analyze GitHub issues
        problematic_repos = analyze_github_issues()
        
        # Create fix instructions
        fix_instructions = create_fix_instructions()
        
        # Create clean repository structure
        clean_structure = create_clean_repository_structure()
        
        # Create automated fix script
        automated_script = create_automated_fix_script()
        
        # Create CV update guide
        cv_guide = create_cv_update_guide()
        
        print("\n" + "=" * 60)
        print("🎉 GITHUB REPOSITORY FIX PLAN COMPLETE!")
        print("=" * 60)
        
        print("📋 WHAT NEEDS TO BE FIXED:")
        print("✅ Repository names (remove spaces)")
        print("✅ Package.json homepage URLs")
        print("✅ README.md broken links")
        print("✅ GitHub Pages deployment")
        print("✅ CV project links")
        
        print("\n📋 PRIORITY ORDER:")
        print("1. 🔧 Rename repositories on GitHub")
        print("2. 📝 Update package.json files")
        print("3. 🔄 Redeploy to GitHub Pages")
        print("4. ✅ Test all links work")
        print("5. 📋 Update your CV")
        
        print("\n🚀 Your GitHub repositories will be clean and professional!")
        
    except Exception as e:
        print(f"❌ Error creating GitHub fix plan: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
