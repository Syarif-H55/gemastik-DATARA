import type {
  DashboardMetrics,
  DecisionRecord,
  ForecastPoint,
  GrowthStage,
  InventoryLog,
  PricingRecommendation,
  Product,
  ProductClass,
  ProductForecast,
  ProductProfitability,
  RestockRecommendation,
  Transaction,
} from "@/lib/types";

const TARGET_MARGIN = 0.3;
const LEAD_TIME_DAYS = 3;

export const demoProducts: Product[] = [
  { id: 1, name: "Es Teh Manis", sku: "MIN-001", selling_price: 5000, hpp: 1500, stock: 12, low_stock_threshold: 10, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { id: 2, name: "Es Jeruk Peras", sku: "MIN-002", selling_price: 8000, hpp: 3200, stock: 4, low_stock_threshold: 10, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { id: 3, name: "Kopi Susu Gula Aren", sku: "MIN-003", selling_price: 15000, hpp: 6900, stock: 26, low_stock_threshold: 10, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { id: 4, name: "Ayam Geprek + Nasi", sku: "FOOD-001", selling_price: 18000, hpp: 10500, stock: 8, low_stock_threshold: 15, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { id: 5, name: "Nasi Goreng Spesial", sku: "FOOD-002", selling_price: 20000, hpp: 11800, stock: 18, low_stock_threshold: 15, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { id: 6, name: "Kentang Goreng", sku: "SNK-001", selling_price: 12000, hpp: 5200, stock: 35, low_stock_threshold: 20, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { id: 7, name: "Pisang Goreng Keju", sku: "SNK-002", selling_price: 10000, hpp: 4400, stock: 6, low_stock_threshold: 15, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { id: 8, name: "Air Mineral 600ml", sku: "MIN-004", selling_price: 4000, hpp: 2500, stock: 48, low_stock_threshold: 24, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
];

export const demoInventoryLogs: InventoryLog[] = [
  { id: 1, product_id: 2, product_name: "Es Jeruk Peras", movement_type: "sale", quantity: -6, stock_after: 4, note: "Penjualan siang", created_at: "2025-06-10T12:00:00" },
  { id: 2, product_id: 4, product_name: "Ayam Geprek + Nasi", movement_type: "sale", quantity: -7, stock_after: 8, note: "Penjualan makan siang", created_at: "2025-06-10T12:30:00" },
  { id: 3, product_id: 1, product_name: "Es Teh Manis", movement_type: "sale", quantity: -18, stock_after: 12, note: "Penjualan harian", created_at: "2025-06-10T13:00:00" },
  { id: 4, product_id: 7, product_name: "Pisang Goreng Keju", movement_type: "sale", quantity: -9, stock_after: 6, note: "Penjualan sore", created_at: "2025-06-10T16:00:00" },
  { id: 5, product_id: 3, product_name: "Kopi Susu Gula Aren", movement_type: "received", quantity: 30, stock_after: 26, note: "Terima dari supplier", created_at: "2025-06-08T09:00:00" },
  { id: 6, product_id: 6, product_name: "Kentang Goreng", movement_type: "adjustment", quantity: -3, stock_after: 35, note: "Stok rusak (basi)", created_at: "2025-06-07T10:00:00" },
  { id: 7, product_id: 3, product_name: "Kopi Susu Gula Aren", movement_type: "sale", quantity: -12, stock_after: 26, note: "Penjualan pagi", created_at: "2025-06-10T09:00:00" },
  { id: 8, product_id: 5, product_name: "Nasi Goreng Spesial", movement_type: "sale", quantity: -10, stock_after: 18, note: "Penjualan makan siang", created_at: "2025-06-10T12:00:00" },
  { id: 9, product_id: 6, product_name: "Kentang Goreng", movement_type: "sale", quantity: -10, stock_after: 35, note: "Penjualan sore", created_at: "2025-06-10T16:00:00" },
  { id: 10, product_id: 8, product_name: "Air Mineral 600ml", movement_type: "sale", quantity: -15, stock_after: 48, note: "Penjualan harian", created_at: "2025-06-10T17:00:00" },
];

export const demoTransactions: Transaction[] = [
  { id: 1, reference_number: "TRX-20250610-001", customer_name: "Andi", transaction_date: "2025-06-10T12:00:00", subtotal: 41000, discount: 0, total: 41000, items: [{ product_id: 2, quantity: 2, unit_price: 8000 }, { product_id: 4, quantity: 1, unit_price: 18000 }, { product_id: 1, quantity: 1, unit_price: 5000 }, { product_id: 3, quantity: 1, unit_price: 15000 }], created_at: "2025-06-10T12:00:00" },
  { id: 2, reference_number: "TRX-20250610-002", customer_name: "Budi", transaction_date: "2025-06-10T12:30:00", subtotal: 23000, discount: 1000, total: 22000, items: [{ product_id: 2, quantity: 1, unit_price: 8000 }, { product_id: 1, quantity: 1, unit_price: 5000 }, { product_id: 6, quantity: 1, unit_price: 12000 }], created_at: "2025-06-10T12:30:00" },
  { id: 3, reference_number: "TRX-20250610-003", customer_name: null, transaction_date: "2025-06-10T13:00:00", subtotal: 15000, discount: 0, total: 15000, items: [{ product_id: 3, quantity: 1, unit_price: 15000 }], created_at: "2025-06-10T13:00:00" },
  { id: 4, reference_number: "TRX-20250610-004", customer_name: "Cici", transaction_date: "2025-06-10T16:00:00", subtotal: 32000, discount: 0, total: 32000, items: [{ product_id: 7, quantity: 2, unit_price: 10000 }, { product_id: 1, quantity: 2, unit_price: 5000 }, { product_id: 2, quantity: 1, unit_price: 8000 }], created_at: "2025-06-10T16:00:00" },
];

export function getProductById(id: number): Product | undefined {
  return demoProducts.find((p) => p.id === id);
}

export function getProductProfitability(): ProductProfitability[] {
  return demoProducts.map((p) => {
    const qtySold = demoInventoryLogs
      .filter((l) => l.product_id === p.id && l.movement_type === "sale")
      .reduce((sum, l) => sum + Math.abs(l.quantity), 0);
    const totalRevenue = qtySold * p.selling_price;
    const totalCost = qtySold * p.hpp;
    const unitProfit = p.selling_price - p.hpp;
    return {
      product_id: p.id,
      name: p.name,
      sku: p.sku,
      selling_price: p.selling_price,
      hpp: p.hpp,
      unit_profit: unitProfit,
      margin_percent: p.selling_price > 0 ? (unitProfit / p.selling_price) * 100 : 0,
      qty_sold: qtySold,
      total_revenue: totalRevenue,
      total_cost: totalCost,
      total_profit: totalRevenue - totalCost,
    };
  });
}

export function getPricingRecommendations(targetMarginPercent = TARGET_MARGIN * 100): PricingRecommendation[] {
  return demoProducts.map((p) => {
    const costBasedPrice = p.hpp / (1 - targetMarginPercent / 100);
    const recommendedPrice = Math.ceil(costBasedPrice / 500) * 500;
    const actualMargin = p.selling_price > 0 ? ((p.selling_price - p.hpp) / p.selling_price) * 100 : 0;
    const needIncrease = recommendedPrice > p.selling_price;
    const reasoning = needIncrease
      ? `HPP Rp ${p.hpp.toLocaleString("id-ID")} membuat margin aktual ${actualMargin.toFixed(0)}% di bawah target ${targetMarginPercent}%. Naikkan harga ke Rp ${recommendedPrice.toLocaleString("id-ID")} untuk mencapai margin ~${targetMarginPercent}%.`
      : `Harga saat ini sudah menghasilkan margin ${actualMargin.toFixed(0)}% (target ${targetMarginPercent}%). Tidak perlu perubahan harga.`;
    return {
      id: p.id,
      product_id: p.id,
      name: p.name,
      sku: p.sku,
      current_price: p.selling_price,
      recommended_price: recommendedPrice,
      hpp: p.hpp,
      target_margin_percent: targetMarginPercent,
      actual_margin_percent: actualMargin,
      reasoning,
    };
  });
}

export function getRestockRecommendations(leadTimeDays = LEAD_TIME_DAYS): RestockRecommendation[] {
  const forecasts = new Map(getProductForecasts().map((f) => [f.product_id, f]));
  return demoProducts.map((p) => {
    const forecast = forecasts.get(p.id);
    const avgDailySold = forecast ? Math.max(1, forecast.predicted_units) : Math.max(1, Math.round(p.stock * 0.35));
    const daysOfSupply = avgDailySold > 0 ? p.stock / avgDailySold : 999;
    const suggestedQuantity = Math.max(0, (avgDailySold * leadTimeDays) - p.stock + p.low_stock_threshold);
    let urgency: RestockRecommendation["urgency"] = "healthy";
    if (p.stock <= p.low_stock_threshold) urgency = "critical";
    else if (daysOfSupply <= leadTimeDays + 2) urgency = "low";

    const basis = forecast ? `Forecast ${avgDailySold} unit/hari` : `Rata-rata ${avgDailySold} unit/hari`;
    const reasoning =
      urgency === "critical"
        ? `Stok tersisa ${p.stock} (di bawah ambang ${p.low_stock_threshold}). ${basis}, diperkirakan habis dalam ~${daysOfSupply.toFixed(0)} hari. Segera restock ${suggestedQuantity} unit.`
        : urgency === "low"
          ? `Stok ${p.stock} masih cukup tapi mendekati ambang. ${basis}, restock ${suggestedQuantity} unit dalam ${leadTimeDays} hari ke depan agar tidak kehabisan.`
          : `Stok ${p.stock} sehat dengan ${basis}, cukup untuk ~${daysOfSupply.toFixed(0)} hari. Belum perlu restock.`;

    return {
      id: p.id,
      product_id: p.id,
      name: p.name,
      sku: p.sku,
      current_stock: p.stock,
      low_stock_threshold: p.low_stock_threshold,
      days_of_supply: daysOfSupply,
      suggested_quantity: suggestedQuantity,
      urgency,
      reasoning,
    };
  });
}

export function getDashboardMetrics(): DashboardMetrics {
  const profitability = getProductProfitability();
  const totalRevenue = profitability.reduce((s, p) => s + p.total_revenue, 0);
  const totalCogs = profitability.reduce((s, p) => s + p.total_cost, 0);
  const totalProfit = profitability.reduce((s, p) => s + p.total_profit, 0);
  const avgMargin = totalRevenue > 0 ? (totalProfit / totalRevenue) * 100 : 0;
  const transactionsCount = demoTransactions.length;
  const productsSold = profitability.filter((p) => p.qty_sold > 0).length;

  const revenueTrend = [
    { date: "2025-06-04", revenue: 182000, profit: 62400 },
    { date: "2025-06-05", revenue: 215000, profit: 73800 },
    { date: "2025-06-06", revenue: 168000, profit: 55100 },
    { date: "2025-06-07", revenue: 249000, profit: 84200 },
    { date: "2025-06-08", revenue: 274000, profit: 94800 },
    { date: "2025-06-09", revenue: 231000, profit: 78100 },
    { date: "2025-06-10", revenue: 111000, profit: 38900 },
  ];

  const categoryBreakdown = [
    { name: "Makanan", value: profitability.filter((p) => p.sku.startsWith("FOOD")).reduce((s, p) => s + p.total_revenue, 0) },
    { name: "Minuman", value: profitability.filter((p) => p.sku.startsWith("MIN")).reduce((s, p) => s + p.total_revenue, 0) },
    { name: "Camilan", value: profitability.filter((p) => p.sku.startsWith("SNK")).reduce((s, p) => s + p.total_revenue, 0) },
  ];

  const rawScore = Math.round(40 + avgMargin + (productsSold / demoProducts.length) * 20);
  const score = Math.min(100, Math.max(0, rawScore));

  return {
    total_revenue: totalRevenue,
    total_profit: totalProfit,
    total_cogs: totalCogs,
    avg_margin_percent: avgMargin,
    transactions_count: transactionsCount,
    products_sold: productsSold,
    business_health: {
      score,
      label: score >= 75 ? "Sehat" : score >= 50 ? "Cukup" : "Perlu Perhatian",
    },
    revenue_trend: revenueTrend,
    category_breakdown: categoryBreakdown,
  };
}

const FORECAST_SERIES: Record<number, { trend: "up" | "down" | "flat"; base: number }> = {
  1: { trend: "flat", base: 18 },
  2: { trend: "up", base: 6 },
  3: { trend: "up", base: 12 },
  4: { trend: "up", base: 14 },
  5: { trend: "flat", base: 10 },
  6: { trend: "up", base: 9 },
  7: { trend: "down", base: 11 },
  8: { trend: "flat", base: 20 },
};

function buildForecastSeries(base: number, trend: "up" | "down" | "flat"): ForecastPoint[] {
  const points: ForecastPoint[] = [];
  const drift = trend === "up" ? 1.6 : trend === "down" ? -1.1 : 0.2;
  for (let i = 6; i >= 0; i--) {
    const wave = Math.round(Math.sin(i / 1.7) * 2.5);
    const level = base + (6 - i) * drift;
    const actual = Math.max(1, Math.round(level + wave));
    const forecast = Math.max(1, Math.round(level + 1));
    points.push({
      period: `2025-06-${10 - i}`,
      actual: i > 0 ? actual : 0,
      forecast,
      lower: Math.max(0, forecast - 3),
      upper: forecast + 3,
    });
  }
  return points;
}

export function getProductForecasts(): ProductForecast[] {
  return demoProducts.map((p) => {
    const cfg = FORECAST_SERIES[p.id] ?? { trend: "flat", base: 10 };
    const points = buildForecastSeries(cfg.base, cfg.trend);
    const predicted = points[points.length - 1].forecast;
    const confidence = cfg.trend === "flat" ? 88 : 76;
    const method =
      cfg.trend === "flat"
        ? "Moving Average (7 hari)"
        : "Simple Exponential Smoothing";
    const reasoning =
      cfg.trend === "up"
        ? `Riwayat penjualan ${p.name} 7 hari terakhir menunjukkan tren naik (rata-rata ${cfg.base} unit/hari). Prediksi ${predicted} unit untuk periode berikutnya dengan kepercayaan ${confidence}%.`
        : cfg.trend === "down"
          ? `Riwayat penjualan ${p.name} menunjukkan tren menurun. Prediksi ${predicted} unit; pertimbangkan evaluasi stok untuk menghindari penumpukan.`
          : `Penjualan ${p.name} stabil di sekitar ${cfg.base} unit/hari. Prediksi ${predicted} unit untuk periode berikutnya.`;
    return {
      product_id: p.id,
      name: p.name,
      sku: p.sku,
      model: cfg.trend === "flat" ? "moving-average" : "linear-trend",
      method,
      next_period: "2025-06-11",
      predicted_units: predicted,
      confidence,
      trend: cfg.trend,
      points,
      reasoning,
    };
  });
}

export function getProductClass(p: ProductProfitability): { classification: ProductClass; label: string; reason: string } {
  const goodMargin = p.margin_percent >= 35;
  const poorMargin = p.margin_percent < 20;
  const highSales = p.qty_sold >= 10;
  const lowSales = p.qty_sold < 4;

  if (highSales && goodMargin) {
    return {
      classification: "profitable",
      label: "Menguntungkan",
      reason: "Volume penjualan tinggi dan margin sehat — pertahankan strategi harga serta stok.",
    };
  }
  if (lowSales && goodMargin) {
    return {
      classification: "potential",
      label: "Berpotensi",
      reason: "Margin tinggi tetapi penjualan rendah. Dorong permintaan lewat promosi atau visibilitas menu.",
    };
  }
  if (highSales && poorMargin) {
    return {
      classification: "evaluate",
      label: "Perlu Evaluasi",
      reason: "Penjualan cukup tetapi margin tipis — tinjau HPP atau harga jual.",
    };
  }
  return {
    classification: "evaluate",
    label: "Perlu Evaluasi",
    reason: "Kombinasi penjualan dan margin belum ideal. Tinjau harga, HPP, dan pemasaran.",
  };
}

export const demoDecisions: DecisionRecord[] = [
  {
    id: 1,
    type: "pricing",
    product_id: 1,
    product_name: "Es Teh Manis",
    title: "Naikkan harga Es Teh Manis",
    summary: "Harga disesuaikan dari Rp 4.000 → Rp 5.000 untuk menutup HPP dan target margin.",
    reasoning: "Margin aktual di bawah target 30%. HPP Rp 1.500 membuat harga lama belum optimal.",
    applied_at: "2025-05-20",
    metrics_before: { revenue: 180000, margin: 55, stock: 40 },
    metrics_after: { revenue: 198000, margin: 68, stock: 35 },
    status: "improved",
    outcome_notes: "Omzet naik dan margin membaik tanpa penurunan volume signifikan.",
  },
  {
    id: 2,
    type: "restock",
    product_id: 3,
    product_name: "Kopi Susu Gula Aren",
    title: "Restock Kopi Susu Gula Aren",
    summary: "Penambahan stok 30 unit mengikuti forecast kenaikan permintaan.",
    reasoning: "Tren penjualan naik; stok diperkirakan habis dalam 4 hari.",
    applied_at: "2025-06-05",
    metrics_before: { revenue: 210000, margin: 54, stock: 26 },
    metrics_after: { revenue: 232000, margin: 58, stock: 41 },
    status: "improved",
    outcome_notes: "Tidak ada kehabisan stok; penjualan tetap berjalan lancar.",
  },
  {
    id: 3,
    type: "pricing",
    product_id: 5,
    product_name: "Nasi Goreng Spesial",
    title: "Harga Nasi Goreng dinaikkan",
    summary: "Penyesuaian harga mengikuti perubahan HPP bahan baku.",
    reasoning: "HPP naik, margin aktual turun mendekati batas minimum.",
    applied_at: "2025-06-08",
    metrics_before: { revenue: 205000, margin: 41, stock: 20 },
    metrics_after: { revenue: 197000, margin: 45, stock: 22 },
    status: "regressed",
    outcome_notes: "Volume turun sedikit; pantau 2 minggu ke depan sebelum evaluasi lanjutan.",
  },
];

export function getGrowthStages(): GrowthStage[] {
  return [
    {
      id: 1,
      label: "Catat & Konsisten",
      description: "Pencatatan transaksi dan biaya berjalan rutin setiap hari.",
      status: "done",
      metric_1: "Transaksi/minggu",
      metric_1_value: 35,
      metric_1_target: 20,
      next_step: "Lanjutkan rutinitas pencatatan harian.",
    },
    {
      id: 2,
      label: "Pahami Profitabilitas",
      description: "Semua produk memiliki HPP dan margin yang terhitung.",
      status: "done",
      metric_1: "Produk terpantau",
      metric_1_value: 8,
      metric_1_target: 8,
      next_step: "Review produk dengan margin rendah.",
    },
    {
      id: 3,
      label: "Keputusan Berbasis Data",
      description: "Menerapkan rekomendasi pricing & restock secara rutin.",
      status: "current",
      metric_1: "Keputusan diterapkan",
      metric_1_value: 2,
      metric_1_target: 5,
      next_step: "Terapkan 3 rekomendasi lain dari Smart Pricing/Restock.",
    },
    {
      id: 4,
      label: "Perluas Menuju Pertumbuhan",
      description: "Evaluasi perkembangan indikator dan siap ekspansi liniteman/menu.",
      status: "upcoming",
      metric_1: "Omzet bulanan",
      metric_1_value: 0,
      metric_1_target: 12000000,
      next_step: "Capai target omzet bulanan sebelum menambah outlet.",
    },
  ];
}