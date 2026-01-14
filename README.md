# Box Agentic Mesh

A middleware layer that provides AI agents with persistent memory, safe file staging, and audit logging capabilities within Box.

## Features

- **Agentic Memory**: Persistent state stored in `.agent_memory.json` files, enabling agents to share context across sessions
- **Shadow Box**: Safe staging area (`[SHADOW]` folders) for autonomous file operations without risking production data
- **Reasoning Ledger**: Audit logging (`.reasoning_ledger.log`) that captures agent actions, prompts, and model identifiers

## Architecture

```
Box Agentic Mesh
├── Memory Layer    → .agent_memory.json
├── Shadow Layer    → [SHADOW]/
└── Ledger Layer    → .reasoning_ledger.log
```

## Quick Start

### Installation

```bash
# Clone and enter directory
cd box-proj

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file with Box credentials (see `docs/setup.md`)
2. Set `DEMO_FOLDER_ID` to a valid Box folder ID

### Running the API

```bash
PYTHONPATH=src python -m uvicorn box_agentic_mesh.api:app --port 8000
```

API documentation: http://localhost:8000/docs

### Running Demos

```bash
# Research Agent (writes to memory)
python demo/research_agent.py

# Writing Agent (reads from memory)
python demo/writing_agent.py
```

## Project Structure

```
src/box_agentic_mesh/
├── config.py          # Configuration and credentials
├── memory.py          # Agentic Memory layer
├── shadow.py          # Shadow Box layer
├── ledger.py          # Reasoning Ledger layer
├── api.py             # FastAPI REST endpoints
└── mcp_server.py      # MCP server integration

demo/
├── research_agent.py  # Simulated Research Agent demo
└── writing_agent.py   # Simulated Writing Agent demo

tests/
└── test_memory.py     # Unit tests

docs/
└── setup.md           # Setup guide
```

## Testing

```bash
PYTHONPATH=src python -m pytest tests/
```

## Requirements

- Python 3.11+
- Box Developer Account
- Box SDK (`boxsdk`)

See `requirements.txt` for full dependency list.
