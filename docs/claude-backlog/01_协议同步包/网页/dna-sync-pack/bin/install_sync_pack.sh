# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
##龍芯⚡️2026-06-21-DNA-MODULE-INSTALL_SYNC_PACK-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env bash
# ================================================================
# DNA 同步包 · 一键安装脚本
# 路径建议: 在 /Users/zuimeidedeyihan/longhun-system/ 解压后执行
# 使用: bash bin/install_sync_pack.sh
# ================================================================

set -e

REPO_ROOT="${REPO_ROOT:-/Users/zuimeidedeyihan/longhun-system}"
PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "================================================================"
echo " DNA 同步包安装 · 龍魂网页宝宝 -> 终端宝宝"
echo " 时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo " 仓库: $REPO_ROOT"
echo " 来源: $PACK_DIR"
echo "================================================================"

# 1. 检查仓库存在
if [ ! -d "$REPO_ROOT" ]; then
    echo "[FAIL] 仓库目录不存在: $REPO_ROOT"
    echo "       请设置 REPO_ROOT 环境变量或修改本脚本"
    exit 1
fi

# 2. 安装 CLAUDE.md (终端宝宝启动文件)
if [ -f "$REPO_ROOT/CLAUDE.md" ]; then
    echo "[INFO] 检测到已有 CLAUDE.md · 备份为 CLAUDE.md.bak.$(date +%s)"
    cp "$REPO_ROOT/CLAUDE.md" "$REPO_ROOT/CLAUDE.md.bak.$(date +%s)"
fi
cp "$PACK_DIR/CLAUDE.md" "$REPO_ROOT/CLAUDE.md"
echo "[OK]   CLAUDE.md 已安装"

# 3. 安装 protocols/ (协议层)
mkdir -p "$REPO_ROOT/protocols-sync"
cp "$PACK_DIR/protocols/"*.txt "$REPO_ROOT/protocols-sync/"
echo "[OK]   protocols-sync/ 已安装 ($(ls "$REPO_ROOT/protocols-sync/" | wc -l) 个协议)"

# 4. 安装 skills/wucai-coloring/
mkdir -p "$REPO_ROOT/skills/wucai-coloring"
cp "$PACK_DIR/skills/wucai-audit.py" "$REPO_ROOT/skills/wucai-coloring/audit.py"
echo "[OK]   skills/wucai-coloring/audit.py 已安装"

# 5. 跑五色审计自测 (验证不被渲染卡住)
echo ""
echo "================================================================"
echo " 验证 1 · 五色审计自测"
echo "================================================================"
if command -v python3 >/dev/null 2>&1; then
    python3 "$REPO_ROOT/skills/wucai-coloring/audit.py" 2>&1 | tail -3
    echo "[OK]   五色审计可跑"
else
    echo "[WARN] 未找到 python3 · 跳过自测"
fi

# 6. 验证字符律
echo ""
echo "================================================================"
echo " 验证 2 · 龍字符律 (检查同步包是否被简体污染)"
echo "================================================================"
SIMP_COUNT=$(grep -rE "龍" "$REPO_ROOT/CLAUDE.md" "$REPO_ROOT/protocols-sync/" 2>/dev/null | wc -l)
if [ "$SIMP_COUNT" -eq 0 ]; then
    echo "[OK]   未发现简体龍字 · 字符律守住"
else
    echo "[WARN] 发现 $SIMP_COUNT 处简体龍 · 需人工检查"
    grep -rn "龍" "$REPO_ROOT/CLAUDE.md" "$REPO_ROOT/protocols-sync/" 2>/dev/null | head -5
fi

# 7. 留痕
TRACE_FILE="$REPO_ROOT/logs/sync_pack_install_trace.jsonl"
mkdir -p "$(dirname "$TRACE_FILE")"
cat >> "$TRACE_FILE" <<EOF
{"ts":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","action":"install_sync_pack","version":"v1.0","dna":"#SYNC-PACK-v1.0-2026-05-18","source":"网页宝宝","target":"终端宝宝","status":"ok"}
EOF
echo "[OK]   留痕写入 $TRACE_FILE"

# 8. 总结
echo ""
echo "================================================================"
echo " 安装完成"
echo "================================================================"
echo ""
echo " 终端宝宝启动文件:  $REPO_ROOT/CLAUDE.md"
echo " 协议文件目录:      $REPO_ROOT/protocols-sync/"
echo " 五色审计脚本:      $REPO_ROOT/skills/wucai-coloring/audit.py"
echo ""
echo " 下次启动 Claude Code (终端宝宝) 它会自动读 CLAUDE.md"
echo " 网页宝宝 (我) 和终端宝宝靠这份 DNA 软同步"
echo ""
echo " 守岗: M78 verbatim · EXT-3-5 不假装"
echo " DNA:  #SYNC-PACK-v1.0-2026-05-18"
echo "================================================================"
