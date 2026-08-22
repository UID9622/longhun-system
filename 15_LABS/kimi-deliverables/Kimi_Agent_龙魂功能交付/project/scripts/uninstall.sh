# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-38227bb0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env bash
# 龍魂自愈引擎 · launchd 卸载脚本。幂等；日志与审计只增不删，卸载不清理。
set -euo pipefail

LABEL="com.longhun.selfheal"
LONGHUN_HOME="${LONGHUN_HOME:-$HOME/.longhun}"
PLIST_PATH="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
  if ! launchctl bootout "$DOMAIN/$LABEL"; then
    echo "[uninstall] 错误：bootout 失败，请执行 'launchctl print $DOMAIN/$LABEL' 排查" >&2
    exit 1
  fi
  echo "[uninstall] 已 bootout $LABEL"
else
  echo "[uninstall] 服务未加载，跳过 bootout（幂等）"
fi

if [ -f "$PLIST_PATH" ]; then
  rm -f "$PLIST_PATH"
  echo "[uninstall] 已移除 $PLIST_PATH"
else
  echo "[uninstall] plist 不存在，跳过移除（幂等）"
fi

echo "[uninstall] ✅ 完成。日志/审计/耻辱墙按只增不删协议保留在 $LONGHUN_HOME"
