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
 *   - ikon logo di link ikut memudar agar tidak dobel,
 *   - tombol toggle BERUBAH menjadi logo DATARA (kotak biru + ChartDonut)
 *     yang terpusat di rel; klik logo = perluas sidebar kembali.
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
          "group-data-[collapsible=icon]:pointer-events-none group-data-[collapsible=icon]:flex-none group-data-[collapsible=icon]:gap-0 group-data-[collapsible=icon]:p-0"
        )}
      >
        <span
          className={cn(
            "flex size-7 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground shadow-sm",
            "transition-opacity duration-200",
            "group-data-[collapsible=icon]:opacity-0"
          )}
        >
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
          "transition-[transform,opacity,background-color] duration-200",
          // Centering saat collapsed memakai auto-margin (bukan translate):
          // variant shadcn `active:translate-y-px` menimpa properti CSS
          // `translate`, yang membuat tombol melompat ~17px saat ditekan
          // dan klik tidak terdaftar. -mt-4 = setengah tinggi tombol (32px).
          "group-data-[collapsible=icon]:absolute group-data-[collapsible=icon]:left-0 group-data-[collapsible=icon]:right-0 group-data-[collapsible=icon]:top-1/2 group-data-[collapsible=icon]:z-20 group-data-[collapsible=icon]:mx-auto group-data-[collapsible=icon]:size-8 group-data-[collapsible=icon]:-mt-4 group-data-[collapsible=icon]:rounded-lg group-data-[collapsible=icon]:border-0 group-data-[collapsible=icon]:bg-primary group-data-[collapsible=icon]:text-primary-foreground group-data-[collapsible=icon]:shadow-sm group-data-[collapsible=icon]:hover:bg-primary/90 group-data-[collapsible=icon]:hover:text-primary-foreground"
        )}
      >
        {isCollapsed ? <ChartDonut className="size-4" /> : <SidebarSimple className="size-4" />}
        <span className="sr-only">{label}</span>
      </Button>
    </div>
  );
}
