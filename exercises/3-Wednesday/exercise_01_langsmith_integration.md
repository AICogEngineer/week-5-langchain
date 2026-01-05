# Exercise 01: LangSmith Integration

## Overview

LangSmith is LangChain's observability platform for debugging, testing, and monitoring LLM applications. In this exercise, you'll configure LangSmith for your development environment and verify that automatic tracing works.

## Learning Objectives

- Set up LangSmith API credentials
- Configure environment variables for tracing
- Verify traces appear in the LangSmith dashboard
- Understand trace hierarchy (runs, spans, events)

## The Scenario

Your team is starting a new LangChain project and wants observability from day one. Before writing any complex agent logic, you need to:

1. Set up LangSmith credentials
2. Verify tracing works
3. Create a project for the team's traces

## Your Tasks

### Task 1: Environment Setup (15 min)

Implement `verify_langsmith_config()` in the starter code:
- Check that all required environment variables are set
- Validate the API key format
- Return configuration status

Required environment variables:
- `LANGSMITH_TRACING` - Must be "true"
- `LANGSMITH_API_KEY` - Your API key from LangSmith
- `LANGSMITH_PROJECT` - Project name for organizing traces

> **Hint**: Use `os.environ.get()` to check variables.

### Task 2: API Connection Test (15 min)

Implement `test_langsmith_connection()`:
- Attempt to connect to LangSmith API
- Verify the project exists or can be created
- Return connection status

### Task 3: First Traced Agent (20 min)

Implement `create_traced_agent()`:
- Create a simple agent with one tool
- Run an invocation that will be traced
- Return the trace URL for verification

### Task 4: Trace Verification (15 min)

Implement `verify_trace_exists()`:
- After running the agent, check that a trace appeared
- Open the LangSmith dashboard to view the trace
- Document what you see in the trace

## Definition of Done

- [_] All environment variables correctly configured
- [_] LangSmith API connection successful
- [_] Agent invocation creates a trace
- [_] Trace visible in LangSmith dashboard
- [_] Can identify agent, LLM calls, and tool calls in trace

## Testing Your Solution

```bash
# First, set environment variables
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="your-key"
export LANGSMITH_PROJECT="week5-exercises"

# Then run the exercise
cd exercises/3-Wednesday/starter_code
python exercise_01_starter.py
```

Expected output format:
```
=== LangSmith Integration Test ===

[INFO] Checking environment configuration...
[OK] LANGSMITH_TRACING = true
[OK] LANGSMITH_API_KEY = lsv2_***abc
[OK] LANGSMITH_PROJECT = week5-exercises

[INFO] Testing LangSmith connection...
[OK] Connected to LangSmith

[INFO] Running traced agent...
[OK] Agent invocation complete

[INFO] Trace URL: https://smith.langchain.com/o/xxx/projects/p/xxx/r/xxx

=== Open the URL above to view your trace ===
```

## LangSmith Dashboard Guide

When you open a trace in LangSmith, you'll see:

| Section | What It Shows |
|---------|---------------|
| **Run Tree** | Hierarchy of all operations (agent → LLM → tools) |
| **Inputs** | What was sent to each component |
| **Outputs** | What each component returned |
| **Latency** | Time taken for each step |
| **Token Usage** | Tokens consumed by LLM calls |
| **Metadata** | Model name, version, parameters |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No traces appearing | Verify `LANGSMITH_TRACING=true` is set |
| Authentication error | Check API key is valid and not expired |
| Project not found | Project is auto-created on first trace |
| Traces show errors | Check the trace details for error messages |

## Stretch Goals (Optional)

1. Create separate projects for dev/staging/prod
2. Add custom metadata to traces
3. Set up trace filtering by tags
