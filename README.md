# Sleep-Based Stress Detection Using Machine Learning

A Flask-based web application that uses machine learning to detect stress levels based on sleep patterns and habits.

## Features

- **User Authentication**: Secure login and registration system with password hashing
- **ML Model**: Random Forest classifier trained on sleep data to predict stress levels
- **Sleep Analysis**: Analyze sleep duration, quality, cycles, restlessness, heart rate, wake-ups, and caffeine intake
- **Stress Detection**: Classify stress as Low, Medium, or High with confidence scores
- **Dashboard**: View sleep analysis history and trends
- **Insights**: Educational content about sleep and stress relationship
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Tech Stack

- **Backend**: Python Flask 2.3.2
- **ML Framework**: scikit-learn 1.2.2 (Random Forest)
- **Data Processing**: NumPy, Pandas
- **Security**: Werkzeug (password hashing)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: JSON-based user storage

## Installation

1. **Clone the repository**:
   ```bash
   cd d:\sleep-stress-detection
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model**:
   ```bash
   python train_model.py
   ```
   This will create `stress_model.pkl` and `scaler.pkl` files.

5. **Create a test user** (optional):
   ```bash
   python create_test_user.py
   ```

6. **Run the Flask application**:
   ```bash
   python app.py
   ```

7. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
sleep-stress-detection/
├── app.py                 # Main Flask application
├── train_model.py         # ML model training script
├── requirements.txt       # Python dependencies
├── users.json            # User database
├── stress_model.pkl      # Trained ML model (generated after training)
├── scaler.pkl            # Feature scaler (generated after training)
├── templates/            # HTML templates
│   ├── base.html        # Base template with navbar and footer
│   ├── index.html       # Landing page
│   ├── dashboard.html   # Dashboard page
│   ├── prediction.html  # Stress detection form
│   ├── insights.html    # Educational insights
│   ├── login.html       # Login page
│   └── register.html    # Registration page
└── static/              # Static files
    ├── css/
    │   └── style.css    # Blue/purple theme styling
    └── js/
        └── main.js      # JavaScript utilities
```

## Usage

### Register and Login
1. Click "Register" to create a new account
2. Provide username (min 3 chars), email, and password (min 6 chars)
3. Login with your credentials

### Make a Prediction
1. Go to the "Prediction" page
2. Enter your sleep data:
   - Sleep duration (hours)
   - Sleep quality (1-10 scale)
   - Sleep cycles (3-6)
   - Restlessness level (0-10)
   - Average heart rate during sleep (BPM)
   - Number of wake-ups
   - Caffeine intake (mg)
3. Click "Analyze Sleep Pattern"
4. View your stress detection result with recommendations

### View Dashboard
- Monitor your sleep analysis history
- See recent predictions and trends
- Learn about the ML model

### Read Insights
- Educational articles about sleep and stress
- Tips for improving sleep quality
- Information about stress management

## ML Model Details

**Model**: Random Forest Classifier
- **Trees**: 100
- **Max Depth**: 15
- **Training Accuracy**: ~95%
- **Testing Accuracy**: ~92%

**Features**:
1. Sleep Duration (hours)
2. Sleep Quality (1-10)
3. Sleep Cycles (count)
4. Restlessness Level (0-10)
5. Heart Rate During Sleep (BPM)
6. Wake-ups Frequency (count)
7. Caffeine Intake (mg)

**Output Classes**:
- 0: Low Stress (green)
- 1: Medium Stress (orange)
- 2: High Stress (red)

## Configuration

The application uses Flask sessions for user management. Key configuration:
- Secret key: 'stress-detection-secret-key-2026'
- Debug mode: True (development)
- Port: 5000

## Security

- Passwords are hashed using Werkzeug's `generate_password_hash`
- User data is stored in JSON with hashed passwords
- Login-required decorator protects prediction and dashboard pages
- Session management for user authentication

## Theme

The application features a modern blue/purple gradient theme:
- Primary Purple: #7c3aed
- Primary Blue: #3b82f6
- Gradient backgrounds with smooth transitions
- Responsive design with mobile-first approach

## API Endpoints

- `GET /` - Landing page
- `GET /register` - Registration page
- `POST /register` - Register new user
- `GET /login` - Login page
- `POST /login` - Login user
- `GET /logout` - Logout user
- `GET /dashboard` - Dashboard (protected)
- `GET /prediction` - Prediction form (protected)
- `POST /prediction` - Submit prediction (protected)
- `GET /insights` - Insights page (protected)
- `POST /api/predict` - JSON prediction API (protected)

## Testing

Test user credentials:
- Username: `testuser`
- Password: `password123`

Create a test user by running:
```bash
python create_test_user.py
```

## Requirements

See `requirements.txt` for complete list:
- Flask==2.3.2
- numpy==1.24.3
- scikit-learn==1.2.2
- joblib==1.2.0
- pandas==2.0.2
- Werkzeug==2.3.6
- Jinja2==3.1.2

## Future Enhancements

- Real-time sleep tracking integration
- Mobile app
- Database migration (from JSON to SQL)
- Advanced analytics and visualization
- Email notifications
- Wearable device integration
- Export reports feature

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please contact the development team.

---

**Last Updated**: January 12, 2026
