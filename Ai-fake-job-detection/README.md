# AI Against Fraud: Intelligent Detection of Fake Job Listings

A Flask web application with authentication and ML-based fake job post detection.

## Project Structure

```
flask-testing-project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── login.html       # Login page
│   ├── dashboard.html   # Dashboard page
│   ├── profile.html     # User profile page
│   └── settings.html    # Settings page
└── static/
    └── css/
        └── style.css    # Application styles
```

## Pages

1. **Login Page** - Starting page with authentication
2. **Dashboard** - Main page after login with statistics
3. **Profile** - User profile information
4. **Settings** - Application preferences and settings

## Features

- User authentication with session management
- Login redirection to dashboard
- Navigation menu between pages
- Logout functionality
- Responsive design with modern UI
- CSS styling with gradient backgrounds

## Installation & Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Default Credentials

For testing purposes, use these credentials:

- **Username:** admin | **Password:** password123
- **Username:** user | **Password:** user123

## How It Works

1. When you start the app, it redirects to the login page
2. Enter username and password to authenticate
3. After successful login, you're redirected to the dashboard
4. Use the navigation menu to access Profile and Settings pages
5. Click Logout to return to the login page

## Security Note

⚠️ **Important:** This is a demo application. For production use:
- Change the `secret_key` in `app.py`
- Use a proper database for user credentials
- Implement password hashing (bcrypt, werkzeug.security)
- Add CSRF protection
- Use HTTPS
