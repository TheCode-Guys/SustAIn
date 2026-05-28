# UI/views/leaderboard_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import config as cfg
from UI.navigation_sidebar import setup_sliding_sidebar

class LeaderboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "LeaderboardFrame")
        
        self.user_impact_card = tk.LabelFrame(
            self.right_workspace, text=" Your Standings ", 
            font=("Helvetica", 10, "bold"), bg="#F3FAF6", fg=cfg.TEXT_MAIN, padx=20, pady=15, relief="flat"
        )
        self.user_impact_card.pack(fill="x", padx=30, pady=(20, 10))
        self.user_impact_card.columnconfigure((0, 1, 2), weight=1)
        
        self.lbl_user_rank = tk.Label(self.user_impact_card, text="#--", font=("Helvetica", 20, "bold"), fg=cfg.SIDEBAR_LIGHT, bg="#F3FAF6")
        self.lbl_user_rank.grid(row=0, column=0, pady=2)
        tk.Label(self.user_impact_card, text="Rank", font=("Helvetica", 9), bg="#F3FAF6").grid(row=1, column=0)
        
        self.lbl_user_score = tk.Label(self.user_impact_card, text="0.00 pts", font=("Helvetica", 20, "bold"), fg=cfg.TEXT_MAIN, bg="#F3FAF6")
        self.lbl_user_score.grid(row=0, column=1, pady=2)
        tk.Label(self.user_impact_card, text="Score", font=("Helvetica", 9), bg="#F3FAF6").grid(row=1, column=1)

        self.lbl_user_diversion = tk.Label(self.user_impact_card, text="0.00 kg", font=("Helvetica", 20, "bold"), fg="#b45309", bg="#F3FAF6")
        self.lbl_user_diversion.grid(row=0, column=2, pady=2)
        tk.Label(self.user_impact_card, text="Waste kg", font=("Helvetica", 9), bg="#F3FAF6").grid(row=1, column=2)

        self.champ_label = tk.Label(self.right_workspace, text="Calculating champion...", font=("Helvetica", 11, "bold"), fg=cfg.COLOR_AMBER, bg="#fef3c7", pady=12)
        self.champ_label.pack(fill="x", padx=30, pady=15)

        tk.Label(self.right_workspace, text="Campus Standings", font=("Helvetica", 14, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=30, pady=(15, 5))
        table_frame = tk.Frame(self.right_workspace)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(5, 30))
        
        columns = ("rank", "nickname", "items_donated", "diversion_kg", "total_points")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("rank", text="Rank"); self.tree.heading("nickname", text="Student")
        self.tree.heading("items_donated", text="Items"); self.tree.heading("diversion_kg", text="Weight (kg)")
        self.tree.heading("total_points", text="Points")
        self.tree.pack(fill="both", expand=True)

    def on_render_refresh(self):
        """Update leaderboard by reading pre-calculated totals from the user database."""
        for record in self.tree.get_children():
            self.tree.delete(record)
            
        current_uid = str(self.controller.current_user.get("matric_id")).strip()
        all_users = self.controller.db_manager.read_all_users()
        
        # We need to count items donated separately if we want that column accurate, 
        # or we can just focus on points/weight which are now in pau_users.
        records = self.controller.db_manager.read_all_hardware_records()
        donation_counts = {}
        for row in records:
            if len(row) > 9:
                email = str(row[9]).strip().lower()
                donation_counts[email] = donation_counts.get(email, 0) + 1

        leaderboard_data = []
        for u in all_users:
            if len(u) >= 6:
                try:
                    matric_id = str(u[0]).strip()
                    email = str(u[1]).strip().lower()
                    nick = str(u[3]).strip()
                    pts = float(u[4])
                    weight = float(u[5])
                    items = donation_counts.get(email, 0)
                    leaderboard_data.append((matric_id, nick, items, weight, pts))
                except: continue
        
        # Sort by points descending
        leaderboard_data.sort(key=lambda x: x[4], reverse=True)
        
        found_current = False
        for i, (mid, nick, items, weight, pts) in enumerate(leaderboard_data, 1):
            self.tree.insert("", "end", values=(f"#{i}", nick, items, f"{round(weight, 2)} kg", f"{round(pts, 2)} pts"))
            
            if mid == current_uid:
                self.lbl_user_rank.config(text=f"#{i}")
                self.lbl_user_score.config(text=f"{round(pts, 2)} pts")
                self.lbl_user_diversion.config(text=f"{round(weight, 2)} kg")
                found_current = True
        
        if not found_current:
            self.lbl_user_rank.config(text="Unranked")
            self.lbl_user_score.config(text="0.00 pts")
            self.lbl_user_diversion.config(text="0.00 kg")

        if leaderboard_data:
            top_nick = leaderboard_data[0][1]
            top_pts = leaderboard_data[0][4]
            self.champ_label.config(text=f"Champion: {top_nick} [{round(top_pts, 2)} pts]")
