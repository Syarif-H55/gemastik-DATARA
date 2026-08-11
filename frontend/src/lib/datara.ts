import { api } from "@/lib/api";
import type {
  DashboardMetrics,
  DecisionRecord,
  GrowthStage,
  PricingRecommendation,
  Product,
  ProductForecast,
  ProductProfitability,
  RestockRecommendation,
  Transaction,
  User,
} from "@/lib/types";

export interface LoginResponse {
  user: User;
  access_token: string;
}

export interface GrowthMap {
  current_stage: string | null;
  stages: GrowthStage[];
}

export interface TransactionItemInput {
  product_id: number;
  quantity: number;
}

export function login(email: string, password: string): Promise<LoginResponse> {
  return api.post<LoginResponse>("/auth/login", { email, password });
}

export function fetchMe(): Promise<User> {
  return api.get<User>("/auth/me");
}

export function fetchBusiness() {
  return api.get<{ id: number; name: string; business_type: string; safety_days: number }>("/business");
}

export function fetchDashboard(): Promise<DashboardMetrics> {
  return api.get<DashboardMetrics>("/dashboard");
}

export function fetchProducts(): Promise<Product[]> {
  return api.get<Product[]>("/products");
}

export function fetchProductProfitability(): Promise<ProductProfitability[]> {
  return api.get<ProductProfitability[]>("/products/profitability");
}

export function fetchForecasts(): Promise<ProductForecast[]> {
  return api.get<ProductForecast[]>("/forecasting/products");
}

export function fetchPricingRecommendations(targetMarginPercent: number): Promise<PricingRecommendation[]> {
  return api.get<PricingRecommendation[]>(`/pricing/recommendations?target_margin=${targetMarginPercent}`);
}

export function applyPricingRecommendation(recommendationId: number) {
  return api.post("/pricing/apply", { recommendation_id: recommendationId });
}

export function fetchRestockRecommendations(): Promise<RestockRecommendation[]> {
  return api.get<RestockRecommendation[]>("/restock/recommendations");
}

export function applyRestockRecommendation(recommendationId: number) {
  return api.post("/restock/apply", { recommendation_id: recommendationId });
}

export function fetchDecisions(): Promise<DecisionRecord[]> {
  return api.get<DecisionRecord[]>("/decisions");
}

export function fetchGrowth(): Promise<GrowthMap> {
  return api.get<GrowthMap>("/growth");
}

export function createTransaction(
  items: TransactionItemInput[],
  opts?: { customer_name?: string; discount?: number }
): Promise<Transaction> {
  return api.post<Transaction>("/transactions", {
    customer_name: opts?.customer_name || null,
    discount: opts?.discount || 0,
    items: items.map((i) => ({ product_id: i.product_id, quantity: i.quantity })),
  });
}
