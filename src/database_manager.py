# src/database_manager.py
import os
import csv

class CSVDatabaseManager:
    def __init__(self, registry_file="data/waste_registry.csv", users_file="data/pau_users.csv"):
        self.registry_file = registry_file
        self.users_file = users_file
        self.initialize_storage_files()

    def initialize_storage_files(self):
        """Creates the blank data sheets with layout headers if they don't exist on disk."""
        # 1. Hardware Registry Sheet
        if not os.path.exists(self.registry_file):
            with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["ID", "Item Name", "Category", "Weight (kg)", "Condition", "Impact Score", "Status", "Donor Phone", "Claimer ID", "Intended Use"])
        
        # 2. User Credentials Sheet
        if not os.path.exists(self.users_file):
            with open(self.users_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Matric ID", "Email", "Password Hash", "Username"])

    # --- HARDWARE REGISTRY OPERATIONS (WRITE/READ/UPDATE) ---
    def save_new_donation(self, item_name, category, weight, condition, score, donor_phone):
        rows = self.read_all_hardware_records()
        next_id = len(rows) + 1
        new_row = [next_id, item_name, category, weight, condition, score, "Available", donor_phone, "None", "None"]
        
        with open(self.registry_file, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(new_row)
        return next_id

    def read_all_hardware_records(self):
        if not os.path.exists(self.registry_file):
            return []
        records = []
        with open(self.registry_file, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip spreadsheet header line
            for row in reader:
                if row:
                    records.append(row)
        return records

    def update_item_to_claimed(self, item_id, claimer_id, claimer_intent):
        records = self.read_all_hardware_records()
        updated = False
        for row in records:
            if str(row[0]) == str(item_id) and row[6] == "Available":
                row[6] = "Claimed"
                row[8] = str(claimer_id).strip()
                row[9] = str(claimer_intent).strip()
                updated = True
                break
        if updated:
            with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Item Name", "Category", "Weight (kg)", "Condition", "Impact Score", "Status", "Donor Phone", "Claimer ID", "Intended Use"])
                writer.writerows(records)
        return updated

    # --- USER ACCOUNT REGISTRY OPERATIONS ---
    def save_new_user(self, matric_id, email, password_hash, username):
        with open(self.users_file, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([matric_id, email, password_hash, username])

    def read_all_users(self):
        if not os.path.exists(self.users_file):
            return []
        users = []
        with open(self.users_file, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row:
                    users.append(row)
        return users

# ==========================================
# LOCAL STANDALONE TEST RUNNER LOOP
# ==========================================
if __name__ == "__main__":
    print("--- Running Isolated Member 4 100% CSV Storage Test ---")
    db = CSVDatabaseManager(registry_file="test_items.csv", users_file="test_users.csv")
    
    # Test recording a user locally
    db.save_new_user("220101", "test@pau.edu.ng", "scrambled_hash", "Kailo")
    print(f"Verified Users Row Logged: {db.read_all_users()}")
    
    # Clean up test files
    for t_file in ["test_items.csv", "test_users.csv"]:
        if os.path.exists(t_file):
            os.remove(t_file)
    print("Workspace cleaned up perfectly!")