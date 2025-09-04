import pyodbc
from PIL import Image, ImageTk
import io
import time
import traceback
from db_config import DatabaseConfig

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.conn_str = DatabaseConfig.get_connection_string()
        self.conn = self.get_connection()
        self._initialized = True

    def get_connection(self):
        try:
            return pyodbc.connect(self.conn_str)
        except Exception as e:
            print(f"Database connection failed: {e}")
            return None

    def test_connection(self):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                return True
            except Exception as e:
                print(f"Connection test failed: {e}")
                return False
            finally:
                conn.close()
        return False

    def get_countries(self):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Country_ID, Name FROM foods.Country")
                return {row[0]: row[1] for row in cursor}
            except Exception as e:
                print(f"Error fetching countries: {e}")
                return {}
            finally:
                conn.close()
        return {}

    def get_meals_by_country_category(self, country_id, category_id):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT Meal_ID, Name, Difficulty_Level, Cooking_Time 
                    FROM foods.Meal 
                    WHERE Country_ID = ? AND Category_ID = ?
                """, (country_id, category_id))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching meals: {e}")
                return []
            finally:
                conn.close()
        return []

    def get_meal_images(self, meal_id):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Image_Url FROM foods.Image_Gallery WHERE Meal_ID = ?", (meal_id,))
                return [row[0] for row in cursor]
            except Exception as e:
                print(f"Error fetching images: {e}")
                return []
            finally:
                conn.close()
        return []

    def get_ingredients(self, meal_id):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT Name, Quantity, Unit 
                    FROM foods.Ingredients 
                    WHERE Meal_ID = ?
                    ORDER BY Name
                """, (meal_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching ingredients: {e}")
                return []
            finally:
                conn.close()
        return []

    def get_ratings(self, meal_id):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.Rating, r.Review, u.Email 
                    FROM users.Rating r
                    JOIN users.[User] u ON r.User_ID = u.User_ID
                    WHERE r.Meal_ID = ?
                    ORDER BY r.Rating DESC
                """, (meal_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching ratings: {e}")
                return []
            finally:
                conn.close()
        return []

def submit_feedback(self, email, meal_id, rating, review):
    conn = self.get_connection()
    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT Country_ID FROM foods.Meal WHERE Meal_ID = ?", meal_id)
            result = cursor.fetchone()
            if not result:
                print(f"Meal_ID '{meal_id}' does not exist.")
                return False
            country_id = result[0]

            if not (1 <= rating <= 5):
                print("Rating must be between 1 and 5.")
                return False

            cursor.execute("SELECT User_ID FROM users.[User] WHERE Email = ?", email)
            user = cursor.fetchone()
            if not user:
                cursor.execute("INSERT INTO users.[User] (Email) VALUES (?)", email)
                conn.commit()
                cursor.execute("SELECT User_ID FROM users.[User] WHERE Email = ?", email)
                user = cursor.fetchone()

            user_id = user[0]
            rating_id = f"R{meal_id}{user_id}_{int(time.time())}"

            cursor.execute("""
                INSERT INTO users.Rating (Rating_ID, Rating, Review, User_ID, Meal_ID, Country_ID)
                VALUES (?, ?, ?, ?, ?, ?)
            """, rating_id, rating, review, user_id, meal_id, country_id)

            conn.commit()
            return True

        except Exception as e:
            print("Error submitting feedback:")
            traceback.print_exc()
            conn.rollback()
            return False
        finally:
            conn.close()
    return False
