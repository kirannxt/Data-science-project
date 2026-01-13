"""
Machine Learning Model Training Script
Uses ExtraTreesClassifier to predict smartphone addiction levels
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_training_data(n_samples=500):
    """
    Generate synthetic training data for smartphone addiction prediction
    
    Features:
    - daily_usage: Hours spent on phone daily (0-24)
    - screen_time: Screen on time score (0-10)
    - notification_checks: Frequency of checking notifications (0-10)
    - sleep_disruption: Impact on sleep quality (0-10)
    - social_anxiety: Anxiety when phone is away (0-10)
    - fomo_score: Fear of missing out score (0-10)
    
    Target:
    - addiction_level: 0 (Low), 1 (Medium), 2 (High)
    """
    
    # Generate features
    daily_usage = np.random.uniform(1, 24, n_samples)
    screen_time = np.random.uniform(0, 10, n_samples)
    notification_checks = np.random.uniform(0, 10, n_samples)
    sleep_disruption = np.random.uniform(0, 10, n_samples)
    social_anxiety = np.random.uniform(0, 10, n_samples)
    fomo_score = np.random.uniform(0, 10, n_samples)
    
    # Create feature matrix
    X = np.column_stack([
        daily_usage,
        screen_time,
        notification_checks,
        sleep_disruption,
        social_anxiety,
        fomo_score
    ])
    
    # Generate target based on weighted combination of features
    weighted_score = (
        daily_usage * 0.25 +
        screen_time * 0.15 +
        notification_checks * 0.15 +
        sleep_disruption * 0.15 +
        social_anxiety * 0.15 +
        fomo_score * 0.15
    )
    
    # Normalize to 0-10 scale
    normalized_score = (weighted_score / 24) * 10
    
    # Create labels: Low (0-3), Medium (3-7), High (7-10)
    y = np.where(normalized_score < 3.3, 0,
                 np.where(normalized_score < 6.7, 1, 2))
    
    return X, y

def train_model():
    """Train ExtraTreesClassifier model"""
    
    print("=" * 60)
    print("SMARTPHONE ADDICTION PREDICTION - ML MODEL TRAINING")
    print("=" * 60)
    
    # Generate training data
    print("\n1. Generating training data...")
    X, y = generate_training_data(n_samples=500)
    print(f"   - Generated {X.shape[0]} samples with {X.shape[1]} features")
    print(f"   - Class distribution:")
    unique, counts = np.unique(y, return_counts=True)
    for label, count in zip(unique, counts):
        risk_level = ["Low", "Medium", "High"][label]
        print(f"     * {risk_level}: {count} samples")
    
    # Split data into training and testing sets
    print("\n2. Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   - Training set: {X_train.shape[0]} samples")
    print(f"   - Testing set: {X_test.shape[0]} samples")
    
    # Normalize features
    print("\n3. Normalizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   - Features normalized using StandardScaler")
    
    # Train ExtraTreesClassifier
    print("\n4. Training ExtraTreesClassifier model...")
    model = ExtraTreesClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        bootstrap=True
    )
    
    model.fit(X_train_scaled, y_train)
    print("   - Model trained successfully!")
    
    # Evaluate model
    print("\n5. Model Evaluation:")
    
    # Training accuracy
    train_pred = model.predict(X_train_scaled)
    train_accuracy = accuracy_score(y_train, train_pred)
    print(f"   - Training Accuracy: {train_accuracy:.4f}")
    
    # Testing accuracy
    test_pred = model.predict(X_test_scaled)
    test_accuracy = accuracy_score(y_test, test_pred)
    print(f"   - Testing Accuracy: {test_accuracy:.4f}")
    
    # Classification report
    print("\n   Classification Report (Test Set):")
    report = classification_report(
        y_test, test_pred,
        target_names=['Low Risk', 'Medium Risk', 'High Risk'],
        labels=np.unique(y_test),
        zero_division=0
    )
    print(report)
    
    # Confusion matrix
    print("   Confusion Matrix:")
    cm = confusion_matrix(y_test, test_pred)
    print(cm)
    
    # Feature importance
    print("\n6. Feature Importance:")
    feature_names = [
        'Daily Usage',
        'Screen Time',
        'Notification Checks',
        'Sleep Disruption',
        'Social Anxiety',
        'FOMO Score'
    ]
    importances = model.feature_importances_
    for name, importance in zip(feature_names, importances):
        print(f"   - {name}: {importance:.4f}")
    
    # Save model and scaler
    print("\n7. Saving model and scaler...")
    model_dir = os.path.dirname(os.path.abspath(__file__))
    
    model_path = os.path.join(model_dir, 'addiction_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"   - Model saved to: {model_path}")
    print(f"   - Scaler saved to: {scaler_path}")
    
    print("\n" + "=" * 60)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return model, scaler

if __name__ == '__main__':
    train_model()
