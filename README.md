Resume AI Builder 🚀

An AI-powered full-stack resume platform that helps users build professional resumes, analyze ATS compatibility, generate keyword suggestions, and export polished PDF resumes.

📌 Features
✅ Resume Builder
✅ Resume Upload & Parsing
✅ ATS Score Checker
✅ Keyword Suggestions
✅ PDF Resume Generation
✅ User Authentication
✅ Responsive UI
✅ SQLite Database Integration
🛠 Tech Stack
Frontend
HTML5
CSS3
JavaScript
Jinja2 Templates
Backend
Python
Flask
Database
SQLite
Additional Libraries
PyPDF2
python-docx
reportlab
📂 Project Structure
Resume-AI-Builder/
│
├── app.py
├── database.py
├── ai_module.py
├── pdf_generator.py
├── file_parser.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── builder.html
│   ├── ats.html
│   ├── keywords.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── uploads/
├── resumes/
│
├── requirements.txt
├── README.md
├── QUICKSTART.md
└── PROJECT_SUMMARY.md
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/resume-ai-builder.git
cd resume-ai-builder
2️⃣ Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Linux / Mac
python3 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Run the Application
python app.py

Open browser:

http://localhost:5000
🧠 How ATS Scoring Works

The ATS checker:

Extracts keywords from job descriptions
Matches them against resume content
Calculates compatibility score
Suggests missing keywords
🔐 Authentication

Passwords are securely hashed using SHA256 before storage.

Example:

User Password → SHA256 Hash → Stored in Database
📄 PDF Resume Generation

Users can:

Build resumes directly in browser
Export resumes as professional PDFs
Store generated resumes locally
📊 Key Learning Concepts

This project demonstrates:

Flask Web Development
Full-Stack Architecture
Database Design
Authentication Systems
File Upload Handling
PDF Parsing
Basic NLP / ATS Analysis
Responsive UI Design
🚀 Future Improvements
OpenAI API Integration
Real NLP-based ATS Analysis
Resume Templates
LinkedIn Import
Email Support
Cloud Deployment
Admin Dashboard
Analytics Panel
🔒 Production Checklist

Before deployment:

 Use environment variables
 Replace Flask secret key
 Enable HTTPS
 Add CSRF protection
 Use PostgreSQL
 Add logging & monitoring
 Configure backups
📸 Screenshots

Add screenshots here:

![Home Page](screenshots/home.png)
![ATS Checker](screenshots/ats.png)
![Resume Builder](screenshots/builder.png)
📦 Requirements

Example:

Flask
PyPDF2
python-docx
reportlab
Werkzeug
🤝 Contributing

Contributions are welcome.

Fork the repository
Create a new branch
Commit changes
Push to branch
Create Pull Request
📜 License

This project is licensed under the MIT License.

👨‍💻 Author

Developed by Giri

⭐ Support

If you like this project:

Star the repository
Share with others
Contribute improvements
🎉 Final Note

This project is a complete beginner-to-intermediate level AI-powered Flask application that combines:

Resume building
ATS analysis
Authentication
File parsing
PDF generation
Responsive UI

A strong portfolio project for students and aspiring developers.
