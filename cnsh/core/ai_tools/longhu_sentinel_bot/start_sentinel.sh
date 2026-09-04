#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1302-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: start_sentinel.sh | 标记时间: 2026-06-03T07:46:12+0800

# 🐉 龍魂 Telegram 哨兵机器人启动脚本
# DNA: #龍芯⚇️2026-05-30-SENTINEL-START-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# UID9622 · 诸葛鑫 · 龍芯北辰

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SENTINEL_HOME="${SCRIPT_DIR}"
CONFIG_DIR="$HOME/.龍魂_config"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════
# 函数定义
# ═══════════════════════════════════════════════════════════

print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🐉 龍魂 Telegram 哨兵机器人启动                             ║${NC}"
    echo -e "${BLUE}║  DNA: #龍芯⚇️2026-05-30-SENTINEL-BOT-v1.0                  ║${NC}"
    echo -e "${BLUE}║  Owner: UID9622 · 龍芯北辰 · 诸葛鑫                         ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ═══════════════════════════════════════════════════════════
# 前置检查
# ═══════════════════════════════════════════════════════════

print_header

print_section "1️⃣  前置检查"

# 检查Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 未安装"
    exit 1
fi
print_success "Python3 已安装: $(python3 --version)"

# 检查必要的库
echo "检查Python库..."
python3 -c "import sqlite3" 2>/dev/null && print_success "sqlite3 已安装" || print_warning "sqlite3 未安装"

# 创建配置目录
mkdir -p "$CONFIG_DIR"
print_success "配置目录就绪: $CONFIG_DIR"

# ═══════════════════════════════════════════════════════════
# Token 设置
# ═══════════════════════════════════════════════════════════

print_section "2️⃣  Token 配置"

# 从环境变量或文件获取Token
TOKEN="${TELEGRAM_BOT_TOKEN}"

if [ -z "$TOKEN" ]; then
    print_warning "未从环境变量获取Token"

    # 尝试从文件读取
    if [ -f "$CONFIG_DIR/telegram_token.json" ]; then
        TOKEN=$(python3 -c "import json; print(json.load(open('$CONFIG_DIR/telegram_token.json')).get('token', ''))" 2>/dev/null)
        if [ -n "$TOKEN" ]; then
            print_success "从文件加载Token"
        fi
    fi
fi

if [ -z "$TOKEN" ]; then
    print_error "Token未找到！"
    echo ""
    echo "请按以下步骤获取Token："
    echo "1. 打开 Telegram 应用"
    echo "2. 搜索 '@BotFather'"
    echo "3. 发送 '/newbot'"
    echo "4. 按提示创建机器人"
    echo "5. 复制 Token（格式: 数字:字母-数字组合）"
    echo ""
    echo "然后设置环境变量："
    echo "  export TELEGRAM_BOT_TOKEN='你的Token'"
    echo ""
    exit 1
fi

# 验证Token格式
if [[ $TOKEN =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
    print_success "Token格式有效: ${TOKEN:0:20}..."
else
    print_error "Token格式无效"
    exit 1
fi

# 保存Token到安全位置
echo "保存Token到本地..."
python3 << PYEOF
import json
from pathlib import Path

config_dir = Path.home() / ".龍魂_config"
config_dir.mkdir(parents=True, exist_ok=True)

token_file = config_dir / "telegram_token.json"
token_data = {
    "token": "$TOKEN",
    "bot_name": "LongHun_Sentinel_Bot",
    "saved_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "version": "1.0"
}

with open(token_file, "w") as f:
    json.dump(token_data, f, indent=2)

print("✅ Token已安全保存")
PYEOF

# ═══════════════════════════════════════════════════════════
# 初始化数据库
# ═══════════════════════════════════════════════════════════

print_section "3️⃣  初始化审计数据库"

python3 << PYEOF
from pathlib import Path
import sys
sys.path.insert(0, "$SENTINEL_HOME")

from sentinel_bot import AuditDatabase

db_path = Path.home() / ".龍魂_config" / "sentinel_audit.db"
db = AuditDatabase(db_path)

print(f"✅ 审计数据库已初始化: {db_path}")
PYEOF

# ═══════════════════════════════════════════════════════════
# 启动哨兵机器人
# ═══════════════════════════════════════════════════════════

print_section "4️⃣  启动哨兵机器人"

export TELEGRAM_BOT_TOKEN="$TOKEN"

# 显示机器人信息
python3 "$SENTINEL_HOME/sentinel_bot.py" --init

# ═══════════════════════════════════════════════════════════
# 启动说明
# ═══════════════════════════════════════════════════════════

print_section "5️⃣  启动完成！"

echo ""
echo -e "${BLUE}📱 Telegram 机器人${NC}"
echo "   Bot: t.me/LongHun_Sentinel_Bot"
echo ""
echo -e "${BLUE}🔐 系统信息${NC}"
echo "   所有者: UID9622 · 龍芯北辰 · 诸葛鑫"
echo "   DNA: #龍芯⚇️2026-05-30-SENTINEL-BOT-v1.0"
echo "   GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
echo ""
echo -e "${BLUE}💾 数据存储${NC}"
echo "   审计数据库: $CONFIG_DIR/sentinel_audit.db"
echo "   Token: $CONFIG_DIR/telegram_token.json"
echo "   日志: $CONFIG_DIR/sentinel_bot.log"
echo ""
echo -e "${BLUE}📖 快速命令${NC}"
echo "   查看状态:   python3 $SENTINEL_HOME/sentinel_bot.py --status"
echo "   审计报告:   python3 $SENTINEL_HOME/sentinel_bot.py --audit-report"
echo "   Token状态:  python3 $SENTINEL_HOME/token_manager.py --status"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🐉 龍魂哨兵已就绪！${NC}"
echo -e "${GREEN}打开 Telegram，向 t.me/LongHun_Sentinel_Bot 发送 /start${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════
# 可选：启动后台监听模式
# ═══════════════════════════════════════════════════════════

echo "启动选项:"
echo "1) 查看审计报告"
echo "2) 显示Token状态"
echo "3) 在终端查看日志"
echo ""
read -p "选择 (按Enter跳过): " choice

case $choice in
    1)
        python3 "$SENTINEL_HOME/sentinel_bot.py" --audit-report
        ;;
    2)
        python3 "$SENTINEL_HOME/token_manager.py" --status
        ;;
    3)
        tail -f "$CONFIG_DIR/sentinel_bot.log"
        ;;
    *)
        echo "已跳过"
        ;;
esac
