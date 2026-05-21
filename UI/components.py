# ui/components.py
import tkinter as tk
from tkinter import ttk
import sys
import os

# Ensure the project root is in the path for standalone execution
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    import config as cfg
except Exception:
    import config as cfg

def create_header_banner(parent, text, bg_color):
    """Generates a clean, modern, flat application header banner."""
    banner = tk.Label(
        parent, 
        text=text, 
        bg=bg_color, 
        fg="white", 
        font=("Helvetica", 13, "bold"), 
        pady=14
    )
    return banner

def apply_modern_button(btn, bg_color):
    """Styles a standard Tkinter button into a flat, modern UI element."""
    btn.config(
        bg=bg_color,
        fg="white",
        font=("Helvetica", 10, "bold"),
        activebackground=bg_color,
        activeforeground="white",
        bd=0,
        padx=15,
        pady=6,
        cursor="hand2"
    )

def create_form_entry(parent, label_text):
    """Creates a unified, clean label-and-entry container block."""
    frame = tk.Frame(parent, bg=cfg.CARD_BG)
    
    label = tk.Label(
        frame, 
        text=label_text, 
        font=("Helvetica", 10, "bold"), 
        fg=cfg.TEXT_MAIN, 
        bg=cfg.CARD_BG
    )
    label.pack(anchor="w", pady=(5, 2))
    
    entry = tk.Entry(
        frame, 
        font=("Helvetica", 11), 
        fg=cfg.TEXT_MAIN, 
        bg="#f1f5f9", 
        bd=1, 
        relief="flat",
        width=35
    )
    entry.pack(fill="x", ipady=4)
    
    return frame, entry

def configure_treeview_theme():
    """Configures the native ttk.Treeview styles to look professional and legible."""
    style = ttk.Style()
    style.theme_use("clam") # Switch to a clean baseline engine
    
    # Configure Table Headers
    style.configure(
        "Treeview.Heading",
        background="#e2e8f0",
        foreground=cfg.TEXT_MAIN,
        font=("Helvetica", 10, "bold"),
        relief="flat",
        padding=6
    )
    
    # Configure Table Rows
    style.configure(
        "Treeview",
        background=cfg.CARD_BG,
        foreground=cfg.TEXT_MAIN,
        rowheight=28,
        fieldbackground=cfg.CARD_BG,
        font=("Helvetica", 10)
    )
    
    # Configure selection highlights
    style.map(
        "Treeview",
        background=[("selected", "#cbd5e1")],
        foreground=[("selected", cfg.TEXT_MAIN)]
    )

# ==========================================
# LOCAL STANDALONE TEST RUNNER LOOP
# ==========================================
if __name__ == "__main__":
    print("--- Running Isolated UI Components Test ---")
    root = tk.Tk()
    root.title("Component Lab")
    root.geometry("400x300")
    root.configure(bg=cfg.BG_PRIMARY)
    
    banner = create_header_banner(root, "Component Testing", cfg.COLOR_GREEN)
    banner.pack(fill="x")
    
    frame, entry = create_form_entry(root, "Test Entry:")
    frame.pack(pady=20)
    
    btn = tk.Button(root, text="Modern Button")
    apply_modern_button(btn, cfg.COLOR_BLUE)
    btn.pack()
    
    root.after(100, root.destroy)
    root.mainloop()
    print("UI Components Initialized Successfully!")
