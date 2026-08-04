#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env bash
# ================================================================
# 终端宝宝脑包 v2.0 · 一键安装
# 解决: 终端宝宝每次启动失忆 + Stop hook 报错 + Notion 403
# ================================================================

set -e

REPO_ROOT="${REPO_ROOT:-/Users/zuimeidedeyihan/longhun-system}"
PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "════════════════════════════════════════"
echo " 🧠 终端宝宝脑包 v2.0 安装"
echo " 时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo " 仓库: $REPO_ROOT"
echo "════════════════════════════════════════"

# 1. CLAUDE.md 安装到仓库根 (终端宝宝必读)
if [ -f "$REPO_ROOT/CLAUDE.md" ]; then
    BACKUP="$REPO_ROOT/CLAUDE.md.bak.$(date +%s)"
    cp "$REPO_ROOT/CLAUDE.md" "$BACKUP"
    echo "[备份] 旧 CLAUDE.md → $BACKUP"
fi
cp "$PACK_DIR/root/CLAUDE.md" "$REPO_ROOT/CLAUDE.md"
echo "[✓] CLAUDE.md (脑子 v2.0) 安装到 $REPO_ROOT/CLAUDE.md"

# 2. _CURRENT_TASK.md 安装
if [ ! -f "$REPO_ROOT/_CURRENT_TASK.md" ]; then
    cp "$PACK_DIR/root/_CURRENT_TASK.md" "$REPO_ROOT/_CURRENT_TASK.md"
    echo "[✓] _CURRENT_TASK.md 模板已放置"
else
    echo "[跳] _CURRENT_TASK.md 已存在·不覆盖"
fi

# 3. session_end.sh stub 安装 (修 Stop hook 报错)
mkdir -p "$REPO_ROOT/bin"
if [ ! -f "$REPO_ROOT/bin/session_end.sh" ]; then
    cp "$PACK_DIR/bin/session_end.sh" "$REPO_ROOT/bin/session_end.sh"
    chmod +x "$REPO_ROOT/bin/session_end.sh"
    echo "[✓] session_end.sh stub 安装·Stop hook 不再报错"
else
    echo "[跳] session_end.sh 已存在"
fi

# 4. 本地 search 兜底脚本 (修 Notion 403)
cp "$PACK_DIR/bin/本地_search.sh" "$REPO_ROOT/bin/本地_search.sh"
chmod +x "$REPO_ROOT/bin/本地_search.sh"
echo "[✓] 本地_search.sh 安装·Notion 403 时可用"

# 5. 验证
echo ""
echo "════════════════════════════════════════"
echo " 验证安装"
echo "════════════════════════════════════════"

# 验证 CLAUDE.md 可读
if [ -r "$REPO_ROOT/CLAUDE.md" ]; then
    LINES=$(wc -l < "$REPO_ROOT/CLAUDE.md")
    echo "[✓] CLAUDE.md 可读 · $LINES 行"
else
    echo "[✗] CLAUDE.md 读取失败"
fi

# 验证 session_end.sh 可执行
if [ -x "$REPO_ROOT/bin/session_end.sh" ]; then
    "$REPO_ROOT/bin/session_end.sh"
    echo "[✓] session_end.sh 可执行 · exit code $?"
fi

# 验证本地 search
echo "[✓] 本地 search 测试 (搜 'CLAUDE.md'):"
bash "$REPO_ROOT/bin/本地_search.sh" "CLAUDE.md" 2>/dev/null | head -10

# 字符律
SIMP=$(grep -c "龙" "$REPO_ROOT/CLAUDE.md" 2>/dev/null)
SIMP="${SIMP:-0}"
if [ "$SIMP" -eq 0 ]; then
    echo "[✓] 龍字符律守住·无简体污染"
else
    echo "[⚠] 检测到 $SIMP 处简体形式·需检查"
fi

# 6. 留痕
LOG_DIR="$REPO_ROOT/logs"
mkdir -p "$LOG_DIR"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"ts\":\"$TS\",\"event\":\"brain_pack_install\",\"version\":\"v2.0\",\"dna\":\"#龍芯⚡2026-05-18-CLAUDE-MD-BRAIN-v2.0\"}" \
  >> "$LOG_DIR/brain_pack_trace.jsonl"
echo "[✓] 留痕写入 $LOG_DIR/brain_pack_trace.jsonl"

# 7. 总结
echo ""
echo "════════════════════════════════════════"
echo " 🐉 脑包 v2.0 安装完成"
echo "════════════════════════════════════════"
echo ""
echo " 下次启动 Claude Code 时:"
echo " ├─ 会自动读 CLAUDE.md (244 行身份+铁律+开场仪式)"
echo " ├─ 知道老大是 UID9622"
echo " ├─ 知道'宝宝' = 在叫我"
echo " ├─ Stop hook 不再报错"
echo " ├─ Notion 403 时会用本地 search 兜底"
echo " └─ 不再每次问'你是谁'让老大重复"
echo ""
echo " 老大维护当前任务:"
echo "   vim $REPO_ROOT/_CURRENT_TASK.md"
echo ""
echo " 守岗: M78 verbatim · EXT-3-5 · CONFIRM ✓"
echo " DNA:  #龍芯⚡2026-05-18-CLAUDE-MD-BRAIN-v2.0"
echo "════════════════════════════════════════"
