# UI/navigation.py
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sys
import os

# Ensure the project root is in the path for modular package discovery
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config as cfg
import UI.components as comp
from src.auth import CSVAuthManager
from src.database_manager import CSVDatabaseManager

# Import modular views from the views package
from UI.views.landing_view import LandingFrame
from UI.views.login_view import LoginFrame
from UI.views.signup_view import SignupFrame
from UI.views.dashboard_view import DashboardFrame
from UI.views.donation_view import DonationFrame
from UI.views.claim_view import ClaimFrame
from UI.views.leaderboard_view import LeaderboardFrame
from UI.views.profile_view import ProfileFrame

class NavigationController(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SustAIn: The Circular Economy Guardian")
        self.geometry("1280x850")
        self.resizable(True, True)
        
        # Load shared application assets for modular views
        try:
            raw_pil = Image.open("images/logo.jpeg")
            # Resize via PIL for the sidebar/small icons
            w, h = raw_pil.size
            small_pil = raw_pil.resize((w//4, h//4), Image.Resampling.LANCZOS)
            self.shared_logo = ImageTk.PhotoImage(small_pil)
        except Exception as e:
            print(f"Error loading shared logo: {e}")
            self.shared_logo = None

        # Initialize core system managers
        self.auth_manager = CSVAuthManager()
        self.db_manager = CSVDatabaseManager()
        
        self.configure(bg=cfg.BG_PRIMARY)
        
        # Central Session State
        self.current_user = {
            "matric_id": "",
            "nickname": "Guest Student",
            "email": ""
        }
        
        # Main Stacking Container
        self.main_container = tk.Frame(self, bg=cfg.BG_PRIMARY)
        self.main_container.pack(fill="both", expand=True)
        
        self.frames = {}
        self.build_all_screens()
        
        # Apply global themes
        comp.configure_treeview_theme()
        
        # Initial Route
        self.show_page("LandingFrame")

    def build_all_screens(self):
        """Iteratively initializes each view class and registers them in the frames map."""
        for PageClass in (LandingFrame, LoginFrame, SignupFrame, DashboardFrame, DonationFrame, ClaimFrame, LeaderboardFrame, ProfileFrame):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def show_page(self, page_name):
        """Switches the top stacked frame and executes its refresh hook."""
        frame = self.frames[page_name]
        if hasattr(frame, "on_render_refresh"):
            frame.on_render_refresh()
        frame.tkraise()

if __name__ == "__main__":
    app = NavigationController()
    app.mainloop()
