"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { formatRupiah, formatDate, formatNumber } from "@/lib/format";
import { cn } from "@/lib/utils";
import { useApi } from "@/hooks/use-api";
import { fetchDecisions } from "@/lib/datara";
import type { DecisionRecord } from "@/lib/types";

type StatusDampak = "Membaik" | "Menurun" | "Stabil";

const statusMeta: Record<DecisionRecord["status"], { label: StatusDampak; className: string }> = {
  improved: { label: "Membaik", className: "bg-emerald-600 text-white" },
  regressed: { label: "Menurun", className: "bg-red-600 text-white" },
  flat: { label: "Stabil", className: "bg-slate-500 text-white" },
};

const tipeMeta: Record<DecisionRecord["type"], string> = {
  pricing: "Smart Pricing",
  restock: "Smart Restock",
};

function formatDelta(delta: number, format: (v: number) => string, unit = ""): string {
  if (delta === 0) return "0 (Stabil)";
  const label = delta > 0 ? "Naik" : "Turun";
  return `${delta > 0 ? "+" : "-"}${format(Math.abs(delta))} ${unit}(${label})`;
}

export default function DecisionsPage() {
  const { data: decisions, loading, error } = useApi(fetchDecisions);
  const [filterProduk, setFilterProduk] = React.useState("all");

  const daftarProduk = React.useMemo(
    () =>
      Array.from(
        new Set((decisions ?? []).map((d) => d.product_name).filter((n): n is string => Boolean(n))),
      ).sort((a, b) => a.localeCompare(b, "id")),
    [decisions],
  );

  const keputusanTampil =
    filterProduk === "all"
      ? (decisions ?? [])
      : (decisions ?? []).filter((d) => d.product_name === filterProduk);

  return (
    <>
      <PageHeader
        title="Keputusan & Monitoring"
        description="Rekap keputusan yang Anda terapkan beserta perkembangan indikator bisnis setelahnya (FR-009, FR-010)."
      />

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <Select value={filterProduk} onValueChange={setFilterProduk}>
          <SelectTrigger className="w-full sm:w-64">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Semua Produk</SelectItem>
            {daftarProduk.map((nama) => (
              <SelectItem key={nama} value={nama}>
                {nama}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {!loading && !error && (
          <p className="text-sm text-muted-foreground">
            {keputusanTampil.length} keputusan ditampilkan
          </p>
        )}
      </div>

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
            Belum ada keputusan yang diterapkan. Terapkan rekomendasi dari Smart Pricing / Smart
            Restock terlebih dahulu.
          </CardContent>
        </Card>
      ) : keputusanTampil.length === 0 ? (
        <Card>
          <CardContent className="py-10 text-center text-sm text-muted-foreground">
            Tidak ada riwayat keputusan untuk produk ini.
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-4">
          {keputusanTampil.map((d) => {
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
                      <Badge variant="secondary">
                        {tipeMeta[d.type]}
                      </Badge>
                      <CardTitle className="text-base">{d.title}</CardTitle>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {d.product_name ?? "—"} · Diterapkan {formatDate(d.applied_at)}
                    </p>
                  </div>
                  <Badge className={meta.className}>{meta.label}</Badge>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="rounded-lg border border-primary/15 bg-primary/5 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Alasan Keputusan
                    </p>
                    <p className="mt-1.5 text-sm leading-relaxed text-foreground/80">
                      {d.reasoning || d.summary}
                    </p>
                    {d.outcome_notes ? (
                      <p className="mt-2 border-t border-primary/10 pt-2 text-sm leading-relaxed text-muted-foreground">
                        {d.outcome_notes}
                      </p>
                    ) : null}
                  </div>

                  <div className="grid grid-cols-3 gap-3">
                    {(
                      [
                        {
                          label: "Omzet",
                          nilai: formatRupiah(d.metrics_after.revenue),
                          delta: formatDelta(deltas.revenue, (v) => formatRupiah(v)),
                          deltaClass: deltas.revenue >= 0 ? "text-emerald-600" : "text-red-600",
                        },
                        {
                          label: "Margin",
                          nilai: `${d.metrics_after.margin}%`,
                          delta: formatDelta(deltas.margin, (v) => `${v}%`),
                          deltaClass: deltas.margin >= 0 ? "text-emerald-600" : "text-red-600",
                        },
                        {
                          label: "Stok",
                          nilai: formatNumber(d.metrics_after.stock),
                          delta: formatDelta(deltas.stock, (v) => `${v} unit `),
                          deltaClass: deltas.stock >= 0 ? "text-emerald-600" : "text-red-600",
                        },
                      ] as const
                    ).map((m) => (
                      <div key={m.label} className="rounded-lg border bg-card p-3">
                        <p className="text-xs text-muted-foreground">{m.label}</p>
                        <p className="mt-0.5 text-lg font-bold tabular-nums">{m.nilai}</p>
                        <p className={cn("mt-0.5 text-xs font-medium", m.deltaClass)}>{m.delta}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </>
  );
}
