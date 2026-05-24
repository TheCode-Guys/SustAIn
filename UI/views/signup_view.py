# UI/views/signup_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import config as cfg

class SignupFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=cfg.BG_PRIMARY)
        self.controller = controller
        
        # 1. INTRODUCE A SCROLLABLE CANVAS CONTAINER
        container = tk.Frame(self, bg=cfg.BG_PRIMARY)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=cfg.BG_PRIMARY, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # 2. MOUNT THE SCROLLABLE CONTENT VIEW
        self.scrollable_content = tk.Frame(canvas, bg=cfg.BG_PRIMARY)
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")

        # 3. CONFIGURE DYNAMIC SCROLL BOUNDS & WINDOW RESIZING
        self.scrollable_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # 4. ENABLE MOUSE WHEEL SCROLLING
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # --- CONTENT LAYOUT (Re-parented to self.scrollable_content) ---
        sidebar = tk.Frame(self.scrollable_content, bg=cfg.SIDEBAR_LIGHT, width=320)
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

        form_container = tk.Frame(self.scrollable_content, bg=cfg.BG_PRIMARY, padx=60)
        form_container.pack(side="left", fill="both", expand=True)
        
        center_box = tk.Frame(form_container, bg=cfg.BG_PRIMARY)
        center_box.pack(anchor="center", expand=True, fill="x", pady=50)
        
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
