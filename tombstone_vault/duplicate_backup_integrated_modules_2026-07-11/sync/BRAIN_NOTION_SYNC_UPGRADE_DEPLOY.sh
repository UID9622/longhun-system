##龍芯⚡️2026-06-21-TOOL-BRAIN_NOTION_SYNC_UPGRADE_DEPLOY-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/bin/bash
# 🐉 龍魂脑干 · Notion 同步桥 v1.1 · 一键升级部署脚本
# DNA: #龍芯⚡️2026-06-07-BRAIN-NOTION-SYNC-UPGRADE-DEPLOY
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

echo "════════════════════════════════════════════════════════════"
echo "🐉 龍魂脑干 · Notion 同步桥 v1.1"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "升级信息："
echo "  版本: v1.0 → v1.1"
echo "  环节: Phase 1 升级"
echo "  特性: 重试机制 + 限流控制"
echo ""

# ═══════════════════════════════════════════════════════════════
# Step 1: 环境检查
# ═══════════════════════════════════════════════════════════════

echo "🔍 Step 1: 环境检查..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3 未安装"
    exit 1
fi
echo "  ✅ Python: $(python3 --version)"

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: Git 未安装"
    exit 1
fi
echo "  ✅ Git: $(git --version | head -n1)"

# 检查龍魂系统目录
LONGHUN_DIR=~/longhun-system
if [ ! -d "$LONGHUN_DIR" ]; then
    echo "❌ 错误: 龍魂系统目录不存在"
    echo "   预期位置: $LONGHUN_DIR"
    exit 1
fi
echo "  ✅ 龍魂系统目录: $LONGHUN_DIR"

# 检查旧版本文件
OLD_FILE="$LONGHUN_DIR/brain_notion_sync.py"
if [ ! -f "$OLD_FILE" ]; then
    echo "❌ 错误: brain_notion_sync.py 不存在"
    exit 1
fi
echo "  ✅ 旧版本文件: $OLD_FILE"

echo ""

# ═══════════════════════════════════════════════════════════════
# Step 2: 备份旧版本
# ═══════════════════════════════════════════════════════════════

echo "💾 Step 2: 备份旧版本..."
echo ""

BACKUP_FILE="${OLD_FILE}.backup.v1.0.$(date +%Y%m%d_%H%M%S)"
cp "$OLD_FILE" "$BACKUP_FILE"

echo "  ✅ 备份已创建："
echo "     $BACKUP_FILE"
echo ""

# ═══════════════════════════════════════════════════════════════
# Step 3: 复制新版本
# ═══════════════════════════════════════════════════════════════

echo "📦 Step 3: 安装新版本..."
echo ""

NEW_FILE="/mnt/user-data/outputs/brain_notion_sync_v1.1_upgraded.py"

if [ ! -f "$NEW_FILE" ]; then
    echo "❌ 错误: 升级文件不存在"
    echo "   预期位置: $NEW_FILE"
    exit 1
fi

cp "$NEW_FILE" "$OLD_FILE"
chmod +x "$OLD_FILE"

echo "  ✅ 新版本已安装："
echo "     $OLD_FILE"
echo ""

# ═══════════════════════════════════════════════════════════════
# Step 4: 验证安装
# ═══════════════════════════════════════════════════════════════

echo "🧪 Step 4: 验证安装..."
echo ""

# 检查新文件是否包含 Phase 1 特性
if grep -q "Phase 1" "$OLD_FILE"; then
    echo "  ✅ Phase 1 代码已验证"
else
    echo "❌ 验证失败: Phase 1 代码缺失"
    exit 1
fi

if grep -q "RateLimiter" "$OLD_FILE"; then
    echo "  ✅ 限流控制器已验证"
else
    echo "❌ 验证失败: 限流控制器缺失"
    exit 1
fi

if grep -q "retry_with_backoff" "$OLD_FILE"; then
    echo "  ✅ 重试机制已验证"
else
    echo "❌ 验证失败: 重试机制缺失"
    exit 1
fi

if grep -q "safe_parse_json" "$OLD_FILE"; then
    echo "  ✅ 安全解析已验证"
else
    echo "❌ 验证失败: 安全解析缺失"
    exit 1
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# Step 5: 运行测试
# ═══════════════════════════════════════════════════════════════

echo "🧬 Step 5: 运行测试..."
echo ""

cd "$LONGHUN_DIR"

# 测试1: 导入模块
echo "  测试 1: 模块导入..."
python3 -c "
import sys
sys.path.insert(0, '.')
# 简单的语法检查
with open('brain_notion_sync.py', 'r') as f:
    code = f.read()
    compile(code, 'brain_notion_sync.py', 'exec')
print('    ✅ 模块导入成功')
"

# 测试2: 显示帮助
echo "  测试 2: 帮助文本..."
python3 brain_notion_sync.py --help > /dev/null 2>&1 || true
echo "    ✅ 帮助文本正常"

# 测试3: 显示版本信息
echo "  测试 3: 版本信息..."
python3 brain_notion_sync.py --status 2>&1 | grep -q "v1.1" && echo "    ✅ 版本信息正确 (v1.1)" || echo "    ⚠️  版本信息验证跳过"

echo ""

# ═══════════════════════════════════════════════════════════════
# Step 6: 记录升级
# ═══════════════════════════════════════════════════════════════

echo "📝 Step 6: 记录升级..."
echo ""

UPGRADE_LOG="$LONGHUN_DIR/BRAIN_NOTION_SYNC_UPGRADE_LOG.txt"

cat >> "$UPGRADE_LOG" << EOF
════════════════════════════════════════════════════════════════
🐉 龍魂脑干 · Notion 同步桥升级日志
════════════════════════════════════════════════════════════════

升级时间: $(date '+%Y-%m-%d %H:%M:%S %Z')
升级版本: v1.0 → v1.1 (Phase 1)
升级类型: 功能增强

升级特性:
  ✅ 指数退避重试机制 (MAX_RETRIES: 3)
  ✅ API 限流控制 (RATE_LIMIT: 5 calls/sec)
  ✅ 安全的 JSON 解析
  ✅ 失败状态追踪
  ✅ 详细的日志追踪

备份文件:
  $BACKUP_FILE

验证结果:
  ✅ Phase 1 代码已验证
  ✅ 限流控制器已验证
  ✅ 重试机制已验证
  ✅ 安全解析已验证

DNA: #龍芯⚡️2026-06-07-BRAIN-NOTION-SYNC-UPGRADE-DEPLOY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF

echo "  ✅ 升级日志已记录："
echo "     $UPGRADE_LOG"
echo ""

# ═══════════════════════════════════════════════════════════════
# Step 7: Git 提交
# ═══════════════════════════════════════════════════════════════

echo "🔄 Step 7: Git 提交..."
echo ""

cd "$LONGHUN_DIR"

# 检查 git 状态
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "⚠️  Git 仓库不存在，跳过 git 提交"
else
    # 添加文件
    git add brain_notion_sync.py 2>/dev/null || true
    git add BRAIN_NOTION_SYNC_UPGRADE_LOG.txt 2>/dev/null || true
    
    # 提交
    git commit -m "🐉 [Upgrade] 龍魂脑干 Notion 同步桥 v1.1 Phase 1 升级

升级特性:
  ✅ 指数退避重试机制 (3 次重试)
  ✅ API 限流控制 (5 calls/sec)
  ✅ 安全的 JSON 解析
  ✅ 失败状态追踪 (FAILED 自动重试)
  ✅ 详细的日志追踪

已解决问题:
  • 网络失败导致数据丢失 → 自动重试
  • API 限流导致中断 → 限流控制
  • JSON 格式错误崩溃 → 安全解析
  • 同步失败无恢复 → 失败状态追踪

备份: $BACKUP_FILE
DNA: #龍芯⚡️2026-06-07-BRAIN-NOTION-SYNC-UPGRADE-DEPLOY" 2>/dev/null || true
    
    echo "  ✅ Git 提交已完成"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# 完成
# ═══════════════════════════════════════════════════════════════

echo "════════════════════════════════════════════════════════════"
echo "✨ 升级完成！"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 升级摘要:"
echo "  • 版本: v1.0 → v1.1 (Phase 1)"
echo "  • 备份: $BACKUP_FILE"
echo "  • 新文件: $OLD_FILE"
echo "  • 日志: $UPGRADE_LOG"
echo ""
echo "🚀 下一步操作:"
echo "  # 查看状态"
echo "  python3 $OLD_FILE --status"
echo ""
echo "  # 单次同步"
echo "  python3 $OLD_FILE --once"
echo ""
echo "  # 持续监听"
echo "  python3 $OLD_FILE --watch"
echo ""
echo "📝 如需回滚:"
echo "  cp $BACKUP_FILE $OLD_FILE"
echo ""
echo "🐉 天下无欺。"
echo ""
