"use client";

import * as React from "react";
import { Plus, X } from "@phosphor-icons/react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { formatRupiah } from "@/lib/format";
import { createProduct, updateProduct, fetchProductCosts } from "@/lib/datara";
import type { Product } from "@/lib/types";
import { toast } from "sonner";

type CostRow = {
  name: string;
  amount: string;
};

interface ProductFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  product?: Product | null;
  onSaved?: () => void;
}

export default function ProductFormDialog({
  open,
  onOpenChange,
  product,
  onSaved,
}: ProductFormDialogProps) {
  const isEdit = Boolean(product);
  const [loading, setLoading] = React.useState(Boolean(product));
  const [saving, setSaving] = React.useState(false);
  const [name, setName] = React.useState(product?.name ?? "");
  const [sku, setSku] = React.useState(product?.sku ?? "");
  const [price, setPrice] = React.useState(product ? String(product.selling_price) : "");
  const [stock, setStock] = React.useState("");
  const [costItems, setCostItems] = React.useState<CostRow[]>(product ? [] : [{ name: "", amount: "" }]);

  React.useEffect(() => {
    if (!product) return;
    let cancelled = false;
    fetchProductCosts(product.id)
      .then((costs) => {
        if (cancelled) return;
        setCostItems(
          costs.items.length > 0
            ? costs.items.map((i) => ({ name: i.name, amount: String(i.cost_per_unit) }))
            : [{ name: "", amount: "" }]
        );
      })
      .catch((err) => {
        if (cancelled) return;
        toast.error(err instanceof Error ? err.message : "Gagal memuat rincian HPP produk.");
        onOpenChange(false);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [product, onOpenChange]);

  const totalHpp = costItems.reduce((sum, row) => sum + (Number(row.amount) || 0), 0);

  const updateCostItem = (index: number, patch: Partial<CostRow>) => {
    setCostItems((prev) => prev.map((row, i) => (i === index ? { ...row, ...patch } : row)));
  };

  const removeCostItem = (index: number) => {
    setCostItems((prev) => prev.filter((_, i) => i !== index));
  };

  const addCostItem = () => {
    setCostItems((prev) => [...prev, { name: "", amount: "" }]);
  };

  const buildCostPayload = () => {
    const items: { name: string; cost_per_unit: number }[] = [];
    for (const row of costItems) {
      const rowName = row.name.trim();
      const rowAmount = Number(row.amount);
      if (rowName === "" && row.amount.trim() === "") continue;
      if (rowName === "") {
        toast.error("Nama komponen HPP tidak boleh kosong");
        return null;
      }
      if (!Number.isFinite(rowAmount) || rowAmount < 0) {
        toast.error("Biaya komponen HPP harus angka lebih dari atau sama dengan 0");
        return null;
      }
      items.push({ name: rowName, cost_per_unit: rowAmount });
    }
    return items;
  };

  const handleSubmit = async () => {
    const trimmedName = name.trim();
    if (!trimmedName) {
      toast.error("Nama produk wajib diisi");
      return;
    }
    const sellingPrice = Number(price);
    if (!Number.isFinite(sellingPrice) || sellingPrice <= 0) {
      toast.error("Harga jual harus angka lebih dari 0");
      return;
    }
    const costPayload = buildCostPayload();
    if (costPayload === null) return;

    setSaving(true);
    try {
      if (product) {
        await updateProduct(product.id, {
          name: trimmedName,
          sku: sku.trim() || undefined,
          selling_price: sellingPrice,
          cost_items: costPayload,
        });
        toast.success(`Produk "${trimmedName}" berhasil diperbarui.`);
      } else {
        await createProduct({
          name: trimmedName,
          sku: sku.trim() || undefined,
          selling_price: sellingPrice,
          current_stock: Number(stock) > 0 ? Number(stock) : 0,
          cost_items: costPayload,
        });
        toast.success(`Produk "${trimmedName}" berhasil ditambahkan.`);
      }
      onOpenChange(false);
      onSaved?.();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Gagal menyimpan produk.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{isEdit ? "Edit Produk" : "Tambah Produk"}</DialogTitle>
          <DialogDescription>
            {isEdit
              ? "Perbarui nama, harga jual, dan rincian HPP produk."
              : "Produk baru langsung tersedia untuk dicatat dalam transaksi."}
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="pfd-name">Nama Produk</Label>
            <Input
              id="pfd-name"
              placeholder="Contoh: Es Cappuccino"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label htmlFor="pfd-sku">SKU (opsional)</Label>
              <Input
                id="pfd-sku"
                placeholder="Contoh: MIN-005"
                value={sku}
                onChange={(e) => setSku(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="pfd-price">Harga Jual (Rp)</Label>
              <Input
                id="pfd-price"
                type="number"
                min={0}
                placeholder="0"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
              />
            </div>
            {!isEdit ? (
              <div className="space-y-2">
                <Label htmlFor="pfd-stock">Stok Awal</Label>
                <Input
                  id="pfd-stock"
                  type="number"
                  min={0}
                  placeholder="0"
                  value={stock}
                  onChange={(e) => setStock(e.target.value)}
                />
              </div>
            ) : null}
          </div>

          <div className="space-y-2">
            <Label>Rincian HPP (per unit)</Label>
            {loading ? (
              <p className="text-xs text-muted-foreground">Memuat rincian HPP...</p>
            ) : (
              <>
                <div className="space-y-2">
                  {costItems.map((row, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <Input
                        placeholder="Nama komponen (mis. Cup + tutup)"
                        value={row.name}
                        onChange={(e) => updateCostItem(index, { name: e.target.value })}
                      />
                      <Input
                        type="number"
                        min={0}
                        placeholder="Biaya"
                        className="w-28"
                        value={row.amount}
                        onChange={(e) => updateCostItem(index, { amount: e.target.value })}
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="size-9 shrink-0"
                        onClick={() => removeCostItem(index)}
                        aria-label="Hapus komponen"
                      >
                        <X className="size-4" />
                      </Button>
                    </div>
                  ))}
                </div>
                <Button type="button" variant="outline" size="sm" onClick={addCostItem}>
                  <Plus className="size-4" />
                  Tambah Komponen
                </Button>
                <p className="text-xs text-muted-foreground">
                  Total HPP: <span className="font-medium text-foreground">{formatRupiah(totalHpp)}</span> per unit —
                  dipakai untuk Smart Pricing.
                </p>
              </>
            )}
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={saving}>
            Batal
          </Button>
          <Button onClick={handleSubmit} disabled={saving || loading}>
            {saving ? "Menyimpan..." : isEdit ? "Simpan Perubahan" : "Simpan Produk"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}