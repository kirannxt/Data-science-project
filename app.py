from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
import os
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'stress-detection-secret-key-2026'

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
        model = joblib.load('stress_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except:
        return None, None

# Stress predictor class
class StressPredictor:
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self.stress_labels = ['Low Stress', 'Medium Stress', 'High Stress']
        self.stress_colors = ['#4caf50', '#ff9800', '#f44336']
    
    def predict(self, features):
        """Make prediction on stress level"""
        try:
            # Normalize features
            features_scaled = self.scaler.transform([features])
            
            # Predict
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            # Calculate stress score (0-100)
            stress_score = int(probabilities[prediction] * 100)
            
            return {
                'stress_level': self.stress_labels[prediction],
                'stress_score': stress_score,
                'confidence': round(probabilities[prediction] * 100, 2),
                'color': self.stress_colors[prediction]
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
            'predictions': []
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

@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    """Prediction page"""
    model, scaler = load_model()
    result = None
    
    if request.method == 'POST':
        try:
            # Get form data
            sleep_duration = float(request.form.get('sleep_duration', 7))
            sleep_quality = int(request.form.get('sleep_quality', 7))
            sleep_cycles = int(request.form.get('sleep_cycles', 4))
            restlessness = float(request.form.get('restlessness', 5))
            heart_rate = float(request.form.get('heart_rate', 65))
            wake_ups = int(request.form.get('wake_ups', 1))
            caffeine_intake = int(request.form.get('caffeine_intake', 100))
            
            # Create predictor
            predictor = StressPredictor(model, scaler)
            
            # Make prediction
            features = [sleep_duration, sleep_quality, sleep_cycles, 
                       restlessness, heart_rate, wake_ups, caffeine_intake]
            result = predictor.predict(features)
            
            # Save prediction
            users = load_users()
            if session.get('user') in users:
                users[session['user']]['predictions'].append({
                    'result': result,
                    'timestamp': str(__import__('datetime').datetime.now())
                })
                save_users(users)
        
        except Exception as e:
            result = {'error': str(e)}
    
    return render_template('prediction.html', result=result, username=session.get('user'))

@app.route('/insights')
@login_required
def insights():
    """Insights page"""
    return render_template('insights.html', username=session.get('user'))

@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """API endpoint for predictions"""
    model, scaler = load_model()
    data = request.json
    
    try:
        features = [
            float(data['sleep_duration']),
            int(data['sleep_quality']),
            int(data['sleep_cycles']),
            float(data['restlessness']),
            float(data['heart_rate']),
            int(data['wake_ups']),
            int(data['caffeine_intake'])
        ]
        
        predictor = StressPredictor(model, scaler)
        result = predictor.predict(features)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
