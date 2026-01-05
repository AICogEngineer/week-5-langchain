"""
Exercise 02: Model Exploration - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

This solution demonstrates multi-provider model comparison using init_chat_model().
"""

import time
from typing import Dict, List, Any

from langchain import init_chat_model


# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_CONFIGS = [
    "openai:gpt-4o-mini",
    # Uncomment if you have access to these providers:
    # "anthropic:claude-3-haiku-20240307",
    # "bedrock:anthropic.claude-3-haiku-20240307-v1:0",
]

TEST_PROMPTS = [
    "What is Python?",
    "Explain REST APIs briefly.",
    "What is machine learning?",
    "Define microservices.",
    "What is cloud computing?",
]


# ============================================================================
# SOLUTION IMPLEMENTATIONS
# ============================================================================

def setup_models(model_strings: List[str] = MODEL_CONFIGS) -> Dict[str, Any]:
    """
    Initialize multiple models using init_chat_model().
    """
    models = {}
    
    for model_str in model_strings:
        try:
            print(f"  Initializing {model_str}...")
            model = init_chat_model(model_str)
            models[model_str] = model
            print(f"  [OK] {model_str} ready")
        except Exception as e:
            print(f"  [ERROR] Failed to initialize {model_str}: {e}")
    
    return models


def compare_invoke(models: Dict[str, Any], prompt: str) -> List[Dict[str, Any]]:
    """
    Compare .invoke() responses across all models.
    """
    results = []
    
    for model_str, model in models.items():
        try:
            start = time.perf_counter()
            response = model.invoke(prompt)
            elapsed = time.perf_counter() - start
            
            content = response.content if hasattr(response, 'content') else str(response)
            
            results.append({
                'model': model_str,
                'response': content[:100] + "..." if len(content) > 100 else content,
                'time': elapsed
            })
            
        except Exception as e:
            results.append({
                'model': model_str,
                'response': f"Error: {e}",
                'time': 0
            })
    
    return results


def test_batch_processing(models: Dict[str, Any], prompts: List[str] = TEST_PROMPTS) -> List[Dict[str, Any]]:
    """
    Test batch processing with .batch() method.
    """
    results = []
    
    for model_str, model in models.items():
        try:
            start = time.perf_counter()
            responses = model.batch(prompts)
            total_time = time.perf_counter() - start
            
            throughput = len(prompts) / total_time if total_time > 0 else 0
            
            response_contents = [
                r.content if hasattr(r, 'content') else str(r)
                for r in responses
            ]
            
            results.append({
                'model': model_str,
                'total_time': total_time,
                'throughput': throughput,
                'responses': [c[:50] + "..." for c in response_contents]
            })
            
        except Exception as e:
            results.append({
                'model': model_str,
                'total_time': 0,
                'throughput': 0,
                'responses': [f"Error: {e}"]
            })
    
    return results


def compare_streaming(models: Dict[str, Any], prompt: str) -> List[Dict[str, Any]]:
    """
    Compare streaming behavior across models.
    """
    results = []
    
    for model_str, model in models.items():
        try:
            first_token_time = None
            content = ""
            
            print(f"\n  Streaming from {model_str}:")
            print("  ", end="")
            
            start = time.perf_counter()
            
            for chunk in model.stream(prompt):
                if first_token_time is None:
                    first_token_time = time.perf_counter() - start
                
                chunk_content = chunk.content if hasattr(chunk, 'content') else str(chunk)
                content += chunk_content
                print(chunk_content, end="", flush=True)
            
            total_time = time.perf_counter() - start
            print()  # New line after streaming
            
            results.append({
                'model': model_str,
                'time_to_first_token': first_token_time or 0,
                'total_time': total_time,
                'response': content
            })
            
        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append({
                'model': model_str,
                'time_to_first_token': 0,
                'total_time': 0,
                'response': f"Error: {e}"
            })
    
    return results


def print_comparison_table(results: List[Dict[str, Any]], title: str) -> None:
    """
    Pretty-print comparison results as a table.
    """
    if not results:
        print("No results to display")
        return
    
    # Get all keys excluding complex types
    keys = [k for k in results[0].keys() if k != 'responses']
    
    # Calculate column widths
    widths = {}
    for key in keys:
        values = [str(r.get(key, ''))[:40] for r in results]
        widths[key] = max(len(key), max(len(v) for v in values))
    
    # Print header
    header = " | ".join(key.ljust(widths[key]) for key in keys)
    print(header)
    print("-" * len(header))
    
    # Print rows
    for result in results:
        row_values = []
        for key in keys:
            value = result.get(key, '')
            if isinstance(value, float):
                value = f"{value:.2f}"
            else:
                value = str(value)[:40]
            row_values.append(value.ljust(widths[key]))
        print(" | ".join(row_values))


# ============================================================================
# TEST HARNESS
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
    
    if not models:
        print("[ERROR] No models initialized - check your API keys and providers")
        return
    
    print(f"\n[OK] {len(models)} model(s) ready")
    print()
    
    # Step 2: Compare invoke
    print("=" * 60)
    print("Invoke Comparison")
    print("=" * 60)
    test_prompt = "Explain what an API is in one sentence."
    print(f'Prompt: "{test_prompt}"')
    print()
    
    invoke_results = compare_invoke(models, test_prompt)
    print_comparison_table(invoke_results, "Invoke Results")
    print()
    
    # Step 3: Batch processing
    print("=" * 60)
    print("Batch Processing")
    print("=" * 60)
    print(f"Processing {len(TEST_PROMPTS)} prompts...")
    print()
    
    batch_results = test_batch_processing(models)
    print_comparison_table(batch_results, "Batch Results")
    print()
    
    # Step 4: Streaming test
    print("=" * 60)
    print("Streaming Test")
    print("=" * 60)
    stream_prompt = "Write a haiku about programming."
    print(f'Prompt: "{stream_prompt}"')
    
    stream_results = compare_streaming(models, stream_prompt)
    print()
    print("\nStreaming Summary:")
    print_comparison_table(stream_results, "Streaming Results")
    print()
    
    print("=" * 60)
    print("Exploration Complete")
    print("=" * 60)


if __name__ == "__main__":
    run_exploration()
