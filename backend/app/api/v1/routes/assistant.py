"""Business Assistant API (API Contract bab 18).

- POST /api/v1/ai/chat — chat dengan asisten AI berbasis data bisnis pemilik.
- GET /api/v1/ai/conversations — daftar percakapan pemilik.
- GET /api/v1/ai/conversations/{id} — pesan-pesan satu percakapan.

Backend menyusun context (source of truth), memanggil LLM, dan menyimpan
percakapan + pesan agar riwayat tidak hilang saat halaman di-refresh.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.schemas.assistant import AssistantChatRequest
from app.services import assistant_service

router = APIRouter()


@router.post("/chat", response_model=dict)
def chat(
    payload: AssistantChatRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": assistant_service.chat(db, business, payload)}


@router.get("/conversations", response_model=dict)
def list_conversations(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": assistant_service.list_conversations(db, business)}


@router.get("/conversations/{conversation_id}", response_model=dict)
def get_conversation(
    conversation_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {
        "success": True,
        "data": assistant_service.get_conversation(db, business, conversation_id),
    }
