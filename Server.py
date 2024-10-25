from flask import Flask, jsonify
from database import init_db, db
from Routes import register_routes
import os
from dotenv import load_dotenv

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

# API route to fetch scrap prices in real-time
@app.route('/getScrapPrices')
def get_scrap_prices():
    # Fetch real-time prices from your database or external source
    # For now, we're using static prices as an example
    prices = {
        'normal_recyclables': '₹10/kg',
        'office_paper': '₹5/kg',
        'newspaper': '₹6/kg',
        'ac_units': '₹500/unit',
        'washing_machine': '₹300/unit',
        'single_door_fridge': '₹400/unit',
        'printer': '₹200/unit',
        'ceiling_fan': '₹150/unit',
        'microwave': '₹250/unit',
        'scrap_laptop': '₹1000/unit',
        'mobile_phones': '₹500/unit',
        'computer_cpu': '₹700/unit'
    }
    return jsonify(prices)

# Uncomment this if you want to drop all tables (for database reset)
# with app.app_context():
#     db.drop_all()
#     print("All tables have been dropped successfully!")

if __name__ == '__main__':
    app.run(debug=True)
