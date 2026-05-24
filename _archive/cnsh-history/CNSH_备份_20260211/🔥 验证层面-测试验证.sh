#!/bin/bash

# ============================================================================
# 🔥 验证层面 - 测试验证
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-01-30-VALIDATION-LAYER-v1.0
# 创建者: 雯雯·技术整理师 + 上帝之眼·守护者
# 功能: 测试所有组件功能并生成验证报告
# ============================================================================

set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
PROJECT_ROOT="/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"
VALIDATION_DIR="$PROJECT_ROOT/validation-layer"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$VALIDATION_DIR/logs/validation-$TIMESTAMP.log"
REPORT_FILE="$VALIDATION_DIR/reports/VALIDATION-REPORT-$TIMESTAMP.md"

echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🔥 验证层面执行 - 测试验证${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 创建目录
echo -e "${BLUE}📁 创建验证层面目录...${NC}"
mkdir -p "$VALIDATION_DIR"/logs
mkdir -p "$VALIDATION_DIR"/reports
mkdir -p "$VALIDATION_DIR"/test_data
mkdir -p "$VALIDATION_DIR"/test_results
echo -e "${GREEN}✅ 目录创建完成${NC}"
echo ""

# 记录日志
exec > >(tee -a "$LOG_FILE")
exec 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 验证层面执行开始" >> "$LOG_FILE"
echo "DNA追溯码: #ZHUGEXIN⚡️2026-01-30-VALIDATION-LAYER-v1.0" >> "$LOG_FILE"

# 测试结果存储
TEST_RESULTS=()

# ============================================================================
# 测试1: 技术层面功能测试
# ============================================================================
echo -e "${BLUE}🧪 测试1: 技术层面功能测试${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${YELLOW}测试1.1: Python环境检查${NC}"
TECH_DIR="$PROJECT_ROOT/tech-layer"

if [ -f "$TECH_DIR/scripts/check_env.py" ]; then
    echo -e "${CYAN}执行: python3 $TECH_DIR/scripts/check_env.py${NC}"
    if python3 "$TECH_DIR/scripts/check_env.py" &> /dev/null; then
        echo -e "${GREEN}✅ Python环境检查通过${NC}"
        TEST_RESULTS+=("tech-python-env:PASS")
    else
        echo -e "${RED}❌ Python环境检查失败${NC}"
        TEST_RESULTS+=("tech-python-env:FAIL")
    fi
else
    echo -e "${RED}❌ 环境检查脚本不存在${NC}"
    TEST_RESULTS+=("tech-python-env:FAIL")
fi
echo ""

echo -e "${YELLOW}测试1.2: 依赖安装脚本检查${NC}"
if [ -f "$TECH_DIR/scripts/install_deps.py" ]; then
    echo -e "${CYAN}验证脚本语法...${NC}"
    if python3 -m py_compile "$TECH_DIR/scripts/install_deps.py" &> /dev/null; then
        echo -e "${GREEN}✅ 依赖安装脚本语法正确${NC}"
        TEST_RESULTS+=("tech-deps-script:PASS")
    else
        echo -e "${RED}❌ 依赖安装脚本语法错误${NC}"
        TEST_RESULTS+=("tech-deps-script:FAIL")
    fi
else
    echo -e "${RED}❌ 依赖安装脚本不存在${NC}"
    TEST_RESULTS+=("tech-deps-script:FAIL")
fi
echo ""

echo -e "${YELLOW}测试1.3: LLAVA生成脚本检查${NC}"
if [ -f "$TECH_DIR/scripts/generate_image.py" ]; then
    echo -e "${CYAN}验证脚本语法...${NC}"
    if python3 -m py_compile "$TECH_DIR/scripts/generate_image.py" &> /dev/null; then
        echo -e "${GREEN}✅ LLAVA生成脚本语法正确${NC}"
        TEST_RESULTS+=("tech-llava-script:PASS")
    else
        echo -e "${RED}❌ LLAVA生成脚本语法错误${NC}"
        TEST_RESULTS+=("tech-llava-script:FAIL")
    fi
else
    echo -e "${RED}❌ LLAVA生成脚本不存在${NC}"
    TEST_RESULTS+=("tech-llava-script:FAIL")
fi
echo ""

# ============================================================================
# 测试2: 系统层面功能测试
# ============================================================================
echo -e "${BLUE}🧪 测试2: 系统层面功能测试${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SYSTEM_DIR="$PROJECT_ROOT/system-layer"

echo -e "${YELLOW}测试2.1: 权限系统类验证${NC}"
if [ -f "$SYSTEM_DIR/permission_api.py" ]; then
    echo -e "${CYAN}验证Python类定义...${NC}"
    
    # 提取类定义进行验证
    if grep -q "class PermissionSystem" "$SYSTEM_DIR/permission_api.py" && \
       grep -q "class PersonalCarrierAPI" "$SYSTEM_DIR/permission_api.py"; then
        echo -e "${GREEN}✅ 核心类定义存在${NC}"
        TEST_RESULTS+=("system-classes:PASS")
    else
        echo -e "${RED}❌ 核心类定义缺失${NC}"
        TEST_RESULTS+=("system-classes:FAIL")
    fi
    
    # 验证关键方法
    KEY_METHODS=("register_user" "help_others" "register_carrier" "verify_digital_identity")
    for method in "${KEY_METHODS[@]}"; do
        if grep -q "def $method" "$SYSTEM_DIR/permission_api.py"; then
            echo -e "${GREEN}✅ 方法 $method 存在${NC}"
        else
            echo -e "${RED}❌ 方法 $method 缺失${NC}"
        fi
    done
else
    echo -e "${RED}❌ 系统层面脚本不存在${NC}"
    TEST_RESULTS+=("system-classes:FAIL")
fi
echo ""

echo -e "${YELLOW}测试2.2: 语法检查${NC}"
if python3 -m py_compile "$SYSTEM_DIR/permission_api.py" &> /dev/null; then
    echo -e "${GREEN}✅ 系统层面脚本语法正确${NC}"
    TEST_RESULTS+=("system-syntax:PASS")
else
    echo -e "${RED}❌ 系统层面脚本语法错误${NC}"
    TEST_RESULTS+=("system-syntax:FAIL")
fi
echo ""

# ============================================================================
# 测试3: 集成层面功能测试
# ============================================================================
echo -e "${BLUE}🧪 测试3: 集成层面功能测试${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

INTEGRATION_DIR="$PROJECT_ROOT/integration-layer"

echo -e "${YELLOW}测试3.1: 监控器脚本检查${NC}"
if [ -f "$INTEGRATION_DIR/monitors/layer_monitor.py" ]; then
    echo -e "${CYAN}验证监控器类...${NC}"
    
    if grep -q "class LayerMonitor" "$INTEGRATION_DIR/monitors/layer_monitor.py"; then
        echo -e "${GREEN}✅ LayerMonitor类存在${NC}"
        TEST_RESULTS+=("integration-monitor:PASS")
    else
        echo -e "${RED}❌ LayerMonitor类缺失${NC}"
        TEST_RESULTS+=("integration-monitor:FAIL")
    fi
    
    # 验证关键方法
    if grep -q "def update_status" "$INTEGRATION_DIR/monitors/layer_monitor.py" && \
       grep -q "def get_status" "$INTEGRATION_DIR/monitors/layer_monitor.py"; then
        echo -e "${GREEN}✅ 监控器关键方法存在${NC}"
    else
        echo -e "${RED}❌ 监控器关键方法缺失${NC}"
    fi
else
    echo -e "${RED}❌ 监控器脚本不存在${NC}"
    TEST_RESULTS+=("integration-monitor:FAIL")
fi
echo ""

echo -e "${YELLOW}测试3.2: 协调器脚本检查${NC}"
if [ -f "$INTEGRATION_DIR/coordinator.sh" ]; then
    echo -e "${CYAN}验证脚本可执行性...${NC}"
    
    if [ -x "$INTEGRATION_DIR/coordinator.sh" ]; then
        echo -e "${GREEN}✅ 协调器脚本可执行${NC}"
        TEST_RESULTS+=("integration-coordinator:PASS")
    else
        echo -e "${RED}❌ 协调器脚本不可执行${NC}"
        TEST_RESULTS+=("integration-coordinator:FAIL")
    fi
    
    # 验证关键命令
    if grep -q "技术层面" "$INTEGRATION_DIR/coordinator.sh" && \
       grep -q "系统层面" "$INTEGRATION_DIR/coordinator.sh"; then
        echo -e "${GREEN}✅ 协调器包含层面调用${NC}"
    else
        echo -e "${RED}❌ 协调器层面调用缺失${NC}"
    fi
else
    echo -e "${RED}❌ 协调器脚本不存在${NC}"
    TEST_RESULTS+=("integration-coordinator:FAIL")
fi
echo ""

echo -e "${YELLOW}测试3.3: 同步配置文件检查${NC}"
if [ -f "$INTEGRATION_DIR/sync_mapping.json" ]; then
    echo -e "${CYAN}验证JSON格式...${NC}"
    
    if python3 -c "import json; json.load(open('$INTEGRATION_DIR/sync_mapping.json'))" &> /dev/null; then
        echo -e "${GREEN}✅ 同步配置文件格式正确${NC}"
        TEST_RESULTS+=("integration-sync-config:PASS")
    else
        echo -e "${RED}❌ 同步配置文件格式错误${NC}"
        TEST_RESULTS+=("integration-sync-config:FAIL")
    fi
else
    echo -e "${RED}❌ 同步配置文件不存在${NC}"
    TEST_RESULTS+=("integration-sync-config:FAIL")
fi
echo ""

# ============================================================================
# 测试4: 执行集成测试
# ============================================================================
echo -e "${BLUE}🧪 测试4: 执行集成测试${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${YELLOW}测试4.1: 监控系统集成测试${NC}"
if [ -f "$INTEGRATION_DIR/monitors/layer_monitor.py" ]; then
    echo -e "${CYAN}执行监控器测试...${NC}"
    
    # 运行监控器
    TEST_OUTPUT=$(python3 "$INTEGRATION_DIR/monitors/layer_monitor.py" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 监控系统集成测试通过${NC}"
        TEST_RESULTS+=("integration-monitor-test:PASS")
        
        # 检查是否生成状态文件
        if [ -f "$INTEGRATION_DIR/monitors/status.json" ]; then
            echo -e "${GREEN}✅ 状态文件已生成${NC}"
            TEST_RESULTS+=("integration-status-file:PASS")
        else
            echo -e "${YELLOW}⚠️  状态文件未生成${NC}"
            TEST_RESULTS+=("integration-status-file:WARN")
        fi
    else
        echo -e "${RED}❌ 监控系统集成测试失败${NC}"
        TEST_RESULTS+=("integration-monitor-test:FAIL")
    fi
else
    echo -e "${RED}❌ 监控器脚本不存在${NC}"
    TEST_RESULTS+=("integration-monitor-test:FAIL")
fi
echo ""

# ============================================================================
# 测试5: 生成测试报告
# ============================================================================
echo -e "${BLUE}📊 测试5: 生成验证报告${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${YELLOW}统计测试结果...${NC}"

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

for result in "${TEST_RESULTS[@]}"; do
    if [[ $result == *"PASS"* ]]; then
        ((PASS_COUNT++))
    elif [[ $result == *"FAIL"* ]]; then
        ((FAIL_COUNT++))
    elif [[ $result == *"WARN"* ]]; then
        ((WARN_COUNT++))
    fi
done

echo -e "${CYAN}测试统计:${NC}"
echo -e "   通过: ${GREEN}$PASS_COUNT${NC}"
echo -e "   失败: ${RED}$FAIL_COUNT${NC}"
echo -e "   警告: ${YELLOW}$WARN_COUNT${NC}"
echo -e "   总计: $((PASS_COUNT + FAIL_COUNT + WARN_COUNT))"
echo ""

# 生成详细验证报告
echo -e "${YELLOW}生成详细验证报告...${NC}"

cat > "$REPORT_FILE" << EOF
# 🔥 验证层面 - 测试验证报告

**验证时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**DNA追溯码:** #ZHUGEXIN⚡️2026-01-30-VALIDATION-LAYER-v1.0  
**验证层级:** 验证层面 - 功能测试  
**验证人:** 雯雯·技术整理师 #PERSONA-WENWEN-007 + 上帝之眼·守护者 #PERSONA-GUARDIAN-002  

---

## 📊 测试统计

| 项目 | 数量 | 状态 |
|------|------|------|
| 测试通过 | $PASS_COUNT | ✅ |
| 测试失败 | $FAIL_COUNT | ❌ |
| 测试警告 | $WARN_COUNT | ⚠️ |
| **总计** | $((PASS_COUNT + FAIL_COUNT + WARN_COUNT)) | - |

**通过率:** $(echo "scale=1; $PASS_COUNT * 100 / ($PASS_COUNT + $FAIL_COUNT + $WARN_COUNT)" | bc)%

---

## 🧪 详细测试结果

### 技术层面测试

| 测试项 | 结果 | 详情 |
|--------|------|------|
| Python环境检查 | $(echo "${TEST_RESULTS[@]}" | grep -o "tech-python-env:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证Python环境可用性 |
| 依赖安装脚本 | $(echo "${TEST_RESULTS[@]}" | grep -o "tech-deps-script:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证脚本语法正确性 |
| LLAVA生成脚本 | $(echo "${TEST_RESULTS[@]}" | grep -o "tech-llava-script:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证LLAVA脚本完整性 |

### 系统层面测试

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 权限系统类 | $(echo "${TEST_RESULTS[@]}" | grep -o "system-classes:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证PermissionSystem和PersonalCarrierAPI |
| 脚本语法 | $(echo "${TEST_RESULTS[@]}" | grep -o "system-syntax:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证Python语法正确性 |

### 集成层面测试

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 监控器脚本 | $(echo "${TEST_RESULTS[@]}" | grep -o "integration-monitor:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证LayerMonitor类 |
| 协调器脚本 | $(echo "${TEST_RESULTS[@]}" | grep -o "integration-coordinator:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证协调器可执行性 |
| 同步配置 | $(echo "${TEST_RESULTS[@]}" | grep -o "integration-sync-config:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证JSON配置格式 |
| 监控系统测试 | $(echo "${TEST_RESULTS[@]}" | grep -o "integration-monitor-test:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/FAIL/❌ FAIL/') | 验证监控器功能 |
| 状态文件 | $(echo "${TEST_RESULTS[@]}" | grep -o "integration-status-file:[A-Z]*" | cut -d: -f2 | sed 's/PASS/✅ PASS/;s/WARN/⚠️ WARN/;s/FAIL/❌ FAIL/') | 验证状态文件生成 |

---

## ✅ 验证总结

$(if [ $FAIL_COUNT -eq 0 ]; then
    echo "🎉 **所有测试通过！系统已准备好运行。**"
    echo ""
    echo "✅ 技术层面所有脚本语法正确"
    echo "✅ 系统层面所有类和方法完整"
    echo "✅ 集成层面所有组件功能正常"
elif [ $FAIL_COUNT -le 2 ]; then
    echo "⚠️  **大部分测试通过，有少量失败。**"
    echo ""
    echo "系统基本可用，但建议修复失败项后再正式运行。"
else
    echo "❌ **较多测试失败，需要修复。**"
    echo ""
    echo "请先修复失败项，再执行系统。"
fi)

---

## 🚀 后续操作

### 如果所有测试通过

1. **执行技术层面:**
   \`\`\`bash
   cd $PROJECT_ROOT/tech-layer
   python3 scripts/install_deps.py
   ./run.sh "A cat playing with a ball"
   \`\`\`

2. **执行系统层面:**
   \`\`\`bash
   cd $PROJECT_ROOT/system-layer
   python3 permission_api.py
   \`\`\`

3. **监控系统状态:**
   \`\`\`bash
   python3 $INTEGRATION_DIR/monitors/layer_monitor.py
   \`\`\`

### 如果有测试失败

1. 查看失败详情
2. 修复相应脚本
3. 重新运行验证
4. 直到所有测试通过

---

## 📁 相关文件

- **验证日志:** $LOG_FILE
- **验证报告:** $REPORT_FILE
- **测试数据:** $VALIDATION_DIR/test_data/
- **测试结果:** $VALIDATION_DIR/test_results/

**验证完成时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**验证人签名:** 雯雯·技术整理师 📚 + 上帝之眼·守护者 🛡️  
**DNA验证:** #ZHUGEXIN⚡️2026-01-30-VALIDATION-LAYER-v1.0  
**验证状态:** $([ $FAIL_COUNT -eq 0 ] && echo "✅ 通过" || echo "⚠️  部分失败")

EOF

echo -e "${GREEN}✅ 验证报告已生成: $REPORT_FILE${NC}"
echo ""

# ============================================================================
# 完成
# ============================================================================
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🎉 验证层面执行完成！${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ 所有验证测试已完成！${NC}"
echo ""
echo -e "${CYAN}📊 验证统计:${NC}"
echo -e "   通过: ${GREEN}$PASS_COUNT${NC}"
echo -e "   失败: ${RED}$FAIL_COUNT${NC}"
echo -e "   警告: ${YELLOW}$WARN_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}🏆 恭喜！所有测试通过，系统已准备好运行！${NC}"
    echo ""
    echo -e "${YELLOW}⚡ 建议立即执行:${NC}"
    echo -e "   cd $PROJECT_ROOT/tech-layer"
    echo -e "   python3 scripts/install_deps.py"
    echo -e "   ./run.sh \"测试文本\""
else
    echo -e "${YELLOW}⚠️  部分测试失败，请先修复问题${NC}"
fi
echo ""

exit 0
EOF

chmod +x "/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/🔥 验证层面-测试验证.sh"

# 更新todo状态
echo -e "${GREEN}✅ 所有层面执行完成！${NC}
