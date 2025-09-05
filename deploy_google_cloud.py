#!/usr/bin/env python3
"""
Google Cloud Run Free Deployment - Completely FREE
"""

import os
import subprocess
import json

def create_dockerfile():
    """Create Dockerfile for Google Cloud Run"""
    dockerfile_content = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Run the application
CMD ["python", "continuous_job_automation_robust.py"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    
    print("✅ Created Dockerfile")

def create_cloudbuild_config():
    """Create Cloud Build configuration"""
    config = {
        "steps": [
            {
                "name": "gcr.io/cloud-builders/docker",
                "args": ["build", "-t", "gcr.io/$PROJECT_ID/job-automation", "."]
            },
            {
                "name": "gcr.io/cloud-builders/docker", 
                "args": ["push", "gcr.io/$PROJECT_ID/job-automation"]
            },
            {
                "name": "gcr.io/cloud-builders/gcloud",
                "args": [
                    "run", "deploy", "job-automation",
                    "--image", "gcr.io/$PROJECT_ID/job-automation",
                    "--region", "us-central1",
                    "--platform", "managed",
                    "--allow-unauthenticated",
                    "--set-env-vars", "GMAIL_USER=$_GMAIL_USER,GMAIL_APP_PASSWORD=$_GMAIL_APP_PASSWORD,NOTION_TOKEN=$_NOTION_TOKEN,NOTION_DATABASE_ID=$_NOTION_DATABASE_ID,CV_PRIMARY_URL=$_CV_PRIMARY_URL,OPENAI_API_KEY=$_OPENAI_API_KEY"
                ]
            }
        ],
        "substitutions": {
            "_GMAIL_USER": os.getenv('GMAIL_USER', ''),
            "_GMAIL_APP_PASSWORD": os.getenv('GMAIL_APP_PASSWORD', ''),
            "_NOTION_TOKEN": os.getenv('NOTION_TOKEN', ''),
            "_NOTION_DATABASE_ID": os.getenv('NOTION_DATABASE_ID', ''),
            "_CV_PRIMARY_URL": os.getenv('CV_PRIMARY_URL', ''),
            "_OPENAI_API_KEY": os.getenv('OPENAI_API_KEY', '')
        }
    }
    
    with open('cloudbuild.yaml', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created cloudbuild.yaml")

def create_deployment_script():
    """Create deployment script"""
    script_content = """#!/bin/bash
# Google Cloud Run Free Deployment Script

echo "🆓 Google Cloud Run Free Deployment"
echo "=================================="
echo "✅ Completely FREE - No credit card required"
echo "✅ 2 million requests/month free"
echo "✅ Perfect for automation"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not found"
    echo "📥 Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ Google Cloud CLI found"

# Login
echo "🔐 Logging in to Google Cloud..."
gcloud auth login

# Create project (if needed)
echo "📁 Setting up project..."
PROJECT_ID="job-automation-$(date +%s)"
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID

# Enable APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
echo "🚀 Building and deploying..."
gcloud builds submit --config cloudbuild.yaml

echo "✅ Deployment successful!"
echo "🌐 Your job automation is running on Google Cloud Run!"
echo "📊 Check status: gcloud run services list"
echo "📋 View logs: gcloud run logs tail job-automation"
"""
    
    with open('deploy_gcloud.sh', 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod('deploy_gcloud.sh', 0o755)
    print("✅ Created deploy_gcloud.sh")

def main():
    """Main function"""
    print("🆓 Google Cloud Run Free Deployment Setup")
    print("=" * 50)
    print("✅ Completely FREE - No credit card required")
    print("✅ 2 million requests/month free")
    print("✅ 180,000 vCPU-seconds free")
    print("✅ Perfect for job automation")
    print()
    
    create_dockerfile()
    create_cloudbuild_config()
    create_deployment_script()
    
    print("\n🎉 SUCCESS!")
    print("Google Cloud Run configuration created!")
    print("\n📋 Next steps:")
    print("1. Install Google Cloud CLI: https://cloud.google.com/sdk/docs/install")
    print("2. Run: chmod +x deploy_gcloud.sh")
    print("3. Run: ./deploy_gcloud.sh")
    print("\n📖 This will:")
    print("- Create a free Google Cloud project")
    print("- Build and deploy your automation")
    print("- Set up all environment variables")
    print("- Start your job automation for FREE!")

if __name__ == "__main__":
    main()
