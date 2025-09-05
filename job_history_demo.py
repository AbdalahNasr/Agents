#!/usr/bin/env python3
"""
Job History Demo
Demonstrates the complete job application history tracking system

Features:
- Job application history storage
- Search and filter capabilities
- Statistics and analytics
- Export functionality
- Integration with Notion
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from entry_level_job_application import EntryLevelJobApplication
from agents.job_history_manager import JobHistoryManager

def main():
    """Demonstrate job history tracking"""
    print("📚 JOB APPLICATION HISTORY DEMO")
    print("=" * 50)
    print("Complete job application tracking and analytics")
    print()
    
    # Initialize the system
    app_system = EntryLevelJobApplication()
    history_manager = JobHistoryManager()
    
    print("📝 Step 1: Create Multiple Job Applications")
    print("-" * 45)
    
    # Create sample job applications
    sample_jobs = [
        {
            "title": "Junior Full Stack Developer",
            "company": "TechCorp",
            "location": "Cairo, Egypt",
            "description": "Looking for a junior developer with React and Node.js experience...",
            "salary": "6000-8000 EGP",
            "job_type": "Full-time"
        },
        {
            "title": "Frontend Developer Intern",
            "company": "Digital Agency",
            "location": "Cairo, Egypt",
            "description": "Internship position for frontend development...",
            "salary": "3000-4000 EGP",
            "job_type": "Internship"
        },
        {
            "title": "Junior Web Developer",
            "company": "E-commerce Company",
            "location": "Cairo, Egypt",
            "description": "Junior web developer position...",
            "salary": "5000-7000 EGP",
            "job_type": "Full-time"
        },
        {
            "title": "React Developer",
            "company": "StartupXYZ",
            "location": "Remote",
            "description": "Remote React developer position...",
            "salary": "7000-9000 EGP",
            "job_type": "Full-time"
        },
        {
            "title": "Full Stack Developer",
            "company": "TechCorp",  # Same company as first
            "location": "Cairo, Egypt",
            "description": "Another position at TechCorp...",
            "salary": "8000-10000 EGP",
            "job_type": "Full-time"
        }
    ]
    
    application_ids = []
    
    for i, job in enumerate(sample_jobs, 1):
        print(f"Creating application {i}: {job['title']} at {job['company']}")
        
        # Create application package
        package = app_system.create_application_package(job)
        
        if package and package.get('application_id'):
            application_ids.append(package['application_id'])
            print(f"✅ Application created: {package['application_id']}")
        else:
            print("❌ Application creation failed")
        print()
    
    print("📊 Step 2: Update Application Statuses")
    print("-" * 40)
    
    # Simulate different outcomes for applications
    status_updates = [
        (application_ids[0], "Interview Scheduled", "Phone interview scheduled for next week"),
        (application_ids[1], "Rejected", "Thank you for your interest. We've decided to move forward with other candidates."),
        (application_ids[2], "Interview Completed", "Technical interview completed. Waiting for feedback."),
        (application_ids[3], "Offer Received", "Congratulations! We'd like to offer you the position."),
        (application_ids[4], "Applied", "Application submitted, waiting for response")
    ]
    
    for app_id, status, notes in status_updates:
        if app_id:
            print(f"Updating {app_id} to: {status}")
            success = history_manager.update_application_status(app_id, status, notes)
            if success:
                print(f"✅ Status updated successfully")
            else:
                print(f"❌ Status update failed")
            print()
    
    print("📅 Step 3: Add Interviews and Follow-ups")
    print("-" * 45)
    
    # Add interviews
    if application_ids[0]:  # TechCorp - Interview Scheduled
        interview_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        history_manager.add_interview(
            application_ids[0], 
            interview_date, 
            "Phone", 
            "Sarah Johnson - HR Manager", 
            "Technical interview focusing on React and Node.js"
        )
        print(f"✅ Interview added for TechCorp: {interview_date}")
    
    # Add follow-ups
    if application_ids[2]:  # E-commerce Company - Interview Completed
        follow_up_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        history_manager.add_follow_up(
            application_ids[2], 
            follow_up_date, 
            "Email", 
            "Follow up on interview feedback"
        )
        print(f"✅ Follow-up added for E-commerce Company: {follow_up_date}")
    
    if application_ids[3]:  # StartupXYZ - Offer Received
        follow_up_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        history_manager.add_follow_up(
            application_ids[3], 
            follow_up_date, 
            "Call", 
            "Discuss offer details and start date"
        )
        print(f"✅ Follow-up added for StartupXYZ: {follow_up_date}")
    
    print()
    
    print("📈 Step 4: Get Application Statistics")
    print("-" * 40)
    
    # Get comprehensive statistics
    stats = app_system.get_application_statistics()
    
    print("📊 JOB APPLICATION STATISTICS:")
    print(f"   Total Applications: {stats['total_applications']}")
    print(f"   Response Rate: {stats['response_rate']}%")
    print(f"   Interview Rate: {stats['interview_rate']}%")
    print(f"   Offer Rate: {stats['offer_rate']}%")
    print(f"   Average Response Time: {stats['average_response_time']} days")
    print()
    
    print("📋 STATUS BREAKDOWN:")
    for status, count in stats['status_breakdown'].items():
        percentage = (count / stats['total_applications']) * 100 if stats['total_applications'] > 0 else 0
        print(f"   {status}: {count} ({percentage:.1f}%)")
    print()
    
    print("🏢 TOP COMPANIES:")
    for company, count in stats['most_applied_companies'][:5]:
        print(f"   {company}: {count} applications")
    print()
    
    print("📅 RECENT ACTIVITY (Last 30 days):")
    print(f"   Applications: {stats['recent_applications_count']}")
    if stats['application_timeline']:
        print("   Recent Applications:")
        for app in stats['application_timeline'][:5]:
            print(f"     • {app['company']} - {app['position']} ({app['status']})")
    print()
    
    print("🔍 Step 5: Search and Filter Applications")
    print("-" * 45)
    
    # Search applications
    print("Searching for 'TechCorp' applications:")
    techcorp_apps = app_system.search_applications("TechCorp")
    for app in techcorp_apps:
        print(f"   • {app['job_info']['title']} - {app['status']} ({app['applied_date'][:10]})")
    print()
    
    print("Searching for 'React' positions:")
    react_apps = app_system.search_applications("React")
    for app in react_apps:
        print(f"   • {app['job_info']['company']} - {app['job_info']['title']} ({app['status']})")
    print()
    
    # Filter by status
    print("Applications with 'Interview Scheduled' status:")
    interview_apps = app_system.get_job_application_history(status_filter="Interview Scheduled")
    for app in interview_apps:
        print(f"   • {app['job_info']['company']} - {app['job_info']['title']}")
    print()
    
    print("⏰ Step 6: Check Upcoming Follow-ups")
    print("-" * 40)
    
    # Get upcoming follow-ups
    follow_ups = app_system.get_upcoming_follow_ups()
    
    if follow_ups:
        print(f"📅 Upcoming Follow-ups ({len(follow_ups)}):")
        for follow_up in follow_ups:
            print(f"   {follow_up['company']} - {follow_up['position']}")
            print(f"   Date: {follow_up['follow_up_date']}")
            print(f"   Type: {follow_up['follow_up_type']}")
            print(f"   Notes: {follow_up['notes']}")
            print()
    else:
        print("✅ No upcoming follow-ups")
    
    print("📋 Step 7: Get Application Summary")
    print("-" * 35)
    
    # Get formatted summary
    summary = app_system.get_application_summary()
    print(summary)
    
    print("💾 Step 8: Export Application History")
    print("-" * 40)
    
    # Export history
    export_file = app_system.export_application_history()
    if export_file:
        print(f"✅ Application history exported to: {export_file}")
    else:
        print("❌ Export failed")
    
    print()
    print("🎉 JOB HISTORY DEMO COMPLETED!")
    print("=" * 50)
    print("✅ Multiple job applications created and tracked")
    print("✅ Application statuses updated")
    print("✅ Interviews and follow-ups added")
    print("✅ Comprehensive statistics generated")
    print("✅ Search and filter functionality demonstrated")
    print("✅ Application history exported")
    print()
    print("💡 BENEFITS OF JOB HISTORY TRACKING:")
    print("   • Complete record of all job applications")
    print("   • Track application progress and outcomes")
    print("   • Monitor response rates and success metrics")
    print("   • Never lose track of important follow-ups")
    print("   • Export data for backup or analysis")
    print("   • Search and filter applications easily")
    print("   • Generate insights for job search strategy")

def demonstrate_history_features():
    """Demonstrate specific history features"""
    print("🔧 JOB HISTORY FEATURES DEMONSTRATION")
    print("=" * 45)
    
    history_manager = JobHistoryManager()
    
    print("📚 Available History Features:")
    print("   • Add new job applications")
    print("   • Update application status")
    print("   • Add interview information")
    print("   • Add follow-up reminders")
    print("   • Search applications by company/position")
    print("   • Filter by status, company, or date")
    print("   • Generate comprehensive statistics")
    print("   • Export history to JSON file")
    print("   • Get upcoming follow-ups")
    print("   • Mark follow-ups as completed")
    print()
    
    print("📊 Statistics Available:")
    print("   • Total applications count")
    print("   • Response rate percentage")
    print("   • Interview rate percentage")
    print("   • Offer rate percentage")
    print("   • Average response time")
    print("   • Status breakdown")
    print("   • Company breakdown")
    print("   • Most applied companies")
    print("   • Recent activity timeline")
    print()
    
    print("🔍 Search Capabilities:")
    print("   • Search by company name")
    print("   • Search by position title")
    print("   • Search by job description")
    print("   • Search by notes")
    print("   • Case-insensitive search")
    print()
    
    print("📁 File Storage:")
    print("   • Local JSON file: job_application_history.json")
    print("   • Automatic backup on every update")
    print("   • Export functionality for data portability")
    print("   • Integration with Notion for cloud backup")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Job History Demo")
    parser.add_argument("--features", action="store_true", help="Show history features")
    
    args = parser.parse_args()
    
    if args.features:
        demonstrate_history_features()
    else:
        main()
