#!/usr/bin/env python3
"""
🔐 OAUTH2 GMAIL NOTIFICATION SYSTEM
Uses Google OAuth2 for secure email notifications
"""
import os
import base64
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime, timedelta

class OAuthGmailNotifier:
    """Gmail notification system using OAuth2"""
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.email = os.getenv('EMAIL_USERNAME')
        self.access_token = None
        self.token_expiry = None
        
        # OAuth2 endpoints
        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.gmail_api = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        
        # Scopes needed for Gmail
        self.scopes = [
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
    
    def get_auth_url(self):
        """Generate OAuth2 authorization URL"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'scope': ' '.join(self.scopes),
            'response_type': 'code',
            'access_type': 'offline'
        }
        
        auth_url = f"{self.auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        return auth_url
    
    def get_access_token(self, auth_code):
        """Exchange authorization code for access token"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
        }
        
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expiry = datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600))
            return True
        return False
    
    def is_token_valid(self):
        """Check if current token is still valid"""
        if not self.access_token or not self.token_expiry:
            return False
        return datetime.now() < self.token_expiry
    
    def send_email(self, to_email, subject, message):
        """Send email using Gmail API"""
        if not self.is_token_valid():
            print("❌ Access token expired or not available")
            return False
        
        try:
            # Create email message
            email_message = MIMEMultipart()
            email_message['to'] = to_email
            email_message['subject'] = subject
            
            # Add message body
            text_part = MIMEText(message, 'plain')
            email_message.attach(text_part)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(email_message.as_bytes()).decode('utf-8')
            
            # Send via Gmail API
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'raw': raw_message
            }
            
            response = requests.post(self.gmail_api, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"✅ Email sent successfully to {to_email}")
                return True
            else:
                print(f"❌ Failed to send email: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def setup_oauth(self):
        """Interactive OAuth2 setup"""
        print("🔐 Setting up Gmail OAuth2 Authentication")
        print("=" * 50)
        
        if not self.client_id or not self.client_secret:
            print("❌ Google OAuth2 credentials not found in config.env")
            return False
        
        print(f"📧 Email: {self.email}")
        print(f"🔑 Client ID: {self.client_id[:20]}...")
        print()
        
        # Generate authorization URL
        auth_url = self.get_auth_url()
        print("🌐 Please visit this URL to authorize the application:")
        print(auth_url)
        print()
        print("📋 After authorization, copy the authorization code and paste it below:")
        
        # Get authorization code from user
        auth_code = input("Enter authorization code: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return False
        
        # Exchange code for token
        print("🔄 Exchanging authorization code for access token...")
        if self.get_access_token(auth_code):
            print("✅ OAuth2 setup completed successfully!")
            print(f"🔑 Access token expires: {self.token_expiry}")
            return True
        else:
            print("❌ Failed to get access token")
            return False

def main():
    """Test the OAuth Gmail system"""
    notifier = OAuthGmailNotifier()
    
    if notifier.setup_oauth():
        print("\n🧪 Testing email notification...")
        test_result = notifier.send_email(
            to_email=notifier.email,
            subject="🧪 Test Email - Personal Automation Hub",
            message="This is a test email from your Personal Automation Hub!\n\nIf you receive this, OAuth2 Gmail is working correctly."
        )
        
        if test_result:
            print("🎉 Gmail OAuth2 system is working perfectly!")
        else:
            print("⚠️ Email test failed, but OAuth2 setup was successful")
    else:
        print("❌ OAuth2 setup failed")

if __name__ == "__main__":
    main()
