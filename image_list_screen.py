# image_list_screen.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from database import DatabaseManager
from final_image_screen import FinalImageScreen

class ImageListScreen(tk.Frame):
    def __init__(self, parent, country_id, category_id):
        super().__init__(parent)
        self.parent = parent
        self.country_id = country_id
        self.category_id = category_id
        self.db = DatabaseManager()
        self.setup_ui()
        self.pack(fill=tk.BOTH, expand=True)
        
    def setup_ui(self):
        # Background
        bg_image = tk.PhotoImage(file=r"D:\SQL\porject\porject\Background.png")
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image

        # Container for meals
        container = tk.Frame(self, bg="white")
        container.pack(pady=40)

        # Get meals from database
        meals = self.db.get_meals_by_country_category(self.country_id, self.category_id)
        
        # Display each meal
        for i, meal in enumerate(meals):
            meal_id, meal_name, difficulty, cook_time = meal
            frame = tk.Frame(container, bg="white")
            frame.grid(row=0, column=i, padx=10)
            
            # Meal image (first image from gallery)
            images = self.db.get_meal_images(meal_id)
            if images:
                try:
                    img = Image.open(images[0])
                    img = img.resize((200, 150), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(frame, image=photo)
                    img_label.image = photo
                except Exception as e:
                    img_label = tk.Label(frame, text=f"Image {i+1}", bg="lightgray", width=20, height=10)
            else:
                img_label = tk.Label(frame, text=f"Image {i+1}", bg="lightgray", width=20, height=10)
            
            img_label.pack(pady=10)
            
            # Meal name and info
            info_label = tk.Label(
                frame, 
                text=f"{meal_name}\nDifficulty: {difficulty}\nTime: {cook_time} min",
                bg="white"
            )
            info_label.pack()
            
            # View button
            view_button = tk.Button(
                frame, 
                text="View Details", 
                command=lambda mid=meal_id: self.open_meal_details(mid)
            )
            view_button.pack()

        # Back button
        back_btn = tk.Button(
            self,
            text="Back",
            command=self.go_back,
            bg="gray",
            fg="white",
            width=10,
            height=2
        )
        back_btn.pack(pady=30)
    
    def open_meal_details(self, meal_id):
        self.pack_forget()
        FinalImageScreen(self.parent, meal_id)
    
    def go_back(self):
        self.pack_forget()
        from subscreen import SubScreen
        countries = list(self.db.get_countries().keys())
        country_index = countries.index(self.country_id)
        SubScreen(self.parent, country_index)