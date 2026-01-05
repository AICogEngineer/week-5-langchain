# AWS Bedrock Setup Guide

## Quick Reference for Instructors

This guide provides step-by-step instructions for configuring AWS Bedrock access for LangChain integration.

---

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed (v2 recommended)
- Python 3.9+ with pip

---

## Step 1: Verify AWS Account Access

```bash
# Check if AWS CLI is configured
aws sts get-caller-identity

# Expected output:
# {
#     "UserId": "AIDAXXXXXXXXXXXXXXX",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-username"
# }
```

---

## Step 2: Configure IAM Permissions

### Minimum Required Policy

Create or attach this policy to your IAM user/role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel"
            ],
            "Resource": "*"
        }
    ]
}
```

### AWS Console Steps

1. Navigate to **IAM** → **Users** → Select your user
2. Click **Add permissions** → **Attach policies directly**
3. Click **Create policy** → **JSON** tab
4. Paste the policy above
5. Name it `BedrockAccessPolicy` and create
6. Attach to your user

---

## Step 3: Request Model Access

**Important:** Models must be explicitly enabled before use.

### AWS Console Steps

1. Navigate to **Amazon Bedrock** console
2. Select your region (recommend `us-east-1` for widest model availability)
3. Click **Model access** in the left sidebar
4. Click **Manage model access**
5. Check the models you need:
   - ✅ Claude 3.5 Sonnet (Anthropic)
   - ✅ Claude 3 Haiku (Anthropic)
   - ✅ Titan Text (Amazon)
6. Click **Request model access**
7. Wait for approval (usually instant, some models require form)

---

## Step 4: Configure Credentials

### Option A: Environment Variables (Recommended for Development)

```bash
# Windows PowerShell
$env:AWS_ACCESS_KEY_ID = "your-access-key"
$env:AWS_SECRET_ACCESS_KEY = "your-secret-key"
$env:AWS_DEFAULT_REGION = "us-east-1"

# Linux/macOS
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1
```

### Option B: AWS CLI Profile

```bash
aws configure
# Follow prompts:
# AWS Access Key ID: [enter your key]
# AWS Secret Access Key: [enter your secret]
# Default region name: us-east-1
# Default output format: json
```

### Option C: Named Profile (For Multiple Accounts)

```bash
aws configure --profile bedrock-demo
# Use with: AWS_PROFILE=bedrock-demo python your_script.py
```

---

## Step 5: Install Required Packages

```bash
pip install langchain langchain-aws boto3
```

---

## Step 6: Verify Bedrock Access

```python
"""
Test script to verify AWS Bedrock is accessible.
Run this before starting the demo.
"""
import boto3

def verify_bedrock_access():
    """List available Bedrock models to verify access."""
    client = boto3.client('bedrock', region_name='us-east-1')
    
    response = client.list_foundation_models()
    
    print("✅ Bedrock Access Verified!")
    print(f"   Available models: {len(response['modelSummaries'])}")
    print("\nRecommended models for demos:")
    
    demo_models = [
        'anthropic.claude-3-sonnet',
        'anthropic.claude-3-haiku',
        'amazon.titan-text'
    ]
    
    for model in response['modelSummaries']:
        for demo in demo_models:
            if demo in model['modelId']:
                print(f"   ✓ {model['modelId']}")

if __name__ == "__main__":
    verify_bedrock_access()
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `AccessDeniedException` | Missing IAM permissions | Attach BedrockAccessPolicy |
| `UnrecognizedClientException` | Invalid credentials | Run `aws configure` again |
| Model not in list | Model access not requested | Request in Bedrock console |
| `RegionDisabledException` | Bedrock not available in region | Switch to us-east-1 |
| Slow responses | Network latency | Use closest region |

---

## Region Availability

| Region | Claude 3 | Titan | Llama 3 |
|--------|----------|-------|---------|
| us-east-1 (N. Virginia) | ✅ | ✅ | ✅ |
| us-west-2 (Oregon) | ✅ | ✅ | ✅ |
| eu-west-1 (Ireland) | ✅ | ✅ | ⚠️ Limited |
| ap-northeast-1 (Tokyo) | ✅ | ✅ | ⚠️ Limited |

---

## Security Best Practices

1. **Never commit credentials** - Use environment variables or AWS profiles
2. **Use IAM roles** in production instead of access keys
3. **Restrict Resource** - Replace `"*"` with specific model ARNs in production
4. **Enable CloudTrail** - Log all Bedrock API calls
5. **Rotate credentials** - Regular key rotation policy

---

## Quick Verification Checklist

- [ ] AWS CLI configured (`aws sts get-caller-identity` works)
- [ ] IAM policy attached with Bedrock permissions
- [ ] Model access requested and approved
- [ ] Credentials set (env vars or profile)
- [ ] Python packages installed
- [ ] Test script runs without errors
