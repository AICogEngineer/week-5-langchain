"""
Exercise 01: Custom Tools - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Create custom tools for a productivity assistant.

Instructions:
1. Implement each tool using the @tool decorator
2. Write descriptive docstrings for agent routing
3. Run this file to test your tools independently
"""

from typing import Dict, Any, List, Literal

# ============================================================================
# IMPORTS - Add the tool decorator
# ============================================================================

# TODO: Import the tool decorator
# from langchain_core.tools import tool


# ============================================================================
# MOCK DATA (DO NOT MODIFY)
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
    "database-connection": {
        "title": "Database Connection Pooling",
        "content": "Use connection pooling with max_connections=20..."
    },
    "logging": {
        "title": "Logging Best Practices",
        "content": "Configure structured logging with JSON format..."
    },
}

MOCK_SERVICE_STATUS = {
    "api": {"status": "healthy", "latency_ms": 45},
    "database": {"status": "healthy", "latency_ms": 12},
    "cache": {"status": "degraded", "latency_ms": 150},
    "auth": {"status": "healthy", "latency_ms": 30},
    "payment": {"status": "down", "error": "Connection timeout"},
}


# ============================================================================
# TODO: IMPLEMENT THESE TOOLS
# ============================================================================

# TODO: Add @tool decorator
def search_docs(query: str) -> Dict[str, Any]:
    """
    TODO: Write a descriptive docstring that helps the agent know when to use this tool.
    
    Include keywords like: documentation, docs, how to, reference, guide
    
    Args:
        query: The search terms to look for in documentation
        
    Returns:
        Dict with 'results' (list of matches) and 'count' (number of matches)
    """
    # TODO: Implement this function
    # Search MOCK_DOCUMENTATION for entries matching the query
    # Return matching results
    
    pass  # Remove this and add your implementation


# TODO: Add @tool decorator
def calculate_story_points(
    task_description: str,
    complexity: Literal["low", "medium", "high"] = "medium"
) -> Dict[str, Any]:
    """
    TODO: Write a docstring explaining this is for estimating development work.
    
    Include keywords like: estimate, story points, task, development, sizing
    
    Args:
        task_description: Description of the development task
        complexity: Complexity level - 'low', 'medium', or 'high'
        
    Returns:
        Dict with 'points' (int) and 'rationale' (str)
    """
    # TODO: Implement this function
    # Calculate story points based on complexity:
    # - low: 1-2 points
    # - medium: 3-5 points
    # - high: 8-13 points
    # Include rationale in the response
    
    pass  # Remove this and add your implementation


# TODO: Add @tool decorator
def check_service_status(service_name: str) -> Dict[str, Any]:
    """
    TODO: Write a docstring for checking system/service health.
    
    Include keywords like: status, health, running, service, system
    
    Args:
        service_name: Name of the service to check
        
    Returns:
        Dict with 'service', 'status', and additional details
    """
    # TODO: Implement this function
    # Look up service_name in MOCK_SERVICE_STATUS
    # Return status information
    # Handle unknown services gracefully
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: IMPLEMENT INDEPENDENT TESTING
# ============================================================================

def test_tools_independently() -> None:
    """
    Test each tool independently before integrating with an agent.
    
    This is a best practice - always test tools in isolation first!
    """
    print("=" * 50)
    print("Tool Testing")
    print("=" * 50)
    print()
    
    # TODO: Test search_docs
    print("[INFO] Testing search_docs...")
    # result = search_docs.invoke({"query": "rate limiting"})
    # print(f"[OK] Tool returned: {result}")
    print("[ERROR] Not implemented yet")
    print()
    
    # TODO: Test calculate_story_points
    print("[INFO] Testing calculate_story_points...")
    # result = calculate_story_points.invoke({
    #     "task_description": "Add new API endpoint",
    #     "complexity": "medium"
    # })
    # print(f"[OK] Tool returned: {result}")
    print("[ERROR] Not implemented yet")
    print()
    
    # TODO: Test check_service_status
    print("[INFO] Testing check_service_status...")
    # result = check_service_status.invoke({"service_name": "api"})
    # print(f"[OK] Tool returned: {result}")
    print("[ERROR] Not implemented yet")
    print()
    
    print("=" * 50)
    print("Testing Complete")
    print("=" * 50)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    test_tools_independently()
