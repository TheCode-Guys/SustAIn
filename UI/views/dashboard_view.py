# UI/views/dashboard_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import config as cfg

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        # We dynamic import to avoid circular dependency since navigation imports views
        from UI.navigation import setup_sliding_sidebar
        setup_sliding_sidebar(self, "DashboardFrame")
        
        # All visual elements now load seamlessly inside scrollable_content frame
        self.welcome_label = tk.Label(
            self.scrollable_content, text="Welcome back to the Hub", 
            font=("Helvetica", 22, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY
        )
        self.welcome_label.pack(anchor="w", padx=35, pady=(30, 5))
        
        caption = tk.Label(
            self.scrollable_content, text="SustAIn: Protecting our campus ecosystem through circular hardware exchange.", 
            font=("Helvetica", 10), fg=cfg.TEXT_MUTED, bg=cfg.BG_PRIMARY
        )
        caption.pack(anchor="w", padx=35, pady=(0, 25))
        
        scorecard = tk.LabelFrame(
            self.scrollable_content, text=" Your Ecological Impact Summary ", 
            font=("Helvetica", 10, "bold"), bg="#F3FAF6", fg=cfg.TEXT_MAIN, padx=25, pady=20, relief="flat"
        )
        scorecard.pack(fill="x", padx=35, pady=10)
        scorecard.columnconfigure((0, 1), weight=1)
        
        pts_frame = tk.Frame(scorecard, bg="#F3FAF6")
        pts_frame.grid(row=0, column=0, sticky="ew")
        tk.Label(pts_frame, text="✨ Current Score Balance", font=("Helvetica", 10), fg=cfg.TEXT_MUTED, bg="#F3FAF6").pack(anchor="w")
        self.lbl_user_points = tk.Label(pts_frame, text="0.00 pts", font=("Helvetica", 28, "bold"), fg=cfg.SIDEBAR_LIGHT, bg="#F3FAF6")
        self.lbl_user_points.pack(anchor="w", pady=2)
        
        wt_frame = tk.Frame(scorecard, bg="#F3FAF6")
        wt_frame.grid(row=0, column=1, sticky="ew")
        tk.Label(wt_frame, text="🌱 Landfill Pollution Prevented", font=("Helvetica", 10), fg=cfg.TEXT_MUTED, bg="#F3FAF6").pack(anchor="w")
        self.lbl_user_weight = tk.Label(wt_frame, text="0.00 kg", font=("Helvetica", 28, "bold"), fg="#b45309", bg="#F3FAF6")
        self.lbl_user_weight.pack(anchor="w", pady=2)

        tk.Label(self.scrollable_content, text="What would you like to do today?", font=("Helvetica", 12, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=35, pady=(25, 10))
        
        grid_container = tk.Frame(self.scrollable_content, bg=cfg.BG_PRIMARY)
        grid_container.pack(fill="x", padx=35, pady=5)
        grid_container.columnconfigure((0, 1, 2), weight=1)
        
        # Shortcut Card A: Donate
        card_donate = tk.Frame(grid_container, bg="#FFFFFF", highlightbackground="#e2e8f0", highlightthickness=1, padx=20, pady=20)
        card_donate.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        tk.Label(card_donate, text="🔄  Donate Hardware", font=("Helvetica", 13, "bold"), fg=cfg.TEXT_MAIN, bg="#FFFFFF").pack(anchor="w")
        tk.Label(card_donate, text="Log e-waste and clear out storage space.", font=("Helvetica", 9), fg=cfg.TEXT_MUTED, bg="#FFFFFF").pack(anchor="w", pady=(5, 15))
        
        btn_go_donate = tk.Button(
            card_donate, text="Go to Donation Center ➔", font=("Helvetica", 9, "bold"),
            bg=cfg.SIDEBAR_LIGHT, fg="white", bd=0, cursor="hand2", padx=15, pady=6,
            command=lambda: controller.show_page("DonationFrame")
        )
        btn_go_donate.pack(anchor="w")

        # Shortcut Card B: Claim
        card_claim = tk.Frame(grid_container, bg="#FFFFFF", highlightbackground="#e2e8f0", highlightthickness=1, padx=20, pady=20)
        card_claim.grid(row=0, column=1, padx=10, sticky="ew")
        tk.Label(card_claim, text="🔍  Browse Marketplace", font=("Helvetica", 13, "bold"), fg=cfg.TEXT_MAIN, bg="#FFFFFF").pack(anchor="w")
        tk.Label(card_claim, text="Search the collective registry for lab reuse.", font=("Helvetica", 9), fg=cfg.TEXT_MUTED, bg="#FFFFFF").pack(anchor="w", pady=(5, 15))
        
        btn_go_claim = tk.Button(
            card_claim, text="Browse Inventory ➔", font=("Helvetica", 9, "bold"),
            bg=cfg.COLOR_BLUE, fg="white", bd=0, cursor="hand2", padx=15, pady=6,
            command=lambda: controller.show_page("ClaimFrame")
        )
        btn_go_claim.pack(anchor="w")

        # Shortcut Card C: Leaderboard
        card_lead = tk.Frame(grid_container, bg="#FFFFFF", highlightbackground="#e2e8f0", highlightthickness=1, padx=20, pady=20)
        card_lead.grid(row=0, column=2, padx=(10, 0), sticky="ew")
        tk.Label(card_lead, text="🏆  Leaderboard", font=("Helvetica", 13, "bold"), fg=cfg.TEXT_MAIN, bg="#FFFFFF").pack(anchor="w")
        tk.Label(card_lead, text="View campus rankings and standings.", font=("Helvetica", 9), fg=cfg.TEXT_MUTED, bg="#FFFFFF").pack(anchor="w", pady=(5, 15))
        
        btn_go_lead = tk.Button(
            card_lead, text="View Rankings ➔", font=("Helvetica", 9, "bold"),
            bg=cfg.COLOR_AMBER, fg="white", bd=0, cursor="hand2", padx=15, pady=6,
            command=lambda: controller.show_page("LeaderboardFrame")
        )
        btn_go_lead.pack(anchor="w")

    def on_render_refresh(self):
        """Runs automatically when the home screen is raised to inject dynamic user states."""
        user_nick = self.controller.current_user.get("nickname", "Student")
        self.welcome_label.config(text=f"Welcome back to the Circle, {user_nick} 🌿")
        
        # Update Impact Summary Stats from real data
        user_id = self.controller.current_user.get("matric_id")
        records = self.controller.db_manager.read_all_hardware_records()
        total_points = 0.0
        total_weight = 0.0
        for row in records:
            if len(row) > 8 and str(row[8]).strip() == user_id:
                try:
                    total_weight += float(row[3])
                    total_points += float(row[5])
                except: continue
        
        self.lbl_user_points.config(text=f"{round(total_points, 2)} pts")
        self.lbl_user_weight.config(text=f"{round(total_weight, 2)} kg")
