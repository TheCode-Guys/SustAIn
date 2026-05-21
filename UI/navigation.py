# ui/navigation.py
import tkinter as tk
from tkinter import messagebox, ttk
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
        
        # UI Session State Handling (Simulating log cache without active database)
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
        
        # Boot up directly onto the modern Login Screen
        self.show_page("LoginFrame")

    def build_all_screens(self):
        """Pre-renders the layout frames for clean stacked navigation."""
        for PageClass in (LoginFrame, SignupFrame, DashboardFrame, DonationFrame, ClaimFrame, LeaderboardFrame):
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
# VIEW 1: MODERN LOGIN PORTAL CARD LAYOUT
# =====================================================================
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        card = tk.Frame(self, bg=cfg.CARD_BG, padx=40, pady=40, relief="flat", bd=0)
        card.pack(anchor="center", expand=True)
        
        tk.Label(card, text="SustAIn Portal", font=("Helvetica", 18, "bold"), fg=cfg.COLOR_GREEN, bg=cfg.CARD_BG).pack(pady=(0, 20))
        
        self.email_box, self.email_entry = comp.create_form_entry(card, "PAU Student Email Address:")
        self.email_box.pack(pady=10)
        
        self.pass_box, self.password_entry = comp.create_form_entry(card, "Password:")
        self.password_entry.config(show="*")
        self.pass_box.pack(pady=10)
        
        login_btn = tk.Button(card, text="Sign In Securely", command=self.mock_login)
        comp.apply_modern_button(login_btn, cfg.COLOR_GREEN)
        login_btn.pack(pady=25, fill="x")
        
        tk.Button(card, text="Don't have an account? Sign Up", fg=cfg.TEXT_MUTED, bg=cfg.CARD_BG, bd=0, cursor="hand2", command=lambda: controller.show_page("SignupFrame")).pack()

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
            # We don't have matric_id in current auth return, let's find it
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
        
        center_box = tk.Frame(self, bg=cfg.CARD_BG, padx=30, pady=30)
        center_box.pack(anchor="center", expand=True)
        
        tk.Label(center_box, text="Create SustAIn Account", font=("Helvetica", 16, "bold"), fg=cfg.COLOR_GREEN, bg=cfg.CARD_BG).pack(pady=10)
        
        self.b1, self.matric_entry = comp.create_form_entry(center_box, "Matric Number:")
        self.b1.pack(pady=5)
        self.b2, self.nick_entry = comp.create_form_entry(center_box, "Nickname / Call-sign:")
        self.b2.pack(pady=5)
        self.b3, self.email_entry = comp.create_form_entry(center_box, "PAU Student Email:")
        self.b3.pack(pady=5)
        self.b4, self.pass_entry = comp.create_form_entry(center_box, "Password:")
        self.pass_entry.config(show="*")
        self.b4.pack(pady=5)
        
        reg_btn = tk.Button(center_box, text="Register", command=self.mock_signup)
        comp.apply_modern_button(reg_btn, cfg.COLOR_GREEN)
        reg_btn.pack(pady=15, fill="x")
        
        tk.Button(center_box, text="Back to Login", fg=cfg.TEXT_MUTED, bg=cfg.CARD_BG, bd=0, command=lambda: controller.show_page("LoginFrame")).pack()

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
        
        self.welcome_label = comp.create_header_banner(self, "Welcome to the Hub Panel", cfg.COLOR_GREEN)
        self.welcome_label.pack(fill="x")
        
        metric_card = tk.LabelFrame(self, text=" System Performance Indicator ", font=("Helvetica", 10, "bold"), bg=cfg.CARD_BG, fg=cfg.TEXT_MAIN, padx=20, pady=20)
        metric_card.pack(pady=30)
        
        tk.Label(metric_card, text="Campus Circular Efficiency Rate", font=("Helvetica", 12), bg=cfg.CARD_BG, fg=cfg.TEXT_MAIN).pack()
        tk.Label(metric_card, text="74.5%", font=("Helvetica", 28, "bold"), fg=cfg.COLOR_GREEN, bg=cfg.CARD_BG).pack(pady=5)
        tk.Label(metric_card, text="Formula: (Claimed Items / Total Items) * 100", font=("Helvetica", 8, "italic"), fg=cfg.TEXT_MUTED, bg=cfg.CARD_BG).pack()

        btn_layout = tk.Frame(self, bg=cfg.BG_PRIMARY)
        btn_layout.pack(pady=20)
        
        b_donate = tk.Button(btn_layout, text="🔄 Donate Hardware", command=lambda: controller.show_page("DonationFrame"))
        comp.apply_modern_button(b_donate, cfg.COLOR_GREEN)
        b_donate.grid(row=0, column=0, padx=15)
        
        b_claim = tk.Button(btn_layout, text="🔍 Browse Items", command=lambda: controller.show_page("ClaimFrame"))
        comp.apply_modern_button(b_claim, cfg.COLOR_BLUE)
        b_claim.grid(row=0, column=1, padx=15)
        
        b_lead = tk.Button(btn_layout, text="🏆 Leaderboard", command=lambda: controller.show_page("LeaderboardFrame"))
        comp.apply_modern_button(b_lead, cfg.COLOR_AMBER)
        b_lead.grid(row=0, column=2, padx=15)
        
        logout_btn = tk.Button(self, text="Logout Session", command=lambda: controller.show_page("LoginFrame"))
        comp.apply_modern_button(logout_btn, cfg.COLOR_RED)
        logout_btn.pack(side="bottom", pady=30)

    def on_render_refresh(self):
        user_nick = self.controller.current_user["nickname"]
        user_id = self.controller.current_user["matric_id"]
        self.welcome_label.config(text=f"Welcome back to the Circle, {user_nick} ({user_id}) 🌿")


# =====================================================================
# VIEW 4: DONATION REGISTRY LOG INPUT FORM (EXPANDED LAB CATEGORIES)
# =====================================================================
class DonationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        header = comp.create_header_banner(self, "E-Waste Material Log Center", cfg.COLOR_GREEN)
        header.pack(fill="x")
        
        form_frame = tk.Frame(self, bg=cfg.CARD_BG, padx=30, pady=20)
        form_frame.pack(pady=25)
        
        self.f1, self.name_entry = comp.create_form_entry(form_frame, "Hardware Name/Model:")
        self.f1.pack(pady=5)
        
        # Expanded Dropdown Architecture Mapping Real-World Project Assets
        tk.Label(form_frame, text="Material Category Type:", font=("Helvetica", 10, "bold"), bg=cfg.CARD_BG, fg=cfg.TEXT_MAIN).pack(anchor="w", pady=(5,2))
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
        self.f2.pack(pady=5)
        
        self.img_placeholder = tk.Label(form_frame, text="[ Photo Verification Preview Box ]", bg="#e2e8f0", width=42, height=4, font=("Helvetica", 9, "italic"), relief="groove")
        self.img_placeholder.pack(pady=12)
        
        sub_btn = tk.Button(form_frame, text="Submit Log to Registry", command=self.mock_log_submit)
        comp.apply_modern_button(sub_btn, cfg.COLOR_GREEN)
        sub_btn.pack(pady=10, fill="x")
        
        back_btn = tk.Button(self, text="⬅ Back Hub", command=lambda: controller.show_page("DashboardFrame"))
        comp.apply_modern_button(back_btn, cfg.TEXT_MUTED)
        back_btn.pack(pady=5)

    def mock_log_submit(self):
        name = self.name_entry.get().strip()
        category = self.cat_var.get()
        weight_str = self.weight_entry.get().strip()
        donor_phone = self.controller.current_user["matric_id"] # Using matric_id as phone for now or we could add a field
        
        if not name or not weight_str:
            messagebox.showerror("Validation Error", "Please provide a name and weight.")
            return
            
        try:
            weight = float(weight_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Weight must be a valid number.")
            return

        # Choose the right OOP class based on category
        if "Battery" in category:
            item = BatteryScrapItem(None, name, category, weight, "Minor Repair", donor_phone)
        elif "Circuit" in category or "PCBs" in category:
            item = PCBScrapItem(None, name, category, weight, "Minor Repair", donor_phone)
        else:
            item = ScrapItem(None, name, category, weight, "Minor Repair", donor_phone)
            
        score = item.calculate_impact_score()
        
        # Save to CSV via DatabaseManager
        item_id = self.controller.db_manager.save_new_donation(
            name, category, weight, "Minor Repair", score, donor_phone
        )
        
        messagebox.showinfo("Donation Success", f"Item Logged Successfully!\nItem ID: {item_id}\nEco-Impact Score: {score}")
        self.controller.show_page("DashboardFrame")

    def on_render_refresh(self):
        self.name_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.cat_var.set(self.categories[0])


# =====================================================================
# VIEW 5: CLAIM REGISTRY TREEVIEW TABLE INTERACTIVE LAYOUT
# =====================================================================
class ClaimFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        header = comp.create_header_banner(self, "Circular Hardware Registry Exchange", cfg.COLOR_BLUE)
        header.pack(fill="x")
        
        self.tree_frame = tk.Frame(self, bg=cfg.BG_PRIMARY)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        columns = ("id", "name", "category", "weight", "score")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="Item ID")
        self.tree.heading("name", text="Hardware Name/Model")
        self.tree.heading("category", text="Category Type")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("score", text="Eco-Impact Score")
        
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=320, anchor="w")
        self.tree.column("category", width=250, anchor="w")
        self.tree.column("weight", width=110, anchor="center")
        self.tree.column("score", width=130, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Bottom transactional tray area layout
        tray = tk.Frame(self, bg=cfg.CARD_BG, pady=15, padx=20)
        tray.pack(fill="x", side="bottom", ipady=5)
        
        back_btn = tk.Button(tray, text="⬅ Back Hub", command=lambda: controller.show_page("DashboardFrame"))
        comp.apply_modern_button(back_btn, cfg.TEXT_MUTED)
        back_btn.pack(side="left")
        
        claim_btn = tk.Button(tray, text="Confirm Material Claim", command=self.mock_claim)
        comp.apply_modern_button(claim_btn, cfg.COLOR_BLUE)
        claim_btn.pack(side="right")

    def mock_claim(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an item to claim.")
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        claimer_id = self.controller.current_user["matric_id"]
        
        success = self.controller.db_manager.update_item_to_claimed(item_id, claimer_id, "Reuse/Repair")
        
        if success:
            messagebox.showinfo("Claim Success", f"Item {item_id} successfully claimed!")
            self.on_render_refresh()
        else:
            messagebox.showerror("Claim Error", "Item could not be claimed.")

    def on_render_refresh(self):
        for record in self.tree.get_children():
            self.tree.delete(record)
            
        records = self.controller.db_manager.read_all_hardware_records()
        for row in records:
            # row format: [ID, Name, Category, Weight, Condition, Score, Status, Donor, Claimer, Intent]
            if row[6] == "Available":
                display_row = (row[0], row[1], row[2], row[3], row[5])
                self.tree.insert("", "end", values=display_row)


# =====================================================================
# VIEW 6: ECO-LEADERBOARD STANDINGS SCREEN
# =====================================================================
class LeaderboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        header = comp.create_header_banner(self, "SustAIn Ecological Champion Standings", cfg.COLOR_AMBER)
        header.pack(fill="x")
        
        self.champ_label = tk.Label(self, text="🥇 Calculating Champion... 🥇", font=("Helvetica", 11, "bold"), fg=cfg.COLOR_AMBER, bg="#fef3c7", pady=12)
        self.champ_label.pack(fill="x", padx=20, pady=15)
        
        self.tree = ttk.Treeview(self, columns=("rank", "nick", "matric", "score"), show="headings")
        self.tree.heading("rank", text="Rank")
        self.tree.heading("nick", text="Student Nickname")
        self.tree.heading("matric", text="Matriculation ID")
        self.tree.heading("score", text="Total Accumulated Points")
        
        self.tree.column("rank", width=80, anchor="center")
        self.tree.column("nick", width=250, anchor="w")
        self.tree.column("matric", width=180, anchor="center")
        self.tree.column("score", width=220, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=5)
        
        back_btn = tk.Button(self, text="⬅ Back Hub", command=lambda: controller.show_page("DashboardFrame"))
        comp.apply_modern_button(back_btn, cfg.COLOR_AMBER)
        back_btn.pack(pady=20)

    def on_render_refresh(self):
        for record in self.tree.get_children():
            self.tree.delete(record)
            
        # Aggregate scores from hardware registry
        records = self.controller.db_manager.read_all_hardware_records()
        user_scores = {}
        
        for row in records:
            donor_id = row[7]
            score = float(row[5])
            user_scores[donor_id] = user_scores.get(donor_id, 0) + score
            
        # Match with nicknames
        users = self.controller.db_manager.read_all_users()
        nick_map = {u[0]: u[3] for u in users}
        
        sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (uid, score) in enumerate(sorted_scores, 1):
            nick = nick_map.get(uid, "Unknown")
            self.tree.insert("", "end", values=(i, nick, uid, round(score, 2)))
            
        if sorted_scores:
            top_uid, top_score = sorted_scores[0]
            top_nick = nick_map.get(top_uid, "Unknown")
            self.champ_label.config(text=f"🥇 Active Student Eco-Champion: {top_nick} [{round(top_score, 2)} Impact Points] 🥇")

# ==========================================
# LOCAL STANDALONE TEST RUNNER LOOP
# ==========================================
if __name__ == "__main__":
    print("--- Running Isolated Member 1 Navigation Shell Test ---")
    app = NavigationController()
    # We will close it immediately to confirm instantiation without errors in a headless environment
    app.after(100, app.destroy) 
    app.mainloop()
    print("Navigation Controller Initialized Successfully!")
