# UI/views/leaderboard_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import config as cfg

class LeaderboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "LeaderboardFrame")
        
        self.user_impact_card = tk.LabelFrame(
            self.scrollable_content, text=" Your Personal Eco-Impact Standings ", 
            font=("Helvetica", 10, "bold"), bg="#F3FAF6", fg=cfg.TEXT_MAIN, padx=20, pady=15, relief="flat"
        )
        self.user_impact_card.pack(fill="x", padx=30, pady=(20, 10))
        self.user_impact_card.columnconfigure((0, 1, 2), weight=1)
        
        self.lbl_user_rank = tk.Label(self.user_impact_card, text="#--", font=("Helvetica", 20, "bold"), fg=cfg.SIDEBAR_LIGHT, bg="#F3FAF6")
        self.lbl_user_rank.grid(row=0, column=0, pady=2)
        tk.Label(self.user_impact_card, text="🏆 Rank", font=("Helvetica", 9), bg="#F3FAF6").grid(row=1, column=0)
        
        self.lbl_user_score = tk.Label(self.user_impact_card, text="0.00 pts", font=("Helvetica", 20, "bold"), fg=cfg.TEXT_MAIN, bg="#F3FAF6")
        self.lbl_user_score.grid(row=0, column=1, pady=2)
        tk.Label(self.user_impact_card, text="✨ Score", font=("Helvetica", 9), bg="#F3FAF6").grid(row=1, column=1)

        self.lbl_user_diversion = tk.Label(self.user_impact_card, text="0.00 kg", font=("Helvetica", 20, "bold"), fg="#b45309", bg="#F3FAF6")
        self.lbl_user_diversion.grid(row=0, column=2, pady=2)
        tk.Label(self.user_impact_card, text="🌱 Waste kg", font=("Helvetica", 9), bg="#F3FAF6").grid(row=1, column=2)

        self.champ_label = tk.Label(self.scrollable_content, text="🥇 Calculating Champion... 🥇", font=("Helvetica", 11, "bold"), fg=cfg.COLOR_AMBER, bg="#fef3c7", pady=12)
        self.champ_label.pack(fill="x", padx=30, pady=15)

        tk.Label(self.scrollable_content, text="Campus Overall Standings League", font=("Helvetica", 14, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=30, pady=(15, 5))
        table_frame = tk.Frame(self.scrollable_content)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(5, 30))
        
        columns = ("rank", "nickname", "items_donated", "diversion_kg", "total_points")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("rank", text="Rank"); self.tree.heading("nickname", text="Student")
        self.tree.heading("items_donated", text="Items"); self.tree.heading("diversion_kg", text="Weight (kg)")
        self.tree.heading("total_points", text="Points")
        self.tree.pack(fill="both", expand=True)

    def on_render_refresh(self):
        for record in self.tree.get_children(): self.tree.delete(record)
        uid = self.controller.current_user.get("matric_id")
        records = self.controller.db_manager.read_all_hardware_records()
        user_stats = {}
        for row in records:
            if len(row) < 9: continue
            donor_id = str(row[8]).strip()
            try:
                w, p = float(row[3]), float(row[5])
            except: continue
            if donor_id not in user_stats: user_stats[donor_id] = {'items': 0, 'w': 0.0, 'p': 0.0}
            user_stats[donor_id]['items'] += 1; user_stats[donor_id]['w'] += w; user_stats[donor_id]['p'] += p
            
        users = {str(u[0]).strip(): str(u[3]).strip() for u in self.controller.db_manager.read_all_users() if len(u) > 3}
        sorted_users = sorted(user_stats.items(), key=lambda x: x[1]['p'], reverse=True)
        
        found = False
        for i, (duid, stats) in enumerate(sorted_users, 1):
            nick = users.get(duid, f"User {duid}")
            self.tree.insert("", "end", values=(f"🏅 #{i}", nick, stats['items'], f"{round(stats['w'], 2)} kg", f"{round(stats['p'], 2)} pts"))
            if duid == uid:
                self.lbl_user_rank.config(text=f"#{i}"); self.lbl_user_score.config(text=f"{round(stats['p'], 2)} pts"); self.lbl_user_diversion.config(text=f"{round(stats['w'], 2)} kg")
                found = True
        if not found:
            self.lbl_user_rank.config(text="Unranked"); self.lbl_user_score.config(text="0.00 pts"); self.lbl_user_diversion.config(text="0.00 kg")
        if sorted_users:
            top_uid, top_stats = sorted_users[0]
            self.champ_label.config(text=f"🥇 Champion: {users.get(top_uid, top_uid)} [{round(top_stats['p'], 2)} Impact Points] 🥇")
