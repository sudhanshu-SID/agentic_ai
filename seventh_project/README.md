# 🎬 CineVibe AI: Multimodal Multi-Agent Content Studio (LangGraph & LangChain)

A production-grade, multimodal multi-agent studio built with **LangGraph**, **LangChain**, and **Gemini 3.8/Flash**. 

CineVibe AI transforms your raw travel gallery (photos, videos, and personal memories) into viral, high-retention video storyboards with automated visual intelligence, cultural fact-checking, and interactive **Human-in-the-Loop (HITL)** topic curation.

---

## 🌟 The Core Problem

* You capture stunning photos and video clips on vacation, but have no idea how to structure them into an engaging video.
* You had a unique emotional experience or funny moment, but struggle to write an irresistible hook.
* You want cultural depth, verified local facts, and proper video pacing without hours of research and editing.

---

## 🏗️ System Architecture & LangGraph Flow

This project leverages **LangGraph's state graph engine** featuring nodes, conditional routing, and interactive human interrupts.

```
                         [ USER INPUT ]
               Media Files (Photos/Videos) + Personal Story
                               │
                               ▼
            ┌──────────────────────────────────────┐
            │   NODE 1: Media Analyst Agent        │
            │   (Gemini Multimodal Vision)         │
            │   - Inspects visuals, mood, & cues   │
            │   - Brainstorms 3-5 Viral Angles     │
            └──────────────────┬───────────────────┘
                               │
                               ▼
              ⚡ HUMAN-IN-THE-LOOP INTERRUPT ⚡
           User reviews proposed angles & picks one
                               │
                               ▼
            ┌──────────────────────────────────────┐
            │   NODE 2: Research Analyst Agent     │
            │   (Tavily Search Tool + Gemini)      │
            │   - Queries live cultural trivia     │
            │   - Fact-checks locations & history  │
            └──────────────────┬───────────────────┘
                               │
                               ▼
            ┌──────────────────────────────────────┐
            │   NODE 3: Storyteller / Writer Agent │
            │   - Bridges personal story + facts   │
            │   - Drafts scene-by-scene script     │
            └──────────────────┬───────────────────┘
                               │
                               ▼
            ┌──────────────────────────────────────┐
            │   NODE 4: Retention Critic Agent     │
            │   - Retention audit (first 3s hook)  │
            │   - Sound design & music vibes       │
            │   - On-screen text & B-roll overlays │
            └──────────────────┬───────────────────┘
                               │
                               ▼
                     [ FINAL STORYBOARD ]
             Director-Ready Shot List & Voiceover
```

---

## 📋 Graph State Schema (`states.py`)

Using LangGraph `TypedDict` state management:

```python
from typing import TypedDict, Annotated
import operator

class CineVibeState(TypedDict):
    # 1. User Inputs
    media_paths: list[str]       # File paths to user photos/videos
    user_experience: str         # User's personal memory/feeling
    target_platform: str         # "Instagram Reel", "TikTok", or "YouTube Short"

    # 2. Media Analyst Output
    media_analysis: str          # Visual breakdown of objects, lighting, landmarks
    suggested_topics: list[str]  # 3-5 pitched angles

    # 3. Human-in-the-Loop Selection
    selected_topic: str          # Winning topic chosen by user

    # 4. Research Output
    research_notes: str          # Real-world facts, history, local lore

    # 5. Writer Output
    writer_notes: str            # Video narrative draft

    # 6. Retention Critic Output
    expert_notes: str            # Pacing, audio vibes, retention critiques

    # 7. Final Deliverable
    final_storyboard: str        # Shot-by-shot production guide
```

---

## 🛠️ Technology Stack

* **LangGraph:** Cyclic state-machine agent orchestration with built-in persistence & human interrupts.
* **LangChain:** Agent tool calling and prompt templating.
* **Google Gemini (Multimodal):** Native visual comprehension of photos and videos.
* **Tavily Search API:** Real-time web intelligence.
* **Python 3.10+ / Dotenv:** Environment & credential security.

---

## 🎯 Learning Objectives

1. Understand **StateGraph**, **Nodes**, and **Edges** in LangGraph.
2. Implement **Human-in-the-Loop (HITL)** using LangGraph's `interrupt()` pattern.
3. Master **Multimodal Agents** combining vision + text reasoning.
4. Production-grade error handling, retries, and state checkpoints.
