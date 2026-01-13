import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings

warnings.filterwarnings('ignore')

def generate_training_data(n_samples=500):
    """
    Generate synthetic training data for fake job listing detection
    Features: salary_range, company_verified, location_specific, 
              job_description_length, contact_verification, posting_age,
              grammatical_errors, keyword_count
    """
    np.random.seed(42)
    
    salary_range = np.random.randint(20000, 150000, n_samples)
    company_verified = np.random.randint(0, 2, n_samples)  # 0 or 1
    location_specific = np.random.randint(0, 2, n_samples)  # 0 or 1
    job_description_length = np.random.randint(100, 2000, n_samples)
    contact_verification = np.random.randint(0, 2, n_samples)  # 0 or 1
    posting_age = np.random.randint(1, 365, n_samples)  # days
    grammatical_errors = np.random.randint(0, 50, n_samples)
    keyword_count = np.random.randint(5, 100, n_samples)
    
    # Generate fraud labels based on features
    fraud_label = np.zeros(n_samples, dtype=int)
    
    for i in range(n_samples):
        fraud_score = 0
        
        # Unusual salary ranges indicate fraud
        if salary_range[i] < 25000 or salary_range[i] > 120000:
            fraud_score += 2
        
        # Unverified company increases fraud risk
        if company_verified[i] == 0:
            fraud_score += 3
        
        # Vague location decreases fraud risk
        if location_specific[i] == 0:
            fraud_score += 2
        
        # Too short or too long descriptions
        if job_description_length[i] < 200:
            fraud_score += 2
        elif job_description_length[i] > 1500:
            fraud_score += 1
        
        # Unverified contact information
        if contact_verification[i] == 0:
            fraud_score += 3
        
        # Very old postings may be spam
        if posting_age[i] > 180:
            fraud_score += 2
        
        # Many grammatical errors indicate fraud
        if grammatical_errors[i] > 20:
            fraud_score += 3
        elif grammatical_errors[i] > 10:
            fraud_score += 1
        
        # Unusual keyword density
        if keyword_count[i] < 10 or keyword_count[i] > 80:
            fraud_score += 2
        
        # Classify as fraud or legitimate
        if fraud_score >= 6:
            fraud_label[i] = 1  # Fraudulent
        else:
            fraud_label[i] = 0  # Legitimate
    
    X = np.column_stack([
        salary_range, company_verified, location_specific,
        job_description_length, contact_verification, posting_age,
        grammatical_errors, keyword_count
    ])
    
    return X, fraud_label


def train_model():
    """Train the fraud detection model"""
    print("=" * 60)
    print("JOB FRAUD DETECTION - ML MODEL TRAINING")
    print("=" * 60)
    
    # Generate data
    print("\n1. Generating synthetic training data...")
    X, y = generate_training_data(n_samples=500)
    print(f"   - Generated {X.shape[0]} samples with {X.shape[1]} features")
    
    # Split data
    print("\n2. Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   - Training set: {X_train.shape[0]} samples")
    print(f"   - Testing set: {X_test.shape[0]} samples")
    
    # Normalize features
    print("\n3. Normalizing features with StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   - Features normalized successfully")
    
    # Train model
    print("\n4. Training Gradient Boosting Classifier...")
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=7,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    print("   - Model training completed")
    
    # Evaluate
    print("\n5. Evaluating model performance...")
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    
    print(f"   - Training Accuracy: {train_accuracy*100:.2f}%")
    print(f"   - Testing Accuracy: {test_accuracy*100:.2f}%")
    
    print("\n6. Detailed Classification Report:")
    print(classification_report(
        y_test, y_pred_test,
        target_names=['Legitimate', 'Fraudulent'],
        labels=np.unique(y_test)
    ))
    
    print("\n7. Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_test))
    
    # Feature importance
    print("\n8. Feature Importance:")
    feature_names = [
        'Salary Range', 'Company Verified', 'Location Specific',
        'Description Length', 'Contact Verified', 'Posting Age',
        'Grammatical Errors', 'Keyword Count'
    ]
    for name, importance in zip(feature_names, model.feature_importances_):
        print(f"   - {name}: {importance*100:.2f}%")
    
    # Save model
    print("\n9. Saving model files...")
    joblib.dump(model, 'fraud_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("   - fraud_model.pkl saved")
    print("   - scaler.pkl saved")
    
    print("\n" + "=" * 60)
    print("Model training completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    train_model()
