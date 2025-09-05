#!/usr/bin/env python3
"""
Notion Workflow Demo
Demonstrates the complete job search workflow with Notion integration

Features:
- Job application tracking
- Interview scheduling
- Follow-up reminders
- Analytics and insights
- Response handling
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from entry_level_job_application import EntryLevelJobApplication
from agents.notion_manager import NotionManager

def main():
    """Demonstrate Notion workflow"""
    print("🔗 NOTION WORKFLOW DEMO")
    print("=" * 50)
    print("Complete job search workflow with Notion integration")
    print()
    
    # Initialize the system
    app_system = EntryLevelJobApplication()
    notion_manager = NotionManager()
    
    print("📋 Step 1: Create Job Application")
    print("-" * 30)
    
    # Create a job application
    sample_job = {
        "title": "Junior Full Stack Developer",
        "company": "TechCorp",
        "location": "Cairo, Egypt",
        "description": """
        We are looking for a Junior Full Stack Developer to join our team.
        The ideal candidate will have experience with React, Node.js, and modern web technologies.
        Experience with mobile development, APIs, and database management is required.
        Strong problem-solving skills and ability to work in fast-paced environments.
        """,
        "salary": "6000-8000 EGP",
        "job_type": "Full-time"
    }
    
    print(f"Creating application for: {sample_job['title']} at {sample_job['company']}")
    
    # Create application package
    package = app_system.create_application_package(sample_job)
    
    if package and package.get('notion_page_id'):
        notion_page_id = package['notion_page_id']
        print(f"✅ Application created and tracked in Notion: {notion_page_id}")
        print(f"📊 ATS Score: {package['cv_result']['ats_analysis']['overall_score']}/100")
    else:
        print("❌ Application creation failed or Notion not configured")
        print("\n📖 To set up Notion integration:")
        print(notion_manager.create_notion_setup_guide())
        return
    
    print("\n📅 Step 2: Handle Job Response - Interview Invitation")
    print("-" * 50)
    
    # Simulate interview invitation
    interview_details = {
        'interview_date': (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        'interview_type': 'Video',
        'interviewer': 'Sarah Johnson - HR Manager',
        'notes': 'Technical interview focusing on React and Node.js. Prepare for coding challenges.'
    }
    
    print(f"📞 Interview invitation received!")
    print(f"   Date: {interview_details['interview_date']}")
    print(f"   Type: {interview_details['interview_type']}")
    print(f"   Interviewer: {interview_details['interviewer']}")
    
    success = app_system.handle_job_response(
        notion_page_id, 
        "interview_invitation", 
        interview_details
    )
    
    if success:
        print("✅ Interview scheduled in Notion")
    else:
        print("❌ Failed to schedule interview")
    
    print("\n📧 Step 3: Add Follow-up Reminder")
    print("-" * 30)
    
    # Add follow-up reminder
    follow_up_details = {
        'follow_up_date': (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        'follow_up_type': 'Email',
        'notes': 'Send thank you email after interview and inquire about next steps'
    }
    
    print(f"⏰ Adding follow-up reminder for: {follow_up_details['follow_up_date']}")
    
    success = app_system.handle_job_response(
        notion_page_id, 
        "follow_up_needed", 
        follow_up_details
    )
    
    if success:
        print("✅ Follow-up reminder added")
    else:
        print("❌ Failed to add follow-up reminder")
    
    print("\n📊 Step 4: Get Job Search Analytics")
    print("-" * 35)
    
    # Get analytics
    analytics = app_system.get_job_search_analytics()
    
    if analytics:
        print("📈 Job Search Analytics:")
        print(f"   Total Applications: {analytics.get('total_applications', 0)}")
        print(f"   Response Rate: {analytics.get('response_rate', 0):.1f}%")
        print(f"   Interview Rate: {analytics.get('interview_rate', 0):.1f}%")
        print(f"   Unique Companies: {analytics.get('unique_companies', 0)}")
        
        status_breakdown = analytics.get('status_breakdown', {})
        if status_breakdown:
            print("   Status Breakdown:")
            for status, count in status_breakdown.items():
                print(f"     {status}: {count}")
    else:
        print("❌ Could not retrieve analytics")
    
    print("\n⏰ Step 5: Check Upcoming Follow-ups")
    print("-" * 35)
    
    # Get upcoming follow-ups
    follow_ups = app_system.get_upcoming_follow_ups()
    
    if follow_ups:
        print(f"📅 Upcoming Follow-ups ({len(follow_ups)}):")
        for follow_up in follow_ups:
            print(f"   {follow_up['company']} - {follow_up['position']}")
            print(f"   Date: {follow_up['follow_up_date']}")
            print(f"   Type: {follow_up['follow_up_type']}")
            print()
    else:
        print("✅ No upcoming follow-ups")
    
    print("\n🎯 Step 6: Simulate Different Response Types")
    print("-" * 45)
    
    # Simulate different response scenarios
    scenarios = [
        {
            "type": "rejection",
            "details": {"notes": "Thank you for your interest. We've decided to move forward with other candidates."},
            "description": "Rejection email received"
        },
        {
            "type": "offer",
            "details": {"notes": "Congratulations! We'd like to offer you the position. Salary: 7000 EGP/month."},
            "description": "Job offer received"
        }
    ]
    
    for scenario in scenarios:
        print(f"📧 {scenario['description']}")
        success = app_system.handle_job_response(
            notion_page_id, 
            scenario['type'], 
            scenario['details']
        )
        
        if success:
            print(f"✅ Status updated to: {scenario['type'].title()}")
        else:
            print(f"❌ Failed to update status")
        print()
    
    print("\n🎉 NOTION WORKFLOW DEMO COMPLETED!")
    print("=" * 50)
    print("✅ Job application created and tracked")
    print("✅ Interview scheduled")
    print("✅ Follow-up reminders added")
    print("✅ Analytics generated")
    print("✅ Response handling demonstrated")
    print()
    print("🔗 Check your Notion database to see all the entries!")
    print()
    print("💡 BENEFITS OF NOTION INTEGRATION:")
    print("   • Track all job applications in one place")
    print("   • Never miss an interview or follow-up")
    print("   • Monitor your job search progress")
    print("   • Generate insights and analytics")
    print("   • Stay organized and professional")

def demonstrate_notion_setup():
    """Demonstrate Notion setup process"""
    print("🔧 NOTION SETUP DEMONSTRATION")
    print("=" * 40)
    
    notion_manager = NotionManager()
    print(notion_manager.create_notion_setup_guide())
    
    print("\n📋 REQUIRED ENVIRONMENT VARIABLES:")
    print("   NOTION_TOKEN=your_notion_integration_token")
    print("   NOTION_DATABASE_ID=your_database_id")
    print()
    print("📝 Add these to your .env file to enable Notion integration")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Notion Workflow Demo")
    parser.add_argument("--setup", action="store_true", help="Show Notion setup guide")
    
    args = parser.parse_args()
    
    if args.setup:
        demonstrate_notion_setup()
    else:
        main()
