# Assessment Email Server

Backend server for sending detailed PDF assessment reports via email.

## Setup Instructions

### 1. Install Dependencies

```bash
cd server
npm install
```

### 2. Configure Email Settings

Edit the `.env` file with your email credentials:

#### For Gmail:
1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security → 2-Step Verification → App passwords
   - Select "Mail" and your device
   - Copy the generated 16-character password
4. Update `.env`:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   EMAIL_FROM=your-email@gmail.com
   ADMIN_EMAIL=admin-email@gmail.com
   ```

#### For Other Email Providers:

**Outlook/Office365:**
```
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
```

**Yahoo:**
```
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
```

**Custom SMTP:**
```
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587
```

### 3. Start the Server

```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

The server will run on `http://localhost:3001`

## Features

The PDF report includes:
- ✅ Student information (name, email, date)
- ✅ Overall score with visual emphasis
- ✅ Section-by-section breakdown
- ✅ Every question with all options
- ✅ Student's answer vs correct answer
- ✅ Code snippets for programming questions
- ✅ Personalized recommendations
- ✅ Professional formatting

## API Endpoints

### POST `/api/submit-assessment`
Submits assessment and sends PDF reports via email.

**Request Body:**
```json
{
  "studentName": "John Doe",
  "studentEmail": "student@example.com",
  "answers": {...},
  "results": {...},
  "recommendations": [...],
  "sections": [...]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Assessment submitted successfully..."
}
```

### GET `/api/health`
Health check endpoint.

## Email Recipients

1. **Student** - Receives their detailed PDF report
2. **Admin** - Receives a copy with summary

## Troubleshooting

**Email not sending:**
- Check your email credentials in `.env`
- Ensure App Password is correct (not your regular password)
- Check if less secure app access is enabled (for some providers)
- Verify SMTP host and port settings

**Server not starting:**
- Make sure port 3001 is not in use
- Check that all dependencies are installed
- Verify `.env` file exists

**CORS errors:**
- Server is configured to accept requests from any origin
- If issues persist, check browser console for details

