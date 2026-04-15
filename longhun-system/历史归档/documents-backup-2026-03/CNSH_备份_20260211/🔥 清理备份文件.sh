#!/bin/bash
# ============================================================================
# 🔥 清理备份文件脚本
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-02-09-CLEAN-BACKUPS-v1.0
# 功能: 清理系统中的备份文件，释放磁盘空间
# ============================================================================

PROJECT_ROOT="/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔥 清理备份文件脚本${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 统计备份文件
echo -e "${YELLOW}📊 统计备份文件...${NC}"
backup_count=$(find "$PROJECT_ROOT" -maxdepth 2 -name "*.backup" -type f 2>/dev/null | wc -l)
backup_size=$(find "$PROJECT_ROOT" -maxdepth 2 -name "*.backup" -type f 2>/dev/null -exec du -ch {} + 2>/dev/null | tail -1)

echo -e "   备份文件数量: ${backup_count}"
echo -e "   备份文件大小: ${backup_size:-0B}"
echo ""

# 询问用户
echo -e "${YELLOW}⚠️  将要删除以下类型的备份文件:${NC}"
echo -e "   1. *.backup 文件"
echo -e "   2. backups/ 目录"
echo ""

read -p "是否继续？[y/N] " confirm

if [[ $confirm != "y" && $confirm != "Y" ]]; then
    echo -e "${YELLOW}⏸️ 已取消${NC}"
    exit 0
fi

echo ""

# 清理 .backup 文件
echo -e "${CYAN}🧹 清理 .backup 文件...${NC}"
backup_deleted=0

find "$PROJECT_ROOT" -maxdepth 2 -name "*.backup" -type f -print0 2>/dev/null | while IFS= read -r -d '' file; do
    echo "   删除: $file"
    rm -f "$file"
    ((backup_deleted++))
done

# 清理 backups/ 目录
if [ -d "$PROJECT_ROOT/backups" ]; then
    echo -e "${CYAN}🧹 清理 backups/ 目录...${NC}"
    echo "   删除: $PROJECT_ROOT/backups"
    rm -rf "$PROJECT_ROOT/backups"
fi

echo ""
echo -e "${GREEN}✅ 清理完成！${NC}"
echo ""
echo -e "${GREEN}💡 建议:${NC}"
echo -e "   1. cnsh_cleaner.py 现在默认不会创建备份"
echo -e "   2. 如需备份，请使用: python cnsh_cleaner.py clean 文件名.md --backup"
echo ""

exit 0
