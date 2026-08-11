import { api } from "@/lib/api";
import type {
  AssistantConversation,
  AssistantMessage,
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

export function loginWithGoogle(idToken: string): Promise<LoginResponse> {
  return api.post<LoginResponse>("/auth/google", { id_token: idToken });
}

export function register(input: {
  name: string;
  email: string;
  password: string;
  business_name: string;
  business_type?: string;
}): Promise<LoginResponse> {
  return api.post<LoginResponse>("/auth/register", {
    name: input.name,
    email: input.email,
    password: input.password,
    business_name: input.business_name,
    business_type: input.business_type ?? "food_beverage",
  });
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

export function createProduct(input: {
  name: string;
  sku?: string;
  selling_price: number;
  unit?: string;
  current_stock?: number;
  low_stock_threshold?: number;
  hpp?: number;
}): Promise<Product> {
  return api.post<Product>("/products", {
    name: input.name,
    sku: input.sku ?? "",
    selling_price: input.selling_price,
    unit: input.unit ?? "unit",
    current_stock: input.current_stock ?? 0,
    low_stock_threshold: input.low_stock_threshold ?? 0,
    hpp: input.hpp,
  });
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

export interface AssistantChatResponse {
  conversation_id: number | null;
  message: string;
}

export function sendAssistantMessage(
  message: string,
  history: AssistantMessage[],
  conversationId: number | null = null
): Promise<AssistantChatResponse> {
  return api.post<AssistantChatResponse>("/ai/chat", {
    message,
    conversation_id: conversationId,
    history: history.map((m) => ({ role: m.role, content: m.content })),
  });
}

export function fetchAssistantConversations(): Promise<AssistantConversation[]> {
  return api.get<AssistantConversation[]>("/ai/conversations");
}

export function fetchAssistantMessages(
  conversationId: number
): Promise<{ id: number; title: string; messages: AssistantMessage[] }> {
  return api.get<{ id: number; title: string; messages: AssistantMessage[] }>(
    `/ai/conversations/${conversationId}`
  );
}
