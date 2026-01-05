# Error Handling Patterns

## Learning Objectives
- Identify common error scenarios in LangChain agents
- Implement retry strategies for transient failures
- Build fallback mechanisms for graceful degradation
- Design robust agents that handle edge cases

## Why This Matters

Production agents encounter errors: API rate limits, network issues, malformed inputs, unexpected model behavior. Without proper error handling, a single failure crashes your entire system. With good patterns, your agent gracefully handles problems and keeps working.

## The Concept

### Common Error Categories

| Category | Examples | Handling Strategy |
|----------|----------|-------------------|
| **API Errors** | Rate limits, auth failures | Retry with backoff |
| **Tool Errors** | External API down, invalid data | Fallback, report to user |
| **Validation Errors** | Output doesn't match schema | Retry or simplify |
| **Timeout Errors** | Slow responses | Retry, extend timeout |
| **Input Errors** | Malformed user input | Request clarification |

### Basic Error Handling

Always wrap agent calls:

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[my_tool],
    name="my_agent"
)

def safe_invoke(message: str, config: dict) -> str:
    """Safely invoke the agent with error handling."""
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": message}]
        }, config)
        return result["messages"][-1].content
    
    except Exception as e:
        return f"I encountered an error: {type(e).__name__}. Please try again."
```

### Retry with Exponential Backoff

For transient failures, retry with increasing delays:

```python
import time
from typing import TypeVar, Callable

T = TypeVar('T')

def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0
) -> T:
    """Retry a function with exponential backoff."""
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = min(base_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                time.sleep(delay)
    
    raise last_exception

# Usage
result = retry_with_backoff(
    lambda: agent.invoke({"messages": [...]}, config)
)
```

### Tool Error Handling

Handle errors within tools:

```python
from langchain_core.tools import tool
import requests

@tool
def fetch_weather(city: str) -> str:
    """Fetch weather data for a city."""
    try:
        response = requests.get(
            f"https://api.weather.example/v1/{city}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return f"Weather in {city}: {data['temp']}°F, {data['condition']}"
    
    except requests.Timeout:
        return f"Weather service timed out. Please try again."
    
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return f"City '{city}' not found. Please check the spelling."
        return f"Weather service error. Please try again later."
    
    except Exception as e:
        return f"Could not fetch weather: {str(e)}"
```

### Fallback Mechanisms

When primary approach fails, use fallbacks:

```python
def get_answer_with_fallback(question: str, config: dict) -> str:
    """Try multiple strategies to answer a question."""
    
    # Strategy 1: Agent with tools
    try:
        result = agent_with_tools.invoke({
            "messages": [{"role": "user", "content": question}]
        }, config)
        return result["messages"][-1].content
    except Exception as e:
        print(f"Agent failed: {e}")
    
    # Strategy 2: Simple model (no tools)
    try:
        from langchain import init_chat_model
        model = init_chat_model("openai:gpt-4o-mini")
        result = model.invoke([{"role": "user", "content": question}])
        return f"(Using simple mode) {result.content}"
    except Exception as e:
        print(f"Model failed: {e}")
    
    # Strategy 3: Canned response
    return "I'm having trouble processing your request. Please try again later."
```

### Rate Limit Handling

Handle API rate limits specifically:

```python
from openai import RateLimitError
import time

def handle_rate_limits(func, max_retries: int = 3):
    """Handle OpenAI rate limits."""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                # Extract wait time from error or use default
                wait_time = getattr(e, 'retry_after', 60)
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### Input Validation

Catch bad inputs before they cause problems:

```python
def validate_and_invoke(user_input: str, config: dict) -> str:
    """Validate input before invoking agent."""
    
    # Check input length
    if len(user_input) > 10000:
        return "Your message is too long. Please keep it under 10,000 characters."
    
    if len(user_input.strip()) == 0:
        return "Please provide a message."
    
    # Check for known problematic patterns
    if contains_injection_attempt(user_input):
        return "I cannot process that request."
    
    # Safe to proceed
    return safe_invoke(user_input, config)
```

### Graceful Degradation Pattern

```python
class RobustAgent:
    """Agent with built-in error handling at multiple levels."""
    
    def __init__(self, agent, timeout: int = 30):
        self.agent = agent
        self.timeout = timeout
    
    def invoke(self, message: str, config: dict) -> dict:
        """Invoke with multiple fallback levels."""
        
        result = {
            "success": False,
            "response": "",
            "fallback_level": 0,
            "error": None
        }
        
        # Level 1: Normal invocation
        try:
            response = self._invoke_with_timeout(message, config)
            result["success"] = True
            result["response"] = response
            result["fallback_level"] = 1
            return result
        except Exception as e:
            result["error"] = str(e)
        
        # Level 2: Retry with simpler prompt
        try:
            simplified = f"Please answer briefly: {message}"
            response = self._invoke_with_timeout(simplified, config)
            result["success"] = True
            result["response"] = response
            result["fallback_level"] = 2
            return result
        except Exception:
            pass
        
        # Level 3: Acknowledge and ask to retry
        result["response"] = "I experienced a temporary issue. Could you please rephrase your question?"
        result["fallback_level"] = 3
        return result
    
    def _invoke_with_timeout(self, message: str, config: dict) -> str:
        # Implementation with timeout handling
        result = self.agent.invoke({
            "messages": [{"role": "user", "content": message}]
        }, config)
        return result["messages"][-1].content
```

### Error Logging for Debugging

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def logged_invoke(agent, message: str, config: dict) -> str:
    """Invoke with comprehensive logging."""
    
    request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    logger.info(f"[{request_id}] Starting request", extra={
        "thread_id": config.get("configurable", {}).get("thread_id"),
        "message_length": len(message)
    })
    
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": message}]
        }, config)
        
        logger.info(f"[{request_id}] Request successful", extra={
            "response_length": len(result["messages"][-1].content)
        })
        
        return result["messages"][-1].content
    
    except Exception as e:
        logger.error(f"[{request_id}] Request failed", extra={
            "error_type": type(e).__name__,
            "error_msg": str(e)
        }, exc_info=True)
        raise
```

## Code Example

```python
"""
Error Handling Patterns Demo
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import time
import random

checkpointer = InMemorySaver()

# Tool that can fail
@tool
def unreliable_service(query: str) -> str:
    """Call an unreliable external service."""
    # Simulate random failures
    if random.random() < 0.3:  # 30% failure rate
        raise Exception("Service temporarily unavailable")
    return f"Service response for: {query}"

# Tool with internal error handling
@tool
def robust_service(query: str) -> str:
    """Call a service with built-in error handling."""
    for attempt in range(3):
        try:
            # Simulate service call
            if random.random() < 0.3:
                raise Exception("Temporary failure")
            return f"Robust response for: {query}"
        except Exception:
            if attempt < 2:
                time.sleep(0.5)
                continue
    return "Service is currently unavailable. Please try again later."

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[unreliable_service, robust_service],
    checkpointer=checkpointer,
    system_prompt="""You help users by calling services.
    If a service fails, acknowledge the issue and try alternatives.""",
    name="error_handling_agent"
)

def safe_agent_invoke(message: str, config: dict, max_retries: int = 3) -> dict:
    """Safely invoke agent with retries and fallbacks."""
    
    result = {
        "success": False,
        "response": "",
        "attempts": 0,
        "error": None
    }
    
    for attempt in range(max_retries):
        result["attempts"] = attempt + 1
        
        try:
            response = agent.invoke({
                "messages": [{"role": "user", "content": message}]
            }, config)
            
            result["success"] = True
            result["response"] = response["messages"][-1].content
            return result
            
        except Exception as e:
            result["error"] = str(e)
            
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 2  # 2, 4, 6 seconds
                print(f"  Attempt {attempt + 1} failed, retrying in {wait}s...")
                time.sleep(wait)
            else:
                result["response"] = (
                    "I apologize, but I'm experiencing technical difficulties. "
                    "Please try again in a moment."
                )
    
    return result

# Demo
config = {"configurable": {"thread_id": "error_demo"}}

print("=== Error Handling Demo ===\n")

print("Test 1: Using unreliable service (may fail)")
result = safe_agent_invoke(
    "Use the unreliable_service to look up 'test query'",
    config
)
print(f"Success: {result['success']}")
print(f"Attempts: {result['attempts']}")
print(f"Response: {result['response'][:100]}...\n")

print("Test 2: Using robust service (handles failures internally)")
result = safe_agent_invoke(
    "Use the robust_service to look up 'another query'",
    config
)
print(f"Success: {result['success']}")
print(f"Attempts: {result['attempts']}")
print(f"Response: {result['response'][:100]}...")
```

## Key Takeaways

- **Wrap all calls in try/except**: Prevent crashes from unexpected errors
- **Retry with backoff**: Transient failures often resolve themselves
- **Handle tool errors internally**: Return error messages, don't raise
- **Build fallback chains**: Primary → secondary → default response
- **Log comprehensively**: You need details to debug production issues
- **Graceful degradation**: Always return something useful
- **Validate inputs early**: Catch problems before they propagate

## Additional Resources

- [LangChain Error Handling](https://docs.langchain.com/oss/python/langchain/how-to/error_handling)
- [Python Retry Libraries (tenacity)](https://github.com/jd/tenacity)
- [Fallback Patterns](https://docs.langchain.com/oss/python/langchain/how-to/fallbacks)
