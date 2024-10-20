from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Dummy user storage for demonstration
users = {}

@app.route('/')
def redirect_to_login():
    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/login', methods=['GET', 'POST'])
def login():
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('index'))  # Redirect to index on successful login
        else:
            flash('Invalid Credentials')  # Flash message for invalid login
            return redirect(url_for('login'))  # Redirect back to login

    return render_template('login.html')  # Render the login page

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if username in users:
        flash('Username already exists. Please choose a different one.')
        return redirect(url_for('login'))

    if password != confirm_password:
        flash('Passwords do not match. Please try again.')
        return redirect(url_for('login'))

    users[username] = password  # Store user credentials (this is just for demonstration)
    flash('Registration successful! You can now log in.')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)