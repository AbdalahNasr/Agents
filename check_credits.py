#!/usr/bin/env python3
"""
Check remaining credits/usage for OpenAI API
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

def check_openai_credits():
    """Check OpenAI API usage and remaining credits"""
    print("🔍 Checking OpenAI API Credits...")
    print("=" * 40)
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        print("   Please set OPENAI_API_KEY in your config.env file")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Test API with a simple request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple test request
    test_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 5
    }
    
    try:
        print("🔄 Testing API connection...")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API is working! You have credits available.")
            result = response.json()
            usage = result.get('usage', {})
            if usage:
                print(f"   Tokens used in this test: {usage.get('total_tokens', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("❌ Invalid API key")
            return False
        elif response.status_code == 429:
            print("⚠️  Rate limit exceeded - but API key is valid")
            return True
        elif response.status_code == 402:
            print("❌ Payment required - no credits remaining")
            return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_usage_endpoint():
    """Try to get usage information from OpenAI API"""
    print("\n📊 Checking usage information...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Try to get usage for current month
        response = requests.get(
            "https://api.openai.com/v1/usage",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            usage_data = response.json()
            print("✅ Usage data retrieved:")
            print(f"   Total usage: {usage_data}")
            return True
        else:
            print(f"⚠️  Could not retrieve usage data: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not check usage: {e}")
        return False

if __name__ == "__main__":
    print("🔍 OpenAI Credit Checker")
    print("=" * 30)
    
    # Check if API key exists
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ No OPENAI_API_KEY found in environment")
        print("   Please check your config.env file")
        exit(1)
    
    # Test API connection
    api_working = check_openai_credits()
    
    # Try to get usage info
    check_usage_endpoint()
    
    print("\n" + "=" * 40)
    if api_working:
        print("✅ Your OpenAI API is working and has credits!")
        print("   You can continue using the automation system.")
    else:
        print("❌ There's an issue with your OpenAI API.")
        print("   Please check your API key and billing status.")