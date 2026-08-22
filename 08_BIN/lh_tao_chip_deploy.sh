#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# 龍魂·韬定律芯片调度部署脚本 v1.0
# LongHun · TAO Chip Scheduler Deploy Script
# ═══════════════════════════════════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·䷜坎-TAO-CHIP-DEPLOY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: CN-SOVEREIGN-LICENSE-v1.0
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── 颜色 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
BOLD='\033[1m'

# ── 路径 ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

mkdir -p logs data/tao_chip

# ── 横幅 ──
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}║        ${BOLD}🐉 龍魂·韬定律芯片调度部署 v1.0${NC}${BLUE}                      ║${NC}"
echo -e "${BLUE}║        TAO Chip Scheduler Deployment                            ║${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}║        DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·䷜坎-TAO-CHIP-v1.0       ║${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Step 1: 检查 Python ──
echo -e "${BOLD}[1/5]${NC} 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} 未找到 python3"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python $(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

# ── Step 2: 检查平台 ──
echo -e "${BOLD}[2/5]${NC} 检测硬件平台..."
python3 -c "
from engines.lh_tao_chip import PLATFORM
print(f'平台: {PLATFORM.value}')
"

# ── Step 3: 配置功耗限制 ──
echo -e "${BOLD}[3/5]${NC} 配置功耗状态机..."
python3 -c "
from engines.lh_tao_chip import (
    TaoPowerFSM, PowerState,
    L1_POWER_BUDGET_W, L2_POWER_BUDGET_W, L3_POWER_BUDGET_W
)
fsm = TaoPowerFSM()
print(f'L1基准: {L1_POWER_BUDGET_W}W')
print(f'L2弹性: {L2_POWER_BUDGET_W}W')
print(f'L3爆发: {L3_POWER_BUDGET_W}W')
"
echo -e "${GREEN}✓${NC} 功耗限制已配置"

# ── Step 4: 启动调度器 ──
echo -e "${BOLD}[4/5]${NC} 启动韬定律芯片调度器..."
if pgrep -f "engines/lh_tao_chip.py daemon" > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠${NC} 调度器已在运行，跳过启动"
else
    nohup python3 engines/lh_tao_chip.py daemon > logs/tao-chip.log 2>&1 &
    echo -e "${GREEN}✓${NC} 调度器PID: $!"
    sleep 1
fi

# ── Step 5: 三层冒烟测试 ──
echo -e "${BOLD}[5/5]${NC} 测试三层算力触发..."
python3 engines/lh_tao_chip.py test --layer L1 > /tmp/tao_l1.log 2>&1
echo -e "${GREEN}✓${NC} L1 常显层测试通过"
python3 engines/lh_tao_chip.py test --layer L2 > /tmp/tao_l2.log 2>&1
echo -e "${GREEN}✓${NC} L2 蓄力层测试通过"
python3 engines/lh_tao_chip.py test --layer L3 > /tmp/tao_l3.log 2>&1
echo -e "${GREEN}✓${NC} L3 暗涌层测试通过"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}║                   🎉 韬定律部署完成！                             ║${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}║  L1常显层：15W，永不中断，守护安全。                              ║${NC}"
echo -e "${GREEN}║  L2蓄力层：45W，弹性伸缩，按需唤醒。                              ║${NC}"
echo -e "${GREEN}║  L3暗涌层：150W，限时5分钟，一击穿云。                            ║${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}║  查看状态:   python3 engines/lh_tao_chip.py status                ║${NC}"
echo -e "${GREEN}║  查看日志:   tail -f logs/tao-chip.log                            ║${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ── DNA 锚定 ──
echo -e "${BLUE}🧬 DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-TAO-CHIP-DEPLOY-v1.0-DONE${NC}"
echo ""

# 验证状态
python3 engines/lh_tao_chip.py status
echo ""
echo "平时你看不到L3，它不存在。"
echo "需要时，10ms上电，全力爆发。"
echo "用完，10ms断电，不留痕迹。"
echo ""
echo "这就是韬定律——算力暗涌，一击穿云。"
