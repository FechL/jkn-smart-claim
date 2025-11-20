"""
Data Generator Utilities
Helper functions to generate realistic dummy data for testing
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any


# Indonesian names
FIRST_NAMES_MALE = [
    'Ahmad', 'Budi', 'Dedi', 'Eko', 'Fajar', 'Hadi', 'Indra', 'Joko', 'Kurniawan', 'Made',
    'Nur', 'Oki', 'Putra', 'Rudi', 'Slamet', 'Tono', 'Umar', 'Wawan', 'Yudi', 'Zaki'
]

FIRST_NAMES_FEMALE = [
    'Ani', 'Dewi', 'Eka', 'Fitri', 'Indah', 'Kartika', 'Lestari', 'Maya', 'Nur', 'Putri',
    'Rina', 'Sari', 'Tuti', 'Wati', 'Yuni', 'Zahra', 'Ayu', 'Bunga', 'Citra', 'Diah'
]

LAST_NAMES = [
    'Santoso', 'Wijaya', 'Kusuma', 'Pratama', 'Saputra', 'Setiawan', 'Wibowo', 'Nugroho',
    'Hidayat', 'Permana', 'Ramadan', 'Suryanto', 'Utomo', 'Hakim', 'Firmansyah', 'Gunawan',
    'Hermawan', 'Irawan', 'Kurniawan', 'Maulana'
]

# Indonesian cities
CITIES = [
    'Jakarta Pusat', 'Jakarta Barat', 'Jakarta Timur', 'Jakarta Selatan', 'Jakarta Utara',
    'Bandung', 'Surabaya', 'Medan', 'Semarang', 'Yogyakarta', 'Makassar', 'Palembang',
    'Tangerang', 'Bekasi', 'Depok', 'Bogor'
]

# Street names
STREET_NAMES = [
    'Merdeka', 'Sudirman', 'Thamrin', 'Gatot Subroto', 'Ahmad Yani', 'Diponegoro',
    'Veteran', 'Pemuda', 'Pahlawan', 'Kartini', 'Gajah Mada', 'Hayam Wuruk'
]

# ICD-10 codes for common diagnoses
ICD10_CODES = [
    {'code': 'A91', 'display': 'Dengue hemorrhagic fever', 'severity': 'severe'},
    {'code': 'I10', 'display': 'Essential (primary) hypertension', 'severity': 'moderate'},
    {'code': 'E11', 'display': 'Type 2 diabetes mellitus', 'severity': 'moderate'},
    {'code': 'J18.9', 'display': 'Pneumonia, unspecified', 'severity': 'severe'},
    {'code': 'K35.8', 'display': 'Acute appendicitis', 'severity': 'severe'},
    {'code': 'J06.9', 'display': 'Acute upper respiratory infection', 'severity': 'mild'},
    {'code': 'A09', 'display': 'Gastroenteritis', 'severity': 'mild'},
    {'code': 'M79.3', 'display': 'Myalgia', 'severity': 'mild'},
    {'code': 'R50.9', 'display': 'Fever, unspecified', 'severity': 'mild'},
    {'code': 'I63.9', 'display': 'Cerebral infarction', 'severity': 'severe'}
]

# Faskes names
FASKES_NAMES = [
    'RSUD Cengkareng', 'RS Harapan Kita', 'RS Pondok Indah', 'RSUD Tangerang',
    'RS Siloam', 'RS Mitra Keluarga', 'Puskesmas Tebet', 'Puskesmas Cikini',
    'Klinik Sehat Jaya', 'Klinik Pratama Husada'
]


def generate_nik(valid: bool = True) -> str:
    """Generate NIK (16 digits)"""
    if not valid:
        # Invalid NIK: wrong length or invalid province code
        if random.choice([True, False]):
            return ''.join(random.choices(string.digits, k=random.choice([14, 15, 17])))
        else:
            return '99' + ''.join(random.choices(string.digits, k=14))  # Invalid province
    
    # Valid NIK
    province_codes = list(range(11, 95))  # Valid province codes
    province = str(random.choice(province_codes)).zfill(2)
    city = ''.join(random.choices(string.digits, k=2))
    district = ''.join(random.choices(string.digits, k=2))
    
    # Birth date (DDMMYY)
    birth_year = random.randint(1950, 2005)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    
    # For female, add 40 to day
    gender = random.choice(['M', 'F'])
    if gender == 'F':
        birth_day += 40
    
    birth_date = f"{birth_day:02d}{birth_month:02d}{str(birth_year)[-2:]}"
    
    # Serial number
    serial = ''.join(random.choices(string.digits, k=4))
    
    return province + city + district + birth_date + serial


def generate_jkn_card(valid: bool = True) -> str:
    """Generate JKN card number (13 digits)"""
    if not valid:
        # Invalid: wrong length
        return ''.join(random.choices(string.digits, k=random.choice([11, 12, 14, 15])))
    
    return ''.join(random.choices(string.digits, k=13))


def generate_phone(duplicate: bool = False, duplicate_pool: List[str] = None) -> str:
    """Generate Indonesian phone number"""
    if duplicate and duplicate_pool:
        return random.choice(duplicate_pool)
    
    prefixes = ['0812', '0813', '0821', '0822', '0852', '0853', '0856', '0857']
    prefix = random.choice(prefixes)
    number = ''.join(random.choices(string.digits, k=7))
    return f"+62{prefix[1:]}{number}"


def generate_address(duplicate: bool = False, duplicate_pool: List[str] = None) -> str:
    """Generate Indonesian address"""
    if duplicate and duplicate_pool:
        return random.choice(duplicate_pool)
    
    street = random.choice(STREET_NAMES)
    number = random.randint(1, 999)
    city = random.choice(CITIES)
    postal = random.randint(10000, 99999)
    
    return f"Jl. {street} No. {number}, {city}"


def generate_name(gender: str = None) -> Dict[str, str]:
    """Generate Indonesian name"""
    if gender is None:
        gender = random.choice(['male', 'female'])
    
    if gender == 'male':
        first = random.choice(FIRST_NAMES_MALE)
    else:
        first = random.choice(FIRST_NAMES_FEMALE)
    
    last = random.choice(LAST_NAMES)
    
    return {
        'first': first,
        'last': last,
        'full': f"{first} {last}"
    }


def generate_diagnosis() -> Dict[str, str]:
    """Generate random diagnosis from ICD-10"""
    return random.choice(ICD10_CODES)


def generate_faskes_id(registered: bool = True) -> str:
    """Generate faskes ID"""
    if not registered:
        return f"org-unregistered-{random.randint(1000, 9999)}"
    
    return f"org-example-{random.randint(100, 999):03d}"


def generate_faskes_name() -> str:
    """Generate faskes name"""
    return random.choice(FASKES_NAMES)


def generate_date(days_ago: int = 0) -> str:
    """Generate date in ISO format"""
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime('%Y-%m-%d')


def generate_datetime(hours_ago: int = 0) -> str:
    """Generate datetime in ISO format with timezone"""
    dt = datetime.now() - timedelta(hours=hours_ago)
    return dt.strftime('%Y-%m-%dT%H:%M:%S+07:00')


def generate_vital_signs(abnormal: bool = False) -> Dict[str, float]:
    """Generate vital signs"""
    if abnormal:
        return {
            'systolic_bp': random.randint(140, 180),
            'diastolic_bp': random.randint(90, 110),
            'temperature': round(random.uniform(38.0, 40.0), 1),
            'pulse': random.randint(100, 130),
            'respiratory_rate': random.randint(24, 35)
        }
    else:
        return {
            'systolic_bp': random.randint(110, 130),
            'diastolic_bp': random.randint(70, 85),
            'temperature': round(random.uniform(36.0, 37.5), 1),
            'pulse': random.randint(60, 90),
            'respiratory_rate': random.randint(16, 22)
        }


def generate_lab_results(abnormal: bool = False) -> Dict[str, float]:
    """Generate lab results"""
    if abnormal:
        return {
            'hemoglobin': round(random.uniform(9.0, 12.0), 1),
            'leukocyte': random.randint(2000, 3500),
            'platelet': random.randint(50000, 120000),
            'hematocrit': random.randint(30, 38)
        }
    else:
        return {
            'hemoglobin': round(random.uniform(13.0, 16.0), 1),
            'leukocyte': random.randint(4000, 10000),
            'platelet': random.randint(150000, 400000),
            'hematocrit': random.randint(40, 50)
        }


def generate_claim_amount(diagnosis_severity: str) -> int:
    """Generate claim amount based on diagnosis severity"""
    if diagnosis_severity == 'severe':
        return random.randint(5000000, 20000000)
    elif diagnosis_severity == 'moderate':
        return random.randint(1000000, 5000000)
    else:  # mild
        return random.randint(200000, 1000000)


if __name__ == '__main__':
    # Test generators
    print("NIK (valid):", generate_nik(True))
    print("NIK (invalid):", generate_nik(False))
    print("JKN Card (valid):", generate_jkn_card(True))
    print("JKN Card (invalid):", generate_jkn_card(False))
    print("Phone:", generate_phone())
    print("Address:", generate_address())
    print("Name:", generate_name())
    print("Diagnosis:", generate_diagnosis())
    print("Faskes ID:", generate_faskes_id())
    print("Vital Signs (normal):", generate_vital_signs(False))
    print("Vital Signs (abnormal):", generate_vital_signs(True))
    print("Lab Results (normal):", generate_lab_results(False))
    print("Lab Results (abnormal):", generate_lab_results(True))
