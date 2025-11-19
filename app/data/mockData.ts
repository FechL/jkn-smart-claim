
export interface Claim {
    id: string
    patientName: string
    faskesName: string
    diagnosis: string
    date: string
    amount: number
    status: "Diterima" | "Ditolak" | "Review"
    score: number
    redFlags: string[]
}

export const mockClaims: Claim[] = [
    {
        id: "CLM-2024-001",
        patientName: "Budi Santoso",
        faskesName: "RSUD Cengkareng",
        diagnosis: "Demam Berdarah Dengue",
        date: "2024-05-20",
        amount: 4500000,
        status: "Diterima",
        score: 95,
        redFlags: [],
    },
    {
        id: "CLM-2024-002",
        patientName: "Siti Aminah",
        faskesName: "Klinik Sehat Jaya",
        diagnosis: "Hipertensi",
        date: "2024-05-20",
        amount: 1200000,
        status: "Review",
        score: 65,
        redFlags: ["Frekuensi kunjungan tinggi"],
    },
    {
        id: "CLM-2024-003",
        patientName: "Joko Widodo",
        faskesName: "RS Harapan Kita",
        diagnosis: "Diabetes Mellitus",
        date: "2024-05-19",
        amount: 8500000,
        status: "Ditolak",
        score: 25,
        redFlags: ["Diagnosis tidak sesuai prosedur", "Tagihan ganda"],
    },
    {
        id: "CLM-2024-004",
        patientName: "Rina Wati",
        faskesName: "Puskesmas Tebet",
        diagnosis: "ISPA",
        date: "2024-05-19",
        amount: 350000,
        status: "Diterima",
        score: 92,
        redFlags: [],
    },
    {
        id: "CLM-2024-005",
        patientName: "Ahmad Dhani",
        faskesName: "RS Pondok Indah",
        diagnosis: "Fraktur Femur",
        date: "2024-05-18",
        amount: 15000000,
        status: "Review",
        score: 55,
        redFlags: ["Biaya obat tidak wajar"],
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
