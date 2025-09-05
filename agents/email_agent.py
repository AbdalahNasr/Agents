"""
Email Agent - Personal Automation Agent

This agent reads your email inbox, categorizes emails by type (work/personal/spam),
and sends you summary notifications with categorized email counts and important details.

Features:
- Connects to IMAP email servers (Gmail, Outlook, etc.)
- Categorizes emails using keyword analysis and sender patterns
- Sends summary notifications via console, Telegram, or email
- Logs all actions and errors for monitoring
- Requires approval for sending emails (configurable)

Usage:
    python agents/email_agent.py
    
    # Or import and use programmatically:
    from agents.email_agent import EmailAgent
    agent = EmailAgent()
    agent.process_inbox()
"""

import imaplib
import email
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from email.header import decode_header
from email.utils import parsedate_to_datetime

from config import Config
from utils.logger import AgentLogger
from utils.notifications import NotificationManager
from utils.approval import ApprovalManager

class EmailAgent:
    """Email processing agent for inbox management and categorization."""
    
    def __init__(self):
        """Initialize the Email Agent with logging, notifications, and approval systems."""
        self.logger = AgentLogger("email_agent")
        self.notifications = NotificationManager("email_agent")
        self.approval = ApprovalManager("email_agent")
        
        # Email categorization patterns
        self.categories = {
            'work': {
                'keywords': ['meeting', 'project', 'deadline', 'report', 'client', 'team', 'work'],
                'domains': ['company.com', 'work.org', 'business.net'],
                'senders': ['boss@', 'hr@', 'it@', 'admin@']
            },
            'personal': {
                'keywords': ['family', 'friend', 'birthday', 'party', 'dinner', 'weekend'],
                'domains': ['gmail.com', 'yahoo.com', 'hotmail.com'],
                'senders': ['mom@', 'dad@', 'friend@', 'family@']
            },
            'spam': {
                'keywords': ['urgent', 'limited time', 'free', 'winner', 'lottery', 'viagra'],
                'domains': ['spam.com', 'suspicious.net'],
                'senders': ['noreply@', 'donotreply@', 'spam@']
            }
        }
        
        # Email connection
        self.imap_connection = None
        self.is_connected = False
        
        self.logger.info("Email Agent initialized", categories=list(self.categories.keys()))
    
    def connect_to_email(self) -> bool:
        """
        Connect to the email server using IMAP.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.logger.action("connect_email", target=Config.EMAIL_SERVER, status="started")
            
            # Create IMAP connection
            self.imap_connection = imaplib.IMAP4_SSL(Config.EMAIL_SERVER, Config.EMAIL_PORT)
            
            # Login
            self.imap_connection.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
            
            # Select inbox
            self.imap_connection.select('INBOX')
            
            self.is_connected = True
            self.logger.action("connect_email", target=Config.EMAIL_SERVER, status="completed")
            self.notifications.success(f"Connected to email server: {Config.EMAIL_SERVER}")
            
            return True
            
        except Exception as e:
            self.logger.error("Failed to connect to email server", error=e)
            self.notifications.error(f"Failed to connect to email server: {str(e)}")
            return False
    
    def disconnect_from_email(self):
        """Safely disconnect from the email server."""
        if self.imap_connection and self.is_connected:
            try:
                self.imap_connection.close()
                self.imap_connection.logout()
                self.is_connected = False
                self.logger.info("Disconnected from email server")
            except Exception as e:
                self.logger.error("Error during email disconnect", error=e)
    
    def fetch_recent_emails(self, hours_back: int = 24) -> List[Dict]:
        """
        Fetch recent emails from the inbox.
        
        Args:
            hours_back: Number of hours back to fetch emails from
            
        Returns:
            List[Dict]: List of email data dictionaries
        """
        if not self.is_connected:
            self.logger.error("Not connected to email server")
            return []
        
        try:
            self.logger.action("fetch_emails", target=f"last_{hours_back}_hours", status="started")
            
            # Calculate date range
            date_since = (datetime.now() - timedelta(hours=hours_back)).strftime("%d-%b-%Y")
            
            # Search for emails since the specified time
            search_criteria = f'(SINCE "{date_since}")'
            status, message_numbers = self.imap_connection.search(None, search_criteria)
            
            if status != 'OK':
                self.logger.error("Failed to search emails", status=status)
                return []
            
            emails = []
            message_list = message_numbers[0].split()
            
            # Limit to last 50 emails to avoid overwhelming
            recent_messages = message_list[-50:] if len(message_list) > 50 else message_list
            
            for num in recent_messages:
                try:
                    status, msg_data = self.imap_connection.fetch(num, '(RFC822)')
                    
                    if status == 'OK':
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        email_data = self._parse_email(email_message)
                        emails.append(email_data)
                        
                except Exception as e:
                    self.logger.warning("Failed to parse email", message_num=num, error=str(e))
                    continue
            
            self.logger.action("fetch_emails", target=f"last_{hours_back}_hours", status="completed", count=len(emails))
            return emails
            
        except Exception as e:
            self.logger.error("Failed to fetch emails", error=e)
            return []
    
    def _parse_email(self, email_message) -> Dict:
        """
        Parse email message into structured data.
        
        Args:
            email_message: Email message object
            
        Returns:
            Dict: Parsed email data
        """
        # Extract basic email information
        subject = self._decode_header(email_message.get('Subject', ''))
        sender = self._decode_header(email_message.get('From', ''))
        date = email_message.get('Date', '')
        
        # Parse date
        try:
            parsed_date = parsedate_to_datetime(date) if date else datetime.now()
        except:
            parsed_date = datetime.now()
        
        # Extract email body
        body = self._extract_email_body(email_message)
        
        # Categorize email
        category = self._categorize_email(subject, sender, body)
        
        return {
            'subject': subject,
            'sender': sender,
            'date': parsed_date,
            'body_preview': body[:200] + '...' if len(body) > 200 else body,
            'category': category,
            'is_important': self._is_important_email(subject, sender, body)
        }
    
    def _decode_header(self, header: str) -> str:
        """Decode email header safely."""
        try:
            decoded_parts = decode_header(header)
            return ''.join([part.decode(charset or 'utf-8') if isinstance(part, bytes) else part 
                          for part, charset in decoded_parts])
        except:
            return str(header)
    
    def _extract_email_body(self, email_message) -> str:
        """Extract text body from email message."""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        continue
        else:
            try:
                body = email_message.get_payload(decode=True).decode()
            except:
                body = str(email_message.get_payload())
        
        return body
    
    def _categorize_email(self, subject: str, sender: str, body: str) -> str:
        """
        Categorize email based on content and sender patterns.
        
        Args:
            subject: Email subject
            sender: Email sender
            body: Email body text
            
        Returns:
            str: Category (work, personal, spam, or unknown)
        """
        # Convert to lowercase for matching
        subject_lower = subject.lower()
        sender_lower = sender.lower()
        body_lower = body.lower()
        
        # Check each category
        for category, patterns in self.categories.items():
            score = 0
            
            # Check keywords
            for keyword in patterns['keywords']:
                if keyword in subject_lower or keyword in body_lower:
                    score += 2
                if keyword in sender_lower:
                    score += 1
            
            # Check domains
            for domain in patterns['domains']:
                if domain in sender_lower:
                    score += 3
            
            # Check sender patterns
            for sender_pattern in patterns['senders']:
                if sender_pattern in sender_lower:
                    score += 2
            
            # If score is high enough, categorize
            if score >= 3:
                return category
        
        return 'unknown'
    
    def _is_important_email(self, subject: str, sender: str, body: str) -> bool:
        """
        Determine if an email is important based on content and sender.
        
        Args:
            subject: Email subject
            sender: Email sender
            body: Email body text
            
        Returns:
            bool: True if email is important
        """
        important_indicators = [
            'urgent', 'important', 'asap', 'deadline', 'meeting', 'call',
            'urgent', 'critical', 'priority', 'action required'
        ]
        
        text_to_check = f"{subject} {body}".lower()
        
        for indicator in important_indicators:
            if indicator in text_to_check:
                return True
        
        # Check if sender is from work domain
        if any(domain in sender.lower() for domain in self.categories['work']['domains']):
            return True
        
        return False
    
    def generate_summary(self, emails: List[Dict]) -> Dict:
        """
        Generate summary statistics from processed emails.
        
        Args:
            emails: List of email data dictionaries
            
        Returns:
            Dict: Summary statistics
        """
        if not emails:
            return {'total': 0, 'categories': {}, 'important': 0}
        
        # Count by category
        category_counts = {}
        important_count = 0
        
        for email_data in emails:
            category = email_data['category']
            category_counts[category] = category_counts.get(category, 0) + 1
            
            if email_data['is_important']:
                important_count += 1
        
        # Get recent important emails
        important_emails = [e for e in emails if e['is_important']][:5]
        
        summary = {
            'total': len(emails),
            'categories': category_counts,
            'important': important_count,
            'important_emails': important_emails,
            'timestamp': datetime.now()
        }
        
        return summary
    
    def send_summary_notification(self, summary: Dict):
        """
        Send summary notification with email statistics.
        
        Args:
            summary: Email summary dictionary
        """
        if summary['total'] == 0:
            self.notifications.info("No new emails found in the last 24 hours")
            return
        
        # Format summary message
        message = f"📧 Email Summary - {summary['total']} emails processed"
        
        # Category breakdown
        for category, count in summary['categories'].items():
            emoji = {'work': '💼', 'personal': '👤', 'spam': '🚫', 'unknown': '❓'}
            message += f"\n{emoji.get(category, '📧')} {category.title()}: {count}"
        
        # Important emails
        if summary['important'] > 0:
            message += f"\n\n⚠️ {summary['important']} important emails found:"
            for email in summary['important_emails']:
                message += f"\n• {email['sender']}: {email['subject']}"
        
        # Send notification
        self.notifications.info(message, 
                              total_emails=summary['total'],
                              important_count=summary['important'])
    
    def process_inbox(self, hours_back: int = 24) -> Dict:
        """
        Main method to process inbox and generate summary.
        
        Args:
            hours_back: Number of hours back to process
            
        Returns:
            Dict: Processing results and summary
        """
        start_time = time.time()
        
        try:
            self.logger.action("process_inbox", target="main_process", status="started")
            
            # Connect to email
            if not self.connect_to_email():
                return {'success': False, 'error': 'Failed to connect to email server'}
            
            # Fetch emails
            emails = self.fetch_recent_emails(hours_back)
            
            # Generate summary
            summary = self.generate_summary(emails)
            
            # Send notification
            self.send_summary_notification(summary)
            
            # Log performance
            duration = time.time() - start_time
            self.logger.performance("process_inbox", duration, email_count=len(emails))
            
            return {
                'success': True,
                'emails_processed': len(emails),
                'summary': summary,
                'duration': duration
            }
            
        except Exception as e:
            self.logger.error("Failed to process inbox", error=e)
            self.notifications.error(f"Failed to process inbox: {str(e)}")
            return {'success': False, 'error': str(e)}
        
        finally:
            # Always disconnect
            self.disconnect_from_email()
    
    def run_scheduled(self):
        """Run the agent on a schedule (can be called by external scheduler)."""
        self.logger.info("Running scheduled email processing")
        return self.process_inbox()


def main():
    """Main function to run the Email Agent standalone."""
    print("🚀 Starting Email Agent...")
    
    # Validate configuration
    missing_config = Config.validate()
    if missing_config:
        print(f"❌ Missing configuration: {', '.join(missing_config)}")
        print("Please check your .env file and env_example.txt for required values.")
        return
    
    # Create and run agent
    agent = EmailAgent()
    result = agent.process_inbox()
    
    if result['success']:
        print(f"✅ Email processing completed successfully!")
        print(f"📧 Processed {result['emails_processed']} emails in {result['duration']:.2f}s")
    else:
        print(f"❌ Email processing failed: {result['error']}")


if __name__ == "__main__":
    main()
