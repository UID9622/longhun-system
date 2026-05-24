#!/usr/bin/env bash
# 龍魂 bin 公共函数（被其它脚本 source，不要直接执行）
# 注意：~/.zshrc 里 LONGHUN_ROOT 可能指向 iCloud「龍魂主权库」，与代码仓库不是同一路径。
_longhun_resolve_repo() {
  local _script="${BASH_SOURCE[2]:-${BASH_SOURCE[1]:-${BASH_SOURCE[0]}}}"
  while [[ -L "$_script" ]]; do
    _script="$(readlink "$_script")"
  done
  cd "$(dirname "$_script")/.." && pwd
}

LONGHUN_REPO="$(_longhun_resolve_repo)"
export LONGHUN_REPO
# 兼容旧变量名：bin 脚本内 LONGHUN_ROOT = 仓库根目录
LONGHUN_ROOT="$LONGHUN_REPO"
export LONGHUN_ROOT
# iCloud 数据目录（若 zshrc 已设则保留，供其它模块用）
export LONGHUN_DATA_ROOT="${LONGHUN_DATA_ROOT:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/龍魂主权库}"
RUN_DIR="${LONGHUN_ROOT}/.run"
LOG_DIR="${LONGHUN_ROOT}/logs"
VENV_PY="${LONGHUN_ROOT}/venv/bin/python"
mkdir -p "$RUN_DIR" "$LOG_DIR"

_longhun_port_listen() {
  local port="$1"
  lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
}

_longhun_mark() {
  if _longhun_port_listen "$1"; then
    echo "🟢"
  else
    echo "⚪"
  fi
}
