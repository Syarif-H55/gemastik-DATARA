import { PageHeader } from "@/components/page-header";
import { ChatPanel } from "@/components/assistant/chat-panel";

export default function AssistantPage() {
  return (
    // Tinggi dikunci setara viewport: 100svh dikurangi header app (h-14 = 3.5rem)
    // dan padding main (p-4/md:p-6/lg:p-8). PageHeader mengambil tinggi alaminya
    // di atas, sisanya diberikan ke ChatPanel (flex-1 + min-h-0) sehingga scroll
    // tetap terjadi di dalam area chat saja, bukan di halaman.
    <div className="flex min-h-[32rem] w-full flex-col h-[calc(100svh-5.5rem)] md:h-[calc(100svh-6.5rem)] lg:h-[calc(100svh-7.5rem)]">
      <PageHeader
        title="AI Business Assistant"
        description="Tanyakan hal apa pun tentang bisnis Anda — asisten menjelaskan hasil analisis dan rekomendasi DATARA."
      />
      <div className="flex min-h-0 flex-1 flex-col">
        <ChatPanel />
      </div>
    </div>
  );
}
