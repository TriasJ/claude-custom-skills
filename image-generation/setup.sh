#!/bin/bash
# Gemini Image Generation Skill - Linux/macOS Setup Script
# Run this script to set up the skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Gemini Image Generation Skill Setup ==="
echo ""

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "Found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "Found: $(python --version)"
else
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

# Navigate to script directory
cd "$SCRIPT_DIR"
echo "Working directory: $SCRIPT_DIR"

# Check if venv exists and has wrong structure (Windows venv on Linux)
if [ -d "venv/Scripts" ]; then
    echo "Detected Windows virtual environment. Removing..."
    rm -rf venv
fi

# Create virtual environment if it doesn't exist
if [ ! -f "venv/bin/python" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "Dependencies installed."

# Check for .env file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo ""
        echo "Creating .env file from template..."
        cp .env.example .env
        echo ""
        echo "IMPORTANT: Edit the .env file and add your Gemini API key!"
        echo "Get your API key from: https://aistudio.google.com/apikey"
        echo ""

        # Try to open with available editor
        if command -v nano &> /dev/null; then
            echo "Opening .env file with nano..."
            nano .env
        elif command -v vim &> /dev/null; then
            echo "Opening .env file with vim..."
            vim .env
        elif command -v code &> /dev/null; then
            echo "Opening .env file with VS Code..."
            code .env
        else
            echo "Please edit .env manually and add your API key."
        fi
    else
        echo "WARNING: .env.example not found. Please create .env manually."
    fi
else
    echo ".env file already exists."
fi

# Show next steps
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Make sure your API key is in the .env file"
echo "2. Add the MCP server to Claude Code:"
echo ""
echo "   claude mcp add gemini-imagegen -- python $SCRIPT_DIR/gemini_imagegen_mcp.py"
echo ""
echo "3. Verify with: claude mcp list"
echo ""
