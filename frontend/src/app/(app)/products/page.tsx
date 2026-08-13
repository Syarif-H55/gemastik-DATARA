"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowsDownUp, CaretDown, MagnifyingGlass } from "@phosphor-icons/react";
import { formatRupiah, formatPercent } from "@/lib/format";
import { getProductClass } from "@/lib/demo-data";
import { fetchProductProfitability, fetchProductCosts } from "@/lib/datara";
import type { ProductCosts } from "@/lib/types";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { toast } from "sonner";
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
  const [expandedId, setExpandedId] = React.useState<number | null>(null);
  const [costsCache, setCostsCache] = React.useState<Record<number, ProductCosts>>({});
  const [costsLoadingId, setCostsLoadingId] = React.useState<number | null>(null);

  const toggleExpand = (productId: number) => {
    if (expandedId === productId) {
      setExpandedId(null);
      return;
    }
    setExpandedId(productId);
    if (!costsCache[productId]) {
      setCostsLoadingId(productId);
      fetchProductCosts(productId)
        .then((costs) => setCostsCache((prev) => ({ ...prev, [productId]: costs })))
        .catch((err) => toast.error(err instanceof Error ? err.message : "Gagal memuat rincian HPP."))
        .finally(() => setCostsLoadingId(null));
    }
  };

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
          const dot = c === "profitable" ? "bg-emerald-500" : c === "potential" ? "bg-blue-500" : "bg-red-500";
          return (
            <Card key={c} className={cn(c === "profitable" && "border-emerald-600/30", c === "potential" && "border-blue-600/30", c === "evaluate" && "border-red-600/30")}>
              <CardContent className="flex items-center justify-between gap-3 py-4">
                <div className="flex items-center gap-2.5">
                  <span className={cn("size-2.5 shrink-0 rounded-full", dot)} />
                  <div>
                    <p className="text-sm font-medium">{label}</p>
                    <p className="text-xs text-muted-foreground">produk diklasifikasikan otomatis</p>
                  </div>
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
          <div className="hidden md:block">
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
                  const isExpanded = expandedId === p.product_id;
                  const costs = costsCache[p.product_id];
                  const costItems = costs?.items ?? [];
                  return (
                    <React.Fragment key={p.product_id}>
                      <TableRow>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <button
                              type="button"
                              onClick={() => toggleExpand(p.product_id)}
                              aria-expanded={isExpanded}
                              aria-label={`Lihat rincian HPP ${p.name}`}
                              className={cn(
                                "shrink-0 rounded-sm p-0.5 text-muted-foreground transition-colors hover:text-foreground",
                                isExpanded && "text-foreground"
                              )}
                            >
                              <CaretDown
                                className={cn("size-3.5 transition-transform", !isExpanded && "-rotate-90")}
                              />
                            </button>
                            <div className="min-w-0">
                              <div className="truncate font-medium">{p.name}</div>
                              <div className="text-xs text-muted-foreground">{p.sku}</div>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell className="text-right tabular-nums">{formatRupiah(p.selling_price)}</TableCell>
                        <TableCell className="text-right">
                          <button
                            type="button"
                            onClick={() => toggleExpand(p.product_id)}
                            className={cn(
                              "tabular-nums underline-offset-4 hover:underline",
                              isExpanded && "underline"
                            )}
                          >
                            {formatRupiah(p.hpp)}
                          </button>
                        </TableCell>
                        <TableCell className="text-right tabular-nums">{formatRupiah(p.unit_profit)}</TableCell>
                        <TableCell className="text-right">
                          <Badge className={marginTone(p.margin_percent)}>{formatPercent(p.margin_percent, 0)}</Badge>
                        </TableCell>
                        <TableCell className="text-right tabular-nums">{p.qty_sold}</TableCell>
                        <TableCell className="text-right tabular-nums font-medium">{formatRupiah(p.total_profit)}</TableCell>
                        <TableCell className="whitespace-normal">
                          {cls ? (
                            <div className="space-y-0.5">
                              <Badge className={classTone[cls.classification]}>{cls.label}</Badge>
                              <p className="max-w-52 text-xs text-muted-foreground">{cls.reason}</p>
                            </div>
                          ) : null}
                        </TableCell>
                      </TableRow>
                      {isExpanded ? (
                        <TableRow>
                          <TableCell colSpan={columns.length} className="whitespace-normal bg-muted/40 p-0">
                            <div className="px-6 py-5">
                              {costsLoadingId === p.product_id ? (
                                <div className="max-w-xl space-y-3">
                                  <Skeleton className="h-3 w-36" />
                                  <Skeleton className="h-4 w-full" />
                                  <Skeleton className="h-4 w-2/3" />
                                </div>
                              ) : costItems.length > 0 ? (
                                <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:gap-12">
                                  <div className="min-w-0 flex-1">
                                    <p className="mb-2 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                                      Rincian HPP per unit
                                    </p>
                                    <div className="grid max-w-2xl gap-x-10 gap-y-1 sm:grid-cols-2">
                                      {costItems.map((item, i) => (
                                        <div
                                          key={item.id ?? i}
                                          className="flex items-baseline justify-between gap-4 border-b border-dashed border-border py-1 text-sm"
                                        >
                                          <span className="truncate text-muted-foreground">{item.name}</span>
                                          <span className="shrink-0 tabular-nums">{formatRupiah(item.cost_per_unit)}</span>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                  <div className="shrink-0 lg:border-l lg:border-border lg:pl-12">
                                    <p className="mb-1 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                                      Total HPP
                                    </p>
                                    <p className="text-xl font-semibold tabular-nums">{formatRupiah(p.hpp)}</p>
                                    <p className="mt-0.5 text-xs text-muted-foreground">
                                      per unit — dipakai Smart Pricing
                                    </p>
                                  </div>
                                </div>
                              ) : (
                                <p className="max-w-xl text-sm text-muted-foreground">
                                  Belum ada rincian HPP untuk produk ini. Buka kartu produk di halaman{" "}
                                  <span className="font-medium text-foreground">Transaksi</span> lalu pilih{" "}
                                  <span className="font-medium text-foreground">Edit</span> untuk menambahkan
                                  komponen biaya.
                                </p>
                              )}
                            </div>
                          </TableCell>
                        </TableRow>
                      ) : null}
                    </React.Fragment>
                  );
                })
              )}
            </TableBody>
          </Table>
          </div>

          <div className="space-y-3 md:hidden">
            {filtered.length === 0 ? (
              <p className="rounded-lg border border-dashed py-8 text-center text-sm text-muted-foreground">
                Tidak ada produk yang cocok dengan pencarian.
              </p>
            ) : (
              filtered.map((p) => {
                const cls = classes.get(p.product_id);
                const isExpanded = expandedId === p.product_id;
                const costs = costsCache[p.product_id];
                const costItems = costs?.items ?? [];
                return (
                  <div key={p.product_id} className="rounded-xl border bg-card p-4 ring-1 ring-foreground/10">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex min-w-0 items-center gap-2">
                        <button
                          type="button"
                          onClick={() => toggleExpand(p.product_id)}
                          aria-expanded={isExpanded}
                          aria-label={`Lihat rincian HPP ${p.name}`}
                          className={cn(
                            "shrink-0 rounded-sm p-0.5 text-muted-foreground transition-colors hover:text-foreground",
                            isExpanded && "text-foreground"
                          )}
                        >
                          <CaretDown className={cn("size-3.5 transition-transform", !isExpanded && "-rotate-90")} />
                        </button>
                        <div className="min-w-0">
                          <p className="truncate font-medium">{p.name}</p>
                          <p className="text-xs text-muted-foreground">{p.sku}</p>
                        </div>
                      </div>
                      {cls ? (
                        <Badge className={cn(classTone[cls.classification], "shrink-0")}>{cls.label}</Badge>
                      ) : null}
                    </div>

                    <div className="mt-3 grid grid-cols-2 gap-2">
                      <div className="rounded-lg border bg-card p-2">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Harga Jual</p>
                        <p className="truncate text-sm font-semibold tabular-nums">{formatRupiah(p.selling_price)}</p>
                      </div>
                      <div className="rounded-lg border bg-card p-2">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Margin</p>
                        <p className="text-sm font-semibold">
                          <Badge className={marginTone(p.margin_percent)}>{formatPercent(p.margin_percent, 0)}</Badge>
                        </p>
                      </div>
                      <div className="rounded-lg border bg-card p-2">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">HPP</p>
                        <button
                          type="button"
                          onClick={() => toggleExpand(p.product_id)}
                          className="text-sm font-semibold tabular-nums underline-offset-4 hover:underline"
                        >
                          {formatRupiah(p.hpp)}
                        </button>
                      </div>
                      <div className="rounded-lg border bg-card p-2">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Laba / Unit</p>
                        <p className="truncate text-sm font-semibold tabular-nums">{formatRupiah(p.unit_profit)}</p>
                      </div>
                      <div className="rounded-lg border bg-card p-2">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Terjual</p>
                        <p className="text-sm font-semibold tabular-nums">{p.qty_sold}</p>
                      </div>
                      <div className="rounded-lg border bg-card p-2">
                        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Total Laba</p>
                        <p className="truncate text-sm font-semibold tabular-nums">{formatRupiah(p.total_profit)}</p>
                      </div>
                    </div>

                    {cls ? <p className="mt-2 text-xs text-muted-foreground">{cls.reason}</p> : null}

                    {isExpanded ? (
                      <div className="mt-3 rounded-lg bg-muted/40 p-4">
                        {costsLoadingId === p.product_id ? (
                          <div className="space-y-3">
                            <Skeleton className="h-3 w-36" />
                            <Skeleton className="h-4 w-full" />
                            <Skeleton className="h-4 w-2/3" />
                          </div>
                        ) : costItems.length > 0 ? (
                          <div className="space-y-4">
                            <div className="min-w-0 flex-1">
                              <p className="mb-2 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                                Rincian HPP per unit
                              </p>
                              <div className="space-y-1">
                                {costItems.map((item, i) => (
                                  <div
                                    key={item.id ?? i}
                                    className="flex items-baseline justify-between gap-4 border-b border-dashed border-border py-1 text-sm"
                                  >
                                    <span className="min-w-0 truncate text-muted-foreground">{item.name}</span>
                                    <span className="shrink-0 tabular-nums">{formatRupiah(item.cost_per_unit)}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                            <div className="border-t border-border pt-3">
                              <p className="mb-1 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                                Total HPP
                              </p>
                              <p className="text-xl font-semibold tabular-nums">{formatRupiah(p.hpp)}</p>
                              <p className="mt-0.5 text-xs text-muted-foreground">per unit — dipakai Smart Pricing</p>
                            </div>
                          </div>
                        ) : (
                          <p className="text-sm text-muted-foreground">
                            Belum ada rincian HPP untuk produk ini. Buka kartu produk di halaman{" "}
                            <span className="font-medium text-foreground">Transaksi</span> lalu pilih{" "}
                            <span className="font-medium text-foreground">Edit</span> untuk menambahkan komponen
                            biaya.
                          </p>
                        )}
                      </div>
                    ) : null}
                  </div>
                );
              })
            )}
          </div>
        </CardContent>
      </Card>
      </>
      )}
    </>
  );
}