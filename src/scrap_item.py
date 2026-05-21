# src/scrap_item.py

class ScrapItem:
    """Base class representing a general E-Waste hardware item."""
    def __init__(self, item_id, item_name, category, weight, damage_state, donor_phone):
        self.id = item_id
        self.item_name = item_name
        self.category = category
        self.weight = float(weight)  # Ensure numeric calculations pass safely
        self.damage_state = damage_state
        self.donor_phone = donor_phone
        self.status = "Available"
        self.claimer_id = ""
        self.claimer_intent = ""

    def get_damage_multiplier(self):
        """Returns a baseline multiplier based on classroom degradation states."""
        state = self.damage_state.lower()
        if "fully functional" in state:
            return 1.5  # High reuse value
        elif "minor repair" in state:
            return 1.0  # Standard refurbishment value
        else:
            return 0.5  # Raw parts/recycling scrap value

    def calculate_impact_score(self):
        """Baseline Sustainability Scoring Formula: Weight * Base Category Factor * Damage State"""
        # Default base factor for general electronics elements
        base_category_factor = 25.0 
        multiplier = self.get_damage_multiplier()
        
        # Core Formula execution
        score = self.weight * base_category_factor * multiplier
        return round(score, 2)


# =====================================================================
# OOP ADVANCED PRINCIPLE: INHERITANCE & POLYMORPHISM
# =====================================================================

class BatteryScrapItem(ScrapItem):
    """Specialized subclass for handling heavy chemical and battery systems."""
    def calculate_impact_score(self):
        """Overrides base formula to include a high environmental toxicity penalty score."""
        battery_toxicity_factor = 45.0  # Higher factor because preventing battery dumping saves more soil/water
        multiplier = self.get_damage_multiplier()
        
        # Batteries get an extra 1.2x impact weight premium due to toxic hazard mitigation
        score = (self.weight * battery_toxicity_factor * multiplier) * 1.2
        return round(score, 2)


class PCBScrapItem(ScrapItem):
    """Specialized subclass for handling circuit boards containing precious gold/copper elements."""
    def calculate_impact_score(self):
        """Overrides base formula to scale based on precious metal recovery index."""
        precious_metal_factor = 35.0
        multiplier = self.get_damage_multiplier()
        return round(self.weight * precious_metal_factor * multiplier, 2)

# ==========================================
# LOCAL STANDALONE TEST RUNNER LOOP
# ==========================================
if __name__ == "__main__":
    print("--- Running Isolated Member 3 OOP Scoring Test ---")
    
    # Test 1: General Scrap Item
    item1 = ScrapItem("001", "Old Keyboard", "Peripherals", 1.2, "Minor Repair", "08012345678")
    print(f"Item 1 Score (General): {item1.calculate_impact_score()}")
    
    # Test 2: Battery Item (Inheritance)
    item2 = BatteryScrapItem("002", "UPS Battery", "Power", 5.0, "Fully Functional", "08098765432")
    print(f"Item 2 Score (Battery): {item2.calculate_impact_score()}")
    
    # Test 3: PCB Item (Inheritance)
    item3 = PCBScrapItem("003", "Motherboard", "Circuit Boards", 0.5, "Damaged", "08000000000")
    print(f"Item 3 Score (PCB): {item3.calculate_impact_score()}")
