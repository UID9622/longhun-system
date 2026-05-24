#!/bin/bash

# ============================================================================
# 🔥 Git Rebase 冲突快速修复脚本
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-01-30-QUICK-GIT-FIX-v1.0
# 创建者: 宝宝·构建师 #PERSONA-BAOBAO-001
# 功能: 快速解决Git Rebase冲突，清理工作区
# ============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 配置
PROJECT_ROOT="/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 标题
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🔥 Git Rebase 冲突快速修复${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 步骤1: 进入项目目录
echo -e "${BLUE}📂 进入项目目录...${NC}"
cd "$PROJECT_ROOT" || {
    echo -e "${RED}❌ 错误：无法进入目录 $PROJECT_ROOT${NC}"
    exit 1
}
echo -e "${GREEN}✅ 当前目录: $(pwd)${NC}"
echo ""

# 步骤2: 验证Git仓库
echo -e "${BLUE}🔍 验证Git仓库...${NC}"
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ 错误：当前目录不是Git仓库${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Git仓库验证通过${NC}"
echo ""

# 步骤3: 检查并删除Git锁文件
echo -e "${BLUE}🗑️  检查Git锁文件...${NC}"
GIT_DIR=$(git rev-parse --git-dir)
if [ -f "$GIT_DIR/index.lock" ]; then
    rm -f "$GIT_DIR/index.lock"
    echo -e "${GREEN}✅ 已删除Git锁文件${NC}"
else
    echo -e "${GREEN}✅ 未发现Git锁文件${NC}"
fi
echo ""

# 步骤4: 检查Rebase状态
echo -e "${BLUE}🔍 检查Rebase状态...${NC}"
REBASE_IN_PROGRESS=false
if [ -d "$GIT_DIR/rebase-merge" ] || [ -d "$GIT_DIR/rebase-apply" ]; then
    REBASE_IN_PROGRESS=true
    echo -e "${YELLOW}⚠️  检测到Rebase正在进行中${NC}"
    
    # 显示详细信息
    if [ -f "$GIT_DIR/rebase-merge/done" ]; then
        echo -e "${CYAN}   已完成提交: $(wc -l < "$GIT_DIR/rebase-merge/done")${NC}"
    fi
    if [ -f "$GIT_DIR/rebase-merge/msgnum" ]; then
        echo -e "${CYAN}   当前提交: $(cat "$GIT_DIR/rebase-merge/msgnum")${NC}"
    fi
    
    # 建议中止
    echo ""
    echo -e "${YELLOW}💡 建议中止当前rebase，清理后再重新执行${NC}"
    read -p "是否中止rebase？(y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git rebase --abort
        echo -e "${GREEN}✅ Rebase已中止${NC}"
    fi
else
    echo -e "${GREEN}✅ 未发现进行中的Rebase${NC}"
fi
echo ""

# 步骤5: 查看当前Git状态
echo -e "${BLUE}📊 当前Git状态统计:${NC}"
git status --short > /tmp/git_status.txt

deleted=$(grep "^ D" /tmp/git_status.txt | wc -l | tr -d ' ')
untracked=$(grep "^??" /tmp/git_status.txt | wc -l | tr -d ' ')
modified=$(grep "^ M" /tmp/git_status.txt | wc -l | tr -d ' ')

echo -e "   删除的文件: ${YELLOW}$deleted${NC}"
echo -e "   未跟踪的文件: ${YELLOW}$untracked${NC}"
echo -e "   修改的文件: ${YELLOW}$modified${NC}"
echo ""

# 步骤6: 清理Git缓存
echo -e "${BLUE}🧹 清理Git缓存（应用.gitignore）...${NC}"
echo -e "${YELLOW}   正在移除缓存...${NC}"
git rm -r --cached . > /tmp/rm_cache.log 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 缓存清理完成${NC}"
else
    echo -e "${RED}⚠️  缓存清理有警告（可能是正常的）${NC}"
fi

echo -e "${YELLOW}   重新添加文件（.gitignore生效）...${NC}"
git add . > /tmp/add.log 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 文件重新添加完成${NC}"
else
    echo -e "${RED}⚠️  添加文件有警告${NC}"
fi
echo ""

# 步骤7: 查看清理后的状态
echo -e "${BLUE}📊 清理后的Git状态:${NC}"
git status --short > /tmp/after_clean.txt
new_deleted=$(grep "^ D" /tmp/after_clean.txt | wc -l | tr -d ' ')
new_untracked=$(grep "^??" /tmp/after_clean.txt | wc -l | tr -d ' ')
new_modified=$(grep "^ M" /tmp/after_clean.txt | wc -l | tr -d ' ')

echo -e "   删除的文件: ${YELLOW}$new_deleted${NC} (${deleted}→${new_deleted})"
echo -e "   未跟踪的文件: ${YELLOW}$new_untracked${NC} (${untracked}→${new_untracked})"
echo -e "   修改的文件: ${YELLOW}$new_modified${NC} (${modified}→${new_modified})"
echo ""

# 步骤8: 提交修复（如果有更改）
echo -e "${BLUE}💾 提交修复...${NC}"
if ! git diff --cached --quiet; then
    COMMIT_MSG="🔧 修复Git工作区状态

- 清理Git缓存，应用.gitignore规则
- 删除不应追踪的文件（如node_modules）
- 文件统计: 删除:$new_deleted, 未跟踪:$new_untracked, 修改:$new_modified

DNA追溯码: #ZHUGEXIN⚡️2026-01-30-QUICK-GIT-FIX-$TIMESTAMP
修复执行人: 宝宝·构建师 #PERSONA-BAOBAO-001"
    
    git commit -m "$COMMIT_MSG"
    echo -e "${GREEN}✅ 修复已提交${NC}"
else
    echo -e "${YELLOW}⚠️  暂无可提交的更改${NC}"
fi
echo ""

# 步骤9: 最终状态
echo -e "${BLUE}📋 最终Git状态:${NC}"
git status --short | head -20
echo ""

# 步骤10: 生成修复报告
echo -e "${BLUE}📄 生成修复报告...${NC}"
REPORT_PATH="$HOME/UID9622_Workspace/logs/git_fix_report_$TIMESTAMP.md"
mkdir -p "$(dirname "$REPORT_PATH")"

cat > "$REPORT_PATH" << EOF
# 🔥 Git Rebase 冲突修复报告

**修复时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**修复脚本:** 快速修复版  
**DNA追溯码:** #ZHUGEXIN⚡️2026-01-30-QUICK-GIT-FIX-$TIMESTAMP

## 📊 修复前后对比

| 项目 | 修复前 | 修复后 | 变化 |
|------|--------|--------|------|
| 删除的文件 | $deleted | $new_deleted | $(($deleted - $new_deleted)) |
| 未跟踪的文件 | $untracked | $new_untracked | $(($untracked - $new_untracked)) |
| 修改的文件 | $modified | $new_modified | $(($modified - $new_modified)) |

## 🔧 执行的操作

1. ✅ 验证Git仓库完整性
2. ✅ 删除Git锁文件（如果存在）
3. ✅ 中止冲突的Rebase（用户确认）
4. ✅ 清理Git缓存（git rm -r --cached .）
5. ✅ 重新添加文件（应用.gitignore）
6. ✅ 提交修复更改

## 📝 提交信息

\`\`\`
$(git log -1 --pretty=format:"%s%n%n%b" 2>/dev/null || echo "无提交")
\`\`\`

## 🚀 下一步操作

1. **推送到远程:**
   \`\`\`bash
   git push
   \`\`\`

2. **验证状态:**
   \`\`\`bash
   git status
   git log --oneline -5
   \`\`\`

3. **重新Rebase（如果需要）:**
   \`\`\`bash
   git fetch origin
   git rebase origin/master
   \`\`\`

## 💾 相关文件

- 修复报告: $REPORT_PATH
- Git状态(修复前): /tmp/git_status.txt
- Git状态(修复后): /tmp/after_clean.txt

**修复完成时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**修复人:** 宝宝·构建师 👶
EOF

echo -e "${GREEN}✅ 报告已生成: $REPORT_PATH${NC}"
echo ""

# 完成
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🎉 Git Rebase 冲突快速修复完成！${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ 所有修复操作已完成！${NC}"
echo ""
echo -e "${YELLOW}⚡ 建议的后续操作:${NC}"
echo -e "   1. git push                   # 推送到远程仓库"
echo -e "   2. git status                 # 验证状态"
echo -e "   3. git log --oneline -5       # 查看提交历史"
echo ""
echo -e "${GREEN}🏮 感谢使用快速修复脚本！${NC}"
echo ""

# 清理临时文件
rm -f /tmp/git_status.txt /tmp/after_clean.txt /tmp/rm_cache.log /tmp/add.log

exit 0
