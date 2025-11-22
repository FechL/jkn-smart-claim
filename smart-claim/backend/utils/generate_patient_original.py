#!/usr/bin/env python3
"""
Generate Patient Data Script
Generates dummy patient claim data with specified quality level

Usage:
    python generate_patient.py <quality_level>
    
    quality_level:
        1 = Good claim (score < 10, auto accept)
        2 = Medium claim (score 10-60, needs review)
        3 = Bad claim (score > 60, auto reject)
"""

import sys
import json
import os
import random
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_generator import (
    generate_nik, generate_jkn_card, generate_phone, generate_address,
    generate_name, generate_diagnosis, generate_faskes_id, generate_faskes_name,
    generate_date, generate_datetime, generate_vital_signs, generate_lab_results,
    generate_claim_amount
)


def generate_patient_data(quality: int) -> dict:
    """
    Generate patient registration data based on quality level
    
    Args:
        quality: 1 (good), 2 (medium), 3 (bad)
        
    Returns:
        FHIR Patient resource
    """
    gender = random.choice(['male', 'female'])
    name_data = generate_name(gender)
    
    # For quality 3 (bad), sometimes use invalid NIK/JKN
    nik_valid = True if quality != 3 else random.choice([True, False, False])
    jkn_valid = True if quality != 3 else random.choice([True, False, False])
    
    patient_id = f"patient-{random.randint(10000, 99999)}"
    
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": [
            {
                "system": "https://fhir.bpjs.go.id/sid/nik",
                "value": generate_nik(nik_valid)
            },
            {
                "system": "https://fhir.bpjs.go.id/sid/no-kartu",
                "value": generate_jkn_card(jkn_valid)
            }
        ],
        "name": [
            {
                "text": name_data['full'],
                "family": name_data['last'],
                "given": [name_data['first']]
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": generate_phone()
            }
        ],
        "gender": gender,
        "birthDate": generate_date(random.randint(365*20, 365*70)),
        "address": [
            {
                "text": generate_address(),
                "city": random.choice(['Jakarta Pusat', 'Jakarta Barat', 'Bandung', 'Surabaya']),
                "postalCode": str(random.randint(10000, 99999)),
                "country": "ID"
            }
        ],
        "active": True
    }
    
    return patient


def generate_faskes_data(quality: int) -> dict:
    """
    Generate faskes data based on quality level
    
    Args:
        quality: 1 (good), 2 (medium), 3 (bad)
        
    Returns:
        FHIR Organization resource
    """
    # For quality 3 (bad), sometimes use unregistered faskes
    registered = True if quality != 3 else random.choice([True, False])
    
    faskes_id = generate_faskes_id(registered)
    faskes_name = generate_faskes_name()
    
    faskes = {
        "resourceType": "Organization",
        "id": faskes_id,
        "identifier": [
            {
                "use": "official",
                "system": "https://fhir.bpjs.go.id/sid/kode-faskes",
                "value": str(random.randint(1000000000, 9999999999))
            }
        ],
        "active": True,
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                        "code": "prov",
                        "display": "Healthcare Provider"
                    }
                ]
            }
        ],
        "name": faskes_name,
        "telecom": [
            {
                "system": "phone",
                "value": generate_phone(),
                "use": "work"
            }
        ],
        "address": [
            {
                "use": "work",
                "type": "physical",
                "line": [generate_address()],
                "city": random.choice(['Jakarta Barat', 'Jakarta Pusat', 'Tangerang']),
                "postalCode": str(random.randint(10000, 99999)),
                "country": "ID"
            }
        ]
    }
    
    return faskes


def generate_ml_data(quality: int, patient_id: str) -> dict:
    """
    Generate medical data for ML model
    
    Args:
        quality: 1 (good), 2 (medium), 3 (bad)
        patient_id: Patient ID
        
    Returns:
        dict with anamnesis, vital signs, lab results, diagnosis, procedures
    """
    diagnosis = generate_diagnosis()
    
    # Adjust abnormality based on quality
    # Quality 1 (good): consistent data
    # Quality 2 (medium): some inconsistencies
    # Quality 3 (bad): major inconsistencies
    
    if quality == 1:
        # Good: diagnosis matches severity, labs match diagnosis
        abnormal_vitals = diagnosis['severity'] in ['moderate', 'severe']
        abnormal_labs = diagnosis['severity'] == 'severe'
    elif quality == 2:
        # Medium: some inconsistencies
        abnormal_labs = random.choice([True, False])
        abnormal_vitals = random.choice([True, False])
    else:
        # Bad: major inconsistencies (mild diagnosis but severe labs, etc.)
        abnormal_vitals = random.choice([True, True, False])
        abnormal_labs = random.choice([True, True, False])
    
    vital_signs = generate_vital_signs(abnormal_vitals)
    lab_results = generate_lab_results(abnormal_labs)
    
    # Generate claim amount
    # For quality 3, sometimes inflate the amount
    if quality == 3 and random.random() < 0.5:
        claim_amount = generate_claim_amount('severe') * random.uniform(1.5, 3.0)
    else:
        claim_amount = generate_claim_amount(diagnosis['severity'])
    
    return {
        'diagnosis': diagnosis,
        'vital_signs': vital_signs,
        'lab_results': lab_results,
        'claim_amount': int(claim_amount),
        'patient_id': patient_id
    }


def run_smart_claim(quality: int) -> dict:
    """
    Generate complete claim data and simulate processing
    
    Args:
        quality: 1 (good), 2 (medium), 3 (bad)
        
    Returns:
        Complete claim data with all components
    """
    # Generate all data
    patient_data = generate_patient_data(quality)
    faskes_data = generate_faskes_data(quality)
    ml_data = generate_ml_data(quality, patient_data['id'])
    
    # Create complete claim package
    claim = {
        'claim_id': f"CLM-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
        'timestamp': generate_datetime(0),
        'patient': patient_data,
        'faskes': faskes_data,
        'medical_data': ml_data,
        'quality_level': quality,
        'quality_label': {1: 'good', 2: 'medium', 3: 'bad'}[quality]
    }
    
    return claim


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_patient.py <quality_level>")
        print("  quality_level:")
        print("    1 = Good claim (score < 10, auto accept)")
        print("    2 = Medium claim (score 10-60, needs review)")
        print("    3 = Bad claim (score > 60, auto reject)")
        sys.exit(1)
    
    try:
        quality = int(sys.argv[1])
        if quality not in [1, 2, 3]:
            raise ValueError("Quality level must be 1, 2, or 3")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Generate claim
    claim = run_smart_claim(quality)
    
    # Save to file
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'generated_claims')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{claim['claim_id']}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(claim, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {claim['quality_label']} claim: {claim['claim_id']}")
    print(f"  Patient: {claim['patient']['name'][0]['text']}")
    print(f"  Faskes: {claim['faskes']['name']}")
    print(f"  Diagnosis: {claim['medical_data']['diagnosis']['display']}")
    print(f"  Amount: Rp {claim['medical_data']['claim_amount']:,}")
    print(f"  Saved to: {output_file}")
    
    # AUTO-PROCESS: Run main.py
    print(f"\n{'='*60}")
    print("AUTO-PROCESSING THROUGH FRAUD DETECTION")
    print(f"{'='*60}\n")
    
    import subprocess
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_py = os.path.join(backend_dir, 'main.py')
    
    result = subprocess.run(
        [sys.executable, main_py, output_file],
        cwd=backend_dir
    )
    
    if result.returncode == 0:
        print(f"\n✓ Claim processed successfully!")
        print(f"  Check: smart-claim/backend/data/claims.json")
    else:
        print(f"\n✗ Error processing claim")
    
    # Also print to stdout for piping
    print("\n" + "="*60)
    print(json.dumps(claim, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
