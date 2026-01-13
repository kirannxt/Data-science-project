import json
import os
from werkzeug.security import generate_password_hash

# Test user credentials
TEST_USERNAME = "fraudtester"
TEST_PASSWORD = "password123"
TEST_EMAIL = "fraudtester@example.com"

def create_test_user():
    """Create a test user for FraudGuard"""
    
    # Check if users.json exists
    users_file = "users.json"
    
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
    else:
        users = {}
    
    # Create the test user
    hashed_password = generate_password_hash(TEST_PASSWORD)
    users[TEST_USERNAME] = {
        "email": TEST_EMAIL,
        "password": hashed_password,
        "created_at": "2024-01-01T00:00:00"
    }
    
    # Save to users.json
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)
    
    print("✓ Test user created successfully!")
    print(f"\nUsername: {TEST_USERNAME}")
    print(f"Password: {TEST_PASSWORD}")
    print(f"Email: {TEST_EMAIL}")
    print("\nYou can now login with these credentials at http://localhost:5000/login")

if __name__ == "__main__":
    create_test_user()
