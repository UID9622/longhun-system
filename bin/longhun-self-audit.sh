#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · 系统自我检测评估脚本
# DNA:#龍芯⚡️2026-06-16-LONGHUN-SELF-AUDIT-FILE4-FILE1-v1.0-1
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPORTS_DIR="$LONGHUN_DIR/skills/warehouse-audit/reports"
mkdir -p "$REPORTS_DIR"

REPORT_FILE="$REPORTS_DIR/longhun-self-audit-$(date +%Y%m%d-%H%M%S).md"
JSON_FILE="$REPORTS_DIR/longhun-self-audit-$(date +%Y%m%d-%H%M%S).json"

echo "🐉 龍魂系统自我检测评估启动..."

# 初始化评分
SCORE=0
TOTAL=0
CHECKS=()

add_check() {
    local name="$1"
    local status="$2"   # PASS / WARN / FAIL
    local max_score="$3"
    local actual_score="$4"
    local note="$5"
    CHECKS+=("{\"name\":\"$name\",\"status\":\"$status\",\"max_score\":$max_score,\"score\":$actual_score,\"note\":\"$note\"}")
    SCORE=$((SCORE + actual_score))
    TOTAL=$((TOTAL + max_score))
}

# 1. Git 仓库状态
cd "$LONGHUN_DIR"
if git diff --quiet && git diff --cached --quiet; then
    add_check "Git工作区干净" "PASS" 10 10 "无未提交变更"
else
    add_check "Git工作区干净" "WARN" 10 5 "存在未提交变更，建议及时提交"
fi

# 2. 核心 Python 可导入
if cd "$LONGHUN_DIR" && python3 -c "from systems.v3 import WuxingDecisionEngine, PersonaMatrixEngine, SecurityDomainActivator, DNATraceabilityManager, TricolorAuditEngine; print('OK')" >/dev/null 2>&1; then
    add_check "v3核心模块可导入" "PASS" 20 20 "5个v3模块正常"
else
    add_check "v3核心模块可导入" "FAIL" 20 0 "存在导入错误"
fi

# 3. Skill 注册表正常
if cd "$LONGHUN_DIR" && python3 -c "from skills import get_registry; r=get_registry(); assert len(r.skills)==10; print('OK')" >/dev/null 2>&1; then
    add_check "Skill注册表正常" "PASS" 15 15 "10/10 skills 已注册"
else
    add_check "Skill注册表正常" "FAIL" 15 0 "注册表异常"
fi

# 4. 关键目录结构完整
for dir in skills/warehouse-audit systems/v3 docs/v3 bin; do
    if [[ -d "$LONGHUN_DIR/$dir" ]]; then
        add_check "目录存在: $dir" "PASS" 3 3 "目录结构完整"
    else
        add_check "目录存在: $dir" "FAIL" 3 0 "目录缺失"
    fi
done

# 5. 核心脚本可执行
for script in bin/run-warehouse-audit.sh bin/skill-launcher-v3.sh; do
    if [[ -x "$LONGHUN_DIR/$script" ]]; then
        add_check "脚本可执行: $script" "PASS" 2 2 "权限正常"
    else
        add_check "脚本可执行: $script" "WARN" 2 1 "权限不足或缺失"
    fi
done

# 6. 运行中服务检测
SERVICE_SCORE=0
for port in 8000 8001 9001 9622; do
    if nc -z -G 1 127.0.0.1 "$port" 2>/dev/null; then
        SERVICE_SCORE=$((SERVICE_SCORE + 1))
    fi
done
if [[ "$SERVICE_SCORE" -ge 2 ]]; then
    add_check "核心服务运行中" "PASS" 10 10 "$SERVICE_SCORE 个端口有服务"
else
    add_check "核心服务运行中" "WARN" 10 5 "仅 $SERVICE_SCORE 个端口有服务"
fi

# 7. 仓储审计引擎可运行
if cd "$LONGHUN_DIR" && python3 skills/warehouse-audit/scripts/audit_engine.py --system "自检" --version "v1.0" --format json --output /tmp/longhun-audit-test >/dev/null 2>&1; then
    add_check "仓储审计引擎可运行" "PASS" 10 10 "引擎无报错"
    rm -rf /tmp/longhun-audit-test
else
    add_check "仓储审计引擎可运行" "FAIL" 10 0 "引擎运行失败"
fi

# 8. 全局索引服务状态
INDEX_PID=$(launchctl list 2>/dev/null | awk '/com.longhun.global-index/ {print $1}')
if [[ -n "$INDEX_PID" && "$INDEX_PID" != "-" ]]; then
    INDEX_COUNT=$(python3 - "$HOME/.longhun/global_index/global_index.db" <<'PY'
import sqlite3, sys
conn = sqlite3.connect(sys.argv[1])
print(conn.execute("SELECT COUNT(*) FROM files WHERE accessible=1").fetchone()[0])
PY
)
    add_check "全局索引服务运行中" "PASS" 10 10 "PID $INDEX_PID | 索引 $INDEX_COUNT 个文件"
else
    add_check "全局索引服务运行中" "WARN" 10 0 "服务未运行"
fi

# 9. 知识图谱公开接口服务
KG_API_PID=$(launchctl list 2>/dev/null | awk '/com.longhun.kg-api/ {print $1}')
if [[ -n "$KG_API_PID" && "$KG_API_PID" != "-" ]]; then
    if curl -s --max-time 3 http://127.0.0.1:8088/api/health >/dev/null 2>&1; then
        add_check "知识图谱公开接口" "PASS" 10 10 "PID $KG_API_PID | http://127.0.0.1:8088"
    else
        add_check "知识图谱公开接口" "WARN" 10 5 "服务运行但接口未响应"
    fi
else
    add_check "知识图谱公开接口" "WARN" 10 0 "服务未运行"
fi

# 10. 主干自我迭代检查
SELF_UPDATE_CHECK=$(~/.龍魂/bin/lh-self-update 2>&1 || true)
if echo "$SELF_UPDATE_CHECK" | grep -q "主干无变化"; then
    add_check "主干自我迭代检查" "PASS" 10 10 "raw.md 无变化，向量库已是最新"
elif echo "$SELF_UPDATE_CHECK" | grep -q "主干自我迭代完成"; then
    add_check "主干自我迭代检查" "PASS" 10 10 "检测到变化并已自动重建向量库"
else
    add_check "主干自我迭代检查" "WARN" 10 5 "自我更新检查异常，需排查 lh-self-update"
fi

# 生成 Markdown 报告
RATE=$(awk "BEGIN {printf \"%.0f\", $SCORE/$TOTAL*100}")
if [[ "$RATE" -ge 90 ]]; then RANK="🟢 卓越"; elif [[ "$RATE" -ge 75 ]]; then RANK="🟢 良好"; elif [[ "$RATE" -ge 60 ]]; then RANK="🟡 合格"; elif [[ "$RATE" -ge 40 ]]; then RANK="🟡 待改进"; else RANK="🔴 不合格"; fi

cat > "$REPORT_FILE" << EOF
# 龍魂系统 · 自我检测评估报告

**DNA**: #龍芯⚡️$(date +%Y-%m-%d)-LONGHUN-SELF-AUDIT-v1.0  
**时间**: $(date '+%Y-%m-%d %H:%M:%S')  
**责任**: UID9622·不免责

---

## 综合评分

| 指标 | 数值 |
|------|------|
| 总分 | $SCORE / $TOTAL |
| 得分率 | $RATE% |
| 评级 | $RANK |

## 全局索引日报

EOF

DAILY_FILE="$HOME/.longhun/global_index/daily/$(date +%Y-%m-%d).md"
if [[ -f "$DAILY_FILE" ]]; then
    cat "$DAILY_FILE" >> "$REPORT_FILE"
else
    echo "未生成今日摘要，路径: $DAILY_FILE" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

## 检查项明细

| 检查项 | 状态 | 得分 | 满分 | 备注 |
|--------|------|------|------|------|
EOF

# 将 CHECKS 数组写入报告
for check in "${CHECKS[@]}"; do
    name=$(echo "$check" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['name'])")
    status=$(echo "$check" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['status'])")
    max_score=$(echo "$check" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['max_score'])")
    score=$(echo "$check" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['score'])")
    note=$(echo "$check" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['note'])")
    icon="🟢"; [[ "$status" == "WARN" ]] && icon="🟡"; [[ "$status" == "FAIL" ]] && icon="🔴"
    echo "| $name | $icon $status | $score | $max_score | $note |" >> "$REPORT_FILE"
done

cat >> "$REPORT_FILE" << EOF

## 改进建议

- 若存在 WARN/FAIL 项，请按优先级修复
- 建议每日运行本检测并留存报告
- 长期趋势可透过 \`skills/warehouse-audit/reports/\` 目录追踪

---

> 🐉 龍魂永世，文化传承，数字主权，科技自主创新不可让渡！
EOF

# 生成 JSON 报告
echo "{" > "$JSON_FILE"
echo "  \"dna\": \"#龍芯⚡️$(date +%Y-%m-%d)-LONGHUN-SELF-AUDIT-v1.0\"," >> "$JSON_FILE"
echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"," >> "$JSON_FILE"
echo "  \"score\": $SCORE," >> "$JSON_FILE"
echo "  \"total\": $TOTAL," >> "$JSON_FILE"
echo "  \"rate\": $RATE," >> "$JSON_FILE"
echo "  \"rank\": \"$RANK\"," >> "$JSON_FILE"
echo "  \"checks\": [" >> "$JSON_FILE"
first=true
for check in "${CHECKS[@]}"; do
    [[ "$first" == true ]] && first=false || echo "," >> "$JSON_FILE"
    echo -n "    $check" >> "$JSON_FILE"
done
echo "" >> "$JSON_FILE"
echo "  ]" >> "$JSON_FILE"
echo "}" >> "$JSON_FILE"

echo ""
echo "✅ 自我检测完成"
echo "   得分: $SCORE / $TOTAL ($RATE%)"
echo "   评级: $RANK"
echo "   报告: $REPORT_FILE"
echo "   JSON: $JSON_FILE"
