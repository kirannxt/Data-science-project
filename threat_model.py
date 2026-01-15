"""
Intelligent Threat Hunting: ML-Driven Anomaly Detection in Network Traffic
Advanced ML Algorithm for Network Security Threat Detection
"""

import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import StackingClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


class AnomalyDetector:
    """
    Machine Learning model for detecting network traffic anomalies
    Uses Stacking Classifier with multiple base learners and meta-learner
    Trained on network traffic dataset
    """
    
    def __init__(self, dataset_path='network_traffic_dataset.csv'):
        """Initialize the ML model with dataset"""
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.dataset_path = dataset_path
        self.training_data = None
        self.labels = None
        self._load_dataset()
        self._train_model()
    
    def _load_dataset(self):
        """Load network traffic dataset from CSV file"""
        try:
            if not os.path.exists(self.dataset_path):
                print(f"Warning: Dataset file '{self.dataset_path}' not found. Using default data.")
                self._create_default_data()
                return
            
            df = pd.read_csv(self.dataset_path)
            
            required_columns = ['source_ip', 'destination_ip', 'protocol', 'packet_size', 'duration', 'bandwidth', 'label']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Dataset must contain columns: {required_columns}")
            
            # Select numeric features for training
            self.feature_columns = ['packet_size', 'duration', 'bandwidth']
            self.training_data = df[self.feature_columns].values
            self.labels = df['label'].values
            
            print(f"✓ Dataset loaded successfully: {len(self.training_data)} samples")
            print(f"  - Normal traffic: {sum(self.labels == 0)}")
            print(f"  - Anomalous traffic: {sum(self.labels == 1)}")
            
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            self._create_default_data()
    
    def _create_default_data(self):
        """Create default training data if dataset not available"""
        # Normal traffic patterns
        normal_samples = [
            [512, 0.5, 256],      # Normal web traffic
            [1024, 1.0, 512],     # Normal file transfer
            [256, 0.1, 128],      # Normal DNS query
            [2048, 2.0, 1024],    # Normal video streaming
            [512, 0.3, 256],      # Normal email
        ]
        
        # Anomalous traffic patterns
        anomalous_samples = [
            [65535, 10.0, 32768],    # Large packet, long duration (DDoS)
            [50000, 8.0, 25000],     # Unusual traffic volume
            [45000, 12.0, 30000],    # Sustained high bandwidth
            [60000, 15.0, 35000],    # Port scanning pattern
            [55000, 9.0, 28000],     # Malware communication
        ]
        
        self.training_data = np.array(normal_samples + anomalous_samples)
        self.labels = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
        self.feature_columns = ['packet_size', 'duration', 'bandwidth']
        print("✓ Using default training data (10 samples)")
    
    def _train_model(self):
        """Train the Stacking Classifier with multiple base learners"""
        if self.training_data is None or self.labels is None:
            print("Error: No training data available")
            return
        
        try:
            # Scale features
            self.scaler = StandardScaler()
            X = self.scaler.fit_transform(self.training_data)
            
            # Define base learners
            base_learners = [
                ('knn', KNeighborsClassifier(n_neighbors=3, weights='distance')),
                ('rf', RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)),
                ('svc', SVC(kernel='rbf', probability=True, random_state=42)),
                ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42, max_depth=5))
            ]
            
            # Define meta-learner
            meta_learner = LogisticRegression(random_state=42, max_iter=1000)
            
            # Create stacking classifier
            self.model = StackingClassifier(
                estimators=base_learners,
                final_estimator=meta_learner,
                cv=3
            )
            
            self.model.fit(X, self.labels)
            print(f"✓ Stacking Classifier trained successfully with {len(base_learners)} base learners")
            print(f"  - Base Learners: KNN, Random Forest, SVM, Gradient Boosting")
            print(f"  - Meta-Learner: Logistic Regression")
            print(f"  - Features: {X.shape[1]}")
            
        except Exception as e:
            print(f"Error training model: {str(e)}")
    
    def predict(self, packet_size, duration, bandwidth):
        """
        Predict if network traffic is anomalous
        
        Args:
            packet_size (float): Average packet size in bytes
            duration (float): Connection duration in seconds
            bandwidth (float): Bandwidth usage in Kbps
        
        Returns:
            dict: Prediction results with confidence scores
        """
        try:
            # Validate input
            if not all([packet_size, duration, bandwidth]):
                return {
                    'error': 'All parameters are required',
                    'is_anomaly': None,
                    'confidence': 0,
                    'anomaly_probability': 0,
                    'normal_probability': 0
                }
            
            # Create input array
            X = np.array([[packet_size, duration, bandwidth]])
            
            # Scale input
            X_scaled = self.scaler.transform(X)
            
            # Make prediction
            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]
            
            # Calculate confidence
            confidence = max(probabilities) * 100
            
            # Get individual probabilities
            normal_prob = probabilities[0] * 100   # Class 0: Normal
            anomaly_prob = probabilities[1] * 100  # Class 1: Anomaly
            
            return {
                'is_anomaly': prediction == 1,
                'confidence': confidence,
                'anomaly_probability': anomaly_prob,
                'normal_probability': normal_prob,
                'prediction_label': 'ANOMALY DETECTED' if prediction == 1 else 'NORMAL TRAFFIC'
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'is_anomaly': None,
                'confidence': 0,
                'anomaly_probability': 0,
                'normal_probability': 0
            }
    
    def get_model_info(self):
        """Get information about the ML model"""
        total_samples = len(self.labels) if self.labels is not None else 0
        normal_samples = sum(self.labels == 0) if self.labels is not None else 0
        anomalous_samples = sum(self.labels == 1) if self.labels is not None else 0
        
        return {
            'model_type': 'Stacking Classifier (Ensemble)',
            'scaler_type': 'StandardScaler',
            'features': 3,
            'base_learners': ['KNN (k=3)', 'Random Forest (50 trees)', 'SVM (RBF kernel)', 'Gradient Boosting (50 trees)'],
            'meta_learner': 'Logistic Regression',
            'training_samples': total_samples,
            'normal_samples': normal_samples,
            'anomalous_samples': anomalous_samples,
            'data_source': 'network_traffic_dataset.csv'
        }


# Initialize the detector
detector = AnomalyDetector()


def process_network_traffic(packet_size, duration, bandwidth):
    """
    Process network traffic and return anomaly detection results
    
    Args:
        packet_size (float): Average packet size in bytes
        duration (float): Connection duration in seconds
        bandwidth (float): Bandwidth usage in Kbps
    
    Returns:
        dict: Prediction results from the ML model
    """
    result = detector.predict(packet_size, duration, bandwidth)
    return result


def get_detector_info():
    """Get information about the detector model"""
    return detector.get_model_info()
