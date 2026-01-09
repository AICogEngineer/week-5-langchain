# Human-in-the-Loop (HITL) Demo

A comprehensive demonstration of Human-in-the-Loop patterns in LangChain v1.0, designed to run locally and in LangSmith Studio.

## Overview

| File | Purpose |
|------|---------|
| `agent.py` | Studio-compatible agent export |
| `demo_y_HITL.py` | Learning demos with 5 examples |
| `langgraph.json` | Studio configuration |

## Quick Start

### 1. Install Dependencies

```bash
pip install langchain langchain-openai langgraph "langgraph-cli[inmem]"
```

### 2. Environment Setup

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Required keys:
- `OPENAI_API_KEY` - Your OpenAI API key
- `LANGSMITH_API_KEY` - From [LangSmith Settings](https://smith.langchain.com/settings)

### 3. Run Learning Demos

```bash
python demo_y_HITL.py
```

This runs 5 examples:
1. **Basic Approval** - Simple approve/reject flow
2. **Edit Capability** - Modify tool args before execution
3. **Reject with Feedback** - Reject with explanation message
4. **Streaming with HITL** - `stream()` with interrupt handling
5. **Interactive CLI** - Full interactive demo

### 4. Run in LangSmith Studio

```bash
langgraph dev
```

This starts a local server and opens your browser to:
```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

In Studio, you can:
- Chat with the agent interactively
- See HITL interrupts in the UI
- Approve, edit, or reject tool calls visually
- View traces in LangSmith

## HITL Decision Types

| Decision | Description |
|----------|-------------|
| `approve` | Execute the tool as-is |
| `edit` | Modify arguments, then execute |
| `reject` | Cancel with feedback message |

## Configuration

The `HumanInTheLoopMiddleware` accepts:

```python
HumanInTheLoopMiddleware(
    interrupt_on={
        "dangerous_tool": True,  # All decisions allowed
        "restricted_tool": {"allowed_decisions": ["approve", "reject"]},
        "safe_tool": False,  # No approval needed
    },
    description_prefix="[!] Approval required",
)
```

## References

- [HITL Documentation](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)
- [LangSmith Studio](https://docs.langchain.com/oss/python/langchain/studio)
- [LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
