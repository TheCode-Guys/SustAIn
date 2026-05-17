# src/database_manager.py
import psycopg2
import csv
from datetime import datetime

# Helper function to easily grab a classroom-level connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="sustain_db",
        user="postgres",
        password="your_password" # Every teammate changes this to their local database password
    )

# 1. WRITE FUNCTION (Donation Entry)
def save_scrap_item(item_name, category, weight, damage_state, value_tier, impact_score, donor_phone):
    """Inserts a newly donated item into the PostgreSQL scraps table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO scraps (item_name, category, weight, damage_state, value_tier, impact_score, donor_phone, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Available');
    """
    
    cursor.execute(query, (item_name, category, weight, damage_state, value_tier, impact_score, donor_phone))
    conn.commit()
    
    cursor.close()
    conn.close()

# 2. READ FUNCTION (Dashboard & Filter View)
def fetch_available_scraps():
    """Fetches all hardware items that are still marked as 'Available'."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT id, item_name, category, weight, damage_state, value_tier, impact_score FROM scraps WHERE status = 'Available';"
    cursor.execute(query)
    records = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return records

# 3. UPDATE FUNCTION & CSV LOG WRAPPER (The Claiming Process)
def claim_scrap_item(item_id, claimer_id, claimer_intent):
    """Updates item status to Claimed in Postgres and appends a transaction log entry to history_log.csv."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update the database record
    query = """
        UPDATE scraps 
        SET status = 'Claimed', claimer_id = %s, claimer_intent = %s 
        WHERE id = %s;
    """
    cursor.execute(query, (claimer_id, claimer_intent, item_id))
    conn.commit()
    
    # Fetch details of the claimed item to log into the CSV file
    cursor.execute("SELECT item_name, category, impact_score FROM scraps WHERE id = %s;", (item_id,))
    item_details = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    # Append transaction info to history_log.csv to satisfy course text file requirements
    if item_details:
        item_name, category, impact_score = item_details
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("history_log.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, claimer_id, item_name, category, impact_score, "CLAIMED"])