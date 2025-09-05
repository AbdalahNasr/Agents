# Personal Automation Agents - Setup Guide

## 🚀 Quick Start

Your automation agents are ready! Here's what you need to do to get them fully working:

## 1. Gmail App Password Setup

**IMPORTANT**: You need to create an App Password for Gmail, not use your regular password.

### Steps:
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click "Security" in the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Scroll down and click "App passwords"
5. Select "Mail" and "Windows Computer"
6. Click "Generate"
7. Copy the 16-character password (it looks like: `abcd efgh ijkl mnop`)
8. Update your `config.env` file:

```bash
EMAIL_PASSWORD=your_16_character_app_password_here
```

## 2. Test Your Agents

### Test Basic Functionality:
```bash
python simple_test.py
```

### Test CV Enhancement (AI-powered):
```bash
python cli.py cv enhance --role "Software Engineer" --text "Python developer with 5 years experience"
```

### Test Email Processing:
```bash
python cli.py email process --hours 24
```

### Test Job Search:
```bash
python cli.py job search --max-apps 5
```

## 3. What Each Agent Does

### 📧 Email Agent
- Connects to your Gmail inbox
- Categorizes emails (work/personal/spam)
- Sends you daily summaries
- **Requires**: Gmail App Password

### 💼 Job Application Agent
- Scrapes job postings from LinkedIn, Indeed, Glassdoor
- Matches jobs to your profile using AI
- Creates application drafts
- **Requires**: Your approval before submitting

### 📄 CV Enhancement Agent
- Takes your CV text
- Enhances it using OpenAI AI
- Creates multiple improved versions
- **Requires**: OpenAI API key (already configured!)

## 4. Configuration Files

- `config.env` - Your credentials and settings
- `agents.log` - Log file with all agent activities
- `.env` - Backup config (you can delete this)

## 5. Troubleshooting

### Email Notifications Not Working?
- Check your Gmail App Password
- Make sure 2FA is enabled on your Google account
- Verify the password in `config.env`

### AI Enhancement Not Working?
- Your OpenAI API key is already configured
- The CV agent will use fallback methods if AI fails

### Agents Not Starting?
- Run `python simple_test.py` to check basic functionality
- Check the `agents.log` file for error details

## 6. Next Steps

1. **Set up Gmail App Password** (see step 1)
2. **Test email processing**: `python cli.py email process`
3. **Enhance your CV**: `python cli.py cv enhance --role "Your Target Role" --text "Your CV text"`
4. **Search for jobs**: `python cli.py job search`

## 7. Security Notes

- ✅ Your credentials are stored in `config.env` (not in code)
- ✅ Job applications require your approval before submission
- ✅ Email sending requires your approval (configurable)
- ✅ All actions are logged for transparency

## 8. Support

If you encounter issues:
1. Check the `agents.log` file for detailed error messages
2. Run `python simple_test.py` to verify basic setup
3. Make sure all dependencies are installed: `pip install -r requirements.txt`

---

**Your agents are ready to save you time and improve your productivity! 🎉**
