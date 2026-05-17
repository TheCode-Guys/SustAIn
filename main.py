# main.py
import tkinter as tk
from tkinter import messagebox
import psycopg2  

class SustAIn(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SustAIn: The Circular Economy Guardian")
        self.geometry("900x600")
        
        # Globally shared user variables (Simple variables, no complex state management)
        self.current_user_id = ""
        self.user_nickname = "Community Member"
        
        # Main application frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Simple label showing the app initialized
        self.info_label = tk.Label(
            self.main_frame, 
            text="SustAIn Core Initialized.\nReady for Team Vorbis module integration.",
            font=("Arial", 12)
        )
        self.info_label.pack(pady=50)

if __name__ == "__main__":
    app = SustAIn()
    app.mainloop()