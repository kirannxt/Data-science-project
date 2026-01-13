"""
AI Against Fraud: Intelligent Detection of Fake Job Listings
Advanced ML Algorithm for Online Recruitment Scam Detection
"""

import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier


class FakeJobPostDetector:
    """
    Machine Learning model for detecting fake job postings
    Uses K-Neighbors Classifier with TF-IDF vectorization
    Trained on real job posting dataset
    """
    
    def __init__(self, dataset_path='job_posts_dataset.csv'):
        """Initialize the ML model with dataset"""
        self.model = None
        self.vectorizer = None
        self.dataset_path = dataset_path
        self.training_data = None
        self.labels = None
        self._load_dataset()
        self._train_model()
    
    def _load_dataset(self):
        """Load job posts dataset from CSV file"""
        try:
            # Check if dataset file exists
            if not os.path.exists(self.dataset_path):
                print(f"Warning: Dataset file '{self.dataset_path}' not found. Using default data.")
                self._create_default_data()
                return
            
            # Load dataset from CSV
            df = pd.read_csv(self.dataset_path)
            
            # Validate required columns
            required_columns = ['job_title', 'company_name', 'job_description', 'salary', 'label']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Dataset must contain columns: {required_columns}")
            
            # Combine text features
            df['combined_text'] = (
                df['job_title'].fillna('') + ' ' +
                df['company_name'].fillna('') + ' ' +
                df['job_description'].fillna('') + ' ' +
                df['salary'].fillna('')
            )
            
            # Extract features and labels
            self.training_data = df['combined_text'].values
            self.labels = df['label'].values
            
            print(f"✓ Dataset loaded successfully: {len(self.training_data)} samples")
            print(f"  - Fake postings: {sum(self.labels == 1)}")
            print(f"  - Legitimate postings: {sum(self.labels == 0)}")
            
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            self._create_default_data()
    
    def _create_default_data(self):
        """Create default training data if dataset not available"""
        training_texts = [
            "Send money to apply",
            "Work from home easy money",
            "No experience needed high pay",
            "Click here to register",
            "Urgent hiring immediate",
            "Free training provided jobs",
            "Make money fast online",
            "Investment required employment",
            "Guaranteed income opportunity",
            "Limited time offer job",
            # Legitimate posts
            "Software Engineer Full Stack Developer Position",
            "We are hiring experienced Python developers for our team",
            "Marketing Manager position at growing tech company",
            "Data Scientist role with competitive salary",
            "Customer Service Representative opportunity",
            "Project Manager needed for enterprise clients",
            "Business Development Executive opening",
            "Quality Assurance Engineer required"
        ]
        
        self.training_data = np.array(training_texts)
        self.labels = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        print("✓ Using default training data (18 samples)")
    
    def _train_model(self):
        """Train the ML model using loaded dataset"""
        if self.training_data is None or self.labels is None:
            print("Error: No training data available")
            return
        
        try:
            # Create TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=200,
                stop_words='english',
                lowercase=True,
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.9
            )
            
            # Transform training texts
            X = self.vectorizer.fit_transform(self.training_data)
            
            # Create and train K-Neighbors classifier
            # n_neighbors set to 5 (default), but can be tuned based on dataset size
            self.model = KNeighborsClassifier(
                n_neighbors=5,
                weights='distance',
                algorithm='auto',
                leaf_size=30,
                p=2,
                metric='minkowski'
            )
            
            self.model.fit(X, self.labels)
            print(f"✓ Model trained successfully with {X.shape[1]} features")
            
        except Exception as e:
            print(f"Error training model: {str(e)}")
    
    def predict(self, job_description, job_title, company_name, salary):
        """
        Predict if a job post is fake or legitimate
        
        Args:
            job_description (str): The job post description
            job_title (str): Job position title
            company_name (str): Company name from the posting
            salary (str): Salary information
        
        Returns:
            dict: Prediction results with confidence scores
        """
        try:
            # Combine all text features
            combined_text = f"{job_title} {company_name} {job_description} {salary}"
            
            # Validate input
            if not combined_text.strip():
                return {
                    'error': 'Job post content is empty',
                    'is_fake': None,
                    'confidence': 0,
                    'fake_probability': 0,
                    'legitimate_probability': 0
                }
            
            # Vectorize the input
            X = self.vectorizer.transform([combined_text])
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            
            # Calculate confidence (highest probability)
            confidence = max(probabilities) * 100
            
            # Get individual probabilities
            legitimate_prob = probabilities[0] * 100  # Class 0: Legitimate
            fake_prob = probabilities[1] * 100        # Class 1: Fake/Scam
            
            return {
                'is_fake': prediction == 1,
                'confidence': confidence,
                'fake_probability': fake_prob,
                'legitimate_probability': legitimate_prob,
                'prediction_label': 'LIKELY SCAM' if prediction == 1 else 'APPEARS LEGITIMATE'
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'is_fake': None,
                'confidence': 0,
                'fake_probability': 0,
                'legitimate_probability': 0
            }
    
    def get_model_info(self):
        """Get information about the ML model"""
        total_samples = len(self.labels) if self.labels is not None else 0
        fake_samples = sum(self.labels == 1) if self.labels is not None else 0
        legitimate_samples = sum(self.labels == 0) if self.labels is not None else 0
        
        return {
            'model_type': 'K-Neighbors Classifier (KNN)',
            'vectorizer_type': 'TF-IDF',
            'features': 200,
            'neighbors': 5,
            'training_samples': total_samples,
            'fake_samples': fake_samples,
            'legitimate_samples': legitimate_samples,
            'data_source': 'job_posts_dataset.csv'
        }


# Initialize the detector
detector = FakeJobPostDetector()


def process_job_post(job_description, job_title, company_name, salary=""):
    """
    Process a job post and return prediction results
    
    Args:
        job_description (str): The job description text
        job_title (str): Job title
        company_name (str): Company name
        salary (str): Salary information
    
    Returns:
        dict: Prediction results from the ML model
    """
    result = detector.predict(job_description, job_title, company_name, salary)
    return result


def get_detector_info():
    """Get information about the detector model"""
    return detector.get_model_info()
