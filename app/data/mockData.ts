
export interface RedFlag {
        type: string
        flag_name: string
        score: number | string
        message: string
}

export interface FraudScores {
        patient: number
        faskes: number
        ai: number
        total: number
}

export interface Claim {
        id: string
        claim_id: string
        timestamp: string
        date: string
        patient_name: string
        patientName: string
        faskes_name: string
        faskesName: string
        diagnosis: string
        claim_amount: number
        amount: number
        fraud_scores: FraudScores
        score: number
        red_flags: RedFlag[]
        redFlags: RedFlag[]
        decision: "ACCEPTED" | "REJECTED" | "NEEDS_REVIEW"
        status: "Diterima" | "Ditolak" | "Review" | "Review Diterima" | "Review Ditolak"
        decision_reason: string
        auto_reject: boolean
        requires_review: boolean
}

export const mockClaims: Claim[] = [{
        id: "CLM-2024-001",
        claim_id: "CLM-2024-001",
        timestamp: "2024-11-20T10:30:00+07:00",
        date: "20 Nov 2024",
        patient_name: "Budi Santoso",
        patientName: "Budi Santoso",
        faskes_name: "RSUD Cengkareng",
        faskesName: "RSUD Cengkareng",
        diagnosis: "Demam Berdarah Dengue",
        claim_amount: 4500000,
        amount: 4500000,
        fraud_scores: {
                patient: 0,
                faskes: 0,
                ai: 8,
                total: 8
        },
        score: 8,
        red_flags: [
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 8,
                        message: "Risiko fraud rendah berdasarkan analisis AI"
                }
        ],
        redFlags: [
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 8,
                        message: "Risiko fraud rendah berdasarkan analisis AI"
                }
        ],
        decision: "ACCEPTED",
        status: "Diterima",
        decision_reason: "Auto accept (score: 8 < 10)",
        auto_reject: false,
        requires_review: false
},
{
        id: "CLM-2024-002",
        claim_id: "CLM-2024-002",
        timestamp: "2024-11-20T11:15:00+07:00",
        date: "20 Nov 2024",
        patient_name: "Siti Aminah",
        patientName: "Siti Aminah",
        faskes_name: "Klinik Sehat Jaya",
        faskesName: "Klinik Sehat Jaya",
        diagnosis: "Hipertensi",
        claim_amount: 1200000,
        amount: 1200000,
        fraud_scores: {
                patient: 15,
                faskes: 20,
                ai: 25,
                total: 60
        },
        score: 60,
        red_flags: [
                {
                        type: "medium",
                        flag_name: "Nomor HP Duplikat",
                        score: 15,
                        message: "Nomor HP digunakan oleh 4 pasien berbeda"
                },
                {
                        type: "flex",
                        flag_name: "Riwayat Fraud: Pelanggaran Ringan",
                        score: 20,
                        message: "Faskes memiliki riwayat pelanggaran ringan"
                },
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 25,
                        message: "Risiko fraud rendah berdasarkan analisis AI"
                }
        ],
        redFlags: [
                {
                        type: "medium",
                        flag_name: "Nomor HP Duplikat",
                        score: 15,
                        message: "Nomor HP digunakan oleh 4 pasien berbeda"
                },
                {
                        type: "flex",
                        flag_name: "Riwayat Fraud: Pelanggaran Ringan",
                        score: 20,
                        message: "Faskes memiliki riwayat pelanggaran ringan"
                },
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 25,
                        message: "Risiko fraud rendah berdasarkan analisis AI"
                }
        ],
        decision: "NEEDS_REVIEW",
        status: "Review",
        decision_reason: "Manual review required (score: 60 in range 10-60)",
        auto_reject: false,
        requires_review: true
},
{
        id: "CLM-2024-003",
        claim_id: "CLM-2024-003",
        timestamp: "2024-11-20T09:45:00+07:00",
        date: "20 Nov 2024",
        patient_name: "Joko Widodo",
        patientName: "Joko Widodo",
        faskes_name: "RS Harapan Kita",
        faskesName: "RS Harapan Kita",
        diagnosis: "Diabetes Mellitus",
        claim_amount: 8500000,
        amount: 8500000,
        fraud_scores: {
                patient: 0,
                faskes: 50,
                ai: 75,
                total: 125
        },
        score: 125,
        red_flags: [
                {
                        type: "flex",
                        flag_name: "Riwayat Fraud: Pelanggaran Sedang",
                        score: 50,
                        message: "Faskes memiliki riwayat pelanggaran sedang: Ditemukan klaim ganda"
                },
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 75,
                        message: "Risiko fraud tinggi berdasarkan analisis AI"
                }
        ],
        redFlags: [
                {
                        type: "flex",
                        flag_name: "Riwayat Fraud: Pelanggaran Sedang",
                        score: 50,
                        message: "Faskes memiliki riwayat pelanggaran sedang: Ditemukan klaim ganda"
                },
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 75,
                        message: "Risiko fraud tinggi berdasarkan analisis AI"
                }
        ],
        decision: "REJECTED",
        status: "Ditolak",
        decision_reason: "Auto reject (score: 125 > 60)",
        auto_reject: false,
        requires_review: false
},
{
        id: "CLM-2024-004",
        claim_id: "CLM-2024-004",
        timestamp: "2024-11-20T14:20:00+07:00",
        date: "20 Nov 2024",
        patient_name: "Rina Wati",
        patientName: "Rina Wati",
        faskes_name: "Puskesmas Tebet",
        faskesName: "Puskesmas Tebet",
        diagnosis: "ISPA",
        claim_amount: 350000,
        amount: 350000,
        fraud_scores: {
                patient: 0,
                faskes: 0,
                ai: 5,
                total: 5
        },
        score: 5,
        red_flags: [
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 5,
                        message: "Risiko fraud rendah berdasarkan analisis AI"
                }
        ],
        redFlags: [
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 5,
                        message: "Risiko fraud rendah berdasarkan analisis AI"
                }
        ],
        decision: "ACCEPTED",
        status: "Diterima",
        decision_reason: "Auto accept (score: 5 < 10)",
        auto_reject: false,
        requires_review: false
},
{
        id: "CLM-2024-005",
        claim_id: "CLM-2024-005",
        timestamp: "2024-11-20T13:10:00+07:00",
        date: "20 Nov 2024",
        patient_name: "Ahmad Dhani",
        patientName: "Ahmad Dhani",
        faskes_name: "RS Pondok Indah",
        faskesName: "RS Pondok Indah",
        diagnosis: "Fraktur Femur",
        claim_amount: 15000000,
        amount: 15000000,
        fraud_scores: {
                patient: 10,
                faskes: 0,
                ai: 35,
                total: 45
        },
        score: 45,
        red_flags: [
                {
                        type: "low",
                        flag_name: "Alamat Duplikat",
                        score: 10,
                        message: "Alamat digunakan oleh 6 pasien berbeda"
                },
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 35,
                        message: "Risiko fraud sedang berdasarkan analisis AI"
                }
        ],
        redFlags: [
                {
                        type: "low",
                        flag_name: "Alamat Duplikat",
                        score: 10,
                        message: "Alamat digunakan oleh 6 pasien berbeda"
                },
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 35,
                        message: "Risiko fraud sedang berdasarkan analisis AI"
                }
        ],
        decision: "NEEDS_REVIEW",
        status: "Review",
        decision_reason: "Manual review required (score: 45 in range 10-60)",
        auto_reject: false,
        requires_review: true
},
{
        "id": "CLM-20251121-5069",
        "claim_id": "CLM-20251121-5069",
        "timestamp": "2025-11-21T00:11:26.958684",
        "date": "21 Nov 2025",
        "patient_name": "Umar Kusuma",
        "patientName": "Umar Kusuma",
        "faskes_name": "RSUD Tangerang",
        "faskesName": "RSUD Tangerang",
        "diagnosis": "Essential (primary) hypertension",
        "claim_amount": 2478506,
        "amount": 2478506,
        "fraud_scores": {
                patient: 0,
                faskes: 0,
                ai: 85,
                total: 85
        },
        score: 85,
        "red_flags": [
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 85,
                        message: "Risiko fraud tinggi berdasarkan analisis AI"
                }
        ],
        "redFlags": [
                {
                        type: "flex",
                        flag_name: "AI Fraud Detection",
                        score: 85,
                        message: "Risiko fraud tinggi berdasarkan analisis AI"
                }
        ],
        "decision": "REJECTED",
        "status": "Ditolak",
        "decision_reason": "Auto reject (score: 85 > 60)",
        "auto_reject": false,
        "requires_review": false
},
]

export const dashboardStats = {
        totalClaims: 1248,
        totalAmount: 4520000000,
        autoAccepted: 856,
        autoRejected: 142,
        needsReview: 250,
        fraudRate: "11.3%",
}

export const dailyVolumeData = [
        { name: "Sen", total: 120, accepted: 90, rejected: 10, review: 20 },
        { name: "Sel", total: 132, accepted: 100, rejected: 12, review: 20 },
        { name: "Rab", total: 101, accepted: 80, rejected: 5, review: 16 },
        { name: "Kam", total: 134, accepted: 100, rejected: 14, review: 20 },
        { name: "Jum", total: 90, accepted: 70, rejected: 8, review: 12 },
        { name: "Sab", total: 230, accepted: 180, rejected: 20, review: 30 },
        { name: "Min", total: 210, accepted: 160, rejected: 25, review: 25 },
]

export const fraudTypeData = [
        { name: "Phantom Billing", value: 400 },
        { name: "Upcoding", value: 300 },
        { name: "Unbundling", value: 300 },
        { name: "Kickback", value: 200 },
]
