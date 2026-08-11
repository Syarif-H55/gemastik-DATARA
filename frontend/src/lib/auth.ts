import type { User } from "@/lib/types";
import { clearToken, getToken, setToken } from "@/lib/api";

const USER_KEY = "datara_user";

export interface Session {
  user: User;
  access_token: string;
}

export function getSessionUser(): User | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as User) : null;
  } catch {
    return null;
  }
}

export function saveSession(session: Session): void {
  setToken(session.access_token);
  window.localStorage.setItem(USER_KEY, JSON.stringify(session.user));
}

export function clearSession(): void {
  clearToken();
  window.localStorage.removeItem(USER_KEY);
}

export function isAuthenticated(): boolean {
  return Boolean(getToken());
}
