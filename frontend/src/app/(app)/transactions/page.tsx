"use client";

import * as React from "react";
import { PageHeader } from "@/components/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Trash, ShoppingBag, Package } from "@phosphor-icons/react";
import { formatRupiah } from "@/lib/format";
import { demoProducts, getProductById } from "@/lib/demo-data";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

type CartItem = {
  productId: number;
  quantity: number;
  unitPrice: number;
};

export default function TransactionsPage() {
  const [cart, setCart] = React.useState<CartItem[]>([]);
  const [customer, setCustomer] = React.useState("");
  const [paymentInput, setPaymentInput] = React.useState("");

  const removeFromCart = (productId: number) => setCart((prev) => prev.filter((c) => c.productId !== productId));

  const changeQty = (productId: number, delta: number) => {
    setCart((prev) =>
      prev
        .map((c) => (c.productId === productId ? { ...c, quantity: c.quantity + delta } : c))
        .filter((c) => c.quantity > 0)
    );
  };

  const subtotal = cart.reduce((sum, c) => sum + c.quantity * c.unitPrice, 0);

  const saveTransaction = () => {
    if (cart.length === 0) {
      toast.error("Keranjang masih kosong");
      return;
    }
    toast.success(`Transaksi disimpan (${cart.length} item, total ${formatRupiah(subtotal)}). Stok berkurang otomatis.`);
    setCart([]);
    setCustomer("");
    setPaymentInput("");
  };

  return (
    <>
      <PageHeader
        title="Catat Transaksi"
        description="Pencatatan penjualan harian. Persediaan stok akan terpotong otomatis."
      />

      <div className="grid gap-4 lg:grid-cols-[1fr_400px]">
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Pilih Produk</CardTitle>
              <CardDescription>Klik produk untuk menambahkan ke keranjang</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-2 sm:grid-cols-2">
                {demoProducts.map((p) => {
                  const inCart = cart.find((c) => c.productId === p.id);
                  const lowStock = p.stock <= p.low_stock_threshold;
                  return (
                    <button
                      key={p.id}
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
                      className={cn(
                        "flex items-start justify-between gap-2 rounded-md border p-3 text-left transition-colors hover:border-foreground",
                        inCart ? "border-foreground bg-foreground text-background" : "border-border hover:bg-muted"
                      )}
                    >
                      <div>
                        <div className="text-sm font-medium">{p.name}</div>
                        <div className={cn("text-xs", inCart ? "text-background/70" : "text-muted-foreground")}>
                          {formatRupiah(p.selling_price)}
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-1">
                        <span className={cn("text-xs", inCart ? "text-background/70" : lowStock ? "text-red-600" : "text-muted-foreground")}>
                          stok: {p.stock}
                        </span>
                        {inCart ? (
                          <span className={cn("rounded px-1 text-xs font-semibold", "bg-background text-foreground")}>
                            {inCart.quantity}x
                          </span>
                        ) : null}
                      </div>
                    </button>
                  );
                })}
              </div>
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
                    const p = getProductById(c.productId);
                    if (!p) return null;
                    return (
                      <div key={c.productId} className="flex items-center gap-3 rounded-md border p-2">
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
              const p = getProductById(c.productId);
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
            <p className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Package className="size-3.5" />
              Sistem akan mengurangi stok otomatis saat transaksi disimpan.
            </p>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={saveTransaction} disabled={cart.length === 0}>
              Simpan Transaksi
            </Button>
          </CardFooter>
        </Card>
      </div>
    </>
  );
}