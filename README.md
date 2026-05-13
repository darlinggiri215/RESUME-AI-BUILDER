# 📄 Resume AI Builder

A college-level web application that helps users create, optimize, and manage resumes with AI-powered ATS (Applicant Tracking System) compatibility checking.

## ✨ Features

- **User Authentication**: Sign up and login system with secure passwords
- **Resume Builder**: Create resumes from scratch using a form
- **Resume Upload**: Upload existing PDFs, DOCX, or TXT resumes
- **ATS Score Checker**: Check how well your resume matches job descriptions (0-100%)
- **Keyword Generator**: Extract important keywords from job postings
- **PDF Generation**: Download your resume as a professional PDF
- **Resume Storage**: Save multiple resumes and ATS check histories

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python with Flask |
| **Database** | SQLite |
| **Frontend** | HTML, CSS, JavaScript |
| **PDF Generation** | ReportLab |
| **File Parsing** | PyPDF2, python-docx |
| **Authentication** | Password hashing with SHA256 |

## 📋 Project Structure

```
Resume AI Builder/
├── app.py                    # Main Flask application with all routes
├── database.py               # User and resume data management
├── ai_module.py              # ATS scoring and keyword analysis
├── pdf_generator.py          # Generate PDFs from resume data
├── file_parser.py            # Extract text from PDF/DOCX files
├── requirements.txt          # Python package dependencies
├── resume_ai.db              # SQLite database (created on first run)
│
├── templates/                # HTML templates
│   ├── base.html             # Base template with navigation
│   ├── index.html            # Home / landing page
│   ├── login.html            # Login page
│   ├── signup.html           # Sign up page
│   ├── dashboard.html        # User dashboard
│   ├── upload.html           # Resume upload page
│   ├── builder.html          # Resume builder form
│   ├── ats.html              # ATS score checker
│   ├── keywords.html         # Keyword generator
│   ├── 404.html              # 404 error page
│   └── 500.html              # 500 error page
│
├── static/                   # Static files
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   └── js/
│       └── script.js         # Client-side JavaScript
│
├── uploads/                  # Uploaded resume files (created at runtime)
└── resumes/                  # Generated PDF files (created at runtime)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A code editor (VS Code, PyCharm, etc.)

### Installation Steps

#### Step 1: Install Python Packages

```bash
pip install -r requirements.txt
```

This installs:
- **Flask**: Web framework
- **python-docx**: Read DOCX files
- **PyPDF2**: Read PDF files
- **reportlab**: Generate PDF files

#### Step 2: Initialize the Database

The database is automatically created when you first run the app, but you can manually initialize it:

```bash
python database.py
```

#### Step 3: Run the Application

```bash
python app.py
```

You should see:
```
============================================================
Resume AI Builder is starting...
============================================================
📱 Open your browser and go to: http://localhost:5000
============================================================
```

#### Step 4: Open in Browser

Go to: **http://localhost:5000**

## 📚 How to Use

### 1. Create an Account

1. Click **"Sign Up"** on the home page
2. Enter your name, email, and password
3. Password must have:
   - At least 8 characters
   - 1 uppercase letter
   - 1 special character (!@#$%^&*)
   - At least 2 numbers
4. Click **"Create Account"**

### 2. Login

1. Enter your email and password
2. Click **"Login"**
3. You'll be taken to your dashboard

### 3. Create or Upload Resume

#### Option A: Build from Scratch

1. Click **"Build from Scratch"** on dashboard
2. Fill in all sections:
   - Name
   - Job Title/Role
   - Professional Summary
   - Work Experience
   - Skills
   - Education
3. See live preview on the right
4. Click **"Create Resume"**

#### Option B: Upload Existing Resume

1. Click **"Upload Resume"** on dashboard
2. Drag & drop or select a PDF/DOCX file
3. (Optional) Add extra information
4. Click **"Upload Resume"**
5. Resume text will be extracted automatically

### 4. Check ATS Score

1. Click **"ATS Score Check"** on dashboard
2. Select one of your resumes
3. Paste a job description
4. Click **"Check ATS Score"**
5. See your score and missing keywords

**Understanding Your Score:**
- **80-100%**: Excellent match
- **60-80%**: Good match
- **30-60%**: Moderate match
- **0-30%**: Low match - needs improvements

### 5. Generate Keywords

1. Click **"Keyword Generator"**
2. Paste a job description
3. Click **"Extract Keywords"**
4. See technical skills, soft skills, and other keywords
5. Copy keywords to use in your resume

### 6. Download Resume

1. On your dashboard, find a resume
2. Click **"Download PDF"**
3. Your resume will be downloaded as a PDF file

## 🔐 Password Security

Passwords are stored securely using SHA256 hashing. This means:
- Even if the database is stolen, passwords are protected
- Your password is never stored in plain text
- Each password requires: uppercase, numbers, special characters, and 8+ characters

## 📊 How ATS Scoring Works

The ATS (Applicant Tracking System) score is calculated by:

1. **Extract Keywords**: Find all important words in both your resume and job description
2. **Find Matches**: Count how many keywords match
3. **Calculate Percentage**: (Matches / Total Job Keywords) × 100
4. **Return Score**: 0-100%

**Example:**
- Job description has 50 important keywords
- Your resume matches 35 of them
- Score = (35/50) × 100 = **70%** (Good match)

## 💡 Tips for Success

### For Better ATS Scores:
1. **Use clear formatting**: Bullet points, standard fonts
2. **Include keywords**: Copy important terms from job description
3. **Complete all sections**: Contact, summary, experience, skills, education
4. **Use numbers**: "Increased sales 40%" beats "Improved sales"
5. **Avoid tables/images**: ATS systems can't read them

### For Resume Building:
1. Keep professional summary to 2-3 sentences
2. List experience in reverse chronological order (newest first)
3. Use action verbs: Led, Managed, Built, Designed, Developed
4. Quantify achievements with numbers and percentages
5. Customize for each job application

## 🔗 API Routes

All routes are in `app.py`. Here's a quick reference:

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/signup` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | End session |
| `/dashboard` | GET | User dashboard |
| `/upload` | GET, POST | Upload resume |
| `/builder` | GET, POST | Build resume from form |
| `/ats-score` | GET, POST | Check ATS compatibility |
| `/keywords` | GET, POST | Generate keywords |
| `/download/<id>` | GET | Download resume as PDF |

## 🐛 Troubleshooting

### "Port 5000 is already in use"
Flask is trying to run on port 5000 but it's in use. Either:
1. Close the other app using port 5000
2. Change port in `app.py`: `app.run(port=5001)`

### "ModuleNotFoundError: No module named 'flask'"
Install packages:
```bash
pip install -r requirements.txt
```

### "Database locked" error
The database file is being accessed by multiple processes. Try:
1. Close the Flask app
2. Delete `resume_ai.db`
3. Run `python database.py` to reinitialize
4. Run `python app.py` again

### Files uploaded but not showing
Check the `uploads/` folder to ensure permission to read/write.

## 📝 File Explanations

### app.py
- Main Flask application
- Contains all routes (login, upload, ATS, etc.)
- Session management for user authentication
- File upload handling
- Integrates all other modules

### database.py
- SQLite database setup
- User management (signup, login)
- Password validation and hashing
- Resume storage
- ATS score history

### ai_module.py
- Keyword extraction from text
- ATS score calculation
- Missing keywords finder
- Resume structure analysis
- Simple AI (no external APIs) - just Python

### pdf_generator.py
- Generates professional PDF resumes
- Uses ReportLab library
- Clean, ATS-friendly formatting
- Supports all resume sections

### file_parser.py
- Extracts text from PDF files (PyPDF2)
- Extracts text from DOCX files (python-docx)
- Identifies resume sections
- Auto-extracts contact info

## 🎨 Customization

### Change Colors
Edit `static/css/style.css` and modify the `--primary-color` variable:
```css
:root {
    --primary-color: #0066cc;  /* Change this */
}
```

### Change App Name
Edit `templates/base.html` and `app.py`:
```python
@app.route('/')
def index():
    # Change title here
```

### Add New Routes
Add new functions in `app.py`:
```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

## 🔒 Security Notes

⚠️ **This is a college project**. For production use:

1. Change `app.secret_key` in `app.py` to a secure random string
2. Use environment variables for secrets (not in code)
3. Enable HTTPS/SSL
4. Add CSRF protection
5. Implement rate limiting
6. Use a production database (PostgreSQL)
7. Add input sanitization
8. Implement logging

Example for environment variables:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')
```

## 📖 Learning Outcomes

This project teaches:

1. **Web Development**: Flask framework and routing
2. **Databases**: SQLite and SQL queries
3. **Authentication**: Password hashing and sessions
4. **File Processing**: Reading PDF and DOCX files
5. **PDF Generation**: Creating documents programmatically
6. **Natural Language Processing**: Simple keyword analysis
7. **Frontend**: HTML, CSS, JavaScript
8. **Full Stack**: Backend and frontend integration
9. **Database Design**: Planning tables and relationships

## 🚢 Deployment

To deploy this app (e.g., to Heroku, PythonAnywhere):

1. Create a `Procfile`:
```
web: python app.py
```

2. Set `debug=False` in `app.py` for production

3. Use a production WSGI server (Gunicorn):
```bash
pip install gunicorn
gunicorn app:app
```

4. Update database path to use environment path

## 📧 Support

If you have issues:
1. Check the error message in terminal
2. Look at browser console (F12 → Console)
3. Review the code comments
4. Check the Troubleshooting section above

## 📄 License

This is a college project. Feel free to use and modify for educational purposes.

## 👨‍💻 Author

Created as a college-level project to demonstrate:
- Full-stack web development
- Database design
- Authentication systems
- Natural language processing
- PDF generation
- Responsive web design

---

**Happy Resume Building! 🚀**

For any questions or improvements, feel free to modify the code and learn!
