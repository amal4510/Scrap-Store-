from database import db

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # Ensure this line exists
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Other fields if necessary

    # Relationship to Scrap and Bids models
    scraps = db.relationship('Scrap', backref='user', lazy=True)
    bids = db.relationship('Bid', backref='user', lazy=True)

class Scrap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # New status column
    status = db.Column(db.String(20), default='selling', nullable=False)

    # Relationship to Bids model
    bids = db.relationship('Bid', backref='scrap', lazy=True, cascade='all, delete-orphan')
class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scrap_id = db.Column(db.Integer, db.ForeignKey('scrap.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Relationships to User and Scrap are already defined via foreign keys
