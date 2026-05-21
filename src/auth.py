# src/auth.py
import hashlib
import os
import sys

# Ensure the project root is in the path for standalone execution
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database_manager import CSVDatabaseManager

class CSVAuthManager:
    def __init__(self):
        self.db = CSVDatabaseManager()

    def register_student(self, matric_id, email, password, username):
        email = str(email).strip().lower()
        if not email.endswith("@pau.edu.ng"):
            return False, "Registration restricted to valid @pau.edu.ng domains." 
            
        # Scan CSV array to ensure no duplicates exist [cite: 15]
        for user in self.db.read_all_users():
            if user[0] == str(matric_id) or user[1] == email:
                return False, "Matric ID or Email is already registered."
                
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() 
        self.db.save_new_user(matric_id, email, hashed_password, username)
        return True, "Account registered successfully in local CSV!"

    def authenticate_student(self, email, password):
        email = str(email).strip().lower()
        hashed_input = hashlib.sha256(password.encode('utf-8')).hexdigest() 
        
        for user in self.db.read_all_users():
            # user format: [0]=Matric ID, [1]=Email, [2]=Password Hash, [3]=Username
            if user[1] == email and user[2] == hashed_input:
                return True, user[3]  # Return true along with their Username [cite: 15]
        return False, "Invalid institutional email or password." 

# ==========================================
# LOCAL STANDALONE TEST RUNNER LOOP
# ==========================================
if __name__ == "__main__":
    print("--- Running Isolated Member 5 Authentication Test ---")
    auth = CSVAuthManager()
    
    # Test 1: Invalid Domain
    success, msg = auth.register_student("220101", "test@gmail.com", "pass", "User")
    print(f"Test 1 (Invalid Domain): {msg}")
    
    # Test 2: Valid PAU Domain
    success, msg = auth.register_student("220102", "student@pau.edu.ng", "secure123", "PauStudent")
    print(f"Test 2 (Valid Registration): {msg}")
    
    # Test 3: Authentication
    success, username = auth.authenticate_student("student@pau.edu.ng", "secure123")
    print(f"Test 3 (Authentication): Success={success}, Username={username}")
    
    # Cleanup
    if os.path.exists("pau_users.csv"):
        os.remove("pau_users.csv")
    print("Cleanup Complete!")
