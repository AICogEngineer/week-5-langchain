"""
Exercise 02: Trace Analysis - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete solution for running scenarios and analyzing traces.
"""

from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_core.tools import tool


# ============================================================================
# TOOLS
# ============================================================================

@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information.
    
    Use when the user asks about:
    - Documentation or how-to guides
    - Reference material
    - Configuration options
    """
    return f"Found documentation about: {query}. This covers setup, configuration, and best practices."


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
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: Could not evaluate '{expression}' - {str(e)}"


@tool
def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Use when the user asks about:
    - Weather conditions
    - Temperature
    - Forecast
    """
    # Simulated weather data
    weather_data = {
        "new york": "Sunny, 72F, humidity 45%",
        "london": "Cloudy, 58F, humidity 70%",
        "tokyo": "Clear, 68F, humidity 55%"
    }
    location_lower = location.lower()
    for city, weather in weather_data.items():
        if city in location_lower:
            return f"Weather in {location}: {weather}"
    return f"Weather in {location}: Partly cloudy, 65F"


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

If no tool is needed, respond directly. Be concise in your responses.""",
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
        "expected_tool": "varies"
    },
    {
        "id": 5,
        "name": "No Tool Needed",
        "message": "Hello, what can you help me with?",
        "expected_tool": None
    },
]


# ============================================================================
# SOLUTION IMPLEMENTATIONS
# ============================================================================

def run_scenario(agent, scenario: Dict) -> Dict[str, Any]:
    """Run a single test scenario and return the result."""
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": scenario["message"]}]
        })
        
        response = result["messages"][-1].content
        
        return {
            "scenario_id": scenario["id"],
            "name": scenario["name"],
            "message": scenario["message"],
            "expected_tool": scenario["expected_tool"],
            "response": response[:200] + "..." if len(response) > 200 else response,
            "trace_url": "Check LangSmith dashboard for this trace"
        }
        
    except Exception as e:
        return {
            "scenario_id": scenario["id"],
            "name": scenario["name"],
            "error": str(e)
        }


def run_all_scenarios(agent) -> List[Dict[str, Any]]:
    """Run all test scenarios."""
    results = []
    
    for scenario in TEST_SCENARIOS:
        print(f"\n[INFO] Running Scenario {scenario['id']}: {scenario['name']}...")
        print(f"       Message: \"{scenario['message']}\"")
        
        result = run_scenario(agent, scenario)
        results.append(result)
        
        if "error" in result:
            print(f"[ERROR] {result['error']}")
        else:
            print(f"[OK] Response: {result['response'][:100]}...")
    
    return results


def print_analysis_template(results: List[Dict[str, Any]]) -> None:
    """Print the trace analysis template for the user to complete."""
    print()
    print("=" * 60)
    print("TRACE ANALYSIS TEMPLATE")
    print("=" * 60)
    print()
    print("Open LangSmith and complete this template for each trace.")
    print("Copy this template and fill in the details from your traces.")
    print()
    
    for result in results:
        if "error" in result:
            continue
            
        print("-" * 60)
        print(f"Scenario {result['scenario_id']}: {result['name']}")
        print("-" * 60)
        print(f"User Message: \"{result['message']}\"")
        print(f"Expected Tool: {result['expected_tool']}")
        print()
        print("Trace URL: [paste from LangSmith]")
        print()
        print("1. Tool Selection")
        print("   - Expected:", result['expected_tool'])
        print("   - Actual: [fill in from trace]")
        print("   - Correct?: [Yes/No]")
        print()
        print("2. Token Usage (from LangSmith)")
        print("   - Input tokens: ___")
        print("   - Output tokens: ___")
        print("   - Estimated cost: $___")
        print()
        print("3. Latency (from LangSmith)")
        print("   - Total time: ___ ms")
        print("   - LLM time: ___ ms")
        print("   - Tool time: ___ ms")
        print()
        print("4. Observations")
        print("   [Your notes about agent behavior]")
        print()


def analyze_patterns(results: List[Dict[str, Any]]) -> None:
    """Guide the user through pattern analysis."""
    print()
    print("=" * 60)
    print("PATTERN ANALYSIS QUESTIONS")
    print("=" * 60)
    print()
    print("After reviewing all traces, answer these questions:")
    print()
    print("1. TOOL SELECTION PATTERNS")
    print("   - What keywords trigger search_knowledge_base?")
    print("   - What makes the agent choose run_calculation?")
    print("   - When does the agent skip tools entirely?")
    print()
    print("2. DECISION QUALITY")
    print("   - Were there any incorrect tool choices?")
    print("   - How did the agent handle the ambiguous request?")
    print("   - Did the tool descriptions guide decisions well?")
    print()
    print("3. EFFICIENCY")
    print("   - Which scenario used the most tokens?")
    print("   - Were there unnecessary LLM calls?")
    print("   - How could prompts be optimized?")
    print()
    print("4. IMPROVEMENT OPPORTUNITIES")
    print("   - How could the system prompt be improved?")
    print("   - Should any tool descriptions be clarified?")
    print("   - Are there edge cases that need handling?")
    print()


def run_failure_scenario(agent) -> None:
    """Run a scenario designed to fail for debugging practice."""
    print()
    print("[INFO] Running failure scenario for debugging practice...")
    print()
    
    # Scenario that will cause a calculation error
    failure_message = "Calculate the result of undefined_variable + 5"
    
    print(f"Message: \"{failure_message}\"")
    print()
    
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": failure_message}]
        })
        
        response = result["messages"][-1].content
        print(f"Response: {response}")
        print()
        
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        print()
    
    print("DEBUGGING PRACTICE:")
    print("1. Find this trace in LangSmith")
    print("2. Expand the tool call to see the error")
    print("3. Look at what expression was passed to run_calculation")
    print("4. Notice how the agent handled (or didn't handle) the error")
    print()
    print("QUESTIONS:")
    print("- What caused the error?")
    print("- How did the error propagate through the agent?")
    print("- How could error handling be improved?")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the trace analysis exercise."""
    print("=" * 60)
    print("Trace Analysis Exercise - Solution")
    print("=" * 60)
    print()
    
    print("[INFO] Creating agent for analysis...")
    agent = create_analysis_agent()
    print("[OK] Agent 'analysis_test_agent' created")
    
    print()
    print("=" * 60)
    print("Running Test Scenarios")
    print("=" * 60)
    
    results = run_all_scenarios(agent)
    
    print_analysis_template(results)
    
    analyze_patterns(results)
    
    print("=" * 60)
    print("Failure Scenario (Debug Practice)")
    print("=" * 60)
    
    run_failure_scenario(agent)
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Open LangSmith: https://smith.langchain.com/")
    print("2. Review each trace from this session")
    print("3. Complete the analysis template above")
    print("4. Document your findings and improvement ideas")


if __name__ == "__main__":
    main()
