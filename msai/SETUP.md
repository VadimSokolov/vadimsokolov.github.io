# Quick Setup Guide

## Step 1: Install Frontend Dependencies

```bash
cd /Users/vsokolov/www/msai
npm install
```

## Step 2: Install Backend Dependencies

```bash
cd /Users/vsokolov/www/msai/server
npm install
```

## Step 3: Configure Email (IMPORTANT!)

Edit the file `server/.env` and add your email credentials:

### For Gmail (Recommended):

1. **Enable 2-Factor Authentication** on your Google account
2. **Create App Password**:
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Scroll down and click "App passwords"
   - Select "Mail" and generate password
   - Copy the 16-character password

3. **Update server/.env**:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=youremail@gmail.com
EMAIL_PASSWORD=your-16-char-password-here
EMAIL_FROM=youremail@gmail.com
ADMIN_EMAIL=admin@example.com
PORT=3001
```

## Step 4: Run the Application

Open **TWO** terminal windows:

### Terminal 1 - Frontend:
```bash
cd /Users/vsokolov/www/msai
npm run dev
```

### Terminal 2 - Backend:
```bash
cd /Users/vsokolov/www/msai/server
npm start
```

## Step 5: Test It!

1. Open browser to http://localhost:5173
2. Complete the assessment
3. Click "Email Detailed Report (PDF)"
4. Check your email for the PDF report!

## What Gets Emailed?

**To Student:**
- Full PDF report with all questions, their answers, and correct answers
- Personalized recommendations

**To Admin:**
- Same PDF report
- Summary of student's performance

## Troubleshooting

**"Error connecting to server":**
- Make sure backend server is running on port 3001
- Check Terminal 2 for any errors

**"Failed to send report":**
- Verify email credentials in `server/.env`
- Check that you're using an App Password (not regular password)
- Look at server logs in Terminal 2

**Frontend not loading:**
- Make sure you ran `npm install` in the main msai directory
- Check Terminal 1 for errors

