# src/database_manager.py

import os
import csv
from datetime import datetime

DATA_DIR = "data"
DEFAULT_REGISTRY_FILE = os.path.join(DATA_DIR, "waste_registry.csv")
DEFAULT_USERS_FILE = os.path.join(DATA_DIR, "pau_users.csv")
DEFAULT_HISTORY_FILE = os.path.join(DATA_DIR, "history_log.csv")


class CSVDatabaseManager:
    def __init__(self, registry_file=None, users_file=None, history_file=None):
        self.registry_file = registry_file or DEFAULT_REGISTRY_FILE
        self.users_file = users_file or DEFAULT_USERS_FILE
        self.history_file = history_file or DEFAULT_HISTORY_FILE
        self.initialize_storage_files()

    def initialize_storage_files(self):
        """Creates blank storage files with schema headers when they do not exist."""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        if not os.path.exists(self.registry_file):
            with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([
                    "ID",
                    "Item Name",
                    "Category",
                    "Weight (kg)",
                    "Condition",
                    "Impact Score",
                    "Status",
                    "Donor Phone",
                    "Claimer ID",
                    "Intended Use",
                ])

        if not os.path.exists(self.users_file):
            with open(self.users_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([
                    "Matric ID",
                    "Email",
                    "Password Hash",
                    "Username",
                ])

        if not os.path.exists(self.history_file):
            with open(self.history_file, mode="w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([
                    "timestamp",
                    "item_id",
                    "item_name",
                    "claimer_id",
                    "action",
                ])

    def save_new_donation(self, item_name, category, weight, condition, score, donor_phone):
        rows = self.read_all_hardware_records()
        next_id = len(rows) + 1
        new_row = [
            next_id,
            item_name,
            category,
            weight,
            condition,
            score,
            "Available",
            donor_phone,
            "None",
            "None",
        ]

        with open(self.registry_file, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(new_row)

        return next_id

    def save_scrap_item(self, item_id, name, category, weight, condition, score, phone):
        with open(self.registry_file, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                item_id,
                name,
                category,
                weight,
                condition,
                score,
                "Available",
                phone,
                "None",
                "None",
            ])

    def read_all_hardware_records(self):
        if not os.path.exists(self.registry_file):
            return []

        records = []
        with open(self.registry_file, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row:
                    records.append(row)
        return records

    def get_all_registry_items(self):
        items = []
        if not os.path.exists(self.registry_file):
            return items

        with open(self.registry_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(row)
        return items

    def update_item_to_claimed(self, item_id, claimer_id, claimer_intent):
        records = self.read_all_hardware_records()
        updated = False
        item_name = "Unknown Item"

        for row in records:
            if str(row[0]) == str(item_id) and row[6] == "Available":
                row[6] = "Claimed"
                row[8] = str(claimer_id).strip()
                row[9] = str(claimer_intent).strip()
                item_name = row[1]
                updated = True
                break

        if updated:
            with open(self.registry_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID",
                    "Item Name",
                    "Category",
                    "Weight (kg)",
                    "Condition",
                    "Impact Score",
                    "Status",
                    "Donor Phone",
                    "Claimer ID",
                    "Intended Use",
                ])
                writer.writerows(records)

            self.log_transaction_event(item_id, item_name, claimer_id, "CLAIMED")

        return updated

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

    def log_transaction_event(self, item_id, item_name, claimer_id, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.history_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, item_id, item_name, claimer_id, action])

    update_item_status_to_claimed = update_item_to_claimed


if __name__ == "__main__":
    print("--- Running CSV Database Manager sanity check ---")
    db = CSVDatabaseManager(registry_file=os.path.join(DATA_DIR, "test_items.csv"), users_file=os.path.join(DATA_DIR, "test_users.csv"), history_file=os.path.join(DATA_DIR, "test_history.csv"))
    db.save_new_user("220101", "test@pau.edu.ng", "scrambled_hash", "Kailo")
    print(f"Verified Users Row Logged: {db.read_all_users()}")

    db.save_new_donation("Example Item", "Electronics", 1.5, "Good", 42, "08001234567")
    print(f"Registry items: {db.get_all_registry_items()}")

    for t_file in [os.path.join(DATA_DIR, "test_items.csv"), os.path.join(DATA_DIR, "test_users.csv"), os.path.join(DATA_DIR, "test_history.csv")]:
        if os.path.exists(t_file):
            os.remove(t_file)
    print("Temporary test files removed.")
