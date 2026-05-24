# UI/views/landing_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import config as cfg

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
