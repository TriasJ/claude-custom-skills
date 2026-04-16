<#
.SYNOPSIS
    Extract images from PDF files with rich contextual metadata.

.DESCRIPTION
    PowerShell wrapper for extract_images.py. Produces image_manifest.json
    with captions, surrounding text, section titles, and bounding boxes.

.PARAMETER PdfPath
    Path to the input PDF file.

.PARAMETER OutputDir
    Directory for extracted images and manifest.

.PARAMETER MineruOutput
    Path to existing MinerU output directory (optional).

.PARAMETER Engine
    Extraction engine: auto, mineru, or pymupdf (default: auto).

.PARAMETER Analyze
    Run Claude Vision analysis on extracted images.

.PARAMETER ApiKey
    Anthropic API key for vision analysis.

.PARAMETER StartPage
    Start page (0-indexed, default: 0).

.PARAMETER EndPage
    End page (0-indexed, inclusive).

.EXAMPLE
    .\extract_images.ps1 -PdfPath "paper.pdf" -OutputDir "./extracted"

.EXAMPLE
    .\extract_images.ps1 -PdfPath "paper.pdf" -OutputDir "./out" -Engine pymupdf

.EXAMPLE
    .\extract_images.ps1 -PdfPath "paper.pdf" -OutputDir "./out" -Analyze
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateScript({ Test-Path $_ -PathType Leaf })]
    [string]$PdfPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputDir,

    [string]$MineruOutput,

    [ValidateSet("auto", "mineru", "pymupdf")]
    [string]$Engine = "auto",

    [switch]$Analyze,

    [string]$ApiKey,

    [int]$StartPage = 0,

    [Nullable[int]]$EndPage
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "extract_images.py"

# Build argument list
$args_list = @($PythonScript, $PdfPath, "-o", $OutputDir, "--engine", $Engine, "--start-page", $StartPage)

if ($MineruOutput) {
    $args_list += @("--mineru-output", $MineruOutput)
}

if ($Analyze) {
    $args_list += "--analyze"
}

if ($ApiKey) {
    $args_list += @("--api-key", $ApiKey)
}

if ($null -ne $EndPage) {
    $args_list += @("--end-page", $EndPage)
}

# Find Python
$python = if (Get-Command "python3" -ErrorAction SilentlyContinue) { "python3" } else { "python" }

Write-Host "Running: $python $($args_list -join ' ')" -ForegroundColor Cyan
& $python @args_list

if ($LASTEXITCODE -ne 0) {
    Write-Error "Extraction failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}
