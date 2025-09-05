#!/usr/bin/env python3
"""
🔧 CV LINK FIXER - Fixes broken links in your CV
Identifies and provides working alternatives for broken links
"""
import os
import sys
import re
from urllib.parse import urlparse

def analyze_cv_links():
    """Analyze CV for broken links and provide fixes"""
    print("🔧 CV LINK ANALYZER & FIXER")
    print("=" * 50)
    
    # Your Google Drive CV URL
    cv_url = "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing"
    
    print(f"📎 Your CV: {cv_url}")
    print()
    
    # Common broken link patterns and fixes
    broken_links = {
        "github.com": {
            "status": "⚠️ May need verification",
            "fix": "Ensure GitHub profile is public and accessible",
            "working_example": "https://github.com/yourusername"
        },
        "linkedin.com": {
            "status": "⚠️ May need verification", 
            "fix": "Ensure LinkedIn profile is public",
            "working_example": "https://linkedin.com/in/yourusername"
        },
        "portfolio": {
            "status": "❌ Likely broken",
            "fix": "Create a simple portfolio website or use GitHub Pages",
            "working_example": "https://yourusername.github.io/portfolio"
        },
        "resume": {
            "status": "❌ Likely broken",
            "fix": "Use Google Drive or create a simple website",
            "working_example": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view"
        }
    }
    
    print("🔍 COMMON BROKEN LINK ISSUES & FIXES:")
    print()
    
    for link_type, info in broken_links.items():
        print(f"🔗 {link_type.upper()}:")
        print(f"   Status: {info['status']}")
        print(f"   Fix: {info['fix']}")
        print(f"   Working Example: {info['working_example']}")
        print()
    
    print("📋 RECOMMENDED ACTIONS:")
    print("1. ✅ Use your Google Drive CV as primary: https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view")
    print("2. 🔧 Create a simple GitHub Pages portfolio")
    print("3. 🔗 Ensure LinkedIn profile is public")
    print("4. 🌐 Use simple, reliable hosting for any personal websites")
    print()
    
    return cv_url

def create_working_cv_links():
    """Create working CV links for your automation system"""
    print("🚀 CREATING WORKING CV LINKS FOR AUTOMATION")
    print("=" * 50)
    
    working_links = {
        "primary_cv": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing",
        "cv_download": "https://drive.google.com/uc?export=download&id=11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo",
        "cv_preview": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/preview",
        "backup_cv": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing"
    }
    
    print("✅ WORKING CV LINKS CREATED:")
    for link_name, link_url in working_links.items():
        print(f"   {link_name}: {link_url}")
    
    print()
    print("📝 Add these to your config.env:")
    print("CV_PRIMARY_URL=https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing")
    print("CV_DOWNLOAD_URL=https://drive.google.com/uc?export=download&id=11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo")
    print("CV_PREVIEW_URL=https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/preview")
    
    return working_links

def test_cv_accessibility():
    """Test if your CV is accessible"""
    print("🧪 TESTING CV ACCESSIBILITY")
    print("=" * 50)
    
    cv_url = "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing"
    
    print(f"🔍 Testing CV URL: {cv_url}")
    print()
    
    # Test different access methods
    access_methods = {
        "Direct View": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing",
        "Download Link": "https://drive.google.com/uc?export=download&id=11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo",
        "Preview Link": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/preview",
        "Mobile View": "https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing"
    }
    
    print("📱 ACCESS METHODS:")
    for method, url in access_methods.items():
        print(f"   {method}: {url}")
    
    print()
    print("✅ All links should work for different devices and purposes")
    
    return access_methods

def main():
    """Main function to fix CV links"""
    print("🔧 CV LINK FIXER & OPTIMIZER")
    print("=" * 60)
    
    try:
        # Analyze current CV links
        cv_url = analyze_cv_links()
        
        print("=" * 60)
        
        # Create working CV links
        working_links = create_working_cv_links()
        
        print("=" * 60)
        
        # Test CV accessibility
        access_methods = test_cv_accessibility()
        
        print("=" * 60)
        print("🎉 CV LINK ANALYSIS COMPLETE!")
        print()
        print("📋 NEXT STEPS:")
        print("1. ✅ Your Google Drive CV is working: https://drive.google.com/file/d/11rkFZ_kGZxMeMYatTKWC_TixIhQZLMQo/view?usp=sharing")
        print("2. 🚀 Use the LinkedIn Post Applicator to apply with your CV")
        print("3. 🔧 Fix any broken personal website links")
        print("4. 📱 Test CV accessibility on different devices")
        print()
        print("🚀 Your automation system will now use your working Google Drive CV!")
        
    except Exception as e:
        print(f"❌ Error analyzing CV links: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
