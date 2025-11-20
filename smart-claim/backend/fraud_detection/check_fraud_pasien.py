"""
Patient Fraud Detection Module
Checks for fraud indicators in patient registration data
"""

import re
import random
from typing import Dict, List, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import NIK_LENGTH, JKN_CARD_LENGTH, DUPLICATE_PHONE_THRESHOLD, DUPLICATE_ADDRESS_THRESHOLD, RED_FLAG_SCORES


def validate_nik(nik: str) -> Dict[str, Any]:
    """
    Validate NIK (Nomor Induk Kependudukan)
    Type: crucial - true = auto reject, false = 0
    
    Args:
        nik: NIK string
        
    Returns:
        dict with 'is_valid', 'score', 'type', 'message'
    """
    # Check if NIK is string of digits and correct length
    if not isinstance(nik, str):
        return {
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'NIK Invalid',
            'message': 'NIK harus berupa string'
        }
    
    if len(nik) != NIK_LENGTH:
        return {
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'NIK Invalid',
            'message': f'NIK harus {NIK_LENGTH} digit, ditemukan {len(nik)} digit'
        }
    
    if not nik.isdigit():
        return {
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'NIK Invalid',
            'message': 'NIK harus berisi angka saja'
        }
    
    # Basic validation: check province code (first 2 digits)
    province_code = nik[:2]
    if not (11 <= int(province_code) <= 94):
        return {
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'NIK Invalid',
            'message': f'Kode provinsi tidak valid: {province_code}'
        }
    
    return {
        'is_valid': True,
        'score': 0,
        'type': 'crucial',
        'flag_name': 'NIK Valid',
        'message': 'NIK valid'
    }


def validate_jkn_card(card_number: str) -> Dict[str, Any]:
    """
    Validate JKN card number
    Type: crucial - true = auto reject, false = 0
    
    Args:
        card_number: JKN card number string
        
    Returns:
        dict with 'is_valid', 'score', 'type', 'message'
    """
    if not isinstance(card_number, str):
        return {
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'Nomor Kartu JKN Invalid',
            'message': 'Nomor kartu JKN harus berupa string'
        }
    
    if len(card_number) != JKN_CARD_LENGTH:
        return {
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'Nomor Kartu JKN Invalid',
            'message': f'Nomor kartu JKN harus {JKN_CARD_LENGTH} digit, ditemukan {len(card_number)} digit'
        }
    
    if not card_number.isdigit():
        return {
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'Nomor Kartu JKN Invalid',
            'message': 'Nomor kartu JKN harus berisi angka saja'
        }
    
    return {
        'is_valid': True,
        'score': 0,
        'type': 'crucial',
        'flag_name': 'Nomor Kartu JKN Valid',
        'message': 'Nomor kartu JKN valid'
    }


def check_duplicate_phone(phone: str, patient_db: List[Dict]) -> Dict[str, Any]:
    """
    Check if phone number is used by multiple patients
    Type: medium - true = 5-30, false = 0
    
    Args:
        phone: Phone number
        patient_db: List of patient records
        
    Returns:
        dict with 'is_duplicate', 'count', 'score', 'type', 'message'
    """
    # Count how many different patients use this phone number
    count = sum(1 for patient in patient_db if patient.get('phone') == phone)
    
    if count >= DUPLICATE_PHONE_THRESHOLD:
        # Calculate score based on how many duplicates (5-30 range)
        score = min(5 + (count - DUPLICATE_PHONE_THRESHOLD) * 5, 30)
        return {
            'is_duplicate': True,
            'count': count,
            'score': score,
            'type': 'medium',
            'flag_name': 'Nomor HP Duplikat',
            'message': f'Nomor HP digunakan oleh {count} pasien berbeda'
        }
    
    return {
        'is_duplicate': False,
        'count': count,
        'score': 0,
        'type': 'medium',
        'flag_name': 'Nomor HP Unik',
        'message': 'Nomor HP tidak duplikat'
    }


def check_duplicate_address(address: str, patient_db: List[Dict]) -> Dict[str, Any]:
    """
    Check if address is used by multiple patients
    Type: low - true = 1-10, false = 0
    
    Args:
        address: Address string
        patient_db: List of patient records
        
    Returns:
        dict with 'is_duplicate', 'count', 'score', 'type', 'message'
    """
    # Normalize address for comparison (lowercase, remove extra spaces)
    normalized_address = ' '.join(address.lower().split())
    
    # Count how many different patients use similar address
    count = 0
    for patient in patient_db:
        patient_address = patient.get('address', '')
        normalized_patient_address = ' '.join(patient_address.lower().split())
        if normalized_patient_address == normalized_address:
            count += 1
    
    if count >= DUPLICATE_ADDRESS_THRESHOLD:
        # Calculate score based on how many duplicates (1-10 range)
        score = min(1 + (count - DUPLICATE_ADDRESS_THRESHOLD), 10)
        return {
            'is_duplicate': True,
            'count': count,
            'score': score,
            'type': 'low',
            'flag_name': 'Alamat Duplikat',
            'message': f'Alamat digunakan oleh {count} pasien berbeda'
        }
    
    return {
        'is_duplicate': False,
        'count': count,
        'score': 0,
        'type': 'low',
        'flag_name': 'Alamat Unik',
        'message': 'Alamat tidak duplikat'
    }


def check_patient_fraud(patient_data: Dict, patient_db: List[Dict] = None) -> Dict[str, Any]:
    """
    Main function to check patient fraud
    
    Args:
        patient_data: Patient registration data (FHIR Patient resource)
        patient_db: Database of patient history (optional, for duplicate checks)
        
    Returns:
        dict with 'total_score', 'red_flags', 'auto_reject'
    """
    if patient_db is None:
        patient_db = []
    
    red_flags = []
    total_score = 0
    auto_reject = False
    
    # Extract data from FHIR format
    nik = None
    jkn_card = None
    phone = None
    address = None
    
    # Get NIK and JKN card from identifiers
    for identifier in patient_data.get('identifier', []):
        system = identifier.get('system', '')
        if 'nik' in system.lower():
            nik = identifier.get('value')
        elif 'kartu' in system.lower() or 'jkn' in system.lower():
            jkn_card = identifier.get('value')
    
    # Get phone from telecom
    for telecom in patient_data.get('telecom', []):
        if telecom.get('system') == 'phone':
            phone = telecom.get('value')
            break
    
    # Get address
    addresses = patient_data.get('address', [])
    if addresses:
        address = addresses[0].get('text', '')
    
    # Check 1: Validate NIK (crucial)
    if nik:
        nik_result = validate_nik(nik)
        if not nik_result['is_valid']:
            auto_reject = True
            red_flags.append(nik_result)
        elif nik_result['score'] > 0:
            red_flags.append(nik_result)
    else:
        auto_reject = True
        red_flags.append({
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'NIK Tidak Ada',
            'message': 'NIK tidak ditemukan dalam data pasien'
        })
    
    # Check 2: Validate JKN Card (crucial)
    if jkn_card:
        jkn_result = validate_jkn_card(jkn_card)
        if not jkn_result['is_valid']:
            auto_reject = True
            red_flags.append(jkn_result)
        elif jkn_result['score'] > 0:
            red_flags.append(jkn_result)
    else:
        auto_reject = True
        red_flags.append({
            'is_valid': False,
            'score': 100,
            'type': 'crucial',
            'flag_name': 'Nomor Kartu JKN Tidak Ada',
            'message': 'Nomor kartu JKN tidak ditemukan dalam data pasien'
        })
    
    # Check 3: Duplicate phone (medium)
    if phone and patient_db:
        phone_result = check_duplicate_phone(phone, patient_db)
        if phone_result['is_duplicate']:
            total_score += phone_result['score']
            red_flags.append(phone_result)
    
    # Check 4: Duplicate address (low)
    if address and patient_db:
        address_result = check_duplicate_address(address, patient_db)
        if address_result['is_duplicate']:
            total_score += address_result['score']
            red_flags.append(address_result)
    
    return {
        'module': 'patient_fraud',
        'total_score': total_score,
        'red_flags': red_flags,
        'auto_reject': auto_reject
    }


if __name__ == '__main__':
    # Test the module
    import json
    
    # Load sample patient data
    with open('../data_schemas/pendaftaran_pasien.json', 'r') as f:
        sample_patient = json.load(f)
    
    # Test with empty database
    result = check_patient_fraud(sample_patient, [])
    print(json.dumps(result, indent=2, ensure_ascii=False))
