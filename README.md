# Box Agentic Mesh

A middleware layer that adds three essential features for AI agents working with Box: shared memory for agent hand-offs, audit logs for compliance, and safe staging for file experiments.

## The Problem

AI agents (Claude Code, Cursor, etc.) are siloed. When you switch from one agent to another:
- **Context is lost** - The new agent doesn't know what the previous one was doing
- **No audit trail** - You can't explain what the AI did or why
- **Risky file changes** - Agents can accidentally break production files

## The Solution

Box Agentic Mesh adds three layers to any Box folder:

```
┌─────────────────────────────────────────────────────────┐
│                    Box Folder                           │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │ Agentic Memory  │  │     Reasoning Ledger        │  │
│  │  (.agent_memory │  │  (.reasoning_ledger.log)    │  │
│  │      .json)     │  │                             │  │
│  └─────────────────┘  └─────────────────────────────┘  │
│                        ┌───────────────────────────┐    │
│                        │      [SHADOW]/            │    │
│                        │   (Safe Staging Area)     │    │
│                        └───────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 1. Agentic Memory
Agents share context by reading/writing to `.agent_memory.json`. Research Agent writes findings → Writing Agent reads and continues.

### 2. Reasoning Ledger
Every action is logged to `.reasoning_ledger.log` with: timestamp, action, prompt, model, and reasoning. Essential for compliance.

### 3. Shadow Box
Agents experiment in `[SHADOW]` subfolder. Changes only commit to production after human approval. Safe experimentation.

## Quick Start

### 1. Install

```bash
git clone https://github.com/ethanchang235/box-agentic-mesh.git
cd box-agentic-mesh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

Create `.env` file with Box credentials:
```
BOX_ACCESS_TOKEN=your_box_token
DEMO_FOLDER_ID=your_folder_id
```

### 3. Run

```bash
# Start API server
PYTHONPATH=src python -m uvicorn box_agentic_mesh.api:app --port 8000

# API docs: http://localhost:8000/docs
```

### 4. Demo

```bash
# Agent 1: Research (writes to memory)
PYTHONPATH=src python demo/research_agent.py

# Agent 2: Writing (reads from memory)
PYTHONPATH=src python demo/writing_agent.py
```

## Project Structure

```
box-agentic-mesh/
├── src/box_agentic_mesh/
│   ├── config.py          # Box credentials
│   ├── memory.py          # Agentic Memory layer
│   ├── shadow.py          # Shadow Box layer
│   ├── ledger.py          # Reasoning Ledger layer
│   ├── api.py             # REST API endpoints
│   └── mcp_server.py      # MCP tools for Claude/Cursor
├── demo/
│   ├── research_agent.py  # Demo: Research → Writing handoff
│   └── writing_agent.py   # Demo: Continues from research
├── tests/
│   └── test_memory.py     # Unit tests
└── docs/
    └── setup.md           # Setup guide
```

## Requirements

- Python 3.11+
- Box Developer Account
- See `requirements.txt` for full dependencies

## Why This Matters

1. **Shared memory** - Agents coordinate across sessions/platforms
2. **Audit trails** - Compliance for regulated industries
3. **Safe staging** - Enterprises trust AI with file access

## Learn More

- Email: ethanchang235@gmail.com
