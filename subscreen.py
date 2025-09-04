# subscreen.py
import tkinter as tk
from tkinter import ttk
from database import DatabaseManager
from image_list_screen import ImageListScreen

class SubScreen(tk.Frame):
    def __init__(self, parent, country_index):
        super().__init__(parent)
        self.parent = parent
        self.country_index = country_index
        self.db = DatabaseManager()
        self.setup_ui()
        self.pack(fill=tk.BOTH, expand=True)
        
    def setup_ui(self):
        # Load background image
        bg_image = tk.PhotoImage(file=r"D:\SQL\porject\porject\Background.png")
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image

        # Get country info
        countries = self.db.get_countries()
        country_ids = list(countries.keys())

        if self.country_index < len(country_ids):
            country_id = country_ids[self.country_index]
            country_name = countries.get(country_id, f"Country {self.country_index + 1}")
        else:
            country_id = None
            country_name = f"Invalid Country Index {self.country_index}"

        # Title
        title_label = tk.Label(
            self,
            text=f"{country_name} Traditional Cuisine",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Menu buttons
        categories = [
            ('BF', 'Breakfast'),
            ('L', 'Lunch'),
            ('D', 'Dinner'),
            ('DS', 'Desserts')
        ]

        for i, (category_id, category_name) in enumerate(categories):
            btn = tk.Button(
                self,
                text=category_name,
                font=("Arial", 16, "bold"),
                bg="#3CB371",
                fg="white",
                width=20,
                height=5,
                command=lambda cid=category_id: self.open_category(cid)
            )
            row = i // 2 + 1
            col = i % 2
            btn.grid(row=row, column=col, padx=40, pady=40, sticky="n")

        # Back button
        back_btn = tk.Button(
            self,
            text="Back",
            font=("Arial", 12),
            bg="gray",
            fg="white",
            width=15,
            height=2,
            command=self.go_back
        )
        back_btn.grid(row=5, column=0, columnspan=2, pady=30)

        # Configure grid
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
    
    def open_category(self, category_id):
        country_ids = list(self.db.get_countries().keys())
        if self.country_index < len(country_ids):
            current_country = country_ids[self.country_index]
            self.pack_forget()
            ImageListScreen(self.parent, current_country, category_id)
        else:
            print("Invalid country index")

    def go_back(self):
        self.pack_forget()
        from main_menu import MainMenu
        MainMenu(self.parent)
