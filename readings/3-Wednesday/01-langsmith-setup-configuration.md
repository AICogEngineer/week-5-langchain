# LangSmith Setup and Configuration

## Learning Objectives
- Understand what LangSmith is and why it's essential for agent development
- Create a LangSmith account and generate API keys
- Configure environment variables for automatic tracing
- Verify that tracing is working correctly

## Why This Matters

Building agents without observability is like driving without a dashboard—you have no idea what's happening inside. LangSmith gives you X-ray vision into your agents:
- See every LLM call and tool invocation
- Debug why agents make wrong decisions
- Monitor costs and token usage
- Compare different agent configurations

For our **"From Basics to Production"** journey, LangSmith is how you go from "it works... I think?" to "I know exactly what's happening."

## The Concept

### What is LangSmith?

LangSmith is LangChain's observability and debugging platform. It automatically captures:

- **Traces**: Complete execution history of agent runs
- **LLM Calls**: Input prompts, output responses, token counts
- **Tool Calls**: Which tools were called, with what arguments, and what they returned
- **Latency**: How long each step took
- **Costs**: Token usage and estimated costs

```
Your Application                     LangSmith Dashboard
┌─────────────────┐                 ┌─────────────────────┐
│   Agent Code    │───traces───────▶│  Visual Execution   │
│                 │                 │  Timeline, Costs,   │
│  create_agent() │                 │  Debugging Tools    │
└─────────────────┘                 └─────────────────────┘
```

### Step 1: Create a LangSmith Account

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Sign up with GitHub, Google, or email
3. Verify your email if required
4. You'll land on the LangSmith dashboard

### Step 2: Generate an API Key

1. Click your profile icon (top right)
2. Select **Settings**
3. Navigate to **API Keys**
4. Click **Create API Key**
5. Give it a descriptive name (e.g., "Development Laptop")
6. **Copy the key immediately** (you won't see it again!)

The key format looks like: `lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Configure Environment Variables

LangSmith requires three environment variables:

```bash
# Enable tracing (required)
export LANGSMITH_TRACING=true

# Your API key (required)
export LANGSMITH_API_KEY=lsv2_pt_your_key_here

# Project name (optional but recommended)
export LANGSMITH_PROJECT=my-project-name
```

#### Windows (PowerShell):
```powershell
$env:LANGSMITH_TRACING = "true"
$env:LANGSMITH_API_KEY = "lsv2_pt_your_key_here"
$env:LANGSMITH_PROJECT = "my-project-name"
```

#### Windows (Command Prompt):
```cmd
set LANGSMITH_TRACING=true
set LANGSMITH_API_KEY=lsv2_pt_your_key_here
set LANGSMITH_PROJECT=my-project-name
```

#### In Python (for scripts):
```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "lsv2_pt_your_key_here"
os.environ["LANGSMITH_PROJECT"] = "my-project-name"
```

#### Using a .env file:
```bash
# .env file
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_your_key_here
LANGSMITH_PROJECT=my-project-name
```

Load with `python-dotenv`:
```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file
```

### Environment Variable Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGSMITH_TRACING` | Yes | Set to `true` to enable tracing |
| `LANGSMITH_API_KEY` | Yes | Your LangSmith API key |
| `LANGSMITH_PROJECT` | No | Project name (default: "default") |
| `LANGSMITH_ENDPOINT` | No | API endpoint (default: production) |

### Step 4: Verify Configuration

Run a simple test to confirm tracing is working:

```python
"""Verify LangSmith is configured correctly."""
import os

# Check environment variables
required_vars = ["LANGSMITH_TRACING", "LANGSMITH_API_KEY"]
for var in required_vars:
    value = os.getenv(var)
    if value:
        # Mask the API key for security
        display = value[:10] + "..." if var == "LANGSMITH_API_KEY" else value
        print(f"✓ {var} = {display}")
    else:
        print(f"✗ {var} is not set!")

# Run a simple agent call
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt="Say 'LangSmith is working!' and nothing else.",
    name="verification_agent"
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Test"}]
})

print(f"\nAgent response: {result['messages'][-1].content}")
print("\nCheck your LangSmith dashboard - you should see this trace!")
```

### Step 5: View Traces in the Dashboard

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Click on your project (or "default" if you didn't set one)
3. You should see your recent trace
4. Click on it to explore the execution timeline

### Project Organization

Use projects to organize traces by purpose:

```python
import os

# Development
os.environ["LANGSMITH_PROJECT"] = "agent-dev"

# Testing
os.environ["LANGSMITH_PROJECT"] = "agent-testing"

# Production
os.environ["LANGSMITH_PROJECT"] = "agent-prod"
```

Or dynamically:
```python
import os
env = os.getenv("ENVIRONMENT", "development")
os.environ["LANGSMITH_PROJECT"] = f"my-agent-{env}"
```

### Security Best Practices

1. **Never commit API keys**: Use environment variables or secure secrets management
2. **Use .gitignore**: Ensure `.env` files aren't committed
3. **Rotate keys periodically**: Create new keys and revoke old ones
4. **Use project-specific keys**: Different keys for dev/staging/prod

```gitignore
# .gitignore
.env
.env.local
*.env
```

### Troubleshooting

**No traces appearing?**
1. Verify `LANGSMITH_TRACING=true` (not "True" or "1")
2. Check API key is correct (try regenerating)
3. Confirm you're looking at the right project
4. Check for network/firewall issues

**"Invalid API Key" error?**
1. Regenerate the key in LangSmith settings
2. Ensure no extra spaces in the environment variable
3. Check the key format starts with `lsv2_pt_`

## Code Example

```python
"""
LangSmith Setup Verification Script
LangChain Version: v1.0+
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def check_langsmith_config():
    """Verify LangSmith configuration."""
    
    # Check required variables
    tracing = os.getenv("LANGSMITH_TRACING")
    api_key = os.getenv("LANGSMITH_API_KEY")
    project = os.getenv("LANGSMITH_PROJECT", "default")
    
    print("LangSmith Configuration Check")
    print("=" * 40)
    
    # Tracing enabled?
    if tracing == "true":
        print("✓ Tracing is ENABLED")
    else:
        print("✗ Tracing is DISABLED")
        print("  Set LANGSMITH_TRACING=true")
        return False
    
    # API key present?
    if api_key:
        masked_key = api_key[:15] + "..." + api_key[-4:]
        print(f"✓ API Key: {masked_key}")
    else:
        print("✗ API Key is MISSING")
        print("  Set LANGSMITH_API_KEY=your_key")
        return False
    
    # Project
    print(f"✓ Project: {project}")
    
    return True

def test_tracing():
    """Run a simple agent to generate a trace."""
    from langchain.agents import create_agent
    from langchain_core.tools import tool
    
    @tool
    def greet(name: str) -> str:
        """Greet someone by name."""
        return f"Hello, {name}!"
    
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[greet],
        system_prompt="You are a friendly greeter.",
        name="langsmith_test_agent"
    )
    
    print("\nRunning test agent...")
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Greet Alice"}]
    })
    
    print(f"Response: {result['messages'][-1].content}")
    print("\n✓ Trace sent! Check your LangSmith dashboard:")
    print(f"  https://smith.langchain.com/")

if __name__ == "__main__":
    if check_langsmith_config():
        test_tracing()
    else:
        print("\nFix the configuration issues above, then run again.")
```

## Key Takeaways

- **LangSmith provides observability**: See inside your agents' execution
- **Three environment variables**: `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`
- **No code changes needed**: Just set environment variables
- **Use projects for organization**: Separate dev/staging/prod traces
- **Protect your API key**: Never commit to version control
- **Verify setup early**: Don't wait until production to enable tracing

## Additional Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Quick Start](https://docs.smith.langchain.com/tracing/quick_start)
- [LangSmith Pricing](https://www.langchain.com/langsmith-pricing)
