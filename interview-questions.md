# Interview Questions: Week 5 - LangChain v1.0

> **Assessment Focus**: From Basics to Production: Mastering LangChain v1.0 Agent Development

---

## Beginner (Foundational) – 70%

### Q1: What is the `create_agent()` function and why is it the standard for building agents in LangChain v1.0?

**Keywords:** create_agent, langchain.agents, simplicity, helper function, v1.0 standard

<details>
<summary>Click to Reveal Answer</summary>

`create_agent()` is a high-level helper function from `langchain.agents` that is the standard way to create agents in LangChain v1.0. It follows the "simplicity first" philosophy—letting you create a fully functional agent in just 4-5 lines of code. It handles tool calling, state management, and message history automatically without requiring manual LangGraph configuration.

</details>

---

### Q2: What is the purpose of the `@tool` decorator in LangChain v1.0?

**Keywords:** @tool, langchain_core.tools, function, agent-callable, docstring

<details>
<summary>Click to Reveal Answer</summary>

The `@tool` decorator from `langchain_core.tools` makes any Python function callable by an agent. The decorator transforms the function into a tool that the agent can invoke during its reasoning process. The **docstring is critical** because it tells the agent when and how to use the tool.

</details>

---

### Q3: What is the purpose of the `init_chat_model()` helper function?

**Keywords:** init_chat_model, provider string, unified interface, model initialization

<details>
<summary>Click to Reveal Answer</summary>

`init_chat_model()` is a helper function that provides a unified interface for initializing chat models across different providers. It uses a simple string format like `"openai:gpt-4o-mini"` or `"bedrock:anthropic.claude-3-5-sonnet"` to abstract away provider-specific setup, giving you a consistent API regardless of which LLM provider you use.

</details>

---

### Q4: Why is the `name` parameter required when calling `create_agent()`?

**Keywords:** name, debugging, tracing, LangSmith, multi-agent

<details>
<summary>Click to Reveal Answer</summary>

The `name` parameter is required for:
1. **Debugging** - Identify which agent produced which output
2. **LangSmith Tracing** - Filter traces by agent name in the dashboard
3. **Multi-Agent Systems** - Know which agent is currently acting
4. **Logging** - Maintain clear audit trails

Names should use snake_case and be descriptive (e.g., `"customer_support_agent"`).

</details>

---

### Q5: What is an `InMemorySaver` and what is its purpose?

**Keywords:** InMemorySaver, checkpointer, memory, langgraph.checkpoint.memory, development

<details>
<summary>Click to Reveal Answer</summary>

`InMemorySaver` is a checkpointer from `langgraph.checkpoint.memory` that enables agent memory by storing state in RAM. It saves and loads conversation state between turns, allowing multi-turn conversations. It's ideal for **development and testing** because it requires no setup, but data is lost when the application restarts—making it unsuitable for production.

</details>

---

### Q6: How do you invoke an agent and access its response in LangChain v1.0?

**Keywords:** invoke, messages, role, user, content, result

<details>
<summary>Click to Reveal Answer</summary>

You invoke an agent by passing a dictionary with a `messages` list:

```python
result = agent.invoke({
    "messages": [{"role": "user", "content": "Hello!"}]
})
```

The response is accessed via `result["messages"][-1].content`, which gets the content of the last message (the agent's reply).

</details>

---

### Q7: What is a `thread_id` and how does it enable multiple conversations?

**Keywords:** thread_id, configurable, config, isolation, conversation state

<details>
<summary>Click to Reveal Answer</summary>

A `thread_id` is a unique identifier passed in the config that isolates conversation state. Each unique `thread_id` maintains independent memory, allowing multiple simultaneous conversations:

```python
config = {"configurable": {"thread_id": "user_123"}}
result = agent.invoke({"messages": [...]}, config)
```

Different `thread_id` values = different conversation histories.

</details>

---

### Q8: Name two deprecated patterns that were removed in LangChain v1.0.

**Keywords:** LCEL, create_react_agent, deprecated, v0.x

<details>
<summary>Click to Reveal Answer</summary>

1. **LCEL (LangChain Expression Language)** - The pipe operator chains (`prompt | llm | parser`) have been deprecated and removed
2. **`create_react_agent`** - The old agent creation function has been replaced by `create_agent()`

Other deprecated items include `ConversationBufferMemory`, `initialize_agent()`, and `RunnableWithMessageHistory`.

</details>

---

### Q9: What environment variables are needed to enable LangSmith tracing?

**Keywords:** LANGSMITH_TRACING, LANGSMITH_API_KEY, LANGSMITH_PROJECT, environment

<details>
<summary>Click to Reveal Answer</summary>

Three environment variables enable LangSmith tracing:
1. `LANGSMITH_TRACING=true` - Activates automatic tracing
2. `LANGSMITH_API_KEY=<your-key>` - Authentication key
3. `LANGSMITH_PROJECT=<project-name>` - Groups traces by project

Once set, LangSmith automatically traces all LangChain operations without code changes.

</details>

---

### Q10: What are the four core components of LangChain v1.0?

**Keywords:** Models, Tools, Agents, Memory

<details>
<summary>Click to Reveal Answer</summary>

The four fundamental building blocks are:
1. **Models** - Chat models, LLM calls, embeddings (via `init_chat_model()`)
2. **Tools** - Functions decorated with `@tool` that agents can call
3. **Agents** - Autonomous systems created with `create_agent()` that reason and act
4. **Memory** - Checkpointers like `InMemorySaver` for state persistence

</details>

---

### Q11: What is the difference between `.invoke()`, `.batch()`, and `.stream()` methods?

**Keywords:** invoke, batch, stream, parallel, real-time, single request

<details>
<summary>Click to Reveal Answer</summary>

| Method | Use Case |
|--------|----------|
| `.invoke()` | Single synchronous request—blocks until complete response |
| `.batch()` | Multiple requests processed in parallel—much faster than sequential invoke calls |
| `.stream()` | Real-time token streaming—yields chunks as they're generated |

Use `.batch()` when processing multiple independent inputs. Use `.stream()` for chat UIs where perceived responsiveness matters.

</details>

---

### Q12: What is Pydantic and how is it used for structured output in LangChain v1.0?

**Keywords:** Pydantic, BaseModel, schema, structured output, validation

<details>
<summary>Click to Reveal Answer</summary>

Pydantic is a data validation library that defines output schemas using Python classes. In LangChain v1.0, you create a `BaseModel` subclass to specify the structure you expect, then use `.with_structured_output()`:

```python
from pydantic import BaseModel

class Sentiment(BaseModel):
    score: float
    label: str

result = model.with_structured_output(Sentiment).invoke([...])
```

This ensures the model returns validated, typed data instead of free-form text.

</details>

---

### Q13: What is the difference between "state" and "store" in LangChain's context engineering?

**Keywords:** state, store, session, cross-conversation, persistence

<details>
<summary>Click to Reveal Answer</summary>

| Data Source | Scope | Examples |
|------------|-------|----------|
| **State** | Current conversation session | Messages, temporary flags, session data |
| **Store** | Cross-conversation (long-term) | User preferences, memories, historical data |

State is ephemeral (session-scoped), while store persists across multiple conversations with the same user.

</details>

---

### Q14: When should you use `SqliteSaver` instead of `InMemorySaver`?

**Keywords:** SqliteSaver, persistence, production, InMemorySaver, restarts

<details>
<summary>Click to Reveal Answer</summary>

Use `SqliteSaver` when you need **persistence across application restarts**. `InMemorySaver` stores data in RAM, so it's lost when the process ends. `SqliteSaver` writes to a local SQLite database file, preserving conversation history between restarts:

```python
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
```

For enterprise production, use `PostgresSaver` or cloud database options.

</details>

---

### Q15: What makes a good tool description for agent routing?

**Keywords:** docstring, description, routing, when to use, specific

<details>
<summary>Click to Reveal Answer</summary>

A good tool description should:
1. **Be specific** about what the tool does
2. **State when to use it** (e.g., "Use for order lookups")
3. **State when NOT to use it** (e.g., "NOT for refund requests")
4. **Describe parameters** clearly

Example:
```python
@tool
def search_orders(order_id: str) -> str:
    """Look up order status by order ID.
    Use when customer asks about order status or tracking.
    DO NOT use for returns—use create_ticket instead."""
```

</details>

---

### Q16: What is the "agentic loop" pattern that agents follow?

**Keywords:** observe, reason, act, tool call, loop, Reasoning and Acting

<details>
<summary>Click to Reveal Answer</summary>

The agentic loop (ReAct pattern) is:
1. **Observe** - Receive user message and conversation history
2. **Reason** - Decide what to do next
3. **Act** - Either call a tool OR generate a response
4. **Repeat** - If tool was called, add result and return to step 1

This loop continues until the agent decides to respond directly instead of calling another tool.

</details>

---

### Q17: How do you add metadata to LangSmith traces for filtering?

**Keywords:** metadata, tags, config, filtering, LangSmith

<details>
<summary>Click to Reveal Answer</summary>

Pass metadata and tags in the config when invoking:

```python
result = agent.invoke(
    {"messages": [...]},
    config={
        "metadata": {
            "user_id": "user_123",
            "request_type": "order_inquiry"
        },
        "tags": ["production", "high-priority"]
    }
)
```

You can then filter traces in the LangSmith dashboard by these values.

</details>

---

## Intermediate (Application) – 25%

### Q18: You want your agent to remember conversations but your application restarts frequently. How would you upgrade from `InMemorySaver` to persistent storage?

**Hint:** Think about the different checkpointer options for development vs. production.

<details>
<summary>Click to Reveal Answer</summary>

Replace `InMemorySaver` with `SqliteSaver` for local persistence:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[...],
    checkpointer=checkpointer,  # Persists across restarts
    name="persistent_agent"
)
```

For production, use `PostgresSaver` or `DynamoDBSaver` for database-backed persistence.

</details>

---

### Q19: Your RAG agent is searching the knowledge base for simple greetings like "Hi, how are you?" How would you configure it to only search when necessary?

**Hint:** Consider the difference between 2-Step RAG and Agentic RAG.

<details>
<summary>Click to Reveal Answer</summary>

Use **Agentic RAG** instead of 2-Step RAG. Update the system prompt to give the agent autonomy:

```python
system_prompt = """You have access to search_knowledge_base.
- Use search for product questions, policies, or technical info
- For greetings or general chat, respond directly without searching
- If you search and find nothing relevant, say so clearly"""
```

The tool description should also clarify when to use it (e.g., "NOT for general knowledge questions").

</details>

---

### Q20: Your agent has multiple tools but keeps choosing the wrong one. What should you check and how would you improve tool selection?

**Hint:** The docstring is critical for agent routing.

<details>
<summary>Click to Reveal Answer</summary>

Check and improve the **tool docstrings**. Agents use docstrings to decide which tool to call:

```python
@tool
def search_orders(order_id: str) -> str:
    """Look up order status by order ID.
    
    Use when customer asks about:
    - Order status or tracking
    - Delivery estimates
    - Order history
    
    DO NOT use for returns or refunds (use create_ticket instead)."""
```

Best practices:
- Be specific about when to use the tool
- Mention what NOT to use it for
- Test tools independently before integration

</details>

---

### Q21: You're building a customer support system with both a support agent and a sales agent. What pattern would you use to coordinate them?

**Hint:** Consider the supervisor/tool-calling pattern for multi-agent systems.

<details>
<summary>Click to Reveal Answer</summary>

Use the **supervisor (tool-calling) pattern**. Create sub-agents and wrap them as tools for a supervisor:

```python
# 1. Create sub-agents
support_agent = create_agent(..., name="support_agent")
sales_agent = create_agent(..., name="sales_agent")

# 2. Wrap as tools
@tool
def handle_support_ticket(request: str) -> str:
    """Handle customer support issues."""
    result = support_agent.invoke({...})
    return result["messages"][-1].content

@tool  
def handle_sales_inquiry(request: str) -> str:
    """Handle sales and product questions."""
    result = sales_agent.invoke({...})
    return result["messages"][-1].content

# 3. Create supervisor
supervisor = create_agent(
    tools=[handle_support_ticket, handle_sales_inquiry],
    name="supervisor_agent"
)
```

</details>

---

### Q22: You need to process 100 customer reviews and analyze sentiment for each. How would you optimize this for performance?

**Hint:** Think about invocation patterns for multiple independent requests.

<details>
<summary>Click to Reveal Answer</summary>

Use `.batch()` instead of calling `.invoke()` 100 times in a loop:

```python
model = init_chat_model("openai:gpt-4o-mini")

# Prepare all reviews as separate message lists
review_prompts = [
    [{"role": "user", "content": f"Analyze sentiment: {review}"}]
    for review in reviews
]

# Process all at once - parallel execution
results = model.batch(review_prompts, config={"max_concurrency": 10})
```

This is significantly faster because requests run in parallel instead of sequentially.

</details>

---

### Q23: Your LangSmith trace shows an agent making 15 LLM calls before completing a simple task. How do you diagnose this issue?

**Hint:** Look for repeating patterns in the trace timeline.

<details>
<summary>Click to Reveal Answer</summary>

Diagnose in LangSmith:
1. View the trace timeline to identify repeating patterns
2. Click on each LLM call to see what the model decided
3. Check if the agent is looping between the same tools

Common causes:
- **Circular tool dependencies** - Tool A's output triggers Tool B, which triggers Tool A
- **No clear stopping condition** - System prompt doesn't guide when to stop
- **Ambiguous tool combination** - Agent can't decide which tool to use

Fixes: Improve system prompt stopping conditions, add loop detection, or clarify tool boundaries.

</details>

---

### Q24: You need your agent to return a structured JSON object with specific fields. How do you ensure reliable, validated output?

**Hint:** Think about Pydantic and `.with_structured_output()`.

<details>
<summary>Click to Reveal Answer</summary>

Use Pydantic models with `.with_structured_output()`:

```python
from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Price in USD")
    in_stock: bool = Field(description="Availability status")

model = init_chat_model("openai:gpt-4o-mini")

result = model.with_structured_output(ProductInfo).invoke([
    {"role": "user", "content": "Tell me about Widget Pro"}
])

# result is a validated ProductInfo object
print(result.name)   # Typed access
print(result.price)  # Guaranteed float
```

Pydantic validates that the output matches the schema, raising an error if it doesn't.

</details>

---

## Advanced (Deep Dive) – 5%

### Q25: In a multi-agent supervisor pattern, your sub-agents are completing their work but the supervisor is receiving empty or incomplete responses. What is likely happening and how do you fix it?

<details>
<summary>Click to Reveal Answer</summary>

This is a common "context engineering" failure: sub-agents perform tool calls or reasoning internally but don't include the results in their **final message**. The supervisor only sees the final output, not intermediate steps.

**Fix:** Update the sub-agent's system prompt to emphasize final output:

```python
system_prompt = """You are a specialist agent.

CRITICAL: The supervisor ONLY sees your final message.
Include ALL results, findings, and details in your final response.
Do not assume the supervisor knows what you did internally."""
```

This ensures sub-agents summarize their work in a way the supervisor can use.

</details>

---

## Scoring Guide

| Level | Questions | Target Correct |
|-------|-----------|----------------|
| Beginner | Q1-Q17 (17 questions) | 12+ correct |
| Intermediate | Q18-Q24 (7 questions) | 4+ correct |
| Advanced | Q25 (1 question) | Bonus |

**Passing Score**: 16+ correct across all levels demonstrates solid Week 5 comprehension.

---

## Topics Covered

| Day | Topics Tested |
|-----|--------------|
| Monday | AWS Bedrock, `init_chat_model()`, invocation patterns (invoke/batch/stream), v1.0 architecture |
| Tuesday | `@tool` decorator, `create_agent()`, agent naming, tool descriptions, agentic loop |
| Wednesday | LangSmith tracing, environment variables, dashboard debugging, trace metadata |
| Thursday | `InMemorySaver`, checkpointers, `thread_id`, state vs store, persistence options |
| Friday | Pydantic structured output, RAG tools, agentic RAG patterns, error handling |
