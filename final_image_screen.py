import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import DatabaseManager

class FinalImageScreen(tk.Frame):
    def __init__(self, parent, meal_id):
        super().__init__(parent)
        self.parent = parent
        self.meal_id = meal_id
        self.db = DatabaseManager()
        self.current_image_index = 0
        self.images = []
        self.rating_var = tk.IntVar(value=0)
        self.setup_ui()
        self.pack(fill=tk.BOTH, expand=True)
        
    def setup_ui(self):
        # Background
        bg_image = tk.PhotoImage(file=r"D:\SQL\porject\porject\Background.png")
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image

        # Get meal details
        meal_details = self.get_meal_details()
        ingredients = self.db.get_ingredients(self.meal_id)
        ratings = self.db.get_ratings(self.meal_id)
        self.images = self.db.get_meal_images(self.meal_id)

        # Main container
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Left side - Image and navigation
        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Image display
        self.img_label = tk.Label(left_frame, bg="lightgray", width=200, height=200)
        self.img_label.pack(pady=10)
        self.show_current_image()

        # Navigation buttons
        nav_frame = tk.Frame(left_frame, bg="white")
        nav_frame.pack(pady=10)

        # Right side - Details
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Meal details
        details_label = tk.Label(
            right_frame,
            text=f"{meal_details['name']}\n\n"
                 f"Difficulty: {meal_details['difficulty']}\n"
                 f"Cooking Time: {meal_details['cook_time']} minutes",
            font=("Arial", 14),
            bg="white",
            justify=tk.LEFT
        )
        details_label.pack(anchor=tk.W, pady=10)

        # Ingredients
        ingredients_label = tk.Label(
            right_frame,
            text="Ingredients:",
            font=("Arial", 12, "bold"),
            bg="white",
            justify=tk.LEFT
        )
        ingredients_label.pack(anchor=tk.W, pady=(20,5))

        ingredients_text = "\n".join(
            [f"- {ing[0]}: {ing[1]} {ing[2]}" for ing in ingredients]
        )
        ingredients_display = tk.Label(
            right_frame,
            text=ingredients_text,
            font=("Arial", 11),
            bg="white",
            justify=tk.LEFT
        )
        ingredients_display.pack(anchor=tk.W)

        # Ratings
        ratings_label = tk.Label(
            right_frame,
            text="Ratings & Reviews:",
            font=("Arial", 12, "bold"),
            bg="white",
            justify=tk.LEFT
        )
        ratings_label.pack(anchor=tk.W, pady=(20,5))

        if ratings:
            for rating in ratings:
                rating_text = f"{'★' * rating[0]}{'☆' * (5-rating[0])} by {rating[2]}\n{rating[1]}\n"
                rating_label = tk.Label(
                    right_frame,
                    text=rating_text,
                    font=("Arial", 10),
                    bg="white",
                    justify=tk.LEFT
                )
                rating_label.pack(anchor=tk.W, pady=2)
        else:
            no_ratings = tk.Label(
                right_frame,
                text="No ratings yet",
                font=("Arial", 10),
                bg="white",
                justify=tk.LEFT
            )
            no_ratings.pack(anchor=tk.W)

        # Rating selection
        rating_frame = tk.Frame(right_frame, bg="white")
        rating_frame.pack(anchor=tk.W, pady=(10, 0))
        tk.Label(rating_frame, text="Your Rating:", font=("Arial", 11), bg="white").pack(side=tk.LEFT)
        for i in range(1, 6):
            tk.Radiobutton(
                rating_frame,
                text=str(i),
                variable=self.rating_var,
                value=i,
                bg="white"
            ).pack(side=tk.LEFT, padx=2)

        # Text field for review
        review_label = tk.Label(right_frame, text="Your Review:", font=("Arial", 11), bg="white")
        review_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.review_text = tk.Text(right_frame, height=3, width=40)
        self.review_text.pack(pady=(0, 10))
        
        # User email entry
        email_frame = tk.Frame(right_frame, bg="white")
        email_frame.pack(anchor=tk.W, pady=(5, 5))
        tk.Label(email_frame, text="Your Email:", font=("Arial", 11), bg="white").pack(side=tk.LEFT)
        self.email_entry = tk.Entry(email_frame, width=30)
        self.email_entry.pack(side=tk.LEFT, padx=5)

        # Submit Rating Button
        submit_rating_btn = tk.Button(
            right_frame,
            text="Submit Rating",
            command=self.submit_rating,
            bg="#3CB371",
            fg="white",
            width=15
        )
        submit_rating_btn.pack(pady=(10, 0))

        # Back button (relocated)
        back_btn = tk.Button(
            right_frame,
            text="Back",
            command=self.go_back,
            bg="gray",
            fg="white",
            width=10,
            height=2
        )
        back_btn.pack(pady=30)

    def get_meal_details(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT m.Name, m.Difficulty_Level, m.Cooking_Time, c.Name 
                    FROM foods.Meal m
                    JOIN foods.Country c ON m.Country_ID = c.Country_ID
                    WHERE m.Meal_ID = ?
                """, self.meal_id)
                row = cursor.fetchone()
                return {
                    'name': row[0],
                    'difficulty': row[1],
                    'cook_time': row[2],
                    'country': row[3]
                }
            except Exception as e:
                print(f"Error fetching meal details: {e}")
                return {
                    'name': "Meal",
                    'difficulty': "Medium",
                    'cook_time': 30,
                    'country': "Country"
                }
            finally:
                conn.close()
        return {
            'name': "Meal",
            'difficulty': "Medium",
            'cook_time': 30,
            'country': "Country"
        }

    def show_current_image(self):
        if self.images and 0 <= self.current_image_index < len(self.images):
            try:
                img = Image.open(self.images[self.current_image_index])
                img = img.resize((400, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.img_label.config(image=photo)
                self.img_label.image = photo
            except Exception as e:
                self.img_label.config(text=f"Image {self.current_image_index+1}")
        else:
            self.img_label.config(text="No Image Available")

    def show_next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_current_image()

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_current_image()

    def submit_rating(self):
        rating = self.rating_var.get()
        if rating == 0:
            messagebox.showwarning("Rating Required", "Please select a rating from 1 to 5 stars")
            return
            
        # Get review from the text field
        review = self.review_text.get("1.0", tk.END).strip()
        
        # Get email from the entry field
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Email Required", "Please enter your email")
            return
        
        try:
            result = self.submit_feedback(email, self.meal_id, rating, review)
            
            if result:
                messagebox.showinfo("Success", "Thank you for your rating!")
                # Clear the input fields
                self.rating_var.set(0)
                self.review_text.delete("1.0", tk.END)
                # Refresh the ratings display
                self.pack_forget()
                self.__init__(self.parent, self.meal_id)
            else:
                messagebox.showerror("Error", "Failed to submit rating. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"Exception in submit_rating: {e}")

    def submit_feedback(self, email, meal_id, rating, review=""):
        conn = self.db.get_connection()
        if not conn:
            print("Database connection failed")
            return False
    
        try:
            cursor = conn.cursor()
    
            # Get User_ID and Country_ID from email and meal
            cursor.execute("SELECT User_ID FROM users.[User] WHERE Email = ?", (email,))
            user_row = cursor.fetchone()
            if not user_row:
                print(f"No user found with email {email}")
                messagebox.showwarning("User Not Found", "Email not found in our system. Please check your email or register first.")
                return False
            user_id = user_row[0]
    
            cursor.execute("SELECT Country_ID FROM foods.Meal WHERE Meal_ID = ?", (meal_id,))
            country_row = cursor.fetchone()
            if not country_row:
                print(f"No meal found with ID {meal_id}")
                return False
            country_id = country_row[0]
    
            # Check if user has already rated this meal
            cursor.execute("""
                SELECT Rating_ID FROM users.Rating 
                WHERE User_ID = ? AND Meal_ID = ?
            """, (user_id, meal_id))
            existing_rating = cursor.fetchone()
            
            if existing_rating:
                # Update existing rating
                cursor.execute("""
                    UPDATE users.Rating 
                    SET Rating = ?, Review = ?
                    WHERE User_ID = ? AND Meal_ID = ?
                """, (rating, review, user_id, meal_id))
            else:
                # Insert new rating
                cursor.execute("""
                    INSERT INTO users.Rating (Rating, Review, User_ID, Meal_ID, Country_ID)
                    VALUES (?, ?, ?, ?, ?)
                """, (rating, review, user_id, meal_id, country_id))
            
            conn.commit()
            return True
    
        except Exception as e:
            print(f"Error in submit_feedback: {e}")
            return False
    
        finally:
            conn.close()

    def go_back(self):
        self.pack_forget()
        from image_list_screen import ImageListScreen
        meal_details = self.get_meal_details()
        countries = list(self.db.get_countries().keys())
        country_id = [k for k, v in self.db.get_countries().items() if v == meal_details['country']][0]

        # Determine category from meal_id prefix
        category_id = self.meal_id[2:4]  # Extract category from meal_id (e.g., 'BF' from 'ITBF1')
        ImageListScreen(self.parent, country_id, category_id)