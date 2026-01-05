"""
Exercise 02: RAG Agent - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete solution for RAG agent with vector store integration.
"""

from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================================
# SAMPLE DOCUMENTS
# ============================================================================

SAMPLE_DOCS = [
    {
        "content": """Authentication Configuration Guide
        
        Our API supports OAuth 2.0 authentication. To configure:
        1. Set AUTH_PROVIDER='oauth' in environment
        2. Provide CLIENT_ID and CLIENT_SECRET
        3. Configure the callback URL in your OAuth app
        
        For API key authentication, set AUTH_PROVIDER='api_key' and provide API_KEY.""",
        "metadata": {"topic": "authentication", "section": "configuration"}
    },
    {
        "content": """Rate Limiting Documentation
        
        Rate limiting protects the API from abuse. Configuration:
        - RATE_LIMIT_PER_MINUTE: Requests per minute (default: 100)
        - RATE_LIMIT_BURST: Allow burst requests (default: 20)
        
        When rate limited, API returns 429 status with Retry-After header.""",
        "metadata": {"topic": "rate-limiting", "section": "configuration"}
    },
    {
        "content": """Database Connection Setup
        
        Configure database connections with these environment variables:
        - DATABASE_URL: Full connection string
        - DB_POOL_SIZE: Connection pool size (default: 10)
        - DB_TIMEOUT: Query timeout in seconds (default: 30)
        
        The application supports PostgreSQL, MySQL, and SQLite.""",
        "metadata": {"topic": "database", "section": "setup"}
    },
    {
        "content": """Error Handling Best Practices
        
        All API errors return a consistent JSON structure:
        {
            "error": true,
            "code": "ERROR_CODE",
            "message": "Human readable message",
            "details": {}
        }
        
        Common error codes: AUTH_FAILED, RATE_LIMITED, NOT_FOUND, VALIDATION_ERROR""",
        "metadata": {"topic": "errors", "section": "api"}
    },
    {
        "content": """Logging Configuration
        
        Configure logging with LOG_LEVEL environment variable:
        - DEBUG: All messages including debug info
        - INFO: Standard operational messages
        - WARNING: Warning and error messages only
        - ERROR: Error messages only
        
        Logs are output in JSON format for easy parsing.""",
        "metadata": {"topic": "logging", "section": "configuration"}
    },
]


# ============================================================================
# VECTOR STORE SETUP
# ============================================================================

def setup_vector_store(documents: List[Dict] = SAMPLE_DOCS):
    """Set up ChromaDB vector store with sample documents."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Convert to Document objects
    docs = [
        Document(page_content=d["content"], metadata=d["metadata"])
        for d in documents
    ]
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./chroma_rag_exercise",
        collection_name="documentation"
    )
    
    return vectorstore


# ============================================================================
# RETRIEVAL TOOL
# ============================================================================

# Global vectorstore reference
_vectorstore = None


def create_search_tool(vectorstore):
    """Create a search tool for the RAG agent."""
    global _vectorstore
    _vectorstore = vectorstore
    
    @tool
    def search_documents(query: str) -> str:
        """Search the documentation for relevant information.
        
        Use this tool when the user asks about:
        - How to configure something (auth, database, logging, etc.)
        - API features or capabilities
        - Error codes or troubleshooting
        - Setup or installation steps
        
        Args:
            query: The search terms or question
            
        Returns:
            Relevant documentation excerpts
        """
        docs = _vectorstore.similarity_search(query, k=3)
        
        if not docs:
            return "No relevant documentation found for your query."
        
        results = []
        for i, doc in enumerate(docs, 1):
            topic = doc.metadata.get("topic", "general")
            section = doc.metadata.get("section", "")
            header = f"[Doc {i} - {topic}/{section}]"
            results.append(f"{header}\n{doc.page_content}")
        
        return "\n\n---\n\n".join(results)
    
    return search_documents


# ============================================================================
# RAG AGENT
# ============================================================================

def create_rag_agent(search_tool, strategy: str = "agentic"):
    """Create a RAG agent with the search tool."""
    
    if strategy == "2step":
        system_prompt = """You are a documentation assistant for our software product.

IMPORTANT RULE: You MUST use the search_documents tool for ANY question about the product.

Process:
1. First, ALWAYS search for relevant documentation
2. Then, synthesize an answer from what you found
3. If no relevant docs are found, clearly state that
4. Always mention which topics your answer draws from

Never answer questions about the product from memory - always search first."""
    else:
        system_prompt = """You are a friendly documentation assistant for our software product.

You have access to search_documents for finding information in our documentation.

Guidelines:
- Use search_documents when users ask about configuration, setup, features, or errors
- For general greetings or off-topic questions, respond directly without searching
- When you search, synthesize the information into a helpful answer
- Always cite which documentation topics your answer comes from
- If you search and find nothing relevant, say so clearly

Be helpful, accurate, and concise."""

    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[search_tool],
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt,
        name="rag_assistant"
    )
    
    return agent


# ============================================================================
# STRATEGY COMPARISON
# ============================================================================

def compare_rag_strategies(vectorstore) -> Dict[str, Any]:
    """Compare 2-Step RAG vs Agentic RAG strategies."""
    
    test_questions = [
        ("How do I configure authentication?", True),  # Should search
        ("What's the default rate limit?", True),       # Should search
        ("Hello, who are you?", False),                 # Should NOT search
        ("How do I set up database connections?", True), # Should search
        ("What's 2 + 2?", False),                       # Should NOT search
    ]
    
    results = {
        "2step": {"total_searches": 0, "responses": []},
        "agentic": {"total_searches": 0, "responses": []}
    }
    
    for strategy in ["2step", "agentic"]:
        print(f"\n--- Testing {strategy} strategy ---")
        
        search_tool = create_search_tool(vectorstore)
        agent = create_rag_agent(search_tool, strategy)
        
        for question, should_search in test_questions:
            config = {"configurable": {"thread_id": f"{strategy}_test"}}
            
            try:
                result = agent.invoke(
                    {"messages": [{"role": "user", "content": question}]},
                    config
                )
                
                response = result["messages"][-1].content
                
                # Check if search was used (simplified check)
                messages = result.get("messages", [])
                search_used = any(
                    hasattr(m, "type") and m.type == "tool" 
                    for m in messages
                )
                
                if search_used:
                    results[strategy]["total_searches"] += 1
                
                results[strategy]["responses"].append({
                    "question": question,
                    "should_search": should_search,
                    "did_search": search_used,
                    "response": response[:100]
                })
                
                print(f"  Q: {question[:40]}...")
                print(f"    Searched: {search_used}, Should: {should_search}")
                
            except Exception as e:
                print(f"  Q: {question[:40]}... [ERROR: {e}]")
    
    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the RAG agent exercise."""
    print("=" * 60)
    print("Exercise 02: RAG Agent - Solution")
    print("=" * 60)
    print()
    
    # Setup vector store
    print("[INFO] Setting up vector store...")
    vectorstore = setup_vector_store()
    print(f"[OK] Indexed {len(SAMPLE_DOCS)} documents")
    print()
    
    # Create search tool
    print("[INFO] Creating search tool...")
    search_tool = create_search_tool(vectorstore)
    print("[OK] Search tool ready")
    print()
    
    # Test search tool directly
    print("[INFO] Testing search tool directly...")
    test_result = search_tool.invoke({"query": "authentication setup"})
    print(f"[OK] Search result preview: {test_result[:150]}...")
    print()
    
    # Create and test RAG agent
    print("[INFO] Creating RAG agent (agentic strategy)...")
    agent = create_rag_agent(search_tool, strategy="agentic")
    print("[OK] Agent 'rag_assistant' created")
    print()
    
    # Test conversations
    print("=" * 60)
    print("Testing RAG Agent")
    print("=" * 60)
    print()
    
    test_questions = [
        "How do I configure OAuth authentication?",
        "What happens if I exceed the rate limit?",
        "Hello, who are you?",
        "What error codes might I see?",
    ]
    
    config = {"configurable": {"thread_id": "demo_session"}}
    
    for q in test_questions:
        print(f"User: {q}")
        
        result = agent.invoke(
            {"messages": [{"role": "user", "content": q}]},
            config
        )
        
        response = result["messages"][-1].content
        print(f"Agent: {response[:250]}...")
        print()
    
    # Strategy comparison
    print("=" * 60)
    print("RAG Strategy Comparison")
    print("=" * 60)
    
    comparison = compare_rag_strategies(vectorstore)
    
    print("\n--- Summary ---")
    for strategy, data in comparison.items():
        total = len(data["responses"])
        searches = data["total_searches"]
        print(f"{strategy}: {searches}/{total} queries used search")
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
