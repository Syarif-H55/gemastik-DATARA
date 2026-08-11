import * as React from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { navItems } from "@/components/layout/app-sidebar";
import { AuthGuard } from "@/components/layout/auth-guard";
import { SessionFooter } from "@/components/layout/session-footer";
import { ChartDonut } from "@/components/datara-icons";

function AppBrand() {
  return (
    <Link href="/dashboard" className="flex items-center gap-2 px-2 py-1">
      <span className="flex size-7 items-center justify-center rounded-md bg-foreground text-background">
        <ChartDonut className="size-4" />
      </span>
      <span className="font-semibold tracking-tight">DATARA</span>
    </Link>
  );
}

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthGuard>
      <AppShell
        brand={<AppBrand />}
        roleLabel="Menu"
        items={navItems}
        footer={<SessionFooter />}
      >
        {children}
      </AppShell>
    </AuthGuard>
  );
}
