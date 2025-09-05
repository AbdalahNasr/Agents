# 🚀 Railway Deployment Guide for Job Application Automation

## Overview
Deploy your job application automation system to Railway for 24/7 operation with a free tier that includes $5 monthly credit.

## Prerequisites
- GitHub repository (already set up ✅)
- Railway account (free)
- Environment variables ready

## Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your GitHub account

## Step 2: Deploy from GitHub
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `Agents` repository
4. Railway will automatically detect Python

## Step 3: Configure Environment Variables
In Railway dashboard, go to Variables tab and add:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_key

# Gmail
GMAIL_USER=body16nasr16bn@gmail.com
GMAIL_APP_PASSWORD=icje wcem lobn swrv

# Notion
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_database_id

# Google Drive
CV_PRIMARY_URL=https://drive.google.com/file/d/1B19SyQeY_Lqjbapj1k7l66Vr9tCckcH7/view?usp=sharing
CV_DOWNLOAD_URL=https://drive.google.com/uc?export=download&id=1B19SyQeY_Lqjbapj1k7l66Vr9tCckcH7
CV_PREVIEW_URL=https://drive.google.com/file/d/1B19SyQeY_Lqjbapj1k7l66Vr9tCckcH7/preview
CV_FILE_ID=1B19SyQeY_Lqjbapj1k7l66Vr9tCckcH7

# LinkedIn
LINKEDIN_USERNAME=Abdalah Nasr
LINKEDIN_PASSWORD=01006113546
```

## Step 4: Create Railway Configuration
Create `railway.json` in your project root:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python cloud_automation.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Step 5: Create Procfile
Create `Procfile` in your project root:

```
worker: python cloud_automation.py
```

## Step 6: Deploy
1. Railway will automatically build and deploy
2. Check logs in Railway dashboard
3. Your automation will run 24/7

## Monitoring
- View logs in Railway dashboard
- Check email notifications
- Monitor Notion database updates

## Cost
- **Free Tier:** $5 credit monthly
- **Your App:** ~$1-2/month (very lightweight)
- **Result:** Completely free for your use case

## Benefits
✅ Runs 24/7 without your computer
✅ Automatic deployments from GitHub
✅ Built-in monitoring and logs
✅ HTTPS endpoints
✅ Environment variable management
✅ No server maintenance needed

## Troubleshooting
- Check Railway logs for errors
- Verify environment variables
- Test locally first with `cloud_automation.py`

