# Sandbox Academy

The isolated tool environment that ELIZA and other ACG tools can call during operations.

## What You'll Learn

- MCP (Model Context Protocol) tool architecture
- Building ACG principle lookup and alignment scoring tools
- REST and stdio interfaces for AI tool integration
- Voice-activated tool calling with Web Speech API
- Tool registry and schema validation patterns

## Prerequisites

- Python 3.10+ for the server-side tools
- Understanding of JSON-RPC / MCP protocol basics
- Browser with Web Speech API for voice features (Chrome recommended)

## Key Concepts

**MCP Tools**: Standardized way for AI models to call external tools. Each tool declares its name, description, and parameter schema. Tools return structured JSON results.

**Alignment Scoring**: Keyword density analysis against ACG principle terminology. Six dimensions: innovation, quality, safety, human, consent, refuse. Scores 0-1 per dimension.

**Voice Interface**: `voice.html` uses the Web Speech API for recognition and SpeechSynthesis for TTS — fully client-side, no cloud APIs.

**Tool Registry**: `registry.py` manages tool schemas and validation. Tools can be served via REST (`server.py`), MCP stdio (`mcp_stdio.py`), or called directly.

## Available Tools

- `acg_lookup_principle` — Look up ACG Manifesto principles 1-6
- `acg_check_alignment` — Score text against all 6 principles
- `acg_generate_scenario` — Generate vetting scenarios per phase
- `acg_hash_response` — Tamper-proof hash of vetting responses
- `konomi_query` — Search konomi standards packages
- `konomi_factory_status` — Factory tag database status

## Architecture

- `tools.py` — Core tool implementations
- `registry.py` — Schema registry and validation
- `server.py` — REST API (port 8066)
- `mcp_stdio.py` — MCP stdio transport
- `voice.html` — Browser voice interface
- `index.html` — Interactive sandbox UI
