import express from 'express';
import cors from 'cors';
import nodemailer from 'nodemailer';
import PDFDocument from 'pdfkit';
import dotenv from 'dotenv';
import { Readable } from 'stream';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// Create email transporter
const transporter = nodemailer.createTransport({
  host: process.env.EMAIL_HOST,
  port: process.env.EMAIL_PORT,
  secure: false,
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASSWORD,
  },
});

// Generate PDF report
function generatePDF(data) {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument({ margin: 50 });
    const chunks = [];

    doc.on('data', (chunk) => chunks.push(chunk));
    doc.on('end', () => resolve(Buffer.concat(chunks)));
    doc.on('error', reject);

    // Header
    doc.fontSize(24).fillColor('#4F46E5').text('AI Program Assessment Report', { align: 'center' });
    doc.moveDown();
    
    // Student Information
    doc.fontSize(12).fillColor('#000000');
    doc.text(`Student Name: ${data.studentName}`, { continued: false });
    doc.text(`Email: ${data.studentEmail}`);
    doc.text(`Date: ${new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })}`);
    doc.moveDown(2);

    // Overall Score
    const overallPercentage = Math.round((data.results.overall.correct / data.results.overall.total) * 100);
    doc.fontSize(16).fillColor('#4F46E5').text('Overall Score', { underline: true });
    doc.moveDown(0.5);
    doc.fontSize(36).fillColor(overallPercentage >= 70 ? '#059669' : '#DC2626')
       .text(`${overallPercentage}%`, { align: 'center' });
    doc.fontSize(12).fillColor('#000000')
       .text(`${data.results.overall.correct} out of ${data.results.overall.total} questions correct`, { align: 'center' });
    doc.moveDown(2);

    // Section Scores
    doc.fontSize(16).fillColor('#4F46E5').text('Section Scores', { underline: true });
    doc.moveDown(1);
    
    data.sections.forEach(section => {
      const sectionResult = data.results[section.id];
      const percentage = Math.round((sectionResult.correct / sectionResult.total) * 100);
      
      doc.fontSize(14).fillColor('#000000').text(section.title, { continued: true });
      doc.fontSize(12).fillColor(percentage >= 70 ? '#059669' : '#DC2626')
         .text(` - ${percentage}% (${sectionResult.correct}/${sectionResult.total})`, { align: 'left' });
      doc.moveDown(0.5);
    });
    doc.moveDown(2);

    // Detailed Answers
    doc.addPage();
    doc.fontSize(18).fillColor('#4F46E5').text('Detailed Assessment Results', { underline: true });
    doc.moveDown(1);

    let questionNumber = 1;
    data.sections.forEach((section, sectionIdx) => {
      doc.fontSize(16).fillColor('#4F46E5').text(`${section.title}`, { underline: true });
      doc.moveDown(0.5);

      section.questions.forEach((question, qIdx) => {
        const studentAnswer = data.answers[question.id];
        const isCorrect = studentAnswer === question.correct;

        // Check if we need a new page
        if (doc.y > 650) {
          doc.addPage();
        }

        // Question number and text
        doc.fontSize(12).fillColor('#000000')
           .text(`Question ${questionNumber}: ${question.question}`, { continued: false });
        doc.moveDown(0.5);

        // Code snippet if exists
        if (question.code) {
          doc.fontSize(9).fillColor('#1F2937').font('Courier')
             .text(question.code, { 
               indent: 20,
               width: doc.page.width - 120
             });
          doc.font('Helvetica');
          doc.moveDown(0.5);
        }

        // Options
        question.options.forEach((option, optIdx) => {
          let prefix = '';
          let color = '#000000';
          
          if (optIdx === question.correct) {
            prefix = '✓ ';
            color = '#059669';
          }
          if (optIdx === studentAnswer && !isCorrect) {
            prefix = '✗ ';
            color = '#DC2626';
          }
          
          doc.fontSize(10).fillColor(color)
             .text(`${prefix}${String.fromCharCode(65 + optIdx)}. ${option}`, { indent: 20 });
        });

        doc.moveDown(0.3);
        
        // Result
        if (studentAnswer === undefined) {
          doc.fontSize(10).fillColor('#DC2626')
             .text('Status: Not answered', { indent: 20 });
        } else if (isCorrect) {
          doc.fontSize(10).fillColor('#059669')
             .text('Status: Correct ✓', { indent: 20 });
        } else {
          doc.fontSize(10).fillColor('#DC2626')
             .text(`Status: Incorrect ✗`, { indent: 20 });
          doc.fillColor('#059669')
             .text(`Correct answer: ${String.fromCharCode(65 + question.correct)}. ${question.options[question.correct]}`, { indent: 20 });
        }

        doc.moveDown(1.5);
        questionNumber++;
      });

      doc.moveDown(1);
    });

    // Recommendations
    doc.addPage();
    doc.fontSize(18).fillColor('#4F46E5').text('Recommendations', { underline: true });
    doc.moveDown(1);

    data.recommendations.forEach(rec => {
      doc.fontSize(14).fillColor('#000000').text(rec.area, { underline: true });
      doc.fontSize(11).fillColor('#374151').text(rec.recommendation, { indent: 20 });
      doc.moveDown(1);
    });

    doc.end();
  });
}

// API endpoint to submit assessment
app.post('/api/submit-assessment', async (req, res) => {
  try {
    const assessmentData = req.body;
    
    // Generate PDF
    const pdfBuffer = await generatePDF(assessmentData);
    
    // Prepare email to student
    const studentMailOptions = {
      from: process.env.EMAIL_FROM,
      to: assessmentData.studentEmail,
      subject: 'Your AI Program Assessment Results',
      html: `
        <h2>Hi ${assessmentData.studentName},</h2>
        <p>Thank you for completing the AI Program Assessment!</p>
        <p>Your overall score: <strong>${assessmentData.results.overall.percentage}%</strong></p>
        <p>Please find your detailed assessment report attached as a PDF.</p>
        <br>
        <p>Best regards,<br>AI Program Team</p>
      `,
      attachments: [
        {
          filename: `assessment-report-${assessmentData.studentName.replace(/\s+/g, '-')}.pdf`,
          content: pdfBuffer,
          contentType: 'application/pdf'
        }
      ]
    };

    // Prepare email to admin
    const adminMailOptions = {
      from: process.env.EMAIL_FROM,
      to: process.env.ADMIN_EMAIL,
      subject: `Assessment Submission: ${assessmentData.studentName}`,
      html: `
        <h2>New Assessment Submission</h2>
        <p><strong>Student:</strong> ${assessmentData.studentName}</p>
        <p><strong>Email:</strong> ${assessmentData.studentEmail}</p>
        <p><strong>Overall Score:</strong> ${assessmentData.results.overall.percentage}%</p>
        <p><strong>Date:</strong> ${new Date().toLocaleString()}</p>
        <br>
        <h3>Section Scores:</h3>
        <ul>
          ${assessmentData.sections.map(section => {
            const result = assessmentData.results[section.id];
            return `<li><strong>${section.title}:</strong> ${result.percentage}% (${result.correct}/${result.total})</li>`;
          }).join('')}
        </ul>
        <p>Full report attached.</p>
      `,
      attachments: [
        {
          filename: `assessment-report-${assessmentData.studentName.replace(/\s+/g, '-')}.pdf`,
          content: pdfBuffer,
          contentType: 'application/pdf'
        }
      ]
    };

    // Send emails
    await transporter.sendMail(studentMailOptions);
    await transporter.sendMail(adminMailOptions);

    res.json({ 
      success: true, 
      message: 'Assessment submitted successfully. Check your email for the detailed report.' 
    });
  } catch (error) {
    console.error('Error submitting assessment:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to submit assessment. Please try again.' 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Assessment server running on port ${PORT}`);
});

