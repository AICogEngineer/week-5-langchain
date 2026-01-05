# Message History Management

## Learning Objectives
- Understand how messages accumulate in agent state
- View and inspect conversation history
- Identify different message types and their purposes
- Manage message history for efficiency

## Why This Matters

Messages are the core of agent memory. Every user input, assistant response, and tool result becomes a message in state. Understanding how messages work—and how they accumulate—is essential for building efficient, cost-effective agents.

## The Concept

### How Messages Accumulate

Each interaction adds messages to state:

```
Turn 1:
  + User: "Hello"
  + Assistant: "Hi there!"
  
Turn 2:
  + User: "What's the weather?"
  + Assistant: (calls weather tool)
  + Tool: "72°F and sunny"
  + Assistant: "The weather is 72°F and sunny."

State now contains 6 messages
```

On each turn, the agent receives the **full history** plus the new message.

### Message Types

LangChain uses different message types:

| Type | Role | Purpose |
|------|------|---------|
| `SystemMessage` | system | Instructions to the agent |
| `HumanMessage` | user | User input |
| `AIMessage` | assistant | Agent responses and tool calls |
| `ToolMessage` | tool | Tool execution results |

```python
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

# Example conversation history
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is 2+2?"),
    AIMessage(content="Let me calculate that.", tool_calls=[...]),
    ToolMessage(content="4", tool_call_id="call_123"),
    AIMessage(content="2 + 2 equals 4.")
]
```

### Viewing Message History

Access the full conversation after invocation:

```python
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]}, config)

# View all messages
for msg in result["messages"]:
    # Using duck typing for different message formats
    if hasattr(msg, "content"):
        role = getattr(msg, "type", "unknown")
        print(f"{role}: {msg.content[:100]}...")
```

### AIMessage with Tool Calls

When an agent calls a tool, the AIMessage includes tool call information:

```python
AIMessage(
    content="",  # Often empty when calling tools
    tool_calls=[
        {
            "name": "get_weather",
            "args": {"city": "Seattle"},
            "id": "call_abc123"
        }
    ]
)
```

This is followed by a ToolMessage with the result:

```python
ToolMessage(
    content="72°F, sunny",
    tool_call_id="call_abc123"  # Matches the tool call
)
```

### Message History Growth

Messages accumulate quickly:

```
Simple Q&A turn: +2 messages (user + assistant)
Tool-using turn: +4 messages (user + AI call + tool result + AI response)
Multi-tool turn: +6 or more messages
```

After 10 turns with tool usage, you might have 40+ messages.

### Impact on Tokens

Every message is sent to the LLM on each turn:

```
Turn 1: System(50) + User(20) = 70 tokens
Turn 5: System(50) + [10 messages, 400 tokens] = 450 tokens
Turn 10: System(50) + [25 messages, 1100 tokens] = 1150 tokens
```

This affects:
- **Cost**: More tokens = more money
- **Latency**: More tokens = longer processing
- **Context limits**: Models have token limits (8K, 32K, 128K)

### Basic History Trimming

Manually trim old messages while keeping recent ones:

```python
def trim_message_history(messages, max_messages=20):
    """Keep system prompt + last N messages."""
    if len(messages) <= max_messages:
        return messages
    
    # Find system messages (usually first)
    system_msgs = [m for m in messages if getattr(m, 'type', '') == 'system']
    
    # Keep last N non-system messages
    non_system = [m for m in messages if getattr(m, 'type', '') != 'system']
    recent = non_system[-max_messages:]
    
    return system_msgs + recent
```

### Message Metadata

Messages can carry metadata:

```python
from langchain_core.messages import HumanMessage

msg = HumanMessage(
    content="Hello",
    additional_kwargs={
        "timestamp": "2024-03-15T10:30:00Z",
        "user_id": "alice"
    }
)
```

This metadata passes through the system and can be useful for debugging or filtering.

### Message Order Matters

The order of messages is significant:

```
✅ Correct order:
1. SystemMessage (instructions)
2. HumanMessage (user question)
3. AIMessage (with tool call)
4. ToolMessage (tool result)
5. AIMessage (final answer)

❌ Wrong order:
1. ToolMessage (result with no preceding call - error!)
2. AIMessage 
...
```

LangChain enforces proper ordering—tool messages must follow tool calls.

### Inspecting State Messages

Access messages directly from state:

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=checkpointer,
    name="inspectable_agent"
)

config = {"configurable": {"thread_id": "test"}}

# Run some turns
agent.invoke({"messages": [{"role": "user", "content": "Hello"}]}, config)
agent.invoke({"messages": [{"role": "user", "content": "World"}]}, config)

# Inspect
state = checkpointer.get(config)
messages = state.get("messages", [])

print(f"Total messages: {len(messages)}")
for i, msg in enumerate(messages):
    msg_type = type(msg).__name__
    content = str(msg.content)[:50]
    print(f"  {i}: {msg_type}: {content}...")
```

## Code Example

```python
"""
Message History Management Demo
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

@tool
def lookup_data(query: str) -> str:
    """Look up data in database."""
    return f"Data for '{query}': Example result"

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_data],
    checkpointer=checkpointer,
    system_prompt="You are a data assistant.",
    name="history_demo_agent"
)

config = {"configurable": {"thread_id": "history_demo"}}

# Build up some history
print("Building conversation history...\n")

# Turn 1: Simple exchange
agent.invoke({
    "messages": [{"role": "user", "content": "Hi, I need some data."}]
}, config)
print("Turn 1: User greeted agent")

# Turn 2: Tool usage
agent.invoke({
    "messages": [{"role": "user", "content": "Look up sales data"}]
}, config)
print("Turn 2: User requested data lookup (tool called)")

# Turn 3: Follow-up
result = agent.invoke({
    "messages": [{"role": "user", "content": "What about Q2 data?"}]
}, config)
print("Turn 3: User asked follow-up\n")

# Inspect the message history
print("=== Message History Inspection ===")
state = checkpointer.get(config)
messages = state.get("messages", [])

print(f"Total messages in state: {len(messages)}\n")

for i, msg in enumerate(messages):
    msg_type = type(msg).__name__
    content = str(getattr(msg, 'content', ''))
    
    # Truncate for display
    content_preview = content[:60] + "..." if len(content) > 60 else content
    
    # Check for tool calls
    tool_calls = getattr(msg, 'tool_calls', None)
    tool_info = f" [calls: {len(tool_calls)}]" if tool_calls else ""
    
    print(f"{i:2}. {msg_type:15} {tool_info}")
    print(f"    Content: {content_preview}")
    print()

# Calculate approximate token count (rough estimate)
total_chars = sum(len(str(getattr(m, 'content', ''))) for m in messages)
estimated_tokens = total_chars // 4  # Rough approximation
print(f"Estimated tokens in history: ~{estimated_tokens}")
print("(This grows with each turn!)")
```

## Key Takeaways

- **Messages accumulate**: Each turn adds 2+ messages to history
- **Full history sent each turn**: LLM sees everything on every call
- **Different message types**: System, Human, AI, Tool—each has a role
- **Tool messages link to calls**: `tool_call_id` connects them
- **Growth affects costs**: More messages = more tokens = higher costs
- **Order matters**: Messages must follow proper sequence

## Additional Resources

- [LangChain Message Types](https://docs.langchain.com/oss/python/langchain/concepts/messages)
- [Managing Conversation History](https://docs.langchain.com/oss/python/langchain/how-to/memory)
- [Message Trimming Strategies](https://docs.langchain.com/oss/python/langraph/how-to/message_history)
