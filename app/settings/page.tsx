import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"

export default function SettingsPage() {
    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">Pengaturan</h2>
                <p className="text-slate-500 dark:text-slate-400">Konfigurasi sistem Smart Claim.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Profil Pengguna</CardTitle>
                    <CardDescription>Kelola informasi akun anda</CardDescription>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-slate-500">Fitur pengaturan akan segera hadir.</p>
                </CardContent>
            </Card>
        </div>
    )
}
