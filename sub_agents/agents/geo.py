"""
Geo Agent — météo et données géographiques.

Modèle : openrouter/qwen3.5-flash.
Outils : openmeteo (MCPO), osm-mcp-server (MCPO).

Stratégie :
  1. LLM extrait le lieu mentionné dans la question.
  2. Géocodage OSM (latitude/longitude).
  3. Prévisions météo Open-Meteo.
  4. LLM synthétise en langage naturel.
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
Tu es un·e expert·e en météorologie et données géographiques.
Présente les données météo de façon claire et lisible : températures, précipitations,
vent, humidité. Indique les coordonnées GPS du lieu identifié.
Réponds dans la même langue que la question.
"""

_LOC_SYSTEM = """\
Extrais le nom du lieu géographique principal de la question utilisateur.
Traduis-le en anglais si nécessaire pour la géolocalisation.
Retourne UNIQUEMENT le nom du lieu, sans explication.
"""


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    emitter = (config.get("configurable") or {}).get("event_emitter") if config else None

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
        max_tokens=1024,
    )

    # 1. Extraire le nom du lieu
    loc_resp = await llm.ainvoke(
        [SystemMessage(content=_LOC_SYSTEM), HumanMessage(content=user_text)],
        config={"max_tokens": 30},
    )
    location = loc_resp.content.strip()[:80]
    _prompt_tokens = (getattr(loc_resp, "usage_metadata", None) or {}).get("input_tokens", 0) or 0
    _completion_tokens = (getattr(loc_resp, "usage_metadata", None) or {}).get("output_tokens", 0) or 0

    context_parts: list[str] = []
    lat: float | None = None
    lon: float | None = None

    # 2. Géocodage OSM
    try:
        await _emit(f"🗺️ Géolocalisation : {location}")
        osm_result = await call_tool("osm-mcp-server", "geocode", {"q": location, "limit": 1})
        osm_str = json.dumps(osm_result, ensure_ascii=False, indent=2)
        context_parts.append(f"## OSM geocoding ({location!r})\n{osm_str[:2000]}")
        # Extraire lat/lon depuis la réponse (structure variable selon impl.)
        if isinstance(osm_result, list) and osm_result:
            first = osm_result[0]
            lat = float(first.get("lat", first.get("latitude", 0)) or 0) or None
            lon = float(first.get("lon", first.get("longitude", 0)) or 0) or None
        elif isinstance(osm_result, dict):
            lat = float(osm_result.get("lat", osm_result.get("latitude", 0)) or 0) or None
            lon = float(osm_result.get("lon", osm_result.get("longitude", 0)) or 0) or None
    except Exception as exc:
        context_parts.append(f"## OSM indisponible\n{exc}")

    # 3. Météo Open-Meteo si coordonnées disponibles
    if lat is not None and lon is not None:
        try:
            await _emit(f"🌦️ Météo pour {location}")
            meteo_result = await call_tool("openmeteo", "get_forecast", {
                "latitude": lat,
                "longitude": lon,
                "forecast_days": 5,
            })
            meteo_str = json.dumps(meteo_result, ensure_ascii=False, indent=2)
            context_parts.append(f"## Prévisions météo ({location})\n{meteo_str[:4000]}")
        except Exception as exc:
            try:
                # Certains serveurs utilisent get_current_weather
                meteo_result = await call_tool("openmeteo", "get_current_weather", {
                    "latitude": lat,
                    "longitude": lon,
                })
                meteo_str = json.dumps(meteo_result, ensure_ascii=False, indent=2)
                context_parts.append(f"## Météo actuelle ({location})\n{meteo_str[:4000]}")
            except Exception as exc2:
                context_parts.append(f"## Open-Meteo indisponible\n{exc} / {exc2}")
    else:
        context_parts.append(f"## Lieu non géolocalisé : {location!r}")

    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nQuestion utilisateur : {user_text}"

    await _emit("✍️ Synthèse géographique…")
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    _prompt_tokens += _u.get("input_tokens", 0) or 0
    _completion_tokens += _u.get("output_tokens", 0) or 0
    return {
        "agent_outputs": {"geo": response.content},
        "agent_metrics": {"geo": {
            "prompt_tokens": _prompt_tokens,
            "completion_tokens": _completion_tokens,
            "model": model or _MODEL,
        }},
    }


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
