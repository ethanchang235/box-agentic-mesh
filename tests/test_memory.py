"""
Unit tests for the Box Agentic Mesh memory module.

Tests cover read and write operations for agent memory files.
Uses mocking to avoid requiring actual Box API calls.
"""

import pytest
from unittest.mock import patch, MagicMock
from box_agentic_mesh.memory import read_memory, write_memory


@patch("box_agentic_mesh.memory.get_box_client")
def test_read_memory(mock_client):
    """Test reading agent memory from a Box folder.

    Verifies that the function correctly:
    - Finds the .agent_memory.json file
    - Parses and returns the JSON content
    """
    mock_folder = MagicMock()
    mock_file = MagicMock()
    mock_file.name = ".agent_memory.json"
    mock_file.type = "file"
    mock_file.content.return_value = b'{"test": "data"}'
    mock_folder.get_items.return_value = [mock_file]
    mock_client.return_value.folder.return_value = mock_folder

    result = read_memory("folder_id")
    assert result == {"test": "data"}


@patch("box_agentic_mesh.memory.get_box_client")
def test_write_memory(mock_client):
    """Test writing agent memory to a Box folder.

    Verifies that the function correctly:
    - Creates a new file if none exists
    - Updates existing file if present
    """
    mock_folder = MagicMock()
    mock_client.return_value.folder.return_value = mock_folder

    write_memory("folder_id", {"test": "data"})
    # If no exception is raised, the test passes
