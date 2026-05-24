# UI/views/profile_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import config as cfg
from UI.navigation_sidebar import setup_sliding_sidebar

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        setup_sliding_sidebar(self, "ProfileFrame")
        
        # Top profile header
        user_card = tk.Frame(self.right_workspace, bg="#EBF4F0", padx=20, pady=15)
        user_card.pack(fill="x", padx=20, pady=(20, 10))
        
        avatar_box = tk.Frame(user_card, bg="#D4E6DC", width=75, height=75)
        avatar_box.pack(side="left")
        avatar_box.pack_propagate(False)
        
        avatar_lbl = tk.Label(avatar_box, text="👤", font=("Arial", 32), bg="#D4E6DC", fg="#3A7D5B")
        avatar_lbl.pack(expand=True)
        
        info_pane = tk.Frame(user_card, bg="#EBF4F0")
        info_pane.pack(side="left", padx=20, anchor="w")
        
        self.name_lbl = tk.Label(info_pane, text="User Name", font=("Helvetica", 18, "bold"), fg="#2C3E35", bg="#EBF4F0")
        self.name_lbl.pack(anchor="w")
        
        self.sub_lbl = tk.Label(info_pane, text="Student Guardian", font=("Helvetica", 11), fg="#5A6E63", bg="#EBF4F0")
        self.sub_lbl.pack(anchor="w", pady=(2, 0))
        
        stats_pane = tk.Frame(user_card, bg="#EBF4F0")
        stats_pane.pack(side="right", anchor="center")
        
        p_box = tk.Frame(stats_pane, bg="#D4E6DC", padx=20, pady=10, width=110, height=65)
        p_box.pack(side="left", padx=8)
        p_box.pack_propagate(False)
        tk.Label(p_box, text="Eco-Points", font=("Helvetica", 8, "bold"), fg="#5A6E63", bg="#D4E6DC").pack()
        self.pts_val = tk.Label(p_box, text="0.00", font=("Helvetica", 14, "bold"), fg="#3A7D5B", bg="#D4E6DC")
        self.pts_val.pack(pady=(2, 0))
        
        i_box = tk.Frame(stats_pane, bg="#D4E6DC", padx=10, pady=10, width=110, height=65)
        i_box.pack(side="left", padx=8)
        i_box.pack_propagate(False)
        tk.Label(i_box, text="Items Logged", font=("Helvetica", 8, "bold"), fg="#5A6E63", bg="#D4E6DC").pack()
        self.item_count_val = tk.Label(i_box, text="0", font=("Helvetica", 14, "bold"), fg="#3A7D5B", bg="#D4E6DC")
        self.item_count_val.pack(pady=(2, 0))

        # Tabs
        tab_bar = tk.Frame(self.right_workspace, bg=cfg.BG_PRIMARY)
        tab_bar.pack(fill="x", padx=20, pady=(10, 0))
        
        self.btn_owned = tk.Button(
            tab_bar, text="MY DONATIONS", font=("Helvetica", 10, "bold"), 
            bd=0, relief="flat", cursor="hand2", activebackground="#2D7A51", activeforeground="white"
        )
        self.btn_owned.pack(side="left", expand=True, fill="x", ipady=10)
        self.btn_owned.config(command=lambda: self.switch_list_view("owned"))
        
        self.btn_requested = tk.Button(
            tab_bar, text="MY CLAIMS", font=("Helvetica", 10), 
            bd=0, relief="flat", cursor="hand2", activebackground="#D1DCD6", activeforeground="#5A6E63"
        )
        self.btn_requested.pack(side="left", expand=True, fill="x", ipady=10)
        self.btn_requested.config(command=lambda: self.switch_list_view("requested"))

        # Table
        self.table_frame = tk.Frame(self.right_workspace, bg=cfg.BG_PRIMARY)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ("id", "name", "category", "weight", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)
        
        self.tree.heading("id", text="Item ID")
        self.tree.heading("name", text="Description")
        self.tree.heading("category", text="Category")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=300, anchor="w")
        self.tree.column("category", width=220, anchor="w")
        self.tree.column("weight", width=110, anchor="center")
        self.tree.column("status", width=110, anchor="center")
        
        self.current_tab = "owned"
        self.tray = tk.Frame(self.right_workspace, bg="#f1f5f9", pady=15, padx=20)
        self.tray.pack(fill="x", side="bottom")

    def switch_list_view(self, target_tab):
        """Toggle views."""
        self.current_tab = target_tab
        
        if target_tab == "owned":
            self.btn_owned.config(bg="#2D7A51", fg="white", font=("Helvetica", 10, "bold"))
            self.btn_requested.config(bg="#CDDAD2", fg="#5A6E63", font=("Helvetica", 10))
        else:
            self.btn_owned.config(bg="#CDDAD2", fg="#5A6E63", font=("Helvetica", 10))
            self.btn_requested.config(bg="#2D7A51", fg="white", font=("Helvetica", 10, "bold"))
            
        self.load_profile_table_rows()

    def load_profile_table_rows(self):
        """Populate table."""
        for record in self.tree.get_children():
            self.tree.delete(record)
            
        current_user_id = self.controller.current_user.get("matric_id")
        all_items = self.controller.db_manager.get_all_registry_items_dict()
        
        total_p = 0.0
        for row in all_items:
            is_match = False
            if self.current_tab == "owned":
                if str(row.get("donor_phone", "")).strip() == str(current_user_id).strip():
                    is_match = True
                    total_p += float(row.get("impact_score", 0))
            else:
                if str(row.get("claimer_id", "")).strip() == str(current_user_id).strip():
                    is_match = True
            
            if is_match:
                self.tree.insert("", "end", values=(
                    row.get("id"),
                    row.get("item_name"),
                    row.get("category"),
                    f"{row.get('weight')} kg",
                    row.get("status")
                ))
        
        self.pts_val.config(text=f"{round(total_p, 2)}")
        self.item_count_val.config(text=str(len(self.tree.get_children())))

    def on_render_refresh(self):
        """Update profile."""
        user_data = self.controller.current_user
        
        if isinstance(user_data, dict):
            user_nick = user_data.get("username", user_data.get("nickname", "Olu Tunde"))
        else:
            user_nick = str(user_data)
        
        self.name_lbl.config(text=user_nick)
        self.sub_lbl.config(text="Student Guardian")
        
        self.switch_list_view("owned")
