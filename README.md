🌍 Food Explorer Desktop App
📌 Project Overview

This project is a Database Management System (DBMS) desktop application built in Python.
We designed and implemented the database from scratch, populated it with sample data, and developed an interactive app where users can explore food from around the world.

The application connects users to global cuisine by allowing them to:

Log in to the system securely.

Choose a country to explore its cuisine.

Select a meal from that country.

View ingredients, ratings, and user reviews for each meal.

This project was created as part of a Database Systems course, showcasing the integration of database design, SQL queries, and Python GUI development.

⚙️ Features

✅ User login and authentication system
✅ Browse meals by country
✅ Select a meal to explore its details
✅ View ingredients list for each meal
✅ Check ratings and user reviews
✅ Database created from scratch (ERD → schema → populated data)
✅ Desktop-based GUI for smooth navigation

🗄️ Database Design

Entity-Relationship (ER) model was created to represent countries, meals, ingredients, users, reviews, and ratings.

Normalization was applied to reduce redundancy.

SQL scripts were used to populate initial data.

Key tables include:

Users → login and authentication

Countries → list of available cuisines

Meals → meals associated with countries

Ingredients → linked to each meal

Reviews → user ratings and comments

🖥️ Tech Stack

Python (backend + desktop GUI)

SQLite / MySQL (database engine)

Tkinter / PyQt (GUI framework, depending on your implementation)

SQL (queries, schema creation, data manipulation)

🚀 How to Run

Clone this repository:

git clone https://github.com/yourusername/food-explorer-db.git
cd food-explorer-db


Install dependencies (if any):

pip install -r requirements.txt


Run the app:

python app.py


Log in with test credentials or register as a new user.

Start exploring food from around the world! 🌍🍴

📊 Screenshots

(Add screenshots of your GUI, e.g. login page, country selection, meal details)

📚 Learning Outcomes

Through this project, we gained hands-on experience in:

Database design (ERD, schema creation, normalization).

Writing SQL queries for CRUD operations.

Connecting a database to a Python application.

Developing a user-friendly GUI for database interaction.

Managing user input, data validation, and retrieval.

✨ Future Enhancements

Add more countries and meals to expand the dataset.

Implement advanced search filters (by rating, ingredients, etc.).

Allow users to upload their own reviews dynamically.

Improve GUI design with richer visuals.

👥 Team

This project was developed by our team as part of the Database Systems course.
