"use client";

import Link from "next/link";
import { SidebarSimple } from "@phosphor-icons/react";
import { ChartDonut } from "@/components/datara-icons";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";

/**
 * Brand header pada Sidebar (desktop).
 *
 * Expanded: [ikon logo] [DATARA] ............ [tombol toggle]
 * Collapsed (data-collapsible=icon, CSS-driven):
 *   - teks "DATARA" disembunyikan dengan transisi halus (w-0 + opacity-0),
 *   - ikon logo tetap terlihat dan berada di tengah sidebar,
 *   - tombol toggle membesar dan mengambang di garis batas kanan sidebar
 *     (absolute -right-3.5 top-5) agar tidak menabrak logo.
 *
 * Kelas `group-data-[collapsible=icon]:*` hanya aktif saat sidebar desktop
 * terlipat; pada mobile (Sheet) teks tetap tampil penuh.
 */
export function AppBrand() {
  const { state, toggleSidebar } = useSidebar();
  const isCollapsed = state === "collapsed";
  const label = isCollapsed ? "Perluas sidebar" : "Minimalkan sidebar";

  return (
    <div
      className={cn(
        "relative flex items-center justify-between gap-1",
        "group-data-[collapsible=icon]:-mx-2 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:gap-0"
      )}
    >
      <Link
        href="/dashboard"
        title="DATARA"
        className={cn(
          "flex min-w-0 flex-1 items-center gap-2 overflow-hidden px-1 py-0.5",
          "group-data-[collapsible=icon]:flex-none group-data-[collapsible=icon]:gap-0 group-data-[collapsible=icon]:p-0"
        )}
      >
        <span className="flex size-7 shrink-0 items-center justify-center rounded-md bg-foreground text-background">
          <ChartDonut className="size-4" />
        </span>
        <span
          className={cn(
            "truncate font-semibold tracking-tight",
            "transition-[width,opacity] duration-200 ease-linear",
            "group-data-[collapsible=icon]:w-0 group-data-[collapsible=icon]:overflow-hidden group-data-[collapsible=icon]:opacity-0"
          )}
        >
          DATARA
        </span>
      </Link>
      <Button
        type="button"
        variant="ghost"
        size="icon-sm"
        onClick={toggleSidebar}
        aria-label={label}
        title={label}
        className={cn(
          "hidden shrink-0 md:inline-flex",
          "transition-all duration-200",
          "group-data-[collapsible=icon]:absolute group-data-[collapsible=icon]:-right-3.5 group-data-[collapsible=icon]:top-5 group-data-[collapsible=icon]:z-20 group-data-[collapsible=icon]:size-7 group-data-[collapsible=icon]:rounded-full group-data-[collapsible=icon]:border group-data-[collapsible=icon]:bg-sidebar group-data-[collapsible=icon]:shadow-sm group-data-[collapsible=icon]:hover:bg-sidebar-accent group-data-[collapsible=icon]:hover:text-sidebar-accent-foreground"
        )}
      >
        <SidebarSimple
          className={cn(
            "size-4 transition-transform duration-200",
            "group-data-[collapsible=icon]:size-4.5 group-data-[collapsible=icon]:rotate-180"
          )}
        />
        <span className="sr-only">{label}</span>
      </Button>
    </div>
  );
}
