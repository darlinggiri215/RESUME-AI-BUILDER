"""
DATABASE.PY - User and Resume Data Management
============================================

This file handles all database operations using SQLite.
It manages:
- User accounts and authentication
- Storing parsed resume data
- Storing ATS scores and results
- OTP verification for email/mobile signup
"""

import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
import random
import string

DB_NAME = 'resume_ai.db'

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """
    Initialize the SQLite database with required tables.
    Run this ONCE when you first start the app.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Users table - stores user login information
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        mobile_number TEXT UNIQUE,
        contact_type TEXT DEFAULT 'email',
        is_verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Resumes table - stores parsed resume data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT,
        phone TEXT,
        email TEXT,
        dob TEXT,
        linkedin TEXT,
        address TEXT,
        github_link TEXT,
        role TEXT,
        summary TEXT,
        experience TEXT,
        internships TEXT,
        projects TEXT,
        certifications TEXT,
        skills TEXT,
        strengths TEXT,
        weaknesses TEXT,
        declaration TEXT,
        education TEXT,
        raw_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # OTP verification table - stores OTP records for email/mobile verification
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS otp_verification (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact TEXT NOT NULL,
        contact_type TEXT NOT NULL,
        otp_code TEXT NOT NULL,
        full_name TEXT,
        password_hash TEXT,
        attempts INTEGER DEFAULT 0,
        max_attempts INTEGER DEFAULT 5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP
    )
    ''')
    
    # Add missing columns to existing users table (migration)
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN mobile_number TEXT UNIQUE DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN contact_type TEXT DEFAULT "email"')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0')
    except:
        pass
    
    # Add missing columns to existing resumes table (migration)
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN phone TEXT DEFAULT ""')
    except:
        pass  # Column already exists
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN email TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN dob TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN linkedin TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN address TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN github_link TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN internships TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN projects TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN certifications TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN strengths TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN weaknesses TEXT DEFAULT ""')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE resumes ADD COLUMN declaration TEXT DEFAULT ""')
    except:
        pass
    
    # ATS Scores table - stores ATS checking results
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ats_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_id INTEGER,
        job_description TEXT,
        ats_score FLOAT,
        missing_keywords TEXT,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (resume_id) REFERENCES resumes(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully!")

# ============================================================================
# PASSWORD VALIDATION
# ============================================================================

def validate_password(password):
    """
    Check if password meets requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 special character
    - At least 2 numbers
    
    Returns: (is_valid, error_message)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least 1 uppercase letter")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        errors.append("Password must contain at least 1 special character (!@#$%^&* etc.)")
    
    # Count numbers
    if len(re.findall(r'\d', password)) < 2:
        errors.append("Password must contain at least 2 numbers")
    
    if errors:
        return False, " | ".join(errors)
    
    return True, "Password is valid"

# ============================================================================
# PASSWORD HASHING
# ============================================================================

def hash_password(password):
    """
    Convert plain text password to hash using SHA256.
    This way, even if database is stolen, passwords are protected.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, password_hash):
    """
    Check if plain password matches the stored hash.
    """
    return hash_password(plain_password) == password_hash

# ============================================================================
# USER MANAGEMENT
# ============================================================================

def signup_user(email, password, full_name):
    """
    Create a new user account.
    
    Args:
        email: User's email (username)
        password: Plain text password (will be hashed)
        full_name: User's full name
    
    Returns:
        (success, message)
    """
    # Validate password
    valid, msg = validate_password(password)
    if not valid:
        return False, msg
    
    # Validate email format
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return False, "Invalid email format"
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Hash password before storing
        password_hash = hash_password(password)
        
        cursor.execute('''
        INSERT INTO users (email, password_hash, full_name)
        VALUES (?, ?, ?)
        ''', (email, password_hash, full_name))
        
        conn.commit()
        conn.close()
        
        return True, "Account created successfully!"
    
    except sqlite3.IntegrityError:
        return False, "Email already registered. Try logging in!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def login_user(email, password):
    """
    Verify user login credentials.
    
    Args:
        email: User's email
        password: Plain text password
    
    Returns:
        (success, user_id, message)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False, None, "Email not found"
        
        user_id, stored_hash = result
        
        if verify_password(password, stored_hash):
            return True, user_id, "Login successful!"
        else:
            return False, None, "Incorrect password"
    
    except Exception as e:
        return False, None, f"Error: {str(e)}"

def get_user_info(user_id):
    """Get user's full name and email."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT email, full_name FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"email": result[0], "full_name": result[1]}
    return None

# ============================================================================
# RESUME MANAGEMENT
# ============================================================================

def save_resume(user_id, name, role, summary, experience, skills, education, raw_text, 
                phone='', email='', dob='', linkedin='', internships='', projects='', certifications='',
                address='', github_link='', strengths='', weaknesses='', declaration=''):
    """
    Save parsed resume data to database with all HR fields.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO resumes (user_id, name, phone, email, dob, linkedin, address, github_link, role, summary, experience, internships, projects, certifications, skills, strengths, weaknesses, declaration, education, raw_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name, phone, email, dob, linkedin, address, github_link, role, summary, experience, internships, projects, certifications, skills, strengths, weaknesses, declaration, education, raw_text))
        
        conn.commit()
        resume_id = cursor.lastrowid
        conn.close()
        
        return True, resume_id
    
    except Exception as e:
        return False, str(e)

def get_user_resumes(user_id):
    """Get all resumes for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, name, role, created_at FROM resumes 
    WHERE user_id = ? 
    ORDER BY created_at DESC
    ''', (user_id,))
    resumes = cursor.fetchall()
    conn.close()
    
    return [{"id": r[0], "name": r[1], "role": r[2], "created_at": r[3]} for r in resumes]

def get_resume(resume_id):
    """Get specific resume details."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # Return results as dictionaries
        cursor = conn.cursor()
        
        # Fetch all columns from the resume
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Convert to dictionary
            resume_data = dict(result)
            # Ensure all expected fields exist with defaults
            expected_fields = ['id', 'user_id', 'name', 'phone', 'email', 'dob', 'linkedin', 
                             'address', 'github_link', 'role', 'summary', 'experience', 
                             'internships', 'projects', 'certifications', 'skills', 
                             'strengths', 'weaknesses', 'declaration', 'education', 'raw_text']
            
            for field in expected_fields:
                if field not in resume_data:
                    resume_data[field] = ''
            
            return resume_data
        return None
    except Exception as e:
        print(f"Error in get_resume: {str(e)}")
        return None

# ============================================================================
# ATS SCORE MANAGEMENT
# ============================================================================

def save_ats_score(user_id, resume_id, job_description, ats_score, missing_keywords, feedback):
    """
    Save ATS check results to database.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO ats_scores (user_id, resume_id, job_description, ats_score, missing_keywords, feedback)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, resume_id, job_description, ats_score, missing_keywords, feedback))
        
        conn.commit()
        score_id = cursor.lastrowid
        conn.close()
        
        return True, score_id
    
    except Exception as e:
        return False, str(e)

def get_user_ats_scores(user_id):
    """Get all ATS scores for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, ats_score, created_at FROM ats_scores 
    WHERE user_id = ? 
    ORDER BY created_at DESC
    LIMIT 5
    ''', (user_id,))
    scores = cursor.fetchall()
    conn.close()
    
    return [{"id": s[0], "score": s[1], "created_at": s[2]} for s in scores]

# ============================================================================
# OTP VERIFICATION
# ============================================================================

def generate_otp(length=6):
    """
    Generate a random OTP code.
    """
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp_code, full_name):
    """
    Send OTP via email using Flask-Mail.
    For now, just print to console for testing.
    In production, configure Flask-Mail properly.
    """
    try:
        print(f"\n{'='*60}")
        print(f"📧 OTP EMAIL SENT")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Name: {full_name}")
        print(f"OTP Code: {otp_code}")
        print(f"{'='*60}\n")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_otp_sms(mobile_number, otp_code, full_name):
    """
    Send OTP via SMS using Twilio.
    For now, just print to console for testing.
    In production, configure Twilio credentials.
    """
    try:
        print(f"\n{'='*60}")
        print(f"📱 OTP SMS SENT")
        print(f"{'='*60}")
        print(f"To: {mobile_number}")
        print(f"Name: {full_name}")
        print(f"OTP Code: {otp_code}")
        print(f"{'='*60}\n")
        return True
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False

def store_otp(contact, contact_type, otp_code, full_name, password_hash):
    """
    Store OTP in database for verification.
    
    Args:
        contact: Email or mobile number
        contact_type: 'email' or 'mobile'
        otp_code: Generated OTP code
        full_name: User's full name
        password_hash: Hashed password
    
    Returns:
        (success, message)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Delete old OTP records for this contact (if any)
        cursor.execute('DELETE FROM otp_verification WHERE contact = ?', (contact,))
        
        # Calculate expiration time (10 minutes from now)
        expires_at = datetime.now() + timedelta(minutes=10)
        
        cursor.execute('''
        INSERT INTO otp_verification (contact, contact_type, otp_code, full_name, password_hash, expires_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (contact, contact_type, otp_code, full_name, password_hash, expires_at))
        
        conn.commit()
        conn.close()
        
        return True, "OTP stored successfully"
    
    except Exception as e:
        return False, f"Error storing OTP: {str(e)}"

def verify_otp(contact, otp_code):
    """
    Verify OTP code for a contact.
    
    Args:
        contact: Email or mobile number
        otp_code: OTP code to verify
    
    Returns:
        (success, full_name, password_hash, contact_type, message)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT full_name, password_hash, contact_type, attempts, max_attempts, expires_at
        FROM otp_verification 
        WHERE contact = ? AND otp_code = ?
        ''', (contact, otp_code))
        
        result = cursor.fetchone()
        
        if not result:
            # Increment attempts for wrong OTP
            cursor.execute('''
            UPDATE otp_verification SET attempts = attempts + 1 
            WHERE contact = ?
            ''', (contact,))
            conn.commit()
            conn.close()
            return False, None, None, None, "Invalid OTP code"
        
        full_name, password_hash, contact_type, attempts, max_attempts, expires_at = result
        
        # Check if OTP has expired
        if datetime.fromisoformat(expires_at) < datetime.now():
            conn.close()
            return False, None, None, None, "OTP has expired. Please request a new one."
        
        # Check attempt limit
        if attempts >= max_attempts:
            conn.close()
            return False, None, None, None, "Too many attempts. Please request a new OTP."
        
        # OTP is valid - delete it after successful verification
        cursor.execute('DELETE FROM otp_verification WHERE contact = ?', (contact,))
        conn.commit()
        conn.close()
        
        return True, full_name, password_hash, contact_type, "OTP verified successfully"
    
    except Exception as e:
        return False, None, None, None, f"Error: {str(e)}"

def create_user_from_otp(contact, full_name, password_hash, contact_type):
    """
    Create user account after OTP verification.
    
    Args:
        contact: Email or mobile number
        full_name: User's full name
        password_hash: Hashed password
        contact_type: 'email' or 'mobile'
    
    Returns:
        (success, user_id, message)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        if contact_type == 'email':
            cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, contact_type, is_verified)
            VALUES (?, ?, ?, ?, 1)
            ''', (contact, password_hash, full_name, contact_type))
        else:  # mobile
            cursor.execute('''
            INSERT INTO users (mobile_number, password_hash, full_name, contact_type, is_verified)
            VALUES (?, ?, ?, ?, 1)
            ''', (contact, password_hash, full_name, contact_type))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return True, user_id, "Account created successfully!"
    
    except sqlite3.IntegrityError:
        return False, None, "This email/mobile is already registered. Please login!"
    except Exception as e:
        return False, None, f"Error: {str(e)}"

# ============================================================================
# Run this once to initialize the database
# ============================================================================

if __name__ == "__main__":
    init_database()
