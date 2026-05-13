# Resume AI Builder - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python Packages (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database (30 seconds)
```bash
python database.py
```

### Step 3: Start the App (30 seconds)
```bash
python app.py
```

### Step 4: Open Browser
Go to: **http://localhost:5000**

---

## First Time Using the App?

1. **Create Account**: Sign up with email and password
2. **Create Resume**: Use the builder form or upload existing resume
3. **Check ATS Score**: Upload job description and get compatibility score
4. **Download PDF**: Download your optimized resume
5. **Repeat**: Create multiple versions for different jobs

---

## File-by-File Explanation

### Backend Files

#### `app.py` - Main Application (700+ lines)
**What it does:**
- Runs the web server
- Handles all HTTP requests
- Manages user sessions
- Processes file uploads
- Connects everything together

**Key functions:**
- `index()` - Home page
- `signup_page()`, `login_page()`, `logout()` - Authentication
- `dashboard()` - User dashboard
- `upload_resume()` - File upload
- `builder()` - Resume builder form
- `ats_score()` - ATS compatibility check
- `keywords()` - Keyword extraction
- `download_resume()` - PDF download

**When to modify:**
- Add new pages
- Change routes
- Add API endpoints

#### `database.py` - Data Management (400+ lines)
**What it does:**
- Creates SQLite database tables
- Manages user accounts
- Validates passwords
- Stores/retrieves resumes
- Tracks ATS scores

**Key functions:**
- `init_database()` - Create tables
- `signup_user()` - New account
- `login_user()` - Check credentials
- `save_resume()` - Store resume data
- `save_ats_score()` - Save ATS results

**When to modify:**
- Add new data fields
- Change validation rules
- Add new tables

#### `ai_module.py` - AI/NLP Logic (400+ lines)
**What it does:**
- Extracts keywords from text
- Calculates ATS compatibility score
- Finds missing keywords
- Analyzes resume structure
- Generates helpful feedback

**Key functions:**
- `extract_keywords()` - Get important words
- `calculate_ats_score()` - Compare resume to job
- `find_missing_keywords()` - What's missing
- `find_skills()` - Identify technical skills
- `perform_ats_check()` - Complete analysis

**How it works (simple algorithm):**
1. Extract words from both texts
2. Remove common filler words
3. Count how many match
4. Return percentage match

**When to modify:**
- Add more technical skills
- Change scoring algorithm
- Improve keyword detection

#### `pdf_generator.py` - PDF Creation (200+ lines)
**What it does:**
- Generates professional PDFs
- Uses ReportLab library
- Creates clean, ATS-friendly formatting
- Saves PDFs to disk

**Key functions:**
- `generate_resume_pdf()` - Main function
- `get_pdf_filename()` - Create unique filename

**When to modify:**
- Change PDF layout
- Add new sections
- Change fonts/colors

#### `file_parser.py` - File Reading (250+ lines)
**What it does:**
- Reads PDF files
- Reads DOCX files
- Extracts plain text
- Identifies resume sections

**Key functions:**
- `extract_text_from_pdf()` - Read PDFs
- `extract_text_from_docx()` - Read DOCX
- `extract_text_from_file()` - Auto-detect type
- `parse_resume_sections()` - Find sections

**When to modify:**
- Add support for new file types
- Improve text extraction

---

### Frontend Files (Templates)

#### Templating Basics
All pages use **Jinja2** templating:
- `{% for ... %}` - Loops
- `{{ variable }}` - Display data
- `{% if ... %}` - Conditionals
- `{% extends "base.html" %}` - Inheritance

#### `templates/base.html` - Base Template
**Includes:**
- Navigation bar (header)
- Session management
- CSS/JS imports
- Footer

Used by ALL pages. Edit here to change navigation for entire site.

#### `templates/index.html` - Home Page
**Shows:**
- Features list
- How it works
- Call-to-action buttons

#### `templates/login.html` - Login Page
**Contains:**
- Email input
- Password input
- Login button
- Link to signup

#### `templates/signup.html` - SignUp Page
**Contains:**
- Name, email, password inputs
- Password strength indicator
- Real-time validation feedback
- Password confirmation check

**JavaScript:**
- `validatePassword()` - Check requirements
- Updates button state

#### `templates/dashboard.html` - User Dashboard
**Shows:**
- Welcome message
- Quick action cards
- User's resumes list
- Recent ATS scores
- Success tips

**Key sections:**
```
1. Header (Welcome)
2. Action Cards (Upload, Build, Check, Keywords)
3. Your Resumes (List of saved resumes)
4. Recent ATS Scores (History)
5. Tips (Success advice)
```

#### `templates/upload.html` - Resume Upload
**Features:**
- Drag & drop area
- File selection button
- Optional info fields
- Upload status

**JavaScript:**
- File upload handling
- Drag & drop support
- File preview

#### `templates/builder.html` - Resume Builder
**Layout:**
- Left: Form with inputs
- Right: Live preview

**Form fields:**
- Name
- Job title
- Summary
- Experience
- Skills
- Education

**JavaScript:**
- Real-time preview updates
- Live formatting

#### `templates/ats.html` - ATS Checker
**Two views:**
1. Form view (input)
   - Resume selector
   - Job description textarea
2. Results view
   - Score (large display)
   - Missing keywords
   - Skills found
   - Feedback
   - Structure check

#### `templates/keywords.html` - Keyword Generator
**Features:**
- Textarea for job description
- Results organized by category:
  - Technical skills
  - Soft skills
  - Other keywords
- Copy buttons for each keyword

---

### Static Files (CSS/JavaScript)

#### `static/css/style.css` - Main Stylesheet (1000+ lines)
**Sections:**
1. **Colors & Variables** - Theme colors
2. **Reset & Base** - Default styles
3. **Components** - Buttons, inputs, alerts
4. **Pages** - Specific page styling
5. **Responsive** - Mobile styles

**Key classes:**
- `.btn` - Buttons
- `.form-input` - Text inputs
- `.card` - Card containers
- `.error-box` - Error messages
- `.dashboard-*` - Dashboard elements

#### `static/js/script.js` - JavaScript (300+ lines)
**Utilities:**
- `showNotification()` - Display messages
- `formatDate()` - Format dates
- `copyToClipboard()` - Copy text

**Validation:**
- `isValidEmail()` - Email check
- `validatePassword()` - Password strength

**File upload:**
- `setupFileUpload()` - Drag & drop

**Animations:**
- CSS keyframes for smooth effects

---

## Database Schema

### Users Table
```
id          (primary key)
email       (unique email)
password_hash (SHA256 hash)
full_name   (user's name)
created_at  (timestamp)
```

### Resumes Table
```
id          (primary key)
user_id     (foreign key → users)
name        (resume owner's name)
role        (job title)
summary     (professional summary)
experience  (work history)
skills      (skills list)
education   (education info)
raw_text    (original full text)
created_at  (timestamp)
```

### ATS Scores Table
```
id              (primary key)
user_id         (foreign key → users)
resume_id       (foreign key → resumes)
job_description (the job posting)
ats_score       (0-100)
missing_keywords (list)
feedback        (recommendations)
created_at      (timestamp)
```

---

## How Data Flows

### Resume Upload Flow
```
1. User selects file
2. Flask receives file (app.py)
3. File saved to uploads/ folder
4. File parser extracts text (file_parser.py)
5. Data saved to database (database.py)
6. User sees success message
```

### ATS Check Flow
```
1. User selects resume + pastes job
2. Flask receives both (app.py)
3. AI module gets resume text from database
4. AI analyzes both texts (ai_module.py)
5. Score calculated
6. Result saved to database
7. Results displayed to user
```

### PDF Download Flow
```
1. User clicks download
2. Flask gets resume from database (app.py)
3. PDF generator creates file (pdf_generator.py)
4. File sent to browser
5. Browser downloads as PDF
```

---

## Key Technologies Explained

### Flask
- **What:** Python web framework
- **Does:** Routes URLs, renders templates, handles requests
- **Key concept:** `@app.route('/path')` - Map URL to function

### SQLite
- **What:** Simple database
- **Does:** Stores users, resumes, ATS scores
- **Benefit:** No server needed, file-based

### Jinja2
- **What:** Template engine
- **Does:** Mix HTML with Python variables
- **Example:** `{{ user.name }}` in HTML

### ReportLab
- **What:** PDF library
- **Does:** Creates PDFs programmatically
- **Benefit:** Professional, ATS-friendly PDFs

### PyPDF2
- **What:** PDF reader
- **Does:** Extract text from PDFs
- **Limitation:** Works for text-based PDFs only

### python-docx
- **What:** DOCX reader
- **Does:** Extract text from Word documents
- **Benefit:** Works perfectly for modern .docx files

---

## Common Modifications

### Add a New Button to Dashboard
1. Edit `templates/dashboard.html`
2. Add new `<a>` with `action-card` class
3. Create new route in `app.py`
4. Create new template

### Change Color Scheme
1. Edit `static/css/style.css`
2. Find `:root` section
3. Change `--primary-color`, `--secondary-color`

### Add New Resume Section
1. Edit `templates/builder.html` - add form field
2. Edit `database.py` - add column to resumes table
3. Edit `ai_module.py` - include in keyword analysis

### Improve ATS Scoring
1. Edit `ai_module.py`
2. Modify `calculate_ats_score()` function
3. Add weighting for important keywords
4. Adjust algorithm logic

---

## Debugging Tips

### Check Server Logs
When running locally, watch terminal output for errors:
```
Traceback (most recent call last):
  File "app.py", line X, in function_name
    # Error here
```

### Use Browser DevTools (F12)
1. **Console** - JavaScript errors
2. **Network** - HTTP requests
3. **Elements** - HTML structure

### Add Debug Prints
```python
# In app.py
@app.route('/example')
def example():
    print("Debug: User ID =", session.get('user_id'))
    return "OK"
```

Check terminal output for the print message.

### Test Locally First
Before deploying:
1. Test signup/login
2. Test file upload
3. Test ATS score
4. Test PDF download
5. Check database for saved data

---

## Ready to Deploy?

See README.md for deployment instructions!

---

## Need Help?

1. **Read the code comments** - Every part is explained
2. **Check README.md** - Full documentation
3. **Look at examples** - HTML templates show patterns
4. **Test locally** - Make changes and test
5. **Print debug info** - Add `print()` statements

**Happy Coding! 🚀**
