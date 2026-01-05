"""
Exercise 02: Trace Analysis - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Run agent scenarios and analyze traces in LangSmith.

Instructions:
1. Ensure LangSmith is configured (from Exercise 01)
2. Run all test scenarios
3. Open LangSmith and analyze each trace
4. Complete the analysis template
"""

from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_core.tools import tool


# ============================================================================
# TOOLS FOR TRACE ANALYSIS
# ============================================================================

@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information.
    
    Use when the user asks about:
    - Documentation or how-to guides
    - Reference material
    - Configuration options
    """
    # Simulated search
    return f"Found documentation about: {query}"


@tool  
def run_calculation(expression: str) -> str:
    """Evaluate a mathematical expression.
    
    Use when the user needs to:
    - Calculate numbers
    - Do math operations
    - Convert units
    """
    try:
        # Safe eval for numbers only
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: Could not evaluate '{expression}'"


@tool
def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Use when the user asks about:
    - Weather conditions
    - Temperature
    - Forecast
    """
    # Simulated weather
    return f"Weather in {location}: Sunny, 72F"


# ============================================================================
# AGENT SETUP
# ============================================================================

def create_analysis_agent():
    """Create the agent for trace analysis."""
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[search_knowledge_base, run_calculation, get_weather],
        system_prompt="""You are a helpful assistant with access to tools.

Use the appropriate tool for each request:
- search_knowledge_base: For documentation and how-to questions
- run_calculation: For math and calculations
- get_weather: For weather information

If no tool is needed, respond directly.""",
        name="analysis_test_agent"
    )
    return agent


# ============================================================================
# TEST SCENARIOS
# ============================================================================

TEST_SCENARIOS = [
    {
        "id": 1,
        "name": "Clear Search Request",
        "message": "How do I configure database connections?",
        "expected_tool": "search_knowledge_base"
    },
    {
        "id": 2,
        "name": "Clear Calculation Request",
        "message": "What is 25 * 4 + 100?",
        "expected_tool": "run_calculation"
    },
    {
        "id": 3,
        "name": "Clear Weather Request",
        "message": "What's the weather like in New York?",
        "expected_tool": "get_weather"
    },
    {
        "id": 4,
        "name": "Ambiguous Request",
        "message": "Tell me about the 30% increase in temperature trends",
        "expected_tool": "varies"  # Could be calc or weather or search
    },
    {
        "id": 5,
        "name": "No Tool Needed",
        "message": "Hello, what can you help me with?",
        "expected_tool": None
    },
]


# ============================================================================
# TODO: IMPLEMENT TRACE ANALYSIS
# ============================================================================

def run_scenario(agent, scenario: Dict) -> Dict[str, Any]:
    """
    Run a single test scenario and return the result.
    
    Args:
        agent: The agent to test
        scenario: Dict with 'id', 'name', 'message', 'expected_tool'
        
    Returns:
        Dict with:
        - 'scenario_id': int
        - 'name': str
        - 'response': str
        - 'trace_url': str (placeholder - actual URL in LangSmith)
    """
    # TODO: Implement this function
    # result = agent.invoke({
    #     "messages": [{"role": "user", "content": scenario["message"]}]
    # })
    # return {
    #     "scenario_id": scenario["id"],
    #     "name": scenario["name"],
    #     "response": result["messages"][-1].content,
    #     "trace_url": "Check LangSmith dashboard"
    # }
    
    pass  # Remove this and add your implementation


def run_all_scenarios(agent) -> List[Dict[str, Any]]:
    """
    Run all test scenarios.
    
    Returns:
        List of results from each scenario
    """
    # TODO: Implement this function
    # results = []
    # for scenario in TEST_SCENARIOS:
    #     print(f"\nRunning: {scenario['name']}...")
    #     result = run_scenario(agent, scenario)
    #     results.append(result)
    # return results
    
    pass  # Remove this and add your implementation


def print_analysis_template(results: List[Dict[str, Any]]) -> None:
    """
    Print the trace analysis template for the user to complete.
    
    After running scenarios, users should open LangSmith and
    fill out this template for each trace.
    """
    # TODO: Implement this function
    # Print a template for each scenario that the user will
    # complete by analyzing the traces in LangSmith
    
    template = """
=== TRACE ANALYSIS TEMPLATE ===

Complete this for each trace in LangSmith:

Scenario {id}: {name}
Trace URL: [paste from LangSmith]

1. Tool Selection
   - Expected: {expected}
   - Actual: [fill in from trace]
   - Correct?: [Yes/No]

2. Token Usage
   - Input tokens: [from trace]
   - Output tokens: [from trace]
   
3. Latency
   - Total time: [from trace]
   
4. Observations
   [Your notes about agent behavior]

---
"""
    pass  # Remove this and add your implementation


def analyze_patterns(results: List[Dict[str, Any]]) -> None:
    """
    Guide the user through pattern analysis.
    
    Print questions for the user to answer after reviewing traces.
    """
    # TODO: Implement this function
    # Print analysis questions:
    # - What patterns do you see in tool selection?
    # - Were there any incorrect tool choices?
    # - What could improve the agent's decisions?
    
    pass  # Remove this and add your implementation


# ============================================================================
# FAILURE SCENARIO (for debugging practice)
# ============================================================================

def run_failure_scenario(agent) -> None:
    """
    Run a scenario designed to fail for debugging practice.
    
    This demonstrates how to use LangSmith to debug issues.
    """
    # TODO: Implement this function
    # Run a request that will cause a tool error
    # Example: run_calculation("undefined_variable + 5")
    # Then guide user to debug via LangSmith trace
    
    pass  # Remove this and add your implementation


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the trace analysis exercise."""
    print("=" * 60)
    print("Trace Analysis Exercise")
    print("=" * 60)
    print()
    
    print("[INFO] Creating agent for analysis...")
    agent = create_analysis_agent()
    print("[OK] Agent created")
    print()
    
    print("=" * 60)
    print("Running Test Scenarios")
    print("=" * 60)
    
    results = run_all_scenarios(agent)
    
    if results is None:
        print("[ERROR] run_all_scenarios() not implemented")
        return
    
    print()
    print("=" * 60)
    print("Analysis Template")
    print("=" * 60)
    
    print_analysis_template(results)
    
    print()
    print("=" * 60)
    print("Pattern Analysis Questions")
    print("=" * 60)
    
    analyze_patterns(results)
    
    print()
    print("=" * 60)
    print("Failure Scenario (Debug Practice)")
    print("=" * 60)
    
    run_failure_scenario(agent)
    
    print()
    print("=" * 60)
    print("Exercise Complete")
    print("=" * 60)
    print()
    print("Now open LangSmith and complete the analysis template!")
    print("https://smith.langchain.com/")


if __name__ == "__main__":
    main()
