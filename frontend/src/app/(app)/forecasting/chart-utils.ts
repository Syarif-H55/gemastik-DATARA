import type { ChartConfig } from "@/components/ui/chart";
import type { ForecastPoint } from "@/lib/types";

export const trendConfig: ChartConfig = {
  actual: { label: "Aktual", color: "var(--chart-1)" },
  forecast: { label: "Forecast", color: "var(--chart-2)" },
};

export type ForecastScale = "daily" | "weekly" | "monthly";

export const scaleLabels: Record<ForecastScale, string> = {
  daily: "Harian",
  weekly: "Mingguan",
  monthly: "Bulanan",
};

function parsePeriod(period: string): Date {
  const [y, m, d] = period.slice(0, 10).split("-").map(Number);
  return new Date(y, m - 1, d);
}

function toISODate(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function bucketKey(date: Date, scale: ForecastScale): string {
  if (scale === "monthly") {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-01`;
  }
  if (scale === "weekly") {
    const monday = new Date(date);
    monday.setDate(date.getDate() - ((date.getDay() + 6) % 7));
    return toISODate(monday);
  }
  return toISODate(date);
}

export function aggregatePoints(points: ForecastPoint[], scale: ForecastScale): ForecastPoint[] {
  if (scale === "daily" || points.length === 0) return points;
  const buckets = new Map<string, ForecastPoint>();
  for (const p of points) {
    const period = bucketKey(parsePeriod(p.period), scale);
    const agg = buckets.get(period) ?? { period, actual: 0, forecast: 0, lower: 0, upper: 0 };
    agg.actual += p.actual ?? 0;
    agg.forecast += p.forecast ?? 0;
    agg.lower = (agg.lower ?? 0) + (p.lower ?? 0);
    agg.upper = (agg.upper ?? 0) + (p.upper ?? 0);
    buckets.set(period, agg);
  }
  return [...buckets.values()].sort((a, b) => a.period.localeCompare(b.period));
}

export const trendBadge: Record<"up" | "down" | "flat", { label: string; className: string }> = {
  up: { label: "Tren Naik", className: "bg-emerald-600 text-white" },
  down: { label: "Tren Menurun", className: "bg-red-600 text-white" },
  flat: { label: "Stabil", className: "bg-slate-500 text-white" },
};