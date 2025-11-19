"use client"

import Link from "next/link"
import { cn } from "@/app/utils"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/Table"
import { mockClaims, fraudTypeData } from "@/app/data/mockData"
import { AlertTriangle, ShieldAlert, TrendingUp } from "lucide-react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts"

export default function FraudCheckPage() {
    const fraudClaims = mockClaims.filter(c => c.score < 90)

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">Fraud Detection Center</h2>
                <p className="text-slate-500 dark:text-slate-400">Monitor dan analisis potensi kecurangan klaim.</p>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
                <Card className="bg-red-50 border-red-200 dark:bg-red-950/20 dark:border-red-900">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-red-700 dark:text-red-400">High Risk Claims</CardTitle>
                        <ShieldAlert className="h-4 w-4 text-red-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-red-700 dark:text-red-400">
                            {fraudClaims.filter(c => c.score < 40).length}
                        </div>
                        <p className="text-xs text-red-600/80">Perlu tindakan segera</p>
                    </CardContent>
                </Card>
                <Card className="bg-amber-50 border-amber-200 dark:bg-amber-950/20 dark:border-amber-900">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-amber-700 dark:text-amber-400">Medium Risk (Review)</CardTitle>
                        <AlertTriangle className="h-4 w-4 text-amber-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-amber-700 dark:text-amber-400">
                            {fraudClaims.filter(c => c.score >= 40 && c.score < 90).length}
                        </div>
                        <p className="text-xs text-amber-600/80">Dalam antrian verifikator</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Potensi Kerugian</CardTitle>
                        <TrendingUp className="h-4 w-4 text-slate-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumSignificantDigits: 3 }).format(
                                fraudClaims.reduce((acc, curr) => acc + curr.amount, 0)
                            )}
                        </div>
                        <p className="text-xs text-slate-500">Dari klaim terindikasi fraud</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-8 lg:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Analisis Tipe Fraud</CardTitle>
                        <CardDescription>Distribusi kategori fraud yang terdeteksi</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[300px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={fraudTypeData} layout="vertical">
                                    <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                                    <XAxis type="number" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                                    <YAxis dataKey="name" type="category" width={100} stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                                    <Tooltip
                                        cursor={{ fill: 'transparent' }}
                                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                    />
                                    <Bar dataKey="value" fill="#ef4444" radius={[0, 4, 4, 0]}>
                                        {fraudTypeData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={['#ef4444', '#f97316', '#f59e0b', '#8b5cf6'][index % 4]} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Daftar Klaim Terindikasi</CardTitle>
                        <CardDescription>Klaim dengan skor confidence rendah</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>ID</TableHead>
                                    <TableHead>Faskes</TableHead>
                                    <TableHead>Score</TableHead>
                                    <TableHead>Red Flags</TableHead>
                                    <TableHead></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {fraudClaims.map((claim) => (
                                    <TableRow key={claim.id}>
                                        <TableCell className="font-medium">{claim.id}</TableCell>
                                        <TableCell>{claim.faskesName}</TableCell>
                                        <TableCell>
                                            <span className={cn(
                                                "font-bold",
                                                claim.score < 40 ? "text-red-600" : "text-amber-600"
                                            )}>
                                                {claim.score}
                                            </span>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex flex-wrap gap-1">
                                                {claim.redFlags.slice(0, 2).map((flag, i) => (
                                                    <Badge key={i} variant="outline" className="text-[10px] border-red-200 text-red-700 bg-red-50">
                                                        {flag}
                                                    </Badge>
                                                ))}
                                                {claim.redFlags.length > 2 && (
                                                    <Badge variant="outline" className="text-[10px]">+{claim.redFlags.length - 2}</Badge>
                                                )}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Link
                                                href={`/claims/${claim.id}`}
                                                className="text-sm font-medium text-emerald-600 hover:underline"
                                            >
                                                Review
                                            </Link>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
