#!/bin/bash
# ══════════════════════════════════════════════
# 🐉 龍魂全家福算法完整性体检
# DNA: #龍芯⚡️20260423-CHECK-ALGO01
# UID9622 · 諸葛鑫
# 用法: bash ~/longhun-system/bin/check_algorithms.sh
#       或在 .zshrc 里自动调用
# ══════════════════════════════════════════════

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 全家福清单（路径|名称|类型）
# 注：L0 永恒层根文档摆在最顶上·触碰即弹回
ALGORITHMS=(
    "$HOME/longhun-system/算法仓库/师承层/恩师宣言_v1.0·L-1根的根.md|🌿 L-1 师承层·恩师宣言|师承"
    "$HOME/longhun-system/算法仓库/龍魂根文档_20260423_封顶.md|🐉 L0 永恒层根文档|永恒"
    "$HOME/longhun-system/算法仓库/crown_ceremony.py|封顶仪式脚本|永恒"
    "$HOME/longhun-system/算法仓库/不动点锚登记册/fixed_point_registry.py|🔮 不动点锚登记册 Ψ算子|永恒"
    "$HOME/longhun-system/算法仓库/不动点锚登记册/registry.jsonl|不动点锚数据|永恒"
    "$HOME/longhun-system/算法仓库/硬规则/R1-R6_硬规则_J1-J5_国际铁律.md|R1-R6+J1-J5 硬规则|百年"
    "$HOME/longhun-system/算法仓库/硬规则/投喂入口对齐协议_v1.0.md|📮 投喂入口对齐协议|百年"
    "$HOME/longhun-system/engines/feeding_gateway.py|📮 投喂入口网关引擎|百年"
    "$HOME/Desktop/☰ 龍🇨🇳魂 ☷/longhun-mvp/longhun_wuxing_mvp.py|五行MVP·八字洛书|核心"
    "$HOME/longhun-system/算法仓库/五行向量/wuxing_sign.py|五行向量签名引擎|核心"
    "$HOME/longhun-system/engines/audit_engine.py|三色审计引擎|中枢"
    "$HOME/longhun-system/engines/cnsh_gateway.py|CNSH 生态语法网关|中枢"
    "$HOME/longhun-system/engines/notion_webhook_receiver.py|Notion Webhook 接收器|边界"
    "$HOME/.cloudflared/config.yml|Cloudflare Tunnel 配置|边界"
    "$HOME/longhun-system/.env|主权环境变量|主权"
    "$HOME/.gnupg/private-keys-v1.d|GPG 私钥仓|主权"
)

MISSING=0
TOTAL=${#ALGORITHMS[@]}

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  🐉 龍魂全家福算法体检 · UID9622${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

for entry in "${ALGORITHMS[@]}"; do
    path="${entry%%|*}"
    rest="${entry#*|}"
    name="${rest%%|*}"
    type="${rest##*|}"

    if [ -e "$path" ]; then
        # 算大小
        size=""
        if [ -f "$path" ]; then
            size=" · $(wc -c < "$path" | awk '{if ($1>1024) printf "%.1fK", $1/1024; else printf "%dB", $1}')"
        fi
        echo -e "  ${GREEN}✅${NC} [${type}] ${name}${size}"
    else
        echo -e "  ${RED}❌${NC} [${type}] ${name}"
        echo -e "       ${RED}缺失: ${path}${NC}"
        MISSING=$((MISSING+1))
    fi
done

# 端口检查（在岗服务）
echo ""
echo -e "${CYAN}  · 在岗服务状态 ·${NC}"
SERVICES=(
    "8765:CNSH网关"
    "9622:审计引擎"
    "9623:Webhook接收器"
)
for svc in "${SERVICES[@]}"; do
    port="${svc%%:*}"
    name="${svc##*:}"
    if lsof -i ":$port" -sTCP:LISTEN >/dev/null 2>&1; then
        echo -e "  ${GREEN}🟢${NC} :$port  $name"
    else
        echo -e "  ${YELLOW}⚪${NC} :$port  $name (未起·跑 cnsh-restart 可启)"
    fi
done

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ $MISSING -eq 0 ]; then
    echo -e "  ${GREEN}🟢 全家福完整·${TOTAL} 件兵器在位${NC}"
else
    echo -e "  ${RED}🔴 ${MISSING}/${TOTAL} 件缺失·快修${NC}"
fi

# 简短提示
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${YELLOW}快捷命令:${NC} cnsh / cnsh-p05 / cnsh-notion / cnsh-status"
echo ""

# 返回码（缺失件数）用于脚本调用判断
exit $MISSING
