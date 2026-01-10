from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import json
import os
from threat_model import process_network_traffic, get_detector_info

app = Flask(__name__)
app.secret_key = 'threat_hunting_secret_key_change_this'
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
            return {'admin': 'password123', 'analyst': 'analyst123'}
    return {'admin': 'password123', 'analyst': 'analyst123'}

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
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
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

@app.route('/threat-detector', methods=['GET', 'POST'])
def threat_detector():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    result = None
    error = None
    if request.method == 'POST':
        try:
            packet_size = float(request.form.get('packet_size', 0))
            duration = float(request.form.get('duration', 0))
            bandwidth = float(request.form.get('bandwidth', 0))
            source_ip = request.form.get('source_ip', '')
            destination_ip = request.form.get('destination_ip', '')
            protocol = request.form.get('protocol', '')
            
            # Validate inputs
            if not all([packet_size, duration, bandwidth, source_ip, destination_ip]):
                error = 'Please fill in all required fields'
                return render_template('threat_detector.html', username=session['username'], error=error)
            
            # Get prediction from ML model
            prediction = process_network_traffic(packet_size, duration, bandwidth)
            
            # Add network details to result
            result = {
                'source_ip': source_ip,
                'destination_ip': destination_ip,
                'protocol': protocol,
                'packet_size': packet_size,
                'duration': duration,
                'bandwidth': bandwidth,
                'is_anomaly': prediction.get('is_anomaly'),
                'confidence': prediction.get('confidence', 0) / 100,  # Convert to 0-1 range
                'anomaly_probability': prediction.get('anomaly_probability', 0),
                'normal_probability': prediction.get('normal_probability', 0),
                'prediction_label': prediction.get('prediction_label', '')
            }
        
        except ValueError:
            error = 'Please enter valid numeric values'
            return render_template('threat_detector.html', username=session['username'], error=error)
    
    # Get model information
    model_info = get_detector_info()
    
    return render_template('threat_detector.html', username=session['username'], result=result, model_info=model_info, error=error)

@app.route('/model-info')
def model_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    info = get_detector_info()
    return render_template('model_info.html', username=session['username'], model_info=info)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
