"""
Exercise 02: Model Exploration - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Explore different model providers and invocation patterns.

Instructions:
1. Implement each TODO function
2. Run this file to test your implementations
3. Compare model behaviors across providers
"""

import time
from typing import Dict, List, Any

# ============================================================================
# IMPORTS - Add any additional imports you need
# ============================================================================

# TODO: Import init_chat_model from langchain
# from langchain import init_chat_model


# ============================================================================
# CONFIGURATION
# ============================================================================

# Models to compare (modify based on your available providers)
MODEL_CONFIGS = [
    "openai:gpt-4o-mini",
    # "anthropic:claude-3-haiku-20240307",
    # "bedrock:anthropic.claude-3-haiku-20240307-v1:0",
]

# Test prompts for batch processing
TEST_PROMPTS = [
    "What is Python?",
    "Explain REST APIs briefly.",
    "What is machine learning?",
    "Define microservices.",
    "What is cloud computing?",
]


# ============================================================================
# TODO: IMPLEMENT THESE FUNCTIONS
# ============================================================================

def setup_models(model_strings: List[str] = MODEL_CONFIGS) -> Dict[str, Any]:
    """
    Initialize multiple models using init_chat_model().
    
    Tasks:
    - Iterate through the model strings
    - Initialize each model using init_chat_model()
    - Store successfully initialized models in a dictionary
    - Handle initialization errors gracefully
    
    Args:
        model_strings: List of provider strings like "openai:gpt-4o-mini"
        
    Returns:
        Dict mapping model string to initialized model instance
        
    Example:
        models = setup_models()
        # {"openai:gpt-4o-mini": <ChatOpenAI>, "anthropic:claude": <ChatAnthropic>}
    """
    # TODO: Implement this function
    # Hint: from langchain import init_chat_model
    # for model_str in model_strings:
    #     try:
    #         model = init_chat_model(model_str)
    #         models[model_str] = model
    #     except Exception as e:
    #         print(f"Failed to init {model_str}: {e}")
    
    pass  # Remove this and add your implementation


def compare_invoke(models: Dict[str, Any], prompt: str) -> List[Dict[str, Any]]:
    """
    Compare .invoke() responses across all models.
    
    Tasks:
    - Send the same prompt to each model
    - Measure response time for each
    - Collect the response content
    - Return comparison results
    
    Args:
        models: Dict of model_string -> model instance
        prompt: The prompt to send to all models
        
    Returns:
        List of dicts with keys:
        - 'model': str (model string)
        - 'response': str (model's response content)
        - 'time': float (response time in seconds)
    """
    # TODO: Implement this function
    # Hint: Use time.perf_counter() for timing
    # start = time.perf_counter()
    # response = model.invoke(prompt)
    # elapsed = time.perf_counter() - start
    
    pass  # Remove this and add your implementation


def test_batch_processing(models: Dict[str, Any], prompts: List[str] = TEST_PROMPTS) -> List[Dict[str, Any]]:
    """
    Test batch processing with .batch() method.
    
    Tasks:
    - Process multiple prompts using .batch()
    - Measure total processing time
    - Calculate throughput (prompts per second)
    
    Args:
        models: Dict of model_string -> model instance
        prompts: List of prompts to process
        
    Returns:
        List of dicts with keys:
        - 'model': str
        - 'total_time': float
        - 'throughput': float (prompts/second)
        - 'responses': List[str]
    """
    # TODO: Implement this function
    # Hint: responses = model.batch(prompts)
    
    pass  # Remove this and add your implementation


def compare_streaming(models: Dict[str, Any], prompt: str) -> List[Dict[str, Any]]:
    """
    Compare streaming behavior across models.
    
    Tasks:
    - Stream a response from each model using .stream()
    - Measure time-to-first-token
    - Measure total streaming time
    - Optionally display streaming output
    
    Args:
        models: Dict of model_string -> model instance
        prompt: The prompt to stream
        
    Returns:
        List of dicts with keys:
        - 'model': str
        - 'time_to_first_token': float
        - 'total_time': float
        - 'response': str (complete response)
    """
    # TODO: Implement this function
    # Hint: 
    # for chunk in model.stream(prompt):
    #     if first_token_time is None:
    #         first_token_time = time.perf_counter() - start
    #     content += chunk.content
    
    pass  # Remove this and add your implementation


def print_comparison_table(results: List[Dict[str, Any]], title: str) -> None:
    """
    Pretty-print comparison results as a table.
    
    Args:
        results: List of result dictionaries
        title: Table title
    """
    # TODO: Implement this function
    # Format results as a readable table
    
    pass  # Remove this and add your implementation


# ============================================================================
# TEST HARNESS (DO NOT MODIFY)
# ============================================================================

def run_exploration():
    """Run the complete model exploration test suite."""
    print("=" * 60)
    print("Model Exploration")
    print("=" * 60)
    print()
    
    # Step 1: Initialize models
    print("[INFO] Initializing models...")
    models = setup_models()
    
    if models is None or len(models) == 0:
        print("[ERROR] No models initialized - check setup_models() implementation")
        return
    
    print(f"[OK] {len(models)} model(s) ready")
    print()
    
    # Step 2: Compare invoke
    print("=" * 60)
    print("Invoke Comparison")
    print("=" * 60)
    test_prompt = "Explain what an API is in one sentence."
    print(f'Prompt: "{test_prompt}"')
    print()
    
    invoke_results = compare_invoke(models, test_prompt)
    if invoke_results:
        print_comparison_table(invoke_results, "Invoke Results")
    else:
        print("[ERROR] compare_invoke() not implemented")
    print()
    
    # Step 3: Batch processing
    print("=" * 60)
    print("Batch Processing")
    print("=" * 60)
    print(f"Processing {len(TEST_PROMPTS)} prompts...")
    print()
    
    batch_results = test_batch_processing(models)
    if batch_results:
        print_comparison_table(batch_results, "Batch Results")
    else:
        print("[ERROR] test_batch_processing() not implemented")
    print()
    
    # Step 4: Streaming test
    print("=" * 60)
    print("Streaming Test")
    print("=" * 60)
    stream_prompt = "Write a haiku about programming."
    print(f'Prompt: "{stream_prompt}"')
    print()
    
    stream_results = compare_streaming(models, stream_prompt)
    if stream_results:
        print_comparison_table(stream_results, "Streaming Results")
    else:
        print("[ERROR] compare_streaming() not implemented")
    print()
    
    print("=" * 60)
    print("Exploration Complete")
    print("=" * 60)


if __name__ == "__main__":
    run_exploration()
