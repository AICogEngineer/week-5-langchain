# Week 5 Readings: LangChain v1.0 & Agentic Design Patterns

> [!IMPORTANT]
> **EVERY SECTION in this README is critical.** Do not skip any material. The concepts here form the foundation for all Week 5 execution.

## Core Readings (LangChain v1.0)
These documents cover the modern standard for building with LangChain.
- **Monday**: Model Initialization & Usage (`init_chat_model`, `bind_tools`)
- **Tuesday**: Tool Creation & Agents (`@tool`, `create_agent`)
- **Wednesday**: Observability (LangSmith, Tracing)
- **Thursday**: Persistence & Memory (`InMemorySaver`, Checkpointing)
- **Friday**: Structured Output & RAG (`with_structured_output`)

## Special Resource: Agentic Design Patterns

We have a special resource included in this directory: **`Agentic_Design_Patterns.pdf`**.

> [!CAUTION]
> **SENSITIVE MATERIAL**: This PDF is an **EXTENSIVELY detailed** guide (400+ pages) from Google (authored by Antonio Gulli et al.). It was originally publicly released and then converted into a paid book.
> **Please be mindful of who you share this with.**

### How to Consume This Resource
This PDF is the **Deep Dive**. It covers 21+ design patterns in exhaustive detail.

**For a Quick Architecture Breakdown:**
Instead of sifting through the 400+ pages immediately, read this architecture breakdown first to understand the core patterns (Sequential, Routing, Parallel, Orchestrator-Workers):

**[Building Effective Agents (Architecture Breakdown)](https://www.anthropic.com/research/building-effective-agents)**
*(Note: While from Anthropic, this article provides the clearest industry-standard breakdown of the agentic workflow patterns discussed in the detailed Google PDF.)*

**[Choose a Design Pattern for Agentic AI (Google Cloud)](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system#compare-design-patterns)**
*(Note: This official Google Cloud guide directly compares the design patterns with decision trees on when to use which.)*

**When to read the PDF:**
- Use it as a reference when you need deep specific implementation details on a pattern.
- Look at the diagrams for "Multi-Agent Collaboration" and "Reflection" patterns.
- Read it after you understand the core concepts from the architecture breakdown.

## Summary of Key Patterns
1.  **Prompt Chaining**: Sequential execution (A -> B -> C).
2.  **Routing**: LLM decides which path to take (A -> B or C).
3.  **Parallelization**: Running independent tasks at the same time.
4.  **Orchestrator-Workers**: Central brain delegates to sub-agents.
5.  **Evaluator-Optimizer**: One model generates, another scores and refines.
