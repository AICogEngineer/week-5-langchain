# Exercise 02: Your First Agent

## Overview

Now that you have working tools, it's time to build your first agent! You'll combine the tools from Exercise 01 into a cohesive productivity assistant using `create_agent()`.

## Learning Objectives

- Use `create_agent()` with the required `name` parameter
- Write effective system prompts for agents
- Configure agents with multiple tools
- Invoke agents and process responses

## The Scenario

The development team loved your tools! Now they want a complete assistant that:
1. Understands natural language requests
2. Decides which tool(s) to use
3. Provides helpful responses
4. Remembers the conversation context

## Your Tasks

### Task 1: Agent Creation (25 min)

Implement `create_productivity_agent()` in the starter code:
- Use `create_agent()` from `langchain.agents`
- Include all three tools from Exercise 01
- Write a system prompt that defines the assistant's role
- **CRITICAL**: Include the `name` parameter

> **Hint**: The system prompt should explain what the assistant does and when to use each tool.

### Task 2: System Prompt Design (15 min)

Design an effective system prompt:
- Define the assistant's persona
- Explain its capabilities
- Guide tool usage decisions
- Set response tone and format

### Task 3: Agent Testing (25 min)

Implement `test_agent()`:
- Send test messages that should trigger each tool
- Verify the agent chooses the correct tools
- Handle cases where the agent doesn't need tools

Test scenarios:
1. "How do I configure the API rate limiting?" (should use search_docs)
2. "This task involves adding a new endpoint with validation" (should use calculate_story_points)
3. "Is the payment service running?" (should use check_service_status)
4. "Hello, who are you?" (should NOT use any tools)

### Task 4: Response Processing (15 min)

Implement `process_agent_response()`:
- Extract the final response content
- Format it for display
- Handle error cases

## Definition of Done

- [_] Agent created with `create_agent()` and `name` parameter
- [_] System prompt clearly defines agent behavior
- [_] Agent correctly routes to appropriate tools
- [_] All test scenarios produce expected behavior
- [_] Responses are properly formatted

## Testing Your Solution

```bash
cd exercises/2-Tuesday/starter_code
python exercise_02_starter.py
```

Expected output format:
```
=== Productivity Agent Test ===

[INFO] Creating agent...
[OK] Agent 'productivity_assistant' created

=== Test Scenario 1: Documentation Query ===
User: "How do I configure the API rate limiting?"
[INFO] Agent is thinking...
[TOOL] Called: search_docs
[OK] Response: Here's what I found about API rate limiting...

=== Test Scenario 2: Story Points ===
User: "Estimate points for adding a payment endpoint"
[INFO] Agent is thinking...
[TOOL] Called: calculate_story_points
[OK] Response: I estimate this task at 5 story points...

=== Test Scenario 3: No Tool Needed ===
User: "Hello, who are you?"
[INFO] Agent is thinking...
[OK] Response: I'm your productivity assistant...

=== All Tests Complete ===
```

## Key Patterns

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_docs, calculate_story_points, check_service_status],
    system_prompt="""You are a productivity assistant for developers.

Your capabilities:
- Search documentation when users ask "how to" questions
- Estimate story points for development tasks
- Check service status when users ask about system health

Be concise and helpful in your responses.""",
    name="productivity_assistant"  # ALWAYS include name!
)

# Invoke the agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "How do I set up OAuth?"}]
})

# Get the response
response = result["messages"][-1].content
```

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Missing `name` | Breaks tracing/debugging | Always provide `name` |
| Vague system prompt | Agent makes poor tool choices | Be specific about when to use each tool |
| No error handling | Agent crashes on tool failures | Wrap tool calls in try/except |
| Ignoring context | Agent forgets previous turns | Use checkpointer for memory |

## Stretch Goals (Optional)

1. Add conversation memory using `InMemorySaver`
2. Implement multi-turn conversations
3. Add a fallback response for unknown queries
4. Log tool calls for debugging
