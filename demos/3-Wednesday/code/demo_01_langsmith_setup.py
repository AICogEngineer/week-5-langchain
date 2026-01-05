"""
Demo 01: LangSmith Setup and Configuration

This demo shows trainees how to:
1. Configure LangSmith environment variables
2. Enable automatic tracing for LangChain operations
3. Verify tracing is working
4. Navigate to the LangSmith dashboard

Learning Objectives:
- Set up LangSmith for development
- Understand the three required environment variables
- Verify traces are being captured

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/langsmith
Last Verified: January 2026

References:
- Written Content: readings/3-Wednesday/01-langsmith-setup-configuration.md
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# PART 1: Environment Variable Configuration
# ============================================================================

print("=" * 70)
print("PART 1: LangSmith Environment Configuration")
print("=" * 70)

print("""
LangSmith requires THREE environment variables:

1. LANGSMITH_TRACING = "true"
   → Enables automatic tracing

2. LANGSMITH_API_KEY = "<your-api-key>"
   → Authentication with LangSmith service
   → Get this from https://smith.langchain.com/

3. LANGSMITH_PROJECT = "<project-name>"
   → Groups traces together
   → Use different projects for dev/staging/prod
""")

# Check if environment variables are set
print("\n[Step 1] Checking environment variables...")

env_vars = {
    "LANGSMITH_TRACING": os.getenv("LANGSMITH_TRACING"),
    "LANGSMITH_API_KEY": os.getenv("LANGSMITH_API_KEY"),
    "LANGSMITH_PROJECT": os.getenv("LANGSMITH_PROJECT")
}

all_set = True
for var, value in env_vars.items():
    if value:
        # Mask API key for security
        display = value[:8] + "..." if var == "LANGSMITH_API_KEY" and len(value) > 8 else value
        print(f"  ✓ {var} = {display}")
    else:
        print(f"  ✗ {var} = NOT SET")
        all_set = False

if not all_set:
    print("\n⚠️  Some variables are not set!")
    print("   Create a .env file with:")
    print("   LANGSMITH_TRACING=true")
    print("   LANGSMITH_API_KEY=your-key-here")
    print("   LANGSMITH_PROJECT=week5-langchain-demos")

# ============================================================================
# PART 2: Creating a .env Template
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Sample .env Configuration")
print("=" * 70)

env_template = """
# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxx
LANGSMITH_PROJECT=week5-langchain-demos

# LLM API Keys
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
"""

print("""
Create a .env file in your project root with:
""")
print(env_template)

# ============================================================================
# PART 3: Verify Tracing with Simple Agent
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Verify Tracing with Simple Agent")
print("=" * 70)

# Only proceed if we have the required environment variables
if all_set or os.getenv("OPENAI_API_KEY"):
    from langchain_core.tools import tool
    from langchain.agents import create_agent
    
    @tool
    def get_greeting(name: str) -> str:
        """Generate a greeting for a person. Use when asked to greet someone."""
        return f"Hello, {name}! Welcome to LangSmith tracing demo."
    
    print("\n[Step 2] Creating a simple agent to generate traces...")
    
    demo_agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[get_greeting],
        system_prompt="You are a friendly greeter. Use the greeting tool when asked to greet someone.",
        name="langsmith_demo_agent"
    )
    
    print("  Agent created: langsmith_demo_agent")
    
    print("\n[Step 3] Invoking agent (this creates a trace)...")
    
    result = demo_agent.invoke({
        "messages": [{"role": "user", "content": "Please greet Alice"}]
    })
    
    response = result["messages"][-1].content
    print(f"\n  User: Please greet Alice")
    print(f"  Agent: {response}")
    
    print("\n[Step 4] Check LangSmith Dashboard...")
    print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │ 1. Open https://smith.langchain.com/                           │
  │ 2. Select your project: week5-langchain-demos                  │
  │ 3. Find the trace for 'langsmith_demo_agent'                   │
  │ 4. Click to expand and see:                                    │
  │    - Input messages                                            │
  │    - Tool calls (get_greeting)                                 │
  │    - LLM responses                                             │
  │    - Token usage                                               │
  └─────────────────────────────────────────────────────────────────┘
    """)
else:
    print("\n⚠️  Skipping agent demo - API keys not configured")
    print("   Set environment variables and run again to see tracing in action")

# ============================================================================
# PART 4: Understanding Trace Structure
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Understanding Trace Structure")
print("=" * 70)

print("""
Each trace in LangSmith shows:

┌─ Run (Parent Trace)
│  ├─ Name: langsmith_demo_agent
│  ├─ Type: chain
│  ├─ Duration: 1.23s
│  └─ Token Count: 156
│
├─── LLM Call (Child)
│    ├─ Model: gpt-4o-mini
│    ├─ Input: [messages...]
│    ├─ Output: [tool_call...]
│    └─ Tokens: 45 in, 20 out
│
├─── Tool Call (Child)
│    ├─ Name: get_greeting
│    ├─ Input: {"name": "Alice"}
│    └─ Output: "Hello, Alice!..."
│
└─── LLM Call (Child)
     ├─ Model: gpt-4o-mini
     ├─ Input: [tool_result...]
     └─ Output: "..."

Key metrics to watch:
- Total duration
- Token usage per step
- Success/failure status
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: LangSmith Setup")
print("=" * 70)

print("""
Key Takeaways:

1. Three environment variables enable LangSmith:
   - LANGSMITH_TRACING=true
   - LANGSMITH_API_KEY=<your-key>
   - LANGSMITH_PROJECT=<project-name>

2. Tracing is AUTOMATIC - no code changes needed!

3. Every LangChain operation gets traced:
   - Agent invocations
   - Tool calls
   - LLM requests/responses

4. Use projects to organize traces by environment
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. How to get an API key from smith.langchain.com
2. Creating a .env file
3. The LangSmith dashboard layout
4. Expanding traces to see details

Live Demo Tips:
- Have LangSmith dashboard open in browser
- Run the agent demo
- Immediately switch to dashboard to show trace appearing
- Click into trace to show structure

Discussion Questions:
- "What would you use LangSmith for in production?"
- "How could traces help debug a chatbot issue?"
- "What's the benefit of different projects?"

Common Issues:
- Traces not appearing: Check LANGSMITH_TRACING=true (must be string "true")
- API key errors: Regenerate key in LangSmith settings
- Wrong project: Check LANGSMITH_PROJECT spelling
""")

print("=" * 70)
