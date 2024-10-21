from flask import Flask, jsonify

app = Flask(__name__)

# Mock auction data
auctions = [
    {
        "id": 1,
        "name": "Metal Scrap Auction",
        "date": "2024-10-25",
        "time": "10:00 AM",
        "companies": ["Company A", "Company B", "Company C"],
        "status": "Ongoing"
    },
    {
        "id": 2,
        "name": "Plastic Waste Auction",
        "date": "2024-10-28",
        "time": "2:00 PM",
        "companies": ["Company D", "Company E"],
        "status": "Upcoming"
    }
]

@app.route('/auctions', methods=['GET'])
def get_auctions():
    return jsonify(auctions)

if __name__ == '__main__':
    app.run(debug=True)
