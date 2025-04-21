from flask import render_template, redirect, url_for, request, flash, session, jsonify
from Model import User, Scrap, Bid
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
def register_routes(app):
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/', methods=['GET','POST'])
    def index():
        user = session.get('User')  # Fetch logged-in user
        scraps = Scrap.query.all()  # Fetch all scrap products
        return render_template('index.html', user=user, products=scraps)

    # About page
    @app.route('/about', methods=['GET'])
    def about():
        return render_template('about.html')
    # donation page
    @app.route('/donation', methods=['GET'])
    def donation():
        scraps = Scrap.query.all()  # Fetch all scrap products
    
        return render_template('donation.html', products=scraps)

    # contact page
    @app.route('/contact', methods=['GET'])
    def contact():
        return render_template('contact.html')
    
    # Register page
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                flash('Please fill out both fields', 'danger')
                return render_template('login.html')

            user = User.query.filter_by(email=username).first()
            if user and check_password_hash(user.password, password):
                session['User'] = user.username
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('User', None)
        flash('You have been logged out', 'info')
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            if not username or not email or not password:
                flash('All fields are required', 'danger')
                return render_template('register.html')

            if User.query.filter_by(email=email).first():
                flash('Email already exists', 'danger')
                return render_template('register.html')

            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')


    @app.route('/add_scrap', methods=['GET', 'POST'])
    def add_scrap():
        if 'User' not in session:
            flash('Please log in to add scrap', 'danger')
            return redirect(url_for('login'))

        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            price = request.form.get('price')
            duration_minutes = int(request.form.get('duration'))  # e.g., 60 for 1 hour

            if 'image_file' not in request.files or not request.files['image_file'].filename:
                flash('No file selected', 'danger')
                return redirect(url_for('add_scrap'))

            file = request.files['image_file']
            if file and allowed_file(file.filename):
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])

                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                user = User.query.filter_by(username=session['User']).first()
                start_time = datetime.utcnow()
                end_time = start_time + timedelta(minutes=duration_minutes)

                new_scrap = Scrap(
                    title=title,
                    description=description,
                    price=price,
                    image_file=f'uploads/{filename}',
                    user_id=user.id,
                    start_time=start_time,
                    end_time=end_time
                )

                new_scrap.generate_slug()
                db.session.add(new_scrap)
                db.session.commit()

                flash('Scrap added and auction started!', 'success')
                return redirect(url_for('index'))

        return render_template('add-scrap.html')


    # @app.route('/add_scrap', methods=['GET', 'POST'])
    # def add_scrap():
    #     if 'User' not in session:
    #         flash('Please log in to add scrap', 'danger')
    #         return redirect(url_for('login'))

    #     if request.method == 'POST':
    #         title = request.form.get('title')
    #         description = request.form.get('description')
    #         price = request.form.get('price')

    #         if 'image_file' not in request.files or not request.files['image_file'].filename:
    #             flash('No file selected', 'danger')
    #             return redirect(url_for('add_scrap'))

    #         file = request.files['image_file']
    #         if file and allowed_file(file.filename):
    #             if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #                 os.makedirs(app.config['UPLOAD_FOLDER'])

    #             filename = secure_filename(file.filename)
    #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #             user = User.query.filter_by(username=session['User']).first()
    #             new_scrap = Scrap(
    #                 title=title,
    #                 description=description,
    #                 price=price,
    #                 image_file=f'uploads/{filename}',
    #                 user_id=user.id
    #             )
                
    #             new_scrap.generate_slug()
    #             db.session.add(new_scrap)
    #             db.session.commit()

    #             flash('Scrap added successfully!', 'success')
    #             return redirect(url_for('index'))

    #     return render_template('add-scrap.html')

    @app.route('/auction', methods=['GET','POST'])
    def auction():
        scraps = Scrap.query.all()

        if 'User' not in session:
            flash('Please log in to place a bid', 'danger')
            return redirect(url_for('login'))

           
        return render_template('auction.html', products=scraps)
    
    
    @app.route('/auction/<slug>', methods=['GET', 'POST'])
    def auction_detail(slug):
        scrap = Scrap.query.filter_by(slug=slug).first_or_404()
        bids = Bid.query.filter_by(scrap_id=scrap.id).order_by(Bid.bid_amount.desc()).all()
        now = datetime.utcnow()
        remaining_time = scrap.end_time - now

        auction_active = scrap.start_time <= now <= scrap.end_time

        if request.method == 'POST':
            if not auction_active:
                flash('Bidding time has ended.', 'danger')
                return redirect(request.url)

            bid_amount = request.form.get('bidprice')

            if 'User' not in session:
                flash('Please log in to place a bid', 'danger')
                return redirect(url_for('login'))

            user = User.query.filter_by(username=session['User']).first()

            if float(bid_amount) <= scrap.price:
                flash('Bid must be higher than current price.', 'warning')
                return redirect(request.url)

            new_bid = Bid(bid_amount=float(bid_amount), user_id=user.id, scrap_id=scrap.id)
            scrap.price = float(bid_amount)  # Update current price
            db.session.add(new_bid)
            db.session.commit()

            flash('Bid placed successfully!', 'success')
            return redirect(request.url)

        return render_template('auction_detail.html', scrap=scrap, bids=bids, auction_active=auction_active, remaining_time=remaining_time)

    
    # @app.route('/auction/<slug>', methods=['GET', 'POST'])
    # def auction_detail(slug):
    #     scrap = Scrap.query.filter_by(slug=slug).first_or_404()
    #     bids = Bid.query.filter_by(scrap_id=scrap.id).order_by(Bid.bid_amount.desc()).all()
        
    #     if request.method == 'POST':
    #         bid_amount = request.form.get('bidprice')

    #         if 'User' not in session:
    #             flash('Please log in to place a bid', 'danger')
    #             return redirect(url_for('login'))

    #         user = User.query.filter_by(username=session['User']).first()

    #         if float(bid_amount) <= scrap.price:
    #             flash('Bid must be higher than current price.', 'warning')
    #             return redirect(request.url)

    #         new_bid = Bid(bid_amount=float(bid_amount), user_id=user.id, scrap_id=scrap.id)
    #         scrap.price = float(bid_amount)  # Update current price
    #         db.session.add(new_bid)
    #         db.session.commit()

    #         flash('Bid placed successfully!', 'success')
    #         return redirect(request.url)

    #     return render_template('auction_detail.html', scrap=scrap, bids=bids)

