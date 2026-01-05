"""
Exercise 01: Structured Responses - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Implement structured output using Pydantic models.

Instructions:
1. Define Pydantic schemas for structured output
2. Create agents with response_format parameter
3. Validate and process structured responses
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# ============================================================================
# IMPORTS
# ============================================================================

# TODO: Import create_agent
# from langchain.agents import create_agent


# ============================================================================
# TODO: TASK 1 - Define Output Schemas
# ============================================================================

class TaskAnalysis(BaseModel):
    """Structured output for task complexity analysis."""
    
    # TODO: Define these fields with proper Field descriptions
    # task_name: str = Field(description="Name of the task being analyzed")
    # complexity: Literal["low", "medium", "high"] = Field(...)
    # estimated_hours: float = Field(...)
    # required_skills: List[str] = Field(...)
    # risks: List[str] = Field(...)
    # recommendation: str = Field(...)
    
    pass  # Remove this and add your field definitions


class ContentExtraction(BaseModel):
    """Structured output for content extraction from text."""
    
    # TODO: Define these fields with proper Field descriptions
    # title: str = Field(...)
    # summary: str = Field(...)
    # key_points: List[str] = Field(...)
    # sentiment: Literal["positive", "negative", "neutral"] = Field(...)
    
    pass  # Remove this and add your field definitions


# ============================================================================
# TODO: TASK 2 - Structured Agent Creation
# ============================================================================

def create_task_analysis_agent():
    """
    Create an agent that outputs TaskAnalysis structured data.
    
    Requirements:
    - Use create_agent() with response_format=TaskAnalysis
    - Include the 'name' parameter
    - Write a system prompt explaining the task
    
    Returns:
        Configured agent for task analysis
    """
    # TODO: Implement this function
    #
    # agent = create_agent(
    #     model="openai:gpt-4o-mini",
    #     tools=[],
    #     response_format=TaskAnalysis,
    #     system_prompt="""You are a project planning assistant.
    #     Analyze tasks and provide structured assessments including:
    #     - Complexity level
    #     - Time estimates
    #     - Required skills
    #     - Potential risks
    #     - Recommendations""",
    #     name="task_analyzer"
    # )
    # return agent
    
    pass  # Remove this and add your implementation


def create_content_extraction_agent():
    """
    Create an agent that outputs ContentExtraction structured data.
    
    Returns:
        Configured agent for content extraction
    """
    # TODO: Implement this function
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 3 - Output Validation
# ============================================================================

def validate_and_process_output(agent, input_text: str, expected_type: type):
    """
    Run agent and validate the structured output.
    
    Args:
        agent: The structured output agent
        input_text: The input to send to the agent
        expected_type: The Pydantic model class expected
        
    Returns:
        Dict with:
        - 'success': bool
        - 'output': The validated Pydantic model or None
        - 'errors': List of validation errors if any
    """
    # TODO: Implement this function
    #
    # try:
    #     result = agent.invoke({
    #         "messages": [{"role": "user", "content": input_text}]
    #     })
    #     
    #     # Access the structured output
    #     output = result.get("structured_output")
    #     
    #     # Validate against expected type
    #     if isinstance(output, expected_type):
    #         return {"success": True, "output": output, "errors": []}
    #     else:
    #         return {"success": False, "output": None, "errors": ["Type mismatch"]}
    #         
    # except Exception as e:
    #     return {"success": False, "output": None, "errors": [str(e)]}
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 4 - Error Handling
# ============================================================================

def handle_structured_errors(agent, input_text: str, expected_type: type, max_retries: int = 2):
    """
    Handle structured output with retry logic.
    
    Args:
        agent: The structured output agent
        input_text: The input to send
        expected_type: Expected Pydantic model
        max_retries: Maximum retry attempts
        
    Returns:
        Validated output or fallback values
    """
    # TODO: Implement this function
    #
    # for attempt in range(max_retries + 1):
    #     result = validate_and_process_output(agent, input_text, expected_type)
    #     if result["success"]:
    #         return result["output"]
    #     
    #     if attempt < max_retries:
    #         print(f"[WARNING] Attempt {attempt + 1} failed, retrying...")
    # 
    # # Return fallback
    # print("[ERROR] Max retries exceeded, returning fallback")
    # return create_fallback_output(expected_type)
    
    pass  # Remove this and add your implementation


def create_fallback_output(output_type: type):
    """Create a fallback output for failed structured responses."""
    # TODO: Implement fallback creation for each type
    
    pass  # Remove this and add your implementation


# ============================================================================
# TEST HARNESS
# ============================================================================

def main():
    """Run the structured output exercise."""
    print("=" * 60)
    print("Exercise 01: Structured Responses")
    print("=" * 60)
    print()
    
    # Task 1: Test schema definitions
    print("[INFO] Testing schema definitions...")
    try:
        # Test TaskAnalysis schema
        test_task = TaskAnalysis(
            task_name="Test Task",
            complexity="medium",
            estimated_hours=4.0,
            required_skills=["Python"],
            risks=["None"],
            recommendation="Proceed"
        )
        print(f"[OK] TaskAnalysis schema valid")
    except Exception as e:
        print(f"[ERROR] TaskAnalysis schema: {e}")
    
    try:
        # Test ContentExtraction schema
        test_content = ContentExtraction(
            title="Test",
            summary="Summary",
            key_points=["Point 1"],
            sentiment="neutral"
        )
        print(f"[OK] ContentExtraction schema valid")
    except Exception as e:
        print(f"[ERROR] ContentExtraction schema: {e}")
    
    print()
    
    # Task 2: Create and test agents
    print("[INFO] Creating TaskAnalysis agent...")
    task_agent = create_task_analysis_agent()
    
    if task_agent is None:
        print("[ERROR] create_task_analysis_agent() not implemented")
        return
    
    print("[OK] Agent created")
    print()
    
    # Task 3: Validate output
    print("[INFO] Testing TaskAnalysis output...")
    test_input = """
    Analyze this task: Build an API integration with a third-party payment provider.
    It involves handling webhooks, error retries, and PCI compliance.
    """
    
    result = validate_and_process_output(task_agent, test_input, TaskAnalysis)
    
    if result is None:
        print("[ERROR] validate_and_process_output() not implemented")
    elif result.get("success"):
        output = result["output"]
        print("[OK] Structured output received:")
        print(f"    Task: {output.task_name}")
        print(f"    Complexity: {output.complexity}")
        print(f"    Hours: {output.estimated_hours}")
        print(f"    Skills: {output.required_skills}")
    else:
        print(f"[ERROR] Validation failed: {result.get('errors')}")
    
    print()
    
    # Task 4: Error handling
    print("[INFO] Testing error handling...")
    handled_result = handle_structured_errors(task_agent, test_input, TaskAnalysis)
    
    if handled_result is None:
        print("[ERROR] handle_structured_errors() not implemented")
    else:
        print(f"[OK] Error handling working, got output of type: {type(handled_result).__name__}")
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
