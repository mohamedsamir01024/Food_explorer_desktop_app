# main.py
import tkinter as tk
from tkinter import messagebox
from login_screen import LoginScreen
from database import DatabaseManager

class FoodExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Explorer App")
        self.geometry("1489x840")
        self.resizable(True, True)
        self.email = None  # To store logged in user's email
        
        # Initialize database connection
        self.db_manager = DatabaseManager()
        if not self.db_manager.test_connection():
            messagebox.showerror("Database Error", 
                               "Failed to connect to the database. Please check your connection settings.")
            self.destroy()
            return
        
        # Start with login screen
        self.login_screen = LoginScreen(self)
        self.login_screen.pack(fill=tk.BOTH, expand=True)

def main():
    app = FoodExplorerApp()
    app.mainloop()

if __name__ == "__main__":
    main()