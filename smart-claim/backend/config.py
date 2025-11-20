"""
Configuration file for Smart Claim BPJS Fraud Detection System
"""

# Score thresholds
SCORE_THRESHOLD_AUTO_ACCEPT = 10
SCORE_THRESHOLD_AUTO_REJECT = 60

# Red flag type score ranges
RED_FLAG_SCORES = {
    'crucial': {
        'true': 'auto_reject',  # Langsung tolak
        'false': 0
    },
    'flex': {
        'true_min': 1,
        'true_max': 100,
        'false': 0
    },
    'high': {
        'true_min': 15,
        'true_max': 40,
        'false': 0
    },
    'medium': {
        'true_min': 5,
        'true_max': 30,
        'false': 0
    },
    'low': {
        'true_min': 1,
        'true_max': 10,
        'false': 0
    }
}

# NIK validation
NIK_LENGTH = 16

# JKN Card validation
JKN_CARD_LENGTH = 13

# Database paths
PATIENT_DB_PATH = 'smart-claim/backend/data/patient_history.json'
FASKES_DB_PATH = 'smart-claim/backend/data/faskes_registry.json'
FRAUD_HISTORY_DB_PATH = 'smart-claim/backend/data/fraud_history.json'
CLAIMS_DB_PATH = 'smart-claim/backend/data/claims.json'

# Model paths
MODEL_PATH = 'smart-claim/backend/models/fraud_detection_model.pkl'
SCALER_PATH = 'smart-claim/backend/models/scaler.pkl'

# Duplicate detection thresholds
DUPLICATE_PHONE_THRESHOLD = 3  # Jika nomor HP dipakai > 3 pasien berbeda
DUPLICATE_ADDRESS_THRESHOLD = 5  # Jika alamat dipakai > 5 pasien berbeda

# Faskes fraud history score mapping
FASKES_FRAUD_HISTORY_SCORE = {
    'no_history': 0,
    'minor_violation': 20,
    'moderate_violation': 50,
    'severe_violation': 80,
    'blacklisted': 100
}
