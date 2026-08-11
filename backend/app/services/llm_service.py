"""LLM adapter (provider-agnostic) untuk Business Assistant.

Backend tetap source of truth: LLM hanya menerima structured context dari
backend dan menghasilkan penjelasan/advisory. Tidak ada akses database
langsung dari lapisan ini.
"""
import httpx

from app.core.config import get_settings
from app.core.errors import LLMUnavailableError

_GEMINI_GENERATE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
_HTTP_TIMEOUT = 90.0


def generate_text(*, system: str, messages: list[dict[str, str]]) -> str:
    """Kirim percakapan ke LLM dan kembalikan teks balasan.

    Args:
        system: instruksi sistem (role, scope, grounding rules).
        messages: daftar ``{"role": "user" | "assistant", "content": ...}``.
    """
    settings = get_settings()
    provider = (settings.llm_provider or "gemini").strip().lower()

    if provider == "gemini":
        return _gemini_generate_text(settings.gemini_api_key, settings.gemini_model, system, messages)
    raise LLMUnavailableError(f"LLM provider '{provider}' belum didukung.")


def _gemini_generate_text(api_key: str, model: str, system: str, messages: list[dict[str, str]]) -> str:
    if not api_key:
        raise LLMUnavailableError(
            "AI Business Assistant belum aktif: GEMINI_API_KEY belum diisi di backend/.env."
        )

    contents = [
        {"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
        for m in messages
    ]
    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1024},
    }
    url = _GEMINI_GENERATE_URL.format(model=model)
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}

    try:
        with httpx.Client(timeout=_HTTP_TIMEOUT) as client:
            response = client.post(url, headers=headers, json=payload)
    except httpx.HTTPError as exc:
        raise LLMUnavailableError("Gagal menghubungi layanan AI.", detail=str(exc)) from exc

    if response.status_code != 200:
        raise LLMUnavailableError(
            f"Layanan AI mengembalikan error ({response.status_code}).",
            detail=response.text[:500],
        )

    data = response.json()
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMUnavailableError("Balasan AI kosong atau tidak valid.", detail=str(data)[:500]) from exc
    return text.strip()
