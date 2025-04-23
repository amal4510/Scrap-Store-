from flask import Blueprint, request, jsonify
from Model import ContactSubmission
from database import db

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json

    name = data.get('name')
    mobile = data.get('mobile')
    wastage_type = data.get('wastage_type')
    address = data.get('address')
    message = data.get('message')

    if not all([name, mobile, wastage_type, address, message]):
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    submission = ContactSubmission(
        name=name,
        mobile=mobile,
        wastage_type=wastage_type,
        address=address,
        message=message
    )
    db.session.add(submission)
    db.session.commit()

    return jsonify({"status": "success", "message": "Submission saved!"}), 200
