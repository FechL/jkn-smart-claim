"""
ML Model Inference Module
Loads trained model and performs fraud score prediction
"""

import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODEL_PATH, SCALER_PATH


def load_model():
    """Load trained Random Forest model"""
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'fraud_detection_model.pkl')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please train the model first using train_model.ipynb")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model


def load_scaler():
    """Load fitted scaler"""
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')
    
    if not os.path.exists(scaler_path):
        return None  # Scaler is optional
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return scaler


def extract_features(ml_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract features from medical data for model input
    
    Args:
        ml_data: Dict containing diagnosis, vital_signs, lab_results, claim_amount
        
    Returns:
        DataFrame with features
    """
    diagnosis = ml_data.get('diagnosis', {})
    vital_signs = ml_data.get('vital_signs', {})
    lab_results = ml_data.get('lab_results', {})
    claim_amount = ml_data.get('claim_amount', 0)
    
    # Map severity to numeric
    severity_map = {'mild': 1, 'moderate': 2, 'severe': 3}
    diagnosis_severity = severity_map.get(diagnosis.get('severity', 'mild'), 1)
    
    # Create feature dict
    features = {
        'diagnosis_severity': diagnosis_severity,
        'systolic_bp': vital_signs.get('systolic_bp', 120),
        'diastolic_bp': vital_signs.get('diastolic_bp', 80),
        'temperature': vital_signs.get('temperature', 36.5),
        'pulse': vital_signs.get('pulse', 75),
        'respiratory_rate': vital_signs.get('respiratory_rate', 18),
        'hemoglobin': lab_results.get('hemoglobin', 14.0),
        'leukocyte': lab_results.get('leukocyte', 7000),
        'platelet': lab_results.get('platelet', 250000),
        'hematocrit': lab_results.get('hematocrit', 42),
        'claim_amount': claim_amount
    }
    
    # Calculate derived features
    features['bp_ratio'] = features['systolic_bp'] / features['diastolic_bp'] if features['diastolic_bp'] > 0 else 1.5
    features['fever'] = 1 if features['temperature'] > 37.5 else 0
    features['tachycardia'] = 1 if features['pulse'] > 100 else 0
    features['tachypnea'] = 1 if features['respiratory_rate'] > 20 else 0
    features['anemia'] = 1 if features['hemoglobin'] < 13.0 else 0
    features['leukopenia'] = 1 if features['leukocyte'] < 4000 else 0
    features['thrombocytopenia'] = 1 if features['platelet'] < 150000 else 0
    
    # Consistency checks (potential fraud indicators)
    # Mild diagnosis but high claim amount
    features['amount_severity_mismatch'] = 1 if (diagnosis_severity == 1 and claim_amount > 2000000) else 0
    
    # Severe diagnosis but normal vitals
    features['vitals_severity_mismatch'] = 1 if (
        diagnosis_severity == 3 and 
        features['fever'] == 0 and 
        features['tachycardia'] == 0
    ) else 0
    
    # Create DataFrame
    df = pd.DataFrame([features])
    
    return df


def preprocess_data(ml_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Preprocessing pipeline for ML data
    
    Args:
        ml_data: Medical data dict
        
    Returns:
        Preprocessed DataFrame ready for model
    """
    # Extract features
    df = extract_features(ml_data)
    
    # Load scaler if available
    scaler = load_scaler()
    if scaler is not None:
        # Scale numerical features
        numerical_cols = [
            'systolic_bp', 'diastolic_bp', 'temperature', 'pulse', 'respiratory_rate',
            'hemoglobin', 'leukocyte', 'platelet', 'hematocrit', 'claim_amount', 'bp_ratio'
        ]
        df[numerical_cols] = scaler.transform(df[numerical_cols])
    
    return df


def predict_fraud_score(ml_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict fraud score using trained model
    Type: flex - score 0-100
    
    Args:
        ml_data: Medical data dict
        
    Returns:
        dict with 'score', 'probability', 'type', 'message'
    """
    try:
        # Load model
        model = load_model()
        
        # Preprocess data
        X = preprocess_data(ml_data)
        
        # Predict probability
        proba = model.predict_proba(X)[0]
        
        # Get fraud probability (assuming class 1 is fraud)
        fraud_proba = proba[1] if len(proba) > 1 else proba[0]
        
        # Convert to score 0-100
        score = int(fraud_proba * 100)
        
        # Determine message based on score
        if score < 30:
            message = "Risiko fraud rendah berdasarkan analisis AI"
        elif score < 60:
            message = "Risiko fraud sedang berdasarkan analisis AI"
        else:
            message = "Risiko fraud tinggi berdasarkan analisis AI"
        
        return {
            'score': score,
            'probability': round(fraud_proba, 3),
            'type': 'flex',
            'flag_name': 'AI Fraud Detection',
            'message': message
        }
        
    except FileNotFoundError as e:
        # Model not trained yet, return default score
        print(f"Warning: {e}")
        print("Returning default score. Please train the model first.")
        
        # Return a random score based on data consistency
        diagnosis_severity = ml_data.get('diagnosis', {}).get('severity', 'mild')
        claim_amount = ml_data.get('claim_amount', 0)
        
        # Simple heuristic for demo
        if diagnosis_severity == 'mild' and claim_amount > 2000000:
            score = np.random.randint(60, 90)
        elif diagnosis_severity == 'severe' and claim_amount < 1000000:
            score = np.random.randint(40, 70)
        else:
            score = np.random.randint(10, 40)
        
        return {
            'score': score,
            'probability': score / 100,
            'type': 'flex',
            'flag_name': 'AI Fraud Detection (Heuristic)',
            'message': f"Skor fraud berdasarkan heuristik (model belum dilatih): {score}/100"
        }


if __name__ == '__main__':
    # Test the module
    import json
    
    # Sample medical data
    sample_ml_data = {
        'diagnosis': {
            'code': 'A91',
            'display': 'Dengue hemorrhagic fever',
            'severity': 'severe'
        },
        'vital_signs': {
            'systolic_bp': 130,
            'diastolic_bp': 85,
            'temperature': 38.5,
            'pulse': 88,
            'respiratory_rate': 20
        },
        'lab_results': {
            'hemoglobin': 13.5,
            'leukocyte': 3200,
            'platelet': 95000,
            'hematocrit': 42
        },
        'claim_amount': 8500000
    }
    
    result = predict_fraud_score(sample_ml_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
