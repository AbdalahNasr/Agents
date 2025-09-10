#!/usr/bin/env python3
"""
Simple credit check using only built-in modules
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error

def check_openai_credits():
    """Check OpenAI API credits using built-in modules"""
    print("🔍 Checking OpenAI API Credits...")
    print("=" * 40)
    
    # Load environment variables manually
    config_file = 'config.env'
    api_key = None
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    api_key = line.split('=', 1)[1].strip().strip('"\'')
                    break
    
    if not api_key:
        print("❌ No OpenAI API key found in config.env")
        print("   Please set OPENAI_API_KEY in your config.env file")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Test API with a simple request
    url = "https://api.openai.com/v1/chat/completions"
    
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
        
        # Create request
        data = json.dumps(test_data).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)
        
        # Make request
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("✅ API is working! You have credits available.")
                result = json.loads(response.read().decode('utf-8'))
                usage = result.get('usage', {})
                if usage:
                    print(f"   Tokens used in this test: {usage.get('total_tokens', 'N/A')}")
                return True
            else:
                print(f"❌ API Error: {response.status}")
                return False
                
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ Invalid API key")
        elif e.code == 429:
            print("⚠️  Rate limit exceeded - but API key is valid")
            return True
        elif e.code == 402:
            print("❌ Payment required - no credits remaining")
        else:
            print(f"❌ API Error: {e.code}")
            print(f"   Response: {e.read().decode('utf-8')}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 OpenAI Credit Checker")
    print("=" * 30)
    
    # Check if config file exists
    if not os.path.exists('config.env'):
        print("❌ No config.env file found")
        print("   Please create a config.env file with your OPENAI_API_KEY")
        exit(1)
    
    # Test API connection
    api_working = check_openai_credits()
    
    print("\n" + "=" * 40)
    if api_working:
        print("✅ Your OpenAI API is working and has credits!")
        print("   You can continue using the automation system.")
    else:
        print("❌ There's an issue with your OpenAI API.")
        print("   Please check your API key and billing status.")
        print("   Visit: https://platform.openai.com/usage")