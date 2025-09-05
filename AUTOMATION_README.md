# 🚀 PERSONAL AUTOMATION HUB - Your Productivity Command Center

## 🎯 **What This System Does**

Your Personal Automation Hub automatically manages your entire productivity workflow:

- **🔗 LinkedIn Management**: Automatically checks for opportunities, optimizes your profile, and searches for jobs
- **📄 CV Generation**: Creates and updates multiple CV versions (ATS, Professional, Concise) automatically
- **💼 Job Applications**: Generates application drafts and cover letters with AI assistance
- **📧 Email Monitoring**: Processes emails and sends smart notifications
- **🔄 Continuous Automation**: Runs all tasks on schedule without manual intervention

## 🚀 **Quick Start**

### **Option 1: Double-Click Launch (Windows)**
1. Double-click `START_AUTOMATION.bat`
2. The system will automatically start and guide you through options

### **Option 2: Command Line Launch**
```bash
python launch_automation.py
```

### **Option 3: Direct Automation Hub**
```bash
python automation_hub.py
```

## 🎮 **Available Options**

When you launch the system, you'll see these choices:

1. **🚀 Start Full Automation** - Runs continuously, monitoring everything automatically
2. **🔄 Run One Complete Workflow** - Executes all tasks once and reports results
3. **🔗 Test LinkedIn Only** - Tests your LinkedIn connection and profile
4. **📄 Generate CV Only** - Creates new CV versions
5. **💼 Job Application Workflow Only** - Generates job application drafts
6. **📧 Test Email Notifications Only** - Tests your email system
7. **❌ Exit** - Closes the system

## ⚙️ **Automation Schedule**

The system automatically runs tasks at these intervals:

- **LinkedIn Checks**: Every 30 minutes
- **CV Updates**: Every 60 minutes
- **Job Searches**: Every 45 minutes
- **Email Monitoring**: Every 15 minutes

## 🔧 **Configuration**

Your system is configured in `config.env`:

```env
# LinkedIn API
LINKEDIN_ACCESS_TOKEN=your_token_here

# OpenAI API
OPENAI_API_KEY=your_openai_key_here

# Email Settings
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Notification Settings
ENABLE_EMAIL_NOTIFICATIONS=true
ENABLE_CONSOLE_NOTIFICATIONS=true
```

## 📊 **What Happens Automatically**

### **LinkedIn Management**
- ✅ Retrieves your profile information
- ✅ Searches for relevant job opportunities
- ✅ Optimizes your headline for ATS systems
- ✅ Sends notifications about new opportunities

### **CV Generation**
- ✅ Reads your original CV PDF
- ✅ Creates 3 optimized versions:
  - **ATS Version**: Optimized for Applicant Tracking Systems
  - **Professional Version**: Enhanced for senior positions
  - **Concise Version**: Streamlined for quick review
- ✅ Generates multiple formats: PDF, DOCX, JSON, Markdown, Text
- ✅ Organizes files in timestamped folders

### **Job Applications**
- ✅ Creates application drafts with AI-generated cover letters
- ✅ Matches CV versions to job requirements
- ✅ Sends approval notifications before submission
- ✅ Tracks application status

### **Email System**
- ✅ Monitors your inbox automatically
- ✅ Categorizes emails (work/personal/spam)
- ✅ Sends summary notifications
- ✅ Handles approval workflows

## 🚨 **Important Notes**

### **Gmail Setup**
- You need a **Gmail App Password** (not your regular password)
- Enable 2-factor authentication first
- Generate an app password in Google Account settings

### **LinkedIn API**
- Your access token is already configured
- The system will automatically test the connection
- If issues occur, check token expiration

### **File Organization**
- All generated files are organized in timestamped folders
- CV versions are separated by type (ATS, Professional, Concise)
- No files clutter your root directory

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Gmail Authentication**
   - Use App Password, not regular password
   - Enable 2FA in Google Account

3. **LinkedIn API Issues**
   - Check if access token is expired
   - Verify API permissions

4. **File Permission Errors**
   - Run as administrator if needed
   - Check folder write permissions

### **Logs and Debugging**
- Check `agents.log` for detailed error information
- Console output shows real-time status
- Email notifications include error details

## 🎯 **Pro Tips**

1. **Start with Option 3** (Test LinkedIn) to verify your setup
2. **Use Option 2** (One Complete Workflow) for testing
3. **Option 1** (Full Automation) for production use
4. **Monitor email notifications** for system status
5. **Check logs** if something isn't working

## 🚀 **Advanced Features**

### **Custom Scheduling**
Edit `automation_hub.py` to change intervals:
```python
self.workflow_config = {
    "linkedin_check_interval": 30,  # minutes
    "cv_update_interval": 60,       # minutes  
    "job_search_interval": 45,      # minutes
    "email_check_interval": 15      # minutes
}
```

### **AI Customization**
The system uses OpenAI GPT-3.5-turbo for:
- Cover letter generation
- Profile optimization
- Content enhancement

### **Notification Channels**
- Console output (real-time)
- Email notifications (Gmail)
- Log files (detailed tracking)

## 🎉 **Success Indicators**

You'll know the system is working when you see:
- ✅ Green checkmarks in console
- 📧 Email notifications about completed tasks
- 📁 New CV files in organized folders
- 🔗 LinkedIn profile updates
- 💼 Job application drafts created

## 🆘 **Need Help?**

If you encounter issues:
1. Check the console output for error messages
2. Review the `agents.log` file
3. Verify your configuration in `config.env`
4. Ensure all dependencies are installed

## 🚀 **Ready to Launch?**

Your Personal Automation Hub is ready! Just run:

```bash
python launch_automation.py
```

Or double-click `START_AUTOMATION.bat` on Windows.

**Sit back and let your personal AI agents handle your productivity! 🎯**
