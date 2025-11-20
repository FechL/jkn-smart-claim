# Smart Claim BPJS Backend

Backend system untuk deteksi fraud klaim BPJS rawat inap.

## Struktur Direktori

```
backend/
├── config.py                 # Konfigurasi sistem
├── main.py                   # Orchestrator utama
├── fraud_detection/          # Modul deteksi fraud
│   ├── check_fraud_pasien.py
│   └── check_fraud_faskes.py
├── ml_model/                 # Model AI
│   └── model_inference.py
├── utils/                    # Utilities
│   ├── data_generator.py
│   └── generate_patient.py
├── data_schemas/             # JSON schemas (FHIR)
├── data/                     # Database JSON
│   ├── faskes_registry.json
│   ├── fraud_history.json
│   ├── patient_history.json
│   └── claims.json
├── models/                   # Saved ML models
└── notebooks/                # Jupyter notebooks
    └── train_model.ipynb
```

## Instalasi

```bash
pip install pandas numpy scikit-learn jupyter
```

## Usage

### 1. Generate Dummy Claim

```bash
cd utils
python generate_patient.py 1  # Good claim (score < 10)
python generate_patient.py 2  # Medium claim (score 10-60)
python generate_patient.py 3  # Bad claim (score > 60)
```

### 2. Process Claim

```bash
python main.py data/generated_claims/CLM-XXXXXXXX-XXXX.json
```

Atau test mode:
```bash
python main.py --test
```

### 3. Train ML Model (Optional)

```bash
jupyter notebook notebooks/train_model.ipynb
```

## Scoring System

- **crucial**: true = auto reject, false = 0
- **flex**: true = 1-100, false = 0
- **high**: true = 15-40, false = 0
- **medium**: true = 5-30, false = 0
- **low**: true = 1-10, false = 0

### Decision Rules

- Score < 10: **Auto Accept**
- Score 10-60: **Needs Review**
- Score > 60: **Auto Reject**

## Red Flag Checks

### Patient Fraud
- NIK validation (crucial)
- JKN card validation (crucial)
- Duplicate phone number (medium)
- Duplicate address (low)

### Faskes Fraud
- Faskes registration (crucial)
- Fraud history (flex, 0-100)

### AI Model
- Medical data consistency check (flex, 0-100)
- Diagnosis-procedure matching
- Claim amount reasonability
