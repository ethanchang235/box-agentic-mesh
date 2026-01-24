"""
Agentic Memory Layer.

Provides persistent state management for AI agents by storing memory files
directly in Box folders. This enables agents to share context and hand off
tasks seamlessly across different platforms and sessions.

Memory Format:
    Memory data is stored as JSON in `.agent_memory.json` files within Box folders.
    Example:
        {
            "task_id": "research-001",
            "topic": "Box Agentic Mesh Benefits",
            "key_points": [...],
            "hand_off_to": "Writing Agent",
            "timestamp": 1698765432.123
        }

Usage:
    # Read memory from a folder
    memory = read_memory("folder_id")

    # Write memory to a folder
    write_memory("folder_id", {"task": "analysis", "status": "in_progress"})
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
import json
import io
from boxsdk import Client, OAuth2
from .config import BOX_CLIENT_ID, BOX_CLIENT_SECRET, BOX_ACCESS_TOKEN


def get_box_client() -> Client:
    """Create and return an authenticated Box client.

    Returns:
        Authenticated Box SDK Client instance.

    Raises:
        ValueError: If BOX_ACCESS_TOKEN is not configured.
    """
    if BOX_ACCESS_TOKEN:
        oauth = OAuth2(
            client_id=BOX_CLIENT_ID,
            client_secret=BOX_CLIENT_SECRET,
            access_token=BOX_ACCESS_TOKEN,
        )
    else:
        raise ValueError("BOX_ACCESS_TOKEN required. Configure in .env file.")
    return Client(oauth)


def read_memory(folder_id: str) -> dict:
    """Read agent memory from a Box folder.

    Retrieves the `.agent_memory.json` file from the specified folder and
    returns its contents as a dictionary. Returns an empty dict if no
    memory file exists.

    Args:
        folder_id: The Box folder ID to read memory from.

    Returns:
        Dictionary containing the memory data, or empty dict if no memory exists.
    """
    client = get_box_client()
    folder = client.folder(folder_id)
    try:
        memory_file = None
        for item in folder.get_items():
            if item.name == ".agent_memory.json" and item.type == "file":
                memory_file = item
                break
        if not memory_file:
            return {}
        content = memory_file.content()
        return json.loads(content.decode("utf-8"))
    except Exception as e:
        print(f"Error reading memory: {e}")
        return {}


def write_memory(folder_id: str, data: dict) -> None:
    """Write agent memory to a Box folder.

    Creates or updates the `.agent_memory.json` file in the specified folder.
    If the file exists, it updates the contents; otherwise, it creates a new file.

    Args:
        folder_id: The Box folder ID to write memory to.
        data: Dictionary containing the memory data to store.
    """
    client = get_box_client()
    folder = client.folder(folder_id)
    memory_json = json.dumps(data, indent=2)
    try:
        memory_file = None
        for item in folder.get_items():
            if item.name == ".agent_memory.json" and item.type == "file":
                memory_file = item
                break
        if memory_file:
            memory_file.update_contents_with_stream(
                io.BytesIO(memory_json.encode("utf-8"))
            )
        else:
            folder.upload_stream(
                io.BytesIO(memory_json.encode("utf-8")), ".agent_memory.json"
            )
    except Exception as e:
        print(f"Error writing memory: {e}")
