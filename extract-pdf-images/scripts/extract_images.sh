#!/usr/bin/env bash
# Extract images from PDF files with rich contextual metadata.
#
# Usage:
#   ./extract_images.sh <pdf_path> -o <output_dir> [options]
#
# Options:
#   -o, --output DIR          Output directory (required)
#   --mineru-output DIR       Path to existing MinerU output
#   --engine ENGINE           auto|mineru|pymupdf (default: auto)
#   --analyze                 Run Claude Vision analysis
#   --api-key KEY             Anthropic API key
#   --start-page N            Start page (0-indexed, default: 0)
#   --end-page N              End page (0-indexed, inclusive)
#
# Examples:
#   ./extract_images.sh paper.pdf -o ./extracted
#   ./extract_images.sh paper.pdf -o ./out --engine pymupdf
#   ./extract_images.sh paper.pdf -o ./out --analyze

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/extract_images.py"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <pdf_path> -o <output_dir> [options]" >&2
    exit 1
fi

# Find Python
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "Error: Python not found. Install Python 3.8+." >&2
    exit 1
fi

echo "Running: ${PYTHON} ${PYTHON_SCRIPT} $*" >&2
exec "${PYTHON}" "${PYTHON_SCRIPT}" "$@"
