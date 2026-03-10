
# Alyx Pipeline — Sequence Diagram

This repository implements the Alyx multi-agent pipeline. Below is a full sequence diagram (Mermaid) showing the entire stack and message flow.

```mermaid
sequenceDiagram
  %% Participants / stack
  participant U as User
  participant FW as OpenWebUI (Frontend)
  participant A as Alyx Pipeline
  participant G as LangGraph (StateGraph)
  participant SV as Supervisor
  participant W as Web
  participant WI as Wikipedia
  participant DOC as Doc
  participant DEV as Dev
  participant DATA as Data
  participant GEO as Geo
  participant MEDIA as Media
  participant RAG as RAG
  participant REA as Reasoning
  participant IMG as ImageGen
  participant TO as Tools / MCPO
  participant PW as Playwright
  participant CT as Context7
  participant DU as DuckDB
  participant YF as Yahoo-Finance
  participant POL as Pollinations (direct)
  participant LL as LiteLLM (proxy)
  participant OR as OpenRouter (provider)
  participant PG as Postgres (LangGraph checkpoint)
  participant RED as Redis (cache)
  participant MEM as Memory Agent / DB
  participant BG as Background Worker

  %% User -> Frontend -> Pipeline
  U->>FW: send message + files / images
  FW->>A: pipe(user_message, messages, event_emitter)

  %% Pipeline ensures graph and runs supervisor
  A->>G: ensure_graph() (builder -> loads agents, timeouts)
  A->>G: astream(initial_state)  -- start state
  G->>SV: call supervisor(route)

  %% Supervisor uses LL via LiteLLM -> provider
  SV->>LL: routing request (system + last message)
  LL->>OR: provider inference
  OR-->>LL: routing reply
  LL-->>SV: routing JSON (["web","wikipedia"] or {"routing":[], "routing_next":[]})
  SV-->>G: return routing (and routing_next)
  G-->>A: routing info (stream update)
  A->>FW: status "Invocation des agents: ..." (event)

  %% Parallel fan-out to agents
  alt Parallel agent fan-out
    par Web/Wikipedia
      G->>W: run web
      W->>TO: duckduckgo / fetch-web
      TO->>PW: playwright (fallback) 
      TO-->>W: page/content
      W-->>G: agent_outputs (with URLs)
      G->>WI: run wikipedia
      WI->>LL: wiki query (via LiteLLM)
      LL->>OR: model call
      OR-->>LL: reply
      LL-->>WI: content
      WI-->>G: agent_outputs
    and Dev
      G->>DEV: run dev
      DEV->>CT: get library docs
      DEV->>TO: git / terminal
      TO-->>DEV: results
      DEV-->>G: agent_outputs (artifacts)
    and Data
      G->>DATA: run data
      DATA->>TO: calculator / duckdb / yahoo-finance
      TO->>DU/YF: respective services
      DU/YF-->>TO: results
      TO-->>DATA: results
      DATA-->>G: agent_outputs
    and Doc / Reasoning / Media / RAG / Geo / Memory
      G->>DOC: run doc (paper-search -> fetch -> sci-hub via TO/PW)
      G->>REA: run reasoning (sequential-thinking via TO)
      G->>MEDIA: run media (youtube transcriptions)
      G->>RAG: run rag (qdrant)
      G->>GEO: run geo (openmeteo/osm)
      each agent ->>LL: model calls when needed
    and ImageGen
      G->>IMG: run image_gen
      IMG->>POL: Pollinations (direct HTTP, not via LiteLLM)
      POL-->>IMG: image_url | dataURI
      IMG-->>G: agent_outputs (image markdown) + artifacts
    end
  end

  %% LangGraph collects + checkpoints
  G->>A: stream agent_outputs + agent_metrics
  G->>PG: checkpoint state (Postgres saver)
  G-->>A: all agents done

  %% Pipeline post-processing
  A->>A: extract citations from agent_outputs
  A->>FW: emit source events (cards) for citations
  A->>FW: emit notifications if any agent returned ⚠️
  A->>FW: if first turn → emit chat:title (via LL -> LL->OR)

  alt Fast-path image-only
    A->>A: detect only image_gen result
    A-->>FW: emit image markdown (skip synthesis)
  else Full synthesis
    A->>A: build synthesis_context (merge agent outputs + artifacts)
    A->>LL: call Alyx synthesis (stream=True, include_usage)
    LL->>OR: provider model calls
    OR-->>LL: stream chunks (usage metadata)
    LL-->>A: streaming tokens
    A->>FW: stream tokens to user
    A->>A: capture usage -> agent_metrics[_synthesis]
  end

  %% Footer, metrics, memory
  A->>A: compute _estimate_cost(agent_metrics), build footer (models + tokens + time)
  A-->>FW: final footer (models, tokens, time, cost)
  A->>BG: schedule memory condensation (run_bg -> MEM)
  BG->>MEM: persist condensed memory (fire-and-forget)

  %% Caching and infra
  LL->>RED: cache lookups (config litellm_config.yaml)
  A->>PG: final checkpoint (conversation state)
  FW->>U: final streamed response + sources + footer

  Note over OR, POL: Providers: OpenRouter (models), Pollinations (images), others...
```

---

For details about the implementation, see `sub_agents/alyx_pipeline.py`, `graph/`, and `sub_agents/agents/`.
