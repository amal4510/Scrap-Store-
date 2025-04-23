from flask import Flask, jsonify, render_template,session
from database import init_db
from Routes import register_routes
import os
from dotenv import load_dotenv
from Model import User
from app import admin_bp
from contact import contact_bp
from sqlalchemy.orm import joinedload
from Model import Scrap, Bid, User
# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize the database
init_db(app)


# Register the admin blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(contact_bp)

register_routes(app)




@app.route('/dashboard')
def user_dashboard():
    if 'User' in session:
        username = session['User']
        user = User.query.filter_by(username=username).first()

        # Get scraps posted by the user
        posted_scraps = Scrap.query.filter_by(user_id=user.id).all()

        # Get scraps the user has bid on
        bidded_scraps = (
            Scrap.query.join(Bid)
            .filter(Bid.user_id == user.id)
            .options(joinedload(Scrap.bids))
            .all()
        )

        return render_template(
            'user_dashboard.html',
            user=user,
            posted_scraps=posted_scraps,
            bidded_scraps=bidded_scraps
        )
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)