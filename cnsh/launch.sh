#!/usr/bin/env bash
# CNSH 整合版任務執行引擎啟動腳本
# DNA: #龍芯⚡️2026-06-17-CNSH-LAUNCH-v1.0

cd "$(dirname "$0")"
echo "🐉 啟動 CNSH 整合版任務執行引擎"
python3 task_executor_v9_integrated.py "$@"
