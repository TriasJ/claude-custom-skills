# notebooklm-studio

A Claude Code skill for creating NotebookLM studio artifacts via MCP tools. Full lifecycle from notebook creation through source ingestion, research, artifact generation, and download.

## Features

- **9 Artifact Types**: Audio overviews (podcasts), video overviews, slide decks, infographics, reports, quizzes, flashcards, mind maps, data tables
- **Full Lifecycle**: Create notebooks, add sources (URLs, files, text, Google Drive), run web/Drive research, generate artifacts, download
- **Preset System**: Quick/Standard/Detailed tiers + type-specific named presets (podcast, debate, whiteboard, etc.)
- **Batch Mode**: Generate multiple artifacts from the same notebook in one go
- **4 Safety Hooks**: Confirm guard, auth health check, download path enforcer, chain enforcer
- **Guided Workflow**: 6-stage interactive flow with user confirmations at each step
- **Multi-Language**: English default with BCP-47 language override support
- **Research Integration**: Fast (~30s) and deep (~5min) web/Drive search to discover sources

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- [NotebookLM MCP CLI](https://github.com/jacob-bd/notebooklm-mcp-cli) installed and configured
- Authenticated with `nlm login`

## Installation

### 1. Copy skill files

```bash
# Clone or copy this repo into your Claude Code skills directory
cp -r . ~/.claude/skills/notebooklm-studio/
```

### 2. Copy slash command

```bash
cp commands/notebooklm-studio.md ~/.claude/commands/
```

### 3. Install hooks

Copy hook scripts to your hooks directory:

```bash
mkdir -p ~/.claude/hooks/notebooklm-studio/
cp hooks/*.js ~/.claude/hooks/notebooklm-studio/
```

Then merge the hooks config from `hooks-config-example.json` into your `~/.claude/hooks.json`. Update the `<PATH_TO_HOOKS>` placeholders with your actual hook script paths.

### 4. Create download directory

```bash
mkdir -p ~/Downloads/notebooklm/
```

## Quick Start

### Via slash command
```
/notebooklm-studio create a podcast from https://example.com/paper1 and https://example.com/paper2
```

### Via natural language
```
"Create a podcast from these papers"
"Make slides about quantum computing"
"Generate a debate podcast and infographic for my CRISPR notebook"
```

## Workflow

The skill follows a **6-stage guided flow**:

1. **Notebook Setup** - List existing notebooks or create a new one
2. **Source Management** - Add URLs, files, text, or Google Drive documents
3. **Research** (optional) - Search web/Drive for additional sources
4. **Artifact Configuration** - Choose type, preset, and options
5. **Generation + Polling** - Create artifact and wait for completion
6. **Download** - Save to `~/Downloads/notebooklm/{notebook-name}/{type}-{date}.{ext}`

## Presets

### Unified Tiers

| Tier | Audio | Video | Slides | Infographic |
|------|-------|-------|--------|-------------|
| **Quick** | brief, short | brief, auto | presenter, short | concise, square |
| **Standard** | deep_dive, default | explainer, auto | detailed, default | standard, landscape |
| **Detailed** | debate, long | explainer, whiteboard | detailed, default | detailed, landscape |

### Named Presets

- **Audio**: `podcast`, `briefing`, `critique`, `debate`
- **Video**: `explainer`, `whiteboard`, `anime`, `watercolor`
- **Slides**: `presentation`, `quick-deck`
- **Infographic**: `landscape`, `portrait`, `poster`, `summary`
- **Report**: `briefing`, `study-guide`, `blog`, `custom`

See `references/presets.md` for complete definitions.

## Hooks

| Hook | Type | Purpose |
|------|------|---------|
| `confirm-guard.js` | PreToolUse | Blocks studio_create and delete operations without confirm=True |
| `auth-health-check.js` | PreToolUse | Injects auth recovery guidance on all NotebookLM MCP calls |
| `download-path-enforcer.js` | PreToolUse | Warns when downloads go outside ~/Downloads/notebooklm/ |
| `chain-enforcer.js` | PostToolUse | Enforces create -> poll -> download chain after studio_create |

## File Structure

```
notebooklm-studio/
├── SKILL.md                      # Main skill file
├── README.md                     # This file
├── references/
│   ├── presets.md                # Complete preset definitions
│   ├── artifact-options.md       # Full parameter reference
│   └── troubleshooting.md       # Error recovery guide
├── hooks/
│   ├── confirm-guard.js          # PreToolUse: confirm=True enforcement
│   ├── auth-health-check.js      # PreToolUse: auth status reminder
│   ├── download-path-enforcer.js # PreToolUse: download path validation
│   └── chain-enforcer.js         # PostToolUse: create->poll->download chain
├── commands/
│   └── notebooklm-studio.md     # Slash command wrapper
├── hooks-config-example.json     # Example hooks.json entries
└── .gitignore
```

## MCP Tools Used

This skill orchestrates the following `mcp__notebooklm-mcp__*` tools:

- `notebook_list`, `notebook_create`, `notebook_get`, `notebook_describe`
- `source_add`, `source_describe`, `source_get_content`
- `research_start`, `research_status`, `research_import`
- `studio_create`, `studio_status`
- `download_artifact`
- `refresh_auth`

## License

MIT
