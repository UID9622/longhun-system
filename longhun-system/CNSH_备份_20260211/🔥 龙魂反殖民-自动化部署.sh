#!/bin/bash

# ============================================================================
# 🔥 龙魂反殖民计划 - 自动化部署脚本
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-02-09-AUTO-DEPLOY-v1.0
# 功能: 一键初始化Git仓库、推送到GitHub
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
PROJECT_ROOT="/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/Longhun-AntiColonial-Algorithm"
GITHUB_USER="uid9622"
GITHUB_REPO="longhun-anti-colonial"

echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🐉 龙魂反殖民计划 - 自动化部署${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 检查项目目录
echo -e "${BLUE}📁 检查项目目录...${NC}"
if [ ! -d "$PROJECT_ROOT" ]; then
    echo -e "${RED}❌ 项目目录不存在: $PROJECT_ROOT${NC}"
    exit 1
fi
echo -e "${GREEN}✅ 项目目录存在${NC}"
echo ""

# 进入项目目录
cd "$PROJECT_ROOT"
echo -e "${CYAN}📍 当前目录: $(pwd)${NC}"
echo ""

# 检查是否已经是Git仓库
if [ ! -d ".git" ]; then
    echo -e "${BLUE}🔧 初始化Git仓库...${NC}"
    git init
    echo -e "${GREEN}✅ Git仓库初始化完成${NC}"
else
    echo -e "${YELLOW}⚠️  已是Git仓库${NC}"
fi
echo ""

# 配置Git用户信息
echo -e "${BLUE}🔧 配置Git用户信息...${NC}"
git config user.name "诸葛鑫"
git config user.email "uid9622@longhun.dev"
echo -e "${GREEN}✅ Git配置完成${NC}"
echo ""

# 添加所有文件
echo -e "${BLUE}📦 添加文件到暂存区...${NC}"
git add .
echo -e "${GREEN}✅ 文件添加完成${NC}"
echo ""

# 创建初始提交
echo -e "${BLUE}💾 创建初始提交...${NC}"
git commit -m "🐉 初始提交: 龙魂反殖民算法工具集

- 数据导出工具: 行使个人信息保护法权利
- 算法检测工具: 检测平台算法杀熟
- 信息流重构插件: 屏蔽焦虑推荐

DNA追溯码: #龙芯⚡️2026-02-09-INITIAL-COMMIT-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

作者: 诸葛鑫（Lucky）｜UID9622"
echo -e "${GREEN}✅ 初始提交完成${NC}"
echo ""

# 添加远程仓库
echo -e "${BLUE}🔗 添加远程仓库...${NC}"
if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  远程仓库已存在${NC}"
    git remote set-url origin "git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git"
else
    git remote add origin "git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git"
fi
echo -e "${GREEN}✅ 远程仓库配置完成${NC}"
echo ""

# 推送到GitHub
echo -e "${BLUE}🚀 推送到GitHub...${NC}"
echo -e "${YELLOW}提示: 首次推送可能需要输入GitHub token或SSH密钥${NC}"
echo ""

git push -u origin main || git push -u origin master

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 部署完成！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${CYAN}📊 项目信息:${NC}"
echo -e "   仓库地址: https://github.com/${GITHUB_USER}/${GITHUB_REPO}"
echo -e "   SSH地址: git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git"
echo -e "   本地路径: $PROJECT_ROOT"
echo ""

echo -e "${CYAN}📝 下一步操作:${NC}"
echo -e "   1. 访问 https://github.com/${GITHUB_USER}/${GITHUB_REPO}"
echo -e "   2. 检查仓库是否创建成功"
echo -e "   3. 配置GitHub仓库描述和标签"
echo -e "   4. 发布第一个Release"
echo ""

echo -e "${PURPLE}🧬 DNA追溯码: #龙芯⚡️2026-02-09-AUTO-DEPLOY-v1.0${NC}"
echo -e "${PURPLE}🔒 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z${NC}"
echo ""

exit 0
