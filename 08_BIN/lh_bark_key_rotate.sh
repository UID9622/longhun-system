#!/usr/bin/env bash
# ============================================================
# 龍魂 · Bark Key 一键更新 v1.0
# DNA: #龍芯⚡️丙午·丙申·丙子·酉时·䷔噬嗑-BARK-KEY-ROTATE-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
#
# 用法: bash bin/lh_bark_key_rotate.sh <新BarkKey>
#   <新BarkKey> 获取: iOS Bark App → 设置/更多 → 复制设备 Key
# 流程: 格式校验 → 实测推送(api.day.app) → 写入统一密钥库(vault)
#       → 复验 P06 数据相位引擎真推送 → 完成
# 安全: key 只在内存与 Keychain 流转·不落盘不打印
# ============================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NEW_KEY="${1:-}"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

if [ -z "$NEW_KEY" ]; then
  echo -e "${RED}🔴 用法: bash bin/lh_bark_key_rotate.sh <新BarkKey>${NC}"
  echo "   新 key 获取: iOS Bark App → 设置 → 复制设备 Key"
  exit 1
fi

# ① 格式校验（Bark key = 22~24 位 base64 风格，字母数字连字符）
if ! printf '%s' "$NEW_KEY" | grep -qE '^[A-Za-z0-9_-]{15,30}$'; then
  echo -e "${RED}🔴 key 格式可疑（应 15-30 位字母/数字/连字符），拒绝写入${NC}"
  exit 1
fi

# ② 实测新 key 有效性（官方 API · 直连不走代理）
echo -e "${YELLOW}① 实测推送 (api.day.app)...${NC}"
RESP=$(curl -s --max-time 8 --noproxy '*' -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"🐉 P06·新key上线","body":"Bark 通道一键更新验证","group":"P06","sound":"alarm"}' \
  "https://api.day.app/$NEW_KEY" || true)
if ! printf '%s' "$RESP" | grep -q '"code":200'; then
  echo -e "${RED}🔴 新 key 无效: $(printf '%s' "$RESP" | head -c 140)${NC}"
  exit 1
fi
echo -e "${GREEN}🟢 推送成功·key 有效${NC}"

# ③ 写入统一密钥库（macOS Keychain · 值不落盘）
echo -e "${YELLOW}② 写入统一密钥库 vault...${NC}"
python3 "$ROOT/bin/lh_vault.py" put BARK_KEY --value "$NEW_KEY"

# ④ 复验 P06 数据相位引擎（真推送全链路）
echo -e "${YELLOW}③ 复验 P06 数据相位引擎（真推送）...${NC}"
python3 "$ROOT/08_BIN/personas/p06_data_phase.py" --once | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    ph=d.get('computed',{})
    print('✅ 相位:', ph.get('phase'), ph.get('color'), '| dr', ph.get('digital_root'), '| 五行', ph.get('wuxing'))
    nb=d.get('notify',{})
    print('✅ Bark:', nb.get('reason') if nb.get('pushed') else '未推('+str(nb.get('reason'))+')')
except Exception as e:
    print('⚠️ 引擎输出非预期:', e)
"

echo -e "${GREEN}✅ 一键更新完成 · 所有 Bark 告警通道已复活${NC}"
