from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Ensure this line exists
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
   # Other fields if necessary

    def __repr__(self):
        return f'<User {self.username}>'
    
    
class Scrap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Add this line

    # Relationship to User model
    user = db.relationship('User', backref='scraps')