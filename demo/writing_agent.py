#!/usr/bin/env python3
"""
Simulated Writing Agent for Box Agentic Mesh Demo.

Demonstrates agent handoff by reading research from agent memory
and producing written content based on that context.

Usage:
    python demo/writing_agent.py

Prerequisites:
    - Set DEMO_FOLDER_ID in .env to a valid Box folder ID
    - Ensure Box API credentials are configured
    - Run demo/research_agent.py first to create memory
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, "src")
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import time
from box_agentic_mesh.memory import read_memory
from box_agentic_mesh.ledger import log_action

# Get Box folder ID from environment
FOLDER_ID = os.getenv("DEMO_FOLDER_ID", "0")


def write_article(data: dict) -> str:
    """Write an article based on research data.

    Args:
        data: Dictionary containing research findings from agent memory.

    Returns:
        Formatted article as a string.
    """
    topic = data.get("topic", "Unknown Topic")
    print(f"Writing article on: {topic}")
    time.sleep(2)  # Simulate processing time

    article = (
        f"Article: {topic}\n\n"
        "Key Points:\n"
        + "\n".join(f"- {point}" for point in data.get("key_points", []))
        + "\n\nSources:\n"
        + "\n".join(f"- {source}" for source in data.get("sources", []))
    )
    return article


if __name__ == "__main__":
    memory = read_memory(FOLDER_ID)

    if memory:
        article = write_article(memory)
        print("\nGenerated Article:\n")
        print(article)

        # Log the action for audit
        log_action(
            FOLDER_ID,
            "article_written",
            model="Claude",
            reasoning="Generated article from research memory",
        )

        print("\nArticle written and logged.")
    else:
        print("No memory found. Ensure research_agent.py was run first.")
