# Monitoring Token Usage and Costs

## Learning Objectives
- Understand how token usage affects costs
- Track token consumption in LangSmith
- Estimate and monitor costs across projects
- Implement strategies to optimize token usage

## Why This Matters

LLM API calls cost money—and costs can add up quickly. An inefficient agent that uses 10x more tokens than necessary costs 10x more to run. In production, unmonitored costs can become budget surprises.

LangSmith gives you visibility into token usage so you can optimize before costs become problems.

## The Concept

### How LLM Pricing Works

LLM providers charge per token (roughly 4 characters or 0.75 words):

| Provider/Model | Input Cost (per 1M tokens) | Output Cost (per 1M tokens) |
|----------------|---------------------------|----------------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

**Key insight**: Output tokens often cost more than input tokens, and smaller models are dramatically cheaper.

### Token Breakdown in Traces

Every trace in LangSmith shows token usage:

```
Run: my_agent (2.1s)
├── Total Tokens: 1,247
│   ├── Input: 892 tokens
│   └── Output: 355 tokens
├── Estimated Cost: $0.0156
└── Cost Breakdown:
    ├── LLM Call 1: 523 tokens ($0.0082)
    ├── LLM Call 2: 412 tokens ($0.0051)
    └── LLM Call 3: 312 tokens ($0.0023)
```

### Viewing Token Metrics

In the LangSmith dashboard:

1. **Per-trace view**: Click any trace to see total tokens
2. **Project aggregate**: See total usage in project settings
3. **Time-based analysis**: Filter by date range the check usage trends

### What Consumes Tokens

Understanding where tokens go:

| Component | Token Cost | Notes |
|-----------|------------|-------|
| System prompt | Input each LLM call | Repeated every call |
| User message | Input | Usually small |
| Conversation history | Input | Grows over time |
| Tool descriptions | Input each call | Adds up with many tools |
| Tool results | Input | Can be large |
| Model responses | Output (expensive) | Varies by task |

### Calculating Costs

```python
# Simple cost calculation
def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Estimate cost for a given model and token count."""
    pricing = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
    }
    
    rates = pricing.get(model, {"input": 0, "output": 0})
    
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    
    return input_cost + output_cost

# Example
cost = estimate_cost(1000, 500, "gpt-4o-mini")
print(f"Estimated cost: ${cost:.6f}")  # $0.000450
```

### Tracking Costs in LangSmith

LangSmith automatically estimates costs when possible:

```
Project: my-agent-prod
Period: Last 7 days
─────────────────────────────
Total Runs: 15,234
Total Tokens: 12.4M
Estimated Cost: $156.78
─────────────────────────────
Daily Average: 1.77M tokens ($22.40)
Peak Day: Monday (2.3M tokens)
```

### Cost Optimization Strategies

#### 1. Use Smaller Models When Possible

```python
# For simple tasks, use cheaper models
simple_agent = create_agent(
    model="openai:gpt-4o-mini",  # Much cheaper
    tools=[...],
    name="simple_task_agent"
)

# For complex reasoning, use capable models
complex_agent = create_agent(
    model="openai:gpt-4o",  # More capable
    tools=[...],
    name="complex_task_agent"
)
```

#### 2. Optimize System Prompts

```python
# ❌ Verbose prompt (many tokens every call)
system_prompt = """
You are an advanced AI assistant designed to help users with their questions.
You should always be polite, helpful, and informative. When answering questions,
try to provide comprehensive responses that fully address the user's needs.
If you don't know something, it's okay to say so. Remember to be concise but
thorough in your explanations. You have access to various tools that can help
you answer questions more accurately. Please use them wisely.
"""

# ✅ Concise prompt (fewer tokens)
system_prompt = """You are a helpful assistant. Use tools when needed. 
Be accurate and concise."""
```

#### 3. Manage Conversation History

Conversation history grows with each turn. Use summarization (covered in Week 6) or trim old messages:

```python
# Manual trimming example
def trim_messages(messages, max_messages=10):
    """Keep only the most recent messages."""
    if len(messages) <= max_messages:
        return messages
    
    # Always keep system message + last N
    system = [m for m in messages if m.get("role") == "system"]
    recent = messages[-max_messages:]
    return system + recent
```

#### 4. Optimize Tool Descriptions

```python
# ❌ Too verbose
@tool
def search_database(query: str) -> str:
    """
    This tool allows you to search our comprehensive database system
    for information about products, customers, orders, and more.
    The database contains millions of records spanning multiple years.
    You can search by any keyword and the tool will return relevant
    matches sorted by relevance score.
    [... 100 more words ...]
    """

# ✅ Concise but clear
@tool
def search_database(query: str) -> str:
    """Search products/customers/orders. Returns top 5 matches."""
```

#### 5. Limit Tool Response Size

```python
@tool
def search_documents(query: str) -> str:
    """Search documents and return summaries."""
    results = db.search(query)
    
    # Don't return full documents
    summaries = [r.summary[:200] for r in results[:5]]
    return "\n".join(summaries)
```

### Setting Up Cost Alerts

While LangSmith doesn't have built-in alerts, you can build your own:

```python
from langsmith import Client

def check_daily_costs(project: str, max_cost: float = 50.0):
    """Check if daily costs exceed threshold."""
    client = Client()
    
    # Get today's runs
    runs = client.list_runs(
        project_name=project,
        start_time=datetime.now().replace(hour=0, minute=0),
    )
    
    total_tokens = sum(r.total_tokens or 0 for r in runs)
    estimated_cost = total_tokens * 0.000001 * 2.50  # Rough estimate
    
    if estimated_cost > max_cost:
        print(f"⚠️ ALERT: Daily cost ${estimated_cost:.2f} exceeds ${max_cost}")
    
    return estimated_cost
```

## Code Example

```python
"""
Token Usage and Cost Monitoring Demo
LangChain Version: v1.0+
"""
import os
from langchain.agents import create_agent
from langchain_core.tools import tool

os.environ["LANGSMITH_PROJECT"] = "cost-monitoring-demo"

# Verbose tool (high token usage)
@tool
def verbose_search(query: str) -> str:
    """
    Search the knowledge base for information matching the query.
    Returns detailed results with full context and metadata.
    """
    return f"""
    Search Results for: {query}
    ─────────────────────────────
    Result 1: Comprehensive information about {query}. This includes 
    extensive details, background context, related topics, and 
    supplementary information that might be useful for understanding
    the full picture. The database record shows...
    
    Result 2: Additional context about {query}. Historical data
    indicates various patterns and trends that are noteworthy...
    
    (Imagine this continues for many more paragraphs)
    """

# Concise tool (efficient token usage)
@tool
def concise_search(query: str) -> str:
    """Search KB. Returns top 3 brief summaries."""
    return f"Found: 1) {query} overview. 2) {query} specs. 3) {query} pricing."

# Create two agents for comparison
verbose_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[verbose_search],
    system_prompt="""You are a helpful assistant. When users ask questions,
    search for information and provide comprehensive, detailed responses
    that fully address their needs with context and examples.""",
    name="verbose_agent"
)

concise_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[concise_search],
    system_prompt="You are a helpful assistant. Be accurate and brief.",
    name="concise_agent"
)

# Same question to both
question = "Tell me about widgets"

print("Testing verbose agent...")
result1 = verbose_agent.invoke({
    "messages": [{"role": "user", "content": question}]
})

print("\nTesting concise agent...")
result2 = concise_agent.invoke({
    "messages": [{"role": "user", "content": question}]
})

print("\n" + "=" * 50)
print("Check LangSmith to compare token usage!")
print("Project: cost-monitoring-demo")
print("\nCompare the two traces:")
print("- verbose_agent: Higher token count, more expensive")
print("- concise_agent: Lower token count, cheaper")
print("\nThis difference multiplies over thousands of calls!")
```

## Key Takeaways

- **Tokens = money**: Every token costs, input and output priced differently
- **LangSmith tracks usage**: See tokens per trace, per project, over time
- **Smaller models save money**: GPT-4o-mini is ~16x cheaper than GPT-4o
- **Optimize prompts**: Shorter system prompts reduce costs
- **Control tool verbosity**: Concise tool descriptions and responses
- **Monitor trends**: Track costs over time to catch issues early

## Additional Resources

- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [LangSmith Analytics](https://docs.smith.langchain.com/tracing/tutorials/analytics)
