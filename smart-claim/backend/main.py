"""
Main Orchestrator for Smart Claim BPJS Fraud Detection System
Integrates patient fraud, faskes fraud, and AI model inference
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fraud_detection.check_fraud_pasien import check_patient_fraud
from fraud_detection.check_fraud_faskes import check_faskes_fraud
from ml_model.model_inference import predict_fraud_score
from config import SCORE_THRESHOLD_AUTO_ACCEPT, SCORE_THRESHOLD_AUTO_REJECT


def load_database(db_path: str) -> List[Dict]:
    """Load JSON database"""
    if not os.path.exists(db_path):
        return []
    
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_database(db_path: str, data: List[Dict]):
    """Save JSON database"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def process_claim(claim_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a claim through the fraud detection pipeline
    
    Args:
        claim_data: Complete claim data with patient, faskes, and medical_data
        
    Returns:
        dict with fraud detection results and decision
    """
    # Extract components
    patient_data = claim_data.get('patient', {})
    faskes_data = claim_data.get('faskes', {})
    ml_data = claim_data.get('medical_data', {})
    claim_id = claim_data.get('claim_id', 'UNKNOWN')
    
    # Load databases
    patient_db = load_database('smart-claim/backend/data/patient_history.json')
    faskes_db = load_database('smart-claim/backend/data/faskes_registry.json')
    fraud_history_db = load_database('smart-claim/backend/data/fraud_history.json')
    
    print(f"\n{'='*60}")
    print(f"Processing Claim: {claim_id}")
    print(f"{'='*60}")
    
    # Step 1: Check Patient Fraud
    print("\n[1/3] Checking Patient Fraud...")
    patient_fraud_result = check_patient_fraud(patient_data, patient_db)
    print(f"  - Patient Fraud Score: {patient_fraud_result['total_score']}")
    print(f"  - Auto Reject: {patient_fraud_result['auto_reject']}")
    print(f"  - Red Flags: {len(patient_fraud_result['red_flags'])}")
    
    # Step 2: Check Faskes Fraud
    print("\n[2/3] Checking Faskes Fraud...")
    faskes_fraud_result = check_faskes_fraud(faskes_data, faskes_db, fraud_history_db)
    print(f"  - Faskes Fraud Score: {faskes_fraud_result['total_score']}")
    print(f"  - Auto Reject: {faskes_fraud_result['auto_reject']}")
    print(f"  - Red Flags: {len(faskes_fraud_result['red_flags'])}")
    
    # Step 3: AI Model Inference
    print("\n[3/3] Running AI Fraud Detection...")
    ai_fraud_result = predict_fraud_score(ml_data)
    print(f"  - AI Fraud Score: {ai_fraud_result['score']}")
    print(f"  - Confidence: {ai_fraud_result['probability']:.2%}")
    
    # Calculate total score
    total_score = 0
    auto_reject = False
    
    # Check for crucial red flags (auto reject)
    if patient_fraud_result['auto_reject'] or faskes_fraud_result['auto_reject']:
        auto_reject = True
        decision = 'REJECTED'
        decision_reason = 'Auto reject due to crucial red flag violations'
    else:
        # Sum up all scores
        total_score = (
            patient_fraud_result['total_score'] +
            faskes_fraud_result['total_score'] +
            ai_fraud_result['score']
        )
        
        # Determine decision based on total score
        if total_score < SCORE_THRESHOLD_AUTO_ACCEPT:
            decision = 'ACCEPTED'
            decision_reason = f'Auto accept (score: {total_score} < {SCORE_THRESHOLD_AUTO_ACCEPT})'
        elif total_score > SCORE_THRESHOLD_AUTO_REJECT:
            decision = 'REJECTED'
            decision_reason = f'Auto reject (score: {total_score} > {SCORE_THRESHOLD_AUTO_REJECT})'
        else:
            decision = 'NEEDS_REVIEW'
            decision_reason = f'Manual review required (score: {total_score} in range {SCORE_THRESHOLD_AUTO_ACCEPT}-{SCORE_THRESHOLD_AUTO_REJECT})'
    
    # Compile all red flags
    all_red_flags = (
        patient_fraud_result['red_flags'] +
        faskes_fraud_result['red_flags'] +
        [ai_fraud_result]
    )
    
    # Create result
    result = {
        'claim_id': claim_id,
        'timestamp': datetime.now().isoformat(),
        'patient_name': patient_data.get('name', [{}])[0].get('text', 'Unknown'),
        'faskes_name': faskes_data.get('name', 'Unknown'),
        'diagnosis': ml_data.get('diagnosis', {}).get('display', 'Unknown'),
        'claim_amount': ml_data.get('claim_amount', 0),
        'fraud_scores': {
            'patient': patient_fraud_result['total_score'],
            'faskes': faskes_fraud_result['total_score'],
            'ai': ai_fraud_result['score'],
            'total': total_score
        },
        'red_flags': all_red_flags,
        'decision': decision,
        'decision_reason': decision_reason,
        'auto_reject': auto_reject,
        'requires_review': decision == 'NEEDS_REVIEW'
    }
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"FRAUD DETECTION SUMMARY")
    print(f"{'='*60}")
    print(f"Patient: {result['patient_name']}")
    print(f"Faskes: {result['faskes_name']}")
    print(f"Diagnosis: {result['diagnosis']}")
    print(f"Claim Amount: Rp {result['claim_amount']:,}")
    print(f"\nFraud Scores:")
    print(f"  - Patient Fraud: {result['fraud_scores']['patient']}")
    print(f"  - Faskes Fraud: {result['fraud_scores']['faskes']}")
    print(f"  - AI Detection: {result['fraud_scores']['ai']}")
    print(f"  - TOTAL SCORE: {result['fraud_scores']['total']}")
    print(f"\nDecision: {result['decision']}")
    print(f"Reason: {result['decision_reason']}")
    print(f"{'='*60}\n")
    
    # Save result to claims database
    claims_db_path = os.path.join(os.path.dirname(__file__), 'data', 'claims.json')
    claims_db = load_database(claims_db_path)
    claims_db.append(result)
    save_database(claims_db_path, claims_db)
    
    return result


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <claim_file.json>")
        print("   or: python main.py --test")
        sys.exit(1)
    
    if sys.argv[1] == '--test':
        # Run test with sample data
        print("Running test mode with sample data...")
        
        # Load sample data
        with open('data_schemas/pendaftaran_pasien.json', 'r') as f:
            sample_patient = json.load(f)
        
        with open('data_schemas/faskes_schema.json', 'r') as f:
            sample_faskes = json.load(f)
        
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
        
        claim_data = {
            'claim_id': 'CLM-TEST-001',
            'patient': sample_patient,
            'faskes': sample_faskes,
            'medical_data': sample_ml_data
        }
    else:
        # Load claim from file
        claim_file = sys.argv[1]
        
        if not os.path.exists(claim_file):
            print(f"Error: File not found: {claim_file}")
            sys.exit(1)
        
        with open(claim_file, 'r', encoding='utf-8') as f:
            claim_data = json.load(f)
    
    # Process claim
    result = process_claim(claim_data)
    
    # Output result as JSON
    print("\nJSON Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
