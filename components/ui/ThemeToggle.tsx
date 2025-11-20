"use client"

import { Moon, Sun } from "lucide-react"
import { useTheme } from "@/components/providers/ThemeProvider"
import { cn } from "@/app/utils"

export function ThemeToggle() {
    const { theme, toggleTheme } = useTheme()

    return (
        <button
            onClick={toggleTheme}
            className={cn(
                "flex h-9 w-9 items-center justify-center rounded-lg border transition-colors",
                "border-slate-200 bg-white hover:bg-slate-100",
                "dark:border-slate-700 dark:bg-slate-800 dark:hover:bg-slate-700"
            )}
            aria-label="Toggle theme"
        >
            {theme === "light" ? (
                <Moon className="h-4 w-4 text-slate-600 dark:text-slate-400" />
            ) : (
                <Sun className="h-4 w-4 text-slate-600 dark:text-slate-400" />
            )}
        </button>
    )
}
