#!/bin/bash
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: move_old_files.sh | 标记时间: 2026-06-03T07:46:00+0800
# 文件移动脚本 - 将旧文档移动到归档目录
# DNA: #ZHUGEXIN⚡️2026-01-27-ARCHIVE-v1.0

SOURCE_DIR="/Users/zuimeidedeyihan/Desktop/打包待命/CNSH 军人的编辑器"
ARCHIVE_DIR="$SOURCE_DIR/归档/旧文档_20260127"

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

# 需要移动的文件列表
FILES_TO_MOVE=(
    "2025-12-10.md"
    "2025-12-11.md"
    "2025-12-13.md"
    "2025-12-16.md"
    "64卦注释-资料目录-20251211.md"
    "策略文件-使用说明.md"
    "调整网络方案-无需新卡.md"
    "分享页面给咱妈.md"
    "给CodeBuddy的超级简单任务.md"
    "防火墙优化完成报告.md"
    "华为云AI助手配置.md"
    "记忆系统+避坑指南-完成总结.md"
    "监管防火墙-DNA极简版_20251223_022822.md"
    "净土36条-AI统一标准.md"
    "开源发布-完成总结报告.md"
    "开源发布快速开始指南.md"
    "跨设备同步指南"
    "龍魂多语言编译系统完整方案.md"
    "龍魂徽章系统_三色审计版_V1.0.md"
    "龍魂身份系统安装说明.md"
    "龍魂P0级-三层交叉监督与镜像人格完整方案.md"
    "论文发布准备-最终报告.md"
    "普惠全民-龍魂系统-推广包.md"
    "签名工具使用说明.md"
)

# 移动文件
count=0
for file in "${FILES_TO_MOVE[@]}"; do
    if [ -f "$SOURCE_DIR/$file" ]; then
        mv "$SOURCE_DIR/$file" "$ARCHIVE_DIR/"
        echo "✓ 已移动: $file"
        ((count++))
    else
        echo "✗ 不存在: $file"
    fi
done

echo ""
echo "=========================================="
echo "整理完成！"
echo "共移动 $count 个文件到: $ARCHIVE_DIR"
echo "=========================================="
