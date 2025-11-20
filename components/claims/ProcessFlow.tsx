"use client"

import { cn } from "@/app/utils"
import { CheckCircle, XCircle, AlertTriangle, ArrowRight, Activity, FileText, User, Building, Brain } from "lucide-react"

interface ProcessFlowProps {
    status: "Diterima" | "Ditolak" | "Review"
    score: number
}

export function ProcessFlow({ status, score }: ProcessFlowProps) {
    const getStepStatus = (step: string) => {
        // Logic to determine if a step is active/completed/error based on overall status and score
        // This is a simplified logic for the demo
        if (status === "Ditolak" && step === "reject") return "error"
        if (status === "Diterima" && step === "accept") return "success"
        if (status === "Review" && step === "review") return "warning"
        return "default"
    }

    return (
        <div className="relative p-8">
            {/* Main Flow Container */}
            <div className="flex flex-col gap-8">

                {/* Level 1: Input */}
                <div className="flex justify-center">
                    <div className="flex flex-col items-center gap-2">
                        <div className="flex h-16 w-48 items-center justify-center rounded-lg border-2 border-emerald-500 bg-emerald-50 font-bold text-emerald-700 dark:border-emerald-600 dark:bg-emerald-950/30 dark:text-emerald-400">
                            Pendaftaran Pasien
                        </div>
                        <ArrowRight className="rotate-90 text-slate-400 dark:text-slate-500" />
                    </div>
                </div>

                {/* Level 2: Medical Process */}
                <div className="grid grid-cols-3 gap-4">
                    <div className="rounded-lg border border-slate-200 bg-white p-4 text-center shadow-sm dark:border-slate-700 dark:bg-slate-800">
                        <div className="mb-2 flex justify-center"><User className="h-6 w-6 text-blue-500 dark:text-blue-400" /></div>
                        <div className="font-medium dark:text-slate-200">Anamnesis</div>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-white p-4 text-center shadow-sm dark:border-slate-700 dark:bg-slate-800">
                        <div className="mb-2 flex justify-center"><Activity className="h-6 w-6 text-blue-500 dark:text-blue-400" /></div>
                        <div className="font-medium dark:text-slate-200">Pemeriksaan Fisik</div>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-white p-4 text-center shadow-sm dark:border-slate-700 dark:bg-slate-800">
                        <div className="mb-2 flex justify-center"><FileText className="h-6 w-6 text-blue-500 dark:text-blue-400" /></div>
                        <div className="font-medium dark:text-slate-200">Penunjang</div>
                    </div>
                </div>

                {/* Level 3: Fraud Checks (The Core) */}
                <div className="relative rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 p-6 dark:border-slate-600 dark:bg-slate-800/50">
                    <div className="absolute -top-3 left-4 bg-slate-50 px-2 text-sm font-bold text-slate-500 dark:bg-slate-800 dark:text-slate-400">
                        AI Fraud Detection Engine
                    </div>

                    <div className="grid grid-cols-3 gap-8">
                        <div className="flex flex-col items-center gap-2">
                            <Building className="h-8 w-8 text-slate-400 dark:text-slate-500" />
                            <div className="text-center text-sm font-medium dark:text-slate-300">Check Fraud Faskes</div>
                            <div className="h-2 w-full rounded-full bg-emerald-200 dark:bg-emerald-900/30">
                                <div className="h-2 w-full rounded-full bg-emerald-500 dark:bg-emerald-600"></div>
                            </div>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                            <User className="h-8 w-8 text-slate-400 dark:text-slate-500" />
                            <div className="text-center text-sm font-medium dark:text-slate-300">Check Fraud Pasien</div>
                            <div className="h-2 w-full rounded-full bg-emerald-200 dark:bg-emerald-900/30">
                                <div className="h-2 w-full rounded-full bg-emerald-500 dark:bg-emerald-600"></div>
                            </div>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                            <Brain className="h-8 w-8 text-purple-500 dark:text-purple-400" />
                            <div className="text-center text-sm font-medium dark:text-slate-300">AI Diagnosis Match</div>
                            <div className={cn(
                                "h-2 w-full rounded-full",
                                score > 60 ? "bg-red-200 dark:bg-red-900/30" : score > 10 ? "bg-amber-200 dark:bg-amber-900/30" : "bg-emerald-200 dark:bg-emerald-900/30"
                            )}>
                                <div className={cn(
                                    "h-2 rounded-full",
                                    score > 60 ? "w-full bg-red-500 dark:bg-red-600" : score > 10 ? "w-3/4 bg-amber-500 dark:bg-amber-600" : "w-1/4 bg-emerald-500 dark:bg-emerald-600"
                                )}></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Level 4: Scoring & Decision */}
                <div className="flex justify-center">
                    <div className="flex flex-col items-center gap-4">
                        <ArrowRight className="rotate-90 text-slate-400 dark:text-slate-500" />
                        <div className="rounded-xl border-2 border-slate-800 bg-slate-900 p-6 text-white shadow-lg dark:border-slate-600 dark:bg-slate-800">
                            <div className="text-center">
                                <div className="text-sm text-slate-400">Score Red Flag</div>
                                <div className={cn(
                                    "text-4xl font-bold",
                                    score <= 10 ? "text-emerald-400" : score <= 60 ? "text-amber-400" : "text-red-400"
                                )}>
                                    {score}
                                </div>
                            </div>
                        </div>
                        <ArrowRight className="rotate-90 text-slate-400 dark:text-slate-500" />
                    </div>
                </div>

                {/* Level 5: Final Status */}
                <div className="grid grid-cols-3 gap-4">
                    <div className={cn(
                        "flex flex-col items-center rounded-lg border p-4 transition-all",
                        status === "Diterima" ? "border-emerald-500 bg-emerald-50 ring-2 ring-emerald-500 dark:border-emerald-600 dark:bg-emerald-950/30 dark:ring-emerald-600" : "border-slate-200 opacity-50 dark:border-slate-700"
                    )}>
                        <CheckCircle className={cn("mb-2 h-8 w-8", status === "Diterima" ? "text-emerald-600 dark:text-emerald-400" : "text-slate-400")} />
                        <div className={cn("font-bold", status === "Diterima" && "dark:text-slate-100")}>Terima Klaim</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Score ≤ 10</div>
                    </div>

                    <div className={cn(
                        "flex flex-col items-center rounded-lg border p-4 transition-all",
                        status === "Review" ? "border-amber-500 bg-amber-50 ring-2 ring-amber-500 dark:border-amber-600 dark:bg-amber-950/30 dark:ring-amber-600" : "border-slate-200 opacity-50 dark:border-slate-700"
                    )}>
                        <AlertTriangle className={cn("mb-2 h-8 w-8", status === "Review" ? "text-amber-600 dark:text-amber-400" : "text-slate-400")} />
                        <div className={cn("font-bold", status === "Review" && "dark:text-slate-100")}>Review Verifikator</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Score 10-60</div>
                    </div>

                    <div className={cn(
                        "flex flex-col items-center rounded-lg border p-4 transition-all",
                        status === "Ditolak" ? "border-red-500 bg-red-50 ring-2 ring-red-500 dark:border-red-600 dark:bg-red-950/30 dark:ring-red-600" : "border-slate-200 opacity-50 dark:border-slate-700"
                    )}>
                        <XCircle className={cn("mb-2 h-8 w-8", status === "Ditolak" ? "text-red-600 dark:text-red-400" : "text-slate-400")} />
                        <div className={cn("font-bold", status === "Ditolak" && "dark:text-slate-100")}>Tolak Klaim</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Score {'>'} 60</div>
                    </div>
                </div>

            </div>
        </div>
    )
}
