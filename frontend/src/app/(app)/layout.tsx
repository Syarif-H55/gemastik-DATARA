import * as React from "react";
import { AppBrand } from "@/components/layout/app-brand";
import { AppShell } from "@/components/layout/app-shell";
import { navItems } from "@/components/layout/app-sidebar";
import { AuthGuard } from "@/components/layout/auth-guard";
import { SessionFooter } from "@/components/layout/session-footer";

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
