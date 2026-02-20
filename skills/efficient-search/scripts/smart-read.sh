#!/bin/bash
#
# Smart Read - Size-aware file reading
# Reads files intelligently based on size to minimize token burn
#

set -e

show_help() {
    cat << EOF
Usage: smart-read.sh <filepath> [options]

Options:
    -f, --full          Force full file read (ignore size limits)
    -l, --lines N       Read last N lines only (default: 100)
    -h, --head N        Read first N lines only
    -s, --summary       Generate extractive summary
    --help              Show this help

Examples:
    smart-read.sh memory/2026-02-01.md         # Smart read based on size
    smart-read.sh large-file.md -l 50          # Read last 50 lines
    smart-read.sh config.json -f               # Force full read
EOF
}

FILE=""
MODE="smart"
LINES=100

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--full)
            MODE="full"
            shift
            ;;
        -l|--lines)
            LINES="$2"
            MODE="tail"
            shift 2
            ;;
        -h|--head)
            LINES="$2"
            MODE="head"
            shift 2
            ;;
        -s|--summary)
            MODE="summary"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            FILE="$1"
            shift
            ;;
    esac
done

if [[ -z "$FILE" ]]; then
    echo "Error: No file specified"
    show_help
    exit 1
fi

if [[ ! -f "$FILE" ]]; then
    echo "Error: File not found: $FILE"
    exit 1
fi

# Get file stats
FILE_SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)
LINE_COUNT=$(wc -l < "$FILE" | tr -d ' ')
ESTIMATED_TOKENS=$((FILE_SIZE / 4))

echo "File: $FILE"
echo "Lines: $LINE_COUNT | Size: ${FILE_SIZE}b | Est. tokens: ~$ESTIMATED_TOKENS"
echo "---"

# Smart mode decision
if [[ "$MODE" == "smart" ]]; then
    if [[ $LINE_COUNT -lt 100 ]]; then
        MODE="full"
    elif [[ $LINE_COUNT -lt 500 ]]; then
        MODE="tail"
    else
        MODE="summary"
    fi
fi

# Execute read based on mode
case $MODE in
    full)
        echo "[Reading full file...]"
        cat "$FILE"
        ;;
    head)
        echo "[Reading first $LINES lines...]"
        head -n "$LINES" "$FILE"
        ;;
    tail)
        echo "[Reading last $LINES lines (most recent)...]"
        tail -n "$LINES" "$FILE"
        ;;
    summary)
        echo "[Generating summary - file too large for full read]"
        echo ""
        echo "## File Structure"
        grep -n "^#" "$FILE" 2>/dev/null | head -20 || echo "(No headers found)"
        echo ""
        echo "## First 50 lines (preview):"
        head -50 "$FILE"
        echo ""
        echo "## Last 50 lines (recent content):"
        tail -50 "$FILE"
        ;;
esac
