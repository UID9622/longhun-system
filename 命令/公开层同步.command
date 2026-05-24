#!/bin/bash
# L3 公开层 · 监听 ~/longhun-pub → DB_PUB
export PATH="$HOME/longhun-system/venv/bin:$PATH"
source "$HOME/.longhun/secrets.env" 2>/dev/null || true
exec python3 "$HOME/longhun-lu/code/longhun_sync.py"
