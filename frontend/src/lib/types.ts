export type Role = "owner" | "staff";

export interface User {
  id: number;
  name: string;
  email: string;
  role: Role;
}

export type ProductMovementType = "received" | "issued" | "adjustment" | "sale";

export interface Product {
  id: number;
  name: string;
  sku: string;
  selling_price: number;
  hpp: number;
  stock: number;
  low_stock_threshold: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductProfitability {
  product_id: number;
  name: string;
  sku: string;
  selling_price: number;
  hpp: number;
  unit_profit: number;
  margin_percent: number;
  qty_sold: number;
  total_revenue: number;
  total_cost: number;
  total_profit: number;
}

export interface InventoryLog {
  id: number;
  product_id: number;
  product_name?: string;
  movement_type: ProductMovementType;
  quantity: number;
  stock_after: number;
  note: string | null;
  created_at: string;
}

export interface TransactionItem {
  product_id: number;
  quantity: number;
  unit_price: number;
}

export interface Transaction {
  id: number;
  reference_number: string;
  customer_name: string | null;
  transaction_date: string;
  subtotal: number;
  discount: number;
  total: number;
  items: TransactionItem[];
  created_at: string;
}

export interface Cost {
  id: number;
  name: string;
  amount: number;
  category: string;
  occurs_at: string;
  notes: string | null;
  created_at: string;
}

export type DecisionType = "pricing" | "restock";
export type DecisionStatus = "recommended" | "applied" | "dismissed";

export interface Decision {
  id: number;
  type: DecisionType;
  title: string;
  explanation: string;
  payload: Record<string, unknown>;
  status: DecisionStatus;
  created_at: string;
}

export interface PricingRecommendation {
  product_id: number;
  name: string;
  sku: string;
  current_price: number;
  recommended_price: number;
  hpp: number;
  target_margin_percent: number;
  actual_margin_percent: number;
  reasoning: string;
}

export interface RestockRecommendation {
  product_id: number;
  name: string;
  sku: string;
  current_stock: number;
  low_stock_threshold: number;
  days_of_supply: number;
  suggested_quantity: number;
  urgency: "critical" | "low" | "healthy";
  reasoning: string;
}

export interface BusinessHealth {
  score: number;
  label: string;
}

export interface DashboardMetrics {
  total_revenue: number;
  total_profit: number;
  total_cogs: number;
  avg_margin_percent: number;
  transactions_count: number;
  products_sold: number;
  business_health: BusinessHealth;
  revenue_trend: { date: string; revenue: number; profit: number }[];
  category_breakdown: { name: string; value: number }[];
}

export interface ForecastPoint {
  period: string;
  actual: number;
  forecast: number;
  lower?: number;
  upper?: number;
}

export interface ProductForecast {
  product_id: number;
  name: string;
  sku: string;
  model: string;
  method: string;
  next_period: string;
  predicted_units: number;
  confidence: number;
  trend: "up" | "down" | "flat";
  points: ForecastPoint[];
  reasoning: string;
}

export type ProductClass = "profitable" | "potential" | "evaluate";

export interface DecisionRecord {
  id: number;
  type: DecisionType;
  title: string;
  summary: string;
  reasoning: string;
  applied_at: string;
  metrics_before: { revenue: number; margin: number; stock: number };
  metrics_after: { revenue: number; margin: number; stock: number };
  status: "improved" | "flat" | "regressed";
  outcome_notes: string;
}

export interface GrowthStage {
  id: number;
  label: string;
  description: string;
  status: "done" | "current" | "next" | "upcoming";
  metric_1: string;
  metric_1_value: number;
  metric_1_target: number;
  next_step: string;
}