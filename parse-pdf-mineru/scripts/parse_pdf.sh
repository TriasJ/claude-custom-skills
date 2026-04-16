#!/bin/bash
#
# Parse PDF files using MinerU and extract text, images, tables, and formulas.
#
# Usage:
#   ./parse_pdf.sh <pdf_path> [options]
#
# Options:
#   -o, --output DIR      Output directory (default: ./output)
#   -l, --lang LANG       Language for OCR (default: en)
#   -s, --start PAGE      Start page (0-indexed)
#   -e, --end PAGE        End page (0-indexed)
#   -m, --method METHOD   Parsing method: auto, txt, ocr (default: auto)
#   -b, --backend BACKEND Backend: pipeline, hybrid-auto-engine (default: pipeline)
#   -d, --device DEVICE   Device: cpu, cuda, cuda:0 (default: cpu)
#   --no-formula          Disable formula parsing
#   --no-table            Disable table parsing
#   -h, --help            Show this help message
#
# Examples:
#   ./parse_pdf.sh document.pdf
#   ./parse_pdf.sh document.pdf -o ./results -l en
#   ./parse_pdf.sh ./pdfs/ -s 0 -e 10

set -e

# Default values
OUTPUT="./output"
LANGUAGE="en"
METHOD="auto"
BACKEND="pipeline"
DEVICE="cpu"
START_PAGE=""
END_PAGE=""
FORMULA="true"
TABLE="true"

# Help function
show_help() {
    sed -n '2,25p' "$0" | sed 's/^# //'
    exit 0
}

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -l|--lang)
            LANGUAGE="$2"
            shift 2
            ;;
        -s|--start)
            START_PAGE="$2"
            shift 2
            ;;
        -e|--end)
            END_PAGE="$2"
            shift 2
            ;;
        -m|--method)
            METHOD="$2"
            shift 2
            ;;
        -b|--backend)
            BACKEND="$2"
            shift 2
            ;;
        -d|--device)
            DEVICE="$2"
            shift 2
            ;;
        --no-formula)
            FORMULA="false"
            shift
            ;;
        --no-table)
            TABLE="false"
            shift
            ;;
        -h|--help)
            show_help
            ;;
        -*|--*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Check for required argument
if [ ${#POSITIONAL_ARGS[@]} -eq 0 ]; then
    echo "Error: PDF path is required"
    echo "Usage: ./parse_pdf.sh <pdf_path> [options]"
    exit 1
fi

PDF_PATH="${POSITIONAL_ARGS[0]}"

# Build command
CMD="mineru -p \"$PDF_PATH\" -o \"$OUTPUT\" -l $LANGUAGE -m $METHOD -b $BACKEND -d $DEVICE -f $FORMULA -t $TABLE"

# Add optional page range
if [ -n "$START_PAGE" ]; then
    CMD="$CMD -s $START_PAGE"
fi

if [ -n "$END_PAGE" ]; then
    CMD="$CMD -e $END_PAGE"
fi

# Create output directory
mkdir -p "$OUTPUT"

# Display command
echo "Running: $CMD"
echo ""

# Execute
eval $CMD

# Check results
if [ $? -eq 0 ]; then
    echo ""
    echo "Parsing complete! Output files:"
    find "$OUTPUT" -type f | while read -r file; do
        echo "  - $file"
    done
else
    echo ""
    echo "Parsing failed!"
    exit 1
fi
