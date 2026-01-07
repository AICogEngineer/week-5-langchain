"""
Demo 02: Agent Creation with create_agent()

This demo shows trainees how to:
1. Create agents using create_agent() - the v1.0 standard
2. Connect tools to agents
3. Use system prompts to guide agent behavior
4. Always include the name parameter

Learning Objectives:
- Master the create_agent() function
- Understand the importance of agent naming
- See how agents decide which tools to call

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: January 2026

References:
- Written Content: readings/2-Tuesday/03-simple-agent-creation.md

CRITICAL v1.0 PATTERNS:
- Use create_agent() from langchain.agents
- ALWAYS include name parameter
- NO LCEL chains or create_react_agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent

# ============================================================================
# PART 1: Basic Agent Creation
# ============================================================================

print("=" * 70)
print("PART 1: Basic Agent Creation with create_agent()")
print("=" * 70)

print("""
create_agent() is the LangChain v1.0 standard for building agents.

Key parameters:
- model: Provider string (e.g., "openai:gpt-4o-mini")
- tools: List of @tool decorated functions
- system_prompt: Optional instructions for the agent
- name: REQUIRED for debugging and tracing
""")

# Create some tools for the agent
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city. Use when asked about weather conditions."""
    # Simulated response
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Rainy, 55°F",
        "tokyo": "Cloudy, 68°F",
        "paris": "Partly cloudy, 65°F"
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")

@tool
def get_time(timezone: str) -> str:
    """Get the current time in a timezone. Use when asked about time."""
    # Simulated response
    times = {
        "est": "3:00 PM EST",
        "pst": "12:00 PM PST",
        "gmt": "8:00 PM GMT",
        "jst": "5:00 AM JST"
    }
    return times.get(timezone.lower(), f"Time data not available for {timezone}")

print("\n[Step 1] Creating a simple agent with tools...")

# THE v1.0 STANDARD: create_agent() with name parameter
simple_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather, get_time],
    system_prompt="You are a helpful assistant that provides weather and time information.",
    name="weather_time_agent"  # ALWAYS include this!
)

print("Agent created successfully!")
print(f"  Model: openai:gpt-4o-mini")
print(f"  Tools: get_weather, get_time")
print(f"  Name: weather_time_agent")

# ============================================================================
# PART 2: Agent Invocation
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Invoking the Agent")
print("=" * 70)

print("\n[Step 2] Testing agent with weather query...")

# Invoke the agent
result = simple_agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in New York?"}]
})

# Extract the response
response = result["messages"][-1].content
print(f"  User: What's the weather in New York?")
print(f"  Agent: {response}")

print("\n[Step 3] Testing agent with time query...")

result = simple_agent.invoke({
    "messages": [{"role": "user", "content": "What time is it in Tokyo (JST)?"}]
})

response = result["messages"][-1].content
print(f"  User: What time is it in Tokyo?")
print(f"  Agent: {response}")

# ============================================================================
# PART 3: The Importance of Agent Naming
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Why Agent Names Matter")
print("=" * 70)

print("""
The 'name' parameter is REQUIRED for:

1. DEBUGGING: Identify which agent produced which output
2. LANGSMITH TRACING: Filter traces by agent name
3. MULTI-AGENT SYSTEMS: Know which agent is acting
4. LOGGING: Clear audit trails

Naming conventions:
- Use snake_case: "weather_agent", "customer_support_bot"
- Be descriptive: "order_processing_agent", not "agent1"
- Keep it unique within your system
""")

print("\n[Step 4] Demonstrating naming importance...")

# Create multiple agents with different names
agent_support = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt="You help with customer support issues.",
    name="customer_support_agent"
)

agent_sales = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt="You help with sales inquiries.",
    name="sales_assistant_agent"
)

print("  Created agents:")
print("    - customer_support_agent")
print("    - sales_assistant_agent")
print("\n  In LangSmith, you can filter traces by these names!")

# ============================================================================
# PART 4: System Prompts Guide Behavior
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: System Prompts Guide Agent Behavior")
print("=" * 70)

print("""
System prompts tell the agent:
- What role to play
- How to respond
- When to use tools
- What to avoid
""")

# Create agents with different personalities
@tool
def lookup_info(topic: str) -> str:
    """Look up information about a topic. Use for any knowledge queries."""
    return f"Information about {topic}: This is sample data for demonstration."

formal_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_info],
    system_prompt="""You are a formal business assistant. 
    Use professional language and be concise.
    Always address the user respectfully.""",
    name="formal_business_agent"
)

#BURN THIS
casual_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_info],
    system_prompt="""You are a friendly casual assistant.
    Use only EMOJIs to answer the query""",
    name="casual_friendly_agent"
)

print("\n[Step 5] Comparing agent personalities...")

query = {"messages": [{"role": "user", "content": "Tell me about Python programming."}]}

print("\n  Testing formal agent:")
formal_result = formal_agent.invoke(query)
print(f"    {formal_result['messages'][-1].content[:200]}...")

print("\n  Testing casual agent:")
casual_result = casual_agent.invoke(query)
print(f"    {casual_result['messages'][-1].content[:200]}...")

# ============================================================================
# PART 5: What NOT to Do - Deprecated Patterns
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Deprecated Patterns to AVOID")
print("=" * 70)

print("""
❌ WRONG - create_react_agent (deprecated in v1.0):
   from langchain.agents import create_react_agent
   agent = create_react_agent(llm, tools, prompt)

❌ WRONG - LCEL chains (deprecated and removed):
   chain = prompt | llm | tools

❌ WRONG - Missing name parameter:
   agent = create_agent(model="openai:gpt-4o-mini", tools=[])  # No name!

❌ WRONG - initialize_agent (removed):
   from langchain.agents import initialize_agent

✅ CORRECT - create_agent() with all required parameters:
   from langchain.agents import create_agent
   
   agent = create_agent(
       model="openai:gpt-4o-mini",
       tools=[my_tool],
       system_prompt="Instructions here.",
       name="my_agent_name"  # ALWAYS include!
   )
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Agent Creation with create_agent()")
print("=" * 70)

print("""
Key Takeaways:

1. create_agent() is the v1.0 standard - always use it
2. ALWAYS include the name parameter
3. Provider string format: "provider:model-name"
4. System prompts guide agent behavior and personality
5. Avoid deprecated patterns (create_react_agent, LCEL, etc.)
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The simplicity of create_agent() vs old patterns
2. How names appear in LangSmith traces (if available)
3. How system prompts change agent responses

Live Demo Tips:
- Show the same query to formal vs casual agents
- Have trainees suggest different system prompts
- Demonstrate tool selection with varied queries

Discussion Questions:
- "What makes a good agent name?"
- "How would you structure a system prompt for a refund agent?"
- "When would you need multiple agents?"

Common Mistakes:
- Forgetting the name parameter
- Using deprecated create_react_agent
- Vague system prompts that don't guide behavior
""")

print("=" * 70)
