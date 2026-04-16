# Gemini Image Generation Skill - Windows Setup Script
# Run this script in PowerShell to set up the skill

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Gemini Image Generation Skill Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Navigate to script directory
Set-Location $scriptDir
Write-Host "Working directory: $scriptDir" -ForegroundColor Gray

# Check if venv exists and has wrong structure (Linux venv on Windows)
if (Test-Path "venv\bin") {
    Write-Host "Detected Linux virtual environment. Removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$scriptDir\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "Dependencies installed." -ForegroundColor Green

# Check for .env file
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host ""
        Write-Host "Creating .env file from template..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host ""
        Write-Host "IMPORTANT: Edit the .env file and add your Gemini API key!" -ForegroundColor Red
        Write-Host "Get your API key from: https://aistudio.google.com/apikey" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Opening .env file for editing..." -ForegroundColor Yellow
        notepad ".env"
    } else {
        Write-Host "WARNING: .env.example not found. Please create .env manually." -ForegroundColor Red
    }
} else {
    Write-Host ".env file already exists." -ForegroundColor Green
}

# Show next steps
Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Make sure your API key is in the .env file"
Write-Host "2. Add the MCP server to Claude Code:"
Write-Host ""
Write-Host "   claude mcp add gemini-imagegen -- python `"$scriptDir\gemini_imagegen_mcp.py`"" -ForegroundColor White
Write-Host ""
Write-Host "3. Verify with: claude mcp list"
Write-Host ""
