#!/bin/bash

# 龍魂密钥备份脚本 v1.0
# DNA: #龍芯⚡️2026-05-25-BACKUP-KEYS-v1.0
# 用法: ./backup_keys.sh

set -e

echo "═══════════════════════════════════════"
echo "🐉 龍魂密钥备份工具 v1.0"
echo "═══════════════════════════════════════"
echo ""

# 1. 检查 GPG 密钥
echo "📋 检查 GPG 密钥..."
gpg --list-secret-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F 2>/dev/null || {
    echo "❌ 错误：GPG 密钥未找到"
    echo "   密钥 ID: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    echo ""
    echo "💡 解决方案：使用 DNA 签名方案（不依赖 GPG agent）"
    exit 0
}

echo "✅ GPG 密钥找到"
echo ""

# 2. 创建备份目录
BACKUP_DIR=~/longhun-system/keys
mkdir -p "$BACKUP_DIR"
echo "📁 备份目录：$BACKUP_DIR"
echo ""

# 3. 导出私钥（armor 格式·可读）
echo "🔐 导出 GPG 私钥..."
gpg --armor --export-secret-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F > "$BACKUP_DIR/master_key.asc" 2>/dev/null || {
    echo "⚠️  GPG agent 不可用·使用替代方案"
    echo ""
    echo "💡 建议：使用 DNA 签名方案"
    exit 0
}

chmod 600 "$BACKUP_DIR/master_key.asc"
echo "✅ 私钥已导出：master_key.asc"
echo ""

# 4. 用户输入加密密码
echo "🔑 设置加密密码（用于保护备份）"
echo "   请输入 8-32 位密码（包含大小写字母和数字）"
echo -n "密码: "
read -s PASSWORD1
echo ""
echo -n "确认密码: "
read -s PASSWORD2
echo ""

if [ "$PASSWORD1" != "$PASSWORD2" ]; then
    echo "❌ 密码不匹配！"
    rm "$BACKUP_DIR/master_key.asc"
    exit 1
fi

if [ ${#PASSWORD1} -lt 8 ]; then
    echo "❌ 密码太短（最少 8 位）"
    rm "$BACKUP_DIR/master_key.asc"
    exit 1
fi

# 5. 用 OpenSSL 加密
echo "🔒 加密密钥备份..."
openssl enc -aes-256-cbc -salt \
    -in "$BACKUP_DIR/master_key.asc" \
    -out "$BACKUP_DIR/master_key.asc.encrypted" \
    -k "$PASSWORD1" -P > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 加密成功"
    rm "$BACKUP_DIR/master_key.asc"
    ls -lh "$BACKUP_DIR/master_key.asc.encrypted"
    echo ""
else
    echo "❌ 加密失败"
    rm "$BACKUP_DIR/master_key.asc"
    exit 1
fi

# 6. 创建恢复说明
echo "📝 创建恢复说明..."
cat > "$BACKUP_DIR/RECOVERY_GUIDE.md" << 'EOF'
# 龍魂 GPG 密钥恢复指南

## 快速恢复

```bash
# 1. 解密备份
openssl enc -d -aes-256-cbc -in master_key.asc.encrypted \
    -out master_key.asc -k "你的密码"

# 2. 导入 GPG
gpg --import master_key.asc

# 3. 验证
gpg --list-secret-keys
```

## 密钥信息

- **密钥 ID**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- **名字**: 龍芯系统 (UID9622)
- **强度**: RSA 4096 位
- **用途**: Git commit 签名 + 协议签署

## 安全建议

✅ 把加密备份放在物理介质（USB/外置硬盘）
✅ 在保险柜或银行保险箱保管
✅ 定期验证备份可以恢复
❌ 不要把密码保存在文件里
❌ 不要把备份上传到云盘
❌ 不要共享密码给任何人

## 长期使用方案

**推荐用龍魂 DNA 签名方案（不依赖 GPG agent）**：
- 简单可靠
- 跨平台通用
- 离线使用
- 避免 GPG agent 问题

详见：PROTOCOL__LONGHUN-KEY-MANAGEMENT-v1.0.md
EOF

echo "✅ 恢复指南已创建"
echo ""

# 7. 总结
echo "═══════════════════════════════════════"
echo "✅ 备份完成！"
echo "═══════════════════════════════════════"
echo ""
echo "📍 备份位置："
echo "   • 加密密钥: $BACKUP_DIR/master_key.asc.encrypted"
echo "   • 恢复指南: $BACKUP_DIR/RECOVERY_GUIDE.md"
echo ""
echo "🎁 后续建议："
echo "   1️⃣  复制到 USB 盘（推荐加密 USB）"
echo "   2️⃣  保管在保险箱或银行保险箱"
echo "   3️⃣  定期测试恢复流程"
echo "   4️⃣  考虑用龍魂 DNA 签名方案作为主要验证"
echo ""
echo "🔗 相关文档："
echo "   PROTOCOL__LONGHUN-KEY-MANAGEMENT-v1.0.md"
echo ""
