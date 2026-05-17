# src/auth.py
import hashlib
from src.database_manager import get_db_connection

def hash_password(password):
    """Converts a plain text password into a secure SHA-256 string."""
    # Standard classroom approach to hashing using Python's built-in hashlib
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(matric_id, email, password, nickname):
    """Validates school credentials and inserts a new user into the database."""
    
    # 1. Classroom String Manipulation: Check if the email ends with @pau.edu.ng
    if not email.strip().lower().endswith("@pau.edu.ng"):
        return False, "Access Denied: You must use a valid PAU student email (@pau.edu.ng)."
        
    # 2. Basic Validation: Ensure fields aren't completely blank
    if not matric_id.strip() or not password.strip():
        return False, "Error: Matric ID and Password cannot be empty."
        
    # Hash the password before saving it to follow security rules
    secure_password = hash_password(password)
    
    # 3. Database operation to save the user
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO users (matric_id, email, password_hash, nickname)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (matric_id.strip(), email.strip().lower(), secure_password, nickname.strip()))
        conn.commit()
        
        cursor.close()
        conn.close()
        return True, "Registration successful!"
        
    except Exception as e:
        # Catches cases where matric_id or email already exists (Primary Key / Unique violations)
        return False, "Registration failed: Matric ID or Email already registered."

def login_user(email, password):
    """Checks credentials against database records and returns the user's data if valid."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Target the user row by email
    query = "SELECT matric_id, password_hash, nickname FROM users WHERE email = %s;"
    cursor.execute(query, (email.strip().lower(),))
    user_record = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user_record:
        db_matric_id, db_password_hash, db_nickname = user_record
        
        # Hash the incoming password and compare it to what's saved in the database
        if hash_password(password) == db_password_hash:
            return True, {"matric_id": db_matric_id, "nickname": db_nickname}
            
    return False, "Invalid email or password."