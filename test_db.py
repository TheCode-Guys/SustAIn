# test_db.py
from src.database_manager import save_scrap_item, fetch_available_scraps, claim_scrap_item

def run_local_test():
    print("--- Starting Local Database Test ---")
    
    # 1. Test the WRITE Function (Donation Entry)
    try:
        print("\nTesting save_scrap_item()...")
        save_scrap_item(
            item_name="Intel Core i7 CPU",
            category="Processor",
            weight=0.05,
            damage_state="Functional",
            value_tier="High",
            impact_score=85.50,
            donor_phone="+2348012345678"
        )
        print("Success: Item saved to PostgreSQL scraps table.")
    except Exception as e:
        print(f"Failed to save item: {e}")
        return

    # 2. Test the READ Function (Fetch Available Items)
    print("\nTesting fetch_available_scraps()...")
    items = fetch_available_scraps()
    print(f"Fetched items from database: {items}")
    
    if len(items) == 0:
        print("Error: No items found in database.")
        return
        
    # Grab the ID of the item we just inserted (it's the first element of the last tuple)
    target_item_id = items[-1][0]

    # 3. Test the UPDATE Function & CSV Log Wrapper (Claiming the Item)
    try:
        print(f"\nTesting claim_scrap_item() for Item ID: {target_item_id}...")
        claim_scrap_item(
            item_id=target_item_id,
            claimer_id="220100", # Mock student matric ID
            claimer_intent="Building a laboratory test bench for project work."
        )
        print("Success: Database updated to 'Claimed' and transaction written to history_log.csv.")
    except Exception as e:
        print(f"Failed to claim item: {e}")
        return

    print("\n--- Local Database Test Completed Successfully! ---")

if __name__ == "__main__":
    run_local_test()