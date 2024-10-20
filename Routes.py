from flask import render_template, redirect, url_for, request, flash,session
from Model import User
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

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
