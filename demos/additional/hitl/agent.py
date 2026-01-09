"""
HITL Agent for LangSmith Studio
================================
A single comprehensive agent export for use with LangSmith Studio.
This agent demonstrates Human-in-the-Loop patterns with multiple tools.

Usage with LangSmith Studio:
  1. Run: langgraph dev
  2. Open: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

Reference: https://docs.langchain.com/oss/python/langchain/human-in-the-loop
"""

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()


# === Tools with varying risk levels ===

@tool
def delete_file(filepath: str) -> str:
    """Delete a file from the filesystem. DANGEROUS - requires approval."""
    # Simulated for demo - doesn't actually delete
    return f"File '{filepath}' has been deleted."


@tool
def execute_sql(query: str) -> str:
    """Execute a SQL query against the database. DANGEROUS - requires approval."""
    # Simulated for demo
    return f"Query executed: {query}\nRows affected: 42"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient. Requires approval but allows editing."""
    return f"Email sent to {to} with subject: '{subject}'"


@tool
def search_web(query: str) -> str:
    """Search the web for information. Safe operation - no approval needed."""
    return f"Search results for '{query}':\n- Result 1: Overview of {query}\n- Result 2: Deep dive into {query}"


@tool
def get_current_time() -> str:
    """Get the current time. Safe operation - no approval needed."""
    from datetime import datetime
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


# === The Agent (exported for LangSmith Studio) ===

agent = create_agent(
    name="hitl_demo_agent",
    model="gpt-4o-mini",
    tools=[delete_file, execute_sql, send_email, search_web, get_current_time],
    system_prompt="""You are a helpful assistant with access to various tools.

Some tools are dangerous and require human approval:
- delete_file: Deletes files (DANGEROUS)
- execute_sql: Runs database queries (DANGEROUS)
- send_email: Sends emails (requires review, can be edited)

Some tools are safe and don't need approval:
- search_web: Safe web search
- get_current_time: Safe time lookup

Always explain what you're about to do before using dangerous tools.""",
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # Dangerous operations - all decisions allowed
                "delete_file": True,
                "execute_sql": True,
                # Email - allow editing before send
                "send_email": True,
                # Safe operations - no approval needed
                "search_web": False,
                "get_current_time": False,
            },
            description_prefix="Action requires human approval",
        ),
    ],
)
