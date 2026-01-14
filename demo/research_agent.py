#!/usr/bin/env python3
"""
Simulated Research Agent for Box Agentic Mesh Demo.

Demonstrates agent handoff by performing research and storing results
in agent memory for the Writing Agent to retrieve.

Usage:
    python demo/research_agent.py

Prerequisites:
    - Set DEMO_FOLDER_ID in .env to a valid Box folder ID
    - Ensure Box API credentials are configured
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, "src")
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import time
from box_agentic_mesh.memory import write_memory
from box_agentic_mesh.ledger import log_action

# Get Box folder ID from environment
FOLDER_ID = os.getenv("DEMO_FOLDER_ID", "0")


def research_topic(topic: str) -> dict:
    """Perform research on a given topic.

    Args:
        topic: The topic to research.

    Returns:
        Dictionary containing research findings.
    """
    print(f"Researching topic: {topic}")
    time.sleep(2)  # Simulate processing time

    research_data = {
        "topic": topic,
        "key_points": [
            "Persistent memory enables agent handoffs",
            "Shadow staging provides safe file operations",
            "Reasoning ledger ensures compliance",
        ],
        "sources": ["Box API Documentation", "MCP Protocol Specification"],
        "hand_off_to": "Writing Agent",
        "timestamp": time.time(),
    }
    return research_data


if __name__ == "__main__":
    topic = "Box Agentic Mesh Benefits"
    data = research_topic(topic)

    # Store research in Box agent memory
    write_memory(FOLDER_ID, data)

    # Log the action for audit
    log_action(
        FOLDER_ID,
        "research_completed",
        model="GPT-4",
        reasoning="Completed research on Box Agentic Mesh benefits",
    )

    print("Research completed and handed off to Writing Agent.")
