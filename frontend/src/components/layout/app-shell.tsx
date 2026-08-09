"use client";

import { AppSidebar, type NavItem } from "@/components/layout/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { ThemeToggle } from "@/components/theme-toggle";
import { cn } from "@/lib/utils";
import * as React from "react";

export function AppShell({
  brand,
  roleLabel,
  items,
  footer,
  children,
  className,
}: {
  brand: React.ReactNode;
  roleLabel: string;
  items: NavItem[];
  footer: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <SidebarProvider>
      <AppSidebar brand={brand} groupLabel={roleLabel} items={items} footer={footer} />
      <SidebarInset className="min-h-svh">
        <header className="flex shrink-0 items-center gap-2 border-b px-4 h-14">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <div className="flex-1" />
          <ThemeToggle />
        </header>
        <main className={cn("flex-1 p-4 md:p-6 lg:p-8", className)}>{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}