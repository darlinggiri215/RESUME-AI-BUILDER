"""
APP.PY - Resume AI Builder Web Application
==========================================

Main Flask application with all routes.

HOW IT WORKS:
1. User signs up / logs in → Sessions manage user context
2. User uploads resume or builds from scratch
3. User can check ATS score, get keyword suggestions, generate PDF
4. All data is stored in SQLite database

ROUTES:
- / (home/login page)
- /signup (register new user)
- /login (user login)
- /logout (end session)
- /dashboard (user dashboard)
- /upload (upload resume file)
- /builder (build resume from form)
- /ats-score (check resume ATS compatibility)
- /keyword-generator (suggest keywords)
- /download (download resume as PDF)
- /history (view past ATS checks)
"""

from flask import Flask, flash, render_template, request, jsonify, session, redirect, url_for, send_file
import sqlite3
from werkzeug.utils import secure_filename
import os
from functools import wraps
import traceback

# Import our custom modules
from database import (
    init_database, signup_user, login_user, get_user_info,
    save_resume, get_user_resumes, get_resume,
    save_ats_score, get_user_ats_scores,
    generate_otp, send_otp_email, send_otp_sms, store_otp, verify_otp, create_user_from_otp, hash_password
)
from ai_module import (
    perform_ats_check, find_missing_keywords, 
    generate_keywords_from_description, find_skills
)
from ai_assistant import generate_response
from file_parser import extract_text_from_file, is_allowed_file, extract_basic_resume_data
from pdf_generator import generate_resume_pdf, get_pdf_filename

# ============================================================================
# FLASK APP SETUP
# ============================================================================

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!

# File upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
DB_NAME = 'resume_ai_builder.db'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists('resumes'):
    os.makedirs('resumes')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ============================================================================
# RESUME TEMPLATES
# ============================================================================

RESUME_TEMPLATES = {
    'software_engineer': {
        'id': 'software_engineer',
        'title': 'Software Engineer',
        'icon': '💻',
        'description': 'Perfect for developers, engineers, and software professionals',
        'data': {
            'name': 'John Doe',
            'phone': '+1 (555) 123-4567',
            'email': 'john.doe@email.com',
            'dob': '01/15/1995',
            'linkedin': 'linkedin.com/in/johndoe',
            'address': 'San Francisco, CA 94105, USA',
            'github_link': 'github.com/johndoe',
            'role': 'Senior Software Engineer',
            'summary': 'Results-driven Senior Software Engineer with 8+ years of experience designing and developing scalable applications. Proficient in Python, Java, and JavaScript with expertise in cloud technologies and microservices architecture. Proven track record of leading cross-functional teams and delivering high-impact projects on time.',
            'experience': '''Senior Software Engineer at Tech Company (2021-Present)
- Led development and deployment of microservices architecture serving 1M+ users
- Mentored team of 5 junior developers, improving code quality by 35%
- Optimized database queries reducing API response time by 40%
- Designed and implemented CI/CD pipeline reducing deployment time by 60%

Software Engineer at StartUp Inc (2018-2021)
- Built REST APIs using Python and Django serving 100k+ requests daily
- Developed React frontend components used by 5M+ users
- Implemented automated testing increasing code coverage from 45% to 85%
- Collaborated with product team to deliver 15+ features quarterly

Junior Developer at Web Solutions (2016-2018)
- Developed full-stack web applications using PHP and JavaScript
- Fixed critical bugs improving application stability by 25%
- Participated in code reviews and knowledge sharing sessions''',
            'internships': '''Software Engineering Intern at Tech Startup (Summer 2015)
- Developed new features for customer dashboard using React and Node.js
- Participated in agile sprint planning and daily standups
- Fixed 20+ bugs improving application stability''',
            'projects': '''Open Source Projects:
- GitHub: Contributed to Django framework (50+ merged PRs)
- Personal Project: Built ML-based Resume Parser using TensorFlow achieving 94% accuracy
- Hackathon Winner: "Smart Task Manager" - Awarded for best UI/UX at Tech Summit 2021''',
            'certifications': '''AWS Certified Solutions Architect - Professional (2021)
Google Cloud Certified Associate Cloud Engineer (2020)
Certified Kubernetes Administrator (CKA) (2019)
MongoDB University - Developer Certified (2018)''',
            'skills': '''Python - Expert in object-oriented programming, data manipulation, and building scalable applications with frameworks like Django and Flask.
Java - Strong foundation in enterprise applications, design patterns, and building robust backend systems.
JavaScript - Proficient in ES6+, async operations, and DOM manipulation for interactive web experiences.
React - Advanced experience building component-based UIs, state management with Redux, and React Hooks.
Django - REST API development, ORM operations, and building secure web applications with authentication.
Flask - Lightweight web framework for rapid development of microservices and RESTful APIs.
PostgreSQL - Database design, complex queries, indexing, and optimization for large-scale applications.
MongoDB - NoSQL database design, document modeling, and building flexible data schemas.
Docker - Containerization of applications, creating Dockerfiles, and managing container orchestration.
Kubernetes - Container orchestration, deployment strategies, and managing distributed systems.
AWS - Cloud services including EC2, S3, Lambda, RDS, and infrastructure as code.''',
            'strengths': '''- Problem-solving mindset with ability to break complex problems into manageable solutions
- Strong communication skills across technical and non-technical teams
- Proven ability to mentor and guide junior developers
- Self-motivated and eager to learn new technologies
- Excellent at time management and meeting deadlines''',
            'weaknesses': '''- Sometimes over-engineer solutions when simple approaches would suffice
- Perfectionist tendencies that can occasionally slow down project delivery
- Preference for working on technical tasks over administrative responsibilities
- Limited experience with certain frontend frameworks
- Need to improve public speaking skills for presentations''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''B.S. Computer Science
State University
Graduated: May 2016
GPA: 3.7/4.0'''
        }
    },
    'data_scientist': {
        'id': 'data_scientist',
        'title': 'Data Scientist',
        'icon': '📊',
        'description': 'For data analysts, machine learning engineers, and data professionals',
        'data': {
            'name': 'Jane Smith',
            'phone': '+1 (555) 234-5678',
            'email': 'jane.smith@email.com',
            'dob': '03/22/1994',
            'linkedin': 'linkedin.com/in/janesmith',
            'address': 'New York, NY 10001, USA',
            'github_link': 'github.com/janesmith',
            'role': 'Senior Data Scientist',
            'summary': 'Data scientist with 7+ years of experience building machine learning models and deriving insights from complex datasets. Expert in Python, SQL, and data visualization tools. Strong background in statistical analysis, predictive modeling, and business analytics. Proven ability to translate business requirements into actionable data solutions.',
            'experience': '''Senior Data Scientist at Analytics Corp (2020-Present)
- Developed machine learning models for customer churn prediction achieving 92% accuracy
- Led data strategy projects generating $2M+ in revenue impact
- Built automated ETL pipelines processing 10TB+ data daily using Apache Spark
- Created interactive dashboards in Tableau used by 50+ stakeholders

Data Scientist at FinTech Solutions (2018-2020)
- Implemented recommendation engine serving 500k+ personalized suggestions daily
- Conducted A/B testing and statistical analysis influencing product decisions
- Optimized ML models reducing inference time from 500ms to 50ms
- Collaborated with engineering team to deploy models into production

Data Analyst at Retail Company (2016-2018)
- Analyzed customer behavior patterns identifying growth opportunities
- Built SQL queries optimizing database queries by 50%
- Developed Python scripts automating repetitive analysis tasks''',
            'internships': '''Data Science Intern at Fortune 500 Tech Company (Summer 2016)
- Analyzed large datasets using Python and SQL
- Built predictive models for customer segmentation
- Collaborated with business stakeholders on analytics projects''',
            'projects': '''Kaggle Competitions:
- Ranked Top 5% in "Housing Price Prediction" competition
- Published 20+ machine learning notebooks with 5k+ upvotes
- Personal ML Project: Built recommendation engine predicting movie preferences with 91% accuracy''',
            'certifications': '''Google Cloud Professional Data Engineer (2021)
AWS Certified ML - Specialty (2020)
DataCamp: Machine Learning Engineer Track (2019)
Coursera: Deep Learning Specialization by Andrew Ng (2018)''',
            'skills': '''Python - Core language for data science with extensive knowledge of data manipulation and statistical computing.
R - Statistical programming language for exploratory data analysis and visualization.
SQL - Advanced query writing, database optimization, and complex joins for data extraction.
Machine Learning - Algorithm selection, model training, hyperparameter tuning, and cross-validation techniques.
TensorFlow - Deep learning framework for building neural networks and training complex models.
PyTorch - Dynamic computational graphs for research and production ML model development.
Scikit-learn - Machine learning library for classification, regression, and clustering tasks.
Pandas - Data manipulation and cleaning with DataFrames and time-series analysis.
NumPy - Numerical computing with arrays, linear algebra, and mathematical operations.
Tableau - Interactive dashboard creation and business intelligence visualization.
Apache Spark - Distributed computing framework for big data processing and analysis.''',
            'strengths': '''- Strong analytical and statistical thinking abilities
- Excellent data visualization skills transforming complex data into actionable insights
- Expertise in explaining ML concepts to non-technical stakeholders
- Highly collaborative and detail-oriented
- Strong problem-solving approach to complex data challenges''',
            'weaknesses': '''- Sometimes focuses too much on data exploration over execution
- Limited experience with real-time streaming data systems
- Can be overly critical of data quality issues
- Preference for Python over other languages impacts versatility
- Need to improve project management skills for larger initiatives''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''M.S. Data Science
Tech University
Graduated: May 2018
GPA: 3.8/4.0

B.S. Statistics
Tech University
Graduated: May 2016'''
        }
    },
    'product_manager': {
        'id': 'product_manager',
        'title': 'Product Manager',
        'icon': '🎯',
        'description': 'For product managers, product owners, and strategy professionals',
        'data': {
            'name': 'Alex Johnson',
            'phone': '+1 (555) 345-6789',
            'email': 'alex.johnson@email.com',
            'dob': '07/10/1993',
            'linkedin': 'linkedin.com/in/alexjohnson',
            'address': 'Seattle, WA 98101, USA',
            'github_link': 'github.com/alexjohnson',
            'role': 'Senior Product Manager',
            'summary': 'Strategic Product Manager with 9+ years of experience leading cross-functional teams and launching successful products. Expertise in product strategy, user research, and data-driven decision making. Strong analytical skills combined with exceptional communication abilities. Proven track record of managing products generating $50M+ in annual revenue.',
            'experience': '''Senior Product Manager at Tech Products (2021-Present)
- Led product strategy and roadmap for flagship product used by 2M+ users
- Increased user engagement by 45% through data-driven feature prioritization
- Managed product budget of $5M+ and cross-functional team of 8
- Launched 12 major features generating $15M in additional revenue

Product Manager at SaaS Company (2018-2021)
- Owned B2B product P&L ($10M annual revenue)
- Reduced customer churn from 8% to 4% through targeted feature improvements
- Led user research with 100+ customers informing product strategy
- Managed product launches impacting 50k+ enterprise customers

Associate Product Manager at StartUp (2016-2018)
- Supported product launches resulting in 3x user growth
- Analyzed user data identifying feature opportunities
- Collaborated with design and engineering to deliver 20+ features''',
            'internships': '''Product Management Intern at Tech Unicorn (Summer 2015)
- Conducted user interviews and analyzed product usage data
- Supported product launch resulting in 2x user growth
- Created product spec documents for new features''',
            'projects': '''Led Product Development:
- Launched "Analytics Dashboard" feature: 30% increase in user retention
- Spearheaded "Mobile App" strategy: 500k+ downloads in first 6 months
- Initiated "Partner Marketplace" program: Generated $5M in GMV year 1''',
            'certifications': '''Reforge: Product Strategy Course (2021)
Reforge: Executing Product Leadership (2020)
Pragmatic Institute: Product Management Certification (2019)
Google Analytics Certification (2018)''',
            'skills': '''Product Strategy - Vision setting, long-term roadmap planning, and aligning teams around strategic objectives.
User Research - Conducting interviews, surveys, and usability testing to understand customer needs.
Data Analysis - Analyzing product metrics, A/B test results, and customer behavior patterns.
SQL - Writing complex queries to extract insights from product databases.
Google Analytics - Tracking user engagement, conversion funnels, and campaign performance.
Figma - Collaboration with design teams on wireframes, mockups, and prototype evaluation.
Jira - Managing sprints, tracking features, and coordinating with engineering teams.
Agile Methodology - Working in two-week sprints with daily standups and retrospectives.
Stakeholder Management - Communicating with executives, customers, and cross-functional teams.''',
            'strengths': '''- Visionary thinking combined with practical execution abilities
- Natural leader capable of inspiring and aligning cross-functional teams
- Strong analytical and data-driven decision making
- Exceptional communication and negotiation skills
- User-centric mindset with empathy for customer needs''',
            'weaknesses': '''- Sometimes focuses too much on long-term vision over short-term execution
- Can be impatient with slower decision-making processes
- Limited technical background impacts hands-on problem-solving
- Tendency to say yes to too many initiatives
- Need to improve conflict resolution skills in heated discussions''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''MBA - Business Administration
Business School
Graduated: May 2018

B.S. Business Administration
University
Graduated: May 2016
Concentration: Marketing'''
        }
    },
    'designer': {
        'id': 'designer',
        'title': 'UX/UI Designer',
        'icon': '🎨',
        'description': 'For designers, UX researchers, and creative professionals',
        'data': {
            'name': 'Sarah Williams',
            'phone': '+1 (555) 456-7890',
            'email': 'sarah.williams@email.com',
            'dob': '09/18/1996',
            'linkedin': 'linkedin.com/in/sarahwilliams',
            'address': 'Austin, TX 78701, USA',
            'github_link': 'github.com/sarahwilliams',
            'role': 'Senior UX/UI Designer',
            'summary': 'Creative UX/UI Designer with 6+ years of experience designing user-centered digital products. Expertise in user research, wireframing, prototyping, and design systems. Passionate about creating intuitive and visually stunning interfaces. Strong portfolio of successful product launches and design improvements.',
            'experience': '''Senior UX/UI Designer at Design Studio (2021-Present)
- Led design system implementation improving design consistency by 60%
- Redesigned core product interface increasing user satisfaction from 72% to 89%
- Conducted user research with 200+ users informing design decisions
- Mentored 3 junior designers improving team productivity by 40%

UX Designer at Tech Company (2018-2021)
- Designed mobile app used by 1M+ users receiving 4.8 star rating
- Created wireframes and prototypes for 25+ features
- Collaborated with engineering to implement designs maintaining pixel-perfect accuracy
- Improved mobile conversion rate by 35% through iterative design improvements

UI Designer at Creative Agency (2016-2018)
- Designed user interfaces for 10+ client projects
- Developed brand guidelines and component libraries
- Conducted usability testing identifying and fixing UX issues''',
            'internships': '''UX/UI Design Intern at Digital Agency (Summer 2015)
- Designed mobile app interfaces using Figma
- Participated in user testing sessions and usability studies
- Created design mockups and prototypes''',
            'projects': '''Design Projects:
- Redesigned Fintech App: Increased user engagement by 45%
- Created Design System: 80+ reusable components adopted by 4 teams
- Mobile Banking App: Award-winning design at Digital Design Summit 2022
- Portfolio: dribbble.com/sarahwilliams (500+ followers)''',
            'certifications': '''Google UX Design Certificate (2021)
Nielsen Norman UX Certification (2020)
Interaction Design Foundation - Advanced Course (2019)
Adobe Creative Cloud Master Certification (2018)''',
            'skills': '''Figma - Collaborative design tool for creating wireframes, prototypes, and interactive components.
Adobe XD - Rapid prototyping and interactive design for web and mobile applications.
Prototyping - Creating clickable prototypes to validate design concepts before development.
Wireframing - Low-fidelity mockups to plan user flows and information architecture.
User Research - Conducting interviews, surveys, and usability studies to inform design decisions.
Design Systems - Creating reusable component libraries and design guidelines for consistency.
HTML/CSS - Front-end markup and styling for web implementations.
JavaScript - Adding interactivity and dynamic behavior to web applications.
Adobe Illustrator - Vector graphics creation and illustration for marketing materials.
Adobe Photoshop - Image editing and digital design for web and print.''',
            'strengths': '''- Exceptional creative thinking and visual design skills
- Strong empathy and ability to understand user needs
- Excellent collaboration skills with engineers and product managers
- Detail-oriented with strong attention to visual consistency
- Passionate about user-centered design principles''',
            'weaknesses': '''- Can be overly perfectionistic about design details
- Limited understanding of backend development constraints
- Sometimes struggles with making quick design decisions
- Difficulty with public presentations and pitch communications
- Need to improve knowledge of accessibility standards''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''B.F.A. Graphic Design
Art Institute
Graduated: May 2016
Honors'''
        }
    },
    'marketing': {
        'id': 'marketing',
        'title': 'Marketing Manager',
        'icon': '📢',
        'description': 'For marketing professionals, growth specialists, and business development roles',
        'data': {
            'name': 'Michael Brown',
            'phone': '+1 (555) 567-8901',
            'email': 'michael.brown@email.com',
            'dob': '05/28/1992',
            'linkedin': 'linkedin.com/in/michaelbrown',
            'address': 'Boston, MA 02101, USA',
            'github_link': 'github.com/michaelbrown',
            'role': 'Senior Marketing Manager',
            'summary': 'Results-driven Marketing Manager with 8+ years of experience leading successful go-to-market strategies and driving business growth. Expertise in digital marketing, brand strategy, and data analytics. Proven ability to develop and execute campaigns generating millions in revenue and increasing brand awareness. Strong leadership skills managing cross-functional teams.',
            'experience': '''Senior Marketing Manager at Growth Company (2021-Present)
- Led marketing strategy generating $20M+ in pipeline value
- Increased brand awareness by 150% through integrated marketing campaigns
- Managed marketing budget of $2M+ optimizing spend for maximum ROI
- Led email marketing campaign achieving 35% open rate and 8% CTR

Marketing Manager at Tech Startup (2018-2021)
- Grew user base from 10k to 500k through viral marketing campaigns
- Developed content strategy producing 100+ pieces of content monthly
- Managed social media channels growing followers from 5k to 250k
- Executed advertising campaigns reducing customer acquisition cost by 40%

Marketing Coordinator at Marketing Agency (2016-2018)
- Supported execution of 20+ client marketing campaigns
- Managed social media accounts and created content
- Analyzed campaign performance and provided insights''',
            'internships': '''Marketing Intern at Fortune 500 Company (Summer 2015)
- Developed social media content and campaigns
- Analyzed marketing metrics and provided data-driven insights
- Supported product launch campaign targeting 1M+ audience''',
            'projects': '''Marketing Campaigns:
- Viral TikTok Campaign: 50M+ views, 500k new users in 3 months
- Email Marketing Program: 35% open rate, $2M revenue generated
- Brand Reposition Project: Increased brand recognition by 80%
- Content Marketing Hub: 10k monthly visitors, #1 in SEO rankings''',
            'certifications': '''Google Analytics Certification (2021)
HubSpot Inbound Marketing Certification (2020)
Marketo Certified Expert (2019)
Hootsuite Social Marketing Certification (2018)''',
            'skills': '''Digital Marketing - Omnichannel campaign strategy across email, social, web, and paid advertising channels.
Content Marketing - Creating compelling blog posts, whitepapers, and case studies to drive engagement.
SEO - Keyword research, on-page optimization, and link building for organic search visibility.
Google Analytics - Tracking campaign performance, conversion rates, and user journey analysis.
HubSpot - Marketing automation, lead nurturing, and pipeline management.
Salesforce - CRM management, customer tracking, and sales reporting.
Email Marketing - Segmentation, automation, and personalization for high-engagement campaigns.
Social Media Marketing - Strategy, content creation, and community management across platforms.
A/B Testing - Hypothesis-driven testing to optimize conversion rates and user engagement.
Market Research - Competitive analysis, customer segmentation, and trend identification.''',
            'strengths': '''- Exceptional creativity and ability to develop viral marketing campaigns
- Strong analytical and data-driven approach to marketing optimization
- Excellent storytelling abilities that resonate with target audiences
- Natural leader with strong team management capabilities
- Proven ability to deliver measurable business results and ROI''',
            'weaknesses': '''- Sometimes overcommits to campaigns without proper resource planning
- Can be overly focused on metrics at the expense of brand building
- Limited understanding of technical marketing tools and implementation
- Difficulty delegating tasks to team members
- Need to improve public speaking skills for investor pitches''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''B.S. Business Administration
University
Graduated: May 2016
Concentration: Marketing'''
        }
    },
    'fresher': {
        'id': 'fresher',
        'title': 'Fresher/Graduate',
        'icon': '🎓',
        'description': 'Perfect for fresh graduates and recent college completers',
        'data': {
            'name': 'Priya Sharma',
            'phone': '+1 (555) 678-9012',
            'email': 'priya.sharma@email.com',
            'dob': '06/12/2002',
            'linkedin': 'linkedin.com/in/priyasharma',
            'address': 'Bangalore, KA 560001, India',
            'github_link': 'github.com/priyasharma',
            'role': 'Junior Software Developer',
            'summary': 'Recent Computer Science graduate with strong foundation in full-stack web development, problem-solving skills, and eagerness to learn. Proficient in Python, JavaScript, and Java. Passionate about building scalable applications and contributing to impactful projects. Quick learner with ability to work independently and in team environments.',
            'experience': '''Intern - Software Development at Tech StartUp (Jan 2024 - June 2024)
- Developed REST APIs using Django and PostgreSQL
- Created UI components using React improving user experience
- Fixed bugs and optimized database queries
- Participated in agile development and code review sessions''',
            'internships': '''Web Development Intern at Digital Agency (July 2023 - Dec 2023)
- Built responsive web pages using HTML, CSS, and JavaScript
- Assisted senior developers in implementing client requirements
- Tested and debugged web applications across different browsers
- Learned version control using Git and GitHub

Full-Stack Intern at Software Company (Jan 2023 - June 2023)
- Developed CRUD applications using Node.js and MySQL
- Created database schemas and optimized queries
- Assisted in API development and testing''',
            'projects': '''Capstone Project: E-Commerce Platform
- Built full-stack e-commerce application using React, Node.js, and MongoDB
- Implemented user authentication, product catalog, and shopping cart
- Technologies: JavaScript, REST APIs, Responsive Design
- GitHub: github.com/priyasharma/ecommerce-platform

Class Projects:
- Student Management System (Python, SQLite)
- Chat Application using Socket.io and Node.js
- Personal Portfolio Website (HTML, CSS, JavaScript)''',
            'certifications': '''Oracle Java Programmer Associate (2024)
Google Cloud Fundamentals (2023)
Udemy: The Complete JavaScript Course (2023)
HackerRank: 5-star Problem Solver''',
            'skills': '''Python - Fundamental programming language with object-oriented principles and basic web framework knowledge.
JavaScript - Front-end scripting for interactive web pages and DOM manipulation.
Java - Understanding of object-oriented programming and basic enterprise applications.
React - Building component-based user interfaces with hooks and state management.
Node.js - Server-side JavaScript for building REST APIs and backend services.
HTML5 - Semantic markup and structure for modern web pages.
CSS3 - Responsive styling, flexbox, and grid layouts for mobile-first design.
MySQL - Relational database design, CRUD operations, and basic query optimization.
MongoDB - NoSQL database operations and document-oriented data modeling.
Git - Version control, branching, merging, and collaborative development.
RESTful APIs - Building and consuming HTTP endpoints for data exchange.
Bootstrap - CSS framework for rapid responsive web development.''',
            'strengths': '''- Quick learner with ability to master new technologies rapidly
- Strong problem-solving skills and logical thinking
- Enthusiastic and self-motivated with desire to grow
- Good communication and collaboration skills
- Solid understanding of data structures and algorithms''',
            'weaknesses': '''- Limited professional experience with real-world projects
- Sometimes lack confidence in technical decision-making
- Need to improve code optimization skills
- Limited understanding of system design at scale
- Struggling with advanced database optimization techniques''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''B.Tech. Computer Science
State University of Technology
Graduated: May 2024
GPA: 3.6/4.0
Relevant Coursework: Data Structures, Web Development, Database Systems, Software Engineering, Operating Systems'''
        }
    },
    'student': {
        'id': 'student',
        'title': 'Current Student',
        'icon': '📚',
        'description': 'For college/university students currently studying',
        'data': {
            'name': 'Arjun Patel',
            'phone': '+1 (555) 789-0123',
            'email': 'arjun.patel@university.edu',
            'dob': '03/25/2003',
            'linkedin': 'linkedin.com/in/arjunpatel',
            'address': 'Mumbai, MH 400001, India',
            'github_link': 'github.com/arjunpatel',
            'role': 'Computer Science Student',
            'summary': 'Motivated third-year Computer Science student with strong academic performance and practical coding skills. Experienced in C++, Python, and web technologies. Active participant in coding competitions and college technical clubs. Seeking internship opportunities to apply classroom knowledge and develop professional experience in software development.',
            'experience': '''Class Representative - Computer Science Department (2023-Present)
- Organized coding contests and technical workshops for 100+ students
- Coordinated with faculty and companies for student placements
- Led study groups improving class performance

Coding Tutor - University Peer Tutoring Center (2023-Present)
- Tutored junior students in Data Structures and Algorithms
- Helped 15+ students improve their programming skills
- Conducted weekly problem-solving sessions''',
            'internships': '''Summer Internship - Web Development (May 2023 - July 2023)
- Developed features for web application using HTML, CSS, JavaScript
- Learned agile development practices and team collaboration
- Contributed to codebase with 5 merged pull requests

Part-time Developer - Campus Project (2022-Present)
- Building campus app for student event management
- Technologies: React, Firebase, Mobile-first design''',
            'projects': '''College Projects:
- Database Management System - Designed and implemented using C++ and SQLite, includes CRUD operations
- Chat Application - Real-time messaging using Python and Socket programming
- Weather Forecasting App - REST API integration using JavaScript and public APIs
- Online Judge Platform - Competitive programming platform codebase

Personal Projects:
- DSA Problem Solver - Solutions to 200+ LeetCode problems
- College Companion App - Flutter-based mobile app (In Development)''',
            'certifications': '''AWS Academy Cloud Foundations (2023)
Google Cloud Skills Boost Badges (2023)
LeetCode: 150+ Problems Solved
HackerEarth: Active Participant (Rank: Top 5%)''',
            'skills': '''C++ - Competitive programming and algorithmic problem-solving with strong data structure understanding.
Python - Learning core programming with libraries like NumPy and Pandas for data manipulation.
JavaScript - Building interactive web pages with vanilla JS and learning React framework.
HTML5/CSS3 - Creating semantic web pages with responsive design and modern layouts.
React - Building single-page applications with components and state management.
Node.js - Learning backend development and building simple REST APIs.
MySQL - Database design, relational modeling, and writing SQL queries.
Git - Version control and collaborative development using GitHub.
Data Structures - Strong understanding of arrays, linked lists, trees, and graphs.
Algorithms - Knowledge of sorting, searching, dynamic programming, and optimization techniques.
Object-Oriented Programming - Classes, inheritance, polymorphism, and design principles.''',
            'strengths': '''- Strong foundation in data structures and algorithms
- Quick to grasp new concepts and technologies
- Excellent academic track record (GPA: 3.8/4.0)
- Active in college technical community and events
- Neat and organized code writing habits''',
            'weaknesses': '''- Limited professional work experience
- Less exposure to large-scale system design
- Need to improve project management skills
- Sometimes get overwhelmed with multiple assignments
- Limited experience with DevOps and deployment tools''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''B.Tech. Computer Science and Engineering
Prestigious Engineering College
Currently Pursuing (Expected Graduation: June 2025)
GPA: 3.8/4.0
Relevant Coursework: Data Structures, Algorithms, Database Systems, Web Development, Operating Systems, Computer Networks'''
        }
    },
    'entry_level': {
        'id': 'entry_level',
        'title': 'Entry-Level Professional',
        'icon': '🚀',
        'description': 'For professionals with 1-3 years of experience starting their career',
        'data': {
            'name': 'Vikram Singh',
            'phone': '+1 (555) 890-1234',
            'email': 'vikram.singh@email.com',
            'dob': '08/18/2000',
            'linkedin': 'linkedin.com/in/vikramsingh',
            'address': 'Hyderabad, TG 500001, India',
            'github_link': 'github.com/vikramsingh',
            'role': 'Software Engineer I',
            'summary': 'Dedicated Software Engineer with 2+ years of experience developing web applications and solving complex technical problems. Proficient in full-stack development with expertise in Python and JavaScript. Proven ability to deliver quality code on schedule while collaborating effectively with cross-functional teams. Eager to advance technical skills and take on more challenging projects.',
            'experience': '''Software Engineer - TechCorp Solutions (July 2022 - Present)
- Developed and maintained 5+ microservices using Python and Flask
- Improved API response time by 30% through code optimization
- Implemented automated testing increasing code coverage to 85%
- Collaborated with product team to deliver 8 features on schedule
- Fixed 20+ production bugs and resolved critical issues

Junior Developer - StartUp Inc (June 2021 - June 2022)
- Built React components for customer dashboard used by 10k+ users
- Implemented RESTful APIs using Node.js and Express
- Participated in code reviews improving team code quality
- Documented features and functions for team reference
- Supported deployment and monitoring of applications''',
            'internships': '''Full-Stack Development Intern - Tech Agency (Jan 2021 - May 2021)
- Developed web pages and backend services for client projects
- Fixed bugs and implemented feature requests from clients
- Learned best practices in software development and testing
- Worked with AWS services for deployment and scaling''',
            'projects': '''Current Major Project - Real-time Analytics Platform
- Building scalable analytics dashboard using React and Python
- Implemented data pipeline using Apache Kafka
- Designing database schema for millions of data points
- Technologies: Python, React, PostgreSQL, AWS, Docker

Previous Project - E-learning Platform
- Developed student portal with course management system
- Implemented user authentication and role-based access
- Created admin dashboard for course creation and management
- Result: Platform serves 5000+ students, 95% uptime''',
            'certifications': '''AWS Certified Cloud Practitioner (2023)
Docker Associate Certification (2023)
Udemy: Complete Python Developer Certificate (2021)
DataCamp: Python Programming Track (2021)''',
            'skills': '''Python - Backend development with Flask framework, API design, and database operations.
JavaScript - Full-stack development with React on frontend and Node.js on backend.
React - Building responsive UIs with component composition and state management.
Node.js - Server-side JavaScript development with Express for REST API creation.
Flask - Lightweight Python framework for rapid web application development.
PostgreSQL - Production database management with complex queries and optimization.
MongoDB - NoSQL database operations for flexible document storage.
Docker - Container creation and management for consistent development and deployment.
AWS - Cloud services for hosting, databases, and infrastructure management.
Git - Source control, branching strategies, and collaborative development.
RESTful APIs - API design, documentation, and building scalable endpoints.
Agile/Scrum - Sprint planning, standup participation, and iterative development.''',
            'strengths': '''- Quick problem-solver with ability to debug complex issues
- Good understanding of software development lifecycle
- Strong communication skills with technical and non-technical teams
- Reliable and consistent in delivering assigned work
- Eager to learn and improve technical capabilities''',
            'weaknesses': '''- Limited experience with system design and architecture
- Less exposure to large-scale distributed systems
- Need to improve technical documentation skills
- Sometimes take longer to estimate complex tasks
- Limited experience with CI/CD pipeline setup''',
            'declaration': 'I hereby declare that the information provided in this resume is true and accurate to the best of my knowledge. I have not omitted any material information.',
            'education': '''B.Tech. Information Technology
National Institute of Engineering
Graduated: May 2021
GPA: 3.5/4.0

Additional Certifications:
- Google Cloud Associate Cloud Engineer (In Progress)
- Kubernetes Administrator Certification (Planned)'''
        }
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def login_required(f):
    """
    Decorator to require login for certain routes.
    If user is not logged in, redirect to login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Check if uploaded file type is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_user():
    """Get current logged-in user's info."""
    if 'user_id' in session:
        return get_user_info(session['user_id'])
    return None

# ============================================================================
# ROUTES - Authentication
# ============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page - shows login/signup form on same page.
    Handles both login and signup form submissions.
    """
    if 'user_id' in session:
        return render_template('index.html')
    
    if request.method == 'POST':
        action = request.form.get('action', 'login')
        
        if action == 'login':
            # Handle login
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            
            if not all([email, password]):
                return render_template('index.html', error="Email and password required")
            
            success, user_id, message = login_user(email, password)
            
            if success:
                session['user_id'] = user_id
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                return render_template('index.html', error=message)
        
        elif action == 'signup':
            # Handle signup
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            full_name = request.form.get('full_name', '').strip()
            
            if not all([email, password, full_name]):
                return render_template('index.html', signup_error="All fields are required")
            
            success, message = signup_user(email, password, full_name)
            
            if success:
                return render_template('index.html', success=message + " You can now login!")
            else:
                return render_template('index.html', signup_error=message)
    
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """
    Signup page - create new account.
    GET: Show signup form
    POST: Process signup (create account)
    """
    if request.method == 'POST':
        # Get data from form
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        full_name = request.form.get('full_name', '').strip()
        
        # Validate input
        if not all([email, password, full_name]):
            return render_template('signup.html', error="All fields are required")
        
        # Try to create account
        success, message = signup_user(email, password, full_name)
        
        if success:
            # Account created - redirect to login
            return render_template('signup.html', success=message)
        else:
            # Show error
            return render_template('signup.html', error=message)
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Login page - authenticate user.
    GET: Show login form
    POST: Process login (verify credentials)
    """
    if request.method == 'POST':
        # Get data from form
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validate input
        if not all([email, password]):
            return render_template('login.html', error="Email and password required")
        
        # Try to login
        success, user_id, message = login_user(email, password)
        
        if success:
            # Login successful - create session
            session['user_id'] = user_id
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            # Login failed - show error
            return render_template('login.html', error=message)
    
    return render_template('login.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    Forgot password page. Shows a form to request a password reset link.
    For now this shows a generic success message (no real email sending).
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        if not email:
            return render_template('forgot_password.html', error="Please enter your email address")

        try:
            conn = sqlite3.connect('resume_ai.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            conn.close()

            # NOTE: In production, generate a secure token and send reset email.
            # Here we always show the same generic message for security/privacy.
            message = 'If an account exists for this email, a password reset link has been sent.'
            return render_template('forgot_password.html', success=message)

        except Exception as e:
            return render_template('forgot_password.html', error='Error processing request')

    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    """
    Logout - clear user session.
    """
    session.clear()
    return redirect(url_for('index'))

# ============================================================================
# ROUTES - Main Dashboard
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard - main page after login.
    Shows options to:
    - Upload resume
    - Build resume from scratch
    - Check ATS score
    - Generate keywords
    """
    user_id = session['user_id']
    user_info = get_current_user()
    resumes = get_user_resumes(user_id)
    ats_scores = get_user_ats_scores(user_id)
    
    return render_template(
        'dashboard.html',
        user=user_info,
        resumes=resumes,
        ats_scores=ats_scores
    )

# ============================================================================
# ROUTES - Resume Upload
# ============================================================================

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_resume():
    """
    Upload and parse resume file (PDF/DOCX).
    GET: Show upload form
    POST: Process file upload
    """
    if request.method == 'POST':
        # Check if file was submitted
        if 'file' not in request.files:
            return render_template('upload.html', error="No file provided")
        
        file = request.files['file']
        
        # Check if file has name
        if file.filename == '':
            return render_template('upload.html', error="No file selected")
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return render_template(
                'upload.html',
                error=f"Invalid file type. Allowed: PDF, DOCX, TXT"
            )
        
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text from file
            text, file_type = extract_text_from_file(file_path)
            
            if not text:
                return render_template('upload.html', error="Could not read file")
            
            # Try to extract basic info
            basic_info = extract_basic_resume_data(text)
            
            # Store in database
            user_id = session['user_id']
            success, resume_id = save_resume(
                user_id,
                name=basic_info.get('name', ''),
                role=basic_info.get('role', ''),
                summary=request.form.get('summary', ''),
                experience=request.form.get('experience', ''),
                skills=request.form.get('skills', ''),
                education=request.form.get('education', ''),
                raw_text=text
            )
            
            if success:
                return render_template(
                    'upload.html',
                    success=True,
                    parsed_data=basic_info,
                    resume_id=resume_id
                )
            else:
                return render_template('upload.html', error="Could not save resume")
        
        except Exception as e:
            print(f"Upload error: {traceback.format_exc()}")
            return render_template('upload.html', error=f"Error: {str(e)}")
    
    return render_template('upload.html')

# ============================================================================
# ROUTES - Resume Builder
# ============================================================================

@app.route('/builder/templates', methods=['GET'])
@login_required
def builder_templates():
    """
    Show resume template selection page.
    User selects a template to start building.
    """
    return render_template('builder_templates.html', templates=RESUME_TEMPLATES)

@app.route('/builder/select/<template_id>', methods=['GET'])
@login_required
def builder_select_template(template_id):
    """
    Load visual builder with selected template pre-filled.
    GET: Show visual builder with template data
    """
    if template_id not in RESUME_TEMPLATES:
        return redirect(url_for('builder_templates'))
    
    template = RESUME_TEMPLATES[template_id]
    return render_template('builder_visual.html', template=template, template_data=template['data'])

@app.route('/builder', methods=['GET', 'POST'])
@login_required
def builder():
    """
    Build resume from scratch using a form.
    GET: Show builder form (redirect to templates first)
    POST: Save built resume
    """
    if request.method == 'GET':
        # Redirect to template selection
        return redirect(url_for('builder_templates'))
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        summary = request.form.get('summary', '').strip()
        experience = request.form.get('experience', '').strip()
        skills = request.form.get('skills', '').strip()
        education = request.form.get('education', '').strip()
        
        # Get optional HR fields
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        dob = request.form.get('dob', '').strip()
        linkedin = request.form.get('linkedin', '').strip()
        address = request.form.get('address', '').strip()
        github_link = request.form.get('github_link', '').strip()
        internships = request.form.get('internships', '').strip()
        projects = request.form.get('projects', '').strip()
        certifications = request.form.get('certifications', '').strip()
        strengths = request.form.get('strengths', '').strip()
        weaknesses = request.form.get('weaknesses', '').strip()
        declaration = request.form.get('declaration', '').strip()
        
        # All required fields
        if not all([name, role, summary, experience, skills, education]):
            return render_template('builder_visual.html', error="All required fields must be completed", 
                                 template_data={
                                     'name': name, 'role': role, 'summary': summary,
                                     'experience': experience, 'skills': skills,
                                     'education': education, 'phone': phone, 'email': email,
                                     'dob': dob, 'linkedin': linkedin, 'address': address, 
                                     'github_link': github_link, 'internships': internships,
                                     'projects': projects, 'certifications': certifications,
                                     'strengths': strengths, 'weaknesses': weaknesses, 'declaration': declaration
                                 })
        
        try:
            # Save to database with all fields
            user_id = session['user_id']
            success, resume_id = save_resume(
                user_id, 
                name, role, summary, experience, skills, education,
                raw_text=f"{name}\n{role}\n{summary}\n{experience}\n{internships}\n{projects}\n{certifications}\n{strengths}\n{weaknesses}\n{skills}\n{education}",
                phone=phone,
                email=email,
                dob=dob,
                linkedin=linkedin,
                address=address,
                github_link=github_link,
                internships=internships,
                projects=projects,
                certifications=certifications,
                strengths=strengths,
                weaknesses=weaknesses,
                declaration=declaration
            )
            
            if success:
                return render_template(
                    'builder_success.html',
                    resume_id=resume_id,
                    name=name,
                    role=role
                )
            else:
                return render_template('builder_visual.html', error="Could not save resume",
                                     template_data={
                                         'name': name, 'role': role, 'summary': summary,
                                         'experience': experience, 'skills': skills,
                                         'education': education, 'phone': phone, 'email': email,
                                         'dob': dob, 'linkedin': linkedin, 'address': address, 
                                         'github_link': github_link, 'internships': internships,
                                         'projects': projects, 'certifications': certifications,
                                         'strengths': strengths, 'weaknesses': weaknesses, 'declaration': declaration
                                     })
        
        except Exception as e:
            return render_template('builder_visual.html', error=str(e),
                                 template_data={
                                     'name': name, 'role': role, 'summary': summary,
                                     'experience': experience, 'skills': skills,
                                     'education': education, 'phone': phone, 'email': email,
                                     'dob': dob, 'linkedin': linkedin, 'address': address, 
                                     'github_link': github_link, 'internships': internships,
                                     'projects': projects, 'certifications': certifications,
                                     'strengths': strengths, 'weaknesses': weaknesses, 'declaration': declaration
                                 })
    
    return render_template('builder.html')

# ============================================================================
# ROUTES - ATS Checking
# ============================================================================

@app.route('/ats-score', methods=['GET', 'POST'])
@login_required
def ats_score():
    """
    Check ATS compatibility score.
    GET: Show form to upload resume and enter job description
    POST: Calculate ATS score (supports both database resumes and uploaded files)
    """
    if request.method == 'POST':
        resume_source = request.form.get('resume_source', 'database')
        job_description = request.form.get('job_description', '').strip()
        
        # Job description required
        if not job_description:
            user_id = session['user_id']
            resumes = get_user_resumes(user_id)
            return render_template('ats.html', resumes=resumes, error="Job description required")
        
        resume_text = None
        resume_id = None
        
        try:
            # Get resume text based on source
            if resume_source == 'database':
                resume_id = request.form.get('resume_id')
                if not resume_id:
                    user_id = session['user_id']
                    resumes = get_user_resumes(user_id)
                    return render_template('ats.html', resumes=resumes, error="Please select a resume from your list")
                
                resume_data = get_resume(resume_id)
                if not resume_data:
                    user_id = session['user_id']
                    resumes = get_user_resumes(user_id)
                    return render_template('ats.html', resumes=resumes, error="Resume not found")
                resume_text = resume_data['raw_text']
                
            elif resume_source == 'upload':
                # Handle file upload
                if 'resume_file' not in request.files:
                    user_id = session['user_id']
                    resumes = get_user_resumes(user_id)
                    return render_template('ats.html', resumes=resumes, error="No file selected")
                
                file = request.files['resume_file']
                if file.filename == '':
                    user_id = session['user_id']
                    resumes = get_user_resumes(user_id)
                    return render_template('ats.html', resumes=resumes, error="No file selected")
                
                if not is_allowed_file(file.filename):
                    user_id = session['user_id']
                    resumes = get_user_resumes(user_id)
                    return render_template('ats.html', resumes=resumes, error="Invalid file format. Allowed: PDF, DOC, DOCX, TXT")
                
                # Extract text from uploaded file
                resume_text = extract_text_from_file(file)
                if not resume_text:
                    user_id = session['user_id']
                    resumes = get_user_resumes(user_id)
                    return render_template('ats.html', resumes=resumes, error="Could not extract text from file")
            
            else:
                user_id = session['user_id']
                resumes = get_user_resumes(user_id)
                return render_template('ats.html', resumes=resumes, error="Invalid resume source")
            
            # Perform ATS check
            result = perform_ats_check(resume_text, job_description)
            
            # Save result to database (only if from database resume)
            if resume_source == 'database' and resume_id:
                user_id = session['user_id']
                save_ats_score(
                    user_id,
                    resume_id,
                    job_description,
                    result['score'],
                    str(result['missing_keywords']),
                    result['feedback']
                )
            
            return render_template(
                'ats.html',
                score=result['score'],
                missing_keywords=result['missing_keywords'],
                feedback=result['feedback'],
                skills_found=result['skills_found'],
                structure=result['structure'],
                is_external=resume_source == 'upload'
            )
        
        except Exception as e:
            print(f"ATS Error: {traceback.format_exc()}")
            user_id = session['user_id']
            resumes = get_user_resumes(user_id)
            return render_template('ats.html', resumes=resumes, error=f"Error: {str(e)}")
    
    # GET request - show form with user's resumes
    user_id = session['user_id']
    resumes = get_user_resumes(user_id)
    return render_template('ats.html', resumes=resumes)

# ============================================================================
# ROUTES - Keyword Generator
# ============================================================================

@app.route('/keywords', methods=['GET', 'POST'])
@login_required
def keywords():
    """
    Generate keyword suggestions from job description.
    GET: Show form
    POST: Extract and display keywords
    """
    if request.method == 'POST':
        job_description = request.form.get('job_description', '').strip()
        
        if not job_description:
            return render_template('keywords.html', error="Please enter job description")
        
        try:
            # Extract keywords
            keywords_data = generate_keywords_from_description(job_description)
            
            return render_template(
                'keywords.html',
                keywords=keywords_data,
                job_description=job_description
            )
        
        except Exception as e:
            return render_template('keywords.html', error=str(e))
    
    return render_template('keywords.html')

# ============================================================================
# ROUTES - PDF Download
# ============================================================================

@app.route('/download/<int:resume_id>')
@login_required
def download_resume(resume_id):
    """
    Generate and download resume as PDF.

    This route attempts to render the resume HTML server-side and convert it
    to PDF using WeasyPrint so the downloaded PDF matches the preview's
    HTML/CSS (multi-page, proper colors, list styles, borders, etc.). If
    WeasyPrint is not available, it falls back to redirecting to the client
    preview which uses html2pdf.js.
    """
    try:
        # Get resume from database
        resume_data = get_resume(resume_id)

        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404

        # Check if user owns this resume
        resume_user_id = int(resume_data.get('user_id', 0))
        session_user_id = int(session.get('user_id', 0))

        if resume_user_id != session_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Try server-side HTML -> PDF conversion using WeasyPrint
        try:
            import importlib
            import io

            weasyprint = importlib.import_module('weasyprint')
            HTML = weasyprint.HTML

            # Render the same template used for preview to a HTML string
            resume_data['id'] = resume_id
            rendered = render_template('resume_display.html', resume=resume_data)

            # WeasyPrint needs a base_url to resolve static files (css, images)
            base_url = request.host_url.rstrip('/')

            # Generate PDF bytes in-memory
            pdf_bytes = HTML(string=rendered, base_url=base_url).write_pdf()

            pdf_io = io.BytesIO(pdf_bytes)
            pdf_io.seek(0)

            # Send the generated PDF bytes to the user
            return send_file(pdf_io, as_attachment=True,
                             download_name=f"{resume_data.get('name','resume')}.pdf",
                             mimetype='application/pdf')

        except Exception:
            # If WeasyPrint isn't installed or conversion fails, fall back to client-side
            # preview (html2pdf.js). This ensures existing behavior remains intact.
            print('WeasyPrint not available or conversion failed, falling back to client-side download')
            return redirect(url_for('preview_resume', resume_id=resume_id, download='true'))

    except Exception as e:
        print(f"Download error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/preview/<int:resume_id>')
@login_required
def preview_resume(resume_id):
    """
    Preview a resume before downloading.
    Shows formatted resume content in browser.
    """
    try:
        # Convert resume_id to int to be safe
        resume_id = int(resume_id)
        
        # Get resume from database
        resume_data = get_resume(resume_id)
        
        if not resume_data:
            flash('Resume not found', 'error')
            return redirect(url_for('dashboard'))
        
        # Check if user owns this resume (convert both to int for comparison)
        resume_user_id = int(resume_data.get('user_id', 0))
        session_user_id = int(session.get('user_id', 0))
        
        if resume_user_id != session_user_id:
            flash('Unauthorized access to this resume', 'error')
            return redirect(url_for('dashboard'))
        
        # Add resume_id to data for template
        resume_data['id'] = resume_id
        
        return render_template('resume_preview.html', resume=resume_data)
    
    except Exception as e:
        print(f"Preview error: {traceback.format_exc()}")
        flash(f'Error loading preview', 'error')
        return redirect(url_for('dashboard'))

# ============================================================================
# API ROUTES (JSON responses)
# ============================================================================

@app.route('/api/check-email', methods=['POST'])
def check_email_api():
    """
    Check if email is already registered (for signup validation).
    Returns {'exists': true/false}
    """
    try:
        email = request.json.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'exists': False})
        
        conn = sqlite3.connect('resume_ai.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE LOWER(email) = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        
        exists = result is not None
        return jsonify({'exists': exists})
    
    except Exception as e:
        return jsonify({'exists': False, 'error': str(e)}), 400

@app.route('/api/validate-password', methods=['POST'])
def validate_password():
    """
    Check password strength on frontend.
    """
    from database import validate_password
    password = request.json.get('password', '')
    valid, msg = validate_password(password)
    return jsonify({'valid': valid, 'message': msg})

@app.route('/api/assistant', methods=['POST'])
def assistant():
    """
    AI Assistant Chat Endpoint.
    RESTRICTED: Only logged-in users can access this.
    Receives user questions and returns helpful responses about the app.
    """
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'error': 'Please login to use the AI assistant'
        }), 401
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate response from AI assistant
        response = generate_response(user_message)
        
        return jsonify({
            'success': True,
            'message': response,
            'user_message': user_message
        })
    
    except Exception as e:
        print(f"Assistant error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your request'
        }), 500

# ============================================================================
# OTP-BASED SIGNUP ROUTES
# ============================================================================

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    """
    Send OTP to email or mobile number during signup.
    """
    try:
        data = request.json
        contact = data.get('contact', '').strip()
        contact_type = data.get('contact_type', 'email')  # 'email' or 'mobile'
        full_name = data.get('full_name', '').strip()
        
        if not all([contact, contact_type, full_name]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Validate contact format
        if contact_type == 'email':
            if not contact.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'):
                return jsonify({
                    'success': False,
                    'message': 'Invalid email format'
                }), 400
        else:
            if not contact.match(r'^[\d\s\+\-\(\)]{7,}$'):
                return jsonify({
                    'success': False,
                    'message': 'Invalid mobile number format'
                }), 400
        
        # Check if contact already exists
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        if contact_type == 'email':
            cursor.execute('SELECT id FROM users WHERE email = ?', (contact,))
        else:
            cursor.execute('SELECT id FROM users WHERE mobile_number = ?', (contact,))
        
        if cursor.fetchone():
            conn.close()
            return jsonify({
                'success': False,
                'message': f'This {contact_type} is already registered'
            }), 400
        
        conn.close()
        
        # Generate OTP
        otp_code = generate_otp(length=6)
        
        # Send OTP via email or SMS
        if contact_type == 'email':
            success = send_otp_email(contact, otp_code, full_name)
        else:
            success = send_otp_sms(contact, otp_code, full_name)
        
        if not success:
            return jsonify({
                'success': False,
                'message': f'Failed to send OTP to {contact_type}'
            }), 500
        
        # Note: We don't store password here - it will be stored during OTP verification
        # This is a temporary OTP record
        success, msg = store_otp(contact, contact_type, otp_code, full_name, '')
        
        if success:
            return jsonify({
                'success': True,
                'message': f'OTP sent successfully to {contact_type}'
            })
        else:
            return jsonify({
                'success': False,
                'message': msg
            }), 500
    
    except Exception as e:
        print(f"Send OTP error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/verify-otp-signup', methods=['POST'])
def verify_otp_signup():
    """
    Verify OTP and create user account.
    """
    try:
        data = request.json
        contact = data.get('contact', '').strip()
        contact_type = data.get('contact_type', 'email')
        otp = data.get('otp', '').strip()
        full_name = data.get('full_name', '').strip()
        password = data.get('password', '').strip()
        
        if not all([contact, contact_type, otp, full_name, password]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Verify OTP
        success, stored_full_name, stored_hash, stored_type, msg = verify_otp(contact, otp)
        
        if not success:
            return jsonify({
                'success': False,
                'message': msg
            }), 400
        
        # Hash the password
        from database import hash_password
        password_hash = hash_password(password)
        
        # Create user account
        success, user_id, message = create_user_from_otp(contact, full_name, password_hash, contact_type)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'user_id': user_id
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        print(f"Verify OTP signup error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

if __name__ == '__main__':
    # Initialize database on first run
    init_database()
    
    # Run Flask app
    # debug=True: Auto-reload on code changes, detailed error messages
    # host='0.0.0.0': Accept connections from any IP address
    # port=5000: Run on http://localhost:5000
    print("\n" + "="*60)
    print("Resume AI Builder is starting...")
    print("="*60)
    print("📱 Open your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
