"use client";

import * as React from "react";
import Link from "next/link";
import { PageHeader } from "@/components/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Check, CircleNotch, Hourglass, Star } from "@phosphor-icons/react";
import { formatNumber } from "@/lib/format";
import { fetchGrowth } from "@/lib/datara";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { cn } from "@/lib/utils";

const stageMeta: Record<string, { label: string; className: string; icon: React.ReactNode }> = {
  done: { label: "Selesai", className: "bg-emerald-600 text-white", icon: <Check className="size-3" /> },
  current: { label: "Sedang Berjalan", className: "bg-blue-600 text-white", icon: <CircleNotch className="size-3" /> },
  next: { label: "Berikutnya", className: "bg-amber-500 text-white", icon: <Star className="size-3" /> },
  upcoming: { label: "Mendatang", className: "bg-muted text-muted-foreground", icon: <Hourglass className="size-3" /> },
};

export default function GrowthPage() {
  const { data, loading, error } = useApi(fetchGrowth);
  const stages = data?.stages ?? [];

  return (
    <>
      <PageHeader
        title="Roadmap Pertumbuhan"
        description="Evaluasi perkembangan usaha berdasarkan indikator bisnis dan langkah menuju target pertumbuhan berikutnya (FR-011, FR-012)."
      />

      {loading ? (
        <div className="grid gap-4 lg:grid-cols-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-40 w-full" />
          ))}
        </div>
      ) : error ? (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : (
      <div className="grid gap-4 lg:grid-cols-2">
        {stages.map((s, i) => {
          const meta = stageMeta[s.status] ?? stageMeta.upcoming;
          const progress = s.metric_1_target > 0 ? Math.min(100, Math.round((s.metric_1_value / s.metric_1_target) * 100)) : 0;
          const reached = s.metric_1_value >= s.metric_1_target;
          return (
            <Card key={s.id} className={cn(s.status === "current" && "border-primary/30 bg-primary/5")}>
              <CardHeader className="flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={cn("flex size-6 items-center justify-center rounded-full text-xs font-semibold tabular-nums", s.status === "current" ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground")}>
                      {i + 1}
                    </span>
                    <CardTitle className="text-base">{s.label}</CardTitle>
                  </div>
                  <Badge className={meta.className}>
                    {meta.label}
                  </Badge>
                </div>
                <CardDescription>{s.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">{s.metric_1}</span>
                    <span className="font-medium tabular-nums">
                      {formatNumber(s.metric_1_value)} / {formatNumber(s.metric_1_target)}
                    </span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>
                {reached ? (
                  <p className="flex items-center gap-1.5 text-sm text-emerald-600">
                    <Check className="size-4" /> Target tercapai
                  </p>
                ) : (
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Langkah berikutnya: {s.next_step}</p>
                    {s.status === "current" && (
                      <div className="rounded-md border border-primary/20 bg-primary/5 p-3">
                        <p className="text-xs font-medium">
                          Target belum tercapai — selisih{" "}
                          {formatNumber(Math.max(0, s.metric_1_target - s.metric_1_value))} dari target{" "}
                          {formatNumber(s.metric_1_target)}
                        </p>
                        <p className="mt-1 text-xs text-muted-foreground">
                          Terapkan rekomendasi Smart Pricing untuk mengejar margin, atau pastikan ketersediaan stok
                          melalui Smart Restock, lalu pantau dampaknya di Keputusan & Monitoring.
                        </p>
                        <div className="mt-2 flex flex-wrap gap-2">
                          <Button asChild size="sm">
                            <Link href="/pricing">Optimasi Smart Pricing</Link>
                          </Button>
                          <Button asChild size="sm" variant="outline">
                            <Link href="/restock">Cek Smart Restock</Link>
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
      )}
    </>
  );
}