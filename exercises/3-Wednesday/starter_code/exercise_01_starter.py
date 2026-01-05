"""
Exercise 01: LangSmith Integration - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Configure LangSmith for automatic tracing and verify the setup.

Instructions:
1. Set up your LangSmith environment variables
2. Implement the verification functions
3. Run this file to test your configuration
"""

import os
from typing import Dict, Any, Optional

# ============================================================================
# IMPORTS
# ============================================================================

# TODO: Import create_agent and tool
# from langchain.agents import create_agent
# from langchain_core.tools import tool


# ============================================================================
# CONFIGURATION
# ============================================================================

REQUIRED_ENV_VARS = [
    "LANGSMITH_TRACING",
    "LANGSMITH_API_KEY", 
    "LANGSMITH_PROJECT"
]


# ============================================================================
# TODO: IMPLEMENT THESE FUNCTIONS
# ============================================================================

def verify_langsmith_config() -> Dict[str, Any]:
    """
    Verify that LangSmith environment variables are configured.
    
    Tasks:
    - Check that LANGSMITH_TRACING is set to "true"
    - Check that LANGSMITH_API_KEY is present
    - Check that LANGSMITH_PROJECT is set
    
    Returns:
        Dict with:
        - 'configured': bool (True if all vars set)
        - 'status': Dict[str, str] (status of each variable)
        - 'missing': List[str] (any missing variables)
    """
    # TODO: Implement this function
    # Example:
    # status = {}
    # missing = []
    # for var in REQUIRED_ENV_VARS:
    #     value = os.environ.get(var)
    #     if value:
    #         # Mask API keys for display
    #         display = f"***{value[-4:]}" if "KEY" in var else value
    #         status[var] = display
    #     else:
    #         missing.append(var)
    #         status[var] = "NOT SET"
    
    pass  # Remove this and add your implementation


def test_langsmith_connection() -> Dict[str, Any]:
    """
    Test connection to LangSmith API.
    
    Tasks:
    - Attempt to verify the API key works
    - Check if the project exists
    - Return connection status
    
    Returns:
        Dict with:
        - 'connected': bool
        - 'project': str (project name)
        - 'message': str
    """
    # TODO: Implement this function
    # Note: LangSmith auto-creates projects on first trace,
    # so you can verify by attempting a simple API call
    
    pass  # Remove this and add your implementation


def create_traced_agent():
    """
    Create a simple agent that will be traced.
    
    Tasks:
    - Create a tool using @tool decorator
    - Create an agent with create_agent()
    - Include the required 'name' parameter
    
    Returns:
        Configured agent instance
    """
    # TODO: Implement this function
    # 
    # @tool
    # def simple_tool(query: str) -> str:
    #     """A simple tool for testing traces."""
    #     return f"Processed: {query}"
    #
    # agent = create_agent(
    #     model="openai:gpt-4o-mini",
    #     tools=[simple_tool],
    #     name="traced_test_agent"
    # )
    # return agent
    
    pass  # Remove this and add your implementation


def run_traced_invocation(agent) -> Dict[str, Any]:
    """
    Run an agent invocation that will be traced.
    
    Args:
        agent: The agent to invoke
        
    Returns:
        Dict with:
        - 'success': bool
        - 'response': str
        - 'trace_info': str (instruction to view trace)
    """
    # TODO: Implement this function
    # result = agent.invoke({
    #     "messages": [{"role": "user", "content": "Process this test message"}]
    # })
    # 
    # return {
    #     'success': True,
    #     'response': result["messages"][-1].content,
    #     'trace_info': "View trace at: https://smith.langchain.com/"
    # }
    
    pass  # Remove this and add your implementation


def verify_trace_exists() -> bool:
    """
    Guide user to verify trace exists in LangSmith.
    
    This is a manual verification step - print instructions
    for the user to check the LangSmith dashboard.
    
    Returns:
        True (user should manually verify)
    """
    # TODO: Implement this function
    # Print instructions for manual verification
    # 
    # print("\nTo verify your trace:")
    # print("1. Open https://smith.langchain.com/")
    # print("2. Navigate to your project")
    # print("3. Look for the most recent trace")
    # print("4. Click to expand and view details")
    
    pass  # Remove this and add your implementation


# ============================================================================
# TEST HARNESS
# ============================================================================

def run_integration_test():
    """Run the complete LangSmith integration test."""
    print("=" * 50)
    print("LangSmith Integration Test")
    print("=" * 50)
    print()
    
    # Step 1: Verify configuration
    print("[INFO] Checking environment configuration...")
    config_result = verify_langsmith_config()
    
    if config_result is None:
        print("[ERROR] verify_langsmith_config() not implemented")
        return
    
    if config_result.get('configured'):
        for var, value in config_result.get('status', {}).items():
            print(f"[OK] {var} = {value}")
    else:
        print("[ERROR] Missing environment variables:")
        for var in config_result.get('missing', []):
            print(f"       - {var}")
        print("\nSet these variables and try again.")
        return
    
    print()
    
    # Step 2: Test connection
    print("[INFO] Testing LangSmith connection...")
    conn_result = test_langsmith_connection()
    
    if conn_result is None:
        print("[ERROR] test_langsmith_connection() not implemented")
    elif conn_result.get('connected'):
        print(f"[OK] {conn_result.get('message')}")
    else:
        print(f"[ERROR] {conn_result.get('message')}")
        return
    
    print()
    
    # Step 3: Create and run agent
    print("[INFO] Creating traced agent...")
    agent = create_traced_agent()
    
    if agent is None:
        print("[ERROR] create_traced_agent() not implemented")
        return
    
    print("[OK] Agent created")
    print()
    
    print("[INFO] Running traced invocation...")
    invoke_result = run_traced_invocation(agent)
    
    if invoke_result is None:
        print("[ERROR] run_traced_invocation() not implemented")
        return
    
    if invoke_result.get('success'):
        print("[OK] Agent invocation complete")
        print(f"Response: {invoke_result.get('response')}")
    else:
        print("[ERROR] Invocation failed")
        return
    
    print()
    
    # Step 4: Verification instructions
    verify_trace_exists()
    
    print()
    print("=" * 50)
    print("Integration Test Complete")
    print("=" * 50)


if __name__ == "__main__":
    run_integration_test()
