"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ChartLineUp,
  ChartPieSlice,
  ClipboardText,
  LineSegments,
  Package,
  Signpost,
  ShoppingCart,
  Target,
  type Icon,
} from "@phosphor-icons/react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

export type NavItem = {
  title: string;
  href: string;
  icon?: Icon;
};

export function AppSidebar({
  brand,
  groupLabel,
  items,
  footer,
}: {
  brand: React.ReactNode;
  groupLabel: string;
  items: NavItem[];
  footer: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>{brand}</SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>{groupLabel}</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => {
                const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
                const Icon = item.icon;
                return (
                  <SidebarMenuItem key={item.href}>
                    <SidebarMenuButton asChild isActive={active} tooltip={item.title}>
                      <Link href={item.href}>
                        {Icon ? <Icon className="size-4" /> : null}
                        <span>{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>{footer}</SidebarFooter>
    </Sidebar>
  );
}

export const navItems: NavItem[] = [
  { title: "Business Dashboard", href: "/dashboard", icon: ChartLineUp },
  { title: "Catat Transaksi", href: "/transactions", icon: ShoppingCart },
  { title: "Sales Forecasting", href: "/forecasting", icon: LineSegments },
  { title: "Product Profitability", href: "/products", icon: ChartPieSlice },
  { title: "Smart Pricing", href: "/pricing", icon: Target },
  { title: "Smart Restock", href: "/restock", icon: Package },
  { title: "Keputusan & Monitoring", href: "/decisions", icon: ClipboardText },
  { title: "Roadmap Pertumbuhan", href: "/growth", icon: Signpost },
];