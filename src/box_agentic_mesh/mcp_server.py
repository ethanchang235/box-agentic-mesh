"""
Model Context Protocol (MCP) Server for Box Agentic Mesh.

Exposes the three core layers as MCP tools for AI agents.
Compatible with MCP-compatible clients like Claude, Cursor, etc.

Run with: python -m src.box_agentic_mesh.mcp_server

Available Tools:
    - hand_off_task: Write task data to agent memory
    - read_agent_memory: Read current agent memory
    - create_shadow_staging: Create Shadow Box staging area
    - commit_shadow_changes: Commit staged changes
    - log_agent_action: Log an agent action for audit
"""

from mcp.server.fastmcp import FastMCP
from .memory import read_memory, write_memory
from .shadow import create_shadow, commit_shadow
from .ledger import log_action

app = FastMCP("Box Agentic Mesh")


@app.tool()
async def hand_off_task(folder_id: str, task_data: dict) -> str:
    """Hand off a task by writing task data to agent memory.

    This enables seamless task transfer between agents by storing
    the current task state in Box for the next agent to retrieve.

    Args:
        folder_id: Box folder ID to store memory in.
        task_data: Dictionary containing task information.

    Returns:
        Confirmation message.
    """
    write_memory(folder_id, task_data)
    log_action(folder_id, "hand_off", reasoning="Agent handoff via MCP")
    return "Task handed off successfully."


@app.tool()
async def read_agent_memory(folder_id: str) -> dict:
    """Read the current agent memory from a Box folder.

    Retrieves the `.agent_memory.json` file contents, providing
    context from previous agent sessions.

    Args:
        folder_id: Box folder ID to read memory from.

    Returns:
        Dictionary containing the memory data.
    """
    return read_memory(folder_id)


@app.tool()
async def create_shadow_staging(
    folder_id: str, file_ids: list[str] | None = None
) -> str:
    """Create a Shadow Box staging area for safe file operations.

    Creates a `[SHADOW]` subfolder and copies files for safe editing.

    Args:
        folder_id: Box folder ID to create staging in.
        file_ids: Optional list of specific file IDs to stage.

    Returns:
        Confirmation message with shadow folder ID.
    """
    shadow_id = create_shadow(folder_id, file_ids)
    log_action(folder_id, "create_shadow", reasoning="Shadow staging created via MCP")
    return f"Shadow created with ID: {shadow_id}"


@app.tool()
async def commit_shadow_changes(folder_id: str) -> str:
    """Commit staged changes from Shadow Box to production.

    Copies files from shadow to main folder and deletes the staging area.

    Args:
        folder_id: Box folder ID containing the shadow staging.

    Returns:
        Confirmation message.
    """
    commit_shadow(folder_id, approval=True)
    log_action(folder_id, "commit_shadow", reasoning="Shadow changes committed via MCP")
    return "Changes committed to production."


@app.tool()
async def log_agent_action(
    folder_id: str,
    action: str,
    prompt: str | None = None,
    model: str | None = None,
    reasoning: str | None = None,
) -> str:
    """Log an agent action to the reasoning ledger for audit.

    Records the action with optional LLM metadata for compliance.

    Args:
        folder_id: Box folder ID to log to.
        action: Type of action performed.
        prompt: LLM prompt used (optional).
        model: LLM model used (optional).
        reasoning: LLM reasoning (optional).

    Returns:
        Confirmation message.
    """
    log_action(folder_id, action, prompt, model, reasoning)
    return "Action logged."
