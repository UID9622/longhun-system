#!/usr/bin/env bash
# Usage: run this on the Huawei cloud host (as root or user with docker/ollama access)
set -euo pipefail

MODEL=qwen2.5:7b
AUDIT_DIR=/root/CNSH/audit
mkdir -p "$AUDIT_DIR"

echo "Pulling model $MODEL..."
ollama pull "$MODEL"

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$AUDIT_DIR/iam_trace.log" <<EOF
$TS | IAM-UID=3e53a2df623044e499b9227c93d55955 | IP=$(hostname -I | awk '{print $1}') | DIR=/root/CNSH | MODEL=$MODEL | DNA=#龍芯⚡️2026-05-23-20:02-EXTERNAL-CLOUD-IAM-VERBATIM-TRACE-v1.0
EOF

echo "Model pulled and IAM trace written to $AUDIT_DIR/iam_trace.log"
