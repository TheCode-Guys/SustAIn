# src/search_filters.py

class MatrixDataFilter:
    @staticmethod
    def apply_inventory_filters(raw_records, category="All", damage_state="All"):
        """
        Filters raw e-waste rows based on specific classification dimensions.
        Expects row schema: [ID, Item Name, Category, Weight, Condition, Score, Status, ...]
        """
        filtered_records = []
        for row in raw_records:
            if not row:
                continue
            
            # Row mapping check coordinates
            match_cat = (category == "All" or str(row[2]).strip() == category)
            match_cond = (damage_state == "All" or str(row[4]).strip() == damage_state)
            
            if match_cat and match_cond:
                filtered_records.append(row)
                
        return filtered_records

    @staticmethod
    def compute_and_sort_leaderboard(raw_records, raw_users):
        """
        Aggregates individual student item contributions and sorts them in descending order.
        Returns a beautifully formatted list of tuples ready for the scoreboard UI grid.
        """
        # Dictionary map structure: { matric_id: [nickname, total_items_count, cumulative_score] }
        standings = {}
        
        # 1. Initialize our matrix map with all registered users
        for user in raw_users:
            if user: # user format: [Matric ID, Email, Password Hash, Nickname]
                standings[user[0]] = [user[3], 0, 0.0]
                
        # 2. Aggregate points from the hardware registry data records
        for item in raw_records:
            if item: # item format: [ID, Name, Cat, Weight, Cond, Score, Status, Donor Phone, Claimer ID, ...]
                # For an e-waste system, points can be tracked via the depositor/donor.
                # If tracing donor by a phone number linkage, we map scores to whoever claims or logs it.
                # To match classroom bounds, we look up the active logged reference (e.g., matching IDs)
                # Let's mock tally by scanning rows where a valid student match occurs
                # For this minimalist model, let's look at the claimer or simulate an owner association:
                owner_id = item[8] 
                if owner_id in standings:
                    standings[owner_id][1] += 1  # Increment items count
                    standings[owner_id][2] += float(item[5])  # Sum up impact score
                    
        # 3. Convert the compiled map into a list of tuples for sorting arrays
        scoreboard_list = []
        for mid, data in standings.items():
            # Only include users who have made active circular contributions
            if data[1] > 0:
                scoreboard_list.append((data[0], mid, f"{data[1]} Items", data[2]))
                
        # 4. Sort the array matrix in descending order targeting index position [3] (the score)
        sorted_list = sorted(scoreboard_list, key=lambda student: student[3], reverse=True)
        
        # 5. Populate and slice the list to return ranked, clean string tuples
        final_rankings = []
        for index, profile in enumerate(sorted_list, start=1):
            rank_suffix = "st" if index == 1 else "nd" if index == 2 else "rd" if index == 3 else "th"
            rank_str = f"{index}{rank_suffix}"
            
            # Format output: (Rank, Nickname, Matric ID, Items Contributed, Total Points String)
            final_rankings.append((rank_str, profile[0], profile[1], profile[2], f"{profile[3]} Points"))
            
        return final_rankings


# ==========================================
# LOCAL STANDALONE TEST RUNNER LOOP
# ==========================================
if __name__ == "__main__":
    # This block allows Member 6 to test their sorting filters independently on their laptop!
    print("--- Running Isolated Member 6 Matrix Filtering & Sorting Test ---")
    
    # Pre-defined mock records simulating what comes out of our database manager
    mock_users = [
        ["220101", "ruth@pau.edu.ng", "hash", "Ruth"],
        ["220102", "archy@pau.edu.ng", "hash", "Archy"],
        ["220105", "kaila@pau.edu.ng", "hash", "Kaila"]
    ]
    
    mock_items = [
        ["1", "Dell Monitor", "Display", "4.5", "65.0", "65.00", "Claimed", "+11", "220101", "Lab"],
        ["2", "Mac Battery", "Battery", "0.4", "45.0", "45.00", "Claimed", "+22", "220102", "Project"],
        ["3", "G Pro Mouse", "Peripherals", "0.1", "25.0", "25.00", "Claimed", "+33", "220101", "Club"]
    ]
    
    # 1. Test Category Filtering
    display_only = MatrixDataFilter.apply_inventory_filters(mock_items, category="Display")
    print(f"Category Filter Target 'Display': Found {len(display_only)} item(s) (Expected: 1)")
    print(f"Filtered Row Data Content:        {display_only[0][1]}\n")
    
    # 2. Test Leaderboard Aggregate Ranking Operations
    leaderboard_standings = MatrixDataFilter.compute_and_sort_leaderboard(mock_items, mock_users)
    print("Calculated Scoreboard Standings:")
    for row in leaderboard_standings:
        print(f"Rank {row[0]}: {row[1]} (Matric: {row[2]}) | {row[3]} -> Total Score: {row[4]}")