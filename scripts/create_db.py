from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

# ✅ Create a Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Define database configuration (SQLite)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to reduce memory usage

# ✅ Initialize the database
db = SQLAlchemy(app)  # Create a database object using SQLAlchemy

# ✅ Define the user model
class UserModel(db.Model):
    __tablename__ = "user_model"  # Explicitly specify the table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key (unique user identifier)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username field (must be unique and required)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email field (must be unique and required)

# ✅ Function to create the database
def create_database():
    with app.app_context():  # Set the application context
        inspector = inspect(db.engine)  # Create a database inspector object
        
        # ✅ Check if the table already exists
        if "user_model" not in inspector.get_table_names():
            db.create_all()  # Create the table if it doesn't exist
            print("✅ Table `user_model` has been created")  # Log message for table creation
        else:
            print("⚠️ Table `user_model` already exists, no need to create it again.")  # Log message if table already exists

# ✅ Run the script if executed directly
if __name__ == "__main__":
    create_database()  # Call the function to create the database
