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
import { getRestockRecommendations, getProductForecasts } from "@/lib/demo-data";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const urgencyMap: Record<string, { label: string; className: string }> = {
  critical: { label: "Kritis", className: "bg-red-600 text-white" },
  low: { label: "Perlu Restock", className: "bg-amber-500 text-white" },
  healthy: { label: "Aman", className: "bg-emerald-600 text-white" },
};

export default function RestockPage() {
  const recommendations = React.useMemo(() => getRestockRecommendations(), []);
  const forecasts = React.useMemo(() => new Map(getProductForecasts().map((f) => [f.product_id, f])), []);
  const [filter, setFilter] = React.useState<string>("all");

  const filtered = filter === "all" ? recommendations : recommendations.filter((r) => r.urgency === filter);
  const criticalCount = recommendations.filter((r) => r.urgency === "critical").length;

  const applyRestock = (r: (typeof recommendations)[number]) => {
    toast.success(`Restock ${r.name} sebanyak ${r.suggested_quantity} unit direkomendasikan`);
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
                    <TableCell className="max-w-sm text-sm text-muted-foreground">{r.reasoning}</TableCell>
                    <TableCell>
                      {r.suggested_quantity > 0 && (
                        <Button size="sm" variant="outline" onClick={() => applyRestock(r)}>
                          <Package className="size-4" />
                          Restock
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
          <p className="mt-4 text-xs text-muted-foreground">
            Perhitungan memadukan Sales Forecasting dan riwayat penjualan: qty = (forecast harian × lead time) − stok + ambang minimum untuk lead time 3 hari.
          </p>
        </CardContent>
      </Card>
    </>
  );
}