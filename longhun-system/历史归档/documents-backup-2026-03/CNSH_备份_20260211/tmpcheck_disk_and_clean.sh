#!/bin/bash
# 🐉 CNSH磁盘清理工具
# DNA追溯码: #龍芯⚡️2026-02-10-磁盘清理工具-v1.0
# 创建者: 诸葛鑫 | UID9622

echo "╔═══════════════════════════════════════════════╗"
echo "║  🐉 CNSH磁盘清理工具 · DragonSoul System    ║"
echo "║  DNA: #龍芯⚡️2026-02-10-v1.0                 ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# ==========================================
# 第一步：检查磁盘使用情况
# ==========================================
echo "📊 【第一步】检查磁盘使用情况..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
df -h
echo ""

# ==========================================
# 第二步：检查Docker容器
# ==========================================
echo "🐳 【第二步】检查Docker容器..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v docker &> /dev/null; then
    echo "✅ Docker已安装"
    echo ""
    
    echo "📦 正在运行的容器："
    docker ps
    echo ""
    
    echo "💾 所有容器（包括停止的）："
    docker ps -a
    echo ""
    
    echo "📊 Docker磁盘使用情况："
    docker system df
    echo ""
else
    echo "⚠️ Docker未安装或未启动"
fi

# ==========================================
# 第三步：检查大文件
# ==========================================
echo "🔍 【第三步】检查大文件（前20个）..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "正在扫描 $HOME 目录中的大文件（可能需要几分钟）..."
find "$HOME" -type f -size +100M 2>/dev/null | head -20 | while read file; do
    size=$(du -h "$file" | cut -f1)
    echo "  📁 $size - $file"
done
echo ""

# ==========================================
# 第四步：检查DragonSoul项目目录
# ==========================================
echo "🐉 【第四步】检查DragonSoul项目..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
DRAGON_PATH="$HOME/DragonSoul"
if [ -d "$DRAGON_PATH" ]; then
    echo "✅ 找到DragonSoul目录: $DRAGON_PATH"
    echo ""
    echo "📊 目录大小："
    du -sh "$DRAGON_PATH"
    echo ""
    echo "📁 子目录大小（前10个最大的）："
    du -sh "$DRAGON_PATH"/* 2>/dev/null | sort -hr | head -10
    echo ""
else
    echo "⚠️ 未找到DragonSoul目录: $DRAGON_PATH"
fi

# ==========================================
# 第五步：提供清理建议
# ==========================================
echo "🧹 【第五步】清理建议..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣ 清理Docker（如果安装了）："
echo "   docker system prune -a --volumes    # 清理所有未使用的Docker资源"
echo "   docker container prune              # 清理停止的容器"
echo "   docker image prune -a               # 清理未使用的镜像"
echo "   docker volume prune                 # 清理未使用的卷"
echo ""
echo "2️⃣ 清理Xcode缓存："
echo "   rm -rf ~/Library/Developer/Xcode/DerivedData/*"
echo "   rm -rf ~/Library/Caches/com.apple.dt.Xcode/*"
echo ""
echo "3️⃣ 清理Homebrew缓存："
echo "   brew cleanup -s"
echo "   rm -rf $(brew --cache)"
echo ""
echo "4️⃣ 清理系统日志："
echo "   sudo rm -rf /private/var/log/asl/*.asl"
echo "   sudo rm -rf /Library/Logs/DiagnosticReports/*"
echo ""
echo "5️⃣ 清理npm缓存："
echo "   npm cache clean --force"
echo ""

echo "╔═══════════════════════════════════════════════╗"
echo "║  ✅ 磁盘检查完成！                           ║"
echo "║  请根据上面的建议进行清理                    ║"
echo "╚═══════════════════════════════════════════════╝"
