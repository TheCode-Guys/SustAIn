# main.py
from UI.navigation import NavigationController

if __name__ == "__main__":
    # 1. Initialize your master navigation framework
    app = NavigationController()
    
    # 2. Start the Tkinter event loop to display the window
    app.mainloop()