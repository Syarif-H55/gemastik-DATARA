"""Business Assistant service: context builder + LLM chat (API Contract bab 18).

Backend adalah source of truth: context disusun dari data bisnis aktual
(finansial, kesehatan, stok, profitabilitas, dan evaluasi harga per produk),
diubah menjadi teks terstruktur, lalu disuntikkan sebagai system instruction
di urutan paling pertama sebelum riwayat chat dikirim ke LLM.

LLM hanya menjelaskan/menyarankan berdasarkan context — tidak mengarang angka,
tidak mengklaim tindakan bisnis, dan tidak menyentuh database.

Percakapan dan pesan dipersistkan ke `ai_conversations` / `ai_messages`
sehingga riwayat chat tidak hilang saat halaman di-refresh.
"""
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.ai_conversation import AIConversation, AIMessage
from app.models.business import Business
from app.models.enums import ConversationStatus, MessageRole
from app.repositories import product_repository, recommendation_repository
from app.schemas.assistant import AssistantChatRequest
from app.services import (
    analytics_service,
    catalog_service,
    llm_service,
    pricing_service,
    restock_service,
)

_MAX_HISTORY = 12
_TITLE_LIMIT = 60

_EVAL_STATUS_LABEL = {
    "margin_below_target": "PERLU EVALUASI",
    "already_healthy": "SUDAH BAIK",
    "incomplete_hpp": "HPP BELUM LENGKAP",
}


def _rupiah(value: float) -> str:
    """Format Rupiah ala Indonesia: 12.500 (titik sebagai pemisah ribuan)."""
    return f"Rp {int(round(value or 0)):,}".replace(",", ".")


def _restock_config(db: Session, business: Business) -> tuple[float, float]:
    config = recommendation_repository.get_configuration(db, business.id)
    return (
        float(config.safety_days) if config else 3.0,
        float(config.lead_time) if config else 3.0,
    )


def build_business_context(db: Session, business: Business) -> dict:
    """Kumpulkan data bisnis aktual (semua produk + evaluasi harga).

    Mencakup data yang sama dengan halaman Product Profitability (HPP, harga
    jual, margin aktual, qty terjual, laba) dan Smart Pricing (status evaluasi:
    PERLU EVALUASI / SUDAH BAIK / HPP BELUM LENGKAP beserta alasannya).
    """
    financial = analytics_service.finance_summary(db, business)
    health = analytics_service.business_health(db, business)

    config = recommendation_repository.get_configuration(db, business.id)
    target_margin = float(config.target_margin) if config else 30.0

    profitability = catalog_service.get_profitability(db, business)
    profitability_by_id = {p["product_id"]: p for p in profitability}

    products: list[dict] = []
    for product in product_repository.list_by_business(db, business.id):
        if not product.is_active:
            continue
        profit = profitability_by_id.get(product.id, {})
        evaluation = pricing_service.build_recommendation(db, product, target_margin)
        products.append(
            {
                "name": product.name,
                "hpp": evaluation["hpp"],
                "selling_price": evaluation["current_price"],
                "margin_percent": evaluation["actual_margin_percent"],
                "qty_sold": profit.get("qty_sold", 0),
                "total_profit": profit.get("total_profit", 0),
                "target_margin_percent": target_margin,
                "evaluation": {
                    "status": _EVAL_STATUS_LABEL.get(
                        evaluation["reason_code"], evaluation["reason_code"]
                    ),
                    "reason": evaluation["reasoning"],
                },
            }
        )

    safety_days, lead_time = _restock_config(db, business)
    restock = restock_service.recommendations(db, business, safety_days, lead_time)
    critical = [r for r in restock if r.get("urgency") == "critical"]

    return {
        "business": {"name": business.name, "business_type": business.business_type},
        "financial": financial,
        "health": {"status": health["status"], "score": health["score"], "label": health["label"]},
        "target_margin": target_margin,
        "products": products,
        "inventory": {
            "high_risk_products": len(critical),
            "critical_products": [
                {
                    "name": r["name"],
                    "current_stock": r["current_stock"],
                    "suggested_quantity": r["suggested_quantity"],
                }
                for r in critical[:5]
            ],
        },
    }


def build_business_context_text(context: dict) -> str:
    """Ubah context dict menjadi teks ringkas yang mudah dibaca LLM."""
    lines: list[str] = []

    business = context.get("business", {})
    lines.append(
        f"Bisnis: {business.get('name', '-')} "
        f"(tipe: {business.get('business_type', '-')})"
    )

    financial = context.get("financial", {})
    lines.append("=== Ringkasan Finansial (30 hari terakhir) ===")
    lines.append(f"- Pendapatan: {_rupiah(financial.get('revenue', 0))}")
    lines.append(f"- HPP terjual: {_rupiah(financial.get('cogs', 0))}")
    lines.append(
        f"- Laba kotor: {_rupiah(financial.get('gross_profit', 0))} "
        f"({financial.get('gross_margin', 0):.1f}%)"
    )
    lines.append(f"- Beban operasional: {_rupiah(financial.get('operating_expense', 0))}")
    lines.append(f"- Laba bersih: {_rupiah(financial.get('net_profit', 0))}")

    health = context.get("health", {})
    lines.append(
        f"Kesehatan bisnis: {health.get('status', '-')} "
        f"(skor {health.get('score', 0):.0f})"
    )

    target_margin = context.get("target_margin", 30)
    products = context.get("products", [])
    lines.append(f"=== Daftar Produk Saat Ini (target margin {target_margin:.0f}%) ===")
    if not products:
        lines.append("- (belum ada produk)")
    for index, product in enumerate(products, start=1):
        evaluation = product.get("evaluation", {})
        lines.append(
            f"{index}. {product['name']} — HPP: {_rupiah(product['hpp'])}; "
            f"Harga Jual: {_rupiah(product['selling_price'])}; "
            f"Margin Aktual: {product['margin_percent']:.1f}%; "
            f"Terjual {product['qty_sold']:.0f} unit (Laba: {_rupiah(product['total_profit'])}). "
            f"Status: {evaluation.get('status', '-')} — {evaluation.get('reason', '-')}"
        )

    inventory = context.get("inventory", {})
    critical = inventory.get("critical_products", [])
    if critical:
        lines.append("=== Stok Kritis (perlu segera restock) ===")
        for item in critical:
            lines.append(
                f"- {item['name']}: sisa {item['current_stock']:.0f} unit, "
                f"disarankan restock {item['suggested_quantity']:.0f} unit"
            )

    return "\n".join(lines)


def _build_system_prompt(context: dict) -> str:
    data_text = build_business_context_text(context)
    return (
        "Anda adalah Asisten Bisnis AI DATARA — asisten untuk pemilik UMKM "
        "Food & Beverage skala mikro.\n"
        "Jawab pertanyaan pengguna berdasarkan data bisnis real-time berikut:\n"
        f"{data_text}\n\n"
        "Aturan:\n"
        "- Jawab dalam bahasa Indonesia yang sederhana dan ringkas (maksimal ~180 kata).\n"
        "- Gunakan HANYA data pada daftar di atas. Jangan mengarang, menebak, "
        "atau menghitung angka baru di luar data tersebut.\n"
        "- Jika data yang dibutuhkan tidak tersedia, nyatakan keterbatasan itu.\n"
        "- Jangan mengklaim telah melakukan tindakan bisnis (restock, ubah harga, dll) — "
        "DATARA hanya memberi rekomendasi; keputusan diterapkan pemilik.\n"
        "- Jangan mengubah rekomendasi yang sudah dihasilkan sistem.\n"
        "- Berikan alasan singkat sebelum saran bila relevan.\n"
        "- Di luar konteks bisnis, tolak dengan sopan.\n"
    )


def _get_owned_conversation(db: Session, business: Business, conversation_id: int) -> AIConversation:
    conversation = db.get(AIConversation, conversation_id)
    if conversation is None or conversation.business_id != business.id:
        raise NotFoundError("Percakapan tidak ditemukan.")
    return conversation


def _messages_to_history(conversation: AIConversation) -> list[dict]:
    ordered = sorted(conversation.messages, key=lambda m: m.id)
    return [
        {"role": m.role.value.lower(), "content": m.content} for m in ordered[-_MAX_HISTORY:]
    ]


def chat(db: Session, business: Business, payload: AssistantChatRequest) -> dict:
    """Bangun context, suntikkan ke system instruction, panggil LLM, simpan pesan."""
    if payload.conversation_id is not None:
        conversation = _get_owned_conversation(db, business, payload.conversation_id)
        history = _messages_to_history(conversation)
    else:
        conversation = AIConversation(
            business_id=business.id,
            title=payload.message[:_TITLE_LIMIT],
            status=ConversationStatus.ACTIVE,
        )
        db.add(conversation)
        db.flush()
        history = [{"role": m.role, "content": m.content} for m in payload.history[-_MAX_HISTORY:]]

    context = build_business_context(db, business)
    system_prompt = _build_system_prompt(context)
    messages = [*history, {"role": "user", "content": payload.message}]
    reply = llm_service.generate_text(system=system_prompt, messages=messages)

    db.add_all(
        [
            AIMessage(conversation_id=conversation.id, role=MessageRole.USER, content=payload.message),
            AIMessage(conversation_id=conversation.id, role=MessageRole.ASSISTANT, content=reply),
        ]
    )
    db.commit()

    return {"conversation_id": conversation.id, "message": reply}


def list_conversations(db: Session, business: Business) -> list[dict]:
    conversations = (
        db.query(AIConversation)
        .filter(
            AIConversation.business_id == business.id,
            AIConversation.status == ConversationStatus.ACTIVE,
        )
        .order_by(AIConversation.updated_at.desc(), AIConversation.id.desc())
        .all()
    )
    return [
        {
            "id": c.id,
            "title": c.title or "Percakapan baru",
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }
        for c in conversations
    ]


def get_conversation(db: Session, business: Business, conversation_id: int) -> dict:
    conversation = _get_owned_conversation(db, business, conversation_id)
    messages = [
        {
            "id": m.id,
            "role": m.role.value.lower(),
            "content": m.content,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in sorted(conversation.messages, key=lambda m: m.id)
    ]
    return {
        "id": conversation.id,
        "title": conversation.title or "Percakapan baru",
        "messages": messages,
    }
