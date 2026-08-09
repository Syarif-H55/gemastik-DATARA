import * as React from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { navItems } from "@/components/layout/app-sidebar";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ChartDonut, SignOut } from "@/components/kira-icons";

function AppBrand() {
  return (
    <Link href="/dashboard" className="flex items-center gap-2 px-2 py-1">
      <span className="flex size-7 items-center justify-center rounded-md bg-foreground text-background">
        <ChartDonut className="size-4" />
      </span>
      <span className="font-semibold tracking-tight">KIRA</span>
    </Link>
  );
}

function AppFooter() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="w-full justify-start gap-2 px-2">
          <Avatar className="size-7">
            <AvatarFallback className="text-xs">PK</AvatarFallback>
          </Avatar>
          <span className="flex-1 text-left text-sm">
            <span className="block font-medium leading-tight">Pemilik UMKM</span>
            <span className="block text-xs text-muted-foreground">owner</span>
          </span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>Akun</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem>
          <SignOut className="size-4" />
          Keluar
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <AppShell
      brand={<AppBrand />}
      roleLabel="Menu"
      items={navItems}
      footer={<AppFooter />}
    >
      {children}
    </AppShell>
  );
}