"""
Exercise 01: Structured Responses - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete solution for structured output with Pydantic models.
"""

from typing import List, Literal
from pydantic import BaseModel, Field
from langchain.agents import create_agent


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class TaskAnalysis(BaseModel):
    """Structured output for task complexity analysis."""
    
    task_name: str = Field(
        description="A concise name for the task being analyzed"
    )
    complexity: Literal["low", "medium", "high"] = Field(
        description="Overall complexity level of the task"
    )
    estimated_hours: float = Field(
        description="Estimated hours to complete the task",
        ge=0
    )
    required_skills: List[str] = Field(
        description="List of skills/technologies needed",
        default_factory=list
    )
    risks: List[str] = Field(
        description="Potential risks or challenges",
        default_factory=list
    )
    recommendation: str = Field(
        description="Brief recommendation or next steps"
    )


class ContentExtraction(BaseModel):
    """Structured output for content extraction from text."""
    
    title: str = Field(
        description="The main title or subject of the content"
    )
    summary: str = Field(
        description="A 2-3 sentence summary of the content"
    )
    key_points: List[str] = Field(
        description="List of main points or takeaways",
        default_factory=list
    )
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="Overall sentiment of the content"
    )


# ============================================================================
# AGENT CREATION
# ============================================================================

def create_task_analysis_agent():
    """Create an agent that outputs TaskAnalysis structured data."""
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        response_format=TaskAnalysis,
        system_prompt="""You are a project planning assistant that analyzes tasks.

For each task, provide a structured analysis including:
- A clear task name
- Complexity assessment (low/medium/high)
- Realistic time estimate in hours
- Required skills and technologies
- Potential risks or challenges
- A brief recommendation

Be thorough but realistic in your assessments.""",
        name="task_analyzer"
    )
    return agent


def create_content_extraction_agent():
    """Create an agent that outputs ContentExtraction structured data."""
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        response_format=ContentExtraction,
        system_prompt="""You are a content analysis assistant.

For any text provided, extract:
- The main title or subject
- A concise summary (2-3 sentences)
- Key points or takeaways (3-5 items)
- Overall sentiment (positive/negative/neutral)

Be objective and thorough in your extraction.""",
        name="content_extractor"
    )
    return agent


# ============================================================================
# VALIDATION
# ============================================================================

def validate_and_process_output(agent, input_text: str, expected_type: type):
    """Run agent and validate the structured output."""
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": input_text}]
        })
        
        # Access structured output from result
        # The exact key may vary based on LangChain version
        output = result.get("structured_output") or result.get("output")
        
        # If we got the raw response, try to parse
        if isinstance(output, expected_type):
            return {"success": True, "output": output, "errors": []}
        elif isinstance(output, dict):
            parsed = expected_type(**output)
            return {"success": True, "output": parsed, "errors": []}
        else:
            return {"success": False, "output": None, "errors": ["Unexpected output type"]}
            
    except Exception as e:
        return {"success": False, "output": None, "errors": [str(e)]}


# ============================================================================
# ERROR HANDLING
# ============================================================================

def create_fallback_output(output_type: type):
    """Create a fallback output for failed structured responses."""
    if output_type == TaskAnalysis:
        return TaskAnalysis(
            task_name="Unknown Task",
            complexity="medium",
            estimated_hours=0.0,
            required_skills=[],
            risks=["Could not analyze - please try again"],
            recommendation="Please provide more details and try again"
        )
    elif output_type == ContentExtraction:
        return ContentExtraction(
            title="Unknown Content",
            summary="Could not extract content summary.",
            key_points=[],
            sentiment="neutral"
        )
    return None


def handle_structured_errors(agent, input_text: str, expected_type: type, max_retries: int = 2):
    """Handle structured output with retry logic."""
    for attempt in range(max_retries + 1):
        result = validate_and_process_output(agent, input_text, expected_type)
        
        if result["success"]:
            return result["output"]
        
        if attempt < max_retries:
            print(f"[WARNING] Attempt {attempt + 1} failed: {result['errors']}")
            print("[INFO] Retrying...")
    
    print(f"[ERROR] Max retries ({max_retries}) exceeded, returning fallback")
    return create_fallback_output(expected_type)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the structured output exercise."""
    print("=" * 60)
    print("Exercise 01: Structured Responses - Solution")
    print("=" * 60)
    print()
    
    # Test TaskAnalysis
    print("[INFO] Creating TaskAnalysis agent...")
    task_agent = create_task_analysis_agent()
    print("[OK] Agent created")
    print()
    
    print("[INFO] Testing TaskAnalysis output...")
    task_input = """
    Analyze this task: Build an API integration with a third-party payment provider.
    It involves handling webhooks, implementing error retries, and ensuring PCI compliance.
    The team has experience with REST APIs but not payment processing.
    """
    
    result = validate_and_process_output(task_agent, task_input, TaskAnalysis)
    
    if result["success"]:
        output = result["output"]
        print("[OK] Structured output received:")
        print(f"  Task Name: {output.task_name}")
        print(f"  Complexity: {output.complexity}")
        print(f"  Estimated Hours: {output.estimated_hours}")
        print(f"  Required Skills: {output.required_skills}")
        print(f"  Risks: {output.risks}")
        print(f"  Recommendation: {output.recommendation}")
    else:
        print(f"[ERROR] {result['errors']}")
    print()
    
    # Test ContentExtraction
    print("[INFO] Creating ContentExtraction agent...")
    content_agent = create_content_extraction_agent()
    print("[OK] Agent created")
    print()
    
    print("[INFO] Testing ContentExtraction output...")
    content_input = """
    Q3 2024 Financial Results Announcement
    
    We are pleased to report a strong quarter with revenue up 23% year-over-year.
    Our cloud division saw particularly impressive growth, expanding to 50 new 
    enterprise customers. Customer satisfaction scores reached an all-time high
    of 94%, reflecting our focus on product quality.
    
    Looking ahead, we expect continued momentum with several major product launches
    planned for Q4. We remain committed to sustainable growth and shareholder value.
    """
    
    result = validate_and_process_output(content_agent, content_input, ContentExtraction)
    
    if result["success"]:
        output = result["output"]
        print("[OK] Structured output received:")
        print(f"  Title: {output.title}")
        print(f"  Summary: {output.summary[:100]}...")
        print(f"  Key Points: {output.key_points}")
        print(f"  Sentiment: {output.sentiment}")
    else:
        print(f"[ERROR] {result['errors']}")
    print()
    
    # Test error handling
    print("[INFO] Testing error handling with retry...")
    handled = handle_structured_errors(task_agent, task_input, TaskAnalysis)
    print(f"[OK] Got result of type: {type(handled).__name__}")
    print()
    
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
