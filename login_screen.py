# login_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
import re
from main_menu import MainMenu

class LoginScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.email = None  # Store email for later use
        self.setup_ui()
        
    def setup_ui(self):
        # Background
        bg_image = tk.PhotoImage(file=r"D:\SQL\porject\porject\Background.png")
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image

        # Title and labels
        tk.Label(self, text="Login", font=("Bradley Hand", 70, "bold"), fg="white", bg="#333333").place(x=400, y=100)
        tk.Label(self, text="Welcome Back", font=("Bradley Hand", 30, "bold"), fg="white", bg="#333333").place(x=400, y=230)
        tk.Label(self, text="Sign in with your email address.", font=("Bradley Hand", 30), fg="white", bg="#333333").place(x=400, y=300)

        # Email entry
        tk.Label(self, text="Email Address:", font=("Bradley Hand", 20), bg="#333333", fg="white").place(x=400, y=370)
        self.email_entry = ttk.Entry(self, width=40, font=("Bradley Hand", 20, "bold"))
        self.email_entry.place(x=400, y=420)

        # Sign in button
        tk.Button(
            self, text="Sign In", font=("Bradley Hand", 30, "bold"), 
            bg="#3CB371", fg="white", width=20, height=1, 
            command=self.validate_email
        ).place(x=400, y=500)
    
    def validate_email(self):
        email = self.email_entry.get().strip()
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_pattern, email):
            messagebox.showerror("Input Error", "Please enter a valid email address")
        else:
            self.parent.email = email  # Store email for later use
            self.pack_forget()
            MainMenu(self.parent)
