"""
Fraud Detection Package
"""

from .check_fraud_pasien import check_patient_fraud
from .check_fraud_faskes import check_faskes_fraud

__all__ = ['check_patient_fraud', 'check_faskes_fraud']
