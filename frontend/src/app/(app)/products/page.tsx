"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowsDownUp, MagnifyingGlass } from "@phosphor-icons/react";
import { formatRupiah, formatPercent } from "@/lib/format";
import { getProductClass } from "@/lib/demo-data";
import { fetchProductProfitability } from "@/lib/datara";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { cn } from "@/lib/utils";

type SortKey = "name" | "selling_price" | "hpp" | "unit_profit" | "margin_percent" | "qty_sold" | "total_profit";

type ColumnKey = SortKey | "classification";

const columns: { key: ColumnKey; label: string; align?: "right" }[] = [
  { key: "name", label: "Produk" },
  { key: "selling_price", label: "Harga Jual", align: "right" },
  { key: "hpp", label: "HPP", align: "right" },
  { key: "unit_profit", label: "Laba / Unit", align: "right" },
  { key: "margin_percent", label: "Margin", align: "right" },
  { key: "qty_sold", label: "Terjual", align: "right" },
  { key: "total_profit", label: "Total Laba", align: "right" },
  { key: "classification", label: "Klasifikasi" },
];

function marginTone(margin: number): string {
  if (margin >= 40) return "bg-emerald-600 text-white";
  if (margin >= 25) return "bg-amber-500 text-white";
  return "bg-red-600 text-white";
}

const classTone: Record<string, string> = {
  profitable: "bg-emerald-600 text-white",
  potential: "bg-blue-600 text-white",
  evaluate: "bg-red-600 text-white",
};

export default function ProductsPage() {
  const { data, loading, error } = useApi(fetchProductProfitability);
  const profits = React.useMemo(() => data ?? [], [data]);
  const classes = React.useMemo(() => new Map(profits.map((p) => [p.product_id, getProductClass(p)])), [profits]);
  const [query, setQuery] = React.useState("");
  const [category, setCategory] = React.useState<string>("all");
  const [classFilter, setClassFilter] = React.useState<string>("all");
  const [sortKey, setSortKey] = React.useState<SortKey>("total_profit");
  const [sortDir, setSortDir] = React.useState<"asc" | "desc">("desc");

  const filtered = React.useMemo(() => {
    return profits
      .filter((p) => {
        const matchesQuery = p.name.toLowerCase().includes(query.toLowerCase()) || p.sku.toLowerCase().includes(query.toLowerCase());
        const matchesCategory = category === "all" || p.sku.startsWith(category);
        const matchesClass = classFilter === "all" || classes.get(p.product_id)?.classification === classFilter;
        return matchesQuery && matchesCategory && matchesClass;
      })
      .sort((a, b) => {
        const av = a[sortKey];
        const bv = b[sortKey];
        if (typeof av === "string" && typeof bv === "string") {
          return sortDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
        }
        return sortDir === "asc" ? (av as number) - (bv as number) : (bv as number) - (av as number);
      });
  }, [profits, query, category, classFilter, classes, sortKey, sortDir]);

  const toggleSort = (key: SortKey) => {
    if (key === sortKey) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else {
      setSortKey(key);
      setSortDir(key === "name" ? "asc" : "desc");
    }
  };

  return (
    <>
      <PageHeader
        title="Product Profitability"
        description="Klasifikasi produk (menguntungkan, berpotensi, perlu dievaluasi) berdasarkan margin, penjualan, dan biaya."
      />

      {loading ? (
        <div className="grid gap-4 sm:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </div>
      ) : error ? (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : (
      <>
      <div className="mb-4 grid gap-4 sm:grid-cols-3">
        {(["profitable", "potential", "evaluate"] as const).map((c) => {
          const count = profits.filter((p) => classes.get(p.product_id)?.classification === c).length;
          const label = c === "profitable" ? "Menguntungkan" : c === "potential" ? "Berpotensi" : "Perlu Evaluasi";
          return (
            <Card key={c} className={cn(c === "profitable" && "border-emerald-600/30", c === "potential" && "border-blue-600/30", c === "evaluate" && "border-red-600/30")}>
              <CardContent className="flex items-center justify-between py-4">
                <div>
                  <p className="text-sm font-medium">{label}</p>
                  <p className="text-xs text-muted-foreground">produk diklasifikasikan otomatis</p>
                </div>
                <span className="text-2xl font-semibold tabular-nums">{count}</span>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Card>
        <CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <CardTitle>Produk</CardTitle>
            <CardDescription>Urutkan berdasarkan kontribusi laba</CardDescription>
          </div>
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
            <div className="relative">
              <MagnifyingGlass className="absolute left-2.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input placeholder="Cari produk / SKU..." value={query} onChange={(e) => setQuery(e.target.value)} className="pl-8 w-56" />
            </div>
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Semua Kategori</SelectItem>
                <SelectItem value="MIN">Minuman</SelectItem>
                <SelectItem value="FOOD">Makanan</SelectItem>
                <SelectItem value="SNK">Camilan</SelectItem>
              </SelectContent>
            </Select>
            <Select value={classFilter} onValueChange={setClassFilter}>
              <SelectTrigger className="w-44">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Semua Klasifikasi</SelectItem>
                <SelectItem value="profitable">Menguntungkan</SelectItem>
                <SelectItem value="potential">Berpotensi</SelectItem>
                <SelectItem value="evaluate">Perlu Evaluasi</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                {columns.map((col) => (
                  <TableHead key={col.key} className={col.align === "right" ? "text-right" : undefined}>
                    {col.key === "classification" ? (
                      col.label
                    ) : (
                      <button
                        type="button"
                        onClick={() => toggleSort(col.key as SortKey)}
                        className={cn(
                          "inline-flex items-center gap-1 hover:text-foreground",
                          sortKey === col.key && "font-semibold text-foreground"
                        )}
                      >
                        {col.label}
                        <ArrowsDownUp className="size-3" />
                      </button>
                    )}
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={columns.length} className="h-24 text-center text-muted-foreground">
                    Tidak ada produk yang cocok dengan pencarian.
                  </TableCell>
                </TableRow>
              ) : (
                filtered.map((p) => {
                  const cls = classes.get(p.product_id);
                  return (
                    <TableRow key={p.product_id}>
                      <TableCell>
                        <div className="font-medium">{p.name}</div>
                        <div className="text-xs text-muted-foreground">{p.sku}</div>
                      </TableCell>
                      <TableCell className="text-right tabular-nums">{formatRupiah(p.selling_price)}</TableCell>
                      <TableCell className="text-right tabular-nums">{formatRupiah(p.hpp)}</TableCell>
                      <TableCell className="text-right tabular-nums">{formatRupiah(p.unit_profit)}</TableCell>
                      <TableCell className="text-right">
                        <Badge className={marginTone(p.margin_percent)}>{formatPercent(p.margin_percent, 0)}</Badge>
                      </TableCell>
                      <TableCell className="text-right tabular-nums">{p.qty_sold}</TableCell>
                      <TableCell className="text-right tabular-nums font-medium">{formatRupiah(p.total_profit)}</TableCell>
                      <TableCell>
                        {cls ? (
                          <div className="space-y-0.5">
                            <Badge className={classTone[cls.classification]}>{cls.label}</Badge>
                            <p className="max-w-52 text-xs text-muted-foreground">{cls.reason}</p>
                          </div>
                        ) : null}
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
      </>
      )}
    </>
  );
}