# UI/views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import config as cfg

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        # Sidebar panel
        sidebar = tk.Frame(self, bg=cfg.SIDEBAR_LIGHT, width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False) 
        
        try:
            self.raw_img = Image.open("images/logo.jpeg")
            # Resize image
            w, h = self.raw_img.size
            small_pil = self.raw_img.resize((w//4, h//4), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(small_pil)
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

        # Right form area
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
            # Show error if validation fails
            messagebox.showerror("Error", "Please enter your email and password.")
            return
            
        success, result = self.controller.auth_manager.authenticate_student(email, password)
        
        if success:
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
            messagebox.showerror("Login Failed", result)

    def on_render_refresh(self):
        """Reset fields."""
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
