# AI Program Assessment Tool

A React-based assessment tool for evaluating student readiness in AI fundamentals with automated PDF report generation and email delivery.

## Features

- ✅ Programming fundamentals assessment (Python/R)
- ✅ Calculus basics evaluation
- ✅ Probability & statistics questions
- ✅ Interactive UI with instant feedback
- ✅ Personalized recommendations based on results
- ✅ **Detailed PDF reports with all questions and answers**
- ✅ **Automated email delivery to students and admins**

## Quick Start

### Frontend Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to http://localhost:5173

### Backend Setup (Required for Email/PDF)

1. **Navigate to server directory:**
   ```bash
   cd server
   ```

2. **Install server dependencies:**
   ```bash
   npm install
   ```

3. **Configure email settings:**
   Edit `server/.env` with your email credentials (see server/README.md for details)

4. **Start the backend server:**
   ```bash
   npm start
   ```
   Server will run on http://localhost:3001

## Running the Full Application

You need **both** servers running:

**Terminal 1 (Frontend):**
```bash
npm run dev
```

**Terminal 2 (Backend):**
```bash
cd server
npm start
```

## PDF Report Contents

The detailed PDF report includes:
- Student information and timestamp
- Overall score with visual emphasis
- Section-by-section breakdown
- **Every question with all answer options**
- **Student's selected answer highlighted**
- **Correct answer clearly marked**
- Code snippets for programming questions
- Personalized study recommendations

Both the student and admin receive the full PDF report via email.

## Email Configuration

See `server/README.md` for detailed instructions on:
- Setting up Gmail with App Passwords
- Configuring other email providers (Outlook, Yahoo, etc.)
- Troubleshooting email delivery issues

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` folder.

## Technology Stack

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Lucide React (icons)

**Backend:**
- Node.js + Express
- PDFKit (PDF generation)
- Nodemailer (email delivery)
- CORS enabled

