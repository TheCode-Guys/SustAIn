# src/csv_manager.py
import os
import csv
from datetime import datetime

# Centralized data file paths
DATA_DIR = "data"
USERS_CSV = os.path.join(DATA_DIR, "pau_users.csv")
REGISTRY_CSV = os.path.join(DATA_DIR, "waste_registry.csv")
HISTORY_CSV = os.path.join(DATA_DIR, "history_log.csv")

def initialize_csv_files():
    """Automatically ensures the data directory and default tracking sheets exist with headers."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    # 1. User Authentication Sheet
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["matric_id", "email", "nickname", "password_hash"])
            # Inject a default seed user for presentation testing safety
            writer.writerow(["220101", "ruth.obama@pau.edu.ng", "Ruth", "pbkdf2_sha256_mock_hash_1"])
            writer.writerow(["220105", "lead.architect@pau.edu.ng", "Lead Architect", "password123"])

    # 2. Centralized Hardware Asset Tracking Registry
    if not os.path.exists(REGISTRY_CSV):
        with open(REGISTRY_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "item_name", "category", "weight", "damage_state", 
                "impact_score", "status", "image_path", "donor_phone", 
                "claimer_id", "claimer_intent"
            ])

    # 3. Transaction History Log Ledger (Audit Trail)
    if not os.path.exists(HISTORY_CSV):
        with open(HISTORY_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "item_id", "item_name", "claimer_id", "action"])

# Initialize immediately upon module import loading
initialize_csv_files()


# =====================================================================
# CORE DATA LAYER TRANSACTION FUNCTIONS
# =====================================================================

def save_new_user(matric_id, email, nickname, password_hash):
    """Appends a freshly verified student account record to the user matrix ledger."""
    with open(USERS_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([matric_id, email, nickname, password_hash])

def get_all_users():
    """Reads and returns a list of dictionary rows representing all registered accounts."""
    users = []
    with open(USERS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users

def save_scrap_item(item_id, name, category, weight, condition, score, phone):
    """Appends a computed scrap item instance payload directly to the central registry sheet."""
    with open(REGISTRY_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            item_id, name, category, weight, condition, 
            score, "Available", "images/uploads/placeholder.jpg", phone, "", ""
        ])

def get_all_registry_items():
    """Extracts all logged circular hardware assets out of the master spreadsheet ledger."""
    items = []
    if not os.path.exists(REGISTRY_CSV):
        return items
    with open(REGISTRY_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)
    return items

def log_transaction_event(item_id, item_name, claimer_id, action):
    """Creates a timestamped forensic entry log row into the system audit ledger."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, item_id, item_name, claimer_id, action])

def update_item_status_to_claimed(item_id, claimer_id, claimer_intent):
    """Locates an active hardware record row and safely shifts its operational flags to claimed."""
    rows = []
    updated = False
    target_item_name = "Unknown Item"
    
    # Read existing entries into memory
    with open(REGISTRY_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows.append(headers)
        
        # Locate correct index positions based on structural schema headers
        id_idx = headers.index("id")
        status_idx = headers.index("status")
        claimer_idx = headers.index("claimer_id")
        intent_idx = headers.index("claimer_intent")
        name_idx = headers.index("item_name")
        
        for row in reader:
            if row[id_idx] == str(item_id) and row[status_idx] == "Available":
                row[status_idx] = "Claimed"
                row[claimer_idx] = claimer_id
                row[intent_idx] = claimer_intent
                target_item_name = row[name_idx]
                updated = True
            rows.append(row)
            
    # Atomic write-back operation sequence rewrite
    if updated:
        with open(REGISTRY_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        # Simultaneously punch this event straight into our system audit trail ledger
        log_transaction_event(item_id, target_item_name, claimer_id, "CLAIMED")
        return True
    return False