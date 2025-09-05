import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from config import Config
from utils.logger import AgentLogger

class NotificationManager:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = AgentLogger(f"notifications.{agent_name}")
        self._validate_config()

    def _validate_config(self):
        """Validate notification configuration."""
        if self.ENABLE_EMAIL_NOTIFICATIONS and not Config.EMAIL_USERNAME:
            self.logger.warning("Email notifications enabled but EMAIL_USERNAME not configured")
        if self.ENABLE_EMAIL_NOTIFICATIONS and not Config.EMAIL_PASSWORD:
            self.logger.warning("Email notifications enabled but EMAIL_PASSWORD not configured")

    @property
    def ENABLE_EMAIL_NOTIFICATIONS(self):
        return Config.ENABLE_EMAIL_NOTIFICATIONS

    @property
    def ENABLE_CONSOLE_NOTIFICATIONS(self):
        return Config.ENABLE_CONSOLE_NOTIFICATIONS

    def notify(self, message: str, level: str = "INFO", **kwargs):
        """Send notification through all enabled channels."""
        if self.ENABLE_CONSOLE_NOTIFICATIONS:
            self._console_notify(message, level, **kwargs)
        
        if self.ENABLE_EMAIL_NOTIFICATIONS:
            self._email_notify(message, level, **kwargs)

    def _console_notify(self, message: str, level: str, **kwargs):
        """Send console notification."""
        timestamp = kwargs.get('timestamp', '')
        agent = kwargs.get('agent', self.agent_name)
        
        if level == "ERROR":
            self.logger.error(f"[{agent}] {message}")
        elif level == "WARNING":
            self.logger.warning(f"[{agent}] {message}")
        elif level == "SUCCESS":
            self.logger.info(f"[{agent}] SUCCESS: {message}")
        else:
            self.logger.info(f"[{agent}] INFO: {message}")

    def _email_notify(self, message: str, level: str, **kwargs):
        """Send email notification."""
        try:
            subject = f"[{self.agent_name.upper()}] {level} - {kwargs.get('subject', 'Agent Notification')}"
            
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_USERNAME
            msg['To'] = Config.EMAIL_USERNAME  # Send to self
            msg['Subject'] = subject
            
            body = f"""
Agent: {self.agent_name}
Level: {level}
Time: {kwargs.get('timestamp', '')}
Message: {message}

Additional Info: {kwargs.get('details', 'None')}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(Config.EMAIL_USERNAME, Config.EMAIL_USERNAME, text)
            server.quit()
            
            self.logger.info(f"Email notification sent successfully", agent=self.agent_name)
            
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {str(e)}", error=e, agent=self.agent_name)

    def success(self, message: str, **kwargs):
        """Send success notification."""
        self.notify(message, "SUCCESS", **kwargs)

    def warning(self, message: str, **kwargs):
        """Send warning notification."""
        self.notify(message, "WARNING", **kwargs)

    def error(self, message: str, **kwargs):
        """Send error notification."""
        self.notify(message, "ERROR", **kwargs)

    def info(self, message: str, **kwargs):
        """Send info notification."""
        self.notify(message, "INFO", **kwargs)
