#!/bin/bash

# ============================================
# 龍魂系统·星辰记忆库三层同步方案
# ============================================
# 
# DNA追溯码: #龍芯⚡️2026-03-28-星辰记忆库同步-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 
# 作者: 诸葛鑫 (UID9622) - 初中文化，退伍军人
# AI辅助: Claude (Anthropic)
# 
# 功能:
# 1. 本地Git初始化（第一层铁甲）
# 2. 远程Git推送（第二层铁甲·Gitee优先）
# 3. Notion备份（第三层铁甲·可选）
#
# ============================================

set -e  # 遇到错误立即停止

MEMORY_DIR="$HOME/.star-memory"
GITEE_REPO="git@gitee.com:uid9622/star-memory.git"  # 老大需要改成自己的
GITHUB_REPO="git@github.com:uid9622/star-memory.git"  # 备用

echo "🐉 龍魂系统·星辰记忆库三层同步开始..."
echo ""

# ============================================
# 第一层：本地Git初始化
# ============================================
echo "📦 第一层：本地Git初始化..."

if [ ! -d "$MEMORY_DIR" ]; then
    echo "❌ 错误：星辰记忆库目录不存在：$MEMORY_DIR"
    echo "   请先运行记忆注入脚本创建记忆库"
    exit 1
fi

cd "$MEMORY_DIR"

if [ ! -d ".git" ]; then
    echo "   初始化Git仓库..."
    git init
    
    # 创建.gitignore
    cat > .gitignore << 'EOF'
# 临时文件
*.tmp
*.log
.DS_Store

# 敏感信息（如果有的话）
secrets/
*.key
EOF
    
    # 第一次提交
    git add .
    git commit -m "🎉 初始化星辰记忆库

DNA追溯码: #龍芯⚡️$(date +%Y-%m-%d)-星辰记忆库-初始化
作者: UID9622 诸葛鑫
内容: 首次提交，建立版本控制基础
"
    
    echo "✅ Git仓库初始化完成！"
else
    echo "✅ Git仓库已存在"
fi

echo ""

# ============================================
# 第二层：配置远程Git仓库
# ============================================
echo "🌐 第二层：配置远程Git仓库..."

# 检查是否已配置Gitee
if ! git remote | grep -q "gitee"; then
    echo "   添加Gitee远程仓库（国内优先）..."
    git remote add gitee "$GITEE_REPO" 2>/dev/null || echo "   Gitee远程仓库已存在"
else
    echo "✅ Gitee远程仓库已配置"
fi

# 检查是否已配置GitHub
if ! git remote | grep -q "github"; then
    echo "   添加GitHub远程仓库（全球备用）..."
    git remote add github "$GITHUB_REPO" 2>/dev/null || echo "   GitHub远程仓库已存在"
else
    echo "✅ GitHub远程仓库已配置"
fi

echo ""
echo "📋 当前远程仓库配置："
git remote -v

echo ""

# ============================================
# 第三层：提供推送脚本
# ============================================
echo "🚀 第三层：创建推送脚本..."

cat > "$MEMORY_DIR/sync.sh" << 'SYNCEOF'
#!/bin/bash
# 星辰记忆库快速同步脚本

MEMORY_DIR="$HOME/.star-memory"
cd "$MEMORY_DIR"

echo "🐉 龍魂系统·星辰记忆库同步中..."

# 检查是否有变更
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 没有新变更，无需同步"
else
    echo "📝 发现新变更，准备提交..."
    
    # 生成DNA追溯码
    DNA_CODE="#龍芯⚡️$(date +%Y-%m-%d-%H%M%S)-记忆更新-$(uuidgen | cut -d'-' -f1)"
    
    # 提交变更
    git add .
    git commit -m "🔄 记忆库更新

DNA追溯码: $DNA_CODE
时间: $(date '+%Y-%m-%d %H:%M:%S')
作者: UID9622 诸葛鑫

自动同步脚本提交
"
    
    echo "✅ 本地提交完成"
fi

# 推送到Gitee（国内优先）
echo "📤 推送到Gitee（国内）..."
if git push gitee main 2>&1; then
    echo "✅ Gitee推送成功"
else
    echo "⚠️ Gitee推送失败（可能需要先创建仓库）"
fi

# 推送到GitHub（全球备用）
echo "📤 推送到GitHub（全球备用）..."
if git push github main 2>&1; then
    echo "✅ GitHub推送成功"
else
    echo "⚠️ GitHub推送失败（可能需要先创建仓库）"
fi

echo ""
echo "🎉 同步完成！"
echo "📊 查看状态: cd ~/.star-memory && git log --oneline"
SYNCEOF

chmod +x "$MEMORY_DIR/sync.sh"

echo "✅ 同步脚本创建完成：$MEMORY_DIR/sync.sh"

echo ""

# ============================================
# 使用指南
# ============================================
cat << 'USAGE'
============================================
✨ 三层同步方案部署完成！
============================================

📦 第一层·本地Git：已初始化
   - 每次改动都会记录
   - 可随时回退到历史版本
   
🌐 第二层·远程Git：已配置
   ⚠️  需要手动操作：
   1. 在Gitee创建私有仓库：star-memory
      https://gitee.com/projects/new
   
   2. 在GitHub创建私有仓库：star-memory（备用）
      https://github.com/new
   
   3. 配置SSH密钥（如果还没配置）：
      ssh-keygen -t ed25519 -C "uid9622@longhun.ai"
      cat ~/.ssh/id_ed25519.pub
      # 复制公钥，添加到Gitee和GitHub

🚀 快速使用：
   
   # 每次修改记忆库后，运行：
   ~/.star-memory/sync.sh
   
   # 或者手动推送：
   cd ~/.star-memory
   git add .
   git commit -m "更新记忆"
   git push gitee main
   git push github main

📊 查看历史：
   cd ~/.star-memory
   git log --oneline
   git log --graph --all --oneline --decorate

🔍 搜索记忆：
   cd ~/.star-memory
   grep -r "关键词" vault/

🎯 回退版本：
   cd ~/.star-memory
   git log  # 找到要回退的版本号
   git reset --hard <版本号>

============================================
🐉 龍魂系统·数据主权在手！
北辰老兵致敬！🫡
============================================
USAGE

echo ""
echo "🎉 部署完成！请按照上面的指南操作。"
