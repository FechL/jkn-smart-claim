# Smart Claim BPJS - Fraud Detection System

Sistem deteksi fraud otomatis untuk klaim BPJS rawat inap menggunakan kombinasi rule-based detection dan machine learning.

![System Architecture](https://img.shields.io/badge/Status-Prototype-yellow) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Next.js](https://img.shields.io/badge/Next.js-14-black)

## 🎯 Overview

Smart Claim BPJS adalah sistem prototipe yang mengotomasi deteksi fraud pada klaim BPJS dengan mengintegrasikan:
- **Rule-based fraud detection** untuk pasien dan faskes
- **Machine Learning model** untuk analisis konsistensi data medis
- **Automated decision making** (Auto Accept/Review/Reject)
- **Dashboard monitoring** dengan Next.js

## 📊 System Flow

```
Pendaftaran Pasien → Fraud Detection → Scoring → Decision
                           ↓
                    ┌──────┴──────┐
                    │             │
              Patient Fraud  Faskes Fraud
                    │             │
                    └──────┬──────┘
                           ↓
                      AI Model
                           ↓
                    Total Score
                           ↓
                    ┌──────┴──────┬──────────┐
                    │             │          │
              Score < 10    Score 10-60  Score > 60
                    │             │          │
              AUTO ACCEPT   NEEDS REVIEW  AUTO REJECT
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm atau yarn

### Installation

```bash
# Clone repository
git clone <repository-url>
cd jkn-smart-claim

# Install backend dependencies
cd smart-claim/backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../..
npm install
```

### Usage

#### 1. Generate Test Claims

```bash
cd smart-claim/backend

# Generate good claim (score < 10, auto accept)
python utils/generate_patient.py 1

# Generate medium claim (score 10-60, needs review)
python utils/generate_patient.py 2

# Generate bad claim (score > 60, auto reject)
python utils/generate_patient.py 3
```

#### 2. Process Claims

```bash
# Process specific claim
python main.py data/generated_claims/CLM-XXXXXXXX-XXXX.json

# Run test mode with sample data
python main.py --test

# Run automated testing
python test_system.py
```

#### 3. (Optional) Train ML Model

```bash
# Open Jupyter notebook
jupyter notebook notebooks/train_model.ipynb

# Run all cells to train and save model
# Model will be saved to models/fraud_detection_model.pkl
```

#### 4. Run Dashboard

```bash
cd ../..
npm run dev
```

Navigate to `http://localhost:3000`

## 📁 Project Structure

```
jkn-smart-claim/
├── smart-claim/
│   ├── backend/                    # Backend fraud detection system
│   │   ├── fraud_detection/        # Fraud detection modules
│   │   ├── ml_model/              # ML model inference
│   │   ├── utils/                 # Data generators
│   │   ├── data_schemas/          # FHIR JSON schemas
│   │   ├── data/                  # JSON databases
│   │   ├── models/                # Saved ML models
│   │   ├── notebooks/             # Jupyter notebooks
│   │   ├── config.py              # Configuration
│   │   ├── main.py                # Main orchestrator
│   │   └── test_system.py         # Automated tests
│   │
│   └── contoh_json/               # Example JSON files
│
├── app/                           # Next.js application
│   ├── data/                      # Mock data
│   ├── claims/                    # Claims pages
│   └── ...
│
└── components/                    # React components
```

## 🔍 Fraud Detection Modules

### 1. Patient Fraud Detection

**File**: `backend/fraud_detection/check_fraud_pasien.py`

| Check | Type | Score | Description |
|-------|------|-------|-------------|
| NIK Validation | crucial | Auto Reject / 0 | Validasi format NIK 16 digit |
| JKN Card Validation | crucial | Auto Reject / 0 | Validasi nomor kartu JKN 13 digit |
| Duplicate Phone | medium | 5-30 | Nomor HP dipakai > 3 pasien |
| Duplicate Address | low | 1-10 | Alamat dipakai > 5 pasien |

### 2. Facility Fraud Detection

**File**: `backend/fraud_detection/check_fraud_faskes.py`

| Check | Type | Score | Description |
|-------|------|-------|-------------|
| Faskes Registration | crucial | Auto Reject / 0 | Validasi faskes terdaftar |
| Fraud History | flex | 0-100 | Riwayat pelanggaran faskes |

### 3. AI Model

**File**: `backend/ml_model/model_inference.py`

- **Algorithm**: Random Forest Classifier
- **Features**: 19 features (diagnosis severity, vital signs, lab results, claim amount, derived features)
- **Output**: Fraud score 0-100 (flex type)
- **Fallback**: Heuristic-based scoring jika model belum dilatih

## 📊 Scoring System

| Red Flag Type | True Score | False Score | Description |
|---------------|------------|-------------|-------------|
| **crucial** | Auto Reject | 0 | Pelanggaran kritis |
| **flex** | 1-100 | 0 | Skor fleksibel |
| **high** | 15-40 | 0 | Risiko tinggi |
| **medium** | 5-30 | 0 | Risiko sedang |
| **low** | 1-10 | 0 | Risiko rendah |

### Decision Rules

- **Score < 10**: Auto Accept ✅
- **Score 10-60**: Needs Manual Review ⚠️
- **Score > 60**: Auto Reject ❌
- **Crucial Red Flag**: Auto Reject (regardless of score) 🚫

## 🧪 Testing

### Automated Testing

```bash
cd smart-claim/backend
python test_system.py
```

Generates and processes 9 claims (3 good, 3 medium, 3 bad) and provides summary report.

### Manual Testing

```bash
# Test patient fraud detection
python fraud_detection/check_fraud_pasien.py

# Test facility fraud detection
python fraud_detection/check_fraud_faskes.py

# Test ML model inference
python ml_model/model_inference.py
```

## 📚 Documentation

- **[Backend README](smart-claim/backend/README.md)** - Detailed backend documentation
- **[Implementation Plan](/.gemini/antigravity/brain/0d0415f0-7a79-43cb-857d-1a0db6f8cb96/implementation_plan.md)** - Technical implementation details
- **[Walkthrough](/.gemini/antigravity/brain/0d0415f0-7a79-43cb-857d-1a0db6f8cb96/walkthrough.md)** - Comprehensive system walkthrough

## 🔧 Configuration

Edit `smart-claim/backend/config.py` to adjust:

- Score thresholds (auto accept/reject)
- Red flag type weights
- Duplicate detection thresholds
- Database paths
- Model paths

## 🎓 Key Features

✅ **FHIR-Compliant**: All data schemas follow SATUSEHAT FHIR standards  
✅ **Modular Design**: Easy to extend with new fraud detection rules  
✅ **Flexible Scoring**: 5 red flag types for granular control  
✅ **ML Fallback**: Works with heuristic if model not trained  
✅ **Realistic Data**: Indonesian-specific data generation (NIK, names, addresses)  
✅ **Automated Testing**: Comprehensive test suite  
✅ **Dashboard Integration**: Next.js dashboard for monitoring  

## 🚧 Limitations & Future Work

### Current Limitations

- JSON file storage (not scalable for production)
- Mock ML model (trained on dummy data)
- No real-time processing
- Limited dashboard features

### Future Enhancements

1. **Database Integration**: PostgreSQL/MongoDB
2. **REST API**: FastAPI/Express backend
3. **Real-time Processing**: Queue system (Celery/RabbitMQ)
4. **Model Retraining**: Automated pipeline with real data
5. **Advanced ML**: Deep learning models
6. **Audit Trail**: Complete logging for compliance
7. **Enhanced Dashboard**:
   - Real-time monitoring
   - Verifikator interface
   - Analytics & reporting
   - Export functionality

## 📝 License

This is a prototype system for demonstration purposes.

## 👥 Contributors

Built as a prototype for BPJS fraud detection system.

## 📞 Support

For questions or issues, please refer to the documentation or create an issue in the repository.

---

**Note**: This is a prototype system using dummy data. For production use, the ML model must be retrained with real data and the system should be integrated with actual BPJS databases.
