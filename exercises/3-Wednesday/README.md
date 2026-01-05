# Wednesday: LangSmith Setup & Agent Debugging

## Exercise Schedule

| Exercise | Type | Duration | Prerequisites |
|----------|------|----------|---------------|
| 01: LangSmith Integration | Implementation | 45-60 min | Reading 01-02, Demo 01 |
| 02: Trace Analysis | Hybrid | 60-75 min | Reading 03-05, Demo 02-03 |

## Learning Objectives

By completing these exercises, you will:
- Configure LangSmith for automatic tracing
- Navigate the LangSmith dashboard
- Analyze agent execution traces
- Debug agent behavior using traces
- Monitor token usage and costs

## Before You Begin

1. **Complete the readings** in `readings/3-Wednesday/`
2. **Watch/run demos** in `demos/3-Wednesday/code/`
3. **LangSmith Account**: Create an account at https://smith.langchain.com/
4. Set up environment variables:
   ```bash
   export LANGSMITH_TRACING=true
   export LANGSMITH_API_KEY="your-langsmith-api-key"
   export LANGSMITH_PROJECT="week5-exercises"
   ```

## Exercises

### Exercise 01: LangSmith Integration (Implementation)
See [exercise_01_langsmith_integration.md](exercise_01_langsmith_integration.md)
Starter code: `starter_code/exercise_01_starter.py`

Configure LangSmith environment and verify automatic tracing works with your agents.

### Exercise 02: Trace Analysis (Hybrid)
See [exercise_02_trace_analysis.md](exercise_02_trace_analysis.md)
Starter code: `starter_code/exercise_02_starter.py`

Run agent scenarios, then analyze the resulting traces in LangSmith dashboard.

## Estimated Time
**Total: 2-2.5 hours**

## Key LangSmith Concepts

```bash
# Required environment variables
export LANGSMITH_TRACING=true           # Enable automatic tracing
export LANGSMITH_API_KEY="lsv2_..."     # Your API key
export LANGSMITH_PROJECT="my-project"   # Project name for organization
```

```python
# No code changes needed! Tracing is automatic.
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[my_tool],
    name="traced_agent"
)

# This invocation is automatically traced
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
# View trace at: https://smith.langchain.com/
```

> **Tip**: LangSmith traces every LLM call, tool invocation, and agent step automatically when `LANGSMITH_TRACING=true`.
