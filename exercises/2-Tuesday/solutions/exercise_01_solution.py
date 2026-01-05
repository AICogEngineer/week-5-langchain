"""
Exercise 01: Custom Tools - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete implementation of custom productivity tools.
"""

from typing import Dict, Any, List, Literal
from langchain_core.tools import tool


# ============================================================================
# MOCK DATA
# ============================================================================

MOCK_DOCUMENTATION = {
    "api-rate-limiting": {
        "title": "API Rate Limiting Configuration",
        "content": "Configure rate limits using the RATE_LIMIT_PER_MINUTE env variable. Default is 100 requests per minute per client."
    },
    "authentication": {
        "title": "Authentication Setup Guide",
        "content": "OAuth 2.0 setup requires client_id and client_secret. Configure in the .env file."
    },
    "database-connection": {
        "title": "Database Connection Pooling",
        "content": "Use connection pooling with max_connections=20. Set DB_POOL_SIZE in environment."
    },
    "logging": {
        "title": "Logging Best Practices",
        "content": "Configure structured logging with JSON format. Use LOG_LEVEL=INFO for production."
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
# TOOL IMPLEMENTATIONS
# ============================================================================

@tool
def search_docs(query: str) -> Dict[str, Any]:
    """Search the knowledge base for relevant documentation.
    
    Use this tool when the user asks about:
    - How to configure something
    - Documentation, guides, or references
    - API usage examples
    - Setup or installation instructions
    
    Args:
        query: The search terms to look for in documentation
        
    Returns:
        Dict with 'results' (list of matching docs) and 'count' (match count)
    """
    query_lower = query.lower()
    query_words = query_lower.split()
    
    results = []
    for key, doc in MOCK_DOCUMENTATION.items():
        # Check if any query word matches the key or title
        title_lower = doc["title"].lower()
        if any(word in key or word in title_lower for word in query_words):
            results.append({
                "title": doc["title"],
                "content": doc["content"],
                "key": key
            })
    
    return {
        "results": results,
        "count": len(results),
        "query": query
    }


@tool
def calculate_story_points(
    task_description: str,
    complexity: Literal["low", "medium", "high"] = "medium"
) -> Dict[str, Any]:
    """Calculate estimated story points for a development task.
    
    Use this tool when the user wants to:
    - Estimate work effort for a task
    - Size a feature or story
    - Plan sprint capacity
    - Get a rough idea of task complexity
    
    Args:
        task_description: Description of the development task to estimate
        complexity: Complexity level - 'low', 'medium', or 'high'
        
    Returns:
        Dict with 'points', 'complexity', and 'rationale'
    """
    # Fibonacci-based story points
    points_map = {
        "low": 2,
        "medium": 5,
        "high": 13
    }
    
    # Validate complexity
    if complexity not in points_map:
        complexity = "medium"  # Default fallback
    
    points = points_map[complexity]
    
    # Generate rationale based on complexity
    rationale_map = {
        "low": "This is a straightforward task with clear requirements and minimal unknowns.",
        "medium": "This task has some complexity and may require research or coordination.",
        "high": "This is a complex task with significant unknowns or cross-team dependencies."
    }
    
    return {
        "points": points,
        "complexity": complexity,
        "task": task_description,
        "rationale": rationale_map[complexity]
    }


@tool
def check_service_status(service_name: str) -> Dict[str, Any]:
    """Check the current health status of a system service.
    
    Use this tool when the user asks about:
    - Service health or availability
    - Whether a system is running
    - System status checks
    - Infrastructure health
    
    Available services: api, database, cache, auth, payment
    
    Args:
        service_name: Name of the service to check (e.g., 'api', 'database')
        
    Returns:
        Dict with 'service', 'status', and additional metrics
    """
    service_key = service_name.lower().strip()
    
    if service_key in MOCK_SERVICE_STATUS:
        status_info = MOCK_SERVICE_STATUS[service_key]
        return {
            "service": service_name,
            **status_info
        }
    else:
        # List available services for user
        available = list(MOCK_SERVICE_STATUS.keys())
        return {
            "service": service_name,
            "status": "unknown",
            "error": f"Service '{service_name}' not found",
            "available_services": available
        }


# ============================================================================
# INDEPENDENT TESTING
# ============================================================================

def test_tools_independently() -> None:
    """Test each tool independently before integrating with an agent."""
    print("=" * 50)
    print("Tool Testing")
    print("=" * 50)
    print()
    
    all_passed = True
    
    # Test search_docs
    print("[INFO] Testing search_docs...")
    try:
        result = search_docs.invoke({"query": "rate limiting"})
        if result["count"] > 0:
            print(f"[OK] Found {result['count']} result(s)")
            for doc in result["results"]:
                print(f"     - {doc['title']}")
        else:
            print("[WARNING] No results found")
    except Exception as e:
        print(f"[ERROR] {e}")
        all_passed = False
    print()
    
    # Test calculate_story_points
    print("[INFO] Testing calculate_story_points...")
    try:
        result = calculate_story_points.invoke({
            "task_description": "Add new API endpoint with validation",
            "complexity": "medium"
        })
        print(f"[OK] Estimated: {result['points']} points ({result['complexity']} complexity)")
        print(f"     Rationale: {result['rationale']}")
    except Exception as e:
        print(f"[ERROR] {e}")
        all_passed = False
    print()
    
    # Test check_service_status - healthy service
    print("[INFO] Testing check_service_status (healthy)...")
    try:
        result = check_service_status.invoke({"service_name": "api"})
        print(f"[OK] Service: {result['service']} - Status: {result['status']}")
        if "latency_ms" in result:
            print(f"     Latency: {result['latency_ms']}ms")
    except Exception as e:
        print(f"[ERROR] {e}")
        all_passed = False
    print()
    
    # Test check_service_status - down service
    print("[INFO] Testing check_service_status (down)...")
    try:
        result = check_service_status.invoke({"service_name": "payment"})
        print(f"[OK] Service: {result['service']} - Status: {result['status']}")
        if "error" in result:
            print(f"     Error: {result['error']}")
    except Exception as e:
        print(f"[ERROR] {e}")
        all_passed = False
    print()
    
    # Test unknown service
    print("[INFO] Testing check_service_status (unknown)...")
    try:
        result = check_service_status.invoke({"service_name": "nonexistent"})
        print(f"[OK] Service: {result['service']} - Status: {result['status']}")
        if "available_services" in result:
            print(f"     Available: {result['available_services']}")
    except Exception as e:
        print(f"[ERROR] {e}")
        all_passed = False
    print()
    
    print("=" * 50)
    if all_passed:
        print("[OK] All Tools Tested Successfully!")
    else:
        print("[INFO] Some tests had issues - review above")
    print("=" * 50)


if __name__ == "__main__":
    test_tools_independently()
