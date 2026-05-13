"""
FILE_PARSER.PY - Extract Text from PDF and DOCX Files
=====================================================

This file handles:
- Extracting text from PDF files (using PyPDF2)
- Extracting text from DOCX files (using python-docx)
- Simple text parsing to identify sections
"""

import os
from pypdf import PdfReader
from docx import Document
import re

# ============================================================================
# PDF PARSING
# ============================================================================

def extract_text_from_pdf(file_path):
    """
    Extract all text from a PDF file.
    
    Args:
        file_path: Path to PDF file
    
    Returns:
        Full text string or None if error
    """
    try:
        pdf_reader = PdfReader(file_path)
        text = []
        
        # Read each page
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        
        full_text = "\n".join(text)
        print(f"✓ Extracted text from PDF: {len(full_text)} characters")
        return full_text
    
    except Exception as e:
        print(f"✗ Error reading PDF: {str(e)}")
        return None

# ============================================================================
# DOCX PARSING
# ============================================================================

def extract_text_from_docx(file_path):
    """
    Extract all text from a DOCX file.
    
    Args:
        file_path: Path to DOCX file
    
    Returns:
        Full text string or None if error
    """
    try:
        doc = Document(file_path)
        text = []
        
        # Read each paragraph
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)
        
        full_text = "\n".join(text)
        print(f"✓ Extracted text from DOCX: {len(full_text)} characters")
        return full_text
    
    except Exception as e:
        print(f"✗ Error reading DOCX: {str(e)}")
        return None

# ============================================================================
# UNIVERSAL FILE PARSER
# ============================================================================

def extract_text_from_file(file_path):
    """
    Automatically detect file type and extract text.
    
    Supports: .pdf, .docx, .txt
    
    Returns:
        (text, file_type) or (None, None) if error
    """
    
    # Get file extension
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
        return text, 'pdf'
    
    elif file_extension == '.docx':
        text = extract_text_from_docx(file_path)
        return text, 'docx'
    
    elif file_extension == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"✓ Extracted text from TXT: {len(text)} characters")
            return text, 'txt'
        except Exception as e:
            print(f"✗ Error reading TXT: {str(e)}")
            return None, None
    
    else:
        print(f"✗ Unsupported file type: {file_extension}")
        return None, None

# ============================================================================
# BASIC RESUME PARSING
# ============================================================================

def parse_resume_sections(full_text):
    """
    Attempt to identify and extract resume sections.
    
    This is simple pattern matching - not perfect, but works for most resumes.
    
    Returns: Dictionary with identified sections
    """
    
    text = full_text.lower()
    
    # Define section patterns
    sections = {
        'contact': r'(contact|phone|email|linkedin|github)',
        'summary': r'(professional\s+summary|summary|objective|profile)',
        'experience': r'(work\s+experience|employment|experience|professional\s+experience)',
        'skills': r'(skills|technical\s+skills|competencies|core\s+skills)',
        'education': r'(education|degree|university|college|school)',
        'projects': r'(projects|portfolio|personal\s+projects)',
        'certifications': r'(certifications|licenses|certifications?\s+and\s+awards)'
    }
    
    found_sections = {}
    
    for section_name, pattern in sections.items():
        if re.search(pattern, text):
            found_sections[section_name] = True
        else:
            found_sections[section_name] = False
    
    return found_sections

# ============================================================================
# RESUME DATA EXTRACTION
# ============================================================================

def extract_basic_resume_data(full_text):
    """
    Try to extract key resume data points.
    
    This uses simple heuristics and will work for well-formatted resumes.
    
    Returns: Dictionary with extracted data
    """
    
    # Find email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, full_text)
    email = emails[0] if emails else "Not found"
    
    # Find phone number (simple pattern)
    phone_pattern = r'(\+?1?\s*)?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})'
    phones = re.findall(phone_pattern, full_text)
    phone = f"{phones[0][1]}-{phones[0][2]}-{phones[0][3]}" if phones else "Not found"
    
    # Find name (usually first line or after contact info)
    lines = full_text.split('\n')
    name = lines[0].strip() if lines else "Not found"
    
    # Try to find a job title (keywords like "Developer", "Engineer", etc.)
    title_keywords = ['developer', 'engineer', 'designer', 'manager', 'analyst',
                      'specialist', 'lead', 'senior', 'junior', 'consultant']
    role = "Not specified"
    
    for i, line in enumerate(lines[:10]):
        line_lower = line.lower()
        for keyword in title_keywords:
            if keyword in line_lower:
                role = line.strip()
                break
    
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'role': role
    }

# ============================================================================
# ALLOWED FILE TYPES
# ============================================================================

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

def is_allowed_file(filename):
    """
    Check if file type is allowed.
    """
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # You can test with actual files:
    # text, ftype = extract_text_from_file('sample_resume.pdf')
    # if text:
    #     print(parse_resume_sections(text))
    #     print(extract_basic_resume_data(text))
    
    print("File parser module loaded. Use extract_text_from_file() to parse resumes.")
