"""
PDF_GENERATOR.PY - Generate Professional Resume PDFs
===================================================

This file uses ReportLab to create clean, professional PDF resumes.
It's simple: takes resume data → creates PDF → returns file path.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.5 * inch
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)

# Colors
COLOR_DARK = '#1a1a1a'      # Dark gray for headers
COLOR_ACCENT = '#0066cc'    # Blue for highlights

# ============================================================================
# PDF GENERATION
# ============================================================================

def generate_resume_pdf(name, role, summary, experience, skills, education, output_path, 
                        phone='', email='', dob='', linkedin='', address='', github_link='',
                        internships='', projects='', certifications='', strengths='', 
                        weaknesses='', declaration=''):
    """
    Generate a professional resume PDF with all sections.
    
    Args:
        name: Candidate name
        role: Job role/title
        summary: Professional summary
        experience: Experience text (can be multiple lines)
        skills: Skills text (usually comma-separated)
        education: Education text
        output_path: Where to save the PDF
        phone: Phone number
        email: Email address
        dob: Date of birth
        linkedin: LinkedIn profile
        address: Physical address
        github_link: GitHub profile
        internships: Internship experience
        projects: Projects
        certifications: Certifications
        strengths: Key strengths
        weaknesses: Weaknesses/areas for improvement
        declaration: Declaration statement
    
    Returns:
        output_path if successful, None if error
    """
    
    try:
        # Create PDF document with multiple pages if needed
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=MARGIN,
            leftMargin=MARGIN,
            topMargin=MARGIN,
            bottomMargin=MARGIN
        )
        
        # Container for PDF content
        elements = []
        
        # Define custom styles
        styles = getSampleStyleSheet()
        
        # Header style (name)
        name_style = ParagraphStyle(
            'CustomName',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=COLOR_DARK,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Role style
        role_style = ParagraphStyle(
            'CustomRole',
            parent=styles['Normal'],
            fontSize=12,
            textColor=COLOR_ACCENT,
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName='Helvetica'
        )
        
        # Contact info style
        contact_style = ParagraphStyle(
            'ContactInfo',
            parent=styles['Normal'],
            fontSize=9,
            textColor='#333333',
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName='Helvetica'
        )
        
        # Section header style
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=COLOR_DARK,
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            borderPadding=4
        )
        
        # Content style
        content_style = ParagraphStyle(
            'ContentStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            leading=12
        )
        
        # ================================================================
        # HEADER SECTION
        # ================================================================
        
        if name:
            elements.append(Paragraph(name.upper(), name_style))
        
        if role:
            elements.append(Paragraph(role, role_style))
        
        # Contact information
        contact_info = []
        if email:
            contact_info.append(email)
        if phone:
            contact_info.append(phone)
        if address:
            contact_info.append(address)
        if linkedin or github_link:
            links = []
            if linkedin:
                links.append(linkedin)
            if github_link:
                links.append(github_link)
            contact_info.append(" | ".join(links))
        
        if contact_info:
            elements.append(Paragraph(" | ".join(contact_info), contact_style))
        
        elements.append(Spacer(1, 0.15 * inch))
        
        # ================================================================
        # PROFESSIONAL SUMMARY
        # ================================================================
        
        if summary and summary.strip():
            elements.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
            elements.append(Paragraph(summary, content_style))
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # WORK EXPERIENCE
        # ================================================================
        
        if experience and experience.strip():
            elements.append(Paragraph("WORK EXPERIENCE", section_style))
            
            # Split by double newline to separate entries
            exp_entries = experience.split('\n\n')
            for entry in exp_entries:
                if entry.strip():
                    # Add entry with formatting
                    for line in entry.strip().split('\n'):
                        if line.strip():
                            if line.startswith('-'):
                                elements.append(Paragraph(line, content_style))
                            else:
                                # Job title/company
                                elements.append(Paragraph(f"<b>{line}</b>", content_style))
            
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # INTERNSHIPS
        # ================================================================
        
        if internships and internships.strip():
            elements.append(Paragraph("INTERNSHIPS", section_style))
            
            for line in internships.strip().split('\n'):
                if line.strip():
                    if line.startswith('-'):
                        elements.append(Paragraph(line, content_style))
                    else:
                        elements.append(Paragraph(f"<b>{line}</b>", content_style))
            
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # EDUCATION
        # ================================================================
        
        if education and education.strip():
            elements.append(Paragraph("EDUCATION", section_style))
            
            for line in education.strip().split('\n'):
                if line.strip():
                    elements.append(Paragraph(line, content_style))
            
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # PROJECTS
        # ================================================================
        
        if projects and projects.strip():
            elements.append(Paragraph("PROJECTS", section_style))
            
            for line in projects.strip().split('\n'):
                if line.strip():
                    if line.startswith('-'):
                        elements.append(Paragraph(line, content_style))
                    else:
                        elements.append(Paragraph(f"<b>{line}</b>", content_style))
            
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # SKILLS
        # ================================================================
        
        if skills and skills.strip():
            elements.append(Paragraph("SKILLS", section_style))
            
            for line in skills.strip().split('\n'):
                if line.strip():
                    elements.append(Paragraph(f"• {line}", content_style))
            
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # CERTIFICATIONS
        # ================================================================
        
        if certifications and certifications.strip():
            elements.append(Paragraph("CERTIFICATIONS & AWARDS", section_style))
            
            for line in certifications.strip().split('\n'):
                if line.strip():
                    elements.append(Paragraph(f"• {line}", content_style))
            
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # KEY STRENGTHS
        # ================================================================
        
        if strengths and strengths.strip():
            elements.append(Paragraph("KEY STRENGTHS", section_style))
            
            for line in strengths.strip().split('\n'):
                if line.strip():
                    elements.append(Paragraph(line, content_style))
            
            elements.append(Spacer(1, 0.08 * inch))
        
        # ================================================================
        # DECLARATION
        # ================================================================
        
        if declaration and declaration.strip():
            elements.append(Spacer(1, 0.1 * inch))
            small_style = ParagraphStyle(
                'SmallText',
                parent=styles['Normal'],
                fontSize=8,
                textColor='#555555',
                alignment=TA_JUSTIFY,
                spaceAfter=4,
                leading=10
            )
            elements.append(Paragraph("DECLARATION", section_style))
            elements.append(Paragraph(declaration, small_style))
        
        # ================================================================
        # FOOTER
        # ================================================================
        
        # Add footer with generation date
        elements.append(Spacer(1, 0.2 * inch))
        footer_text = f"<font size='8' color='gray'>Generated on {datetime.datetime.now().strftime('%B %d, %Y')}</font>"
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor='#999999'
        )
        elements.append(Paragraph(footer_text, footer_style))
        
        # ================================================================
        # BUILD AND SAVE PDF
        # ================================================================
        
        doc.build(elements)
        
        print(f"✓ PDF created successfully: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"✗ Error creating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# SIMPLE ALTERNATIVE - Basic PDF with reportlab canvas (even simpler)
# ============================================================================

def generate_simple_resume_pdf(name, role, summary, experience, skills, education, output_path):
    """
    Generate a very simple resume PDF using basic canvas.
    More control, less automatic formatting.
    
    Good for: Minimalist, quick PDFs
    """
    
    try:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Set up margins
        margin = 0.5 * inch
        y = height - margin
        
        # Font setup
        c.setFont("Helvetica-Bold", 20)
        c.drawString(margin, y, name.upper() if name else "")
        
        y -= 0.25 * inch
        c.setFont("Helvetica", 11)
        c.setFillColor('#0066cc')
        c.drawString(margin, y, role if role else "")
        
        y -= 0.3 * inch
        c.setFillColor('#000000')  # Back to black
        
        # Professional Summary
        if summary and summary.strip():
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin, y, "PROFESSIONAL SUMMARY")
            y -= 0.15 * inch
            c.setFont("Helvetica", 10)
            
            # Wrap text
            for line in summary.split('\n'):
                if line.strip():
                    c.drawString(margin + 0.2 * inch, y, line[:80])
                    y -= 0.15 * inch
            
            y -= 0.1 * inch
        
        # Skills
        if skills and skills.strip():
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin, y, "SKILLS")
            y -= 0.15 * inch
            c.setFont("Helvetica", 10)
            c.drawString(margin + 0.2 * inch, y, skills[:100])
            y -= 0.2 * inch
        
        # Experience
        if experience and experience.strip():
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin, y, "EXPERIENCE")
            y -= 0.15 * inch
            c.setFont("Helvetica", 10)
            
            for line in experience.split('\n'):
                if line.strip():
                    c.drawString(margin + 0.2 * inch, y, f"• {line[:70]}")
                    y -= 0.15 * inch
            
            y -= 0.1 * inch
        
        # Education
        if education and education.strip():
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin, y, "EDUCATION")
            y -= 0.15 * inch
            c.setFont("Helvetica", 10)
            c.drawString(margin + 0.2 * inch, y, education[:80])
        
        # Save
        c.save()
        print(f"✓ Simple PDF created: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

# ============================================================================
# FILE MANAGEMENT
# ============================================================================

def get_pdf_filename(user_id, resume_id=None):
    """
    Generate a unique PDF filename.
    
    Example: 'resumes/user_123_resume_456.pdf'
    """
    if resume_id:
        return f"resumes/user_{user_id}_resume_{resume_id}.pdf"
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"resumes/user_{user_id}_resume_{timestamp}.pdf"

# ============================================================================
# Testing
# ============================================================================

if __name__ == "__main__":
    # Test data
    test_name = "John Doe"
    test_role = "Senior Python Developer"
    test_summary = "Experienced full-stack Python developer with 5+ years building web applications using Django and Flask. Strong proficiency in database design, API development, and cloud deployments."
    test_experience = "Led development team at Tech Company | Built scalable REST APIs using Django | Implemented CI/CD pipelines | Deployed to AWS"
    test_skills = "Python, Django, Flask, PostgreSQL, Docker, AWS, Git, JavaScript, HTML/CSS"
    test_education = "B.S. Computer Science from University of Example (2019)"
    
    # Generate PDF
    generate_resume_pdf(
        test_name,
        test_role,
        test_summary,
        test_experience,
        test_skills,
        test_education,
        "test_resume.pdf"
    )
