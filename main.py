if __name__ == "__main__":
    print("--- Testing Member 3 OOP Logic & Calculations ---")
    
    # Test 1: General Monitor Item
    item1 = ScrapItem("001", "Dell Monitor 24-inch", "Displays & Screens", 4.5, "Minor Repair Required", "+23480")
    print(f"Item: {item1.item_name} -> Impact Score: {item1.calculate_impact_score()} pts")
    
    # Test 2: Overridden Battery Item
    item2 = BatteryScrapItem("002", "MacBook Air Battery", "Power & Batteries", 0.35, "Fully Functional", "+23481")
    print(f"Item: {item2.item_name} -> Overridden Battery Score: {item2.calculate_impact_score()} pts")
    
    print("-------------------------------------------------")