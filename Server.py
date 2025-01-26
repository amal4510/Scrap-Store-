from flask import Flask, jsonify, render_template,session
from database import init_db
from Routes import register_routes
import os
from dotenv import load_dotenv
from Model import User
# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize the database
init_db(app)

# Register routes from external file
register_routes(app)




@app.route('/dashboard')
def user_dashboard():
    if 'User' in session:
        username = session['User']
        user = User.query.filter_by(username=username).first()
    return render_template('user_dashboard.html',user = user)



if __name__ == '__main__':
    app.run(debug=True)