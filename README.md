# 🤖 Automated Job Application System

An intelligent job application automation system that finds jobs, applies automatically, and tracks everything in Notion and local history.

## ✨ Features

- **🤖 Automated Job Applications**: Finds and applies to jobs every 2-4 hours
- **📧 Gmail Integration**: Sends professional applications with CV and portfolio
- **🗄️ Notion Tracking**: Stores all applications in a cloud database
- **📊 Local History**: Complete application records and statistics
- **🔐 Access Control**: User approval required for CV usage
- **📈 Analytics**: Response rates and application statistics
- **☁️ Cloud Ready**: Can run on Google Colab, Replit, or any cloud service

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/job-application-automation.git
cd job-application-automation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy the template
cp config.template.env config.env

# Edit config.env with your credentials
# See setup instructions below
```

### 4. Run the System
```bash
# Test the system
python test_complete_system_with_drive_link.py

# Start automation
python continuous_job_automation.py
```

## ⚙️ Setup Instructions

### Gmail Configuration
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification (enable if needed)
3. App passwords → Mail → Other
4. Enter name: "Job Application System"
5. Copy the 16-character password to `GMAIL_APP_PASSWORD`

### Notion Integration
1. Go to [Notion Developers](https://developers.notion.com/)
2. Create a new integration
3. Copy the Internal Integration Token to `NOTION_TOKEN`
4. Share your database with the integration
5. Copy your database ID to `NOTION_DATABASE_ID`

### LinkedIn Automation (Optional)
1. Use your regular LinkedIn credentials
2. For automation, consider LinkedIn API instead

### Google Drive API (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Drive API
3. Create OAuth 2.0 credentials
4. Download as `drive_credentials.json`

## 📁 Project Structure

```
job-application-automation/
├── agents/                    # Core automation agents
│   ├── ats_cv_generator.py   # CV generation and optimization
│   ├── email_application_manager.py  # Email applications
│   ├── linkedin_application_manager.py  # LinkedIn automation
│   ├── notion_manager.py     # Notion integration
│   ├── job_history_manager.py  # Local history tracking
│   └── cv_manager.py         # CV access control
├── utils/                    # Utility functions
│   ├── logger.py            # Logging system
│   └── notifications.py     # Notification system
├── config.template.env      # Configuration template
├── continuous_job_automation.py  # Main automation script
├── cloud_automation.py      # Cloud-ready version
└── README.md               # This file
```

## 🔧 Usage

### Basic Job Application
```bash
python simple_job_cycle.py
```

### Continuous Automation
```bash
python continuous_job_automation.py
```

### Cloud Deployment
```bash
python cloud_automation.py
```

## 📊 Features in Detail

### Automated Job Applications
- Finds 1-3 jobs every 2-4 hours
- Sends professional applications with CV
- Includes portfolio links and project demos
- Tracks everything in Notion and local history

### Gmail Integration
- Professional email templates
- CV attachment via Google Drive
- Portfolio links included
- Automatic notifications

### Notion Database
- Complete application tracking
- Status updates and follow-ups
- Interview scheduling
- Response tracking

### Local History
- JSON-based storage
- Application statistics
- Response rate tracking
- Export functionality

### Access Control
- User approval for CV usage
- Monthly review reminders
- Complete audit trail
- Professional file naming

## 🛡️ Security

- All sensitive data in `.env` files (gitignored)
- No hardcoded credentials
- Secure API integrations
- Local and cloud storage options

## ☁️ Cloud Deployment

### Google Colab (Free)
1. Upload `cloud_automation.py` to Google Colab
2. Set environment variables
3. Run - works 24/7 for free!

### Replit (Free)
1. Create new Python project
2. Upload `cloud_automation.py`
3. Set environment variables
4. Run - works 24/7 for free!

### Heroku (Free Tier)
1. Create Heroku app
2. Deploy with `cloud_automation.py`
3. Set environment variables
4. Run - works 24/7 for free!

## 📈 Statistics

The system tracks:
- Total applications sent
- Response rates
- Interview scheduling
- Follow-up reminders
- Monthly CV reviews

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use. Always follow job application guidelines and respect company policies. Use responsibly and ethically.

## 🆘 Support

If you encounter any issues:
1. Check the configuration in `config.env`
2. Verify all API credentials
3. Check the logs in `agents.log`
4. Open an issue on GitHub

## 🎯 Roadmap

- [ ] LinkedIn API integration
- [ ] More job sites support
- [ ] Advanced CV optimization
- [ ] Interview preparation tools
- [ ] Salary negotiation tips
- [ ] Company research integration

---

**Happy job hunting! 🚀**