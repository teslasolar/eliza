# Ops — CLI / REST API / MCP

Unified operations layer for KONOMI — command-line, HTTP API, and MCP tool provider.

## Key Classes

- **CLI** — Command-line interface for directory operations
- **APIServer** — REST API on port 8077
- **MCPProvider** — Model Context Protocol tool provider for AI workflows
- **DirectoryOps** — Core operations: list, describe, validate, compile

## Access Methods

- **CLI**: `python -m konomi list`, `python -m konomi validate`, `python -m konomi compile`
- **REST**: `GET /api/packages`, `POST /api/validate`, `POST /api/compile`
- **MCP**: stdio transport for AI assistants — same operations, tool-call interface
