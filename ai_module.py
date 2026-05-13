"""
AI_MODULE.PY - ATS Score & Keyword Matching (Simple AI without APIs)
=====================================================================

This file implements simple keyword matching to:
- Calculate ATS compatibility score
- Find missing keywords from job description
- Provide feedback for resume optimization

No external AI APIs needed - just pure Python text analysis!
"""

import re
from collections import Counter

# ============================================================================
# KEYWORD EXTRACTION
# ============================================================================

def extract_keywords(text):
    """
    Extract important keywords from text.
    
    Simple algorithm:
    1. Convert to lowercase
    2. Remove special characters and numbers
    3. Split into words
    4. Remove common meaningless words (stopwords)
    5. Keep technical terms
    """
    
    # Common words that don't matter (stopwords)
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'at', 'to', 'for',
        'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
        'could', 'may', 'might', 'can', 'am', 'it', 'its', 'on', 'by', 'from',
        'as', 'if', 'who', 'which', 'that', 'this', 'these', 'those',
        'than', 'very', 'more', 'most', 'other', 'some', 'any', 'all',
        'no', 'not', 'your', 'my', 'our', 'their', 'he', 'she', 'they',
        'i', 'you', 'we', 'them', 'him', 'her', 'me'
    }
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters, keep only letters, numbers, and spaces
    text = re.sub(r'[^a-z0-9\s\+\#\-]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Keep only words that:
    # - Are longer than 2 characters
    # - Are not in stopwords
    # - Are not purely numeric
    keywords = [
        word for word in words 
        if len(word) > 2 and word not in stopwords and not word.isdigit()
    ]
    
    return keywords

# ============================================================================
# SKILL MATCHING
# ============================================================================

# Common technical skills and certifications to recognize
TECHNICAL_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'csharp', 'c#', 'c++', 'typescript',
    'php', 'ruby', 'go', 'kotlin', 'swift', 'sql', 'html', 'css',
    
    # Web Frameworks
    'django', 'flask', 'fastapi', 'spring', 'react', 'angular', 'vue',
    'nodejs', 'express', 'laravel', 'rails', 'asp.net',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle',
    'mssql', 'dynamodb', 'elasticsearch', 'cassandra',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
    'gitlab', 'github', 'terraform', 'ansible',
    
    # Data & AI
    'tensorflow', 'pytorch', 'sklearn', 'pandas', 'numpy', 'matplotlib',
    'apache', 'spark', 'hadoop', 'tableau', 'powerbi', 'ml', 'ai',
    
    # Other Tools
    'jira', 'slack', 'figma', 'wordpress', 'linux', 'windows', 'macos',
    'api', 'rest', 'graphql', 'json', 'xml', 'agile', 'scrum',
    'responsive', 'ux', 'ui', 'seo', 'ecommerce'
}

def find_skills(text):
    """
    Find recognized technical skills in text.
    """
    keywords = extract_keywords(text)
    found_skills = set()
    
    for keyword in keywords:
        if keyword in TECHNICAL_SKILLS:
            found_skills.add(keyword)
    
    return list(found_skills)

# ============================================================================
# ATS SCORE CALCULATION
# ============================================================================

def calculate_ats_score(resume_text, job_description):
    """
    Calculate ATS compatibility score (0-100).
    
    Algorithm:
    1. Extract keywords from both resume and job description
    2. Find how many match
    3. Calculate percentage
    4. Apply bonus for exact role match
    
    Returns: score (0-100)
    """
    
    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Create word frequency maps
    resume_set = set(resume_keywords)
    job_set = set(job_keywords)
    
    # Find matching keywords
    matches = resume_set.intersection(job_set)
    
    # If empty, return 0
    if len(job_set) == 0:
        return 0
    
    # Calculate base score (percentage of job keywords found in resume)
    base_score = (len(matches) / len(job_set)) * 100
    
    # Cap at 100
    score = min(base_score, 100)
    
    return round(score, 2)

# ============================================================================
# MISSING KEYWORDS FINDER
# ============================================================================

def find_missing_keywords(resume_text, job_description):
    """
    Find important keywords from job description that are missing in resume.
    
    Returns: List of missing keywords (prioritized)
    """
    
    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Create sets for comparison
    resume_set = set(resume_keywords)
    job_set = set(job_keywords)
    
    # Missing = in job description but not in resume
    missing = job_set - resume_set
    
    # Find technical skills in missing keywords (these are important)
    missing_list = list(missing)
    
    # Sort: technical skills first, then by alphabetical
    technical_missing = []
    other_missing = []
    
    for keyword in missing_list:
        if keyword in TECHNICAL_SKILLS:
            technical_missing.append(keyword)
        else:
            other_missing.append(keyword)
    
    # Combine: technical skills first (more important for ATS)
    technical_missing.sort()
    other_missing.sort()
    result = technical_missing + other_missing
    
    # Return top 15 most important missing keywords
    return result[:15]

# ============================================================================
# ATS FEEDBACK GENERATOR
# ============================================================================

def generate_ats_feedback(resume_text, job_description, ats_score):
    """
    Generate helpful feedback for improving ATS score.
    
    Returns: Feedback message
    """
    
    missing_keywords = find_missing_keywords(resume_text, job_description)
    
    feedback = []
    
    # Score-based feedback
    if ats_score < 30:
        feedback.append("⚠️  LOW MATCH: Your resume is significantly different from the job description.")
        feedback.append("   Try adding more relevant keywords and technical skills.")
    elif ats_score < 60:
        feedback.append("📊 MODERATE MATCH: There's good overlap, but you can improve further.")
        feedback.append("   Consider adding the missing keywords below.")
    elif ats_score < 80:
        feedback.append("✓ GOOD MATCH: Your resume matches well with the job requirements.")
        feedback.append("   A few more tweaks could push it higher.")
    else:
        feedback.append("✓✓ EXCELLENT MATCH: Your resume is highly compatible with this position!")
        feedback.append("   You're well-positioned for this application.")
    
    # Missing keywords feedback
    if missing_keywords:
        feedback.append("\n🔑 TOP MISSING KEYWORDS:")
        # Show top 8 keywords
        for i, keyword in enumerate(missing_keywords[:8], 1):
            feedback.append(f"   {i}. {keyword}")
        feedback.append("\n   💡 TIP: Try incorporating these keywords naturally in your resume.")
    
    # Additional tips
    feedback.append("\n💡 GENERAL TIPS:")
    feedback.append("   • Use the exact job title if it applies")
    feedback.append("   • Include specific technical skills mentioned in the job description")
    feedback.append("   • Use bullet points - they're ATS-friendly")
    feedback.append("   • Avoid tables, images, and unusual formatting")
    feedback.append("   • Use standard fonts (Arial, Calibri, Times New Roman)")
    
    return "\n".join(feedback)

# ============================================================================
# SECTION ANALYZER
# ============================================================================

def analyze_resume_structure(resume_text):
    """
    Analyze if resume has important sections.
    
    Returns: Dictionary with section analysis
    """
    
    text_lower = resume_text.lower()
    
    sections = {
        'contact': bool(re.search(r'(email|phone|linkedin|contact)', text_lower)),
        'summary': bool(re.search(r'(professional\s+summary|summary|objective)', text_lower)),
        'experience': bool(re.search(r'(experience|employment|work\s+history)', text_lower)),
        'skills': bool(re.search(r'(skills|technical\s+skills|competencies)', text_lower)),
        'education': bool(re.search(r'(education|degree|university|college)', text_lower)),
        'projects': bool(re.search(r'(projects|portfolio)', text_lower))
    }
    
    return sections

# ============================================================================
# MAIN ATS CHECK FUNCTION
# ============================================================================

def perform_ats_check(resume_text, job_description):
    """
    Complete ATS analysis.
    
    Returns: Dictionary with all results
    """
    
    # Calculate score
    score = calculate_ats_score(resume_text, job_description)
    
    # Find missing keywords
    missing = find_missing_keywords(resume_text, job_description)
    
    # Generate feedback
    feedback = generate_ats_feedback(resume_text, job_description, score)
    
    # Analyze structure
    structure = analyze_resume_structure(resume_text)
    
    return {
        'score': score,
        'missing_keywords': missing,
        'feedback': feedback,
        'structure': structure,
        'skills_found': find_skills(resume_text)
    }

# ============================================================================
# KEYWORD GENERATOR
# ============================================================================

def generate_keywords_from_description(job_description):
    """
    Extract and suggest important keywords from job description.
    
    Returns: Organized list of keywords by category
    """
    
    keywords = extract_keywords(job_description)
    technical_skills = []
    soft_skills = []
    other_keywords = []
    
    soft_skill_keywords = {
        'communication', 'leadership', 'teamwork', 'problem', 'solving',
        'analytical', 'creative', 'organized', 'management', 'planning',
        'critical', 'thinking', 'initiative', 'collaboration', 'adaptable'
    }
    
    for keyword in keywords:
        if keyword in TECHNICAL_SKILLS:
            technical_skills.append(keyword)
        elif keyword in soft_skill_keywords:
            soft_skills.append(keyword)
        else:
            other_keywords.append(keyword)
    
    return {
        'technical': list(set(technical_skills))[:10],
        'soft_skills': list(set(soft_skills))[:8],
        'other': list(set(other_keywords))[:10]
    }

# ============================================================================
# For testing
# ============================================================================

if __name__ == "__main__":
    sample_resume = """
    John Doe
    Python Developer
    john@email.com
    
    Experienced Python developer with 3 years experience in Django and Flask.
    Strong in database design with MySQL and PostgreSQL.
    Familiar with Docker and Git version control.
    """
    
    sample_job = """
    Seeking Python Developer with Django experience.
    Must know Python, Django, PostgreSQL, Docker, Git.
    Experience with REST APIs and JSON required.
    AWS experience is a plus.
    """
    
    result = perform_ats_check(sample_resume, sample_job)
    print(f"ATS Score: {result['score']}")
    print(f"Missing Keywords: {result['missing_keywords']}")
    print(result['feedback'])
