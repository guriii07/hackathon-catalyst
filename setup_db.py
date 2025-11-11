# This script is for running one-off commands on Render to set up the database.
import os
from app import app, db
# Assuming your database models (the classes inheriting db.Model) are in a file named 'models.py'
import models 

# 1. Ensure the Flask application context is active.
# This makes sure the app can access its configuration (like the DATABASE_URL).
with app.app_context():
    print("Creating all tables on the PostgreSQL database...")
    
    # 2. Create all tables defined in your models.
    # This reads the schema from your Python classes and builds the corresponding 
    # tables in the PostgreSQL database.
    db.create_all()
    
    print("Database tables created successfully!")
    
    # If you have initial data (seed data), you would run it here.
    # For example, if you had a seed.py file:
    # from seed import seed_data
    # seed_data()