from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
import os
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'fraud-detection-secret-key-2026'

# Load users from JSON file
def load_users():
    """Load users from JSON file"""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Save users to JSON file
def save_users(users):
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

# Load ML model
def load_model():
    """Load the trained ML model and scaler"""
    try:
        model = joblib.load('fraud_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except:
        return None, None

# Fraud detector class
class FraudDetector:
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self.fraud_labels = ['Legitimate Listing', 'Fraudulent Listing']
        self.fraud_colors = ['#28a745', '#dc3545']
    
    def predict(self, features):
        """Make prediction on job listing"""
        try:
            # Normalize features
            features_scaled = self.scaler.transform([features])
            
            # Predict
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            # Calculate fraud score (0-100)
            fraud_score = int(probabilities[prediction] * 100)
            
            return {
                'status': self.fraud_labels[prediction],
                'fraud_score': fraud_score,
                'confidence': round(probabilities[prediction] * 100, 2),
                'color': self.fraud_colors[prediction]
            }
        except Exception as e:
            return {'error': str(e)}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        users = load_users()
        
        # Validation
        if not username or len(username) < 3:
            return render_template('register.html', error='Username must be at least 3 characters')
        
        if username in users:
            return render_template('register.html', error='Username already exists')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters')
        
        # Create user
        users[username] = {
            'email': email,
            'password': generate_password_hash(password),
            'created_at': str(__import__('datetime').datetime.now()),
            'detections': []
        }
        
        save_users(users)
        return render_template('register.html', success='Registration successful! Please login.')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_users()
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html', username=session.get('user'))

@app.route('/detection', methods=['GET', 'POST'])
@login_required
def detection():
    """Fraud detection page"""
    model, scaler = load_model()
    result = None
    
    if request.method == 'POST':
        try:
            # Get form data
            salary_range = int(request.form.get('salary_range', 50000))
            company_verified = int(request.form.get('company_verified', 1))
            location_specific = int(request.form.get('location_specific', 1))
            description_length = int(request.form.get('description_length', 500))
            contact_verified = int(request.form.get('contact_verified', 1))
            posting_age = int(request.form.get('posting_age', 10))
            grammatical_errors = int(request.form.get('grammatical_errors', 2))
            keyword_count = int(request.form.get('keyword_count', 30))
            
            # Create detector
            detector = FraudDetector(model, scaler)
            
            # Make prediction
            features = [salary_range, company_verified, location_specific,
                       description_length, contact_verified, posting_age,
                       grammatical_errors, keyword_count]
            result = detector.predict(features)
            
            # Save detection
            users = load_users()
            if session.get('user') in users:
                users[session['user']]['detections'].append({
                    'result': result,
                    'timestamp': str(__import__('datetime').datetime.now())
                })
                save_users(users)
        
        except Exception as e:
            result = {'error': str(e)}
    
    return render_template('detection.html', result=result, username=session.get('user'))

@app.route('/insights')
@login_required
def insights():
    """Insights page"""
    return render_template('insights.html', username=session.get('user'))

@app.route('/api/detect', methods=['POST'])
@login_required
def api_detect():
    """API endpoint for fraud detection"""
    model, scaler = load_model()
    data = request.json
    
    try:
        features = [
            int(data['salary_range']),
            int(data['company_verified']),
            int(data['location_specific']),
            int(data['description_length']),
            int(data['contact_verified']),
            int(data['posting_age']),
            int(data['grammatical_errors']),
            int(data['keyword_count'])
        ]
        
        detector = FraudDetector(model, scaler)
        result = detector.predict(features)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
