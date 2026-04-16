#!/usr/bin/env python3
"""
Gemini Image Generation MCP Server

An MCP server that enables Claude to generate and edit images using Google's
Gemini image generation API (also known as "Nano Banana Pro").

Requires: GEMINI_API_KEY environment variable (or .env file in skill directory)
"""

import os
import sys
import json
import base64
import tempfile
from pathlib import Path
from typing import Optional, List, Literal
from enum import Enum
from datetime import datetime

# Load .env file from the skill directory (cross-platform)
def _load_env_file():
    """Load .env file from the skill directory if it exists."""
    try:
        from dotenv import load_dotenv
        # Get the directory where this script is located
        script_dir = Path(__file__).parent.resolve()
        env_path = script_dir / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return True
    except ImportError:
        pass  # python-dotenv not installed, rely on environment variables
    return False

_load_env_file()

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, field_validator

# Initialize MCP server
mcp = FastMCP("gemini_imagegen_mcp")

# Constants
DEFAULT_MODEL = "gemini-3-pro-image-preview"
SUPPORTED_ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]


class ImageModel(str, Enum):
    """Available image generation models."""
    GEMINI_PRO = "gemini-3-pro-image-preview"  # Best quality, contextual refinement, recommended default
    GEMINI_FLASH = "gemini-2.5-flash-image"  # Fast and capable, good second option
    IMAGEN_ULTRA = "imagen-4.0-ultra-generate-001"  # Imagen 4.0 Ultra - highest quality
    IMAGEN_FAST = "imagen-4.0-fast-generate-001"  # Imagen 4.0 Fast - quickest generation


class AspectRatio(str, Enum):
    """Supported aspect ratios for image generation."""
    SQUARE = "1:1"
    PORTRAIT_2_3 = "2:3"
    LANDSCAPE_3_2 = "3:2"
    PORTRAIT_3_4 = "3:4"
    LANDSCAPE_4_3 = "4:3"
    PORTRAIT_4_5 = "4:5"
    LANDSCAPE_5_4 = "5:4"
    PORTRAIT_9_16 = "9:16"
    LANDSCAPE_16_9 = "16:9"
    ULTRAWIDE = "21:9"


class GenerateImageInput(BaseModel):
    """Input model for text-to-image generation."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    prompt: str = Field(
        ...,
        description="Text prompt describing the image to generate. Be specific about style, composition, lighting, and details. Example: 'A photorealistic close-up portrait, shot on 85mm lens, golden hour lighting'",
        min_length=1,
        max_length=4000
    )
    output_path: str = Field(
        ...,
        description="File path where the generated image will be saved (e.g., 'C:/Users/name/output.png' or '/home/user/output.png')",
        min_length=1
    )
    aspect_ratio: AspectRatio = Field(
        default=AspectRatio.SQUARE,
        description="Aspect ratio for the generated image. Options: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9"
    )
    model: ImageModel = Field(
        default=ImageModel.GEMINI_PRO,
        description="Model: 'gemini-3-pro-image-preview' (default, best quality with contextual refinement), 'gemini-2.5-flash-image' (fast), 'imagen-4.0-ultra-generate-001' (ultra quality), 'imagen-4.0-fast-generate-001' (fastest)"
    )

    @field_validator('output_path')
    @classmethod
    def validate_output_path(cls, v: str) -> str:
        if not v.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            raise ValueError("Output path must end with .png, .jpg, .jpeg, or .webp")
        return v


class EditImageInput(BaseModel):
    """Input model for image editing."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    prompt: str = Field(
        ...,
        description="Instruction describing how to edit the image. Example: 'Add a sunset to this scene' or 'Remove the background'",
        min_length=1,
        max_length=4000
    )
    input_path: str = Field(
        ...,
        description="Path to the source image to edit"
    )
    output_path: str = Field(
        ...,
        description="File path where the edited image will be saved"
    )
    model: ImageModel = Field(
        default=ImageModel.GEMINI_PRO,
        description="Model to use for editing. Gemini models support contextual editing; Imagen models for standalone generation."
    )

    @field_validator('output_path')
    @classmethod
    def validate_output_path(cls, v: str) -> str:
        if not v.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            raise ValueError("Output path must end with .png, .jpg, .jpeg, or .webp")
        return v


class MultiImageInput(BaseModel):
    """Input model for multi-image composition."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    prompt: str = Field(
        ...,
        description="Instruction for combining/composing the reference images. Example: 'Create a group photo of these people in an office'",
        min_length=1,
        max_length=4000
    )
    input_paths: List[str] = Field(
        ...,
        description="List of paths to reference images (up to 14 images)",
        min_length=1,
        max_length=14
    )
    output_path: str = Field(
        ...,
        description="File path where the composed image will be saved"
    )
    aspect_ratio: AspectRatio = Field(
        default=AspectRatio.SQUARE,
        description="Aspect ratio for the output image"
    )
    model: ImageModel = Field(
        default=ImageModel.GEMINI_PRO,
        description="Model to use. Gemini models recommended for multi-image composition."
    )


def _is_imagen_model(model: str) -> bool:
    """Check if the model is an Imagen model (uses generate_images API)."""
    return model.startswith("imagen-")


def _get_client():
    """Get initialized Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        script_dir = Path(__file__).parent.resolve()
        raise ValueError(
            "GEMINI_API_KEY not found. Set it using one of these methods:\n"
            f"1. Create a .env file in {script_dir} with: GEMINI_API_KEY=your_key\n"
            "2. Set environment variable: export GEMINI_API_KEY=your_key (Linux/macOS)\n"
            "   or: set GEMINI_API_KEY=your_key (Windows CMD)\n"
            "   or: $env:GEMINI_API_KEY='your_key' (PowerShell)\n"
            "Get your API key from https://aistudio.google.com/apikey"
        )

    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except ImportError:
        raise ImportError(
            "google-genai package not installed. "
            "Install with: pip install google-genai"
        )


def _save_image_from_response(response, output_path: str) -> dict:
    """Extract and save image from Gemini response."""
    text_content = ""
    image_saved = False
    
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text') and part.text:
            text_content += part.text + "\n"
        elif hasattr(part, 'inline_data') and part.inline_data:
            # Save the image
            image_data = part.inline_data.data
            if isinstance(image_data, str):
                image_data = base64.b64decode(image_data)
            
            # Ensure directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            image_saved = True
    
    return {
        "success": image_saved,
        "output_path": output_path if image_saved else None,
        "description": text_content.strip() if text_content else None
    }


def _load_image_for_api(image_path: str):
    """Load an image file for the Gemini API."""
    from PIL import Image
    return Image.open(image_path)


@mcp.tool(
    name="gemini_generate_image",
    annotations={
        "title": "Generate Image from Text",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def gemini_generate_image(params: GenerateImageInput) -> str:
    """Generate an image from a text prompt using Google's Gemini/Imagen API.

    This tool creates images from detailed text descriptions. For best results,
    include specifics about style, composition, lighting, and visual details.

    Args:
        params (GenerateImageInput): Parameters including:
            - prompt (str): Detailed description of the desired image
            - output_path (str): Where to save the generated image
            - aspect_ratio (str): Image dimensions ratio (default: 1:1)
            - model (str): Which model to use

    Returns:
        str: JSON with success status, output path, and optional description

    Example prompts:
        - Photorealistic: "A photorealistic close-up portrait, shot on 85mm lens, golden hour lighting, shallow depth of field"
        - Stylized: "A kawaii red panda sticker, bold outlines, cel-shading, white background"
        - Logo: "Clean black-and-white logo with text 'Daily Grind', sans-serif font, coffee bean icon"
    """
    try:
        client = _get_client()
        model_name = params.model.value

        # Ensure output directory exists
        Path(params.output_path).parent.mkdir(parents=True, exist_ok=True)

        if _is_imagen_model(model_name):
            # Use Imagen API (generate_images)
            response = client.models.generate_images(
                model=model_name,
                prompt=params.prompt,
                config={'number_of_images': 1, 'aspect_ratio': params.aspect_ratio.value}
            )

            if response.generated_images:
                img = response.generated_images[0]
                with open(params.output_path, 'wb') as f:
                    f.write(img.image.image_bytes)
                return json.dumps({
                    "success": True,
                    "message": "Image generated successfully",
                    "output_path": params.output_path,
                    "aspect_ratio": params.aspect_ratio.value,
                    "model": model_name
                }, indent=2)
            else:
                return json.dumps({
                    "success": False,
                    "error": "No image was generated by Imagen"
                }, indent=2)
        else:
            # Use Gemini API (generate_content)
            from google.genai import types

            response = client.models.generate_content(
                model=model_name,
                contents=[params.prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                )
            )

            result = _save_image_from_response(response, params.output_path)

            if result["success"]:
                return json.dumps({
                    "success": True,
                    "message": "Image generated successfully",
                    "output_path": result["output_path"],
                    "description": result["description"],
                    "aspect_ratio": params.aspect_ratio.value,
                    "model": model_name
                }, indent=2)
            else:
                return json.dumps({
                    "success": False,
                    "error": "No image was generated in the response",
                    "response_text": result["description"]
                }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "suggestion": _get_error_suggestion(e)
        }, indent=2)


@mcp.tool(
    name="gemini_edit_image",
    annotations={
        "title": "Edit an Existing Image",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def gemini_edit_image(params: EditImageInput) -> str:
    """Edit an existing image using natural language instructions.

    Gemini automatically understands what to modify through semantic masking.
    You can add, remove, or modify elements in the image.

    Args:
        params (EditImageInput): Parameters including:
            - prompt (str): Editing instruction (e.g., "Add a sunset to this scene")
            - input_path (str): Path to the source image
            - output_path (str): Where to save the edited image
            - model (str): Which Gemini model to use

    Returns:
        str: JSON with success status and output path

    Example prompts:
        - "Add a sunset to this scene"
        - "Remove the background and make it transparent"
        - "Change the color of the car to red"
        - "Add dramatic lighting"
    """
    try:
        # Validate input file exists
        if not Path(params.input_path).exists():
            return json.dumps({
                "success": False,
                "error": f"Input file not found: {params.input_path}"
            }, indent=2)
        
        client = _get_client()
        from google.genai import types
        
        # Load the input image
        input_image = _load_image_for_api(params.input_path)
        
        response = client.models.generate_content(
            model=params.model.value,
            contents=[params.prompt, input_image],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        result = _save_image_from_response(response, params.output_path)
        
        if result["success"]:
            return json.dumps({
                "success": True,
                "message": "Image edited successfully",
                "input_path": params.input_path,
                "output_path": result["output_path"],
                "description": result["description"]
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "error": "No edited image was generated",
                "response_text": result["description"]
            }, indent=2)
            
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "suggestion": _get_error_suggestion(e)
        }, indent=2)


@mcp.tool(
    name="gemini_compose_images",
    annotations={
        "title": "Compose Multiple Images",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def gemini_compose_images(params: MultiImageInput) -> str:
    """Create a new image by combining multiple reference images.

    This tool can compose up to 14 reference images into a new scene.
    Useful for product comparisons, character sheets, team photos, 
    and maintaining consistent styles across images.

    Args:
        params (MultiImageInput): Parameters including:
            - prompt (str): How to combine the images
            - input_paths (list): Paths to reference images (max 14)
            - output_path (str): Where to save the result
            - aspect_ratio (str): Output image dimensions
            - model (str): Which Gemini model to use

    Returns:
        str: JSON with success status and output path

    Example use cases:
        - "Create a group photo of these people in an office"
        - "Combine these product images into a comparison shot"
        - "Create a character sheet showing all these poses"
    """
    try:
        # Validate all input files exist
        missing_files = [p for p in params.input_paths if not Path(p).exists()]
        if missing_files:
            return json.dumps({
                "success": False,
                "error": f"Input files not found: {missing_files}"
            }, indent=2)
        
        client = _get_client()
        from google.genai import types
        
        # Build content list with prompt and all images
        contents = [params.prompt]
        for img_path in params.input_paths:
            contents.append(_load_image_for_api(img_path))
        
        response = client.models.generate_content(
            model=params.model.value,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
            )
        )
        
        result = _save_image_from_response(response, params.output_path)
        
        if result["success"]:
            return json.dumps({
                "success": True,
                "message": f"Composed {len(params.input_paths)} images successfully",
                "input_count": len(params.input_paths),
                "output_path": result["output_path"],
                "description": result["description"]
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "error": "No composed image was generated",
                "response_text": result["description"]
            }, indent=2)
            
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "suggestion": _get_error_suggestion(e)
        }, indent=2)


@mcp.tool(
    name="gemini_list_models",
    annotations={
        "title": "List Available Models",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def gemini_list_models() -> str:
    """List available Gemini image generation models and their capabilities.

    Returns information about available models, supported aspect ratios,
    and recommended use cases.

    Returns:
        str: JSON with model information and capabilities
    """
    return json.dumps({
        "models": [
            {
                "id": "gemini-3-pro-image-preview",
                "name": "Gemini 3 Pro (Image Preview)",
                "description": "Best quality with contextual refinement - can refine images iteratively",
                "best_for": ["Logos", "Text in images", "Complex scenes", "Iterative refinement", "Professional assets"],
                "api": "generate_content",
                "default": True
            },
            {
                "id": "gemini-2.5-flash-image",
                "name": "Gemini 2.5 Flash Image",
                "description": "Fast and capable multimodal image generation",
                "best_for": ["Quick iterations", "Text+image responses", "General purpose"],
                "api": "generate_content",
                "default": False
            },
            {
                "id": "imagen-4.0-ultra-generate-001",
                "name": "Imagen 4.0 Ultra",
                "description": "Highest quality standalone image generation",
                "best_for": ["Photorealistic images", "High detail", "Premium quality"],
                "api": "generate_images",
                "default": False
            },
            {
                "id": "imagen-4.0-fast-generate-001",
                "name": "Imagen 4.0 Fast",
                "description": "Fastest image generation for rapid prototyping",
                "best_for": ["Quick prototypes", "High volume", "Speed priority"],
                "api": "generate_images",
                "default": False
            }
        ],
        "supported_aspect_ratios": SUPPORTED_ASPECT_RATIOS,
        "features": [
            "Text-to-image generation",
            "Image editing with semantic masking",
            "Multi-image composition (up to 14 reference images)",
            "Natural language instructions"
        ],
        "setup": {
            "api_key": "Set GEMINI_API_KEY environment variable",
            "get_key_url": "https://aistudio.google.com/apikey"
        }
    }, indent=2)


def _get_error_suggestion(error: Exception) -> str:
    """Provide helpful suggestions based on error type."""
    error_str = str(error).lower()

    if "api_key" in error_str or "authentication" in error_str or "gemini_api_key" in error_str:
        return "Create a .env file in the skill directory with GEMINI_API_KEY=your_key, or set the environment variable. Get a key at https://aistudio.google.com/apikey"
    elif "quota" in error_str or "rate" in error_str:
        return "You may have exceeded API rate limits. Wait a moment and try again."
    elif "not found" in error_str:
        return "Check that the file path exists and is accessible."
    elif "permission" in error_str:
        return "Check file permissions for the input/output paths."
    elif "import" in error_str or "module" in error_str:
        return "Install required packages: pip install google-genai Pillow"
    else:
        return "Check the error message above. Ensure GEMINI_API_KEY is set and the google-genai package is installed."


if __name__ == "__main__":
    mcp.run()
