"""
Audio Agent — transcription audio + Text-to-Speech locales.

Modèle : openrouter/gpt-oss pour la synthèse textuelle post-transcription.
Outils :
  - Transcription : appel HTTP à un serveur Whisper local (faster-whisper-server,
    whisper.cpp en mode HTTP, ou autre). URL via env WHISPER_URL (défaut
    http://whisper:9000/asr). Si le service n'est pas joignable, on retourne un
    message clair avec les instructions pour l'ajouter.
  - TTS : appel à un serveur edge-tts local OU au modèle TTS de LiteLLM si configuré.

Pour le TTS : sortie produite en tant qu'artifact audio (base64 wav/mp3) que la
pipeline peut convertir en lien data-URI ou en pièce jointe native.

Note : ce scaffold est prêt à l'emploi côté pipeline mais nécessite qu'un service
Whisper soit ajouté au compose.yaml. Voir README pour les options recommandées
(faster-whisper-server, openai-whisper-asr-webservice…).
"""

from __future__ import annotations

import base64
import os
from typing import TYPE_CHECKING

import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.text_utils import last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

# Endpoint d'un serveur Whisper local (à ajouter au compose si on veut la
# transcription). Compatible avec openai-whisper-asr-webservice (Onerahmet) ou
# faster-whisper-server.
_WHISPER_URL = os.environ.get("WHISPER_URL", "http://whisper:9000/asr")
_WHISPER_TIMEOUT = float(os.environ.get("WHISPER_TIMEOUT", "120"))


_SYSTEM_TRANSCRIBE = """\
You are a transcription assistant. The user provided audio that has been
automatically transcribed below. Your job is to:
  - Present the transcript cleanly (fix obvious punctuation/casing only)
  - Identify speakers if the transcript marks them
  - Summarize key points if the transcript is long (>500 words)
Reply in the language of the transcript.
"""


async def _transcribe(b64_audio: str) -> str:
    """Envoie l'audio à un serveur Whisper local. Le serveur attend un fichier
    multipart `audio_file`. Format de réponse selon l'API : on prend la clé `text`.
    """
    try:
        raw = base64.b64decode(b64_audio)
    except Exception as exc:
        return f"[base64 decode error: {exc}]"
    files = {"audio_file": ("input.wav", raw, "audio/wav")}
    params = {"task": "transcribe", "language": "auto"}
    try:
        async with httpx.AsyncClient(timeout=_WHISPER_TIMEOUT) as client:
            resp = await client.post(_WHISPER_URL, files=files, params=params)
            resp.raise_for_status()
            data = resp.json() if "application/json" in resp.headers.get("content-type", "") else {"text": resp.text}
            return str(data.get("text") or data)[:8000]
    except httpx.ConnectError:
        return (
            "[whisper service not reachable at " + _WHISPER_URL + " — "
            "add a faster-whisper-server / openai-whisper-asr-webservice container to compose.yaml]"
        )
    except Exception as exc:
        return f"[transcription error: {exc}]"


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = last_user_message(messages)
    audios_b64 = state.get("audios_b64") or []

    emitter = (config.get("configurable") or {}).get("event_emitter") if config else None

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

    if not audios_b64:
        return {
            "agent_outputs": {"audio": (
                "⚠️ Aucun audio fourni. Joins un fichier audio (wav/mp3/m4a/ogg) "
                "au message pour activer la transcription."
            )},
            "agent_confidence": {"audio": 0.0},
        }

    # Transcrire chaque audio (en série pour respecter la mémoire GPU du serveur whisper)
    transcripts: list[str] = []
    for i, b64 in enumerate(audios_b64[:3], 1):
        await _emit(f"🎙️ Transcription audio {i}/{min(len(audios_b64), 3)}…")
        text = await _transcribe(b64)
        transcripts.append(f"### Audio {i}\n{text}")

    raw_text = "\n\n".join(transcripts)

    # Si Whisper n'est pas dispo, on retourne le warning brut sans appeler le LLM
    if all("[whisper service not reachable" in t for t in transcripts):
        return {
            "agent_outputs": {"audio": raw_text + (
                "\n\n> 🎙️ Pour activer la transcription audio, ajoute un service Whisper au compose.yaml "
                "(ex. `onerahmet/openai-whisper-asr-webservice:latest-cpu`) et expose-le en `whisper:9000`."
            )},
            "agent_confidence": {"audio": 0.0},
        }

    # Post-traitement par le LLM
    await _emit("✍️ Synthèse de la transcription…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )
    prompt = f"User context: {user_text}\n\n## Raw transcripts\n{raw_text}"
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM_TRANSCRIBE),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    output = (response.content or "") + f"\n\n> 🎙️ Source : transcription locale (Whisper, {len(audios_b64)} fichier(s))"
    return {
        "agent_outputs": {"audio": output},
        "agent_confidence": {"audio": 0.75},
        "agent_metrics": {"audio": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }
