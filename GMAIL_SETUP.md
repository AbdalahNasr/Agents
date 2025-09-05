# 📧 GMAIL APP PASSWORD SETUP GUIDE

## 🚨 **Why You Need an App Password**

Your regular Gmail password (`01069509757`) won't work with automation systems due to Google's security policies. You need to create an **App Password**.

## 🔧 **Step-by-Step Setup**

### **Step 1: Enable 2-Factor Authentication**
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click **"Security"** in the left menu
3. Under **"Signing in to Google"**, click **"2-Step Verification"**
4. Follow the steps to enable it

### **Step 2: Generate App Password**
1. Go back to **"Security"**
2. Under **"Signing in to Google"**, click **"App passwords"**
3. Select **"Mail"** as the app
4. Select **"Windows Computer"** as the device
5. Click **"Generate"**
6. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### **Step 3: Update Your Config**
1. Open `config.env`
2. Replace `EMAIL_PASSWORD=01069509757` with your new App Password
3. **Remove spaces** from the App Password
4. Set `ENABLE_EMAIL_NOTIFICATIONS=true`

## 📝 **Example Config Update**
```env
EMAIL_PASSWORD=abcdefghijklmnop
ENABLE_EMAIL_NOTIFICATIONS=true
```

## ✅ **After Setup**
1. **Test email notifications**: Run the system
2. **Check your inbox** for automation notifications
3. **Verify everything works** before setting up auto-start

## 🆘 **Common Issues**
- **"Invalid credentials"**: Make sure you copied the App Password exactly
- **"2FA not enabled"**: You must enable 2-Factor Authentication first
- **"App password not working"**: Wait a few minutes after generating

## 🎯 **Security Note**
- **App Passwords are safe** for automation
- **Never share** your App Password
- **You can revoke** App Passwords anytime in Google settings

**Once you have the App Password, we can test the full system! 🚀**
