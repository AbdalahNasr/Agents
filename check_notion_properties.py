#!/usr/bin/env python3
"""
Check the exact property names in the Notion database
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

def check_database_properties():
    """Check the exact property names in the database"""
    print("Checking Notion Database Properties")
    print("=" * 40)
    
    notion_token = os.getenv('NOTION_TOKEN')
    notion_database_id = os.getenv('NOTION_DATABASE_ID')
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{notion_database_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            db_info = response.json()
            properties = db_info.get('properties', {})
            
            print("Exact Property Names:")
            print("-" * 30)
            for prop_name, prop_info in properties.items():
                prop_type = prop_info.get('type', 'unknown')
                print(f"'{prop_name}' -> {prop_type}")
                
                # Show the exact string representation
                print(f"  Raw: {repr(prop_name)}")
                print()
            
            return properties
        else:
            print(f"❌ Failed to get database info: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    check_database_properties()
