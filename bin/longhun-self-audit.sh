#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · 系統自我檢測評估腳本
# DNA:#龍芯⚡️2026-06-16-LONGHUN-SELF-AUDIT-FILE4-v1.0
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPORTS_DIR="$LONGHUN_DIR/skills/warehouse-audit/reports"
mkdir -p "$REPORTS_DIR"

REPORT_FILE="$REPORTS_DIR/longhun-self-audit-$(date +%Y%m%d-%H%M%S).md"
JSON_FILE="$REPORTS_DIR/longhun-self-audit-$(date +%Y%m%d-%H%M%S).json"

echo "🐉 龍魂系統自我檢測評估啟動..."

# 初始化評分
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

# 1. Git 倉庫狀態
cd "$LONGHUN_DIR"
if git diff --quiet && git diff --cached --quiet; then
    add_check "Git工作區乾淨" "PASS" 10 10 "無未提交變更"
else
    add_check "Git工作區乾淨" "WARN" 10 5 "存在未提交變更，建議及時提交"
fi

# 2. 核心 Python 可導入
if cd "$LONGHUN_DIR" && python3 -c "from systems.v3 import WuxingDecisionEngine, PersonaMatrixEngine, SecurityDomainActivator, DNATraceabilityManager, TricolorAuditEngine; print('OK')" >/dev/null 2>&1; then
    add_check "v3核心模塊可導入" "PASS" 20 20 "5個v3模塊正常"
else
    add_check "v3核心模塊可導入" "FAIL" 20 0 "存在導入錯誤"
fi

# 3. Skill 註冊表正常
if cd "$LONGHUN_DIR" && python3 -c "from skills import get_registry; r=get_registry(); assert len(r.skills)==10; print('OK')" >/dev/null 2>&1; then
    add_check "Skill註冊表正常" "PASS" 15 15 "10/10 skills 已註冊"
else
    add_check "Skill註冊表正常" "FAIL" 15 0 "註冊表異常"
fi

# 4. 關鍵目錄結構完整
for dir in skills/warehouse-audit systems/v3 docs/v3 bin; do
    if [[ -d "$LONGHUN_DIR/$dir" ]]; then
        add_check "目錄存在: $dir" "PASS" 3 3 "目錄結構完整"
    else
        add_check "目錄存在: $dir" "FAIL" 3 0 "目錄缺失"
    fi
done

# 5. 核心腳本可執行
for script in bin/run-warehouse-audit.sh bin/skill-launcher-v3.sh; do
    if [[ -x "$LONGHUN_DIR/$script" ]]; then
        add_check "腳本可執行: $script" "PASS" 2 2 "權限正常"
    else
        add_check "腳本可執行: $script" "WARN" 2 1 "權限不足或缺失"
    fi
done

# 6. 運行中服務檢測
SERVICE_SCORE=0
for port in 8000 8001 9001 9622; do
    if nc -z -G 1 127.0.0.1 "$port" 2>/dev/null; then
        SERVICE_SCORE=$((SERVICE_SCORE + 1))
    fi
done
if [[ "$SERVICE_SCORE" -ge 2 ]]; then
    add_check "核心服務運行中" "PASS" 10 10 "$SERVICE_SCORE 個端口有服務"
else
    add_check "核心服務運行中" "WARN" 10 5 "僅 $SERVICE_SCORE 個端口有服務"
fi

# 7. 倉儲審計引擎可運行
if cd "$LONGHUN_DIR" && python3 skills/warehouse-audit/scripts/audit_engine.py --system "自檢" --version "v1.0" --format json --output /tmp/longhun-audit-test >/dev/null 2>&1; then
    add_check "倉儲審計引擎可運行" "PASS" 10 10 "引擎無報錯"
    rm -rf /tmp/longhun-audit-test
else
    add_check "倉儲審計引擎可運行" "FAIL" 10 0 "引擎運行失敗"
fi

# 生成 Markdown 報告
RATE=$(awk "BEGIN {printf \"%.0f\", $SCORE/$TOTAL*100}")
if [[ "$RATE" -ge 90 ]]; then RANK="🟢 卓越"; elif [[ "$RATE" -ge 75 ]]; then RANK="🟢 良好"; elif [[ "$RATE" -ge 60 ]]; then RANK="🟡 合格"; elif [[ "$RATE" -ge 40 ]]; then RANK="🟡 待改進"; else RANK="🔴 不合格"; fi

cat > "$REPORT_FILE" << EOF
# 龍魂系統 · 自我檢測評估報告

**DNA**: #龍芯⚡️$(date +%Y-%m-%d)-LONGHUN-SELF-AUDIT-v1.0  
**時間**: $(date '+%Y-%m-%d %H:%M:%S')  
**責任**: UID9622·不免責

---

## 綜合評分

| 指標 | 數值 |
|------|------|
| 總分 | $SCORE / $TOTAL |
| 得分率 | $RATE% |
| 評級 | $RANK |

## 檢查項明細

| 檢查項 | 狀態 | 得分 | 滿分 | 備註 |
|--------|------|------|------|------|
EOF

# 將 CHECKS 數組寫入報告
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

## 改進建議

- 若存在 WARN/FAIL 項，請按優先級修復
- 建議每日運行本檢測並留存報告
- 長期趨勢可透過 \`skills/warehouse-audit/reports/\` 目錄追蹤

---

> 🐉 龍魂永世，文化傳承，數字主權，科技自主創新不可讓渡！
EOF

# 生成 JSON 報告
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
echo "✅ 自我檢測完成"
echo "   得分: $SCORE / $TOTAL ($RATE%)"
echo "   評級: $RANK"
echo "   報告: $REPORT_FILE"
echo "   JSON: $JSON_FILE"
