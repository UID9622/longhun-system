#!/bin/bash

# ============================================================================
# 🔥 继续推送脚本
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-02-09-CONTINUE-PUSH-v1.0
# ============================================================================

set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 配置
PROJECT_ROOT="/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/Longhun-AntiColonial-Algorithm"
GITHUB_USER="uid9622"
GITHUB_REPO="longhun-anti-colonial"

echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🚀 继续推送到GitHub${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 进入项目目录
cd "$PROJECT_ROOT"
echo -e "${BLUE}📍 当前目录: $(pwd)${NC}"
echo ""

# 添加远程仓库
echo -e "${BLUE}🔗 添加远程仓库...${NC}"
if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${GREEN}✅ 远程仓库已配置${NC}"
    git remote -v
else
    git remote add origin "git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git"
    echo -e "${GREEN}✅ 远程仓库添加完成${NC}"
fi
echo ""

# 检查分支
echo -e "${BLUE}🌿 检查当前分支...${NC}"
CURRENT_BRANCH=$(git branch --show-current)
echo -e "   当前分支: ${CURRENT_BRANCH}"
echo ""

# 如果是master,重命名为main
if [ "$CURRENT_BRANCH" = "master" ]; then
    echo -e "${BLUE}🔄 重命名分支为main...${NC}"
    git branch -M main
    echo -e "${GREEN}✅ 分支重命名完成${NC}"
    CURRENT_BRANCH="main"
fi
echo ""

# 推送到GitHub
echo -e "${BLUE}🚀 推送到GitHub...${NC}"
echo -e "${YELLOW}提示: 首次推送可能需要输入GitHub token或SSH密钥${NC}"
echo ""

git push -u origin ${CURRENT_BRANCH}

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 推送完成！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${BLUE}📊 访问你的仓库:${NC}"
echo -e "   https://github.com/${GITHUB_USER}/${GITHUB_REPO}"
echo ""

exit 0
