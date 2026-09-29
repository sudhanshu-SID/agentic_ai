# Agentic AI Projects

Here are the practical projects to build for each phase of the roadmap. They build upon each other, culminating in a final capstone project.

## Phase 1: Job Description Analyzer CLI
- **Project Description:** Build a Python CLI that accepts a job-description URL or text, calls an API, extracts structured requirements, and saves the result as JSON/Markdown.
- **Checkpoint:** You should be able to write a small Python service that calls an API, handles failure, parses JSON, and stores results.
- **Connection to Next Stage:** This becomes the foundation for every later agent project.
- **Interview Value:** Be prepared to discuss APIs, async code, error handling, environment variables, and why Python is commonly used for AI tooling.

## Phase 2: Resume ↔ Job Description Matcher
- **Project Description:** Send a resume and JD to an LLM and return strict JSON: matched skills, missing skills, evidence, and interview topics.
- **Checkpoint:** You should understand that your application owns the workflow; the LLM is a probabilistic reasoning/generation component inside it.
- **Connection to Next Stage:** Tool calling will add real actions to this model interaction.
- **Interview Value:** Be prepared to discuss tokens, context limits, structured output, hallucination, and latency/cost tradeoffs.

## Phase 3: Personal Developer Assistant
- **Project Description:** Build tools such as a calculator, GitHub-repo lookup, weather/search API, and a local project-file reader. The LLM decides which tool to call.
- **Checkpoint:** You should be able to explain: the model does not magically execute your function. It requests a tool call; your application validates and executes it, then sends the result back.
- **Connection to Next Stage:** The next step is to let the model decide repeatedly until the goal is complete.
- **Interview Value:** Be prepared to discuss function calling, tool schemas, permissions, validation, and why tool access changes an LLM into an action-capable system.

## Phase 4: Autonomous Research Agent v1
- **Project Description:** Build an agent loop without LangChain/LangGraph/n8n. Given a technical topic, it searches, reads results, extracts evidence, identifies gaps, performs follow-up searches, and produces a cited report. Add a maximum-step limit.
- **Checkpoint:** You should be able to implement a simple agent loop yourself.
- **Connection to Next Stage:** This is the conceptual foundation for orchestration frameworks.
- **Interview Value:** Be prepared to discuss agent vs chatbot, the agent loop, autonomy, tool use, state, stopping conditions, and failure modes.

## Phase 5: Personal Knowledge Assistant
- **Project Description:** Index your technical notes/docs, retrieve relevant chunks, answer questions with source references, and explicitly say when evidence is insufficient.
- **Checkpoint:** You should understand the difference between model knowledge, retrieval, and generation.
- **Connection to Next Stage:** RAG becomes a capability/tool inside agentic systems.
- **Interview Value:** Be prepared to discuss embeddings, vector search, chunking, retrieval quality, hallucination reduction, and when RAG is preferable to fine-tuning.

## Phase 6: Developer MCP Server
- **Project Description:** Expose safe read-only tools such as project search, documentation lookup, issue lookup, or database schema inspection. Connect an MCP-capable client and observe tool discovery/calls.
- **Checkpoint:** You should be able to explain why MCP can reduce one-off integrations between an AI client and many tool providers.
- **Connection to Next Stage:** MCP becomes one of the ways your agents acquire capabilities.
- **Interview Value:** Be prepared to discuss MCP client/server, tools/resources, discovery, standardization, and security implications.

## Phase 7: Interview Preparation Agent
- **Project Description:** Use LangGraph to model explicit orchestration: ingest resume → analyze JD → research company → generate question set → simulate interview → evaluate answer → route weak areas back for another study cycle.
- **Checkpoint:** You should understand why explicit workflow graphs are useful when an agent needs predictable control instead of unrestricted autonomy.
- **Connection to Next Stage:** This prepares you for orchestration and multi-agent systems.
- **Interview Value:** Be prepared to discuss state machines/graphs, deterministic vs agentic nodes, routing, persistence, and human approval.

## Phase 8: Job Application Workflow
- **Project Description:** Build a workflow in n8n. Trigger from a new job posting → extract JD → classify fit → retrieve resume context → generate tailored suggestions → save to database/Notion → send a review notification. Keep approvals before external actions.
- **Checkpoint:** You should be able to decide: fixed sequence = workflow; uncertain decision/action selection = agent.
- **Connection to Next Stage:** Now combine visual automation with code-based agents and external tools.
- **Interview Value:** Be prepared to discuss workflow automation vs agents, triggers, integrations, webhooks, approvals, and reliability.

## Phase 9: Software Engineering Team (Multi-Agent)
- **Project Description:** Planner agent creates a plan; Research agent investigates; Coder agent proposes implementation; Reviewer agent checks it; a supervisor decides whether to revise or finish.
- **Checkpoint:** You should know when one agent is enough and when multiple agents provide a real architectural advantage.
- **Connection to Next Stage:** This is orchestration at the system level.
- **Interview Value:** Be prepared to discuss supervisor vs handoff, parallelism, context isolation, agent coordination, and why multi-agent can increase failure/cost.

## Phase 10: Agent Evaluation Harness
- **Project Description:** Create 30–50 representative tasks for your research/job agent. Record success/failure, tool choices, latency, token usage, and common failure reasons. Run it after changes.
- **Checkpoint:** You should be able to answer: 'How do you know your agent got better?'
- **Connection to Next Stage:** This is what turns experimentation into engineering.
- **Interview Value:** Be prepared to discuss evaluation datasets, deterministic tests, LLM-as-judge limitations, traces, cost, and reliability.

## Phase 11: Production-Style Agent Service
- **Project Description:** Expose your agent through an API, persist runs/results in Postgres, run long tasks in a worker/queue, authenticate users, log traces, enforce tool permissions, and provide a simple web UI.
- **Checkpoint:** You should be able to explain the difference between a prototype agent and a production agent.
- **Connection to Next Stage:** This completes the path from LLM call to real agentic application.
- **Interview Value:** Be prepared to discuss reliability, security, deployment, background jobs, state, observability, and cost management.

---

## 🏆 The Capstone: Personal Career Agent Platform
Combine the strongest pieces into one portfolio project: a system that monitors selected job sources, evaluates jobs against your resume, researches the company, retrieves your project/skill evidence from a RAG knowledge base, prepares interview questions, creates a personalized study plan, and tracks outcomes.

**System Architecture Guidelines:**
- Use an **orchestrator** for decisions.
- Use **specialized tools/MCP** for capabilities.
- Use **n8n** for integrations/triggers.
- Build an **evaluation layer** to measure the agent's performance.
- **Crucial Rule:** Keep human approval checkpoints before applying, sending messages, or taking other consequential external actions.
