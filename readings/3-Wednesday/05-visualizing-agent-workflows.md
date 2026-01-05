# Visualizing Agent Workflows

## Learning Objectives
- Understand agent decision flow through LangSmith traces
- Identify bottlenecks and inefficiencies in agent execution
- Compare different agent approaches visually
- Use visualization insights to improve agent design

## Why This Matters

Reading traces as text is one thing; *seeing* the execution flow is another. Visualization reveals patterns that text logs hide—bottlenecks, unnecessary loops, unbalanced tool usage. These insights guide optimization.

When you can see the workflow, you can design better agents.

## The Concept

### The Trace Timeline

LangSmith provides a visual timeline for each trace:

```
Time →
├─────────────┬───────────┬─────────┬──────────────┤
│  ChatOpenAI │ tool: get │ChatOpenAI│   Response   │
│   (0.8s)    │ weather   │ (0.5s)  │              │
│             │  (1.2s)   │         │              │
└─────────────┴───────────┴─────────┴──────────────┘
0s            0.8s        2.0s      2.5s
```

This immediately shows:
- Total execution time (2.5s)
- Which component took longest (tool: 1.2s)
- Sequential vs. parallel execution

### Reading the Execution Graph

The trace tree shows parent-child relationships:

```
my_agent (root)
├── ChatOpenAI    ← Model decides what to do
├── search_kb     ← Tool execution
│   └── [internal operations if any]
├── ChatOpenAI    ← Model processes tool result
└── Final: "The answer is..."
```

**Interpretation:**
- First LLM call: Received user message, decided to call tool
- Tool call: Executed with specific arguments
- Second LLM call: Saw tool result, generated final answer

### Identifying Patterns

#### Healthy Patterns

**Simple tool use:**
```
Agent
├── LLM (decide)
├── Tool (execute)
├── LLM (respond)
└── Done (3 steps)
```

**Multi-tool workflow:**
```
Agent
├── LLM (analyze, decide multiple tools)
├── Tool A (parallel)
├── Tool B (parallel)
├── LLM (synthesize)
└── Done (efficient parallelism)
```

#### Warning Patterns

**Unnecessary loop:**
```
Agent
├── LLM → Tool A
├── LLM → Tool A (same thing!)
├── LLM → Tool A (again?)
└── Finally responds (wasted 2 calls)
```

**Long tool chain:**
```
Agent
├── LLM → Tool A → LLM → Tool B → LLM → Tool C → LLM
└── Total: 7 steps for simple question
```

### Bottleneck Identification

In the timeline view, look for:

1. **Disproportionately long steps**: One component taking 80% of time
2. **Sequential when parallel possible**: Tools that could run together
3. **Repeated tool calls**: Same tool called multiple times unnecessarily
4. **Long LLM calls**: Suggests complex prompts or large context

### Comparing Agent Approaches

Use LangSmith's compare feature to see differences:

```
Agent A (Basic)              Agent B (Optimized)
─────────────────           ──────────────────
├─ LLM (1.2s)               ├─ LLM (0.8s)
├─ Tool (0.5s)              ├─ Tool (0.5s)
├─ LLM (0.9s)               └─ Done (1.3s)
├─ Tool (0.5s)
├─ LLM (0.7s)
└─ Done (3.8s)

Improvement: 66% faster
```

### Workflow Optimization Insights

**From visualization, you might learn:**

| Observation | Action |
|-------------|--------|
| Tool takes 70% of time | Optimize tool implementation |
| LLM called 5 times | Consolidate into fewer calls |
| Same tool called repeatedly | Cache results or fix prompts |
| Long first LLM call | System prompt too complex |
| Many small tool calls | Batch into single tool |

### Using Trace Comparisons

To compare runs side-by-side:

1. Select multiple traces (checkbox)
2. Click "Compare" button
3. View synchronized timelines

This is powerful for:
- A/B testing prompt changes
- Before/after optimization
- Success vs. failure analysis

### Workflow Patterns for Different Use Cases

**Q&A Agent:**
```
User Question → LLM → Search Tool → LLM → Answer
(Expected: 3-4 steps, <3 seconds)
```

**Research Agent:**
```
Task → LLM → Multiple Searches → LLM → Synthesis → Answer
(Expected: 5-8 steps, <10 seconds)
```

**Complex Task Agent:**
```
Task → LLM → Sub-task Planning → [Multiple Tool Phases] → Synthesis
(Expected: 10+ steps, may take minutes)
```

### Anomaly Detection

Watch for anomalies in workflow patterns:

```
Normal Run:                    Anomalous Run:
LLM → Tool → LLM → Done       LLM → Tool → LLM → Tool → LLM → 
(2.5s)                        Tool → LLM → Tool → LLM → Done
                              (12.3s) ← Something went wrong
```

When you spot anomalies:
1. Compare to normal runs
2. Check tool inputs—was something different?
3. Review LLM reasoning at each step
4. Look for error patterns

## Code Example

```python
"""
Creating Traces for Workflow Visualization
LangChain Version: v1.0+
"""
import os
import time
from langchain.agents import create_agent
from langchain_core.tools import tool

os.environ["LANGSMITH_PROJECT"] = "workflow-visualization"

# Tools with varying latencies
@tool
def fast_lookup(key: str) -> str:
    """Quick database lookup. Use for simple ID-based retrieval."""
    time.sleep(0.1)  # Fast
    return f"Quick result for {key}"

@tool
def medium_search(query: str) -> str:
    """Search across documents. Use for keyword searches."""
    time.sleep(0.5)  # Medium
    return f"Search results for {query}"

@tool
def slow_analysis(data: str) -> str:
    """Deep analysis of data. Use for complex computations."""
    time.sleep(1.5)  # Slow - this will show as bottleneck
    return f"Analysis complete for {data}"

# Create agents with different tool combinations
quick_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[fast_lookup],
    system_prompt="Use the lookup tool for direct answers.",
    name="quick_lookup_agent"
)

multi_step_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[fast_lookup, medium_search, slow_analysis],
    system_prompt="""You help with research tasks.
    1. Start with fast lookup for basic info
    2. Use search for broader context
    3. Use analysis only when needed""",
    name="multi_step_agent"
)

print("Creating traces for workflow visualization...\n")

# Quick workflow
print("Test 1: Quick lookup (should be fast)")
result = quick_agent.invoke({
    "messages": [{"role": "user", "content": "Look up ID-123"}]
})
print(f"Result: {result['messages'][-1].content}\n")

# Multi-step workflow
print("Test 2: Multi-step research (shows bottleneck)")
result = multi_step_agent.invoke({
    "messages": [{
        "role": "user", 
        "content": "Research product XYZ: look it up, search for reviews, and analyze the data"
    }]
})
print(f"Result: {result['messages'][-1].content}\n")

# Simple question to multi-step agent (should not use all tools)
print("Test 3: Simple question to complex agent")
result = multi_step_agent.invoke({
    "messages": [{"role": "user", "content": "Just look up ID-456"}]
})
print(f"Result: {result['messages'][-1].content}\n")

print("=" * 50)
print("Check LangSmith for workflow visualization!")
print("Project: workflow-visualization")
print("\nThings to observe:")
print("1. Quick agent: Short, simple timeline")
print("2. Multi-step: Longer timeline, slow_analysis as bottleneck")
print("3. Simple question: Does it efficiently skip unused tools?")
print("\nUse the timeline view to see execution patterns!")
```

## Key Takeaways

- **Timelines reveal structure**: See sequential vs. parallel execution
- **Identify bottlenecks**: Long bars show where time is spent
- **Spot inefficiencies**: Loops, redundant calls, over-complicated flows
- **Compare approaches**: Side-by-side visualization of alternatives
- **Optimize informed**: Use visual patterns to guide improvements
- **Expect patterns**: Different agent types have characteristic traces

## Additional Resources

- [LangSmith Trace Visualization](https://docs.smith.langchain.com/tracing/concepts)
- [Understanding Agent Execution](https://docs.smith.langchain.com/tracing/tutorials/debugging)
- [Performance Optimization Guide](https://docs.langchain.com/oss/python/langchain/how-to/performance)
