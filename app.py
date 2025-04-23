from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from numpy import sort
from database import db
from Model import Scrap, ContactSubmission

admin_bp = Blueprint('admin', __name__, template_folder='../templates')

# Dummy admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Authentication decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash("You need to log in first!", "danger")
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Login successful!", "success")
            return redirect(url_for('admin.index'))
        else:
            flash("Invalid username or password!", "danger")
    return render_template('admin_login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def index():
    scraps = Scrap.query.all()
    return render_template('admin.html', products=scraps)

@admin_bp.route('/edit_bids')
@login_required
def edit_bids():
    scraps = Scrap.query.all()
    return render_template('edit_bids.html', products=scraps)

@admin_bp.route('/bids')
@login_required
def bids():
    scraps_with_bids = []
    scraps = Scrap.query.all()
    for scrap in scraps:
        bids_info = [
            {"bid_amount": bid.bid_amount, "username": bid.user.username}
            for bid in scrap.bids
        ]
        print(bids_info)
        scraps_with_bids.append({"scrap": scrap, "bids": bids_info})
    return render_template('bids.html', scraps_with_bids=scraps_with_bids)

@admin_bp.route('/delete/<int:scrap_id>', methods=['POST'])
@login_required
def delete_scrap(scrap_id):
    scrap = Scrap.query.get_or_404(scrap_id)
    try:
        db.session.delete(scrap)
        db.session.commit()
        flash("Product deleted successfully!", "success")
    except Exception as e:
        print(f"Error deleting scrap: {e}")
        db.session.rollback()
        flash("Error deleting product. Please try again.", "danger")
    return redirect(url_for('admin.index'))

@admin_bp.route('/update/<int:scrap_id>', methods=['GET', 'POST'])
@login_required
def update_scrap(scrap_id):
    scrap = Scrap.query.get_or_404(scrap_id)
    if request.method == 'POST':
        new_price = request.form.get('price')
        new_status = request.form.get('status')
        
        try:
            if new_price and float(new_price) > 0:
                scrap.price = float(new_price)
                if new_status:
                    scrap.status = new_status
                db.session.commit()
                flash("Product details updated successfully!", "success")
                return redirect(url_for('admin.index'))
            else:
                flash("Please enter a valid price!", "danger")
        except ValueError:
            flash("Price must be a valid number!", "danger")
    
    return render_template('update.html', scrap=scrap)


@admin_bp.route('/notification', methods=['GET', 'POST'])
@login_required
def show_notification():
    # Fetch all contact submissions from the DB (latest first)
    submissions = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).all()
    return render_template('notification.html', submissions=submissions)

@admin_bp.route('/notification/delete/<int:id>', methods=['POST'])
@login_required
def delete_notification(id):
    submission = ContactSubmission.query.get_or_404(id)
    db.session.delete(submission)
    db.session.commit()
    flash('Notification deleted successfully!', 'success')
    return redirect(url_for('admin.show_notification'))