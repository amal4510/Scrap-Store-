from flask import Flask, jsonify, render_template,session
from database import init_db, db
from Routes import register_routes
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
import random 

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

# Initialize the database
init_db(app)

# Register routes from external file
register_routes(app)

# Placeholder for auction items - this can be fetched dynamically from a database
auctions = {
    1: {"id": 1, "title": "Scrap Metal Auction", "current_bid": random.randint(100, 1000)},
    2: {"id": 2, "title": "Old Electronics", "current_bid": random.randint(100, 1000)}
}


@app.route('/user/dashboard')
def user_dashboard():
    if 'username' in session:
        username = session['username']
        print(session)
    return render_template('user_dashboard.html')

# Route to render the auction page
@app.route('/auction')
def auction():
    return render_template('auction.html')

# API route to fetch scrap prices in real-time
@app.route('/getScrapPrices')
def get_scrap_prices():
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

# API route to fetch auction data
@app.route('/auction')
def auction_page():
    return render_template('auction.html')

# API route to fetch auction data
@app.route('/api/auctions')
def fetch_auctions():
    return jsonify(list(auctions.values()))

# Socket.IO event handler for placing a bid
@socketio.on('place_bid')
def handle_place_bid(data):
    auction_id = data['auction_id']
    new_bid = data['new_bid']
    company_name = data['company_name']  # Get company name
    if auction_id in auctions and new_bid > auctions[auction_id]['current_bid']:
        auctions[auction_id]['current_bid'] = new_bid
        # Broadcast the updated bid and company name to all clients
        emit('update_bid', {
            'auction_id': auction_id,
            'new_bid': new_bid,
            'company_name': company_name
        }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)