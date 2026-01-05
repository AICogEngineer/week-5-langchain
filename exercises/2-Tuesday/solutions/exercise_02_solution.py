"""
Exercise 02: Your First Agent - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete implementation of a productivity assistant agent.
"""

from typing import Dict, Any, Literal
from langchain.agents import create_agent
from langchain_core.tools import tool


# ============================================================================
# MOCK DATA
# ============================================================================

MOCK_DOCUMENTATION = {
    "api-rate-limiting": {
        "title": "API Rate Limiting Configuration",
        "content": "Configure rate limits using the RATE_LIMIT_PER_MINUTE env variable. Default is 100 requests per minute."
    },
    "authentication": {
        "title": "Authentication Setup Guide",
        "content": "OAuth 2.0 setup requires client_id and client_secret in .env file."
    },
    "database-connection": {
        "title": "Database Connection Pooling",
        "content": "Use connection pooling with max_connections=20."
    },
}

MOCK_SERVICE_STATUS = {
    "api": {"status": "healthy", "latency_ms": 45},
    "database": {"status": "healthy", "latency_ms": 12},
    "payment": {"status": "down", "error": "Connection timeout"},
}


# ============================================================================
# TOOLS
# ============================================================================

@tool
def search_docs(query: str) -> Dict[str, Any]:
    """Search the knowledge base for relevant documentation.
    
    Use this tool when the user asks about:
    - How to configure something
    - Documentation, guides, or references
    - API usage examples
    - Setup instructions
    """
    query_lower = query.lower()
    results = []
    for key, doc in MOCK_DOCUMENTATION.items():
        if any(word in key or word in doc["title"].lower() 
               for word in query_lower.split()):
            results.append(doc)
    return {"results": results, "count": len(results)}


@tool
def calculate_story_points(
    task_description: str,
    complexity: Literal["low", "medium", "high"] = "medium"
) -> Dict[str, Any]:
    """Calculate estimated story points for a development task.
    
    Use when the user wants to:
    - Estimate work effort
    - Size a task or feature
    - Plan sprint work
    """
    points = {"low": 2, "medium": 5, "high": 13}.get(complexity, 5)
    return {
        "points": points,
        "complexity": complexity,
        "task": task_description,
        "rationale": f"Based on {complexity} complexity assessment"
    }


@tool
def check_service_status(service_name: str) -> Dict[str, Any]:
    """Check the current health status of a service.
    
    Use when the user asks about:
    - Service health or availability
    - Whether something is running
    - System status
    """
    service = MOCK_SERVICE_STATUS.get(service_name.lower())
    if service:
        return {"service": service_name, **service}
    return {
        "service": service_name,
        "status": "unknown",
        "available_services": list(MOCK_SERVICE_STATUS.keys())
    }


# ============================================================================
# AGENT CREATION
# ============================================================================

def create_system_prompt() -> str:
    """Design the system prompt for the productivity agent."""
    return """You are a productivity assistant for software developers.

Your capabilities:
1. **Documentation Search**: When users ask "how to" questions, configuration questions, or need reference material, use the search_docs tool.

2. **Story Points Estimation**: When users describe development tasks and want sizing or estimates, use the calculate_story_points tool. Ask about complexity if not specified.

3. **Service Status**: When users ask if services are running, healthy, or available, use the check_service_status tool.

Guidelines:
- Be concise and helpful
- If you don't need a tool to answer, respond directly
- Explain your findings clearly
- If a tool returns no results, acknowledge this and suggest alternatives"""


def create_productivity_agent():
    """Create the productivity assistant agent."""
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[search_docs, calculate_story_points, check_service_status],
        system_prompt=create_system_prompt(),
        name="productivity_assistant"  # REQUIRED - always include name
    )
    return agent


# ============================================================================
# AGENT TESTING
# ============================================================================

def test_agent(agent, message: str) -> str:
    """Test the agent with a message and return the response."""
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": message}]
        })
        # Extract the last message content
        return result["messages"][-1].content
    except Exception as e:
        return f"Error: {e}"


def run_test_scenarios():
    """Run the agent through various test scenarios."""
    print("=" * 60)
    print("Productivity Agent Test")
    print("=" * 60)
    print()
    
    # Create agent
    print("[INFO] Creating agent...")
    agent = create_productivity_agent()
    print(f"[OK] Agent 'productivity_assistant' created")
    print()
    
    # Test scenarios
    test_cases = [
        {
            "name": "Documentation Query",
            "message": "How do I configure the API rate limiting?",
            "expected_tool": "search_docs"
        },
        {
            "name": "Story Points Estimation",
            "message": "I need to add a new payment endpoint with validation. It's medium complexity. How many points?",
            "expected_tool": "calculate_story_points"
        },
        {
            "name": "Service Status Check",
            "message": "Is the payment service running?",
            "expected_tool": "check_service_status"
        },
        {
            "name": "No Tool Needed",
            "message": "Hello, who are you?",
            "expected_tool": None
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"=== Test Scenario {i}: {test['name']} ===")
        print(f"User: \"{test['message']}\"")
        if test["expected_tool"]:
            print(f"[INFO] Expected tool: {test['expected_tool']}")
        else:
            print("[INFO] No tool expected")
        print()
        
        response = test_agent(agent, test["message"])
        
        # Truncate long responses for display
        display_response = response[:300] + "..." if len(response) > 300 else response
        print(f"Agent: {display_response}")
        print()
    
    print("=" * 60)
    print("All Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    run_test_scenarios()
