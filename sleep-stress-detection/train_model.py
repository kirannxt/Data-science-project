import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings

warnings.filterwarnings('ignore')

def generate_training_data(n_samples=500):
    """
    Generate synthetic training data for sleep-based stress detection
    Features: sleep_duration, sleep_quality, sleep_cycles, restlessness, 
              heart_rate, wake_ups, caffeine_intake
    """
    np.random.seed(42)
    
    sleep_duration = np.random.normal(7, 1.5, n_samples)  # hours
    sleep_quality = np.random.randint(1, 10, n_samples)  # 1-10 scale
    sleep_cycles = np.random.randint(3, 7, n_samples)  # typically 4-6 cycles
    restlessness = np.random.normal(5, 2, n_samples)  # 0-10 scale
    heart_rate = np.random.normal(65, 10, n_samples)  # BPM
    wake_ups = np.random.randint(0, 6, n_samples)  # number of times
    caffeine_intake = np.random.randint(0, 500, n_samples)  # mg
    
    # Generate stress labels based on features
    stress_level = np.zeros(n_samples, dtype=int)
    
    for i in range(n_samples):
        stress_score = 0
        
        # Low sleep duration increases stress
        if sleep_duration[i] < 6:
            stress_score += 2
        elif sleep_duration[i] > 9:
            stress_score += 1
            
        # Low sleep quality increases stress
        if sleep_quality[i] < 5:
            stress_score += 2
        elif sleep_quality[i] < 7:
            stress_score += 1
            
        # High restlessness increases stress
        if restlessness[i] > 6:
            stress_score += 2
            
        # High heart rate indicates stress
        if heart_rate[i] > 80:
            stress_score += 2
        elif heart_rate[i] > 75:
            stress_score += 1
            
        # Multiple wake-ups increase stress
        if wake_ups[i] > 3:
            stress_score += 2
        elif wake_ups[i] > 1:
            stress_score += 1
            
        # High caffeine intake increases stress
        if caffeine_intake[i] > 300:
            stress_score += 1
            
        # Classify stress level
        if stress_score <= 2:
            stress_level[i] = 0  # Low stress
        elif stress_score <= 5:
            stress_level[i] = 1  # Medium stress
        else:
            stress_level[i] = 2  # High stress
    
    X = np.column_stack([
        sleep_duration, sleep_quality, sleep_cycles, restlessness,
        heart_rate, wake_ups, caffeine_intake
    ])
    
    return X, stress_level


def train_model():
    """Train the stress detection model"""
    print("=" * 60)
    print("SLEEP-BASED STRESS DETECTION - ML MODEL TRAINING")
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
    print("\n4. Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
        bootstrap=True
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
        target_names=['Low Stress', 'Medium Stress', 'High Stress'],
        labels=np.unique(y_test)
    ))
    
    print("\n7. Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_test))
    
    # Feature importance
    print("\n8. Feature Importance:")
    feature_names = [
        'Sleep Duration', 'Sleep Quality', 'Sleep Cycles', 'Restlessness',
        'Heart Rate', 'Wake Ups', 'Caffeine Intake'
    ]
    for name, importance in zip(feature_names, model.feature_importances_):
        print(f"   - {name}: {importance*100:.2f}%")
    
    # Save model
    print("\n9. Saving model files...")
    joblib.dump(model, 'stress_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("   - stress_model.pkl saved")
    print("   - scaler.pkl saved")
    
    print("\n" + "=" * 60)
    print("Model training completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    train_model()
