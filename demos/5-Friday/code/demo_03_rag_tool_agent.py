"""
Demo 03: RAG Tool Agent - Combining Vector Stores with Agents

This demo shows trainees how to:
1. Create a RAG tool using @tool decorator
2. Integrate vector stores with agents
3. Implement agentic RAG patterns
4. Build production-ready RAG agents

Learning Objectives:
- Build RAG tools for agent integration
- Understand 2-step vs agentic RAG
- Create agents with knowledge base access

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: January 2026

References:
- Written Content: readings/5-Friday/05-building-rag-tools-for-agents.md

Prerequisites (Week 3-4):
- Vector store concepts
- Embeddings
- Similarity search
"""

import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

from langchain import init_chat_model
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# PART 1: Setting Up a Simple Knowledge Base
# ============================================================================

print("=" * 70)
print("PART 1: Creating a Knowledge Base (Vector Store)")
print("=" * 70)

print("""
First, we need a knowledge base to search.
In production, this would be ChromaDB, Pinecone, etc.
For this demo, we'll use a simple in-memory simulation.
""")

# Simulated vector store with company documentation
# In production, you'd use:
# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings

KNOWLEDGE_BASE = {
    "refund_policy": {
        "content": """REFUND POLICY: Customers can request a full refund within 30 days 
        of purchase for any unused product. Used products may be eligible for partial 
        refund at management discretion. Digital products are non-refundable after 
        download. Refunds are processed within 5-7 business days to the original 
        payment method.""",
        "metadata": {"category": "policies", "last_updated": "2025-01-01"}
    },
    "shipping_info": {
        "content": """SHIPPING INFORMATION: Standard shipping takes 5-7 business days. 
        Express shipping (2-3 days) available for $12.99. Free shipping on orders 
        over $50. International shipping available to select countries with 
        additional customs fees. All orders include tracking number via email.""",
        "metadata": {"category": "logistics", "last_updated": "2025-01-01"}
    },
    "product_warranty": {
        "content": """WARRANTY COVERAGE: All electronics carry a 1-year manufacturer 
        warranty. Extended warranty available for purchase (2 or 3 year options). 
        Warranty covers defects in materials and workmanship. Does not cover 
        accidental damage, water damage, or misuse. Warranty claims require proof 
        of purchase.""",
        "metadata": {"category": "policies", "last_updated": "2025-01-01"}
    },
    "account_management": {
        "content": """ACCOUNT MANAGEMENT: Users can update profile information in 
        Settings > Profile. Password reset available via email verification. 
        Two-factor authentication recommended for security. Account deletion 
        requests processed within 48 hours. Contact support for account recovery.""",
        "metadata": {"category": "support", "last_updated": "2025-01-01"}
    },
    "payment_methods": {
        "content": """PAYMENT OPTIONS: We accept Visa, Mastercard, American Express, 
        and PayPal. Apple Pay and Google Pay available on mobile. Monthly payment 
        plans available for orders over $200 through Affirm. Gift cards accepted 
        both online and in-store.""",
        "metadata": {"category": "payments", "last_updated": "2025-01-01"}
    }
}

def simulate_search(query: str, k: int = 2) -> List[dict]:
    """Simulate vector similarity search."""
    # In production, this would be vectorstore.similarity_search()
    query_lower = query.lower()
    results = []
    
    for doc_id, doc in KNOWLEDGE_BASE.items():
        content_lower = doc["content"].lower()
        # Simple keyword matching (production would use embeddings)
        relevance_score = sum(1 for word in query_lower.split() if word in content_lower)
        if relevance_score > 0:
            results.append({
                "content": doc["content"],
                "metadata": doc["metadata"],
                "score": relevance_score
            })
    
    # Sort by relevance and return top k
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]

print("\n[Step 1] Testing simulated knowledge base...")
test_results = simulate_search("refund policy", k=2)
print(f"  Found {len(test_results)} relevant documents for 'refund policy'")
for i, doc in enumerate(test_results):
    print(f"    Doc {i+1}: {doc['content'][:60]}...")

# ============================================================================
# PART 2: Creating RAG Tool
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Creating the RAG Tool")
print("=" * 70)

print("""
The RAG tool wraps the vector store search.
The docstring tells the agent WHEN to use it.
""")

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the company knowledge base for relevant information.
    
    Use this tool when the user asks about:
    - Refund or return policies
    - Shipping information and delivery times
    - Warranty coverage and claims
    - Account settings and management
    - Payment methods and options
    
    Returns relevant documentation to answer customer questions.
    """
    results = simulate_search(query, k=2)
    
    if not results:
        return "No relevant information found in the knowledge base for this query."
    
    # Format results for the agent
    formatted = []
    for i, doc in enumerate(results, 1):
        formatted.append(f"Document {i}:\n{doc['content']}")
    
    return "\n\n---\n\n".join(formatted)

print("\n[Step 2] Testing RAG tool directly...")
result = search_knowledge_base.invoke({"query": "how do I get a refund?"})
print(f"  Tool output:\n    {result[:200]}...")

# ============================================================================
# PART 3: Building the RAG Agent
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Building the RAG Agent")
print("=" * 70)

print("""
Now we combine the RAG tool with an agent.
The agent decides when to search and synthesizes answers.
""")

rag_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_knowledge_base],
    system_prompt="""You are a helpful customer support agent for an e-commerce company.
    
    When customers ask questions about policies, shipping, warranties, accounts, or payments:
    1. Use the search_knowledge_base tool to find relevant information
    2. Synthesize the information into a helpful, conversational response
    3. Cite the source when providing policy details
    
    If the knowledge base doesn't have the answer, be honest and offer to connect 
    them with a human agent.
    
    Be friendly, professional, and concise.""",
    checkpointer=InMemorySaver(),
    name="rag_support_agent"
)

print("  ✓ RAG agent created: rag_support_agent")

config = {"configurable": {"thread_id": "customer_support_session_001"}}

# ============================================================================
# PART 4: Testing the RAG Agent
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Testing the RAG Agent")
print("=" * 70)

test_questions = [
    "Can I get a refund if I opened the product?",
    "How long does shipping take?",
    "What does the warranty cover?",
]

for question in test_questions:
    print(f"\n  Customer: {question}")
    result = rag_agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config
    )
    response = result['messages'][-1].content
    print(f"  Agent: {response[:200]}...")

# ============================================================================
# PART 5: 2-Step RAG vs Agentic RAG
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: 2-Step RAG vs Agentic RAG")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│                    2-STEP RAG vs AGENTIC RAG                        │
├──────────────────────┬──────────────────────────────────────────────┤
│ 2-STEP RAG           │ AGENTIC RAG                                  │
├──────────────────────┼──────────────────────────────────────────────┤
│ ALWAYS retrieves     │ Agent DECIDES when to retrieve               │
│                      │                                              │
│ Fixed k documents    │ Can adapt based on initial results           │
│                      │                                              │
│ Single query         │ Can reformulate or follow-up                 │
│                      │                                              │
│ Retrieve → Generate  │ Think → Retrieve? → Generate → Repeat?       │
│                      │                                              │
│ Simpler              │ More flexible                                │
│                      │                                              │
│ Lower latency        │ Potentially higher latency                   │
│                      │                                              │
│ Better for simple QA │ Better for complex interactions              │
└──────────────────────┴──────────────────────────────────────────────┘

When to use which:
- 2-Step: FAQ lookup, simple document QA, low latency needs
- Agentic: Multi-turn conversations, complex queries, when retrieval 
          is sometimes unnecessary
""")

# Demonstrate agentic behavior - agent decides NOT to search
print("\n[Step 5] Agent deciding when NOT to search...")

# Question that doesn't need knowledge base
general_question = "Hello! How are you today?"
print(f"\n  Customer: {general_question}")
result = rag_agent.invoke(
    {"messages": [{"role": "user", "content": general_question}]},
    {"configurable": {"thread_id": "agentic_demo"}}
)
response = result['messages'][-1].content
print(f"  Agent: {response}")
print("  (Notice: Agent didn't use the search tool for this greeting)")

# ============================================================================
# PART 6: Enhanced RAG Tool with Metadata
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: Enhanced RAG with Source Citations")
print("=" * 70)

@tool
def search_with_sources(query: str) -> str:
    """
    Search knowledge base and return results with source citations.
    
    Use for any customer question about company policies, products, or services.
    Results include source document information for citation.
    """
    results = simulate_search(query, k=2)
    
    if not results:
        return "No relevant information found."
    
    formatted = []
    for i, doc in enumerate(results, 1):
        source_info = f"[Source: {doc['metadata']['category'].upper()}, Updated: {doc['metadata']['last_updated']}]"
        formatted.append(f"{doc['content']}\n{source_info}")
    
    return "\n\n---\n\n".join(formatted)

print("\n[Step 6] Testing RAG with source citations...")
result = search_with_sources.invoke({"query": "warranty information"})
print(f"  {result[:300]}...")

# ============================================================================
# PART 7: Production Considerations
# ============================================================================

print("\n" + "=" * 70)
print("PART 7: Production RAG Agent Checklist")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│ PRODUCTION RAG AGENT CHECKLIST                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ☐ USE REAL VECTOR STORE                                             │
│   Replace simulation with ChromaDB, Pinecone, etc.                  │
│   vectorstore = Chroma(persist_directory="./db", ...)               │
│                                                                     │
│ ☐ QUALITY EMBEDDINGS                                                │
│   Use text-embedding-3-small or better                              │
│   Same model for indexing and querying!                             │
│                                                                     │
│ ☐ APPROPRIATE CHUNK SIZE                                            │
│   800-1200 characters typical                                       │
│   ~200 character overlap                                            │
│                                                                     │
│ ☐ RETRIEVAL TUNING                                                  │
│   Adjust k based on use case (3-5 typical)                          │
│   Consider MMR for diversity                                        │
│   Score thresholding for quality                                    │
│                                                                     │
│ ☐ ERROR HANDLING                                                    │
│   Handle empty results                                              │
│   Timeout for vector store queries                                  │
│   Fallback responses                                                │
│                                                                     │
│ ☐ MONITORING                                                        │
│   Log retrieval quality                                             │
│   Track which documents are used                                    │
│   Monitor latency                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: RAG Tool Agent")
print("=" * 70)

print("""
Key Takeaways:

1. RAG tools wrap vector store search with @tool decorator
2. Tool docstring tells agent when to search
3. Agent synthesizes search results into helpful responses
4. Agentic RAG = agent decides when/if to retrieve
5. Include source citations for trust and accuracy

Week 5 Complete!
You now have all the pieces for production LangChain agents:
- Model initialization (Monday)
- Tools and agents (Tuesday)
- Debugging with LangSmith (Wednesday)
- Memory and state (Thursday)
- Structured output and RAG (Friday)
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. How the agent decides to use the RAG tool
2. The difference when agent doesn't need to search
3. How to format results for best agent understanding

Live Demo Tips:
- Show traces in LangSmith to see tool calls
- Try questions that need multiple docs
- Show what happens with irrelevant queries

Discussion Questions:
- "How would you improve retrieval quality?"
- "When would you use 2-step vs agentic RAG?"
- "How do you handle when the knowledge base doesn't have the answer?"

Pair Programming Exercise:
Build a RAG agent for a different domain (e.g., HR policies, 
technical documentation, product catalog) using real ChromaDB.
""")

print("=" * 70)
