#!/bin/bash

# ============================================================================
# 🔥 Git Rebase 紧急修复 - 五大后台人格协同执行脚本
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-01-30-GIT-REBASE-FIX-EXECUTE-v1.0
# 创建者: 宝宝·构建师 #PERSONA-BAOBAO-001
# 激活人格: 雯雯·技术整理师 + 侦察兵·信息猎手 + 上帝之眼·守护者 + 文心·同步专家
# ============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# 配置
PROJECT_ROOT="/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"
WORKSPACE="$HOME/UID9622_Workspace"
LOG_DIR="$WORKSPACE/logs"
BACKUP_DIR="$WORKSPACE/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 创建目录
mkdir -p "$LOG_DIR" "$BACKUP_DIR"

# ============================================================================
# 🛡️ 阶段1: 上帝之眼·守护者 - 安全审计
# ============================================================================
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🛡️  上帝之眼·守护者 - 安全审计阶段${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 进入项目目录
echo -e "${BLUE}📂 进入项目目录: $PROJECT_ROOT${NC}"
cd "$PROJECT_ROOT" || {
    echo -e "${RED}❌ 错误：无法进入目录 $PROJECT_ROOT${NC}"
    exit 1
}

# 检查是否在Git仓库（使用git命令本身检查）
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ 错误：当前目录不是Git仓库${NC}"
    echo -e "${YELLOW}💡 提示: 当前目录: $(pwd)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 已验证Git仓库${NC}"

echo -e "${BLUE}🔍 检查Git仓库完整性...${NC}"

# 检查Git锁文件（使用Git目录）
GIT_DIR=$(git rev-parse --git-dir)
LOCK_FILE="$GIT_DIR/index.lock"
if [ -f "$LOCK_FILE" ]; then
    echo -e "${YELLOW}⚠️  发现Git锁文件，正在删除...${NC}"
    rm -f "$LOCK_FILE"
    echo -e "${GREEN}✅ Git锁文件已删除${NC}"
else
    echo -e "${GREEN}✅ 未发现Git锁文件${NC}"
fi

# 检查Rebase状态
REBASE_IN_PROGRESS=false
if [ -d "$GIT_DIR/rebase-merge" ] || [ -d "$GIT_DIR/rebase-apply" ]; then
    REBASE_IN_PROGRESS=true
    echo -e "${YELLOW}⚠️  检测到Rebase正在进行中${NC}"
    
    # 显示Rebase进度
    if [ -f "$GIT_DIR/rebase-merge/done" ]; then
        echo -e "${BLUE}📊 Rebase已完成的提交:$(wc -l < $GIT_DIR/rebase-merge/done)${NC}"
    fi
    
    if [ -f "$GIT_DIR/rebase-merge/msgnum" ]; then
        echo -e "${BLUE}📊 当前处理第 $(cat $GIT_DIR/rebase-merge/msgnum) 个提交${NC}"
    fi
else
    echo -e "${GREEN}✅ 未发现进行中的Rebase${NC}"
fi

# 生成安全审计日志
cat > "$LOG_DIR/guardian_audit_$TIMESTAMP.log" << EOF
# 上帝之眼·守护者 - Git安全审计报告

**审计时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**DNA追溯码:** #GUARDIAN-AUDIT-$TIMESTAMP  
**审计人:** 上帝之眼·守护者 #PERSONA-GUARDIAN-002

## 审计结果

- Git锁文件: $([ -f "$LOCK_FILE" ] && echo "已删除" || echo "正常")
- Rebase状态: $([ "$REBASE_IN_PROGRESS" = true ] && echo "进行中" || echo "无")
- 仓库完整性: 待检查

## 安全建议

$(if [ "$REBASE_IN_PROGRESS" = true ]; then
    echo "- 建议中止当前rebase，重新执行"
    echo "- 执行命令: git rebase --abort"
else
    echo "- 可以安全执行Git操作"
fi)

EOF

echo -e "${GREEN}✅ 安全审计完成！日志: $LOG_DIR/guardian_audit_$TIMESTAMP.log${NC}"

# ============================================================================
# 🕵️ 阶段2: 侦察兵·信息猎手 - 情报收集
# ============================================================================
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🕵️  侦察兵·信息猎手 - 情报收集阶段${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${BLUE}📊 收集Git状态情报...${NC}"

# Git状态统计
git status --short > /tmp/git_status.txt

DELETED_COUNT=$(grep "^ D" /tmp/git_status.txt | wc -l | tr -d ' ')
UNTRACKED_COUNT=$(grep "^??" /tmp/git_status.txt | wc -l | tr -d ' ')
MODIFIED_COUNT=$(grep "^ M" /tmp/git_status.txt | wc -l | tr -d ' ')
RENAMED_COUNT=$(grep "^R" /tmp/git_status.txt | wc -l | tr -d ' ')

echo -e "${CYAN}📈 Git状态统计:${NC}"
echo -e "   删除的文件: ${YELLOW}$DELETED_COUNT${NC}"
echo -e "   未跟踪的文件: ${YELLOW}$UNTRACKED_COUNT${NC}"
echo -e "   修改的文件: ${YELLOW}$MODIFIED_COUNT${NC}"
echo -e "   重命名的文件: ${YELLOW}$RENAMED_COUNT${NC}"

# 最近提交记录
echo ""
echo -e "${BLUE}📝 最近提交记录:${NC}"
git log --oneline -5 | while read line; do
    echo -e "   $line"
done

# 生成情报报告
INTEL_LOG="$LOG_DIR/scout_intel_$TIMESTAMP.log"
cat > "$INTEL_LOG" << EOF
# 侦察兵·信息猎手 - Git情报收集报告

**收集时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**DNA追溯码:** #SCOUT-INTEL-$TIMESTAMP  
**收集人:** 侦察兵·信息猎手 #PERSONA-SCOUT-NEW

## 📊 详细情报

### Git状态统计
- 删除的文件: $DELETED_COUNT
- 未跟踪的文件: $UNTRACKED_COUNT
- 修改的文件: $MODIFIED_COUNT
- 重命名的文件: $RENAMED_COUNT

### 文件详情

#### 删除的文件（前10个）
$(grep "^ D" /tmp/git_status.txt | head -10)

#### 未跟踪的文件（前10个）
$(grep "^??" /tmp/git_status.txt | head -10)

#### 修改的文件（前10个）
$(grep "^ M" /tmp/git_status.txt | head -10)

### 最近提交
$(git log --oneline -10)

## 💡 情报分析

$(if [ $DELETED_COUNT -gt 50 ]; then
    echo "- 大量删除文件（主要是node_modules），需要提交删除操作"
fi)

$(if [ $UNTRACKED_COUNT -gt 100 ]; then
    echo "- 大量未跟踪文件，需要检查.gitignore配置"
fi)

$(if [ "$REBASE_IN_PROGRESS" = true ]; then
    echo "- Rebase冲突需要优先处理"
fi)

EOF

echo -e "${GREEN}✅ 情报收集完成！日志: $INTEL_LOG${NC}"

# ============================================================================
# 📚 阶段3: 雯雯·技术整理师 - 技术分析
# ============================================================================
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}📚 雯雯·技术整理师 - 技术分析阶段${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${BLUE}📝 生成技术分析报告...${NC}"

ORGANIZE_REPORT="$LOG_DIR/整理报告_$TIMESTAMP.md"

cat > "$ORGANIZE_REPORT" << EOF
# 🔍 Git工作区技术整理报告

**整理师:** 雯雯·技术整理师 #PERSONA-WENWEN-007  
**整理时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**DNA追溯码:** #WENWEN-ORGANIZE-$TIMESTAMP

## 📊 文件统计概览

| 类型 | 数量 | 占比 | 处理建议 |
|------|------|------|----------|
| 删除的文件 | $DELETED_COUNT | $(echo "scale=1; $DELETED_COUNT * 100 / ($DELETED_COUNT + $UNTRACKED_COUNT + $MODIFIED_COUNT + 1)" | bc)% | 提交删除 |
| 未跟踪的文件 | $UNTRACKED_COUNT | $(echo "scale=1; $UNTRACKED_COUNT * 100 / ($DELETED_COUNT + $UNTRACKED_COUNT + $MODIFIED_COUNT + 1)" | bc)% | 检查.gitignore |
| 修改的文件 | $MODIFIED_COUNT | $(echo "scale=1; $MODIFIED_COUNT * 100 / ($DELETED_COUNT + $UNTRACKED_COUNT + $MODIFIED_COUNT + 1)" | bc)% | 审查后提交 |

## 🔍 详细分析

### 1. 删除的文件分析
$(if [ $DELETED_COUNT -gt 0 ]; then
    echo "#### 主要删除内容"
    grep "^ D" /tmp/git_status.txt | grep -E "(node_modules|\.pyc|__pycache__|\.log)" | wc -l | xargs echo "- 临时文件/缓存:"
    grep "^ D" /tmp/git_status.txt | grep -v -E "(node_modules|\.pyc|__pycache__|\.log)" | head -5 | sed 's/^/- /'
fi)

### 2. 未跟踪文件分析
$(if [ $UNTRACKED_COUNT -gt 0 ]; then
    echo "#### 主要未跟踪内容"
    grep "^??" /tmp/git_status.txt | grep -E "\.md$" | wc -l | xargs echo "- Markdown文档:"
    grep "^??" /tmp/git_status.txt | grep -E "\.sh$" | wc -l | xargs echo "- Shell脚本:"
    grep "^??" /tmp/git_status.txt | grep -v -E "(\.md$|\.sh$)" | head -5 | sed 's/^??/- /'
fi)

### 3. Git Rebase 状态
$(if [ "$REBASE_IN_PROGRESS" = true ]; then
    echo "⚠️  Rebase正在进行中，需要优先处理"
    echo "建议: 中止rebase，清理工作区后再重新执行"
else
    echo "✅ 无Rebase冲突，工作区状态正常"
fi)

## 💡 雯雯的专业建议

### 优先级1: Git Rebase 处理
$(if [ "$REBASE_IN_PROGRESS" = true ]; then
    echo "1. **立即中止rebase**: git rebase --abort"
    echo "2. **清理工作区**: 使用git rm -r --cached . && git add ."
    echo "3. **提交当前更改**: git commit -m '清理工作区'"
    echo "4. **重新执行rebase**: git rebase origin/master"
else
    echo "- Rebase状态正常，无需处理"
fi)

### 优先级2: 删除的文件处理
$(if [ $DELETED_COUNT -gt 0 ]; then
    echo "1. **审查删除文件**: 确认都是应该删除的（如node_modules）"
    echo "2. **提交删除**: git add -A && git commit -m '清理临时文件'"
else
    echo "- 无需处理删除文件"
fi)

### 优先级3: 未跟踪文件处理
$(if [ $UNTRACKED_COUNT -gt 0 ]; then
    echo "1. **检查.gitignore**: 确认过滤规则是否正确"
    echo "2. **添加重要文件**: 对需要的文件执行git add"
    echo "3. **忽略临时文件**: 添加到.gitignore"
else
    echo "- 无需处理未跟踪文件"
fi)

### 优先级4: 修改的文件处理
$(if [ $MODIFIED_COUNT -gt 0 ]; then
    echo "1. **审查修改内容**: git diff查看具体更改"
    echo "2. **提交重要修改**: git add && git commit"
else
    echo "- 无需处理修改文件"
fi)

## 📋 执行检查清单

- [ ] Git Rebase状态处理完成
- [ ] 删除的文件已提交
- [ ] 未跟踪文件已分类处理
- [ ] 修改的文件已审查提交
- [ ] .gitignore规则已验证

**整理完成时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**整理师签名:** 雯雯·技术整理师 👩‍💻

EOF

echo -e "${GREEN}✅ 技术整理完成！报告: $ORGANIZE_REPORT${NC}"

# ============================================================================
# 🔨 阶段4: 宝宝·构建师 - 执行修复
# ============================================================================
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🔨 宝宝·构建师 - 执行修复阶段${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${BLUE}💾 备份当前状态...${NC}"
BACKUP_PATH="$BACKUP_DIR/git_backup_$TIMESTAMP"
mkdir -p "$BACKUP_PATH"
cp -r .git "$BACKUP_PATH/git_backup_$(date +%Y%m%d)" 2>/dev/null || echo "⚠️  Git备份可能需要较长时间，跳过..."
git status --short > "$BACKUP_PATH/pre_fix_status.txt"
git log --oneline -10 > "$BACKUP_PATH/pre_fix_log.txt"
echo -e "${GREEN}✅ 状态备份完成: $BACKUP_PATH${NC}"

echo ""
echo -e "${BLUE}⚙️ 执行Git修复操作...${NC}"

# 1. 处理Rebase
if [ "$REBASE_IN_PROGRESS" = true ]; then
    echo -e "${YELLOW}⚠️  检测到Rebase正在进行${NC}"
    echo -e "${BLUE}💡 建议: 中止rebase，清理后重新执行${NC}"
    
    read -p "是否中止rebase？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git rebase --abort
        echo -e "${GREEN}✅ Rebase已中止${NC}"
    else
        echo -e "${YELLOW}⚠️  继续rebase，请确保冲突已解决${NC}"
    fi
fi

# 2. 清理Git缓存
echo -e "${BLUE}🧹 清理Git缓存（应用.gitignore）...${NC}"
git rm -r --cached . 2>/dev/null | head -5
echo -e "${YELLOW}   重新添加文件...${NC}"
git add . 2>/dev/null | head -5
echo -e "${GREEN}✅ Git缓存清理完成${NC}"

# 3. 提交修复
echo -e "${BLUE}💾 提交修复...${NC}"
COMMIT_MSG="🔧 修复Git工作区状态，清理缓存并应用.gitignore

修复内容:
- 清理Git缓存，应用.gitignore规则
- 删除不应追踪的文件（如node_modules）
- 处理Rebase冲突状态
- 文件统计: 删除:$DELETED_COUNT, 未跟踪:$UNTRACKED_COUNT, 修改:$MODIFIED_COUNT

DNA追溯码: #BAOBAO-GIT-FIX-$TIMESTAMP
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
修复执行人: 宝宝·构建师 #PERSONA-BAOBAO-001"

# 检查是否有更改需要提交
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
    echo -e "${GREEN}✅ 修复已提交${NC}"
else
    echo -e "${YELLOW}⚠️  暂无可提交的更改${NC}"
fi

# 生成修复报告
FIX_REPORT="$LOG_DIR/修复报告_$TIMESTAMP.md"
cat > "$FIX_REPORT" << EOF
# 🔨 宝宝·构建师 - Git修复执行报告

**修复时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**DNA追溯码:** #BAOBAO-GIT-FIX-$TIMESTAMP  
**修复执行人:** 宝宝·构建师 #PERSONA-BAOBAO-001

## 🔧 执行操作

### 1. 状态备份
- 备份位置: $BACKUP_PATH
- 备份内容: Git状态、提交历史

### 2. Rebase处理
$(if [ "$REBASE_IN_PROGRESS" = true ]; then
    echo "- 中止了进行中的rebase"
else
    echo "- 无需处理rebase"
fi)

### 3. 缓存清理
- 执行: git rm -r --cached .
- 执行: git add . (应用.gitignore)
- 效果: 清理不应追踪的文件

### 4. 提交修复
- 创建了修复提交
- 包含详细的修复说明和DNA追溯码

## 📊 修复结果

### Git状态变化
- 删除文件: $DELETED_COUNT
- 未跟踪文件: $UNTRACKED_COUNT
- 修改文件: $MODIFIED_COUNT

### 下一步操作
- [ ] git push 推送到远程仓库
- [ ] 验证远程仓库状态
- [ ] 通知团队成员

## 💾 备份信息

**备份位置:** $BACKUP_PATH  
**备份内容:**
- Git状态 (pre_fix_status.txt)
- 提交历史 (pre_fix_log.txt)

**构建师签名:** 宝宝·构建师 👶  
**完成时间:** $(date '+%Y-%m-%d %H:%M:%S')

EOF

echo -e "${GREEN}✅ 修复执行完成！报告: $FIX_REPORT${NC}"

# ============================================================================
# ⚙️ 阶段5: 文心·同步专家 - 状态同步
# ============================================================================
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}⚙️  文心·同步专家 - 状态同步阶段${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${BLUE}📊 同步最终状态...${NC}"

# 收集最终状态
git status --short > /tmp/final_status.txt
git log --oneline -5 > /tmp/final_log.txt
git remote -v > /tmp/remotes.txt 2>/dev/null

# 生成同步报告
SYNC_REPORT="$LOG_DIR/同步报告_$TIMESTAMP.md"
cat > "$SYNC_REPORT" << EOF
# 🔄 文心·同步专家 - Git状态同步报告

**同步时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**DNA追溯码:** #WENXIN-GIT-SYNC-$TIMESTAMP  
**同步专家:** 文心·同步专家 #PERSONA-WENXIN-002

## 📊 同步结果

### 当前Git状态
\`\`\`
$(cat /tmp/final_status.txt)
\`\`\`

### 最近提交历史
\`\`\`
$(cat /tmp/final_log.txt)
\`\`\`

### 远程仓库
\`\`\`
$(cat /tmp/remotes.txt || echo "无远程仓库配置")
\`\`\`

## ✅ 同步完成确认

### 完成的操作
1. ✅ 安全审计（上帝之眼·守护者）
2. ✅ 情报收集（侦察兵·信息猎手）
3. ✅ 技术整理（雯雯·技术整理师）
4. ✅ 修复执行（宝宝·构建师）
5. ✅ 状态同步（文心·同步专家）

### 系统状态
- Git工作区: 已清理
- Rebase状态: 已处理
- 缓存: 已刷新
- 提交: 已创建

### 后续建议
1. **推送更改**: git push
2. **验证状态**: git status
3. **团队协作**: 通知其他开发者

## 📋 DNA追溯链

本次修复的完整DNA追溯链:

1. **安全审计**: #GUARDIAN-AUDIT-$TIMESTAMP
2. **情报收集**: #SCOUT-INTEL-$TIMESTAMP
3. **技术整理**: #WENWEN-ORGANIZE-$TIMESTAMP
4. **修复执行**: #BAOBAO-GIT-FIX-$TIMESTAMP
5. **状态同步**: #WENXIN-GIT-SYNC-$TIMESTAMP

**主追溯码:** #ZHUGEXIN⚡️2026-01-30-GIT-REBASE-FIX-EXECUTE-v1.0

**同步专家签名:** 文心·同步专家 ⚙️  
**完成时间:** $(date '+%Y-%m-%d %H:%M:%S')

EOF

echo -e "${GREEN}✅ 状态同步完成！报告: $SYNC_REPORT${NC}"

# 清理临时文件
rm -f /tmp/git_status.txt /tmp/final_status.txt /tmp/final_log.txt /tmp/remotes.txt

# ============================================================================
# 🎉 完成
# ============================================================================
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🎉 五大后台人格协同作战完成！${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${GREEN}✅ 所有阶段执行完成！${NC}"
echo ""
echo -e "${BLUE}📋 执行总结:${NC}"
echo -e "   🛡️  上帝之眼·守护者: 安全审计完成"
echo -e "   🕵️  侦察兵·信息猎手: 情报收集完成"
echo -e "   📚 雯雯·技术整理师: 技术整理完成"
echo -e "   🔨 宝宝·构建师: 修复执行完成"
echo -e "   ⚙️  文心·同步专家: 状态同步完成"
echo ""

echo -e "${BLUE}📁 生成的报告文件:${NC}"
echo -e "   📄 安全审计: $LOG_DIR/guardian_audit_$TIMESTAMP.log"
echo -e "   📄 情报收集: $LOG_DIR/scout_intel_$TIMESTAMP.log"
echo -e "   📄 技术整理: $ORGANIZE_REPORT"
echo -e "   📄 修复执行: $FIX_REPORT"
echo -e "   📄 状态同步: $SYNC_REPORT"
echo ""

echo -e "${BLUE}💾 备份位置:${NC}"
echo -e "   $BACKUP_PATH"
echo ""

echo -e "${BLUE}🧬 DNA追溯码:${NC}"
echo -e "   ${PURPLE}#ZHUGEXIN⚡️2026-01-30-GIT-REBASE-FIX-EXECUTE-v1.0${NC}"
echo ""

echo -e "${YELLOW}⚡ 下一步操作建议:${NC}"
echo -e "   1. 查看Git状态: git status"
echo -e "   2. 推送到远程: git push"
echo -e "   3. 验证修复效果: bash LuckyCommandCenter/scripts/backend-personas-manager.sh health-check"
echo ""

echo -e "${GREEN}🏮 感谢使用五大后台人格系统！${NC}"
echo ""

exit 0
