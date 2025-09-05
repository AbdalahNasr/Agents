#!/usr/bin/env python3
"""
📧 GMAIL APP PASSWORD NOTIFICATION SYSTEM
Uses Gmail App Password for simple email notifications
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class AppPasswordGmailNotifier:
    """Gmail notification system using App Password"""
    
    def __init__(self):
        # Try to load config.env if it exists
        try:
            from dotenv import load_dotenv
            load_dotenv("config.env")
        except ImportError:
            print("⚠️ python-dotenv not installed, using direct values")
        
        self.smtp_server = os.getenv('EMAIL_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('EMAIL_PORT', '587'))
        self.username = os.getenv('EMAIL_USERNAME', 'body16nasr16bn@gmail.com')
        self.password = os.getenv('EMAIL_PASSWORD', 'icje wcem lobn swrv')
        
        # Fallback to hardcoded values if env vars are None
        if not self.username:
            self.username = 'body16nasr16bn@gmail.com'
        if not self.password:
            self.password = 'icje wcem lobn swrv'
        
    def send_email(self, to_email, subject, message):
        """Send email using Gmail SMTP with App Password"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to Gmail SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            
            # Login with App Password
            server.login(self.username, self.password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            
            print(f"✅ Email sent successfully to {to_email}")
            print(f"   Subject: {subject}")
            print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def test_connection(self):
        """Test Gmail connection and authentication"""
        try:
            print("🔍 Testing Gmail connection...")
            print(f"   Server: {self.smtp_server}:{self.smtp_port}")
            print(f"   Username: {self.username}")
            print(f"   Password: {'*' * len(self.password) if self.password else 'Not set'}")
            print(f"   Password length: {len(self.password) if self.password else 0} characters")
            
            # Test connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            # Test login
            server.login(self.username, self.password)
            server.quit()
            
            print("✅ Gmail connection successful!")
            return True
            
        except Exception as e:
            print(f"❌ Gmail connection failed: {e}")
            return False
    
    def send_test_email(self):
        """Send a test email to verify everything works"""
        if not self.test_connection():
            return False
        
        test_subject = "🧪 Test Email - Personal Automation Hub"
        test_message = f"""
Hello from your Personal Automation Hub!

This is a test email to verify that Gmail App Password authentication is working correctly.

📧 Sent from: {self.username}
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔑 Authentication: Gmail App Password

If you receive this email, your automation system is ready to send notifications!

Best regards,
Your Personal Automation Hub
        """
        
        return self.send_email(self.username, test_subject, test_message)

def main():
    """Test the App Password Gmail system"""
    print("🧪 Testing Gmail App Password System")
    print("=" * 50)
    
    notifier = AppPasswordGmailNotifier()
    
    # Test connection
    if notifier.test_connection():
        print("\n📧 Sending test email...")
        if notifier.send_test_email():
            print("\n🎉 Gmail App Password system is working perfectly!")
            print("Your automation system can now send email notifications!")
        else:
            print("\n⚠️ Test email failed, but connection was successful")
    else:
        print("\n❌ Gmail connection failed")
        print("Please check your App Password and settings")

if __name__ == "__main__":
    main()
