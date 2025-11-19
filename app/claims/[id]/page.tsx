"use client"

import { useParams } from "next/navigation"
import Link from "next/link"
import { ArrowLeft, Calendar, CreditCard, FileText, User, AlertTriangle, Building as BuildingIcon } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { ProcessFlow } from "@/components/claims/ProcessFlow"
import { mockClaims } from "@/app/data/mockData"

export default function ClaimDetailPage() {
    const params = useParams()
    const id = params.id as string
    const claim = mockClaims.find(c => c.id === id)

    if (!claim) {
        return <div className="p-8">Klaim tidak ditemukan</div>
    }

    return (
        <div className="space-y-8">
            <div className="flex items-center gap-4">
                <Link href="/claims" className="rounded-full bg-slate-100 p-2 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700">
                    <ArrowLeft className="h-5 w-5" />
                </Link>
                <div>
                    <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">Detail Klaim {claim.id}</h2>
                    <p className="text-slate-500 dark:text-slate-400">Lihat detail proses dan status klaim.</p>
                </div>
                <div className="ml-auto">
                    <Badge className="text-lg px-4 py-1" variant={
                        claim.status === "Diterima" ? "success" :
                            claim.status === "Ditolak" ? "destructive" : "warning"
                    }>
                        {claim.status}
                    </Badge>
                </div>
            </div>

            <div className="grid gap-8 lg:grid-cols-3">
                {/* Left Column: Patient Info */}
                <div className="space-y-6 lg:col-span-1">
                    <Card>
                        <CardHeader>
                            <CardTitle>Informasi Pasien</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <User className="h-5 w-5 text-slate-500" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500">Nama Pasien</p>
                                    <p className="font-semibold">{claim.patientName}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <BuildingIcon className="h-5 w-5 text-slate-500" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500">Faskes</p>
                                    <p className="font-semibold">{claim.faskesName}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <FileText className="h-5 w-5 text-slate-500" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500">Diagnosis</p>
                                    <p className="font-semibold">{claim.diagnosis}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <Calendar className="h-5 w-5 text-slate-500" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500">Tanggal Masuk</p>
                                    <p className="font-semibold">{claim.date}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <CreditCard className="h-5 w-5 text-slate-500" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500">Total Tagihan</p>
                                    <p className="font-semibold text-emerald-600">
                                        {new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(claim.amount)}
                                    </p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {claim.redFlags.length > 0 && (
                        <Card className="border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/20">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2 text-red-700 dark:text-red-400">
                                    <AlertTriangle className="h-5 w-5" />
                                    Red Flags Terdeteksi
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <ul className="list-disc pl-5 text-sm text-red-700 dark:text-red-400">
                                    {claim.redFlags.map((flag, i) => (
                                        <li key={i}>{flag}</li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    )}
                </div>

                {/* Right Column: Process Flow */}
                <div className="lg:col-span-2">
                    <Card className="h-full">
                        <CardHeader>
                            <CardTitle>Alur Proses Klaim</CardTitle>
                            <CardDescription>Visualisasi perjalanan klaim melalui sistem Smart Claim</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <ProcessFlow status={claim.status} score={claim.score} />
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
