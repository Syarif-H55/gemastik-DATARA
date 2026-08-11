"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendDown, TrendUp, Minus } from "@phosphor-icons/react";
import { formatRupiah, formatDate } from "@/lib/format";
import { fetchDecisions } from "@/lib/datara";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { cn } from "@/lib/utils";

const statusMeta: Record<string, { label: string; className: string; icon: React.ReactNode }> = {
  improved: { label: "Membaik", className: "bg-emerald-600 text-white", icon: <TrendUp className="size-3" /> },
  restricted: { label: "Terbatas", className: "bg-slate-500 text-white", icon: <Minus className="size-3" /> },
  regressed: { label: "Menurun", className: "bg-red-600 text-white", icon: <TrendDown className="size-3" /> },
  flat: { label: "Stabil", className: "bg-slate-500 text-white", icon: <Minus className="size-3" /> },
};

export default function DecisionsPage() {
  const { data: decisions, loading, error } = useApi(fetchDecisions);

  return (
    <>
      <PageHeader
        title="Keputusan & Monitoring"
        description="Rekap rekomendasi yang Anda terapkan beserta perkembangan indikator bisnis setelahnya (FR-009, FR-010)."
      />

      {loading ? (
        <div className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-48 w-full" />
          ))}
        </div>
      ) : error ? (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : (decisions ?? []).length === 0 ? (
        <Card>
          <CardContent className="py-10 text-center text-sm text-muted-foreground">
            Belum ada keputusan yang diterapkan. Terapkan rekomendasi dari Smart Pricing / Smart Restock terlebih dahulu.
          </CardContent>
        </Card>
      ) : (
      <div className="space-y-4">
        {(decisions ?? []).map((d) => {
          const meta = statusMeta[d.status] ?? statusMeta.flat;
          const deltas = {
            revenue: d.metrics_after.revenue - d.metrics_before.revenue,
            margin: d.metrics_after.margin - d.metrics_before.margin,
            stock: d.metrics_after.stock - d.metrics_before.stock,
          };
          return (
            <Card key={d.id}>
              <CardHeader className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant={d.type === "pricing" ? "secondary" : "outline"}>
                      {d.type === "pricing" ? "Smart Pricing" : "Smart Restock"}
                    </Badge>
                    <CardTitle className="text-base">{d.title}</CardTitle>
                  </div>
                  <CardDescription>{d.summary}</CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted-foreground">Diterapkan {formatDate(d.applied_at)}</span>
                  <Badge className={meta.className}>{meta.label}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="rounded-md border bg-muted/40 p-3 text-sm">
                  <p className="font-medium">Alasan & Data Pendukung</p>
                  <p className="mt-1 text-muted-foreground">{d.reasoning}</p>
                </div>

                <div className="grid gap-3 sm:grid-cols-3">
                  {(
                    [
                      { key: "revenue", label: "Omzet", value: formatRupiah(d.metrics_after.revenue), before: d.metrics_before.revenue, delta: deltas.revenue },
                      { key: "margin", label: "Margin", value: `${d.metrics_after.margin}%`, before: d.metrics_before.margin, delta: deltas.margin },
                      { key: "stock", label: "Stok", value: `${d.metrics_after.stock}`, before: d.metrics_before.stock, delta: deltas.stock },
                    ] as const
                  ).map((m) => (
                    <div key={m.key} className="rounded-md border p-3">
                      <p className="text-xs text-muted-foreground">{m.label}</p>
                      <p className="text-lg font-semibold tabular-nums">{m.value}</p>
                      <p className={cn("text-xs", m.delta >= 0 ? "text-emerald-600" : "text-red-600")}>
                        {m.delta >= 0 ? "+" : ""}
                        {m.delta.toLocaleString("id-ID")} dibanding sebelum keputusan
                      </p>
                    </div>
                  ))}
                </div>

                <p className="text-sm text-muted-foreground">{d.outcome_notes}</p>
              </CardContent>
            </Card>
          );
        })}
      </div>
      )}
    </>
  );
}