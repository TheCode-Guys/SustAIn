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

def setup_sliding_sidebar(frame_instance, active_page_name):
    """
    Exported utility function to inject the responsive, collapsible 
    sliding navigation sidebar onto any target sub-view frame.
    """
    controller = frame_instance.controller
    
    # 1. Outer Layout Allocation Layer
    frame_instance.sidebar_state = True  # Tracks visibility state: True = Visible, False = Hidden
    
    # This is the actual sidebar canvas frame
    frame_instance.nav_sidebar = tk.Frame(frame_instance, bg=cfg.SIDEBAR_LIGHT, width=240)
    frame_instance.nav_sidebar.pack(side="left", fill="y")
    frame_instance.nav_sidebar.pack_propagate(False)
    
    # This is the dynamic workspace content canvas on the right side
    frame_instance.right_workspace = tk.Frame(frame_instance, bg=cfg.BG_PRIMARY)
    frame_instance.right_workspace.pack(side="left", fill="both", expand=True)
    
    # 2. Add Toggle Controller Button right inside the workspace upper corner
    toggle_bar = tk.Frame(frame_instance.right_workspace, bg=cfg.BG_PRIMARY)
    toggle_bar.pack(fill="x", anchor="n", padx=15, pady=10)
    
    def toggle_sidebar_action():
        if frame_instance.sidebar_state:
            frame_instance.nav_sidebar.pack_forget()
            toggle_btn.config(text="Show Sidebar", bg=cfg.SIDEBAR_LIGHT)
        else:
            # To ensure the sidebar stays on the left of the workspace:
            frame_instance.right_workspace.pack_forget()
            frame_instance.nav_sidebar.pack(side="left", fill="y")
            frame_instance.right_workspace.pack(side="left", fill="both", expand=True)
            toggle_btn.config(text="Hide Sidebar", bg=cfg.SIDEBAR_DEEP)
        frame_instance.sidebar_state = not frame_instance.sidebar_state

    toggle_btn = tk.Button(
        toggle_bar, text="Hide Sidebar", font=("Helvetica", 9, "bold"),
        bg=cfg.SIDEBAR_DEEP, fg="white", activebackground=cfg.SIDEBAR_LIGHT, activeforeground="white",
        bd=0, cursor="hand2", padx=12, pady=6, command=toggle_sidebar_action
    )
    toggle_btn.pack(side="left")

    # 3. Sidebar Header Title Branding Block
    tk.Label(frame_instance.nav_sidebar, text="Navigation", font=("Helvetica", 11, "bold"), fg="#DDF1E6", bg=cfg.SIDEBAR_LIGHT).pack(anchor="w", padx=20, pady=(30, 20))

    # 4. Navigation Links Array
    pages_map = [
        ("🏠  Dashboard Home", "DashboardFrame"),
        ("🔄  Donate Hardware", "DonationFrame"),
        ("🔍  Browse & Claim", "ClaimFrame"),
        ("🏆  Leaderboard Ranks", "LeaderboardFrame"),
        ("👤  My Profile & Items", "ProfileFrame")
    ]
    
    for display_text, target_frame in pages_map:
        is_active = (active_page_name == target_frame)
        bg_col = cfg.SIDEBAR_DEEP if is_active else cfg.SIDEBAR_LIGHT
        fg_col = "white" if is_active else "#DDF1E6"
        
        nav_link = tk.Button(
            frame_instance.nav_sidebar, text=f"  {display_text}", font=("Helvetica", 10, "bold" if is_active else "normal"),
            bg=bg_col, fg=fg_col, activebackground=cfg.SIDEBAR_DEEP, activeforeground="white",
            bd=0, relief="flat", anchor="w", cursor="hand2"
        )
        if not is_active:
            nav_link.config(command=lambda t=target_frame: controller.show_page(t))
            
        nav_link.pack(fill="x", pady=2, ipady=12)

    # 5. Logout Session Link
    logout_btn = tk.Button(
        frame_instance.nav_sidebar, text="🚪  Logout Session", font=("Helvetica", 10, "bold"),
        bg=cfg.COLOR_RED, fg="white", activebackground=cfg.COLOR_RED, activeforeground="white",
        bd=0, relief="flat", anchor="w", cursor="hand2", command=lambda: controller.show_page("LoginFrame")
    )
    logout_btn.pack(side="bottom", fill="x", ipady=12)

class NavigationController(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SustAIn: The Circular Economy Guardian")
        self.geometry("1100x700")
        self.resizable(False, False)
        
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
