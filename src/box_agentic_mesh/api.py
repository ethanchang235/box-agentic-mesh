"""
FastAPI REST API for Box Agentic Mesh.

Provides REST endpoints for all three layers:
    - /memory/*: Agentic Memory operations
    - /shadow/*: Shadow Box staging operations
    - /ledger/*: Reasoning Ledger logging operations

Run with: python -m src.box_agentic_mesh.api

Access documentation at: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .memory import read_memory, write_memory
from .shadow import create_shadow, commit_shadow
from .ledger import log_action

app = FastAPI(title="Box Agentic Mesh API")


class MemoryData(BaseModel):
    """Request body for writing memory data."""

    data: dict


class ShadowCreateRequest(BaseModel):
    """Request body for creating shadow staging area."""

    file_ids: list[str] | None = None


class LedgerLogRequest(BaseModel):
    """Request body for logging an agent action."""

    folder_id: str
    action: str
    prompt: str | None = None
    model: str | None = None
    reasoning: str | None = None


@app.get("/memory/{folder_id}")
async def get_memory(folder_id: str):
    """Get agent memory from a Box folder.

    Returns the contents of `.agent_memory.json` as JSON.
    """
    try:
        data = read_memory(folder_id)
        return {"memory": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memory/{folder_id}")
async def post_memory(folder_id: str, memory_data: MemoryData):
    """Write agent memory to a Box folder.

    Creates or updates `.agent_memory.json` in the specified folder.
    """
    try:
        write_memory(folder_id, memory_data.data)
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/shadow/create/{folder_id}")
async def post_create_shadow(folder_id: str, request: ShadowCreateRequest):
    """Create a Shadow Box staging subfolder.

    Creates `[SHADOW]` subfolder and copies specified files (or all files).
    """
    try:
        shadow_id = create_shadow(folder_id, request.file_ids)
        return {"shadow_folder_id": shadow_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/shadow/commit/{folder_id}")
async def post_commit_shadow(folder_id: str):
    """Commit changes from Shadow Box to production.

    Copies staged files back to the main folder and deletes the shadow.
    """
    try:
        commit_shadow(folder_id, approval=True)
        return {"status": "committed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ledger/log")
async def post_log(request: LedgerLogRequest):
    """Log an agent action to the reasoning ledger.

    Appends a new entry to `.reasoning_ledger.log` with action details.
    """
    try:
        log_action(
            request.folder_id,
            request.action,
            request.prompt,
            request.model,
            request.reasoning,
        )
        return {"status": "logged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
