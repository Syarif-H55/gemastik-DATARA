"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { ArrowsDownUp } from "@phosphor-icons/react";
import { formatRupiah, formatPercent } from "@/lib/format";
import { fetchPricingRecommendations, applyPricingRecommendation } from "@/lib/datara";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

export default function PricingPage() {
  const [targetMargin, setTargetMargin] = React.useState(30);
  const { data, loading, error } = useApi(() => fetchPricingRecommendations(targetMargin), [targetMargin]);
  const [applying, setApplying] = React.useState(false);

  const recommendations = data ?? [];

  const applyAll = async () => {
    const changes = recommendations.filter((r) => r.recommended_price !== r.current_price);
    if (changes.length === 0) {
      toast("Tidak ada produk yang perlu penyesuaian harga.");
      return;
    }
    setApplying(true);
    try {
      for (const r of changes) {
        await applyPricingRecommendation(r.id);
      }
      toast.success(`Menerapkan harga baru untuk ${changes.length} produk`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Gagal menerapkan harga.");
    } finally {
      setApplying(false);
    }
  };

  return (
    <>
      <PageHeader
        title="Smart Pricing"
        description="Rekomendasi harga jual produk dengan alasan berbasis HPP, biaya, dan target margin."
      />

      <Card className="mb-4">
        <CardContent className="flex flex-col gap-4 py-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="max-w-md flex-1 space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="margin">Target Margin Kotor</Label>
              <span className="text-sm font-semibold tabular-nums">{targetMargin}%</span>
            </div>
            <input
              id="margin"
              type="range"
              min={10}
              max={60}
              step={1}
              value={targetMargin}
              onChange={(e) => setTargetMargin(Number(e.target.value))}
              className="w-full accent-foreground"
            />
            <p className="text-xs text-muted-foreground">
              Harga rekomendasi = HPP ÷ (1 − target margin). Dibulatkan ke kelipatan Rp 500.
            </p>
          </div>
          <Button onClick={applyAll} disabled={applying}>
            {applying ? "Menerapkan..." : "Terapkan Semua Rekomendasi"}
          </Button>
        </CardContent>
      </Card>

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
        <CardHeader>
          <CardTitle>Rekomendasi Harga</CardTitle>
          <CardDescription>Target margin {targetMargin}% — produk dengan harga perlu penyesuaian ditandai.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Produk</TableHead>
                <TableHead className="text-right">Harga Saat Ini</TableHead>
                <TableHead className="text-right">HPP</TableHead>
                <TableHead className="text-right">Margin Aktual</TableHead>
                <TableHead className="text-right">Harga Rekomendasi</TableHead>
                <TableHead>Alasan</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recommendations.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="h-24 text-center text-muted-foreground">
                    Belum ada data produk.
                  </TableCell>
                </TableRow>
              ) : (
                recommendations.map((r) => {
                const change = r.recommended_price !== r.current_price;
                return (
                  <TableRow key={r.product_id} className={cn(change && "bg-primary/5")}>
                    <TableCell>
                      <div className="font-medium">{r.name}</div>
                      <div className="text-xs text-muted-foreground">{r.sku}</div>
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {formatRupiah(r.current_price)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">{formatRupiah(r.hpp)}</TableCell>
                    <TableCell className="text-right">
                      <Badge variant={change ? "destructive" : "secondary"}>
                        {formatPercent(r.actual_margin_percent, 0)}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <span className={cn("tabular-nums font-medium", change ? "text-primary" : "text-muted-foreground")}>
                        {formatRupiah(r.recommended_price)}
                      </span>
                    </TableCell>
                    <TableCell className="max-w-sm text-sm text-muted-foreground">{r.reasoning}</TableCell>
                  </TableRow>
                );
              })
              )}
            </TableBody>
          </Table>
          <div className="mt-4 flex items-center gap-2 pt-2">
            <ArrowsDownUp className="size-4" />
            <p className="text-sm text-muted-foreground">
              Rekomendasi ini dihasilkan engine berdasarkan HPP, target margin, dan pembulatan harga psikologis.
            </p>
          </div>
        </CardContent>
      </Card>
      )}
    </>
  );
}