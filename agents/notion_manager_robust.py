#!/usr/bin/env python3
"""
Robust Notion Manager that handles dynamic property mapping
"""

import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class RobustNotionManager:
    def __init__(self):
        load_dotenv('config.env')
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        self.database_properties = None
        self._load_database_properties()
    
    def _load_database_properties(self):
        """Load and cache database properties"""
        if not self.notion_token or not self.notion_database_id:
            print("❌ Notion credentials not found")
            return
        
        try:
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            
            # Add timeout to prevent hanging
            response = requests.get(
                f"https://api.notion.com/v1/databases/{self.notion_database_id}",
                headers=headers,
                timeout=10  # 10 second timeout
            )
            
            if response.status_code == 200:
                db_info = response.json()
                self.database_properties = db_info.get('properties', {})
                print(f"✅ Loaded {len(self.database_properties)} database properties")
            else:
                print(f"❌ Failed to load database properties: {response.status_code}")
                # Use fallback properties if API fails
                self._use_fallback_properties()
                
        except requests.exceptions.Timeout:
            print("⏰ Notion API timeout - using fallback properties")
            self._use_fallback_properties()
        except Exception as e:
            print(f"❌ Error loading database properties: {e}")
            self._use_fallback_properties()
    
    def _use_fallback_properties(self):
        """Use fallback properties when API is unavailable"""
        self.database_properties = {
            "Company\xa0": {"type": "title"},
            "Position\xa0": {"type": "rich_text"},
            "Location": {"type": "url"},
            "Salary ": {"type": "rich_text"},
            "Job Type": {"type": "select"},
            "Applied Date": {"type": "date"},
            "Job Description": {"type": "rich_text"},
            "Status": {"type": "status"}
        }
        print("🔄 Using fallback database properties")
    
    def _map_job_to_properties(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """Map job details to available database properties"""
        if not self.database_properties:
            print("❌ No database properties available")
            return {}
        
        mapped_properties = {}
        
        # Define property mapping rules
        property_mappings = {
            # Title properties (for company/position)
            'title': [
                'Company\xa0', 'Company ', 'Company', 'Name', 'Title'
            ],
            # Rich text properties
            'rich_text': [
                'Position\xa0', 'Position ', 'Position', 'Text', 'Description', 
                'Job Description', 'Salary ', 'Salary', 'CV Files'
            ],
            # URL properties
            'url': [
                'Location', 'URL', 'Link', 'Job URL'
            ],
            # Select properties
            'select': [
                'Job Type', 'Status', 'Type', 'Category'
            ],
            # Date properties
            'date': [
                'Applied Date', 'Date', 'Created Date', 'Application Date'
            ]
        }
        
        # Try to map each job field to available properties
        job_mappings = {
            'company': f"{job_details.get('company', 'Unknown')} - {job_details.get('title', 'Position')}",
            'title': job_details.get('title', 'Position'),
            'url': job_details.get('url', 'https://example.com'),
            'salary': job_details.get('salary', 'Not specified'),
            'job_type': job_details.get('job_type', 'Full-time'),
            'description': job_details.get('description', 'No description available'),
            'status': 'Applied'
        }
        
        # Map to available properties
        for field, value in job_mappings.items():
            if field == 'company':
                # Try to find a title property
                for prop_name in property_mappings['title']:
                    if prop_name in self.database_properties:
                        prop_type = self.database_properties[prop_name]['type']
                        if prop_type == 'title':
                            mapped_properties[prop_name] = {
                                "title": [{"text": {"content": value}}]
                            }
                            break
            
            elif field == 'title':
                # Try to find a rich text property for position
                for prop_name in property_mappings['rich_text']:
                    if prop_name in self.database_properties:
                        prop_type = self.database_properties[prop_name]['type']
                        if prop_type == 'rich_text':
                            mapped_properties[prop_name] = {
                                "rich_text": [{"text": {"content": value}}]
                            }
                            break
            
            elif field == 'url':
                # Try to find a URL property
                for prop_name in property_mappings['url']:
                    if prop_name in self.database_properties:
                        prop_type = self.database_properties[prop_name]['type']
                        if prop_type == 'url':
                            mapped_properties[prop_name] = {"url": value}
                            break
            
            elif field == 'salary':
                # Try to find a rich text property for salary
                for prop_name in property_mappings['rich_text']:
                    if prop_name in self.database_properties and 'salary' in prop_name.lower():
                        prop_type = self.database_properties[prop_name]['type']
                        if prop_type == 'rich_text':
                            mapped_properties[prop_name] = {
                                "rich_text": [{"text": {"content": value}}]
                            }
                            break
            
            elif field == 'job_type':
                # Try to find a select property
                for prop_name in property_mappings['select']:
                    if prop_name in self.database_properties:
                        prop_type = self.database_properties[prop_name]['type']
                        if prop_type == 'select':
                            mapped_properties[prop_name] = {
                                "select": {"name": value}
                            }
                            break
            
            elif field == 'description':
                # Try to find a rich text property for description
                for prop_name in property_mappings['rich_text']:
                    if prop_name in self.database_properties and 'description' in prop_name.lower():
                        prop_type = self.database_properties[prop_name]['type']
                        if prop_type == 'rich_text':
                            mapped_properties[prop_name] = {
                                "rich_text": [{"text": {"content": value}}]
                            }
                            break
            
            elif field == 'status':
                # Try to find a status property
                for prop_name in property_mappings['select']:
                    if prop_name in self.database_properties and 'status' in prop_name.lower():
                        prop_type = self.database_properties[prop_name]['type']
                        if prop_type == 'status':
                            # Use a valid status option
                            mapped_properties[prop_name] = {
                                "status": {"name": "Not started"}  # Use valid option
                            }
                            break
        
        # Add date if available
        for prop_name in property_mappings['date']:
            if prop_name in self.database_properties:
                prop_type = self.database_properties[prop_name]['type']
                if prop_type == 'date':
                    mapped_properties[prop_name] = {
                        "date": {"start": datetime.now().strftime('%Y-%m-%d')}
                    }
                    break
        
        return mapped_properties
    
    def create_job_application_entry(self, job_details: Dict[str, Any], application_result: Dict[str, Any] = None) -> Optional[str]:
        """Create a job application entry in Notion with dynamic property mapping"""
        if not self.notion_token or not self.notion_database_id:
            print("❌ Notion not configured")
            return None
        
        if not self.database_properties:
            print("❌ Database properties not loaded")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            
            # Map job details to available properties
            mapped_properties = self._map_job_to_properties(job_details)
            
            # Add application result information if available
            if application_result and application_result.get('submitted_answers'):
                # Add submitted answers to description
                answers_text = "\n\n📋 Submitted Answers:\n"
                for field, answer in application_result['submitted_answers'].items():
                    answers_text += f"• {field}: {answer}\n"
                
                # Add CV information
                if application_result.get('cv_uploaded'):
                    answers_text += f"\n📄 CV Uploaded: {application_result['cv_uploaded']}\n"
                
                # Add to existing description or create new one
                if "Job Description" in mapped_properties:
                    existing_desc = mapped_properties["Job Description"].get("rich_text", [{}])[0].get("text", {}).get("content", "")
                    mapped_properties["Job Description"]["rich_text"] = [{
                        "type": "text",
                        "text": {"content": f"{existing_desc}{answers_text}"}
                    }]
            
            if not mapped_properties:
                print("❌ No properties could be mapped")
                return None
            
            print(f"📝 Mapping {len(mapped_properties)} properties:")
            for prop_name, prop_value in mapped_properties.items():
                print(f"   - {prop_name}: {type(prop_value).__name__}")
            
            data = {
                "parent": {"database_id": self.notion_database_id},
                "properties": mapped_properties
            }
            
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                entry_id = result.get('id')
                print(f"✅ Notion entry created successfully! ID: {entry_id}")
                return entry_id
            else:
                print(f"❌ Notion entry creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating Notion entry: {e}")
            return None
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get information about the database structure"""
        if not self.database_properties:
            return {}
        
        info = {
            "total_properties": len(self.database_properties),
            "properties": {}
        }
        
        for prop_name, prop_info in self.database_properties.items():
            info["properties"][prop_name] = {
                "type": prop_info.get('type', 'unknown'),
                "raw_name": repr(prop_name)
            }
        
        return info

def test_robust_notion():
    """Test the robust Notion manager"""
    print("Testing Robust Notion Manager")
    print("=" * 40)
    
    manager = RobustNotionManager()
    
    # Show database info
    db_info = manager.get_database_info()
    print(f"Database has {db_info.get('total_properties', 0)} properties:")
    for prop_name, prop_info in db_info.get('properties', {}).items():
        print(f"  - {prop_name} ({prop_info['type']})")
    
    # Test job entry
    test_job = {
        "title": "Junior Full Stack Developer",
        "company": "TechCorp Egypt",
        "location": "Cairo, Egypt",
        "salary": "$3,000 - $4,500",
        "job_type": "Full-time",
        "url": "https://www.linkedin.com/jobs/view/1234567890",
        "description": "Looking for a junior developer with React and Node.js experience"
    }
    
    print(f"\nTesting job entry creation...")
    entry_id = manager.create_job_application_entry(test_job)
    
    if entry_id:
        print(f"✅ Success! Entry created with ID: {entry_id}")
    else:
        print("❌ Failed to create entry")

if __name__ == "__main__":
    test_robust_notion()
