"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, FileText, Settings, ShieldCheck } from "lucide-react"
import { cn } from "@/app/utils"
import { ThemeToggle } from "@/components/ui/ThemeToggle"

const sidebarItems = [
    {
        title: "Dashboard",
        href: "/",
        icon: LayoutDashboard,
    },
    {
        title: "Data Klaim",
        href: "/claims",
        icon: FileText,
    },
    {
        title: "Fraud Detection",
        href: "/fraud-check",
        icon: ShieldCheck,
    },
    {
        title: "Pengaturan",
        href: "/settings",
        icon: Settings,
    },
]

export function Sidebar() {
    const pathname = usePathname()

    return (
        <div className="sticky top-0 flex h-screen w-64 flex-col border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
            <div className="flex h-16 items-center justify-between border-b border-slate-200 px-6 dark:border-slate-800">
                <div className="flex items-center gap-2 font-bold text-xl text-emerald-600">
                    <ShieldCheck className="h-6 w-6" />
                    <span>Smart Claim</span>
                </div>
                <ThemeToggle />
            </div>
            <div className="flex-1 overflow-y-auto py-4">
                <nav className="grid gap-1 px-2">
                    {sidebarItems.map((item, index) => {
                        const Icon = item.icon
                        const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href))

                        return (
                            <Link
                                key={index}
                                href={item.href}
                                className={cn(
                                    "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all hover:text-emerald-600",
                                    isActive
                                        ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-950/50 dark:text-emerald-400"
                                        : "text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800"
                                )}
                            >
                                <Icon className="h-4 w-4" />
                                {item.title}
                            </Link>
                        )
                    })}
                </nav>
            </div>
            <div className="border-t border-slate-200 p-4 dark:border-slate-800">
                <div className="flex items-center gap-3">
                    <div className="h-9 w-9 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 font-bold dark:bg-emerald-900 dark:text-emerald-400">
                        A
                    </div>
                    <div className="text-sm">
                        <p className="font-medium dark:text-slate-200">Admin BPJS</p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">admin@bpjs.go.id</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
