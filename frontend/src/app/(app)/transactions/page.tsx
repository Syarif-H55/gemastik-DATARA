"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { PencilSimple, Trash, ShoppingBag, Package, Plus } from "@phosphor-icons/react";
import { formatRupiah } from "@/lib/format";
import { fetchProducts, deleteProduct, createTransaction } from "@/lib/datara";
import type { Product } from "@/lib/types";
import ProductFormDialog from "@/components/product-form-dialog";
import { useApi } from "@/hooks/use-api";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

type CartItem = {
  productId: number;
  quantity: number;
  unitPrice: number;
};

export default function TransactionsPage() {
  const [reloadKey, setReloadKey] = React.useState(0);
  const { data: products, loading, error } = useApi(fetchProducts, [reloadKey]);
  const [cart, setCart] = React.useState<CartItem[]>([]);
  const [customer, setCustomer] = React.useState("");
  const [paymentInput, setPaymentInput] = React.useState("");
  const [saving, setSaving] = React.useState(false);
  const [productDialogOpen, setProductDialogOpen] = React.useState(false);
  const [formKey, setFormKey] = React.useState(0);
  const [editProduct, setEditProduct] = React.useState<Product | null>(null);
  const [deleteTarget, setDeleteTarget] = React.useState<Product | null>(null);
  const [deleting, setDeleting] = React.useState(false);

  const removeFromCart = (productId: number) => setCart((prev) => prev.filter((c) => c.productId !== productId));

  const changeQty = (productId: number, delta: number) => {
    setCart((prev) =>
      prev
        .map((c) => (c.productId === productId ? { ...c, quantity: c.quantity + delta } : c))
        .filter((c) => c.quantity > 0)
    );
  };

  const subtotal = cart.reduce((sum, c) => sum + c.quantity * c.unitPrice, 0);
  const payment = paymentInput === "" ? 0 : Number(paymentInput);
  const change = payment - subtotal;
  const paymentValid = cart.length > 0 && payment >= subtotal;

  const openCreateDialog = () => {
    setEditProduct(null);
    setFormKey((k) => k + 1);
    setProductDialogOpen(true);
  };

  const openEditDialog = (product: Product) => {
    setEditProduct(product);
    setFormKey((k) => k + 1);
    setProductDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (!deleteTarget) return;
    setDeleting(true);
    try {
      await deleteProduct(deleteTarget.id);
      toast.success(`Produk "${deleteTarget.name}" dihapus.`);
      setCart((prev) => prev.filter((c) => c.productId !== deleteTarget.id));
      setDeleteTarget(null);
      setReloadKey((k) => k + 1);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Gagal menghapus produk.");
    } finally {
      setDeleting(false);
    }
  };

  const saveTransaction = async () => {
    if (cart.length === 0) {
      toast.error("Keranjang masih kosong");
      return;
    }
    if (payment < subtotal) {
      toast.error("Uang diterima kurang dari total transaksi");
      return;
    }
    setSaving(true);
    try {
      await createTransaction(
        cart.map((c) => ({ product_id: c.productId, quantity: c.quantity })),
        { customer_name: customer.trim() || undefined }
      );
      toast.success(`Transaksi disimpan (${cart.length} item, total ${formatRupiah(subtotal)}). Stok berkurang otomatis.`);
      setCart([]);
      setCustomer("");
      setPaymentInput("");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Gagal menyimpan transaksi.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <PageHeader
        title="Catat Transaksi"
        description="Pencatatan penjualan harian. Persediaan stok akan terpotong otomatis."
      />

      {error ? (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-[1fr_400px]">
        <div className="space-y-4">
          <Card>
            <CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <CardTitle>Pilih Produk</CardTitle>
                <CardDescription>Klik produk untuk menambahkan ke keranjang</CardDescription>
              </div>
              <Button variant="outline" size="sm" onClick={openCreateDialog}>
                <Plus className="size-4" />
                Tambah Produk
              </Button>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="grid gap-2 sm:grid-cols-2">
                  {Array.from({ length: 8 }).map((_, i) => (
                    <Skeleton key={i} className="h-24 w-full" />
                  ))}
                </div>
              ) : (
                <div className="grid gap-2 sm:grid-cols-2">
                  {(products ?? []).map((p) => {
                    const inCart = cart.find((c) => c.productId === p.id);
                    const lowStock = p.stock <= p.low_stock_threshold;
                    return (
                      <div
                        key={p.id}
                        className={cn(
                          "rounded-lg border p-3 transition-all duration-150",
                          inCart
                            ? "border-primary bg-primary text-primary-foreground shadow-sm"
                            : "border-border bg-card hover:border-primary/40 hover:bg-primary/[0.03]"
                        )}
                      >
                        <button
                          type="button"
                          onClick={() => {
                            if (inCart && inCart.quantity >= p.stock) {
                              toast(`Stok "${p.name}" tidak cukup (${p.stock})`);
                              return;
                            }
                            setCart((prev) => {
                              const existing = prev.find((c) => c.productId === p.id);
                              if (existing) {
                                return prev.map((c) => (c.productId === p.id ? { ...c, quantity: c.quantity + 1 } : c));
                              }
                              return [...prev, { productId: p.id, quantity: 1, unitPrice: p.selling_price }];
                            });
                          }}
                          className="flex w-full items-start justify-between gap-2 text-left"
                        >
                          <div>
                            <div className="text-sm font-medium">{p.name}</div>
                            <div className={cn("text-xs", inCart ? "text-primary-foreground/75" : "text-muted-foreground")}>
                              {formatRupiah(p.selling_price)}
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-1">
                            <span
                              className={cn(
                                "text-xs",
                                inCart ? "text-primary-foreground/75" : lowStock ? "text-red-600" : "text-muted-foreground"
                              )}
                            >
                              stok: {p.stock}
                            </span>
                            {inCart ? (
                              <span className={cn("rounded-full bg-white px-2 py-0.5 text-xs font-semibold tabular-nums text-primary")}>
                                {inCart.quantity}x
                              </span>
                            ) : null}
                          </div>
                        </button>
                        <div
                          className={cn(
                            "mt-2 flex items-center justify-between gap-2 border-t pt-2",
                            inCart ? "border-primary-foreground/15" : "border-border"
                          )}
                        >
                          <span
                            className={cn("text-[11px]", inCart ? "text-primary-foreground/60" : "text-muted-foreground")}
                          >
                            HPP: {formatRupiah(p.hpp)}/unit
                          </span>
                          <div className="flex gap-1">
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-7 gap-1 px-2"
                              onClick={() => openEditDialog(p)}
                            >
                              <PencilSimple className="size-3.5" />
                              Edit
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-7 gap-1 px-2 text-red-600 hover:text-red-700"
                              onClick={() => setDeleteTarget(p)}
                            >
                              <Trash className="size-3.5" />
                              Hapus
                            </Button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Keranjang</CardTitle>
              <CardDescription>{cart.length} item</CardDescription>
            </CardHeader>
            <CardContent>
              {cart.length === 0 ? (
                <p className="py-8 text-center text-sm text-muted-foreground">Belum ada item. Pilih produk di atas.</p>
              ) : (
                <div className="space-y-2">
                  {cart.map((c) => {
                    const p = (products ?? []).find((prod) => prod.id === c.productId);
                    if (!p) return null;
                    return (
                      <div key={c.productId} className="flex items-center gap-3 rounded-lg border bg-card p-2.5">
                        <div className="flex-1">
                          <div className="text-sm font-medium">{p.name}</div>
                          <div className="text-xs text-muted-foreground">{formatRupiah(c.unitPrice)} / unit</div>
                        </div>
                        <div className="flex items-center gap-1">
                          <Button size="icon" variant="outline" className="size-7" onClick={() => changeQty(c.productId, -1)}>
                            −
                          </Button>
                          <span className="w-8 text-center text-sm tabular-nums">{c.quantity}</span>
                          <Button size="icon" variant="outline" className="size-7" onClick={() => changeQty(c.productId, 1)}>
                            +
                          </Button>
                        </div>
                        <div className="w-24 text-right text-sm font-medium tabular-nums">
                          {formatRupiah(c.quantity * c.unitPrice)}
                        </div>
                        <Button size="icon" variant="ghost" className="size-7" onClick={() => removeFromCart(c.productId)} aria-label="Hapus">
                          <Trash className="size-4" />
                        </Button>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
            <CardFooter className="flex flex-col gap-4 border-t pt-4">
              <div className="flex w-full items-center justify-between text-sm">
                <span className="text-muted-foreground">Subtotal</span>
                <span className="text-lg font-semibold tabular-nums">{formatRupiah(subtotal)}</span>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="space-y-1.5">
                  <Label htmlFor="customer">Nama Pelanggan</Label>
                  <Input
                    id="customer"
                    placeholder="Opsional"
                    value={customer}
                    onChange={(e) => setCustomer(e.target.value)}
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="payment">Uang Diterima</Label>
                  <Input
                    id="payment"
                    type="number"
                    min={0}
                    placeholder="0"
                    value={paymentInput}
                    onChange={(e) => setPaymentInput(e.target.value)}
                  />
                </div>
              </div>
            </CardFooter>
          </Card>
        </div>

        <Card className="h-fit lg:sticky lg:top-20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShoppingBag className="size-4" />
              Ringkasan
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Subtotal</span>
              <span className="tabular-nums">{formatRupiah(subtotal)}</span>
            </div>
            {cart.map((c) => {
              const p = (products ?? []).find((prod) => prod.id === c.productId);
              return p ? (
                <div key={c.productId} className="flex justify-between text-xs text-muted-foreground">
                  <span>
                    {p.name} × {c.quantity}
                  </span>
                  <span className="tabular-nums">{formatRupiah(c.quantity * c.unitPrice)}</span>
                </div>
              ) : null;
            })}
            <Separator />
            <div className="flex justify-between text-base font-semibold">
              <span>Total</span>
              <span className="tabular-nums">{formatRupiah(subtotal)}</span>
            </div>
            {payment > 0 ? (
              <>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Uang Diterima</span>
                  <span className="tabular-nums">{formatRupiah(payment)}</span>
                </div>
                {change >= 0 ? (
                  <div className="flex justify-between text-sm font-semibold text-emerald-600">
                    <span>Kembalian</span>
                    <span className="tabular-nums">{formatRupiah(change)}</span>
                  </div>
                ) : (
                  <div className="flex justify-between text-sm font-semibold text-red-600">
                    <span>Uang kurang</span>
                    <span className="tabular-nums">{formatRupiah(Math.abs(change))}</span>
                  </div>
                )}
              </>
            ) : cart.length > 0 ? (
              <p className="text-xs text-muted-foreground">Masukkan Uang Diterima untuk menghitung kembalian.</p>
            ) : null}
            <p className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Package className="size-3.5" />
              Sistem akan mengurangi stok otomatis saat transaksi disimpan.
            </p>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={saveTransaction} disabled={cart.length === 0 || saving || !paymentValid}>
              {saving ? "Menyimpan..." : "Simpan Transaksi"}
            </Button>
          </CardFooter>
        </Card>
      </div>

      <ProductFormDialog
        key={formKey}
        open={productDialogOpen}
        onOpenChange={setProductDialogOpen}
        product={editProduct}
        onSaved={() => setReloadKey((k) => k + 1)}
      />

      <AlertDialog open={Boolean(deleteTarget)} onOpenChange={(open) => !open && setDeleteTarget(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Hapus produk?</AlertDialogTitle>
            <AlertDialogDescription>
              &quot;{deleteTarget?.name}&quot; akan dihapus dari daftar produk. Riwayat transaksi, stok, dan rekomendasi
              tetap tersimpan di sistem.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setDeleteTarget(null)} disabled={deleting}>
              Batal
            </AlertDialogCancel>
            <AlertDialogAction variant="destructive" onClick={confirmDelete} disabled={deleting}>
              {deleting ? "Menghapus..." : "Ya, Hapus"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}