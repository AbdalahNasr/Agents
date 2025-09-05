import os
from dotenv import load_dotenv
from typing import List

# Load from config.env instead of .env
load_dotenv('config.env')

class Config:
    EMAIL_SERVER = os.getenv('EMAIL_SERVER', 'imap.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '993'))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    JOB_SITES = os.getenv('JOB_SITES', 'https://linkedin.com/jobs,https://indeed.com').split(',')
    ENABLE_EMAIL_NOTIFICATIONS = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'true').lower() == 'true'
    ENABLE_CONSOLE_NOTIFICATIONS = os.getenv('ENABLE_CONSOLE_NOTIFICATIONS', 'true').lower() == 'true'
    REQUIRE_APPROVAL_FOR_EMAILS = os.getenv('REQUIRE_APPROVAL_FOR_EMAILS', 'true').lower() == 'true'
    REQUIRE_APPROVAL_FOR_JOB_APPLICATIONS = os.getenv('REQUIRE_APPROVAL_FOR_JOB_APPLICATIONS', 'true').lower() == 'true'
    REQUIRE_APPROVAL_FOR_CV_CHANGES = os.getenv('REQUIRE_APPROVAL_FOR_CV_CHANGES', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'agents.log')

    @classmethod
    def validate(cls) -> List[str]:
        missing = []
        if not cls.EMAIL_USERNAME: missing.append('EMAIL_USERNAME')
        if not cls.EMAIL_PASSWORD: missing.append('EMAIL_PASSWORD')
        if not cls.OPENAI_API_KEY: missing.append('OPENAI_API_KEY')
        return missing
