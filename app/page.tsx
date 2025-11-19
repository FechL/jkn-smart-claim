"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { dashboardStats, dailyVolumeData, fraudTypeData, mockClaims } from "@/app/data/mockData"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts"
import { Activity, AlertTriangle, CheckCircle, Clock, FileText, TrendingUp, Users } from "lucide-react"

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">Dashboard Overview</h2>
        <p className="text-slate-500 dark:text-slate-400">Selamat datang kembali, Admin BPJS.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Klaim</CardTitle>
            <FileText className="h-4 w-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.totalClaims}</div>
            <p className="text-xs text-slate-500">+20.1% dari bulan lalu</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Auto-Accepted</CardTitle>
            <CheckCircle className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.autoAccepted}</div>
            <p className="text-xs text-slate-500">68.5% tingkat penerimaan</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Butuh Review</CardTitle>
            <Clock className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.needsReview}</div>
            <p className="text-xs text-slate-500">20% dari total klaim</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Potensi Fraud</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.autoRejected}</div>
            <p className="text-xs text-slate-500">{dashboardStats.fraudRate} tingkat deteksi</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Volume Klaim Harian</CardTitle>
            <CardDescription>Tren klaim masuk selama 7 hari terakhir</CardDescription>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={dailyVolumeData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}`} />
                  <Tooltip
                    cursor={{ fill: 'transparent' }}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Bar dataKey="accepted" name="Diterima" stackId="a" fill="#10b981" radius={[0, 0, 4, 4]} />
                  <Bar dataKey="review" name="Review" stackId="a" fill="#f59e0b" radius={[0, 0, 0, 0]} />
                  <Bar dataKey="rejected" name="Ditolak" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Distribusi Tipe Fraud</CardTitle>
            <CardDescription>Kategori fraud yang terdeteksi sistem AI</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={fraudTypeData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    fill="#8884d8"
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {fraudTypeData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend verticalAlign="bottom" height={36} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Aktivitas Terbaru</CardTitle>
          <CardDescription>Klaim yang baru saja diproses oleh sistem</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-8">
            {mockClaims.map((claim) => (
              <div key={claim.id} className="flex items-center">
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">{claim.patientName}</p>
                  <p className="text-sm text-slate-500">{claim.faskesName} • {claim.diagnosis}</p>
                </div>
                <div className="ml-auto font-medium">
                  {new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(claim.amount)}
                </div>
                <div className="ml-4">
                  <Badge variant={
                    claim.status === "Diterima" ? "success" :
                      claim.status === "Ditolak" ? "destructive" : "warning"
                  }>
                    {claim.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
