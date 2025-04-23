from database import db
# Useful lib Start
import re
import unicodedata

def slugify(text):
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # Convert to lowercase
    text = text.lower()

    # Replace spaces and undesired characters with hyphens
    text = re.sub(r'[^a-z0-9\s-]', '', text)  # Remove special characters
    text = re.sub(r'[\s_-]+', '-', text)      # Replace spaces/underscores with single hyphen
    text = re.sub(r'^-+|-+$', '', text)       # Strip leading/trailing hyphens

    return text

# Useful lib end
class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # Ensure this line exists
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Other fields if necessary

    # Relationship to Scrap and Bids models
    scraps = db.relationship('Scrap', backref='user', lazy=True)
    bids = db.relationship('Bid', backref='user', lazy=True)
    
from datetime import datetime, timedelta

class Scrap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(120), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='selling', nullable=False)

    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)

    bids = db.relationship('Bid', backref='scrap', lazy=True, cascade='all, delete-orphan')

    def generate_slug(self):
        self.slug = slugify(self.title)


# class Scrap(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     image_file = db.Column(db.String(200), nullable=False)
#     slug = db.Column(db.String(120), unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
#     # New status column
#     status = db.Column(db.String(20), default='selling', nullable=False)

#     # Relationship to Bids model
#     bids = db.relationship('Bid', backref='scrap', lazy=True, cascade='all, delete-orphan')
#     def generate_slug(self):
#         self.slug = slugify(self.title)
class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scrap_id = db.Column(db.Integer, db.ForeignKey('scrap.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Relationships to User and Scrap are already defined via foreign keys
    
    
class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    wastage_type = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
