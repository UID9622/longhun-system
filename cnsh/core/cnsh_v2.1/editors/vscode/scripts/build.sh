#!/usr/bin/env bash
# CNSH VS Code 插件构建脚本
# DNA: #龍芯⚡️2026-06-29-CNSH-VSCODE-BUILD-v0.1.0
set -e
cd "$(dirname "$0")/.."

npm install
npx tsc -p ./
npx vsce package --out ./cnsh-vscode.vsix

echo "✅ 插件已打包: $(pwd)/cnsh-vscode.vsix"
