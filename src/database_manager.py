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
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # 1. Hardware Registry Sheet (11 Columns)
        if not os.path.exists(self.registry_file):
            with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["id", "item_name", "category", "weight", "damage_state", "impact_score", "status", "image_path", "donor_phone", "claimer_id", "claimer_intent"])
        
        # 2. User Credentials Sheet
        if not os.path.exists(self.users_file):
            with open(self.users_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Matric ID", "Email", "Password Hash", "Username"])

    def save_new_donation(self, item_name, category, weight, condition, score, donor_phone, image_path="images/default.png"):
        rows = self.read_all_hardware_records()
        max_id = 0
        for r in rows:
            try:
                mid = int(r[0])
                if mid > max_id: max_id = mid
            except: continue
        next_id = max_id + 1
        
        new_row = [next_id, item_name, category, weight, condition, score, "Available", image_path, donor_phone, "None", "None"]
        
        with open(self.registry_file, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(new_row)
        return next_id

    def read_all_hardware_records(self):
        if not os.path.exists(self.registry_file):
            return []
        records = []
        try:
            with open(self.registry_file, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if row:
                        records.append(row)
        except Exception as e:
            print(f"Error reading registry: {e}")
        return records

    def get_all_registry_items_dict(self):
        records = self.read_all_hardware_records()
        keys = ["id", "item_name", "category", "weight", "damage_state", "score", "status", "image_path", "donor_phone", "claimer_id", "claimer_intent"]
        return [dict(zip(keys, row)) for row in records if len(row) >= 7]

    def update_item_to_claimed(self, item_id, claimer_id, claimer_intent):
        records = self.read_all_hardware_records()
        updated = False
        for row in records:
            if len(row) < 7: continue
            if str(row[0]) == str(item_id) and row[6] == "Available":
                row[6] = "Claimed"
                # Ensure we have enough columns to update
                while len(row) < 11: row.append("None")
                row[9] = str(claimer_id).strip()
                row[10] = str(claimer_intent).strip()
                updated = True
                break
        if updated:
            try:
                with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "item_name", "category", "weight", "damage_state", "impact_score", "status", "image_path", "donor_phone", "claimer_id", "claimer_intent"])
                    writer.writerows(records)
            except Exception as e:
                print(f"Error saving registry update: {e}")
                return False
        return updated

    def save_new_user(self, matric_id, email, password_hash, username):
        try:
            with open(self.users_file, mode="a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([matric_id, email, password_hash, username])
        except Exception as e:
            print(f"Error saving user: {e}")

    def read_all_users(self):
        if not os.path.exists(self.users_file):
            return []
        users = []
        try:
            with open(self.users_file, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row:
                        users.append(row)
        except Exception as e:
            print(f"Error reading users: {e}")
        return users

def query_and_filter_registry(search_query="", category_filter="All Categories"):
    from src.scrap_item import scrap_item_factory
    
    db = CSVDatabaseManager()
    all_raw_items = db.get_all_registry_items_dict()
    
    filtered_objects = []
    
    for row in all_raw_items:
        if row.get("status") != "Available":
            continue
            
        item_category = row.get("category", "")
        if category_filter != "All Categories" and item_category != category_filter:
            continue
            
        item_name = row.get("item_name", "").lower()
        if search_query and search_query.lower() not in item_name:
            continue
            
        try:
            item_obj = scrap_item_factory(row)
            filtered_objects.append(item_obj)
        except:
            continue
            
    return filtered_objects

if __name__ == "__main__":
    print("--- Running Isolated Member 4 100% CSV Storage Test ---")
    db = CSVDatabaseManager(registry_file="test_items.csv", users_file="test_users.csv")
    db.save_new_user("220101", "test@pau.edu.ng", "scrambled_hash", "Kailo")
    print(f"Verified Users Row Logged: {db.read_all_users()}")
    for t_file in ["test_items.csv", "test_users.csv"]:
        if os.path.exists(t_file):
            os.remove(t_file)
    print("Workspace cleaned up perfectly!")
