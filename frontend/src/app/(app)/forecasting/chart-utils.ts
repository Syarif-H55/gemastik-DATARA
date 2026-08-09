import type { ChartConfig } from "@/components/ui/chart";

export const trendConfig: ChartConfig = {
  actual: { label: "Aktual", color: "var(--chart-1)" },
  forecast: { label: "Forecast", color: "var(--chart-2)" },
};

export const trendBadge: Record<"up" | "down" | "flat", { label: string; className: string }> = {
  up: { label: "Tren Naik", className: "bg-emerald-600 text-white" },
  down: { label: "Tren Menurun", className: "bg-red-600 text-white" },
  flat: { label: "Stabil", className: "bg-slate-500 text-white" },
};