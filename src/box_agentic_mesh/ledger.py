"""
Reasoning Ledger Layer.

Provides audit logging for agent actions, capturing not just what was done
but the LLM reasoning, prompts, and model identifiers used. This is essential
for compliance in regulated industries requiring "Proof of Intent".

Log Format:
    Each action is logged as a JSON object on a single line.
    Example:
        {
            "timestamp": "2026-01-14T10:30:00.123456",
            "action": "research_completed",
            "prompt": "Analyze Box Agentic Mesh benefits...",
            "model": "GPT-4",
            "reasoning": "Identified 3 key benefits..."
        }

Usage:
    log_action(
        folder_id="folder_id",
        action="analysis_completed",
        prompt="Original prompt used",
        model="GPT-4",
        reasoning="Decision rationale"
    )
"""

import json
import io
from datetime import datetime
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


def log_action(
    folder_id: str,
    action: str,
    prompt: str | None = None,
    model: str | None = None,
    reasoning: str | None = None,
) -> None:
    """Log an agent action to the reasoning ledger.

    Appends a new entry to the `.reasoning_ledger.log` file in the specified
    folder. The log entry includes timestamp, action type, and optional
    metadata about the LLM interaction.

    Args:
        folder_id: The Box folder ID to log to.
        action: Type of action performed (e.g., "research_completed").
        prompt: The prompt sent to the LLM (optional).
        model: The LLM model used (e.g., "GPT-4", "Claude").
        reasoning: The reasoning or decision made by the LLM (optional).
    """
    client = get_box_client()
    folder = client.folder(folder_id)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "prompt": prompt,
        "model": model,
        "reasoning": reasoning,
    }
    log_line = json.dumps(log_entry) + "\n"

    log_file = None
    for item in folder.get_items():
        if item.name == ".reasoning_ledger.log" and item.type == "file":
            log_file = item
            break
    if log_file:
        current_content = log_file.content().decode("utf-8")
        new_content = current_content + log_line
        log_file.delete()
        folder.upload_stream(
            io.BytesIO(new_content.encode("utf-8")), ".reasoning_ledger.log"
        )
    else:
        folder.upload_stream(
            io.BytesIO(log_line.encode("utf-8")), ".reasoning_ledger.log"
        )
