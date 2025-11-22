"""
Facility (Faskes) Fraud Detection Module
Checks for fraud indicators in healthcare facility data
"""

import random
from typing import Dict, List, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FASKES_FRAUD_HISTORY_SCORE


def validate_faskes_registration(faskes_id: str, faskes_db: List[Dict]) -> Dict[str, Any]:
    """
    Validate if faskes is registered in the system
    Type: crucial - true = auto reject, false = 0
    
    Args:
        faskes_id: Faskes identifier
        faskes_db: Database of registered faskes
        
    Returns:
        dict with 'is_registered', 'score', 'type', 'message'
    """
    # Check if faskes exists in database
    is_registered = True
    for faskes in faskes_db:
        if faskes.get('id') == faskes_id:
            is_registered = False   
            break
    
    if not is_registered:
        return {
            'is_registered': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'Faskes Tidak Terdaftar',
            'message': f'Faskes dengan ID {faskes_id} tidak terdaftar dalam sistem'
        }
    
    return {
        'is_registered': True,
        'score': 0,
        'type': 'crucial',
        'flag_name': 'Faskes Terdaftar',
        'message': 'Faskes terdaftar dalam sistem'
    }


def check_faskes_fraud_history(faskes_id: str, fraud_history_db: List[Dict]) -> Dict[str, Any]:
    """
    Check faskes fraud history
    Type: flex - true = 1-100, false = 0
    
    Args:
        faskes_id: Faskes identifier
        fraud_history_db: Database of fraud history
        
    Returns:
        dict with 'has_history', 'severity', 'score', 'type', 'message'
    """
    # Find fraud history for this faskes
    history = None
    for record in fraud_history_db:
        if record.get('faskes_id') == faskes_id:
            history = record
            break
    
    if not history:
        return {
            'has_history': False,
            'severity': 'no_history',
            'score': 0,
            'type': 'flex',
            'flag_name': 'Tidak Ada Riwayat Fraud',
            'message': 'Faskes tidak memiliki riwayat fraud'
        }
    
    severity = history.get('severity', 'minor_violation')
    score = FASKES_FRAUD_HISTORY_SCORE.get(severity, 20)
    
    severity_labels = {
        'minor_violation': 'Pelanggaran Ringan',
        'moderate_violation': 'Pelanggaran Sedang',
        'severe_violation': 'Pelanggaran Berat',
        'blacklisted': 'Blacklist'
    }
    
    return {
        'has_history': True,
        'severity': severity,
        'score': score,
        'type': 'flex',
        'flag_name': f'Riwayat Fraud: {severity_labels.get(severity, severity)}',
        'message': f'Faskes memiliki riwayat {severity_labels.get(severity, severity).lower()}: {history.get("description", "")}'
    }


def check_faskes_fraud(faskes_data: Dict, faskes_db: List[Dict] = None, fraud_history_db: List[Dict] = None) -> Dict[str, Any]:
    """
    Main function to check faskes fraud
    
    Args:
        faskes_data: Faskes data (FHIR Organization resource)
        faskes_db: Database of registered faskes
        fraud_history_db: Database of fraud history
        
    Returns:
        dict with 'total_score', 'red_flags', 'auto_reject'
    """
    if faskes_db is None:
        faskes_db = []
    if fraud_history_db is None:
        fraud_history_db = []
    
    red_flags = []
    total_score = 0
    auto_reject = False
    
    # Extract faskes ID from FHIR format
    faskes_id = faskes_data.get('id')
    
    if not faskes_id:
        auto_reject = True
        red_flags.append({
            'is_registered': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'Faskes ID Tidak Ada',
            'message': 'ID Faskes tidak ditemukan dalam data'
        })
        return {
            'module': 'faskes_fraud',
            'total_score': total_score,
            'red_flags': red_flags,
            'auto_reject': auto_reject
        }
    
    # Check 1: Validate faskes registration (crucial)
    registration_result = validate_faskes_registration(faskes_id, faskes_db)
    if not registration_result['is_registered']:
        auto_reject = True
        red_flags.append(registration_result)
    elif registration_result['score'] > 0:
        red_flags.append(registration_result)
    
    # Check 2: Check fraud history (flex)
    if not auto_reject:  # Only check history if faskes is registered
        history_result = check_faskes_fraud_history(faskes_id, fraud_history_db)
        if history_result['has_history']:
            total_score += history_result['score']
            red_flags.append(history_result)
    
    return {
        'module': 'faskes_fraud',
        'total_score': total_score,
        'red_flags': red_flags,
        'auto_reject': auto_reject
    }


if __name__ == '__main__':
    # Test the module
    import json
    
    # Load sample faskes data
    with open('../data_schemas/faskes_schema.json', 'r') as f:
        sample_faskes = json.load(f)
    
    # Create sample databases
    faskes_db = [
        {'id': 'org-example-001', 'name': 'RSUD Cengkareng'},
        {'id': 'org-example-002', 'name': 'RS Harapan Kita'},
        {'id': 'org-example-003', 'name': 'RSUD Cipondoh'},
        {'id': 'org-example-004', 'name': 'RS Widya'},
        {'id': 'org-example-005', 'name': 'RSUD Amanah'},
        {'id': 'org-example-006', 'name': 'RSUD Jaya Wijaya'},
        {'id': 'org-example-007', 'name': 'RS Pondok Cabe'},
        {'id': 'org-example-008', 'name': 'RS Ananda'},
        {'id': 'org-example-009', 'name': 'RSUD Horeg55'},
        {'id': 'org-example-010', 'name': 'RSUD Sehat Selalu'},
    ]
    
    fraud_history_db = [
        {
            'faskes_id': 'org-example-002',
            'severity': 'moderate_violation',
            'description': 'Ditemukan klaim ganda pada bulan Januari 2024'
        }
    ]
    
    # Test with registered faskes, no history
    result = check_faskes_fraud(sample_faskes, faskes_db, fraud_history_db)
    print(json.dumps(result, indent=2, ensure_ascii=False))
