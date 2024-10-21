from flask import render_template, redirect, url_for, request, flash,session,jsonify
from Model import User,Scrap
from database import db
from bot import auctions
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

def register_routes(app):
    @app.route('/')
    def index():
        if 'username' in session:
            username = session['username']
            return render_template('index.html')
        else:
            return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Ensure form fields are not empty
            if not username or not password:
                flash('Please fill out both fields', 'danger')
                return render_template('login.html')
            
            user = User.query.filter_by(username=username).first()
            # Check if user exists and if the password matches the hash
            if user and check_password_hash(user.password, password):
                session['username'] = user.username
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'danger')

        return render_template('login.html')


    @app.route('/logout')
    def logout():
        # Clear the session to log the user out
        session.pop('username', None)
        flash('You have been logged out', 'info')
        return redirect(url_for('login'))


    # Example route to register new users
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            # Hash the password with the correct method
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')
    
    # Scraping processs
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    @app.route('/add_scrap', methods=['GET', 'POST'])
    def add_scrap():

        if 'username' not in session:
            flash('Please log in to add scrap', 'danger')
            return redirect(url_for('login'))
        print(session['id'])
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']

            if 'image_file' not in request.files:
                flash('No file selected', 'danger')
                return redirect(url_for('add_scrap'))

            file = request.files['image_file']

            if file.filename == '':
                flash('No file selected', 'danger')
                return redirect(url_for('add_scrap'))

            if file and allowed_file(file.filename):
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])

                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Store the relative path to the image correctly
                file_url = f'uploads/{filename}'  # Altered line


                new_scrap = Scrap(title=title, description=description, price=price, image_file=file_url)
                db.session.add(new_scrap)
                db.session.commit()

                flash('Scrap added successfully!', 'success')
                return redirect(url_for('scrap_listings'))

        return render_template('add-scrap.html')

    
    @app.route('/auctions', methods=['GET'])
    def get_auctions():
        # return jsonify(auctions)
        return render_template('auction.html')


    @app.route('/scrap-listings')
    def scrap_listings():
        scraps = Scrap.query.all()  # Fetch all scraps from the database
        return render_template('scrap-listing.html', scraps=scraps)
