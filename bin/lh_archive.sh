#!/bin/bash
# LongHun Archive Script
# DNA: #龍芯⚡️2026-07-18-ARCHIVE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

ARCHIVE_DIR="$HOME/longhun-system/L3_语义层/$(date +%Y%m%d)"
MODEL_PATH="$HOME/longhun-models/best_checkpoint"
DATA_PATH="$HOME/longhun-data/clean_998_clean.jsonl"
REPORT_PATH="$HOME/longhun-models/eval_report.json"

echo "[ARCHIVE] LongHun System L3 Layer"
echo "[DNA] #龍芯⚡️2026-07-18-ARCHIVE-v1.0"

mkdir -p "$ARCHIVE_DIR"

# Copy model
if [ -d "$MODEL_PATH" ]; then
    cp -r "$MODEL_PATH" "$ARCHIVE_DIR/model"
    echo "[COPY] Model -> $ARCHIVE_DIR/model"
fi

# Copy data
if [ -f "$DATA_PATH" ]; then
    cp "$DATA_PATH" "$ARCHIVE_DIR/data.jsonl"
    echo "[COPY] Data -> $ARCHIVE_DIR/data.jsonl"
fi

# Copy report
if [ -f "$REPORT_PATH" ]; then
    cp "$REPORT_PATH" "$ARCHIVE_DIR/report.json"
    echo "[COPY] Report -> $ARCHIVE_DIR/report.json"
fi

# Generate DNA signature
HASH=$(find "$ARCHIVE_DIR" -type f -exec sha256sum {} \; | sha256sum | cut -d' ' -f1 | head -c 16)

cat > "$ARCHIVE_DIR/DNA.sig" << EOF
#龍芯⚡️2026-07-18-ARCHIVE-v1.0-$HASH
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%SZ)
LAYER: L3_语义层
STATUS: SEALED
EOF

echo "[SEAL] DNA.sig generated"
echo "[DONE] Archive: $ARCHIVE_DIR"
echo "[HASH] $HASH"
