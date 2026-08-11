"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { LineChart, Line, XAxis, YAxis, ReferenceLine } from "recharts";
import { fetchForecasts } from "@/lib/datara";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { formatNumber } from "@/lib/format";
import { cn } from "@/lib/utils";
import { aggregatePoints, scaleLabels, trendBadge, trendConfig, type ForecastScale } from "./chart-utils";

export default function ForecastingPage() {
  const { data, loading, error } = useApi(fetchForecasts);
  const forecasts = data ?? [];
  const [productId, setProductId] = React.useState<number | null>(null);
  const [scale, setScale] = React.useState<ForecastScale>("daily");

  const selected = forecasts.find((f) => f.product_id === productId) ?? forecasts[0] ?? null;

  const chartPoints = React.useMemo(
    () => (selected ? aggregatePoints(selected.points, scale) : []),
    [selected, scale]
  );

  return (
    <>
      <PageHeader
        title="Sales Forecasting"
        description="Prediksi penjualan berdasarkan riwayat transaksi — menjadi dasar perencanaan persediaan dan Smart Restock."
      />

      {loading ? (
        <Card>
          <CardContent className="space-y-6 py-6">
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-72 w-full" />
          </CardContent>
        </Card>
      ) : error ? (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : (
      <Card>
        <CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <CardTitle>Forecast per Produk</CardTitle>
            <CardDescription>Pilih produk untuk melihat estimasi penjualan periode berikutnya</CardDescription>
          </div>
          <Select value={String(selected?.product_id ?? "")} onValueChange={(v) => setProductId(Number(v))}>
            <SelectTrigger className="w-56">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {forecasts.map((f) => (
                <SelectItem key={f.product_id} value={String(f.product_id)}>
                  {f.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardHeader>
        <CardContent className="space-y-6">
          {selected ? (
            <>
              <div className="grid gap-4 sm:grid-cols-3">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Prediksi Periode</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-lg font-semibold">{new Date(selected.next_period).toLocaleDateString("id-ID", { day: "2-digit", month: "short", year: "numeric" })}</div>
                    <p className="text-xs text-muted-foreground">{selected.method}</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Estimasi Penjualan</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-semibold tabular-nums">{formatNumber(selected.predicted_units)} unit</div>
                    <p className="text-xs text-muted-foreground">periode berikutnya</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Kepercayaan</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-semibold tabular-nums">{selected.confidence}%</div>
                    <p className="text-xs text-muted-foreground">tingkat keyakinan model</p>
                  </CardContent>
                </Card>
              </div>

              <div>
                <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-medium">Prediksi vs Aktual</p>
                  <div className="flex items-center gap-1 rounded-md border bg-muted/40 p-1">
                    {(["daily", "weekly", "monthly"] as const).map((s) => (
                      <button
                        key={s}
                        type="button"
                        onClick={() => setScale(s)}
                        className={cn(
                          "rounded-sm px-2.5 py-1 text-xs font-medium transition-colors",
                          scale === s
                            ? "bg-background text-foreground shadow-sm"
                            : "text-muted-foreground hover:text-foreground"
                        )}
                      >
                        {scaleLabels[s]}
                      </button>
                    ))}
                  </div>
                </div>
                <ChartContainer config={trendConfig} className="aspect-auto h-72 w-full">
                  <LineChart data={chartPoints} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                    <XAxis
                      dataKey="period"
                      tickFormatter={(v: string) =>
                        new Date(v).toLocaleDateString(
                          "id-ID",
                          scale === "monthly"
                            ? { month: "short", year: "numeric" }
                            : { day: "2-digit", month: "short" }
                        )
                      }
                      tickLine={false}
                      axisLine={false}
                      tickMargin={8}
                    />
                    <YAxis tickLine={false} axisLine={false} tickMargin={8} />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Line type="monotone" dataKey="actual" stroke="var(--color-actual)" strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="forecast" stroke="var(--color-forecast)" strokeWidth={2} strokeDasharray="4 4" dot={false} />
                    <ReferenceLine x={chartPoints[chartPoints.length - 1]?.period} stroke="var(--border)" strokeDasharray="3 3" />
                  </LineChart>
                </ChartContainer>
                <p className="mt-2 text-center text-xs text-muted-foreground">
                  Garis padat = penjualan aktual · garis putus-putus = prediksi · skala {scaleLabels[scale]}
                </p>
              </div>

              <div className="rounded-md border bg-muted/40 p-3 text-sm">
                <span className="mr-2">
                  <Badge className={trendBadge[selected.trend].className}>
                    {trendBadge[selected.trend].label}
                  </Badge>
                </span>
                <p className="mt-2 text-muted-foreground">{selected.reasoning}</p>
              </div>
            </>
          ) : (
            <p className="py-10 text-center text-sm text-muted-foreground">Belum ada data forecasting.</p>
          )}
        </CardContent>
      </Card>
      )}
    </>
  );
}