# UI/views/donation_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import config as cfg
import UI.components as comp
from src.scrap_item import ScrapItem, BatteryScrapItem, PCBScrapItem
from src.database_manager import validate_scrap_donation_data
from UI.navigation_sidebar import setup_sliding_sidebar

class DonationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "DonationFrame")
        
        tk.Label(self.right_workspace, text="Book / Donate E-Waste Scrap", font=("Helvetica", 18, "bold"), fg=cfg.TEXT_MAIN, bg=cfg.BG_PRIMARY).pack(anchor="w", padx=30, pady=(20, 20))
        
        form_frame = tk.Frame(self.right_workspace, bg="#F3FAF6", padx=30, pady=25)
        form_frame.pack(anchor="w", padx=30, fill="x")
        
        # 1. Hardware Item Details
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

        # --- NEW FIELD: Damage State Selector Dropdown ---
        tk.Label(form_frame, text="⚙️  Current Hardware Condition / Damage State:", font=("Helvetica", 10, "bold"), bg="#F3FAF6", fg=cfg.TEXT_MAIN).pack(anchor="w", pady=(5, 2))
        
        self.condition_options = [
            "Fully Functional",
            "Minor Repair Required",
            "Scrap / Raw Parts"
        ]
        self.selected_condition = tk.StringVar(self)
        self.selected_condition.set(self.condition_options[0]) # Default option
        
        self.condition_dropdown = tk.OptionMenu(form_frame, self.selected_condition, *self.condition_options)
        self.condition_dropdown.config(font=("Helvetica", 10), bg="#f1f5f9", fg=cfg.TEXT_MAIN, bd=0, relief="flat", activebackground="#f1f5f9")
        self.condition_dropdown.pack(fill="x", ipady=4, pady=(0, 15))

        # 2. Donor Coordination Details
        self.f3, self.phone_entry = comp.create_form_entry(form_frame, "Donor Contact Phone Number:")
        self.f3.pack(fill="x", pady=5)

        self.f5, self.pickup_entry = comp.create_form_entry(form_frame, "Exact Campus Pickup Location (e.g. SST Lab 1):")
        self.f5.pack(fill="x", pady=5)
        
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
        donor_phone = self.phone_entry.get().strip()
        # Automatically retrieve donor email from the active session credentials
        donor_email = self.controller.current_user.get("email", "unknown@pau.edu.ng")
        pickup_location = self.pickup_entry.get().strip()
        condition = self.selected_condition.get()
        
        # 1. Enforce data verification filters (Member 4 implementation)
        is_valid, error_msg = validate_scrap_donation_data(
            name, category, weight_str, donor_phone, donor_email, pickup_location
        )

        if not is_valid:
            messagebox.showwarning("Data Verification Alert", error_msg)
            return
            
        weight = float(weight_str)

        # 2. Choose the right OOP class based on category
        if "Battery" in category:
            item = BatteryScrapItem(None, name, category, weight, condition, donor_phone)
        elif "Circuit" in category or "PCBs" in category:
            item = PCBScrapItem(None, name, category, weight, condition, donor_phone)
        else:
            item = ScrapItem(None, name, category, weight, condition, donor_phone)
            
        score = item.calculate_impact_score()

        # 3. Save to CSV via DatabaseManager with coordination columns
        item_id = self.controller.db_manager.save_new_donation(
            name, category, weight, condition, score, 
            donor_phone, donor_email, pickup_location, self.image_path
        )
        
        messagebox.showinfo("Donation Success", f"Item Logged Successfully!\nEco-Impact Score: {score}")
        self.controller.show_page("DashboardFrame")

    def on_render_refresh(self):
        self.name_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.pickup_entry.delete(0, tk.END)
        self.cat_var.set(self.categories[0])
        self.selected_condition.set(self.condition_options[0])
        self.image_path = "images/default.png"
        self.img_label.config(text="No file selected (Default will be used)", fg=cfg.TEXT_MUTED)

