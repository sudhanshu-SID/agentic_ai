# Agentic AI Learning Field

This repository is my practical workspace for learning Agentic AI. It holds my notes, experiments, projects, evaluations, and production-style implementations.

## North Star

Build the ability to explain and implement an AI workflow end to end:

- Where the LLM fits and what it is responsible for.
- How tools are discovered, validated, permissioned, and executed.
- How state, memory, retrieval, and context are managed.
- How deterministic workflows differ from agentic decisions.
- How agents are orchestrated, evaluated, observed, and made safe enough for real use.

The goal is working knowledge first, depth later. Learn the underlying architecture, build one useful thing, understand its failure modes, then move forward. Frameworks will change; models, tools, state, retrieval, orchestration, evaluation, permissions, and reliable execution will remain useful.

## Roadmap At A Glance

| Phase | Focus | Outcome |
| --- | --- | --- |
| 1 | Python for AI workflows | Build small backend and automation scripts confidently. |
| 2 | LLM APIs | Call models, manage prompts, produce structured output, and handle failures. |
| 3 | Tool calling | Give an LLM controlled capabilities through functions and APIs. |
| 4 | Agent loop | Build a reason -> act -> observe loop without a framework. |
| 5 | RAG | Ground responses in private or current knowledge. |
| 6 | MCP | Connect models to tools and context through a standard protocol. |
| 7 | LangGraph | Model stateful, controlled agent workflows explicitly. |
| 8 | n8n | Build reliable AI-assisted business automations. |
| 9 | Multi-agent orchestration | Delegate, route, parallelize, and coordinate specialists when justified. |
| 10 | Evaluation and observability | Measure, debug, and improve agent behavior. |
| 11 | Production deployment | Turn a prototype into a secure, reliable service. |

Read [phase.md](./phase.md) for the complete learning curriculum and checkpoints. Read [project.md](./project.md) for the build sequence and capstone.

## The System In Layers

Think of an agentic application as a stack of connected layers, not a collection of unrelated tools:

`User goal -> application/backend -> orchestrator/agent loop -> LLM -> tools -> external systems and data -> results -> evaluation and observability -> human approval when needed`

| Layer | Examples | Responsibility |
| --- | --- | --- |
| Interface | Web app, chat, API | Receives goals and displays results. |
| Application | Python, FastAPI, TypeScript | Owns business logic, authentication, and permissions. |
| Orchestration | Agent loop, LangGraph | Controls state, routing, and execution. |
| Reasoning | GPT, Claude, Gemini | Interprets goals and selects next actions. |
| Capabilities | Functions, APIs, MCP | Lets the system act and retrieve information. |
| Knowledge | RAG, Postgres, files | Provides current or private context. |
| Automation | n8n, queues, cron | Connects systems and runs repeatable workflows. |
| Reliability | Evaluation, tracing, guardrails | Measures and controls behavior. |
| Infrastructure | Docker, cloud, workers | Runs the system reliably. |

## How To Work In This Repository

For each phase:

1. Learn only the listed concepts well enough to build the project.
2. Build the phase project in its own folder.
3. Add a short `README.md` inside that project covering architecture, setup, decisions, limitations, and lessons learned.
4. Record failures, costs, latency, and next improvements as the work becomes agentic.
5. Complete the checkpoint before moving on.

Use this folder structure as it grows:

```text
Agentic_ai_/
  README.md
  phase.md
  project.md
  notes/
  experiments/
  projects/
    01-job-description-analyzer/
    02-resume-jd-matcher/
    ...
  evaluations/
  references/
```

Keep secrets out of version control. Use `.env` files locally, document required variables in `.env.example`, and add human approval before any consequential external action such as applying for a job, sending a message, changing data, or spending meaningful money.

## Suggested Pace

These are learning estimates, not deadlines. Move on when you can explain the concept, build the small project, and understand its failure modes.

| Stages | Suggested focus |
| --- | --- |
| 1-2 | 2-4 days each: Python and API fluency. |
| 3-4 | 4-7 days: tool calling and a hand-built agent loop. |
| 5-6 | 3-5 days each: RAG fundamentals and MCP hands-on work. |
| 7-9 | 1-2 weeks total: orchestration, n8n, and multi-agent patterns. |
| 10 | 3-5 days: add evaluation to an existing project. |
| 11 | 1-2 weeks: deploy one production-style version. |

## Interview Readiness

By the end of the roadmap, be able to explain and demonstrate:

- What makes an agent different from a standard LLM call.
- The LLM -> tool call -> result -> LLM cycle and its stopping conditions.
- Deterministic workflows versus agentic workflows.
- RAG, retrieval quality, and when retrieval is preferable to fine-tuning.
- What MCP standardizes and its security implications.
- When a single agent is sufficient and when multi-agent coordination helps.
- How to evaluate agent quality, trace its actions, and investigate failures.
- How tool permissions, privacy, persistence, retries, monitoring, and approval gates make an agent safer to operate.

## Source Of This Roadmap

This workspace guide is distilled from `C:\Users\91911\Downloads\Agentic_AI_Breadth_First_Roadmap.pdf`. The PDF remains the source reference; this README plus the phase and project documents are the working context for future learning and builds.
