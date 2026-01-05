# Exercise 02: Trace Analysis

## Overview

Now that LangSmith is configured, it's time to use it for what it's built for: understanding and debugging agent behavior. You'll run several agent scenarios and analyze the resulting traces.

## Learning Objectives

- Analyze trace hierarchies in LangSmith
- Identify agent decision points
- Debug failed tool calls
- Monitor token usage and latency
- Document insights from traces

## The Scenario

The QA team has reported that an agent "sometimes doesn't use the right tool." Your job is to:

1. Run the agent with different inputs
2. Analyze the traces to understand its decisions
3. Document patterns in agent behavior
4. Identify potential improvements

## Your Tasks

### Task 1: Run Test Scenarios (20 min)

Run the provided agent with these test cases:
1. A clear request that should use Tool A
2. A clear request that should use Tool B
3. An ambiguous request (could be either)
4. A request that needs no tools
5. An invalid/edge case request

Each run creates a trace in LangSmith.

### Task 2: Trace Analysis (25 min)

For each trace, document:
- Which tool(s) were called (if any)
- The LLM's reasoning (visible in the trace)
- Total tokens used
- Latency breakdown

Use the template in the starter code to record your findings.

### Task 3: Pattern Identification (15 min)

Look across all traces and identify:
- What makes the agent choose Tool A vs Tool B?
- Are there cases where it makes wrong choices?
- How could the system prompt or tool descriptions be improved?

### Task 4: Debugging Practice (15 min)

The starter code includes an intentional failure scenario. Run it and use the trace to:
- Identify where the failure occurred
- Understand why it failed
- Propose a fix

## Definition of Done

- [_] All 5 test scenarios executed
- [_] Trace analysis template completed for each
- [_] Pattern analysis documented
- [_] Failure scenario debugged with proposed fix
- [_] Summary report generated

## Testing Your Solution

```bash
cd exercises/3-Wednesday/starter_code
python exercise_02_starter.py
```

## Trace Analysis Template

For each trace, fill out:

```
Scenario: [Description of the test case]
Trace URL: [LangSmith URL]

1. Tool Selection
   - Expected: [Which tool should be used]
   - Actual: [Which tool was used]
   - Match: [Yes/No]

2. Token Usage
   - Input tokens: [N]
   - Output tokens: [N]
   - Total cost estimate: [$X.XX]

3. Latency Breakdown
   - Total time: [Ns]
   - LLM time: [Ns]
   - Tool time: [Ns]

4. Observations
   [Notes about agent behavior, interesting decisions, etc.]
```

## What to Look For in Traces

### Agent Decision Flow
```
Agent Run
├── LLM Call (decides to use tool)
│   ├── Input: User message + system prompt
│   └── Output: Tool call request
├── Tool Execution
│   ├── Input: Arguments from LLM
│   └── Output: Tool result
└── LLM Call (formulates response)
    ├── Input: Tool result + context
    └── Output: Final response
```

### Red Flags to Watch For
- LLM calling wrong tool for the task
- Tool errors not handled gracefully
- Excessive token usage for simple tasks
- Long latency in specific steps
- Missing or unclear reasoning

## Questions to Answer

After analyzing your traces, answer these questions:

1. **Tool Selection**: How does the agent decide which tool to use? What keywords or phrases trigger each tool?

2. **Failure Modes**: What causes the agent to make mistakes? How could you prevent these?

3. **Efficiency**: Are there cases where the agent uses more tokens/calls than necessary?

4. **Improvements**: Based on your analysis, what changes would you recommend to:
   - System prompt?
   - Tool descriptions?
   - Tool implementations?

## Stretch Goals (Optional)

1. Compare traces across different model temperatures
2. Analyze how conversation history affects token usage
3. Create a dashboard of key metrics from your traces
