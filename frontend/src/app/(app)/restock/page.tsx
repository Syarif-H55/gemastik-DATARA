"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { WarningCircle, Package } from "@phosphor-icons/react";
import { formatNumber } from "@/lib/format";
import { fetchRestockRecommendations, fetchForecasts, applyRestockRecommendation } from "@/lib/datara";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const urgencyMap: Record<string, { label: string; className: string }> = {
  critical: { label: "Kritis", className: "bg-red-600 text-white" },
  low: { label: "Perlu Restock", className: "bg-amber-500 text-white" },
  healthy: { label: "Aman", className: "bg-emerald-600 text-white" },
};

export default function RestockPage() {
  const { data: recs, loading, error } = useApi(fetchRestockRecommendations);
  const { data: forecastData } = useApi(fetchForecasts);
  const [filter, setFilter] = React.useState<string>("all");
  const [applyingId, setApplyingId] = React.useState<number | null>(null);

  const recommendations = recs ?? [];
  const forecasts = React.useMemo(() => new Map((forecastData ?? []).map((f) => [f.product_id, f])), [forecastData]);

  const filtered = filter === "all" ? recommendations : recommendations.filter((r) => r.urgency === filter);
  const criticalCount = recommendations.filter((r) => r.urgency === "critical").length;

  const applyRestock = async (r: (typeof recommendations)[number]) => {
    setApplyingId(r.id);
    try {
      await applyRestockRecommendation(r.id);
      toast.success(`Restock ${r.name} sebanyak ${r.suggested_quantity} unit dilakukan`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Gagal melakukan restock.");
    } finally {
      setApplyingId(null);
    }
  };

  return (
    <>
      <PageHeader
        title="Smart Restock"
        description="Rekomendasi waktu dan jumlah restock berdasarkan kondisi stok, riwayat penjualan, dan hasil Sales Forecasting."
        actions={
          criticalCount > 0 ? (
            <Badge className="bg-red-600 text-white">
              <WarningCircle className="size-3" /> {criticalCount} produk kritis
            </Badge>
          ) : undefined
        }
      />

      {loading ? (
        <Card>
          <CardContent className="space-y-3 py-6">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-12 w-full" />
            ))}
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
            <CardTitle>Rekomendasi Restock</CardTitle>
            <CardDescription>Berdasarkan stok saat ini, ambang minimum, dan estimasi penjualan harian.</CardDescription>
          </div>
          <Select value={filter} onValueChange={setFilter}>
            <SelectTrigger className="w-44">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Semua Prioritas</SelectItem>
              <SelectItem value="critical">Kritis</SelectItem>
              <SelectItem value="low">Perlu Restock</SelectItem>
              <SelectItem value="healthy">Aman</SelectItem>
            </SelectContent>
          </Select>
        </CardHeader>
        <CardContent>
          <div className="hidden md:block">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Produk</TableHead>
                  <TableHead className="text-right">Stok</TableHead>
                  <TableHead className="text-right">Forecast</TableHead>
                  <TableHead className="text-right">Hari Persediaan</TableHead>
                  <TableHead className="text-right">Rekomendasi Restock</TableHead>
                  <TableHead>Prioritas</TableHead>
                  <TableHead>Alasan</TableHead>
                  <TableHead />
                </TableRow>
              </TableHeader>
              <TableBody>
              {filtered.map((r) => {
                const u = urgencyMap[r.urgency];
                const forecast = forecasts.get(r.product_id);
                return (
                  <TableRow key={r.product_id} className={cn(r.urgency === "critical" && "bg-red-500/5")}>
                    <TableCell>
                      <div className="font-medium">{r.name}</div>
                      <div className="text-xs text-muted-foreground">{r.sku}</div>
                    </TableCell>
                    <TableCell className={cn("text-right tabular-nums font-semibold", r.current_stock <= r.low_stock_threshold && "text-red-600")}>
                      {formatNumber(r.current_stock)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {forecast ? `${formatNumber(forecast.predicted_units)} unit` : "—"}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">{r.days_of_supply.toFixed(0)} hari</TableCell>
                    <TableCell className="text-right tabular-nums font-medium">
                      {r.suggested_quantity > 0 ? `${formatNumber(r.suggested_quantity)} unit` : "—"}
                    </TableCell>
                    <TableCell>
                      <Badge className={u.className}>{u.label}</Badge>
                    </TableCell>
                    <TableCell className="max-w-sm whitespace-normal break-words text-sm leading-relaxed text-muted-foreground">{r.reasoning}</TableCell>
                    <TableCell>
                      {r.suggested_quantity > 0 && (
                        <Button size="sm" variant="outline" onClick={() => applyRestock(r)} disabled={applyingId === r.id}>
                          <Package className="size-4" />
                          {applyingId === r.id ? "..." : "Restock"}
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
          </div>

          <div className="space-y-3 md:hidden">
            {filtered.length === 0 ? (
              <p className="rounded-lg border border-dashed py-8 text-center text-sm text-muted-foreground">
                Tidak ada rekomendasi dengan prioritas ini.
              </p>
            ) : (
              filtered.map((r) => {
                const u = urgencyMap[r.urgency];
                const forecast = forecasts.get(r.product_id);
                return (
                  <div
                    key={r.product_id}
                    className={cn(
                      "rounded-xl border bg-card p-4 ring-1 ring-foreground/10",
                      r.urgency === "critical" && "border-red-500/30"
                    )}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <p className="truncate font-medium">{r.name}</p>
                        <p className="text-xs text-muted-foreground">{r.sku}</p>
                      </div>
                      <Badge className={cn(u.className, "shrink-0")}>{u.label}</Badge>
                    </div>
                    <div className="mt-3 grid grid-cols-3 gap-2">
                      <div className="rounded-lg border bg-card p-2 text-center">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Stok</p>
                        <p className={cn("text-sm font-semibold tabular-nums", r.current_stock <= r.low_stock_threshold && "text-red-600")}>
                          {formatNumber(r.current_stock)}
                        </p>
                      </div>
                      <div className="rounded-lg border bg-card p-2 text-center">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Forecast</p>
                        <p className="text-sm font-semibold tabular-nums">
                          {forecast ? formatNumber(forecast.predicted_units) : "—"}
                        </p>
                      </div>
                      <div className="rounded-lg border bg-card p-2 text-center">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Hari</p>
                        <p className="text-sm font-semibold tabular-nums">{r.days_of_supply.toFixed(0)}</p>
                      </div>
                    </div>
                    <div className="mt-3 flex items-center justify-between gap-3">
                      <div className="min-w-0">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Rekomendasi Restock</p>
                        <p className="text-sm font-semibold tabular-nums">
                          {r.suggested_quantity > 0 ? `${formatNumber(r.suggested_quantity)} unit` : "—"}
                        </p>
                      </div>
                      {r.suggested_quantity > 0 && (
                        <Button size="sm" variant="outline" onClick={() => applyRestock(r)} disabled={applyingId === r.id}>
                          <Package className="size-4" />
                          {applyingId === r.id ? "..." : "Restock"}
                        </Button>
                      )}
                    </div>
                    <p className="mt-3 border-t border-border pt-3 text-sm leading-relaxed text-muted-foreground">
                      {r.reasoning}
                    </p>
                  </div>
                );
              })
            )}
          </div>

          <p className="mt-4 text-xs text-muted-foreground">
            Perhitungan memadukan Sales Forecasting dan riwayat penjualan: qty = (forecast harian × lead time) − stok + ambang minimum untuk lead time 3 hari.
          </p>
        </CardContent>
      </Card>
      )}
    </>
  );
}