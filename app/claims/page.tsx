"use client"

import { useState } from "react"
import Link from "next/link"
import { cn } from "@/app/utils"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/Table"
import { mockClaims } from "@/app/data/mockData"
import { Search, Filter } from "lucide-react"

export default function ClaimsPage() {
    const [searchTerm, setSearchTerm] = useState("")
    const [statusFilter, setStatusFilter] = useState<string>("All")

    const filteredClaims = mockClaims.filter(claim => {
        const matchesSearch =
            claim.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
            claim.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            claim.faskesName.toLowerCase().includes(searchTerm.toLowerCase())

        const matchesStatus = statusFilter === "All" || claim.status === statusFilter

        return matchesSearch && matchesStatus
    })

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">Data Klaim</h2>
                <p className="text-slate-500 dark:text-slate-400">Kelola dan monitor status klaim BPJS.</p>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>Daftar Klaim Masuk</CardTitle>
                            <CardDescription>Total {filteredClaims.length} klaim ditemukan</CardDescription>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="relative">
                                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-500" />
                                <input
                                    type="text"
                                    placeholder="Cari pasien, ID, atau faskes..."
                                    className="h-9 w-[250px] rounded-md border border-slate-200 bg-white pl-9 pr-4 text-sm outline-none focus:border-emerald-500 dark:border-slate-800 dark:bg-slate-950"
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                />
                            </div>
                            <select
                                className="h-9 rounded-md border border-slate-200 bg-white px-3 text-sm outline-none focus:border-emerald-500 dark:border-slate-800 dark:bg-slate-950"
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                            >
                                <option value="All">Semua Status</option>
                                <option value="Diterima">Diterima</option>
                                <option value="Ditolak">Ditolak</option>
                                <option value="Review">Review</option>
                            </select>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>ID Klaim</TableHead>
                                <TableHead>Pasien</TableHead>
                                <TableHead>Faskes</TableHead>
                                <TableHead>Diagnosis</TableHead>
                                <TableHead>Tanggal</TableHead>
                                <TableHead>Total Biaya</TableHead>
                                <TableHead>Score</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Aksi</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredClaims.map((claim) => (
                                <TableRow key={claim.id}>
                                    <TableCell className="font-medium">{claim.id}</TableCell>
                                    <TableCell>{claim.patientName}</TableCell>
                                    <TableCell>{claim.faskesName}</TableCell>
                                    <TableCell>{claim.diagnosis}</TableCell>
                                    <TableCell>{claim.date}</TableCell>
                                    <TableCell>{new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(claim.amount)}</TableCell>
                                    <TableCell>
                                        <span className={cn(
                                            "font-bold",
                                            claim.score <= 10 ? "text-emerald-600 dark:text-emerald-400" :
                                                claim.score <= 60 ? "text-amber-600 dark:text-amber-400" : "text-red-600 dark:text-red-400"
                                        )}>
                                            {claim.score}
                                        </span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={
                                            claim.status === "Diterima" ? "success" :
                                                claim.status === "Ditolak" ? "destructive" : "warning"
                                        }>
                                            {claim.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Link
                                            href={`/claims/${claim.id}`}
                                            className="text-sm font-medium text-emerald-600 hover:underline"
                                        >
                                            Detail
                                        </Link>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    )
}
