from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import json
import os
from ml_model import process_job_post, get_detector_info

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# User storage file
USERS_FILE = 'users.json'

# Load users from file or initialize with default users
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'admin': 'password123', 'user': 'user123'}
    return {'admin': 'password123', 'user': 'user123'}

# Save users to file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

USERS = load_users()

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=24)

@app.route('/')
def index():
    # Redirect to dashboard if logged in, otherwise to login
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        error = None
        
        # Validation
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif password != confirm_password:
            error = 'Passwords do not match'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters long'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long'
        elif username in USERS:
            error = 'Username already exists'
        
        if error:
            return render_template('register.html', error=error)
        
        # Add new user
        USERS[username] = password
        save_users(USERS)
        
        # Log the user in
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('profile.html', username=session['username'])

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('settings.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/job-post-detector', methods=['GET', 'POST'])
def job_post_detector():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        job_title = request.form.get('job_title', '')
        company_name = request.form.get('company_name', '')
        job_description = request.form.get('job_description', '')
        salary = request.form.get('salary', '')
        location = request.form.get('location', '')
        
        # Validate inputs
        if not all([job_title, company_name, job_description]):
            error = 'Please fill in all required fields'
            return render_template('job_post_detector.html', username=session['username'], error=error)
        
        # Get prediction from ML model in separate file
        result = process_job_post(job_description, job_title, company_name, salary)
    
    # Get model information
    model_info = get_detector_info()
    
    return render_template('job_post_detector.html', username=session['username'], result=result, model_info=model_info)

@app.route('/model-info')
def model_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    info = get_detector_info()
    return render_template('model_info.html', username=session['username'], model_info=info)

if __name__ == '__main__':
    app.run(debug=True)
