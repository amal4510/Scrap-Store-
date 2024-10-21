from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_KEY = os.getenv('DATABASE_KEY')
# Initialize the database object
db = SQLAlchemy()

def init_db(app):
    # Configure your database URI here
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Create the tables if they don't exist
    with app.app_context():
        db.create_all()

