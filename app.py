from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from datetime import datetime
import os
import json
import joblib
import warnings
from functools import wraps

warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# User database file
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def login_required(f):
    """Decorator to protect routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Load trained ML model and scaler
def load_model():
    """Load the trained ExtraTreesClassifier model and scaler"""
    model_path = os.path.join(os.path.dirname(__file__), 'addiction_model.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
    
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except FileNotFoundError:
        print("Warning: Model files not found. Please run 'python train_model.py' to train the model.")
        return None, None

# Load model and scaler
ml_model, scaler = load_model()

class AddictionPredictor:
    """Real ML-based prediction using ExtraTreesClassifier"""
    
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self.risk_levels = {0: "Low", 1: "Medium", 2: "High"}
    
    def predict(self, features):
        """
        Predicts smartphone addiction level using trained ML model
        
        Args:
            features: List of 6 features [daily_usage, screen_time, notification_checks, 
                     sleep_disruption, social_anxiety, fomo_score]
        
        Returns:
            addiction_score (0-100), risk_level (Low/Medium/High), confidence (%)
        """
        if self.model is None or self.scaler is None:
            # Fallback to mock if model not loaded
            return self._fallback_predict(features)
        
        try:
            # Prepare feature array
            X = np.array(features).reshape(1, -1)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Get prediction
            prediction = self.model.predict(X_scaled)[0]
            
            # Get prediction probabilities for confidence
            probabilities = self.model.predict_proba(X_scaled)[0]
            confidence = max(probabilities) * 100
            
            # Map prediction to addiction score
            # Calculate average feature value weighted by importance
            feature_importance = self.model.feature_importances_
            weighted_score = np.sum(np.array(features) * feature_importance) / np.sum(feature_importance)
            
            # Normalize to 0-100 scale
            addiction_score = (weighted_score / 10) * 100
            addiction_score = min(100, max(0, addiction_score))
            
            risk_level = self.risk_levels.get(prediction, "Medium")
            
            return addiction_score, risk_level, confidence
        
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._fallback_predict(features)
    
    def _fallback_predict(self, features):
        """Fallback prediction if model loading fails"""
        score = np.mean(features) * 10
        score = min(100, max(0, score))
        
        if score < 30:
            risk = "Low"
        elif score < 70:
            risk = "Medium"
        else:
            risk = "High"
        
        return score, risk, 0

# Initialize predictor
predictor = AddictionPredictor(ml_model, scaler)

# ========================
# AUTHENTICATION ROUTES
# ========================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            return render_template('register.html', error='All fields are required'), 400
        
        if len(username) < 3:
            return render_template('register.html', error='Username must be at least 3 characters'), 400
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters'), 400
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match'), 400
        
        users = load_users()
        
        if username in users:
            return render_template('register.html', error='Username already exists'), 400
        
        # Create new user
        users[username] = {
            'email': email,
            'password': generate_password_hash(password),
            'created_at': datetime.now().isoformat(),
            'predictions': []
        }
        
        save_users(users)
        
        return redirect(url_for('login', success='Registration successful! Please login.'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template('login.html', error='Username and password are required'), 400
        
        users = load_users()
        
        if username not in users:
            return render_template('login.html', error='Invalid username or password'), 401
        
        user = users[username]
        
        if not check_password_hash(user['password'], password):
            return render_template('login.html', error='Invalid username or password'), 401
        
        # Set session
        session['user'] = username
        session['email'] = user['email']
        
        return redirect(url_for('dashboard'))
    
    success = request.args.get('success', '')
    return render_template('login.html', success=success)

@app.route('/logout')
def logout():
    """Handle user logout"""
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login', success='Logged out successfully!'))

@app.route('/')
def home():
    """Home page - redirect to login if not authenticated"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard - protected route"""
    return render_template('dashboard.html', username=session.get('user'))

@app.route('/prediction')
@login_required
def prediction():
    """Prediction page - protected route"""
    return render_template('prediction.html', username=session.get('user'))

@app.route('/insights')
@login_required
def insights():
    """Insights page - protected route"""
    return render_template('insights.html', username=session.get('user'))

@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """API endpoint for addiction prediction - protected"""
    try:
        data = request.json
        features = [
            float(data.get('daily_usage', 0)),
            float(data.get('screen_time', 0)),
            float(data.get('notification_checks', 0)),
            float(data.get('sleep_disruption', 0)),
            float(data.get('social_anxiety', 0)),
            float(data.get('fomo_score', 0)),
        ]
        
        score, risk, confidence = predictor.predict(features)
        
        return jsonify({
            'success': True,
            'addiction_score': round(score, 2),
            'risk_level': risk,
            'confidence': round(confidence, 2),
            'timestamp': datetime.now().isoformat(),
            'model': 'ExtraTreesClassifier'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    return jsonify({
        'avg_daily_usage': 5.3,
        'users_high_risk': 42,
        'total_predictions': 156,
        'improvement_rate': 23.5
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
