# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env bash
# 龍魂自愈引擎 · macOS launchd 一键部署脚本。
# 幂等可重入；$HOME 动态展开，禁硬编码用户名；仅 macOS 真机可验证 launchctl（🟡）。
set -euo pipefail

LABEL="com.longhun.selfheal"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LONGHUN_HOME="${LONGHUN_HOME:-$HOME/.longhun}"
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$PLIST_DIR/$LABEL.plist"
TEMPLATE="$SCRIPT_DIR/$LABEL.plist.template"
DOMAIN="gui/$(id -u)"

# DNA 占位横幅：优先调用信任核心生成（生成器不可用时其内部自动日期占位兜底，
# 永不手写干支）；python 不可用则打印固定占位串。
print_banner() {
  local dna
  if dna="$(PYTHONPATH="$PROJECT_ROOT" python3 -c \
      'from longhun_trust.dna import generate_dna; print(generate_dna("INSTALL"))' \
      2>/dev/null)" && [ -n "$dna" ]; then
    echo "$dna"
  else
    echo "#龍芯⚡️$(date +%F)-INSTALL-v1.0-【干支待本地生成器校准】"
  fi
}

print_banner
echo "[install] 项目根: $PROJECT_ROOT"
echo "[install] LONGHUN_HOME: $LONGHUN_HOME"

if [ ! -f "$TEMPLATE" ]; then
  echo "[install] 错误：plist 模板缺失 $TEMPLATE" >&2
  exit 1
fi

# sed 以 | 为分隔符且 & 在替换串中有特殊含义：替换前校验变量不含 & 或 |，
# 防止路径里的特殊字符注入/破坏 plist（含则报错退出非零）。
for var_name in HOME PROJECT_ROOT LONGHUN_HOME; do
  var_value="${!var_name}"
  case "$var_value" in
    *[\&\|]*)
      echo "[install] 错误：\$$var_name 含非法字符 '&' 或 '|'：$var_value" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$PLIST_DIR" "$LONGHUN_HOME/logs"

# 用 $HOME / 项目根 / LONGHUN_HOME 动态生成 plist
# （sed 替换占位符，先写临时文件再比对，保证幂等）。
TMP_PLIST="$(mktemp)"
trap 'rm -f "$TMP_PLIST"' EXIT
sed -e "s|__HOME__|$HOME|g" -e "s|__PROJECT_ROOT__|$PROJECT_ROOT|g" \
  -e "s|__LONGHUN_HOME__|$LONGHUN_HOME|g" \
  "$TEMPLATE" >"$TMP_PLIST"

if [ -f "$PLIST_PATH" ] && cmp -s "$TMP_PLIST" "$PLIST_PATH"; then
  echo "[install] plist 无变化，跳过写入（幂等）"
else
  cp "$TMP_PLIST" "$PLIST_PATH"
  echo "[install] 已写入 $PLIST_PATH"
fi

# 测试/自检逃生门：LONGHUN_INSTALL_DRYRUN=1 时生成完 plist 即退出，
# 不触碰 launchctl（launchd 仅 macOS 真机可验证 🟡）。
if [ "${LONGHUN_INSTALL_DRYRUN:-0}" = "1" ]; then
  echo "[install] DRYRUN：plist 已生成，跳过 launchctl 装载"
  exit 0
fi

# 已加载则先卸载再装载（幂等重入）；未加载直接 bootstrap。
if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
  echo "[install] 服务已加载，先 bootout 再 bootstrap"
  launchctl bootout "$DOMAIN/$LABEL" || {
    echo "[install] 错误：bootout 失败，请执行 'launchctl print $DOMAIN/$LABEL' 排查" >&2
    exit 1
  }
fi

if ! launchctl bootstrap "$DOMAIN" "$PLIST_PATH"; then
  echo "[install] 错误：launchctl bootstrap 失败。" >&2
  echo "[install] 排查：plutil -lint '$PLIST_PATH'；确认在 macOS 图形会话内执行（launchd 仅 macOS 真机可验证 🟡）。" >&2
  exit 1
fi

echo "[install] ✅ $LABEL 已通过 launchd 装载（KeepAlive + RunAtLoad，日志在 $LONGHUN_HOME/logs/）"
