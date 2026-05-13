"""
AI_ASSISTANT.PY - Interactive Chat Assistant & Task Performer
==============================================================

This module provides an intelligent assistant that:
1. Answers questions about the Resume AI Builder
2. PERFORMS ACTUAL TASKS like:
   - Write professional summaries
   - Generate declarations
   - Create skill descriptions
   - Optimize resume text
   - Suggest keywords
   - And more!

The assistant uses pattern matching and task execution to provide real value.
Can be extended to use external AI APIs (OpenAI, etc.) for more advanced responses.
"""

import re
from difflib import SequenceMatcher
import random

# ============================================================================
# KNOWLEDGE BASE - Information about the app and resume tips
# ============================================================================

KNOWLEDGE_BASE = {
    "features": {
        "keywords": ["features", "what can i do", "what does", "capabilities", "how do i use", "what features"],
        "response": """🎯 **Resume AI Builder Features:**

1. **Resume Builder** - Create professional resumes from scratch using pre-built templates
   - Choose from multiple templates (Software Engineer, Data Scientist, Designer, etc.)
   - Easy-to-use form to fill in your details
   
2. **Resume Upload** - Upload your existing resume (PDF, DOCX, TXT)
   - Instantly parse and analyze your resume
   - Extract key information automatically
   
3. **ATS Score Checker** - Get an ATS (Applicant Tracking System) compatibility score
   - Compare your resume against job descriptions
   - See how well optimized your resume is (0-100%)
   - Identify missing skills/keywords
   
4. **Keyword Generator** - Find important keywords from job postings
   - Extract technical skills and requirements
   - Suggests keywords to add to your resume
   
5. **PDF Download** - Export your resume as a professional PDF
   - Print-ready format
   - Professional formatting
   
6. **Resume History** - Save and manage multiple resumes
   - Store different versions
   - Track ATS scores over time

What would you like to know more about?"""
    },
    
    "ats_score": {
        "keywords": ["ats", "score", "ats score", "compatibility", "how does ats work", "what is ats"],
        "response": """📊 **Understanding ATS Score:**

**What is ATS?**
ATS stands for "Applicant Tracking System" - software used by recruiters to scan resumes.

**How does our ATS Score work?**
Our tool compares your resume against a job description and calculates a compatibility score:

1. **Keyword Matching** - Checks if your resume contains important keywords from the job description
2. **Skill Recognition** - Identifies technical skills and certifications
3. **Experience Level** - Analyzes years of experience mentioned
4. **Format Analysis** - Checks if your resume is ATS-friendly

**Score Interpretation:**
- **80-100%** ✅ Excellent - Your resume matches the job well
- **60-79%** 👍 Good - Decent match, could be improved
- **40-59%** ⚠️ Fair - Missing important keywords or skills
- **Below 40%** ❌ Poor - Significant gaps between your resume and job requirements

**How to Improve Your Score:**
1. Add missing keywords from the job description
2. Include relevant technical skills
3. Quantify achievements (percentages, numbers)
4. Use simple, clear language (no jargon ATS systems can't parse)

Try uploading your resume and a job description to see your score!"""
    },
    
    "keywords": {
        "keywords": ["keywords", "keyword generator", "what keywords should i add", "missing keywords", "skills"],
        "response": """🔑 **Keyword Generator Guide:**

**Why Keywords Matter?**
Recruiters use ATS systems to search for specific keywords. If your resume doesn't contain these terms, it won't get matched to relevant jobs.

**How the Keyword Generator Works:**
1. Upload or paste a job description
2. Our system extracts important keywords (technical skills, tools, frameworks)
3. We highlight which ones are missing from your resume
4. Suggestions to improve your ATS score

**Types of Keywords to Include:**
- **Programming Languages**: Python, Java, JavaScript, C++, etc.
- **Frameworks**: Django, React, Spring, Laravel, etc.
- **Databases**: SQL, MongoDB, PostgreSQL, etc.
- **Cloud Services**: AWS, Azure, GCP
- **Tools & Platforms**: Docker, Kubernetes, Git, Jira
- **Soft Skills**: Leadership, Communication, Problem-solving
- **Certifications**: AWS, Azure, Google Cloud, etc.

**Pro Tips:**
✅ Use exact terms from job descriptions
✅ Include both full names and abbreviations (Python vs Py)
✅ List skills relevant to the role
✅ Don't stuff keywords unrelated to your role
❌ Avoid keyword stuffing - keep it natural

Try the Keyword Generator to see what skills you should add!"""
    },
    
    "upload": {
        "keywords": ["upload", "upload resume", "how to upload", "file upload", "supported formats", "pdf docx"],
        "response": """⬆️ **Resume Upload Guide:**

**Supported File Formats:**
✅ PDF (.pdf)
✅ Word Documents (.docx)
✅ Text Files (.txt)

**Maximum File Size:** 10 MB

**How to Upload:**
1. Go to the **Upload** page from the dashboard
2. Click "Choose File" and select your resume
3. Click "Upload"
4. Our system will automatically extract information from your resume

**What Happens After Upload:**
- Your resume is parsed and stored securely
- Basic information is extracted (name, email, phone, etc.)
- You can view it in your dashboard
- Use it for ATS scoring or keyword analysis

**Tips for Best Results:**
✅ Use standard formatting (avoid unusual fonts/colors)
✅ Include clear section headers (Experience, Education, Skills)
✅ Use consistent date formats
✅ Avoid images and graphics (ATS systems can't parse them)
❌ Don't use complex tables or text boxes
❌ Avoid scanning PDFs from printed resumes (use digital PDFs)

**Having Issues?**
Make sure your resume file:
- Is under 10 MB
- Is a valid PDF, DOCX, or TXT file
- Has readable text (not an image)"""
    },
    
    "builder": {
        "keywords": ["builder", "build resume", "how to build", "create resume", "resume builder", "templates"],
        "response": """🛠️ **Resume Builder Guide:**

**How to Use the Resume Builder:**

1. **Select a Template** 
   - Choose from multiple professional templates
   - Each template includes pre-filled example content
   - Customize to your style

2. **Fill in Your Information**
   - Personal Details (name, email, phone, LinkedIn)
   - Professional Summary
   - Work Experience
   - Internships
   - Projects
   - Education
   - Skills
   - Certifications
   - And more!

3. **Available Templates:**
   - Software Engineer
   - Data Scientist
   - Product Manager
   - Designer
   - Marketing Professional
   - Sales Executive

4. **Build Your Resume**
   - Click on each section to edit
   - Add multiple entries (e.g., multiple jobs)
   - Use bullet points for clarity
   - Include quantifiable achievements

5. **Download as PDF**
   - Once done, download your resume
   - Professional formatting included
   - Ready to send to employers

**Pro Tips for Better Resumes:**
✅ Use action verbs (Led, Designed, Implemented, etc.)
✅ Include numbers and metrics (30%, $50K, 500+ users)
✅ Keep it to 1-2 pages
✅ Use clear section headers
✅ Save multiple versions for different job types
❌ Avoid personal pronouns (I, me, we)
❌ Don't include salary information
❌ Avoid personal interests unless relevant"""
    },
    
    "login": {
        "keywords": ["login", "sign in", "password", "account", "forgot password", "can't login"],
        "response": """🔐 **Login & Accounts:**

**How to Log In:**
1. Go to the home page
2. Enter your email and password
3. Click "Login"
4. You'll be taken to your dashboard

**How to Sign Up:**
1. Click "Sign Up" on the login page
2. Enter a valid email address
3. Choose a strong password
4. Click "Register"
5. You can now log in with these credentials

**Password Requirements:**
✅ At least 8 characters
✅ Mix of uppercase and lowercase
✅ Include numbers
✅ Include special characters

**Forgot Password?**
Currently, we don't have a password reset feature. Please contact support for assistance.

**Security Tips:**
✅ Use a unique, strong password
✅ Don't share your password
✅ Log out on public computers
✅ Keep your email updated
❌ Don't use simple passwords (123456, password)
❌ Don't reuse passwords from other sites"""
    },
    
    "tips": {
        "keywords": ["tips", "advice", "how to", "best practices", "recommendations", "resume tips"],
        "response": """💡 **Resume Writing Tips:**

**Content Tips:**
✅ **Use Action Verbs** - Led, Designed, Implemented, Developed, Optimized
✅ **Include Numbers** - "Increased sales by 35%" not "improved sales"
✅ **Be Specific** - "Built REST API in Python" not "worked with coding"
✅ **Quantify Impact** - "Reduced load time by 40%" not "improved performance"
✅ **Highlight Achievements** - Focus on results, not just duties
✅ **Tailor Your Resume** - Customize for each job application
✅ **Use Keywords** - Include terms from job descriptions

**Formatting Tips:**
✅ Keep it to 1-2 pages
✅ Use consistent formatting
✅ Clear section headers
✅ Use bullet points
✅ 10-12pt font, readable sans-serif fonts
✅ 0.5-1" margins
✅ Leave white space for readability

**What to Include:**
1. Contact Information (email, phone, LinkedIn, GitHub)
2. Professional Summary (2-3 lines)
3. Work Experience (most recent first)
4. Education
5. Skills & Technical Competencies
6. Certifications (if relevant)
7. Optional: Projects, Publications, Volunteer Work

**What to Avoid:**
❌ Typos and grammatical errors
❌ Vague language or buzzwords without context
❌ Personal info (age, photo, marital status - unless required)
❌ Company logos or images (breaks ATS)
❌ Unusual fonts or colors
❌ More than 2 pages
❌ Unexplained gaps in employment
❌ Too technical (remember, recruiters read first)

**Interview Preparation:**
Once you land an interview, be ready to discuss items on your resume with specific examples!"""
    },
    
    "account_settings": {
        "keywords": ["account", "settings", "profile", "delete account", "change email", "preferences"],
        "response": """⚙️ **Account Settings:**

**Currently Available:**
- View your profile
- See your saved resumes
- View ATS score history
- Log out

**Planned Features:**
- Change password
- Update email address
- Delete account
- Theme preferences
- Email notifications

**For Now:**
📧 To change your email or delete your account, please contact our support team.

**Your Data:**
Your resume data is stored securely in our database. You can download your resumes as PDF at any time."""
    },
    
    "support": {
        "keywords": ["help", "support", "contact", "issue", "problem", "error", "bug", "feedback"],
        "response": """🆘 **Support & Feedback:**

**Having Issues?**
We're here to help! Common issues:

1. **Resume Upload Failed**
   - Check file size (under 10 MB)
   - Ensure it's PDF, DOCX, or TXT
   - Try saving as a different format

2. **ATS Score Seems Wrong**
   - Make sure job description is provided
   - Check for formatting issues in resume
   - Try uploading a cleaner version

3. **Missing Features**
   - Some features are still in development
   - Check the roadmap for coming soon items

**Contact & Feedback:**
📧 Email: support@resumeaibuilder.com
💬 Twitter: @ResumeAIBuilder
🐛 Report a Bug: Click "Report Issue" in your dashboard

**Response Time:**
We typically respond within 24-48 hours.

**Feature Requests:**
We'd love to hear what features you'd like! Please share your ideas with us."""
    },
    
    "faq": {
        "keywords": ["faq", "frequently asked", "questions", "common", "q&a"],
        "response": """❓ **Frequently Asked Questions:**

**Q: Is my resume data safe?**
A: Yes! Your data is stored securely and encrypted. We never share your information.

**Q: Can I download my resumes?**
A: Yes! Go to your dashboard and click "Download PDF" for any resume.

**Q: Can I edit my resume after uploading?**
A: Yes, you can view and re-download. Full editing features coming soon.

**Q: How is the ATS score calculated?**
A: We match keywords from your resume against the job description and calculate compatibility.

**Q: Can I use the same account on multiple devices?**
A: Yes! Log in from any device and access all your resumes.

**Q: How long are resumes stored?**
A: Your resumes are stored as long as your account is active.

**Q: Is this free?**
A: Yes! Resume AI Builder is completely free to use.

**Q: What if I have more questions?**
A: Type anything you need help with, and I'll try to assist!"""
    }
}

# ============================================================================
# TASK EXECUTION FUNCTIONS - Actually perform requests
# ============================================================================

def write_profile_summary(job_title, skills, experience_years, industry=None):
    """
    Generate a professional profile summary.
    """
    summaries = [
        f"Results-driven {job_title} with {experience_years}+ years of proven expertise in designing, developing, and implementing scalable solutions. Proficient in {', '.join(skills[:3]) if skills else 'various technologies'} with a strong track record of delivering high-impact projects. Passionate about solving complex problems and staying current with emerging technologies.",
        
        f"Dynamic {job_title} professional with {experience_years}+ years of hands-on experience. Expert in {', '.join(skills[:2]) if skills else 'core technologies'} with demonstrated ability to lead cross-functional teams. Committed to driving innovation and continuous improvement in all endeavors.",
        
        f"Innovative {job_title} with {experience_years}+ years of experience building robust, scalable applications. Strong foundation in {', '.join(skills[:3]) if skills else 'technical development'} and proven success in delivering projects on time and within budget. Eager to leverage expertise to create meaningful impact.",
        
        f"Accomplished {job_title} professional with {experience_years}+ years of experience in {industry or 'the tech industry'}. Proficient in {', '.join(skills[:2]) if skills else 'multiple technologies'} with a focus on code quality, performance optimization, and team collaboration. Driven by challenges and committed to excellence.",
    ]
    
    return "✨ **Professional Profile Summary:**\n\n" + random.choice(summaries) + "\n\n*Feel free to customize this to better match your style and achievements.*"

def write_declaration():
    """
    Generate a professional declaration statement.
    """
    declarations = [
        "I hereby declare that all the information provided in this resume is true, accurate, and complete to the best of my knowledge. I have not concealed or omitted any material information.",
        
        "I certify that the information presented in this resume is factual, accurate, and honest. I understand that providing false information may result in rejection of my application or termination of employment.",
        
        "I declare that the details mentioned in this resume are true and genuine to the best of my knowledge and belief. I am responsible for the accuracy and authenticity of the information.",
        
        "I hereby certify that the information provided in this resume is complete and accurate. I have taken full responsibility for the correctness of all facts presented.",
    ]
    
    return "📝 **Declaration:**\n\n" + random.choice(declarations)

def optimize_text(text):
    """
    Optimize resume text with action verbs and metrics.
    """
    action_verbs = {
        "worked": "Led, Designed, Implemented, or Developed",
        "did": "Executed, Accomplished, or Delivered",
        "made": "Transformed, Optimized, or Enhanced",
        "helped": "Supported, Facilitated, or Enabled",
        "used": "Leveraged, Utilized, or Mastered",
        "created": "Architected, Built, or Engineered",
        "improved": "Streamlined, Enhanced, or Accelerated",
        "managed": "Orchestrated, Supervised, or Directed",
    }
    
    suggestions = ["Consider using stronger action verbs", "Add quantifiable metrics (numbers, percentages)", "Include specific technologies/tools used", "Highlight business impact and results"]
    
    optimized = "✅ **Text Optimization Suggestions:**\n\n"
    optimized += f"**Your Text:** \"{text}\"\n\n"
    optimized += "**Recommendations:**\n"
    optimized += f"• Use action verbs like: {', '.join(list(action_verbs.values())[0].split(', '))} instead of common verbs\n"
    optimized += f"• {random.choice(suggestions)}\n"
    optimized += "• Make it specific and measurable\n"
    optimized += "• Keep it concise (1-2 lines)\n\n"
    optimized += "**Example Optimization:**\n"
    optimized += f"\"Developed mobile app using React Native that increased user engagement by 40% and reduced load time by 35%\"\n\n"
    optimized += "*Provide more context if you want a specific rewrite!*"
    
    return optimized

def suggest_keywords(job_description):
    """
    Suggest keywords to include in resume based on job description.
    """
    common_keywords = {
        "python": ["Django", "Flask", "FastAPI", "NumPy", "Pandas"],
        "java": ["Spring", "Hibernate", "Maven", "JDBC", "Multithreading"],
        "javascript": ["React", "Node.js", "TypeScript", "Vue", "Angular"],
        "aws": ["EC2", "S3", "Lambda", "RDS", "CloudFront", "VPC"],
        "kubernetes": ["Docker", "Container Orchestration", "Helm", "CI/CD"],
        "sql": ["PostgreSQL", "MySQL", "Database Design", "Query Optimization"],
        "devops": ["Docker", "Git", "Jenkins", "GitHub Actions", "Monitoring"],
    }
    
    response = "🔑 **Suggested Keywords for Your Resume:**\n\n"
    response += "Based on the job description, consider adding:\n\n"
    
    # Try to find relevant keywords
    job_desc_lower = job_description.lower()
    found_keywords = []
    
    for keyword, related in common_keywords.items():
        if keyword in job_desc_lower:
            found_keywords.extend(related)
    
    if found_keywords:
        response += "**Technical Skills:**\n"
        for keyword in found_keywords[:5]:
            response += f"• {keyword}\n"
    else:
        response += "**Technical Skills:**\n"
        response += "• Leadership\n• Problem Solving\n• Communication\n• Project Management\n• Attention to Detail\n"
    
    response += "\n**Soft Skills:**\n"
    response += "• Team Leadership\n• Strategic Planning\n• Stakeholder Management\n• Agile Methodology\n"
    response += "\n💡 *Add 3-5 keywords from this list to boost your ATS score!*"
    
    return response

def write_cover_letter(job_title, company_name, your_name, years_experience):
    """
    Generate a professional cover letter template.
    """
    cover_letter = f"""📄 **Cover Letter Template:**

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With {years_experience}+ years of progressive experience in the field, I am confident in my ability to contribute significantly to your team and help drive organizational success.

In my current/previous role, I have developed a comprehensive skill set that aligns perfectly with your job requirements. I have successfully [mention key achievement], resulting in [quantifiable impact]. My expertise in [mention key skills] has enabled me to consistently deliver high-quality results while maintaining strong collaboration with cross-functional teams.

What particularly excites me about this opportunity at {company_name} is [mention something about the company]. I am eager to bring my passion for [relevant field] and my proven track record of success to your organization.

I am confident that my background, skills, and enthusiasm make me an excellent candidate for this position. I would welcome the opportunity to discuss how I can contribute to your team. Thank you for considering my application. I look forward to speaking with you soon.

Sincerely,
{your_name}

---
*Feel free to customize with your specific achievements and details!*"""
    
    return cover_letter

def write_skill_description(skill_name, skill_level="Intermediate"):
    """
    Generate detailed skill descriptions for resume.
    """
    descriptions = {
        "python": {
            "Advanced": "Expert in Python development with deep knowledge of OOP, data structures, and design patterns. Proficient in Django, Flask, FastAPI frameworks and data analysis libraries (Pandas, NumPy). Experienced in building scalable backend systems.",
            "Intermediate": "Solid understanding of Python fundamentals and common libraries. Comfortable with Django/Flask for web development and basic data manipulation with Pandas. Able to write clean, maintainable code.",
            "Beginner": "Basic knowledge of Python syntax and core concepts. Can write simple scripts and understand fundamental programming principles."
        },
        "javascript": {
            "Advanced": "Expert in JavaScript/TypeScript with mastery of ES6+ features. Proficient in React, Vue.js, and Node.js. Experience with async programming, state management, and building scalable frontend applications.",
            "Intermediate": "Comfortable with JavaScript fundamentals and DOM manipulation. Can work with React or similar frameworks. Understanding of asynchronous programming and REST APIs.",
            "Beginner": "Basic knowledge of JavaScript syntax and basic web interactions. Can understand and modify existing code."
        },
        "default": {
            "Advanced": f"Expert-level proficiency in {skill_name}. Deep understanding of advanced concepts and best practices. Proven ability to mentor others and lead projects using this technology.",
            "Intermediate": f"Solid working knowledge of {skill_name}. Comfortable using this technology in production environments. Can solve complex problems independently.",
            "Beginner": f"Foundational understanding of {skill_name}. Able to use this technology with guidance and actively learning to improve skills."
        }
    }
    
    skill_lower = skill_name.lower()
    skill_translations = descriptions.get(skill_lower, descriptions["default"])
    
    response = f"🎯 **Skill Description for {skill_name}:**\n\n"
    response += skill_translations.get(skill_level, skill_translations["Intermediate"])
    
    return response

def detect_task(query):
    """
    Detect what task the user is asking for and execute it.
    Returns (is_task, response)
    """
    query_lower = query.lower()
    
    # Profile summary
    if any(word in query_lower for word in ["write profile", "profile summary", "professional summary", "about me", "introduce myself"]):
        job_title = extract_value(query, "job title", "Software Engineer")
        skills = extract_value(query, "skills", "Python, React, Django")
        years = extract_value(query, "years", "5")
        return True, write_profile_summary(job_title, skills.split(","), int(years))
    
    # Declaration
    if any(word in query_lower for word in ["write declaration", "declaration", "declare", "statement of authenticity"]):
        return True, write_declaration()
    
    # Cover letter
    if any(word in query_lower for word in ["write cover letter", "cover letter", "letter for job", "application letter"]):
        job_title = extract_value(query, "position|job|title", "Software Engineer")
        company = extract_value(query, "company", "Tech Company")
        name = extract_value(query, "name|my name is", "John Doe")
        years = extract_value(query, "years|experience", "5")
        return True, write_cover_letter(job_title, company, name, years)
    
    # Optimize text - look for quoted text or text after "this:"
    if any(word in query_lower for word in ["optimize", "improve this", "rewrite", "make better", "stronger version"]):
        # Try to extract text from quotes or after "this:"
        quoted = re.findall(r'["\'](.+?)["\']', query)
        if quoted:
            return True, optimize_text(quoted[0])
        
        # Try to extract text after "this:"
        if "this:" in query_lower:
            text_to_optimize = query.split("this:", 1)[1].strip()
            if text_to_optimize:
                return True, optimize_text(text_to_optimize)
        
        # Try to extract everything after "optimize" or similar
        for keyword in ["optimize", "improve", "rewrite", "better"]:
            if keyword in query_lower:
                parts = query_lower.split(keyword, 1)
                if len(parts) > 1:
                    text = parts[1].strip().lstrip(": ").lstrip("\""  ).lstrip("'")
                    if text and len(text) > 3:
                        return True, optimize_text(text)
    
    # Suggest keywords
    if any(word in query_lower for word in ["suggest keywords", "what keywords", "keywords to add", "keywords for", "keywords based on"]):
        # Extract job description
        quoted = re.findall(r'["\'](.+?)["\']', query)
        if quoted:
            return True, suggest_keywords(quoted[0])
        
        # Try to extract text after "for:" or after the keyword phrase
        if "for:" in query_lower:
            job_desc = query.split("for:", 1)[1].strip()
            if job_desc and len(job_desc) > 3:
                return True, suggest_keywords(job_desc)
        
        # If just asking for keywords for a specific role
        if "backend" in query_lower or "frontend" in query_lower or "data scientist" in query_lower or "devops" in query_lower:
            role = ""
            if "backend" in query_lower:
                role = "Python, Java, Node.js, databases, API design, microservices, Docker, Kubernetes"
            elif "frontend" in query_lower:
                role = "JavaScript, React, Vue, Angular, CSS, HTML, Responsive Design, UI/UX"
            elif "data scientist" in query_lower:
                role = "Python, Machine Learning, TensorFlow, PyTorch, SQL, Statistics, Big Data"
            elif "devops" in query_lower:
                role = "Docker, Kubernetes, Jenkins, AWS, CI/CD, Linux, Terraform, Monitoring"
            
            if role:
                return True, suggest_keywords(role)
    
    # Skill description
    if any(word in query_lower for word in ["describe skill", "skill description", "explain", "tell about", "describe my"]):
        # Extract the skill name
        skill = None
        for keyword in ["skill", "expertise", "knowledge", "proficiency", "my"]:
            if keyword in query_lower:
                parts = query.split(keyword, 1)
                if len(parts) > 1:
                    skill = parts[1].strip().lstrip(": ").lstrip("'").lstrip("\"").split()[0]
                    break
        
        if not skill:
            skill = "Communication"
        
        level = "Intermediate"
        if "advanced" in query_lower or "expert" in query_lower:
            level = "Advanced"
        elif "beginner" in query_lower or "basic" in query_lower:
            level = "Beginner"
        
        return True, write_skill_description(skill, level)
    
    return False, None

def extract_value(query, keyword, default):
    """
    Extract value from query using keywords.
    """
    # For years/experience, try to extract numbers first
    if "years" in keyword or "experience" in keyword:
        numbers = re.findall(r'\d+', query)
        if numbers:
            return numbers[0]
    
    if not keyword:
        words = query.split()
        return words[-1] if words else default
    
    keywords = keyword.split("|")
    for kw in keywords:
        pattern = rf"{kw}\s+(?:is\s+)?['\"]?([^'\",.?!]+)"
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Make sure we don't get malformed values
            if value and len(value) > 1:
                return value
    
    return default

def extract_text_content(query):
    """
    Extract text content from query (text between quotes or after certain keywords).
    """
    # Try to find quoted text
    quoted = re.findall(r'["\'](.+?)["\']', query)
    if quoted:
        return quoted[0]
    
    # Try to extract text after keywords
    keywords = ["for:", "about:", "regarding:"]
    for kw in keywords:
        if kw in query.lower():
            text = query.split(kw, 1)[1].strip()
            return text
    
    return None

# ============================================================================
# GREETING & RESPONSE GENERATION
# ============================================================================

GREETINGS = {
    "keywords": ["hello", "hi", "hey", "greetings", "what's up", "how are you"],
    "responses": [
        "👋 Hello! I'm your Resume AI Assistant. I can help you with:\n\n✨ **PERFORM TASKS** - Write summaries, optimize text, suggest keywords, and more!\n📚 **ANSWER QUESTIONS** - About features, resume tips, ATS scoring, etc.\n\nWhat would you like me to do?",
        "Hi there! 👋 I can write professional content for your resume, optimize your text, answer questions about the app, and much more. What can I help with?",
        "Hey! 😊 Ready to create an amazing resume? I can write, optimize, suggest keywords, or answer any questions!",
        "🤖 Welcome! I'm here to:\n• Write your profile summary or cover letter\n• Optimize your resume text\n• Suggest keywords for ATS\n• Answer any questions\n\nWhat do you need?"
    ]
}

# ============================================================================
# SIMILARITY MATCHING - Find the best matching response
# ============================================================================

def string_similarity(a, b):
    """Calculate similarity between two strings (0.0 to 1.0)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(query, knowledge_base=KNOWLEDGE_BASE):
    """
    Find the best matching topic from knowledge base based on query.
    Returns (topic_name, response, confidence_score)
    """
    query_lower = query.lower()
    best_match = None
    best_score = 0
    best_response = None
    
    for topic, data in knowledge_base.items():
        keywords = data.get("keywords", [])
        
        # Check if any keyword matches
        for keyword in keywords:
            similarity = string_similarity(query_lower, keyword)
            if similarity > best_score:
                best_score = similarity
                best_match = topic
                best_response = data.get("response", "")
    
    return best_match, best_response, best_score

def handle_greeting(query):
    """Check if query is a greeting and return random greeting response"""
    greeting_keywords = GREETINGS["keywords"]
    query_lower = query.lower()
    
    for keyword in greeting_keywords:
        if keyword in query_lower:
            import random
            return random.choice(GREETINGS["responses"])
    
    return None

def generate_response(query):
    """
    Generate a response to user's question or request.
    
    Process:
    1. Check if it's a task (write, optimize, suggest, etc.)
    2. Check if it's a greeting
    3. Find best matching topic from knowledge base
    4. Return appropriate response
    """
    
    # First, check if user is asking for a TASK
    is_task, task_response = detect_task(query)
    if is_task:
        return task_response
    
    # Check for greetings
    greeting_response = handle_greeting(query)
    if greeting_response:
        return greeting_response
    
    # Find best matching topic
    topic, response, confidence = find_best_match(query)
    
    # If confidence is high enough, return the response
    if confidence > 0.3:  # Low threshold to catch various phrasing
        return response
    
    # If no good match, provide helpful fallback
    fallback = """😊 I'm not sure I understood that. Let me help you!

**I can PERFORM these tasks:**
✨ **Write** - Profile summary, cover letter, declarations, skill descriptions
✏️ **Optimize** - Improve your resume text with stronger verbs and metrics
🔑 **Suggest** - Keywords to add to boost your ATS score
📋 **Answer** - Questions about features, tips, and how to use the app

**Try asking:**
- "Write a profile summary for Software Engineer role"
- "Optimize this text: [your text]"
- "Suggest keywords for: [job description]"
- "Write a cover letter for [company name]"
- "Describe my Python skills"
- "What are the features?"
- "How do I improve my ATS score?"

What would you like me to do?"""
    
    return fallback

# ============================================================================
# TEST FUNCTION
# ============================================================================

if __name__ == "__main__":
    # Test the assistant
    test_queries = [
        "Hello!",
        "Write a profile summary for Python Developer with 3 years experience",
        "Write a declaration",
        "Optimize this: worked on projects and did good things",
        "Suggest keywords for a backend developer job",
        "Write cover letter for Google as John Doe",
        "What is ATS?",
        "How do I upload my resume?",
        "Something random"
    ]
    
    print("🤖 AI Assistant Test:\n")
    for query in test_queries:
        print(f"User: {query}")
        response = generate_response(query)
        print(f"Assistant: {response}\n")
        print("-" * 70 + "\n")
