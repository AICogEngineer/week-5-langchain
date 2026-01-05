"""
Exercise 02: Your First Agent - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Build a productivity assistant agent with multiple tools.

Instructions:
1. Import tools from your Exercise 01 solution (or use the provided mock tools)
2. Create an agent using create_agent()
3. Test with various scenarios
"""

from typing import Dict, Any, List, Literal

# ============================================================================
# IMPORTS
# ============================================================================

# TODO: Import create_agent
# from langchain.agents import create_agent
from langchain_core.tools import tool


# ============================================================================
# TOOLS (Copy from Exercise 01 or use these mock implementations)
# ============================================================================

MOCK_DOCUMENTATION = {
    "api-rate-limiting": {
        "title": "API Rate Limiting Configuration",
        "content": "Configure rate limits using the RATE_LIMIT_PER_MINUTE env variable..."
    },
    "authentication": {
        "title": "Authentication Setup Guide", 
        "content": "OAuth 2.0 setup requires client_id and client_secret..."
    },
}

MOCK_SERVICE_STATUS = {
    "api": {"status": "healthy", "latency_ms": 45},
    "payment": {"status": "down", "error": "Connection timeout"},
}


@tool
def search_docs(query: str) -> Dict[str, Any]:
    """Search documentation for relevant information.
    
    Use when the user asks about:
    - How to configure something
    - Documentation or reference material
    - API usage or setup guides
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
    """Calculate story points for a development task.
    
    Use when the user wants to:
    - Estimate work effort
    - Size a task or feature
    - Plan sprint capacity
    """
    points_map = {"low": 2, "medium": 5, "high": 13}
    points = points_map.get(complexity, 5)
    return {
        "points": points,
        "complexity": complexity,
        "rationale": f"Based on {complexity} complexity for: {task_description}"
    }


@tool
def check_service_status(service_name: str) -> Dict[str, Any]:
    """Check the health status of a service.
    
    Use when the user asks about:
    - Service health or status
    - System availability
    - Whether something is running
    """
    service = MOCK_SERVICE_STATUS.get(service_name.lower())
    if service:
        return {"service": service_name, **service}
    return {"service": service_name, "status": "unknown", "error": "Service not found"}


# ============================================================================
# TODO: IMPLEMENT AGENT CREATION
# ============================================================================

def create_productivity_agent():
    """
    Create the productivity assistant agent.
    
    Requirements:
    - Use create_agent() from langchain.agents
    - Include all three tools
    - Write a clear system prompt
    - CRITICAL: Include the 'name' parameter
    
    Returns:
        Configured agent instance
    """
    # TODO: Implement this function
    # 
    # agent = create_agent(
    #     model="openai:gpt-4o-mini",
    #     tools=[search_docs, calculate_story_points, check_service_status],
    #     system_prompt="...",
    #     name="productivity_assistant"
    # )
    # return agent
    
    pass  # Remove this and add your implementation


def create_system_prompt() -> str:
    """
    Design the system prompt for the productivity agent.
    
    The prompt should:
    - Define the assistant's role
    - Explain when to use each tool
    - Set the response tone
    
    Returns:
        System prompt string
    """
    # TODO: Write your system prompt
    # Example structure:
    # """You are a productivity assistant for developers.
    #
    # Your capabilities:
    # - Search documentation: Use when users ask "how to" questions
    # - Estimate story points: Use when users describe tasks to size
    # - Check service status: Use when users ask about system health
    #
    # Be helpful and concise."""
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: IMPLEMENT AGENT TESTING
# ============================================================================

def test_agent(agent, message: str) -> str:
    """
    Test the agent with a message and return the response.
    
    Args:
        agent: The productivity agent
        message: User message to send
        
    Returns:
        Agent's response content
    """
    # TODO: Implement this function
    # result = agent.invoke({
    #     "messages": [{"role": "user", "content": message}]
    # })
    # return result["messages"][-1].content
    
    pass  # Remove this and add your implementation


def run_test_scenarios():
    """Run the agent through various test scenarios."""
    print("=" * 60)
    print("Productivity Agent Test")
    print("=" * 60)
    print()
    
    # Create agent
    print("[INFO] Creating agent...")
    agent = create_productivity_agent()
    
    if agent is None:
        print("[ERROR] create_productivity_agent() not implemented")
        return
    
    print("[OK] Agent created")
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
            "message": "I need to add a new payment endpoint with validation. How many points?",
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
        print("[INFO] Agent is thinking...")
        
        response = test_agent(agent, test["message"])
        
        if response is None:
            print("[ERROR] test_agent() not implemented")
        else:
            print(f"[OK] Response: {response[:200]}..." if len(response) > 200 else f"[OK] Response: {response}")
        print()
    
    print("=" * 60)
    print("All Tests Complete")
    print("=" * 60)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    run_test_scenarios()
