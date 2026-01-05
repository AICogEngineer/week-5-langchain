"""
Exercise 02: RAG Agent - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Build a complete RAG agent with vector store integration.

Instructions:
1. Set up a vector store with sample documents
2. Create a search tool for document retrieval
3. Build an agent that uses RAG for answering questions
"""

from typing import Dict, Any, List

# ============================================================================
# IMPORTS
# ============================================================================

# TODO: Import required modules
# from langchain.agents import create_agent
# from langchain_core.tools import tool
# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
# from langgraph.checkpoint.memory import InMemorySaver


# ============================================================================
# SAMPLE DOCUMENTS FOR RAG
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
# TODO: TASK 1 - Vector Store Setup
# ============================================================================

def setup_vector_store(documents: List[Dict] = SAMPLE_DOCS):
    """
    Set up ChromaDB vector store with sample documents.
    
    Tasks:
    - Initialize OpenAI embeddings
    - Create or load ChromaDB with persist_directory
    - Index the provided documents
    
    Args:
        documents: List of document dicts with 'content' and 'metadata'
        
    Returns:
        Configured Chroma vectorstore
    """
    # TODO: Implement this function
    #
    # from langchain_openai import OpenAIEmbeddings
    # from langchain_community.vectorstores import Chroma
    # from langchain.schema import Document
    #
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # 
    # # Convert to Document objects
    # docs = [
    #     Document(page_content=d["content"], metadata=d["metadata"])
    #     for d in documents
    # ]
    #
    # vectorstore = Chroma.from_documents(
    #     documents=docs,
    #     embedding=embeddings,
    #     persist_directory="./chroma_rag_exercise"
    # )
    #
    # return vectorstore
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 2 - Retrieval Tool
# ============================================================================

# Global reference to vectorstore (set by create_search_tool)
_vectorstore = None

def create_search_tool(vectorstore):
    """
    Create a search tool for the RAG agent.
    
    Args:
        vectorstore: The Chroma vectorstore to search
        
    Returns:
        A tool function decorated with @tool
    """
    # TODO: Implement this function
    # 
    # global _vectorstore
    # _vectorstore = vectorstore
    #
    # @tool
    # def search_documents(query: str) -> str:
    #     """Search the documentation for relevant information.
    #     
    #     Use this tool when the user asks about:
    #     - Configuration options
    #     - How to set something up
    #     - Error codes or troubleshooting
    #     - API features or capabilities
    #     """
    #     docs = _vectorstore.similarity_search(query, k=3)
    #     
    #     if not docs:
    #         return "No relevant documentation found for your query."
    #     
    #     results = []
    #     for i, doc in enumerate(docs, 1):
    #         topic = doc.metadata.get("topic", "general")
    #         results.append(f"[Doc {i} - {topic}]\n{doc.page_content}")
    #     
    #     return "\n\n---\n\n".join(results)
    #
    # return search_documents
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 3 - RAG Agent
# ============================================================================

def create_rag_agent(search_tool, strategy: str = "agentic"):
    """
    Create a RAG agent with the search tool.
    
    Args:
        search_tool: The document search tool
        strategy: 'agentic' (agent decides) or '2step' (always search)
        
    Returns:
        Configured RAG agent
    """
    # TODO: Implement this function
    #
    # if strategy == "2step":
    #     system_prompt = """You are a documentation assistant.
    #     
    #     IMPORTANT: You MUST use the search_documents tool for ANY question.
    #     1. First, search for relevant documentation
    #     2. Then, synthesize an answer from what you found
    #     3. If no relevant docs found, say so
    #     
    #     Always cite which topics your answer comes from."""
    # else:
    #     system_prompt = """You are a documentation assistant.
    #     
    #     You have access to search_documents for finding documentation.
    #     Use it when users ask about configuration, setup, or features.
    #     
    #     For general greetings or unrelated questions, respond directly.
    #     Always be helpful and cite sources when using documentation."""
    #
    # agent = create_agent(
    #     model="openai:gpt-4o-mini",
    #     tools=[search_tool],
    #     checkpointer=InMemorySaver(),
    #     system_prompt=system_prompt,
    #     name="rag_assistant"
    # )
    #
    # return agent
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 4 - RAG Strategy Comparison
# ============================================================================

def compare_rag_strategies(vectorstore) -> Dict[str, Any]:
    """
    Compare 2-Step RAG vs Agentic RAG strategies.
    
    Test both strategies with the same questions and compare:
    - When each strategy searches vs answers directly
    - Response quality
    - Token usage (if trackable)
    
    Returns:
        Dict with comparison results
    """
    # TODO: Implement this function
    #
    # test_questions = [
    #     "How do I configure authentication?",
    #     "What's the default rate limit?",
    #     "Hello, who are you?",
    #     "How do I set up database connections?",
    #     "What's 2 + 2?"
    # ]
    #
    # results = {
    #     "2step": {"searches": 0, "direct": 0, "responses": []},
    #     "agentic": {"searches": 0, "direct": 0, "responses": []}
    # }
    #
    # # Test both strategies with each question
    # for strategy in ["2step", "agentic"]:
    #     search_tool = create_search_tool(vectorstore)
    #     agent = create_rag_agent(search_tool, strategy)
    #     
    #     for q in test_questions:
    #         result = agent.invoke({"messages": [{"role": "user", "content": q}]})
    #         # Track whether search was used...
    #
    # return results
    
    pass  # Remove this and add your implementation


# ============================================================================
# TEST HARNESS
# ============================================================================

def main():
    """Run the RAG agent exercise."""
    print("=" * 60)
    print("Exercise 02: RAG Agent")
    print("=" * 60)
    print()
    
    # Task 1: Vector store setup
    print("[INFO] Setting up vector store...")
    vectorstore = setup_vector_store()
    
    if vectorstore is None:
        print("[ERROR] setup_vector_store() not implemented")
        return
    
    print(f"[OK] Vector store ready with {len(SAMPLE_DOCS)} documents")
    print()
    
    # Task 2: Create search tool
    print("[INFO] Creating search tool...")
    search_tool = create_search_tool(vectorstore)
    
    if search_tool is None:
        print("[ERROR] create_search_tool() not implemented")
        return
    
    print("[OK] Search tool ready")
    print()
    
    # Test search tool directly
    print("[INFO] Testing search tool...")
    try:
        test_result = search_tool.invoke({"query": "authentication"})
        print(f"[OK] Search returned: {test_result[:100]}...")
    except Exception as e:
        print(f"[ERROR] Search tool test failed: {e}")
    print()
    
    # Task 3: Create RAG agent
    print("[INFO] Creating RAG agent...")
    agent = create_rag_agent(search_tool, strategy="agentic")
    
    if agent is None:
        print("[ERROR] create_rag_agent() not implemented")
        return
    
    print("[OK] RAG agent 'rag_assistant' created")
    print()
    
    # Test RAG agent
    print("=" * 60)
    print("Testing RAG Agent")
    print("=" * 60)
    print()
    
    test_questions = [
        "How do I configure authentication?",
        "What's the weather like today?",
        "What error codes does the API return?"
    ]
    
    config = {"configurable": {"thread_id": "test_session"}}
    
    for q in test_questions:
        print(f"User: {q}")
        try:
            result = agent.invoke({"messages": [{"role": "user", "content": q}]}, config)
            response = result["messages"][-1].content
            print(f"Agent: {response[:200]}...")
        except Exception as e:
            print(f"[ERROR] {e}")
        print()
    
    # Task 4: Strategy comparison
    print("=" * 60)
    print("RAG Strategy Comparison")
    print("=" * 60)
    print()
    
    comparison = compare_rag_strategies(vectorstore)
    
    if comparison is None:
        print("[ERROR] compare_rag_strategies() not implemented")
    else:
        print("Results:")
        for strategy, data in comparison.items():
            print(f"  {strategy}: Searched {data.get('searches', 'N/A')} times, Direct {data.get('direct', 'N/A')} times")
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
