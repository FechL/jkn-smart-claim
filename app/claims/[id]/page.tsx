"use client"

import { useParams } from "next/navigation"
import Link from "next/link"
import { useState, useEffect } from "react"
import { ArrowLeft, Calendar, CreditCard, FileText, User, AlertTriangle, Building as BuildingIcon, CheckCircle, XCircle } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { ProcessFlow } from "@/components/claims/ProcessFlow"
import { mockClaims } from "@/app/data/mockData"
import { cn } from "@/app/utils"

export default function ClaimDetailPage() {
    const params = useParams()
    const id = params.id as string
    const claim = mockClaims.find(c => c.id === id)
    const [claimStatus, setClaimStatus] = useState<"Diterima" | "Ditolak" | "Review" | "Review Diterima" | "Review Ditolak" | undefined>(claim?.status)

    // Load verification status from localStorage on mount
    useEffect(() => {
        if (claim) {
            const savedStatus = localStorage.getItem(`claim-status-${claim.id}`)
            if (savedStatus) {
                setClaimStatus(savedStatus as typeof claimStatus)
            }
        }
    }, [claim])

    if (!claim) {
        return <div className="p-8">Klaim tidak ditemukan</div>
    }

    const handleAccept = async () => {
        const newStatus = "Review Diterima"
        setClaimStatus(newStatus)
        localStorage.setItem(`claim-status-${claim.id}`, newStatus)
        console.log("Claim accepted:", claim.id)
    }

    const handleReject = async () => {
        const newStatus = "Review Ditolak"
        setClaimStatus(newStatus)
        localStorage.setItem(`claim-status-${claim.id}`, newStatus)
        console.log("Claim rejected:", claim.id)
    }

    const displayStatus = claimStatus || claim.status

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
                        displayStatus === "Diterima" || displayStatus === "Review Diterima" ? "success" :
                            displayStatus === "Ditolak" || displayStatus === "Review Ditolak" ? "destructive" : "warning"
                    }>
                        {displayStatus}
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
                                    <User className="h-5 w-5 text-slate-500 dark:text-slate-400" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Nama Pasien</p>
                                    <p className="font-semibold dark:text-slate-100">{claim.patientName}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <BuildingIcon className="h-5 w-5 text-slate-500 dark:text-slate-400" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Faskes</p>
                                    <p className="font-semibold dark:text-slate-100">{claim.faskesName}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <FileText className="h-5 w-5 text-slate-500 dark:text-slate-400" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Diagnosis</p>
                                    <p className="font-semibold dark:text-slate-100">{claim.diagnosis}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <Calendar className="h-5 w-5 text-slate-500 dark:text-slate-400" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Tanggal Masuk</p>
                                    <p className="font-semibold dark:text-slate-100">{claim.date}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
                                    <CreditCard className="h-5 w-5 text-slate-500 dark:text-slate-400" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Total Tagihan</p>
                                    <p className="font-semibold text-emerald-600 dark:text-emerald-400">
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
                                <ul className="space-y-3">
                                    {claim.redFlags.map((flag, i) => (
                                        <li key={i} className="flex items-start gap-2">
                                            <Badge variant={
                                                flag.type === "crucial" ? "destructive" :
                                                    flag.type === "medium" ? "warning" : "secondary"
                                            } className="mt-0.5">
                                                {flag.type}
                                            </Badge>
                                            <div className="flex-1">
                                                <div className="flex items-center justify-between">
                                                    <p className="text-sm font-medium text-red-700 dark:text-red-400">{flag.flag_name}</p>
                                                    <span className={cn(
                                                        "text-sm font-bold",
                                                        typeof flag.score === 'number' && flag.score <= 10 ? "text-emerald-600 dark:text-emerald-400" :
                                                            typeof flag.score === 'number' && flag.score <= 30 ? "text-amber-600 dark:text-amber-400" :
                                                                "text-red-600 dark:text-red-400"
                                                    )}>
                                                        +{flag.score}
                                                    </span>
                                                </div>
                                                <p className="text-xs text-red-600 dark:text-red-500">{flag.message}</p>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    )}

                    {/* Decision Buttons for Review Status - In Left Column */}
                    {!claimStatus?.startsWith("Review ") && claim.status === "Review" && (
                        <Card className="border-amber-200 bg-amber-50 dark:border-amber-900 dark:bg-amber-950/20">
                            <CardHeader>
                                <CardTitle className="text-amber-700 dark:text-amber-400">Keputusan Verifikator</CardTitle>
                                <CardDescription className="dark:text-amber-600">
                                    Klaim ini memerlukan review manual.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="flex flex-col gap-3">
                                    <button
                                        onClick={handleAccept}
                                        className="flex items-center justify-center gap-2 rounded-lg bg-emerald-600 px-4 py-3 font-semibold text-white transition-colors hover:bg-emerald-700 dark:bg-emerald-700 dark:hover:bg-emerald-600">
                                        <CheckCircle className="h-5 w-5" />
                                        Terima Klaim
                                    </button>
                                    <button
                                        onClick={handleReject}
                                        className="flex items-center justify-center gap-2 rounded-lg bg-red-600 px-4 py-3 font-semibold text-white transition-colors hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-600">
                                        <XCircle className="h-5 w-5" />
                                        Tolak Klaim
                                    </button>
                                </div>
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
                            <ProcessFlow status={displayStatus} score={claim.score} />
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
