"use client";

import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { ChatCircle, CircleNotch, PaperPlaneTilt, Plus, Robot, Sparkle } from "@phosphor-icons/react";
import { cn } from "@/lib/utils";
import { formatDateTime } from "@/lib/format";
import type { AssistantConversation, AssistantMessage } from "@/lib/types";
import { fetchAssistantConversations, fetchAssistantMessages, sendAssistantMessage } from "@/lib/datara";

const SUGGESTIONS = [
  "Bagaimana kesehatan bisnis saya?",
  "Produk mana yang perlu segera direstock?",
  "Berapa harga jual yang disarankan?",
  "Bagaimana prediksi penjualan bulan depan?",
];

const WELCOME_MESSAGE: AssistantMessage = {
  id: 0,
  role: "assistant",
  content:
    "Halo! Saya asisten bisnis DATARA. Tanyakan hal apa pun tentang kesehatan bisnis, profitabilitas produk, harga, stok, atau prediksi penjualan Anda.",
  created_at: "",
};

export function ChatPanel() {
  const [conversations, setConversations] = React.useState<AssistantConversation[]>([]);
  const [activeId, setActiveId] = React.useState<number | null>(null);
  const [messages, setMessages] = React.useState<AssistantMessage[]>([WELCOME_MESSAGE]);
  const [input, setInput] = React.useState("");
  const [loading, setLoading] = React.useState(true);
  const [sending, setSending] = React.useState(false);
  const nextId = React.useRef(1);
  const endRef = React.useRef<HTMLDivElement>(null);

  const refreshConversations = React.useCallback(async () => {
    try {
      setConversations(await fetchAssistantConversations());
    } catch {
      // List percakapan gagal dimuat — biarkan state apa adanya.
    }
  }, []);

  const openConversation = React.useCallback(async (conversationId: number) => {
    setLoading(true);
    try {
      const data = await fetchAssistantMessages(conversationId);
      setActiveId(conversationId);
      setMessages(data.messages.length > 0 ? data.messages : [WELCOME_MESSAGE]);
    } catch {
      // Percakapan tidak bisa dimuat — kembali ke welcome.
      setActiveId(null);
      setMessages([WELCOME_MESSAGE]);
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const list = await fetchAssistantConversations();
        if (cancelled) return;
        setConversations(list);
        if (list.length > 0) {
          const data = await fetchAssistantMessages(list[0].id);
          if (cancelled) return;
          setActiveId(list[0].id);
          setMessages(data.messages.length > 0 ? data.messages : [WELCOME_MESSAGE]);
        }
      } catch {
        // Riwayat gagal dimuat — mulai dari welcome message.
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  React.useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, sending]);

  const startNewChat = () => {
    setActiveId(null);
    setMessages([WELCOME_MESSAGE]);
  };

  const sendMessage = async () => {
    const prompt = input.trim();
    if (!prompt || sending) return;

    const userMessage: AssistantMessage = {
      id: -(nextId.current++),
      role: "user",
      content: prompt,
      created_at: "",
    };
    const historyForApi = messages.filter((m) => m.id !== 0);
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setSending(true);

    try {
      let reply: AssistantMessage;
      try {
        const response = await sendAssistantMessage(prompt, historyForApi, activeId);
        const newConversationId = response.conversation_id;
        if (newConversationId !== null) {
          setActiveId(newConversationId);
          const title = prompt.slice(0, 60);
          setConversations((prev) => {
            const exists = prev.some((c) => c.id === newConversationId);
            const list = exists
              ? prev.map((c) =>
                  c.id === newConversationId
                    ? { ...c, title, updated_at: new Date().toISOString() }
                    : c
                )
              : [{ id: newConversationId, title, updated_at: null }, ...prev];
            return [...list].sort((a, b) => (b.updated_at ?? "").localeCompare(a.updated_at ?? ""));
          });
        }
        reply = {
          id: -(nextId.current++),
          role: "assistant",
          content: response.message,
          created_at: "",
        };
      } catch {
        // Layanan AI belum aktif (mis. GEMINI_API_KEY belum diisi) — pakai
        // balasan simulasi sebagai fallback.
        await new Promise((resolve) => setTimeout(resolve, 900));
        reply = {
          id: -(nextId.current++),
          role: "assistant",
          content: `Terima kasih atas pertanyaan Anda: "${prompt}". Asisten AI sedang belum aktif — isi GEMINI_API_KEY di backend/.env lalu mulai ulang server untuk mengaktifkannya.`,
          created_at: "",
        };
      }
      setMessages((prev) => [...prev, reply]);
      refreshConversations();
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="flex h-full min-h-0 min-w-0">
      {/* Panel riwayat percakapan — desktop */}
      <aside className="hidden w-72 shrink-0 flex-col border-r border-border md:flex">
        <div className="flex items-center justify-between px-4 pb-2 pt-4">
          <h2 className="text-sm font-medium text-muted-foreground">Riwayat</h2>
        </div>
        <div className="flex-1 space-y-1 overflow-y-auto px-3 pb-4">
          <Button
            type="button"
            variant={activeId === null ? "default" : "outline"}
            size="sm"
            className="mb-2 w-full justify-start gap-2"
            onClick={startNewChat}
          >
            <Plus className="size-4" />
            Percakapan baru
          </Button>
          {conversations.length === 0 ? (
            <p className="px-2 py-3 text-xs text-muted-foreground">Belum ada percakapan.</p>
          ) : (
            conversations.map((c) => (
              <Button
                key={c.id}
                type="button"
                variant={activeId === c.id ? "default" : "ghost"}
                size="sm"
                className="w-full justify-start gap-2 text-left"
                onClick={() => openConversation(c.id)}
                title={c.title}
              >
                <ChatCircle className="size-4 shrink-0" />
                <span className="truncate">{c.title}</span>
              </Button>
            ))
          )}
        </div>
      </aside>

      {/* Area chat utama */}
      <Card className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <CardHeader className="border-b px-4 py-4 md:px-8 lg:px-12">
          <CardTitle className="flex items-center gap-2 text-base">
            <span className="flex size-7 items-center justify-center rounded-full bg-primary text-primary-foreground">
              <Robot className="size-4" />
            </span>
            AI Business Assistant
          </CardTitle>
          <div className="mt-1 md:hidden">
            <Select
              value={activeId === null ? "new" : String(activeId)}
              onValueChange={(v) =>
                v === "new" ? startNewChat() : openConversation(Number(v))
              }
            >
              <SelectTrigger className="h-9 w-full">
                <span className="text-sm font-medium">Riwayat Chat</span>
              </SelectTrigger>
              <SelectContent position="popper" side="bottom" sideOffset={4} collisionPadding={16}>
                <SelectItem value="new">Percakapan baru</SelectItem>
                {conversations.map((c) => (
                  <SelectItem key={c.id} value={String(c.id)}>
                    {c.title}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardHeader>

        <CardContent className="flex min-h-0 flex-1 flex-col p-0">
          <div className="flex-1 space-y-4 overflow-y-auto px-4 py-5 md:px-8 lg:px-12">
            {loading ? (
              <div className="flex h-full items-center justify-center text-muted-foreground">
                <CircleNotch className="size-5 animate-spin" />
              </div>
            ) : (
              messages.map((m) =>
                m.role === "user" ? (
                  <div key={m.id} className="flex flex-col items-end">
                    <div className="max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-br-md bg-primary px-3 py-2 text-sm text-primary-foreground md:max-w-[75%] lg:max-w-[60%]">
                      {m.content}
                    </div>
                    {m.created_at ? (
                      <span className="mt-1 text-[10px] text-muted-foreground/70">
                        {formatDateTime(m.created_at)}
                      </span>
                    ) : null}
                  </div>
                ) : (
                  <div key={m.id} className="flex items-start gap-2">
                    <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-muted">
                      <Robot className="size-4" />
                    </span>
                    <div className="flex flex-col items-start">
                      <div className="max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-bl-md border bg-muted/50 px-3 py-2 text-sm md:max-w-[75%] lg:max-w-[60%]">
                        {m.content}
                      </div>
                      {m.created_at ? (
                        <span className="mt-1 text-[10px] text-muted-foreground/70">
                          {formatDateTime(m.created_at)}
                        </span>
                      ) : null}
                    </div>
                  </div>
                )
              )
            )}

            {sending && (
              <div className="flex items-start gap-2">
                <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-muted">
                  <Robot className="size-4" />
                </span>
                <div className="flex items-center gap-2 rounded-lg border bg-muted/50 px-3 py-2 text-sm text-muted-foreground">
                  <CircleNotch className="size-4 animate-spin" />
                  Sedang mengetik…
                </div>
              </div>
            )}
            <div ref={endRef} />
          </div>

          {/* Area input — menempel di dasar panel */}
          <div className="space-y-3 border-t px-4 pb-5 pt-3 md:px-8 lg:px-12">
            <div className="flex flex-wrap gap-2">
              {SUGGESTIONS.map((s) => (
                <Button
                  key={s}
                  type="button"
                  size="sm"
                  variant="outline"
                  disabled={sending}
                  onClick={() => setInput(s)}
                  className="h-auto rounded-full px-3 py-1 text-xs"
                >
                  <Sparkle className="size-3" />
                  {s}
                </Button>
              ))}
            </div>
            <div className="flex items-end gap-2">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                placeholder="Tanyakan sesuatu tentang bisnis Anda… (Enter untuk kirim, Shift+Enter untuk baris baru)"
                className={cn("min-h-11 max-h-40 flex-1 resize-none")}
                disabled={sending}
              />
              <Button onClick={sendMessage} disabled={sending || !input.trim()} className="shrink-0">
                <PaperPlaneTilt className="size-4" />
                Kirim
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
