# UI/navigation_sidebar.py
import tkinter as tk
from tkinter import ttk
import config as cfg

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

    # 4. Navigation Links Array
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
