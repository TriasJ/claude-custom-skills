<#
.SYNOPSIS
    Parse PDF files using MinerU and extract text, images, tables, and formulas.

.DESCRIPTION
    A wrapper script for MinerU that simplifies PDF parsing and provides
    sensible defaults for common use cases.

.PARAMETER Path
    Path to the PDF file or directory containing PDFs.

.PARAMETER Output
    Output directory for parsed files. Defaults to ./output

.PARAMETER Language
    Language for OCR optimization. Defaults to 'en' for English.
    Options: en, ch, korean, japan, arabic, latin, etc.

.PARAMETER StartPage
    Starting page number (0-indexed). Optional.

.PARAMETER EndPage
    Ending page number (0-indexed). Optional.

.PARAMETER Method
    Parsing method: auto, txt, ocr. Defaults to 'auto'.

.PARAMETER Backend
    Processing backend. Defaults to 'pipeline' for CPU compatibility.
    Options: pipeline, hybrid-auto-engine, vlm-auto-engine

.PARAMETER NoFormula
    Disable formula parsing.

.PARAMETER NoTable
    Disable table parsing.

.PARAMETER Device
    Device for processing: cpu, cuda, cuda:0. Defaults to 'cpu'.

.EXAMPLE
    .\parse_pdf.ps1 -Path "document.pdf"

.EXAMPLE
    .\parse_pdf.ps1 -Path "document.pdf" -Output "./results" -Language "en"

.EXAMPLE
    .\parse_pdf.ps1 -Path "./pdfs/" -StartPage 0 -EndPage 10
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Path,

    [Parameter(Mandatory=$false)]
    [string]$Output = "./output",

    [Parameter(Mandatory=$false)]
    [string]$Language = "en",

    [Parameter(Mandatory=$false)]
    [int]$StartPage = -1,

    [Parameter(Mandatory=$false)]
    [int]$EndPage = -1,

    [Parameter(Mandatory=$false)]
    [ValidateSet("auto", "txt", "ocr")]
    [string]$Method = "auto",

    [Parameter(Mandatory=$false)]
    [ValidateSet("pipeline", "hybrid-auto-engine", "vlm-auto-engine")]
    [string]$Backend = "pipeline",

    [switch]$NoFormula,
    [switch]$NoTable,

    [Parameter(Mandatory=$false)]
    [string]$Device = "cpu"
)

# Build command
$cmd = "mineru -p `"$Path`" -o `"$Output`" -l $Language -m $Method -b $Backend -d $Device"

# Add optional parameters
if ($StartPage -ge 0) {
    $cmd += " -s $StartPage"
}

if ($EndPage -ge 0) {
    $cmd += " -e $EndPage"
}

if ($NoFormula) {
    $cmd += " -f false"
}

if ($NoTable) {
    $cmd += " -t false"
}

# Create output directory if it doesn't exist
if (-not (Test-Path $Output)) {
    New-Item -ItemType Directory -Path $Output -Force | Out-Null
    Write-Host "Created output directory: $Output"
}

# Display command being run
Write-Host "Running: $cmd" -ForegroundColor Cyan
Write-Host ""

# Execute
Invoke-Expression $cmd

# Check results
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Parsing complete! Output files:" -ForegroundColor Green
    Get-ChildItem -Path $Output -Recurse | ForEach-Object {
        Write-Host "  - $($_.FullName)"
    }
} else {
    Write-Host ""
    Write-Host "Parsing failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}
