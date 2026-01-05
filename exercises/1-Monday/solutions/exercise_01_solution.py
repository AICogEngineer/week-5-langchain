"""
Exercise 01: AWS Bedrock Connection - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

This solution demonstrates proper AWS Bedrock configuration and connection testing.
"""

import os
import time
from typing import Optional, Dict, Any

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from langchain import init_chat_model


# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_MODEL = "bedrock:anthropic.claude-3-haiku-20240307-v1:0"
EXPECTED_REGION = "us-east-1"


# ============================================================================
# SOLUTION IMPLEMENTATIONS
# ============================================================================

def verify_aws_credentials() -> Dict[str, Any]:
    """
    Verify that AWS credentials are properly configured.
    
    Returns:
        Dict with 'success', 'region', and 'message' keys
    """
    try:
        # Create a boto3 session to check credentials
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials is None:
            return {
                'success': False,
                'region': None,
                'message': 'No AWS credentials found'
            }
        
        # Check the region
        region = session.region_name or os.environ.get('AWS_DEFAULT_REGION', EXPECTED_REGION)
        
        # Verify credentials are valid by making a simple STS call
        sts = session.client('sts', region_name=region)
        identity = sts.get_caller_identity()
        
        return {
            'success': True,
            'region': region,
            'message': f"Credentials found for account {identity['Account']}"
        }
        
    except NoCredentialsError:
        return {
            'success': False,
            'region': None,
            'message': 'AWS credentials not configured'
        }
    except ClientError as e:
        return {
            'success': False,
            'region': None,
            'message': f'Invalid credentials: {e}'
        }
    except Exception as e:
        return {
            'success': False,
            'region': None,
            'message': f'Unexpected error: {e}'
        }


def initialize_bedrock_model(model_string: str = DEFAULT_MODEL):
    """
    Initialize a Bedrock model using init_chat_model().
    
    Returns:
        Initialized model instance or None if initialization fails
    """
    try:
        # Use the v1.0 init_chat_model() helper
        model = init_chat_model(model_string)
        return model
        
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        print("[INFO] Try: pip install langchain-aws")
        return None
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize model: {e}")
        return None


def test_model_connection(model) -> Dict[str, Any]:
    """
    Test the model connection with a simple invocation.
    
    Returns:
        Dict with 'success', 'response', 'response_time', and 'message' keys
    """
    test_message = "Say 'Hello, connection successful!' and nothing else."
    
    try:
        start_time = time.perf_counter()
        response = model.invoke(test_message)
        elapsed_time = time.perf_counter() - start_time
        
        # Extract response content
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        return {
            'success': True,
            'response': response_content,
            'response_time': elapsed_time,
            'message': 'Connection successful'
        }
        
    except Exception as e:
        return {
            'success': False,
            'response': None,
            'response_time': 0,
            'message': f'Connection failed: {e}'
        }


def diagnose_connection_issues() -> None:
    """
    Diagnose common connection issues and provide guidance.
    """
    print("\n--- Diagnostics ---\n")
    
    # Check environment variables
    env_vars = {
        'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
        'AWS_DEFAULT_REGION': os.environ.get('AWS_DEFAULT_REGION'),
    }
    
    print("Environment Variables:")
    for var, value in env_vars.items():
        status = "[OK]" if value else "[MISSING]"
        masked = f"***{value[-4:]}" if value else "Not set"
        print(f"  {status} {var}: {masked}")
    
    # Check for credentials file
    creds_file = os.path.expanduser("~/.aws/credentials")
    config_file = os.path.expanduser("~/.aws/config")
    
    print("\nAWS Configuration Files:")
    print(f"  {'[OK]' if os.path.exists(creds_file) else '[MISSING]'} {creds_file}")
    print(f"  {'[OK]' if os.path.exists(config_file) else '[MISSING]'} {config_file}")
    
    # Remediation steps
    print("\nRemediation Steps:")
    if not any(env_vars.values()) and not os.path.exists(creds_file):
        print("  1. Run 'aws configure' to set up credentials")
        print("  2. Or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
    
    print("  - Verify Bedrock model access is enabled in AWS Console")
    print("  - Ensure you're using a region where Bedrock is available")
    print("  - Check your IAM permissions include bedrock:InvokeModel")
    
    print("\n--- End Diagnostics ---\n")


# ============================================================================
# TEST HARNESS
# ============================================================================

def run_connection_test():
    """Run the complete Bedrock connection test suite."""
    print("=" * 50)
    print("AWS Bedrock Connection Test")
    print("=" * 50)
    print()
    
    all_passed = True
    
    # Step 1: Verify AWS credentials
    print("[INFO] Checking AWS credentials...")
    cred_result = verify_aws_credentials()
    
    if cred_result.get('success'):
        print(f"[OK] {cred_result.get('message')} (region: {cred_result.get('region')})")
    else:
        print(f"[ERROR] {cred_result.get('message')}")
        print("[INFO] Running diagnostics...")
        diagnose_connection_issues()
        all_passed = False
    
    print()
    
    # Step 2: Initialize model
    print("[INFO] Initializing Bedrock model...")
    model = initialize_bedrock_model()
    
    if model is None:
        print("[ERROR] Model initialization failed")
        all_passed = False
    else:
        print(f"[OK] Model initialized: {DEFAULT_MODEL}")
    
    print()
    
    # Step 3: Test connection
    if model is not None:
        print("[INFO] Testing model connection...")
        test_result = test_model_connection(model)
        
        if test_result.get('success'):
            print(f"[OK] Response received in {test_result.get('response_time', 0):.2f}s")
            print(f"Response: {test_result.get('response', 'N/A')}")
        else:
            print(f"[ERROR] {test_result.get('message')}")
            all_passed = False
    
    print()
    print("=" * 50)
    if all_passed:
        print("[OK] Connection Test Complete - All checks passed!")
    else:
        print("[INFO] Some checks failed. Review the errors above.")
    print("=" * 50)


if __name__ == "__main__":
    run_connection_test()
