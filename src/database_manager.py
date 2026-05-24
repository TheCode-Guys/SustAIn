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

        if not os.path.exists(self.registry_file):
            with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([
                    "id",
                    "item_name",
                    "category",
                    "weight",
                    "damage_state",
                    "impact_score",
                    "status",
                    "image_path",
                    "donor_phone",
                    "donor_email",
                    "pickup_location",
                    "claimer_id",
                    "claimer_intent",
                ])

        if not os.path.exists(self.users_file):
            with open(self.users_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Matric ID", "Email", "Password Hash", "Username"])

    def save_new_donation(self, item_name, category, weight, condition, score, donor_phone, donor_email, pickup_location, image_path="images/default.png"):
        rows = self.read_all_hardware_records()
        max_id = 0
        for r in rows:
            try:
                mid = int(r[0])
                if mid > max_id:
                    max_id = mid
            except (ValueError, IndexError):
                continue

        next_id = max_id + 1
        new_row = [
            next_id,
            item_name,
            category,
            weight,
            condition,
            score,
            "Available",
            image_path,
            donor_phone,
            donor_email,
            pickup_location,
            "None",
            "None",
        ]

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
                next(reader, None)  # Skip spreadsheet header line
                for row in reader:
                    if row:
                        records.append(row)
        except Exception as e:
            print(f"Error reading registry: {e}")
        return records

    def get_all_registry_items_dict(self):
        records = self.read_all_hardware_records()
        keys = [
            "id",
            "item_name",
            "category",
            "weight",
            "damage_state",
            "impact_score",
            "status",
            "image_path",
            "donor_phone",
            "donor_email",
            "pickup_location",
            "claimer_id",
            "claimer_intent",
        ]
        return [dict(zip(keys, row)) for row in records if len(row) >= 7]

    def update_item_to_claimed(self, item_id, claimer_id, claimer_intent):
        records = self.read_all_hardware_records()
        updated = False
        for row in records:
            if len(row) < 7:
                continue
            if str(row[0]) == str(item_id) and row[6] == "Available":
                row[6] = "Claimed"
                # Ensure we have enough columns to update (13 columns now)
                while len(row) < 13:
                    row.append("None")
                row[11] = str(claimer_id).strip()
                row[12] = str(claimer_intent).strip()
                updated = True
                break

        if updated:
            try:
                with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "id",
                        "item_name",
                        "category",
                        "weight",
                        "damage_state",
                        "impact_score",
                        "status",
                        "image_path",
                        "donor_phone",
                        "donor_email",
                        "pickup_location",
                        "claimer_id",
                        "claimer_intent",
                    ])
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
        except Exception:
            continue

    return filtered_objects

import re

def validate_user_registration_data(matric_id, email, nickname, password):
    """
    Validates institutional sign-up data rules.
    Returns a tuple: (is_valid: bool, error_message: str)
    """
    # 1. Check for empty string inputs
    if not all([matric_id.strip(), email.strip(), nickname.strip(), password.strip()]):
        return False, "All registration fields are required!"
        
    # 2. Strict Pan-Atlantic University Matric Number Validation (11 continuous digits)
    if not (matric_id.isdigit() and len(matric_id) == 11):
        return False, "Matric Number must be exactly 11 digits (e.g., 25120112025)."
        
    # 3. Institutional Email Regex Enforcement (@pau.edu.ng)
    email_pattern = r"^[a-zA-Z0-9._%+-]+@pau\.edu\.ng$"
    if not re.match(email_pattern, email.strip().lower()):
        return False, "Must use a valid institutional email ending in @pau.edu.ng"
        
    # 4. Password Security Constraint 
    if len(password) < 6:
        return False, "Password security threshold failed: Must be at least 6 characters long."
        
    return True, "Success"

def validate_scrap_donation_data(name, category, weight_str, donor_phone, donor_email, pickup_location):
    """
    Validates physical material submission data strings.
    Returns a tuple: (is_valid: bool, error_message: str)
    """
    if not name.strip():
        return False, "Hardware Model Description cannot be left blank."
        
    if category == "Select Category" or not category:
        return False, "Please select a valid material category type."
        
    if not donor_phone.strip():
        return False, "Donor Contact Phone Number cannot be left blank."

    if not donor_email.strip():
        return False, "Donor Email Address cannot be left blank."

    email_pattern = r"^[a-zA-Z0-9._%+-]+@pau\.edu\.ng$"
    if not re.match(email_pattern, donor_email.strip().lower()):
        return False, "Must use a valid institutional email ending in @pau.edu.ng for donor contact."

    if not pickup_location.strip():
        return False, "Exact Campus Pickup Location cannot be left blank."

    # Try converting physical net weight string securely 
    try:
        weight = float(weight_str)
        if weight <= 0:
            return False, "Physical weight metric must be a positive number greater than 0 kg."
        if weight > 150:
            return False, "Industrial alert: Asset weight exceeds individual student campus drop-off limits (150kg)."
    except ValueError:
        return False, "Weight format error: Value must be a valid decimal number (e.g., 1.35)."
        
    return True, "Success"


if __name__ == "__main__":
    print("--- Running Isolated Member 4 100% CSV Storage Test ---")
    db = CSVDatabaseManager(registry_file="test_items.csv", users_file="test_users.csv")
    db.save_new_user("220101", "test@pau.edu.ng", "scrambled_hash", "Kailo")
    print(f"Verified Users Row Logged: {db.read_all_users()}")
    for t_file in ["test_items.csv", "test_users.csv"]:
        if os.path.exists(t_file):
            os.remove(t_file)
    print("Workspace cleaned up perfectly!")
