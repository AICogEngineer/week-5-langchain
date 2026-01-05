"""
Demo 02: Trace Exploration

This demo shows trainees how to:
1. Generate meaningful traces for exploration
2. Understand trace hierarchies
3. Navigate the LangSmith dashboard
4. Analyze agent execution flow

Learning Objectives:
- Read and interpret LangSmith traces
- Understand parent-child relationships in traces
- Track execution flow through complex agents

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/langsmith
Last Verified: January 2026

References:
- Written Content: readings/3-Wednesday/02-tracing-agent-execution.md
"""

import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent

# ============================================================================
# PART 1: Create Tools for Tracing Demo
# ============================================================================

print("=" * 70)
print("PART 1: Creating Tools for Trace Exploration")
print("=" * 70)

@tool
def search_database(query: str) -> str:
    """
    Search the company database for information.
    Use when asked to find, look up, or search for data.
    """
    # Simulate database search
    time.sleep(0.5)  # Simulate latency
    results = {
        "revenue": "Q4 2025 revenue was $12.5M, up 15% YoY",
        "employees": "Current headcount is 450 employees across 3 offices",
        "products": "Main products: CloudSync, DataFlow, and AIAssist"
    }
    for key, value in results.items():
        if key in query.lower():
            return value
    return f"Search results for '{query}': [Sample data would appear here]"

@tool
def calculate_metric(formula: str) -> str:
    """
    Calculate a business metric.
    Use when asked to calculate, compute, or find percentages/ratios.
    """
    # Simulate calculation
    time.sleep(0.3)
    return f"Calculation result for '{formula}': 42.5%"

@tool
def generate_report(topic: str) -> str:
    """
    Generate a summary report on a topic.
    Use when asked for a report, summary, or overview.
    """
    # Simulate report generation
    time.sleep(0.8)
    return f"Report on {topic}: [Executive summary with key findings and recommendations]"

print("  Created 3 tools: search_database, calculate_metric, generate_report")

# ============================================================================
# PART 2: Create Agent and Generate Traces
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Generating Traces with Multi-Tool Agent")
print("=" * 70)

business_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_database, calculate_metric, generate_report],
    system_prompt="""You are a business analyst assistant.
    Use the available tools to answer questions about the company.
    Always use relevant tools before providing your final answer.""",
    name="business_analyst_agent"
)

print("  Agent created: business_analyst_agent")

# Scenario 1: Simple single-tool query
print("\n[Scenario 1] Simple query (single tool)...")
result1 = business_agent.invoke({
    "messages": [{"role": "user", "content": "What is our current employee count?"}]
})
print(f"  Query: What is our current employee count?")
print(f"  Response: {result1['messages'][-1].content[:150]}...")

# Scenario 2: Complex multi-tool query
print("\n[Scenario 2] Complex query (multiple tools)...")
result2 = business_agent.invoke({
    "messages": [{"role": "user", "content": "Find our Q4 revenue and calculate the growth rate compared to last year."}]
})
print(f"  Query: Find Q4 revenue and calculate growth rate")
print(f"  Response: {result2['messages'][-1].content[:150]}...")

# Scenario 3: Report generation
print("\n[Scenario 3] Report generation...")
result3 = business_agent.invoke({
    "messages": [{"role": "user", "content": "Generate a report on our product portfolio."}]
})
print(f"  Query: Generate product portfolio report")
print(f"  Response: {result3['messages'][-1].content[:150]}...")

# ============================================================================
# PART 3: What to Look For in Traces
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Exploring Traces in LangSmith")
print("=" * 70)

print("""
Now open LangSmith and explore the traces we just generated!

URL: https://smith.langchain.com/

┌─────────────────────────────────────────────────────────────────────┐
│ WHAT TO LOOK FOR IN EACH TRACE:                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 1. TRACE OVERVIEW                                                   │
│    - Find traces for 'business_analyst_agent'                       │
│    - Note the different durations for each scenario                 │
│    - See which had single vs multiple tool calls                    │
│                                                                     │
│ 2. TRACE HIERARCHY (click to expand)                                │
│    Parent (agent invocation)                                        │
│    └─ Child 1 (LLM decides which tool)                              │
│    └─ Child 2 (tool execution)                                      │
│    └─ Child 3 (LLM generates response)                              │
│                                                                     │
│ 3. PER-STEP DETAILS                                                 │
│    - Input: What was sent to the LLM/tool                           │
│    - Output: What came back                                         │
│    - Duration: How long this step took                              │
│    - Tokens: Input/output token counts                              │
│                                                                     │
│ 4. MULTI-TOOL TRACES (Scenario 2)                                   │
│    - See how agent called search_database first                     │
│    - Then called calculate_metric                                   │
│    - Then synthesized final answer                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
# PART 4: Understanding Token Usage
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Analyzing Token Usage")
print("=" * 70)

print("""
In LangSmith, token usage is shown at each step.

Token Breakdown Example:
┌──────────────────────────────────────────────────────────────┐
│ Step                    │ Input Tokens │ Output Tokens     │
├─────────────────────────┼──────────────┼───────────────────┤
│ Initial LLM call        │     245      │      35           │
│ Tool: search_database   │     n/a      │      n/a          │
│ Follow-up LLM call      │     312      │      89           │
│ TOTAL                   │     557      │     124           │
└──────────────────────────────────────────────────────────────┘

Cost Estimation (GPT-4o-mini pricing ~$0.15/1M input, ~$0.60/1M output):
- This trace: ~$0.0001 (very cheap!)
- 1000 similar calls: ~$0.10

Key Insight:
Multi-tool traces use more tokens because each LLM call includes 
the full conversation history plus tool results.
""")

# ============================================================================
# PART 5: Comparing Traces
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Comparing Different Traces")
print("=" * 70)

print("""
Compare the three scenarios we ran:

┌─────────────────────────────────────────────────────────────────┐
│ Scenario        │ Tools Called │ LLM Calls │ Est. Duration    │
├─────────────────┼──────────────┼───────────┼──────────────────┤
│ 1. Employee ct  │      1       │     2     │   ~1.5s          │
│ 2. Revenue calc │      2       │     3     │   ~2.5s          │
│ 3. Report gen   │      1       │     2     │   ~2.0s          │
└─────────────────────────────────────────────────────────────────┘

Observations:
- More tools = more LLM calls = longer duration
- Report generation took longer due to slower tool (simulated)
- Token usage scales with conversation length

Questions to ask yourself:
- Is this trace longer than expected?
- Which step is the bottleneck?
- Could we reduce LLM calls?
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Trace Exploration")
print("=" * 70)

print("""
Key Takeaways:

1. Every agent invocation creates a trace
2. Traces show parent-child relationships
3. Each step has duration and token metrics
4. Compare traces to optimize performance
5. Use filters to find specific traces

What to do next:
- Open LangSmith dashboard
- Find the 3 traces from this demo
- Expand each to see the execution flow
- Note the differences between simple and complex queries
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. How to find traces in the dashboard
2. Expanding the trace hierarchy
3. Viewing input/output at each step
4. The token usage breakdown

Live Demo Tips:
- Run this script while dashboard is open
- Refresh dashboard to see new traces appear
- Click into Scenario 2 trace to show multi-tool flow
- Use the comparison view if available

Discussion Questions:
- "Looking at Scenario 2, why are there multiple LLM calls?"
- "What would you do if you saw a 10-second trace?"
- "How would you reduce token usage?"

Exercise:
Have trainees predict which tools will be called before 
running a new query, then verify in traces.
""")

print("=" * 70)
