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

    # src/scrap_item.py (Member 3 updates the calculation logic)

    def calculate_impact_score(self):
        """
        ALGORITHMIC PARADIGM: Automatically computes the precise ecological 
        impact score using physical weight and localized condition multipliers.
        """
        # 1. Establish the baseline material weight factor (e.g., 25 pts per kg)
        base_points = float(self.weight) * 25.0
        
        # 2. Extract and evaluate the damage state modifier context
        condition = str(self.damage_state).strip()
        
        # Condition Multiplier Matrix mapping your data row values
        if condition == "Fully Functional":
            multiplier = 1.5  # High priority reuse asset bonus
        elif condition == "Minor Repair Required":
            multiplier = 1.0  # Standard baseline weight
        elif condition == "Scrap / Raw Parts":
            multiplier = 0.5  # Degraded raw material penalty
        else:
            multiplier = 1.0  # Safe default fallback
            
        # 3. Compute the final gamified ecological point metric
        final_score = base_points * multiplier
        return round(final_score, 2)


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
# ECO TIER MANAGEMENT LOGIC
# ==========================================
class EcoTierManager:
    @staticmethod
    def determine_tier_details(points):
        if points > 500:
            return "Eco-Titan", "👑", "#b91c1c"
        elif points > 200:
            return "Green Guardian", "🌱", "#31805B"
        else:
            return "Active Contributor", "⭐", "#1d4ed8"

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

# src/scrap_item.py (Append this function to the bottom of the file)

def scrap_item_factory(row_dict):
    """
    DESIGN PATTERN: Factory Method.
    Takes a flat dictionary row from the CSV file and instantiates the 
    correct polymorphic OOP class type with calculated impact scores.
    """
    category = row_dict.get("category", "")
    
    # Safely extract attributes from the data row payload
    item_id = row_dict.get("id")
    name = row_dict.get("item_name")
    weight = row_dict.get("weight", 0.0)
    condition = row_dict.get("damage_state")
    phone = row_dict.get("donor_phone", "")
    
    # OOP Polymorphic routing choice matrix
    if "Battery" in category:
        item_obj = BatteryScrapItem(item_id, name, category, weight, condition, phone)
    elif "Circuit" in category or "PCB" in category:
        item_obj = PCBScrapItem(item_id, name, category, weight, condition, phone)
    else:
        item_obj = ScrapItem(item_id, name, category, weight, condition, phone)
        
    # Re-sync database flags to runtime object properties
    item_obj.status = row_dict.get("status", "Available")
    item_obj.claimer_id = row_dict.get("claimer_id", "")
    item_obj.claimer_intent = row_dict.get("claimer_intent", "")
    
    return item_obj
# src/scrap_item.py (Member 3 appends this to the bottom of the file)

class EcoTierManager:
    """Manages the gamified achievement ranking tiers based on cumulative impact points."""
    
    @staticmethod
    def determine_tier_details(total_points):
        """
        Evaluates point boundaries and returns a tuple containing:
        (Tier Name String, Graphic Badge Symbol, UI Hex Color Highlight Swatch)
        """
        points = float(total_points)
        
        if points >= 500:
            return "Sustainability Titan", "👑", "#b45309"      # Rich Amber Highlight
        elif points >= 250:
            return "Circular Guardian", "🛡️", "#31805B"     # Signature Eco Green
        elif points >= 100:
            return "E-Waste Crusader", "⚡", "#1d4ed8"      # Active Brand Blue
        elif points >= 30:
            return "Eco Innovator", "🌱", "#113E38"         # Deep Forest Green
        else:
            return "Green Novice", "🥚", "#64748b"          # Slate Gray Baseline