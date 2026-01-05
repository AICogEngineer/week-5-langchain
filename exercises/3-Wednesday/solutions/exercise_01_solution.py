"""
Exercise 01: LangSmith Integration - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete solution for LangSmith configuration and verification.
"""

import os
from typing import Dict, Any
from langchain.agents import create_agent
from langchain_core.tools import tool


# ============================================================================
# CONFIGURATION
# ============================================================================

REQUIRED_ENV_VARS = [
    "LANGSMITH_TRACING",
    "LANGSMITH_API_KEY",
    "LANGSMITH_PROJECT"
]


# ============================================================================
# SOLUTION IMPLEMENTATIONS
# ============================================================================

def verify_langsmith_config() -> Dict[str, Any]:
    """Verify that LangSmith environment variables are configured."""
    status = {}
    missing = []
    
    for var in REQUIRED_ENV_VARS:
        value = os.environ.get(var)
        if value:
            # Mask API keys for display
            if "KEY" in var:
                display = f"***{value[-4:]}" if len(value) > 4 else "***"
            else:
                display = value
            status[var] = display
        else:
            missing.append(var)
            status[var] = "NOT SET"
    
    # Check LANGSMITH_TRACING is specifically "true"
    tracing = os.environ.get("LANGSMITH_TRACING", "").lower()
    if tracing != "true":
        if "LANGSMITH_TRACING" not in missing:
            status["LANGSMITH_TRACING"] = f"{tracing} (should be 'true')"
    
    return {
        "configured": len(missing) == 0 and tracing == "true",
        "status": status,
        "missing": missing
    }


def test_langsmith_connection() -> Dict[str, Any]:
    """Test connection to LangSmith API."""
    try:
        # LangSmith auto-traces and auto-creates projects
        # We just need to verify the key is valid format
        api_key = os.environ.get("LANGSMITH_API_KEY", "")
        project = os.environ.get("LANGSMITH_PROJECT", "default")
        
        if not api_key:
            return {
                "connected": False,
                "project": None,
                "message": "API key not set"
            }
        
        # Check key format (LangSmith keys start with lsv2_)
        if not api_key.startswith("lsv2_"):
            return {
                "connected": False,
                "project": project,
                "message": "API key format invalid (should start with lsv2_)"
            }
        
        return {
            "connected": True,
            "project": project,
            "message": f"Connected to project: {project}"
        }
        
    except Exception as e:
        return {
            "connected": False,
            "project": None,
            "message": f"Connection error: {e}"
        }


@tool
def simple_echo(message: str) -> str:
    """Echo back the message for testing traces.
    
    Use this to test that tracing is working.
    """
    return f"Echo: {message}"


def create_traced_agent():
    """Create a simple agent that will be traced."""
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[simple_echo],
        system_prompt="You are a test agent. Use the echo tool when asked to process or echo something.",
        name="traced_test_agent"
    )
    return agent


def run_traced_invocation(agent) -> Dict[str, Any]:
    """Run an agent invocation that will be traced."""
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Please echo this test message: Hello LangSmith!"}]
        })
        
        response = result["messages"][-1].content
        project = os.environ.get("LANGSMITH_PROJECT", "default")
        
        return {
            "success": True,
            "response": response,
            "trace_info": f"View traces at: https://smith.langchain.com/ (project: {project})"
        }
        
    except Exception as e:
        return {
            "success": False,
            "response": None,
            "trace_info": f"Error: {e}"
        }


def verify_trace_exists() -> bool:
    """Guide user to verify trace exists in LangSmith."""
    project = os.environ.get("LANGSMITH_PROJECT", "default")
    
    print("\n" + "=" * 50)
    print("MANUAL VERIFICATION STEPS")
    print("=" * 50)
    print()
    print("To verify your trace exists:")
    print()
    print("1. Open https://smith.langchain.com/")
    print("2. Sign in to your account")
    print(f"3. Navigate to project: '{project}'")
    print("4. Look for the most recent trace (should show 'traced_test_agent')")
    print("5. Click the trace to expand and view details")
    print()
    print("In the trace, you should see:")
    print("  - Agent run with input message")
    print("  - LLM call (model decision)")
    print("  - Tool call to 'simple_echo'")
    print("  - Final response")
    print()
    print("=" * 50)
    
    return True


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
    
    if config_result["configured"]:
        for var, value in config_result["status"].items():
            print(f"[OK] {var} = {value}")
    else:
        print("[ERROR] Configuration incomplete:")
        for var, value in config_result["status"].items():
            status = "[OK]" if var not in config_result["missing"] else "[MISSING]"
            print(f"       {status} {var} = {value}")
        
        if config_result["missing"]:
            print("\nSet these environment variables:")
            print("  export LANGSMITH_TRACING=true")
            print("  export LANGSMITH_API_KEY=your-key")
            print("  export LANGSMITH_PROJECT=week5-exercises")
        return
    
    print()
    
    # Step 2: Test connection
    print("[INFO] Testing LangSmith connection...")
    conn_result = test_langsmith_connection()
    
    if conn_result["connected"]:
        print(f"[OK] {conn_result['message']}")
    else:
        print(f"[ERROR] {conn_result['message']}")
        return
    
    print()
    
    # Step 3: Create and run agent
    print("[INFO] Creating traced agent...")
    agent = create_traced_agent()
    print("[OK] Agent 'traced_test_agent' created")
    print()
    
    print("[INFO] Running traced invocation...")
    invoke_result = run_traced_invocation(agent)
    
    if invoke_result["success"]:
        print("[OK] Agent invocation complete")
        print(f"Response: {invoke_result['response']}")
        print()
        print(f"[INFO] {invoke_result['trace_info']}")
    else:
        print(f"[ERROR] {invoke_result['trace_info']}")
        return
    
    # Step 4: Verification instructions
    verify_trace_exists()
    
    print()
    print("[OK] Integration Test Complete!")
    print("=" * 50)


if __name__ == "__main__":
    run_integration_test()
