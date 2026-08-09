"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { LineChart, Line, XAxis, YAxis, ReferenceLine } from "recharts";
import { getProductForecasts } from "@/lib/demo-data";
import { formatNumber } from "@/lib/format";
import { trendBadge, trendConfig } from "./chart-utils";

export default function ForecastingPage() {
  const forecasts = React.useMemo(() => getProductForecasts(), []);
  const [productId, setProductId] = React.useState(forecasts[0]?.product_id ?? 0);

  const selected = forecasts.find((f) => f.product_id === productId) ?? forecasts[0];

  return (
    <>
      <PageHeader
        title="Sales Forecasting"
        description="Prediksi penjualan berdasarkan riwayat transaksi — menjadi dasar perencanaan persediaan dan Smart Restock."
      />

      <Card>
        <CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <CardTitle>Forecast per Produk</CardTitle>
            <CardDescription>Pilih produk untuk melihat estimasi penjualan periode berikutnya</CardDescription>
          </div>
          <Select value={String(productId)} onValueChange={(v) => setProductId(Number(v))}>
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
                <ChartContainer config={trendConfig} className="aspect-auto h-72 w-full">
                  <LineChart data={selected.points} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                    <XAxis dataKey="period" tickFormatter={(v: string) => new Date(v).toLocaleDateString("id-ID", { day: "2-digit", month: "short" })} tickLine={false} axisLine={false} tickMargin={8} />
                    <YAxis tickLine={false} axisLine={false} tickMargin={8} />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Line type="monotone" dataKey="actual" stroke="var(--color-actual)" strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="forecast" stroke="var(--color-forecast)" strokeWidth={2} strokeDasharray="4 4" dot={false} />
                    <ReferenceLine x={selected.points[selected.points.length - 1]?.period} stroke="var(--border)" strokeDasharray="3 3" />
                  </LineChart>
                </ChartContainer>
                <p className="mt-2 text-center text-xs text-muted-foreground">
                  Garis padat = penjualan aktual · garis putus-putus = prediksi
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
    </>
  );
}