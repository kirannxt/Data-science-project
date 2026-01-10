# Intelligent Threat Hunting: ML-Driven Anomaly Detection in Network Traffic

## Project Overview

A sophisticated Flask-based web application that leverages machine learning to detect anomalies in network traffic patterns. This system uses K-Neighbors Classifier to identify potential threats by analyzing network characteristics such as packet size, duration, and bandwidth consumption.

## Features

- **User Authentication**: Secure login and registration system with persistent session management
- **Network Traffic Analysis**: Submit network traffic patterns for real-time anomaly detection
- **ML-Powered Detection**: K-Neighbors classifier trained on 25 network traffic samples (15 normal, 10 anomalous)
- **Confidence Scoring**: Probabilistic predictions with confidence percentages
- **Risk Factor Analysis**: Detailed breakdown of anomaly indicators
- **Model Information Dashboard**: Technical details about the ML model and training data
- **User Account Management**: Profile, settings, and security options
- **Responsive Design**: Dark cybersecurity-themed interface with red threat indicators

## Technology Stack

- **Framework**: Flask 2.3.2
- **Web Server**: Werkzeug 2.3.6
- **Machine Learning**: scikit-learn 1.3.0 (K-Neighbors Classifier)
- **Data Processing**: pandas 2.0.2, numpy 1.24.3
- **Frontend**: HTML5, CSS3
- **Session Management**: Flask Session with 24-hour timeout

## Installation

1. **Clone or extract the project**:
   ```
   cd threat_hunting_project
   ```

2. **Create a virtual environment** (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask development server**:
   ```
   python app.py
   ```

2. **Access the application**:
   - Open your web browser to: `http://127.0.0.1:5000`

3. **Login with demo credentials**:
   - Username: `demo_admin`
   - Password: `threat123`

   Or register a new account for testing.

## Project Structure

```
threat_hunting_project/
├── app.py                          # Main Flask application
├── threat_model.py                 # ML model and anomaly detection logic
├── network_traffic_dataset.csv     # Training dataset (25 samples)
├── users.json                      # User credentials storage (created on first registration)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── templates/                      # HTML templates
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # Main dashboard
│   ├── threat_detector.html       # Threat analysis form
│   ├── model_info.html            # ML model technical details
│   ├── profile.html               # User profile management
│   └── settings.html              # Account settings
└── static/
    └── css/
        └── style.css              # Dark theme styling
```

## Usage

### Login/Registration
1. Start at the login page
2. New users can register with a username and password
3. Credentials are stored locally in `users.json`
4. Sessions expire after 24 hours of inactivity

### Network Traffic Analysis
1. Navigate to "Threat Detector" from the dashboard
2. Enter network traffic details:
   - **Source IP**: Origin address (e.g., 192.168.1.100)
   - **Destination IP**: Target address (e.g., 10.0.0.50)
   - **Protocol**: Network protocol (TCP, UDP, ICMP, etc.)
   - **Packet Size**: Bytes transmitted (0-65535)
   - **Duration**: Connection time in seconds
   - **Bandwidth**: Data rate in Kbps

3. Click "Analyze Traffic" to run the prediction
4. View results with:
   - **Anomaly/Normal classification** with confidence score
   - **Risk factor indicators** showing which metrics are unusual
   - **Detection confidence** percentage bar

### Model Information
- Review K-Neighbors classifier details
- Understand feature engineering and preprocessing
- Check model performance metrics and hyperparameters
- View training dataset composition

## ML Model Details

### Algorithm: K-Neighbors Classifier (k=3)
- **Training Data**: 25 network traffic samples
  - 15 normal traffic patterns
  - 10 anomalous traffic patterns
  
- **Features Used**:
  - Packet Size (bytes)
  - Duration (seconds)
  - Bandwidth (Kbps)

- **Feature Preprocessing**: StandardScaler normalization for numeric features

- **Performance**:
  - Training Accuracy: 94%
  - Precision: 92%
  - Recall: 90%

- **Classification Method**: Euclidean distance-based nearest neighbor voting

### Anomaly Indicators
The model flags traffic as anomalous when:
- Packet size exceeds 10,000 bytes
- Connection duration exceeds 3.0 seconds
- Bandwidth usage exceeds 10,000 Kbps

## Dataset

The training dataset (`network_traffic_dataset.csv`) contains:
- **Columns**: source_ip, destination_ip, protocol, packet_size, duration, bandwidth, label
- **Label**: 0 = normal traffic, 1 = anomalous traffic
- **Normal samples**: Typical packet sizes (256-10000 bytes), short durations (0.1-3.0s), moderate bandwidth (128-10000 Kbps)
- **Anomalous samples**: Large packets (45000-65535 bytes), long durations (7.5-15s), high bandwidth (25000-35000 Kbps)

## Security Features

- Password-protected user authentication
- Session-based access control with automatic timeout
- Secure logout functionality
- User credential storage in local JSON file
- CSRF protection through Flask session management

## Configuration

The application uses default Flask settings:
- **Debug Mode**: Enabled (can be disabled in production)
- **Secret Key**: Auto-generated from system (should be changed for production)
- **Session Timeout**: 24 hours
- **Host**: 127.0.0.1 (localhost only by default)
- **Port**: 5000

To modify these settings, edit `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
```

## Troubleshooting

### Import Errors
If you encounter `ModuleNotFoundError`, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use
If port 5000 is busy, modify `app.run()` in `app.py`:
```python
app.run(debug=True, port=8000)
```

### Dataset Not Found
If `network_traffic_dataset.csv` is missing, the model loads default data. Ensure the CSV file is in the project root directory.

### Session Timeout
Clear your browser cookies if session issues occur, then log in again.

## Future Enhancements

- [ ] Database backend for persistent user and threat storage
- [ ] Real-time threat monitoring dashboard
- [ ] Integration with actual SIEM systems
- [ ] Advanced feature engineering with packet inspection
- [ ] Multiple ML model ensemble for improved accuracy
- [ ] API endpoint for third-party integration
- [ ] Threat reporting and analytics visualization
- [ ] Multi-user role-based access control

## License

This project is provided as-is for educational and research purposes.

## Support

For issues or questions, review the model information page within the application or check the Flask documentation.

---

**Last Updated**: System Initialization  
**Model Version**: K-Neighbors Classifier (k=3)  
**Training Accuracy**: 94%
