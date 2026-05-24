# UI/views/claim_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import config as cfg
from UI.navigation_sidebar import setup_sliding_sidebar

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

        # Bottom Action Bar Tray for claiming items
        claim_tray = tk.Frame(self.right_workspace, bg="#f1f5f9", pady=15, padx=20)
        claim_tray.pack(fill="x", side="bottom")
        
        btn_claim = tk.Button(
            claim_tray, text="🤝  Request / Claim Selection", font=("Helvetica", 10, "bold"), 
            bg=cfg.COLOR_BLUE, fg="white", bd=0, cursor="hand2", padx=25, pady=8,
            command=self.process_active_claim
        )
        btn_claim.pack(side="right")

    def process_active_claim(self):
        """Captures selected item row, target the registry dictionary, and triggers the Handshake Protocol."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an item from the table first.")
            return
            
        item_values = self.tree.item(selected[0], "values")
        item_id = item_values[0]
        hardware_name = item_values[1]
        
        # 1. Retrieve full item record from backend
        db_items = self.controller.db_manager.get_all_registry_items_dict()
        item_data = next((item for item in db_items if str(item['id']) == str(item_id)), None)
        
        if not item_data:
            messagebox.showerror("Error", "Could not retrieve asset data from registry.")
            return

        # 2. Extract coordination properties
        donor_phone = item_data.get("donor_phone", "N/A")
        donor_email = item_data.get("donor_email", "N/A")
        pickup_venue = item_data.get("pickup_location", "N/A")
        
        # 3. Commit the claim to storage
        claimer_id = self.controller.current_user.get("matric_id", "Guest")
        success = self.controller.db_manager.update_item_to_claimed(
            item_id=item_id, 
            claimer_id=claimer_id, 
            claimer_intent="Educational Reuse / Lab Research"
        )
        
        if success:
            # 4. Display the informative Coordination Dialog Pop-up
            coordination_msg = (
                f"🎉 Hardware Claim Confirmed!\n\n"
                f"Core Product Info:\n"
                f"-------------------\n"
                f"Item ID: {item_id}\n"
                f"Hardware Model: {hardware_name}\n\n"
                f"Donor Coordination Details:\n"
                f"---------------------------\n"
                f"Donor Phone: {donor_phone}\n"
                f"Donor Email: {donor_email}\n\n"
                f"Logistics / Fulfillment:\n"
                f"---------------------------\n"
                f"Designated Campus Pickup Venue: {pickup_venue}\n\n"
                f"Instructions:\n"
                f"Please copy the contact credentials above and coordinate a physical handoff with the donor at the specified venue."
            )
            messagebox.showinfo("Handshake Exchange Protocol", coordination_msg)
            
            # 5. Immediately trigger life-cycle sync to hide claimed item
            self.on_render_refresh()
        else:
            messagebox.showerror("Claim Error", "Item could not be claimed. It might have already been processed.")

    def on_item_selected(self, event):
        selected = self.tree.selection()
        if not selected: return
        iid = self.tree.item(selected[0])['values'][0]
        db_items = self.controller.db_manager.get_all_registry_items_dict()
        data = next((item for item in db_items if str(item['id']) == str(iid)), None)
        
        if data:
            self.item_name_lbl.config(text=data['item_name'])
            meta_text = f"Category: {data['category']}\nCondition: {data['damage_state']}\nPoints: {data.get('impact_score', '0')} pts"
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
        # Redirect to the main process_active_claim for consistency
        self.process_active_claim()

    def load_rows(self):
        for record in self.tree.get_children(): self.tree.delete(record)
        q = self.search_var.get().strip().lower()
        cat = self.selected_cat_var.get()
        records = self.controller.db_manager.read_all_hardware_records()
        for row in records:
            # Ensure index 6 is status (Available) and index 2 is category
            if len(row) > 6 and row[6] == "Available" and (not q or q in str(row[1]).lower()) and (cat == "All Categories" or str(row[2]) == cat):
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[5]))

    def on_render_refresh(self):
        self.search_var.set(""); self.selected_cat_var.set(self.cat_options[0])
        self.load_rows()
        self.item_name_lbl.config(text="No Item Selected"); self.btn_claim_now.config(state="disabled")
