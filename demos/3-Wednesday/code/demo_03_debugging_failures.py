"""
Demo 03: Debugging Failures with LangSmith

This demo shows trainees how to:
1. Identify failures in LangSmith traces
2. Debug common agent problems
3. Trace tool errors back to root causes
4. Fix issues based on trace analysis

Learning Objectives:
- Recognize failure patterns in traces
- Debug tool errors effectively
- Identify wrong tool selection issues
- Fix agent problems using trace data

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/langsmith
Last Verified: January 2026

References:
- Written Content: readings/3-Wednesday/03-debugging-with-langsmith-dashboard.md
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent

# ============================================================================
# PART 1: Tool Error Scenario
# ============================================================================

print("=" * 70)
print("PART 1: Debugging Tool Errors")
print("=" * 70)

print("""
We'll intentionally create a tool that can fail,
then trace the execution to find the error.
""")

# Tool that can fail
@tool
def divide_numbers(numerator: float, denominator: float) -> str:
    """
    Divide two numbers.
    Use when asked to divide, calculate ratios, or find percentages.
    """
    if denominator == 0:
        # Return error message instead of crashing
        raise ValueError("ERROR: Cannot divide by zero. Please provide a non-zero denominator.")
    result = numerator / denominator
    return f"{numerator} / {denominator} = {result:.4f}"

@tool
def get_data(metric_name: str) -> str:
    """
    Get a metric value from the database.
    Use when asked to retrieve, fetch, or look up metric values.
    """
    data = {
        "revenue": "1000000",
        "costs": "750000",
        "zero_metric": "0",  # This will cause issues when used as divisor
        "employees": "450"
    }
    value = data.get(metric_name.lower())
    if value is None:
        return f"ERROR: Metric '{metric_name}' not found. Available: {list(data.keys())}"
    return value

print("  Created tools: divide_numbers, get_data")

math_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[divide_numbers, get_data],
    system_prompt="""You are a financial calculator assistant.
    Use get_data to retrieve values, then divide_numbers for calculations.
    If a tool returns an ERROR, explain it to the user.""",
    name="financial_calculator_agent"
)

print("  Agent created: financial_calculator_agent")

# Scenario 1: Successful calculation
print("\n[Scenario 1] Successful calculation...")
result1 = math_agent.invoke({
    "messages": [{"role": "user", "content": "What is revenue divided by costs?"}]
})
print(f"  Query: What is revenue divided by costs?")
print(f"  Response: {result1['messages'][-1].content}")

# Scenario 2: Division by zero error
print("\n[Scenario 2] Division by zero (will cause error)...")
result2 = math_agent.invoke({
    "messages": [{"role": "user", "content": "What is revenue divided by zero_metric?"}]
})
print(f"  Query: What is revenue divided by zero_metric?")
print(f"  Response: {result2['messages'][-1].content}")

# Scenario 3: Missing data error
print("\n[Scenario 3] Missing data error...")
result3 = math_agent.invoke({
    "messages": [{"role": "user", "content": "Get the profit margin metric."}]
})
print(f"  Query: Get the profit margin metric.")
print(f"  Response: {result3['messages'][-1].content}")

# ============================================================================
# PART 2: How to Debug in LangSmith
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Debugging Workflow in LangSmith")
print("=" * 70)

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                     DEBUGGING WORKFLOW                               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. FIND THE FAILED TRACE                                            ║
║     - Look for red/error indicators in trace list                    ║
║     - Filter by time if you know when the error occurred             ║
║                                                                      ║
║  2. IDENTIFY THE FAILURE POINT                                       ║
║     - Expand the trace hierarchy                                     ║
║     - Find the step marked as failed                                 ║
║     - Could be: LLM call, tool call, or parent chain                 ║
║                                                                      ║
║  3. EXAMINE THE INPUTS                                               ║
║     - What was sent to the failing step?                             ║
║     - Was the input malformed or unexpected?                         ║
║     - Did previous steps produce bad data?                           ║
║                                                                      ║
║  4. CHECK THE OUTPUT/ERROR                                           ║
║     - Read the actual error message                                  ║
║     - Is it a code exception or graceful error return?               ║
║     - What does the error tell you about the root cause?             ║
║                                                                      ║
║  5. TRACE BACKWARDS                                                  ║
║     - If tool received bad input, check the LLM that called it       ║
║     - Why did the LLM pass that input?                               ║
║     - Was the tool description unclear?                              ║
║                                                                      ║
║  6. FIX AND VERIFY                                                   ║
║     - Apply fix (improve tool, update prompt, handle error)          ║
║     - Run same query again                                           ║
║     - Compare new trace to old trace                                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# ============================================================================
# PART 3: Wrong Tool Selection Scenario
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Debugging Wrong Tool Selection")
print("=" * 70)

print("""
Sometimes agents call the WRONG tool. Let's create a scenario
where this might happen and debug it.
""")

# Tools with potentially confusing descriptions
@tool
def tool4(name: str) -> str:
    """
    Search name.
    """
    return f"Found customer: {name} - Email: {name.lower()}@example.com"

@tool
def tool2(name: str) -> str:
    """
    Search name.
    """
    return f"Found product: {name} - Price: $99.99, Stock: 42 units"

@tool
def tool3(name: str) -> str:
    """
    Search name.
    """
    return f"Orders for {name}: Order #1234 (Shipped), Order #5678 (Processing)"

@tool
def tool1(name: str) -> str:
    """
    Search name.
    """
    return f"Address: {name}" 

search_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[tool1, tool2, tool3, tool4],
    system_prompt="""You are a customer service assistant.
    Use the appropriate search tool based on what the user is asking for.""",
    name="customer_service_agent"
)

print("  Agent created with 3 search tools")

# Query that might be ambiguous
print("\n[Scenario 4] Potentially ambiguous query...")
result4 = search_agent.invoke({
    "messages": [{"role": "user", "content": "Find John's orders"}]
})
print(f"  Query: Find John's orders")
print(f"  Response: {result4['messages'][-1].content}")

print("\n[Scenario 5] Clear customer lookup...")
result5 = search_agent.invoke({
    "messages": [{"role": "user", "content": "What is the email for customer named Sarah?"}]
})
print(f"  Query: What is the email for customer named Sarah?")
print(f"  Response: {result5['messages'][-1].content}")

result5 = search_agent.invoke({
    "messages": [{"role": "user", "content": "Do you have pie?"}]
})

result5 = search_agent.invoke({
    "messages": [{"role": "user", "content": "Do you know the muffin man?"}]
})
# ============================================================================
# PART 4: Common Debugging Patterns
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Common Issues and Solutions")
print("=" * 70)

print("""
┌────────────────────────────────────────────────────────────────────────┐
│ ISSUE                          │ WHAT TO LOOK FOR IN TRACE │ FIX    │
├────────────────────────────────┼───────────────────────────┼────────┤
│ Tool returns error             │ ERROR in tool output      │ Handle │
│                                │                           │ in tool│
├────────────────────────────────┼───────────────────────────┼────────┤
│ Wrong tool called              │ Check LLM reasoning       │ Improve│
│                                │ Usually tool description  │ desc   │
│                                │ was unclear               │        │
├────────────────────────────────┼───────────────────────────┼────────┤
│ Agent ignores tools            │ LLM output has no         │ Update │
│                                │ tool_calls                │ prompt │
├────────────────────────────────┼───────────────────────────┼────────┤
│ Tool called with wrong params  │ Check tool_call input     │ Fix    │
│                                │                           │ types  │
├────────────────────────────────┼───────────────────────────┼────────┤
│ Infinite tool loop             │ Same tool called          │ Add    │
│                                │ repeatedly                │ exit   │
│                                │                           │ cond   │
├────────────────────────────────┼───────────────────────────┼────────┤
│ Token limit exceeded           │ Trace shows truncation    │ Summa- │
│                                │ or failure                │ rize   │
└────────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
# PART 5: Debugging Exercise
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Debugging Exercise")
print("=" * 70)

print("""
EXERCISE: Debug the following scenarios in LangSmith

1. Find the trace for "division by zero_metric"
   - Which tool returned an error?
   - What was the error message?
   - How did the agent handle it?

2. Find the trace for "John's orders"
   - Which search tool was called?
   - Was it the correct choice?
   - Would you improve the tool descriptions?

3. Compare successful vs failed traces
   - What's different about the execution flow?
   - How many LLM calls in each?
   - What patterns do you notice?
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Debugging Failures")
print("=" * 70)

print("""
Key Takeaways:

1. Tool errors show in trace output - look for ERROR messages
2. Wrong tool selection is visible in LLM reasoning
3. Trace backwards from failure to find root cause
4. Improve tool descriptions to fix wrong tool selection
5. Add error handling in tools to prevent crashes

Debugging Workflow:
1. Find failed trace
2. Identify failure point
3. Examine inputs/outputs
4. Trace backwards to root cause
5. Apply fix and verify
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. How to find error traces in LangSmith (red indicators)
2. Expanding traces to find the exact failure point
3. Comparing successful vs failed traces side-by-side
4. How tool descriptions affect agent decisions

Live Demo Tips:
- Have both failed and successful traces ready
- Walk through the debugging workflow step by step
- Show how fixing a tool description changes behavior

Discussion Questions:
- "What would you do if the agent kept calling the same tool?"
- "How would you improve search_products description?"
- "When should a tool return an error vs raise an exception?"

Exercise:
Have trainees find a bug in their own agent and 
use LangSmith to debug it.
""")

print("=" * 70)
