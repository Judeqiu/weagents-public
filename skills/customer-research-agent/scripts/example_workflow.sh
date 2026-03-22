#!/bin/bash
# Example Workflow for Customer Research Agent
# 
# This script demonstrates the complete workflow for researching a customer
# and generating analysis + email using OpenClaw.

set -e

# Configuration
COMPANY_NAME="${1:-TechVision Automation GmbH}"
OUTPUT_DIR="./example_output"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=================================="
echo "Customer Research Agent - Example Workflow"
echo "=================================="
echo ""
echo "Company: $COMPANY_NAME"
echo "Output: $OUTPUT_DIR"
echo ""

# Step 1: Check Chrome CDP
echo "Step 1: Checking Chrome CDP connection..."
if curl -s http://127.0.0.1:9222/json/version > /dev/null 2>&1; then
    echo "  ✓ Chrome CDP is accessible"
else
    echo "  ✗ Chrome CDP not accessible at http://127.0.0.1:9222"
    echo ""
    echo "Please start Chrome with:"
    echo "  google-chrome --remote-debugging-port=9222 --user-data-dir=~/.chrome-research &"
    exit 1
fi

# Step 2: Run research
echo ""
echo "Step 2: Running automated research..."
python3 "$SCRIPT_DIR/research_customer.py" \
    --company "$COMPANY_NAME" \
    --output "$OUTPUT_DIR"

# Find the generated files
DATA_FILE=$(ls -t "$OUTPUT_DIR"/*_data.json 2>/dev/null | head -1)
if [ -z "$DATA_FILE" ]; then
    echo "  ✗ Research data file not found"
    exit 1
fi

echo "  ✓ Research data: $DATA_FILE"

# Step 3: Generate analysis prompt
echo ""
echo "Step 3: Preparing AI analysis..."
python3 "$SCRIPT_DIR/analyze_customer.py" \
    --data "$DATA_FILE" \
    --prompt-only > "$OUTPUT_DIR/analysis_prompt.txt"

echo "  ✓ Analysis prompt saved to: $OUTPUT_DIR/analysis_prompt.txt"
echo ""
echo "  Next: Copy the prompt from $OUTPUT_DIR/analysis_prompt.txt"
echo "        and send it to your LLM (OpenClaw/ChatGPT/Claude/etc.)"
echo "        Save the JSON response as: $OUTPUT_DIR/analysis.json"
echo ""

# Display summary
echo "=================================="
echo "Files Generated:"
echo "=================================="
ls -la "$OUTPUT_DIR"/*"$(basename "$DATA_FILE" | cut -d'_' -f1-2)"* 2>/dev/null || ls -la "$OUTPUT_DIR"

echo ""
echo "Next Steps:"
echo "  1. Review the research report: $OUTPUT_DIR/*_report.md"
echo "  2. Get AI analysis using the prompt in: $OUTPUT_DIR/analysis_prompt.txt"
echo "  3. Save AI response as: $OUTPUT_DIR/analysis.json"
echo "  4. Generate email: python3 $SCRIPT_DIR/analyze_customer.py --data $DATA_FILE --analysis $OUTPUT_DIR/analysis.json"
echo ""
echo "Or use this one-liner for full workflow:"
echo "  python3 $SCRIPT_DIR/research_customer.py --company \"$COMPANY_NAME\" --output $OUTPUT_DIR"
