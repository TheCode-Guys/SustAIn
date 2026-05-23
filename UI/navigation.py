# ui/navigation.py
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import sys
import os

# Ensure the project root is in the path for standalone execution
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config as cfg
import UI.components as comp
from src.auth import CSVAuthManager
from src.database_manager import CSVDatabaseManager
from src.scrap_item import ScrapItem, BatteryScrapItem, PCBScrapItem

def setup_sliding_sidebar(frame_instance, active_page_name):
    """
    Injects a responsive, collapsible sliding navigation sidebar 
    directly onto any target sub-view frame container.
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

    # 4. Navigation Links Array Array
    pages_map = [
        ("🏠  Dashboard Home", "DashboardFrame"),
        ("🔄  Donate Hardware", "DonationFrame"),
        ("🔍  Browse & Claim", "ClaimFrame"),
        ("🏆  Leaderboard Ranks", "LeaderboardFrame"),
        ("👤  My Profile & Items", "ProfileFrame")
    ]
    
    for display_text, target_frame in pages_map:
        # Determine styling if this current tab is the active view panel
        is_active = (active_page_name == target_frame)
        bg_col = cfg.SIDEBAR_DEEP if is_active else cfg.SIDEBAR_LIGHT
        fg_col = "white" if is_active else "#DDF1E6"
        
        # Standard functional button generation sequence
        nav_link = tk.Button(
            frame_instance.nav_sidebar, text=f"  {display_text}", font=("Helvetica", 10, "bold" if is_active else "normal"),
            bg=bg_col, fg=fg_col, activebackground=cfg.SIDEBAR_DEEP, activeforeground="white",
            bd=0, relief="flat", anchor="w", cursor="hand2"
        )
        # Prevent recursive routing loops if already clicking the active view page
        if not is_active:
            nav_link.config(command=lambda t=target_frame: controller.show_page(t))
            
        nav_link.pack(fill="x", pady=2, ipady=12)

    # 5. Add a hard system logout command trigger link locked down at the bottom margin area
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
        
        # Initialize Managers
        self.auth_manager = CSVAuthManager()
        self.db_manager = CSVDatabaseManager()
        
        # Configure application window background baseline
        self.configure(bg=cfg.BG_PRIMARY)
        
        # UI Session State Handling
        self.current_user = {
            "matric_id": "",
            "nickname": "Guest Student",
            "email": ""
        }
        
        # Main Layout Container Frame
        self.main_container = tk.Frame(self, bg=cfg.BG_PRIMARY)
        self.main_container.pack(fill="both", expand=True)
        
        self.frames = {}
        self.build_all_screens()
        
        # Configure Table/Treeview Themes Across All Sub-Frames
        comp.configure_treeview_theme()
        
        # Boot up directly onto the Landing Screen
        self.show_page("LandingFrame")

    def build_all_screens(self):
        """Pre-renders the layout frames for clean stacked navigation."""
        for PageClass in (LandingFrame, LoginFrame, SignupFrame, DashboardFrame, DonationFrame, ClaimFrame, LeaderboardFrame, ProfileFrame):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def show_page(self, page_name):
        """Switches the top stacked frame and triggers state data cleanups."""
        frame = self.frames[page_name]
        if hasattr(frame, "on_render_refresh"):
            frame.on_render_refresh()
        frame.tkraise()


# =====================================================================
# VIEW 0: LANDING PAGE (HERO)
# =====================================================================
class LandingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#000000") # Black background to blend the logo perfectly
        self.controller = controller
        
        # --- CENTRAL HERO SECTION ---
        hero_pane = tk.Frame(self, bg="#000000")
        hero_pane.pack(expand=True)
        
        # 1. CENTRAL LOGO (CAPTIVATING SIZE)
        try:
            pil_img = Image.open("images/logo.jpeg")
            # Proportional scaling - making it large and prominent
            pil_img.thumbnail((500, 350), Image.Resampling.LANCZOS)
            self.hero_logo_tk = ImageTk.PhotoImage(pil_img)
            
            logo_label = tk.Label(hero_pane, image=self.hero_logo_tk, bg="#000000", bd=0)
            logo_label.pack(pady=(0, 10))
        except Exception as e:
            print(f"Hero logo load error: {e}")
            tk.Label(hero_pane, text="♻", font=("Arial", 100), bg="#000000", fg="#31805B").pack(pady=20)

        # 2. BRAND HEADLINE
        tk.Label(
            hero_pane, text="SustAIn", 
            font=("Helvetica", 60, "bold"), fg="#DDF1E6", bg="#000000"
        ).pack()
        
        tk.Label(
            hero_pane, text="T H E   C I R C U L A R   G U A R D I A N", 
            font=("Helvetica", 10, "bold"), fg="#31805B", bg="#000000"
        ).pack(pady=(5, 40))

        # 3. MISSION STATEMENT DESCRIPTION
        mission_text = (
            "Building a Sustainable Society through Responsible Reuse,\n"
            "Advanced Recycling, and Circular Asset Management."
        )
        tk.Label(
            hero_pane, text=mission_text, font=("Helvetica", 14),
            fg="#DDF1E6", bg="#000000", justify="center", wraplength=800
        ).pack(pady=(0, 50))

        # 4. ENTER BUTTON (CENTERED ACTION)
        enter_btn = tk.Button(
            hero_pane, text="ENTER ECO-SYSTEM  ➔", font=("Helvetica", 12, "bold"),
            bg="#31805B", fg="white", activebackground="#113E38", activeforeground="white",
            bd=0, cursor="hand2", padx=50, pady=18,
            command=lambda: controller.show_page("LoginFrame")
        )
        enter_btn.pack()
        
        # 5. SUBTLE DECORATIVE FOOTER
        footer = tk.Frame(self, bg="#000000", pady=30)
        footer.pack(side="bottom", fill="x")
        
        tk.Label(
            footer, text="Artificial Intelligence & Sustainable Society Initiative", 
            font=("Helvetica", 8, "italic"), fg="#64748b", bg="#000000"
        ).pack()

    def on_render_refresh(self):
        """No runtime state caches required for passive landing viewport."""
        pass


# =====================================================================
# VIEW 1: MODERN LOGIN PORTAL CARD LAYOUT
# =====================================================================
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        # LEFT PANEL: THE ECO-GREEN BRAND SIDEBAR
        sidebar = tk.Frame(self, bg=cfg.SIDEBAR_LIGHT, width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False) 
        
        try:
            self.raw_img = tk.PhotoImage(file="images/logo.jpeg")
            self.logo_img = self.raw_img.subsample(4, 4)
            logo_label = tk.Label(sidebar, image=self.logo_img, bg=cfg.SIDEBAR_LIGHT)
            logo_label.pack(pady=(120, 20))
        except Exception:
            logo_label = tk.Label(sidebar, text="♻", font=("Arial", 48), bg=cfg.SIDEBAR_LIGHT, fg="white")
            logo_label.pack(pady=(120, 20))
            
        tk.Label(sidebar, text="SustAIn", font=("Helvetica", 24, "bold"), fg="white", bg=cfg.SIDEBAR_LIGHT).pack()
        tk.Label(sidebar, text="The Circular Guardian", font=("Helvetica", 11, "italic"), fg="#DDF1E6", bg=cfg.SIDEBAR_LIGHT).pack(pady=(5, 0))

        tab_container = tk.Frame(sidebar, bg=cfg.SIDEBAR_LIGHT)
        tab_container.pack(side="bottom", fill="x", pady=50)
        
        login_tab = tk.Label(tab_container, text="  LOGIN  ▶", font=("Helvetica", 11, "bold"), fg="white", bg=cfg.SIDEBAR_DEEP, anchor="w", pady=12)
        login_tab.pack(fill="x", pady=2)
        
        signup_tab = tk.Button(
            tab_container, text="  SIGN UP", font=("Helvetica", 11, "bold"), fg="#DDF1E6", bg=cfg.SIDEBAR_LIGHT, 
            activebackground=cfg.SIDEBAR_LIGHT, activeforeground="white", bd=0, relief="flat", anchor="w", cursor="hand2",
            command=lambda: controller.show_page("SignupFrame")
        )
        signup_tab.pack(fill="x", pady=2, ipady=10)

        # RIGHT PANEL: THE CLEAN MODERN FORM AREA
        form_container = tk.Frame(self, bg=cfg.BG_PRIMARY, padx=60)
        form_container.pack(side="left", fill="both", expand=True)
        
        center_box = tk.Frame(form_container, bg=cfg.BG_PRIMARY)
        center_box.pack(anchor="center", expand=True, fill="x")
        
        tk.Label(center_box, text="Account Portal Login", font=("Helvetica", 22, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", pady=(0, 35))
        
        tk.Label(center_box, text="✉  Student Email Address", font=("Helvetica", 10, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w")
        self.email_entry = tk.Entry(center_box, font=("Helvetica", 11), bg="#f1f5f9", fg=cfg.TEXT_MAIN, bd=0, relief="flat")
        self.email_entry.pack(fill="x", ipady=10, pady=(4, 20))
        
        line1 = tk.Frame(center_box, height=1, bg="#cbd5e1")
        line1.pack(fill="x", pady=(0, 20))
        
        tk.Label(center_box, text="🔒  Password", font=("Helvetica", 10, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w")
        self.password_entry = tk.Entry(center_box, show="*", font=("Helvetica", 11), bg="#f1f5f9", fg=cfg.TEXT_MAIN, bd=0, relief="flat")
        self.password_entry.pack(fill="x", ipady=10, pady=(4, 5))
        
        line2 = tk.Frame(center_box, height=1, bg="#cbd5e1")
        line2.pack(fill="x", pady=(0, 15))
        
        action_bar = tk.Frame(center_box, bg=cfg.BG_PRIMARY)
        action_bar.pack(fill="x", pady=10)
        
        tk.Label(action_bar, text="Forgot Password?", font=("Helvetica", 9), fg=cfg.TEXT_MUTED, bg=cfg.BG_PRIMARY).pack(side="left")
        
        login_btn = tk.Button(
            action_bar, text="LOGIN  ➔", font=("Helvetica", 10, "bold"), 
            bg=cfg.COLOR_GREEN, fg="white", activebackground=cfg.COLOR_GREEN, activeforeground="white",
            bd=0, cursor="hand2", padx=25, pady=8, command=self.mock_login
        )
        login_btn.pack(side="right")

    def mock_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("UI Validation Error", "Please fill in all layout credentials.")
            return
            
        success, result = self.controller.auth_manager.authenticate_student(email, password)
        
        if success:
            # result is the username on success
            self.controller.current_user["nickname"] = result
            self.controller.current_user["email"] = email
            # Find matric_id
            for user in self.controller.db_manager.read_all_users():
                if user[1] == email:
                    self.controller.current_user["matric_id"] = user[0]
                    break
            
            messagebox.showinfo("Login Success", f"Welcome back, {result}!")
            self.controller.show_page("DashboardFrame")
        else:
            messagebox.showerror("Authentication Failed", result)

    def on_render_refresh(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


# =====================================================================
# VIEW 2: REGISTRATION SCREEN SKELETON
# =====================================================================
class SignupFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        sidebar = tk.Frame(self, bg=cfg.SIDEBAR_LIGHT, width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        try:
            logo_label = tk.Label(sidebar, image=controller.frames["LoginFrame"].logo_img, bg=cfg.SIDEBAR_LIGHT)
            logo_label.pack(pady=(120, 20))
        except Exception:
            pass
            
        tk.Label(sidebar, text="SustAIn", font=("Helvetica", 24, "bold"), fg="white", bg=cfg.SIDEBAR_LIGHT).pack()
        
        tab_container = tk.Frame(sidebar, bg=cfg.SIDEBAR_LIGHT)
        tab_container.pack(side="bottom", fill="x", pady=50)
        
        login_tab = tk.Button(
            tab_container, text="  LOGIN", font=("Helvetica", 11, "bold"), fg="#DDF1E6", bg=cfg.SIDEBAR_LIGHT, 
            activebackground=cfg.SIDEBAR_LIGHT, activeforeground="white", bd=0, relief="flat", anchor="w", cursor="hand2",
            command=lambda: controller.show_page("LoginFrame")
        )
        login_tab.pack(fill="x", pady=2, ipady=10)
        
        signup_tab = tk.Label(tab_container, text="  SIGN UP  ▶", font=("Helvetica", 11, "bold"), fg="white", bg=cfg.SIDEBAR_DEEP, anchor="w", pady=12)
        signup_tab.pack(fill="x", pady=2)

        form_container = tk.Frame(self, bg=cfg.BG_PRIMARY, padx=60)
        form_container.pack(side="left", fill="both", expand=True)
        
        center_box = tk.Frame(form_container, bg=cfg.BG_PRIMARY)
        center_box.pack(anchor="center", expand=True, fill="x")
        
        tk.Label(center_box, text="Create An Account", font=("Helvetica", 22, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", pady=(0, 5))
        tk.Label(center_box, text="Sign up with your institutional student email credentials", font=("Helvetica", 10, "italic"), fg=cfg.TEXT_MUTED, bg=cfg.BG_PRIMARY).pack(anchor="w", pady=(0, 25))
        
        tk.Label(center_box, text="📇  Matriculation Number", font=("Helvetica", 9, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w")
        self.matric_entry = tk.Entry(center_box, font=("Helvetica", 10), bg="#f1f5f9", fg=cfg.TEXT_MAIN, bd=0, relief="flat")
        self.matric_entry.pack(fill="x", ipady=7, pady=(2, 10))
        
        tk.Label(center_box, text="👤  Full Registration Name", font=("Helvetica", 9, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w")
        self.nick_entry = tk.Entry(center_box, font=("Helvetica", 10), bg="#f1f5f9", fg=cfg.TEXT_MAIN, bd=0, relief="flat")
        self.nick_entry.pack(fill="x", ipady=7, pady=(2, 10))
        
        tk.Label(center_box, text="✉  PAU Student Email Address", font=("Helvetica", 9, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w")
        self.email_entry = tk.Entry(center_box, font=("Helvetica", 10), bg="#f1f5f9", fg=cfg.TEXT_MAIN, bd=0, relief="flat")
        self.email_entry.pack(fill="x", ipady=7, pady=(2, 10))
        
        tk.Label(center_box, text="🔒  Secure Account Password", font=("Helvetica", 9, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w")
        self.pass_entry = tk.Entry(center_box, show="*", font=("Helvetica", 10), bg="#f1f5f9", fg=cfg.TEXT_MAIN, bd=0, relief="flat")
        self.pass_entry.pack(fill="x", ipady=7, pady=(2, 20))
        
        action_bar = tk.Frame(center_box, bg=cfg.BG_PRIMARY)
        action_bar.pack(fill="x")
        
        reg_btn = tk.Button(
            action_bar, text="REGISTER  ➔", font=("Helvetica", 10, "bold"), 
            bg=cfg.COLOR_GREEN, fg="white", activebackground=cfg.COLOR_GREEN, activeforeground="white",
            bd=0, cursor="hand2", padx=25, pady=8, command=self.mock_signup
        )
        reg_btn.pack(side="right")

    def mock_signup(self):
        matric = self.matric_entry.get().strip()
        nick = self.nick_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not all([matric, nick, email, password]):
            messagebox.showerror("Validation Error", "All fields are required.")
            return
            
        success, msg = self.controller.auth_manager.register_student(matric, email, password, nick)
        
        if success:
            # Set session state directly for professional instant-login flow
            self.controller.current_user["matric_id"] = matric
            self.controller.current_user["nickname"] = nick
            self.controller.current_user["email"] = email
            
            messagebox.showinfo("Registration Success", f"Account created! Welcome to SustAIn, {nick}!")
            self.controller.show_page("DashboardFrame")
        else:
            messagebox.showerror("Registration Failed", msg)

    def on_render_refresh(self):
        self.matric_entry.delete(0, tk.END)
        self.nick_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)


# =====================================================================
# VIEW 3: HOMEPAGE DYNAMIC HUB BANNER
# =====================================================================
class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "DashboardFrame")
        
        self.welcome_label = tk.Label(
            self.right_workspace, text="Welcome back to the Hub", 
            font=("Helvetica", 22, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY
        )
        self.welcome_label.pack(anchor="w", padx=35, pady=(30, 5))
        
        caption = tk.Label(
            self.right_workspace, text="SustAIn: Protecting our campus ecosystem through circular hardware exchange.", 
            font=("Helvetica", 10), fg=cfg.TEXT_MUTED, bg=cfg.BG_PRIMARY
        )
        caption.pack(anchor="w", padx=35, pady=(0, 25))
        
        scorecard = tk.LabelFrame(
            self.right_workspace, text=" Your Ecological Impact Summary ", 
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

        tk.Label(self.right_workspace, text="What would you like to do today?", font=("Helvetica", 12, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=35, pady=(25, 10))
        
        grid_container = tk.Frame(self.right_workspace, bg=cfg.BG_PRIMARY)
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
        user_id = self.controller.current_user.get("matric_id")
        self.welcome_label.config(text=f"Welcome back to the Circle, {user_nick} 🌿")
        
        # Update Impact Summary Stats from real data
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


# =====================================================================
# VIEW 4: DONATION REGISTRY LOG INPUT FORM
# =====================================================================
class DonationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "DonationFrame")
        
        tk.Label(self.right_workspace, text="Book / Donate E-Waste Scrap", font=("Helvetica", 18, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=30, pady=(20, 20))
        
        form_frame = tk.Frame(self.right_workspace, bg="#F3FAF6", padx=30, pady=25)
        form_frame.pack(anchor="w", padx=30, fill="x")
        
        self.f1, self.name_entry = comp.create_form_entry(form_frame, "Hardware Name / Model:")
        self.f1.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Material Category Type:", font=("Helvetica", 10, "bold"), bg="#F3FAF6", fg=cfg.TEXT_MAIN).pack(anchor="w", pady=(5,2))
        self.categories = [
            "Processors & Integrated Circuits (ICs)",
            "Displays & Screens",
            "Power & Batteries",
            "Peripherals & Input Devices",
            "Circuit Boards (PCBs)",
            "Storage & Memory",
            "Cables & Interconnects"
        ]
        self.cat_var = tk.StringVar(self)
        self.cat_var.set(self.categories[0])
        self.cat_dropdown = tk.OptionMenu(form_frame, self.cat_var, *self.categories)
        self.cat_dropdown.config(font=("Helvetica", 10), bg="#f1f5f9", relief="flat")
        self.cat_dropdown.pack(fill="x", pady=5)
        
        self.f2, self.weight_entry = comp.create_form_entry(form_frame, "Net Weight (kg):")
        self.f2.pack(fill="x", pady=5)
        
        # --- IMAGE UPLOAD SECTION ---
        tk.Label(form_frame, text="📸 Hardware Photo / Verification:", font=("Helvetica", 10, "bold"), bg="#F3FAF6", fg=cfg.TEXT_MAIN).pack(anchor="w", pady=(10,2))
        img_controls = tk.Frame(form_frame, bg="#F3FAF6")
        img_controls.pack(fill="x", pady=5)
        
        self.image_path = "images/default.png"
        self.img_label = tk.Label(img_controls, text="No file selected (Default will be used)", font=("Helvetica", 9), fg=cfg.TEXT_MUTED, bg="#F3FAF6")
        self.img_label.pack(side="left")
        
        btn_browse = tk.Button(img_controls, text="Browse...", font=("Helvetica", 9), bg="#cbd5e1", command=self.choose_image)
        btn_browse.pack(side="right")
        
        sub_btn = tk.Button(form_frame, text="Log Item Into Registry", font=("Helvetica", 11, "bold"), bg=cfg.COLOR_GREEN, fg="white", bd=0, cursor="hand2", command=self.mock_log_submit)
        sub_btn.pack(pady=20, ipady=6, fill="x")

    def choose_image(self):
        fpath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if fpath:
            self.image_path = fpath
            fname = os.path.basename(fpath)
            self.img_label.config(text=f"Selected: {fname}", fg=cfg.SIDEBAR_LIGHT)

    def mock_log_submit(self):
        name = self.name_entry.get().strip()
        category = self.cat_var.get()
        weight_str = self.weight_entry.get().strip()
        donor_phone = self.controller.current_user["matric_id"]
        
        if not name or not weight_str:
            messagebox.showerror("Validation Error", "Please provide a name and weight.")
            return
            
        try:
            weight = float(weight_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Weight must be a valid number.")
            return

        if "Battery" in category:
            item = BatteryScrapItem(None, name, category, weight, "Minor Repair", donor_phone)
        elif "Circuit" in category or "PCBs" in category:
            item = PCBScrapItem(None, name, category, weight, "Minor Repair", donor_phone)
        else:
            item = ScrapItem(None, name, category, weight, "Minor Repair", donor_phone)
            
        score = item.calculate_impact_score()
        item_id = self.controller.db_manager.save_new_donation(
            name, category, weight, "Minor Repair", score, donor_phone, self.image_path
        )
        
        messagebox.showinfo("Donation Success", f"Item Logged Successfully!\nItem ID: {item_id}\nEco-Impact Score: {score}")
        self.controller.show_page("DashboardFrame")

    def on_render_refresh(self):
        self.name_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.cat_var.set(self.categories[0])
        self.image_path = "images/default.png"
        self.img_label.config(text="No file selected (Default will be used)", fg=cfg.TEXT_MUTED)


# =====================================================================
# VIEW 5: CLAIM REGISTRY TREEVIEW TABLE
# =====================================================================
class ClaimFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "ClaimFrame")
        
        tk.Label(self.right_workspace, text="Hardware Registry Exchange", font=("Helvetica", 18, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=30, pady=(20, 10))
        
        filter_bar = tk.Frame(self.right_workspace, bg="#F3FAF6", padx=20, pady=15)
        filter_bar.pack(fill="x", padx=30, pady=(5, 15))
        filter_bar.columnconfigure(0, weight=2)
        filter_bar.columnconfigure(1, weight=1)
        
        search_pane = tk.Frame(filter_bar, bg="#F3FAF6")
        search_pane.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        tk.Label(search_pane, text="🔍  Search Hardware Name:", font=("Helvetica", 9, "bold"), fg=cfg.TEXT_MAIN, bg="#F3FAF6").pack(anchor="w")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_rows())
        self.search_entry = tk.Entry(search_pane, textvariable=self.search_var, font=("Helvetica", 10), bg="#FFFFFF", bd=1, relief="flat")
        self.search_entry.pack(fill="x", ipady=6, pady=(2, 0))
        
        cat_pane = tk.Frame(filter_bar, bg="#F3FAF6")
        cat_pane.grid(row=0, column=1, padx=(0, 15), sticky="ew")
        tk.Label(cat_pane, text="📁  Filter Category:", font=("Helvetica", 9, "bold"), fg=cfg.TEXT_MAIN, bg="#F3FAF6").pack(anchor="w")
        self.cat_options = [
            "All Categories",
            "Processors & Integrated Circuits (ICs)",
            "Displays & Screens",
            "Power & Batteries",
            "Peripherals & Input Devices",
            "Circuit Boards (PCBs)",
            "Storage & Memory",
            "Cables & Interconnects"
        ]
        self.selected_cat_var = tk.StringVar(self)
        self.selected_cat_var.set(self.cat_options[0])
        self.selected_cat_var.trace_add("write", lambda *args: self.load_rows())
        self.cat_dropdown = tk.OptionMenu(cat_pane, self.selected_cat_var, *self.cat_options)
        self.cat_dropdown.config(font=("Helvetica", 9), bg="#FFFFFF", relief="flat")
        self.cat_dropdown.pack(fill="x", pady=(2, 0))
        
        self.tree_frame = tk.Frame(self.right_workspace)
        self.tree_frame.pack(fill="both", expand=True, padx=30, pady=5)
        
        columns = ("id", "name", "category", "weight", "score")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID"); self.tree.heading("name", text="Description")
        self.tree.heading("category", text="Category"); self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("score", text="Eco-Score")
        
        self.tree.column("id", width=60, anchor="center"); self.tree.column("name", width=300, anchor="w")
        self.tree.column("category", width=180, anchor="w"); self.tree.column("weight", width=90, anchor="center")
        self.tree.column("score", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        # BOTTOM PREVIEW PANEL
        self.preview_pane = tk.Frame(self.right_workspace, bg="#FFFFFF", highlightbackground="#e2e8f0", highlightthickness=1)
        self.preview_pane.pack(fill="x", padx=30, pady=(10, 30))
        
        self.img_frame = tk.Frame(self.preview_pane, bg="#f1f5f9", width=120, height=120)
        self.img_frame.pack(side="left", padx=15, pady=15); self.img_frame.pack_propagate(False)
        self.item_preview_img = tk.Label(self.img_frame, text="Select Item", bg="#f1f5f9", fg=cfg.TEXT_MUTED)
        self.item_preview_img.pack(expand=True, fill="both")
        
        self.meta_frame = tk.Frame(self.preview_pane, bg="#FFFFFF")
        self.meta_frame.pack(side="left", fill="both", expand=True, padx=10, pady=15)
        self.item_name_lbl = tk.Label(self.meta_frame, text="No Item Selected", font=("Helvetica", 14, "bold"), fg=cfg.TEXT_MAIN, bg="#FFFFFF")
        self.item_name_lbl.pack(anchor="w")
        self.item_meta_lbl = tk.Label(self.meta_frame, text="Click an item above to view details and photos.", font=("Helvetica", 9), fg=cfg.TEXT_MUTED, bg="#FFFFFF", wraplength=400, justify="left")
        self.item_meta_lbl.pack(anchor="w", pady=5)
        
        self.btn_claim_now = tk.Button(
            self.preview_pane, text="Claim for Reuse ➔", font=("Helvetica", 10, "bold"),
            bg=cfg.COLOR_BLUE, fg="white", bd=0, cursor="hand2", padx=20, pady=10,
            command=self.mock_claim
        )
        self.btn_claim_now.pack(side="right", padx=20)
        self.btn_claim_now.config(state="disabled")

    def on_item_selected(self, event):
        selected = self.tree.selection()
        if not selected: return
        iid = self.tree.item(selected[0])['values'][0]
        db_items = self.controller.db_manager.get_all_registry_items_dict()
        data = next((item for item in db_items if str(item['id']) == str(iid)), None)
        
        if data:
            self.item_name_lbl.config(text=data['item_name'])
            meta_text = f"Category: {data['category']}\nCondition: {data['damage_state']}\nPoints: {data['score']} pts"
            self.item_meta_lbl.config(text=meta_text)
            self.btn_claim_now.config(state="normal")
            
            img_path = data.get('image_path', "images/default.png")
            if not os.path.exists(img_path): img_path = "images/default.png"
            try:
                raw_img = Image.open(img_path)
                raw_img.thumbnail((120, 120), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(raw_img)
                self.item_preview_img.config(image=self.photo, text="")
            except:
                self.item_preview_img.config(image="", text="No Image")

    def mock_claim(self):
        selected = self.tree.selection()
        if not selected: return
        iid = self.tree.item(selected[0])['values'][0]
        uid = self.controller.current_user["matric_id"]
        if self.controller.db_manager.update_item_to_claimed(iid, uid, "Reuse"):
            messagebox.showinfo("Success", f"Item {iid} claimed!")
            self.on_render_refresh()
        else:
            messagebox.showerror("Error", "Could not claim item.")

    def load_rows(self):
        for record in self.tree.get_children(): self.tree.delete(record)
        q = self.search_var.get().strip().lower()
        cat = self.selected_cat_var.get()
        records = self.controller.db_manager.read_all_hardware_records()
        for row in records:
            if row[6] == "Available" and (not q or q in str(row[1]).lower()) and (cat == "All Categories" or str(row[2]) == cat):
                self.tree.insert("", "end", values=(row[0], row[1], row[2], f"{row[3]} kg", f"{row[5]} pts"))

    def on_render_refresh(self):
        self.search_var.set(""); self.selected_cat_var.set(self.cat_options[0])
        self.load_rows()
        self.item_name_lbl.config(text="No Item Selected"); self.btn_claim_now.config(state="disabled")


# =====================================================================
# VIEW 6: ECO-LEADERBOARD STANDINGS SCREEN
# =====================================================================
class LeaderboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "LeaderboardFrame")
        
        self.user_impact_card = tk.LabelFrame(
            self.right_workspace, text=" Your Personal Eco-Impact Standings ", 
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

        self.champ_label = tk.Label(self.right_workspace, text="🥇 Calculating Champion... 🥇", font=("Helvetica", 11, "bold"), fg=cfg.COLOR_AMBER, bg="#fef3c7", pady=12)
        self.champ_label.pack(fill="x", padx=30, pady=15)

        tk.Label(self.right_workspace, text="Campus Overall Standings League", font=("Helvetica", 14, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=30, pady=(15, 5))
        table_frame = tk.Frame(self.right_workspace)
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


# =====================================================================
# VIEW 7: PROFILE
# =====================================================================
class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "ProfileFrame")
        
        user_card = tk.Frame(self.right_workspace, bg="#F3FAF6", padx=25, pady=20)
        user_card.pack(fill="x", padx=30, pady=(20, 15))
        
        info_pane = tk.Frame(user_card, bg="#F3FAF6")
        info_pane.pack(side="left")
        self.name_lbl = tk.Label(info_pane, text="Name", font=("Helvetica", 16, "bold"), bg="#F3FAF6")
        self.name_lbl.pack(anchor="w")
        self.sub_lbl = tk.Label(info_pane, text="ID: --", fg=cfg.TEXT_MUTED, bg="#F3FAF6")
        self.sub_lbl.pack(anchor="w", pady=2)
        
        stats_pane = tk.Frame(user_card, bg="#F3FAF6")
        stats_pane.pack(side="right")
        self.pts_val = tk.Label(stats_pane, text="0.00", font=("Helvetica", 14, "bold"), fg=cfg.SIDEBAR_LIGHT, bg="#F3FAF6")
        self.pts_val.pack(); tk.Label(stats_pane, text="Eco-Points", font=("Helvetica", 8), bg="#F3FAF6").pack()
        
        # Items Box
        k_box = tk.Frame(stats_pane, bg="#DDF1E6", padx=15, pady=5)
        k_box.pack(side="left", padx=5)
        tk.Label(k_box, text="Items Logged", font=("Helvetica", 8, "bold"), fg=cfg.TEXT_MAIN, bg="#DDF1E6").pack()
        self.item_count_val = tk.Label(k_box, text="0", font=("Helvetica", 14, "bold"), fg=cfg.SIDEBAR_LIGHT, bg="#DDF1E6")
        self.item_count_val.pack()

        tab_bar = tk.Frame(self.right_workspace, bg=cfg.BG_PRIMARY)
        tab_bar.pack(fill="x", padx=30, pady=10)
        self.btn_owned = tk.Button(tab_bar, text="MY DONATIONS", command=lambda: self.switch_view("owned"))
        self.btn_owned.pack(side="left", expand=True, fill="x")
        self.btn_requested = tk.Button(tab_bar, text="MY CLAIMS", command=lambda: self.switch_view("requested"))
        self.btn_requested.pack(side="left", expand=True, fill="x")

        self.table_frame = tk.Frame(self.right_workspace)
        self.table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        self.tree = ttk.Treeview(self.table_frame, columns=("id", "name", "category", "status"), show="headings")
        for c in ("id", "name", "category", "status"): self.tree.heading(c, text=c.title())
        self.tree.pack(fill="both", expand=True)
        self.current_tab = "owned"

    def switch_view(self, t):
        self.current_tab = t; self.load_rows()

    def load_rows(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        uid = self.controller.current_user.get("matric_id")
        records = self.controller.db_manager.read_all_hardware_records()
        total_p = 0.0
        for row in records:
            if len(row) < 10: continue
            donor, claimer = str(row[8]).strip(), str(row[9]).strip()
            if donor == uid:
                total_p += float(row[5])
                if self.current_tab == "owned": self.tree.insert("", "end", values=(row[0], row[1], row[2], row[6]))
            elif self.current_tab == "requested" and claimer == uid:
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[6]))
        self.pts_val.config(text=f"{round(total_p, 2)}")

    def on_render_refresh(self):
        """
        Updates the profile summary with real-time statistics aggregated 
        from the user's registry submissions.
        """
        # 1. Update basic profile info
        self.name_lbl.config(text=self.controller.current_user["nickname"])
        self.sub_lbl.config(text=f"Student Guardian | ID: {self.controller.current_user['matric_id']}")
        
        # 2. Aggregation Logic
        uid = self.controller.current_user["matric_id"]
        records = self.controller.db_manager.read_all_hardware_records()
        
        total_points = 0.0
        total_items = 0
        
        for r in records:
            # Donor phone (col 8) matches matric_id
            if len(r) > 8 and str(r[8]).strip() == uid:
                try:
                    total_points += float(r[5])
                    total_items += 1
                except (ValueError, IndexError):
                    continue
        
        # 3. Update dynamic scorecard widgets
        self.pts_val.config(text=f"{round(total_points, 2)}")
        self.item_count_val.config(text=f"{total_items}")
        
        # 4. Refresh table view
        self.switch_view(self.current_tab)

if __name__ == "__main__":
    app = NavigationController()
    app.mainloop()
