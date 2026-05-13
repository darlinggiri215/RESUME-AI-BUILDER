import os
from database import init_database, get_resume
from pdf_generator import generate_resume_pdf

os.makedirs('resumes', exist_ok=True)
init_database()
resume = get_resume(1)
if not resume:
    print('NO_RESUME')
else:
    out = os.path.join('resumes', f"test_resume_{resume.get('id', 1)}.pdf")
    result = generate_resume_pdf(
        resume.get('name', ''),
        resume.get('role', ''),
        resume.get('summary', ''),
        resume.get('experience', ''),
        resume.get('skills', ''),
        resume.get('education', ''),
        out,
        phone=resume.get('phone', ''),
        email=resume.get('email', ''),
        dob=resume.get('dob', ''),
        linkedin=resume.get('linkedin', ''),
        address=resume.get('address', ''),
        github_link=resume.get('github_link', ''),
        internships=resume.get('internships', ''),
        projects=resume.get('projects', ''),
        certifications=resume.get('certifications', ''),
        strengths=resume.get('strengths', ''),
        weaknesses=resume.get('weaknesses', ''),
        declaration=resume.get('declaration', '')
    )
    print('RESULT:', result)
