---
name: image-generation
description: Generate and edit images using Google's Gemini and Imagen APIs. Use when Claude needs to create images from text prompts, edit existing images, compose multiple images, create logos, illustrations, or any visual content. Triggers on requests like "generate an image", "create a picture", "edit this photo", "make a logo", "draw", "illustrate", or any image creation task.
---

<objective>
Generate, edit, and compose images using Google's Gemini and Imagen image generation APIs. This skill provides access to multiple models optimized for different use cases: photorealistic images, text rendering, logos, and rapid prototyping.

The skill automatically loads API credentials from a `.env` file in the skill directory, making it portable across different machines and Claude Code instances.
</objective>

<quick_start>
**Generate an image using Python:**

```python
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path
import os

# Load API key from skill directory
skill_dir = Path.home() / ".claude" / "skills" / "image-generation"
load_dotenv(skill_dir / ".env")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["A professional logo with the text 'My Brand', modern minimalist style"],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
)

for part in response.candidates[0].content.parts:
    if hasattr(part, "inline_data") and part.inline_data:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
        print("Image saved to output.png")
```

**Cross-platform paths:**
- Windows: `%USERPROFILE%\.claude\skills\image-generation`
- Linux/macOS: `~/.claude/skills/image-generation`
</quick_start>

<success_criteria>
- Image file saved to specified output path
- No API key errors (`.env` file loaded correctly)
- Generated image matches prompt description
- Text in images rendered clearly (when using Gemini models)
</success_criteria>

<models>
| Model | Best For | API Method |
|-------|----------|------------|
| `gemini-3-pro-image-preview` | **Default** - Best quality, contextual refinement, logos, text rendering | `generate_content` |
| `gemini-2.5-flash-image` | Fast multimodal generation, good second option | `generate_content` |
| `imagen-4.0-ultra-generate-001` | Highest quality photorealistic images | `generate_images` |
| `imagen-4.0-fast-generate-001` | Fastest generation for rapid prototyping | `generate_images` |

**Model selection guidance:**
- For **text in images** (logos, slides, diagrams): Use `gemini-3-pro-image-preview`
- For **photorealistic images**: Use `imagen-4.0-ultra-generate-001`
- For **quick iterations**: Use `gemini-2.5-flash-image` or `imagen-4.0-fast-generate-001`
</models>

<api_usage>
**Gemini models** use `generate_content`:
```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
)
```

**Imagen models** use `generate_images`:
```python
response = client.models.generate_images(
    model="imagen-4.0-ultra-generate-001",
    prompt=prompt,
    config={"number_of_images": 1, "aspect_ratio": "1:1"}
)
# Access: response.generated_images[0].image.image_bytes
```
</api_usage>

<setup>
**1. Get API key:** https://aistudio.google.com/apikey

**2. Create `.env` file in skill directory:**

Windows (PowerShell):
```powershell
cd $env:USERPROFILE\.claude\skills\image-generation
copy .env.example .env
notepad .env  # Add your API key
```

Linux/macOS:
```bash
cd ~/.claude/skills/image-generation
cp .env.example .env
nano .env  # Add your API key
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

The `.env` file format:
```
GEMINI_API_KEY=your_api_key_here
```
</setup>

<aspect_ratios>
Supported ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
</aspect_ratios>

<prompting_tips>
**Photorealistic images:**
```
A photorealistic close-up portrait, shot on 85mm lens, golden hour lighting, shallow depth of field
```

**Logos with text:**
```
Clean black-and-white logo with text 'Daily Grind', sans-serif font, coffee bean icon, minimal design
```

**Presentation slides:**
```
Professional presentation slide about [topic], dark background, bullet points, relevant imagery on the right
```

**Product mockups:**
```
Studio-lit product photo on polished concrete, 3-point softbox, 45-degree angle
```
</prompting_tips>

<image_editing>
Pass an existing image with editing instructions (Gemini models only):

```python
from PIL import Image

img = Image.open("input.png")
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Add a sunset to this scene", img],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
)
```
</image_editing>

<mcp_server>
The skill includes an MCP server for Claude Code and Claude Desktop integration.

**Add to Claude Code:**

Windows:
```powershell
claude mcp add gemini-imagegen -- python "$env:USERPROFILE\.claude\skills\image-generation\gemini_imagegen_mcp.py"
```

Linux/macOS:
```bash
claude mcp add gemini-imagegen -- python ~/.claude/skills/image-generation/gemini_imagegen_mcp.py
```

**MCP Tools:**
- `gemini_generate_image` - Create images from text prompts
- `gemini_edit_image` - Edit existing images with instructions
- `gemini_compose_images` - Combine up to 14 reference images
- `gemini_list_models` - List available models and capabilities
</mcp_server>

<troubleshooting>
- **API Key Error**: Ensure `.env` file exists in skill directory with `GEMINI_API_KEY=your_key`
- **Import Error**: Run `pip install -r requirements.txt`
- **Rate Limits**: Wait and retry, or check quota at Google AI Studio
- **Model not found**: Use exact model names from the models table above
</troubleshooting>
