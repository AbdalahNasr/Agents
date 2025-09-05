#!/usr/bin/env python3
"""
Check what status options are available in the Notion database
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

def check_status_options():
    """Check available status options"""
    print("Checking Status Options")
    print("=" * 30)
    
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
            
            # Find Status property
            status_prop = None
            for prop_name, prop_info in properties.items():
                if 'status' in prop_name.lower():
                    status_prop = prop_info
                    print(f"Found Status property: '{prop_name}'")
                    break
            
            if status_prop:
                status_options = status_prop.get('status', {}).get('options', [])
                print(f"\nAvailable Status Options:")
                for option in status_options:
                    name = option.get('name', 'Unknown')
                    color = option.get('color', 'default')
                    print(f"  - {name} ({color})")
                
                # Use the first available option
                if status_options:
                    first_option = status_options[0]['name']
                    print(f"\n✅ Will use: '{first_option}'")
                    return first_option
                else:
                    print("❌ No status options available")
                    return None
            else:
                print("❌ No Status property found")
                return None
                
        else:
            print(f"❌ Failed to get database info: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    check_status_options()
