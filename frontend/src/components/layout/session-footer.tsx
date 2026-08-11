"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { SignOut } from "@/components/datara-icons";
import { clearSession, getSessionUser } from "@/lib/auth";
import { cn } from "@/lib/utils";

export function SessionFooter() {
  const router = useRouter();
  const user = getSessionUser();

  const handleLogout = () => {
    clearSession();
    router.replace("/login");
  };

  const initials = user?.name
    ? user.name
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((p) => p[0]?.toUpperCase())
        .join("")
    : "PK";

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          className={cn(
            "w-full justify-start gap-2 px-2",
            // Saat sidebar terlipat: teks disembunyikan (transisi halus),
            // avatar tetap terlihat dan dipusatkan, padding/gap dihilangkan
            // agar tidak meluber melewati lebar sidebar (48px).
            "group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:gap-0 group-data-[collapsible=icon]:px-0"
          )}
        >
          <Avatar className="size-7 shrink-0">
            <AvatarFallback className="text-xs">{initials}</AvatarFallback>
          </Avatar>
          <span
            className={cn(
              "min-w-0 flex-1 overflow-hidden text-left text-sm",
              "transition-[width,opacity] duration-200 ease-linear",
              "group-data-[collapsible=icon]:w-0 group-data-[collapsible=icon]:grow-0 group-data-[collapsible=icon]:opacity-0"
            )}
          >
            <span className="block truncate font-medium leading-tight">
              {user?.name ?? "Pemilik UMKM"}
            </span>
            <span className="block truncate text-xs text-muted-foreground">
              {user?.email ?? "owner"}
            </span>
          </span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>Akun</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onSelect={handleLogout}>
          <SignOut className="size-4" />
          Keluar
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
