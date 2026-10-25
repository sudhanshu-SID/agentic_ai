# 🌐 Phase 6: Multi-Agent Travel Content Agency (From Scratch)

A clean, foundational implementation of a multi-agent system built from first principles using pure Python and typed state passing (the Blackboard Pattern).

---

## 🎯 Purpose & Philosophy

Before jumping into heavy multi-agent frameworks like LangGraph or CrewAI, this project teaches the raw engineering mechanics that power them:
1. How shared state is represented and mutated cleanly.
2. How individual worker agents operate in isolation on partial state updates.
3. How state is passed sequentially from one worker agent to another.

---

## 🏛️ Agency Architecture

```
                       [ Input: topic ]
                              │
                              ▼
                ┌───────────────────────────┐
                │   🔍 Worker 1: Researcher │
                │   (Tavily Search + Gemini)│
                │   - Updates:              │
                │     `research_notes`      │
                └─────────────┬─────────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │   ✍️ Worker 2: Writer     │
                │   (Gemini Storyteller)    │
                │   - Updates:              │
                │     `writer_notes`        │
                └─────────────┬─────────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │   🧐 Worker 3: Expert     │
                │   (Gemini Travel Critic)  │
                │   - Updates:              │
                │     `expert_notes`        │
                │     `final_draft`         │
                └─────────────┬─────────────┘
                              │
                              ▼
                    [ Output: final_draft ]
```

---

## 📋 State Schema (`states.py`)

```python
from typing import TypedDict

class AgencyState(TypedDict):
    topic: str
    research_notes: str
    writer_notes: str
    expert_notes: str
    final_draft: str
```

---

## 📁 Project Structure

* `states.py`: TypedDict state definition (the office clipboard).
* `researcher.py`: Worker 1 — Queries Tavily and synthesizes factual notes.
* `writer.py`: Worker 2 — Crafts an engaging video/article script with strong hooks.
* `expert.py`: Worker 3 — Critiques, fact-checks, and polishes the final draft.
* `main.py`: The orchestrator that coordinates the pipeline end-to-end.
