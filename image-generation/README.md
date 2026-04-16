# Gemini Image Generation Skill

A portable Claude Code skill for generating and editing images using Google's Gemini image generation API.

## Features

- Generate images from text prompts
- Edit existing images with natural language instructions
- Compose multiple images (up to 14) into new scenes
- MCP server integration for Claude Code and Claude Desktop
- Multiple aspect ratios supported (1:1, 16:9, 9:16, etc.)
- Cross-platform support (Windows, macOS, Linux)

## Quick Setup

### 1. Prerequisites

- Python 3.8 or higher
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 2. Installation

#### Windows (PowerShell)
```powershell
# Navigate to the skill directory
cd $env:USERPROFILE\.claude\skills\image-generation

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env

# Edit .env and add your API key
notepad .env
```

#### Windows (CMD)
```cmd
cd %USERPROFILE%\.claude\skills\image-generation
pip install -r requirements.txt
copy .env.example .env
notepad .env
```

#### Linux/macOS
```bash
# Navigate to the skill directory
cd ~/.claude/skills/image-generation

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env and add your API key
nano .env  # or vim, code, etc.
```

### 3. Add to Claude Code

#### Windows (PowerShell)
```powershell
claude mcp add gemini-imagegen -- python "$env:USERPROFILE\.claude\skills\image-generation\gemini_imagegen_mcp.py"
```

#### Windows (CMD)
```cmd
claude mcp add gemini-imagegen -- python "%USERPROFILE%\.claude\skills\image-generation\gemini_imagegen_mcp.py"
```

#### Linux/macOS
```bash
claude mcp add gemini-imagegen -- python ~/.claude/skills/image-generation/gemini_imagegen_mcp.py
```

### 4. Verify Installation

```bash
claude mcp list
```

You should see `gemini-imagegen` in the list.

## Usage

Once installed, you can use the skill through Claude Code:

```
Generate an image of a cat wearing a wizard hat
```

```
Edit this image to add a sunset in the background: /path/to/image.png
```

```
Create a comparison showing these three products side by side
```

## Skill Structure

```
image-generation/
├── SKILL.md                    # Skill definition and documentation
├── README.md                   # This file
├── gemini_imagegen_mcp.py      # MCP server implementation
├── requirements.txt            # Python dependencies
├── .env.example                # Template for API key configuration
├── .env                        # Your API key (not committed to git)
├── .gitignore                  # Git ignore rules
└── venv/                       # Virtual environment (optional, not committed)
```

## API Key Configuration

The skill supports two methods for API key configuration:

### Method 1: .env File (Recommended)

1. Copy `.env.example` to `.env`
2. Edit `.env` and replace `your_api_key_here` with your actual Gemini API key
3. Save the file

The `.env` file is automatically loaded when the MCP server starts.

### Method 2: Environment Variable

Set the `GEMINI_API_KEY` environment variable directly:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your_key_here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your_key_here
```

**Linux/macOS (temporary):**
```bash
export GEMINI_API_KEY=your_key_here
```

**Linux/macOS (persistent):** Add to `~/.bashrc`, `~/.zshrc`, or `~/.profile`:
```bash
export GEMINI_API_KEY=your_key_here
```

## Supported Models

- **gemini-3-pro-image-preview** (default): Best quality with contextual refinement, excellent text rendering
- **gemini-2.5-flash-image**: Fast multimodal generation, good second option
- **imagen-4.0-ultra-generate-001**: Highest quality photorealistic images
- **imagen-4.0-fast-generate-001**: Fastest generation for rapid prototyping

## Supported Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

## Troubleshooting

### API Key Not Found

**Windows (PowerShell):**
```powershell
# Check if .env file exists
Test-Path "$env:USERPROFILE\.claude\skills\image-generation\.env"

# Check environment variable
echo $env:GEMINI_API_KEY
```

**Linux/macOS:**
```bash
# Check if .env file exists
ls -la ~/.claude/skills/image-generation/.env

# Check environment variable
echo $GEMINI_API_KEY
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Virtual Environment Issues (Windows)

If you have a venv created on Linux, delete it and recreate:

**PowerShell:**
```powershell
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**CMD:**
```cmd
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Portability

This skill is designed to work in any Claude Code environment:

- No hardcoded paths
- Environment variable or .env file for API key
- Relative path references
- Cross-platform compatible (Windows, Linux, macOS)
- Dependencies specified in requirements.txt
- Virtual environment support

## Development

### Setting up a development environment

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing locally

```bash
# Run the MCP server directly
python gemini_imagegen_mcp.py
```

## License

See skill metadata for license information.

## Support

- GitHub Issues: Report bugs or request features
- Documentation: See SKILL.md for detailed usage examples
- API Documentation: https://ai.google.dev/gemini-api/docs
