from werkzeug.security import generate_password_hash
import json
import os
from datetime import datetime

def create_test_user():
    """Create a test user for the application"""
    
    # Load existing users
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)
    else:
        users = {}
    
    # Create test user
    username = 'testuser'
    email = 'test@example.com'
    password = 'password123'
    
    if username in users:
        print(f"Test user '{username}' already exists!")
        return
    
    users[username] = {
        'email': email,
        'password': generate_password_hash(password),
        'created_at': str(datetime.now()),
        'predictions': []
    }
    
    # Save users
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"✓ Test user created successfully!")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"  Email: {email}")

if __name__ == '__main__':
    create_test_user()
