# Claude Custom Skills

A collection of custom Claude Code skills for scientific research, media handling, presentations, and content creation.

## Skills Included

### Priority Skills
| Skill | Description |
|---|---|
| **parse-pdf-mineru** | Extract text, images, tables, and formulas from PDFs using MinerU with layout preservation |
| **notebooklm** | Query Google NotebookLM notebooks from Claude Code for source-grounded answers |
| **notebooklm-studio** | Create NotebookLM studio artifacts (audio, video, slides, infographics, reports) |
| **fetch-media** | Search and download open-access images from Wikimedia Commons, NASA, Unsplash, Pixabay, NIH BioArt |
| **image-generation** | Generate and edit images using Google Gemini/Imagen APIs |

### Presentation & Content Skills
| Skill | Description |
|---|---|
| **biomedical-marp-presentations** | Scientific presentations with MARP + PubMed citations |
| **create-powerpoint-presentations** | PowerPoint via PptxGenJS (8 templates) |
| **create-revealjs-presentations** | reveal.js HTML presentations (8 templates, D3/Three.js support) |
| **create-remotion-videos** | React-based programmatic videos (social media, educational, scientific) |
| **create-manim-animations** | Animated math videos using Manim |

### Utility & Authoring Skills
| Skill | Description |
|---|---|
| **convert-knowledge-to-xml** | Convert .md/.txt knowledge bases to structured XML |
| **extract-pdf-images** | Extract images from PDFs with contextual metadata (captions, bounding boxes) |
| **create-meta-prompts** | Optimized prompts for Claude-to-Claude pipelines |

### Claude Code Development Skills
| Skill | Description |
|---|---|
| **create-agent-skills** | Guide for authoring Claude Code Skills |
| **create-hooks** | Guide for creating Claude Code hooks |
| **create-slash-commands** | Guide for creating custom slash commands |
| **create-subagents** | Guide for building and using subagents |

## Installation

### Quick Install (WSL/Ubuntu or any Linux)

```bash
git clone https://github.com/TriasJ/claude-custom-skills.git
cd claude-custom-skills
./install.sh
```

### Manual Install

Copy the skill folders you want into your Claude Code skills directory:

```bash
# The skills directory location
SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR"

# Copy all skills
cp -r */ "$SKILLS_DIR/" 2>/dev/null

# Or copy specific skills
cp -r parse-pdf-mineru notebooklm notebooklm-studio fetch-media image-generation "$SKILLS_DIR/"
```

### API Keys Setup

Some skills require API keys. Copy the `.env.example` files and fill in your keys:

```bash
# For fetch-media (Unsplash + Pixabay)
cp "$SKILLS_DIR/fetch-media/.env.example" "$SKILLS_DIR/fetch-media/.env"
# Edit with your keys

# For image-generation (Gemini)
cp "$SKILLS_DIR/image-generation/.env.example" "$SKILLS_DIR/image-generation/.env"
# Edit with your key
```

### NotebookLM Setup

The `notebooklm` and `notebooklm-studio` skills require the NotebookLM MCP server:

```bash
npm install -g notebooklm-mcp
nlm login
```

### MinerU Setup (for parse-pdf-mineru)

```bash
pip install magic-pdf[full]
mineru-models-download
```

## Cross-Platform Notes

- Skills are plain text (Markdown + scripts) and work on Windows, macOS, and Linux
- The `fetch-media` skill includes PowerShell scripts (Windows) -- on Linux, use the Python/Node alternatives
