#!/usr/bin/env python3
"""
Converter: main.py output → mockData.ts format
Converts fraud detection results to frontend-compatible format
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def convert_decision(decision: str) -> str:
    """Convert backend decision to frontend status"""
    mapping = {
        "ACCEPTED": "Diterima",
        "REJECTED": "Ditolak",
        "NEEDS_REVIEW": "Review"
    }
    return mapping.get(decision, "Review")


def convert_to_frontend_format(backend_result: dict) -> dict:
    """
    Convert main.py output to mockData.ts format
    
    Args:
        backend_result: Output from main.py process_claim()
        
    Returns:
        dict in mockData.ts Claim interface format
    """
    # Extract data
    claim_id = backend_result.get('claim_id', 'UNKNOWN')
    timestamp = backend_result.get('timestamp', datetime.now().isoformat())
    
    # Convert timestamp to date
    try:
        dt = datetime.fromisoformat(timestamp.replace('+07:00', ''))
        date_str = dt.strftime('%d %b %Y')
    except:
        date_str = datetime.now().strftime('%d %b %Y')
    
    # Get fraud scores
    fraud_scores = backend_result.get('fraud_scores', {})
    total_score = fraud_scores.get('total', 0)
    
    # Convert red flags
    red_flags = []
    for flag in backend_result.get('red_flags', []):
        # Handle different flag formats
        if isinstance(flag, dict):
            red_flag = {
                "type": flag.get('type', 'medium'),
                "flag_name": flag.get('flag_name', flag.get('name', 'Unknown')),
                "score": flag.get('score', 0),
                "message": flag.get('message', flag.get('reason', ''))
            }
            red_flags.append(red_flag)
    
    # Convert decision
    decision = backend_result.get('decision', 'NEEDS_REVIEW')
    status = convert_decision(decision)
    
    # Create frontend format
    frontend_claim = {
        "id": claim_id,
        "claim_id": claim_id,
        "timestamp": timestamp,
        "date": date_str,
        "patient_name": backend_result.get('patient_name', 'Unknown'),
        "patientName": backend_result.get('patient_name', 'Unknown'),
        "faskes_name": backend_result.get('faskes_name', 'Unknown'),
        "faskesName": backend_result.get('faskes_name', 'Unknown'),
        "diagnosis": backend_result.get('diagnosis', 'Unknown'),
        "claim_amount": backend_result.get('claim_amount', 0),
        "amount": backend_result.get('claim_amount', 0),
        "fraud_scores": {
            "patient": fraud_scores.get('patient', 0),
            "faskes": fraud_scores.get('faskes', 0),
            "ai": fraud_scores.get('ai', 0),
            "total": total_score
        },
        "score": total_score,
        "red_flags": red_flags,
        "redFlags": red_flags,
        "decision": decision,
        "status": status,
        "decision_reason": backend_result.get('decision_reason', ''),
        "auto_reject": backend_result.get('auto_reject', False),
        "requires_review": backend_result.get('requires_review', False)
    }
    
    return frontend_claim


def main():
    """Main converter function"""
    if len(sys.argv) < 2:
        print("Usage: python convert_to_frontend.py <backend_result.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Read backend result
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both single claim and array of claims
    if isinstance(data, list):
        if not data:
            print("Error: Empty claims array")
            sys.exit(1)
        # Use the last claim (most recent)
        backend_result = data[-1]
        print(f"Processing last claim from array: {backend_result.get('claim_id', 'UNKNOWN')}")
    else:
        backend_result = data
    
    # Convert to frontend format
    frontend_claim = convert_to_frontend_format(backend_result)
    
    # Output
    output_file = input_file.replace('.json', '_frontend.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(frontend_claim, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Converted to frontend format: {output_file}")
    print(json.dumps(frontend_claim, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
