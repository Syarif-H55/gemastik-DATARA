"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { ChartContainer, ChartLegend, ChartLegendContent, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import { TrendUp, Wallet, Receipt, ChartPieSlice } from "@/components/datara-icons";
import { formatRupiah, formatPercent } from "@/lib/format";
import { fetchDashboard } from "@/lib/datara";
import { useApi } from "@/hooks/use-api";
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

const trendConfig: ChartConfig = {
  revenue: { label: "Omzet", color: "var(--chart-1)" },
  profit: { label: "Laba", color: "var(--chart-2)" },
};

const categoryConfig: ChartConfig = {
  value: { label: "Omzet", color: "var(--chart-3)" },
};

export default function DashboardPage() {
  const { data, loading, error } = useApi(fetchDashboard);

  const periodLabel = new Intl.DateTimeFormat("id-ID", { month: "long", year: "numeric" }).format(new Date());

  if (loading) {
    return (
      <>
        <PageHeader title="Business Dashboard" description="Ringkasan kesehatan bisnis dari data penjualan, HPP, dan biaya operasional." />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      </>
    );
  }

  if (error || !data) {
    return (
      <>
        <PageHeader title="Business Dashboard" description="Ringkasan kesehatan bisnis dari data penjualan, HPP, dan biaya operasional." />
        <Alert variant="destructive">
          <AlertDescription>{error ?? "Data tidak tersedia."}</AlertDescription>
        </Alert>
      </>
    );
  }

  const metrics = [
    { label: "Omzet", value: formatRupiah(data.total_revenue), icon: TrendUp, hint: "Total penjualan 30 hari terakhir" },
    { label: "Laba", value: formatRupiah(data.total_profit), icon: TrendUp, hint: "Pendapatan dikurangi HPP & biaya" },
    { label: "HPP", value: formatRupiah(data.total_cogs), icon: Wallet, hint: "Harga pokok penjualan" },
    { label: "Margin Rata-rata", value: formatPercent(data.avg_margin_percent), icon: ChartPieSlice, hint: "Margin kotor rata-rata" },
  ];

  const activity = [
    { label: "Transaksi", value: data.transactions_count, icon: Receipt, hint: "Jumlah transaksi 30 hari terakhir" },
    { label: "Produk terjual", value: data.products_sold, icon: TrendUp, hint: "Total item terjual" },
  ];

  return (
    <>
      <PageHeader
        title="Business Dashboard"
        description="Ringkasan kesehatan bisnis dari data penjualan, HPP, dan biaya operasional."
        actions={
          <div className="flex items-center gap-2">
            <Badge variant="secondary">Periode: {periodLabel}</Badge>
            <Badge className="bg-emerald-600 text-white">{data.business_health.label}</Badge>
          </div>
        }
      />

      <Card className="mb-4 border-primary/30 bg-primary/5">
        <CardContent className="flex items-center justify-between gap-4 py-4">
          <div className="space-y-1">
            <CardTitle className="text-base">Business Health Score</CardTitle>
            <p className="text-xs text-muted-foreground">
              Komposit dari margin, aktivitas penjualan, dan keterjualan produk.
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-3xl font-semibold tabular-nums">{data.business_health.score}</p>
              <p className="text-xs text-muted-foreground">dari 100</p>
            </div>
            <div className="w-40">
              <Progress value={data.business_health.score} className="h-3" />
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((m) => (
          <Card key={m.label}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{m.label}</CardTitle>
              <m.icon className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-semibold tabular-nums">{m.value}</div>
              <p className="text-xs text-muted-foreground">{m.hint}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        {activity.map((m) => (
          <Card key={m.label}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{m.label}</CardTitle>
              <m.icon className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-semibold tabular-nums">{m.value}</div>
              <p className="text-xs text-muted-foreground">{m.hint}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-4 grid gap-4 lg:grid-cols-5">
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>Tren Pendapatan</CardTitle>
            <CardDescription>Omzet dan laba per hari (7 hari terakhir)</CardDescription>
          </CardHeader>
          <CardContent>
            <ChartContainer config={trendConfig} className="aspect-auto h-64 w-full">
              <AreaChart data={data.revenue_trend} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="fillRevenue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--color-revenue)" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="var(--color-revenue)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="date" tickFormatter={(v: string) => new Date(v).toLocaleDateString("id-ID", { day: "2-digit", month: "short" })} tickLine={false} axisLine={false} tickMargin={8} />
                <YAxis tickLine={false} axisLine={false} tickMargin={8} tickFormatter={(v: number) => `Rp ${(v / 1000).toFixed(0)}k`} />
                <ChartTooltip content={<ChartTooltipContent labelFormatter={(v) => `Tanggal: ${v}`} formatter={(value) => formatRupiah(Number(value))} />} />
                <Area type="monotone" dataKey="revenue" stroke="var(--color-revenue)" fill="url(#fillRevenue)" name="omzet" />
                <Area type="monotone" dataKey="profit" stroke="var(--color-profit)" fill="var(--color-profit)" fillOpacity={0.15} name="laba" />
              </AreaChart>
            </ChartContainer>
            <ChartLegend content={<ChartLegendContent nameKey="revenue" />} />
            <ChartLegend content={<ChartLegendContent nameKey="profit" />} />
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Kontribusi Kategori</CardTitle>
            <CardDescription>Omzet per kategori produk</CardDescription>
          </CardHeader>
          <CardContent>
            <ChartContainer config={categoryConfig} className="aspect-auto h-56 w-full">
              <BarChart data={data.category_breakdown} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tickLine={false} axisLine={false} tickMargin={8} />
                <YAxis tickLine={false} axisLine={false} tickMargin={8} tickFormatter={(v: number) => `Rp ${(v / 1000).toFixed(0)}k`} />
                <ChartTooltip content={<ChartTooltipContent formatter={(value) => formatRupiah(Number(value))} />} />
                <Bar dataKey="value" fill="var(--color-value)" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ChartContainer>
            <ChartLegend content={<ChartLegendContent nameKey="value" />} />
          </CardContent>
        </Card>
      </div>
    </>
  );
}
