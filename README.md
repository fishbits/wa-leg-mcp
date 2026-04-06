# Washington State Legislature MCP Server

An [MCP](https://modelcontextprotocol.io/) server that gives AI assistants real-time access to Washington State Legislature data — bills, votes, committees, session laws, and more — through the official [WSLWS](https://wslwebservices.leg.wa.gov/) APIs.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-444%20passing-brightgreen.svg)](#testing)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Why This Exists

Washington State publishes legislative data through SOAP web services, but those APIs aren't easy to use conversationally. This server bridges that gap — it wraps the full WSLWS API surface as MCP tools so AI assistants like Claude can answer questions like:

- *"What bills about housing passed the House this session?"*
- *"How did my district's representatives vote on HB 1234?"*
- *"What bills has the governor vetoed this biennium?"*
- *"Show me the RCW sections affected by SB 5678."*

The goal is to make civic engagement more accessible by letting people ask questions in plain language and get real legislative data back.

## What It Can Do

**35 tools** covering the full WSLWS API, organized into these categories:

| Category | Tools | Examples |
|----------|-------|---------|
| Bill Information | 8 | Search bills, get status, read bill text in XML/HTML/PDF |
| Committees | 9 | Active committees, membership, meeting schedules and agendas |
| Committee Actions | 6 | Referrals, do-pass recommendations, executive actions |
| Roll Call Votes | 1 | Legislator-level voting records (yea/nay/absent/excused) |
| Amendments | 2 | Amendments by biennium or year |
| Session Laws & RCW | 7 | Chapter lookups, RCW citations affected, hearing schedules |
| Governor Actions | 3 | Bills signed, vetoed, or partially vetoed |
| Sponsors & Legislators | 5 | Legislator lookup, sponsor lists by chamber |
| Bill Passage | 5 | Passed House/Senate/both, prefiled bills, status changes |
| Documents & Metadata | 7 | Document classes, legislation types, request number lookup |

Plus **4 MCP resource URIs** for direct bill document access (`bill://xml/...`, `bill://htm/...`, `bill://pdf/...`).

See [docs/API.md](docs/API.md) for full tool documentation with parameters and return types.

## Quick Start

### Install

```bash
git clone https://github.com/fishbits/wa-leg-mcp.git
cd wa-leg-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Run

```bash
# Start the server (stdio transport)
python src/wa_leg_mcp/server.py

# Or test interactively with MCP Inspector
pip install -e ".[dev]"
mcp dev src/wa_leg_mcp/server.py
```

### Connect to Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "wa-leg": {
      "command": "python",
      "args": ["/path/to/wa-leg-mcp/src/wa_leg_mcp/server.py"]
    }
  }
}
```

### Configuration (Optional)

Environment variables or `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `WSL_API_TIMEOUT` | API request timeout (seconds) | 30 |
| `WSL_CACHE_TTL` | Cache TTL (seconds) | 300 |
| `LOG_LEVEL` | Logging level | INFO |

## Project Structure

```
src/wa_leg_mcp/
├── server.py                  # MCP server entry point
├── clients/                   # WSLWS SOAP + Search API clients
├── tools/                     # 35 MCP tools (14 modules)
├── resources/                 # Bill document resource handlers
└── utils/                     # Formatting and document helpers

tests/
├── test_*.py                  # 330+ unit tests
└── property/                  # 110+ property-based tests (Hypothesis)
```

## Testing

```bash
pip install -e ".[dev]"
make test
```

444 tests (330+ unit, 110+ property-based) covering bill tools, roll calls, amendments, committees, session laws, governor actions, sponsors, passage tracking, documents, and metadata.

## Acknowledgments

This project is a fork of [wa-leg-mcp](https://github.com/awalcutt/wa-leg-mcp) by [Alex Walcutt](https://github.com/awalcutt), who built the original MCP server with the core bill information tools, search client, and document resources. That foundation made this expanded coverage possible.

### What this fork adds

- 28 additional MCP tools (roll calls, amendments, session laws, governor actions, committee actions, sponsors, passage tracking, documents, metadata)
- 444 tests including property-based testing with Hypothesis
- Full WSLWS API coverage across all major legislative data endpoints

## License

[MIT](LICENSE) — Original work © 2025 Alex Walcutt. Fork enhancements © 2026 Eric Fisher.
