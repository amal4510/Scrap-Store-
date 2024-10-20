from flask import Flask
from db import init_db
from routes import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management, CSRF protection

# Initialize the database
init_db(app)

# Register routes from external file
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
